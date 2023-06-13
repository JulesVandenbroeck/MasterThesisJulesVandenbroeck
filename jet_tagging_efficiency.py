import numpy as np
import uproot
import matplotlib.pyplot as plt
from ROOT import TLorentzVector
import os
from itertools import combinations
from Analysis_Info import Analysis
import correctionlib._core as core

class Event:
    def __init__(self,data,i,Info):
        self.leptons = [[Lepton(data,i,e,True,Info) for e in range(data["nElectron"][i])],[Lepton(data,i,mu,False,Info) for mu in range(data["nMuon"][i])]]
        self.nleptons = len(self.leptons)
        self.jets = [Jet(data,i,jet_nr,Info) for jet_nr in range(data["nJet"][i])]
        self.nJets = len(self.jets)
        self.nBJets = 0.
        #self.genWeight =np.float64(data["genWeight"][i])/totalweights
        #self.Pileup_nTrueInt = data["Pileup_nTrueInt"][i]

    def object_selection(self,Info):
        obj_sel_leptons =[]
        obj_sel_jets = []
        for lepton in self.leptons[0]:
                if lepton.electron_object_selection(Info):
                    obj_sel_leptons.append(lepton)

        for lepton in self.leptons[1]:
                if lepton.muon_object_selection(Info):
                    obj_sel_leptons.append(lepton)
        for jet in self.jets:
            if jet.jet_object_selection(obj_sel_leptons,Info):
                obj_sel_jets.append(jet)
                self.nBJets += jet.b_tagged

        self.leptons = obj_sel_leptons
        self.nleptons = len(obj_sel_leptons)
        self.jets = obj_sel_jets
        self.nJets = len(obj_sel_jets)

class Lepton:
    def __init__(self,data,i,nr,is_electron,Info):
        self.is_electron = is_electron
        if is_electron:
            self.pt = np.float64(data["Electron_pt"][i][nr])
            self.eta = np.float64(data["Electron_eta"][i][nr])
            self.phi = data["Electron_phi"][i][nr]
            self.charge = data["Electron_charge"][i][nr]
            self.mass = data["Electron_mass"][i][nr]
            self.deltaEtaSC = data["Electron_deltaEtaSC"][i][nr]
            self.Electron_sieie = data["Electron_sieie"][i][nr]
            self.Electron_hoe = data["Electron_hoe"][i][nr]
            self.Electron_eInvMinusPInv = data["Electron_eInvMinusPInv"][i][nr]
            self.Electron_lostHits = data["Electron_lostHits"][i][nr]
            self.Electron_convVeto = data["Electron_convVeto"][i][nr]
            self.dxy = data["Electron_dxy"][i][nr]
            self.dz = data["Electron_dz"][i][nr]
            self.sip3d = data["Electron_sip3d"][i][nr]
            self.Id = data[Info.ElectronWorkingPoint][i][nr]
            self.pfRelIso03_all = data["Electron_pfRelIso03_all"][i][nr]
            self.miniPFRelIso_all = data["Electron_miniPFRelIso_all"][i][nr]


        else:
            self.pt = np.float64(data["Muon_pt"][i][nr])
            self.eta = np.float64(data["Muon_eta"][i][nr])
            self.phi = data["Muon_phi"][i][nr]
            self.charge = data["Muon_charge"][i][nr]
            self.mass = data["Muon_mass"][i][nr]
            self.phi = data["Muon_phi"][i][nr]
            self.mediumId = data[Info.MuonIDWorkingPoint][i][nr]
            self.pfIsoId = data["Muon_pfIsoId"][i][nr]
            self.dxy = data["Muon_dxy"][i][nr]
            self.dz = data["Muon_dz"][i][nr]
            self.sip3d = data["Muon_sip3d"][i][nr]
            self.pfRelIso03_all = data["Muon_pfRelIso03_all"][i][nr]
            self.miniPFRelIso_all = data["Muon_miniPFRelIso_all"][i][nr]

        lorentz = TLorentzVector()
        lorentz.SetPtEtaPhiM( self.pt , self.eta , self.phi, self.mass)
        self.lorentz = lorentz



    def electron_object_selection(self,Info):
        return (self.pt >Info.ElectronPtCut and np.abs(self.eta)<Info.ElectronEtaCut and not 1.444 < np.abs(self.eta+self.deltaEtaSC)<1.566 and self.Id and self.Electron_convVeto)

    def muon_object_selection(self,Info):
        return (self.pt>Info.MuonPtCut and np.abs(self.eta)<Info.MuonEtaCut and self.mediumId and self.pfIsoId >=Info.MuonISOWorkingPoint)

class Jet:
    def __init__(self,data,i,jet_nr,Info):
        self.pt = np.float64(data["Jet_pt"][i][jet_nr])
        self.eta = np.float64(data["Jet_eta"][i][jet_nr])
        self.phi = np.float64(data["Jet_phi"][i][jet_nr])
        self.Id = data["Jet_jetId"][i][jet_nr]
        self.mass = data["Jet_mass"][i][jet_nr]
        self.hadronFlavour = data["Jet_hadronFlavour"][i][jet_nr]

        if data["Jet_btagDeepB"][i][jet_nr] >Info.deepCSV_WorkingPoint_number:
            self.b_tagged = 1
        else:
            self.b_tagged = 0

        lorentz = TLorentzVector()
        lorentz.SetPtEtaPhiM( self.pt , self.eta , self.phi, self.mass)
        self.lorentz = lorentz

    def jet_object_selection(self,selected_leptons,Info):
        if self.phi < -3.0543261909902775:
            phi = -3.1
        elif self.phi > 3.0543261909902775:
            phi = 3.1
        else:
            phi = self.phi

        if (self.pt >Info.JetPtCut and np.abs(self.eta) <Info.JetEtaCut and self.Id >=Info.JetIDWorkingPoint and Info.evaluators["jetvetomap"][Info.jetvetomapSample].evaluate("jetvetomap",self.eta,phi) ==0.0):

            for lepton in selected_leptons:
                dR = np.sqrt((self.eta-lepton.eta)**2+(self.phi-lepton.phi)**2)
                if dR< Info.JetDRCut:
                    return False
            return True
        else:
            return False



def main(file,savefolder,labelnumber,year,nJob):
    Info = Analysis(year)
    pt_bins = np.array([30.,40.,60.,100.,300.,1000.])
    eta_bins = np.array([0.0,0.8,1.6,2.5])

    LeptonKeys =  [  "nElectron",    "Electron_pt",      "Electron_eta", "Electron_phi", "Electron_deltaEtaSC",  "Electron_charge",  "Electron_mass", Info.ElectronWorkingPoint,
                        "Electron_sieie",   "Electron_hoe", "Electron_pfRelIso03_all", "Electron_eInvMinusPInv",    "Electron_lostHits","Electron_convVeto","Electron_dxy","Electron_dz","Electron_sip3d","Electron_miniPFRelIso_all",
                        "nMuon",        "Muon_pt",          "Muon_eta",     "Muon_phi",Info.MuonIDWorkingPoint,         "Muon_pfIsoId",         "Muon_charge",      "Muon_mass","Muon_dxy","Muon_dz","Muon_sip3d","Muon_pfRelIso03_all", "Muon_miniPFRelIso_all"]
    JetKeys =     ["nJet",         "Jet_pt",           "Jet_eta",      "Jet_phi",      "Jet_jetId",            "Jet_btagDeepB", "Jet_mass", 'MET_pt', "MET_phi"]
    TriggerKeys = list(Info.lepton_triggers) + list(Info.reference_triggers) + ["nTrigObj","TrigObj_id","TrigObj_eta","TrigObj_pt","TrigObj_phi"]
    if Info.year == 2018:
        MonteCarloKeys =   ["Jet_hadronFlavour", "Pileup_nTrueInt","fixedGridRhoFastjetAll", "genWeight"]
    elif Info.year == 2022:
        MonteCarloKeys =   ["Jet_hadronFlavour", "Pileup_nTrueInt","Rho_fixedGridRhoFastjetAll", "genWeight"]

    important_keys = LeptonKeys + JetKeys + TriggerKeys + MonteCarloKeys



    total_Bjets = np.zeros((len(pt_bins)-1,len(eta_bins)-1))
    total_Btags = np.zeros((len(pt_bins)-1,len(eta_bins)-1))
    total_Cjets =np.zeros((len(pt_bins)-1,len(eta_bins)-1))
    total_Ctags = np.zeros((len(pt_bins)-1,len(eta_bins)-1))
    total_UDSGjets =np.zeros((len(pt_bins)-1,len(eta_bins)-1))
    total_UDSGtags = np.zeros((len(pt_bins)-1,len(eta_bins)-1))



    for batch in uproot.iterate(file,important_keys,step_size=100000,library = 'np'):

        jet_pt = []
        jet_eta = []
        jet_btag = []
        jet_hadron_flavour = []

        nbatch = len(batch['nElectron'])
        print("number of events in batch: {}".format(nbatch))
        for i in range(nbatch):
            event = Event(batch,i,Info)
            event.object_selection(Info)
            for jet in event.jets:
                pt_ind = np.minimum(np.digitize(jet.pt,pt_bins),len(pt_bins)-1)-1
                eta_ind = np.digitize(np.abs(jet.eta),eta_bins)-1
                if jet.hadronFlavour == 5:
                    total_Bjets[pt_ind,eta_ind] += 1.
                    total_Btags[pt_ind,eta_ind] += jet.b_tagged

                elif jet.hadronFlavour == 4:
                    total_Cjets[pt_ind,eta_ind] += 1.
                    total_Ctags[pt_ind,eta_ind] += jet.b_tagged

                else:
                    total_UDSGjets[pt_ind,eta_ind] += 1.
                    total_UDSGtags[pt_ind,eta_ind] += jet.b_tagged

            #print("B-tagging efficiency of other jets: {}".format(total_Btags/total_UDSGtags))
    print(total_Btags)
    print(total_Bjets)
    with uproot.recreate(savefolder+"/hist_{}_{}.root".format(labelnumber,nJob)) as file:

        file["Btags"] = total_Btags,pt_bins,eta_bins
        file["Bjets"] = total_Bjets,pt_bins,eta_bins

        file["Ctags"] = total_Ctags,pt_bins,eta_bins
        file["Cjets"] = total_Bjets,pt_bins,eta_bins

        file["UDSGtags"] = total_UDSGtags,pt_bins,eta_bins
        file["UDSGjets"] = total_UDSGjets,pt_bins,eta_bins

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', nargs=1, required = True)
    parser.add_argument('-y', '--year', nargs=1,type = int, required = True)
    parser.add_argument('-o', '--savefolder', nargs=1,required=True)
    parser.add_argument('-l', '--labelnumber', nargs=1,type = int, required=True)
    parser.add_argument('-j', '--nJob', nargs=1, type = int,required=True)
    args = parser.parse_args()
    files = args.files[0]
    year = args.year[0]
    savefolder = args.savefolder[0]
    labelnumber = args.labelnumber[0]
    nJob = args.nJob[0]
    file = files.split(',')[nJob]
    main(file,savefolder,labelnumber,year,nJob)

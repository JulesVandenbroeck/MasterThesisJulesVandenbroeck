import numpy as np
import uproot
import matplotlib.pyplot as plt
from ROOT import TLorentzVector
import os
from itertools import combinations
from Analysis_Info import Analysis
import correctionlib._core as core
from utils import Golden_JSON2018D, Golden_JSON2022EFG, DoubleCounting, Binning


class Event:
    def __init__(self,data,i,is_mc,Info,JEC_JER):
        self.leptons = [[Lepton(data,i,e,True,Info) for e in range(data["nElectron"][i])],[Lepton(data,i,mu,False,Info) for mu in range(data["nMuon"][i])]]
        self.nleptons = len(self.leptons)
        self.nElectron = 0
        self.nMuon = 0
        self.jets = [Jet(data,i,jet_nr,is_mc,Info,JEC_JER) for jet_nr in range(data["nJet"][i])]
        self.raw_HT = np.sum([jet.pt for jet in self.jets])
        self.nJets = len(self.jets)
        self.MET_pt = np.float64(data["MET_pt"][i])
        self.MET_phi = np.float64(data["MET_phi"][i])
        self.index = i
        self.mll = 0.
        self.min_mll = 0.
        self.mlll = 0.
        self.MT = 0.
        self.Zpt = 0.

        if self.nJets !=0:
            self.leading_jet = self.jets[np.argmax([jet.pt for jet in self.jets])]
        self.nBJets = 0.

        if is_mc:
            self.Pileup_nTrueInt = np.float64(data["Pileup_nTrueInt"][i])
        else:
            self.event = data["event"][i]
            self.run =  data["run"][i]
            self.luminosityBlock = data["luminosityBlock"][i]

        self.Pass_Lepton_Trigger = int(any([data[trigger][i] for trigger in Info.lepton_triggers]))
        self.Pass_Reference_Trigger =   int(any([data[trigger][i] for trigger in Info.reference_triggers]))




    def object_selection(self,Info):
        obj_sel_leptons =[]
        obj_sel_jets = []
        for lepton in self.leptons[0]:
                if lepton.electron_object_selection(Info):
                    obj_sel_leptons.append(lepton)
                    self.nElectron+=1

        for lepton in self.leptons[1]:
                if lepton.muon_object_selection(Info):
                    obj_sel_leptons.append(lepton)
                    self.nMuon+=1

        for jet in self.jets:
            if jet.jet_object_selection(obj_sel_leptons,Info):
                obj_sel_jets.append(jet)
                self.nBJets += jet.b_tagged

        self.leptons = obj_sel_leptons
        self.nleptons = len(obj_sel_leptons)
        self.jets = obj_sel_jets
        self.nJets = len(obj_sel_jets)



    def event_selection(self):
        if self.nleptons ==3:

            sorted_leptons = np.argsort([self.leptons[i].pt for i in range(3)] )
            leading_lepton = self.leptons[sorted_leptons[2]]
            subleading_lepton = self.leptons[sorted_leptons[1]]
            subsubleading_lepton = self.leptons[sorted_leptons[0]]
            leptons = [leading_lepton,subleading_lepton,subsubleading_lepton]

            m_ll = np.array([(leading_lepton.lorentz + subleading_lepton.lorentz).M(),(leading_lepton.lorentz + subsubleading_lepton.lorentz).M(),(subleading_lepton.lorentz + subsubleading_lepton.lorentz).M()])
            self.min_mll = np.min(m_ll)
            self.mlll = (leading_lepton.lorentz + subleading_lepton.lorentz + subsubleading_lepton.lorentz).M()
            delta_m = np.abs(m_ll-91.1876)
            arg = np.argmin(delta_m)

            Z_is_reconstructed = False
            if delta_m[arg] < 10:
                self.mll = m_ll[arg]

                if (arg == 0 and leading_lepton.charge != subleading_lepton.charge and leading_lepton.is_electron == subleading_lepton.is_electron):
                    self.MT = np.sqrt(2*self.MET_pt*subsubleading_lepton.pt*(1-np.cos(self.MET_phi-subsubleading_lepton.phi)))
                    self.Zpt = (leading_lepton.lorentz + subleading_lepton.lorentz).Pt()
                    Z_is_reconstructed = True
                elif (arg ==1 and leading_lepton.charge != subsubleading_lepton.charge and leading_lepton.is_electron == subsubleading_lepton.is_electron):
                    self.MT = np.sqrt(2*self.MET_pt*subleading_lepton.pt*(1-np.cos(self.MET_phi-subleading_lepton.phi)))
                    self.Zpt = (leading_lepton.lorentz + subsubleading_lepton.lorentz).Pt()
                    Z_is_reconstructed = True
                elif (arg ==2 and subleading_lepton.charge != subsubleading_lepton.charge and subleading_lepton.is_electron == subsubleading_lepton.is_electron):
                    self.MT = np.sqrt(2*self.MET_pt*leading_lepton.pt*(1-np.cos(self.MET_phi-leading_lepton.phi)))
                    self.Zpt = (subleading_lepton.lorentz + subsubleading_lepton.lorentz).Pt()
                    Z_is_reconstructed = True

            return (leading_lepton.pt>40 and subleading_lepton.pt>20 and subsubleading_lepton.pt>10 and self.nJets >=1 and Z_is_reconstructed)
        else:
            return False

    def save(self,batch,memory,is_mc,dataset,Info):

        sorted_leptons = np.argsort([self.leptons[i].pt for i in range(3)])
        for i,order in enumerate(("subsubleading","subleading","leading")):
            memory["{}_lepton_pt".format(order)].append(self.leptons[sorted_leptons[i]].pt)
            memory["{}_lepton_eta".format(order)].append(self.leptons[sorted_leptons[i]].eta)
            memory["{}_lepton_phi".format(order)].append(self.leptons[sorted_leptons[i]].phi)
            memory["{}_lepton_charge".format(order)].append(self.leptons[sorted_leptons[i]].charge)
            memory["{}_lepton_is_electron".format(order)].append(self.leptons[sorted_leptons[i]].is_electron)

            memory["{}_lepton_miniPFRelIso_all".format(order)].append(self.leptons[sorted_leptons[i]].miniPFRelIso_all)
            memory["{}_lepton_pfRelIso03_all".format(order)].append(self.leptons[sorted_leptons[i]].pfRelIso03_all)


        memory["max_dxy".format(order)].append(np.amax([np.abs(lepton.dxy) for lepton in self.leptons]))
        memory["max_dz".format(order)].append(np.amax([np.abs(lepton.dz) for lepton in self.leptons]))
        memory["max_sip3d".format(order)].append(np.amax([np.abs(lepton.sip3d) for lepton in self.leptons]))

        leading_lepton = self.leptons[sorted_leptons[2]]
        subleading_lepton = self.leptons[sorted_leptons[1]]
        subsubleading_lepton = self.leptons[sorted_leptons[0]]

        memory["mll"].append(self.mll)
        memory["mlll"].append(self.mlll)
        memory["Zpt"].append(self.Zpt)
        memory["min_mll"].append(self.min_mll)
        memory["MT"].append(self.MT)
        memory["MET_pt"].append(self.MET_pt)
        memory["nJets"].append(self.nJets)
        memory["leading_jet_pt"].append(self.leading_jet.pt)
        memory["leading_jet_eta"].append(self.leading_jet.eta)
        memory["leading_jet_phi"].append(self.leading_jet.phi)
        memory["nBJets"].append(self.nBJets)
        memory["raw_HT"].append(self.raw_HT)
        memory["Binning"].append(Binning(self.leptons[sorted_leptons[2]].pt,self.nJets,self.nBJets))
        memory["nElectron"].append(self.nElectron)
        memory["nMuon"].append(self.nMuon)
        memory["ZisReconstructed"].append(int(self.Zpt == 0))

        memory["Pass_Lepton_Trigger"].append(self.Pass_Lepton_Trigger)
        memory["Pass_Reference_Trigger"].append(self.Pass_Reference_Trigger)

        if is_mc:
            for Weight in Info.Weights.keys():
                if Weight == "genWeight":
                    memory[Weight].append(batch[Weight][i])
                elif Weight == "PSWeight":
                    memory["PSWeightISRup"].append(batch[Weight][i][0]*batch["genWeight"][i])
                    memory["PSWeightFSRup"].append(batch[Weight][i][1]*batch["genWeight"][i])

                    memory["PSWeightISRdown"].append(batch[Weight][i][2]*batch["genWeight"][i])
                    memory["PSWeightFSRdown"].append(batch[Weight][i][3]*batch["genWeight"][i])
                elif dataset not in Info.WeightExclusion:
                    for WeightBin in range(Info.Weights[Weight]["values"]):
                        memory[Weight+"{}".format(WeightBin)].append(batch[Weight][i][WeightBin]*batch["genWeight"][i])

            memory["Pileup_nTrueInt"].append(self.Pileup_nTrueInt)

            Systematics = {}
            for Systematic in Info.Systematics:

                Systematics[Systematic] = {"nom": 1.,"up": 1.,"down": 1.}
            evaluators = Info.evaluators

            for lepton in self.leptons:

                if lepton.is_electron:
                    if lepton.pt < 20:
                        reco = "RecoBelow20"
                    else:
                        reco = "RecoAbove20"

                    Systematics["Electron_SF"]["nom"] *= evaluators["Electron_SF"]["UL-Electron-ID-SF"].evaluate("2018","sf",Info.ElectronIDWorkingPoint,lepton.eta, lepton.pt)*evaluators["Electron_SF"]["UL-Electron-ID-SF"].evaluate("2018","sf",reco,lepton.eta, lepton.pt)
                    Systematics["Electron_SF"]["up"] *= evaluators["Electron_SF"]["UL-Electron-ID-SF"].evaluate("2018","sfup",Info.ElectronIDWorkingPoint,lepton.eta, lepton.pt)*evaluators["Electron_SF"]["UL-Electron-ID-SF"].evaluate("2018","sfup",reco,lepton.eta, lepton.pt)
                    Systematics["Electron_SF"]["down"] *= evaluators["Electron_SF"]["UL-Electron-ID-SF"].evaluate("2018","sfdown",Info.ElectronIDWorkingPoint,lepton.eta, lepton.pt)*evaluators["Electron_SF"]["UL-Electron-ID-SF"].evaluate("2018","sfdown",reco,lepton.eta, lepton.pt)

                else:

                    #muon  Scale Factors
                    for Muon_scalefactor_name in Info.MuonSFnames:
                        Systematics["Muon_SF"]["nom"] *= evaluators["Muon_SF"][Muon_scalefactor_name].evaluate("2018_UL",np.abs(lepton.eta), np.maximum(lepton.pt,15.0),"sf")
                        Systematics["Muon_SF"]["up"] *= evaluators["Muon_SF"][Muon_scalefactor_name].evaluate("2018_UL",np.abs(lepton.eta), np.maximum(lepton.pt,15.0),"systup")
                        Systematics["Muon_SF"]["down"] *= evaluators["Muon_SF"][Muon_scalefactor_name].evaluate("2018_UL",np.abs(lepton.eta), np.maximum(lepton.pt,15.0),"systdown")

            for jet in self.jets:

                #if jet.pt <= 50:
                #    Systematics["PileUpId_SF"]["nom"] *= evaluators["PileUpId_SF"]["PUJetID_eff"].evaluate(np.abs(jet.eta), jet.pt,"nom", "T")
                #    Systematics["PileUpId_SF"]["up"] *= evaluators["PileUpId_SF"]["PUJetID_eff"].evaluate(np.abs(jet.eta), jet.pt,"up", "T")
                #    Systematics["PileUpId_SF"]["down"] *= evaluators["PileUpId_SF"]["PUJetID_eff"].evaluate(np.abs(jet.eta), jet.pt,"down", "T")

                if jet.hadronFlavour == 0:
                    BtaggingSyst = "BtaggingIncl_SF"
                    SF = evaluators["Btagging_SF"]["deepCSV_incl"].evaluate("central",Info.deepCSV_WorkingPoint,0,np.abs(jet.eta),jet.pt)
                    SF_up = evaluators["Btagging_SF"]["deepCSV_incl"].evaluate("up",Info.deepCSV_WorkingPoint,0,np.abs(jet.eta),jet.pt)
                    SF_down = evaluators["Btagging_SF"]["deepCSV_incl"].evaluate("down",Info.deepCSV_WorkingPoint,0,np.abs(jet.eta),jet.pt)

                else:
                    BtaggingSyst = "BtaggingComb_SF"
                    SF= evaluators["Btagging_SF"]["deepCSV_comb"].evaluate("central",Info.deepCSV_WorkingPoint,jet.hadronFlavour,np.abs(jet.eta),jet.pt)
                    SF_up= evaluators["Btagging_SF"]["deepCSV_comb"].evaluate("up",Info.deepCSV_WorkingPoint,jet.hadronFlavour,np.abs(jet.eta),jet.pt)
                    SF_down= evaluators["Btagging_SF"]["deepCSV_comb"].evaluate("down",Info.deepCSV_WorkingPoint,jet.hadronFlavour,np.abs(jet.eta),jet.pt)

                #symmetrizing the jet tagging scale factors
                if jet.b_tagged:
                    Systematics[BtaggingSyst]["nom"] *= SF
                    Systematics[BtaggingSyst]["up"] *= SF_up
                    Systematics[BtaggingSyst]["down"] *= SF_down
                else:
                    eff = evaluators["Btagging_Eff"]["Btagging_Efficiency"].evaluate("central",Info.deepCSV_WorkingPoint,jet.hadronFlavour,np.abs(jet.eta),np.minimum(jet.pt,301.))
                    Systematics[BtaggingSyst]["nom"]*=(1-SF*eff)/(1-eff)
                    Systematics[BtaggingSyst]["up"] *= (1-SF_down*eff)/(1-eff)
                    Systematics[BtaggingSyst]["down"]*= (1-SF_up*eff)/(1-eff)

            #TRIGGER SF
            Systematics["Trigger_SF"]["nom"] *= evaluators["Trigger_SF"]["Trigger_Scalefactors"].evaluate("central","SF",np.abs(leading_lepton.eta), np.minimum(leading_lepton.pt,239.9))
            Systematics["Trigger_SF"]["up"] *= evaluators["Trigger_SF"]["Trigger_Scalefactors"].evaluate("up","SF",np.abs(leading_lepton.eta), np.minimum(leading_lepton.pt,239.9))
            Systematics["Trigger_SF"]["down"] *= evaluators["Trigger_SF"]["Trigger_Scalefactors"].evaluate("down","SF",np.abs(leading_lepton.eta), np.minimum(leading_lepton.pt,239.9))

            Systematics["PileUp_SF"]["nom"] *= evaluators["PileUp_SF"]["Collisions18D_UltraLegacy_goldenJSON"].evaluate(self.Pileup_nTrueInt, "nominal")
            Systematics["PileUp_SF"]["up"] *= evaluators["PileUp_SF"]["Collisions18D_UltraLegacy_goldenJSON"].evaluate(self.Pileup_nTrueInt, "up")
            Systematics["PileUp_SF"]["down"] *= evaluators["PileUp_SF"]["Collisions18D_UltraLegacy_goldenJSON"].evaluate(self.Pileup_nTrueInt, "down")


            for Systematic in Systematics.keys():
                memory[Systematic].append(Systematics[Systematic]["nom"])
                memory[Systematic+"up"].append(Systematics[Systematic]["up"])
                memory[Systematic+"down"].append(Systematics[Systematic]["down"])

            memory["Before_Trigger_SF"].append(Systematics["Muon_SF"]["nom"]*Systematics["Electron_SF"]["nom"])

        else:
            memory["event"].append(self.event)
            memory["run"].append(self.run)
            memory["luminosityBlock"].append(self.luminosityBlock)

        return memory


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
    def __init__(self,data,i,jet_nr,is_mc,Info,JEC_JER):
        self.pt = np.float64(data["Jet_pt"][i][jet_nr])
        self.eta = np.float64(data["Jet_eta"][i][jet_nr])
        self.phi = np.float64(data["Jet_phi"][i][jet_nr])
        self.Id = data["Jet_jetId"][i][jet_nr]
        self.mass = data["Jet_mass"][i][jet_nr]
        #self.puId = data["Jet_puId"][i][jet_nr]

        if is_mc:
            self.hadronFlavour = data["Jet_hadronFlavour"][i][jet_nr]

        if data["Jet_btagDeepB"][i][jet_nr] >Info.deepCSV_WorkingPoint_number:
            self.b_tagged = True
        else:
            self.b_tagged = False



        if is_mc:
            if Info.year == 2018:
                pt_Res = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_PtResolution_AK4PFchs"].evaluate(self.eta,self.pt,np.float64(data["fixedGridRhoFastjetAll"][i]))
            elif Info.year == 2022:
                pt_Res = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_PtResolution_AK4PFchs"].evaluate(self.eta,self.pt,np.float64(data["Rho_fixedGridRhoFastjetAll"][i]))
            self.Trigger_Obj = False

            if JEC_JER == "JECup":
                self.pt = (1.+Info.evaluators["jet_jerc"]["Summer19UL18_V5_MC_Total_AK4PFchs"].evaluate(self.eta,self.pt))*self.pt
                sJER = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs"].evaluate(self.eta,"nom")
            elif JEC_JER == "JECdown":
                self.pt = (1.-Info.evaluators["jet_jerc"]["Summer19UL18_V5_MC_Total_AK4PFchs"].evaluate(self.eta,self.pt))*self.pt
                sJER = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs"].evaluate(self.eta,"nom")
            elif JEC_JER == "JERup":
                sJER = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs"].evaluate(self.eta,"up")
            elif JEC_JER == "JERdown":
                sJER = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs"].evaluate(self.eta,"down")
            else:
                sJER = Info.evaluators["jet_jerc"]["Summer19UL18_JRV2_MC_ScaleFactor_AK4PFchs"].evaluate(self.eta,"nom")


            self.Trigger_Obj = False
            if data["nTrigObj"][i] >0:
                for j in range(data["nTrigObj"][i]):
                    if data["TrigObj_id"][i][j] ==1 and not self.Trigger_Obj:
                        TrigObj_dR = np.sqrt(np.square(data["TrigObj_eta"][i][j]-self.eta)+np.square(data["TrigObj_phi"][i][j]-self.phi))
                        TrigObj_dpt = np.abs(data["TrigObj_pt"][i][j]-self.pt)
                        if ((TrigObj_dR <=0.2) & (TrigObj_dpt <=3.*pt_Res*self.pt)):
                            self.Trigger_Obj_pt = data["TrigObj_pt"][i][j]
                            self.Trigger_Obj = True


            if self.Trigger_Obj:
                cJER = np.maximum(1 + (sJER-1)*(self.pt-self.Trigger_Obj_pt)/self.pt,0.)
            else:
                cJER = 1+ np.random.normal(0., pt_Res)*np.sqrt(np.maximum(sJER*sJER-1.,0.))

            lorentz = TLorentzVector()
            lorentz.SetPtEtaPhiM( self.pt , self.eta , self.phi, self.mass)
            self.lorentz = lorentz*cJER
            self.pt =  self.pt*cJER
        else:
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



        if (self.pt >Info.JetPtCut and np.abs(self.eta) <Info.JetEtaCut and self.Id >=Info.JetIDWorkingPoint
                and Info.evaluators["jetvetomap"][Info.jetvetomapSample].evaluate("jetvetomap",self.eta,phi) ==0.0
                #and self.puId == 7
                ):

            for lepton in selected_leptons:
                dR = np.sqrt((self.eta-lepton.eta)**2+(self.phi-lepton.phi)**2)
                if dR< Info.JetDRCut:
                    return False
            return True
        else:
            return False



def main(data_file_name,dataset,nJob,is_mc,outputfolder,year):
    #Keys nessecary for event selection and write out
    Info = Analysis(year)

    LeptonKeys =  [  "nElectron",    "Electron_pt",      "Electron_eta", "Electron_phi", "Electron_deltaEtaSC",  "Electron_charge",  "Electron_mass", Info.ElectronWorkingPoint,
                        "Electron_sieie",   "Electron_hoe", "Electron_pfRelIso03_all", "Electron_eInvMinusPInv",    "Electron_lostHits","Electron_convVeto","Electron_dxy","Electron_dz","Electron_sip3d","Electron_miniPFRelIso_all",
                        "nMuon",        "Muon_pt",          "Muon_eta",     "Muon_phi",Info.MuonIDWorkingPoint,         "Muon_pfIsoId",         "Muon_charge",      "Muon_mass","Muon_dxy","Muon_dz","Muon_sip3d","Muon_pfRelIso03_all", "Muon_miniPFRelIso_all"]
    JetKeys =     ["nJet",         "Jet_pt",           "Jet_eta",      "Jet_phi",      "Jet_jetId",            "Jet_btagDeepB", "Jet_mass", 'MET_pt', "MET_phi"]
    TriggerKeys = list(Info.lepton_triggers) + list(Info.reference_triggers) + ["nTrigObj","TrigObj_id","TrigObj_eta","TrigObj_pt","TrigObj_phi"]
    MonteCarloKeys =   ["Jet_hadronFlavour", "Pileup_nTrueInt","fixedGridRhoFastjetAll", "genWeight","PSWeight"]
    if dataset not in Info.WeightExclusion:
            MonteCarloKeys = MonteCarloKeys + ["LHEScaleWeight","nLHEScaleWeight","LHEPdfWeight","nLHEPdfWeight"]
    DataKeys = [ "luminosityBlock","run","event"]
    #select important keys of input root file
    if is_mc:
        important_keys = LeptonKeys + JetKeys + TriggerKeys + MonteCarloKeys
    else:
        important_keys = LeptonKeys + JetKeys + TriggerKeys + DataKeys

    #CREATE OUTPUT FILES
    with uproot.recreate(outputfolder+"/file{}.root".format(nJob)) as root_file:

        #Create root file output
        if is_mc:
            if Info.year == 2018:
                Trees = ("nom","JECup","JECdown","JERup","JERdown")
            elif Info.year == 2022:
                Trees = ("nom",)
            Tree = Info.OutputMC
            AdditionalOutputs = {}
            CumulativeWeights = {}
            with uproot.open(data_file_name+":Runs") as WeightFile:

                for Weight in Info.Weights.keys():
                    if Weight == "genWeight":
                        AdditionalOutputs[Weight] = np.float64
                        root_file["Weights/"+Weight] = np.array([WeightFile["genEventSumw"].array(library = "np")[0]]),np.array([0.,1.])
                    elif Weight == "PSWeight":
                        for temp in ("PSWeightISRup","PSWeightFSRup","PSWeightISRdown","PSWeightFSRdown"):
                            CumulativeWeights[temp] = 0.
                            AdditionalOutputs[temp] = np.float64
                    elif dataset not in Info.WeightExclusion:
                        Info.Weights[Weight]["values"] = WeightFile["n{}".format(Info.Weights[Weight]["SumName"])].array(library = "np")[0]
                        for WeightBin in range(Info.Weights[Weight]["values"]):
                            root_file["Weights/"+Weight+"{}".format(WeightBin)] = np.array([WeightFile[Info.Weights[Weight]["SumName"]].array(library = "np")[0][WeightBin]*WeightFile["genEventSumw"].array(library = "np")[0]]),np.array([0.,1.])
                            AdditionalOutputs[Weight+"{}".format(WeightBin)] = np.float64

            for Systematic in Info.Systematics:
                AdditionalOutputs[Systematic] = np.float64
                AdditionalOutputs[Systematic+"up"] = np.float64
                AdditionalOutputs[Systematic+"down"] = np.float64

            Tree.update(AdditionalOutputs)
        else:
            Trees = ("nom",)
            Tree = Info.OutputDATA

        for JEC_JER in Trees:
            print("Start Event Selection of Tree {}..........".format(JEC_JER))
            Tree_name = "Events_{}".format(JEC_JER)
            root_file.mktree(Tree_name, Tree)

            memory = {}
            for variable in Tree:
                memory[variable] = []
            for batch in uproot.iterate(data_file_name+":Events",important_keys,step_size=100000,library = 'np'):
                nbatch = len(batch['nElectron'])
                print("number of events in batch: {}".format(nbatch))
                for i in range(nbatch):
                    #CHECK DOUBLE COUNTING
                    if not is_mc:

                        if year == 2018:
                            DataCheck = (DoubleCounting(batch,i,dataset,year) and Golden_JSON2018D(batch['run'][i],batch['luminosityBlock'][i]))
                        elif year == 2022:
                            DataCheck = (DoubleCounting(batch,i,dataset,year) and Golden_JSON2022EFG(batch['run'][i],batch['luminosityBlock'][i]))

                    else:
                        DataCheck = DoubleCounting(batch,i,dataset,year)

                        if JEC_JER =="nom":
                            CumulativeWeights["PSWeightISRup"] += batch["PSWeight"][i][0]*batch["genWeight"][i]
                            CumulativeWeights["PSWeightFSRup"] += batch["PSWeight"][i][1]*batch["genWeight"][i]
                            CumulativeWeights["PSWeightISRdown"] += batch["PSWeight"][i][2]*batch["genWeight"][i]
                            CumulativeWeights["PSWeightFSRdown"] += batch["PSWeight"][i][3]*batch["genWeight"][i]

                    if DataCheck:
                        event = Event(batch,i,is_mc,Info,JEC_JER)
                        event.object_selection(Info)
                        if event.event_selection():
                            memory = event.save(batch,memory,is_mc,dataset,Info)

                print("saved events: {}".format(len(memory['nElectron'])))
                print()
            root_file[Tree_name].extend(memory)


        if is_mc:
            for name in CumulativeWeights.keys():
                root_file["Weights/"+name] = np.array([CumulativeWeights[name]]),np.array([0.,1.])

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--files', nargs=1, required = True)
    parser.add_argument('-r', '--dataset', nargs=1, required=True)
    parser.add_argument('-m', '--is_mc', nargs=1, required=True)
    parser.add_argument('-o', '--outputfolder', nargs=1,required=True)
    parser.add_argument('-y', '--year', nargs=1,type = int,required=True)
    parser.add_argument('-j', '--nJob', nargs=1, type = int,required=True)
    args = parser.parse_args()
    files = args.files[0]
    dataset = args.dataset[0]
    outputfolder = args.outputfolder[0]
    nJob = args.nJob[0]
    year = args.year[0]
    is_mc = args.is_mc[0]
    if is_mc == "True":
        is_mc = True
    else:
        is_mc = False
    print(dataset)
    main(files.split(',')[nJob],dataset,nJob,is_mc,outputfolder,year)

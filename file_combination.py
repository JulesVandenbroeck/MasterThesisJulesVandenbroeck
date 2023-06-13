#!/usr/bin/env python3

import numpy as np
import uproot
import subprocess
import os
from Analysis_Info import Analysis
import ROOT
from Analysis_Info import Analysis
from ROOT import RDataFrame, TH1, TH1D
import uproot
ROOT.gROOT.SetBatch(True)

# Declare the range of the histogram for each variable
#
# Each entry in the dictionary contains of the variable name as key and a tuple
# specifying the histogram layout as value. The tuple sets the number of bins,
# the lower edge and the upper edge of the histogram.
default_nbins = 20
variables = ("Binning","leading_lepton_pt","subleading_lepton_pt","subsubleading_lepton_pt","leading_lepton_eta","leading_lepton_phi","nJets","nBJets","raw_HT","nElectron","leading_jet_pt","leading_jet_eta","mll","min_mll","mlll","MT","MET_pt","max_sip3d","nMuon","Zpt")
ranges = {
        "TTZ_SR": {
            "Binning": (12,-0.5,11.5),
            "leading_lepton_pt": (default_nbins, 40, 250),
            "subleading_lepton_pt": (default_nbins, 20, 200),
            "subsubleading_lepton_pt": (default_nbins, 10, 100),
            "leading_lepton_eta": (default_nbins, -2.4,2.4),
            "nJets": (3, 2.5, 5.5),
            "nBJets": (2, 0.5, 2.5),
            "raw_HT": (default_nbins, 300, 1500),
            "leading_jet_pt": (default_nbins, 30, 500),
            "nElectron": (4,-0.5,3.5) ,
            "mll": (default_nbins, 91.1876-10, 91.1876+10),
            "min_mll": (default_nbins,12,80),
            "Zpt": (default_nbins,0,500),
            "mlll": (default_nbins, 50, 400),
            "MT": (default_nbins,0,200),
            "MET_pt":(default_nbins,0,200),
            "nMuon":(1,-1,5),
            "max_sip3d": (20,0,10)
        },

        "CR_WZ": {
            "WZ_Binning": (6,-0.5,5.5),
            "leading_lepton_pt": (default_nbins, 50, 250),
            "subleading_lepton_pt": (default_nbins, 20, 200),
            "subsubleading_lepton_pt": (default_nbins, 20, 100),
            "leading_lepton_eta": (default_nbins, -2.4,2.4),
            "nJets": (4, -0.5, 3.5),
            "nBJets": (2, -0.5, 1.5),
            "raw_HT": (default_nbins, 0, 1000),
            "leading_jet_pt": (default_nbins, 30, 500),
            "nElectron": (4,-0.5,3.5) ,
            "mll": (default_nbins, 91.1876-10, 91.1876+10),
            "min_mll": (default_nbins,0,80),
            "mlll": (default_nbins, 50, 400),
            "Zpt": (default_nbins,0,500),
            "MT": (default_nbins,0,200),
            "MET_pt":(default_nbins,0,200),
            "nMuon":(1,-1,5),
        },


        "No_cuts": {    "leading_lepton_pt": (default_nbins, 50, 250),},
        "No_Jetcut": {"nJets": (5, 0.5, 5.5),
                        "nMuon":(1,-1,5),},
        "No_BJetcut": {"nJets": (5, 0.5, 5.5),
                       "nBJets": (3, -0.5, 2.5),
                       "nMuon":(1,-1,5),},
        "No_HTcut": {"nBJets": (3, -0.5, 2.5),
                     "raw_HT": (20, 0, 1000),
                     "nMuon":(1,-1,5),},
        "No_minllcut": {"raw_HT": (20, 0, 1000),
                        "min_mll": (20,0,100),
                        "nMuon":(1,-1,5),},
        "No_max_sip3dcut": {"max_sip3d": (20,0,10),
                            "nMuon":(1,-1,5),}
}


CrossSectionVariation = {
                    "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8": 1.082,
                    "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8": 1.082,
                    "GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8": 1.082,
                    "GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8": 1.082,
                    "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8": 1.082,
                    "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8": 1.082,
                    "GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8": 1.082,
                    "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8": 1.082,
                    "TTHH_TuneCP5_13TeV-madgraph-pythia8": 1.126,
                    "TTTT_TuneCP5_13TeV-amcatnlo-pythia8": 1.126,
                    "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8": 1.134,
                    "TTWH_TuneCP5_13TeV-madgraph-pythia8": 1.126,
                    "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8": 1.087,
                    "TTWW_TuneCP5_13TeV-madgraph-pythia8": 1.126,
                    "TTWZ_TuneCP5_13TeV-madgraph-pythia8": 1.126,
                    "TTZH_TuneCP5_13TeV-madgraph-pythia8": 1.126,
                    "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8": 1.167,
                    "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8": 1.167,
                    "TTZZ_TuneCP5_13TeV-madgraph-pythia8": 1.126,
                    "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8": 1.098,
                    "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8": 1.098,
                    "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8": 1.098,
                    "WZZ_TuneCP5_13TeV-amcatnlo-pythia8": 1.256,
                    "ZZTo4L_TuneCP5_13TeV_powheg_pythia8": 1.098,
                    "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8": 1.098,
                    "tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8": 1.111,
                    "ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8": 1.087,
                    "TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8": 1.117,
                    "TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8": 1.117,
                    "TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8": 1.117,
                }

def bookHistogram_MC(df, variable, range_, weight):

        h = df.Histo1D(ROOT.ROOT.RDF.TH1DModel(variable, variable, range_[0], range_[1], range_[2]),variable,weight)

        #h.SetBinContent(1,h.GetBinContent(0)+h.GetBinContent(1))
        #h.SetBinContent(range_[0],h.GetBinContent(range_[0])+h.GetBinContent(range_[0]+1))
        return h

def bookHistogram_DATA(df, variable, range_):

        return df.Histo1D(ROOT.ROOT.RDF.TH1DModel(variable, variable, range_[0], range_[1], range_[2]),variable)

    # Write a histogram with a given name to the output ROOT file
def writeHistogram(h, name,variable):
        #h.GetXaxis().SetRangeUser(-1,  ranges[variable][0]+1)
        h.SetName(name)
        h.Write()

def check_jobs(folder_date,run_name):
        output = subprocess.check_output("ls Event_Folders/Post_ES/Post_ES_{}/{}".format(folder_date,run_name), shell=True, universal_newlines=True)
        input_files = ['Event_Folders/Post_ES/Post_ES_{}/{}/{}'.format(folder_date,run_name,o) for o in output.split('\n')[:-1]]

        for i in range(len(input_files)):
            submit_file = 'Log_Folders/Post_ES_logs/Post_ES_logs_{}/{}/out_{}.txt'.format(folder_date,run_name,i)
            with open(submit_file, "rb") as file:
                try:
                    file.seek(-2, os.SEEK_END)
                    while file.read(1) != b'\n':
                        file.seek(-2, os.SEEK_CUR)
                except OSError:
                    file.seek(0)
                last_line = file.readline().decode()
            if last_line[:9] != 'Job done!' or os.path.getsize('Log_Folders/Post_ES_logs/Post_ES_logs_{}/{}/err_{}.txt'.format(folder_date,run_name,i)) != 0:
                print("job {} not finished".format(i))
                input_files.remove('Event_Folders/Post_ES/Post_ES_{}/{}/file{}.root'.format(folder_date,run_name,i))
        return input_files

def recreate_Tree(is_mc,Info,run_name = "None"):

    Tree = {}


    Tree["dataset"] = np.float64
    Tree["Pass_Lepton_Trigger"] = np.float64
    Tree["Pass_Reference_Trigger"] = np.float64

    for variable in variables:
        Tree[variable] = np.float64

    if is_mc:
        Tree["Weight"] = np.float64
        Tree["Before_Trigger_SF"] = np.float64
        for Systematic in Info.Systematics:
            Tree[Systematic] = np.float64
            Tree[Systematic+"up"] = np.float64
            Tree[Systematic+"down"] = np.float64
            Tree[Systematic+"NoSF"] = np.float64
            Tree[Systematic+"NoSFup"] = np.float64
            Tree[Systematic+"NoSFdown"] = np.float64


        for Weight in Info.Weights.keys():
            if Weight == "genWeight":
                Tree[Weight] = np.float64
            elif Weight == "PSWeight":
                Tree[Weight+"ISRup"] = np.float64
                Tree[Weight+"ISRdown"] = np.float64
                Tree[Weight+"FSRup"] = np.float64
                Tree[Weight+"FSRdown"] = np.float64
            elif run_name not in Info.WeightExclusion:
                for WeightBin in range(Info.Weights[Weight]["values"]):
                    Tree[Weight+"{}".format(WeightBin)] = np.float64
    else:
        Tree["run"] = np.uint32
        Tree["luminosityBlock"] = np.uint32
        Tree["event"] = np.uint32

    return Tree


def file_combination(label,folder_date,Info):
    CrossSections = Info.CrossSections
    Luminosity = 21128                                   # CHANGE FOR SCALING: Info.Luminosity
    Cluster = Info.SampleClusters[label]
    Systematics = list(Info.Systematics)
    print("combining files in folder: {}".format(label))

    #CALCULATE TOTAL GENTWEIGHT


    with uproot.recreate("Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label)) as output_file:
        if label not in ("DATA","REFDATA"):
            folder_date = "230512_154934"       #CHANGE FOR SCALING
            is_mc = True
            #if Info.year == 2018:
            Trees = ("nom","JECup","JECdown","JERup","JERdown")
            #elif Info.year == 2022:
            #    Trees = ("nom",)
            TotalWeight = {}
        else:
            is_mc = False
            Trees = ("nom",)

        for JEC_JER in Trees:
            Tree = recreate_Tree(is_mc,Info)
            output_file.mktree("Events_{}".format(JEC_JER), Tree)
            for i,run_name in enumerate(Cluster):
                Tree = recreate_Tree(is_mc,Info,run_name)
                print("current run {}: {}...........".format(i,run_name))
                files = ["Event_Folders/Post_ES/Post_ES_{}/{}/{}".format(folder_date,run_name,file) for file in subprocess.check_output("ls Event_Folders/Post_ES/Post_ES_{}/{}".format(folder_date,run_name), shell=True,universal_newlines=True).rstrip("\n").split("\n")]
                files = check_jobs(folder_date,run_name)
                if is_mc and JEC_JER == "nom":
                    TotalWeight[run_name] = {}
                    for j,file in enumerate(files):
                        with uproot.open(file) as f:
                            for Weight in Info.Weights.keys():
                                if Weight == "genWeight":
                                    if j == 0:
                                        TotalWeight[run_name][Weight] = f["Weights/"+Weight].values()[0]
                                    else:
                                        TotalWeight[run_name][Weight] += f["Weights/"+Weight].values()[0]
                                elif Weight == "PSWeight":
                                    for temp in ("PSWeightISRup","PSWeightFSRup","PSWeightISRdown","PSWeightFSRdown"):
                                        if j == 0:
                                            TotalWeight[run_name][temp] = f["Weights/"+temp].values()[0]
                                        else:
                                            TotalWeight[run_name][temp] += f["Weights/"+temp].values()[0]
                                elif run_name not in Info.WeightExclusion:
                                    for WeightBin in range(Info.Weights[Weight]["values"]):
                                        if j == 0:
                                            TotalWeight[run_name][Weight+"{}".format(WeightBin)] = f["Weights/"+Weight+"{}".format(WeightBin)].values()[0]
                                        else:
                                            TotalWeight[run_name][Weight+"{}".format(WeightBin)] += f["Weights/"+Weight+"{}".format(WeightBin)].values()[0]


                total_events = 0.
                total_event_count = 0.
                FilesWTree = ["{}:Events_{}".format(file,JEC_JER) for file in files]
                if 'dataset' in Tree: del Tree['dataset']
                batch = uproot.concatenate(FilesWTree,library = 'np')

                output_dict = {}
                total_event_count += len(batch["leading_lepton_pt"])

                for name in Tree.keys():
                    if name in batch.keys():
                        output_dict[name] = batch[name]
                output_dict["dataset"] = np.ones(len(batch["leading_lepton_pt"]))*i


                if is_mc:
                    output_dict["Weight"] = CrossSections[run_name]*batch["genWeight"]*Luminosity/TotalWeight[run_name]["genWeight"]
                    SF = np.product([batch[syst] for syst in Systematics],axis=0)
                    for Systematic in Systematics:
                        Other_Systematics = Systematics[:]
                        Other_Systematics.remove(Systematic)
                        Other_Systematics_SF = np.product([batch[syst] for syst in Other_Systematics],axis=0)

                        output_dict[Systematic+"up"] = batch[Systematic+"up"]*Other_Systematics_SF*CrossSections[run_name]*batch["genWeight"]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name]["genWeight"]
                        output_dict[Systematic+"down"] = batch[Systematic+"down"]*Other_Systematics_SF*CrossSections[run_name]*batch["genWeight"]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name]["genWeight"]

                        output_dict[Systematic+"NoSF"] = batch[Systematic]*CrossSections[run_name]*batch["genWeight"]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name]["genWeight"]
                        output_dict[Systematic+"NoSFup"] = batch[Systematic+"up"]*CrossSections[run_name]*batch["genWeight"]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name]["genWeight"]
                        output_dict[Systematic+"NoSFdown"] = batch[Systematic+"down"]*CrossSections[run_name]*batch["genWeight"]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name]["genWeight"]

                    for Weight in ("genWeight","PSWeightISRup","PSWeightFSRup","PSWeightISRdown","PSWeightFSRdown"):
                        output_dict[Weight] = SF*CrossSections[run_name]*batch[Weight]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name][Weight]

                    for Weight in ("LHEScaleWeight","LHEPdfWeight"):
                        for WeightBin in range(Info.Weights[Weight]["values"]):
                            if run_name not in Info.WeightExclusion:

                                output_dict[Weight+"{}".format(WeightBin)] = SF*CrossSections[run_name]*batch[Weight+"{}".format(WeightBin)]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name][Weight+"{}".format(WeightBin)]
                            else:
                                output_dict[Weight+"{}".format(WeightBin)] = SF*CrossSections[run_name]*batch["genWeight"]*Luminosity*CrossSectionVariation[run_name]/TotalWeight[run_name]["genWeight"]

                    total_events += np.sum(output_dict["genWeight"])

                output_file["Events_{}".format(JEC_JER)].extend(output_dict)

    #SAME FOR SINGLE LEPTON

def main(label,folder_date,Info):

    Systematics = list(Info.Systematics[::])
    Systematics.extend(["PSWeightISR","PSWeightFSR"])
    print(Systematics)

    # Set up multi-threading capability of ROOT
    ROOT.ROOT.EnableImplicitMT()

    # Create The PSWeight Histograms

    print("making histogram of event type: {}".format(label))

    if label not in ("DATA","REFDATA"):
        if Info.year == 2018:
            Trees = ("nom","JECup","JECdown","JERup","JERdown")
        elif Info.year == 2022:
            Trees = ("nom",)
        is_mc = True
    else:
        is_mc = False
        Trees = ("nom",)

    hist = {}

    for AnalysisRegion in Info.AnalysisRegions.keys():
        if not os.path.exists("Event_Folders/histograms_folders/histograms_{}/{}".format(folder_date,AnalysisRegion)):
            os.mkdir("Event_Folders/histograms_folders/histograms_{}/{}".format(folder_date,AnalysisRegion))

        tfile = ROOT.TFile("Event_Folders/histograms_folders/histograms_{}/{}/{}.root".format(folder_date,AnalysisRegion,label), "RECREATE")

        for Tree in Trees:
            df = RDataFrame("Events_{}".format(Tree), "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))
            df = df.Define("WZ_Binning","int(Zpt>100)+int(Zpt>200)+3*int(nJets>2)")
            for variable in ranges[AnalysisRegion].keys():
                for AnalysisCut in Info.AnalysisRegions[AnalysisRegion]:
                    df = df.Filter(AnalysisCut, "{} cut".format(AnalysisCut))

                if variable == "Binning" and AnalysisRegion == "TTZ_SR" and Tree == "nom":
                    df.Report().Print()
                if is_mc:
                    hist[variable+"_"+Tree] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],"genWeight")
                    if Tree == "nom":
                        hist[variable] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],"Weight")
                        for Systematic in Systematics:
                            hist[variable+"_"+Systematic+"up"] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Systematic+"up")
                            hist[variable+"_"+Systematic+"down"] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Systematic+"down")
                            if Systematic not in ("PSWeightISR","PSWeightFSR"):
                                hist[variable+"_"+Systematic+"NoSF"] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Systematic+"NoSF")
                                hist[variable+"_"+Systematic+"NoSFup"] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Systematic+"NoSFup")
                                hist[variable+"_"+Systematic+"NoSFdown"] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Systematic+"NoSFdown")
                else:
                    hist[variable] = bookHistogram_DATA(df, variable, ranges[AnalysisRegion][variable])

        for name in hist.keys():
            writeHistogram(hist[name], name,variable)

        tfile.Close()

        if is_mc:
            tfile = ROOT.TFile("Event_Folders/histograms_folders/histograms_{}/{}/{}_weights.root".format(folder_date,AnalysisRegion,label), "RECREATE")
            temp = {}
            df = RDataFrame("Events_nom", "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))
            df = df.Define("WZ_Binning","int(Zpt>100)+int(Zpt>200)+3*int(nJets>2)")
            for AnalysisCut in Info.AnalysisRegions[AnalysisRegion]:
                df = df.Filter(AnalysisCut, "{} cut".format(AnalysisCut))

            for variable in ranges[AnalysisRegion].keys():
                for Weight in ("LHEScaleWeight","LHEPdfWeight","genWeight"):
                    if Weight in ("LHEScaleWeight","LHEPdfWeight"):
                        for WeightBin in range(Info.Weights[Weight]["values"]):
                            temp[variable+"_"+Weight+"{}".format(WeightBin)] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Weight+"{}".format(WeightBin))
                    elif Weight == "genWeight":
                        temp[variable+"_"+Weight] = bookHistogram_MC(df, variable, ranges[AnalysisRegion][variable],Weight)

            for name in temp.keys():
                writeHistogram(temp[name], name,variable)
            tfile.Close()

            with uproot.open("Event_Folders/histograms_folders/histograms_{}/{}/{}_weights.root".format(folder_date,AnalysisRegion,label)) as WeightFile:
                with uproot.update("Event_Folders/histograms_folders/histograms_{}/{}/{}.root".format(folder_date,AnalysisRegion,label)) as OutputFile:
                    for variable in ranges[AnalysisRegion].keys():
                        LHEScaleWeightMax = np.zeros(ranges[AnalysisRegion][variable][0])
                        LHEScaleWeightMin = np.zeros(ranges[AnalysisRegion][variable][0])
                        LHEPdfWeightRMS_sq = np.zeros(ranges[AnalysisRegion][variable][0])
                        bins = WeightFile["{}_genWeight".format(variable)].axis().edges()
                        nominal = WeightFile["{}_genWeight".format(variable)].values()
                        for Weight in ("LHEScaleWeight","LHEPdfWeight"):
                            for WeightBin in range(Info.Weights[Weight]["values"]):
                                WeightVar = WeightFile["{}_{}{}".format(variable,Weight,WeightBin)].values()-nominal
                                if Weight == "LHEScaleWeight":
                                    for i in range(ranges[AnalysisRegion][variable][0]):
                                        if WeightVar[i] > LHEScaleWeightMax[i]:
                                            LHEScaleWeightMax[i] = WeightVar[i]
                                        if WeightVar[i] < LHEScaleWeightMin[i]:
                                            LHEScaleWeightMin[i] = WeightVar[i]
                                else:
                                    LHEPdfWeightRMS_sq += WeightVar**2
                        LHEPdfWeightRMS = np.sqrt(LHEPdfWeightRMS_sq)

                        OutputFile["{}_LHEScaleWeightup".format(variable)] = nominal+LHEScaleWeightMax,bins
                        OutputFile["{}_LHEScaleWeightdown".format(variable)] = nominal+LHEScaleWeightMin,bins
                        OutputFile["{}_LHEPdfWeightup".format(variable)] = nominal+LHEPdfWeightRMS,bins
                        OutputFile["{}_LHEPdfWeightdown".format(variable)] = nominal-LHEPdfWeightRMS,bins
#__________________________________


def COMBINE(folder_date,Info,job):

    region,binning = (("CR_WZ","WZ_Binning"),("TTZ_SR","Binning"))[job]
    ROOT.ROOT.EnableImplicitMT()

    # Create output file
    tfile = ROOT.TFile.Open("COMBINE_{}.root".format(region) , "RECREATE")
    tfile.cd()
    tfile.mkdir("crz/")
    tfile.cd("crz/")

    print(region,binning,ranges[region][binning])
    for label in Info.SampleClusters.keys():
        df = RDataFrame("Events_nom", "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))
        for AnalysisCut in Info.AnalysisRegions[region]:
            df = df.Filter(AnalysisCut, "{} cut".format(AnalysisCut))

        df = df.Define("WZ_Binning","int(Zpt>100)+int(Zpt>200)+3*int(nJets>2)")
        if label == "TTZ":
            df.Report().Print()
        if label != "DATA":
            hist = bookHistogram_MC(df, binning, ranges[region][binning],"genWeight")
            writeHistogram(hist, label,binning)
        else:
            hist = bookHistogram_DATA(df, binning, ranges[region][binning])
            writeHistogram(hist, "data_obs",binning)

    Systematics = list(Info.Systematics[::])
    Systematics.extend(["PSWeightISR","PSWeightFSR"])
    for Systematic in Systematics:
        for (sf,CAP) in (("up","Up"),("down","Down")):
             tfile.cd()
             folder = "{}{}".format(Systematic,CAP)
             weight = "{}{}".format(Systematic,sf)
             tfile.mkdir("crz/{}/".format(folder))
             tfile.cd("crz/{}/".format(folder))

             for label in Info.SampleClusters.keys():
                 if label != "DATA":
                     df = RDataFrame("Events_nom", "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))
                     for AnalysisCut in Info.AnalysisRegions[region]:
                         df = df.Filter(AnalysisCut, "{} cut".format(AnalysisCut))

                     df = df.Define("WZ_Binning","int(Zpt>100)+int(Zpt>200)+3*int(nJets>2)")
                     hist = bookHistogram_MC(df, binning, ranges[region][binning],weight)
                     writeHistogram(hist, label,binning)


    for Systematic in ("JEC","JER"):
        for (sf,CAP) in (("up","Up"),("down","Down")):
            tfile.cd()
            folder = "{}{}".format(Systematic,CAP)
            weight = "{}{}".format(Systematic,sf)
            print(folder)
            tfile.mkdir("crz/{}/".format(folder))
            tfile.cd("crz/{}/".format(folder))
            for label in Info.SampleClusters.keys():
                if label != "DATA":

                    df = RDataFrame("Events_{}".format(weight), "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))
                    for AnalysisCut in Info.AnalysisRegions[region]:
                        df = df.Filter(AnalysisCut, "{} cut".format(AnalysisCut))

                    df = df.Define("WZ_Binning","int(Zpt>100)+int(Zpt>200)+3*int(nJets>2)")
                    hist = bookHistogram_MC(df, binning, ranges[region][binning],"genWeight")
                    writeHistogram(hist, label,binning)

    tfile.Close()
    tfile = ROOT.TFile("Event_Folders/histograms_folders/histograms_{}/{}/CombineWeights.root".format(folder_date,region), "RECREATE")
    for label in Info.SampleClusters.keys():
        if label != "DATA":
            temp = {}
            df = RDataFrame("Events_nom", "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))
            for AnalysisCut in Info.AnalysisRegions[region]:
                df = df.Filter(AnalysisCut, "{} cut".format(AnalysisCut))

            df = df.Define("WZ_Binning","int(Zpt>100)+int(Zpt>200)+3*int(nJets>2)")
            for Weight in ("LHEScaleWeight","LHEPdfWeight","genWeight"):
                if Weight in ("LHEScaleWeight","LHEPdfWeight"):
                    for WeightBin in range(Info.Weights[Weight]["values"]):
                        temp["{}_{}{}".format(label,Weight,WeightBin)] = bookHistogram_MC(df, binning, ranges[region][binning],Weight+"{}".format(WeightBin))
                elif Weight == "genWeight":
                    temp["{}_{}".format(label,Weight)] = bookHistogram_MC(df, binning, ranges[region][binning],Weight)

            for name in temp.keys():
                writeHistogram(temp[name], name,binning)
    tfile.Close()

    with uproot.update("COMBINE_{}.root".format(region)) as OutputFile:
        with uproot.open("Event_Folders/histograms_folders/histograms_{}/{}/CombineWeights.root".format(folder_date,region)) as WeightFile:
            for label in Info.SampleClusters.keys():
                if label != "DATA":
                    LHEScaleWeightMax = np.zeros(ranges[region][binning][0])
                    LHEScaleWeightMin = np.zeros(ranges[region][binning][0])
                    LHEPdfWeightRMS_sq = np.zeros(ranges[region][binning][0])
                    bins = WeightFile["{}_genWeight".format(label)].axis().edges()
                    nominal = WeightFile["{}_genWeight".format(label)].values()
                    for Weight in ("LHEScaleWeight","LHEPdfWeight"):
                        for WeightBin in range(Info.Weights[Weight]["values"]):
                            WeightVar = WeightFile["{}_{}{}".format(label,Weight,WeightBin)].values()-nominal
                            if Weight == "LHEScaleWeight":
                                for i in range(ranges[region][binning][0]):
                                    if WeightVar[i] > LHEScaleWeightMax[i]:
                                        LHEScaleWeightMax[i] = WeightVar[i]
                                    if WeightVar[i] < LHEScaleWeightMin[i]:
                                        LHEScaleWeightMin[i] = WeightVar[i]
                            else:
                                LHEPdfWeightRMS_sq += WeightVar**2
                OutputFile["crz/LHEScaleWeightUp/{}".format(label)] = nominal+LHEScaleWeightMax,bins
                OutputFile["crz/LHEScaleWeightDown/{}".format(label)] = nominal+LHEScaleWeightMin,bins
                OutputFile["crz/LHEPdfWeightUp/{}".format(label)] = nominal+np.sqrt(LHEPdfWeightRMS_sq),bins
                OutputFile["crz/LHEPdfWeightDown/{}".format(label)] = nominal-np.sqrt(LHEPdfWeightRMS_sq),bins

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-o', '--option', nargs=1, required = True)
    parser.add_argument('-f', '--folder_date', nargs=1, required = True)
    parser.add_argument('-l', '--labels', nargs=1, required = True)
    parser.add_argument('-y', '--year', nargs=1,type=int, required = True)
    parser.add_argument('-j', '--job', nargs=1,type=int, required = True)

    args = parser.parse_args()
    folder_date = args.folder_date[0]
    option = args.option[0]
    labels = args.labels[0]
    year = args.year[0]
    job = args.job[0]
    labels = labels.split(",")
    label = labels[job]

    Info = Analysis(year)


    if option == "ADD":
        file_combination(label,folder_date,Info)
    elif option == "HISTOGRAM":
        main(label,folder_date,Info)
    elif option == "ALL":
        file_combination(label,folder_date,Info)
        main(label,folder_date,Info)
    elif option == "COMBINE":
        COMBINE(folder_date,Info,job)

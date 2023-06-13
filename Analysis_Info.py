import correctionlib._core as core
import numpy as np

class Analysis:
    def __init__(self,year = 2018):
        self.year = year
        """Object Selection"""

        if year == 2018:
            self.Luminosity =                           31800.
            self.ElectronIDWorkingPoint =               "wp80iso"           #wp80iso
            self.ElectronWorkingPoint =                 "Electron_mvaFall17V2Iso_WP80" #Electron_mvaFall17V2Iso_WP80
            self.ElectronPtCut =                        10.
            self.ElectronEtaCut =                       2.4


            self.MuonIDWorkingPoint =                   "Muon_tightId"      #"Muon_tightId"
            self.MuonISOWorkingPoint =                  4       #4
            self.MuonPtCut =                           10.
            self.MuonEtaCut =                           2.4
            self.MuonSFnames =                          ("NUM_TrackerMuons_DEN_genTracks","NUM_TightID_DEN_TrackerMuons","NUM_TightRelIso_DEN_TightIDandIPCut")

            self.deepCSV_WorkingPoint =                 "M"
            self.deepCSV_WorkingPoint_number =          0.4941
            self.JetPtCut =                             30.
            self.JetEtaCut =                            2.5
            self.JetIDWorkingPoint =                    2
            self.JetDRCut =                             0.4
        elif year == 2022:

            self.Luminosity =                           21128


            self.ElectronIDWorkingPoint =               "wp80iso"
            self.ElectronWorkingPoint =                 "Electron_mvaIso_WP80"
            self.ElectronPtCut =                        10.
            self.ElectronEtaCut =                       2.4


            self.MuonIDWorkingPoint =                   "Muon_tightId" #see DOCU for Muon MediumID
            self.MuonISOWorkingPoint =                  4
            self.MuonPtCut =                           10.
            self.MuonEtaCut =                           2.4
            self.MuonSFnames =                          ("NUM_TrackerMuons_DEN_genTracks","NUM_TightID_DEN_TrackerMuons","NUM_TightRelIso_DEN_TightIDandIPCut")

            self.deepCSV_WorkingPoint =                 "M"
            self.deepCSV_WorkingPoint_number =          0.4941
            self.JetPtCut =                             30.
            self.JetEtaCut =                            2.5
            self.JetIDWorkingPoint =                    2
            self.JetDRCut =                             0.4
        """Event Selection"""

        self.LeadingLeptonPtCut =                   40.
        self.SubLeadingLeptonPtCut =                20.
        self.SubSubLeadingLeptonPtCut =             10.

        self.AnalysisRegions = {
            "TTZ_SR": (
                "nJets>=3",
                "nBJets>=1",
                "raw_HT>=300",
                "min_mll>=12",
                "max_sip3d<5"),

            "CR_WZ": (
                "nJets>1",
                "nJets<3 || nBJets==0",
                "leading_lepton_pt>50",
                "subleading_lepton_pt>30",
                "subsubleading_lepton_pt>20",
                "min_mll>=12",
                "max_sip3d<5"
            ),

            "No_cuts": (),
            "No_Jetcut": ("min_mll>=12",),
            "No_BJetcut": ("nJets>=3","min_mll>=12"),
            "No_HTcut": ("nJets>=3",
                        "nBJets>=1",
                        "min_mll>=12"),
            "No_max_sip3dcut": ("nJets>=3",
                        "nBJets>=1",
                        "raw_HT>=300",
                        "min_mll>=12"),



        }


        self.Weights = {
                        "LHEScaleWeight": {
                                "values": 7,
                                "calcuation": "Max",
                                "SumName": "LHEScaleSumw"
                                        },
                        "PSWeight": {
                                "values": 4,
                                "calcuation": "Systematic",
                                "SumName": "PSSumw"
                                    },

                        "genWeight": {
                                "values": 1,
                                "calcuation": "None",
                                "SumName": "genEventSumw"
                                     },
                        "LHEPdfWeight": {
                                "values": 100,
                                "calcuation": "RMS",
                                "SumName": "LHEPdfSumw"
                                        },
                        }

        """Monte Carlo Samples"""

        if year == 2018:
            self.DASMCFiles = (
                                "/DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTHH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/TTTT_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTWH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTWW_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTWZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTZH_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TTZZ_TuneCP5_13TeV-madgraph-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM",
                                "/WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM",
                                "/WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/WZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM",
                                "/ZZTo4L_TuneCP5_13TeV_powheg_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v2/NANOAODSIM",
                                "/ZZZ_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1_ext1-v2/NANOAODSIM",
                                "/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM",
                                "/TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL18NanoAODv9-106X_upgrade2018_realistic_v16_L1v1-v1/NANOAODSIM"
                                )

            self.Data = (           "/DoubleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                                    "/EGamma/Run2018D-UL2018_MiniAODv2_NanoAODv9-v3/NANOAOD",
                                    "/MuonEG/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                                    "/SingleMuon/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                                    #"/JetHT/Run2018D-UL2018_MiniAODv2_NanoAODv9-v2/NANOAOD",
                                    #"/MET/Run2018D-UL2018_MiniAODv2_NanoAODv9_GT36-v1/NANOAOD",
                                    )
            self.CrossSections = {
                                "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8": 6077.22,
                                "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8": 0.005423,
                                "GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8": 0.005423,
                                "GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8": 0.005423,
                                "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8": 0.0027,
                                "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8": 0.0027,
                                "GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8": 0.0027,
                                "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8": 2.22,
                                "TTHH_TuneCP5_13TeV-madgraph-pythia8": 0.0003697,
                                "TTTT_TuneCP5_13TeV-amcatnlo-pythia8": 0.01337,
                                "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8": 88.4,
                                "TTWH_TuneCP5_13TeV-madgraph-pythia8": 0.001141,
                                "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8": 0.235,
                                "TTWW_TuneCP5_13TeV-madgraph-pythia8": 0.007003,
                                "TTWZ_TuneCP5_13TeV-madgraph-pythia8": 0.002453,
                                "TTZH_TuneCP5_13TeV-madgraph-pythia8": 0.00113,
                                "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8": 0.281,
                                "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8": 0.08416,
                                "TTZZ_TuneCP5_13TeV-madgraph-pythia8": 0.001386,
                                "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8": 0.2086,
                                "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8": 0.1651,
                                "WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8": 4.9173,
                                "WZZ_TuneCP5_13TeV-amcatnlo-pythia8": 0.05565,
                                "ZZTo4L_TuneCP5_13TeV_powheg_pythia8": 1.256,
                                "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8": 0.01476,
                                "tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8": 0.07358,
                                "ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8": 0.211,
                                "TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8": 0.003004,
                                "TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8": 0.003004,
                                "TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8": 0.0015,
                            }

            """DATA Samples"""

            self.RefData = ( "JetHT","MET")

            self.DataNames = (      "DoubleMuonRun2018D",
                                    "EGammaRun2018D",
                                    "MuonEGRun2018D",
                                    "SingleMuonRun2018D"
                                    )

            self.SampleClusters = {
                        "TTZ":  (
                        "TTZToLLNuNu_M-10_TuneCP5_13TeV-amcatnlo-pythia8",
                                ),

                        "OtherT":  (
                        "tZq_ll_4f_ckm_NLO_TuneCP5_13TeV-amcatnlo-pythia8",
                        "TWZToLL_thad_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8",
                        "TWZToLL_tlept_Whad_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8",
                        "TWZToLL_tlept_Wlept_5f_DR_TuneCP5_13TeV-amcatnlo-pythia8",
                                ),

                        "NonPrompt":    (
                        "TTTo2L2Nu_TuneCP5_13TeV-powheg-pythia8",
                        "DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8",
                                        ),

                        "WZ": ("WZTo3LNu_TuneCP5_13TeV-amcatnloFXFX-pythia8",),

                        "ZZ":   (
                        "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
                        "GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8",
                        "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
                        "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
                        "GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8",
                        "GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8",
                        "ZZTo4L_TuneCP5_13TeV_powheg_pythia8",
                                        ),

                        "TTX":          (
                        "TTHH_TuneCP5_13TeV-madgraph-pythia8",
                        "TTTT_TuneCP5_13TeV-amcatnlo-pythia8",
                        "TTGamma_Dilept_TuneCP5_13TeV-madgraph-pythia8",
                        "TTWH_TuneCP5_13TeV-madgraph-pythia8",
                        "TTWJetsToLNu_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8",
                        "TTWW_TuneCP5_13TeV-madgraph-pythia8",
                        "TTWZ_TuneCP5_13TeV-madgraph-pythia8",
                        "TTZH_TuneCP5_13TeV-madgraph-pythia8",
                        "TTZZ_TuneCP5_13TeV-madgraph-pythia8",
                        "ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8",
                        "TTZToLL_M-1to10_TuneCP5_13TeV-amcatnlo-pythia8",
                                        ),

                        "VVV":       (
                        "WWW_4F_TuneCP5_13TeV-amcatnlo-pythia8",
                        "WWZ_4F_TuneCP5_13TeV-amcatnlo-pythia8",
                        "WZZ_TuneCP5_13TeV-amcatnlo-pythia8",
                        "ZZZ_TuneCP5_13TeV-amcatnlo-pythia8",
                                    ),
                        "DATA":     (
                        "EGammaRun2022F",
                        "EGammaRun2022G",
                        "MuonRun2022F",
                        "MuonRun2022G",
                        "MuonEGRun2022F",
                        "MuonEGRun2022G",                            #"MuonEGRun2018D",
                                                    #"SingleMuonRun2018D",
                                                    #"EGammaRun2018D",
                                                    #"DoubleMuonRun2018D",
                        ),
                        #}"REFDATA": (

                        #"JetHTRun2018D",
                        #"METRun2018D"
                        #)

                }

            self.MClabels = ("NonPrompt","TTX","OtherT","WZ","ZZ","VVV","TTZ")

            self.WeightExclusion = (
                                    "GluGluToContinToZZTo2e2mu_TuneCP5_13TeV-mcfm701-pythia8",
                                    "GluGluToContinToZZTo2e2tau_TuneCP5_13TeV-mcfm701-pythia8",
                                    "GluGluToContinToZZTo4e_TuneCP5_13TeV-mcfm701-pythia8",
                                    "GluGluToContinToZZTo4mu_TuneCP5_13TeV-mcfm701-pythia8",
                                    "GluGluToContinToZZTo4tau_TuneCP5_13TeV-mcfm701-pythia8",
                                    "GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV-mcfm701-pythia8"
                                    )

            self.Systematics = ("Electron_SF","Muon_SF","Trigger_SF","BtaggingIncl_SF","BtaggingComb_SF","PileUp_SF",)#"PileUpId_SF")

            self.Electron_MVAWP =                       "scalefactors/egammaEffi_MVA_ID_2018.json"
            self.btagging_SF =                          "scalefactors/btagging.json"
            self.MuonSF =                               "scalefactors/muon_2018UL.json"
            self.Btagging_Efficiency =                  "scalefactors/Btagging_Efficiency.json"
            self.jet_jerc =                             "scalefactors/jet_jerc.json"
            self.jetvetomap =                           "scalefactors/jetvetomaps2018UL.json"
            self.trigger_SF =                           "scalefactors/Trigger_Efficiency_SF.json"
            self.PileUp_SF =                            "scalefactors/2018D_UL_puWeights.json"
            self.PileUpId_SF =                            "scalefactors/UL18_jmar.json"

            self.jetvetomapSample = "Summer19UL18_V1"

            self.evaluators = {
                            "Electron_SF": core.CorrectionSet.from_file(self.Electron_MVAWP),
                            "Btagging_SF": core.CorrectionSet.from_file(self.btagging_SF),
                            "Muon_SF": core.CorrectionSet.from_file(self.MuonSF),
                            "Btagging_Eff": core.CorrectionSet.from_file(self.Btagging_Efficiency),
                            "jetvetomap": core.CorrectionSet.from_file(self.jetvetomap),
                            "jet_jerc": core.CorrectionSet.from_file(self.jet_jerc),
                            "Trigger_SF": core.CorrectionSet.from_file(self.trigger_SF),
                            "PileUp_SF": core.CorrectionSet.from_file(self.PileUp_SF),
                            "PileUpId_SF": core.CorrectionSet.from_file(self.PileUpId_SF)
                                }

            self.lepton_triggers =                      ("HLT_TripleMu_10_5_5_DZ", "HLT_Mu37_TkMu27","HLT_TripleMu_12_10_5","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
                "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ","HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                "HLT_Mu27_Ele37_CaloIdL_MW","HLT_Mu37_Ele27_CaloIdL_MW","HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ","HLT_Mu8_DiEle12_CaloIdL_TrackIdL",
                "HLT_IsoMu24", "HLT_IsoMu27", "HLT_Mu50", "HLT_OldMu100", "HLT_TkMu100",
                "HLT_Ele32_WPTight_Gsf", "HLT_Ele115_CaloIdVT_GsfTrkIdT","HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL","HLT_DoubleEle25_CaloIdL_MW","HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL")

            self.reference_triggers =                   ("HLT_PFHT1050",
                                                        "HLT_AK8PFJet500",
                                                        "HLT_CaloMET350_HBHECleaned",
                                                        "HLT_PFJet500",
                                                        "HLT_PFMET120_PFMHT120_IDTight",
                                                        "HLT_PFMET250_HBHECleaned",
                                                        "HLT_PFMETTypeOne140_PFMHT140_IDTight",
                                                        "HLT_DiJet110_35_Mjj650_PFMET110",
                                                        "HLT_PFHT800_PFMET75_PFMHT75_IDTight",
                                                        "HLT_PFHT700_PFMET85_PFMHT85_IDTight",
                                                        "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
                                                        "HLT_TripleJet110_35_35_Mjj650_PFMET110")
        elif year == 2022:

            self.DASMCFiles = ("/TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                                "/WZ_TuneCP5_13p6TeV_pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                                "/ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                                "/WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                                "/TTZZ_TuneCP5_13p6TeV_madgraph-madspin-pythia8/Run3Summer22EENanoAODv11-126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM",
                                "/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8/Run3Summer22EENanoAODv11-forPOG_126X_mcRun3_2022_realistic_postEE_v1-v1/NANOAODSIM")

            self.Data = (
                        "/EGamma/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD",
                        "/Muon/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD",
                        "/MuonEG/Run2022F-PromptNanoAODv11_v1-v2/NANOAOD",
                        "/EGamma/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                        "/Muon/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD",
                        "/MuonEG/Run2022G-PromptNanoAODv11_v1-v2/NANOAOD")

            self.CrossSections = {
                                "TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8": 88.4,
                                "WZ_TuneCP5_13p6TeV_pythia8": 4.9173,
                                }

            self.SampleClusters = {
                        "NonPrompt":    (
                        "TTto2L2Nu_TuneCP5_13p6TeV_powheg-pythia8",
                        "DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8",
                        ),

                        "WZ":   (
                        "WZ_TuneCP5_13p6TeV_pythia8",
                                       ),
                        "VVV": (
                        "WZZ_TuneCP5_13p6TeV_amcatnlo-pythia8",
                        "ZZZ_TuneCP5_13p6TeV_amcatnlo-pythia8"
                        ),

                        "DATA":     (
                        "EGammaRun2022F",
                        "EGammaRun2022G",
                        "MuonRun2022F",
                        "MuonRun2022G",
                        "MuonEGRun2022F",
                        "MuonEGRun2022G",
                                    ),

                        #"REFDATA": (
                        #    "JetMETRun2022F","JetMETRun2022G"
                        #)
                                }


            self.WeightExclusion = (
                                    "WZ_TuneCP5_13p6TeV_pythia8",
                                    )
            self.MClabels = ("NonPrompt","VV",)

            """Scalefactors Json Files"""
            self.Systematics = ("Electron_SF","Muon_SF","Trigger_SF","BtaggingIncl_SF","BtaggingComb_SF","PileUp_SF")



            self.Electron_MVAWP =                       "scalefactors/egammaEffi_MVA_ID_2018.json"
            self.btagging_SF =                          "scalefactors/btagging.json"
            self.MuonSF =                               "scalefactors/muon_2018UL.json"
            self.Btagging_Efficiency =                  "scalefactors/Btagging_Efficiency.json"
            self.jet_jerc =                             "scalefactors/jet_jerc.json"
            self.jetvetomap =                           "scalefactors/jetvetomaps2022.json"
            self.trigger_SF =                           "scalefactors/Trigger_Efficiency_SF.json"
            self.PileUp_SF =                            "scalefactors/2018D_UL_puWeights.json"

            self.jetvetomapSample = "Winter22Run3_RunE_V1"

            self.evaluators = {
                            "Electron_SF": core.CorrectionSet.from_file(self.Electron_MVAWP),
                            "Btagging_SF": core.CorrectionSet.from_file(self.btagging_SF),
                            "Muon_SF": core.CorrectionSet.from_file(self.MuonSF),
                            "Btagging_Eff": core.CorrectionSet.from_file(self.Btagging_Efficiency),
                            "jetvetomap": core.CorrectionSet.from_file(self.jetvetomap),
                            "jet_jerc": core.CorrectionSet.from_file(self.jet_jerc),
                            "Trigger_SF": core.CorrectionSet.from_file(self.trigger_SF),
                            "PileUp_SF": core.CorrectionSet.from_file(self.PileUp_SF)
                                }

            self.lepton_triggers =                      ("HLT_TripleMu_10_5_5_DZ", "HLT_Mu37_TkMu27","HLT_TripleMu_12_10_5","HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8",
                "HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ","HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ","HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL",
                "HLT_Mu27_Ele37_CaloIdL_MW","HLT_Mu37_Ele27_CaloIdL_MW","HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ","HLT_Mu8_DiEle12_CaloIdL_TrackIdL",
                "HLT_IsoMu24", "HLT_IsoMu27", "HLT_Mu50",
                "HLT_Ele32_WPTight_Gsf", "HLT_Ele115_CaloIdVT_GsfTrkIdT","HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL","HLT_DoubleEle25_CaloIdL_MW","HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL")

            self.reference_triggers =                   ("HLT_PFHT1050",
                                                        "HLT_AK8PFJet500",
                                                        "HLT_PFJet500",
                                                        "HLT_PFMET120_PFMHT120_IDTight",
                                                        "HLT_PFMETTypeOne140_PFMHT140_IDTight",
                                                        "HLT_DiJet110_35_Mjj650_PFMET110",
                                                        "HLT_PFHT800_PFMET75_PFMHT75_IDTight",
                                                        "HLT_PFHT700_PFMET85_PFMHT85_IDTight",
                                                        "HLT_PFHT500_PFMET100_PFMHT100_IDTight",
                                                        "HLT_TripleJet110_35_35_Mjj650_PFMET110")


        self.OutputMC = {    "leading_lepton_pt": np.float64,        "leading_lepton_eta": np.float64,       "leading_lepton_phi": np.float64,       "leading_lepton_is_electron": np.uint8,         "leading_lepton_charge": np.uint8,
                                    "subleading_lepton_pt": np.float64,     "subleading_lepton_eta": np.float64,    "subleading_lepton_phi": np.float64,    "subleading_lepton_is_electron": np.uint8,      "subleading_lepton_charge": np.uint8,
                                    "subsubleading_lepton_pt": np.float64,  "subsubleading_lepton_eta": np.float64, "subsubleading_lepton_phi": np.float64, "subsubleading_lepton_is_electron": np.uint8,   "subsubleading_lepton_charge": np.uint8,
                                    "max_dxy":  np.float64,
                                    "max_dz":  np.float64,
                                    "leading_lepton_miniPFRelIso_all":  np.float64, "subleading_lepton_miniPFRelIso_all":  np.float64, "subsubleading_lepton_miniPFRelIso_all":  np.float64,
                                    "leading_lepton_pfRelIso03_all":  np.float64, "subleading_lepton_pfRelIso03_all":  np.float64, "subsubleading_lepton_pfRelIso03_all":  np.float64,
                                    "max_sip3d":  np.float64,

                                    "nJets": np.uint8,                      "nBJets": np.uint8,                     "raw_HT": np.float64, "leading_jet_pt": np.float64, "leading_jet_eta": np.float64, "leading_jet_phi": np.float64,
                                    "nElectron": np.uint8,                  "nMuon": np.uint8,                      "mll": np.float64, "mlll": np.float64, "min_mll": np.float64, "MT": np.float64, "MET_pt": np.float64, "Zpt": np.float64,
                                    "Pass_Lepton_Trigger": np.uint8, "Pass_Reference_Trigger": np.uint8,
                                    "Pileup_nTrueInt": np.float64 ,"Before_Trigger_SF": np.float64, "ZisReconstructed": np.uint8,
                                    "Binning": np.uint8
                                    }

        self.OutputDATA = {         "leading_lepton_pt": np.float64,        "leading_lepton_eta": np.float64,       "leading_lepton_phi": np.float64,       "leading_lepton_is_electron": np.uint8,         "leading_lepton_charge": np.uint8,
                                    "subleading_lepton_pt": np.float64,     "subleading_lepton_eta": np.float64,    "subleading_lepton_phi": np.float64,    "subleading_lepton_is_electron": np.uint8,      "subleading_lepton_charge": np.uint8,
                                    "subsubleading_lepton_pt": np.float64,  "subsubleading_lepton_eta": np.float64, "subsubleading_lepton_phi": np.float64, "subsubleading_lepton_is_electron": np.uint8,   "subsubleading_lepton_charge": np.uint8,
                                    "max_dxy":  np.float64,
                                    "max_dz":  np.float64,
                                    "leading_lepton_miniPFRelIso_all":  np.float64, "subleading_lepton_miniPFRelIso_all":  np.float64, "subsubleading_lepton_miniPFRelIso_all":  np.float64,
                                    "leading_lepton_pfRelIso03_all":  np.float64, "subleading_lepton_pfRelIso03_all":  np.float64, "subsubleading_lepton_pfRelIso03_all":  np.float64,
                                    "max_sip3d":  np.float64,

                                    "nJets": np.uint8,                      "nBJets": np.uint8,                     "raw_HT": np.float64,
                                    "leading_jet_pt": np.float64, "leading_jet_eta": np.float64, "leading_jet_phi": np.float64,
                                    "nElectron": np.uint8,                  "nMuon": np.uint8,                      "mll": np.float64, "mlll": np.float64, "min_mll": np.float64, "MT": np.float64, "MET_pt": np.float64, "Zpt": np.float64,
                                    "Pass_Lepton_Trigger": np.uint8, "Pass_Reference_Trigger": np.uint8, "ZisReconstructed": np.uint8,
                                    "luminosityBlock": np.uint32, "run": np.uint32, "event":np.uint32,
                                    "Binning": np.uint8,
                                    }

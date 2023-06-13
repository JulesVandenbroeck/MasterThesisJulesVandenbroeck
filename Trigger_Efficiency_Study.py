import numpy as np
import uproot
import matplotlib.pyplot as plt
import scipy.stats
import mplhep as hep
import ROOT
from ROOT import RDataFrame, TH1, TH2D
import datetime, os, subprocess
from Analysis_Info import Analysis
import json


def clopper_pearson(k,n,alpha=0.32):
    """
    http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    alpha confidence intervals for a binomial distribution of k expected successes on n trials
    Clopper Pearson intervals are a conservative estimate.
    """
    lo = scipy.stats.beta.ppf(alpha/2,k, n-k+1)
    hi = scipy.stats.beta.ppf(1 - alpha/2, k+1, n-k)


    hi[np.where(np.isnan(hi))] = 1

    return lo, hi


def book2DHistogram_MC(df,bins, weight):
    h = df.Histo2D(ROOT.ROOT.RDF.TH2DModel("trigger_eff","Triggers", bins, 40., 240., bins, 0, 2.4),"leading_lepton_pt","abseta",weight)
    #h.SetBinContent(1,h.GetBinContent(0)+h.GetBinContent(1))
    #h.SetBinContent(range_[0],h.GetBinContent(range_[0])+h.GetBinContent(range_[0]+1))
    return h

def book2DHistogram_DATA(df,bins):


    h = df.Histo1D(ROOT.ROOT.RDF.TH1DModel("trigger_eff","Triggers", bins, 10., 200.),"leading_lepton_pt")
    #h.SetBinContent(1,h.GetBinContent(0)+h.GetBinContent(1))
    #h.SetBinContent(range_[0],h.GetBinContent(range_[0])+h.GetBinContent(range_[0]+1))
    return h



def writeHistogram(h, name):
    h.SetName(name)
    h.Write()




def write_json(year):

    file = uproot.open("scalefactors/Trigger_SF{}.root".format(year))

    pt_edges = list(file["Trigger_Eff_Data"].axis(0).edges())
    eta_edges = list(file["Trigger_Eff_Data"].axis(1).edges())

    Trigger_Eff_Data = list(file["Trigger_Eff_Data"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    Trigger_Eff_Data_up = list(file["Trigger_Eff_Data_up"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    Trigger_Eff_Data_down = list(file["Trigger_Eff_Data_down"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))

    Trigger_Eff_MC = list(file["Trigger_Eff_MC"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    Trigger_Eff_MC_up = list(file["Trigger_Eff_MC_up"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    Trigger_Eff_MC_down = list(file["Trigger_Eff_MC_down"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))

    Trigger_SF = list(file["Trigger_SF"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    Trigger_SF_up = list(file["Trigger_SF_up"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    Trigger_SF_down = list(file["Trigger_SF_down"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))

    dict = {
        "schema_version": 2,
        "description": "These are the trigger scalefactors and efficiencies for the ttZ 2018 measurement",
        "corrections": [
            {
                "name": "Trigger_Scalefactors",
                "description": "These are the trigger scalefactors and efficiencies for the ttZ 2018 measurement",
                "version": 2,
                "inputs": [
                    {
                        "name": "systematic",
                        "type": "string",
                        "description": "central,up,down"
                    },
                    {
                        "name": "type",
                        "type": "string",
                        "description": "Type: trigger efficiency SF, trigger efficiency in data or trigger efficiency in MC"
                    },
                    {
                        "name": "eta",
                        "type": "real",
                        "description": "jet eta"
                    },
                    {
                        "name": "pt",
                        "type": "real",
                        "description": "jet pT"
                    }
                ],
                "output": {
                    "name": "weight",
                    "type": "real",
                    "description": "value of scale factor (nominal, up or down)"
                },
                "data": {
                                "nodetype": "category",
                                "input": "systematic",
                                "content":
                            [
                                    {
                                        "key": "central",
                                        "value": {
                                            "nodetype": "category",
                                                        "input": "type",
                                                        "content": [
                                                            {
                                                                "key": "EfficiencyData",
                                                                "value": {
                                                                    "nodetype": "multibinning",
                                                                    "inputs": [
                                                                        "eta",
                                                                        "pt"
                                                                    ],
                                                                    "edges": [
                                                                        eta_edges,
                                                                        pt_edges
                                                                    ],
                                                                    "content": Trigger_Eff_Data,
                                                                    "flow": "error"
                                                                }
                                                          },
                                                          {
                                                              "key": "EfficiencyMC",
                                                              "value": {
                                                                  "nodetype": "multibinning",
                                                                  "inputs": [
                                                                      "eta",
                                                                      "pt"
                                                                  ],
                                                                  "edges": [
                                                                      eta_edges,
                                                                      pt_edges
                                                                  ],
                                                                  "content": Trigger_Eff_MC,
                                                                  "flow": "error"
                                                              }
                                                        },
                                                        {
                                                            "key": "SF",
                                                            "value": {
                                                                "nodetype": "multibinning",
                                                                "inputs": [
                                                                    "eta",
                                                                    "pt"
                                                                ],
                                                                "edges": [
                                                                    eta_edges,
                                                                    pt_edges
                                                                ],
                                                                "content": Trigger_SF,
                                                                "flow": "error"
                                                            }
                                                      }]
                                                        }
                                                },
                                    {
                                        "key": "up",
                                        "value": {
                                            "nodetype": "category",
                                                        "input": "type",
                                                        "content": [
                                                            {
                                                                "key": "EfficiencyData",
                                                                "value": {
                                                                    "nodetype": "multibinning",
                                                                    "inputs": [
                                                                        "eta",
                                                                        "pt"
                                                                    ],
                                                                    "edges": [
                                                                        eta_edges,
                                                                        pt_edges
                                                                    ],
                                                                    "content": Trigger_Eff_Data_up,
                                                                    "flow": "error"
                                                                }
                                                          },
                                                          {
                                                              "key": "EfficiencyMC",
                                                              "value": {
                                                                  "nodetype": "multibinning",
                                                                  "inputs": [
                                                                      "eta",
                                                                      "pt"
                                                                  ],
                                                                  "edges": [
                                                                      eta_edges,
                                                                      pt_edges
                                                                  ],
                                                                  "content": Trigger_Eff_MC_up,
                                                                  "flow": "error"
                                                              }
                                                        },
                                                        {
                                                            "key": "SF",
                                                            "value": {
                                                                "nodetype": "multibinning",
                                                                "inputs": [
                                                                    "eta",
                                                                    "pt"
                                                                ],
                                                                "edges": [
                                                                    eta_edges,
                                                                    pt_edges
                                                                ],
                                                                "content": Trigger_SF_up,
                                                                "flow": "error"
                                                            }
                                                      }]
                                                        }
                                                },
                                    {
                                        "key": "down",
                                        "value": {
                                                        "nodetype": "category",
                                                        "input": "type",
                                                        "content": [

                                                          {
                                                              "key": "EfficiencyData",
                                                              "value": {
                                                                  "nodetype": "multibinning",
                                                                  "inputs": [
                                                                      "eta",
                                                                      "pt"
                                                                  ],
                                                                  "edges": [
                                                                      eta_edges,
                                                                      pt_edges
                                                                  ],
                                                                  "content": Trigger_Eff_Data_down,
                                                                  "flow": "error"
                                                              }
                                                        },
                                                        {
                                                            "key": "EfficiencyMC",
                                                            "value": {
                                                                "nodetype": "multibinning",
                                                                "inputs": [
                                                                    "eta",
                                                                    "pt"
                                                                ],
                                                                "edges": [
                                                                    eta_edges,
                                                                    pt_edges
                                                                ],
                                                                "content": Trigger_Eff_MC_down,
                                                                "flow": "error"
                                                            }
                                                      },
                                                        {
                                                            "key": "SF",
                                                            "value": {
                                                                "nodetype": "multibinning",
                                                                "inputs": [
                                                                    "eta",
                                                                    "pt"
                                                                ],
                                                                "edges": [
                                                                    eta_edges,
                                                                    pt_edges
                                                                ],
                                                                "content": Trigger_SF_down,
                                                                "flow": "error"
                                                            }
                                                      }]
                                                        }
                                                }]
                                            }
                                }
                            ]
                      }

    with open("scalefactors/Trigger_Efficiency_SF{}.json".format(year), "w") as outfile:
        json.dump(dict, outfile,indent = 4)


def plot_trigger_SF(year):

    file = uproot.open("scalefactors/Trigger_SF{}.root".format(year))

    pt_bins = file["Trigger_Eff_Data"].axis(0).edges()
    pt_center = (pt_bins[1:]+pt_bins[:-1])/2
    eta_bins = file["Trigger_Eff_Data"].axis(1).edges()

    Trigger_Eff_Data = file["Trigger_Eff_Data"].values()
    Trigger_Eff_Data_up = file["Trigger_Eff_Data_up"].values()-Trigger_Eff_Data
    Trigger_Eff_Data_down = Trigger_Eff_Data-file["Trigger_Eff_Data_down"].values()

    Trigger_Eff_MC = file["Trigger_Eff_MC"].values()
    Trigger_Eff_MC_up = file["Trigger_Eff_MC_up"].values()
    Trigger_Eff_MC_down = file["Trigger_Eff_MC_down"].values()


    colors = ["tab:red","tab:green","tab:blue","tab:orange","tab:purple","tab:olive","tab:pink"]
    for i in range(len(eta_bins)-1):
        hep.style.use("CMS")
        fig,[ax1,ax2] = plt.subplots(2,gridspec_kw={'height_ratios': [6, 1.5]})
        ax1.step(pt_bins,np.insert(Trigger_Eff_MC[i], 0, Trigger_Eff_MC[i][0]),color = "blue", label = "MC",where = 'pre')
        ax1.errorbar(pt_center,Trigger_Eff_Data[i],yerr= [Trigger_Eff_Data_down[i],Trigger_Eff_Data_up[i]], fmt='.k', label = "JetMET Data")
        ax1.fill_between(pt_bins,np.insert(Trigger_Eff_MC_down[i], 0, Trigger_Eff_MC_down[i][0]),np.insert(Trigger_Eff_MC_up[i], 0, Trigger_Eff_MC_up[i][0]), step='pre',color = "tab:blue", alpha=0.35,hatch="xx")

        ax2.errorbar(pt_center,Trigger_Eff_Data[i]/Trigger_Eff_MC[i],yerr = [Trigger_Eff_Data_down[i]/Trigger_Eff_MC[i],Trigger_Eff_Data_up[i]/Trigger_Eff_MC[i]], fmt='.k',label = "Scale Factor")
        ax2.fill_between(pt_bins,np.insert(Trigger_Eff_MC_down[i]/Trigger_Eff_MC[i], 0, (Trigger_Eff_MC_down[i]/Trigger_Eff_MC[i])[0]),np.insert(Trigger_Eff_MC_up[i]/Trigger_Eff_MC[i], 0, (Trigger_Eff_MC_up[i]/Trigger_Eff_MC[i])[0]), step='pre',color = "tab:blue", alpha=0.35,hatch="xx")

        ax1.grid()
        ax1.legend()
        ax2.grid()
        ax2.legend()
        ax1.set_xticks(pt_bins)
        ax2.set_xticks(pt_bins)
        ax2.set_xticklabels(np.append(pt_bins.astype(str)[:-1],"inf"))
        ax1.set_xticklabels(["" for _ in pt_bins])
        ax2.set_xlabel("Leading Lepton Pt")
        ax1.set_ylabel("Efficiency(%)/(bin)")
        ax2.set_ylabel("SF")
        ax1.set_xlim(pt_bins[0],pt_bins[-1])
        ax2.set_xlim(pt_bins[0],pt_bins[-1])
        if year == 2018:
            hep.cms.label(label ="Trigger Efficiency, eta = [{}-{}]".format(eta_bins[i],eta_bins[i+1]),ax=ax1,data = True,rlabel= "2018UL")
        elif year == 2022:
            hep.cms.label(label ="Trigger Efficiency, eta = [{}-{}]".format(eta_bins[i],eta_bins[i+1]),ax=ax1,data = True,rlabel= "2022")
        fig.savefig("scalefactors/json_plots/Trigger_Efficiency{}_{}.png".format(year,i))

def Histogram2D(bins,folder_date,year):

    Info = Analysis(year)

    tfile = ROOT.TFile("scalefactors/Trigger_Histograms{}.root".format(year), "RECREATE")

    hist = {}
    for i,label in enumerate(Info.MClabels):
        df = RDataFrame("Events_nom", "Event_Folders/Post_Merge/Post_Merge_{}/{}.root".format(folder_date,label))



        df = df.Define("abseta","abs(leading_lepton_eta)")

        df_denominator = df.Filter("Pass_Reference_Trigger==1", "Must Pass Reference Triggers")
        df_nominator = df_denominator.Filter("Pass_Lepton_Trigger==1", "Must Pass Lepton Triggers")



        if i==0:
            hist["denominator_mc"] = book2DHistogram_DATA(df_denominator, bins)
            hist["nominator_mc"] = book2DHistogram_DATA(df_nominator, bins)

        else:
            hist["denominator_mc"].Add(book2DHistogram_DATA(df_denominator, bins).GetPtr())
            hist["nominator_mc"].Add(book2DHistogram_DATA(df_nominator, bins).GetPtr())



    df_denominator = RDataFrame("Events_nom", "Event_Folders/Post_Merge/Post_Merge_{}/REFDATA.root".format(folder_date))
    df_denominator = df_denominator.Define("abseta","abs(leading_lepton_eta)")
    df_nominator = df_denominator.Filter("Pass_Lepton_Trigger==1", "Must Pass Lepton Triggers")

    hist["denominator_data"] = book2DHistogram_DATA(df_denominator, bins)
    hist["nominator_data"] = book2DHistogram_DATA(df_nominator, bins)
        #df_denominator = df.Filter("Pass_Reference_Trigger==1", "Must Pass Reference Triggers")


    for name in hist.keys():
        writeHistogram(hist[name], name)

    tfile.Close()


    with uproot.recreate("scalefactors/Trigger_SF{}.root".format(year)) as output_file:

        file = uproot.open("scalefactors/Trigger_Histograms{}.root".format(year))

        pt_bins = file["denominator_data"].axis(0).edges()
        eta_bins = file["denominator_data"].axis(1).edges()

        denominator_data = file["denominator_data"].values()
        nominator_data = file["nominator_data"].values()
        denominator_mc = file["denominator_mc"].values()
        nominator_mc = file["nominator_mc"].values()

        lo_data,hi_data = clopper_pearson(nominator_data,denominator_data)
        lo_mc,hi_mc = clopper_pearson(nominator_mc,denominator_mc)

        print("number of data events: {}".format(np.sum(denominator_data)))
        print("number of passed data events: {}".format(np.sum(nominator_data)))
        output_file["Trigger_Eff_Data"] = nominator_data/denominator_data,pt_bins,eta_bins
        output_file["Trigger_Eff_Data_up"] = hi_data,pt_bins,eta_bins
        output_file["Trigger_Eff_Data_down"] = lo_data,pt_bins,eta_bins
        output_file["Trigger_Eff_MC"] = nominator_mc/denominator_mc,pt_bins,eta_bins
        output_file["Trigger_Eff_MC_up"] = hi_mc,pt_bins,eta_bins
        output_file["Trigger_Eff_MC_down"] = lo_mc,pt_bins,eta_bins


        output_file["Trigger_SF"] = (nominator_data/denominator_data)/(nominator_mc/denominator_mc),pt_bins,eta_bins
        output_file["Trigger_SF_up"] = hi_data/(nominator_mc/denominator_mc),pt_bins,eta_bins
        output_file["Trigger_SF_down"] = lo_data/(nominator_mc/denominator_mc),pt_bins,eta_bins

        file.close()



def TriggerFromScratch(file):

    tfile = ROOT.TFile("scalefactors/Trigger_Histograms2018.root", "RECREATE")

    hist = {}
    df = RDataFrame("Events", file)

    ROOT.gInterpreter.Declare("""
            float LeadingLeptonPt(const float Electron_pt, float Muon_pt)
            {
                if (Electron_pt >= Muon_pt) {
                        return Electron_pt;
                    } else {
                        return Muon_pt;
                    }
            }
            """)

    df = df.Define("ObjSelectedElectron", "abs(Electron_eta) < 2.4 && Electron_pt > 10 && (abs(Electron_eta+Electron_deltaEtaSC)> 1.566 || abs(Electron_eta+Electron_deltaEtaSC) < 1.444 ) && Electron_mvaFall17V2Iso_WP80 & Electron_convVeto")
    df = df.Define("ObjSelectedMuon","abs(Muon_eta) < 2.4 && Muon_pt > 10 && Muon_tightId && Muon_pfIsoId >= 4")
    df = df.Filter("Sum(ObjSelectedElectron)+Sum(ObjSelectedMuon) >=3")
    df = df.Define("LeadingElectron", "Max(Electron_pt[ObjSelectedElectron])").Define("LeadingMuon", "Max(Muon_pt[ObjSelectedMuon])")
    df = df.Define("leading_lepton_pt","LeadingLeptonPt(LeadingElectron,LeadingMuon)")

    df_denominator = df.Filter("HLT_PFHT1050 || HLT_AK8PFJet500 || HLT_PFJet500 ||HLT_PFMET120_PFMHT120_IDTight || HLT_PFMETTypeOne140_PFMHT140_IDTight || HLT_DiJet110_35_Mjj650_PFMET110 || HLT_PFHT800_PFMET75_PFMHT75_IDTight ||HLT_PFHT700_PFMET85_PFMHT85_IDTight ||HLT_PFHT500_PFMET100_PFMHT100_IDTight ||HLT_TripleJet110_35_35_Mjj650_PFMET110", "Must Pass Reference Triggers")
    df_nominator = df_denominator.Filter("HLT_TripleMu_10_5_5_DZ || HLT_Mu37_TkMu27 || HLT_TripleMu_12_10_5 || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu27_Ele37_CaloIdL_MW || HLT_Mu37_Ele27_CaloIdL_MW || HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ || HLT_Mu8_DiEle12_CaloIdL_TrackIdL || HLT_IsoMu24 || HLT_IsoMu27 || HLT_Mu50 || HLT_Ele32_WPTight_Gsf || HLT_Ele115_CaloIdVT_GsfTrkIdT || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_DoubleEle25_CaloIdL_MW || HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL", "Must Pass Lepton Triggers")

    df.Report().Print()

    #hist["denominator"] = book2DHistogram_DATA(df_denominator,5)
    ##hist["nominator"] = book2DHistogram_DATA(df_nominator,5)
    #for name in hist.keys():
    #    writeHistogram(hist[name], name)

    #tfile.Close()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file', nargs=1, required = True)
    args = parser.parse_args()
    file = args.file[0]
    TriggerFromScratch(file)

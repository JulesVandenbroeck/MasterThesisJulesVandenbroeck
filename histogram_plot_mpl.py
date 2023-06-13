import numpy as np
import uproot
import seaborn as sns
import matplotlib.pyplot as plt
import mplhep as hep
import os
from matplotlib.backends.backend_pdf import PdfPages
from Analysis_Info import Analysis

labels = {
        "Binning": "Final Binning",
        "leading_lepton_pt": "leading lepton pT (GeV)",
        "subleading_lepton_pt": "subleading lepton pT (GeV)",
        "subsubleading_lepton_pt": "susubleading lepton pT (GeV)",
        "leading_lepton_eta": "leading lepton eta",
        "leading_lepton_phi": "leading lepton phi",
        "nJets": "number of Jets",
        "nBJets": "number of BJets",
        "raw_HT": "Jet HT (GeV)",
        "leading_jet_pt": "leading Jet pT (GeV)",
        "leading_jet_eta": "leading Jet Eta",
        "nElectron": "number of Electrons",
        "mll": "m(ll) (GeV)",
        "mlll": "m(lll) (GeV)",
        "min_mll": "min m(ll) (GeV)",
        "MT": "MT",
        "MET_pt": "MET pT (GeV)",
        "nMuon": "Total Yield",
        "Zpt": "Z-boson pT (GeV)",
        "max_sip3d": "max sip3d (cm)",
        "WZ_Binning": "Z-boson pT (GeV)",
        }


default_nbins = 9
ranges = {
        "TTZ_SR": {
            "Binning": (12,-0.5,11.5),
            "leading_lepton_pt": (default_nbins, 40, 250),
            "subleading_lepton_pt": (default_nbins, 20, 150),
            "subsubleading_lepton_pt": (default_nbins, 10, 100),
            "leading_lepton_eta": (default_nbins, -2.4,2.4),
            "nJets": (3, 2.5, 5.5),
            "nBJets": (2, 0.5, 2.5),
            "raw_HT": (default_nbins, 300, 1500),
            "leading_jet_pt": (default_nbins, 30, 500),
            "nElectron": (4,-0.5,3.5) ,
            "mll": (default_nbins, 91.1876-10, 91.1876+10),
            "min_mll": (default_nbins,12,80),
            "mlll": (default_nbins, 50, 400),
            "MT": (default_nbins,0,200),
            "MET_pt":(default_nbins,0,200),
            "Zpt": (default_nbins,0,200),
            "nMuon":(1,-1,5),
            "max_sip3d": (20,0,10),
        },

        "CR_WZ": {
            "WZ_Binning": (6,-0.5,5.5),
            "leading_lepton_pt": (default_nbins, 40, 250),
            "subleading_lepton_pt": (default_nbins, 20, 150),
            "subsubleading_lepton_pt": (default_nbins, 10, 100),
            "leading_lepton_eta": (default_nbins, -2.4,2.4),
            "nJets": (3, 0.5, 3.5),
            "nBJets": (2, -0.5, 1.5),
            "raw_HT": (default_nbins, 0, 1000),
            "leading_jet_pt": (default_nbins, 30, 500),
            "nElectron": (4,-0.5,3.5) ,
            "mll": (default_nbins, 91.1876-10, 91.1876+10),
            "min_mll": (default_nbins,0,80),
            "mlll": (default_nbins, 50, 400),
            "MT": (default_nbins,0,200),
            "MET_pt":(default_nbins,0,200),
            "Zpt": (default_nbins,0,200),
            "nMuon":(1,-1,5),
        },

        "No_Jetcut": {"nJets": (5, 0.5, 5.5),
        "nMuon":(1,-1,5),},
        "No_BJetcut": {"nJets": (5, 0.5, 5.5),
                       "nBJets": (3, -0.5, 2.5),
                       "nMuon":(1,-1,5),},
        "No_HTcut": {"nBJets": (3, -0.5, 2.5),
                     "raw_HT": (20, 0, 1000),
                     "nMuon":(1,-1,5),},
        "No_max_sip3dcut": {"max_sip3d": (20,0,10),
                            "nMuon":(1,-1,5),}
}

#"Drell Yan": ("DYJetsToLL_M_10to50_TuneCP5_13TeV","DYJetsToLL_M_50_TuneCP5_13TeV",)
colours = {                 "TTZ": "gold",
                            "NonPrompt": "cornflowerblue",
                            "WZ": "mediumpurple",
                            "ZZ": "tab:olive",
                            "OtherT": "violet",
                            "VVV": "green",
                            "TTX": "pink",
                    }



event_types_mc_labels = ("NonPrompt","TTX","OtherT","WZ","ZZ","VVV","TTZ")

SF_comparison_variables = { "Btagging_SF": ["nBJets","nJets"],
                            "Electron_SF": ["nElectron","leading_lepton_pt","leading_lepton_eta"],
                            "Muon_SF": ["nElectron","leading_lepton_pt","leading_lepton_eta"]}


Systematics = {

                "Electron_SF": {                "binned": True,
                                                "value": None},

                "Muon_SF": {                    "binned": True,
                                                "value": None},

                "PileUp_SF": {                  "binned": True,
                                                "value": None},

                #"PileUpId_SF": {                "binned": True,
                #                                "value": None},

                "BtaggingComb_SF": {            "binned": True,
                                                "value": None},

                "BtaggingIncl_SF": {            "binned": True,
                                                "value": None},

                "Normalisation": {              "binned": False,
                                                "value": {   "TTZ": 0.15,"NonPrompt": 0.50,"WZ": 0.30,"ZZ": 0.30,"OtherT": 0.15,"VVV": 0.50,"TTX": 0.15}
                                                },

                "JEC": {                        "binned": True,
                                                "value": None},

                "JER": {                        "binned": True,
                                                "value": None},

                "LHEScaleWeight": {             "binned": True,
                                                "value": None},

                "LHEPdfWeight": {               "binned": True,
                                                "value": None},

                "PSWeightISR": {             "binned": True,
                                                "value": None},

                "PSWeightFSR": {               "binned": True,
                                                "value": None},

                "Luminosity": {                 "binned": False,
                                                "value": 0.025},

                "Trigger_SF": {                 "binned": False,
                                                "value": 0.030} }

def get_histograms(Info,input_histogram_file,label,variable):
    if variable in ("nElectron","leading_lepton_eta","leading_jet_eta","mll","nMuon","Binning","WZ_Binning"):
        flow_value = False
        start_value = 0
    elif variable in ("leading_lepton_dxy",):
        flow_value = True
        start_value = 0
    else:
        flow_value = True
        start_value = 1


    with uproot.open(input_histogram_file+"/{}.root".format(label)) as hist_file:
        bins = hist_file["{}_nom".format(variable)].axis().edges(flow=flow_value)[start_value:]
        nbins = len(bins)-1
        mc = np.maximum(hist_file["{}_nom".format(variable)].values(flow=flow_value)[start_value:],np.zeros(nbins))
        mc_up = np.maximum(hist_file["{}_nom".format(variable)].errors(flow=flow_value)[start_value:],np.zeros(nbins))
        mc_down = np.maximum(hist_file["{}_nom".format(variable)].errors(flow=flow_value)[start_value:],np.zeros(nbins))
        for Systematic in Systematics.keys():
            if Systematics[Systematic]["binned"]:
                #print("{} down: {}".format(Systematic,np.sum(hist_file["{}_{}down".format(variable,Systematic)].values(flow=flow_value)[start_value:])))
                up_err = (hist_file["{}_{}up".format(variable,Systematic)].values(flow=flow_value)[start_value:]-mc)
                down_err = (hist_file["{}_{}down".format(variable,Systematic)].values(flow=flow_value)[start_value:]-mc)

                if Systematic in ("JEC","JER"):
                    err = (np.abs(up_err)+np.abs(down_err))*0.5
                    up_err = err
                    down_err = err
            else:
                if Systematic == "Normalisation":
                    up_err = Systematics[Systematic]["value"][label]*mc
                    down_err = Systematics[Systematic]["value"][label]*mc
                else:
                    up_err = Systematics[Systematic]["value"]*mc
                    down_err = Systematics[Systematic]["value"]*mc
            #print("{} has down error: {}".format(Systematic,down_err[0]))
            mc_up = np.sqrt((up_err)**2+mc_up**2)
            mc_down = np.sqrt((down_err)**2+mc_down**2)
    return bins, mc,mc_up,mc_down

def main_histograms(folder_date,comparison):

    Info = Analysis()

    if not os.path.exists("Histograms/Histograms_{}".format(folder_date)):
        os.mkdir("Histograms/Histograms_{}".format(folder_date))

    for region in ranges.keys():
        print()
        print("region: {}".format(region))

        figs = []
        input_histogram_file = "Event_Folders/histograms_folders/histograms_{}/{}".format(folder_date,region)
        output_histogram_file = "Histograms/Histograms_{}/{}".format(folder_date,region)
        if not os.path.exists(output_histogram_file):
            os.mkdir(output_histogram_file)
        for variable in ranges[region].keys():
            hep.style.use("CMS")
            fig,[ax1,ax2] = plt.subplots(2,figsize = (16,16),gridspec_kw={'height_ratios': [6, 1.5]})

            if variable in ("nElectron","leading_lepton_eta","leading_jet_eta","mll","nMuon","Binning","WZ_Binning"):
                flow_value = False
                start_value = 0
            elif variable in ("leading_lepton_dxy"):
                flow_value = True
                start_value = 0
            else:
                flow_value = True
                start_value = 1

            for i,label in enumerate(event_types_mc_labels):
                bins, mc,mc_up,mc_down = get_histograms(Info,input_histogram_file,label,variable)
                if variable == "nMuon":
                    print("{}: {}".format(label,mc[0]))

                if flow_value:
                    bins[-1] =2*bins[-2]- bins[-3]
                    if start_value == 0:
                        bins[0] = 2*bins[1]-bins[2]

                if i == 0:
                    total_mc = mc
                    total_mc_up = mc_up
                    total_mc_down = mc_down

                    ax1.step(bins,np.insert(mc, 0, mc[0]),color = "black",where = 'pre')
                    ax1.stairs(mc,bins, label = label,fill = True, color = colours[label],zorder=-1)
                else:

                    if label == "TTZ" and variable == "nMuon" and region == "TTZ_SR":
                        sgn = [mc[0],mc_up[0],mc_down[0]]
                        bkg = [total_mc[0],total_mc_up[0],total_mc_down[0]]
                    total_mc = mc+total_mc
                    total_mc_up = np.sqrt(mc_up**2+total_mc_up**2)
                    total_mc_down = np.sqrt(mc_down**2+total_mc_down**2)

                    ax1.step(bins,np.insert(total_mc, 0, total_mc[0]),color = "black",where = 'pre')
                    ax1.stairs(total_mc,bins,baseline = base,label = label,fill = True, color = colours[label],zorder=-1)

                base = total_mc


            total_mc_up = total_mc + total_mc_up
            total_mc_down = total_mc - total_mc_down
            total_mc_down = np.maximum(total_mc_down,np.zeros(len(bins)-1))

            if variable == "nMuon":
                print("total mc up: ",total_mc_up)
                print("total mc: ",total_mc)
                print("total mc down: ",total_mc_down)
                print()
            ax1.fill_between(bins,np.append(total_mc_down,total_mc_down[-1]),np.append(total_mc_up,total_mc_up[-1]) , step='post',hatch="xx", color='grey',zorder=1, alpha=0.35,label = 'uncertainty')


            with uproot.open(input_histogram_file+"/DATA.root") as hist_file:
                total_data = hist_file[variable].values(flow = flow_value)[start_value:]
                error_data = hist_file[variable].errors(flow = flow_value)[start_value:]

            if label == "TTZ" and variable == "nMuon" and region == "TTZ_SR":
                print("signal strength measurement:")
                print(sgn)
                print(bkg)
                print(total_data[0],error_data[0])
            center = (bins[1:]+bins[:-1])/2
            diff = (bins[:-1]-bins[1:])

            ax1.errorbar(center-diff*0.2,total_data,yerr=error_data,fmt='.r',label ="2022 Data")
            if comparison == 1:
                with uproot.open("Event_Folders/histograms_folders/histograms_230512_154934/{}/DATA.root".format(region)) as hist_file:
                    total_2018data = hist_file[variable].values(flow = flow_value)[start_value:]*0.66
                    error_2018data = hist_file[variable].errors(flow = flow_value)[start_value:]*0.66

                ax1.errorbar(center+diff*0.2,total_2018data,yerr=error_2018data ,fmt='.k',label ="2018D Data (x0.66)")
                #ax2.errorbar(center,total_data/total_2018data, yerr = (total_data/total_2018data)*np.sqrt((error_data/total_data)**2+(error_2018data/total_2018data)**2),fmt='.k')

                #ax2.plot(bins,np.ones(len(bins))*(21128/31800),color = "red", label ="Lumi Ratio")
                ax2.errorbar(center-diff*0.2,total_data/total_mc,yerr = error_data/total_mc,fmt='.r')
                #ax2.errorbar(center+diff*0.2,total_2018data/total_mc,yerr = error_data/total_mc,fmt='.k')
                ax2.fill_between(bins,np.append(total_mc_down/total_mc,(total_mc_down/total_mc)[-1]),np.append(total_mc_up/total_mc,(total_mc_up/total_mc)[-1]) , step='post',hatch="xx", color='grey',zorder=1, alpha=0.35)
                ax2.set_ylabel("Data/MC.")
            else:
                ax2.errorbar(center,total_data/total_mc,yerr = error_data/total_mc,fmt='.k')
                ax2.fill_between(bins,np.append(total_mc_down/total_mc,(total_mc_down/total_mc)[-1]),np.append(total_mc_up/total_mc,(total_mc_up/total_mc)[-1]) , step='post',hatch="xx", color='grey',zorder=1, alpha=0.35)
                ax2.set_ylabel("Data/MC.")

            ax1.set_ylabel("Events")
            #ax2.set_ylim(0.0,2.0)
            if variable in ("nJets","nBJets","nElectron","Binning","WZ_Binning"):
                ax1.set_xticks(bins + 0.5)
                ax2.set_xticks(bins + 0.5)
                if variable in ("nJets", "nBJets"):
                     ax1.set_xticklabels(["" for _ in bins])
                     ax2.set_xticklabels(np.append((bins+0.5).astype(str)[:-1],"{}+".format(bins[-1]+0.5)))
                elif variable in ("Binning",):
                    ax2.set_xticklabels(["" for _ in bins])
                    ax1.set_xticklabels(["3J","4J",">5J","3J","4J",">5J","3J","4J",">5J","3J","4J",">5J",""])

                    ax1.plot([2.5,2.5],[0,np.amax(total_mc)-10],linestyle='dashed',color ="grey")
                    ax1.plot([8.5,8.5],[0,np.amax(total_mc)-10],linestyle='dashed',color ="grey")
                    ax1.plot([5.5,5.5],[0,np.amax(total_mc)+10],linestyle='dashed',color ="black")

                    #ax1.text(0.8,np.amax(total_mc)-15,"1 BJet",fontweight ="semibold")
                    #ax1.text(3.5,np.amax(total_mc)-15,">1 BJet",fontweight ="semibold")
                    #ax1.text(6.8,np.amax(total_mc)-20,"1 BJet",fontweight ="semibold")
                    #ax1.text(9.5,np.amax(total_mc)-20,">1 BJet",fontweight ="semibold")
                    #ax1.text(1.4,np.amax(total_mc)-10,"pt < 100 GeV",fontweight ="bold")
                    #ax1.text(7.4,np.amax(total_mc)-15,"pt > 100 GeV",fontweight ="bold")
                elif variable == "WZ_Binning":
                    ax1.set_xlabel("Z boson pT (GeV)")
                    ax1.set_xticklabels(["0","100","200","0","100","200",""])
                    ax1.plot([2.5,2.5],[0,np.amax(total_mc)+10],linestyle='dashed',color ="grey")
                    ax1.text(0.8,np.amax(total_mc)-15,"2 Jets",fontweight ="semibold")
                    ax1.text(3.5,np.amax(total_mc)-15,">2 Jets",fontweight ="semibold")
                else:
                    ax1.set_xticklabels(["" for _ in bins])
                    ax2.set_xticklabels(bins + 0.5)

            elif variable != "nMuon":
                ax1.set_xticks(bins[::2])
                ax2.set_xticks(bins[::2])
                ax1.set_xticklabels(["" for _ in bins[::2]])
                if variable in ("leading_jet_eta","leading_lepton_eta","leading_lepton_phi"):
                    ax2.set_xticklabels(["{:.2f}".format(bin) for bin in bins[::2]])
                elif variable in ("leading_lepton_dxy"):
                    ax2.set_xticklabels(["{:.4f}".format(bin) for bin in bins[::2]])
                else:
                    ax2.set_xticklabels(["{:.1f}".format(bin) for bin in bins[::2]])
            ax1.set_xlim(min(bins),max(bins))
            ax2.set_xlim(min(bins),max(bins))
            ax1.grid()
            ax1.legend()
            ax2.grid()
            ax2.set_xlabel(labels[variable])
            if comparison == 0:
                ax2.set_ylim(0,2)
                hep.cms.label(label ="Private",ax=ax1,data = True,rlabel= "31.8 fb-1, sqrt(s) = 13TeV")
            elif comparison == 1:
                ax2.set_ylim(0,2)
                hep.cms.label(label ="Private",ax=ax1,data = True,rlabel= "21.1 fb-1 (13.6TeV) & 31.8 fb-1 (13TeV)")

            #hep.cms.label(label ="Private",ax=ax1,data = True,rlabel= "31.8 fb-1, sqrt(s) = 13TeV")
            figs.append(fig)
            fig.savefig("{}/{}".format(output_histogram_file,variable))

        with PdfPages(output_histogram_file+'/histograms.pdf') as pdf:
            for fig in figs:
                pdf.savefig(fig)
                plt.close()







def PostFitPlot(folder_date,PostFitFile):

    output_histogram_file = "Histograms/Histograms_{}".format(folder_date)
    with uproot.open("{}".format(PostFitFile)) as file:

        print("plotting PostFit for Final Binning................")
        hep.style.use("CMS")
        fig,[ax1,ax2] = plt.subplots(2,figsize = (16,16),gridspec_kw={'height_ratios': [6, 1.5]})


        for i,label in enumerate(event_types_mc_labels):
            mc = file["crz_postfit/{}".format(label)].values()
            bins =  file["crz_postfit/{}".format(label)].axis().edges()
            if i == 0:
                ax1.step(bins,np.insert(mc, 0, mc[0]),color = "black",where = 'pre')
                ax1.stairs(mc,bins,label = label,fill = True, color = colours[label],zorder=-1)
                base = mc
            else:
                total_mc = base + mc
                ax1.step(bins,np.insert(total_mc, 0, total_mc[0]),color = "black",where = 'pre')
                ax1.stairs(total_mc,bins,baseline = base,label = label,fill = True, color = colours[label],zorder=-1)
                base = total_mc


        total_mc_down = total_mc - file["crz_postfit/TotalProcs"].errors()
        total_mc_up = total_mc + file["crz_postfit/TotalProcs"].errors()
        ax1.fill_between(bins,np.append(total_mc_down,total_mc_down[-1]),np.append(total_mc_up,total_mc_up[-1]) , step='post',hatch="xx", color='grey',zorder=1, alpha=0.35,label = 'uncertainty')

        data = file["crz_postfit/data_obs".format(label)].values()
        error_data = file["crz_postfit/data_obs".format(label)].errors()

        center = (bins[1:]+bins[:-1])/2
        ax1.errorbar(center,data,yerr=error_data,fmt='.k',label ="Data")
        ax2.errorbar(center, data/total_mc,yerr=error_data/total_mc,fmt='.k')
        ax2.fill_between(bins,np.append(total_mc_down/total_mc,(total_mc_down/total_mc)[-1]),np.append(total_mc_up/total_mc,(total_mc_up/total_mc)[-1]) , step='post',hatch="xx", color='grey',zorder=1, alpha=0.35,label = 'uncertainty')


        ax1.set_ylabel("Events")
        ax2.set_ylabel("Data/Pred.")
        ax1.set_xticks(bins + 0.5)
        ax2.set_xticks(bins + 0.5)
        ax2.set_xticklabels(["" for _ in bins])
        if PostFitFile == "TTZPostFIT.root":
            ax1.set_xticks(bins + 0.5)
            ax2.set_xticks(bins + 0.5)
            ax1.set_xticklabels(["3J","4J",">5J","3J","4J",">5J","3J","4J",">5J","3J","4J",">5J",""])

            ax1.plot([2.5,2.5],[0,np.amax(total_mc)-20],linestyle='dashed',color ="grey")
            ax1.plot([8.5,8.5],[0,np.amax(total_mc)-20],linestyle='dashed',color ="grey")
            ax1.plot([5.5,5.5],[0,np.amax(total_mc)+10],linestyle='dashed',color ="black")

            ax1.text(0.8,np.amax(total_mc)-15,"1 BJet",fontweight ="semibold")
            ax1.text(3.5,np.amax(total_mc)-15,">1 BJet",fontweight ="semibold")
            ax1.text(6.8,np.amax(total_mc)-20,"1 BJet",fontweight ="semibold")
            ax1.text(9.5,np.amax(total_mc)-20,">1 BJet",fontweight ="semibold")
            ax1.text(1.4,np.amax(total_mc)-10,"pt < 100 GeV",fontweight ="bold")
            ax1.text(7.4,np.amax(total_mc)-15,"pt > 100 GeV",fontweight ="bold")

        else:
            ax1.set_xlabel("Z boson pT (GeV)")
            ax1.set_xticklabels(["0","100","200","0","100","200",""])
            ax1.plot([2.5,2.5],[0,np.amax(total_mc)+10],linestyle='dashed',color ="grey")
            ax1.text(0.8,np.amax(total_mc)-15,"2 Jets",fontweight ="semibold")
            ax1.text(3.5,np.amax(total_mc)-15,">2 Jets",fontweight ="semibold")

        ax1.set_xlim(min(bins),max(bins))
        ax2.set_xlim(min(bins),max(bins))
        ax1.grid()
        ax1.legend()
        ax2.grid()
        hep.cms.label(label ="Private, PostFit",ax=ax1,data = True,rlabel= "31.8 fb-1 (13TeV)")
        fig.savefig("{}/WZPostFitPlot".format(output_histogram_file))



def MediumIDComparisonPlot(folder_date):

    variable = "leading_lepton_pt"
    hep.style.use("CMS")
    fig,ax = plt.subplots(figsize = (16,12))

    for i,label in enumerate(event_types_mc_labels):
        with uproot.open("Event_Folders/histograms_folders/histograms_{}/No_cuts/{}.root".format(folder_date,label)) as hist_file:
            bins = hist_file["{}_nom".format(variable)].axis().edges(flow=1)[1:]
            bins[-1] =2*bins[-2]- bins[-3]
            nbins = len(bins)-1
            if label == "NonPrompt":
                nonprompt = np.maximum(hist_file["{}".format(variable)].values(flow=1)[1:],np.zeros(nbins))
            else:
                if i == 1:
                    prompt = np.maximum(hist_file["{}".format(variable)].values(flow=1)[1:],np.zeros(nbins))
                else:
                    prompt += np.maximum(hist_file["{}".format(variable)].values(flow=1)[1:],np.zeros(nbins))


    ax.step(bins,np.insert(nonprompt, 0, nonprompt[0]),color = "black",where = 'pre')
    ax.stairs(nonprompt,bins, label = "NonPrompt",fill = True, color = colours["NonPrompt"],zorder=-1)

    ax.step(bins,np.insert(nonprompt+prompt, 0, (nonprompt+prompt)[0]),color = "black",where = 'pre')
    ax.stairs(nonprompt+prompt,bins,baseline = nonprompt,label = "Prompt",fill = True, color = colours["TTZ"],zorder=-1)

    ax.set_yscale("log")
    ax.set_xticks(bins[::2])
    ax.set_xticklabels(["{:.1f}".format(bin) for bin in bins[::2]])
    ax.set_xlim(min(bins),max(bins))
    ax.set_ylim(bottom=None,top=5000)
    ax.grid()
    ax.legend()
    ax.set_xlabel("Highest lepton pT (GeV)")
    ax.set_ylabel("Events")
    if folder_date == "230605_111923":
        hep.cms.label(label ="Private, mediumID",ax=ax,data = True,rlabel= "All samples (13TeV)")
    else:
        hep.cms.label(label ="Private, tightID",ax=ax,data = True,rlabel= "All samples (13TeV)")

    fig.savefig("IDComparison_{}".format(folder_date))

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder_date', nargs=1, required = True)
    parser.add_argument('-c', '--comparison', nargs=1, required = True)
    parser.add_argument('-o', '--option', nargs=1, required = True)
    args = parser.parse_args()
    folder_date = args.folder_date[0]
    comparison = args.comparison[0]
    option = args.option[0]

    if option == "PREFIT":
        comparison = int(comparison)
        main_histograms(folder_date,comparison)
    elif option == "POSTFIT":
        PostFitPlot(folder_date,comparison)
    elif option == "ID":
        MediumIDComparisonPlot(folder_date)

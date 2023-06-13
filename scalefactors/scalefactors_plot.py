import numpy as np
import correctionlib._core as core
import seaborn as sns
import matplotlib.pyplot as plt
import mplhep as hep
import json

labels = {  "wp80iso": "Electron tightID SF",
            "RecoAbove20": "Electron Reconstruction SF",
            "NUM_TrackerMuons_DEN_genTracks": "Muon Reconstruction SF",
            "NUM_TightID_DEN_TrackerMuons": "Muon tightID SF",
            "NUM_TightRelIso_DEN_TightIDandIPCut": "Muon tightISO SF"}

def from_edges_get_eta_bins(eta_bins):
    if eta_bins[0] != 0.0:
        eta_bins[0] = -2.4
    eta_bins[-1] = 2.4
    eta_bins = np.array(eta_bins,dtype = np.float64)
    eta_bins = eta_bins[np.where(eta_bins == 0.0)[0][0]:]
    eta_get_output = eta_bins[:-1]+0.1
    return eta_bins, eta_get_output

def from_edges_get_pt_bins(pt_bins):
    pt_bins[-1] = pt_bins[-2]+50
    pt_bins = np.array(pt_bins,dtype = np.float64)
    pt_get_output = pt_bins[:-1]+0.1

    return pt_bins,pt_get_output

def plotting_scalefactors(json_file,type,workingpoint,JetFlavour):
    print((type,workingpoint,JetFlavour))

    with open("scalefactors/"+json_file) as json_file_unpacked:
        data = json.load(json_file_unpacked)
        for list1 in data["corrections"]:
            if type in ("deepCSV_incl","deepCSV_comb","Btagging_Efficiency"):
                print("finding the binning of a B tagging related json files")
                if list1["name"] == type:
                    print(type)
                    for list2 in list1["data"]["content"]:
                        if list2["key"] == "up":
                            for list3 in list2["value"]["content"]:
                                if list3["key"] == workingpoint:
                                    print(workingpoint)
                                    for list4 in list3["value"]["content"]:
                                        if list4["key"] == int(JetFlavour):
                                            print(JetFlavour)
                                            if type == "Btagging_Efficiency":
                                                eta_bins = list4["value"]["edges"][0]
                                                pt_bins = list4["value"]["edges"][1]
                                                print(eta_bins,pt_bins)
                                            else:
                                                eta_bins = list4["value"]["edges"]
                                                pt_bins = list4["value"]["content"][0]["edges"]
                                            eta_bins = np.array(eta_bins)
                                            eta_get_output = eta_bins[:-1]+0.1
                                            pt_bins,pt_get_output = from_edges_get_pt_bins(pt_bins)


            else:
                for list2 in list1["data"]["content"]:
                    if list2["key"] == "2018" or list2["key"] == "2018_UL":
                        if type == "NUM_TrackerMuons_DEN_genTracks" or type == "NUM_TightID_DEN_TrackerMuons" or type == "NUM_TightRelIso_DEN_TightIDandIPCut":

                            eta_bins = np.array(list2["value"]["edges"])
                            pt_bins = list2["value"]["content"][0]["edges"]

                            eta_get_output = eta_bins[:-1]+0.1
                            pt_bins,pt_get_output = from_edges_get_pt_bins(pt_bins)
                        else:
                            for list3 in list2["value"]["content"][0]["value"]["content"]:
                                if workingpoint == "RecoAbove20":
                                    if list3["key"] == "RecoAbove20":
                                        edges = list3["value"]["edges"]
                                        eta_bins,eta_get_output =  from_edges_get_eta_bins(edges[0])
                                        pt_binsAbove20,pt_get_outputAbove20 = from_edges_get_pt_bins(edges[1])
                                        pt_bins = np.insert(pt_binsAbove20, 0, 10., axis=0)
                                        pt_get_output = np.insert(pt_get_outputAbove20, 0, 10.1, axis=0)
                                else:
                                    if list3["key"] == workingpoint:
                                        edges = list3["value"]["edges"]
                                        eta_bins,eta_get_output =  from_edges_get_eta_bins(edges[0])
                                        pt_bins,pt_get_output = from_edges_get_pt_bins(edges[1])
                                    elif list3["key"] == int(JetFlavour):
                                        edges = list3["value"]["edges"]
                                        eta_bins,eta_get_output =  from_edges_get_eta_bins(edges[0])
                                        pt_bins,pt_get_output = from_edges_get_pt_bins(edges[1])

    print(pt_bins)
    print(eta_bins)
    hep.style.use("CMS")
    evaluator   = core.CorrectionSet.from_file("scalefactors/"+json_file)


    colors = ["tab:red","tab:green","tab:blue","tab:orange","tab:purple","tab:olive","tab:pink"]

    pt_output = np.zeros_like(pt_bins)
    pt_output_up = np.zeros_like(pt_bins)
    pt_output_down = np.zeros_like(pt_bins)
    for i,eta in enumerate(eta_get_output):
        fig,ax = plt.subplots(figsize = (16,10))
        if not 1.444<eta<1.566:
            for j,pt in enumerate(pt_get_output):
                if type in ("NUM_TrackerMuons_DEN_genTracks","NUM_TightID_DEN_TrackerMuons","NUM_TightRelIso_DEN_TightIDandIPCut"):
                    pt_output[j+1] = evaluator[type].evaluate("2018_UL",eta, pt,"sf")
                    pt_output_up[j+1] = evaluator[type].evaluate("2018_UL",eta, pt,"systup")
                    pt_output_down[j+1] = evaluator[type].evaluate("2018_UL",eta, pt,"systdown")
                elif type in ("deepCSV_incl","deepCSV_comb","Btagging_Efficiency"):
                    pt_output[j+1] = evaluator[type].evaluate("central",workingpoint,int(JetFlavour),eta,pt)
                    pt_output_up[j+1] = evaluator[type].evaluate("up",workingpoint,int(JetFlavour),eta,pt)
                    pt_output_down[j+1] = evaluator[type].evaluate("down",workingpoint,int(JetFlavour),eta,pt)
                else:
                    if workingpoint == "RecoAbove20" and pt<20.:
                        pt_output[j+1] = evaluator["UL-Electron-ID-SF"].evaluate("2018","sf","RecoBelow20",eta, pt)
                        pt_output_up[j+1] = evaluator["UL-Electron-ID-SF"].evaluate("2018","sfup","RecoBelow20",eta, pt)
                        pt_output_down[j+1] = evaluator["UL-Electron-ID-SF"].evaluate("2018","sfdown","RecoBelow20",eta, pt)
                    else:
                        pt_output[j+1] = evaluator["UL-Electron-ID-SF"].evaluate("2018","sf",workingpoint,eta, pt)
                        pt_output_up[j+1] = evaluator["UL-Electron-ID-SF"].evaluate("2018","sfup",workingpoint,eta, pt)
                        pt_output_down[j+1] = evaluator["UL-Electron-ID-SF"].evaluate("2018","sfdown",workingpoint,eta, pt)

            pt_output[0] = pt_output[1]
            pt_output_up[0] = pt_output_up[1]
            pt_output_down[0] = pt_output_down[1]

            ax.step(pt_bins,pt_output,color = "black", label = "{} < |eta| < {}".format(eta_bins[i],eta_bins[i+1]),where = 'pre')
            ax.fill_between(pt_bins,pt_output_down,pt_output_up , step='pre',hatch="xx", color='grey',zorder=1, alpha=0.35)
            ax.grid()
            ax.legend()
            ax.set_xscale("log")
            ax.set_xticks(pt_bins)
            ax.set_xticklabels(np.append(pt_bins.astype(str)[:-1],"inf"))
            ax.set_xlabel("lepton pT (GeV)")
            if type == "Btagging_Efficiency":
                ax.set_ylabel("Efficiency(%)/(bin)")

            else:
                ax.set_ylabel("scale factor/(bin)")
            ax.set_xlim(pt_bins[0],pt_bins[-1])
            #ax.set_ylim(0.9,1.1)
            if type in ("deepCSV_incl","deepCSV_comb","Btagging_Efficiency"):
                if int(JetFlavour) == 5:
                    hep.cms.label(label ="\t{} B-Jet".format(type),ax=ax,data = True,rlabel= "2018UL MC")
                    fig.savefig("json_plots/{}_{}_bjet.png".format(type,workingpoint))
                elif int(JetFlavour) == 4:
                    hep.cms.label(label ="\t{} C-Jet".format(type),ax=ax,data = True,rlabel= "2018UL")
                    fig.savefig("json_plots/{}_{}_cjet.png".format(type,workingpoint))
                else:
                    hep.cms.label(label ="\t{} UDSG-Jets".format(type),ax=ax,data = True,rlabel= "2018UL")
                    fig.savefig("json_plots/{}_{}.png".format(type,workingpoint))
            else:
                hep.cms.label(label ="Private, {}".format(labels[type]),ax=ax,data = True,rlabel= "2018 MC")
                fig.savefig("scalefactors/json_plots/{}_{}_{}.png".format(type,workingpoint,eta_bins[i]))



if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--json_file', nargs=1, required = True)
    parser.add_argument('-t', '--type', nargs=1, required = True)
    parser.add_argument('-w', '--workingpoint', nargs=1, required = True)
    parser.add_argument('-j', '--JetFlavour', nargs=1, required = True)
    args = parser.parse_args()
    json_file = args.json_file[0]
    type = args.type[0]
    workingpoint = args.workingpoint[0]
    JetFlavour = args.JetFlavour[0]

    plotting_scalefactors(json_file,type,workingpoint,JetFlavour)

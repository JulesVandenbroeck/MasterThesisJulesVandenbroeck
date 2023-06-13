import numpy as np
import uproot
import matplotlib.pyplot as plt
from ROOT import TLorentzVector
import os,subprocess
from itertools import combinations
from correctionlib import _core
import scipy.stats
import shutil
import json
from Analysis_Info import Analysis

submission_file = lambda args, logfolder, nfiles,i: """
executable = job_jet_tagging_efficiency.sh
arguments = "{0} $(Process)"
log = {1}/log_{3}_$(Process).txt
output = {1}/out_{3}_$(Process).txt
error = {1}/err_{3}_$(Process).txt
should_transfer_files = No
queue {2}
""".format(args, logfolder, nfiles,i)


def write_json(root_file,year):

    file = uproot.open(root_file)

    pt_edges = list(file["Btag_Eff"].axis(0).edges())
    eta_edges = list(file["Btag_Eff"].axis(1).edges())
    values_BJets = list(file["Btag_Eff"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    values_BJets_up = list(file["Btag_Eff_up"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    values_BJets_down = list(file["Btag_Eff_down"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))

    values_CJets = list(file["Ctag_Eff"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    values_CJets_up = list(file["Ctag_Eff_up"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    values_CJets_down = list(file["Ctag_Eff_down"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))

    values_UDSGJets = list(file["UDSGtag_Eff"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    values_UDSGJets_up = list(file["UDSGtag_Eff_up"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))
    values_UDSGJets_down = list(file["UDSGtag_Eff_down"].values().reshape((len(pt_edges)-1)*(len(eta_edges)-1), order='F'))

    dict = {
        "schema_version": 2,
        "description": "These are the btagging efficiencies of c-jets and b-jets",
        "corrections": [
            {
                "name": "Btagging_Efficiency",
                "description": "These are the btagging efficiencies of c-jets and b-jets",
                "version": 2,
                "inputs": [
                    {
                        "name": "systematic",
                        "type": "string",
                        "description": "central,up,down"
                    },
                    {
                        "name": "working_point",
                        "type": "string",
                        "description": "jet flavour"
                    },
                    {
                        "name": "jetFlavour",
                        "type": "int",
                        "description": "jet flavour"
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
                                            "input": "working_point",
                                            "content": [
                                                {
                                                "key": "M",
                                                "value": {
                                                        "nodetype": "category",
                                                        "input": "jetFlavour",
                                                        "content": [
                                                            {
                                                                "key": 5,
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
                                                                    "content": values_BJets,
                                                                    "flow": "error"
                                                                }
                                                          },
                                                          {
                                                              "key": 4,
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
                                                                  "content": values_CJets,
                                                                  "flow": "error"
                                                              }
                                                        },
                                                        {
                                                            "key": 0,
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
                                                                "content": values_UDSGJets,
                                                                "flow": "error"
                                                            }
                                                      }]
                                                        }
                                                }]
                                                }
                                    },

                                    {
                                        "key": "up",
                                        "value": {
                                            "nodetype": "category",
                                            "input": "working_point",
                                            "content": [
                                                {
                                                "key": "M",
                                                "value": {
                                                        "nodetype": "category",
                                                        "input": "jetFlavour",
                                                        "content": [
                                                            {
                                                                "key": 5,
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
                                                                    "content": values_BJets_up,
                                                                    "flow": "error"
                                                                }
                                                          },
                                                          {
                                                              "key": 4,
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
                                                                  "content": values_CJets_up,
                                                                  "flow": "error"
                                                              }
                                                        },
                                                        {
                                                            "key": 0,
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
                                                                "content": values_UDSGJets_up,
                                                                "flow": "error"
                                                            }
                                                      }]
                                                        }
                                                }]
                                                }
                                    },
                                    {
                                        "key": "down",
                                        "value": {
                                            "nodetype": "category",
                                            "input": "working_point",
                                            "content": [
                                                {
                                                "key": "M",
                                                "value": {
                                                        "nodetype": "category",
                                                        "input": "jetFlavour",
                                                        "content": [
                                                            {
                                                                "key": 5,
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
                                                                    "content": values_BJets_down,
                                                                    "flow": "error"
                                                                }
                                                          },
                                                          {
                                                              "key": 4,
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
                                                                  "content": values_CJets_down,
                                                                  "flow": "error"
                                                              }
                                                        },
                                                        {
                                                            "key": 0,
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
                                                                "content": values_UDSGJets_down,
                                                                "flow": "error"
                                                            }
                                                      }]
                                                        }
                                                }]
                                            }
                                }
                            ]
                      }
          }
    ]
}

    with open("scalefactors/Btagging_Efficiency{}.json".format(year), "w") as outfile:
        json.dump(dict, outfile,indent = 4)

def clopper_pearson(k,n,alpha=0.32):
    """
    http://en.wikipedia.org/wiki/Binomial_proportion_confidence_interval
    alpha confidence intervals for a binomial distribution of k expected successes on n trials
    Clopper Pearson intervals are a conservative estimate.
    """
    lo = scipy.stats.beta.ppf(alpha/2,k, n-k+1)
    hi = scipy.stats.beta.ppf(1 - alpha/2, k+1, n-k)
    return lo, hi

def main(year):
    Info = Analysis(year)
    savefolder = "Event_Folders/Jet_Tagging_Efficiency/{}".format(year)
    logfolder = "Log_Folders/Jet_Tagging_Efficiency_logs_{}".format(year)
    if os.path.exists(logfolder):
        shutil.rmtree(logfolder)
    if os.path.exists(savefolder):
        shutil.rmtree(savefolder)

    os.mkdir(logfolder)
    os.mkdir(savefolder)
    for i,DASFile in enumerate(Info.DASMCFiles):

        files = ["/pnfs/iihe/cms/ph/sc4/"+file+":Events" for file in subprocess.check_output('dasgoclient --query "file dataset={}"'.format(DASFile), shell=True,universal_newlines=True).rstrip("\n").split("\n")]
        nfiles = len(files)
        files = ",".join(files)

        submissionfilename = '{}/submit.sub'.format(logfolder)
        print("submitting Jobs for {} files".format(nfiles))
        with open(submissionfilename, 'w') as f:
            #print(submission_file(" ".join((filenames,directory, savefolder,"{}".format(i))), logfolder, nfiles,i))
            f.write(submission_file(" ".join((files, savefolder,"{} {}".format(i,year))), logfolder, nfiles,i))

        subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)


def combine(year):
    input_directory = "Event_Folders/Jet_Tagging_Efficiency/{}/".format(year)
    files = subprocess.check_output("ls {}".format(input_directory), shell=True,universal_newlines=True).rstrip("\n").split("\n")
    hists = {}
    for i,file in enumerate(files):

        file = uproot.open(input_directory+file)
        for name in file.classnames().keys():
            if i == 0:
                pt_bins = file[name].axis(0).edges()
                eta_bins = file[name].axis(1).edges()
                hists[name] = file[name].values()
            else:
                hists[name] += file[name].values()

        file.close()
    with uproot.recreate("scalefactors/Btagging_Efficiency{}.root".format(year)) as file:

        for Flavour in ("B","C","UDSG"):
            file["{}tag_Eff".format(Flavour)] = hists["{}tags;1".format(Flavour)]/hists["{}jets;1".format(Flavour)],pt_bins,eta_bins
            down,up = clopper_pearson(hists["{}tags;1".format(Flavour)],hists["{}jets;1".format(Flavour)])
            file["{}tag_Eff_up".format(Flavour)] = down,pt_bins,eta_bins
            file["{}tag_Eff_down".format(Flavour)] = up,pt_bins,eta_bins


    write_json("scalefactors/Btagging_Efficiency{}.root".format(year),year)



if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--process', nargs=1, required = True)
    parser.add_argument('-y', '--year', nargs=1,type = int, required = True)
    args = parser.parse_args()
    process = args.process[0]
    year = args.year[0]

    if process =="submit":
        main(year)
    elif process == "combine":
        combine(year)
    elif process == "json":
        print("make this code")

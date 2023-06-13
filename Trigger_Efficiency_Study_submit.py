import datetime, os, subprocess
from shutil import rmtree
import uproot
import numpy as np

submission_file = lambda args, logfolder, nfiles: """
executable = job.sh
arguments = "{0} $(Process)"
log = {1}/log_$(Process).txt
output = {1}/out_$(Process).txt
error = {1}/err_$(Process).txt
should_transfer_files = No
queue {2}
""".format(args, logfolder, nfiles)


def submit_sample(input_directory, run_type,is_mc,savefolder,logfolder):
    print("starting submitting process for run {}".format(run_type))
    filenames = subprocess.check_output(["ls",input_directory],universal_newlines=True).rstrip("\n").split("\n")

    nfiles = len(filenames)
    print("files: {}".format(nfiles))
    totalweights = 0.
    print("checking total weights...")
    if is_mc:
        for filename in filenames:
            with uproot.open(input_directory+filename) as file:
                totalweights += np.max(file["totalweights"].values())

    print("total weights: {}".format(totalweights))
    filenames = ",".join(filenames)
    logfolder = logfolder+"/"+run_type
    savefolder = savefolder+"/"+run_type
    if not os.path.exists(logfolder):
        os.mkdir(logfolder)
    if os.path.exists(savefolder):
        rmtree(savefolder)
    os.mkdir(savefolder)

    jobs_to_submit = nfiles
    submissionfilename = '{}/submit.sub'.format(logfolder)


    print("submitting {} Jobs for {} files".format(jobs_to_submit,nfiles))
    with open(submissionfilename, 'w') as f:
        f.write(submission_file(" ".join((filenames,input_directory, run_type,"{} {}".format(is_mc,totalweights), savefolder)), logfolder, jobs_to_submit))

    subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)



def full_event_selection():


    timestamp = '{:%y%m%d_%H%M%S}'.format(datetime.datetime.now())
    savefolder = "Event_Folders/Trigger_Eff/Trigger_Eff_"+timestamp
    logfolder = "Log_Folders/Trigger_Eff_logs/Trigger_Eff_logs_"+timestamp

    os.mkdir(savefolder)
    os.mkdir(logfolder)

    input_directories_mc = ("/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V1/TTZToLLNuNu_M_10_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221027_113808/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTZToLL_M_1to10_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161124/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V1/WZTo3LNu_TuneCP5_13TeV_amcatnloFXFX_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221027_113815/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/tZq_ll_4f_ckm_NLO_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161250/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/DYJetsToLL_M_10to50_TuneCP5_13TeV_madgraphMLM_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161206/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/DYJetsToLL_M_50_TuneCP5_13TeV_amcatnloFXFX_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161209/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/GluGluToContinToZZTo2e2mu_TuneCP5_13TeV_mcfm701_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161229/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/GluGluToContinToZZTo2e2tau_TuneCP5_13TeV_mcfm701_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161231/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/GluGluToContinToZZTo2mu2tau_TuneCP5_13TeV_mcfm701_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161234/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/GluGluToContinToZZTo4e_TuneCP5_13TeV_mcfm701_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161236/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/GluGluToContinToZZTo4mu_TuneCP5_13TeV_mcfm701_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161238/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/GluGluToContinToZZTo4tau_TuneCP5_13TeV_mcfm701_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161241/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTHHToNon4b_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161408/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTTT_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161122/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTTo2L2Nu_TuneCP5_13TeV_powheg_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161147/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTGamma_Dilept_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161403/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTWH_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161411/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTWJetsToLNu_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161120/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTWW_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161413/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTWZ_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161415/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTZHToNon4b_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161418/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/TTZZToNon4b_TuneCP5_13TeV_madgraph_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161420/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/ttHJetToNonbb_M125_TuneCP5_13TeV_amcatnloFXFX_madspin_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v1/221026_161127/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/WWW_4F_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_ext1_v2/221026_161354/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/WWZ_4F_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_ext1_v2/221026_161356/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/WZZ_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_ext1_v2/221026_161359/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/ZZZ_TuneCP5_13TeV_amcatnlo_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_ext1_v2/221026_161401/",
                            "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/ZZTo4L_TuneCP5_13TeV_powheg_pythia8_RunIISummer20UL18NanoAODv9_106X_upgrade2018_realistic_v16_L1v1_v2/221026_161335/")


    input_directories_data = (  "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/DoubleMuon_Run2018D_UL2018_MiniAODv2_NanoAODv9_v2/221026_160814/",
                                "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/EGamma_Run2018D_UL2018_MiniAODv2_NanoAODv9_v3/221026_160817/",
                                "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/SingleMuon_Run2018D_UL2018_MiniAODv2_NanoAODv9_v1/221026_160820/",
                                "/pnfs/iihe/cms/store/user/joknolle/run2nanofiles/Ttz2018SkimmerOct22V0/MuonEG_Run2018D_UL2018_MiniAODv2_NanoAODv9_v1/221026_160812/",
                            )

    for input_directory in input_directories_mc:
        run_type = input_directory.split("/")[9]
        submit_sample(input_directory, run_type,True,savefolder,logfolder)

    for input_directory in input_directories_data:

        run_type = input_directory.split("/")[9]
        submit_sample(input_directory, run_type,False,savefolder,logfolder)




if __name__ == '__main__':
    full_event_selection()

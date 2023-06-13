import datetime, os, subprocess
from shutil import rmtree

submission_file_MC = lambda args, logfolder, nfiles: """
executable = job_MC.sh
arguments = "{0} $(Process)"
log = {1}/log_$(Process).txt
output = {1}/out_$(Process).txt
error = {1}/err_$(Process).txt
should_transfer_files = No
queue {2}
""".format(args, logfolder, nfiles)

submission_file_DATA = lambda args, logfolder, nfiles: """
executable = job_DATA.sh
arguments = "{0} $(Process)"
log = {1}/log_$(Process).txt
output = {1}/out_$(Process).txt
error = {1}/err_$(Process).txt
should_transfer_files = No
queue {2}
""".format(args, logfolder, nfiles)


def submit_sample(input_directory, run_type,clumping,is_data):
    print("starting submitting process for run {}".format(run_type))
    filenames = next(os.walk(input_directory), (None, None, []))[2]
    nfiles = len(filenames)
    filenames = ",".join(filenames)

    logfolder = 'submit_{}'.format(run_type)
    if not os.path.exists(logfolder):
        os.mkdir(logfolder)
    if not os.path.exists(run_type):
        os.mkdir(run_type)

    if os.path.exists("{}/double_lepton".format(run_type)):
        rmtree("{}/double_lepton".format(run_type))
    os.mkdir("{}/double_lepton".format(run_type))

    if os.path.exists("{}/single_lepton".format(run_type)):
        rmtree("{}/single_lepton".format(run_type))
    os.mkdir("{}/single_lepton".format(run_type))

    jobs_to_submit = nfiles//clumping+1
    submissionfilename = '{}/submit.sub'.format(logfolder)


    print("submitting {} Jobs for {} files".format(jobs_to_submit,nfiles))
    if is_data:
        with open(submissionfilename, 'w') as f:
            f.write(submission_file_DATA(" ".join((filenames,input_directory, run_type,'{}'.format(clumping))), logfolder, jobs_to_submit))

        subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)
    else:
        with open(submissionfilename, 'w') as f:
            f.write(submission_file_MC(" ".join((filenames,input_directory, run_type,'{}'.format(clumping))), logfolder, jobs_to_submit))

        subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)






if __name__ == '__main__':

    clumping = 10


    #MONTE CARLO FILES
    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/TTTo2J1L1Nu_CP5_13p6TeV_powheg-pythia8/"
    run_type = "TTTo2J1L1Nu"
    submit_sample(input_directory, run_type,clumping,False)

    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/TTTo2L2Nu_CP5_13p6TeV_powheg-pythia8/"
    run_type = "TTTo2L2Nu"
    submit_sample(input_directory, run_type,clumping,False)


    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/DYJetsToLL_M-50_TuneCP5_13p6TeV-madgraphMLM-pythia8-ext1/"
    run_type = "DYJetsToLL"
    submit_sample(input_directory, run_type,clumping,False)


    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/TWminus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8/"
    run_type = "tWminus"
    submit_sample(input_directory, run_type,clumping,False)

    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/TbarWplus_DR_AtLeastOneLepton_CP5_13p6TeV_powheg-pythia8/"
    run_type = "TbarWplus"
    submit_sample(input_directory, run_type,clumping,False)


    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/WJetsToLNu_TuneCP5_13p6TeV-madgraphMLM-pythia8/"
    run_type = "WJetsToLNu"
    submit_sample(input_directory, run_type,clumping,False)

    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/WW_TuneCP5_13p6TeV-pythia8/"
    run_type = "WW"
    submit_sample(input_directory, run_type,clumping,False)


    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/WZ_TuneCP5_13p6TeV-pythia8/"
    run_type = "WZ"
    submit_sample(input_directory, run_type,clumping,False)

    input_directory = "/pnfs/iihe/cms/store/user/juvanden/run3nanofiles/rawdata/ZZ_TuneCP5_13p6TeV-pythia8/"
    run_type = "ZZ"
    submit_sample(input_directory, run_type,clumping,False)

    #DATA FILES
    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/EGamma_Run2022_PromptReco_DESY_v1/220921_110501/"
    run_type = "EGamma"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/DoubleMuon_Run2022_PromptReco_DESY_v1/220921_110457/"
    run_type = "DoubleMuon"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/MuonEG_Run2022_PromptReco_DESY_v1/220921_110454/"
    run_type = "MuonEG"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/SingleMuon_Run2022_PromptReco_DESY_v1/220921_110528/"
    run_type = "SingleMuon"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/Muon_Run2022_PromptReco_DESY_v1/220921_110510/"
    run_type = "Muon"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/MET_Run2022_PromptReco_DESY_v1/220921_110532/"
    run_type = "MET"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/JetHT_Run2022_PromptReco_DESY_v1/220921_110540/"
    run_type = "JetHT"
    submit_sample(input_directory, run_type,clumping,True)

    input_directory = "/pnfs/iihe/cms/store/user/joknolle/run3nanofiles/TriggerStudiesSkimmerSep22V1/JetMET_Run2022_PromptReco_DESY_v1/220921_110534/"
    run_type = "JetMET"
    submit_sample(input_directory, run_type,clumping,True)

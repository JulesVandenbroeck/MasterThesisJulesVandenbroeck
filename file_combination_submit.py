import datetime, os, subprocess
from shutil import rmtree
import uproot
import numpy as np
from Analysis_Info import Analysis

submission_file = lambda args, logfolder, nfiles: """
executable = file_combination_job.sh
arguments = "{0} $(Process)"
log = {1}/log_$(Process).txt
output = {1}/out_$(Process).txt
error = {1}/err_$(Process).txt
should_transfer_files = No
queue {2}
""".format(args, logfolder, nfiles)

submission_file_COMBINE = lambda args, logfolder: """
executable = file_combination_job.sh
arguments = "{0} $(Process)"
log = {1}/log$(Process).txt
output = {1}/out$(Process).txt
error = {1}/err$(Process).txt
should_transfer_files = No
queue 2
""".format(args, logfolder)


def full_file_combination(folder_date,option,year):
    Info = Analysis(year)

    labels = Info.SampleClusters.keys()
    print(labels)
    post_Merge_folder = "Event_Folders/Post_Merge/Post_Merge_{}".format(folder_date)
    Histogram_folder = "Event_Folders/histograms_folders/histograms_{}".format(folder_date)
    logfolder = "Log_Folders/Post_Merge_logs/Post_Merge_logs_{}".format(folder_date)
    if not os.path.exists(post_Merge_folder):
        os.mkdir(post_Merge_folder)
    if not os.path.exists(logfolder):
        os.mkdir(logfolder)
    if not os.path.exists(Histogram_folder):
        os.mkdir(Histogram_folder)

    submissionfilename = '{}/submit.sub'.format(logfolder)
    njobs = len(labels)
    labels = ','.join(labels)
    with open(submissionfilename, 'w') as f:
        f.write(submission_file(" ".join((folder_date,option,labels,"{}".format(year))), logfolder, njobs))

    subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)


def COMBINE(folder_date,option,year):
    Info = Analysis(year)
    labels = ','.join(Info.SampleClusters.keys())

    logfolder = "Combine_logs"
    if not os.path.exists(logfolder):
        os.mkdir(logfolder)

    submissionfilename = '{}/submit.sub'.format(logfolder)

    with open(submissionfilename, 'w') as f:
        f.write(submission_file_COMBINE(" ".join((folder_date,option,labels,"{}".format(year))), logfolder))

    subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)

if __name__=="__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder_date', nargs=1, required = True)
    parser.add_argument('-o', '--option', nargs=1, required = True)
    parser.add_argument('-y', '--year', nargs=1,type = int, required = True)
    args = parser.parse_args()
    folder_date = args.folder_date[0]
    option = args.option[0]
    year = args.year[0]

    if option == "COMBINE":
         COMBINE(folder_date,option,year)
    else:
        full_file_combination(folder_date,option,year)

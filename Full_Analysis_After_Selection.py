import datetime, os, subprocess
from shutil import rmtree
import uproot
import numpy as np
import time

submission_file = lambda label, logfolder,jobs_to_submit: """
executable = job_Full_Analysis_After_Selection.sh
arguments = "{0}"
log = {1}/log_$(Process).txt
output = {1}/out_$(Process).txt
error = {1}/err_$(Process).txt
should_transfer_files = No
queue {2}
""".format(label, logfolder,jobs_to_submit)

event_types_labels = ("NonPrompt","ZZ","TTX","VVV","tZq","WZ","TTZ","DATA")


def job_checker(logfolder,label):

    os.system("condor_q")
    veto = 0
    for label in event_types_labels:
        if os.path.isfile("{}/{}/out_0.txt".format(logfolder,label)):
            with open("{}/{}/out_0.txt".format(logfolder,label), "rb") as file:
                try:
                    file.seek(-2, os.SEEK_END)
                    while file.read(1) != b'\n':
                        file.seek(-2, os.SEEK_CUR)
                except OSError:
                    file.seek(0)
                last_line = file.readline().decode()
            if last_line[:9] != 'Job done!':
                veto = 1
        else:
            veto = 1

    return (not bool(veto))



def main(folder_date):
    analysis_date = '{:%y%m%d_%H%M%S}'.format(datetime.datetime.now())


    subprocess.call(["dos2unix","job_Full_Analysis_After_Selection.sh"])

    logfolder = 'Log_Folders/Analysis_logs/Analysis_logs_{}'.format(analysis_date)
    if not os.path.exists(logfolder):
        os.mkdir(logfolder)
    histogram_folder = "Event_Folders/histograms_folders/histograms_{}".format(analysis_date)
    if not os.path.exists(histogram_folder):
        os.mkdir(histogram_folder)

    for label in event_types_labels:
        logfolder_label = "{}/{}".format(logfolder,label)
        if not os.path.exists(logfolder_label):
            os.mkdir(logfolder_label)

        submissionfilename = '{}/submit.sub'.format(logfolder_label)
        with open(submissionfilename, 'w') as f:
            f.write(submission_file(" ".join((label,folder_date,analysis_date)),logfolder_label,1))
        subprocess.call('condor_submit {}'.format(submissionfilename), shell=True)


    jobs_are_ready = False
    os.system("condor_q")
    while not jobs_are_ready:
        input("Press Enter to check jobs...")
        jobs_are_ready = job_checker(logfolder,label)

    print("Starting Histogram Plotting")
    subprocess.call(['python3','histogram_plot_mpl.py','-l','{}'.format(31.8*(10**3)),'-a',analysis_date])

    print("Finished Full Analysis after Selection at %H:%M:%S")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--folder_date', nargs=1, required = True)
    args = parser.parse_args()
    folder_date = args.folder_date[0]
    main(folder_date)

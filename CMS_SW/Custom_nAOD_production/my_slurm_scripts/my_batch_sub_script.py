# Author Tiziano Bevilacqua (05/13/2022) 
# Script to submit nAODomisation jobs to slurm, tested on PSI tier3 

from importlib.metadata import metadata
import re, os, sys, glob, time, logging, multiprocessing, socket, subprocess, shlex, getpass, math, shutil
from optparse import OptionParser
import json
from importlib import resources
from pathlib import Path

# ---------------------- A few helping functions  ----------------------

def colored_text(txt, keys=[]):
    _tmp_out = ''
    for _i_tmp in keys:
        _tmp_out += '\033['+_i_tmp+'m'
    _tmp_out += txt
    if len(keys) > 0: _tmp_out += '\033[0m'

    return _tmp_out

color_dict = {
    "cyan": '\033[96m',
    "green": '\033[92m',
    "red": '\033[91m',
    "yellow": '\33[33m',
    "blue": '\33[34m',
    "white": '\033[37m',
    "bold": '\033[01m',
    "end": '\033[0m'
    
}

def KILL(log):
    raise RuntimeError('\n '+colored_text('@@@ FATAL', ['1','91'])+' -- '+log+'\n')

def WARNING(log):
    print ('\n '+colored_text('@@@ WARNING', ['1','93'])+' -- '+log+'\n')

def MKDIRP(dirpath, verbose=False, dry_run=False):
    if verbose: print ('\033[1m'+'>'+'\033[0m'+' os.mkdirs("'+dirpath+'")')
    if dry_run: return
    try:
      os.makedirs(dirpath)
    except OSError:
      if not os.path.isdir(dirpath):
        raise
    return

def EXE(cmd, suspend=True, verbose=False, dry_run=False):
    if verbose: print ('\033[1m'+'>'+'\033[0m'+' '+cmd)
    if dry_run: return

    _exitcode = os.system(cmd)
    _exitcode = min(255, _exitcode)

    if _exitcode and suspend:
       raise RuntimeError(_exitcode)

    return _exitcode

#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#
#- USAGE: -------------------------------------------------------------------------------------------------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --create ----------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --status ----------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --submit ----------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --resubmit --------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --missing ---------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --hadd ------------#
#----------------------------------------------------------------------------------------------------------#
#----------------------------------------------------------------------------------------------------------#

# Read options from command line
usage = "Usage: python %prog filelists [options]"
parser = OptionParser(usage=usage)
parser.add_option("--slurm_file",  dest="job_template",type="string",       default="slurm_template.sh", help="Slurm job template")
parser.add_option("--input",       dest="input",       type="string",       default="",    help="input configuration file")
parser.add_option("--create",      dest="create",      action="store_true", default=False, help="create taskdir and prepare submission scripts, it divide the input filelist (provided from the dataset within the config file) according to the number of file for each job (specified with --nfile)")
parser.add_option("--submit",      dest="submit",      action="store_true", default=False, help="submit jobs from task")
parser.add_option("--resubmit",    dest="resubmit",    action="store_true", default=False, help="prepare resubmit script with missing jobs")
parser.add_option("--resubmit_debug",    dest="resubmit_debug",    action="store_true", default=False, help="prepare resubmit script with missing jobs")
parser.add_option("--status",      dest="status",      action="store_true", default=False, help="check status of submitted jobs (R, PD, Completed")
parser.add_option("--missing",     dest="missing",     action="store_true", default=False, help="look for missing jobs")
parser.add_option("--queue",       dest="queue",       type="string",       default="standard", help="slurm queue to submit jobs to, default: standard, if this needs to be changed one should also have a look at the --time option")
parser.add_option("--time",        dest="time",        type="string",       default="12:00:00", help="slurm job time limit, default: 12:00:00, make sure not to exceed time limit for each partition (for limits ref to https://wiki.chipp.ch/twiki/bin/view/CmsTier3/SlurmUsage) ")
parser.add_option("--debug",       dest="debug",       action="store_true", default=False, help="Debug verbosity and skip removing of some intermediate files")
parser.add_option("--redirector",  dest="redirector",  type="string",       default="root://cms-xrd-global.cern.ch:/", help="Redirector to use when trying to open the files")
parser.add_option("--redirector_alt",  dest="redirector_alt",  type="string",       default="davs://xrootd.cmsaf.mit.edu:1094/", help="Redirector to use when trying to open troubled files")
parser.add_option("--user",  dest="user",  type="string",       default="", help="User to look fot the log files")
(opt,args) = parser.parse_args()

# --------------------- Proxy check ----------------------
if opt.input == "":
    KILL("no config json specified")
else:
    with open(opt.input) as f:
        metadata = json.load(f)

os.system("voms-proxy-info --timeleft > proxy.txt")
with open('proxy.txt') as proxyfile:
    lines = proxyfile.readlines()
    if len(lines)==1:
        if not "Proxy not found" in lines[0]:
            timeleft = int(lines[0])
os.remove('proxy.txt')
if timeleft<1000: #172800:
    print ("-"*80)
    print (color_dict["red"]+"New proxy needed"+color_dict["end"])
    print ("suggest to use: voms-proxy-init -voms cms -valid 168:00")
    print ("-"*80)
    raise RuntimeError("PROXY ERROR")
else:
    print ("-"*80)
    print (color_dict["green"]+"Current proxy is long enough"+color_dict["end"])
    print ("-"*80)

# ----------------------  Settings -----------------------
# Some further (usually) fixed settings, should edit them in this file

# Output directories/files
SUBTIME = time.strftime("%Y_%m_%d_%Hh%Mm%S", time.localtime())
if metadata["outdir"] == "":
    KILL("no output directory specified")

# Working directory, during running we cd here and back
OUT_PATH = metadata["outdir"]
EXEC_PATH = os.getcwd()
EXEC_PATH = EXEC_PATH+"/"+metadata["taskname"]

if opt.create:
    # Check input filelist
    if opt.input == "": KILL("no configuration provided provided (--input configs/<your_config>.json)")

    # Create Task dir and copy input filelist and slurm template
    opt.input = os.path.abspath(opt.input)
    metadata["job_template"] = os.path.abspath(metadata["job_template"])
    MKDIRP(EXEC_PATH+"/filelists")
    if len(os.listdir(EXEC_PATH+"/filelists")) != 0:
        os.system("rm "+EXEC_PATH+"/filelists/*")
    os.chdir(EXEC_PATH) 
    EXEC_PATH = os.getcwd()

    os.system("dasgoclient -query=\"file dataset="+metadata["sample"]+"\" > all_input.txt")
    os.system("cp "+metadata["job_template"]+" "+EXEC_PATH+"/slurm_jobscript.sh")
    if opt.queue != "standard":
        os.system("sed \"s;\#SBATCH --partition=standard;\#SBATCH --partition="+opt.queue+";g\" slurm_jobscript.sh > tmp")
        os.system("mv tmp slurm_jobscript.sh")
    if opt.time != "12:00:00":
        os.system("sed \"s;\#SBATCH --time=12:00:00;\#SBATCH --time="+opt.time+";g\" slurm_jobscript.sh > tmp")
        os.system("mv tmp slurm_jobscript.sh")
    os.system("cp ../Cert*.json "+EXEC_PATH+"/")

    # Summary file
    os.system("echo \"nanoAOD conversion process for "+metadata["taskname"]+" summary\" > "+EXEC_PATH+"/summary.txt")
    os.system("echo \"\" >> "+EXEC_PATH+"/summary.txt")
    os.system("echo \"Task name: "+metadata["taskname"]+"\" >> "+EXEC_PATH+"/summary.txt")
    os.system("echo \"Output dir: "+metadata["outdir"]+"\" >> "+EXEC_PATH+"/summary.txt")
    os.system("echo \"Input filelist: all_input.txt\" >> "+EXEC_PATH+"/summary.txt")
    os.system("echo \"Slurm jobs template: slurm_jobscript.sh\" >> "+EXEC_PATH+"/summary.txt")

    # Create filelist dir and filelists files to divide input files to jobs
    with open("all_input.txt") as fl:
        files = fl.readlines()
        njobs = int(len(files)/metadata["nfile"])
        print ("-"*80)
        print ("number of jobs: "+str(njobs))
        print ("total input files: "+str(len(files)))

        # Summary file 
        os.system("echo \"Number of files per job: "+str(metadata["nfile"])+"\" >> "+EXEC_PATH+"/summary.txt" )
        os.system("echo \"Number of jobs: "+str(njobs)+"\" >> "+EXEC_PATH+"/summary.txt")
        os.system("echo \"Total number of input files: "+str(len(files))+"\" >> "+EXEC_PATH+"/summary.txt")
        for i, filename in enumerate(files):
            idx = int((i/metadata["nfile"]) // 1)
            ash = int((100.0/(njobs)*idx) // 1 )
            space = int((100.0/(njobs)*(njobs-idx)) // 1)-1
            print ("preparing file lists "+color_dict["cyan"]+"|"+"#"*ash+" "*space+"|"+color_dict["end"], end="\r")
            EXE("echo "+filename[:-1]+" | awk '{ print $1 }'"+' >> filelists/filelist_{:04d}.txt'.format(idx))
        print ("\nprepared "+str(njobs)+" temporary filelists at: ", os.getcwd()+"/filelists")
    
    # Prepare submission script with "sbatch [job name] [out-log] [out-err] slurm_jobscript.sh [GoodLumi.json path] [job_label] [input_files_list] [output dir] [other self explanatory options for cmsDriver]  
    print ("")
    print ("Job Script file: "+color_dict["blue"]+metadata["job_template"]+color_dict["end"])
    os.system("ls -l filelists | awk '{ print $NF }' | tail -n +2 | head -n -1 > filelists/job_list.txt")
    if metadata["customise_commands"] == "": metadata["customise_commands"] = "skip"
    if metadata["customise"] == "": metadata["customise"] = "skip"
    os.system("cat -n filelists/job_list.txt | awk '{ printf \"%.4d %s\\n\", $1, $2 }' | awk '{ print \"sbatch --job-name="+metadata["taskname"]+"_\"$1\" -o /work/%u/test/.slurm/%x_%A_\"$1\".out -e /work/%u/test/.slurm/%x_%A_\"$1\".err slurm_jobscript.sh "+EXEC_PATH+"/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.json \"$1\" "+EXEC_PATH+"/filelists/\"$2\" "+OUT_PATH+"/"+metadata["taskname"]+" "+metadata["customise"]+" "+metadata["customise_commands"]+" "+metadata["era"]+" "+metadata["conditions"]+" "+metadata["type"]+" "+metadata["step"]+" "+opt.redirector+" "+opt.redirector_alt+" "+EXEC_PATH+"/filelists/problematic_files.txt\"}' > alljobs.sh")
    os.system("head -1 alljobs.sh | sed \"s;0001;test;g;\" > test.sh")

    print ("Jobs prepared at:", color_dict["blue"]+os.getcwd()+color_dict["end"], "as: "+color_dict["blue"]+"alljobs.sh"+color_dict["end"]) 
    print ("or test 1 job with: test.sh")
    print ("-"*80)

    print ("-"*80)

    # Option to submit jobs right away
    answ = input(color_dict["green"]+"Do you want to directly submit the jobs to slurm (all jobs or 1 test job)? (y/n/test) \n"+color_dict["end"])
    if str(answ) == "y":
        os.system("wc -l alljobs.sh | awk '{print \"submitting \"$1\" jobs from \"$2\" ...\"}'")
        EXE("sh alljobs.sh")   
    elif str(answ) == "test":
        os.system("wc -l test.sh | awk '{print \"submitting \"$1\" jobs from \"$2\" ...\"}'")
        EXE("sh test.sh") 
    print ("-"*80)

# Same as before, ask for submission of jobs
elif opt.submit:
    os.chdir(EXEC_PATH) 
    EXEC_PATH = os.getcwd()
    print ("-"*80)
    answ = input(color_dict["green"]+"Do you want to directly submit the jobs to slurm (all jobs or 1 test job)? (y/n/test) \n"+color_dict["end"])
    if str(answ) == "y":
        os.system("wc -l alljobs.sh | awk '{print \"submitting \"$1\" jobs from \"$2\" ...\"}'")
        EXE("sh alljobs.sh")   
    elif str(answ) == "test":
        os.system("wc -l test.sh | awk '{print \"submitting \"$1\" jobs from \"$2\" ...\"}'")
        EXE("sh test.sh") 
    print ("-"*80)
    
# Check the status of submitted jobs, it recover job info from summary file in the task directory 
# and query squeue for pending and running jobs. Then check the output dir to look for completed jobs.
elif opt.status:
    print ("-"*80)
    with open(EXEC_PATH+"/summary.txt") as fl:
        lines = fl.readlines()
        for line in lines:
            fields = re.split(": |\n", line)
            if fields[0] == "Number of jobs":
                njobs = int(fields[1])
            elif fields[0] == "Task name":
                TASKNAME = fields[1]
            elif fields[0] == "Output dir":
                OUT_PATH = fields[1]
                
    os.system("( squeue -n `cat "+EXEC_PATH+"/alljobs.sh | awk '{print $2}' | sed 's;--job-name=;;g;' | sed ':label1 ; N ; $! b label1;s;\\n;,;g'` > taskjobs ) > /dev/null")
    os.system("grep PD taskjobs > Pending")
    os.system("grep \" R \" taskjobs > Running")
    os.system("( ls "+OUT_PATH+"/"+TASKNAME+" | grep .root > Completed ) >  /dev/null")
    os.system("sort -u Completed > Comp")
    os.system("mv Comp Completed")
    os.system("ls -l "+OUT_PATH+"/"+TASKNAME+"/logs | grep -v test | grep .out > Done")
    os.system("echo "+color_dict["bold"]+"\"Status of Task "+TASKNAME+": ("+str(njobs)+" Jobs)\""+color_dict["end"])
    os.system("echo \"Jobs - Pending                : `wc -l Pending | awk '{ print $1}'`\"")
    os.system("echo \"     - Running                : `wc -l Running | awk '{ print $1}'`\"")
    os.system("echo \"     - Done (with STDOUT)     : `wc -l Done | awk '{ print $1}'`\"")
    os.system("echo \"------------------------------------\"")
    os.system("echo \"     - "+color_dict["green"]+"Completed (has output) : `wc -l Completed | awk '{ print $1}'`\""+color_dict["end"])
    os.system("rm taskjobs Pending Running Completed Done")
    print ("-"*80)
    
# Look for finished jobs and then prints number of jobs that are not in the output dir
elif opt.missing:
    print ("-"*80)
    with open(EXEC_PATH+"/summary.txt") as fl:
        lines = fl.readlines()
        for line in lines:
            fields = re.split(": |\n", line)
            if fields[0] == "Number of jobs":
                njobs = int(fields[1])
            elif fields[0] == "Task name":
                TASKNAME = fields[1]
            elif fields[0] == "Output dir":
                OUT_PATH = fields[1]

    os.system("ls "+OUT_PATH+"/"+TASKNAME+" | grep .root >> output")
    os.system("cat output | sort -u | sed 's;_; ;g;s;\.; ;g' | awk '{ printf \"%d\\n\", $(NF-1) }' > jobnums")
    os.system("seq 1 "+str(njobs)+" > Seq")
    os.system("diff Seq jobnums | grep \"<\" | awk '{ printf \"%d,\", $2 }' | sed 's;,$;\\n;'")
    os.system("rm Seq jobnums output")
    print ("-"*80)

# same as missing option but also prepare a resubmission script for such jobs
elif opt.resubmit:
    print ("-"*80)
    with open(EXEC_PATH+"/summary.txt") as fl:
        lines = fl.readlines()
        for line in lines:
            fields = re.split(": |\n", line)
            if fields[0] == "Number of jobs":
                njobs = int(fields[1])
            elif fields[0] == "Task name":
                TASKNAME = fields[1]
            elif fields[0] == "Output dir":
                OUT_PATH = fields[1]
    os.chdir(EXEC_PATH) 
    EXEC_PATH = os.getcwd()

    os.system("ls "+OUT_PATH+"/"+TASKNAME+" | grep .root >> output")
    os.system("cat output | sort -u | sed 's;_; ;g;s;\.; ;g' | awk '{ printf \"%d\\n\", $(NF-1) }' > jobnums")
    os.system("seq 1 "+str(njobs)+" > Seq")
    os.system("diff Seq jobnums | grep \"<\" | awk '{ printf \"%.4d,\", $2 }' | sed 's;,$;\\n;' > resubmit ")
    if os.path.exists(EXEC_PATH+"/resubmit.sh"): os.system("rm "+EXEC_PATH+"/resubmit.sh")
    with open("resubmit") as fl:
        files = fl.readlines()
        if len(files) > 0:
            files = re.split(',|\n',files[0])
        for i,job in enumerate(files):
            if job == '': break
            idx = (int((i/(float(len(files))/100)) // 1) if (len(files) > 2) else 100)
            print ("preparing resubmission jobs list "+color_dict["cyan"]+"|"+"#"*idx+" "*(100-idx)+"|"+color_dict["end"], end="\r")
            os.system("grep "+TASKNAME+"_"+job+" "+EXEC_PATH+"/alljobs.sh >> "+EXEC_PATH+"/resubmit.sh")
    os.system("rm Seq jobnums output resubmit")
    if len(files) > 0:
        print("\nDone: "+color_dict["blue"]+"resubmit.sh"+color_dict["end"]+" file created at "+color_dict["blue"]+EXEC_PATH+"/resubmit.sh"+color_dict["end"])
        # Option to submit jobs right away
        answ = input(color_dict["green"]+"Do you want to directly resubmit the jobs to slurm? (y/n) \n"+color_dict["end"])
        if str(answ) == "y":
            return_dir = os.getcwd()
            os.chdir(EXEC_PATH)
            os.system("wc -l resubmit.sh | awk '{print \"submitting \"$1\" jobs from \"$2\"...\"}'")
            EXE("sh resubmit.sh")   
            os.system(f"cd {return_dir}")
        else:
            os.system("echo 'ok, nothing to be done then.'")
    else:    
        print("No jobs to resubmit")
    print ("-"*80) 

# same as missing option but also prepare a resubmission script for such jobs
elif opt.resubmit_debug:
    user = "$USER" if opt.user == "" else opt.user
    logdir = f"/work/{user}/test/.slurm/"
    print ("-"*80)
    with open(EXEC_PATH+"/summary.txt") as fl:
        lines = fl.readlines()
        for line in lines:
            fields = re.split(": |\n", line)
            if fields[0] == "Number of jobs":
                njobs = int(fields[1])
            elif fields[0] == "Task name":
                TASKNAME = fields[1]
            elif fields[0] == "Output dir":
                OUT_PATH = fields[1]
    os.chdir(EXEC_PATH) 
    EXEC_PATH = os.getcwd()

    os.system("ls "+OUT_PATH+"/"+TASKNAME+" | grep .root >> output")
    os.system("cat output | sort -u | sed 's;_; ;g;s;\.; ;g' | awk '{ printf \"%d\\n\", $(NF-1) }' > jobnums")
    os.system("seq 1 "+str(njobs)+" > Seq")
    os.system("diff Seq jobnums | grep \"<\" | awk '{ printf \"%.4d,\", $2 }' | sed 's;,$;\\n;' > resubmit ")

    os.system("cat resubmit")
    with open("resubmit") as fl:
        files = fl.readlines()
        if len(files) > 0:
            files = re.split(',|\n',files[0])
            print(files)
            for f in files[:-1]:
                os.system(f"ls -l {logdir} | grep {TASKNAME} | grep {f} | grep .err |"+" awk '{print $7}' | sort -k1 | tail -n 1")
                day = subprocess.check_output(f"ls -l {logdir} | grep {TASKNAME} | grep {f} | grep .err |"+" awk '{print $7}' | sort -k1 | tail -n 1", shell=True).decode('UTF-8').split("\n")[0]
                nlogs = subprocess.check_output(f"ls -l {logdir} | grep {TASKNAME} | grep {f} | grep .err |"+" awk '{print $7, $8, $NF}' "+f"| awk '$1 == {day}' | sort -k1 | tail -n 1 | wc -l", shell=True).decode('UTF-8').split("\n")[0]
                if nlogs == "1":
                    log_fname = subprocess.check_output(f"ls -l {logdir} | grep {TASKNAME} | grep {f} | grep .err |"+" awk '{print $7, $8, $NF}' "+f"| awk '$1 == {day}' | sort -k1 | tail -n 1 | "+" awk '{print $NF}' ", shell=True).decode('UTF-8').split("\n")[0]
                    print("log:", log_fname)
                    failing_fname = str(subprocess.check_output(f"cat {logdir}/{log_fname} | grep 'Failed to open the file' | "+" awk '{print $NF}'", shell=True).decode('UTF-8')).split("\n")[0].split("'")[1]
                    print("failing_fname:", failing_fname)
                    if not Path("filelists/problematic_files.txt").exists():
                        print("creating problematic filelist")
                        os.system("echo '' > filelists/problematic_files.txt")
                    try:
                        cmd = ["grep", failing_fname, "filelists/problematic_files.txt"]
                        output = subprocess.check_output(cmd).decode('utf-8')
                        print("problematic filename already in the filelist")
                    except subprocess.CalledProcessError:
                        os.system(f"echo '{failing_fname}' >> filelists/problematic_files.txt")
        if os.path.exists(EXEC_PATH+"/resubmit.sh"): os.system("rm "+EXEC_PATH+"/resubmit.sh")

    with open("resubmit") as fl:
        files = fl.readlines()
        if len(files) > 0:
            files = re.split(',|\n',files[0])
        for i,job in enumerate(files):
            if job == '': break
            idx = (int((i/(float(len(files))/100)) // 1) if (len(files) > 2) else 100)
            print ("preparing resubmission jobs list "+color_dict["cyan"]+"|"+"#"*idx+" "*(100-idx)+"|"+color_dict["end"], end="\r")
            os.system("grep "+TASKNAME+"_"+job+" "+EXEC_PATH+"/alljobs.sh >> "+EXEC_PATH+"/resubmit.sh")
    os.system("rm Seq jobnums output resubmit")
    if len(files) > 0:
        print("\nDone: "+color_dict["blue"]+"resubmit.sh"+color_dict["end"]+" file created at "+color_dict["blue"]+EXEC_PATH+"/resubmit.sh"+color_dict["end"])
        # Option to submit jobs right away
        answ = input(color_dict["green"]+"Do you want to directly resubmit the jobs to slurm? (y/n) \n"+color_dict["end"])
        if str(answ) == "y":
            return_dir = os.getcwd()
            os.chdir(EXEC_PATH)
            os.system("wc -l resubmit.sh | awk '{print \"submitting \"$1\" jobs from \"$2\"...\"}'")
            EXE("sh resubmit.sh")   
            os.system(f"cd {return_dir}")
        else:
            os.system("echo 'ok, nothing to be done then.'")
    else:    
        print("No jobs to resubmit")
    print ("-"*80) 
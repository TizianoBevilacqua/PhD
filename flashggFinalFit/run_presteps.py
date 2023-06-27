# Author Tiziano Bevilacqua (17/03/2023) 
# Script to run FlashggFinalFit Signal, Background and Datacard steps

import re, os, sys, glob, time, logging, multiprocessing, socket, subprocess, shlex, getpass, math, shutil
from optparse import OptionParser
import json
import inspect
import subprocess

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

#--------------------------------------------------------------------------------------------------------------------------#
#- USAGE: -----------------------------------------------------------------------------------------------------------------#
#- python3 run_presteps.py --input ../out_dir_syst_090323/ --merged --root --ws --syst --cats --args "--do_syst" -#
#--------------------------------------------------------------------------------------------------------------------------#

# Read options from command line
usage = "Usage: python %prog filelists [options]"
parser = OptionParser(usage=usage)
parser.add_option("--input", dest="input", type="string", default="higgs_dna_signals_2017_cats", help="input dir")
parser.add_option("--sig", dest="signal", action="store_true", default=False, help="Do Signal steps")
parser.add_option("--skip", dest="skip", type="string", default="", help="Comma separated steps to skip during run.")
parser.add_option("--bkg", dest="background", action="store_true", default=False, help="Do Background step")
parser.add_option("--data", dest="datacard", action="store_true", default=False, help="Do Datacard step")
parser.add_option("--sig_config", dest="sconfig", type="string", default="config_hdna_test_2017_cats.py", help="configuration file for Signal steps, as it is now it must be stored in Signal directory in FinalFit")
parser.add_option("--bkg_config", dest="bconfig", type="string", default="config_hdna_test_cats.py", help="configuration file for Background steps, as it is now it must be stored in Background directory in FinalFit")
parser.add_option("--dc_config", dest="dconfig", type="string", default="config_hdna_test_cats.py", help="configuration file for Datacard steps, as it is now it must be stored in Datacard directory in FinalFit")
parser.add_option("--syst", dest="syst", action="store_true", default=False, help="Do systematics variation treatment")
parser.add_option("--ext", dest="ext", type="string", default="test_hdna", help="extension to attach to names")
parser.add_option("--verbose", dest="verbose", type="string", default="INFO", help="verbose lefer for the logger: INFO (default), DEBUG")
(opt,args) = parser.parse_args()

skip = opt.skip.split(",")
opt.input = os.path.abspath(opt.input)
if opt.signal:
    print("Running signal steps...")
    print("-"*120)
    os.chdir("Signal")
    if "ftest" not in skip:
        os.system(f"python RunSignalScripts.py --inputConfig {opt.sconfig} --mode fTest --modeOpts \"--doPlots --skipWV\"")
    if "syst" not in skip:
        os.system(f"python RunSignalScripts.py --inputConfig {opt.sconfig} --mode calcPhotonSyst")
    if "fit" not in skip:
        print("Using eff x acceptance json, have you set it up correctly?")
        os.system(f"python RunSignalScripts.py --inputConfig {opt.sconfig} --mode signalFit --modeOpts \"--skipVertexScenarioSplit --doPlots --doEffAccFromJson\"")
    if "package" not in skip:
        os.system(f"python RunPackager.py --cats auto --inputWSDir {opt.input} --ext {opt.ext} --batch local --massPoints 125 --year 2017")
    os.chdir("..")
    print("Signal steps done.")
    print("-"*120)

if opt.background:
    print("Running background steps...")
    print("-"*120)
    os.chdir("Background")
    if "ftest" not in skip:
        os.system(f"python RunBackgroundScripts.py --inputConfig {opt.bconfig} --mode fTestParallel")
    os.chdir("..")
    print("Background steps done.")
    print("-"*120)

if opt.datacard:
    print("Running datacard steps...")
    print("-"*120)
    os.chdir("Datacard")
    os.system(f"python RunYields.py --inputWSDirMap 2017={opt.input} --cats auto --procs auto --batch local --ext {opt.ext} --doSystematics --skipZeroes")
    os.system(f"python makeDatacard.py --years 2017 --ext {opt.ext} --doSystematics --prune")
    os.chdir("..")
    print("datacard steps done.")
    print("-"*120)

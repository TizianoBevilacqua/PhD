# FlashGG instructions:
## SetUP
### Supported releases:

* 10_6_1_patch2 required for the STXS stage 1.1 information
* 10_6_8 required for the STXS stage 1.2 information

### get flashgg:
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_8
cd CMSSW_10_6_8/src
cmsenv
git cms-init
cd $CMSSW_BASE/src 
git clone -b dev/cH_2018 git@github.com:higgs-charm/flashgg.git
source flashgg/setup_flashgg.sh
```
### build:
```
cd $CMSSW_BASE/src
scram b -j 4
```

## run the code
The code runs on microAODs, skimmed fancy files for HToGG analysis, in which some optimizations are performed to enhance the performance on the diphoton analysis.
It is structured in `Taggers` that select the events, and `Systematics` files that take care of the corrections.
### To run the code on microAODs:
The main file to run is `fggRunJobs.py` (situated in `flashgg/MetaData/scripts/fggRunJobs.py`), it is simply used to run other scripts and it takes many parameters and othe files that store metadata and parameters as input.
```
Usage: fggRunJobs.py [options]

Options:
  --processes=PROCESSES
                        List of datasets to be analyzed
  --dsfilter='/ds1*,/ds2*'
                        comma separated list of dataset name patterns to run
                        on (default: run on all)
  --load=CONFIG.json    load JSON file with configuration
  -n NJOBS, --njobs=NJOBS
                        number of jobs to run
  -q QUEUE, --queue=QUEUE
                        LSF queue to use. default: none
  --sync-lsf            Run LSF jobs in sync mode (with -K). This will spawn
                        one thread per job. Use only if you know what you are
                        doing. default: False
  --use-tarball         Make a sandbox tarball for the task default: True
  --no-use-tarball      Do not make a sandbox tarball for the task.
  --stage-to=STAGETO    Stage output to folder. default: none
  --stage-cmd=STAGECMD  Stage out command. (use 'guess' to have the script
                        guessing the command from the output folder) default :
                        guess
  --summary             Print jobs summary and exit
  -o OUTPUT, --output=OUTPUT
                        output file name. default: output.root
  -d OUTPUTDIR, --outputDir=OUTPUTDIR
                        output folder. default: none
  -x JOBEXE, --jobEx=JOBEXE
                        job executable. default: none
  -c CMDLINE, --cmdLine=CMDLINE
                        job command line. The script arguments will be
                        prepended. default: none
  --dumpCfg             dump configuaration and exit. default: False
  -v, --verbose         default: False
  -m MAXRESUB, --max-resubmissions=MAXRESUB
  -N NCPU, --ncpu=NCPU  
  --nCondorCpu=NCONDORCPU
                        Number of cpu cores per job to request from condor
  --make-light-tarball  Include datafolders only as symbolic link in tarball
  -H, --hadd            hadd output files when all jobs are finished.
  -D, --hadd-dateset    hadd output per dataset when all jobs are finished.
  -P, --hadd-process    hadd output per process when all jobs are finished.
  --dry-run             do not actually run the jobs.
  -C, --cont            continue interrupted task.
  -R, --resubmit-missing
                        resubmit unfinished jobs upon continue.
  --resubmit-ids=RESUBMIT_IDS
                        Specify list of job ids to be resubmitted
  -b BATCHSYSTEM, --batch-system=BATCHSYSTEM
                        Batch system name. Currently supported: sge lsf,
                        default: auto
  --no-copy-proxy       Do not try to copy the grid proxy to the worker nodes.
  -h, --help            show this help message and exit
```
to load the configuration for the analysis one must use the option `--load=CONFIG.json    load JSON file with configuration`, the json file contains a list of processes with the respective datasets, and some command line options. An example config.json for our private MC can be found at `flashgg/Systematics/test/jsons/cH/cH_privateMC_2018.json`.
In this file some more options are linked in the `cmdline` entry:
* `campaign=Era2018_legacy_v1_Summer19UL_cHPrivateMC` a directory containing another json with the expanded list of all the microAODs, situated at `flashgg/MetaData/data/Era2018_legacy_v1_Summer19UL_cHPrivateMC/`.
* `metaConditions=$CMSSW_BASE/src/flashgg/MetaData/data/MetaConditions/Era2018_legacy_v1.json` yet one more json containing metadata options.
* `useAAA=True` redirector option to load the input files, this particular option corresponds to `root://cms-xrd-global.cern.ch/`
* `cHTagsOnly=True` Important option to be passed to the `flashgg/Systematics/test/workspaceStd.py` script, used to select the tagger for the cH analysis. Using this option one load the configuration of the taggers from `flashgg/Systematics/python/cHCustomize.py` where taggers can be selected and the output variables are decided. Stuff contained in `flashgg/MicroAOD/flashggDiPhotons_cfi` is done as well
* the `cHTagger` is `flashgg/Taggers/python/flashggcHTag_cfi.py`, in this file some cuts and options are specified, the `jetID` lable is hardcoded in `cHCustomize.py` at [line 139](https://github.com/higgs-charm/flashgg/blob/58e151b1836a8fb1b691b317fc26d65c29078cd1/Systematics/python/cHCustomize.py#L139)

an example command line to produce NTuples for the private samples with what "should" be the configuration used by Huilin is:
```
fggRunJobs.py --load jsons/cH/cH_privateMC_2018.json -d out_test --stage-to /eos/user/t/tbevilac/H+c/flashgg/out_test_020822 workspaceStd.py -n 10 -q workday --no-copy-proxy
```
the output directory to stage the files must exist prior the execution of the program.

The 0th vertex should be selected [here](https://github.com/higgs-charm/flashgg/blob/58e151b1836a8fb1b691b317fc26d65c29078cd1/Systematics/test/workspaceStd.py#L239)

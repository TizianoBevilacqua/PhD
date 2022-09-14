#!/bin/bash -e

export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_26
cd CMSSW_10_6_26
cmsenv
git cms-merge-topic lgray:topic_hgg_nano_on-10_6_26
cd src
git remote add origin git@github.com:maxgalli/cmssw.git
git fetch origin
git checkout -t origin/lindsey_hgg_nanoaod
git cms-addpkg hgg_nanoaod_tools
scramv1 b

echo "python Private_nAOD_slurm.py -p HIG-DoubleEG-CMSSW_10_6_0-106X_dataRun2_v10_RelVal_2017B-v1_NANO.py -t DoubleEG-2017B -o /work/bevila_t/HpC_Analysis/CustomNAOD/Out_nAODs/ -b long --last_job 100"    
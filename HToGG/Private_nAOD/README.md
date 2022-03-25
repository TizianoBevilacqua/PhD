# Private nAOD Production (for HiggsDNA)

# SetUp
From(Max Galli)
This is probably not the most conventional way to do this, but it works:

* cmsrel CMSSW_10_6_26
* cd CMSSW_10_6_26
* cmsenv
* git cms-merge-topic lgray:topic_hgg_nano_on-10_6_26
* cd src
* git remote add origin git@github.com:maxgalli/cmssw.git
* git fetch origin
* git checkout -t origin/lindsey_hgg_nanoaod
* git cms-addpkg hgg_nanoaod_tools
* scramv1 b

# What To Do

As it is partially explained here in order to produce NanoAODs privately we need to generate a config file using cmsDriver.py (with one thousand billion options) and then feed it to cmsRun (or do everything in one step removing the flag no-exec).








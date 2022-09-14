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

As it is partially explained [here](https://twiki.cern.ch/twiki/bin/view/Sandbox/NanoAODProduction) in order to produce NanoAODs privately we need to generate a config file using cmsDriver.py (with one thousand billion options) and then feed it to cmsRun (or do everything in one step removing the flag no-exec).

Using this setup nAOD for HToGG analysis with HiggsDNA for run2 are produced, but the commands are general, the CMSSW release and configuration are peculiar to this analysis instead.

To produce a python configuration for MC file use:
```
cmsDriver.py --python_filename {name_of_the_cfg_file}.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:{name_of:the_flat_nTuple}.root --conditions {Global_Tag} --step NANO --filein dbs:{miniAOD_dataset} --era {era} --no_exec --mc -n -1
```
a complete command would be for istance:
```
cmsDriver.py --python_filename HIG-VHToGG-RunIISummer20UL17NanoAODv2-coffea-test_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer19UL17NanoAODv2-00001.root --conditions 106X_mc2017_realistic_v7 --step NANO --filein dbs:/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM --era Run2_2017,run2_nanoAOD_106Xv1 --no_exec --mc -n -1
```
after this step to obtain the nAOD one has to run:
```
cmsRun {name_of_the_cfg_file}.py
```
or in this example:
```
cmsRun HIG-VHToGG-RunIISummer20UL17NanoAODv2-coffea-test_cfg.py
```
For large dataset it's better to submit job to the batch system. 

## SLURM
To submit jobs on Slurm on the T3 use the script `Private_nAOD_slurm.py`, it submit jobs to slurm dividing the input files in groups of max_processes files (default = 5), the input are:
* -p) the python executable, 
* -t) the tag that will be used as output sub-directory name, 
* -o) main path of the output directory,
* -m) number of files per job.

## SLURM (smarter way)
To make job monitoring and resubmission way easier another workflow that is built inside the [XPlusCharm](https://github.com/missirol/XPlusCharmAnalysis) package is available (credits to M. Missiroli).
A recipe is provided here:
```
cmsrel CMSSW_10_6_18
cd CMSSW_10_6_18/src
cmsenv
git clone git@github.com:missirol/XPlusCharmAnalysis.git
scram b
mkdir Out_nAODs
cd Out_nAODs
bdriverEDM -o {out_dir} -d /work/"${USER}"/tmp_cmssw -w {config.json} -q long -t 24:00:00
bmonitor -i /path/to/{out_dir} -r 
```
where `config.json` is a file containing informations about CMSSW release settings, datasets, jobs specifications. 
An example file is provided in this directory (config_slurm_bdriverEDM.json)

## SLURM (nAOD v10, used for private MC production 09/2022)
A new set of scripts for the conversion of miniAODs to nAODs v10 with slurm is stored in the `slurm_pkg` directory. \n
There is a main python script that takes care of creating the task, submitting the jobs to slurm, babysit them by querying `squeue`, and, if needed, resubmit the failed ones. \n
The configuration for the job have to be fed to the script via a `.json` config file, an example is stored in the `slurm_pkg/configs` directory. the usage of the scripts is quite simple and shoud work out of the box on PSI tier3.
```
#- USAGE: -------------------------------------------------------------------------------------------------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --create ----------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --status ----------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --submit ----------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --resubmit --------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --missing ---------#
#- python my_batch_sub_script.py --input [config json file, example in the configs dir] --hadd ------------#
#----------------------------------------------------------------------------------------------------------#
```
Informations about the **GlobalTag** to place in the `conditions` entry of the json can be found [here](https://github.com/cms-sw/cmssw/blob/CMSSW_12_4_8/Configuration/AlCa/python/autoCond.py), the nAOD v10 page instead can be found [here](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv10). \n
To select the proper customisation of the cmsDriver.py script in order to include the pdf variations one can refer to [this](https://cms-talk.web.cern.ch/t/validate-requests-with-store-rwgt-info-false-in-gridpacks/12417/15?u=tbevilac) cmsTalk discussion. 
## CRAB

To be fixed

N.B.: for the dataset to be published, the line containing `process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",` has to be changed to `process.NANOAODSIMoutput = cms.OutputModule("PoolOutputModule",`.

N.B.B: remember to add the parameter `fakeNameForCrab =cms.untracked.bool(True)` when calling `cms.OuputModule`, since this is actually what is needed to publish the dataset

Then write a file `HIG-RunIISummer19UL17NanoAODv2-coffea-test_submit.py`

```
from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName       = 'HggNANO_UL17_v1_GluGluH'
config.General.transferLogs      = True
config.General.transferOutputs   = True

config.section_('JobType')
config.JobType.pluginName        = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName          = 'HIG-RunIISummer19UL17NanoAODv2-coffea-test_cfg.py'
config.JobType.priority          = 30

config.section_('Data')
# This string determines the primary dataset of the newly-produced outputs.
config.Data.inputDataset         = '/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer19UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'Automatic'
config.Data.lumiMask             = ''
#config.Data.unitsPerJob          = 10
config.Data.totalUnits           = -1
config.Data.publication          = True

# This string is used to construct the output dataset name
config.Data.outLFNDirBase        = '/store/user/gallim/HggNano/'

config.section_('Site')
# Where the output files will be transmitted to
config.Site.storageSite          = 'T3_CH_PSI'
```
and submit with `crab submit -c HIG-RunIISummer19UL17NanoAODv2-coffea-test_submit.py`

## Further reading

Some CRAB useful pages: [instructions](https://twiki.cern.ch/twiki/bin/view/CMSPublic/WorkBookCRAB3Tutorial), [advanced tutorial](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3AdvancedTutorial), [FAQs](https://twiki.cern.ch/twiki/bin/view/CMSPublic/CRAB3FAQ#crab_submit_fails_with_Task_coul), [data handling](https://twiki.cern.ch/twiki/bin/view/CMSPublic/Crab3DataHandling#Publication_in_DBS).










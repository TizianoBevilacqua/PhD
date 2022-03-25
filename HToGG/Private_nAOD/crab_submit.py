from WMCore.Configuration import Configuration

config = Configuration()

config.section_('General')
config.General.requestName       = 'HggNANO_UL17_v2_GluGluH'
config.General.transferLogs      = True
config.General.transferOutputs   = True

config.section_('JobType')
config.JobType.pluginName        = 'Analysis'

# Name of the CMSSW configuration file
config.JobType.psetName          = 'HIG-RunIISummer19UL17NanoAODv2-coffea-test_cfg.py'
config.JobType.priority          = 30

config.section_('Data')
# This string determines the primary dataset of the newly-produced outputs.
config.Data.inputDataset         = '/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM'
config.Data.inputDBS             = 'global'
config.Data.splitting            = 'Automatic'
#config.Data.splitting            = 'FileBased'
#config.Data.unitsPerJob          = 10
config.Data.lumiMask             = ''
config.Data.totalUnits           = -1
config.Data.publication          = True

# This string is used to construct the output dataset name
config.Data.outLFNDirBase        = '/store/user/tbevilac'

config.section_('Site')
# Where the output files will be transmitted to
config.Site.storageSite          = 'T3_CH_PSI'

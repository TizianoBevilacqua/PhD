# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename HIG-VHToGG-RunIISummer20UL17NanoAODv2-coffea-test_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer19UL17NanoAODv2-00001.root --conditions 106X_mc2017_realistic_v7 --step NANO --filein dbs:/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM --era Run2_2017,run2_nanoAOD_106Xv1 --no_exec --mc -n 10
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run2_2017_cff import Run2_2017
from Configuration.Eras.Modifier_run2_nanoAOD_106Xv1_cff import run2_nanoAOD_106Xv1

process = cms.Process('NANO',Run2_2017,run2_nanoAOD_106Xv1)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('PhysicsTools.NanoAOD.nano_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/0E060D47-71F3-AB4F-BAF3-681BA66DD888.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/12575E4E-21B4-7C4E-9BDE-678B37D8659C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/1ABF079D-F380-F041-90DC-A0A26E3B9D1C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/20BFE593-685B-E740-B718-D45DBF63507E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/26309999-0C6D-8C43-8888-EC5B9108B17D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/2A6807D4-BA92-444D-99C7-061C5646D9DD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/321CC618-9D98-9A41-A896-A893BC082AC5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/452FD30E-1F42-D744-B2F3-A92FA4CC91BD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/4DE0F8ED-9658-B444-AEBD-1636FF1E510B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/4F637B87-6193-0743-89C2-189884243CDA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/54AA782B-35A9-434C-BA36-E900D6159ABF.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/56DEEE9D-F800-2843-BE13-F29C246462C6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/570CBA86-707E-F549-9F13-B8273A046CF3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/5DE1A867-2F19-0E44-9F93-2B866209577B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/5FC1C0D0-6ED0-6A46-9ABC-8A210E83DD57.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/67E0EB4E-8B93-704A-8FB7-2539EDFDCEA9.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/688B01F8-0B16-9240-A9C8-71C9F4EE8378.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/70539D52-3859-6841-AF11-93727FCAA5E4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/7368C73B-25E2-234B-991C-8475056C2DB1.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/7F9C5592-778C-D24B-8A0E-E30A02675255.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/813478A2-E381-7A42-BDE7-146383D7399E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/8738EAE3-3D39-E747-B1A8-14B336BF7143.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/9292A830-2050-984A-A778-16F4F7CD81BD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/973647AD-FA05-E343-BE4E-82790BF3D548.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/9AA1096A-7A4E-4C41-8821-E0F72E2FFCD8.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/9C1ACD64-5D33-5B4E-8F2F-FBA6A7399CC9.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/A53021C4-7FD6-E64A-A874-6B497E7C50DC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/AED085B0-41DD-0444-8F0E-D3DD54DE006E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/B354FE08-A3F5-AA46-9223-C040AECADEFC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/BEC55BE0-C15E-5343-9A82-D552A515C003.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/C2B5DF9B-D8CE-0D4F-A42B-97082F6EC4B2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/C736E8FD-E041-2545-9F6D-B3B9E805F937.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/CC2F4E9D-81FB-8F48-A69D-7333CCA7DB33.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/CE46C0E9-A81B-CB4E-B7C3-F860C829C5F6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/D6B7A80F-9792-E34D-9358-95FB9C43A835.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/D7D6B885-7474-2546-8CEE-25585D5A0048.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/DF06152F-A8F4-3646-856F-5C82759C7E38.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/DFAE91A2-9AC8-7D4E-A20C-590CF622357A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/E123D1DF-B8D4-8041-802F-E520EC13DA48.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/F43E1AA4-500C-1D4C-9E83-B2A7BF2EA87B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/F58D99A2-C0D0-1B47-9150-90E73286FF09.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2540000/F7E8C9F4-2D12-9045-9EF7-C3A94AC3B926.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

process.NANOAODSIMoutput = cms.OutputModule("NanoAODOutputModule",
    compressionAlgorithm = cms.untracked.string('LZMA'),
    compressionLevel = cms.untracked.int32(9),
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('NANOAODSIM'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:HIG-RunIISummer19UL17NanoAODv2-00001.root'),
    outputCommands = process.NANOAODSIMEventContent.outputCommands
)

# Additional output definition

# Other statements
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '106X_mc2017_realistic_v7', '')

# Path and EndPath definitions
process.nanoAOD_step = cms.Path(process.nanoSequenceMC)
process.endjob_step = cms.EndPath(process.endOfProcess)
process.NANOAODSIMoutput_step = cms.EndPath(process.NANOAODSIMoutput)

# Schedule definition
process.schedule = cms.Schedule(process.nanoAOD_step,process.endjob_step,process.NANOAODSIMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.

# Automatic addition of the customisation function from PhysicsTools.NanoAOD.nano_cff
from PhysicsTools.NanoAOD.nano_cff import nanoAOD_customizeMC 

#call to customisation function nanoAOD_customizeMC imported from PhysicsTools.NanoAOD.nano_cff
process = nanoAOD_customizeMC(process)

# Automatic addition of the customisation function from Configuration.DataProcessing.Utils
from Configuration.DataProcessing.Utils import addMonitoring 

#call to customisation function addMonitoring imported from Configuration.DataProcessing.Utils
process = addMonitoring(process)

# End of customisation functions

# Customisation from command line

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion

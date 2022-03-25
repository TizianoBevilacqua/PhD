# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename HIG-ttHJetToGG-RunIISummer20UL17NanoAODv2-coffea-test_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer19UL17NanoAODv2-00001.root --conditions 106X_mc2017_realistic_v7 --step NANO --filein dbs:/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM --era Run2_2017,run2_nanoAOD_106Xv1 --no_exec --mc -n 10
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
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/007068B9-B4EB-064F-9105-DED67DAC8AEE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/02BA9F0D-A536-9342-A418-BF2A62510286.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/068CC87D-1C76-1344-B766-A13AA4E0A411.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/1AC04F02-85D0-274E-BB1D-532A6C9F94D4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/1DB944D5-D6E1-7D43-9312-8102FAEF33EE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/1E0CE08E-1E40-DE4F-A7AC-ECCCD8EF6F55.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/264A8356-4CE3-884D-A84A-EF21EB64D354.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/2A9AC668-0541-F848-BF23-785F46BE7ECC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/2F634E00-227E-704E-839D-80D51819CC41.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/329B524D-FC72-0E46-A804-7E4632C39D74.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/345FF3C8-7E31-CB48-BC8A-634E67DEBDA2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/363B019D-0D4A-AC42-B0A9-CEBAA3DA7879.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/3B56D724-C195-E147-9097-9A7125C7144C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/43C0C4E3-C693-4449-86CF-3C131E755666.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/510E4D93-67D8-EB44-884E-61E6AAE17D74.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/51E8FDB9-153F-214B-A7DB-D009FC0F2AA2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/55F09232-DCDB-D349-B8DC-689AD6449FBD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/5BAA41CC-5E8F-7F44-B9B1-B15DD5058131.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/613A96B8-D902-7D4F-9D30-DD63F7657EAB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/6756A88F-8E1F-BE4D-8A81-A95354DC4F32.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/6979496E-0097-AE44-A1FD-3D9A3A83A69A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/6B4FA6B4-2E18-5946-AE5B-0FE8D1A35C32.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/7FD61B2A-C9E0-E448-AFCA-0F4F3E7BBADE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/80ADFF2E-8B70-5947-82DD-3320CA4CA74E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/82937271-6512-C442-92F0-7B8488A3B98C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/8E3FD250-636C-E04D-86F6-FDD450E52ABB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/9BB246DB-2C8D-8342-A19B-A0B2602BD82C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/9BBBAC44-BD5B-084F-9888-514A3EF42697.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/9D19C05C-0F22-5F46-A3D1-D39C39DDADEE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/A719FFF1-8AD2-B64D-A44B-5D49079EDD09.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/AA10C597-66CC-274C-8246-3B46FFD7FBB0.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/B14FCC85-197A-F64C-88AB-5EECBAD0BDFE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/B22F7AA2-33CF-9C4C-B4CD-FFD578DAC8B1.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/BB2841F7-851B-0341-8D03-738F4E50E4E5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/BBA742CC-6D88-7E4F-833C-F61746086D8C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/BFA9F16A-0CFD-F547-A5F7-8BD16D95757F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/C3D563E7-98EF-2A44-AE3F-33F1ED2758D0.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/C622C829-B865-1D4E-B598-22AC9928711A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/CC7D9466-9DAA-CC44-ABD0-DD54E8913BB1.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/D1A7A7B8-BDEB-CB4B-B094-D46BE8183455.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/DCFA9CEB-5F82-974A-83C6-1B1E992CDB34.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/E58F3145-5D88-EB4D-A62F-F222A8EC5C6C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/EE8DC6E6-279F-0E47-A086-78E34148A801.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/F06B7A3C-782A-2A4F-A358-63C43E72851C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/F318054C-B778-0B40-8601-DFFC806C7ACD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/F41871E0-EC90-0842-ACD2-43DF7F84AEC5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/F6C7AB2C-14FF-7247-B44F-20CC9F0889AB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/F7BDD474-EB0E-9844-A691-4C00DEF69831.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2560000/FC2D3890-2086-4446-B680-4E10DBF55E12.root'
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

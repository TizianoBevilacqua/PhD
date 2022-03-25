# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename HIG-VBFHToGG-RunIISummer20UL17NanoAODv2-coffea-test_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer19UL17NanoAODv2-00001.root --conditions 106X_mc2017_realistic_v7 --step NANO --filein dbs:/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v2/MINIAODSIM --era Run2_2017,run2_nanoAOD_106Xv1 --no_exec --mc -n 10
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
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/00B8B918-D4E9-2F4B-A914-AFC31132CD36.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/0380A7BE-D6F3-E54A-81F0-64CE96810486.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/099A854F-E34D-C642-975A-1F65CAA8512E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/0BCE5136-51DC-A544-8AC0-B49990A4475E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/16F968A0-5EC0-3F4E-BB3B-E50E2F3C9B0E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/19D5196A-D44A-D245-A0D2-BBF4E33B20FD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/1BFE706E-B4DD-F640-A4A7-BCA0FF9721C4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/1C5C1B39-BE96-3B4B-A7AD-B87357510A54.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/1D4364FD-9B54-5842-82B2-8F3B06023E55.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/1F09F032-2A58-4542-B11D-50A7A953F9B3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/203A1BAB-3587-9340-BE49-A7AED71062E1.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/20CAAC40-CD2B-9345-9A4F-EE444D1462E7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/236C13EB-5963-2344-A420-3BE0DD457650.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/24742EDC-39E6-0E4D-BFD5-A90934FFE185.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/30400955-877A-BA40-A7BB-6BAB75B201EA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/32C8681D-C0AE-6B41-AADC-8325C8CA0839.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/39AAADA0-FF4A-0A45-A733-2D6A30F15656.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/3B419100-EBDA-034C-8D11-869862417B7C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/3E9D94FF-59FC-7D46-828E-D6655639F12F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/3F0AD7DA-8F13-464A-B6EB-588CD1A1B61E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/3F849302-0734-3D43-B618-431611E1A81D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/40D780B4-E372-A741-8F51-47CC414BF44B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/419E2F53-D654-A44E-BD62-916476548DE5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/4351B2C3-6DA5-6C45-828E-275C6DAC59F5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/4459D8B9-8D98-4D45-A815-1884BC716F7E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/465628E0-EF08-4B42-8AEB-CFA144FF5746.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/47212923-2879-214C-BB07-E252DD025BCE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/47B2E1C1-2AC5-0A41-8FC8-FD5627E39634.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/4873692E-37CE-F940-AE45-07BA84F62EE4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/4B65A7AF-C898-CE4B-A679-C6D1A4272134.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/4F9E4E52-D7BB-2A46-8278-5CF9D24B8079.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/50D1803C-DF97-F345-B86E-99118D1E21B8.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/548B8EDE-831E-6F42-9B0E-687A83002EDE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/54DB8D58-601C-9B47-9D4C-DD97F5481B8D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/556F3934-CC0C-F845-BDEF-B48BA2C5A65C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/567B103F-FEBC-4F4E-9398-B930DA737A4D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/5854807D-03D7-7948-8DB6-E8E2CDE12F8D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/58AF78D3-F654-F64E-B130-964F8072C04F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/58FFFF11-6A18-3A47-8014-7962C2891B29.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/59C2496D-B2DF-D042-AB09-71039B973170.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/5ADC126A-D7BE-7648-AE8E-644E47B7BDCF.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/5D9A57A3-A2B3-FF41-9520-0E1CB7D07A01.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/5E63A3E3-5D8D-E84D-8700-A843E8A9BD72.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/61FA528D-26F1-3740-9E59-05E2D8D09FE2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/63B566A7-DEB6-854F-A532-3BD96F71576F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/660AA70A-02D6-9748-B73A-7F6CC1F26800.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/66944581-72D0-5E42-9A9D-5AB4DC3D1B58.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/68B46A5A-8C56-9849-BE96-B0587659125B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/699A417C-C462-C845-B8F2-EE7FC60E8D8A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/69BC755F-3478-6F42-936F-075327618531.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/6A4B33C4-516B-F549-BBAB-BF4909E2BB3D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/6CE010D1-A02B-AC45-A659-B3AFEE6A2F16.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/6DA3174F-18E5-9D49-97FF-A30CF771A762.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/759F0829-F673-C54A-8BC9-6E6DD5126E7F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/76A26034-1DDD-2E48-A45F-124799D6001B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/76F25958-2602-E341-85B8-F0926FADAC40.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/7F3BC1DF-857E-8841-9BBB-3CD8D92FE9B7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/81400CE5-90AF-5540-8FA2-0CF77B419D10.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/8527290C-D388-164C-920E-C18732FCCCCA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/8886B91D-57EC-EE41-9BAB-FA157DBC04BE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/88C9EC37-B81D-ED49-9AF6-EAE5EF22AE83.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/8A425F63-9378-464D-AEC9-49A1F333A7A4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/8D76B854-D51A-0147-AAFF-9F1006C0E13E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/8DCC5EA8-CA41-E54D-A77C-7FDE56BDBC60.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/8EAE8DE3-8E3F-724D-A3DB-50F9A7026BD2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/932CCB58-39C1-954D-BB7D-977691CC2A3C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/96BED094-89D3-9C48-824D-946F414486CE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/96FF5B88-1EBE-5C4C-AAA5-D0B922B728F8.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/97262800-F739-E747-B349-9A05531344DF.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/98644FD3-1154-3E4B-B24A-804C7DF9E2CB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/99930BC6-102E-8043-9F7E-C122B7DCE459.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/99C8675D-5DB8-8146-B346-60EC7401DED5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/9B052EEA-60DE-9C4B-809C-90F1C903EAFB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/9D9C0DB1-975A-2641-8367-62CBB5CD4F48.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/A622C9A3-A50A-CC4B-AC27-576497FDB070.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/A72598CD-2491-2148-80EA-B2D3637B9880.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/ABE39B3F-1ED5-9B47-8812-7B2B45139DC6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/AC36CDE1-4B36-AC46-A544-89349FF87DB5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/AD7F1A99-EEF8-5F40-93B1-1CA7C6824F2C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/AEF80489-61A6-7848-8DC9-3D18C8974AAE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/B15EC03F-A988-2C46-B68B-10EC883EC832.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/B1A60F31-8583-2048-9CE6-335395F1D628.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/B1B97FCC-F899-EF46-A155-3BC7E0A68E39.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/B765DA68-897A-2040-97B6-095AA1F271C5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/BD9FEC56-9857-EE45-807F-FEFC4F6B5509.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/BE6029B9-31C4-2D44-AFC7-4F0261DFE0CD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/BE88E485-251F-7D42-A85C-C76C98CAFE0C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/BF1D8ADE-7D6C-B748-8002-9B2F2D578DD2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/C0D3A7B3-5031-3D4D-8082-DABA9FD1DBD7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/C306A75E-AE51-584D-95E0-27DDD02E453F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/C44B6267-BA01-3A46-8CAB-4A1283378CAA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/C639DA26-DD9E-3D4D-A3BC-A65CA184C007.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/C65503EA-7413-CA4F-B70E-AF7185E2FF03.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/CB6FF3BF-9EFB-F44B-934D-02CD476E655E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/CEB638DE-1A1E-F542-97B2-EFE8BD68F1C2.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/CF55A916-8191-1F43-A487-BB02941CF6D3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/D5D6365E-A013-6C42-81DF-93131B99AE32.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/D8371792-C668-584C-93A3-2FFDBFADC5C1.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/D8FAACF3-D930-CF42-B90A-DA8AB4CAAC75.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/D92CF028-698F-4E4C-989C-B2BAF9F7ECFB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/DB9E135F-51AA-7744-8F2D-358CD936818F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/DCFB2FED-EE22-8E4F-9154-E31CA7277597.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/DD03F9B7-56AD-E340-91FF-DA8D222F3EF6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/DEE27589-0E5B-394D-8544-716FCF0CC5CE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/E061D241-C8F4-4949-9DE7-53011DC3CDAE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/E2FA6B6F-0E5D-BE4C-A8CA-4989885E16DB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/E3AA29B3-1408-804B-854F-F7C30C2D8CE9.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/E999B89A-1830-D949-9BEA-417C17DC1540.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/EA974195-7426-2440-96C6-9B352B4F1707.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/EC2FE23E-11AD-5546-B046-7811EE2BDF75.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/EC7DDE19-A826-E14C-B12C-8BF1D9CBA973.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/EC99CD4C-34FC-0F4A-BCD7-1820C818DD8D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/ED3E98D9-7B27-9A4E-BB57-49F69F8354C9.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/EF398580-B7EA-1C44-8B6D-061C8306238A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/F1D98C9C-CA17-C843-85CA-6CB0820C0F75.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/F5F34D6C-73A0-9C45-AB79-48C6B31EF4A9.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/F6E3217F-609E-F949-91A3-142B560A2020.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/F9601DFD-5FE2-1343-96FB-F27707424469.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/F9B99278-2E30-B947-AFAB-9A220C4A7091.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/FAADF4AD-190B-C142-9DC3-18DB7E67A83D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/FCE90468-BE9C-0546-BBBF-C496E556150E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/FD3BC88C-F180-EB4C-8244-544B0167BE61.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/FE5ABADC-C677-4945-A3BB-0328C9533D58.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v2/2550000/FF1BAD91-9DC8-634D-B288-35DB6A77F6BC.root'
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

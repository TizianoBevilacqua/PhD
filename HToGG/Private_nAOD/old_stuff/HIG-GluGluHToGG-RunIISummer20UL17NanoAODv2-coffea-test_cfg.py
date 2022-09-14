# Auto generated configuration file
# using: 
# Revision: 1.19 
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v 
# with command line options: --python_filename HIG-RunIISummer19UL17NanoAODv2-coffea-test_cfg.py --eventcontent NANOAODSIM --customise Configuration/DataProcessing/Utils.addMonitoring --datatier NANOAODSIM --fileout file:HIG-RunIISummer19UL17NanoAODv2-00001.root --conditions 106X_mc2017_realistic_v7 --step NANO --filein dbs:/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/RunIISummer20UL17MiniAOD-106X_mc2017_realistic_v6-v1/MINIAODSIM --era Run2_2017,run2_nanoAOD_106Xv1 --no_exec --mc -n -1
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
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/02CF1923-3AE9-A040-B7F1-0C497987A25A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/07C15FDF-5E41-1D46-95FB-84C606EB320A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/09E8818A-65C6-AA48-A802-4FED7F5141C0.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/0FE9FC98-2156-1145-9124-2F53F405E066.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/1C3234C3-6D19-5942-BCB8-6438E81D61B5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/1C5822ED-A273-D240-BF2E-21A8601B54E7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/1D7CB1FD-5089-D542-9507-B0100284CE74.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/28BFC182-73C4-BA41-9B06-054D392D152C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/301C4FE7-AD48-584A-B83B-E02DC9515DEC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/35DB1882-74A3-0140-952B-FD452354C4F0.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/40D3146F-CD40-4F47-BA38-AF96327DFF27.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/45D02C61-3F8D-1644-B4C1-9B8E192A378F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/463D14E9-706B-F443-B79E-C53F6259D707.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/4662CACB-F27F-0A4B-A575-A26571EF7E82.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/4CEA887D-9DE2-7149-96F5-E45189230890.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/56278137-06D2-984E-87F8-DBDF270107F3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/65FE36B3-C892-6A49-B147-E77749808C54.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/71605BBF-3B33-E248-B02A-7FC5E488B75F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/71AE8D2C-649B-6F43-8B95-04CB18D60DCD.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/7548B4A4-3E85-424F-BD42-F52AA0218640.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/7E6E2139-08F7-E649-8D1A-19D87B69A174.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/85C814C3-965E-4C44-A9BB-387D5A9EE43E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/8968D8ED-FCBC-7347-9AA2-E92044034E99.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/9CE9057D-9C47-3245-8E7D-50CABC4A5C45.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/9F55253B-C53A-1748-A7AC-D1EC6F500AE4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/B42934B1-3A1E-494C-BE49-BE25F557949A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/BA9A4FEF-1BAE-0545-B525-925F7456B4A4.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/D816C7DD-E2B1-4B4F-BE40-FE5EE3C479CA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/DCE81570-BEC6-3843-9A44-4659BEECE4AC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/DEC7EA79-1B58-3B4F-90CE-29496CA17F75.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/E9180C8A-A91D-E542-929A-4C06165C547D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/E975B5A8-1475-8B45-A6EA-12F10A227EAE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/EBB00C48-820B-D54D-A087-ABC40D79EF6D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/F069FC9D-55A9-2E4A-B92A-D3B54C8286F7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/F55AFE4E-7FDE-D241-92B1-A9B52A64545E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/2560000/F7E79878-7684-6846-ADC5-60C542E7A124.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/0177CB46-54D7-E541-8483-75BDB1F0A93C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/08044C27-0319-6547-8BE3-955F19A6CCEC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/1B31E5E4-ED14-AA4D-B5F4-6B1FE1269FDC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/2DABD4CE-9338-6044-92F2-CA58F7079D96.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/2F365238-2D8E-0C40-B68B-2A57AE821CD3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/34784E7E-A693-344D-A6E9-6DFBCE0DA3CB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/354017C5-A47F-684C-AC0A-B034D3C25232.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/3A377299-776D-584A-9E8E-337773496429.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/3CEE097E-E8F0-5E42-97F5-275B09F08E92.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/401AB9A1-1B18-4A48-BAAD-4BF54D92F762.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/50750F67-56A7-EC48-8A78-99CB530C69E7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/550A73A4-B665-0842-A2DC-78093B1F39BE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/556623E3-3687-8C4E-8884-65CEAA11CAFC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/55C305EF-AC74-9C41-84C1-B5C2C602300E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/573227E3-7729-A74D-AE01-9966B95D75D6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/57648D97-1855-404D-A945-6F159D172AAF.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/592E28E3-E740-8F4D-9BFD-955AA4D0AA85.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/60E39020-3E62-5B4D-BB09-0C7E7C0DEDCE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/63548CBB-6A9B-7A40-B80E-79978DDA8834.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/65E29039-37D6-9C46-A55B-2099058C7930.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/677B4FD8-6DBD-1945-9AC4-597AA109C8D0.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/67B9AD45-361B-1E46-82CC-4BDF25FB00B5.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/67F92400-1D46-5544-BB7C-9E73C287995C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/6B52B923-95BF-4541-BC1C-52D689A4D036.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/6BDA6E85-49C7-A444-A09B-189EFC7BA689.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/6DB22E66-CC35-D047-B536-0EAE09D5A014.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/720A9928-F0B9-6F40-8EC9-F4A5DD32E9C7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/7738278F-C800-0444-8735-C238CDE0E918.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/7B409887-6BA7-9F43-B204-3DD5753534BE.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/7D817738-EDF6-AC40-AFB2-4D722E195078.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/86247CF6-648E-3A43-9887-2583C00A3CB9.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/8C2BA550-E34B-D84F-A925-3126BB639670.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/92BF7E31-7B49-7145-9E5F-976E3EC8AA2E.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/939B1C9C-F5CF-FD43-8CDB-EE8DBF4B464C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/94CAF035-7D07-DF41-A15A-E7B532A36106.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/9CD5032B-C112-EB46-92F5-8790C74784D3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/A48D049D-1652-3A43-AD6A-4D3BBBB76B5C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/A525E489-D58E-D846-944E-2ED720C8291D.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/AFB79E59-951D-004F-8CBD-DDBD324455FC.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/B4D7EA96-7575-1A40-9231-007A095FADC7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/B56D7B74-9981-CC43-8D96-E237A4CF67BA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/B832715E-E1B6-8543-A001-BCF7554B6208.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/B9DFBD26-7F80-2B4E-922C-38D731E57F6F.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/BCC05570-1D1A-F94A-BC67-2C0F11AF1DAB.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/C09259B3-0172-8F4C-8118-F04833DFE5D6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/C185ACE8-5477-3B48-8783-44275B876EE3.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/C236875A-20B8-2B4F-8CBB-C09DB4C27902.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/C4395505-EA6F-B246-A0C1-3148B32849D7.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/CA9A7E63-8FC7-1B49-99B7-C4AC7CFB8EAA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/D5B1D661-0BA2-7141-B659-E1A20DB51C5B.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/DA54A8EA-9156-E247-89A3-E44BF88EFD80.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/DB65B786-B451-514E-8911-8D9F01AEF77C.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/E3DEA73C-5146-8644-A497-91936C4941F6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/E7B67C4A-EE9E-0C47-BF95-158DC29963B6.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/EC0745BC-6784-384E-959A-68F1D66C2894.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/F2BBCCF3-5F05-CD47-BC16-57C8B91C2C34.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/F43B375B-2875-8545-B2CB-AACDFA56F4CA.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/F582C92F-4965-E342-BD13-82559FC979E8.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/F8714570-B12E-F54A-A7C0-567FC7BEACE1.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/FC0EBB87-A5E0-FA4B-991D-7D46C082168A.root', 
        '/store/mc/RunIISummer20UL17MiniAOD/GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8/MINIAODSIM/106X_mc2017_realistic_v6-v1/30000/FC0FD67F-0511-EA42-8DB8-F38EB05534C5.root'
    ),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('--python_filename nevts:-1'),
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
    fileName = cms.untracked.string('file:HIG-GluGluHToGG-RunIISummer20UL17NanoAODv2-00001.root'),
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

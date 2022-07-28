# Bookkeeping file for HToGG ANs and MC samples:

## Relevant Analysis Notes:
* [AN2020_088](http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2020_088_v9.pdf) SM H -¿ gg differential and fiducial cross sections (full run 2): Table of samples  
* [AN2018_249](http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2018_249_v9.pdf) Search for low mass resonances in the diphoton final state in pp collisions at √s =13 TeV with the 2017 and 2018 dataset: Table of MC samples
* [AN2019_259](http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2019_259_v17.pdf) Measurements of Higgs boson properties in the diphoton decay channel using the full Run 2 dataset: yields (?) pag 100
* [AN2019_149](http://cms.cern.ch/iCMS/jsp/openfile.jsp?tp=draft&files=AN2019_149_v5.pdf) Common tools for analyses of Higgs boson decay in the diphoton final state: MC and Data Samples

## Sample used up to now:
### Signal
* ttHJetToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2_MINIAODSIM :       Xsec (0.5071)
* GluGluHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-pythia8_storeWeights_RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_MINIAODSIM : Xsec (48.58)
* VBFHToGG_M125_TuneCP5_13TeV-amcatnlo-pythia8_storeWeights_RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_MINIAODSIM :        Xsec (3.782) 
* VHToGG_M125_TuneCP5_13TeV-amcatnloFXFX-madspin-pythia8_RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2_MINIAODSIM :           Xsec (1.896)
### Background
* DiPhotonJetsBox_M40_80-sherpa/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM :                                    Xsec (303.2)
* DiPhotonJetsBox_MGG-80toInf_13TeV-sherpa/RunIISummer20UL16MiniAODAPVv2-106X_mcRun2_asymptotic_preVFP_v11-v2/MINIAODSIM :             Xsec (84.4)
* GJets_HT-40To100_TuneCP5_13TeV-madgraphMLM-pythia8_RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_MINIAODSIM :               Xsec (23100)
* GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8_RunIISummer19UL17MiniAODv2-4cores5k_106X_mc2017_realistic_v9-v1_MINIAODSIM :     Xsec (9110)
* GJets_HT-200To400_TuneCP5_13TeV-madgraphMLM-pythia8_RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_MINIAODSIM :              Xsec (2280)
* GJets_HT-400To600_TuneCP5_13TeV-madgraphMLM-pythia8_RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_MINIAODSIM :              Xsec (273)
* GJets_HT-600ToInf_TuneCP5_13TeV-madgraphMLM-pythia8_RunIISummer19UL17MiniAODv2-106X_mc2017_realistic_v9-v1_MINIAODSIM :              Xsec (94.5)
* DYJetsToLL_M-50_TuneCP5_13TeV-madgraphMLM-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM :                Xsec (6225.42)
* QCD_Pt-40ToInf_DoubleEMEnriched_MGG-80ToInf_TuneCP5_13TeV-pythia8/RunIISummer20UL17MiniAODv2-106X_mc2017_realistic_v9-v2/MINIAODSIM: Xsec (118100)
### Data
* DoubleEG_Run2017B-UL2017_MiniAODv2-v1_MINIAOD
* DoubleEG_Run2017C-UL2017_MiniAODv2-v1_MINIAOD
* DoubleEG_Run2017D-UL2017_MiniAODv2-v1_MINIAOD
* DoubleEG_Run2017E-UL2017_MiniAODv2-v1_MINIAOD
* DoubleEG_Run2017F-UL2017_MiniAODv2-v1_MINIAOD

## Completely converted samples:
### Data 2017:
* DoubleEG_Run2017C-UL2017 Delivered lumi (5.107925250 /fb) Recorded lumi (4.802294592 /fb)
* DoubleEG_Run2017C-UL2017 Delivered lumi (10.57034756 /fb) Recorded lumi (9.695726055 /fb)
### BG 2017
* GJets_HT-100To200
* GJets_HT-200To400
* GJets_HT-400To600
* GJets_HT-600ToInf
* QCD


# Private samples cross section summary:


4FS-FXFX:
```
------------------------------------
GenXsecAnalyzer:
------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Overall cross-section summary 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Process		xsec_before [pb]		passed	nposw	nnegw	tried	nposw	nnegw 	xsec_match [pb]			accepted [%]	 event_eff [%]
0		8.110e-02 +/- 2.278e-04		82087	69909	12178	94781	82532	12249	6.662e-02 +/- 2.234e-04		82.1 +/- 0.2	86.6 +/- 0.1
1		6.374e-02 +/- 3.203e-04		56364	38856	17508	305219	181011	124208	2.396e-02 +/- 2.939e-04		37.6 +/- 0.4	18.5 +/- 0.1
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Total		1.448e-01 +/- 3.930e-04		138451	108765	29686	400000	263543	136457	9.013e-02 +/- 4.659e-04		62.2 +/- 0.3	34.6 +/- 0.1
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Before matching: total cross section = 1.448e-01 +- 3.930e-04 pb
After matching: total cross section = 9.013e-02 +- 4.659e-04 pb
Matching efficiency = 0.3 +/- 0.0   [TO BE USED IN MCM]
Filter efficiency (taking into account weights)= (36304) / (36304) = 1.000e+00 +- 0.000e+00
Filter efficiency (event-level)= (138451) / (138451) = 1.000e+00 +- 0.000e+00    [TO BE USED IN MCM]

After filter: final cross section = 9.013e-02 +- 4.659e-04 pb
After filter: final fraction of events with negative weights = 2.144e-01 +- 1.550e-04
After filter: final equivalent lumi for 1M events (1/fb) = 3.620e+03 +- 1.111e+01

=============================================
```
4FS:
```
------------------------------------
GenXsecAnalyzer:
------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Overall cross-section summary 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Process		xsec_before [pb]		passed	nposw	nnegw	tried	nposw	nnegw 	xsec_match [pb]			accepted [%]	 event_eff [%]
0		8.065e-02 +/- 7.943e-05		1000000	873576	126424	1000000	873576	126424	8.065e-02 +/- 7.943e-05		100.0 +/- 0.0	100.0 +/- 0.0
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Total		8.065e-02 +/- 7.943e-05		1000000	873576	126424	1000000	873576	126424	8.065e-02 +/- 7.943e-05		100.0 +/- 0.0	100.0 +/- 0.0
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Before matching: total cross section = 8.065e-02 +- 7.943e-05 pb
After matching: total cross section = 8.065e-02 +- 7.943e-05 pb
Matching efficiency = 1.0 +/- 0.0   [TO BE USED IN MCM]
Filter efficiency (taking into account weights)= (80562.9) / (80562.9) = 1.000e+00 +- 0.000e+00
Filter efficiency (event-level)= (1e+06) / (1e+06) = 1.000e+00 +- 0.000e+00    [TO BE USED IN MCM]

After filter: final cross section = 8.065e-02 +- 7.943e-05 pb
After filter: final fraction of events with negative weights = 1.264e-01 +- 1.514e-05
After filter: final equivalent lumi for 1M events (1/fb) = 6.922e+03 +- 7.271e+00

=============================================
```
3FS:
```
------------------------------------
GenXsecAnalyzer:
------------------------------------
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Overall cross-section summary 
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Process		xsec_before [pb]		passed	nposw	nnegw	tried	nposw	nnegw 	xsec_match [pb]			accepted [%]	 event_eff [%]
0		4.987e-02 +/- 3.747e-04		1000000	601722	398278	1000000	601722	398278	4.987e-02 +/- 3.747e-04		100.0 +/- 0.0	100.0 +/- 0.0
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------- 
Total		4.987e-02 +/- 3.747e-04		1000000	601722	398278	1000000	601722	398278	4.987e-02 +/- 3.747e-04		100.0 +/- 0.0	100.0 +/- 0.0
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Before matching: total cross section = 4.987e-02 +- 3.747e-04 pb
After matching: total cross section = 4.987e-02 +- 3.747e-04 pb
Matching efficiency = 1.0 +/- 0.0   [TO BE USED IN MCM]
Filter efficiency (taking into account weights)= (50432.5) / (50432.5) = 1.000e+00 +- 0.000e+00
Filter efficiency (event-level)= (1e+06) / (1e+06) = 1.000e+00 +- 0.000e+00    [TO BE USED IN MCM]

After filter: final cross section = 4.987e-02 +- 3.747e-04 pb
After filter: final fraction of events with negative weights = 3.983e-01 +- 1.234e-04
After filter: final equivalent lumi for 1M events (1/fb) = 8.299e+02 +- 1.343e+00

=============================================
```

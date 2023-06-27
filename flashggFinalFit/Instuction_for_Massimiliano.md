# SETUP

```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_2_13
cd CMSSW_10_2_13/src
cmsenv
git cms-init

# Install the GBRLikelihood package which contains the RooDoubleCBFast implementation
git clone git@github.com:jonathon-langford/HiggsAnalysis.git

# Install Combine as per the documentation here: cms-analysis.github.io/HiggsAnalysis-CombinedLimit/
git clone git@github.com:cms-analysis/HiggsAnalysis-CombinedLimit.git HiggsAnalysis/CombinedLimit

# Checkout previous combine tag (fits are failing in latest, to be investigated!)
cd HiggsAnalysis/CombinedLimit
git checkout tags/v8.1.0
cd ../..

# Install Combine Harvester for parallelizing fits
git clone https://github.com/cms-analysis/CombineHarvester.git CombineHarvester

# Compile external libraries
cmsenv
scram b -j 9

# Install Flashgg Final Fit packages
git clone ssh://git@gitlab.cern.ch:7999/tbevilac/flashggfinalfits.git flashggFinalFit
cd flashggFinalFit/
mkdir higgs_dna_signals_2017
cd higgs_dna_signals_2017
wget https://tiziano-bevilacqua.web.cern.ch/finalfit/higgs_dna_signals_2017/allData.root
wget https://tiziano-bevilacqua.web.cern.ch/finalfit/higgs_dna_signals_2017/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_GG2H_WStest.root
wget https://tiziano-bevilacqua.web.cern.ch/finalfit/higgs_dna_signals_2017/output_TTHToGG_M125_13TeV_amcatnloFXFX_pythia8_TTH_WStest.root
wget https://tiziano-bevilacqua.web.cern.ch/finalfit/higgs_dna_signals_2017/output_VBFHToGG_M125_13TeV_amcatnloFXFX_pythia8_VBF_WStest.root
wget https://tiziano-bevilacqua.web.cern.ch/finalfit/higgs_dna_signals_2017/output_VHToGG_M125_13TeV_amcatnloFXFX_pythia8_vh_WStest.root
cd ..

source setup.sh
```

# SIGNAL

```
cd Signal

python RunSignalScripts.py --inputConfig config_hdna_test_2017_cats.py --mode fTest --modeOpts "--doPlots --skipWV"

python RunSignalScripts.py --inputConfig config_hdna_test_2017_cats.py --mode calcPhotonSyst # optional if you use this remove --skipSystematics in next command

python RunSignalScripts.py --inputConfig config_hdna_test_2017.py --mode signalFit --modeOpts "--skipVertexScenarioSplit --skipSystematics --doPlots --doEffAccFromJson"

python RunPackager.py --cats auto --inputWSDir ../higgs_dna_signals_2017_cats --ext test_hdna --batch local --massPoints 125 --year 2017

cd ..
```

# Background

```
cd Background

make

python RunBackgroundScripts.py --inputConfig config_hdna_test.py --mode fTestParallel

cd ..
```

# DATACARD

```
cd Datacard

python RunYields.py --inputWSDirMap 2017=../higgs_dna_signals_2017 --cats auto --procs auto --batch local --ext test_higgsdna

# or if you have systematics (active ones defined in systematics.py)
python RunYields.py --inputWSDirMap 2017=../higgs_dna_signals_2017 --cats auto --procs auto --batch local --ext test_higgsdna --doSystematics 

rm Datacard.txt

python makeDatacard.py --years 2017 --ext test_higgsdna --doSystematics

python cleanDatacard.py --datacard Datacard.txt --factor 2 --removeDoubleSided

cd ..
```

# COMBINE
```
cd Combine

mkdir Models
mkdir Models/signal
mkdir Models/background

cp ../Signal/outdir_packaged/CMS-HGG_sigfit_packaged_WStest_2017.root Models/signal/
cp ../Background/outdir_test_hdna/CMS-HGG_multipdf_WStest.root Models/background/CMS-HGG_multipdf_WStest_2017.root
cp ../Datacard/Datacard.txt .

python RunText2Workspace.py --mode mu_inclusive --batch local

python RunFits.py --inputJson inputs.json --mode mu_inclusive --dryRun

cd runFits_mu_inclusive

# Fix manually the condor_profile1D_syst_r.sh script to be runnable locally

sh condor_profile1D_syst_r.sh
```








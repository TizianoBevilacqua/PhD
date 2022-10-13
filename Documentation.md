# DOCUMENTATION 

## GENERAL ##

### PROXY
```
voms-proxy-init --valid 192:00 --voms cms
voms-proxy-info -all | grep -Ei "role|subject"
```

To use the Grid access one needs a Grid Certificate granted by CERN to users with a computing account. 

To request a new Grid Certificate one has to go to [this page](https://ca.cern.ch/ca/) and click on `New Grid User Certificate` option.
After that a password have to be decided and the certificate can be downloaded.

To install and use the certificate:

* Copy the new Grid Certificate on the machine with which you want to access the grid: **PSI tier3** -> `/t3home/bevila_t/.globus`, **lxplus** -> `/afs/cern.ch/user/t/tbevilac/.globus`, **private mac** -> `/Users/tiziano-bevilacqua/.globus`
* Extrack the public and private keys with (assuming your certificate is calle `myCert.p12`):
```
openssl pkcs12 -in myCert.p12 -clcerts -nokeys -out $HOME/.globus/usercert.pem
openssl pkcs12 -in myCert.p12 -nocerts -out $HOME/.globus/userkey.pem
```
* You must set the mode on your `userkey.pem` file to read/write only by the owner, otherwise `voms-proxy-init` will not use it:
```
chmod 600 $HOME/.globus/userkey.pem
chmod 600 $HOME/.globus/usercert.pem
```
and then delete `myCert.p12`, further informations on this matter, including how to import the certificate on Browsers can be found [here](https://ca.cern.ch/ca/Help/?kbid=021001)

### CMSSW
To build:
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_18
cmsenv
git cms-init
```
the last command synch also all the tags from the central remore directory that contains the "official" CMSSW, it also create a personal directory under the name `my-cmssw`. To make changes and eventually propose modifications to the central code one has to create a new branch, connect it to his own fork and commit the changhes. All this can be done with the following commands:
```
git checkout -b <new-branch>
git push my-cmssw <new-branch> 
```
now git knows that the new branch and your fork are connected, so you can directly commit and push changes to your private area.
```
git add new-stuff
git commit -m "adding new-stuff"
git push my-cmssw
```
Further info can be found [here](http://cms-sw.github.io/tutorial.html)

To know which CMSSW releases are available: 
```
scram list CMSSW
```

To dump information about what is called during execution with cmsRun
```
open('tmptmp.py', 'w').write(process.dumpPython())
```

### CRAB 
After setting up the CMSSW environment, it is possible to use CRAB from any directory. One can check that the crab command is indeed available and the version being used by executing: `which crab`
Check if you can write to the `/store/user/` area:
```
voms-proxy-init -voms cms
crab checkwrite --site=T3_US_FNALLPC
```
### CMSSW Configuration to generate MC events

### CMS filesystem 
To access documentation:
* [DAS](https://cmsweb.cern.ch/das/) finds files through queries:
```
dataset = /PrimaryDataset/ProcessingVersion/DataTier
dataset release=CMSSW_10_6_14 dataset=/RelValZMM*/*CMSSW_10_6_14*/MINIAOD*
dataset file=/store/relval/CMSSW_10_6_14/RelValZMM_13/MINIAODSIM/106X_mc2017_realistic_v7-v1/10000/0EB976F4-F84B-814D-88DA-CB2C29A52D72.root
```
from command line:
```
dasgoclient --query="dataset=/DoubleMuon/Run2018A-12Nov2019_UL2018-v2/MINIAOD" --format=plain
```
* [CMS OMS](https://cmsoms.cern.ch/cms/index/index) find informations on runs 
* [CMS McM](https://cms-pdmv.cern.ch/mcm/) find mc samples 
* [CMS GrASP](https://cms-pdmv.cern.ch/grasp) find datasets and mc samples. One has to self register [here](https://cms-pdmv.cern.ch/mcm/users?page=0&shown=51), by pressing the button in the bottom left corner “add me”. It takes a while to propagate the changes
* [CDS](https://cds.cern.ch/) find CMS thesis and documents
* [iCMS](https://cms.cern.ch/iCMS/analysisadmin/cadilines?awg=HIG&awgyear=2015) find AN and papers
* [CADi](https://cms.cern.ch/iCMS/analysisadmin/cadilines?id=2293&ancode=HIG-19-016&tp=an&line=HIG-19-016) find AN and papers 
* [GlobalTags](https://github.com/cms-sw/cmssw/blob/CMSSW_12_4_8/Configuration/AlCa/python/autoCond.py), this is for CMSSW_12_4_8, changing branch one can look for what he/she needs.

To access files with XRootD the prefix is:
```
root://cms-xrd-global.cern.ch//store/etc/etc
```
To list dir content with xrd:
```
xrdfs redirector.t2.ucsd.edu ls /store/user/hmei/nanoaod_runII/HHggtautau/GJets_HT-100To200_TuneCP5_13TeV-madgraphMLM-pythia8_RunIIFall17MiniAODv2-PU2017_12Apr2018_94X_mc2017_realistic_v14-v1_MINIAODSIM_v0.6_20201021
```
To find files in the filesystem from command line another option is:
```
edmFileUtil -d /store/relval/CMSSW_10_6_14/RelValZMM_13/MINIAODSIM/106X_mc2017_realistic_v7-v1/10000/0EB976F4-F84B-814D-88DA-CB2C29A52D72.root
```
To dump a summary of the products that are contained within the file:
```
edmDumpEventContent --all --regex slimmedMuons root://cmsxrootd-site.fnal.gov//store/relval/CMSSW_10_6_14/RelValZMM_13/MINIAODSIM/106X_mc2017_realistic_v7-v1/10000/0EB976F4-F84B-814D-88DA-CB2C29A52D72.root
```
To print out all the tracked parameters used to create the data file:
```
edmProvDump root://cmsxrootd-site.fnal.gov//store/relval/CMSSW_10_6_14/RelValZMM_13/MINIAODSIM/106X_mc2017_realistic_v7-v1/10000/0EB976F4-F84B-814D-88DA-CB2C29A52D72.root > EdmProvDump.txt
```
To determine the size of different branches in the data file:
```
edmEventSize -v `edmFileUtil -d /store/relval/CMSSW_10_6_14/RelValZMM_13/MINIAODSIM/106X_mc2017_realistic_v7-v1/10000/0EB976F4-F84B-814D-88DA-CB2C29A52D72.root` > EdmEventSize.txt 
```
### Luminosity

To calculate luminosity of Datasets one must use brilcalc tool. I installed it on `lxplus` under: `/afs/cern.ch/user/t/tbevilac/.local/bin`.
To check the good section of runs the Golden json can be found here: `/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/`

To run brilcalc use for example
```
brilcalc lumi -c web -i Runs_2017B_brilcalc.json -u /fb
```
or 
```
brilcalc lumi --normtag /cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json -u /fb  --begin 7920 --end  8210 
```
where `begin` and `end` are fill numbers

### FWLite ANALYSIS
Adding FWLite to CMSSW:
```
git cms-addpkg PhysicsTools/FWLite
scram b
cmsenv
```
Loading FWLite in root:
```
root -l
gSystem->Load("libFWCoreFWLite.so");
FWLiteEnabler::enable();
gSystem->Load("libDataFormatsFWLite.so");
gROOT->SetStyle ("Plain");
gStyle->SetOptStat(111111);

TFile *theFile = TFile::Open("root://cmseos.fnal.gov//store/user/cmsdas/2022/pre_exercises/Set1/CMSDataAnaSch_Data_706_MiniAOD.root");
Events->Draw("patMuons_slimmedMuons__PAT.obj.pt()")
```
Using FWlite to create histograms:
```
FWLiteHistograms inputFiles=slimMiniAOD_data_MuEle.root outputFile=ZPeak_data.root maxEvents=-1 outputEvery=100
```

### DATA ANALISYS SCHOOL  
Logging in to the cmslpc-sl7:
```
kinit tbevilac@FNAL.GOV (tbWed11172146#)
ssh -Y tbevilac@cmslpc-sl7.fnal.gov
```

### ROOT commands ##
List of ROOT executables:
* `rootbrowse`: Open a ROOT file and a TBrowser
* `rootls`: List file content, tree branches, objects’ stats
* `rootcp`: Copy objects within a file or between files
* `rootdrawtree`: Simple analyses from the command line
* `rooteventselector`: Select branches, events, compression algorithms and extract slimmer trees
* `rootmkdir`: Creates a directory in a TFile
* `rootmv`: Move objects between files
* `rootprint`: Print objects in plots on files
* `rootrm`: Remove objects from files

Convert ROOT to numpy with `RDataFrame`:
```
# Read out the data as a dictionary of numpy arrays
import ROOT
df = ROOT.RDataFrame('TreeS', 'https://root.cern/files/tmva_class_example.root')
columns = ['var1', 'var2', 'var3', 'var4']
data = df.AsNumpy(columns)
print('var1: {}'.format(data['var1']))
```
Below is an example that computes the mean of each column:
```
print('Means: {}'.format([np.mean(data[c]).item() for c in columns]))
```
Another interesting usecase is moving the dataset directly to a pandas dataframe. You can use the output of AsNumpy directly as input to its constructor:
```
import pandas
pdf = pandas.DataFrame(data)
print(pdf)
```

Enable multi-threading with the specified amount of threads (let's start with just one)
Note that older ROOT versions may require to write ROOT.ROOT.EnableImplicitMT()
```
ROOT.EnableImplicitMT(1)
# Or enable multi-threading with an auto-detected amount of threads
#ROOT.EnableImplicitMT()
```
Stuff from das:
```
# Create dataframe from a (reduced) NanoAOD file
df = ROOT.RDataFrame("Events", "Run2012BC_DoubleMuParked_Muons.root")

# For simplicity, select only events with exactly two muons and require opposite charge
df_2mu = df.Filter("nMuon == 2", "Events with exactly two muons")
df_os = df_2mu.Filter("Muon_charge[0] != Muon_charge[1]", "Muons with opposite charge")

# Compute invariant mass of the dimuon system
# Perform the computation of the invariant mass in C++
ROOT.gInterpreter.Declare('''
using Vec_t = const ROOT::RVec<float>&;
float ComputeInvariantMass(Vec_t pt, Vec_t eta, Vec_t phi, Vec_t mass) {
    const ROOT::Math::PtEtaPhiMVector p1(pt[0], eta[0], phi[0], mass[0]);
    const ROOT::Math::PtEtaPhiMVector p2(pt[1], eta[1], phi[1], mass[1]);
    return (p1 + p2).M();
}
''')

# Add the result of the computation to the dataframe
df_mass = df_os.Define("Dimuon_mass", "ComputeInvariantMass(Muon_pt, Muon_eta, Muon_phi, Muon_mass)")

# Book histogram of the dimuon mass spectrum (does not actually run the computation!)
h = df_mass.Histo1D(("Dimuon_mass", ";m_{#mu#mu} (GeV);N_{Events}", 30000, 0.25, 300), "Dimuon_mass")

# Request a cut-flow report (also does not run the computation yet!)
report = df_mass.Report()
```
you have to keep the Python interpreter running to investigate the plot interactively. You can do this with python -i your_script.py

### DAS

#### Jet exercise

#### Jet Types and Algorithms
The jet algorithms take as input a set of 4-vectors. At CMS, the most popular jet type is the "Particle Flow Jet", which attempts to use the entire detector at once and derive single four-vectors representing specific particles.For this reason it is very comparable (ideally) to clustering generator-level four-vectors also.
#### Particle Flow Jets (PFJets)
Particle Flow candidates (PFCandidates) combine information from various detectors to make a combined estimation of particle properties based on their assigned identities (photon, electron, muon, charged hadron, neutral hadron).
PFJets are created by clustering PFCandidates into jets, and contain information about contributions of every particle class: Electromagnetic/hadronic, Charged/neutral etc.
The jet response is high. The jet pT resolution is good: starting at 15--20% at low pT and asymptotically reaching 5% at high pT.
#### Monte Carlo Generator-level Jets (GenJets)
GenJets are pure Monte Carlo simulated jets. They are useful for analysis with MC samples. GenJets are formed by clustering the four-momenta of Monte Carlo truth particles. This may include “invisible” particles (muons, neutrinos, WIMPs, etc.).
As there are no detector effects involved, the jet response (or jet energy scale) is 1, and the jet resolution is perfect, by definition.
GenJets include information about the 4-vectors of the constituent particles, the hadronic and electromagnetic components of the energy etc.
#### Calorimeter Jets (CaloJets)
CaloJets are formed from energy deposits in the calorimeters (hadronic and electromagnetic), with no tracking information considered. In the barrel region, a calorimeter tower consists of a single HCAL cell and the associated 5x5 array of ECAL crystals (the HCAL-ECAL association is similar but more complicated in the endcap region). The four-momentum of a tower is assigned from the energy of the tower, assuming zero mass, with the direction corresponding to the tower position from the interaction point.
In CMS, CaloJets are used less often than PFJets. Examples of their use include performance studies to disentangle tracker and calorimeter effects, and trigger-level analyses where the tracker is neglected to reduce the event processing time. ATLAS makes much more use of CaloJets, as their version of particle flow is not as mature as CMS's.

#### Jet ID
In order to avoid using fake jets, which can originate from a hot calorimeter cell or electronic read-out box, we need to require some basic quality criteria for jets. These criteria are collectively called "jet ID". Details on the jet ID for PFJets can be found in the following twiki:
https://twiki.cern.ch/twiki/bin/viewauth/CMS/JetID
The JetMET POG recommends a single jet ID for most physics analysess in CMS, which corresponds to what used to be called the tight Jet ID. Some important observations from the above twiki:
Jet ID is defined for uncorrected jets only. Never apply jet ID on corrected jets. This means that in your analysis you should apply jet ID first, and then apply JECs on those jets that pass jet ID.
Jet ID is fully efficient (>99%) for real, high- 𝑝T jets used in most physics analysis. Its background rejection power is similarly high.

#### Applying Jet ID
There are several ways to apply jet ID. In our above exercises, we have run the cuts "on-the-fly" in our python FWLite macro (the first option here). Others are listed for your convenience.
The following examples use somewhat out of date numbers. See the above link to the JetID twiki for the current numbers.
To apply the cuts on pat::Jet (like in miniAOD) in python then you can do :

#### Apply jet ID to uncorrected jet
```
nhf = jet.neutralHadronEnergy() / uncorrJet.E()
nef = jet.neutralEmEnergy() / uncorrJet.E()
chf = jet.chargedHadronEnergy() / uncorrJet.E()
cef = jet.chargedEmEnergy() / uncorrJet.E()
nconstituents = jet.numberOfDaughters()
nch = jet.chargedMultiplicity()
goodJet = \
  nhf < 0.99 and \
  nef < 0.99 and \
  chf > 0.00 and \
  cef < 0.99 and \
  nconstituents > 1 and \
  nch > 0
```
To apply the cuts on pat::Jet (like in miniAOD) in C++ then you can do:
```
// Apply jet ID to uncorrected jet
double nhf = jet.neutralHadronEnergy() / uncorrJet.E();
double nef = jet.neutralEmEnergy() / uncorrJet.E();
double chf = jet.chargedHadronEnergy() / uncorrJet.E();
double cef = jet.chargedEmEnergy() / uncorrJet.E();
int nconstituents = jet.numberOfDaughters();
int nch = jet.chargedMultiplicity();
bool goodJet = 
  nhf < 0.99 &&
  nef < 0.99 &&
  chf > 0.00 &&
  cef < 0.99 &&
  nconstituents > 1 &&
  nch > 0;
```
To create selected jets in cmsRun:
```
from PhysicsTools.SelectorUtils.pfJetIDSelector_cfi import pfJetIDSelector
process.tightPatJetsPFlow = cms.EDFilter("PFJetIDSelectionFunctorFilter",
                                         filterParams = pfJetIDSelector.clone(quality=cms.string("TIGHT")),
                                         src = cms.InputTag("slimmedJets")
                                         )
```                                         
It is also possible to use the PFJetIDSelectionFunctor C++ selector (actually, either in C++ or python), but this was primarily developed in the days before PF when applying CaloJet ID was not possible very easily. Nevertheless, the functionality of more complicated selection still exists for PFJets, but is almost never used other than the few lines above. If you would still like to use that C++ class, it is documented as an example here.

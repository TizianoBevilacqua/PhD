# Some random info to keep in mind

## Setting up a CMSSW environment

Build CMSSW
```
export SCRAM_ARCH=slc7_amd64_gcc700
cmsrel CMSSW_10_6_18
cmsenv
git cms-init
```
To add packages to CMSSW:
```
git cms-addpkg [pkg name]
```
Useful packages are: `PhisicsTools`, `DataFormats`, `FWCore`.
To know which CMSSW releases are available:
``` 
scram list CMSSW
```
Proxy info:
```
voms-proxy-init --valid 192:00 --voms cms
voms-proxy-info -all | grep -Ei "role|subject"
```
To access and copy files with `root` or `xrdcp` one need to use the prefix:
```
root://cms-xrd-global.cern.ch/
```

## CMS filesystem 
* [DAS](https://cmsweb.cern.ch/das/), bookkeeping of files, it can be surfed through queries, in each field wildcards can be used before, after and in between.
```
dataset = /PrimaryDataset/ProcessingVersion/DataTier
```
examples of queries:
```
dataset release=CMSSW_10_6_14 dataset=/RelValZMM*/*CMSSW_10_6_14*/MINIAOD*
dataset file=/store/relval/CMSSW_10_6_14/RelValZMM_13/MINIAODSIM/106X_mc2017_realistic_v7-v1/10000/0EB976F4-F84B-814D-88DA-CB2C29A52D72.root
```
das can also be used from commandline:
```
dasgoclient --query="dataset=/DoubleMuon/Run2018A-12Nov2019_UL2018-v2/MINIAOD" --format=plain
```
* [CMS OMS](https://cmsoms.cern.ch/cms/index/index): website to  find informations on runs.
* [CMS McM](https://cms-pdmv.cern.ch/mcm/): website to find mc samples, with info also on the status of ongoing requests for new samples.
* [CMS GrASP](https://cms-pdmv.cern.ch/grasp): again another website for MC samples bookkeeping, it also has the option to create labels to group the relevant samples for one's analysis. To create labels a registration [here](https://cms-pdmv.cern.ch/mcm/users?page=0&shown=51) is needed, one can self-register by pressing the "add me" button in the bottom left corner. It takes a while to propagate the changes.
* [CDS](https://cds.cern.ch/): find CMS thesis and documents.
* [CADi](https://cms.cern.ch/iCMS/analysisadmin/cadilines?id=2293&ancode=HIG-19-016&tp=an&line=HIG-19-016): find AN and papers

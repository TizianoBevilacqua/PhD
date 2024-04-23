# HiggsDNA  
Higgs to diphoton nanoAOD framework  
* My fork: https://gitlab.cern.ch/tbevilac/higgs-dna-tiziano-bevilacqua/-/tree/master/
  
## Installation  
  
The installation procedure consists in the following steps:  
  
**1. Clone this repository**  
```  
git clone -b HpC_merge ssh://git@gitlab.cern.ch:7999/tbevilac/higgs-dna-tiziano-bevilacqua.git 
cd HiggsDNA  
```  
**2. Install dependencies**  
  
The necessary dependencies (listed in ```environment.yml```) can be installed manually, but the suggested way is to create a [conda environment](https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/mana  
ge-environments.html) by running:  
```  
conda env create -f environment.yml  
```  
Please note that the field ```python>=3.6``` will create an environment with the most recent stable version of Python. Change it to suite your needs (but still matching the requirement of Python>=3.6).  
  
**3. Install ```higgs_dna```**  
  
**Users** can install the package by simply running:  
```  
python setup.py install  
```  
(when a stable version will be available, it will be uploaded to the PyPI and it will be possible to install with just ```pip install higgs_dna``` without the need to clone the repository).  
  
  
For **developers**, the suggested way to install is:  
```  
python3 -m pip install -e .[dev]  
```  
this prevents the need to run the installation step every time a change is performed.

If you notice issues with the ```conda pack``` command for creating the tarball, try updating and cleaning your environment with (after running ```conda activate higgs-dna```):
```
conda env update --file environment.yml --prune
```

### Running HiggsDNA 

To run an analysis with coffea the main core of the work is done using an instance of the class `HggBaseProcessor`. This function (located at `higgs-dna/workflows/base.py`) contains the preselections on photons and diphoton candidate as were provided by the central release of HiggsDNA, further simple selections can be defined using the `process_extra` function and run on top of the diphoton preselection. An alternative approach that is more suitable if you have important modification to the wf, and that I've followed for the H+c analysis is to create another processor. I've created starting from the `HggBaseProcessor` a new one called `HplusCharmProcessor` that inherits from the `base` one but redefine also the `process` function. This can be found in `higgs-dna/workflows/hpc_processor.py` and has been implemented to select diphoton candidates, jets, svs, apply mva and such.

To run the analysis the standard approach is to use the `run_analysis.py` script.

An example command:

```
run_analysis.py --json-analysis runnerJSON.json --dump output_test
```

this is very basic and will use all the default options, which probably is not what you want. The option list and the default values are defined in the `higgs_dna/utils/runner_utils.py` script, one can see the option list using the `--help` option.

```
options:
  -h, --help            show this help message and exit
  --json-analysis JSON_ANALYSIS_FILE
                        JSON analysis file where workflow, taggers, metaconditions, samples and systematics are defined. It has to look like this: { "samplejson": "path to sample
                        JSON", "workflow": one of ['dystudies', 'tagandprobe', 'HHbbgg', 'particleLevel', 'top', 'zmmy', 'zmmyHist', 'zmmyZptHist', 'hpc'], "metaconditions": one
                        of ['Era2017_legacy_xgb_v1', 'Era2017_legacy_v1', 'Era2017_RR-31Mar2018_v1', 'Era2018_legacy_xgb_v1', 'Era2022_v1', 'Era2018_legacy_v1'], "taggers": list
                        from ['DummyTagger1', 'DummyTagger2', 'HHWWggTagger', 'yTagger', 'ptTagger', 'fiducialClassicalTagger', 'fiducialGeometricTagger'], "systematics": path to
                        systematics JSON or systematics in JSON style, "corrections": path to corrections JSON or corrections in JSON sytle }
  --no-trigger          Turn off trigger selection
  -d DUMP, --dump DUMP  Path to dump parquet outputs to (default: None)
  -o OUTPUT, --output OUTPUT
                        Output filename (default: output.coffea)
  --schema {nano,base}  input file format schema(default: nano)
  -f {root,parquet}, --format {root,parquet}
                        input file format (default: root)
  --save SAVE           If not None, save the coffea output, e.g., --save run_summary.coffea
  --executor {iterative,futures,parsl/slurm,parsl/condor,dask/condor,dask/slurm,dask/lpc,dask/lxplus,dask/casa,vanilla_lxplus}
                        The type of executor to use (default: futures). Other options can be implemented. For example see
                        https://parsl.readthedocs.io/en/stable/userguide/configuring.html- `parsl/slurm` - tested at DESY/Maxwell- `parsl/condor` - tested at DESY, RWTH-
                        `dask/slurm` - tested at DESY/Maxwell- `dask/condor` - tested at DESY, RWTH- `dask/lpc` - custom lpc/condor setup (due to write access restrictions)-
                        `dask/lxplus` - custom lxplus/condor setup (due to port restrictions)- `vanilla_lxplus` - custom plain lxplus submitter
  -j WORKERS, --workers WORKERS
                        Number of workers (cores/threads) to use for multi-worker executors (e.g. futures or condor) (default: 6)
  -m MEMORY, --memory MEMORY
                        Memory to use for each job in distributed executors (default: 10GB)
  --walltime WALLTIME   Walltime to use for each job in distributed executors (default: 01:00:00)
  --disk DISK           Disk space to use for each job in distributed executors (default: 20GB)
  -s SCALEOUT, --scaleout SCALEOUT
                        Number of nodes to scale out to if using slurm/condor. Total number of concurrent threads is ``workers x scaleout`` (default: 6)
  --max-scaleout MAX_SCALEOUT
                        The maximum number of nodes to adapt the cluster to. (default: 150)
  -q QUEUE, --queue QUEUE
                        Queue to submit jobs to if using slurm/condor (default: None)
  --voms VOMS           Path to voms proxy, accessible to worker nodes. Note that when this is specified the environment variable X509_CERT_DIR must be set to the certificates
                        directory location
  --validate            Do not process, just check all files are accessible
  --skipbadfiles        Skip bad files.
  --only ONLY           Only process specific dataset or file
  --limit N             Limit to the first N files of each dataset in sample JSON
  --chunk N             Number of events per process chunk
  --max N               Max number of chunks to run in total
  --skipCQR             Do not apply chained quantile regression (CQR) corrections
  --skipJetVetoMap      Do not apply jet vetomap selections
  --debug               Print debug information with a logger
  --fiducialCuts {classical,geometric,none}
                        Apply fiducial cuts at detector level according to standard CMS approach (classical with 1/3 and 1/4 thresholds for scaled pT of lead and sublead),
                        geometric cuts (proposed in 2106.08329), or none at all. Fiducial selection at particle level is handled with taggers.
  --doDeco              Perform the mass resolution decorrelation
  --Smear_sigma_m       Perform the mass resolution Smearing
  --doFlow_corrections  Perform the mvaID and energyErr corrections with normalizing flows
  --output_format {root,parquet}
                        Output format (default: parquet).
```

The important ones are:

* `-d DUMP, --dump DUMP  Path to dump parquet outputs to (default: None)`
* `--executor {iterative,futures,parsl/slurm,parsl/condor,dask/condor,dask/slurm,dask/lpc,dask/lxplus,dask/casa,vanilla_lxplus}` the one you need on the tier3 are `iterative` or `futures` to run locally or `dask/slurm` to submit to the `batch`.
* `-j WORKERS, --workers WORKERS - Number of workers (cores/threads) to use for multi-worker executors (e.g. futures or condor)` number of **LOCAL** workers allocated on each node, keeping it to 1 is good practice on t3.
* `-m MEMORY, --memory MEMORY - Memory to use for each job in distributed executors (default: 10GB)` be generous if you run on a big number of files.
* `-s SCALEOUT, --scaleout SCALEOUT` and `--max-scaleout MAX_SCALEOUT` regulate the minimum and maximum nodes that will be put up by dask
* `--limit N             Limit to the first N files of each dataset in sample JSON`
* `--chunk N             Number of events per process chunk`
* `--skipCQR             Do not apply chained quantile regression (CQR) corrections`
* `--skipJetVetoMap      Do not apply jet vetomap selections`

a full blown option command example to run on the cluster:

```
run_analysis.py --json-analysis runnerJSON.json --dump output_test --skipCQR --executor dask/slurm -m 22GB --chunk 100000 -j 1 --scaleout 2 --max-scaleout 80
```

### Postprocessing

After running HiggsDNA some postprocessing is helpful to manage the output and normalise it to `XSec x Acceptance`. This can be made wit a set of scripts than can be found in `scripts/postprocessing`.
Instructions on how to use them are in the [HiggsDNA guide](https://higgs-dna.readthedocs.io/en/latest/output_grooming.html), but there recently was an update that is not documented there yet.
The only difference is that now the category and systematic `json`s have to be fed to the script "externally".





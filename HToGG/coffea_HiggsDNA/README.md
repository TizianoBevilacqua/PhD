# HiggsDNA  
Higgs to diphoton nanoAOD framework  
* My fork: https://gitlab.cern.ch/tbevilac/higgs-dna-tiziano-bevilacqua/-/tree/master/
  
## Installation  
  
The installation procedure consists in the following steps:  
  
**1. Clone this repository**  
```  
git clone ssh://git@gitlab.cern.ch:7999/tbevilac/higgs-dna-tiziano-bevilacqua.git  
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

## Development Guidelines and Contribution
Here we summarize some general guidelines for developers and contributors.

### Printing Useful Analysis Info
We use the Python [logging facility](https://docs.python.org/3/library/logging.html) together with [rich](https://github.com/willmcgugan/rich) (for pretty printing) to provide useful analysis information. At the time of writing, two levels of information are supported: **INFO** and **DEBUG**.

All we have to do to print information from the code we are developing consists in:

- if not already present in the submodule, add the lines 
```
import logging
logger = logging.getLogger(__name__)
```
- type ```logger.info(message)``` or ```logger.debug(message)``` depending on which level we want our ```message``` to be displayed

Note: due to the way the logging package works, if the level is set to INFO only INFO messages are printed; if the level is set to DEBUG, both DEBUG and INFO messages are printed.

### Raising Detailed Exceptions

Raising detailed exceptions is important. Whenever it is possible, let's try to raise exception with detailed messages and possible solutions for the user to fix their code.

### Tests

A battery of tests based on [unittests](https://docs.python.org/3/library/unittest.html) is available. Before sending a PR, it is suggested to check that the new code didn't break anything by running:

```
python -m unittest -v
``` 

Please note that this is good practice even if CI is available. It is indeed a waste of time and resources to trigger a build if there is something clearly wrong that can be spotted by simply running the above mentioned command.

### Running HiggsDNA 

To run an analysis with coffea the main core of the work is done using an instance of the class `HggBaseProcessor`. This function (located at `higgs-dna/workflows/base.py`) contains the preselections on photons and diphoton candidate as were provided by the central release of HiggsDNA, further simple selections can be defined using the `process_extra` function and run on top of the diphoton preselection. To synch with the old version of the framework and further develop the H+c analysis I've created starting from the `HggBaseProcessor` a new processor called `HplusCharmProcessor` that inherits from the `base` one but redefine also the `process` function. This can be found in `higgs-dna/workflows/HplusCharm.py` and has been implemented to select diphoton candidates and jets.

To run the analysis an example workflow is available in the `Run_with_DaskSlurm` Jupiter notebook in the `notebooks` directory.

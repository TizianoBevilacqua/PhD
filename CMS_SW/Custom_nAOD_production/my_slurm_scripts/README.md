# Instructions to produce customised nAOD using v11

The procedure is rather simple, and it follows the instructions from the [nAOD guide](https://gitlab.cern.ch/cms-nanoAOD/nanoaod-doc/-/wikis/Releases/NanoAODv11), there is one main script `my_batch_sub_script.py` that takes care of everything.

It has different running option that are summarised inside the file itself:

* `--create`: create a task directory here and prepare the submission jobs according to what is set in the config file. It also asks if you want to directly submit all the jobs, only one test job or none.
* `--submit`: self explanatory.
* `--resubmit`: self explanatory.
* `--submit`: query to `squeue` to check the status of the jobs, Pendant (PD), Running (R) or Completed.
* `--missing`: looks for missing jobs.

there are some other additional options that can be used together with the oter to change some settings of the jobs:
* `--queue`: changes the job queue
* `--time`: changes the wall time, to be matched to the queue you intend to use, standar has a limit of 12 hours 12:00:00

The configuration files are stored in the `config` directory.
Some out-of-the-box working examples (I hope) are the 2017 QCD samples that can be found in `config/2017`.

To run the jobs you can directly do:
```
python3 my_batch_sub_script.py --input configs/2017/QCD_2017_v11.json --create
```

As it is now the `slurm_template.sh` file is the job that will be launched and will create a `CMSSW_12_6_0_patch1` environment, merge my private branch `TizianoBevilacqua:devel-nAOD-v11` to introduce the changes to calculate the HoE of the Photons correctly and then run the NANO step with v11.

The Jobs in this particular config file split the miniAOD samples in 5 files at a time, with running times of 6-12 hours.

# Random instructions:

## Parquet $\rightarrow$ RooWorkspace conversion:
To save the Diphoton collection to a `.parquet` file using HiggsDNA one has to specify the `output_location` variable of the processor pointing to the output directory, if you're using a Jupiter notebook this can be done directly in the processor definition (an example can be found [here]() at cell #6), if instead you're running the analysis with the [Run_HpC_analysis.py]() script this will automatically be done unless you use the `--out_dir` option to modify the path to the output directory or to avoid the dump.

Since there's an output file for each chunk of each sample the next step is to merge the `.parquet` files of each sample using the [merge_parquet.py]() script:
```
python merge_parquet.py --source [output_dir containing only .parquet files] --target [output_dir_merged/name of the file without extension]
```

Then the merged file must be converted to a root TTree using the [convert_parquet_to_root.py]() script, here one has to be careful to name the things correctly so that FinalFit finds everithing it needs:
```
python3 convert_parquet_to_root.py [path to the merged parquet produced in the previous step] [output_dir_root/name of the root file with the extension .root] [type of sample (data or mc)] --process [process (ggh,vbf...)]
```

Finally one has to create the RooWorkspace using the Tree2WS package inside flashggFinalFit. This step require a configuration file that specifies the variables to be added to the WS and other stuff, an example can be found [here]().
To run the step from the `flashggFinalFit/Tree2WS` directory:
```
python trees2ws.py --inputConfig config_higgsdna.py --inputTreeFile /work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/higgs-dna-tiziano-bevilacqua/scripts/output_dir_root/output_GluGluHToGG_M125_13TeV_amcatnloFXFX_pythia8_WStest.root --doNOTAG --productionMode ggh
```
the naming of the input file is important, basically the script should be fed something like `*pithia8_CATEGORYNAME.root`.

## Signal modelling
Also here a few steps have to be done. starting from the *fTest* in which the optimal numbers of gaussian to be used in the fit is decided. To run go to the `flashggFinalFit/Signal` directory and write a proper configuration file, examples can be found in the same directory.
Then:
```
python RunSignalScripts.py --inputConfig config_hdna_test_2017.py --mode fTest --modeOpts "--doPlots --skipWV"
```

The next step is to calculate the photon systematics. Up to now I've not done this one and used `--skipSystematics` in the `signalFit` step.

Then one can extract the $(\epsilon \cdot A)_{ij}$ using the NOTAG dataset:
```
python RunSignalScripts.py --inputConfig config_hdna_test_2017.py --mode getEffAcc --modeOpt "--skipCOWCorr --massPoints 125"
```

Finally one can perform the fit:
```
python RunSignalScripts.py --inputConfig config_hdna_test_2017.py --mode signalFit --modeOpt "--skipVertexScenarioSplit --skipSystematics --massPoints 125 --doPlots"
```

Package the different years and stuff:
```
python /work/bevila_t/HpC_Analysis/HiggsDNA/flasggFinalFit/CMSSW_10_2_13/src/flashggFinalFit/Signal/scripts/packageSignal.py --cat WStest --outputExt packaged --massPoints 125 --exts test_hdna --year 2017
```

and after removing the extra `2017` from the output file name of the previous step:
```
python RunPlotter.py --procs all --cats all --years 2017 --ext packaged
```

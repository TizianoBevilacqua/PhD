# text2ws

## 2POIs
```
text2workspace.py Datacard.txt -o Datacard_mu_2_ch_bh.root -m 125 higgsMassRange=122,128 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO "map=.*ggh_c.*:r_c[1,-10,10]" --PO "map=.*vbf_c.*:r_c[1,-10,10]" --PO "map=.*vh_c.*:r_c[1,-10,10]" --PO "map=.*tth_c.*:r_c[1,-10,10]" --PO "map=.*ch_c.*:r_c[1,-10,10]" --PO "map=.*bh_c.*:r_c[1,-10,10]" --PO "map=.*ggh_b.*:r_b[1,-10,10]" --PO "map=.*vbf_b.*:r_b[1,-10,10]" --PO "map=.*vh_b.*:r_b[1,-10,10]" --PO "map=.*tth_b.*:r_b[1,-10,10]" --PO "map=.*ch_b.*:r_b[1,-10,10]" --PO "map=.*bh_b.*:r_b[1,-10,10]"

text2workspace.py Datacard.txt -o Datacard_mu_2_ch_bh_add_SM_nature.root -m 125 higgsMassRange=122,128 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO "map=.*ggh_c.*:r_c[1,-15,15]" --PO "map=.*ch_c.*:r_c[1,-15,15]" --PO "map=.*bh_c.*:r_c[1,-15,15]" --PO "map=.*ggh_b.*:r_b[1,-15,15]" --PO "map=.*ch_b.*:r_b[1,-15,15]" --PO "map=.*bh_b.*:r_b[1,-15,15]"

text2workspace.py Datacard.txt -o Datacard_mu_3_ch_bh_SM.root -m 125 higgsMassRange=122,128 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO "map=.*ggh_c.*:r_c[1,-15,15]" --PO "map=.*ch_c.*:r_c[1,-15,15]" --PO "map=.*bh_c.*:r_c[1,-15,15]" --PO "map=.*ggh_b.*:r_b[1,-15,15]" --PO "map=.*ch_b.*:r_b[1,-15,15]" --PO "map=.*bh_b.*:r_b[1,-15,15]" --PO "map=.*tth_c.*:r_SM[1,-15,15]"  --PO "map=.*tth_b.*:r_SM[1,-15,15]" --PO "map=.*vbf_c.*:r_SM[1,-15,15]"  --PO "map=.*vbf_b.*:r_SM[1,-15,15]" --PO "map=.*vh_c.*:r_SM[1,-15,15]"  --PO "map=.*vh_b.*:r_SM[1,-15,15]"

text2workspace.py Datacard.txt -o Datacard_mu_5_ch_bh_SM.root -m 125 higgsMassRange=122,128 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO "map=.*ggh_c.*:r_c[1,-15,15]" --PO "map=.*ch_c.*:r_c[1,-15,15]" --PO "map=.*bh_c.*:r_c[1,-15,15]" --PO "map=.*ggh_b.*:r_b[1,-15,15]" --PO "map=.*ch_b.*:r_b[1,-15,15]" --PO "map=.*bh_b.*:r_b[1,-15,15]" --PO "map=.*tth_c.*:r_tth[1,-15,15]" --PO "map=.*tth_l.*:r_tth[1,-15,15]"  --PO "map=.*tth_b.*:r_tth[1,-15,15]" --PO "map=.*vbf_c.*:r_vbf[1,-15,15]"  --PO "map=.*vbf_b.*:r_vbf[1,-15,15]" --PO "map=.*vbf_l.*:r_vbf[1,-15,15]" --PO "map=.*vh_c.*:r_vh[1,-15,15]"  --PO "map=.*vh_b.*:r_vh[1,-15,15]" --PO "map=.*vh_l.*:r_vh[1,-15,15]"

text2workspace.py Datacard.txt -o Datacard_mu_6_ch_bh_SM.root -m 125 higgsMassRange=122,128 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO "map=.*ggh_c.*:r_c[1,-15,15]" --PO "map=.*ch_c.*:r_c[1,-15,15]" --PO "map=.*bh_c.*:r_c[1,-15,15]" --PO "map=.*ggh_b.*:r_b[1,-15,15]" --PO "map=.*ch_b.*:r_b[1,-15,15]" --PO "map=.*bh_b.*:r_b[1,-15,15]" --PO "map=.*tth_c.*:r_tth[1,-15,15]" --PO "map=.*tth_l.*:r_tth[1,-15,15]"  --PO "map=.*tth_b.*:r_tth[1,-15,15]" --PO "map=.*vbf_c.*:r_vbf[1,-15,15]"  --PO "map=.*vbf_b.*:r_vbf[1,-15,15]" --PO "map=.*vbf_l.*:r_vbf[1,-15,15]" --PO "map=.*vh_c.*:r_vh[1,-15,15]"  --PO "map=.*vh_b.*:r_vh[1,-15,15]" --PO "map=.*vh_l.*:r_vh[1,-15,15]" --PO "map=.*ggh_l.*:r_l[1,-15,15]" --PO "map=.*ch_l.*:r_l[1,-15,15]" --PO "map=.*bh_l.*:r_l[1,-15,15]"


```
# MultidimFit

## Comments on Asimov closure

To reach a complete closure of the Asimov fit one has to be sure that the pdfindex for each category is the same between the extraction of the asimov dataset and the actual fit.
To do so before running the multidim scan one has to perform a best_fit run specifying to combine to save the postfit values of the pdfindexes:
```
combine -M MultiDimFit Datacard_mu_2_ch_bh.root -m 125 -n .best_fit_cH_bH.  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH  -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --saveSpecifiedIndex pdfindex_bTag_2017_13TeV,pdfindex_cTag_2017_13TeV,pdfindex_lbTag_2017_13TeV,pdfindex_lcTag_2017_13TeV
```
### 2017
```
combine -M MultiDimFit ../../Datacard_mu_2_ch_bh_add_SM_nature.root -m 125 -n .best_fit_cH_float_bH  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --saveSpecifiedIndex pdfindex_bTag_low_2017_13TeV,pdfindex_bTag_high_2017_13TeV,pdfindex_cTag_high_2017_13TeV,pdfindex_cTag_low_2017_13TeV,pdfindex_lbTag_2017_13TeV,pdfindex_lcTag_high_2017_13TeV,pdfindex_lcTag_low_2017_13TeV,pdfindex_tthTag_2017_13TeV,pdfindex_vbfTag_2017_13TeV,pdfindex_vhTag_2017_13TeV
```

one then has to open the best_fit file and go through the very tedious step of extracting the final value of the indices from the post-fit workspace.
```
combine -M MultiDimFit ../../Datacard_mu_2_ch_bh_add_SM_nature.root -m 125 -n .scan.syst.cH_bH_float_add_SM_nature --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1,pdfindex_bTag_high_2017_13TeV=6,pdfindex_bTag_low_2017_13TeV=4,pdfindex_cTag_high_2017_13TeV=6,pdfindex_cTag_low_2017_13TeV=4,pdfindex_lbTag_2017_13TeV=3,pdfindex_lcTag_high_2017_13TeV=1,pdfindex_lcTag_low_2017_13TeV=3,pdfindex_tthTag_2017_13TeV=2,pdfindex_vbfTag_2017_13TeV=4,pdfindex_vhTag_2017_13TeV=2 -P r_c --floatOtherPOIs 1 --saveFitResult

combine  -M MultiDimFit higgsCombine.scan.syst.cH_bH_float.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_bH_float --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_c=1.,r_b=1,pdfindex_bTag_high_2017_13TeV=6,pdfindex_bTag_low_2017_13TeV=4,pdfindex_cTag_high_2017_13TeV=5,pdfindex_cTag_low_2017_13TeV=4,pdfindex_lbTag_high_2017_13TeV=4,pdfindex_lbTag_low_2017_13TeV=5,pdfindex_lcTag_high_2017_13TeV=2,pdfindex_lcTag_low_2017_13TeV=2 -P r_c --floatOtherPOIs 1 --saveFitResult --snapshotName MultiDimFit
```


pdfindex_bTag_high_2017_13TeV,pdfindex_bTag_low_2017_13TeV,pdfindex_cTag_high_2017_13TeV,pdfindex_cTag_low_2017_13TeV,pdfindex_lbTag_high_2017_13TeV,pdfindex_lbTag_low_2017_13TeV,pdfindex_lcTag_high_2017_13TeV,pdfindex_lcTag_low_2017_13TeV


#### PNet WPs



*2017*
```
combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .best_fit_cH_float_bH  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --saveSpecifiedIndex pdfindex_bTag_low_2017_13TeV,pdfindex_bTag_high_2017_13TeV,pdfindex_cTag_high_2017_13TeV,pdfindex_cTag_low_2017_13TeV,pdfindex_lTag_high_2017_13TeV,pdfindex_lTag_low_2017_13TeV,pdfindex_tthTag_2017_13TeV,pdfindex_vbfTag_2017_13TeV,pdfindex_vhTag_2017_13TeV


combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_float_bH_5POIs --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1,pdfindex_bTag_high_2017_13TeV=5,pdfindex_bTag_low_2017_13TeV=4,pdfindex_cTag_high_2017_13TeV=5,pdfindex_cTag_low_2017_13TeV=1,pdfindex_lTag_high_2017_13TeV=5,pdfindex_lTag_low_2017_13TeV=2,pdfindex_tthTag_2017_13TeV=2,pdfindex_vbfTag_2017_13TeV=3,pdfindex_vhTag_2017_13TeV=1 -P r_c --floatOtherPOIs 1 --saveFitResult

combine  -M MultiDimFit higgsCombine.scan.syst.cH_float_bH_5POIs.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_bH_float --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --snapshotName MultiDimFit
```

*2018*
```
combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .best_fit_cH_float_bH  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --saveSpecifiedIndex pdfindex_bTag_low_2018_13TeV,pdfindex_bTag_high_2018_13TeV,pdfindex_cTag_high_2018_13TeV,pdfindex_cTag_low_2018_13TeV,pdfindex_lTag_high_2018_13TeV,pdfindex_lTag_low_2018_13TeV,pdfindex_tthTag_2018_13TeV,pdfindex_vbfTag_2018_13TeV,pdfindex_vhTag_2018_13TeV

combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_float_bH_5POIs --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1,pdfindex_bTag_high_2018_13TeV=5,pdfindex_bTag_low_2018_13TeV=4,pdfindex_cTag_high_2018_13TeV=5,pdfindex_cTag_low_2018_13TeV=1,pdfindex_lTag_high_2018_13TeV=5,pdfindex_lTag_low_2018_13TeV=2,pdfindex_tthTag_2018_13TeV=2,pdfindex_vbfTag_2018_13TeV=3,pdfindex_vhTag_2018_13TeV=1 -P r_c --floatOtherPOIs 1 --saveFitResult

combine  -M MultiDimFit higgsCombine.scan.syst.cH_float_bH_5POIs.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_bH_float --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --snapshotName MultiDimFit
```

*2016*
```
combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .best_fit_cH_float_bH  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robuste 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --saveSpecifiedIndex pdfindex_bTag_low_2016_13TeV,pdfindex_bTag_high_2016_13TeV,pdfindex_cTag_high_2016_13TeV,pdfindex_cTag_low_2016_13TeV,pdfindex_lTag_high_2016_13TeV,pdfindex_lTag_low_2016_13TeV,pdfindex_tthTag_2016_13TeV,pdfindex_vbfTag_2016_13TeV,pdfindex_vhTag_2016_13TeV

combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_float_bH_5POIs --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1,pdfindex_bTag_high_2016_13TeV=2,pdfindex_bTag_low_2016_13TeV=2,pdfindex_cTag_high_2016_13TeV=4,pdfindex_cTag_low_2016_13TeV=3,pdfindex_lTag_high_2016_13TeV=2,pdfindex_lTag_low_2016_13TeV=2,pdfindex_tthTag_2016_13TeV=2,pdfindex_vbfTag_2016_13TeV=3,pdfindex_vhTag_2016_13TeV=2 -P r_c --floatOtherPOIs 1 --saveFitResult

combine  -M MultiDimFit higgsCombine.scan.syst.cH_float_bH_5POIs.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_bH_float --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --snapshotName MultiDimFit
```

*Combined*
```
combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .best_fit_cH_float_bH  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --saveSpecifiedIndex pdfindex_bTag_low_2017_13TeV,pdfindex_bTag_high_2017_13TeV,pdfindex_cTag_high_2017_13TeV,pdfindex_cTag_low_2017_13TeV,pdfindex_lTag_high_2017_13TeV,pdfindex_lTag_low_2017_13TeV,pdfindex_tthTag_2017_13TeV,pdfindex_vbfTag_2017_13TeV,pdfindex_vhTag_2017_13TeV,pdfindex_bTag_low_2018_13TeV,pdfindex_bTag_high_2018_13TeV,pdfindex_cTag_high_2018_13TeV,pdfindex_cTag_low_2018_13TeV,pdfindex_lTag_high_2018_13TeV,pdfindex_lTag_low_2018_13TeV,pdfindex_tthTag_2018_13TeV,pdfindex_vbfTag_2018_13TeV,pdfindex_vhTag_2018_13TeV,pdfindex_bTag_low_2016_13TeV,pdfindex_bTag_high_2016_13TeV,pdfindex_cTag_high_2016_13TeV,pdfindex_cTag_low_2016_13TeV,pdfindex_lTag_high_2016_13TeV,pdfindex_lTag_low_2016_13TeV,pdfindex_tthTag_2016_13TeV,pdfindex_vbfTag_2016_13TeV,pdfindex_vhTag_2016_13TeV

combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_float_bH_5POIs --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1,pdfindex_bTag_high_2017_13TeV=5,pdfindex_bTag_low_2017_13TeV=4,pdfindex_cTag_high_2017_13TeV=5,pdfindex_cTag_low_2017_13TeV=1,pdfindex_lTag_high_2017_13TeV=5,pdfindex_lTag_low_2017_13TeV=2,pdfindex_tthTag_2017_13TeV=2,pdfindex_vbfTag_2017_13TeV=3,pdfindex_vhTag_2017_13TeV=1,pdfindex_bTag_high_2018_13TeV_2,pdfindex_bTag_low_2018_13TeV=5,pdfindex_cTag_high_2018_13TeV=2,pdfindex_cTag_low_2018_13TeV=3,pdfindex_lTag_high_2018_13TeV=2,pdfindex_lTag_low_2018_13TeV=2,pdfindex_tthTag_2018_13TeV=4,pdfindex_vbfTag_2018_13TeV=3,pdfindex_bTag_high_2016_13TeV=2,pdfindex_bTag_low_2016_13TeV=2,pdfindex_cTag_high_2016_13TeV=4,pdfindex_cTag_low_2016_13TeV=3,pdfindex_lTag_high_2016_13TeV=2,pdfindex_lTag_low_2016_13TeV=2,pdfindex_tthTag_2016_13TeV=2,pdfindex_vbfTag_2016_13TeV=3,pdfindex_vhTag_2016_13TeV=2 -P r_c --floatOtherPOIs 1 --saveFitResult
```

#### 2D scan 

```
combine -M MultiDimFit ../Datacard_mu_2_ch_bh.root -m 125 -n .scan.syst.cH_bH --algo grid --points 120 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH  -t -1 --setParameters r_c=1.,r_b=1 -P r_c -P r_b --saveFitResult
```
Same but for **2018**
```
combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_bH --algo grid --points 720 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH  -t -1 --setParameters r_c=1.,r_b=1 -P r_c -P r_b --saveFitResult --floatOtherPOIs 1
```
Same but for **2016**
```
combine -M MultiDimFit ../Datacard_mu_5.root -m 125 -n .scan.syst.cH_bH --algo grid --points 720 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH  -t -1 --setParameters r_c=1.,r_b=1 -P r_c -P r_b --saveFitResult --floatOtherPOIs 1
```

### Combined commands for **full run2**

to combine the datacards:
```
combineCards.py Name1=Datacard_2016.txt Name2=Datacard_2017.txt Name3=Datacard_2018.txt > Datacard.txt
```
then text2workspace remains the same, and we do the **bestfit**
```
combine -M MultiDimFit ../Datacard_mu_2_ch.root -m 125 -n .best_fit_cH  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,r_SM  -t -1 --setParameters r_SM=1.,r_cH=1 -P r_cH --saveFitResult --saveSpecifiedIndex pdfindex_cHTag_0_2016_13TeV,pdfindex_cHTag_1_2016_13TeV,pdfindex_cHTag_2_2016_13TeV,pdfindex_cHTag_3_2016_13TeV,pdfindex_cHTag_4_2016_13TeV,pdfindex_cHTag_5_2016_13TeV,pdfindex_cHTag_6_2016_13TeV,pdfindex_cHTag_7_2016_13TeV,pdfindex_cHTag_8_2016_13TeV,pdfindex_cHTag_0_2017_13TeV,pdfindex_cHTag_1_2017_13TeV,pdfindex_cHTag_2_2017_13TeV,pdfindex_cHTag_3_2017_13TeV,pdfindex_cHTag_4_2017_13TeV,pdfindex_cHTag_5_2017_13TeV,pdfindex_cHTag_6_2017_13TeV,pdfindex_cHTag_7_2017_13TeV,pdfindex_cHTag_8_2017_13TeV,pdfindex_cHTag_0_2018_13TeV,pdfindex_cHTag_1_2018_13TeV,pdfindex_cHTag_2_2018_13TeV,pdfindex_cHTag_3_2018_13TeV,pdfindex_cHTag_4_2018_13TeV,pdfindex_cHTag_5_2018_13TeV,pdfindex_cHTag_6_2018_13TeV,pdfindex_cHTag_7_2018_13TeV,pdfindex_cHTag_8_2018_13TeV
```
we then set the indices and do the scan with systematics
```
combine -M MultiDimFit ../Datacard_mu_2_ch.root -m 125 -n .scan.syst.cH_SM_fixed  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,r_SM  -t -1 --setParameters r_SM=1.,r_cH=1,pdfindex_cHTag_0_2016_13TeV=2,pdfindex_cHTag_1_2016_13TeV=1,pdfindex_cHTag_2_2016_13TeV=6,pdfindex_cHTag_3_2016_13TeV=3,pdfindex_cHTag_4_2016_13TeV=5,pdfindex_cHTag_5_2016_13TeV=3,pdfindex_cHTag_6_2016_13TeV=4,pdfindex_cHTag_7_2016_13TeV=1,pdfindex_cHTag_8_2016_13TeV=2,pdfindex_cHTag_0_2017_13TeV=5,pdfindex_cHTag_1_2017_13TeV=1,pdfindex_cHTag_2_2017_13TeV=0,pdfindex_cHTag_3_2017_13TeV=5,pdfindex_cHTag_4_2017_13TeV=0,pdfindex_cHTag_5_2017_13TeV=2,pdfindex_cHTag_6_2017_13TeV=5,pdfindex_cHTag_7_2017_13TeV=3,pdfindex_cHTag_8_2017_13TeV=3,pdfindex_cHTag_0_2018_13TeV=5,pdfindex_cHTag_1_2018_13TeV=1,pdfindex_cHTag_2_2018_13TeV=2,pdfindex_cHTag_3_2018_13TeV=1,pdfindex_cHTag_4_2018_13TeV=1,pdfindex_cHTag_5_2018_13TeV=3,pdfindex_cHTag_6_2018_13TeV=4,pdfindex_cHTag_7_2018_13TeV=1,pdfindex_cHTag_8_2018_13TeV=4 -P r_cH --saveFitResult 
```
and repeat without
```
combine -M MultiDimFit higgsCombine.scan.syst.cH_SM_fixed.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_SM_fixed  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances,r_SM -t -1 --setParameters r_SM=1.,r_cH=1 -P r_cH --saveFitResult --snapshotName MultiDimFit
```
## 2POIs

### 1 POI FIXED 

r_SM only, r_cH fixed stat+theory uncertainties 
```
combine -M MultiDimFit Datacard_mu_2_ch.root -m 125 -n .scan.syst.SM_cH_fixed  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_SM=1.,r_cH=1 -P r_SM --saveFitResult 
```

r_SM only, r_cH fixed statistical uncertainties only
```
combine -M MultiDimFit higgsCombine.scan.syst.SM_cH_fixed.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.SM_cH_fixed  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_SM=1.,r_cH=1 -P r_SM --saveFitResult --snapshotName MultiDimFit
```

r_cH only, r_SM fixed stat+theory uncertainties
```
combine -M MultiDimFit Datacard_mu_2_ch.root -m 125 -n .scan.syst.cH_SM_fixed  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_SM=1.,r_cH=1 -P r_cH --saveFitResult
```

r_cH only, r_SM fixed statistical uncertainties only
```
combine -M MultiDimFit higgsCombine.scan.syst.cH_SM_fixed.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_SM_fixed  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_SM=1.,r_cH=1 -P r_cH --saveFitResult --snapshotName MultiDimFit
```

`--cminDefaultMinimizerTolerance 0.1` is not strictly necessary, as other flags that have a misterious meaning

#### Plots
```
plot1DScan.py higgsCombine.scan.syst.cH_float_bH_5POIs.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.cH_bH_float.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_cH_float_bH --POI r_c
plot1DScan.py higgsCombine.scan.syst.bH_float_cH_5POIs.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.bH_cH_float.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_cH_float_bH --POI r_b
plot1DScan.py higgsCombine.scan.syst.SM_cH_fixed.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.SM_cH_fixed.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_SM_fixed_cH --POI r_SM
```

```
python ../../../Plots/makeSplusBModelPlot.py --inputWSFile higgsCombine.scan.syst.cH_SM_fixed.MultiDimFit.mH125.root  --doZeroes --ext test  --cats all
```

### 1 POI FLOATING

r_SM only, r_cH fixed stat+theory uncertainties 
```
combine -M MultiDimFit Datacard_mu_2_ch.root -m 125 -n .scan.syst.SM_cH_float  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_SM=1.,r_cH=1 -P r_SM --saveFitResult --floatOtherPOIs
```

r_SM only, r_cH fixed statistical uncertainties only
```
combine -M MultiDimFit higgsCombine.scan.syst.SM_cH_float.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.SM_cH_float  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_SM=1.,r_cH=1 -P r_SM --saveFitResult --snapshotName MultiDimFit --floatOtherPOIs
```

r_cH only, r_SM fixed stat+theory uncertainties
```
combine -M MultiDimFit Datacard_mu_2_ch.root -m 125 -n .scan.syst.cH_SM_float  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_SM=1.,r_cH=1 -P r_cH --saveFitResult --floatOtherPOIs
```

r_cH only, r_SM fixed statistical uncertainties only
```
combine -M MultiDimFit higgsCombine.scan.syst.cH_SM_float.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_SM_float  --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --algo grid --points 30 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_SM=1.,r_cH=1 -P r_cH --saveFitResult --snapshotName MultiDimFit --floatOtherPOIs
```

varie ed eventuali
```
combine  -M MultiDimFit higgsCombine.scan.syst.cH_bH_float_SM_float.MultiDimFit.mH125.root -m 125 -n .scan.no_syst.cH_bH_float_SM_float --algo grid --points 30 --saveWorkspace --saveInactivePOI 1 --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH,allConstrainedNuisances -t -1 --setParameters r_c=1.,r_b=1 -P r_c --floatOtherPOIs 1 --saveFitResult --snapshotName MultiDimFit
```

#### Plots
```
plot1DScan.py higgsCombine.scan.syst.cH_SM_float.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.cH_SM_float.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_cH_float_SM --POI r_cH
plot1DScan.py higgsCombine.scan.syst.SM_cH_float.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.SM_cH_float.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_SM_float_cH --POI r_SM
```
#### 2D plots

```

```


# Asymptotic Limit

```
combine -M AsymptoticLimits ../Datacard_mu_2_ch.root --run blind --redefineSignalPOIs r_cH --setParameters r_cH=1.,r_SM=1.  --freezeParameters MH
combine -M AsymptoticLimits ../Datacard_mu_2_ch.root --run blind --redefineSignalPOIs r_cH --setParameters r_cH=1.,r_SM=1.  --freezeParameters MH,r_SM
combine -M AsymptoticLimits ../Datacard_mu_2_ch.root --run blind --redefineSignalPOIs r_cH,r_SM --setParameters r_cH=1.,r_SM=1.  --freezeParameters MH
```

# Impacts

## Floating r_SM
```
combineTool.py -M Impacts -d ../Datacard_mu_2_ch_bh.root -m 125 --doInitialFit --freezeParameters MH -n .impacts --setParameterRanges r_c=-10,10:r_b=-10,10 --robustFit 1 --redefineSignalPOIs r_c --setParameters r_c=1,r_b=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1
```
## fixed r_SM

```
combineTool.py -M Impacts -d ../Datacard_mu_2_ch.root -m 125 --doInitialFit --freezeParameters MH,r_SM -n .impacts --setParameterRanges r_cH=-1000,1000:r_SM=0,2 --robustFit 1 --redefineSignalPOIs r_cH --setParameters r_cH=1,r_SM=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1

combineTool.py -M Impacts -d ../Datacard_mu_2_ch.root -m 125 --doFits --freezeParameters MH,r_SM -n .impacts --setParameterRanges r_cH=-1000,1000:r_SM=0,2 --robustFit 1 --redefineSignalPOIs r_cH --setParameters r_cH=1,r_SM=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1

combineTool.py -M Impacts -d ../Datacard_mu_2_ch.root -m 125 --output impacts.json --freezeParameters MH,r_SM -n .impacts --setParameterRanges r_cH=-1000,1000:r_SM=0,2 --robustFit 1 --redefineSignalPOIs r_cH --setParameters r_cH=1,r_SM=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1

plotImpacts.py -i impacts.json -o impacts


```

### PNetWPs
```

combineTool.py -M Impacts -d ../Datacard_mu_5.root -m 125 --doInitialFit --freezeParameters MH -n .impacts --robustFit 1 --redefineSignalPOIs r_c --setParameters r_c=1,r_b=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1

combineTool.py -M Impacts -d ../Datacard_mu_5.root -m 125 --doFits --freezeParameters MH -n .impacts --robustFit 1 --redefineSignalPOIs r_c --setParameters r_c=1,r_b=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1 --parallel 6

combineTool.py -M Impacts -d ../Datacard_mu_5.root -m 125 --output impacts.json --freezeParameters MH -n .impacts --robustFit 1 --redefineSignalPOIs r_c --setParameters r_c=1,r_b=1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --X-rtd MINIMIZER_multiMin_maskChannels=2 --cminDefaultMinimizerStrategy=0 --robustHesse 1 -t -1

plotImpacts.py -i impacts.json -o impacts

```
## fitDiagnostics

```
combine -M FitDiagnostics ../../Datacard_mu_2_ch_bh_add_SM_nature.root -m 125 -n .best_fit_cH_float_bh_add_SM_nature --saveWorkspace --cminDefaultMinimizerTolerance 0.1 --cminApproxPreFitTolerance=10 --cminDefaultMinimizerStrategy=0 --robustHesse 1 --X-rtd MINIMIZER_freezeDisassociatedParams --X-rtd MINIMIZER_multiMin_hideConstants --X-rtd MINIMIZER_multiMin_maskConstraints --freezeParameters MH -t -1 --setParameters r_c=1.,r_b=1 --plots

```

## addLine to datacard

```
 python3 addLineToDatacard.py --inputDatacard Datacard.txt --systMap BDT_unc_sig:bdt_unc_sig:BDT_uncertainty_jsons/ggH_vs_RB_unc_2017_250219.json+BDT_unc_tth:bdt_unc_tth:BDT_uncertainty_jsons/ggH_vs_RB_unc_2017_250219.json+BDT_unc_vh:bdt_unc_vh:BDT_uncertainty_jsons/ggH_vs_RB_unc_2017_250219.json+BDT_unc_vbf:bdt_unc_vbf:BDT_uncertainty_jsons/ggH_vs_RB_unc_2017_250219.json+cH_FS_Unc:fs_unc:FS_uncertainty_jsons/HpCharm_FS_unc_per_category_2017.json+bH_FS_Unc:fs_unc:FS_uncertainty_jsons/HpBottom_FS_unc_per_category_2017.json
```
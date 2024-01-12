# text2ws

## 2POIs

```
text2workspace.py Datacard.txt -o Datacard_mu_2_ch.root -m 125 higgsMassRange=122,128 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO "map=.*ggH.*:r_SM[1,0,2]" --PO "map=.*qqH.*:r_SM[1,0,2]" --PO "map=.*vh.*:r_SM[1,0,2]" --PO "map=.*ttH.*:r_SM[1,0,2]" --PO "map=.*ch.*:r_cH[1,-500,500]" --PO "map=.*bh.*:r_SM[1,0,2]"
```

# MultidimFit

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
plot1DScan.py higgsCombine.scan.syst.cH_SM_fixed.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.cH_SM_fixed.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_cH_fixed_SM --POI r_cH
plot1DScan.py higgsCombine.scan.syst.SM_cH_fixed.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.SM_cH_fixed.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_SM_fixed_cH --POI r_SM
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

#### Plots
```
plot1DScan.py higgsCombine.scan.syst.cH_SM_float.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.cH_SM_float.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_cH_float_SM --POI r_cH
plot1DScan.py higgsCombine.scan.syst.SM_cH_float.MultiDimFit.mH125.root --main-label "With systematics" --main-color 1 --others higgsCombine.scan.no_syst.SM_cH_float.MultiDimFit.mH125.root:"Stat-only":2 -o part3_scan_SM_float_cH --POI r_SM
```

# Asymptotic Limit

```
combine -M AsymptoticLimits ../Datacard_mu_2_ch.root --run blind --redefineSignalPOIs r_cH --setParameters r_cH=1.,r_SM=1.  --freezeParameters MH
combine -M AsymptoticLimits ../Datacard_mu_2_ch.root --run blind --redefineSignalPOIs r_cH --setParameters r_cH=1.,r_SM=1.  --freezeParameters MH,r_SM
combine -M AsymptoticLimits ../Datacard_mu_2_ch.root --run blind --redefineSignalPOIs r_cH,r_SM --setParameters r_cH=1.,r_SM=1.  --freezeParameters MH
```


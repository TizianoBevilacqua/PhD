import awkward
import xgboost
import numpy as np
import json
import awkward as ak
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.metrics import roc_curve, auc, recall_score, precision_score, accuracy_score
# import packages for hyperparameters tuning
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
import scipy.stats as stats
import hist
from operator import itemgetter
import json

def get_importance(gbm, features):
    create_feature_map(features)
    importance = gbm.get_fscore(fmap='xgb.fmap')
    importance = sorted(importance.items(), key=itemgetter(1), reverse=True)
    return importance

def create_feature_map(features):
    outfile = open('xgb.fmap', 'w')
    for i, feat in enumerate(features):
        outfile.write('{0}\t{1}\tq\n'.format(i, feat))
    outfile.close()

def objective(space):
        clf = xgboost.XGBClassifier(
                n_estimators = space['n_estimators'], 
                max_depth = int(space['max_depth']), 
                gamma = space['gamma'],
                reg_alpha = space['reg_alpha'],
                reg_lambda = space['reg_lambda'],
                min_child_weight = int(space['min_child_weight']),
                subsample = space['subsample']
        )
    
        evaluation = [
                (X_train, y_train),
                (X_test, y_test)
        ]
    
        clf.fit(
                X_train,
                y_train,
                eval_set = evaluation,
                eval_metric = "auc",
                early_stopping_rounds = 10,
                verbose=True
        )

        pred = clf.predict(evaluation[1][0])
        accuracy = accuracy_score(evaluation[1][1], pred>0.5)
        print ("SCORE:", accuracy)
        return {'loss': -accuracy, 'status': STATUS_OK }

proc_dict = {
    "ggh_M125_2017": {
        # "file": "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master/SYST/higgs-dna-tiziano-bevilacqua/output/output_test_dlenSig/merged/ggh_M125_2017/NOTAG_merged.parquet",
        "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/output_signal_2017_newBDT/merged_NOTAG/ggh_M125_2017/NOTAG_merged.parquet",
        "type": "background",
        "label": 0.,
        "proc_id": 1,
    },
    "tth_M125_2017": {
        # "file": "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master/SYST/higgs-dna-tiziano-bevilacqua/output/output_test_dlenSig/merged/tth_M125_2017/NOTAG_merged.parquet",
        "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/output_signal_2017_newBDT/merged_NOTAG/tth_M125_2017/NOTAG_merged.parquet",
        "type": "background",
        "label": 0.,
        "proc_id": 2,
    },
    "vbf_M125_2017": {
        # "file": "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master/SYST/higgs-dna-tiziano-bevilacqua/output/output_test_dlenSig/merged/vbf_M125_2017/NOTAG_merged.parquet",
        "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/output_signal_2017_newBDT/merged_NOTAG/vbf_M125_2017/NOTAG_merged.parquet",
        "type": "background",
        "label": 0.,
        "proc_id": 3,
    },
    "vh_M125_2017": {
        # "file": "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master/SYST/higgs-dna-tiziano-bevilacqua/output/output_test_dlenSig/merged/vh_M125_2017/NOTAG_merged.parquet",
        "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/output_signal_2017_newBDT/merged_NOTAG/vh_M125_2017/NOTAG_merged.parquet",
        "type": "background",
        "label": 0.,
        "proc_id": 4,
    },
    "cH_4FS_FXFX_M125_2017": {
        # "file": "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master/SYST/higgs-dna-tiziano-bevilacqua/output/output_test_dlenSig/merged/cH_4FS_FXFX_M125_2017/NOTAG_merged.parquet",
        "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/output_signal_2017_newBDT/merged_NOTAG/cH_4FS_FXFX_M125_2017/NOTAG_merged.parquet",
        "type": "signal",
        "label": 1.,
        "proc_id": 5,
    },
    # "bH_5FS_FXFX_M125_2017": {
    #     "file": "/work/bevila_t/HpC_Analysis/cHvsggH_BDT_training/inputs/merged/bH_5FS_FXFX_M125_2017/nominal/NOTAG_merged.parquet",
    #     "type": "background",
    #     "label": 0.,
    #     "proc_id": 6,
    # }
}

# Open files load data and normalize
with open(
        "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/dev-master2/higgs-dna-tiziano-bevilacqua/higgs_dna/metaconditions/cross_sections.json", "r"
    ) as pf:
        XSs = json.load(pf)

sig_events = []
bkg_events = []
data_events = []

e = ak.from_parquet("/work/bevila_t/HpC_Analysis/cHvsggH_BDT_training/inputs/merged/cH_4FS_FXFX_M125_2017/nominal/NOTAG_merged.parquet")
columns = [f for f in e.fields]
               
for i, dataset in enumerate(proc_dict):
    if "Data" not in dataset:
        norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"]["2017"] * 1000
        print(f"{dataset}: xsec = {XSs[dataset]['xs']}, bf = {XSs[dataset]['bf']}, lumi = {XSs['lumi']['2017']}, norm = {norm}")
    else:
        print(f"{dataset}")
    if proc_dict[dataset]["type"] == "signal":
        norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"]["2017"] * 1000
        proc_dict[dataset]["norm"] = norm
        if len(sig_events) == 0:
            sig_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
            sig_events["weight"] = sig_events["weight"] * norm
            sig_events["proc_id"] = ak.ones_like(sig_events["weight"]) * proc_dict[dataset]["proc_id"]
        else:
            tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
            tmp_["weight"] = tmp_["weight"] * norm
            tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_dict[dataset]["proc_id"]
            sig_events = ak.concatenate([sig_events, tmp_])
        print(f'|----> sum normalised weights: {ak.sum(sig_events[sig_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
        print(f'|----> number of events: {len(sig_events[sig_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
    
    elif proc_dict[dataset]["type"] == "background":
        norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"]["2017"] * 1000
        proc_dict[dataset]["norm"] = norm
        if len(bkg_events) == 0:
            bkg_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
            bkg_events["weight"] = bkg_events["weight"] * norm
            bkg_events["proc_id"] = ak.ones_like(bkg_events["weight"]) * proc_dict[dataset]["proc_id"]
        else:
            tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
            tmp_["weight"] = tmp_["weight"] * norm
            #tmp_["weight"] = tmp_["weight"] * norm * 1.42
            tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_dict[dataset]["proc_id"]
            bkg_events = ak.concatenate([bkg_events, tmp_])
        print(f'|----> sum normalised weights: {ak.sum(bkg_events[bkg_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
        print(f'|----> number of events: {len(bkg_events[bkg_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
        
    elif proc_dict[dataset]["type"] == "data":
        if len(data_events) == 0:
            data_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
            data_events["proc_id"] = ak.ones_like(data_events["weight"]) * proc_dict[dataset]["proc_id"]
        else:
            tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
            tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_dict[dataset]["proc_id"]
            data_events = ak.concatenate([data_events, tmp_])

sig_events["label"] = ak.ones_like(sig_events["weight"])
bkg_events["label"] = ak.zeros_like(bkg_events["weight"])

# calculate some additional variables for the training
MC_events = ak.concatenate([sig_events, bkg_events[bkg_events.proc_id > -80]])

MC_events["dEta_ljh"] = abs(MC_events.eta - MC_events.first_jet_eta)
MC_events["dEta_sljh"] = abs(MC_events.eta - MC_events.second_jet_eta)
MC_events["dR_ljlp"] = np.sqrt((MC_events.LeadPhoton_eta - MC_events.first_jet_eta)**2 + (MC_events.DeltaPhi_gamma1_cjet)**2)
MC_events["dR_ljslp"] = np.sqrt((MC_events.SubleadPhoton_eta - MC_events.first_jet_eta)**2 + (MC_events.DeltaPhi_gamma2_cjet)**2)

MC_events["lj_ptoM"] = abs(MC_events.first_jet_pt/MC_events.first_jet_mass)
MC_events["slj_ptoM"] = abs(MC_events.second_jet_pt/MC_events.second_jet_mass)

MC_events["first_SV_ptoM"] = MC_events.first_sv_pt/MC_events.first_sv_mass
MC_events["second_SV_ptoM"] = MC_events.second_sv_pt/MC_events.second_sv_mass

MC_events["first_SV_ptoH_pt"] = MC_events.first_sv_pt/MC_events.pt
MC_events["Sv_J_MoM"] = abs(MC_events.first_sv_mass/MC_events.first_jet_mass)

# fix missing variables and division by zero
MC_events["Sv_J_MoM"] = awkward.where(
        MC_events["Sv_J_MoM"] > 50000,
        ak.ones_like(MC_events.Sv_J_MoM) * 50000,
        MC_events["Sv_J_MoM"]
)
MC_events["lj_ptoM"] = awkward.where(
        MC_events["lj_ptoM"] > 50000,
        ak.ones_like(MC_events.lj_ptoM) * 50000,
        MC_events["lj_ptoM"]
)
MC_events["slj_ptoM"] = awkward.where(
        MC_events["slj_ptoM"] > 50000,
        ak.ones_like(MC_events.slj_ptoM) * 50000,
        MC_events["slj_ptoM"]
)
MC_events["first_SV_ptoM"] = awkward.where(
        MC_events["first_sv_pt"] == 0,
        ak.zeros_like(MC_events.slj_ptoM),
        MC_events["first_SV_ptoM"]
)
MC_events["first_sv_mass"] = awkward.where(
        MC_events["first_sv_mass"] < -10,
        ak.ones_like(MC_events.slj_ptoM) * -1.,
        MC_events["first_sv_mass"]
)
MC_events["first_jet_n_sv"] = awkward.where(
        MC_events["first_jet_n_sv"] < -10,
        ak.ones_like(MC_events.first_jet_n_sv) * -1.,
        MC_events["first_jet_n_sv"]
)
MC_events["first_SV_ptoH_pt"] = awkward.where(
        MC_events["first_SV_ptoH_pt"] > 50000,
        ak.ones_like(MC_events.slj_ptoM) * 50000,
        MC_events["first_SV_ptoH_pt"]
)
MC_events["second_SV_ptoM"] = awkward.where(
        MC_events["second_SV_ptoM"] > 50000,
        ak.ones_like(MC_events.slj_ptoM) * 50000,
        MC_events["second_SV_ptoM"]
)

# print number of events per sample
print("")
print("-"*100)
for proc in range(-4, 6):
    print(f"proc: {proc}, n ev: {len(MC_events[MC_events.proc_id == proc])}, sum weights: {ak.sum(MC_events.weight[MC_events.proc_id == proc])}")

# load config
config="/work/bevila_t/HpC_Analysis/cHvsggH_BDT_training/inputs/cH_vs_ggH_bdt_config.json"

with open(config, "r") as f_in:
    bdt_config = json.load(f_in)

feature_labels = bdt_config["features"]

# create input matrix, here we also normalise for  the max of the distribution
features = ak.Array([])

print("")
print("-"*100)
print("create input matrix, here we also normalise for  the max of the distribution")
for feature in feature_labels:
    _max =  max(MC_events[feature])
    print(f"adding feature {feature} to events_in array")
    if len(features):
        features = ak.concatenate([features, ak.singletons(MC_events[feature]/_max)], axis=1)
    else:
        features = ak.singletons(MC_events[feature]/_max)

target = ak.Array([])
for process in proc_dict:
    if process in ["tth_M125_2017", "vbf_M125_2017", "vh_M125_2017", "ggh_M125_2017"]: 
        continue
    else:
        test = MC_events.proc_id == 5
    print(f"adding labels for process {process} to target array")
    lab = ak.where(
            test,
            ak.singletons(ak.ones_like(MC_events.pt)),
            ak.singletons(ak.zeros_like(MC_events.pt))
        )
    if len(target):   
        target = ak.concatenate([target, lab], axis=1)
    else:
        target = lab

print("Processes marked as 'Signal' or 'Background' will be used to train the DNN as signal and background, respectively.")

#print("Out of %d total events, found %d signal and %d background events." % (len(features), len(features[target[:,1]==1]), len(features[target[:,0]==1])))


# Add test/train/val split

X_train, X_test, y_train, y_test = train_test_split(features.to_numpy(), target.to_numpy(), test_size=0.33)
print(X_train.shape, X_test.shape, y_train.shape, y_test.shape)

del features, target


# Create the XGBoost model object
xgb_model = xgboost.XGBClassifier(**bdt_config["mva"]["param"])

evaluation = [
        (X_train, y_train),
        (X_test, y_test)
]

print("starting prefit")

xgb_model.fit(
        X_train,
        y_train,
        eval_set = evaluation,
        early_stopping_rounds = 10,
        verbose = True
)


# Define the hyperparameter distributions
space = {
    'max_depth': hp.quniform("max_depth", 3, 8, 1),
    'gamma': hp.quniform ('gamma', 3, 9, 1),
    'reg_alpha' : hp.uniform('reg_alpha', 0, 1),
    'reg_lambda' : hp.uniform('reg_lambda', 0, 1),
    'alpha' : hp.uniform('alpha', 0, 0.5),
    'lambda' : hp.uniform('lambda', 0.5, 1),
    'min_child_weight' : hp.quniform('min_child_weight', 3, 10, 1),
    'subsample' : hp.uniform('subsample', 0, 0.7),
    'seed': 0,
    'n_estimators': 180
}

trials = Trials()

best_hyperparams = fmin(
        fn = objective,
        space = space,
        algo = tpe.suggest,
        max_evals = 100,
        trials = trials
)

print("")
print("The best hyperparameters are : ","\n")
print(best_hyperparams)


# File path to save the JSON file
file_path = "/work/bevila_t/HpC_Analysis/cHvsggH_BDT_training/best_hyperparams.json"

# Write the dictionary to a JSON file
with open(file_path, "w") as json_file:
    json.dump(best_hyperparams, json_file)

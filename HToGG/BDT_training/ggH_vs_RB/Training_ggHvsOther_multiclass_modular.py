#!/usr/bin/env python
# coding: utf-8

import awkward
import xgboost as xgboost
import numpy as np
import os
import json
import awkward as ak
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import roc_curve, auc,recall_score,precision_score
from optparse import OptionParser
from plot_utils import plot_variable_comparison, plot_ROC, plot_ROC_multiclass, plot_confusion_matrix
import correctionlib
import correctionlib.schemav2 as cs

import hist
import mplhep as hep
from cycler import cycler
hep.style.use("CMS")

import uproot

from operator import itemgetter

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

def evaluate_wp(year, nth_jet_pn_b_plus_c, nth_jet_pn_b_vs_c):
    # ParticleNetAK4 -- exclusive b- and c-tagging categories
    # 5x: b-tagged; 4x: c-tagged; 0: light
    _wp_54 = ak.ones_like(nth_jet_pn_b_plus_c) * 54
    _wp_53 = ak.ones_like(nth_jet_pn_b_plus_c) * 53
    _wp_52 = ak.ones_like(nth_jet_pn_b_plus_c) * 52
    _wp_51 = ak.ones_like(nth_jet_pn_b_plus_c) * 51
    _wp_50 = ak.ones_like(nth_jet_pn_b_plus_c) * 50

    _wp_44 = ak.ones_like(nth_jet_pn_b_plus_c) * 44
    _wp_43 = ak.ones_like(nth_jet_pn_b_plus_c) * 43
    _wp_42 = ak.ones_like(nth_jet_pn_b_plus_c) * 42
    _wp_41 = ak.ones_like(nth_jet_pn_b_plus_c) * 41
    _wp_40 = ak.ones_like(nth_jet_pn_b_plus_c) * 40

    _wp_0 = ak.zeros_like(nth_jet_pn_b_plus_c)
    wp = ak.zeros_like(nth_jet_pn_b_plus_c)

    if year in ("2017", "2018", "combined"):
        # b WPs
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (nth_jet_pn_b_vs_c > 0.99),
            _wp_54,
            wp
        )
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (0.96 < nth_jet_pn_b_vs_c) & (nth_jet_pn_b_vs_c <= 0.99),
            _wp_53,
            wp
        )
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (0.88 < nth_jet_pn_b_vs_c) & (nth_jet_pn_b_vs_c <= 0.96),
            _wp_52,
            wp
        )
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (0.70 < nth_jet_pn_b_vs_c) & (nth_jet_pn_b_vs_c <= 0.88),
            _wp_51,
            wp
        )
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (0.40 < nth_jet_pn_b_vs_c) & (nth_jet_pn_b_vs_c <= 0.70),
            _wp_50,
            wp
        )

        # c WPs
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (nth_jet_pn_b_vs_c <= 0.05),
            _wp_44,
            wp
        )
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (0.05 < nth_jet_pn_b_vs_c) & (nth_jet_pn_b_vs_c <= 0.15),
            _wp_43,
            wp
        )
        wp = ak.where(
            (nth_jet_pn_b_plus_c > 0.5) & (0.15 < nth_jet_pn_b_vs_c) & (nth_jet_pn_b_vs_c <= 0.40),
            _wp_42,
            wp
        )
        wp = ak.where(
            (0.2 < nth_jet_pn_b_plus_c) & (nth_jet_pn_b_vs_c <= 0.5),
            _wp_41,
            wp
        )
        wp = ak.where(
            (0.1 < nth_jet_pn_b_plus_c) & (nth_jet_pn_b_vs_c <= 0.2),
            _wp_40,
            wp
        )

        # light wp
        wp = ak.where(
            (nth_jet_pn_b_plus_c <= 0.1),
            _wp_0,
            wp
        )
    return wp

def define_process_dict(input_dir, processes, years):
    proc_dict = {}
    for i, sample in enumerate(processes):
        for year in years:
            print(f"processing {sample} for {year}")
            sample = f"{sample}_{year}"
            proc_dict[sample] = {}
            # define the file path
            if str(year) in ["combined", "2017", "2018"]:
                merged = "merged"
            else:
                merged = ""
            if os.path.exists(f"{input_dir}/{merged}/{sample}/NOTAG_merged.parquet"):
                print('loading file from:', f"{input_dir}/{merged}/")
                proc_dict[sample]["file"] = f"{input_dir}/{merged}/{sample}/NOTAG_merged.parquet"
            elif os.path.exists(f"{input_dir}/{merged}/{sample}/nominal/NOTAG_merged.parquet"):
                print(f'loading file from: {input_dir}/{merged}/ "nominal"')
                proc_dict[sample]["file"] = f"{input_dir}/{merged}/{sample}/nominal/NOTAG_merged.parquet"
            else:
                print(f"File not found for {sample} in {input_dir}/{merged}/{sample}/")
                input_dir_tmp = "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2017/HpC_signal_gen_pt10_eta2p5_simple_JEC_classical_phoID_JetVeto_250408/"
                sample_tmp = sample.replace("2018", "2017")
                proc_dict[sample]["file"] = f"{input_dir_tmp}/{merged}/{sample_tmp}/NOTAG_merged.parquet"
            # assigne the label
            if sample.lower().split("_")[0] in ["ggh", "ch", "bh"]:
                proc_dict[sample]["type"] = "signal"
                proc_dict[sample]["label"] = 1.0
            else:    
                proc_dict[sample]["type"] = "background"
                proc_dict[sample]["label"] = 0.0 
            # assign the proc_id
            proc_dict[sample]["proc_id"] = i
    return proc_dict

usage = "Usage: python %prog %args"
parser = OptionParser(usage=usage)
parser.add_option("--year", dest="year", type="string", default="2017", help="year to analyse")
parser.add_option("--skip_save", dest="SAVE", action="store_false", default=True, help="save the weight set")
parser.add_option('--multiclass',  action="store_true", default=False, help='train multiclass model')
parser.add_option("--load", dest="LOAD", action="store_true", default=False, help="load the weight set instead of training a new one")
parser.add_option("--xgb_model_dir", dest="xgb_model_dir", type="string", default="/work/bevila_t/HpC_Analysis/ggHvOthers_BDT_training/XGBoost_models", help="where to load the weight set from")
parser.add_option("--wgt_name", dest="wgt_model", type="string", default="", help="Path to pre-trained model, name of the weight to load (without the .xgb extensionand the even/odd suffix)")
parser.add_option("--transform", dest="TRANSFORM", action="store_true", default=False, help="transform the input features in the [-1, 1] range")
parser.add_option("--full", dest="full", action="store_true", default=False, help="use only ggh as signal")
parser.add_option("--no_plots", dest="PLOTS", action="store_false", default=True, help="don't save plots")
parser.add_option("--config", dest="config", type="string", default="inputs/ggH_vs_other_bdt_config_2p0.json", help="don't save plots")
parser.add_option('--skip_concatenation', action="store_true", help='load a pre-processed file set')
(opt, args) = parser.parse_args()

# configs
year = opt.year

processes = [
    "ggh_M125",
    "tth_M125",
    "vbf_M125",
    "vh_M125",
    #"THQ_HToGG",
    #"THW_HToGG",
    "cH_4FS_FXFX_M125",
    "bH_5FS_FXFX_M125"
]

from datetime import date
# Get the current date
current_date = date.today()
# Format the date
formatted_date = current_date.strftime("%y%m%d")

if year == "2017":
    #input_dir = "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2017/HpC_signal_gen_pt10_eta2p5_simple_JEC_classical_phoID_JetVeto_250408/"
    input_dir = "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2017/HpC_NewBDT_250525/"
    proc_dict = define_process_dict(input_dir, processes, ["2017"])
elif year == "2018":
    input_dir = "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2018/higgs_dna_HpC_HpC_signal_samples_2018_250424/"
    proc_dict = define_process_dict(input_dir, processes, ["2018"])
elif year == "2016":
    #input_dir = "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2016/higgs_dna_HpC_signal_samples_2016_tot/"
    input_dir = "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/sensitivity_studies/2016/fit_newBDT_250505"
    proc_dict = define_process_dict(input_dir, processes, ["2016"])
elif year == "combined":
    # Combine all dictionaries
    years = ["2017", "2018"]
    input_dirs = [
        #"/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2017/HpC_signal_gen_pt10_eta2p5_simple_JEC_classical_phoID_JetVeto_250408/",
        "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2017/HpC_NewBDT_250525/",
        "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/ggHvsRB_training_2018/higgs_dna_HpC_HpC_signal_samples_2018_250424/"
    ]
    for i, year in enumerate(years):
        name = f"proc_dict_{year}"
        value = define_process_dict(input_dirs[i], processes, [year])
        globals()[name] = value
    proc_dict = {**proc_dict_2017, **proc_dict_2018}

if os.path.exists(f"plots/{formatted_date}"):
    f"today's plot directory already exists, saving plots to plots/{formatted_date}"
else:
    os.makedirs(f"plots/{formatted_date}")
    print(f"created plot directory at: plots/{formatted_date}")

if os.path.exists(f"nTuples"):
    f"nTuples directory already exists, saving and loading from nTuples"
else:
    os.makedirs(f"nTuples")
    print(f"created nTuples directory at: nTuples")

if not opt.skip_concatenation:
    e = ak.from_parquet(proc_dict[[*proc_dict][0]]["file"])

    print()
    print("available fields in the parquet file:")
    for f in e.fields:
        print(f"    * {f}")

    # concatenate the MC and Data events (separately) and add normalisation
    with open(
            "inputs/cross_sections.json", "r"
        ) as pf:
            XSs = json.load(pf)

    sig_events = []
    bkg_events = []
    data_events = []

    columns = [
            "CMS_hgg_mass",
            "pt",
            "eta",
            "PV_score",
            "LeadPhoton_pt_mgg",
            "SubleadPhoton_pt_mgg",
            "LeadPhoton_eta",
            "SubleadPhoton_eta",
            "Diphoton_cos_dPhi",
            "n_jets",
            "n_b_jets_medium",
            "n_b_jets_loose",
            "first_jet_pt",
            "first_jet_phi",
            "first_jet_mass",
            "first_jet_eta",
            "first_jet_hFlav",
            "first_jet_particleNetAK4_CvsL",
            "first_jet_particleNetAK4_CvsB",
            "first_jet_jet_pn_b_plus_c",
            "first_jet_jet_pn_b_vs_c",
            "second_jet_pt",
            "second_jet_phi",
            "second_jet_mass",
            "second_jet_eta",
            "second_jet_hFlav",
            "second_jet_pt",
            "second_jet_particleNetAK4_CvsL",
            "second_jet_particleNetAK4_CvsB",
            "second_jet_jet_pn_b_plus_c",
            "second_jet_jet_pn_b_vs_c",
            "first_pt_jet_pt",
            "first_pt_jet_phi",
            "first_pt_jet_mass",
            "first_pt_jet_eta",
            "first_pt_jet_hFlav",
            "second_pt_jet_pt",
            "second_pt_jet_phi",
            "second_pt_jet_mass",
            "second_pt_jet_eta",
            "second_pt_jet_hFlav",
            "second_pt_jet_pt",
            "second_pt_jet_mass",
            "second_pt_jet_eta",
            "third_jet_pt",
            "third_jet_eta",
            "third_jet_phi",
            "third_jet_mass",
            "third_jet_hFlav",
            "third_jet_jet_pn_b_plus_c",
            "third_jet_jet_pn_b_vs_c",
            "dijet_pt",
            "dijet_eta",
            "dijet_phi",
            "dijet_mass",
            "first_muon_pt",
            "first_muon_eta",
            "first_muon_phi",
            "first_muon_charge",
            "first_electron_pt",
            "first_electron_eta",
            "first_electron_phi",
            "first_electron_charge",
            "DeltaPhi_gamma1_cjet",
            "DeltaPhi_gamma2_cjet",
            "MET_pt",
            "MET_sumEt",
            "MET_phi",
            "MET_significance",
            "nMuon",
            "nTau",
            "nElectron",
            "sigmaMrv",
            # "sigmaMwv",
            "event",
            "weight"
        ]

    # columns = [f for f in e.fields]
    print()
    print("-"*80)
    print("Loading events from parquet files")
    print()            
    for i, dataset in enumerate(proc_dict):
        if "Data" not in dataset:
            norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"][f"{year}"] * 1000
            print(f"{dataset}: xsec = {XSs[dataset]['xs']}, bf = {XSs[dataset]['bf']}, lumi = {XSs['lumi'][f'{year}']}, norm = {norm}")
        else:
            print(f"{dataset}")
        if proc_dict[dataset]["type"] == "signal":
            norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"][f"{year}"] * 1000
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
            print(f'    |----> sum normalised weights: {ak.sum(sig_events[sig_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
            print(f'    |----> number of events: {len(sig_events[sig_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
    
        elif proc_dict[dataset]["type"] == "background":
            norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"][f"{year}"] * 1000
            proc_dict[dataset]["norm"] = norm
            if ("th" in dataset.lower()):
                proc_id = proc_dict[f"tth_M125_{year}"]["proc_id"]
            else:
                proc_id = proc_dict[dataset]["proc_id"]
            if len(bkg_events) == 0:
                bkg_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                bkg_events["weight"] = bkg_events["weight"] * norm
                bkg_events["proc_id"] = ak.ones_like(bkg_events["weight"]) * proc_id
            else:
                tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                tmp_["weight"] = tmp_["weight"] * norm
                tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_id
                bkg_events = ak.concatenate([bkg_events, tmp_])
            print(f'    |----> sum normalised weights: {ak.sum(bkg_events[bkg_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
            print(f'    |----> number of events: {len(bkg_events[bkg_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
        
        elif proc_dict[dataset]["type"] == "data":
            if len(data_events) == 0:
                data_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                data_events["proc_id"] = ak.ones_like(data_events["weight"]) * proc_dict[dataset]["proc_id"]
            else:
                tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_dict[dataset]["proc_id"]
                data_events = ak.concatenate([data_events, tmp_])


    sig_events["label"] = ak.zeros_like(sig_events["weight"])
    bkg_events["label"] = ak.ones_like(bkg_events["weight"]) * bkg_events["proc_id"]

    MC_events = ak.concatenate([sig_events, bkg_events])
    MC_events = ak.values_astype(MC_events, np.float64)

    # Manipulate fields to adjust missing fields
    MC_events["dEta_ljh"] = abs(MC_events.eta - MC_events.first_pt_jet_eta)
    MC_events["dEta_sljh"] = ak.where(
        MC_events["second_jet_eta"] != -999.,
        abs(MC_events.eta - MC_events.second_pt_jet_eta),
        ak.ones_like(MC_events.second_jet_eta) * -1
    )
    MC_events["dEta_ljslj"] = ak.where(
        MC_events["second_jet_eta"] != -999.,
        abs(MC_events.first_pt_jet_eta - MC_events.second_pt_jet_eta),
        ak.ones_like(MC_events.second_jet_eta) * -1
    )
    MC_events["dR_ljlp"] = np.sqrt((MC_events.LeadPhoton_eta - MC_events.first_jet_eta)**2 + (MC_events.DeltaPhi_gamma1_cjet)**2)
    MC_events["dR_ljslp"] = np.sqrt((MC_events.SubleadPhoton_eta - MC_events.first_jet_eta)**2 + (MC_events.DeltaPhi_gamma2_cjet)**2)

    MC_events["lj_ptoM"] = MC_events.first_jet_pt / MC_events.first_jet_mass

    MC_events["slj_ptoM"] =  ak.where(
        MC_events.second_jet_pt != -999,
        MC_events.second_jet_pt / MC_events.second_jet_mass,
        ak.ones_like(MC_events.second_jet_pt) * -1
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
    MC_events["lj_ptoM"] = awkward.where(
            MC_events["lj_ptoM"] < -1.,
            ak.ones_like(MC_events.lj_ptoM) * -1,
            MC_events["lj_ptoM"]
    )
    MC_events["slj_ptoM"] = awkward.where(
            MC_events["slj_ptoM"] < -1.,
            ak.ones_like(MC_events.slj_ptoM) * -1,
            MC_events["slj_ptoM"]
    )
    MC_events["first_muon_pt"] = awkward.where(
            MC_events["first_muon_pt"] < 0,
            ak.ones_like(MC_events.first_muon_pt) * -1,
            MC_events["first_muon_pt"]
    )
    MC_events["first_electron_pt"] = awkward.where(
            MC_events["first_electron_pt"] < 0,
            ak.ones_like(MC_events.first_electron_pt) * -1,
            MC_events["first_electron_pt"]
    )

    MC_events["first_jet_wp"] = evaluate_wp(year, MC_events.first_jet_jet_pn_b_plus_c, MC_events.first_jet_jet_pn_b_vs_c)
    MC_events["second_jet_wp"] = evaluate_wp(year, MC_events.second_jet_jet_pn_b_plus_c, MC_events. second_jet_jet_pn_b_vs_c)
    MC_events["third_jet_wp"] = evaluate_wp(year, MC_events.third_jet_jet_pn_b_plus_c, MC_events.third_jet_jet_pn_b_vs_c)

    # print yields
    for proc in range(0, 8):
        print(f"proc: {proc}, n ev: {len(MC_events[MC_events.proc_id == proc])}, sum weights: {ak.sum(MC_events.weight[MC_events.proc_id == proc])}")

# load configurtion for the bdt
config=f"{opt.config}"
print(f"Loading BDT configuration from: {config}")

with open(config, "r") as f_in:
    bdt_config = json.load(f_in)

if not opt.skip_concatenation:
    # decide if you want to transform the features in the range -1, 1
    print()
    if opt.TRANSFORM:
        print("Transforming features to the range -1, 1")
        for field in bdt_config["features"]:
            if field == "n_jets": 
                print("max", field, ak.max(MC_events[field]), bdt_config["features_norm"][field])
                continue
            print("max", field, ak.max(MC_events[field]), bdt_config["features_norm"][field])
            MC_events[field] = MC_events[field] / bdt_config["features_norm"][field]
            #print(field, MC_events[field])
    else:
        print("skip transforming features")

    for field in bdt_config["features"]:
        # print(field, MC_events[field][MC_events[field]<-1])
        print(field, MC_events[field])

    print()
    print("Processes marked as 'Signal' or 'Background' will be used to train the BDT as signal and background,     respectively.")
    print("Out of %d total events, found %d signal and %d background events." % (len(MC_events), len(sig_events), len(bkg_events)))

    if opt.multiclass:
        MC_dump_name = "nTuples/MC_events_multiclass.parquet"
    else:
        MC_dump_name = "nTuples/MC_events.parquet"
    ak.to_parquet(MC_events, MC_dump_name, compression="snappy")
    print("MC_events saved successfully!")

# Reload MC_events
if opt.multiclass:
    MC_dump_name = "nTuples/MC_events_multiclass.parquet"
else:
    MC_dump_name = "nTuples/MC_events.parquet"
MC_events = ak.from_parquet(MC_dump_name)
print("MC_events reloaded successfully!")

# Split events for k-fold training
MC_events_kfold = []
MC_events_kfold.append(MC_events[((MC_events.event % 2) == 0)])
MC_events_kfold.append(MC_events[((MC_events.event % 2) == 1)])

# Add test/train/val split
for i, MC in enumerate(MC_events_kfold):
    split = np.random.randint(6, size = len(MC))
    MC_events_kfold[i]["train_split"] = awkward.from_numpy(split) # 0-3 = train, 4-5 = test, none = validation

    #events = awkward.nan_to_num(events, nan=-999., posinf=-999., neginf=-999.)
    print(MC_events_kfold[i]["train_split"])
    print(len(MC_events_kfold[i][MC_events_kfold[i]["train_split"] < 4]), len(MC_events_kfold[i][MC_events_kfold[i]["train_split"] > 3]), len(MC_events_kfold[i][MC_events_kfold[i]["train_split"] >= 6]))

# perform the actual training
bdt = []
d_train = []
d_test = []
events_train = []
events_test = []
ggh_only = []
select_train = []
select_test = []
opt.full = True

# Correct for the abs(weight) for XGBoost
file = "inputs/abs_to_nominal.json"
ceval = correctionlib.CorrectionSet.from_file(file)
for corr in ceval.values():
    print(f"Correction {corr.name} has {len(corr.inputs)} inputs")
    for ix in corr.inputs:
        print(f"   Input {ix.name} ({ix.type}): {ix.description}")
var_sf = "LeadPhoton_pt_mgg"
var_sf_2 = "SubleadPhoton_pt_mgg"

print(f'bdt features: {bdt_config["features"]}')
for i, MC in enumerate(MC_events_kfold):
        MC["weight_train"] = ak.ones_like(MC.weight)  
        # MC["weight_train"] = abs(MC.weight)  
        events_train.append((MC.train_split <= 3))
        events_test.append((MC.train_split > 3))

        ggh_only.append((MC.proc_id == 0))
        
        sf = ceval["abs_to_nominal"].evaluate(MC[var_sf], MC[var_sf_2])
        MC[events_train[i]]["weight"] = MC[events_train[i]].weight * sf[events_train[i]]

        # we double the ggh signal events for the training
        MC[events_train[i]]["weight_train"] = awkward.where(
                    MC[events_train[i]]["proc_id"] == 0,
                    MC[events_train[i]].weight_train * 2,
                    MC[events_train[i]].weight_train
            )

        if opt.full:
                select_train.append(events_train[i])
                select_test.append(events_test[i])
        else:
                select_train.append((events_train[i]) & (ggh_only[i]))
                select_test.append((events_test[i]) & (ggh_only[i]))

        
        features_train = awkward.to_numpy(MC[select_train[i]][bdt_config["features"]])
        # features_train = features_train[MC[events_train[i]]["weight"] > 0]
        features_train = features_train.view((float, len(features_train.dtype.names)))

        features_test = awkward.to_numpy(MC[select_test[i]][bdt_config["features"]])
        # features_test = features_test[MC[events_test[i]]["weight"] > 0]
        features_test = features_test.view((float, len(features_test.dtype.names))) 

        # Make dmatrix for xgboost
        # XGBoost can't handle negative weights so we put the negative ones to zero
        d_train.append(
                xgboost.DMatrix(
                        features_train,
                        awkward.to_numpy(MC[select_train[i]]["label"]),
                        weight = awkward.to_numpy(MC[select_train[i]]["weight_train"]),
                        feature_names=bdt_config["features"]
                )
        )

        d_test.append(
                xgboost.DMatrix(
                        features_test,
                        awkward.to_numpy(MC[select_test[i]]["label"]),
                        weight = awkward.to_numpy(MC[select_test[i]]["weight_train"]),
                        feature_names=bdt_config["features"]
                )
        )
        
        if not opt.LOAD:
            print("training...")
            eval_list = [(d_train[i], "train"), (d_test[i], "test")]
            progress = {}
            bdt_config["mva"]["param"]["scale_pos_weight"] = awkward.sum(MC[MC.label == 0]["weight_train"]) / awkward.sum(MC[MC.label == 1]["weight_train"])
            bdt.append(
                    xgboost.train(
                            bdt_config["mva"]["param"],
                            d_train[i],
                            bdt_config["mva"]["n_trees"],
                            eval_list, 
                            evals_result = progress,
                            early_stopping_rounds = bdt_config["mva"]["early_stopping_rounds"]
                    )
            )
        else:
            sets = ["even", "odd"]
            print("loading model...")
            model = xgboost.Booster()
            model.load_model(f"{opt.xgb_model_dir}/{opt.wgt_model}_{sets[i]}.xgb")
            bdt.append(model)


#model_name = f"{formatted_date}_full_MET_bjets_ssljet_dijet_multiclass_{year}"
if "tagger" in opt.config:
    model_name = f"{formatted_date}_MET_taggers_ssljet_dijet_multiclass_TH_{year}"
else:
    model_name = f"{formatted_date}_MET_bjets_ssljet_dijet_multiclass_TH_2_{year}"
if opt.TRANSFORM:
    model_name = model_name + "_tranformed"
if not opt.full:
    model_name = model_name + "_ggh_only"
if opt.SAVE:
    for i, set in enumerate(["even", "odd"]):
        os.system("mkdir -p %s" % ("/work/bevila_t/HpC_Analysis/ggHvOthers_BDT_training/"))
        bdt[i].save_model(f"/work/bevila_t/HpC_Analysis/ggHvOthers_BDT_training/XGBoost_models/weights_{model_name}_{set}.xgb")

# Validate 
print()
check_train = []
check = []
for i, MC in enumerate(MC_events_kfold): 
    print("validating...")
    check_train.append(bdt[i].predict(d_train[i]))
    check.append(bdt[i].predict(d_test[i]))
    #area under the precision-recall curve
    score = average_precision_score(MC[select_test[i]]["label"], check[i])
    print('area under the precision-recall curve: {:.6f}'.format(score))

    check2 = check[i].round()
    score = precision_score(MC[select_test[i]]["label"], np.argmax((check2), axis=1), average="micro")
    print('precision score: {:.6f}'.format(score))

    score = recall_score(MC[select_test[i]]["label"], np.argmax((check2), axis=1), average="micro")
    print('recall score: {:.6f}'.format(score))

    imp = get_importance(bdt[i], bdt_config["features"])
    print('Importance array: ', imp)
    print("|"+"-"*10+"importance"+"-"*10+"|")
    for var in imp:
        print("| {:20} : {: >5} |".format(var[0], var[1]))
    print("|"+"-"*30+"|")

    print('area under the precision-recall curve test set: {:.6f}'.format(score))

    plot_ROC_multiclass(
        test_mask = events_test[i], 
        train_mask = events_train[i], 
        labels = MC["label"],
        check_test = check[i],
        check_train = check_train[i],
        bdt = bdt[i], 
        bdt_config = bdt_config,
        plot_labels_ = ["signal", "th/tth", "vbf", "vh"],
        weights = MC["weight_train"],
        outname = f"plots/{formatted_date}/ROC_training_wgts_{i}_{formatted_date}_multiclass.png"
    )

    plot_ROC_multiclass(
        test_mask = events_test[i], 
        train_mask = events_train[i], 
        labels = MC["label"],
        check_test = check[i],
        check_train = check_train[i],
        bdt = bdt[i], 
        bdt_config = bdt_config,
        plot_labels_ = ["signal", "th/tth", "vbf", "vh"],
        weights = MC["weight"],
        outname = f"plots/{formatted_date}/ROC_true_wgt_{i}_{formatted_date}_multiclass.png"
    )

    # Predict
    features = awkward.to_numpy(MC[bdt_config["features"]])
    features = features.view((float, len(features.dtype.names)))
    
    if i == 0:
        MC["mva_score"] = bdt[1].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
    else:
        MC["mva_score"] = bdt[0].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
    labels_ = ["sig", "tth", "vbf", "vh"]
    for j in range(bdt_config["mva"]["param"]["num_class"]):
        MC[f"mva_score_{labels_[j]}"] = MC["mva_score"][:, j]


features = awkward.to_numpy(MC_events[bdt_config["features"]])
features = features.view((float, len(features.dtype.names)))
bdt_score_0 = bdt[1].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
bdt_score_1 = bdt[0].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
bdt_score = ak.concatenate([bdt_score_0, bdt_score_1])

for i in range(bdt_config["mva"]["param"]["num_class"]):
    MC_events[f"mva_score_{labels_[i]}"] = ak.where(
        MC_events.event % 2 == 0,
        bdt_score_0[:, i],
        bdt_score_1[:, i]
    )
scores = [ak.singletons(MC_events[f"mva_score_{labels_[x]}"]) for x in range(bdt_config["mva"]["param"]["num_class"])]
MC_events["mva_score"] = ak.concatenate(scores, axis=1)

plot_confusion_matrix(MC_events, bdt_config, f"plots/{formatted_date}/confusion_matrix_{formatted_date}_multiclass.png", labels_)


for i, MC in enumerate(MC_events_kfold):
        sf = ceval["abs_to_nominal"].evaluate(MC[var_sf], MC[var_sf])
        MC[events_train[i]]["weight"] = MC[events_train[i]].weight / sf[events_train[i]]
        MC["square_weight"] = MC.weight ** 2
MC_events["square_weight"] = MC_events.weight ** 2

#bdt_score
for i, MC in enumerate(MC_events_kfold):
    fig, axs = plt.subplots(1,1, figsize=(7, 7))
    min_ = 0
    max_ = 1
    nbins = 50
    var = "mva_score_sig"
    h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot_err = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_bg = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot.fill(bdt_score_tot = MC[var], weight = MC.weight/ak.sum(MC.weight))
    #h_bdt_score_tot.fill(bdt_score_tot = MC_events.mva_score[(MC_events.proc_id > -3)], weight = MC_events.weight[(MC_events.proc_id > -3)])
    #h_bdt_score_tot.fill(bdt_score_tot = qcd.mva_score, weight = qcd.weight)
    h_bdt_score_tot_err.fill(bdt_score_tot = MC[var], weight = MC.square_weight)
    h_bdt_score_sig.fill(bdt_score_tot = MC[var][(MC.label == 0)], weight = MC.weight[(MC.label == 0)]/ak.sum(MC.weight))
    h_bdt_score_bg.fill( bdt_score_tot = MC[var][(MC.label != 0)], weight = MC.weight[(MC.label != 0)]/ak.sum(MC.weight))

    h_bdt_score_sig = h_bdt_score_sig

    h_bdt_score_bg.project("bdt_score_tot").plot(ax=axs, label="bg_mc")
    h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal")
    h_bdt_score_tot.project("bdt_score_tot").plot(ax=axs, color="green", label="tot_mc")


    axs.legend( prop={'size': 14})
    axs.grid(color='grey', linestyle='--', alpha=0.5)
    axs.set_ylabel('events')
    # axs.set_yscale('log')
    axs.set_xlabel('mva score', fontsize=14)
    axs.set_ylabel('events/0.02', fontsize=14)
    axs.tick_params(axis='x', labelsize=14)
    axs.tick_params(axis='y', labelsize=14)

    plt.plot()
    plt.savefig(f"plots/{formatted_date}/mva_score_sig_bg_{model_name}_{i}.pdf")


#bdt_score
fig, axs = plt.subplots(1,1, figsize=(10, 10))

min_ = 0
max_ = 1
nbins = 50

LeadPhoton_et_ax  = hist.axis.Regular(nbins, min_, max_, flow=False, name="bdt_score_tot")
LeadPhoton_et_cax = hist.axis.StrCategory(["vbf", "vh", "tth", "thq", "thw", "ch", "bh", "ggh_l", "ggh_c","ggh_b"], name="c")
full_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax)
h_bdt_score_tot_err = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "bdt_score_tot", label = "tot"))
h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))

#for i, MC in enumerate(MC_events_kfold):
var = "mva_score_sig"
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], c="ggh_c")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], c="ggh_l")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], c="ggh_b")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 1)], weight=MC_events.weight[(MC_events.proc_id == 1)], c="tth")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 2)], weight=MC_events.weight[(MC_events.proc_id == 2)], c="vbf")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 3)], weight=MC_events.weight[(MC_events.proc_id == 3)], c="vh")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 4)], weight=MC_events.weight[(MC_events.proc_id == 4)], c="thq")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 5)], weight=MC_events.weight[(MC_events.proc_id == 5)], c="thw")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 6)], weight=MC_events.weight[(MC_events.proc_id == 6)], c="ch")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 7)], weight=MC_events.weight[(MC_events.proc_id == 7)], c="bh")
#full_hist.fill(bdt_score_tot = qcd.mva_score, weight=qcd.weight, c="QCD")

h_bdt_score_tot.fill(bdt_score_tot = MC_events[var], weight = MC_events.weight)
h_bdt_score_tot_err.fill(bdt_score_tot = MC_events[var], weight = MC_events.square_weight)
# h_bdt_score_tot_err.fill(bdt_score_tot = MC_events.mva_score[(MC_events.proc_id > -3)], weight = MC_events.square_weight[(MC_events.proc_id > -3)])
# h_bdt_score_tot_err.fill(bdt_score_tot = qcd.mva_score, weight = qcd.square_weight)
h_stack = full_hist.stack("c")

h_stack[::-1].plot(ax=axs, stack=True, histtype="fill")

h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
h_bdt_score_sig.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) | (MC_events.proc_id > 3)], weight = MC_events.weight[(MC_events.proc_id == 0) | (MC_events.proc_id > 3)])
h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal")
axs.legend( prop={'size': 14})
axs.grid(color='grey', linestyle='--', alpha=0.5)

mc= {}
mc["bins"] = {}
mc["errs"] = {}
mc["edges"] = {}

mc["bins"]["tot"] = h_bdt_score_tot.to_numpy()[0]
mc["edges"]["tot"] = h_bdt_score_tot.to_numpy()[1] + 0.01
mc["errs"]["tot"] = np.sqrt(h_bdt_score_tot_err.to_numpy()[0])

ydn = [mc["bins"]["tot"][i] - x for i, x in enumerate(mc["errs"]["tot"])]
yup = [mc["bins"]["tot"][i] + x for i, x in enumerate(mc["errs"]["tot"])]

for i, x in enumerate(mc["edges"]["tot"][:-1]):
    axs.fill_between([x - 0.01, x + 0.01], [ydn[i], ydn[i]], [yup[i], yup[i]], facecolor='grey', alpha=0.5, edgecolor='grey', label="MC stat unc.")

axs.set_title('ggH vs H bkg - sig mva score', fontsize=14)
axs.set_ylabel('events')
axs.set_xlabel('ggH vs H bkg mva score', fontsize=14)
axs.set_ylabel('events/0.02', fontsize=14)
axs.tick_params(axis='x', labelsize=14)
axs.tick_params(axis='y', labelsize=14)
    
plt.plot()
if opt.PLOTS: fig.savefig(f"plots/{formatted_date}/mva_score_sig_bg_stack_{model_name}.pdf")

#bdt_score
fig, axs = plt.subplots(1,1, figsize=(10, 10))

min_ = 0
max_ = 1
nbins = 80
var = "mva_score_sig"

LeadPhoton_et_ax  = hist.axis.Regular(nbins, min_, max_, flow=False, name="bdt_score_tot")
LeadPhoton_et_cax_sig = hist.axis.StrCategory(["ch", "bh", "ggh_l", "ggh_c","ggh_b"], name="c")
LeadPhoton_et_cax_bkg = hist.axis.StrCategory(["bkg"], name="c")
sig_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_sig)
bkg_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_bkg)
h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))

#for i, MC in enumerate(MC_events_kfold):
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], c="ggh_c")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], c="ggh_l")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], c="ggh_b")
bkg_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 1)], weight=MC_events.weight[(MC_events.proc_id == 1)], c="bkg")
bkg_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 2)], weight=MC_events.weight[(MC_events.proc_id == 2)], c="bkg")
bkg_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 3)], weight=MC_events.weight[(MC_events.proc_id == 3)], c="bkg")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 4)], weight=MC_events.weight[(MC_events.proc_id == 4)], c="thq")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 5)], weight=MC_events.weight[(MC_events.proc_id == 5)], c="thw")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 6)], weight=MC_events.weight[(MC_events.proc_id == 6)], c="ch")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 7)], weight=MC_events.weight[(MC_events.proc_id == 7)], c="bh")
#full_hist.fill(bdt_score_tot = qcd.mva_score, weight=qcd.weight, c="QCD")

h_bdt_score_tot.fill(bdt_score_tot = MC_events[var], weight = MC_events.weight)
sh_stack = sig_hist.stack("c")
bh_stack = bkg_hist.stack("c")

sh_stack[::-1].plot(ax=axs, stack=True, histtype="fill", alpha=0.6)
bh_stack[::-1].plot(ax=axs, stack=True, histtype="step", alpha=0.9)

#h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
#h_bdt_score_sig.fill(bdt_score_tot = MC_events.DNN_score[(MC_events.proc_id == 1) | (MC_events.proc_id > 4)], weight = MC_events.weight[(MC_events.proc_id == 1) | (MC_events.proc_id > 4)])
#h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal")
axs.legend( prop={'size': 14})
axs.grid(color='grey', linestyle='--', alpha=0.5)

mc= {}
mc["bins"] = {}
mc["errs"] = {}
mc["edges"] = {}

mc["bins"]["tot"] = h_bdt_score_tot.to_numpy()[0]

axs.set_ylabel('events')
axs.set_title('BDT sig score', fontsize=14)
axs.set_xlabel('ggH vs H bkg mva score', fontsize=14)
axs.set_ylabel('events/0.02', fontsize=14)
axs.tick_params(axis='x', labelsize=14)
axs.tick_params(axis='y', labelsize=14)
    
plt.plot()
if opt.PLOTS: fig.savefig(f"plots/{formatted_date}/mva_score_sig_bg_stack_{model_name}.pdf")

#bdt_score
fig, axs = plt.subplots(1,1, figsize=(10, 10))

min_ = 0
max_ = 1
nbins = 80
var = "mva_score_sig"

LeadPhoton_et_ax  = hist.axis.Regular(nbins, min_, max_, flow=False, name="bdt_score_tot")
LeadPhoton_et_cax_sig = hist.axis.StrCategory(["sig"], name="c")
LeadPhoton_et_cax_bkg = hist.axis.StrCategory(["vbf/vh", "tth"], name="c")
sig_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_sig)
bkg_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax_bkg)
h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))

#for i, MC in enumerate(MC_events_kfold):
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], c="sig")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], c="sig")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], c="sig")
bkg_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 1)], weight=MC_events.weight[(MC_events.proc_id == 1)], c="tth")
bkg_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 2)], weight=MC_events.weight[(MC_events.proc_id == 2)], c="vbf/vh")
bkg_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 3)], weight=MC_events.weight[(MC_events.proc_id == 3)], c="vbf/vh")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 4)], weight=MC_events.weight[(MC_events.proc_id == 4)], c="sig")
sig_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 5)], weight=MC_events.weight[(MC_events.proc_id == 5)], c="sig")
#full_hist.fill(bdt_score_tot = qcd.mva_score, weight=qcd.weight, c="QCD")

h_bdt_score_tot.fill(bdt_score_tot = MC_events[var], weight = MC_events.weight)
sh_stack = sig_hist.stack("c")
bh_stack = bkg_hist.stack("c")

sh_stack[::-1].plot(ax=axs, stack=True, histtype="step", alpha=0.9)
bh_stack[::-1].plot(ax=axs, stack=True, histtype="fill", alpha=0.6)

#h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
#h_bdt_score_sig.fill(bdt_score_tot = MC_events.DNN_score[(MC_events.proc_id == 1) | (MC_events.proc_id > 4)], weight = MC_events.weight[(MC_events.proc_id == 1) | (MC_events.proc_id > 4)])
#h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal")
axs.legend( prop={'size': 14})
axs.grid(color='grey', linestyle='--', alpha=0.5)

mc= {}
mc["bins"] = {}
mc["errs"] = {}
mc["edges"] = {}

mc["bins"]["tot"] = h_bdt_score_tot.to_numpy()[0]

axs.set_ylabel('events')
axs.set_title('BDT sig score', fontsize=14)
axs.set_xlabel('ggH vs H bkg mva score', fontsize=14)
axs.set_ylabel('events/0.02', fontsize=14)
axs.tick_params(axis='x', labelsize=14)
axs.tick_params(axis='y', labelsize=14)
    
plt.plot()
if opt.PLOTS: fig.savefig(f"plots/{formatted_date}/mva_score_sig_bg_stack.pdf")

#bdt_score
fig, axs = plt.subplots(1,1, figsize=(7, 7))

min_ = 0
max_ = 1
nbins = 50
var = "mva_score_sig"
LeadPhoton_et_ax  = hist.axis.Regular(nbins, min_, max_, flow=False, name="bdt_score_tot")
LeadPhoton_et_cax = hist.axis.StrCategory(["ggh_l", "ggh_c", "ggh_b"], name="c")
full_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax)
h_bdt_score_tot_err = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "bdt_score_tot", label = "tot"))
h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))

#for i, MC in enumerate(MC_events_kfold):
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 4)], c="ggh_c")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 0)], c="ggh_l")
full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], weight=MC_events.weight[(MC_events.proc_id == 0) & (MC_events.first_jet_hFlav == 5)], c="ggh_b")

h_stack = full_hist.stack("c")

h_stack[::-1].plot(ax=axs, stack=True, histtype="fill")

axs.legend( prop={'size': 14})
axs.grid(color='grey', linestyle='--', alpha=0.5)

axs.set_ylabel('events')
axs.set_xlabel('ggH vs H bkg mva score', fontsize=14)
axs.set_ylabel('events/0.02', fontsize=14)
axs.tick_params(axis='x', labelsize=14)
axs.tick_params(axis='y', labelsize=14)
axs.set_xlim([min_, max_])
    
plt.plot()
if opt.PLOTS:
    fig.savefig(f"plots/{formatted_date}/mva_score_sig_bg_stack_{model_name}.pdf")

    with open(f"inputs/plot_dict.json", "r") as config_file:
        plot_config = json.load(config_file)

    for plot in plot_config:
        plot_variable_comparison(plot_config[plot], MC_events, None, formatted_date)


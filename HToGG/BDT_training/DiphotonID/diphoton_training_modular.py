#!/usr/bin/env python
import argparse
from datetime import date
from operator import itemgetter
from sklearn import preprocessing
from sklearn.metrics import average_precision_score
from sklearn.metrics import roc_curve, auc, recall_score, precision_score
from sklearn.utils.class_weight import compute_sample_weight
import awkward as ak
import correctionlib
import correctionlib.schemav2 as cs
import gc  # For garbage collection if needed
import hist
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pickle
import xgboost
from plot_utils import plot_variable_comparison, plot_ROC, plot_ROC_multiclass, plot_confusion_matrix

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
    

def main():
    parser = argparse.ArgumentParser(description='Diphoton BDT Analysis')
    parser.add_argument('--input', type=str, help='Path to input file')
    parser.add_argument('--year', type=str, default="2017", help='year to analyse')
    parser.add_argument('--model', type=str, help='Path to pre-trained model')
    parser.add_argument('--multiclass',  action="store_true", default=False, help='train multiclass model')
    parser.add_argument('--skip_concatenation', action="store_true", help='load a pre-processed file set')
    parser.add_argument('--config', type=str, default="input/diphoton_bdt_config_combined.json", help='config file for the training')
    parser.add_argument('--abs_eta', action="store_true", default=False, help='anchor the eta fields')
    parser.add_argument('--saved', dest="SAVE", action="store_false", default=True, help='save the model')
    args = parser.parse_args()

    # ---- Main analysis pipeline ----
    # Add your data loading and processing logic here using `args.input`, etc.
    print(f"XGBoost version: {xgboost.__version__}")
    # # Read files and normalise the weights
    proc_dict_2018 = {
        "cH_4FS_FXFX_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/cH_4FS_FXFX_M125_2018/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 1,
        },
        "bH_5FS_FXFX_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/bH_5FS_FXFX_M125_2018/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 1,
        },
        "ggh_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/ggh_M125_2018/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 2,
        },
        "tth_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/tth_M125_2018/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 3,
        },
        "vbf_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/vbf_M125_2018/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 4,
        },
        "vh_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/vh_M125_2018/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 5,
        },
        "DiphotonBox_low_mass_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged//DiphotonBox_low_mass_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "DiphotonBox_high_mass_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/DiphotonBox_high_mass_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "GJets_HT-40To100_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/GJets_HT-40To100_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-100To200_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/GJets_HT-100To200_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-200To400_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/GJets_HT-200To400_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-400To600_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/GJets_HT-400To600_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-600ToInf_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/GJets_HT-600ToInf_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "DY_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/DY_M125_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -4,
        },
        "QCD_M125_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/QCD_M125_mgg_high_pt_40ToInf_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2018_mgg_low": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/QCD_mgg_low_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2018_mgg_high_pt_30To40": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/QCD_M125_mgg_high_pt_30To40_2018/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "Data_2018": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2018/diphoton_training_2018_250417/merged/Data_2018/allData_NOTAG_merged.parquet",
            "type": "data",
            "label": -1.,
            "proc_id": 0,
        },
    }
    proc_dict_2017 = {
        "ggh_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/ggh_M125_2017/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 2,
        },
        "tth_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/tth_M125_2017/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 3,
        },
        "vbf_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/vbf_M125_2017/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 4,
        },
        "vh_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/vh_M125_2017/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 5,
        },
        "cH_4FS_FXFX_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/cH_4FS_FXFX_M125_2017/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 1,
        },
        "bH_5FS_FXFX_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/bH_5FS_FXFX_M125_2017/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 1,
        },
        "DiphotonBox_low_mass_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged//DiphotonBox_low_mass_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "DiphotonBox_high_mass_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/DiphotonBox_high_mass_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "GJets_HT-40To100_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/GJets_HT-40To100_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-100To200_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/GJets_HT-100To200_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-200To400_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/GJets_HT-200To400_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-400To600_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/GJets_HT-400To600_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-600ToInf_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_no_cTag_JEC_2017_241014/merged/GJets_HT-600ToInf_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "DY_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_no_cTag_JEC_2017_241014/merged/DYJetsToLL_M-50_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -4,
        },
        "QCD_M125_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/QCD_M125_2017/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2017_mgg_low": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/QCD_2017_mgg_low/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2017_mgg_high_pt_30To40": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/QCD_2017_mgg_high_pt_30To40/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "Data_2017": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2017/DiphotonID_training_Recalculated_photonID_250411/diphoton_training/merged/Data_2017/allData_NOTAG_merged.parquet",
            "type": "data",
            "label": -1.,
            "proc_id": 0,
        },
    }
    proc_dict_2016_pre = {
        "ggh_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/ggh_M125_2016_pre/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 2,
        },
        "tth_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/tth_M125_2016_pre/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 3,
        },
        "vbf_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/vbf_M125_2016_pre/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 4,
        },
        "vh_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/vh_M125_2016_pre/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 5,
        },
        "DiphotonBox_low_mass_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged//DiphotonBox_low_mass_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "DiphotonBox_high_mass_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/DiphotonBox_high_mass_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "GJets_HT-40To100_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/GJets_HT-40To100_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-100To200_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/GJets_HT-100To200_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-200To400_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/GJets_HT-200To400_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-400To600_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/GJets_HT-400To600_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-600ToInf_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/GJets_HT-600ToInf_M125_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        #"DY_M125_2016_pre": {
        #    "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/DYJetsToLL_M-50_2016_pre/NOTAG_merged.parquet",
        #    "type": "background",
        #    "label": 0.,
        #    "proc_id": -4,
        #},
        "QCD_M125_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/QCD_M125_mgg_high_pt_high_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2016_pre_mgg_low": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/QCD_M125_low_high_pt_high_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2016_pre_mgg_high_pt_30To40": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/QCD_M125_mgg_high_pt_low_2016_pre/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "Data_2016_pre": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/Data_2016/allData_NOTAG_merged.parquet",
            "type": "data",
            "label": -1.,
            "proc_id": 0,
        },
    }
    proc_dict_2016_post = {
        "ggh_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/ggh_M125_2016_post/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 2,
        },
        "tth_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/tth_M125_2016_post/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 3,
        },
        "vbf_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/vbf_M125_2016_post/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 4,
        },
        "vh_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/vh_M125_2016_post/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 5,
        },
        "DiphotonBox_low_mass_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged//DiphotonBox_low_mass_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "DiphotonBox_high_mass_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/DiphotonBox_high_mass_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "GJets_HT-40To100_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/GJets_HT-40To100_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-100To200_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/GJets_HT-100To200_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-200To400_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/GJets_HT-200To400_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-400To600_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/GJets_HT-400To600_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-600ToInf_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/GJets_HT-600ToInf_M125_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        # "DY_M125_2016_post": {
        #     "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016pre/merged/DYJetsToLL_M-50_2016_pre/NOTAG_merged.parquet",
        #     "type": "background",
        #     "label": 0.,
        #     "proc_id": -4,
        # },
        "QCD_M125_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/QCD_M125_mgg_high_pt_high_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2016_post_mgg_low": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/QCD_M125_low_high_pt_high_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_2016_post_mgg_high_pt_30To40": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/QCD_M125_mgg_high_pt_low_2016_post/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "Data_2016_post": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016post/merged/Data_2016/allData_NOTAG_merged.parquet",
            "type": "data",
            "label": -1.,
            "proc_id": 0,
        },
    }
    proc_dict_2016 = {
        "ggh_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/ggh_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 2,
        },
        "tth_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/tth_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 3,
        },
        "vbf_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/vbf_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 4,
        },
        "vh_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/vh_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "signal",
            "label": 1.,
            "proc_id": 5,
        },
        "DiphotonBox_low_mass_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged//DiphotonBox_low_mass_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "DiphotonBox_high_mass_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/DiphotonBox_high_mass_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -1,
        },
        "GJets_HT-40To100_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/GJets_HT-40To100_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-100To200_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/GJets_HT-100To200_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-200To400_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/GJets_HT-200To400_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-400To600_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/GJets_HT-400To600_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "GJets_HT-600ToInf_M125_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/GJets_HT-600ToInf_M125_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -2,
        },
        "DYJetsToLL_M-50_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/DYJetsToLL_M-50_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -4,
        },
        "QCD_mgg_high_pt_high_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/QCD_mgg_high_pt_high_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_mgg_low_pt_high_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/QCD_mgg_low_pt_high_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "QCD_mgg_high_pt_low_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/QCD_mgg_high_pt_low_2016/nominal/NOTAG_merged.parquet",
            "type": "background",
            "label": 0.,
            "proc_id": -3,
        },
        "Data_2016": {
            "file": "/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/HiggsDNA_output/DiphotonID_training_2016/diphoton_training_2016/merged/Data_2016/allData_NOTAG_merged.parquet",
            "type": "data",
            "label": -1.,
            "proc_id": 0,
        },
    }
    # Get the current date
    current_date = date.today()
    # Format the date
    formatted_date = current_date.strftime("%y%m%d")

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

    if not args.skip_concatenation:
        if args.year == "combined":
            # Combine all dictionaries
            # proc_dict = {**proc_dict_2016_pre, **proc_dict_2016_post, **proc_dict_2017, **proc_dict_2018}
            proc_dict = {**proc_dict_2016, **proc_dict_2017, **proc_dict_2018}
            # proc_dict = {**proc_dict_2017, **proc_dict_2018}
        elif args.year == "2016":
            # proc_dict = {**proc_dict_2016_pre, **proc_dict_2016_post}
            proc_dict = {**proc_dict_2016}
        elif args.year == "2017":
            proc_dict = proc_dict_2017
        elif args.year == "2018":
            proc_dict = proc_dict_2018
        else:
            raise ValueError(f"Year not specified or unrecognized: {args.year}")
        # # concatenate the MC and Data events (separately) and add normalisation
        with open(
                "/work/bevila_t/HpC_Analysis/DiphotonMVA_training/input/cross_section_amrutha.json", "r"
            ) as pf:
                XSs = json.load(pf)
        # Initialize lists for events
        sig_events = []
        bkg_events = []
        data_events = []
        columns = ['weight', 'dZ', 'CMS_hgg_mass', 'event', 'pt', 'eta', 'phi', 'LeadPhoton_pt_mgg', 'LeadPhoton_eta', 
                   'LeadPhoton_mvaID', 'LeadPhoton_pt', 'LeadPhoton_energy', 'SubleadPhoton_energy', 'SubleadPhoton_pt_mgg', 
                   'SubleadPhoton_eta', 'SubleadPhoton_mvaID', 'Diphoton_cos_dPhi', 'sigmaMrv', 'PV_score', 
                    'nPV', 'dZ', 'dZ_1', 'dZ_2', "n_jets", "sigmaMwv"]
        # Loop through all datasets in the combined dictionary
        for dataset in proc_dict:
            # Determine the year and luminosity for the current dataset
            if "2016_pre" in dataset:
                lumi = XSs["lumi"]["2016_pre"]
            elif "2016_post" in dataset:
                lumi = XSs["lumi"]["2016_post"]
            elif "2017" in dataset:
                lumi = XSs["lumi"]["2017"]
            elif "2018" in dataset:
                lumi = XSs["lumi"]["2018"]
            elif ("2016" in dataset) and ("pre" not in dataset) and ("post" not in dataset):
                lumi = XSs["lumi"]["2016"]
            else:
                raise ValueError(f"Dataset year not specified or unrecognized in key: {dataset}")
            if "Data" not in dataset:
                norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * lumi * 1000
                print(f"{dataset}: xsec = {XSs[dataset]['xs']}, bf = {XSs[dataset]['bf']}, lumi = {lumi}, norm = {norm}")
            else:
                print(f"{dataset}")
            # Process signal events
            if proc_dict[dataset]["type"] == "signal":
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
            # Process background events
            elif proc_dict[dataset]["type"] == "background":
                norm = norm * 1.55 # Adjusting the normalisation for background events
                proc_dict[dataset]["norm"] = norm
                if len(bkg_events) == 0:
                    bkg_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                    bkg_events["weight"] = bkg_events["weight"] * norm
                    bkg_events["proc_id"] = ak.ones_like(bkg_events["weight"]) * proc_dict[dataset]["proc_id"]
                else:
                    tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                    tmp_["weight"] = tmp_["weight"] * norm
                    tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_dict[dataset]["proc_id"]
                    bkg_events = ak.concatenate([bkg_events, tmp_])
                print(f'|----> sum normalised weights: {ak.sum(bkg_events[bkg_events["proc_id"] == proc_dict[dataset]["proc_id"]].weight)}')
            # Process data events
            elif proc_dict[dataset]["type"] == "data":
                if len(data_events) == 0:
                    data_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                    data_events["proc_id"] = ak.ones_like(data_events["weight"]) * proc_dict[dataset]["proc_id"]
                else:
                    tmp_ = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
                    tmp_["proc_id"] = ak.ones_like(tmp_["weight"]) * proc_dict[dataset]["proc_id"]
                    data_events = ak.concatenate([data_events, tmp_])

        if not args.multiclass:
            print()
            print("-"*60)
            print("You have chosen to run single class")
            # Assign labels
            sig_events["label"] = ak.ones_like(sig_events["weight"])
            bkg_events["label"] = ak.zeros_like(bkg_events["weight"])
            data_events["label"] = ak.ones_like(data_events["weight"]) * -1.
        else:
            print("You have chosen to run multi class")
            sig_events["label"] = ak.zeros_like(sig_events["proc_id"])
            bkg_events["label"] = ak.ones_like(bkg_events["proc_id"])
            bkg_events["label"] = ak.where(
                bkg_events["proc_id"] == -1, 
                ak.ones_like(bkg_events["proc_id"]), 
                ak.ones_like(bkg_events["proc_id"]) * 2
            )
            data_events["label"] = ak.ones_like(data_events["weight"]) * -1.

        print(bkg_events.label, bkg_events.label[0])

        # Print final counts
        print(f"Total signal events: {len(sig_events)}")
        print(f"Total background events: {len(bkg_events)}")
        print(f"Total data events: {len(data_events)}")

        # Convert all fields to consistent types in sig_events
        for field in ["dZ", "nPV", "n_jets"]:
            sig_events[field] = ak.values_astype(sig_events[field], np.float64)
            bkg_events[field] = ak.values_astype(bkg_events[field], np.float64)

        for field in sig_events.fields:
            sig_events[field] = ak.fill_none(sig_events[field], 0)
            bkg_events[field] = ak.fill_none(bkg_events[field], 0)

        print()
        print("-"*60)
        print("available fields:")
        for f in  sig_events.fields:
            print(f"    - {f}: {sig_events[f].type}")  # Check fields for 2017
        print("-"*60)
        print()

        # Concatenate arrays
        MC_events = ak.concatenate([sig_events, bkg_events])
        MC_events = ak.values_astype(MC_events, np.float64)
        print("Concatenation successful!")
        # Save MC_events to Parquet

        if args.multiclass:
            MC_dump_name = "nTuples/MC_events_multiclass.parquet"
            data_dump_name = "nTuples/data_events_multiclass.parquet"
        else:
            MC_dump_name = "nTuples/MC_events.parquet"
            data_dump_name = "nTuples/data_events.parquet"

        ak.to_parquet(MC_events, MC_dump_name, compression="snappy")
        print("MC_events saved successfully!")
        # Save data_events to Parquet
        ak.to_parquet(data_events, data_dump_name, compression="snappy")
        print("data_events saved successfully!")
    
    if args.multiclass:
        MC_dump_name = "nTuples/MC_events_multiclass.parquet"
        data_dump_name = "nTuples/data_events_multiclass.parquet"
    else:
        MC_dump_name = "nTuples/MC_events.parquet"
        data_dump_name = "nTuples/data_events.parquet"

    # Reload MC_events
    MC_events = ak.from_parquet(MC_dump_name)
    print("MC_events reloaded successfully!")

    # Reload data_events
    data_events = ak.from_parquet(data_dump_name)
    print("data_events reloaded successfully!")

    # Verify MC_events
    print(f"Number of events in MC_events: {len(MC_events)}")
    # Verify data_events
    print(f"Number of events in data_events: {len(data_events)}")

    # Ready to continue processing
    print("Both MC_events and data_events are loaded. Ready to proceed!")
    gc.collect()  # Trigger garbage collection

    # add VtxProbability 
    if "vtxProb" not in MC_events.fields:
        MC_events["vtxProb"] = 2 * MC_events["sigmaMrv"] / (MC_events["sigmaMrv"] + MC_events["sigmaMwv"])
        data_events["vtxProb"] = 2 * data_events["sigmaMrv"] / (data_events["sigmaMrv"] + data_events["sigmaMwv"])
        MC_events["sigmaMrv"] = ak.values_astype(MC_events["sigmaMrv"], np.float64)
        MC_events["sigmaMwv"] = ak.values_astype(MC_events["sigmaMwv"], np.float64)
        data_events["sigmaMrv"] = ak.values_astype(data_events["sigmaMrv"], np.float64)
        data_events["sigmaMwv"] = ak.values_astype(data_events["sigmaMwv"], np.float64)

    config = args.config
    # Load JSON configuration
    with open(config, "r") as f_in:
        print()
        print("-"*60)
        print(f"Loading BDT configuration from JSON file... {config}")
        bdt_config = json.load(f_in)

    # Verify JSON contents
    print("Training features:", bdt_config["features"])
    # Split by diphoton_eta
    eta_fields = [x for x in bdt_config["features"] if "eta" in x]
    print("Eta-related fields:", eta_fields)
    # Inspect MC_events
    print("Total events:", len(MC_events))

    # Split for k-fold training
    MC_events_kfold = []
    MC_events_kfold.append(MC_events[MC_events.event % 2 == 0])
    MC_events_kfold.append(MC_events[MC_events.event % 2 == 1])
    print("k-fold split complete. Fold sizes:", [len(fold) for fold in MC_events_kfold])
    # Add train/test/val split
    for i, MC in enumerate(MC_events_kfold):
        split = np.random.randint(5, size=len(MC))
        MC["train_split"] = ak.from_numpy(split)
        print(f"Fold {i} splits:", ak.sum(MC.train_split < 3), ak.sum(MC.train_split >= 3), ak.sum(MC.train_split >= 6))

    print(MC_events.event[0], MC_events.event[1], MC_events.event[2])

    if args.abs_eta:
        for field in eta_fields:
            data_events[field] = data_events[field] * np.sign(data_events.eta)
            MC_events[field] = MC_events[field] * np.sign(MC_events.eta)
            for fold in MC_events_kfold:
                fold[field] = fold[field] * np.sign(fold.eta)
                
    # Correct for the abs(weight) for XGBoost
    file = "input/abs_to_nominal.json"
    ceval = correctionlib.CorrectionSet.from_file(file)
    for corr in ceval.values():
        print(f"Correction {corr.name} has {len(corr.inputs)} inputs")
        for ix in corr.inputs:
            print(f"   Input {ix.name} ({ix.type}): {ix.description}")
    var = "LeadPhoton_pt_mgg"
    var2 = "SubleadPhoton_pt_mgg"

    bdt = []
    d_train = []
    d_test = []
    events_train = []
    events_test = []
    scale_weights = []

    for i, MC in enumerate(MC_events_kfold):      
            events_train.append((MC.train_split <= 3))
            events_test.append((MC.train_split > 3))
            # decrease QCD weights for training
            MC[events_train[i]]["weight"] = ak.where(
                        MC[events_train[i]].proc_id != -3,
                        MC[events_train[i]].weight,
                        MC[events_train[i]].weight/30
                )
            sf = ceval["abs_to_nominal"].evaluate(MC[var], MC[var2])
            if not args.multiclass:
                sig_label = 1
            else: 
                sig_label = 0
            MC[events_train[i]]["weight"] = ak.where(
                        MC[events_train[i]]["label"] == sig_label,
                        MC[events_train[i]].weight * sf[events_train[i]],# * (MC[events_train[i]].vtxProb/MC[events_train[i]].sigmaMrv + (1-MC[events_train[i]].vtxProb)/MC[events_train[i]].sigmaMwv),
                        MC[events_train[i]].weight
                )
            features_train = ak.to_numpy(MC[events_train[i]][bdt_config["features"]])
            features_train = features_train.view((float, len(features_train.dtype.names)))

            features_test = ak.to_numpy(MC[events_test[i]][bdt_config["features"]])
            features_test = features_test.view((float, len(features_test.dtype.names))) 

            # Make dmatrix for xgboost
            # XGBoost can't handle negative weights so we put the negative ones to zero

            if args.multiclass:
                scale_weights.append(compute_sample_weight(class_weight = "balanced", y = MC.label))
                #scale_weights.append(compute_sample_weight(class_weight={0: 1.0, 1: 1.0, 2: 1.0}, y = MC.label))
            else:
                scale_weights.append(ak.to_numpy(abs(MC["weight"])))
                bdt_config["mva"]["param"]["scale_pos_weight"] = ak.sum(MC[MC.label != sig_label]["weight"]) / ak.sum(MC[MC.label == sig_label]["weight"])
            d_train.append(
                    xgboost.DMatrix(
                            features_train,
                            label = ak.to_numpy(MC[events_train[i]]["label"]),
                            weight = scale_weights[i][events_train[i]],
                            feature_names = bdt_config["features"]
                    )
            )
            d_test.append(
                    xgboost.DMatrix(
                            features_test,
                            label = ak.to_numpy(MC[events_test[i]]["label"]),
                            weight = scale_weights[i][events_test[i]],
                            feature_names = bdt_config["features"]
                    )
            )
            print("training...")
            eval_list = [(d_train[i], "train"), (d_test[i], "test")]
            progress = {}
            
            print("-"*60)

            if args.SAVE:
                bdt.append(
                    xgboost.train(
                        bdt_config["mva"]["param"],
                        d_train[i],
                        bdt_config["mva"]["n_trees"],
                        eval_list, 
                        evals_result = progress,
                        early_stopping_rounds = bdt_config["mva"]["early_stopping_rounds"],
                        
                    )
                )

    if args.SAVE:
        if args.multiclass:
            outname_ = f"XGBoost_models/new/weights_DiphotonID_full_run2_{formatted_date}_multiclass"
        else:
            outname_ = f"XGBoost_models/new/weights_DiphotonID_full_run2_{formatted_date}"
        for i, set in enumerate(["even", "odd"]):
            bdt[i].save_model(f"{outname_}_{set}.xgb")
            bdt[i].dump_model(f"{outname_}_{set}.json", dump_format='json')
    else:
        for i, set in enumerate(["even", "odd"]):
            booster = xgboost.Booster()
            booster.load_model(f"{args.model}_{set}.xgb")
            bdt.append(booster)

    # Validate 
    check_train = []
    check = []
    print("")
    print("-"*60)
    print("Validation time")
    print("")
    for i, MC in enumerate(MC_events_kfold): 
        print("validating...")
        check_train.append(bdt[i].predict(d_train[i]))
        check.append(bdt[i].predict(d_test[i]))
        # area under the precision-recall curve
        print(check[i])
        score = average_precision_score(MC[events_test[i]]["label"], check[i])
        print('area under the precision-recall curve: {:.6f}'.format(score))

        check2 = check[i].round()
        if args.multiclass:
            check2 = np.argmax(check[i], axis=1)
        
        score = precision_score(MC[events_test[i]]["label"], check2, average="micro")
        print('precision score: {:.6f}'.format(score))

        score = recall_score(MC_events[events_test[i]]["label"], check2, average="micro")
        print('recall score: {:.6f}'.format(score))
        print()

        imp = get_importance(bdt[i], bdt_config["features"])
        print('Importance array: ', imp)
        print("|"+"-"*10+"importance"+"-"*10+"|")
        for var in imp:
            print("| {:20} : {: >5} |".format(var[0], var[1]))
        print("|"+"-"*30+"|")
        print(f'area under the precision-recall curve test set: {score:.6f}')

        colors = ['orange', 'royalblue', 'crimson', 'brown', 'purple', 'olive']

        if args.multiclass:
            plot_ROC_multiclass(
                test_mask = events_test[i], 
                train_mask = events_train[i], 
                labels = MC["label"],
                check_test = check[i],
                check_train = check_train[i],
                bdt = bdt[i], 
                bdt_config = bdt_config,
                plot_labels_ = ["signal", "photon_bkg", "fake_bkg"],
                weights = MC["weight"],
                outname = f"plots/{formatted_date}/ROC_{i}_{formatted_date}_multiclass.png"
            )
        else:
            plot_ROC(
                test_mask = events_test[i], 
                train_mask = events_train[i], 
                labels = MC["label"],
                check_test = check[i],
                check_train = check_train[i],
                bdt = bdt[i],
                weights = MC["weight"],
                outname = f"plots/{formatted_date}/ROC_{i}_{formatted_date}.png"
            )

    del features_train 
    del features_test 
    del d_train 
    del d_test 
    # Predict
    for i, MC in enumerate(MC_events_kfold):
        features = ak.to_numpy(MC[bdt_config["features"]])
        features = features.view((float, len(features.dtype.names)))
        if args.multiclass:
            if i == 0:
                MC["mva_score"] = bdt[1].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
            else:
                MC["mva_score"] = bdt[0].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))

            labels_ = ["sig", "photon_bkg", "fake_bkg"]
            for j in range(bdt_config["mva"]["param"]["num_class"]):
                MC[f"mva_score_{labels_[j]}"] = MC["mva_score"][:, j]
        else:
            if i == 0:
                MC["mva_score"] = bdt[1].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
            else:
                MC["mva_score"] = bdt[0].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))

            
    features = ak.to_numpy(MC_events[bdt_config["features"]])
    features = features.view((float, len(features.dtype.names)))
    bdt_score_0 = bdt[1].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
    bdt_score_1 = bdt[0].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))

    features = ak.to_numpy(data_events[bdt_config["features"]])
    features = features.view((float, len(features.dtype.names)))
    bdt_score_0_data = bdt[0].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))
    bdt_score_1_data = bdt[1].predict(xgboost.DMatrix(features, feature_names=bdt_config["features"]))

    if args.multiclass:
        for i in range(bdt_config["mva"]["param"]["num_class"]):
            labels_ = ["sig", "photon_bkg", "fake_bkg"]
            MC_events[f"mva_score_{labels_[i]}"] = ak.where(
                MC_events.event % 2 == 0,
                bdt_score_0[:, i],
                bdt_score_1[:, i]
            )
            data_events[f"mva_score_{labels_[i]}"] = ak.where(
                data_events.event % 2 == 0,
                bdt_score_0_data[:, i],
                bdt_score_1_data[:, i]
            )
        scores = [ak.singletons(MC_events[f"mva_score_{labels_[x]}"]) for x in range(bdt_config["mva"]["param"]["num_class"])]
        MC_events["mva_score"] = ak.concatenate(scores, axis=1)
        scores = [ak.singletons(data_events[f"mva_score_{labels_[x]}"]) for x in range(bdt_config["mva"]["param"]["num_class"])]
        data_events["mva_score"] = ak.concatenate(scores, axis=1)
        plot_confusion_matrix(MC_events, bdt_config, f"plots/{formatted_date}/confusion_matrix_{formatted_date}_multiclass.png")
    else:
        MC_events["mva_score"] = ak.where(
            MC_events.event % 2 == 0,
            bdt_score_0,
            bdt_score_1
        )

        data_events["mva_score"] = ak.where(
            data_events.event % 2 == 0,
            bdt_score_0_data,
            bdt_score_1_data
        )


    # Rescale the train QCD to its original weight
    # Here we go back to the correct normalisation for QCD and weight with negative sign
    var = "LeadPhoton_pt_mgg"
    var2 = "SubleadPhoton_pt_mgg"
    for i, MC in enumerate(MC_events_kfold):
            MC[events_train[i]]["weight"] = ak.where(
                        MC[events_train[i]].proc_id != -3,
                        MC[events_train[i]].weight,
                        MC[events_train[i]].weight * 30
                )
            sf = ceval["abs_to_nominal"].evaluate(MC[var], MC[var2])
            MC[events_train[i]]["weight"] = ak.where(
                        MC[events_train[i]]["label"] == 1,
                        MC[events_train[i]].weight / sf[events_train[i]],
                        MC[events_train[i]].weight
                )
            MC["square_weight"] = MC.weight ** 2
    # Here I add a branch that helps with erros in the histograms, there probably is a smarter way 
    MC_events["square_weight"] = MC_events.weight ** 2

    #bdt_score
    for i, MC in enumerate(MC_events_kfold):
        if args.multiclass:
            for l in labels_:
                fig, axs = plt.subplots(1, 1, figsize=(10, 10))
                var = f"mva_score_{l}"
                min_ = 0
                max_ = 1
                nbins = 50
                h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
                h_bdt_score_tot_err = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
                h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
                h_bdt_score_bg = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
                h_bdt_score_tot.fill(bdt_score_tot = MC[var], weight = MC.weight)
                h_bdt_score_tot_err.fill(bdt_score_tot = MC[var], weight = MC.square_weight)
                h_bdt_score_sig.fill(bdt_score_tot = MC[var][(MC.proc_id > 0)], weight = MC.weight[(MC.proc_id > 0)])
                h_bdt_score_bg.fill( bdt_score_tot = MC[var][(MC.proc_id < 0)], weight = MC.weight[(MC.proc_id < 0)])
                h_bdt_score_sig = h_bdt_score_sig * 300
                h_bdt_score_bg.project("bdt_score_tot").plot(ax=axs, label="bg_mc")
                h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal x 300")
                h_bdt_score_tot.project("bdt_score_tot").plot(ax=axs, color="green", label="tot_mc")
                axs.legend( prop={'size': 14})
                axs.grid(color='grey', linestyle='--', alpha=0.5)
                axs.set_ylabel('events')
                axs.set_xlabel('DiPhoton mva score', fontsize=14)
                axs.set_ylabel('events/0.02', fontsize=14)
                axs.tick_params(axis='x', labelsize=14)
                axs.tick_params(axis='y', labelsize=14)
                plt.plot()
        
                outname_ = f"plots/{formatted_date}/mva_score_{l}_bg_{formatted_date}_multiclass_fold_{i}.png"
                plt.savefig(outname_)
        else:
            fig, axs = plt.subplots(1, 1, figsize=(10, 10))
            var = "mva_score"
            min_ = 0
            max_ = 1
            nbins = 50
            h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
            h_bdt_score_tot_err = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
            h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
            h_bdt_score_bg = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
            h_bdt_score_tot.fill(bdt_score_tot = MC[var], weight = MC.weight)
            h_bdt_score_tot_err.fill(bdt_score_tot = MC[var], weight = MC.square_weight)
            h_bdt_score_sig.fill(bdt_score_tot = MC[var][(MC.proc_id > 0)], weight = MC.weight[(MC.proc_id > 0)])
            h_bdt_score_bg.fill( bdt_score_tot = MC[var][(MC.proc_id < 0)], weight = MC.weight[(MC.proc_id < 0)])
            h_bdt_score_sig = h_bdt_score_sig * 300
            h_bdt_score_bg.project("bdt_score_tot").plot(ax=axs, label="bg_mc")
            h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal x 300")
            h_bdt_score_tot.project("bdt_score_tot").plot(ax=axs, color="green", label="tot_mc")
            axs.legend( prop={'size': 14})
            axs.grid(color='grey', linestyle='--', alpha=0.5)
            axs.set_ylabel('events')
            axs.set_xlabel('DiPhoton mva score', fontsize=14)
            axs.set_ylabel('events/0.02', fontsize=14)
            axs.tick_params(axis='x', labelsize=14)
            axs.tick_params(axis='y', labelsize=14)
            plt.plot()
            outname_ = f"plots/{formatted_date}/mva_score_sig_bg_{formatted_date}_fold_{i}.png"
            plt.savefig(outname_)
        
        # Plot signal score with training weights
        fig, axs = plt.subplots(1,1, figsize=(10, 10))
        if args.multiclass:
            var = "mva_score_sig"
            for f in MC_events.fields:
                print(f)
        else:
            var = "mva_score"
        min_ = 0
        max_ = 1
        nbins = 50
        h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
        h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
        h_bdt_score_bg = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
        h_bdt_score_tot.fill(bdt_score_tot = MC[var], weight = scale_weights[i])
        h_bdt_score_sig.fill(bdt_score_tot = MC[var][(MC.proc_id == sig_label)], weight = scale_weights[i][(MC.proc_id == sig_label)])
        h_bdt_score_bg.fill( bdt_score_tot = MC[var][(MC.proc_id != sig_label)], weight = scale_weights[i][(MC.proc_id != sig_label)])
        # h_bdt_score_sig = h_bdt_score_sig * 300
        h_bdt_score_bg.project("bdt_score_tot").plot(ax=axs, label="bg_mc")
        h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal")
        h_bdt_score_tot.project("bdt_score_tot").plot(ax=axs, color="green", label="tot_mc")
        axs.legend( prop={'size': 14})
        axs.grid(color='grey', linestyle='--', alpha=0.5)
        axs.set_ylabel('events')
        axs.set_xlabel('DiPhoton mva score', fontsize=14)
        axs.set_ylabel('events/0.02', fontsize=14)
        axs.tick_params(axis='x', labelsize=14)
        axs.tick_params(axis='y', labelsize=14)
        plt.plot()
        
        if args.multiclass:
            outname_ = f"plots/{formatted_date}/mva_score_sig_bg_{formatted_date}_multiclass_fold_{i}_train_weight.png"
        else:
            outname_ = f"plots/{formatted_date}/mva_score_sig_bg_{formatted_date}_fold_{i}_train_weight.png"
        plt.savefig(outname_)

    #bdt_score
    fig, axs = plt.subplots(1,1, figsize=(10, 10))
    min_ = 100
    max_ = 180
    nbins = 80
    h_mass_tot = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_tot_err = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_sig = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_bg = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_tot.fill(bdt_score_tot = MC_events.CMS_hgg_mass, weight = MC_events.weight)
    h_mass_sig.fill(bdt_score_tot = MC_events.CMS_hgg_mass[MC_events.proc_id > 0], weight = MC_events.weight[MC_events.proc_id > 0])
    h_mass_bg.fill( bdt_score_tot = MC_events.CMS_hgg_mass[MC_events.proc_id < 0], weight = MC_events.weight[MC_events.proc_id < 0])
    h_mass_sig = h_mass_sig * 100
    h_mass_bg.project("bdt_score_tot").plot(ax=axs, label="bg_mc")
    h_mass_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal x 100")
    h_mass_tot.project("bdt_score_tot").plot(ax=axs, color="green", label="tot_mc")
    h_mass_data = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_mass_data.fill(bdt_score_tot=data_events.CMS_hgg_mass, weight=data_events.weight)
    bins_data, edges_data = h_mass_data.to_numpy()
    bins_err   = np.sqrt(bins_data)
    edges_data = np.resize(edges_data, nbins)
    edges_data = edges_data + np.abs((edges_data[1]-edges_data[0]))/2
    dump = np.logical_or((edges_data < 120),(edges_data > 130))
    axs.errorbar(edges_data[dump], bins_data[dump], yerr = bins_err[dump], color="black", marker="o", linestyle="", label="data")
    axs.legend( prop={'size': 14})
    axs.grid(color='grey', linestyle='--', alpha=0.5)
    axs.set_ylabel('events')
    axs.set_title('Diphoton mass', fontsize=14)
    axs.set_xlabel('Mgg [GeV]', fontsize=14)
    axs.set_ylabel('events/1 GeV', fontsize=14)
    axs.tick_params(axis='x', labelsize=14)
    axs.tick_params(axis='y', labelsize=14)
    plt.plot()
    if args.SAVE:
        if args.multiclass:
            outname_ = f"plots/{formatted_date}/mgg_sig_bg_{formatted_date}_multiclass.png"
        else:
            outname_ = f"plots/{formatted_date}/mgg_sig_bg_{formatted_date}.png"
        fig.savefig(outname_)


    fig, axs = plt.subplots(1,1, figsize=(10, 10))
    min_ = 100
    max_ = 180
    nbins = 80
    h_mass_tot = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_tot_err = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_sig = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_mass_bg = hist.Hist(hist.axis.Regular(bins=nbins,   start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    for i, MC in enumerate(MC_events_kfold):
        h_mass_tot.fill(bdt_score_tot = MC.CMS_hgg_mass, weight = MC.weight)
        h_mass_tot_err.fill(bdt_score_tot = MC.CMS_hgg_mass, weight = MC.square_weight)
        h_mass_sig.fill(bdt_score_tot = MC.CMS_hgg_mass[(MC.proc_id > 0)], weight = MC.weight[(MC.proc_id > 0)])
        h_mass_bg.fill( bdt_score_tot = MC.CMS_hgg_mass[(MC.proc_id < 0)], weight = MC.weight[(MC.proc_id < 0)])
    h_mass_sig = h_mass_sig * 100
    h_mass_bg.project("bdt_score_tot").plot(ax=axs, label="bg_mc")
    h_mass_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal x 100")
    h_mass_tot.project("bdt_score_tot").plot(ax=axs, color="green", label="tot_mc")
    h_mass_data = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_mass_data.fill(bdt_score_tot=data_events.CMS_hgg_mass, weight=data_events.weight)
    bins_data, edges_data = h_mass_data.to_numpy()
    bins_err   = np.sqrt(bins_data)
    edges_data = np.resize(edges_data, nbins)
    edges_data = edges_data + np.abs((edges_data[1]-edges_data[0]))/2
    dump = np.logical_or((edges_data < 120),(edges_data > 130))
    axs.errorbar(edges_data[dump], bins_data[dump], yerr = bins_err[dump], color="black", marker="o", linestyle="", label="data")
    axs.legend( prop={'size': 14})
    axs.grid(color='grey', linestyle='--', alpha=0.5)
    axs.set_ylabel('events')
    axs.set_title('Diphoton mass', fontsize=14)
    axs.set_xlabel('Mgg [GeV]', fontsize=14)
    axs.set_ylabel('events/1 GeV', fontsize=14)
    axs.tick_params(axis='x', labelsize=14)
    axs.tick_params(axis='y', labelsize=14)
    plt.plot()
    

    #bdt_score
    fig, axs = plt.subplots(1,1, figsize=(10, 10))
    min_ = 0
    max_ = 1
    nbins = 50
    if args.multiclass:
        var = "mva_score_sig"
        for f in MC_events.fields:
            print(f)
    else:
        var = "mva_score"
    LeadPhoton_et_ax  = hist.axis.Regular(nbins, min_, max_, flow=True, name="bdt_score_tot")
    LeadPhoton_et_cax = hist.axis.StrCategory(["ggh", "vbf", "vh", "tth", "nr_GG", "GJets", "QCD", "DY"], name="c")
    full_hist = hist.Hist(LeadPhoton_et_ax, LeadPhoton_et_cax)
    h_bdt_score_tot_err = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "bdt_score_tot", label = "tot"))
    h_bdt_score_tot = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    #for i, MC in enumerate(MC_events_kfold):
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 2)], weight=MC_events.weight[(MC_events.proc_id == 2)], c="ggh")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 3)], weight=MC_events.weight[(MC_events.proc_id == 3)], c="tth")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 4)], weight=MC_events.weight[(MC_events.proc_id == 4)], c="vbf")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == 5)], weight=MC_events.weight[(MC_events.proc_id == 5)], c="vh")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == -1)], weight=MC_events.weight[(MC_events.proc_id == -1)], c="nr_GG")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == -2)], weight=MC_events.weight[(MC_events.proc_id == -2)], c="GJets")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == -3)], weight=MC_events.weight[(MC_events.proc_id == -3)], c="QCD")
    full_hist.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id == -4)], weight=MC_events.weight[(MC_events.proc_id == -4)], c="DY")
    h_bdt_score_tot.fill(bdt_score_tot = MC_events[var], weight = MC_events.weight)
    h_bdt_score_tot_err.fill(bdt_score_tot = MC_events[var], weight = MC_events.square_weight)
    h_stack = full_hist.stack("c")
    h_stack[::-1].plot(ax=axs, stack=True, histtype="fill")
    h_bdt_score_sig = hist.Hist(hist.axis.Regular(bins=nbins, start=min_, stop=max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_sig.fill(bdt_score_tot = MC_events[var][(MC_events.proc_id > 0)], weight = MC_events.weight[(MC_events.proc_id > 0)])
    h_bdt_score_sig = h_bdt_score_sig * 300
    h_bdt_score_sig.project("bdt_score_tot").plot(ax=axs, color="red", label="signal x 300")
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
        
    h_bdt_score_data = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_data.fill(bdt_score_tot=data_events[var], weight=data_events.weight)
    bins_data, edges_data = h_bdt_score_data.to_numpy()
    bins_err   = np.sqrt(bins_data)
    edges_data = np.resize(edges_data, nbins)
    edges_data = edges_data + np.abs((edges_data[1] - edges_data[0]))/2
    dump = np.logical_or((edges_data < 120),(edges_data > 130))
    axs.errorbar(edges_data[dump], bins_data[dump], yerr = bins_err[dump], color="black", marker="o", linestyle="", label="data")
    axs.set_ylabel('events')
    axs.set_xlabel('DiPhoton mva score', fontsize=14)
    axs.set_ylabel('events/0.02', fontsize=14)
    axs.tick_params(axis='x', labelsize=14)
    axs.tick_params(axis='y', labelsize=14)
    plt.plot()
    
    if args.SAVE: 
        if args.multiclass:
            fig.savefig(f"plots/{formatted_date}/mva_score_sig_bg_stack_multiclass.png")
        else:
            fig.savefig(f"plots/{formatted_date}/mva_score_sig_bg_stack.png")

    with open(f"plot_dict.json", "r") as config_file:
        plot_config = json.load(config_file)
        
    for plot in plot_config:
        plot_variable_comparison(plot_config[plot], MC_events, data_events, formatted_date)

    # # Train and test overlay
    #bdt_score
    min_ = 0
    max_ = 1
    nbins = 50
    h_bdt_score_tot_train = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot_err_train = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_sig_train = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot_test = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot_err_test = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_sig_test = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot_val = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_tot_err_val = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    h_bdt_score_sig_val = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="bdt_score_tot", label="tot"))
    for i, MC in enumerate(MC_events_kfold):
        val = 1 if i == 0 else 0
        h_bdt_score_tot_train.fill(bdt_score_tot = MC_events_kfold[i][var][MC_events_kfold[i].train_split == 0], weight = MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 0]/sum(MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 0]))
        h_bdt_score_tot_err_train.fill(bdt_score_tot = MC_events_kfold[i][var][MC_events_kfold[i].train_split == 0], weight = (MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 0]/sum(MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 0]))**2)
        h_bdt_score_sig_train.fill(bdt_score_tot = MC_events_kfold[i][var][(MC_events_kfold[i].proc_id > 0) & (MC_events_kfold[i].train_split == 0)], weight = MC_events_kfold[i].weight[(MC_events_kfold[i].proc_id > 0) & (MC_events_kfold[i].train_split == 0)])
        h_bdt_score_tot_test.fill(bdt_score_tot = MC_events_kfold[i][var][MC_events_kfold[i].train_split == 1], weight = MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 1]/sum(MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 1]))
        h_bdt_score_tot_err_test.fill(bdt_score_tot = MC_events_kfold[i][var][MC_events_kfold[i].train_split == 1], weight = (MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 1]/sum(MC_events_kfold[i].weight[MC_events_kfold[i].train_split == 1]))**2)
        h_bdt_score_sig_test.fill(bdt_score_tot = MC_events_kfold[i][var][(MC_events_kfold[i].proc_id > 0) & (MC_events_kfold[i].train_split == 1)], weight = MC_events_kfold[i].weight[(MC_events_kfold[i].proc_id > 0) & (MC_events_kfold[i].train_split == 1)])
        h_bdt_score_tot_val.fill(bdt_score_tot = MC_events_kfold[val][var], weight=MC_events_kfold[val].weight/sum(MC_events_kfold[val].weight))
        h_bdt_score_tot_err_val.fill(bdt_score_tot = MC_events_kfold[val][var], weight=(MC_events_kfold[val].weight/sum(MC_events_kfold[val].weight))**2)
        h_bdt_score_sig_val.fill(bdt_score_tot = MC_events_kfold[val][var][(MC_events_kfold[val].proc_id > 0)], weight = MC_events_kfold[val].weight[(MC_events_kfold[val].proc_id > 0)])
        h_bdt_score_sig_train = h_bdt_score_sig * 300
    fig = plt.figure(figsize=(8, 8))
    ax0 = plt.subplot2grid((5, 3), (0, 0), rowspan=4, colspan=3)
    h_bdt_score_tot_train.project("bdt_score_tot").plot(ax=ax0, histtype="fill", color="red", alpha=0.4, label="training", linestyle="-", edgecolor="red")
    h_bdt_score_tot_test.project("bdt_score_tot").plot(ax=ax0, histtype="fill", linestyle="-", color="royalblue", alpha=0.4, label="test", edgecolor="royalblue")
    h_bdt_score_tot_val.project("bdt_score_tot").plot(ax=ax0, histtype="fill", linestyle="-", color="lawngreen", alpha=0.4, label="validation", edgecolor="lawngreen")
    #h_bdt_score_tot_val.project("bdt_score_tot").plot(ax=ax0, histtype="fill", alpha=0.3)
    #h_bdt_score_sig_train.project("bdt_score_tot").plot(ax=ax0, histtype="fill")
    #h_bdt_score_sig_train.project("bdt_score_tot").plot(ax=ax0, color="red", label="signal x 300")
    ax0.set_ylabel('events')
    ax0.set_title('DiPhoton ID mva score', fontsize=15)
    ax0.set_ylabel('events/0.02', fontsize=13)
    ax0.tick_params(axis='x', labelsize=10)
    ax0.tick_params(axis='y', labelsize=10)
    ax1 = plt.subplot2grid((5, 3), (4, 0), rowspan=1, colspan=3)
    mc["bins"]["train"] = h_bdt_score_tot_train.to_numpy()[0]
    mc["bins"]["test"] = h_bdt_score_tot_test.to_numpy()[0]
    mc["bins"]["val"] = h_bdt_score_tot_val.to_numpy()[0]
    mc["edges"]["train"] = h_bdt_score_tot_train.to_numpy()[1] + 0.01
    mc["edges"]["test"] = h_bdt_score_tot_test.to_numpy()[1] + 0.01
    mc["edges"]["val"] = h_bdt_score_tot_val.to_numpy()[1] + 0.01
    mc["errs"]["train"] = np.sqrt(h_bdt_score_tot_err_train.to_numpy()[0])
    mc["errs"]["test"] = np.sqrt(h_bdt_score_tot_err_test.to_numpy()[0])
    mc["errs"]["val"] = np.sqrt(h_bdt_score_tot_err_val.to_numpy()[0])
    #create up and down edges to plot shaded area for each bin
    yup = {}
    ydn = {}
    for set in ["train", "test", "val"]:
        ydn[set] = [mc["bins"][set][i] - x for i, x in enumerate(mc["errs"][set])]
        yup[set] = [mc["bins"][set][i] + x for i, x in enumerate(mc["errs"][set])]
    ax0.errorbar(mc["edges"]["train"][:-1], mc["bins"]["train"], yerr=mc["errs"]["train"], color="red", marker="_", linestyle="")
    ax0.errorbar(mc["edges"]["test"][:-1], mc["bins"]["test"], yerr=mc["errs"]["test"], color="royalblue", marker="_", linestyle="")
    ax0.errorbar(mc["edges"]["val"][:-1], mc["bins"]["val"], yerr=mc["errs"]["val"], color="lawngreen", marker="_", linestyle="")
    ax0.legend( prop={'size': 15})
    ax0.grid(color='grey', linestyle='--', alpha=0.5)
    ax1.grid(color='grey', linestyle='--', alpha=0.5)
    colors = ["red", "royalblue", "lawngreen"]
    for j, set in enumerate(["train", "test", "val"]):
        for i, x in enumerate(mc["edges"][set][:-1]):
            ax1.fill_between([x - 0.01, x + 0.01], [ydn[set][i]/mc["bins"]["train"][i], ydn[set][i]/mc["bins"]["train"][i]], [yup[set][i]/mc["bins"]["train"][i], yup[set][i]/mc["bins"]["train"][i]], facecolor=colors[j], alpha=0.3, edgecolor=colors[j], label="MC stat unc.")
    ax1.errorbar(mc["edges"]["train"][:-1], mc["bins"]["val"]/mc["bins"]["train"], yerr=abs(mc["errs"]["val"]/mc["bins"]["train"]), color="lawngreen", marker="+",linestyle="", label="training")
    ax1.errorbar(mc["edges"]["train"][:-1], mc["bins"]["train"]/mc["bins"]["train"], yerr=abs(mc["errs"]["train"]/mc["bins"]["train"]), color="red", marker="+",linestyle="", label="training")
    ax1.errorbar(mc["edges"]["train"][:-1], mc["bins"]["test"]/mc["bins"]["train"], yerr=abs(mc["errs"]["test"]/mc["bins"]["train"]), color="royalblue", marker="+",linestyle="", label="training")
    #ax1.fill_between(mc["edges"]["val"][:-1], mc["bins"]["val"]/mc["bins"]["train"]-mc["errs"]["val"]/mc["bins"]["train"], mc["bins"]["val"]/mc["bins"]["train"] + mc["errs"["val"]/mc["bins"]["train"], facecolor='lawngreen', alpha=0.4)
    #ax1.fill_between(mc["edges"]["train"][:-1], mc["bins"]["train"]/mc["bins"]["train"]-mc["errs"]["train"]/mc["bins"]["train"], mc["bins"]["train"]/mc["bins"]["train"] + m["errs"]["train"]/mc["bins"]["train"], facecolor='red', alpha=0.4)
    #ax1.fill_between(mc["edges"]["test"][:-1], mc["bins"]["test"]/mc["bins"]["train"]-mc["errs"]["test"]/mc["bins"]["train"], mc["bins"]["test"]/mc["bins"]["train"] + m["errs"]["test"]/mc["bins"]["train"], facecolor='royalblue', alpha=0.4)
    ax1.set_ylabel('ratio', fontsize=12)
    ax1.set_ylim([0.5,1.5])
    ax1.set_xlim([0,1])
    ax0.set_xlim([0,1])
    plt.tight_layout()
    if args.multiclass:
        plt.savefig(f"plots/{formatted_date}/mva_score_train_test_multiclass.png")
    else:
        plt.savefig(f"plots/{formatted_date}/mva_score_train_test.png")


if __name__ == '__main__':
    main()
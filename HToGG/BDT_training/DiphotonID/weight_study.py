import awkward
import xgboost
import numpy as np
import os
import json
import awkward as ak
import coffea.util as util
#%pip install sklearn
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from sklearn import preprocessing
from sklearn.metrics import roc_curve, auc,recall_score,precision_score
from copy import deepcopy

import math
import correctionlib
import correctionlib.schemav2 as cs
import rich
from optparse import OptionParser

import hist


proc_dict = {
    "cH_4FS_FXFX_M125_2017": {
        "file": "input/merged_signals/cH_4FS_FXFX_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "signal",
        "coffea": "input/ch_signal.coffea",
        "label": 1.,
        "proc_id": 1,
    },
    "ggh_M125_2017": {
        "file": "input/merged_signals/ggh_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "signal",
        "coffea": "input/signals.coffea",
        "label": 1.,
        "proc_id": 2,
    },
    "tth_M125_2017": {
        "file": "input/merged_signals/tth_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "signal",
        "coffea": "input/signals.coffea",
        "label": 1.,
        "proc_id": 3,
    },
    "vbf_M125_2017": {
        "file": "input/merged_signals/vbf_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "signal",
        "coffea": "input/signals.coffea",
        "label": 1.,
        "proc_id": 4,
    },
    "vh_M125_2017": {
        "file": "input/merged_signals/vh_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "signal",
        "coffea": "input/signals.coffea",
        "label": 1.,
        "proc_id": 5,
    },
    "DiphotonBox_low_mass_M125_2017": {
        "file": "input/merged_backgrounds/DiphotonBox_low_mass_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/backgrounds_DiphotonBox_low_mass_M125.coffea",
        "label": 0.,
        "proc_id": -1,
    },
    "DiphotonBox_high_mass_M125_2017": {
        "file": "input/merged_backgrounds/DiphotonBox_high_mass_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/backgrounds_DiphotonBox_high_mass_M125.coffea",
        "label": 0.,
        "proc_id": -1,
    },
    "GJets_HT-40To100_M125_2017": {
        "file": "input/merged_backgrounds/GJets_HT-40To100_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/background_GJets_HT40To200_M125.coffea",
        "label": 0.,
        "proc_id": -2,
    },
    "GJets_HT-100To200_M125_2017": {
        "file": "input/merged_backgrounds/GJets_HT-100To200_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/background_GJets_HT40To200_M125.coffea",
        "label": 0.,
        "proc_id": -2,
    },
    "GJets_HT-200To400_M125_2017": {
        "file": "input/merged_backgrounds/GJets_HT-200To400_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/background_GJets_HT-200To400_M125.coffea",
        "label": 0.,
        "proc_id": -2,
    },
    "GJets_HT-400To600_M125_2017": {
        "file": "input/merged_backgrounds/GJets_HT-400To600_M125_2017/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/background_GJets_HT-400To600_M125.coffea",
        "label": 0.,
        "proc_id": -2,
    },
    "QCD_M125_2017": {
        "file": "input/merged_backgrounds/QCD_M125_2017_syst_2/NOMINAL/UNTAGGED_merged.parquet",
        "type": "background",
        "coffea": "input/merged_backgrounds/QCD_M125_2017_syst_2/background_QCD_M125.coffea",
        "label": 0.,
        "proc_id": -3,
    },
    "DoubleEG_B_2017": {
        "file": "input/merged_data/DoubleEG_B_2017_UNTAGGED_merged.parquet",
        "type": "data",
        "coffea": "input/master-dev/data.coffea",
        "label": -1.,
        "proc_id": 0,
    },
    "DoubleEG_C_2017": {
        "file": "input/merged_data/DoubleEG_C_2017_UNTAGGED_merged.parquet",
        "type": "data",
        "coffea": "input/data.coffea",
        "label": -1.,
        "proc_id": 0,
    },
    "DoubleEG_D_2017": {
        "file": "input/merged_data/DoubleEG_D_2017_UNTAGGED_merged.parquet",
        "type": "data",
        "coffea": "input/master-dev/data.coffea",
        "label": -1.,
        "proc_id": 0,
    },
    "DoubleEG_E_2017": {
        "file": "input/merged_data/DoubleEG_E_2017_UNTAGGED_merged.parquet",
        "type": "data",
        "coffea": "input/master-dev/data.coffea",
        "label": -1.,
        "proc_id": 0,
    },
    "DoubleEG_F_2017": {
        "file": "input/merged_data/DoubleEG_F_2017_UNTAGGED_merged.parquet",
        "type": "data",
        "coffea": "input/master-dev/data.coffea",
        "label": -1.,
        "proc_id": 0,
    },
}

# concatenate the MC and Data events (separately) and add normalisation

with open(
        "/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/dev/higgs-dna-tiziano-bevilacqua/higgs_dna/metaconditions/cross_sections.json", "r"
    ) as pf:
        XSs = json.load(pf)

sig_coffea = util.load("input/master-dev/signals.coffea")
bkg_coffea = util.load("input/master-dev/backgrounds.coffea")
data_coffea = util.load("input/master-dev/data.coffea")
qcd_coffea = util.load("input/merged_backgrounds/QCD_M125_2017_syst_2/background_QCD_M125.coffea")

sig_events = []
bkg_events = []
data_events = []

# columns = ['weight', 'centralObjectWeight', 'bdt_score', 'dZ', 'CMS_hgg_mass', 'event', 'pt', 'eta', 'phi', 'n_jets', 'lead_jet_pt', 'lead_jet_eta', 'lead_jet_phi', 'lead_jet_mass', 'lead_jet_PN_CvL', 'lead_jet_PN_CvB', 'lead_jet_PN_B', 'lead_jet_btagDeepFlav_B', 'lead_jet_btagDeepFlav_CvB', 'lead_jet_btagDeepFlav_CvL', 'lead_jet_btagDeepFlav_QG', 'LeadPhoton_pt_mgg', 'LeadPhoton_eta', 'LeadPhoton_phi', 'LeadPhoton_mvaID', 'SubleadPhoton_pt_mgg', 'SubleadPhoton_eta', 'SubleadPhoton_phi', 'SubleadPhoton_mvaID', 'Diphoton_cos_dPhi', 'sigmaMrv', 'sigmaMwv', 'PV_score', 'PV_chi2', 'nPV', 'dZ_1', 'dZ_2', 'dZ_3']
columns = ['weight', 'dZ', 'CMS_hgg_mass', 'event', 'pt', 'eta', 'phi', 'LeadPhoton_pt_mgg', 'LeadPhoton_eta', 'LeadPhoton_phi', 'LeadPhoton_mvaID', 'SubleadPhoton_pt_mgg', 'SubleadPhoton_eta', 'SubleadPhoton_phi', 'SubleadPhoton_mvaID', 'Diphoton_cos_dPhi', 'sigmaMrv', 'sigmaMwv', 'PV_score', 'PV_chi2', 'nPV', 'dZ_1', 'dZ_2', 'dZ_3']
               
for i, dataset in enumerate(proc_dict):
    meta = util.load(proc_dict[dataset]["coffea"])
    if dataset == "QCD_M125_2017":
        # QCD is not added to the MC set of events
        print(dataset, ":)")
        norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"]["2017"] / meta["weight_sum"][XSs[dataset]["name"]]  * 1000
        qcd_events = ak.from_parquet(proc_dict[dataset]["file"], columns=columns)
        qcd_events["weight"] = qcd_events["weight"] * norm
        qcd_events["proc_id"] = ak.ones_like(qcd_events["weight"]) * proc_dict[dataset]["proc_id"]
        continue
    print(dataset)
    if proc_dict[dataset]["type"] == "signal":
        norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"]["2017"] / meta["weight_sum"][XSs[dataset]["name"]] * 1000
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
    
    elif proc_dict[dataset]["type"] == "background":
        norm = XSs[dataset]["xs"] * XSs[dataset]["bf"] * XSs["lumi"]["2017"] / meta["weight_sum"][XSs[dataset]["name"]]  * 1000
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
data_events["label"] = ak.ones_like(data_events["weight"]) * -1.

# read old qcd from samuel may's higgsdna
events = []
events = awkward.from_parquet("test_Data_2017_photon_cleaning/merged_nominal.parquet") 
events = awkward.values_astype(events, np.float64)
data   = events[events.process_id==0]
events = events[events.process_id>0]

qcd = events[(events.process_id == 7)]# & (abs(events.LeadPhoton_eta) <= 2.3) & (abs(events.SubleadPhoton_eta) <= 2.3)]
norm = ak.sum(qcd_events.weight) / ak.sum(qcd["weight_central"])
qcd["weight"] = qcd["weight_central"] * norm
qcd["square_weight"] = qcd["weight"] ** 2
qcd["CMS_hgg_mass"] = qcd["Diphoton_mass"]
qcd["pt"] = qcd["Diphoton_pt"]
qcd["eta"] = qcd["Diphoton_eta"]
qcd["phi"] = qcd["Diphoton_phi"]
qcd["dZ"] = ak.zeros_like(qcd["Diphoton_pt"])
qcd = qcd[columns]
qcd["label"] = ak.zeros_like(qcd["weight"])
qcd["proc_id"] = ak.ones_like(qcd["weight"]) * proc_dict["QCD_M125_2017"]["proc_id"]
bkg_events = ak.concatenate([bkg_events, qcd])

MC_events = ak.concatenate([sig_events, bkg_events])

# add VtxProbability 
MC_events["vtxProb"] = 2 * MC_events["sigmaMrv"] / (MC_events["sigmaMrv"] + MC_events["sigmaMwv"])
data_events["vtxProb"] = 2 * data_events["sigmaMrv"] / (data_events["sigmaMrv"] + data_events["sigmaMwv"])
MC_events = ak.values_astype(MC_events, np.float64)
data_events = ak.values_astype(data_events, np.float64)

MC_events_zero = deepcopy(MC_events)
MC_events_zero["weight"] = ak.where(
    MC_events.weight > 0,
    MC_events.weight,
    MC_events.weight * 0.
)

MC_events_abs = deepcopy(MC_events)
MC_events_abs["weight"] = abs(MC_events_abs["weight"])

MC_events["square_weight"] = MC_events["weight"] ** 2
MC_events_zero["square_weight"] = MC_events_zero["weight"] ** 2
MC_events_abs["square_weight"] = MC_events_abs["weight"] ** 2

# Signals lead and sublead pt/mgg scale factors

# cuts for mask in the plots 
signal_cut = (MC_events.proc_id > 0)
colors = ["red", "blue", "green"]

min_ = 0.
max_ = 1
nbins = 50
var = "LeadPhoton_pt_mgg"
var2 = "SubleadPhoton_pt_mgg"

# SF creation
dists = (
    hist.Hist.new
    .StrCat(["nominal", "zero"], name="dataset", growth=True)
    .Reg(bins=nbins, start=min_, stop=max_, name="lead", label="lead pt/mgg")
    .Reg(bins=nbins, start=min_, stop=max_, name="sublead", label="sublead pt/mgg")
    .Weight()
    .fill(
        dataset="nominal",
        lead=MC_events[var][signal_cut],
        sublead=MC_events[var2][signal_cut],
        weight=MC_events.weight[signal_cut]/sum(MC_events.weight[signal_cut])
    )
    .fill(
        dataset="zero",
        lead=MC_events_zero[var][signal_cut],
        sublead=MC_events_zero[var2][signal_cut],
        weight=MC_events_zero.weight[signal_cut]/sum(MC_events_zero.weight[signal_cut])
    )
    .fill(
        dataset="abs",
        lead=MC_events[var][signal_cut],
        sublead=MC_events[var2][signal_cut],
        weight=abs(MC_events.weight[signal_cut])/sum(abs(MC_events.weight[signal_cut]))
    )
)

# zero weight approach
num = dists["nominal", :, :].values()
den = dists["zero", :, :].values()
sf = np.where(
    (num > 0) & (den > 0),
    num / den,
    1.0,
)

fig, ax = plt.subplots()
# a quick way to plot the scale factor is to steal the axis definitions from the input histograms:
sfhist = hist.Hist(*dists.axes[1:], data=sf)
sfhist.plot2d()
fig.savefig(f"plots/weight_study_plots/SFs_lead_vs_sublead_ptomgg_zero.pdf")

den = dists["abs", :, :].values()
sf_abs = np.where(
    (num > 0) & (den > 0),
    num / den,
    1.0,
)

# a quick way to plot the scale factor is to steal the axis definitions from the input histograms:
fig, ax = plt.subplots()
sfhist_abs = hist.Hist(*dists.axes[1:], data=sf_abs)
sfhist_abs.plot2d()
fig.savefig(f"plots/weight_study_plots/SFs_lead_vs_sublead_ptomgg_abs.pdf")

import correctionlib.convert

# without a name, the resulting object will fail validation
sfhist.name = "zero_to_nominal"
sfhist.label = "reweighted"
zero_to_nominal = correctionlib.convert.from_histogram(sfhist)
zero_to_nominal.description = "Reweights zero wgt to agree with nominal"
# set overflow bins behavior (default is to raise an error when out of bounds)
zero_to_nominal.data.flow = "clamp"

# absolute value of the weights
sfhist_abs.name = "abs_to_nominal"
sfhist_abs.label = "reweighted"
abs_to_nominal = correctionlib.convert.from_histogram(sfhist_abs)
abs_to_nominal.description = "Reweights abs wgt to agree with nominal"
# set overflow bins behavior (default is to raise an error when out of bounds)
abs_to_nominal.data.flow = "clamp"

out_abs_to_nominal = cs.CorrectionSet(
    schema_version=2,
    description="abs_to_nominal",
    corrections=[
        abs_to_nominal,
    ],
)
out_zero_to_nominal = cs.CorrectionSet(
    schema_version=2,
    description="zero_to_nominal",
    corrections=[
        zero_to_nominal,
    ],
)

import gzip
with open("zero_to_nominal.json", "w") as fout:
    fout.write(out_zero_to_nominal.json(exclude_unset=True))

with gzip.open("zero_to_nominal.json.gz", "wt") as fout:
    fout.write(out_zero_to_nominal.json(exclude_unset=True))

with open("abs_to_nominal.json", "w") as fout:
    fout.write(out_abs_to_nominal.json(exclude_unset=True))

with gzip.open("abs_to_nominal.json.gz", "wt") as fout:
    fout.write(out_abs_to_nominal.json(exclude_unset=True))

dists.fill(
    dataset="zero reweighted",
    lead=MC_events_zero[var][signal_cut],
    sublead=MC_events_zero[var2][signal_cut],
    weight=MC_events_zero.weight[signal_cut]/sum(MC_events_zero.weight[signal_cut])*zero_to_nominal.to_evaluator().evaluate(MC_events_zero[var][signal_cut], MC_events_zero[var2][signal_cut])
)
dists.fill(
    dataset="abs reweighted",
    lead=MC_events[var][signal_cut],
    sublead=MC_events[var2][signal_cut],
    weight=abs(MC_events.weight[signal_cut])/sum(abs(MC_events.weight[signal_cut]))*abs_to_nominal.to_evaluator().evaluate(MC_events[var][signal_cut], MC_events[var2][signal_cut])
)


#################
# Plots #########
#################

plot_dict = {
    "LeadPhoton_pt_mgg": {
        "min": 0.,
        "max": 1.,
        "nbins": 50,
        "scale": "linear",
        "xlabel": "Lead Photon pT/mgg",
        "title": "Lead Photon pT/mgg"
    },
    "SubleadPhoton_pt_mgg": {
        "min": 0.,
        "max": 1.,
        "nbins": 50,
        "scale": "linear",
        "xlabel": "Sublead Photon pT/mgg",
        "title": "Sublead Photon pT/mgg"
    },
    "LeadPhoton_mvaID": {
        "min": -1.,
        "max": 1.,
        "nbins": 40,
        "scale": "linear",
        "xlabel": "Lead Photon mvaID",
        "title": "Lead Photon mvaID"
    },
    "SubleadPhoton_mvaID": {
        "min": -1.,
        "max": 1.,
        "nbins": 40,
        "scale": "linear",
        "xlabel": "Sublead Photon mvaID",
        "title": "Sublead Photon mvaID"
    },
    "LeadPhoton_eta": {
        "min": -3.,
        "max": 3.,
        "nbins": 60,
        "scale": "linear",
        "xlabel": "Lead Photon eta",
        "title": "Lead Photon eta"
    },
    "SubleadPhoton_eta": {
        "min": -3.,
        "max": 3.,
        "nbins": 60,
        "scale": "linear",
        "xlabel": "Sublead Photon eta",
        "title": "Sublead Photon eta"
    },
    "sigmaMrv": {
        "min": 0.,
        "max": 0.05,
        "nbins": 50,
        "scale": "linear",
        "xlabel": "Sigma M Right Vertex",
        "title": "Sigma M Right Vertex"
    },
    "sigmaMwv": {
        "min": 0.,
        "max": 0.05,
        "nbins": 50,
        "scale": "linear",
        "xlabel": "Sigma M Wrong Vertex",
        "title": "Sigma M Wrong Vertex"
    },
    "Diphoton_cos_dPhi": {
        "min": -1.,
        "max": 0.,
        "nbins": 50,
        "scale": "log",
        "xlabel": "Diphoton cos(DPhi)",
        "title": "Diphoton cos(DPhi)"
    },
}

# Uncorrected plots

for plot in plot_dict:
    print(f"plotting {plot}")
    fig = plt.figure(figsize=(9, 9))
    ax0 = plt.subplot2grid((5, 3), (0, 0), rowspan=4, colspan=3)

    var = plot
    min_ = plot_dict[plot]["min"]
    max_ = plot_dict[plot]["max"]
    nbins = plot_dict[plot]["nbins"]

    h = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "axs", label="nominal"))
    h_zero_wgt = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "axs", label="zero"))
    h_abs_wgt = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "axs", label="abs"))

    h.fill(axs = MC_events[var][signal_cut], weight = MC_events.weight[signal_cut]/sum(MC_events.weight[signal_cut]))
    h_zero_wgt.fill(axs = MC_events_zero[var][signal_cut], weight = MC_events_zero.weight[signal_cut]/sum(MC_events_zero.weight[signal_cut]))
    h_abs_wgt.fill(axs = MC_events_abs[var][signal_cut], weight = abs(MC_events_abs.weight[signal_cut])/sum(MC_events_abs.weight[signal_cut]))

    h.project("axs").plot(ax=ax0, color="red", label="nominal")
    h_abs_wgt.project("axs").plot(ax=ax0, color="blue", label="abs")
    h_zero_wgt.project("axs").plot(ax=ax0, color="green", label="zero")

    mc = {}
    mc["bins"] = {}
    mc["errs"] = {}
    mc["edges"] = {}

    # this is useful to manipulate bin content better when doing ratios and error plotting
    mc["bins"]["nominal"], mc["edges"]["nominal"] = h.to_numpy()
    mc["bins"]["zero"], mc["edges"]["zero"] = h_zero_wgt.to_numpy()
    mc["bins"]["abs"], mc["edges"]["abs"] = h_abs_wgt.to_numpy()
    half_bin = np.abs((mc["edges"]["nominal"][1] - mc["edges"]["nominal"][0])) / 2

    for hist_ in ["nominal", "zero", "abs"]:
        mc["edges"][hist_] = mc["edges"][hist_] + half_bin
        mc["errs"][hist_] = np.sqrt(mc["bins"][hist_])

    ax0.legend(prop={'size': 14})
    ax0.set_ylabel(f'events/{str(2 * half_bin)[:4]} GeV', fontsize=14)
    ax0.set_xlabel('', fontsize=1)
    ax0.set_title(plot_dict[plot]["title"], fontsize=12)
    ax0.set_yscale(plot_dict[plot]["scale"])
    ax0.grid(color='grey', linestyle='--', alpha=0.5)

    # ratio plot
    ax1 = plt.subplot2grid((5, 3), (4, 0), rowspan=1, colspan=3)
    ax1.grid(color='grey', linestyle='--', alpha=0.5)
    # orizontal line at 1
    ax1.plot(mc["edges"]["nominal"][:-1], ak.ones_like(mc["bins"]["nominal"]), color=colors[0], marker="_", linestyle="-", label="mc")

    ratio = {}

    for i, hist_ in enumerate(["abs", "zero"]):
        ratio[hist_] = ak.where(
            mc["bins"]["nominal"] != 0,
            mc["bins"][hist_] / mc["bins"]["nominal"],
            ak.ones_like(mc["bins"]["nominal"])
        )
        ax1.errorbar(mc["edges"]["nominal"][:-1], ratio[hist_], color=colors[i+1], marker="", linestyle="-", label=hist_)

    ax1.set_ylim([0.,2])
    ax1.set_xlim([min_, max_])
    ax0.set_xlim([min_, max_])
    ax1.set_xlabel(plot_dict[plot]["xlabel"], fontsize=12)
    ax1.set_ylabel('ratio', fontsize=14)

    plt.plot()
    fig.savefig(f"plots/weight_study_plots/uncorrected_{plot}.pdf")

# Corrected plots

for plot in plot_dict:
    print(f"plotting {plot}")
    fig = plt.figure(figsize=(9, 9))
    ax0 = plt.subplot2grid((5, 3), (0, 0), rowspan=4, colspan=3)

    var = plot
    min_ = plot_dict[plot]["min"]
    max_ = plot_dict[plot]["max"]
    nbins = plot_dict[plot]["nbins"]

    h = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "axs", label="nominal"))
    h_zero_wgt = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "axs", label="zero"))
    h_abs_wgt = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "axs", label="abs"))

    h.fill(axs = MC_events[var][signal_cut], weight = MC_events.weight[signal_cut]/sum(MC_events.weight[signal_cut]))
    h_zero_wgt.fill(axs = MC_events_zero[var][signal_cut], weight = MC_events_zero.weight[signal_cut]/sum(MC_events_zero.weight[signal_cut]) * zero_to_nominal.to_evaluator().evaluate(MC_events_zero["LeadPhoton_pt_mgg"][signal_cut], MC_events_zero["SubleadPhoton_pt_mgg"][signal_cut]))
    h_abs_wgt.fill(axs = MC_events_abs[var][signal_cut], weight = abs(MC_events_abs.weight[signal_cut])/sum(abs(MC_events_abs.weight[signal_cut])) * abs_to_nominal.to_evaluator().evaluate(MC_events_abs["LeadPhoton_pt_mgg"][signal_cut], MC_events_abs["SubleadPhoton_pt_mgg"][signal_cut]))

    h.project("axs").plot(ax=ax0, color="red", label="nominal")
    h_zero_wgt.project("axs").plot(ax=ax0, color="green", label="zero")
    h_abs_wgt.project("axs").plot(ax=ax0, color="blue", label="abs")

    mc = {}
    mc["bins"] = {}
    mc["errs"] = {}
    mc["edges"] = {}

    # this is useful to manipulate bin content better when doing ratios and error plotting
    mc["bins"]["nominal"], mc["edges"]["nominal"] = h.to_numpy()
    mc["bins"]["zero"], mc["edges"]["zero"] = h_zero_wgt.to_numpy()
    mc["bins"]["abs"], mc["edges"]["abs"] = h_abs_wgt.to_numpy()
    half_bin = np.abs((mc["edges"]["nominal"][1] - mc["edges"]["nominal"][0])) / 2

    for hist_ in ["nominal", "zero", "abs"]:
        mc["edges"][hist_] = mc["edges"][hist_] + half_bin
        mc["errs"][hist_] = np.sqrt(mc["bins"][hist_])

    ax0.legend(prop={'size': 14})
    ax0.set_ylabel(f'events/{str(2 * half_bin)[:4]} GeV', fontsize=14)
    ax0.set_xlabel('', fontsize=1)
    ax0.set_title(plot_dict[plot]["title"], fontsize=12)
    ax0.set_yscale(plot_dict[plot]["scale"])
    ax0.grid(color='grey', linestyle='--', alpha=0.5)

    # ratio plot
    ax1 = plt.subplot2grid((5, 3), (4, 0), rowspan=1, colspan=3)
    ax1.grid(color='grey', linestyle='--', alpha=0.5)
    # orizontal line at 1
    ax1.plot(mc["edges"]["nominal"][:-1], ak.ones_like(mc["bins"]["nominal"]), color=colors[0], marker="_", linestyle="-", label="mc")

    ratio = {}

    for i, hist_ in enumerate(["abs", "zero"]):
        ratio[hist_] = ak.where(
            mc["bins"]["nominal"] != 0,
            mc["bins"][hist_] / mc["bins"]["nominal"],
            ak.ones_like(mc["bins"]["nominal"])
        )
        ax1.errorbar(mc["edges"]["nominal"][:-1], ratio[hist_], color=colors[i+1], marker="", linestyle="-", label=hist_)

    ax1.set_ylim([0.,2])
    ax1.set_xlim([min_, max_])
    ax0.set_xlim([min_, max_])
    ax1.set_xlabel(plot_dict[plot]["xlabel"], fontsize=12)
    ax1.set_ylabel('ratio', fontsize=14)

    plt.plot()
    fig.savefig(f"plots/weight_study_plots/corrected_{plot}.pdf")
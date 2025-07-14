
import matplotlib.pyplot as plt
import numpy as np
import awkward as ak
from sklearn.metrics import roc_curve, auc, recall_score, precision_score, confusion_matrix
from sklearn.preprocessing import label_binarize
import xgboost
import seaborn as sns
import pickle

import hist
import mplhep as hep
from cycler import cycler
hep.style.use("CMS")
colors = plt.cm.get_cmap("tab10").colors  # or use "nipy_spectral", "turbo", etc.
plt.rcParams["axes.prop_cycle"] = cycler(color=colors)

def plot_confusion_matrix(MC_events, bdt_config, outname):

    y_val_class = MC_events["label"]
    predict_val_class = np.argmax(MC_events["mva_score"], axis=1)
    labels = ["sig", "dipho_NR", "fake"]

    cm = confusion_matrix(y_val_class, predict_val_class, normalize='true')

    # Plot the confusion matrix
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt='.2f', cmap='Blues', ax=ax)

    # Set axis labels and title
    ax.set_xlabel('Predicted Labels', fontsize=14)
    ax.set_ylabel('True Labels', fontsize=14)
    ax.set_xticks(np.arange(len(labels[:bdt_config["mva"]["param"]["num_class"]])) + 0.5)
    ax.set_yticks(np.arange(len(labels[:bdt_config["mva"]["param"]["num_class"]])) + 0.5)
    ax.set_xticklabels(labels[:bdt_config["mva"]["param"]["num_class"]], fontsize=14)
    ax.set_yticklabels(labels[:bdt_config["mva"]["param"]["num_class"]], fontsize=14)
    ax.set_title('Confusion Matrix', fontsize=14)
    plt.plot()

    plt.tight_layout()
    fig.savefig(outname)

def plot_ROC(test_mask, train_mask, labels, check_test, check_train, weights, bdt, outname):
    fpr, tpr, _ = roc_curve(labels[test_mask], check_test, sample_weight=abs(weights[test_mask]))
    fpr_train, tpr_train, _train = roc_curve(labels[train_mask], check_train, sample_weight=abs(weights[train_mask]))
    roc_auc = auc(fpr, tpr)
    roc_auc_train = auc(fpr_train, tpr_train)
    xgboost.plot_importance(bdt)
    lw = 2
    fig = plt.figure(figsize=(15,10))
    plt.plot(fpr, tpr, color='darkorange',
             lw=lw, label='ROC curve test (area = %0.3f)' % roc_auc)
    plt.plot(fpr_train, tpr_train, color='royalblue',
             lw=lw, label='ROC curve train (area = %0.3f)' % roc_auc_train)
    plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
    plt.xlim([-0.02, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=20)
    plt.ylabel('True Positive Rate', fontsize=20)
    plt.title('ROC curve', fontsize=30)
    plt.legend(loc="lower right", fontsize=20)
    plt.tick_params(axis='x', labelsize=20)
    plt.tick_params(axis='y', labelsize=20)
    
    #if not SAVE: 
    fig.savefig(outname)

def plot_ROC_multiclass(test_mask, train_mask, labels, check_test, check_train, weights, bdt, outname, bdt_config, plot_labels_):
    # Compute micro-average ROC curve and ROC area with true weights
    y_test_binarized = []
    y_train_binarized = []

    colors = ['orange', 'royalblue', 'crimson', 'brown', 'purple', 'olive']
    num_classes = bdt_config["mva"]["param"]["num_class"]

    bdt.feature_names = bdt_config["features"]
    xgboost.plot_importance(bdt)

    # Binarize the labels for multi-class ROC curve
    y_test_binarized = label_binarize(labels[test_mask], classes=range(num_classes))
    y_train_binarized = label_binarize(labels[train_mask], classes=range(num_classes))

    fpr_ = {}
    tpr_ = {}
    _ = {}
    roc_auc_ = {}
    fpr_train_ = {}
    tpr_train_ = {}
    _train_ = {}
    roc_auc_train_ = {}

    for j in range(num_classes):
        # Compute ROC curve and ROC area for each class
        fpr_[j], tpr_[j], _[j] = roc_curve(y_test_binarized[:, j], check_test[:, j], sample_weight=abs(weights[test_mask]))
        fpr_train_[j], tpr_train_[j], _train_[j] = roc_curve(y_train_binarized[:, j], check_train[:, j], sample_weight=abs(weights[train_mask]))
        roc_auc_[j] = auc(fpr_[j], tpr_[j])
        roc_auc_train_[j] = auc(fpr_train_[j], tpr_train_[j])

    fig = plt.figure(figsize=(9, 9))

    for j in range(num_classes):
        plt.plot(tpr_[j], fpr_[j], lw=2, color=colors[j], label=f'{plot_labels_[j]} test (AUC = {roc_auc_[j]:.2f})')
        plt.plot(tpr_train_[j], fpr_train_[j], "--", color=colors[j], lw=2, label=f'{plot_labels_[j]} train (AUC = {roc_auc_train_[j]:.2f})')

    # Plot diagonal line for reference (random classifier)
    plt.plot([0, 1], [0, 1], 'k--', lw=2)

    # Configure plot
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.ylabel('False Positive Rate', fontsize=14)
    plt.xlabel('True Positive Rate', fontsize=14)
    plt.title('Multi-Class ROC Curve', fontsize=18)
    plt.legend(loc='lower right', fontsize=14)
    plt.tick_params(axis='x', labelsize=14)
    plt.tick_params(axis='y', labelsize=14)
    plt.semilogy()
    plt.ylim(0.00001,1)
    plt.grid()

    # Show the plot
    fig.savefig(outname)

def extract_errors_and_bins(h_tot, h_tot_err, label, dict_):
    for f in ["bins", "edges", "errs", "half_bin", "ydn", "yup"]:
        if f not in dict_:
            dict_[f] = {}
    # the histograms contains the axes corresponding to the number of categories
    # here we want to project the histogram on the axis of the variable, getting the total amount of events
    tot = h_tot.project("ax")
    tot_err = h_tot_err.project("ax")
    dict_["bins"][label], dict_["edges"][label] = tot.to_numpy()
    dict_["half_bin"][label] = np.abs((dict_["edges"][label][1] - dict_["edges"][label][0])) / 2
    dict_["edges"][label] = dict_["edges"][label] + dict_["half_bin"][label]
    dict_["errs"][label] = np.sqrt(tot_err.to_numpy()[0])

    dict_["ydn"][label] = [dict_["bins"][label][i] - x for i, x in enumerate(dict_["errs"][label])]
    dict_["yup"][label] = [dict_["bins"][label][i] + x for i, x in enumerate(dict_["errs"][label])]

    return dict_

def plot_variable_comparison(config, MC_events, data_events, formatted_date, dump=Ellipsis):
    # extract configuration parameters
    fig_size = config["fig_size"]
    min_ = config["x_min"]
    max_ = config["x_max"]
    nbins = config["n_bins"]
    var = config["variable"]
    wgt = config["weight"]
    err_wgt = config["err_weight"]
    processes = config["processes"] # disctionary of processes {category: process_id}
    errors = config["errors"]
    fill = config["fill"]
    stack = config["stack"]
    
    if var not in MC_events.fields:
        print("skipping plot for variable", var, "not in MC_events")
        return

    print()
    print("-"*60)
    if (has_extra_dimension(MC_events[var])) and (var == "mva_score"):
        var = var + "_sig"
    print(f"    * Plotting {var} with {len(processes)} processes")
    
    # create the figure and axes
    fig = plt.figure(figsize=fig_size)
    ax0 = plt.subplot2grid((5, 3), (0, 0), rowspan=4, colspan=3)
    ax1 = plt.subplot2grid((5, 3), (4, 0), rowspan=1, colspan=3)

    # create the histograms
    # MC
    h_ax  = hist.axis.Regular(nbins, min_, max_, flow=True, name="ax")
    h_cax = hist.axis.StrCategory([*processes], name="c")
    h_cax_sig = hist.axis.StrCategory(["sig"], name="c")
    h_tot = hist.Hist(h_ax, h_cax)
    h_tot_err = hist.Hist(h_ax, h_cax)
    h_sig = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "ax", label = "sig"))
    h_bkg = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name = "ax", label = "bkg"))

    # create masks for signal, background etc
    if config["sig_vs_bkg"]:
        sig_mask = (MC_events.proc_id > 0)
        bkg_mask = (MC_events.proc_id < 0)
    if config["sidebands"]:
        SB_MC = (MC_events.CMS_hgg_mass > 135) | (MC_events.CMS_hgg_mass < 115)
        SB_DATA = (data_events.CMS_hgg_mass > 135) | (data_events.CMS_hgg_mass < 115)
    else:
        SB_MC = (MC_events.CMS_hgg_mass > 0)
        SB_DATA = (data_events.CMS_hgg_mass > 0)

    # fill the histograms with MC
    for cat, proc in processes.items():
        print(f"    * Filling {cat} with process {proc}")
        mask = MC_events.proc_id == proc
        h_tot.fill(ax = MC_events[var][(mask) & (SB_MC)], weight = MC_events[wgt][(mask) & (SB_MC)], c = cat)
        if errors:
            h_tot_err.fill(ax = MC_events[var][(mask) & (SB_MC)], weight = MC_events[err_wgt][(mask) & (SB_MC)], c = cat)
        if proc < 0:
            h_bkg.fill(ax = MC_events[var][(mask) & (SB_MC)], weight = MC_events[wgt][(mask) & (SB_MC)])
        elif proc > 0:
            print(f"    * Filling signal with process {proc}")
            h_sig.fill(ax = MC_events[var][(mask)], weight = MC_events[wgt][(mask)])

    if config["rescale_signal"]:
        print(f"")
        print(f"    * Rescaling signal by 100")
        print(f"")
        h_sig = h_sig * 100

    # DATA
    if config["data"]:
        # create and fill the histogram
        h_data = hist.Hist(hist.axis.Regular(bins = nbins, start = min_, stop = max_, name="ax", label="data"))
        h_data.fill(ax = data_events[var][SB_DATA], weight = data_events.weight[SB_DATA])
        # conversion to numpy because we want the scatter plot
        bins_data, edges_data = h_data.to_numpy()
        # error calculation
        bins_err = np.sqrt(bins_data)
        # eliminate last edge to have same size
        edges_data = np.resize(edges_data, nbins)
        # center the bins
        half_bin = np.abs((edges_data[1] - edges_data[0])) / 2
        edges_data = edges_data + half_bin
        # blind
        if config["blind"]:
            dump = np.logical_or((edges_data < 120), (edges_data > 130))
        else:
            dump = ak.ones_like(edges_data, dtype=bool)

    # create a stack and plot it
    h_stack = h_tot.stack("c")
    h_stack[::-1].plot(ax = ax0, stack = stack, histtype=fill)
    if config["sig_vs_bkg"]:
        h_sig.project("ax").plot(ax = ax0, color = "red", label = "signal x 100")

    # extract errors and bins
    mc = {}
    mc = extract_errors_and_bins(h_tot, h_tot_err, "tot", mc)

    # plot shaded area for MC errors
    for i, x in enumerate(mc["edges"]["tot"][:-1]):
        if i == 0:
            ax0.fill_between([x - mc["half_bin"]["tot"], x + mc["half_bin"]["tot"]], [mc["ydn"]["tot"][i], mc["ydn"]["tot"][i]], [mc["yup"]["tot"][i], mc["yup"]["tot"][i]], facecolor='grey', alpha=0.5, edgecolor='grey', label="MC stat unc.") # we want just one entry in the legend
        else:
            ax0.fill_between([x - mc["half_bin"]["tot"], x + mc["half_bin"]["tot"]], [mc["ydn"]["tot"][i], mc["ydn"]["tot"][i]], [mc["yup"]["tot"][i], mc["yup"]["tot"][i]], facecolor='grey', alpha=0.5, edgecolor='grey', label="")
    
    if config["data"]:
        # plot data
        ax0.errorbar(edges_data[dump], bins_data[dump], yerr = bins_err[dump], color="black", marker="o", linestyle="", label="data")

    if config["ratio"]:
        # ratio plot
        ax1.plot(mc["edges"]["tot"][:-1], ak.ones_like(mc["bins"]["tot"]), color="grey", marker="_", linestyle="", label="mc")
        for i, x in enumerate(mc["edges"]["tot"][:-1]):
            ax1.fill_between(
                [x - mc["half_bin"]["tot"], x + mc["half_bin"]["tot"]],
                [mc["ydn"]["tot"][i] / mc["bins"]["tot"][i], mc["ydn"]["tot"][i] / mc["bins"]["tot"][i]],
                [mc["yup"]["tot"][i] / mc["bins"]["tot"][i], mc["yup"]["tot"][i] / mc["bins"]["tot"][i]],
                facecolor='grey', alpha=0.5, edgecolor='grey', label="MC stat unc."
            )
        if config["data"]:
            ax1.errorbar(edges_data[dump], bins_data[dump] / mc["bins"]["tot"][dump], yerr = bins_err[dump] / mc["bins"]["tot"][dump], color="black", marker="o", linestyle="", label="data")

    # cosmetics

    ax0.legend(prop = {'size': 14})
    ax0.grid(color = 'grey', linestyle = '--', alpha = 0.5)
    ax1.grid(color = 'grey', linestyle = '--', alpha = 0.5)

    ax0.tick_params(axis = 'x', labelsize = 12)
    ax1.tick_params(axis = 'x', labelsize = 12)
    ax0.tick_params(axis = 'y', labelsize = 12)
    ax1.tick_params(axis = 'y', labelsize = 12)

    ax0.set_title(config["title"], fontsize=16)
    ax0.set_ylabel(config.get("ylabel", f'events/{(2 * mc["half_bin"]["tot"]):.2f}'), fontsize=16)
    ax1.set_xlabel(config.get("xlabel", 'var'), fontsize=16)
    ax0.set_xlabel('', fontsize=1)
    ax1.set_ylim(config.get("ratio_ylim", [0, 2]))
    ax1.set_xlim(config.get("xlim", [min_, max_]))
    ax0.set_xlim(config.get("xlim", [min_, max_]))
    plt.tight_layout()

    output_path = config.get("output_path", f"plots/{var}_{formatted_date}.png")
    output_path = output_path.format(formatted_date=formatted_date)
    print(f"    * Saving plot to {output_path}")
    plt.savefig(output_path)

    with open(output_path.replace(".png", ".pkl"), "wb") as f:
        pickle.dump(fig, f)

def has_extra_dimension(arr):
    try:
        # Try to get number of elements along axis=1
        ak.num(arr, axis=1)
        return True
    except ValueError:
        return False
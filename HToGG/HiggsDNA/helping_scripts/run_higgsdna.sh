#!/bin/bash


# Input directory
input_runner=$1
# Destination directory
destination=$2

# executor
if [[ ${4} == "DEBUG" ]]; then 
    executor="iterative"
    limit="--limit 1"
    echo ! DEBUG mode !, limit = 1 and iterative execution
else
    executor="dask/slurm"
    limit=""
fi
# year tag
year=$3

# List of subdirectories
if [[ ${year} == "2017" ]]; then
    echo "-------------------------------------------------------------------------------------------------------"
    echo "You have selected to run with 2017 samples"
    echo
    configs=(
        #"config_jsons/filesets/Backgrounds/DiphotonNR_samples_2017.json"
        #"config_jsons/filesets/Backgrounds/GJets200-400_samples_2017.json"
        #"config_jsons/filesets/Backgrounds/GJets400-600_samples_2017.json"
        #"config_jsons/filesets/Backgrounds/GJets600-Inf_samples_2017.json"
        #"config_jsons/filesets/Backgrounds/GJets40-200_samples_2017.json"
        #"config_jsons/filesets/Backgrounds/QCD_samples_2017.json"
        #"config_jsons/filesets/TH_bkg_samples.json"
        #"config_jsons/filesets/HpC_signal_samples.json"
        #"config_jsons/filesets/Data_2017_v11.json"
        #"config_jsons/filesets/Backgrounds/DY_samples_2017.json"
        #"config_jsons/filesets/FS_unc/Unc_cH_2017.json"
        "config_jsons/filesets/FS_unc/Unc_bH_2017.json"
    )
    trigger=".*DoubleEG.*"
    prefix=higgs_dna_HpC
elif [[ ${year} == "2017_TnP" ]]; then
    echo "-------------------------------------------------------------------------------------------------------"
    echo "You have selected to run with 2017 samples and TnP workflow"
    echo
    configs=(
        #"config_jsons/filesets/Backgrounds/DY_samples_2017.json"
        "config_jsons/filesets/TTTo2L2Nu_samples_2017.json"
        #"config_jsons/filesets/ttH_samples_2017.json"
        #"config_jsons/filesets/DY_pt1_2017.json"
        #"config_jsons/filesets/DY_pt2_2017.json"
        #"config_jsons/filesets/Data_2017_v11.json"
    )
    trigger=".*SingleEle.*"
    prefix=TnP_HpC
elif [[ ${year} == "2018" ]]; then
    echo "-------------------------------------------------------------------------------------------------------"
    echo "You have selected to run with 2018 samples"
    echo
    configs=(
        # "config_jsons/filesets/Backgrounds/DiphotonNR_samples_2018.json"
        # "config_jsons/filesets/Backgrounds/GJets200-400_samples_2018.json"
        # "config_jsons/filesets/Backgrounds/GJets400-Inf_samples_2018.json"
        # "config_jsons/filesets/Backgrounds/GJets40-200_samples_2018.json"
        # "config_jsons/filesets/Backgrounds/QCD_samples_2018.json"
        # "config_jsons/filesets/HpC_signal_samples_2018.json"
        # "config_jsons/filesets/TH_bkg_samples_2018.json"
        # "config_jsons/filesets/Data_BC_2018_v13.json"
        # "config_jsons/filesets/Data_2018D_v13.json"
        # "config_jsons/filesets/Data_2018D_v13.json"
        # "config_jsons/filesets/Backgrounds/DY_samples_2018.json"
        "config_jsons/filesets/FS_unc/Unc_cH_2018.json"
        "config_jsons/filesets/FS_unc/Unc_bH_2018.json"
    )
    trigger=".*EGamma.*2018.*"
    prefix=higgs_dna_HpC
elif [[ ${year} == "2016pre" ]]; then
    echo "-------------------------------------------------------------------------------------------------------"
    echo "You have selected to run with 2016 pre VFP samples"
    echo
    configs=(
        #"config_jsons/filesets/2016/DiphotonNR_2016pre.json"
        #"config_jsons/filesets/2016/GJets_200_400_2016pre.json"
        #"config_jsons/filesets/2016/GJets_400_Inf_2016pre.json"
        #"config_jsons/filesets/2016/GJets_40_200_2016pre.json"
        #"config_jsons/filesets/2016/QCD_2016pre.json"
        #"config_jsons/filesets/2016/HpC_signal_samples_2016pre.json"
        "config_jsons/filesets/TH_bkg_samples_2016pre.json"
        #"config_jsons/filesets/2016/DoubleEG_samples_2016pre.json"
        #"config_jsons/filesets/2016/DY_2016pre.json"
        #"config_jsons/filesets/FS_unc/Unc_cH_2016_pre.json"
        #"config_jsons/filesets/FS_unc/Unc_bH_2016pre.json"
    )
    trigger=".*DoubleEG.*"
    prefix=higgs_dna_HpC
elif [[ ${year} == "2016post" ]]; then
    echo "-------------------------------------------------------------------------------------------------------"
    echo "You have selected to run with 2016 post VFP samples"
    echo
    configs=(
        #"config_jsons/filesets/2016/DiphotonNR_2016post.json"
        #"config_jsons/filesets/2016/GJets_200_400_2016post.json"
        #"config_jsons/filesets/2016/GJets_400_Inf_2016post.json"
        #"config_jsons/filesets/2016/GJets_40_200_2016post.json"
        #"config_jsons/filesets/2016/QCD_2016post.json"
        #"config_jsons/filesets/2016/HpC_signal_samples_2016post.json"
        "config_jsons/filesets/TH_bkg_samples_2016post.json"
        #"config_jsons/filesets/2016/DoubleEG_samples_2016post.json"
        #"config_jsons/filesets/2016/DY_2016post_wrong.json"
        #"config_jsons/filesets/FS_unc/Unc_cH_2016_post.json"
        #"config_jsons/filesets/FS_unc/Unc_bH_2016post.json"
    )
    trigger=".*DoubleEG.*"
    prefix=higgs_dna_HpC
else
    configs=()
    echo "-------------------------------------------------------------------------------------------------------"
    echo "You have not selected any available year [2016pre, 2016post, 2017, 2018]"
    echo
fi 



higgsdna_dir="/work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master_240821/higgs-dna-tiziano-bevilacqua"
# Loop through each subdirectory
for config in "${configs[@]}"; do 
    if [ -d "${destination}" ]; then
        # Extract the base filename from the config path (e.g., "DiphotonNR_samples_2017.json")
        base_filename=$(basename "$config")
        # Remove the ".json" extension to get "DiphotonNR_samples_2017"
        base_filename_no_ext="${base_filename%.json}"
        # Create the output directory with the last part of the config path
        output_dir="${destination}/${prefix}_${base_filename_no_ext}"
        # Check if the subdirectory exists
        if [ -e "$higgsdna_dir/${config}" ]; then
            echo "-------------------------------------------------------------------------------------------------------"
            echo "will run HiggsDNA with the following fileset: ${config}"
            echo "     and the following runner: ${input_runner}"
            echo
            cat $input_runner | sed "s;SAMPLE_JSON;\"${higgsdna_dir}/${config}\";g;" > tmp_run
            run_analysis.py --json-analysis tmp_run -d $output_dir --analysis mainAnalysis --executor $executor -j 1 -m 25GB -s 2 --max-scaleout 80 --chunk 150000 --skipJetVetoMap --fiducialCuts simple --wall 08:00:00 --triggerGroup $trigger $limit --skipbadfiles --walltime 11:59:00 # --skipCQR 

        else
            echo "failed to locate fileset: ${config}"
        fi
    else
        echo "failed to locate output directory: ${destination}"
    fi
done

echo "The full production was run."

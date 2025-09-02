#!/bin/bash
#SBATCH --job-name=run_analysis
#SBATCH --output=/work/bevila_t/test/.slurm/run_analysis_%j.out
#SBATCH --error=/work/bevila_t/test/.slurm/run_analysis_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=10G
#SBATCH --partition=standard

# Load required modules (edit these according to your environment)
echo activating conda
. "/work/bevila_t/MINICONDA3/envs/higgs-dna/etc/profile.d/conda.sh"
conda activate higgs-dna-merge 
echo conda activated

cd /work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master_merge_250211/higgs-dna-tiziano-bevilacqua

# Optional: Create logs directory
mkdir -p logs

output=$1
fiducialCuts=$2
if [ $3 == "CQR" ]; then
  applyCQR="--applyCQR"
else
  applyCQR=""
fi
echo ${output}

# Run the command
command="higgs_dna/scripts/run_analysis.py \
  --json-analysis /work/bevila_t/HpC_Analysis/HiggsDNA/coffea/myfork/master_merge_250211/higgs-dna-tiziano-bevilacqua/runner_ggH.json \
  -d output/${output} \
  --analysis mainAnalysis \
  --executor dask/slurm \
  -j 1 \
  -m 25GB \
  -s 2 \
  --max-scaleout 40 \
  --chunk 100000 \
  --triggerGroup ".*DoubleEG.*" \
  --skipJetVetoMap \
  --fiducialCuts ${fiducialCuts} \
  --walltime 11:59:00 \
  --nano-version 11 \
  ${applyCQR}"

echo $command

python3 $command

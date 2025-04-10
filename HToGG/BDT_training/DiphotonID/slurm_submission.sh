#!/bin/bash
#SBATCH --job-name=run_diphoton_bdt_training
#SBATCH --output=/work/bevila_t/test/.slurm/run_diphoton_bdt_training_%j.out
#SBATCH --error=/work/bevila_t/test/.slurm/run_diphoton_bdt_training_%j.err
#SBATCH --time=12:00:00
#SBATCH --mem=30G
#SBATCH --cpus-per-task=8
#SBATCH --partition=standard

SLURM_JOB_NAME="diphoton_BDT_training"
# Load required modules (edit these according to your environment)
echo activating conda
. "/work/bevila_t/MINICONDA3/envs/higgs-dna/etc/profile.d/conda.sh"
conda activate higgs-dna-merge 
echo conda activated

echo
echo "--------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------"
echo "                          Creating JOB ["BDT_Opt"]"
echo

USERDIR=/work/bevila_t/HpC_Analysis/DiphotonMVA_training
python_script=$1
ARGS=$2

echo executing ${USERDIR}/${python_script} ${ARGS}
python3 ${USERDIR}/${python_script} ${ARGS}

echo
echo "--------------------------------------------------------------------------------"
echo "                                  JOB ["BDT_Opt"] Finished"
echo

# Copy to pnfs
if [[ ${USERDIR} == /pnfs/* ]]; then
    xrdcp -f -N /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out root://t3dcachedb.psi.ch:1094/$USERDIR/logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out
    xrdcp -f -N /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.err root://t3dcachedb.psi.ch:1094/$USERDIR/logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.err
    echo "logs copied..."
    if [ ! -f ${USERDIR}/${step}_cfg.py ]; then
        xrdcp -f -N ${step}_cfg.py ${USERDIR}/${step}_cfg.py
    fi
else
    cp  /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out $USERDIR/logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.out
    cp  /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.err $USERDIR/logs/${SLURM_JOB_NAME}_${SLURM_JOB_ID}.err
    echo "logs copied..."
fi

echo
echo "Output: "
ls -l $USERDIR

echo
echo "--------------------------------------------------------------------------------"
echo "                                 JOB ["BDT_Opt"] DONE"
echo "--------------------------------------------------------------------------------"
echo "--------------------------------------------------------------------------------"

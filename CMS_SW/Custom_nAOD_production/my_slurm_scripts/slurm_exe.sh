#!/bin/bash -e
#SBATCH --account=t3
#SBATCH --partition=standard
#SBATCH --job-name=EGamma_Run2018A
#SBATCH --cpus-per-task=1
#SBATCH --mem=1G
#SBATCH --time=01:00:00
#SBATCH --nodes=1
#SBATCH -o /work/%u/test/.slurm/%x_%A_%a.out
#SBATCH -e /work/%u/test/.slurm/%x_%A_%a.err

echo "------------------------------------------------------------"
echo "[`date`] Job started"
echo "------------------------------------------------------------"
DATE_START=`date +%s`

echo HOSTNAME: ${HOSTNAME}
echo HOME: ${HOME}
echo USER: ${USER}
echo X509_USER_PROXY: ${X509_USER_PROXY}
echo CMD-LINE ARGS: $@

if [ -z ${SLURM_ARRAY_TASK_ID} ]; then
  printf "%s\n" "Environment variable \"SLURM_ARRAY_TASK_ID\" is not defined. Job will be stopped." 1>&2
  exit 1
fi

# define SLURM_JOB_NAME and SLURM_ARRAY_JOB_ID, if they are not defined already (e.g. if script is executed locally)
[ ! -z ${SLURM_JOB_NAME} ] || SLURM_JOB_NAME=EGamma_Run2018A
[ ! -z ${SLURM_ARRAY_JOB_ID} ] || SLURM_ARRAY_JOB_ID=local$(date +%y%m%d%H%M%S)

echo SLURM_JOB_NAME: ${SLURM_JOB_NAME}
echo SLURM_JOB_ID: ${SLURM_JOB_ID}
echo SLURM_ARRAY_JOB_ID: ${SLURM_ARRAY_JOB_ID}
echo SLURM_ARRAY_TASK_ID: ${SLURM_ARRAY_TASK_ID}

OUTPUT_DIR=/pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/job_$(printf "%04d" ${SLURM_ARRAY_TASK_ID})
echo OUTPUT_DIR: ${OUTPUT_DIR}

[ ! -f ${OUTPUT_DIR}/flag.done ] || exit 0

if [ ! -f ${X509_USER_PROXY} ]; then
  printf "%s\n" "Authentication failed, invalid path to grid-certificate proxy: ${X509_USER_PROXY}" 1>&2
  exit 1
fi

# load CMSSW environment
cd /work/bevila_t/HpC_Analysis/CMSSW_10_6_18/src/XPlusCharmAnalysis/HPlusCharm/test/macros/SLURM_TEST_NAOD/tmp_cmssw/CMSSW_10_6_26_EGamma_Run2018A_NANOAOD/src
eval `scram runtime -sh`

# local /scratch dir to be used by the job
TMPDIR=/scratch/${USER}/slurm/${SLURM_JOB_NAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}
echo TMPDIR: ${TMPDIR}
mkdir -p ${TMPDIR}
cd ${TMPDIR}

if [ ${SLURM_ARRAY_TASK_ID} -eq 0 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=79114 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/006AA924-0DDF-DB4F-B68D-D9A6B4075AF2.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 1 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=80447 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/008BFC28-3BE7-1C42-953D-E8F24CDAD155.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 2 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=117527 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/01039813-905F-D146-B17A-546523061BB6.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 3 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=83199 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/0168DB79-0B8F-2B4F-AFDC-320F680F2BA5.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 4 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=68649 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/01768959-BBAC-0D43-A9C8-5AC0FEF2EA92.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 5 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=73195 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/0182C6C6-4E0E-7C44-8DEC-B217530DBA11.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 6 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=79169 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/01BA82E7-5451-0C48-A073-3F7007BBBC01.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 7 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=78354 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/01BCC1E7-C0DD-474E-83EA-FCCF84729121.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 8 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=78446 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/01D393B4-8E0B-C548-B13F-3CD03B2A9E0C.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 9 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=65084 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/022FB69F-C040-B742-8EE8-C1557B9FC169.root

elif [ ${SLURM_ARRAY_TASK_ID} -eq 10 ]; then
  cmsRun /pnfs/psi.ch/cms/trivcat/store/user/bevila_t/test2/phys/xpluscharm/Out_nAODs/NEW/2018/Data/EGamma/EGamma_Run2018A/NANOAOD_configDump.py \
  maxEvents=65927 \
  skipEvents=0 \
  inputFiles=/store/data/Run2018A/EGamma/MINIAOD/15Feb2022_UL2018-v1/2430000/02905218-91CE-C942-9E7B-2ED31C90C6F5.root


else
  printf "%s\n" "Invalid value for SLURM_ARRAY_TASK_ID: ${SLURM_ARRAY_TASK_ID}"
fi

touch ${TMPDIR}/flag.done

if [ ! -d ${OUTPUT_DIR}/logs ]; then
  if [[ ${OUTPUT_DIR} == /pnfs/* ]]; then
  (
    (! command -v scram &> /dev/null) || eval `scram unsetenv -sh`
    gfal-mkdir -p root://t3dcachedb.psi.ch:1094/${OUTPUT_DIR}/logs
    sleep 5
  )
  else
    mkdir -p ${OUTPUT_DIR}/logs
  fi
fi

for tmpf in /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.{out,err}; do
  [ -f ${tmpf} ] || continue # stdout/err outputs not produced if running locally
  if [[ ${OUTPUT_DIR} == /pnfs/* ]]; then
    xrdcp -f -N ${tmpf} root://t3dcachedb.psi.ch:1094//${OUTPUT_DIR}/logs
  else
    cp ${tmpf} ${OUTPUT_DIR}/logs
  fi
  printf "%s\n" "> output file copied: ${tmpf} -> ${OUTPUT_DIR}/logs"
done

for tmpf in ${TMPDIR}/*.root ${TMPDIR}/flag.done; do
  if [[ ${OUTPUT_DIR} == /pnfs/* ]]; then
    xrdcp -f -N ${tmpf} root://t3dcachedb.psi.ch:1094//${OUTPUT_DIR}
  else
    cp ${tmpf} ${OUTPUT_DIR}
  fi
  printf "%s\n" "> output file copied: ${tmpf} -> ${OUTPUT_DIR}"
done

# removal of temporary working dir when job is completed
rm -rf ${TMPDIR}

echo "------------------------------------------------------------"
echo "[`date`] Job completed successfully"
DATE_END=`date +%s`
runtime=$((DATE_END-DATE_START))
echo "[`date`] Elapsed time: ${runtime} sec"
echo "------------------------------------------------------------"

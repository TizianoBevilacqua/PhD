#!/bin/bash -ex

if [ $# -ne 1 ]; then
  printf "%s\n" ">> ERROR -- specify 1 cmd-line arg: path to output directory"
  exit 1
fi

BASE_DIR="${CMSSW_BASE}"/src/XPlusCharmAnalysis/HPlusCharm/test/MadGraph5_aMCatNLO
OUT_DIR="${1}"

if [ -d "${OUT_DIR}" ]; then
  printf "%s\n" ">> ERROR -- target output directory already exists: ${OUT_DIR}"
  exit 1
fi

## list of MinBias SIM files for PU mixing:
## - DAS sample needs to match MC scenario used in wf config (see -w below)
## - restricted to files available at a T2
#dasgoclient -query "file dataset=/MinBias_TuneCP5_13TeV-pythia8/RunIISummer19UL18SIM-106X_upgrade2018_realistic_v4-v1/SIM site=T2_TR_METU" \
#  > "${BASE_DIR}"/.MinBias_RunIISummer19UL18SIM_SIM.txt

# loop over MC samples to be produced
SAMPLE_TAGS=(
  #HPlusCharm_3FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13TeV_amcatnlo_pythia8
  #HPlusCharm_3FS_MuRFScaleDynX0p50_HToZZTo4L_M125_TuneCP5_13TeV_amcatnlo_JHUGenV7011_pythia8
  #HPlusCharm_4FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13TeV_amcatnlo_pythia8
  HPlusCharm_4FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13p6TeV_amcatnloFXFX_pythia8
  #HPlusCharm_4FS_MuRFScaleDynX0p50_HToZZTo4L_M125_TuneCP5_13TeV_amcatnlo_JHUGenV7011_pythia8
  #HPlusCharm_4FS_MuRFScaleDynX0p50_HToZZTo4L_M125_TuneCP5_13TeV_amcatnloFXFX_JHUGenV7011_pythia8

  #HPlusBottom_4FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13TeV_amcatnlo_pythia8
  #HPlusBottom_4FS_MuRFScaleDynX0p50_HToZZTo4L_M125_TuneCP5_13TeV_amcatnlo_JHUGenV7011_pythia8
  #HPlusBottom_5FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13TeV_amcatnlo_pythia8
  #HPlusBottom_5FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13TeV_amcatnloFXFX_pythia8
  #HPlusBottom_5FS_MuRFScaleDynX0p50_HToZZTo4L_M125_TuneCP5_13TeV_amcatnlo_JHUGenV7011_pythia8
  #HPlusBottom_5FS_MuRFScaleDynX0p50_HToZZTo4L_M125_TuneCP5_13TeV_amcatnloFXFX_JHUGenV7011_pythia8
)

for sampleTag_i in "${SAMPLE_TAGS[@]}"; do

  NUM_EVENTS=1000

  JSON="${sampleTag_i}"_workflows_23.json

  bdriver_mg5naod \
  -d "${BASE_DIR}"/../../../../../../cmssw_areas \
  -w ../wfs/"${JSON}" \
  -g /work/bevila_t/HpC_Analysis/CMSSW_10_6_18/src/XPlusCharmAnalysis/HPlusCharm/test/MadGraph5_aMCatNLO/genproductions_HPlusCharm_4FS_MuRFScaleDynX0p50_HToGG_M125_TuneCP5_13p6TeV_amcatnloFXFX_pythia8/bin/MadGraph5_aMCatNLO/"${sampleTag_i}"_slc7_amd64_gcc820_CMSSW_10_6_19_tarball.tar.xz \
  -f "${BASE_DIR}"/prod/fragments/"${sampleTag_i}".py \
  -o "${OUT_DIR}"/output_"${sampleTag_i}" \
  -p filelist:"${BASE_DIR}"/prod/data/Neutrino_E-10_gun_RunIIISummer22.txt \
  -q "long" \
  -b slurm \
  -l 1 -j 1000 -n "${NUM_EVENTS}" --cpus 4 --mem 4000 --time 24:00:00

  unset NUM_EVENTS
done
unset sampleTag_i

#rm -f "${BASE_DIR}"/.MinBias_RunIISummer19UL18SIM_SIM.txt

unset BASE_DIR OUT_DIR SAMPLE_TAGS

#!/usr/bin/env python
import argparse
import os
import stat
import json
import re
import multiprocessing
from commands import getstatusoutput

# execute program
def runCommand(cmd):
  cmd_exitcode, cmd_out = getstatusoutput(cmd)
  return cmd_exitcode

def showCommand(cmd):
  print cmd
  return 0

def getCommand(**kwargs):
  jobLabel = kwargs.get('jobLabel')
  envDir = kwargs.get('envDir')
  outputDir = kwargs.get('outputDir')
  outputFileName = kwargs.get('outputFileName')
  sampleTag = kwargs.get('sampleTag')
  jobID = kwargs.get('jobID')
  batch_part = kwargs.get('batch_part')
  time = kwargs.get('time')
  py_exec = kwargs.get('py_exec')

  outputROOTFile = outputFileName
  if not outputROOTFile.endswith('.root'):
    outputROOTFile += '.root'

  outputLogFile = outputROOTFile[:-5]+'.log'

  cmds = [
    '#!/bin/bash -e',
    '#SBATCH --account=t3',
    '#SBATCH --partition='+batch_part,
    '#SBATCH --cpus-per-task=4',
    '#SBATCH --mem=7000',
    '#SBATCH --time='+time,
    '#SBATCH --nodes=1',
    '#SBATCH -o /work/%u/test/.slurm/'+jobLabel+'_%A_%a.out',
    '#SBATCH -e /work/%u/test/.slurm/'+jobLabel+'_%A_%a.err',
    '',
    'echo "------------------------------------------------------------"',
    'echo "[`date`] Job started"',
    'echo "------------------------------------------------------------"',
    'DATE_START=`date +%s`',
    '',
    'echo HOSTNAME: ${HOSTNAME}',
    'echo HOME: ${HOME}',
    'echo USER: ${USER}',
    'echo X509_USER_PROXY: ${X509_USER_PROXY}',
    'echo CMD-LINE ARGS: $@',
    '',
    'mkdir -p /work/${USER}/test/.slurm ',
    '',
    'SLURM_ARRAY_TASK_ID='+jobID,
    'SAMPLE='+sampleTag,
    'if [ -z ${SLURM_ARRAY_TASK_ID} ]; then',
    '  printf "%s\n" "Environment variable \"SLURM_ARRAY_TASK_ID\" is not defined. Job will be stopped." 1>&2',
    '  exit 1',
    'fi',
    '',
    '[ ! -z ${SLURM_JOB_NAME} ] || SLURM_JOB_NAME=${SAMPLE}',
    '[ ! -z ${SLURM_ARRAY_JOB_ID} ] || SLURM_ARRAY_JOB_ID=local$(date +%y%m%d%H%M%S)',
    '[ ! -z ${SLURM_JOB_ID} ] || SLURM_JOB_ID='+jobID,
    '',
    'echo SLURM_JOB_NAME: ${SLURM_JOB_NAME}',
    'echo SLURM_JOB_ID: ${SLURM_JOB_ID}',
    'echo SLURM_ARRAY_JOB_ID: ${SLURM_ARRAY_JOB_ID}',
    'echo SLURM_ARRAY_TASK_ID: ${SLURM_ARRAY_TASK_ID}',
    '',
    'OUTPUT_DIR='+outputDir,
    'OUTPUT_FILE='+outputROOTFile,
    'echo OUTPUT_DIR: ${OUTPUT_DIR}',
    'echo OUTPUT_FILE: ${OUTPUT_FILE}',
    '',
    '[ ! -f ${OUTPUT_DIR}/flag.done ] || exit 0',
    '',
    'if [ ! -f ${X509_USER_PROXY} ]; then',
    '  printf "%s\n" "Authentication failed, invalid path to grid-certificate proxy: ${X509_USER_PROXY}" 1>&2',
    '  exit 1',
    'fi',
    '',
    'TMPDIR=/scratch/${USER}/slurm/${SLURM_JOB_NAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}',
    'echo TMPDIR: ${TMPDIR}',
    'mkdir -p ${TMPDIR}',
    'cd ${TMPDIR}',
    '',
    'source /cvmfs/cms.cern.ch/cmsset_default.sh',
    '',
    'export SCRAM_ARCH=slc7_amd64_gcc700e',
    'cd '+envDir,
    'eval `scram runtime -sh`',
    'cd ${TMPDIR}',
    'cmsRun '+py_exec,
    '', 
    'touch ${TMPDIR}/flag.done',
    '',
    'if [ ! -d ${OUTPUT_DIR}/logs ]; then',
    '  if [[ ${OUTPUT_DIR} == /pnfs/* ]]; then',
    '  (',
    '    (! command -v scram &> /dev/null) || eval `scram unsetenv -sh`',
    '    gfal-mkdir -p root://t3dcachedb.psi.ch:1094/${OUTPUT_DIR}/logs',
    '    sleep 5',
    '  )',
    '  else',
    '    mkdir -p ${OUTPUT_DIR}/logs',
    '  fi',
    'fi',
    '',
    'for tmpf in /work/${USER}/test/.slurm/${SLURM_JOB_NAME}_${SLURM_ARRAY_JOB_ID}_${SLURM_ARRAY_TASK_ID}.{out,err}; do',
    '  [ -f ${tmpf} ] || continue # stdout/err outputs not produced if running locally',
    '  if [[ ${OUTPUT_DIR} == /pnfs/* ]]; then',
    '    xrdcp -f -N ${tmpf} root://t3dcachedb.psi.ch:1094//${OUTPUT_DIR}/logs',
    '  else',
    '    cp ${tmpf} ${OUTPUT_DIR}/logs',
    '  fi',
    '  printf "%s\n" "> output file copied: ${tmpf} -> ${OUTPUT_DIR}/logs"',
    'done',
    '',
    'for tmpf in ${TMPDIR}/*.root ${TMPDIR}/flag.done ${TMPDIR}/*.txt; do',
    '  if [[ ${OUTPUT_DIR} == /pnfs/* ]]; then',
    '    xrdcp -f -N ${tmpf} root://t3dcachedb.psi.ch:1094//${OUTPUT_DIR}',
    '  else',
    '    cp ${tmpf} ${OUTPUT_DIR}',
    '  fi',
    '  printf "%s\n" "> output file copied: ${tmpf} -> ${OUTPUT_DIR}"',
    'done',
    '',
    '# removal of temporary working dir when job is completed',
    'rm -rf ${TMPDIR}',
    '',
    'echo "------------------------------------------------------------"',
    'echo "[`date`] Job completed successfully"',
    'DATE_END=`date +%s`',
    'runtime=$((DATE_END-DATE_START))',
    'echo "[`date`] Elapsed time: ${runtime} sec"',
    'echo "------------------------------------------------------------"',
  ]

  runScript = os.path.join(outputDir, 'run_'+jobID+'.sh')

  with open(runScript, 'w') as ofile:
    ofile.write('#!/bin/bash -e\n')
    for cmd in cmds: ofile.write(cmd+'\n')
    os.chmod(ofile.name, os.stat(ofile.name).st_mode | stat.S_IEXEC)

  return runScript

# main function
def main():

    parser = argparse.ArgumentParser(
        prog='./'+os.path.basename(__file__),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=__doc__)

    parser.add_argument('-o', '--output', dest='output_dir', action='store', default=None, required=False,
                      help='path to output directory')

    parser.add_argument('-b', '--batch-partition', dest='batch_part', action='store', type=str, default='standard',
                      help='batch-partition to use (default: long)')

    parser.add_argument('-m', '--max-processes', dest='max_processes', action='store', type=int, default=30,
                      help='maximum number of processes to run in parallel')

    parser.add_argument('-p', '--plugin', dest='py_exec', action='store', default='',
                      help='name of the python scrip to execute')

    parser.add_argument('-t', '--tag', dest='sampleTag', action='store', default='HToGG',
                      help='name of the sample')

    parser.add_argument('-f', '--output-file', dest='output_file', action='store', default='',
                      help='basename of output ROOT file')

    parser.add_argument('-d', '--dry-run', dest='dry_run', action='store_true', default=False,
                      help='enable dry-run mode')

    parser.add_argument('-v', '--verbosity', dest='verbosity', nargs='?', type=int, default=0, const=1,
                      help='level of verbosity (default: 0)')

    opts, opts_unknown = parser.parse_known_args()
    ### -------------------------

    log_prx = os.path.basename(__file__)+' -- '

    if len(opts_unknown) > 0:
        raise Exception('unrecognized command-line arguments: '+str(opts_unknown))

    if 'CMSSW_BASE' not in os.environ:
        raise Exception(log_prx+'global variable CMSSW_BASE is not defined (set up CMSSW environment with "cmsenv" before submitting jobs)')

    outputDir = os.path.abspath(opts.output_dir)
    outputSubDir = os.path.join(outputDir, opts.sampleTag)

    if os.path.exists(outputSubDir):
        raise Exception(log_prx+'target path to output directory already exists [-o]: '+str(outputSubDir))

    os.makedirs(outputSubDir)

    commands = []
    commandTags = []
    count = []

    job_dim = 5
    with open(opts.py_exec) as fp:
        Lines = fp.readlines()

        tot_files = sum('/store' in s for s in Lines)
        for i, line in enumerate(Lines):
            if '/store' in line: 
                start = i
                stop = start + job_dim
                break

        for idx in range(tot_files/job_dim+1):
            of = open(outputSubDir+"/tmp_"+str(idx)+".py", "w")
            for i, line in enumerate(Lines):
                if ('/store' in line and i not in range(start, stop)):
                    of.write('#'+line)
                elif ('fileName = cms.untracked.string' in line):
                    of.write('  fileName = cms.untracked.string(\'file:'+re.split('_', opts.py_exec)[0]+'_'+str(idx)+'.root\'),')
                else:
                    of.write(line)
                
            of.close()
            start = stop
            stop = start + job_dim

            commands.append('sbatch '+getCommand(**{
              'jobLabel': opts.sampleTag,
              'envDir': os.environ['CMSSW_BASE']+'/src',
              'outputDir': outputSubDir,
              'outputFileName': re.split('_', opts.py_exec)[0]+str(idx),
              'sampleTag': opts.sampleTag,
              'jobID': str(idx),
              'batch_part': opts.batch_part,
              'time': '2-00:00:00' if opts.batch_part == 'long' else ('12:00:00' if opts.batch_part == 'standard' else '00:45:00'),
              'py_exec': outputSubDir+'/'+"tmp_"+str(idx)+".py"
            }))

            commandTags.append(opts.sampleTag+str(idx))
            if opts.dry_run:
                count.append(showCommand(commands[idx]))
            else:
                count.append(runCommand(commands[idx]))

        #pool = multiprocessing.Pool(processes=min(opts.max_processes, len(commands)))
        #count = pool.map(showCommand if opts.dry_run else runCommand, commands)
#
        maxTagLength = max([len(tmp) for tmp in commandTags])
        maxExitCodeLength = max([len(str(tmp)) for tmp in count])
#
        reportLineFormat = '{: <'+str(maxTagLength)+'} : {: '+str(maxExitCodeLength)+'d}'

        for sampleTagIdx in range(len(commandTags)):
            print reportLineFormat.format(commandTags[sampleTagIdx], count[sampleTagIdx])




###
### main
###
if __name__ == '__main__':
  main()

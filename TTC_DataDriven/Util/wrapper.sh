#!/bin/bash -e 
echo "TEST FIRST" 

PWD=`pwd`
HOME=$PWD

echo $HOME 
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

# this is the actual work dir (replaced from python)
WorkDir=ACTUALDIR

cd $WorkDir
ls -lrth
eval `scramv1 runtime -sh`

# run the command to make plots
python INPUTFILE --era ERA --saveDir OUTPUTDIR DATAFLAG

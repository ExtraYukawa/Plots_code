#!/bin/bash -e 
echo "TEST FIRST" 

PWD=`pwd`
HOME=$PWD

echo $HOME 
export SCRAM_ARCH=slc7_amd64_gcc700
source /cvmfs/cms.cern.ch/cmsset_default.sh

# this should not be USER dependent FIXME
WorkDir=/afs/cern.ch/user/g/gkole/work/TTC/plots/CMSSW_10_6_27/src/Plots_code/TTC_DataDriven

cd $WorkDir
ls -lrth
eval `scramv1 runtime -sh`

# run the command to make plots
python INPUTFILE --era ERA --saveDir OUTPUTDIR DATAFLAG

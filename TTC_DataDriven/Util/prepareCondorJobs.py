#==============
# Last used:
# python Util/prepareCondorJobs.py -i ttc_mumu.py --era 2017
# python Util/prepareCondorJobs.py -i ttc_mumu.py --era 2017 --draw_data --test 
#==============
import os
import sys
import numpy as np
CURRENT_WORKDIR = os.getcwd()
sys.path.append(CURRENT_WORKDIR)
import argparse, datetime
import string
import random

cmsswBase = os.environ['CMSSW_BASE']

#from Util.General_Tool import CheckDir, CheckFile
parser = argparse.ArgumentParser()
coupling_value = []
for coupling in ['rtc','rtu','rtt']:
    for value in ['01','04','08','10']:
        coupling_value.append(coupling+value)

parser.add_argument('-i','--inputfile',type=str,default='ttc_mumu.py',help='Specify the configuration filename.')
parser.add_argument('-o','--outputDir',type=str,default='',help='Specify the output directory.')
parser.add_argument('--era',choices =['2016apv','2016postapv','2016merged','2017','2018'],default='2018',type=str,help='year of job.')
parser.add_argument("-draw_data", "--draw_data", action="store_true", dest="draw_data", default=False,
                    help="make it to True if you want to draw_data on MC stacks")
parser.add_argument("--test", action="store_true")

args = parser.parse_args()

###########################################################################
# Make a condor submission script
###########################################################################

config_filename = os.path.basename(args.inputfile)

if not args.outputDir:
    args.outputDir = '%s_%s_%s' % (config_filename.replace(".py", ""), args.era, datetime.datetime.now().strftime("%d%b%YT%H%M"))
    
# Go to the actual submission dir
os.mkdir(cmsswBase + '/src/Plots_code/TTC_DataDriven/'+args.outputDir)
os.chdir(cmsswBase + '/src/Plots_code/TTC_DataDriven/'+args.outputDir)
print ("submission dir: ", os. getcwd())

# prepare submit jdl file
os.system(r'cp ../Util/sub.jdl .')
# os.system(r'sed -i "s/wrapper.sh/wrapper_%s.sh/g" sub.jdl' %())

# copy wrapper script from Template and modify
#os.system(r'cp ../wrapper.sh wrapper_%s.sh' %(Era))
os.system(r'cp ../Util/wrapper.sh .')
os.system(r'sed -i "s/INPUTFILE/%s/g" wrapper.sh' %(config_filename))
os.system(r'sed -i "s/ERA/%s/g" wrapper.sh' %(args.era))
os.system(r'sed -i "s/OUTPUTDIR/%s/g" wrapper.sh' %(args.outputDir))
if args.draw_data:
    os.system(r'sed -i "s/DATAFLAG/%s/g" wrapper.sh' %("--draw_data"))
else:
    os.system(r'sed -i "s/DATAFLAG/%s/g" wrapper.sh' %(""))

# Final submission
if not args.test:
    print ("Submitting Jobs on Condor")
    os.system('condor_submit sub.jdl')

import os
import sys
import optparse, argparse
import subprocess
import json
import ROOT
from collections import OrderedDict


def prepare_range(path, fin, step):

  try:
    f_read = ROOT.TFile.Open(os.path.join(path, fin))
    entries = (f_read.Get('Events')).GetEntriesFast()
    init = 0
    index = []
    while(init < entries):
      index.append(init)
      init += step
    index.append(int(entries))
    f_read.Close()
    return index

  except:
    print("%s%s fail to process."%(path,fin))
    return None  

if __name__ == "__main__":
  
  usage  = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-m', '--method', dest='method', help='[data/slim_mc/slim_data/...]', default='all', type=str)
  parser.add_argument('-e', '--era',    dest='era',    help='[all/2016apv/2016postapv/2017/2018]',default='all',type=str, choices=["all","2016apv","2016postapv","2017","2018"])
  parser.add_argument('--JobFlavour', dest = 'JobFlavour', help='espresso/microcentury/longlunch/workday/tomorrow', type=str, default='espresso')
  parser.add_argument('--universe',   dest = 'universe', help='vanilla/local', type=str, default='vanilla')
  parser.add_argument('--outdir',     dest = 'outdir',     help='output directory',   type=str, default='./')
  parser.add_argument("--test",       action = "store_true")
  parser.add_argument("--blocksize",   dest = 'blocksize',   help='segment size', type = int, default = 1000000)
  parser.add_argument("--check",       action = "store_true")
  parser.add_argument("--region", dest = 'region', type = str, default = ['TTTo1L_control_region'], nargs = '+')
  parser.add_argument("--channels", dest = 'channels', type = str, default = ['mu', 'ele'], nargs = '+')
  parser.add_argument("--Labels", dest = 'Labels', default = ['Normal'], nargs='+')
  parser.add_argument("--Black_list", dest = 'Black_list', default = ['Bug'], nargs='+')
  parser.add_argument("--POIs",   dest = 'POIs',   default = [], nargs='+')
  args = parser.parse_args()
  args_dict = vars(args)
  check_text = "python runcondor.py --check "
  for arg in args_dict:
    if isinstance(args_dict[arg], list):
     if len(args_dict[arg]) > 0:
      check_text = check_text + " --" + arg + " " + ' '.join(args_dict[arg])
    elif isinstance(args_dict[arg], bool):
      pass
    else:
      check_text = check_text + " --" + arg + " " + str(args_dict[arg])
  with open('check.sh', 'w') as shell:
    shell.write(check_text)
  ##################
  ## Sample Label ##
  ##################

  Labels_text = ' '.join(args.Labels)
  if len(args.Black_list) == 0: Black_list_text = ''
  else: 
    Black_list_text = '--Black_list ' + ' '.join(args.Black_list)
  POIs_text   = ' '.join(args.POIs)
  #########
  ## Era ##
  #########

  Eras_List = ['2016apv', '2016postapv', '2017', '2018']
  Eras      = []
  for Era in Eras_List:
    if args.era == 'all' or args.era == Era:
      Eras.append(Era)

  ############
  ##  Path  ##
  ############

  #cmsswBase = os.environ['CMSSW_BASE']
  farm_dir  = os.path.join('./', 'Farm')
  cwd       = os.getcwd()

  os.system('mkdir -p %s '%farm_dir)
  os.system('cp %s/../../python/common.py .'%cwd)
  os.system('cp %s/../../python/haddnano.py .'%cwd)

  from common import prepare_shell, Get_Sample, cmsswBase, inputFile_path
  
  ##############
  ##  Condor  ##
  ##############

  condor = open(os.path.join(farm_dir, 'condor.sub'), 'w')
  condor.write('output = %s/job_common_$(Process).out\n'%farm_dir)
  condor.write('error  = %s/job_common_$(Process).err\n'%farm_dir)
  condor.write('log    = %s/job_common_$(Process).log\n'%farm_dir)
  condor.write('executable = %s/$(cfgFile)\n'%farm_dir)
  condor.write('universe = %s\n'%args.universe)
  condor.write('requirements = (OpSysAndVer =?= "CentOS7")\n')
  condor.write('+JobFlavour = "%s"\n'%args.JobFlavour)
  #condor.write('+MaxRuntime = 7200\n')
  cwd = os.getcwd()

  ##############
  ##  Script  ##
  ##############

  Check_GreenLight = True

  for Era in Eras:
   for channel in args.channels:
     for region in args.region:
       Outdir   = os.path.join(args.outdir, Era, region, channel)
       template = "%s/../../script/slim.h"%cwd
       era_header = "script/slim_%s.h"%Era

       os.system('mkdir -p script')
       os.system('cat %s | sed "s/EraToBeReplaced/%s/g" > %s'%(template,Era,era_header))
       os.system('cp %s/../../script/env.sh script/.'%cwd)

       json_file_name = "../../data/sample_%s.json"%Era #tihsu: cg sample studied only

       for sample_Label in [["MC", "Background"], ["MC", "Signal"], ["Data"]]:

         print("Creating configuration for slim")
         python_file   =  os.path.join(cwd, 'slim.py')
      
         File_List      = Get_Sample(json_file_name, sample_Label, Era) # Use all the MC samples
         print(File_List)

         sample_label_text = " ".join(sample_Label)
         print(File_List)
         for iin in File_List:

           if args.blocksize == -1:
             shell_file = "step1_%s_%s_%s_%s.sh"%(iin, Era, region, channel)
             command = 'python slim.py --era %s --iin %s --outdir %s --region %s --channel %s --Labels %s %s --sample_labels %s --POIs %s'%(Era, iin, Outdir, region, channel, Labels_text,Black_list_text, sample_label_text, POIs_text)
             prepare_shell(shell_file, command, condor, farm_dir)

           else:
             ranges = prepare_range(inputFile_path[Era], iin, args.blocksize)
             for idx, num in enumerate(ranges[:-1]):
               if args.check:
                 try:
                   f  = ROOT.TFile.Open(os.path.join(Outdir, str(idx) + "_" + iin), "READ")
                   if f.IsZombie():
                     print(os.path.join(Outdir, str(idx) + "_" + iin), "is zombie")
                     Check_GreenLight = False
                   continue
                 except:
                   Check_GreenLight = False
                   print(os.path.join(Outdir, str(idx) + "_" + iin), "not exist")
               start = ranges[idx]
               end   = ranges[idx+1]
               command = 'python slim.py --era %s --iin %s --outdir %s --start %d --end %d --index %d --region %s --channel %s --Labels %s %s --sample_labels %s --POIs %s'%(Era, iin, Outdir, start, end, idx, region, channel, Labels_text, Black_list_text, sample_label_text, POIs_text)
               shell_file = "step1_%s_%s_%s_%s_%d.sh"%(iin, Era, region, channel, idx)
               prepare_shell(shell_file,command, condor, farm_dir)
  #################
  ##  Merge ROOT ##
  #################

  
  if args.check and Check_GreenLight:
    print("All files are produced successfully. Start to merge the files.")

    for Era in Eras:
     for channel in args.channels:
       for region in args.region:
        for sample_Label in [["MC", "Background"], ["MC", "Signal"], ["Data"]]:
         Outdir = os.path.join(args.outdir, Era, region, channel)
         json_file_name = "../../data/sample_%s.json"%Era
         File_List      = Get_Sample(json_file_name, sample_Label, Era, withTail = False) # Use all the MC samples
         Final_List     = []
         for iin in File_List:
           print("start merging %s"%os.path.join(Outdir, iin))
           os.system("rm %s.root"%os.path.join(Outdir, iin))
           merge_list = []
           for file_ in os.listdir(Outdir):
             if "_" + iin + "." in file_ or "_" + iin + "_" in file_:
               merge_list.append(os.path.join(Outdir,file_))
           os.system("python haddnano.py %s.root %s"%(os.path.join(Outdir, iin), ' '.join(merge_list)))
           if os.path.exists(os.path.join(Outdir, iin + ".root")):
             f = ROOT.TFile.Open(os.path.join(Outdir, iin + ".root"), "READ")
             if f.IsZombie(): #Any other failing situation? TODO
                print(os.path.join(Outdir, iin), "merge failed. Please fixed by hand (at this stage)")
             else:
               #os.system("rm %s"%os.path.join(Outdir, "*_" + iin))
               pass
  ##################
  ##  Submit Job  ##
  ##################

  condor.close()
  if not args.test and not (args.check and Check_GreenLight):
    print("Submitting Jobs on Condor")
    os.system('condor_submit %s/condor.sub'%farm_dir)


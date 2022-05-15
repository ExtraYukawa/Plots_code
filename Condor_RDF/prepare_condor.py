import os,json
import sys
from os import walk

def prepare_condor(year, sample):
  BASIC_PATH="/eos/cms/store/group/phys_top/ExtraYukawa/"
  WHICH_YEAR=year
  WHICH_SAMPLE=sample
  FULL_PATH=BASIC_PATH+WHICH_YEAR+"/"+WHICH_SAMPLE
  samples=[]
  dir_temp=[]
  for (dirpath, dirnames, filenames) in walk(FULL_PATH):
    if len(dirnames)>0:
      for id in range(0,len(dirnames)):
        if "000" in dirnames[id]:
          dir_temp.append(dirpath+'/'+dirnames[id])
  
  for id in range(0,len(dir_temp)):
    for (dirpath, dirnames, filenames) in walk(dir_temp[id]):
      if filenames:
        if 'tar.gz' in filenames[0]:continue
        samples=samples+[dir_temp[id]+'/'+xx for xx in filenames]
  return samples

if __name__ == "__main__":
  PWD=os.getcwd()
  wrapper_dir=PWD+'/wrapper.sh'
  year="2016apv"
  sample=["DYJetsToLL_M-50_TuneCP5_13TeV-amcatnloFXFX-pythia8"]
#  sample=["TTTW_TuneCP5_13TeV-madgraph-pythia8"]
#  sample=["TTZZ_TuneCP5_13TeV-madgraph-pythia8"]
  isdata=[0]
  channel='ee'
  region="DY"
  samples_temp=prepare_condor(year,sample[0])
  dir_str_temp=samples_temp[0].split("/")[:9]
  dir_str_temp=[a+"/" for a in dir_str_temp]
  dir_temp=''.join(a for a in dir_str_temp)
  dir_count=0
  for (dirpath, dirnames, filenames) in walk(dir_temp):
    if dir_count>0:break
    dirs_temp=dirnames
    dir_count=dir_count+1

  fin =open("filter.json", 'r')
  data=json.load(fin)
  filter_ee=data['region_filter'][region]['ee']+' && '+data['MET_filter'][year]
  filter_em=data['region_filter'][region]['em']+' && '+data['MET_filter'][year]
  filter_mm=data['region_filter'][region]['mm']+' && '+data['MET_filter'][year]

  for iname in range(0,len(dirs_temp)):
    os.mkdir(dirs_temp[iname])
    os.chdir(dirs_temp[iname])
    os.system(r'cp ../make_hists.py .')
    os.system(r'sed -i "s/FILTERS_EE/%s/g" make_hists.py'%(filter_ee))
    os.system(r'sed -i "s/FILTERS_EM/%s/g" make_hists.py'%(filter_em))
    os.system(r'sed -i "s/FILTERS_MM/%s/g" make_hists.py'%(filter_mm))
    os.system(r'sed -i "s/FILTERS_EEFILTERS_EE/\&\&/g" make_hists.py')
    os.system(r'sed -i "s/FILTERS_EMFILTERS_EM/\&\&/g" make_hists.py')
    os.system(r'sed -i "s/FILTERS_MMFILTERS_MM/\&\&/g" make_hists.py')
    os.system(r'cp ../sub.jdl .')
    for i in range(0,len(samples_temp)):
      num_temp=samples_temp[i].split('/')[-1].split('.')[0].split('_')[-1]
      num_temp=int(num_temp)-1
      os.mkdir(dirs_temp[iname]+'_'+str(num_temp))
      os.chdir(dirs_temp[iname]+'_'+str(num_temp))
      os.system(r'cp %s .'%(wrapper_dir))
      name_temp=samples_temp[i].replace("/","DUMMY")
      os.system(r'sed -i "s/dummyroot/%s/g" wrapper.sh' %(name_temp))
      os.system(r'sed -i "s/DUMMY/\//g" wrapper.sh')
      os.system(r'sed -i "s/STEPNUM/%s/g" wrapper.sh' %(samples_temp[i].split('/')[-1]))
      os.chdir(PWD+'/'+dirs_temp[iname])
    os.chdir(PWD+'/'+dirs_temp[iname])
    os.system(r'sed -i "s/NUMBER/%s/g" sub.jdl' %(len(samples_temp)))
    os.system(r'sed -i "s/DUMMY/%s/g" sub.jdl' %(dirs_temp[iname]))

#==============
# Last used:
# python ttc_mumu_2016merged.py --era 2016merged --saveDir 2016merged_mm_24Nov_18h22
# python ttc_mumu_2016merged.py --era 2016merged --saveDir 2016merged_mm
#==============

import ROOT
import time
import os
import sys
import math
from math import sqrt
import plot
from LoadData import *

ROOT.gROOT.SetBatch(True)

TTC_header_path = os.path.join("TTC.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

SAVEFORMATS  = "png" #pdf,png,C"
SAVEDIR      = None

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("--era", dest="era", default="2016APV",
                    help="When making the plots, read the files with this era(years), default: 2016APV")
parser.add_argument("--channel", dest="channel", default="mm",
                    help="Channel for drawing plots [default: mumu]")
parser.add_argument("-s", "--saveFormats", dest="saveFormats", default = SAVEFORMATS,
                      help="Save formats for all plots [default: %s]" % SAVEFORMATS)

parser.add_argument("--saveDir", dest="saveDir", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

parser.add_argument("-draw_data", "--draw_data", action="store_true", dest="draw_data", default=False,
                    help="make it to True if you want to draw_data on MC stacks")

opts = parser.parse_args()

# the EnableImplicitMT option should only use in cluster, at lxplus, it will make the code slower(my experience)
# ROOT.ROOT.EnableImplicitMT()
def check_histo(_h):
  for i in range(1, _h.GetNbinsX()):
    if _h.GetBinContent(i) < 0:
      _h.SetBinContent(i, 0)

def add_two_histos(h1, h2):
  added_histos = []
  h1.Add(h2)
  added_histos.append(h1)
  return added_histos

def get_filelist(path, flist=[]):
  f_list = ROOT.std.vector('string')()
  for f in flist:
    # print (path+f)
    f_list.push_back(path+f)
  return f_list

def histos_book(flist, filters, variables, isData = "False", isFake = "False", era="2016APV"):
  # print ("flist: ", str(flist[0]).split('/')[-1])
  df_xyz_tree = ROOT.RDataFrame("Events",flist)

  if not isData:
    df_xyz_tree = df_xyz_tree.Define("trigger_SF","trigger_sf_mm_"+era+"(ttc_l1_pt,ttc_l2_pt)")
    # check if the events are fake or not
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_mm_"+era+"(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta, "+str(isData).lower()+")")
      df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
    else:
      df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*trigger_SF*Muon_CutBased_LooseID_SF[ttc_l1_id]*Muon_CutBased_LooseID_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  else:
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_mm_"+era+"(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,muon_conePt[ttc_l2_id],ttc_l2_eta, "+str(isData).lower()+")")

  # common for data/MC
  df_xyz = df_xyz_tree.Filter(filters)
  if not isData:
    df_xyz_trigger = all_trigger(df_xyz, era)
  else:
    if "doublemu" in str(flist[0]).split('/')[-1].lower():
      print ("doubleMu")
      df_xyz_trigger = for_dimuon_trigger(df_xyz, era)
    elif "singlemu" in str(flist[0]).split('/')[-1].lower():
      print ("singleMu")
      df_xyz_trigger = for_singlemuon_trigger_mumuchannel(df_xyz, era)
    else:
      print ("choose correct trigger function")
  # put histos in a list
  df_xyz_histos = []
  for variable in variables:
    if not isData:
      df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',len(ranges[variable])-1, ranges[variable]), variable,'genweight')
    else:
      if isFake:
        df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',len(ranges[variable])-1, ranges[variable]), variable,'fakelep_weight')
      else:
        df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',len(ranges[variable])-1, ranges[variable]), variable)
    h = df_xyz_histo.GetValue()
    h.SetDirectory(0)
    df_xyz_histos.append(h.Clone())
    ROOT.TH1.AddDirectory(0)

  return df_xyz_histos

# Data paths 
if opts.era == "2016APV":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged/'
elif opts.era == "2016postAPV":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/'
elif opts.era == "2016merged":
  pathAPV='/eos/cms/store/group/phys_top/ExtraYukawa/2016apvMerged/'
  pathpostAPV='/eos/cms/store/group/phys_top/ExtraYukawa/2016postapvMerged/'
else:
  raise Exception ("select correct subEra!")

if opts.era == "2016APV":
  print ("Reading 2016 APV files \n")
  doubleMu_names = get_filelist(path, ["DoubleMuon_B2.root","DoubleMuon_C.root","DoubleMuon_D.root","DoubleMuon_E.root","DoubleMuon_F.root"])
  singleMu_names = get_filelist(path, ["SingleMuon_B2.root","SingleMuon_C.root","SingleMuon_D.root","SingleMuon_E.root","SingleMuon_F.root"])
elif opts.era == "2016postAPV":
  print ("Reading 2016 postAPV files \n")
  doubleMu_names = get_filelist(path, ["DoubleMuon_F.root","DoubleMuon_G.root","DoubleMuon_H.root"])
  singleMu_names = get_filelist(path, ["SingleMuon_F.root","SingleMuon_G.root","SingleMuon_H.root"])
elif opts.era == "2016merged":
  print ("Reading 2016 APV and postAPV files \n")
  doubleMu_names_APV = get_filelist(pathAPV, ["DoubleMuon_B2.root","DoubleMuon_C.root","DoubleMuon_D.root","DoubleMuon_E.root","DoubleMuon_F.root"])
  doubleMu_names_postAPV = get_filelist(pathpostAPV, ["DoubleMuon_F.root","DoubleMuon_G.root","DoubleMuon_H.root"])
  singleMu_names_APV = get_filelist(pathAPV, ["SingleMuon_B2.root","SingleMuon_C.root","SingleMuon_D.root","SingleMuon_E.root","SingleMuon_F.root"])
  singleMu_names_postAPV = get_filelist(pathpostAPV, ["SingleMuon_F.root","SingleMuon_G.root","SingleMuon_H.root"])
else:
  raise Exception ("select correct subEra!")

# MC for APV  
DY_list_APV = get_filelist(pathAPV, ['DYnlo.root'])
osWW_list_APV = get_filelist(pathAPV, ['ww.root'])
ssWW_list_APV = get_filelist(pathAPV, ['ssWW.root']) # not present for 2016APV and postAPV
WWdps_list_APV = get_filelist(pathAPV, ['WWdps.root']) # not present for 2016APV and postAPV
WZew_list_APV = get_filelist(pathAPV, ['WZ_ew.root']) # not present for 2016APV and postAPV
WZqcd_list_APV = get_filelist(pathAPV, ['wz_qcd.root'])
ZZ_list_APV = get_filelist(pathAPV, ['zz2l.root'])
ZG_list_APV = get_filelist(pathAPV, ['ZG_ew.root']) # not present for 2016APV and postAPV
WWW_list_APV = get_filelist(pathAPV, ['www1.root'])
WWZ_list_APV = get_filelist(pathAPV, ['wwz1.root'])
WZZ_list_APV = get_filelist(pathAPV, ['wzz1.root'])
ZZZ_list_APV = get_filelist(pathAPV, ['zzz1.root'])
tW_list_APV = get_filelist(pathAPV, ['tW.root'])
tbarW_list_APV = get_filelist(pathAPV, ['tbarW.root'])
ttWtoLNu_list_APV = get_filelist(pathAPV, ['ttW.root'])
ttWtoQQ_list_APV = get_filelist(pathAPV, ['ttWToQQ.root'])
ttZ_list_APV = get_filelist(pathAPV, ['ttZ.root'])
ttZtoQQ_list_APV = get_filelist(pathAPV, ['ttZToQQ.root'])
ttH_list_APV = get_filelist(pathAPV, ['ttH.root'])
tttt_list_APV = get_filelist(pathAPV, ['tttt.root'])
tttJ_list_APV = get_filelist(pathAPV, ['tttJ.root'])
tttW_list_APV = get_filelist(pathAPV, ['tttW.root']) #not present for 2016postAPV
ttG_list_APV = get_filelist(pathAPV, ['TTG.root']) # not present for 2016APV and postAPV
ttZH_list_APV = get_filelist(pathAPV, ['ttZH.root'])
ttWH_list_APV = get_filelist(pathAPV, ['ttWH.root'])
ttWW_list_APV = get_filelist(pathAPV, ['ttWW.root'])
ttWZ_list_APV = get_filelist(pathAPV, ['ttWZ.root'])
ttZZ_list_APV = get_filelist(pathAPV, ['ttZZ.root'])
tzq_list_APV = get_filelist(pathAPV, ['tZq.root'])
TTTo2L_list_APV = get_filelist(pathAPV, ['TTTo2L.root'])
WLLJJ_list_APV = get_filelist(pathAPV, ['WLLJJ.root'])
WpWpJJ_EWK_list_APV = get_filelist(pathAPV, ['WpWpJJ_EWK.root'])
WpWpJJ_QCD_list_APV = get_filelist(pathAPV, ['WpWpJJ_QCD.root'])
ZZJJTo4L_list_APV = get_filelist(pathAPV, ['ZZJJTo4L.root'])

# MC for postAPV
DY_list_postAPV = get_filelist(pathpostAPV, ['DYnlo.root'])
osWW_list_postAPV = get_filelist(pathpostAPV, ['ww.root'])
ssWW_list_postAPV = get_filelist(pathpostAPV, ['ssWW.root']) # not present for 2016APV and postAPV
WWdps_list_postAPV = get_filelist(pathpostAPV, ['WWdps.root']) # not present for 2016APV and postAPV
WZew_list_postAPV = get_filelist(pathpostAPV, ['WZ_ew.root']) # not present for 2016APV and postAPV
WZqcd_list_postAPV = get_filelist(pathpostAPV, ['wz_qcd.root'])
ZZ_list_postAPV = get_filelist(pathpostAPV, ['zz2l.root'])
ZG_list_postAPV = get_filelist(pathpostAPV, ['ZG_ew.root']) # not present for 2016APV and postAPV
WWW_list_postAPV = get_filelist(pathpostAPV, ['www1.root'])
WWZ_list_postAPV = get_filelist(pathpostAPV, ['wwz1.root'])
WZZ_list_postAPV = get_filelist(pathpostAPV, ['wzz1.root'])
ZZZ_list_postAPV = get_filelist(pathpostAPV, ['zzz1.root'])
tW_list_postAPV = get_filelist(pathpostAPV, ['tW.root'])
tbarW_list_postAPV = get_filelist(pathpostAPV, ['tbarW.root'])
ttWtoLNu_list_postAPV = get_filelist(pathpostAPV, ['ttW.root'])
ttWtoQQ_list_postAPV = get_filelist(pathpostAPV, ['ttWToQQ.root'])
ttZ_list_postAPV = get_filelist(pathpostAPV, ['ttZ.root'])
ttZtoQQ_list_postAPV = get_filelist(pathpostAPV, ['ttZToQQ.root'])
ttH_list_postAPV = get_filelist(pathpostAPV, ['ttH.root'])
tttt_list_postAPV = get_filelist(pathpostAPV, ['tttt.root'])
tttJ_list_postAPV = get_filelist(pathpostAPV, ['tttJ.root'])
tttW_list_postAPV = get_filelist(pathpostAPV, ['tttW.root']) #not present for 2016postAPV
ttG_list_postAPV = get_filelist(pathpostAPV, ['TTG.root']) # not present for 2016APV and postAPV
ttZH_list_postAPV = get_filelist(pathpostAPV, ['ttZH.root'])
ttWH_list_postAPV = get_filelist(pathpostAPV, ['ttWH.root'])
ttWW_list_postAPV = get_filelist(pathpostAPV, ['ttWW.root'])
ttWZ_list_postAPV = get_filelist(pathpostAPV, ['ttWZ.root'])
ttZZ_list_postAPV = get_filelist(pathpostAPV, ['ttZZ.root'])
tzq_list_postAPV = get_filelist(pathpostAPV, ['tZq.root'])
TTTo2L_list_postAPV = get_filelist(pathpostAPV, ['TTTo2L.root'])
WLLJJ_list_postAPV = get_filelist(pathpostAPV, ['WLLJJ.root'])
WpWpJJ_EWK_list_postAPV = get_filelist(pathpostAPV, ['WpWpJJ_EWK.root'])
WpWpJJ_QCD_list_postAPV = get_filelist(pathpostAPV, ['WpWpJJ_QCD.root'])
ZZJJTo4L_list_postAPV = get_filelist(pathpostAPV, ['ZZJJTo4L.root'])

def TTC_Analysis(opts):

  histos = []

  variables = ranges.keys()
  for ij in range(0,len(variables)):
    print (variables[ij])
  
  # import selections
  filters_mc, filters_mc_fake, filters_data, filters_data_fake = selections("mm")
  print ("filters_mc:        ", filters_mc)
  print ("filters_mc_fake:   ", filters_mc_fake)
  print ("filters_data:      ", filters_data)
  print ("filters_data_fake: ", filters_data_fake)
  
  ##############
  ## DY samples
  ##############
  df_DY_histos_APV = histos_book(DY_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_DY_histos_postAPV = histos_book(DY_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_DY_histos_APV = histos_book(DY_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_DY_histos_postAPV = histos_book(DY_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("DY both genuine and fake histo loading complete!")
  print ("df_DY_histos_APV[0] integral", df_DY_histos_APV[0].Integral())
  print ("df_DY_histos_postAPV[0] integral", df_DY_histos_postAPV[0].Integral())
  h3 = add_two_histos(df_DY_histos_APV[0], df_DY_histos_postAPV[0])
  print ("h3[0].Integral(): ", h3[0].Integral())
  print ("test(need to understand): ", add_two_histos(df_DY_histos_APV[0], df_DY_histos_postAPV[0])[0].Integral())
  

  ##############
  ## osWW samples
  ##############
  df_osWW_histos_APV = histos_book(osWW_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_osWW_histos_postAPV = histos_book(osWW_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_osWW_histos_APV = histos_book(osWW_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_osWW_histos_postAPV = histos_book(osWW_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("osWW both genuine and fake histo loading complete!")
  

  ##############
  ## ssWW samples(NOT present in 2016)
  ##############
  #df_ssWW_histos = histos_book(ssWW_list, filters_mc, variables, False, False) #isData, isFake
  #df_Fake_ssWW_histos = histos_book(ssWW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ssWW histos are taken from osWW, but Reset to 0!")
  df_ssWW_histos_APV = []
  df_ssWW_histos_postAPV = []
  df_Fake_ssWW_histos_APV = []
  df_Fake_ssWW_histos_postAPV = []
  for ii in range(0,len(variables)):
    h1 = df_osWW_histos_APV[ii].Clone()
    h1.Reset()
    df_ssWW_histos_APV.append(h1.Clone())
    df_ssWW_histos_postAPV.append(h1.Clone())
    h2 = df_Fake_osWW_histos_APV[ii].Clone()
    h2.Reset()
    df_Fake_ssWW_histos_APV.append(h2.Clone())
    df_Fake_ssWW_histos_postAPV.append(h2.Clone())
  
  
  ##############
  ## WWdps samples
  ##############
  #df_WWdps_histos = histos_book(WWdps_list, filters_mc, variables, False, False) #isData, isFake 
  #df_Fake_WWdps_histos = histos_book(WWdps_list, filters_mc_fake, variables, False, True) #isData, isFake 
  print ("WWdps histos are taken from osWW, but Reset to 0!")
  df_WWdps_histos_APV = []
  df_WWdps_histos_postAPV = []
  df_Fake_WWdps_histos_APV = []
  df_Fake_WWdps_histos_postAPV = []
  for ii in range(0,len(variables)):
    h1 = df_osWW_histos_APV[ii].Clone()
    h1.Reset()
    df_WWdps_histos_APV.append(h1.Clone())
    df_WWdps_histos_postAPV.append(h1.Clone())
    h2 = df_Fake_osWW_histos_APV[ii].Clone()
    h2.Reset()
    df_Fake_WWdps_histos_APV.append(h2.Clone())
    df_Fake_WWdps_histos_postAPV.append(h2.Clone())
  
  ##############
  ## WZew samples
  ##############
  print ("WZew histos are taken from osWW, but Reset to 0!")
  df_WZew_histos_APV = []
  df_WZew_histos_postAPV = []
  df_Fake_WZew_histos_APV = []
  df_Fake_WZew_histos_postAPV = []
  for ii in range(0,len(variables)):
    h1 = df_osWW_histos_APV[ii].Clone()
    h1.Reset()
    df_WZew_histos_APV.append(h1.Clone())
    df_WZew_histos_postAPV.append(h1.Clone())
    h2 = df_Fake_osWW_histos_APV[ii].Clone()
    h2.Reset()
    df_Fake_WZew_histos_APV.append(h2.Clone())
    df_Fake_WZew_histos_postAPV.append(h2.Clone())
  
  ##############
  ## WZqcd samples
  ##############
  df_WZqcd_histos_APV = histos_book(WZqcd_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake 
  df_WZqcd_histos_postAPV = histos_book(WZqcd_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_WZqcd_histos_APV = histos_book(WZqcd_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WZqcd_histos_postAPV = histos_book(WZqcd_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WZqcd both genuine and fake histo loading complete!")
  
  ##############
  ## ZZ samples
  ##############
  df_ZZ_histos_APV = histos_book(ZZ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ZZ_histos_postAPV = histos_book(ZZ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ZZ_histos_APV = histos_book(ZZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ZZ_histos_postAPV = histos_book(ZZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("zz both genuine and fake histo loading complete!")
  
  ##############
  ## ZG samples
  ##############
  print ("ZG histos are taken from osWW, but Reset to 0!")
  df_ZG_histos_APV = []
  df_ZG_histos_postAPV = []
  df_Fake_ZG_histos_APV = []
  df_Fake_ZG_histos_postAPV = []
  for ii in range(0,len(variables)):
    h1 = df_osWW_histos_APV[ii].Clone()
    h1.Reset()
    df_ZG_histos_APV.append(h1.Clone())
    df_ZG_histos_postAPV.append(h1.Clone())
    h2 = df_Fake_osWW_histos_APV[ii].Clone()
    h2.Reset()
    df_Fake_ZG_histos_APV.append(h2.Clone())
    df_Fake_ZG_histos_postAPV.append(h2.Clone())

  ##############
  ## WWW samples
  ##############
  df_WWW_histos_APV = histos_book(WWW_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_WWW_histos_postAPV = histos_book(WWW_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_WWW_histos_APV = histos_book(WWW_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WWW_histos_postAPV = histos_book(WWW_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WWW both genuine and fake histo loading complete!")

  ##############
  ## WWZ samples
  ##############
  df_WWZ_histos_APV = histos_book(WWZ_list_APV, filters_mc, variables, False, False,  "2016APV") #isData, isFake 
  df_WWZ_histos_postAPV = histos_book(WWZ_list_postAPV, filters_mc, variables, False, False,  "2016postAPV") #isData, isFake 
  df_Fake_WWZ_histos_APV = histos_book(WWZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WWZ_histos_postAPV = histos_book(WWZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WWZ both genuine and fake histo loading complete!")
  
  ##############
  ## WZZ samples
  ##############
  df_WZZ_histos_APV = histos_book(WZZ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_WZZ_histos_postAPV = histos_book(WZZ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_WZZ_histos_APV = histos_book(WZZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WZZ_histos_postAPV = histos_book(WZZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WZZ both genuine and fake histo loading complete!")
  
  ##############
  ## ZZZ samples
  ##############
  df_ZZZ_histos_APV = histos_book(ZZZ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ZZZ_histos_postAPV = histos_book(ZZZ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ZZZ_histos_APV = histos_book(ZZZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ZZZ_histos_postAPV = histos_book(ZZZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ZZZ both genuine and fake histo loading complete!")
  
  ##############
  ## tW samples
  ##############
  df_tW_histos_APV = histos_book(tW_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_tW_histos_postAPV = histos_book(tW_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_tW_histos_APV = histos_book(tW_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_tW_histos_postAPV = histos_book(tW_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("tW both genuine and fake histo loading complete!")

  ##############
  ## tbarW samples
  ##############
  df_tbarW_histos_APV = histos_book(tbarW_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_tbarW_histos_postAPV = histos_book(tbarW_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_tbarW_histos_APV = histos_book(tbarW_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_tbarW_histos_postAPV = histos_book(tbarW_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("tbarW both genuine and fake histo loading complete!")
  
  ##############
  ## ttWtoLNu samples
  ##############
  df_ttWtoLNu_histos_APV = histos_book(ttWtoLNu_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttWtoLNu_histos_postAPV = histos_book(ttWtoLNu_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttWtoLNu_histos_APV = histos_book(ttWtoLNu_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttWtoLNu_histos_postAPV = histos_book(ttWtoLNu_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttWtoLNu both genuine and fake histo loading complete!")
  
  ##############
  ## ttWtoQQ samples
  ##############
  df_ttWtoQQ_histos_APV = histos_book(ttWtoQQ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttWtoQQ_histos_postAPV = histos_book(ttWtoQQ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttWtoQQ_histos_APV = histos_book(ttWtoQQ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake 
  df_Fake_ttWtoQQ_histos_postAPV = histos_book(ttWtoQQ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttWtoQQ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZ samples
  ##############
  df_ttZ_histos_APV = histos_book(ttZ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttZ_histos_postAPV = histos_book(ttZ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttZ_histos_APV = histos_book(ttZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttZ_histos_postAPV = histos_book(ttZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttZ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZtoQQ samples
  ##############
  df_ttZtoQQ_histos_APV = histos_book(ttZtoQQ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttZtoQQ_histos_postAPV = histos_book(ttZtoQQ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttZtoQQ_histos_APV = histos_book(ttZtoQQ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttZtoQQ_histos_postAPV = histos_book(ttZtoQQ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttZtoQQ both genuine and fake histo loading complete!")
  
  ##############
  ## ttH samples
  ##############
  df_ttH_histos_APV = histos_book(ttH_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttH_histos_postAPV = histos_book(ttH_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttH_histos_APV = histos_book(ttH_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake 
  df_Fake_ttH_histos_postAPV = histos_book(ttH_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake 
  print ("ttH both genuine and fake histo loading complete!")


  ##############
  ## tttW samples
  ##############
  print ("tttW postAPV histos are taken from osWW, but Reset to 0!")
  df_tttW_histos_postAPV = []
  df_Fake_tttW_histos_postAPV = []
  for ii in range(0,len(variables)):
    h1 = df_osWW_histos_postAPV[ii].Clone()
    h1.Reset()
    df_tttW_histos_postAPV.append(h1.Clone())
    h2 = df_Fake_osWW_histos_postAPV[ii].Clone()
    h2.Reset()
    df_Fake_tttW_histos_postAPV.append(h2.Clone())
    
  df_tttW_histos_APV = histos_book(tttW_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_Fake_tttW_histos_APV = histos_book(tttW_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  print ("tttW both genuine and fake histo loading complete!")
  
  
  ##############
  ## tttJ samples
  ##############
  df_tttJ_histos_APV = histos_book(tttJ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_tttJ_histos_postAPV = histos_book(tttJ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_tttJ_histos_APV = histos_book(tttJ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_tttJ_histos_postAPV = histos_book(tttJ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("tttJ both genuine and fake histo loading complete!")
  
  ##############
  ## ttG samples
  ##############
  #df_ttG_histos = histos_book(ttG_list, filters_mc, variables, False, False) #isData, isFake
  #df_Fake_ttG_histos = histos_book(ttG_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttG histos are taken from osWW, but Reset to 0!")
  df_ttG_histos_APV = []
  df_Fake_ttG_histos_APV = []
  df_ttG_histos_postAPV = []
  df_Fake_ttG_histos_postAPV = []
  for ii in range(0,len(variables)):
    h1 = df_osWW_histos_APV[ii].Clone()
    h1.Reset()
    df_ttG_histos_APV.append(h1.Clone())
    df_ttG_histos_postAPV.append(h1.Clone())
    h2 = df_Fake_osWW_histos_APV[ii].Clone()
    h2.Reset()
    df_Fake_ttG_histos_APV.append(h2.Clone())
    df_Fake_ttG_histos_postAPV.append(h2.Clone())
  
  ##############
  ## ttWH samples
  ##############
  df_ttWH_histos_APV = histos_book(ttWH_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttWH_histos_postAPV = histos_book(ttWH_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttWH_histos_APV = histos_book(ttWH_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttWH_histos_postAPV = histos_book(ttWH_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttWH both genuine and fake histo loading complete!")
  
  ##############
  ## ttZH samples
  ##############
  df_ttZH_histos_APV = histos_book(ttZH_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttZH_histos_postAPV = histos_book(ttZH_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttZH_histos_APV = histos_book(ttZH_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttZH_histos_postAPV = histos_book(ttZH_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttZH both genuine and fake histo loading complete!")
  
  ##############
  ## tttt samples
  ##############
  df_tttt_histos_APV = histos_book(tttt_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake 
  df_tttt_histos_postAPV = histos_book(tttt_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_tttt_histos_APV = histos_book(tttt_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_tttt_histos_postAPV = histos_book(tttt_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("tttt both genuine and fake histo loading complete!")
  
  ##############
  ## ttWW samples
  ##############
  df_ttWW_histos_APV = histos_book(ttWW_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttWW_histos_postAPV = histos_book(ttWW_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttWW_histos_APV = histos_book(ttWW_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttWW_histos_postAPV = histos_book(ttWW_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttWW both genuine and fake histo loading complete!")
  
  ##############
  ## ttWZ samples
  ##############
  df_ttWZ_histos_APV = histos_book(ttWZ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttWZ_histos_postAPV = histos_book(ttWZ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttWZ_histos_APV = histos_book(ttWZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttWZ_histos_postAPV = histos_book(ttWZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttWZ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZZ samples
  ##############
  df_ttZZ_histos_APV = histos_book(ttZZ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_ttZZ_histos_postAPV = histos_book(ttZZ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_ttZZ_histos_APV = histos_book(ttZZ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ttZZ_histos_postAPV = histos_book(ttZZ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ttZZ both genuine and fake histo loading complete!")
  
  ##############
  ## tzq samples
  ##############
  df_tzq_histos_APV = histos_book(tzq_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake 
  df_tzq_histos_postAPV = histos_book(tzq_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_tzq_histos_APV = histos_book(tzq_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_tzq_histos_postAPV = histos_book(tzq_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("tzq both genuine and fake histo loading complete!")
  
  ##############
  ## TTTo2L samples
  ##############
  df_TTTo2L_histos_APV = histos_book(TTTo2L_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake 
  df_TTTo2L_histos_postAPV = histos_book(TTTo2L_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_TTTo2L_histos_APV = histos_book(TTTo2L_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_TTTo2L_histos_postAPV = histos_book(TTTo2L_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("TTTo2L both genuine and fake histo loading complete!")

  
  ##############
  ## DoubleMu samples
  ##############
  df_DoubleMu_histos_APV = histos_book(doubleMu_names_APV, filters_data, variables, True, False, "2016APV") #isData, isFake 
  df_DoubleMu_histos_postAPV = histos_book(doubleMu_names_postAPV, filters_data, variables, True, False, "2016postAPV") #isData, isFake 
  df_FakeLep_DoubleMu_histos_APV = histos_book(doubleMu_names_APV, filters_data_fake, variables, True, True, "2016APV") #isData, isFake, what is data fake? 
  df_FakeLep_DoubleMu_histos_postAPV = histos_book(doubleMu_names_postAPV, filters_data_fake, variables, True, True, "2016postAPV") #isData, isFake, what is data fake? 
  print ("DoubleMu both genuine and fake histo loading complete!")

  ##############
  ## SingleMu samples
  ##############
  df_SingleMu_histos_APV = histos_book(singleMu_names_APV, filters_data, variables, True, False, "2016APV") #isData, isFake
  df_SingleMu_histos_postAPV = histos_book(singleMu_names_postAPV, filters_data, variables, True, False, "2016postAPV") #isData, isFake
  df_FakeLep_SingleMu_histos_APV = histos_book(singleMu_names_APV, filters_data_fake, variables, True, True, "2016APV") #isData, isFake
  df_FakeLep_SingleMu_histos_postAPV = histos_book(singleMu_names_postAPV, filters_data_fake, variables, True, True, "2016postAPV") #isData, isFake
  print ("SingleMu both genuine and fake histo loading complete!")
  
  ##############
  ## WLLJJ samples
  ##############
  df_WLLJJ_histos_APV = histos_book(WLLJJ_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake 
  df_WLLJJ_histos_postAPV = histos_book(WLLJJ_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_WLLJJ_histos_APV = histos_book(WLLJJ_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WLLJJ_histos_postAPV = histos_book(WLLJJ_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WLLJJ both genuine and fake histo loading complete!")

  ##############
  ## ZZJJTo4L samples
  ##############
  df_ZZJJTo4L_histos_APV = histos_book(ZZJJTo4L_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake 
  df_ZZJJTo4L_histos_postAPV = histos_book(ZZJJTo4L_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake 
  df_Fake_ZZJJTo4L_histos_APV = histos_book(ZZJJTo4L_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_ZZJJTo4L_histos_postAPV = histos_book(ZZJJTo4L_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("ZZJJTo4L both genuine and fake histo loading complete!")

  ##############
  ## WpWpJJ_EWK samples
  ##############
  df_WpWpJJ_EWK_histos_APV = histos_book(WpWpJJ_EWK_list_APV, filters_mc, variables, False, False, "2016APV") #isData, isFake
  df_WpWpJJ_EWK_histos_postAPV = histos_book(WpWpJJ_EWK_list_postAPV, filters_mc, variables, False, False, "2016postAPV") #isData, isFake
  df_Fake_WpWpJJ_EWK_histos_APV = histos_book(WpWpJJ_EWK_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WpWpJJ_EWK_histos_postAPV = histos_book(WpWpJJ_EWK_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WpWpJJ_EWK both genuine and fake histo loading complete!")

  ##############
  ## WpWpJJ_QCD samples
  ##############
  df_WpWpJJ_QCD_histos_APV = histos_book(WpWpJJ_QCD_list_APV, filters_mc, variables, False, False,"2016APV") #isData, isFake 
  df_WpWpJJ_QCD_histos_postAPV = histos_book(WpWpJJ_QCD_list_postAPV, filters_mc, variables, False, False,"2016postAPV") #isData, isFake 
  df_Fake_WpWpJJ_QCD_histos_APV = histos_book(WpWpJJ_QCD_list_APV, filters_mc_fake, variables, False, True, "2016APV") #isData, isFake
  df_Fake_WpWpJJ_QCD_histos_postAPV = histos_book(WpWpJJ_QCD_list_postAPV, filters_mc_fake, variables, False, True, "2016postAPV") #isData, isFake
  print ("WpWpJJ_QCD both genuine and fake histo loading complete!")  

  APV_lumi = 19520.
  postAPV_lumi = 16810.
  
  # Loop over histograms
  for ij in range(0,len(variables)):
  
    # ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
    #  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})
    h_DY_APV = df_DY_histos_APV[ij].Clone()
    h_osWW_APV = df_osWW_histos_APV[ij].Clone()
    h_ssWW_APV = df_ssWW_histos_APV[ij].Clone()
    h_WWdps_APV = df_WWdps_histos_APV[ij].Clone()
    h_WZew_APV = df_WZew_histos_APV[ij].Clone()
    h_WZqcd_APV = df_WZqcd_histos_APV[ij].Clone()
    h_ZZ_APV = df_ZZ_histos_APV[ij].Clone()
    h_ZG_APV = df_ZG_histos_APV[ij].Clone()
    h_WWW_APV = df_WWW_histos_APV[ij].Clone()
    h_WWZ_APV = df_WWZ_histos_APV[ij].Clone()
    h_WZZ_APV = df_WZZ_histos_APV[ij].Clone()
    h_ZZZ_APV = df_ZZZ_histos_APV[ij].Clone()
    h_tW_APV = df_tW_histos_APV[ij].Clone()
    h_tbarW_APV = df_tbarW_histos_APV[ij].Clone()
    h_ttWtoLNu_APV = df_ttWtoLNu_histos_APV[ij].Clone()
    h_ttWtoQQ_APV = df_ttWtoQQ_histos_APV[ij].Clone()
    h_ttZ_APV = df_ttZ_histos_APV[ij].Clone()
    h_ttZtoQQ_APV = df_ttZtoQQ_histos_APV[ij].Clone()
    h_ttH_APV = df_ttH_histos_APV[ij].Clone()
    h_ttG_APV = df_ttG_histos_APV[ij].Clone()
    h_tttW_APV = df_tttW_histos_APV[ij].Clone()
    h_tttJ_APV = df_tttJ_histos_APV[ij].Clone()
    h_tttt_APV = df_tttt_histos_APV[ij].Clone()
    h_ttZH_APV = df_ttZH_histos_APV[ij].Clone()
    h_ttWH_APV = df_ttWH_histos_APV[ij].Clone()
    h_ttWW_APV = df_ttWW_histos_APV[ij].Clone()
    h_ttWZ_APV = df_ttWZ_histos_APV[ij].Clone()
    h_ttZZ_APV = df_ttZZ_histos_APV[ij].Clone()
    h_tzq_APV = df_tzq_histos_APV[ij].Clone()
    h_TTTo2L_APV = df_TTTo2L_histos_APV[ij].Clone()
    h_DoubleMu_APV = df_DoubleMu_histos_APV[ij].Clone()
    h_SingleMu_APV = df_SingleMu_histos_APV[ij].Clone()
    h_WLLJJ_APV = df_WLLJJ_histos_APV[ij].Clone()
    h_ZZJJTo4L_APV = df_ZZJJTo4L_histos_APV[ij].Clone()
    h_WpWpJJ_EWK_APV = df_WpWpJJ_EWK_histos_APV[ij].Clone()
    h_WpWpJJ_QCD_APV = df_WpWpJJ_QCD_histos_APV[ij].Clone()

    h_DY_postAPV = df_DY_histos_postAPV[ij].Clone()
    h_osWW_postAPV = df_osWW_histos_postAPV[ij].Clone()
    h_ssWW_postAPV = df_ssWW_histos_postAPV[ij].Clone()
    h_WWdps_postAPV = df_WWdps_histos_postAPV[ij].Clone()
    h_WZew_postAPV = df_WZew_histos_postAPV[ij].Clone()
    h_WZqcd_postAPV = df_WZqcd_histos_postAPV[ij].Clone()
    h_ZZ_postAPV = df_ZZ_histos_postAPV[ij].Clone()
    h_ZG_postAPV = df_ZG_histos_postAPV[ij].Clone()
    h_WWW_postAPV = df_WWW_histos_postAPV[ij].Clone()
    h_WWZ_postAPV = df_WWZ_histos_postAPV[ij].Clone()
    h_WZZ_postAPV = df_WZZ_histos_postAPV[ij].Clone()
    h_ZZZ_postAPV = df_ZZZ_histos_postAPV[ij].Clone()
    h_tW_postAPV = df_tW_histos_postAPV[ij].Clone()
    h_tbarW_postAPV = df_tbarW_histos_postAPV[ij].Clone()
    h_ttWtoLNu_postAPV = df_ttWtoLNu_histos_postAPV[ij].Clone()
    h_ttWtoQQ_postAPV = df_ttWtoQQ_histos_postAPV[ij].Clone()
    h_ttZ_postAPV = df_ttZ_histos_postAPV[ij].Clone()
    h_ttZtoQQ_postAPV = df_ttZtoQQ_histos_postAPV[ij].Clone()
    h_ttH_postAPV = df_ttH_histos_postAPV[ij].Clone()
    h_ttG_postAPV = df_ttG_histos_postAPV[ij].Clone()
    h_tttW_postAPV = df_tttW_histos_postAPV[ij].Clone()
    h_tttJ_postAPV = df_tttJ_histos_postAPV[ij].Clone()
    h_tttt_postAPV = df_tttt_histos_postAPV[ij].Clone()
    h_ttZH_postAPV = df_ttZH_histos_postAPV[ij].Clone()
    h_ttWH_postAPV = df_ttWH_histos_postAPV[ij].Clone()
    h_ttWW_postAPV = df_ttWW_histos_postAPV[ij].Clone()
    h_ttWZ_postAPV = df_ttWZ_histos_postAPV[ij].Clone()
    h_ttZZ_postAPV = df_ttZZ_histos_postAPV[ij].Clone()
    h_tzq_postAPV = df_tzq_histos_postAPV[ij].Clone()
    h_TTTo2L_postAPV = df_TTTo2L_histos_postAPV[ij].Clone()
    h_DoubleMu_postAPV = df_DoubleMu_histos_postAPV[ij].Clone()
    h_SingleMu_postAPV = df_SingleMu_histos_postAPV[ij].Clone()
    h_WLLJJ_postAPV = df_WLLJJ_histos_postAPV[ij].Clone()
    h_ZZJJTo4L_postAPV = df_ZZJJTo4L_histos_postAPV[ij].Clone()
    h_WpWpJJ_EWK_postAPV = df_WpWpJJ_EWK_histos_postAPV[ij].Clone()
    h_WpWpJJ_QCD_postAPV = df_WpWpJJ_QCD_histos_postAPV[ij].Clone()
    
    # FakeAPV
    h_fake_DY_APV = df_Fake_DY_histos_APV[ij].Clone()
    h_fake_osWW_APV = df_Fake_osWW_histos_APV[ij].Clone()
    h_fake_ssWW_APV = df_Fake_ssWW_histos_APV[ij].Clone()
    h_fake_WWdps_APV = df_Fake_WWdps_histos_APV[ij].Clone()
    h_fake_WZew_APV = df_Fake_WZew_histos_APV[ij].Clone()
    h_fake_WZqcd_APV = df_Fake_WZqcd_histos_APV[ij].Clone()
    h_fake_ZZ_APV = df_Fake_ZZ_histos_APV[ij].Clone()
    h_fake_ZG_APV = df_Fake_ZG_histos_APV[ij].Clone()
    h_fake_WWW_APV = df_Fake_WWW_histos_APV[ij].Clone()
    h_fake_WWZ_APV = df_Fake_WWZ_histos_APV[ij].Clone()
    h_fake_WZZ_APV = df_Fake_WZZ_histos_APV[ij].Clone()
    h_fake_ZZZ_APV = df_Fake_ZZZ_histos_APV[ij].Clone()
    h_fake_tW_APV = df_Fake_tW_histos_APV[ij].Clone()
    h_fake_tbarW_APV = df_Fake_tbarW_histos_APV[ij].Clone()
    h_fake_ttWtoLNu_APV = df_Fake_ttWtoLNu_histos_APV[ij].Clone()
    h_fake_ttWtoQQ_APV = df_Fake_ttWtoQQ_histos_APV[ij].Clone()
    h_fake_ttZ_APV = df_Fake_ttZ_histos_APV[ij].Clone()
    h_fake_ttZtoQQ_APV = df_Fake_ttZtoQQ_histos_APV[ij].Clone()
    h_fake_ttH_APV = df_Fake_ttH_histos_APV[ij].Clone()
    h_fake_ttG_APV = df_Fake_ttG_histos_APV[ij].Clone()
    h_fake_tttW_APV = df_Fake_tttW_histos_APV[ij].Clone()
    h_fake_tttJ_APV = df_Fake_tttJ_histos_APV[ij].Clone()
    h_fake_tttt_APV = df_Fake_tttt_histos_APV[ij].Clone()
    h_fake_ttZH_APV = df_Fake_ttZH_histos_APV[ij].Clone()
    h_fake_ttWH_APV = df_Fake_ttWH_histos_APV[ij].Clone()
    h_fake_ttWW_APV = df_Fake_ttWW_histos_APV[ij].Clone()
    h_fake_ttWZ_APV = df_Fake_ttWZ_histos_APV[ij].Clone()
    h_fake_ttZZ_APV = df_Fake_ttZZ_histos_APV[ij].Clone()
    h_fake_tzq_APV = df_Fake_tzq_histos_APV[ij].Clone()
    h_fake_TTTo2L_APV = df_Fake_TTTo2L_histos_APV[ij].Clone()
    h_fake_WLLJJ_APV = df_Fake_WLLJJ_histos_APV[ij].Clone()
    h_fake_ZZJJTo4L_APV = df_Fake_ZZJJTo4L_histos_APV[ij].Clone()
    h_fake_WpWpJJ_EWK_APV = df_Fake_WpWpJJ_EWK_histos_APV[ij].Clone()
    h_fake_WpWpJJ_QCD_APV = df_Fake_WpWpJJ_QCD_histos_APV[ij].Clone()
    h_fakelep_DoubleMu_APV = df_FakeLep_DoubleMu_histos_APV[ij].Clone()
    h_fakelep_SingleMu_APV = df_FakeLep_SingleMu_histos_APV[ij].Clone()
    
    h_fake_DY_postAPV = df_Fake_DY_histos_postAPV[ij].Clone()
    h_fake_osWW_postAPV = df_Fake_osWW_histos_postAPV[ij].Clone()
    h_fake_ssWW_postAPV = df_Fake_ssWW_histos_postAPV[ij].Clone()
    h_fake_WWdps_postAPV = df_Fake_WWdps_histos_postAPV[ij].Clone()
    h_fake_WZew_postAPV = df_Fake_WZew_histos_postAPV[ij].Clone()
    h_fake_WZqcd_postAPV = df_Fake_WZqcd_histos_postAPV[ij].Clone()
    h_fake_ZZ_postAPV = df_Fake_ZZ_histos_postAPV[ij].Clone()
    h_fake_ZG_postAPV = df_Fake_ZG_histos_postAPV[ij].Clone()
    h_fake_WWW_postAPV = df_Fake_WWW_histos_postAPV[ij].Clone()
    h_fake_WWZ_postAPV = df_Fake_WWZ_histos_postAPV[ij].Clone()
    h_fake_WZZ_postAPV = df_Fake_WZZ_histos_postAPV[ij].Clone()
    h_fake_ZZZ_postAPV = df_Fake_ZZZ_histos_postAPV[ij].Clone()
    h_fake_tW_postAPV = df_Fake_tW_histos_postAPV[ij].Clone()
    h_fake_tbarW_postAPV = df_Fake_tbarW_histos_postAPV[ij].Clone()
    h_fake_ttWtoLNu_postAPV = df_Fake_ttWtoLNu_histos_postAPV[ij].Clone()
    h_fake_ttWtoQQ_postAPV = df_Fake_ttWtoQQ_histos_postAPV[ij].Clone()
    h_fake_ttZ_postAPV = df_Fake_ttZ_histos_postAPV[ij].Clone()
    h_fake_ttZtoQQ_postAPV = df_Fake_ttZtoQQ_histos_postAPV[ij].Clone()
    h_fake_ttH_postAPV = df_Fake_ttH_histos_postAPV[ij].Clone()
    h_fake_ttG_postAPV = df_Fake_ttG_histos_postAPV[ij].Clone()
    h_fake_tttW_postAPV = df_Fake_tttW_histos_postAPV[ij].Clone()
    h_fake_tttJ_postAPV = df_Fake_tttJ_histos_postAPV[ij].Clone()
    h_fake_tttt_postAPV = df_Fake_tttt_histos_postAPV[ij].Clone()
    h_fake_ttZH_postAPV = df_Fake_ttZH_histos_postAPV[ij].Clone()
    h_fake_ttWH_postAPV = df_Fake_ttWH_histos_postAPV[ij].Clone()
    h_fake_ttWW_postAPV = df_Fake_ttWW_histos_postAPV[ij].Clone()
    h_fake_ttWZ_postAPV = df_Fake_ttWZ_histos_postAPV[ij].Clone()
    h_fake_ttZZ_postAPV = df_Fake_ttZZ_histos_postAPV[ij].Clone()
    h_fake_tzq_postAPV = df_Fake_tzq_histos_postAPV[ij].Clone()
    h_fake_TTTo2L_postAPV = df_Fake_TTTo2L_histos_postAPV[ij].Clone()
    h_fake_WLLJJ_postAPV = df_Fake_WLLJJ_histos_postAPV[ij].Clone()
    h_fake_ZZJJTo4L_postAPV = df_Fake_ZZJJTo4L_histos_postAPV[ij].Clone()
    h_fake_WpWpJJ_EWK_postAPV = df_Fake_WpWpJJ_EWK_histos_postAPV[ij].Clone()
    h_fake_WpWpJJ_QCD_postAPV = df_Fake_WpWpJJ_QCD_histos_postAPV[ij].Clone()
    h_fakelep_DoubleMu_postAPV = df_FakeLep_DoubleMu_histos_postAPV[ij].Clone()
    h_fakelep_SingleMu_postAPV = df_FakeLep_SingleMu_histos_postAPV[ij].Clone()

    # check_histo(h_DY_APV)
    h_DY_APV.Scale(APV_lumi*xsec['DY']/get_mcEventnumber(DY_list_APV))
    # check_histo(h_osWW_APV)
    h_osWW_APV.Scale(APV_lumi*xsec['osWW']/get_mcEventnumber(osWW_list_APV))
    # check_histo(h_ssWW_APV)
    h_ssWW_APV.Scale(1.0)
    # check_histo(h_WWdps_APV)
    h_WWdps_APV.Scale(1.0) 
    # check_histo(h_WZew_APV)
    h_WZew_APV.Scale(1.0)
    # check_histo(h_WZqcd_APV)
    h_WZqcd_APV.Scale(APV_lumi*xsec['WZqcd']/get_mcEventnumber(WZqcd_list_APV))
    # check_histo(h_ZZ_APV)
    h_ZZ_APV.Scale(APV_lumi*xsec['ZZ']/get_mcEventnumber(ZZ_list_APV))
    # check_histo(h_ZG_APV)
    h_ZG_APV.Scale(1.0)
    # check_histo(h_WWW_APV)
    h_WWW_APV.Scale(APV_lumi*xsec['WWW']/get_mcEventnumber(WWW_list_APV))
    # check_histo(h_WWZ_APV)
    h_WWZ_APV.Scale(APV_lumi*xsec['WWZ']/get_mcEventnumber(WWZ_list_APV))
    # check_histo(h_WZZ_APV)
    h_WZZ_APV.Scale(APV_lumi*xsec['WZZ']/get_mcEventnumber(WZZ_list_APV))
    # check_histo(h_ZZZ_APV)
    h_ZZZ_APV.Scale(APV_lumi*xsec['ZZZ']/get_mcEventnumber(ZZZ_list_APV))
    # check_histo(h_tW_APV)
    h_tW_APV.Scale(APV_lumi*xsec['tW']/get_mcEventnumber(tW_list_APV))
    # check_histo(h_tbarW_APV)
    h_tbarW_APV.Scale(APV_lumi*xsec['tbarW']/get_mcEventnumber(tbarW_list_APV))
    # check_histo(h_ttWtoLNu_APV)
    h_ttWtoLNu_APV.Scale(APV_lumi*xsec['TTWtoLNu']/get_mcEventnumber(ttWtoLNu_list_APV))
    # check_histo(h_ttWtoQQ_APV)
    h_ttWtoQQ_APV.Scale(APV_lumi*xsec['TTWtoQQ']/get_mcEventnumber(ttWtoQQ_list_APV))
    # check_histo(h_ttZ_APV)
    h_ttZ_APV.Scale(APV_lumi*xsec['TTZ']/get_mcEventnumber(ttZ_list_APV))
    # check_histo(h_ttZtoQQ_APV)
    h_ttZtoQQ_APV.Scale(APV_lumi*xsec['TTZtoQQ']/get_mcEventnumber(ttZtoQQ_list_APV))
    # check_histo(h_ttH_APV)
    h_ttH_APV.Scale(APV_lumi*xsec['TTH']/get_mcEventnumber(ttH_list_APV))
    # check_histo(h_ttG_APV)
    h_ttG_APV.Scale(1.0)
    # check_histo(h_tttW_APV)
    h_tttW_APV.Scale(APV_lumi*xsec['TTTW']/get_mcEventnumber(tttW_list_APV))
    # check_histo(h_tttJ_APV)
    h_tttJ_APV.Scale(APV_lumi*xsec['TTTJ']/get_mcEventnumber(tttJ_list_APV))
    # check_histo(h_tttt_APV)
    h_tttt_APV.Scale(APV_lumi*xsec['TTTT']/get_mcEventnumber(tttt_list_APV))
    # check_histo(h_ttZH_APV)
    h_ttZH_APV.Scale(APV_lumi*xsec['TTZH']/get_mcEventnumber(ttZH_list_APV))
    # check_histo(h_ttWH_APV)
    h_ttWH_APV.Scale(APV_lumi*xsec['TTWH']/get_mcEventnumber(ttWH_list_APV))
    # check_histo(h_ttWW_APV)
    h_ttWW_APV.Scale(APV_lumi*xsec['TTWW']/get_mcEventnumber(ttWW_list_APV))
    # check_histo(h_ttWZ_APV)
    h_ttWZ_APV.Scale(APV_lumi*xsec['TTWZ']/get_mcEventnumber(ttWZ_list_APV))
    # check_histo(h_ttZZ_APV)
    h_ttZZ_APV.Scale(APV_lumi*xsec['TTZZ']/get_mcEventnumber(ttZZ_list_APV))
    # check_histo(h_tzq_APV)
    h_tzq_APV.Scale(APV_lumi*xsec['tZq']/get_mcEventnumber(tzq_list_APV))
    # check_histo(h_TTTo2L_APV)
    h_TTTo2L_APV.Scale(APV_lumi*xsec['TTTo2L']/get_mcEventnumber(TTTo2L_list_APV))
    h_WLLJJ_APV.Scale(xsec['WLLJJ']/get_mcEventnumber(WLLJJ_list_APV))
    h_ZZJJTo4L_APV.Scale(xsec['ZZJJTo4L']/get_mcEventnumber(ZZJJTo4L_list_APV))
    h_WpWpJJ_EWK_APV.Scale(xsec['WpWpJJ_EWK']/get_mcEventnumber(WpWpJJ_EWK_list_APV))
    h_WpWpJJ_QCD_APV.Scale(xsec['WpWpJJ_QCD']/get_mcEventnumber(WpWpJJ_QCD_list_APV))
    
    ##########
    # postAPV
    ##########
    # check_histo(h_DY_postAPV)
    h_DY_postAPV.Scale(postAPV_lumi*xsec['DY']/get_mcEventnumber(DY_list_postAPV))
    # check_histo(h_osWW_postAPV)
    h_osWW_postAPV.Scale(postAPV_lumi*xsec['osWW']/get_mcEventnumber(osWW_list_postAPV))
    # check_histo(h_ssWW_postAPV)
    h_ssWW_postAPV.Scale(1.0)
    # check_histo(h_WWdps_postAPV)
    h_WWdps_postAPV.Scale(1.0) 
    # check_histo(h_WZew_postAPV)
    h_WZew_postAPV.Scale(1.0)
    # check_histo(h_WZqcd_postAPV)
    h_WZqcd_postAPV.Scale(postAPV_lumi*xsec['WZqcd']/get_mcEventnumber(WZqcd_list_postAPV))
    # check_histo(h_ZZ_postAPV)
    h_ZZ_postAPV.Scale(postAPV_lumi*xsec['ZZ']/get_mcEventnumber(ZZ_list_postAPV))
    # check_histo(h_ZG_postAPV)
    h_ZG_postAPV.Scale(1.0)
    # check_histo(h_WWW_postAPV)
    h_WWW_postAPV.Scale(postAPV_lumi*xsec['WWW']/get_mcEventnumber(WWW_list_postAPV))
    # check_histo(h_WWZ_postAPV)
    h_WWZ_postAPV.Scale(postAPV_lumi*xsec['WWZ']/get_mcEventnumber(WWZ_list_postAPV))
    # check_histo(h_WZZ_postAPV)
    h_WZZ_postAPV.Scale(postAPV_lumi*xsec['WZZ']/get_mcEventnumber(WZZ_list_postAPV))
    # check_histo(h_ZZZ_postAPV)
    h_ZZZ_postAPV.Scale(postAPV_lumi*xsec['ZZZ']/get_mcEventnumber(ZZZ_list_postAPV))
    # check_histo(h_tW_postAPV)
    h_tW_postAPV.Scale(postAPV_lumi*xsec['tW']/get_mcEventnumber(tW_list_postAPV))
    # check_histo(h_tbarW_postAPV)
    h_tbarW_postAPV.Scale(postAPV_lumi*xsec['tbarW']/get_mcEventnumber(tbarW_list_postAPV))
    # check_histo(h_ttWtoLNu_postAPV)
    h_ttWtoLNu_postAPV.Scale(postAPV_lumi*xsec['TTWtoLNu']/get_mcEventnumber(ttWtoLNu_list_postAPV))
    # check_histo(h_ttWtoQQ_postAPV)
    h_ttWtoQQ_postAPV.Scale(postAPV_lumi*xsec['TTWtoQQ']/get_mcEventnumber(ttWtoQQ_list_postAPV))
    # check_histo(h_ttZ_postAPV)
    h_ttZ_postAPV.Scale(postAPV_lumi*xsec['TTZ']/get_mcEventnumber(ttZ_list_postAPV))
    # check_histo(h_ttZtoQQ_postAPV)
    h_ttZtoQQ_postAPV.Scale(postAPV_lumi*xsec['TTZtoQQ']/get_mcEventnumber(ttZtoQQ_list_postAPV))
    # check_histo(h_ttH_postAPV)
    h_ttH_postAPV.Scale(postAPV_lumi*xsec['TTH']/get_mcEventnumber(ttH_list_postAPV))
    # check_histo(h_ttG_postAPV)
    h_ttG_postAPV.Scale(1.0)
    # check_histo(h_tttW_postAPV)
    h_tttW_postAPV.Scale(1.0)
    # check_histo(h_tttJ_postAPV)
    h_tttJ_postAPV.Scale(postAPV_lumi*xsec['TTTJ']/get_mcEventnumber(tttJ_list_postAPV))
    # check_histo(h_tttt_postAPV)
    h_tttt_postAPV.Scale(postAPV_lumi*xsec['TTTT']/get_mcEventnumber(tttt_list_postAPV))
    # check_histo(h_ttZH_postAPV)
    h_ttZH_postAPV.Scale(postAPV_lumi*xsec['TTZH']/get_mcEventnumber(ttZH_list_postAPV))
    # check_histo(h_ttWH_postAPV)
    h_ttWH_postAPV.Scale(postAPV_lumi*xsec['TTWH']/get_mcEventnumber(ttWH_list_postAPV))
    # check_histo(h_ttWW_postAPV)
    h_ttWW_postAPV.Scale(postAPV_lumi*xsec['TTWW']/get_mcEventnumber(ttWW_list_postAPV))
    # check_histo(h_ttWZ_postAPV)
    h_ttWZ_postAPV.Scale(postAPV_lumi*xsec['TTWZ']/get_mcEventnumber(ttWZ_list_postAPV))
    # check_histo(h_ttZZ_postAPV)
    h_ttZZ_postAPV.Scale(postAPV_lumi*xsec['TTZZ']/get_mcEventnumber(ttZZ_list_postAPV))
    # check_histo(h_tzq_postAPV)
    h_tzq_postAPV.Scale(postAPV_lumi*xsec['tZq']/get_mcEventnumber(tzq_list_postAPV))
    # check_histo(h_TTTo2L_postAPV)
    h_TTTo2L_postAPV.Scale(postAPV_lumi*xsec['TTTo2L']/get_mcEventnumber(TTTo2L_list_postAPV))
    h_WLLJJ_postAPV.Scale(xsec['WLLJJ']/get_mcEventnumber(WLLJJ_list_postAPV))
    h_ZZJJTo4L_postAPV.Scale(xsec['ZZJJTo4L']/get_mcEventnumber(ZZJJTo4L_list_postAPV))
    h_WpWpJJ_EWK_postAPV.Scale(xsec['WpWpJJ_EWK']/get_mcEventnumber(WpWpJJ_EWK_list_postAPV))
    h_WpWpJJ_QCD_postAPV.Scale(xsec['WpWpJJ_QCD']/get_mcEventnumber(WpWpJJ_QCD_list_postAPV))

    # Fake (APV)
    h_fake_DY_APV.Scale(APV_lumi*xsec['DY']/get_mcEventnumber(DY_list_APV))
    h_fake_osWW_APV.Scale(APV_lumi*xsec['osWW']/get_mcEventnumber(osWW_list_APV))
    h_fake_ssWW_APV.Scale(1.0)
    h_fake_WWdps_APV.Scale(1.0)
    h_fake_WZew_APV.Scale(1.0)
    h_fake_WZqcd_APV.Scale(APV_lumi*xsec['WZqcd']/get_mcEventnumber(WZqcd_list_APV))
    h_fake_ZZ_APV.Scale(APV_lumi*xsec['ZZ']/get_mcEventnumber(ZZ_list_APV))
    h_fake_ZG_APV.Scale(1.0)
    h_fake_WWW_APV.Scale(APV_lumi*xsec['WWW']/get_mcEventnumber(WWW_list_APV))
    h_fake_WWZ_APV.Scale(APV_lumi*xsec['WWZ']/get_mcEventnumber(WWZ_list_APV))
    h_fake_WZZ_APV.Scale(APV_lumi*xsec['WZZ']/get_mcEventnumber(WZZ_list_APV))
    h_fake_ZZZ_APV.Scale(APV_lumi*xsec['ZZZ']/get_mcEventnumber(ZZZ_list_APV))
    h_fake_tW_APV.Scale(APV_lumi*xsec['tW']/get_mcEventnumber(tW_list_APV))
    h_fake_tbarW_APV.Scale(APV_lumi*xsec['tbarW']/get_mcEventnumber(tbarW_list_APV))
    h_fake_ttWtoLNu_APV.Scale(APV_lumi*xsec['TTWtoLNu']/get_mcEventnumber(ttWtoLNu_list_APV))
    h_fake_ttWtoQQ_APV.Scale(APV_lumi*xsec['TTWtoQQ']/get_mcEventnumber(ttWtoQQ_list_APV))
    h_fake_ttZ_APV.Scale(APV_lumi*xsec['TTZ']/get_mcEventnumber(ttZ_list_APV))
    h_fake_ttZtoQQ_APV.Scale(APV_lumi*xsec['TTZtoQQ']/get_mcEventnumber(ttZtoQQ_list_APV))
    h_fake_ttH_APV.Scale(APV_lumi*xsec['TTH']/get_mcEventnumber(ttH_list_APV))
    h_fake_ttG_APV.Scale(1.0)
    h_fake_tttW_APV.Scale(APV_lumi*xsec['TTTW']/get_mcEventnumber(tttW_list_APV))
    h_fake_tttJ_APV.Scale(APV_lumi*xsec['TTTJ']/get_mcEventnumber(tttJ_list_APV))
    h_fake_tttt_APV.Scale(APV_lumi*xsec['TTTT']/get_mcEventnumber(tttt_list_APV))
    h_fake_ttZH_APV.Scale(APV_lumi*xsec['TTZH']/get_mcEventnumber(ttZH_list_APV))
    h_fake_ttWH_APV.Scale(APV_lumi*xsec['TTWH']/get_mcEventnumber(ttWH_list_APV))
    h_fake_ttWW_APV.Scale(APV_lumi*xsec['TTWW']/get_mcEventnumber(ttWW_list_APV))
    h_fake_ttWZ_APV.Scale(APV_lumi*xsec['TTWZ']/get_mcEventnumber(ttWZ_list_APV))
    h_fake_ttZZ_APV.Scale(APV_lumi*xsec['TTZZ']/get_mcEventnumber(ttZZ_list_APV))
    h_fake_tzq_APV.Scale(APV_lumi*xsec['tZq']/get_mcEventnumber(tzq_list_APV))
    h_fake_TTTo2L_APV.Scale(APV_lumi*xsec['TTTo2L']/get_mcEventnumber(TTTo2L_list_APV))
    h_fake_WLLJJ_APV.Scale(xsec['WLLJJ']/get_mcEventnumber(WLLJJ_list_APV))
    h_fake_ZZJJTo4L_APV.Scale(xsec['ZZJJTo4L']/get_mcEventnumber(ZZJJTo4L_list_APV))
    h_fake_WpWpJJ_EWK_APV.Scale(xsec['WpWpJJ_EWK']/get_mcEventnumber(WpWpJJ_EWK_list_APV))
    h_fake_WpWpJJ_QCD_APV.Scale(xsec['WpWpJJ_QCD']/get_mcEventnumber(WpWpJJ_QCD_list_APV))

    # Fake (postAPV)
    h_fake_DY_postAPV.Scale(postAPV_lumi*xsec['DY']/get_mcEventnumber(DY_list_postAPV))
    h_fake_osWW_postAPV.Scale(postAPV_lumi*xsec['osWW']/get_mcEventnumber(osWW_list_postAPV))
    h_fake_ssWW_postAPV.Scale(1.0)
    h_fake_WWdps_postAPV.Scale(1.0)
    h_fake_WZew_postAPV.Scale(1.0)
    h_fake_WZqcd_postAPV.Scale(postAPV_lumi*xsec['WZqcd']/get_mcEventnumber(WZqcd_list_postAPV))
    h_fake_ZZ_postAPV.Scale(postAPV_lumi*xsec['ZZ']/get_mcEventnumber(ZZ_list_postAPV))
    h_fake_ZG_postAPV.Scale(1.0)
    h_fake_WWW_postAPV.Scale(postAPV_lumi*xsec['WWW']/get_mcEventnumber(WWW_list_postAPV))
    h_fake_WWZ_postAPV.Scale(postAPV_lumi*xsec['WWZ']/get_mcEventnumber(WWZ_list_postAPV))
    h_fake_WZZ_postAPV.Scale(postAPV_lumi*xsec['WZZ']/get_mcEventnumber(WZZ_list_postAPV))
    h_fake_ZZZ_postAPV.Scale(postAPV_lumi*xsec['ZZZ']/get_mcEventnumber(ZZZ_list_postAPV))
    h_fake_tW_postAPV.Scale(postAPV_lumi*xsec['tW']/get_mcEventnumber(tW_list_postAPV))
    h_fake_tbarW_postAPV.Scale(postAPV_lumi*xsec['tbarW']/get_mcEventnumber(tbarW_list_postAPV))
    h_fake_ttWtoLNu_postAPV.Scale(postAPV_lumi*xsec['TTWtoLNu']/get_mcEventnumber(ttWtoLNu_list_postAPV))
    h_fake_ttWtoQQ_postAPV.Scale(postAPV_lumi*xsec['TTWtoQQ']/get_mcEventnumber(ttWtoQQ_list_postAPV))
    h_fake_ttZ_postAPV.Scale(postAPV_lumi*xsec['TTZ']/get_mcEventnumber(ttZ_list_postAPV))
    h_fake_ttZtoQQ_postAPV.Scale(postAPV_lumi*xsec['TTZtoQQ']/get_mcEventnumber(ttZtoQQ_list_postAPV))
    h_fake_ttH_postAPV.Scale(postAPV_lumi*xsec['TTH']/get_mcEventnumber(ttH_list_postAPV))
    h_fake_ttG_postAPV.Scale(1.0)
    h_fake_tttW_postAPV.Scale(1.0)
    h_fake_tttJ_postAPV.Scale(postAPV_lumi*xsec['TTTJ']/get_mcEventnumber(tttJ_list_postAPV))
    h_fake_tttt_postAPV.Scale(postAPV_lumi*xsec['TTTT']/get_mcEventnumber(tttt_list_postAPV))
    h_fake_ttZH_postAPV.Scale(postAPV_lumi*xsec['TTZH']/get_mcEventnumber(ttZH_list_postAPV))
    h_fake_ttWH_postAPV.Scale(postAPV_lumi*xsec['TTWH']/get_mcEventnumber(ttWH_list_postAPV))
    h_fake_ttWW_postAPV.Scale(postAPV_lumi*xsec['TTWW']/get_mcEventnumber(ttWW_list_postAPV))
    h_fake_ttWZ_postAPV.Scale(postAPV_lumi*xsec['TTWZ']/get_mcEventnumber(ttWZ_list_postAPV))
    h_fake_ttZZ_postAPV.Scale(postAPV_lumi*xsec['TTZZ']/get_mcEventnumber(ttZZ_list_postAPV))
    h_fake_tzq_postAPV.Scale(postAPV_lumi*xsec['tZq']/get_mcEventnumber(tzq_list_postAPV))
    h_fake_TTTo2L_postAPV.Scale(postAPV_lumi*xsec['TTTo2L']/get_mcEventnumber(TTTo2L_list_postAPV))
    h_fake_WLLJJ_postAPV.Scale(xsec['WLLJJ']/get_mcEventnumber(WLLJJ_list_postAPV))
    h_fake_ZZJJTo4L_postAPV.Scale(xsec['ZZJJTo4L']/get_mcEventnumber(ZZJJTo4L_list_postAPV))
    h_fake_WpWpJJ_EWK_postAPV.Scale(xsec['WpWpJJ_EWK']/get_mcEventnumber(WpWpJJ_EWK_list_postAPV))
    h_fake_WpWpJJ_QCD_postAPV.Scale(xsec['WpWpJJ_QCD']/get_mcEventnumber(WpWpJJ_QCD_list_postAPV))
    
    # Append final hists
    # function which does hadd 
    h_DY_APV.Add(h_DY_postAPV)
    check_histo(h_DY_APV)
    histos.append(h_DY_APV.Clone())
    h_osWW_APV.Add(h_osWW_postAPV)
    histos.append(h_osWW_APV.Clone())
    h_ssWW_APV.Add(h_ssWW_postAPV)
    histos.append(h_ssWW_APV.Clone())
    h_WWdps_APV.Add(h_WWdps_postAPV)
    histos.append(h_WWdps_APV.Clone())
    h_WZew_APV.Add(h_WZew_postAPV)
    histos.append(h_WZew_APV.Clone())
    h_WZqcd_APV.Add(h_WZqcd_postAPV)
    histos.append(h_WZqcd_APV.Clone())
    h_ZZ_APV.Add(h_ZZ_postAPV)
    histos.append(h_ZZ_APV.Clone())
    h_ZG_APV.Add(h_ZG_postAPV)
    histos.append(h_ZG_APV.Clone())
    h_WWW_APV.Add(h_WWW_postAPV)
    histos.append(h_WWW_APV.Clone())
    h_WWZ_APV.Add(h_WWZ_postAPV)
    histos.append(h_WWZ_APV.Clone())
    h_WZZ_APV.Add(h_WZZ_postAPV)
    histos.append(h_WZZ_APV.Clone())
    h_ZZZ_APV.Add(h_ZZZ_postAPV)
    histos.append(h_ZZZ_APV.Clone())
    h_tW_APV.Add(h_tW_postAPV)
    histos.append(h_tW_APV.Clone())
    h_tbarW_APV.Add(h_tbarW_postAPV)
    histos.append(h_tbarW_APV.Clone())
    h_ttWtoLNu_APV.Add(h_ttWtoLNu_postAPV)
    histos.append(h_ttWtoLNu_APV.Clone())
    h_ttWtoQQ_APV.Add(h_ttWtoQQ_postAPV)
    histos.append(h_ttWtoQQ_APV.Clone())
    h_ttZ_APV.Add(h_ttZ_postAPV)
    histos.append(h_ttZ_APV.Clone())
    h_ttZtoQQ_APV.Add(h_ttZtoQQ_postAPV)
    histos.append(h_ttZtoQQ_APV.Clone())
    h_ttH_APV.Add(h_ttH_postAPV)
    histos.append(h_ttH_APV.Clone())
    h_ttG_APV.Add(h_ttG_postAPV)
    histos.append(h_ttG_APV.Clone())
    h_tttW_APV.Add(h_tttW_postAPV)
    histos.append(h_tttW_APV.Clone())
    h_tttJ_APV.Add(h_tttJ_postAPV)
    histos.append(h_tttJ_APV.Clone())
    h_tttt_APV.Add(h_tttt_postAPV)
    histos.append(h_tttt_APV.Clone())
    h_ttZH_APV.Add(h_ttZH_postAPV)
    histos.append(h_ttZH_APV.Clone())
    h_ttWH_APV.Add(h_ttWH_postAPV)
    histos.append(h_ttWH_APV.Clone())
    h_ttWW_APV.Add(h_ttWW_postAPV)
    histos.append(h_ttWW_APV.Clone())
    h_ttWZ_APV.Add(h_ttWZ_postAPV)
    histos.append(h_ttWZ_APV.Clone())
    h_ttZZ_APV.Add(h_ttZZ_postAPV)
    histos.append(h_ttZZ_APV.Clone())
    h_tzq_APV.Add(h_tzq_postAPV)
    histos.append(h_tzq_APV.Clone())
    h_TTTo2L_APV.Add(h_TTTo2L_postAPV)
    histos.append(h_TTTo2L_APV.Clone())
    
    h_fake_DY_APV.Add(h_fake_DY_postAPV)
    histos.append(h_fake_DY_APV.Clone())
    h_fake_osWW_APV.Add(h_fake_osWW_postAPV)
    histos.append(h_fake_osWW_APV.Clone())
    h_fake_ssWW_APV.Add(h_fake_ssWW_postAPV)
    histos.append(h_fake_ssWW_APV.Clone())
    h_fake_WWdps_APV.Add(h_fake_WWdps_postAPV)
    histos.append(h_fake_WWdps_APV.Clone())
    h_fake_WZew_APV.Add(h_fake_WZew_postAPV)
    histos.append(h_fake_WZew_APV.Clone())
    h_fake_WZqcd_APV.Add(h_fake_WZqcd_postAPV)
    histos.append(h_fake_WZqcd_APV.Clone())
    h_fake_ZZ_APV.Add(h_fake_ZZ_postAPV)
    histos.append(h_fake_ZZ_APV.Clone())
    h_fake_ZG_APV.Add(h_fake_ZG_postAPV)
    histos.append(h_fake_ZG_APV.Clone())
    h_fake_WWW_APV.Add(h_fake_WWW_postAPV)
    histos.append(h_fake_WWW_APV.Clone())
    h_fake_WWZ_APV.Add(h_fake_WWZ_postAPV)
    histos.append(h_fake_WWZ_APV.Clone())
    h_fake_WZZ_APV.Add(h_fake_WZZ_postAPV)
    histos.append(h_fake_WZZ_APV.Clone())
    h_fake_ZZZ_APV.Add(h_fake_ZZZ_postAPV)
    histos.append(h_fake_ZZZ_APV.Clone())
    h_fake_tW_APV.Add(h_fake_tW_postAPV)
    histos.append(h_fake_tW_APV.Clone())
    h_fake_tbarW_APV.Add(h_fake_tbarW_postAPV)
    histos.append(h_fake_tbarW_APV.Clone())
    h_fake_ttWtoLNu_APV.Add(h_fake_ttWtoLNu_postAPV)
    histos.append(h_fake_ttWtoLNu_APV.Clone())
    h_fake_ttWtoQQ_APV.Add(h_fake_ttWtoQQ_postAPV)
    histos.append(h_fake_ttWtoQQ_APV.Clone())
    h_fake_ttZ_APV.Add(h_fake_ttZ_postAPV)
    histos.append(h_fake_ttZ_APV.Clone())
    h_fake_ttZtoQQ_APV.Add(h_fake_ttZtoQQ_postAPV)
    histos.append(h_fake_ttZtoQQ_APV.Clone())
    h_fake_ttH_APV.Add(h_fake_ttH_postAPV)
    histos.append(h_fake_ttH_APV.Clone())
    h_fake_ttG_APV.Add(h_fake_ttG_postAPV)
    histos.append(h_fake_ttG_APV.Clone())
    h_fake_tttW_APV.Add(h_fake_tttW_postAPV)
    histos.append(h_fake_tttW_APV.Clone())
    h_fake_tttJ_APV.Add(h_fake_tttJ_postAPV)
    histos.append(h_fake_tttJ_APV.Clone())
    h_fake_tttt_APV.Add(h_fake_tttt_postAPV)
    histos.append(h_fake_tttt_APV.Clone())
    h_fake_ttZH_APV.Add(h_fake_ttZH_postAPV)
    histos.append(h_fake_ttZH_APV.Clone())
    h_fake_ttWH_APV.Add(h_fake_ttWH_postAPV)
    histos.append(h_fake_ttWH_APV.Clone())
    h_fake_ttWW_APV.Add(h_fake_ttWW_postAPV)
    histos.append(h_fake_ttWW_APV.Clone())
    h_fake_ttWZ_APV.Add(h_fake_ttWZ_postAPV)
    histos.append(h_fake_ttWZ_APV.Clone())
    h_fake_ttZZ_APV.Add(h_fake_ttZZ_postAPV)
    histos.append(h_fake_ttZZ_APV.Clone())
    h_fake_tzq_APV.Add(h_fake_tzq_postAPV)
    histos.append(h_fake_tzq_APV.Clone())
    h_fake_TTTo2L_APV.Add(h_fake_TTTo2L_postAPV)
    histos.append(h_fake_TTTo2L_APV.Clone())
    h_fakelep_DoubleMu_APV.Add(h_fakelep_DoubleMu_postAPV)
    histos.append(h_fakelep_DoubleMu_APV.Clone())
    h_fakelep_SingleMu_APV.Add(h_fakelep_SingleMu_postAPV)
    histos.append(h_fakelep_SingleMu_APV.Clone())
    h_DoubleMu_APV.Add(h_DoubleMu_postAPV)
    histos.append(h_DoubleMu_APV.Clone()) 
    h_SingleMu_APV.Add(h_SingleMu_postAPV)
    histos.append(h_SingleMu_APV.Clone())

    h_WLLJJ_APV.Add(h_WLLJJ_postAPV)
    histos.append(h_WLLJJ_APV.Clone())
    h_ZZJJTo4L_APV.Add(h_ZZJJTo4L_postAPV)
    histos.append(h_ZZJJTo4L_APV.Clone())
    h_WpWpJJ_EWK_APV.Add(h_WpWpJJ_EWK_postAPV)
    histos.append(h_WpWpJJ_EWK_APV.Clone())
    h_WpWpJJ_QCD_APV.Add(h_WpWpJJ_QCD_postAPV)
    histos.append(h_WpWpJJ_QCD_APV.Clone())

    h_fake_WLLJJ_APV.Add(h_fake_WLLJJ_postAPV)
    histos.append(h_fake_WLLJJ_APV.Clone())
    h_fake_ZZJJTo4L_APV.Add(h_fake_ZZJJTo4L_postAPV)
    histos.append(h_fake_ZZJJTo4L_APV.Clone())
    h_fake_WpWpJJ_EWK_APV.Add(h_fake_WpWpJJ_EWK_postAPV)
    histos.append(h_fake_WpWpJJ_EWK_APV.Clone())
    h_fake_WpWpJJ_QCD_APV.Add(h_fake_WpWpJJ_QCD_postAPV)
    histos.append(h_fake_WpWpJJ_QCD_APV.Clone())

    for i in range(0,64):
      histos[i]=overunder_flowbin(histos[i])

    c1 = plot.draw_plots(opts, histos, variables[ij], 0)
    del histos[:]
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  TTC_Analysis(opts)
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

#==============
# Last used:
# python ttc_emu.py --era 2017 --saveDir 2017_em
# python ttc_emu.py --era 2018 --saveDir 2018_em_v0
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

parser.add_argument("-s", "--saveFormats", dest="saveFormats", default = SAVEFORMATS,
                      help="Save formats for all plots [default: %s]" % SAVEFORMATS)

parser.add_argument("--saveDir", dest="saveDir", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

opts = parser.parse_args()

# the EnableImplicitMT option should only use in cluster, at lxplus, it will make the code slower(my experience)
#ROOT.ROOT.EnableImplicitMT()

def get_filelist(path, flist=[]):
  f_list = ROOT.std.vector('string')()
  for f in flist:
    # print (path+f)
    f_list.push_back(path+f)
  return f_list


def histos_book(flist, filters, variables, isData = "False", isFake = "False"):
  # print ("flist: ", str(flist[0]).split('/')[-1])
  df_xyz_tree = ROOT.RDataFrame("Events",flist)

  if not isData:
    df_xyz_tree = df_xyz_tree.Define("trigger_SF","trigger_sf_em_"+opts.era+"(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
    # check if the events are fake or not
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_em_"+opts.era+"(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta, "+str(isData).lower()+")")
      if opts.era == "2017":
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
      else:
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*fakelep_weight*genWeight/abs(genWeight)")
    else:
      if opts.era == "2017":
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*trigger_SF*Muon_CutBased_LooseID_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
      else:
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*trigger_SF*Muon_CutBased_LooseID_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  else:
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_em_"+opts.era+"(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,muon_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta, "+str(isData).lower()+")")

  # common for data/MC
  df_xyz = df_xyz_tree.Filter(filters)
  if not isData:
    df_xyz_trigger = all_trigger(df_xyz, opts.era)
  else:
    if "doubleeg" in str(flist[0]).split('/')[-1].lower():
      print ("doubleEle")
      df_xyz_trigger = for_diele_trigger(df_xyz, opts.era)
    elif "singleeg" in str(flist[0]).split('/')[-1].lower():
      print ("singleEle")
      df_xyz_trigger = for_singleele_trigger_emuchannel(df_xyz, opts.era)
    elif "egamma" in str(flist[0]).split('/')[-1].lower():
      print ("eGamma")
      df_xyz_trigger = for_singleele_trigger_emuchannel(df_xyz, opts.era)
    elif "singlemu" in str(flist[0]).split('/')[-1].lower():
      print ("singleMu")
      df_xyz_trigger = for_singlemuon_trigger_emuchannel(df_xyz, opts.era)
    elif "muoneg" in str(flist[0]).split('/')[-1].lower():
      print ("muonEG")
      df_xyz_trigger = for_cross_trigger(df_xyz, opts.era)
    else:
      print ("choose correct trigger function")
  # put histos in a list
  df_xyz_histos = []
  for variable in variables:
    if not isData:
      df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',ranges[variable][0], ranges[variable][1], ranges[variable][2]), variable,'genweight')
    else:
      if isFake:
        df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',ranges[variable][0], ranges[variable][1], ranges[variable][2]), variable,'fakelep_weight')
      else:
        df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',ranges[variable][0], ranges[variable][1], ranges[variable][2]), variable)
    h = df_xyz_histo.GetValue()
    h.SetDirectory(0)
    df_xyz_histos.append(h.Clone())
    ROOT.TH1.AddDirectory(0)

  return df_xyz_histos

# Data paths
if opts.era == "2017":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/'
elif opts.era == "2018":
  path='/eos/cms/store/group/phys_top/ExtraYukawa/2018/'
else:
  raise Exception ("select correct era!")

if opts.era == "2017":
  print ("Reading 2017 files \n")
  singleMu_names  = get_filelist(path, ["SingleMuonB.root","SingleMuonC.root","SingleMuonD.root","SingleMuonE.root","SingleMuonF.root"])
  singleEle_names = get_filelist(path, ["SingleEGB.root","SingleEGC.root","SingleEGD.root","SingleEGE.root","SingleEGF.root"])
  muonEle_names   = get_filelist(path, ["MuonEGB.root","MuonEGC.root","MuonEGD.root","MuonEGE.root","MuonEGF.root"])
elif opts.era == "2018":
  print ("Reading 2018 files \n")
  singleMu_names = get_filelist(path, ["SingleMuonA.root","SingleMuonB.root","SingleMuonC.root","SingleMuonD_0.root","SingleMuonD_1.root"])
  egamma_names   = get_filelist(path, ["EGammaA.root","EGammaB.root","EGammaC.root","EGammaD_0.root","EGammaD_1.root"])
  muonEle_names   = get_filelist(path, ["MuonEGA.root","MuonEGB.root","MuonEGC.root","MuonEGD_0.root","MuonEGD_1.root"])
else:
  raise Exception ("select correct era!")

# MC samples
DY_list = get_filelist(path, ['DY.root'])
osWW_list = get_filelist(path, ['osWW.root'])
ssWW_list = get_filelist(path, ['ssWW.root'])
WWdps_list = get_filelist(path, ['WWdps.root'])
WZew_list = get_filelist(path, ['WZ_ew.root'])
WZqcd_list = get_filelist(path, ['WZ_qcd.root'])
ZZ_list = get_filelist(path, ['ZZ.root'])
ZG_list = get_filelist(path, ['ZG_ew.root'])
WWW_list = get_filelist(path, ['WWW.root'])
WWZ_list = get_filelist(path, ['WWZ.root'])
WZZ_list = get_filelist(path, ['WZZ.root'])
ZZZ_list = get_filelist(path, ['ZZZ.root'])
tW_list = get_filelist(path, ['tW.root'])
tbarW_list = get_filelist(path, ['tbarW.root'])
ttWtoLNu_list = get_filelist(path, ['ttWtoLNu.root'])
ttWtoQQ_list = get_filelist(path, ['ttWtoQQ.root'])
ttZ_list = get_filelist(path, ['ttZ.root'])
ttZtoQQ_list = get_filelist(path, ['ttZtoQQ.root'])
ttH_list = get_filelist(path, ['ttH.root'])
tttt_list = get_filelist(path, ['tttt.root'])
tttJ_list = get_filelist(path, ['tttJ.root'])
tttW_list = get_filelist(path, ['tttW.root'])
ttG_list = get_filelist(path, ['TTG.root'])
ttZH_list = get_filelist(path, ['ttZH.root'])
ttWH_list = get_filelist(path, ['ttWH.root'])
ttWW_list = get_filelist(path, ['ttWW.root'])
ttWZ_list = get_filelist(path, ['ttWZ.root'])
ttZZ_list = get_filelist(path, ['ttZZ.root'])
tzq_list = get_filelist(path, ['tzq.root'])
TTTo2L_list = get_filelist(path, ['TTTo2L.root'])


def TTC_Analysis(opts):

  histos = []
  
  variables = ranges.keys()
  for ij in range(0,len(variables)):
    print (variables[ij])

  # define the filters here, 1:2mu, 2:1e1m, 3:2ele
  filters_mc="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && ttc_2P0F"
  filters_mc_fake="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
  filters_data="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"
  filters_data_fake="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"

  ##############
  ## DY samples
  ##############
  df_DY_histos = histos_book(DY_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_DY_histos = histos_book(DY_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("DY both genuine and fake histo loading complete!")
  # print ("df_DY_histos[0] integral", df_DY_histos[0].Integral())
  # print ("df_Fake_DY_histos[0] integral", df_Fake_DY_histos[0].Integral())
  # sys.exit(1)
  
  ##############
  ## osWW samples
  ##############
  df_osWW_histos = histos_book(osWW_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_osWW_histos = histos_book(osWW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("osWW both genuine and fake histo loading complete!")
  
  ##############
  ## ssWW samples
  ##############
  df_ssWW_histos = histos_book(ssWW_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ssWW_histos = histos_book(ssWW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ssWW both genuine and fake histo loading complete!")
  
  ##############
  ## WWdps samples
  ##############
  df_WWdps_histos = histos_book(WWdps_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_WWdps_histos = histos_book(WWdps_list, filters_mc_fake, variables, False, True) #isData, isFake 
  print ("WWdps both genuine and fake histo loading complete!")

  ##############
  ## WZew samples
  ##############
  df_WZew_histos = histos_book(WZew_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_WZew_histos = histos_book(WZew_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("WWew both genuine and fake histo loading complete!")
  
  ##############
  ## WZqcd samples
  ##############
  df_WZqcd_histos = histos_book(WZqcd_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_WZqcd_histos = histos_book(WZqcd_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("WZqcd both genuine and fake histo loading complete!")
  
  ##############
  ## ZZ samples
  ##############
  df_ZZ_histos = histos_book(ZZ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ZZ_histos = histos_book(ZZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("zz both genuine and fake histo loading complete!")

  ##############
  ## ZG samples
  ##############
  df_ZG_histos = histos_book(ZG_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ZG_histos = histos_book(ZG_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ZG both genuine and fake histo loading complete!")
  
  ##############
  ## WWW samples
  ##############
  df_WWW_histos = histos_book(WWW_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_WWW_histos = histos_book(WWW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("WWW both genuine and fake histo loading complete!")
  
  ##############
  ## WWZ samples
  ##############
  df_WWZ_histos = histos_book(WWZ_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_WWZ_histos = histos_book(WWZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("WWZ both genuine and fake histo loading complete!")
  
  ##############
  ## WZZ samples
  ##############
  df_WZZ_histos = histos_book(WZZ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_WZZ_histos = histos_book(WZZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("WZZ both genuine and fake histo loading complete!")
  
  ##############
  ## ZZZ samples
  ##############
  df_ZZZ_histos = histos_book(ZZZ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ZZZ_histos = histos_book(ZZZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ZZZ both genuine and fake histo loading complete!")
  
  ##############
  ## tW samples
  ##############
  df_tW_histos = histos_book(tW_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_tW_histos = histos_book(tW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("tW both genuine and fake histo loading complete!")
  
  ##############
  ## tbarW samples
  ##############
  df_tbarW_histos = histos_book(tbarW_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_tbarW_histos = histos_book(tbarW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("tbarW both genuine and fake histo loading complete!")
  
  ##############
  ## ttWtoLNu samples
  ##############
  df_ttWtoLNu_histos = histos_book(ttWtoLNu_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttWtoLNu_histos = histos_book(ttWtoLNu_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttWtoLNu both genuine and fake histo loading complete!")
  
  ##############
  ## ttWtoQQ samples
  ##############
  df_ttWtoQQ_histos = histos_book(ttWtoQQ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttWtoQQ_histos = histos_book(ttWtoQQ_list, filters_mc_fake, variables, False, True) #isData, isFake 
  print ("ttWtoQQ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZ samples
  ##############
  df_ttZ_histos = histos_book(ttZ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttZ_histos = histos_book(ttZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttZ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZtoQQ samples
  ##############
  df_ttZtoQQ_histos = histos_book(ttZtoQQ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttZtoQQ_histos = histos_book(ttZtoQQ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttZtoQQ both genuine and fake histo loading complete!")
  
  ##############
  ## ttH samples
  ##############
  df_ttH_histos = histos_book(ttH_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttH_histos = histos_book(ttH_list, filters_mc_fake, variables, False, True) #isData, isFake 
  print ("ttH both genuine and fake histo loading complete!")
  
  ##############
  ## tttW samples
  ##############
  df_tttW_histos = histos_book(tttW_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_tttW_histos = histos_book(tttW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("tttW both genuine and fake histo loading complete!")
  
  ##############
  ## tttJ samples
  ##############
  df_tttJ_histos = histos_book(tttJ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_tttJ_histos = histos_book(tttJ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("tttJ both genuine and fake histo loading complete!")

  ##############
  ## ttG samples
  ##############
  if opts.era == "2017":
    df_ttG_histos = histos_book(ttG_list, filters_mc, variables, False, False) #isData, isFake
    df_Fake_ttG_histos = histos_book(ttG_list, filters_mc_fake, variables, False, True) #isData, isFake
    print ("ttG both genuine and fake histo loading complete!")
  else:
    print ("ttG histos are taken from tttJ, but Reset to 0!")
    df_ttG_histos = []
    df_Fake_ttG_histos = []
    for ii in range(0,len(variables)):
      h1 = df_tttJ_histos[ii].Clone()
      h1.Reset()
      df_ttG_histos.append(h1.Clone())
      h2 = df_Fake_tttJ_histos[ii].Clone()
      h2.Reset()
      df_Fake_ttG_histos.append(h2.Clone())
  
  ##############
  ## ttWH samples
  ##############
  df_ttWH_histos = histos_book(ttWH_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttWH_histos = histos_book(ttWH_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttWH both genuine and fake histo loading complete!")
  
  ##############
  ## ttZH samples
  ##############
  df_ttZH_histos = histos_book(ttZH_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttZH_histos = histos_book(ttZH_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttZH both genuine and fake histo loading complete!")
  
  ##############
  ## tttt samples
  ##############
  df_tttt_histos = histos_book(tttt_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_tttt_histos = histos_book(tttt_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("tttt both genuine and fake histo loading complete!")
  
  ##############
  ## ttWW samples
  ##############
  df_ttWW_histos = histos_book(ttWW_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttWW_histos = histos_book(ttWW_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttWW both genuine and fake histo loading complete!")
  
  ##############
  ## ttWZ samples
  ##############
  df_ttWZ_histos = histos_book(ttWZ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttWZ_histos = histos_book(ttWZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttWZ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZZ samples
  ##############
  df_ttZZ_histos = histos_book(ttZZ_list, filters_mc, variables, False, False) #isData, isFake
  df_Fake_ttZZ_histos = histos_book(ttZZ_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("ttZZ both genuine and fake histo loading complete!")

  ##############
  ## tzq samples
  ##############
  df_tzq_histos = histos_book(tzq_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_tzq_histos = histos_book(tzq_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("tzq both genuine and fake histo loading complete!")
  
  ##############
  ## TTTo2L samples
  ##############
  df_TTTo2L_histos = histos_book(TTTo2L_list, filters_mc, variables, False, False) #isData, isFake 
  df_Fake_TTTo2L_histos = histos_book(TTTo2L_list, filters_mc_fake, variables, False, True) #isData, isFake
  print ("TTTo2L both genuine and fake histo loading complete!")

  ##############
  ## SingleMu samples 
  ##############
  df_SingleMu_histos = histos_book(singleMu_names, filters_data, variables, True, False) #isData, isFake 
  df_FakeLep_SingleMu_histos = histos_book(singleMu_names, filters_data_fake, variables, True, True) #isData, isFake 
  
  ##############
  ## SingleEle samples
  ##############
  if opts.era == "2017":
    df_SingleEle_histos = histos_book(singleEle_names, filters_data, variables, True, False) #isData, isFake
    df_FakeLep_SingleEle_histos = histos_book(singleEle_names, filters_data_fake, variables, True, True) #isData, isFake
  else:
    print ("NOTE: We are taking EGamma PD for 2018")
    df_SingleEle_histos = histos_book(egamma_names, filters_data, variables, True, False) #isData, isFake
    df_FakeLep_SingleEle_histos = histos_book(egamma_names, filters_data_fake, variables, True, True) #isData, isFake, what is data fake?
  print ("Egamma both genuine and fake histo loading complete!")

  ##############
  ## MuonEle samples
  ##############
  df_MuonEle_histos = histos_book(muonEle_names, filters_data, variables, True, False) #isData, isFake 
  df_FakeLep_MuonEle_histos = histos_book(muonEle_names, filters_data_fake, variables, True, True) #isData, isFake 
  
  # Loop over histograms:  
  for ij in range(0,len(variables)):

    # ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
    #  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})
    print ("Now get values")
    h_DY = df_DY_histos[ij].Clone()
    h_osWW = df_osWW_histos[ij].Clone()
    h_ssWW = df_ssWW_histos[ij].Clone()
    h_WWdps = df_WWdps_histos[ij].Clone()
    h_WZew = df_WZew_histos[ij].Clone()
    h_WZqcd = df_WZqcd_histos[ij].Clone()
    h_ZZ = df_ZZ_histos[ij].Clone()
    h_ZG = df_ZG_histos[ij].Clone()
    h_WWW = df_WWW_histos[ij].Clone()
    h_WWZ = df_WWZ_histos[ij].Clone()
    h_WZZ = df_WZZ_histos[ij].Clone()
    h_ZZZ = df_ZZZ_histos[ij].Clone()
    h_tW = df_tW_histos[ij].Clone()
    h_tbarW = df_tbarW_histos[ij].Clone()
    h_ttWtoLNu = df_ttWtoLNu_histos[ij].Clone()
    h_ttWtoQQ = df_ttWtoQQ_histos[ij].Clone()
    h_ttZ = df_ttZ_histos[ij].Clone()
    h_ttZtoQQ = df_ttZtoQQ_histos[ij].Clone()
    h_ttH = df_ttH_histos[ij].Clone()
    h_ttG = df_ttG_histos[ij].Clone()
    h_tttW = df_tttW_histos[ij].Clone()
    h_tttJ = df_tttJ_histos[ij].Clone()
    h_tttt = df_tttt_histos[ij].Clone()
    h_ttZH = df_ttZH_histos[ij].Clone()
    h_ttWH = df_ttWH_histos[ij].Clone()
    h_ttWW = df_ttWW_histos[ij].Clone()
    h_ttWZ = df_ttWZ_histos[ij].Clone()
    h_ttZZ = df_ttZZ_histos[ij].Clone()
    h_tzq = df_tzq_histos[ij].Clone()
    h_TTTo2L = df_TTTo2L_histos[ij].Clone()
    h_SingleEle = df_SingleEle_histos[ij].Clone()
    h_SingleMu = df_SingleMu_histos[ij].Clone()
    h_MuonEle = df_MuonEle_histos[ij].Clone()
    h_fakelep_SingleEle = df_FakeLep_SingleEle_histos[ij].Clone()
    h_fakelep_SingleMu = df_FakeLep_SingleMu_histos[ij].Clone()
    h_fakelep_MuonEle = df_FakeLep_MuonEle_histos[ij].Clone()
    h_fake_DY = df_Fake_DY_histos[ij].Clone()
    h_fake_osWW = df_Fake_osWW_histos[ij].Clone()
    h_fake_ssWW = df_Fake_ssWW_histos[ij].Clone()
    h_fake_WWdps = df_Fake_WWdps_histos[ij].Clone()
    h_fake_WZew = df_Fake_WZew_histos[ij].Clone()
    h_fake_WZqcd = df_Fake_WZqcd_histos[ij].Clone()
    h_fake_ZZ = df_Fake_ZZ_histos[ij].Clone()
    h_fake_ZG = df_Fake_ZG_histos[ij].Clone()
    h_fake_WWW = df_Fake_WWW_histos[ij].Clone()
    h_fake_WWZ = df_Fake_WWZ_histos[ij].Clone()
    h_fake_WZZ = df_Fake_WZZ_histos[ij].Clone()
    h_fake_ZZZ = df_Fake_ZZZ_histos[ij].Clone()
    h_fake_tW = df_Fake_tW_histos[ij].Clone()
    h_fake_tbarW = df_Fake_tbarW_histos[ij].Clone()
    h_fake_ttWtoLNu = df_Fake_ttWtoLNu_histos[ij].Clone()
    h_fake_ttWtoQQ = df_Fake_ttWtoQQ_histos[ij].Clone()
    h_fake_ttZ = df_Fake_ttZ_histos[ij].Clone()
    h_fake_ttZtoQQ = df_Fake_ttZtoQQ_histos[ij].Clone()
    h_fake_ttH = df_Fake_ttH_histos[ij].Clone()
    h_fake_ttG = df_Fake_ttG_histos[ij].Clone()
    h_fake_tttW = df_Fake_tttW_histos[ij].Clone()
    h_fake_tttJ = df_Fake_tttJ_histos[ij].Clone()
    h_fake_tttt = df_Fake_tttt_histos[ij].Clone()
    h_fake_ttZH = df_Fake_ttZH_histos[ij].Clone()
    h_fake_ttWH = df_Fake_ttWH_histos[ij].Clone()
    h_fake_ttWW = df_Fake_ttWW_histos[ij].Clone()
    h_fake_ttWZ = df_Fake_ttWZ_histos[ij].Clone()
    h_fake_ttZZ = df_Fake_ttZZ_histos[ij].Clone()
    h_fake_tzq = df_Fake_tzq_histos[ij].Clone()
    h_fake_TTTo2L = df_Fake_TTTo2L_histos[ij].Clone()

    h_DY.Scale(xsec['DY']/get_mcEventnumber(DY_list))
    h_osWW.Scale(xsec['osWW']/get_mcEventnumber(osWW_list))
    h_ssWW.Scale(xsec['ssWW']/get_mcEventnumber(ssWW_list))
    h_WWdps.Scale(xsec['WWdps']/get_mcEventnumber(WWdps_list))
    h_WZew.Scale(xsec['WZew']/get_mcEventnumber(WZew_list))
    h_WZqcd.Scale(xsec['WZqcd']/get_mcEventnumber(WZqcd_list))
    h_ZZ.Scale(xsec['ZZ']/get_mcEventnumber(ZZ_list))
    h_ZG.Scale(xsec['ZG']/get_mcEventnumber(ZG_list))
    h_WWW.Scale(xsec['WWW']/get_mcEventnumber(WWW_list))
    h_WWZ.Scale(xsec['WWZ']/get_mcEventnumber(WWZ_list))
    h_WZZ.Scale(xsec['WZZ']/get_mcEventnumber(WZZ_list))
    h_ZZZ.Scale(xsec['ZZZ']/get_mcEventnumber(ZZZ_list))
    h_tW.Scale(xsec['tW']/get_mcEventnumber(tW_list))
    h_tbarW.Scale(xsec['tbarW']/get_mcEventnumber(tbarW_list))
    h_ttWtoLNu.Scale(xsec['TTWtoLNu']/get_mcEventnumber(ttWtoLNu_list))
    h_ttWtoQQ.Scale(xsec['TTWtoQQ']/get_mcEventnumber(ttWtoQQ_list))
    h_ttZ.Scale(xsec['TTZ']/get_mcEventnumber(ttZ_list))
    h_ttZtoQQ.Scale(xsec['TTZtoQQ']/get_mcEventnumber(ttZtoQQ_list))
    h_ttH.Scale(xsec['TTH']/get_mcEventnumber(ttH_list))
    if opts.era == "2017":
      h_ttG.Scale(xsec['TTG']/get_mcEventnumber(ttG_list))
    else:
      h_ttG.Scale(0.0)
    h_tttW.Scale(xsec['TTTW']/get_mcEventnumber(tttW_list))
    h_tttJ.Scale(xsec['TTTJ']/get_mcEventnumber(tttJ_list))
    h_tttt.Scale(xsec['TTTT']/get_mcEventnumber(tttt_list))
    h_ttZH.Scale(xsec['TTZH']/get_mcEventnumber(ttZH_list))
    h_ttWH.Scale(xsec['TTWH']/get_mcEventnumber(ttWH_list))
    h_ttWW.Scale(xsec['TTWW']/get_mcEventnumber(ttWW_list))
    h_ttWZ.Scale(xsec['TTWZ']/get_mcEventnumber(ttWZ_list))
    h_ttZZ.Scale(xsec['TTZZ']/get_mcEventnumber(ttZZ_list))
    h_tzq.Scale(xsec['tZq']/get_mcEventnumber(tzq_list))
    h_TTTo2L.Scale(xsec['TTTo2L']/get_mcEventnumber(TTTo2L_list))

    h_fake_DY.Scale(xsec['DY']/get_mcEventnumber(DY_list))
    h_fake_osWW.Scale(xsec['osWW']/get_mcEventnumber(osWW_list))
    h_fake_ssWW.Scale(xsec['ssWW']/get_mcEventnumber(ssWW_list))
    h_fake_WWdps.Scale(xsec['WWdps']/get_mcEventnumber(WWdps_list))
    h_fake_WZew.Scale(xsec['WZew']/get_mcEventnumber(WZew_list))
    h_fake_WZqcd.Scale(xsec['WZqcd']/get_mcEventnumber(WZqcd_list))
    h_fake_ZZ.Scale(xsec['ZZ']/get_mcEventnumber(ZZ_list))
    h_fake_ZG.Scale(xsec['ZG']/get_mcEventnumber(ZG_list))
    h_fake_WWW.Scale(xsec['WWW']/get_mcEventnumber(WWW_list))
    h_fake_WWZ.Scale(xsec['WWZ']/get_mcEventnumber(WWZ_list))
    h_fake_WZZ.Scale(xsec['WZZ']/get_mcEventnumber(WZZ_list))
    h_fake_ZZZ.Scale(xsec['ZZZ']/get_mcEventnumber(ZZZ_list))
    h_fake_tW.Scale(xsec['tW']/get_mcEventnumber(tW_list))
    h_fake_tbarW.Scale(xsec['tbarW']/get_mcEventnumber(tbarW_list))
    h_fake_ttWtoLNu.Scale(xsec['TTWtoLNu']/get_mcEventnumber(ttWtoLNu_list))
    h_fake_ttWtoQQ.Scale(xsec['TTWtoQQ']/get_mcEventnumber(ttWtoQQ_list))
    h_fake_ttZ.Scale(xsec['TTZ']/get_mcEventnumber(ttZ_list))
    h_fake_ttZtoQQ.Scale(xsec['TTZtoQQ']/get_mcEventnumber(ttZtoQQ_list))
    h_fake_ttH.Scale(xsec['TTH']/get_mcEventnumber(ttH_list))
    if opts.era == "2017":
      h_fake_ttG.Scale(xsec['TTG']/get_mcEventnumber(ttG_list))
    else:
      h_fake_ttG.Scale(0.0)
    h_fake_tttW.Scale(xsec['TTTW']/get_mcEventnumber(tttW_list))
    h_fake_tttJ.Scale(xsec['TTTJ']/get_mcEventnumber(tttJ_list))
    h_fake_tttt.Scale(xsec['TTTT']/get_mcEventnumber(tttt_list))
    h_fake_ttZH.Scale(xsec['TTZH']/get_mcEventnumber(ttZH_list))
    h_fake_ttWH.Scale(xsec['TTWH']/get_mcEventnumber(ttWH_list))
    h_fake_ttWW.Scale(xsec['TTWW']/get_mcEventnumber(ttWW_list))
    h_fake_ttWZ.Scale(xsec['TTWZ']/get_mcEventnumber(ttWZ_list))
    h_fake_ttZZ.Scale(xsec['TTZZ']/get_mcEventnumber(ttZZ_list))
    h_fake_tzq.Scale(xsec['tZq']/get_mcEventnumber(tzq_list))
    h_fake_TTTo2L.Scale(xsec['TTTo2L']/get_mcEventnumber(TTTo2L_list))

    
    histos.append(h_DY.Clone())
    histos.append(h_osWW.Clone())
    histos.append(h_ssWW.Clone())
    histos.append(h_WWdps.Clone())
    histos.append(h_WZew.Clone())
    histos.append(h_WZqcd.Clone())
    histos.append(h_ZZ.Clone())
    histos.append(h_ZG.Clone())
    histos.append(h_WWW.Clone())
    histos.append(h_WWZ.Clone())
    histos.append(h_WZZ.Clone())
    histos.append(h_ZZZ.Clone())
    histos.append(h_tW.Clone())
    histos.append(h_tbarW.Clone())
    histos.append(h_ttWtoLNu.Clone())
    histos.append(h_ttWtoQQ.Clone())
    histos.append(h_ttZ.Clone())
    histos.append(h_ttZtoQQ.Clone())
    histos.append(h_ttH.Clone())
    histos.append(h_ttG.Clone())
    histos.append(h_tttW.Clone())
    histos.append(h_tttJ.Clone())
    histos.append(h_tttt.Clone())
    histos.append(h_ttZH.Clone())
    histos.append(h_ttWH.Clone())
    histos.append(h_ttWW.Clone())
    histos.append(h_ttWZ.Clone())
    histos.append(h_ttZZ.Clone())
    histos.append(h_tzq.Clone())
    histos.append(h_TTTo2L.Clone())
    histos.append(h_fake_DY.Clone())
    histos.append(h_fake_osWW.Clone())
    histos.append(h_fake_ssWW.Clone())
    histos.append(h_fake_WWdps.Clone())
    histos.append(h_fake_WZew.Clone())
    histos.append(h_fake_WZqcd.Clone())
    histos.append(h_fake_ZZ.Clone())
    histos.append(h_fake_ZG.Clone())
    histos.append(h_fake_WWW.Clone())
    histos.append(h_fake_WWZ.Clone())
    histos.append(h_fake_WZZ.Clone())
    histos.append(h_fake_ZZZ.Clone())
    histos.append(h_fake_tW.Clone())
    histos.append(h_fake_tbarW.Clone())
    histos.append(h_fake_ttWtoLNu.Clone())
    histos.append(h_fake_ttWtoQQ.Clone())
    histos.append(h_fake_ttZ.Clone())
    histos.append(h_fake_ttZtoQQ.Clone())
    histos.append(h_fake_ttH.Clone())
    histos.append(h_fake_ttG.Clone())
    histos.append(h_fake_tttW.Clone())
    histos.append(h_fake_tttJ.Clone())
    histos.append(h_fake_tttt.Clone())
    histos.append(h_fake_ttZH.Clone())
    histos.append(h_fake_ttWH.Clone())
    histos.append(h_fake_ttWW.Clone())
    histos.append(h_fake_ttWZ.Clone())
    histos.append(h_fake_ttZZ.Clone())
    histos.append(h_fake_tzq.Clone())
    histos.append(h_fake_TTTo2L.Clone())
    histos.append(h_fakelep_SingleMu.Clone())
    histos.append(h_fakelep_SingleEle.Clone())
    histos.append(h_SingleEle.Clone())
    histos.append(h_SingleMu.Clone())
    histos.append(h_fakelep_MuonEle.Clone())
    histos.append(h_MuonEle.Clone())

    for i in range(0,66):
      histos[i]=overunder_flowbin(histos[i])

    c1 = plot.draw_plots(opts, histos, 1, variables[ij], 1)
    del histos[:]
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  TTC_Analysis(opts)
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

import ROOT
import time
import os
import sys
import math
from math import sqrt
import plot

ROOT.gROOT.SetBatch(True)

TTC_header_path = os.path.join("TTC.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

# the EnableImplicitMT option should only use in cluster, at lxplus, it will make the code slower(my experience)
#ROOT.ROOT.EnableImplicitMT()

def overunder_flowbin(h1):
  h1.SetBinContent(1,h1.GetBinContent(0)+h1.GetBinContent(1))
  h1.SetBinError(1,sqrt(h1.GetBinError(0)*h1.GetBinError(0)+h1.GetBinError(1)*h1.GetBinError(1)))
  h1.SetBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX())+h1.GetBinContent(h1.GetNbinsX()+1))
  h1.SetBinError(h1.GetNbinsX(),sqrt(h1.GetBinError(h1.GetNbinsX())*h1.GetBinError(h1.GetNbinsX())+h1.GetBinError(h1.GetNbinsX()+1)*h1.GetBinError(h1.GetNbinsX()+1)))
  return h1

def get_mcEventnumber(filename):
  print 'opening file ', filename
  nevent_temp=0
  for i in range(0,len(filename)):
    ftemp=ROOT.TFile.Open(filename[i])
    htemp=ftemp.Get('nEventsGenWeighted')
    nevent_temp=nevent_temp+htemp.GetBinContent(1)
  return nevent_temp


def histos_book(flist, filters, hists_name, histos_bins, histos_bins_low, histos_bins_high, isData = "False", isFake = "False"):
  # print ("flist: ", str(flist[0]).split('/')[-1])
  df_xyz_tree = ROOT.RDataFrame("Events",flist)

  if not isData:
    df_xyz_tree = df_xyz_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
    # check if the events are fake or not
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
      df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
    else:
      df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  else:
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_ee_data(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")

  # common for data/MC
  df_xyz = df_xyz_tree.Filter(filters)
  if not isData:
    df_xyz_trigger = all_trigger(df_xyz)
  else:
    if "doubleeg" in str(flist[0]).split('/')[-1].lower():
      print ("doubleEle")
      df_xyz_trigger = for_diele_trigger(df_xyz)
    elif "singleeg" in str(flist[0]).split('/')[-1].lower():
      print ("singleEle")
      df_xyz_trigger = for_singleele_trigger_eechannel(df_xyz)
    else:
      print ("choose correct trigger function")
  # put histos in a list
  df_xyz_histos = []
  for i in hists_name:
    if not isData:
      df_xyz_histo = df_xyz_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    else:
      if isFake:
        df_xyz_histo = df_xyz_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'fakelep_weight')
      else:
        df_xyz_histo = df_xyz_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    h = df_xyz_histo.GetValue()
    h.SetDirectory(0)
    df_xyz_histos.append(h.Clone())
    ROOT.TH1.AddDirectory(0)

  return df_xyz_histos


def all_trigger(df):
  all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf")
  return all_trigger

def for_diele_trigger(df):
  ditri_ele_trigger = df.Filter("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ")
  return ditri_ele_trigger

def for_singleele_trigger_eechannel(df):
  sin_ele_trigger = df.Filter("!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)")
  return sin_ele_trigger

def for_singleele_trigger_emuchannel(df):
  sin_ele_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)")
  return sin_ele_trigger

def for_dimuon_trigger(df):
  ditri_mu_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)")
  return ditri_mu_trigger

def for_singlemuon_trigger_mumuchannel(df):
  single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27")
  return single_mu_trigger

def for_singlemuon_trigger_emuchannel(df):
  single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27")
  return single_mu_trigger

def for_cross_trigger(df):
  x_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)")
  return x_trigger

path='/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/'

doubleEle_names = ROOT.std.vector('string')()
for f in ["DoubleEGB.root","DoubleEGC.root","DoubleEGD.root","DoubleEGE.root","DoubleEGF.root"]:
  doubleEle_names.push_back(path+f)

singleEle_names = ROOT.std.vector('string')()
for f in ["SingleEGB.root","SingleEGC.root","SingleEGD.root","SingleEGE.root","SingleEGF.root"]:
  singleEle_names.push_back(path+f)

DY_list = ROOT.std.vector('string')()
for f in ['DY.root']:
  DY_list.push_back(path+f)

osWW_list = ROOT.std.vector('string')()
for f in ['osWW.root']:
  osWW_list.push_back(path+f)

ssWW_list = ROOT.std.vector('string')()
for f in ['ssWW.root']:
  ssWW_list.push_back(path+f)

WWdps_list = ROOT.std.vector('string')()
for f in ['WWdps.root']:
  WWdps_list.push_back(path+f)

WZew_list = ROOT.std.vector('string')()
for f in ['WZ_ew.root']:
  WZew_list.push_back(path+f)

WZqcd_list = ROOT.std.vector('string')()
for f in ['WZ_qcd.root']:
  WZqcd_list.push_back(path+f)

ZZ_list = ROOT.std.vector('string')()
for f in ['ZZ.root']:
  ZZ_list.push_back(path+f)

ZG_list = ROOT.std.vector('string')()
for f in ['ZG_ew.root']:
  ZG_list.push_back(path+f)

WWW_list = ROOT.std.vector('string')()
for f in ['WWW.root']:
  WWW_list.push_back(path+f)

WWZ_list = ROOT.std.vector('string')()
for f in ['WWZ.root']:
  WWZ_list.push_back(path+f)

WZZ_list = ROOT.std.vector('string')()
for f in ['WZZ.root']:
  WZZ_list.push_back(path+f)

ZZZ_list = ROOT.std.vector('string')()
for f in ['ZZZ.root']:
  ZZZ_list.push_back(path+f)

tW_list = ROOT.std.vector('string')()
for f in ['tW.root']:
  tW_list.push_back(path+f)

tbarW_list = ROOT.std.vector('string')()
for f in ['tbarW.root']:
  tbarW_list.push_back(path+f)

ttWtoLNu_list = ROOT.std.vector('string')()
for f in ['ttWtoLNu.root']:
  ttWtoLNu_list.push_back(path+f)

ttWtoQQ_list = ROOT.std.vector('string')()
for f in ['ttWtoQQ.root']:
  ttWtoQQ_list.push_back(path+f)

ttZ_list = ROOT.std.vector('string')()
for f in ['ttZ.root']:
  ttZ_list.push_back(path+f)

ttZtoQQ_list = ROOT.std.vector('string')()
for f in ['ttZtoQQ.root']:
  ttZtoQQ_list.push_back(path+f)

ttH_list = ROOT.std.vector('string')()
for f in ['ttH.root']:
  ttH_list.push_back(path+f)

tttt_list = ROOT.std.vector('string')()
for f in ['tttt.root']:
  tttt_list.push_back(path+f)

tttJ_list = ROOT.std.vector('string')()
for f in ['tttJ.root']:
  tttJ_list.push_back(path+f)

tttW_list = ROOT.std.vector('string')()
for f in ['tttW.root']:
  tttW_list.push_back(path+f)

ttG_list = ROOT.std.vector('string')()
for f in ['TTG.root']:
  ttG_list.push_back(path+f)

ttZH_list = ROOT.std.vector('string')()
for f in ['ttZH.root']:
  ttZH_list.push_back(path+f)

ttWH_list = ROOT.std.vector('string')()
for f in ['ttWH.root']:
  ttWH_list.push_back(path+f)

ttWW_list = ROOT.std.vector('string')()
for f in ['ttWW.root']:
  ttWW_list.push_back(path+f)

ttWZ_list = ROOT.std.vector('string')()
for f in ['ttWZ.root']:
  ttWZ_list.push_back(path+f)

ttZZ_list = ROOT.std.vector('string')()
for f in ['ttZZ.root']:
  ttZZ_list.push_back(path+f)

tzq_list = ROOT.std.vector('string')()
for f in ['tzq.root']:
  tzq_list.push_back(path+f)

TTTo2L_list = ROOT.std.vector('string')()
for f in ['TTTo2L.root']:
  TTTo2L_list.push_back(path+f)

#histograms name
hists_name = ['ttc_l1_pt','ttc_l1_eta','ttc_l1_phi','ttc_l2_pt','ttc_l2_eta','ttc_l2_phi','ttc_mll','ttc_drll','ttc_dphill','ttc_met','ttc_met_phi','j1_pt','j1_eta','j1_phi','j1_mass','j2_pt','j2_eta','j2_phi','j2_mass','j3_pt','j3_eta','j3_phi','j3_mass','n_tight_jet','ttc_mllj1','ttc_mllj2','ttc_mllj3','ttc_dr_l1j1','ttc_dr_l1j2','ttc_dr_l1j3','ttc_dr_l2j1','ttc_dr_l2j2','ttc_dr_l2j3']

hists_name = ['ttc_l1_pt']

#histograms bins
histos_bins = {
hists_name[0]:14
#hists_name[1]:12,
#hists_name[2]:10,
#hists_name[3]:10,
#hists_name[4]:12,
#hists_name[5]:10,
#hists_name[6]:14,
#hists_name[7]:12,
#hists_name[8]:10,
#hists_name[9]:10,
#hists_name[10]:10,
#hists_name[11]:12,
#hists_name[12]:10,
#hists_name[13]:10,
#hists_name[14]:10,
#hists_name[15]:8,
#hists_name[16]:10,
#hists_name[17]:10,
#hists_name[18]:10,
#hists_name[19]:8,
#hists_name[20]:10,
#hists_name[21]:10,
#hists_name[22]:10,
#hists_name[23]:10,
#hists_name[24]:10,
#hists_name[25]:10,
#hists_name[26]:10,
#hists_name[27]:10,
#hists_name[28]:10,
#hists_name[29]:10,
#hists_name[30]:10,
#hists_name[31]:10,
#hists_name[32]:10,
}

#low edge
histos_bins_low = {
hists_name[0]:0
#hists_name[1]:-3,
#hists_name[2]:-4,
#hists_name[3]:0,
#hists_name[4]:-3,
#hists_name[5]:-4,
#hists_name[6]:0,
#hists_name[7]:0,
#hists_name[8]:-4,
#hists_name[9]:0,
#hists_name[10]:-4,
#hists_name[11]:0,
#hists_name[12]:-3,
#hists_name[13]:-4,
#hists_name[14]:0,
#hists_name[15]:0,
#hists_name[16]:-3,
#hists_name[17]:-4,
#hists_name[18]:0,
#hists_name[19]:0,
#hists_name[20]:-3,
#hists_name[21]:-4,
#hists_name[22]:0,
#hists_name[23]:0,
#hists_name[24]:0,
#hists_name[25]:0,
#hists_name[26]:0,
#hists_name[27]:0,
#hists_name[28]:0,
#hists_name[29]:0,
#hists_name[30]:0,
#hists_name[31]:0,
#hists_name[32]:0,
}

#high edge
histos_bins_high = {
hists_name[0]:210
#hists_name[1]:3,
#hists_name[2]:4,
#hists_name[3]:100,
#hists_name[4]:3,
#hists_name[5]:4,
#hists_name[6]:280,
#hists_name[7]:3.6,
#hists_name[8]:4,
#hists_name[9]:300,
#hists_name[10]:4,
#hists_name[11]:360,
#hists_name[12]:3,
#hists_name[13]:4,
#hists_name[14]:50,
#hists_name[15]:240,
#hists_name[16]:3,
#hists_name[17]:4,
#hists_name[18]:50,
#hists_name[19]:240,
#hists_name[20]:3,
#hists_name[21]:4,
#hists_name[22]:50,
#hists_name[23]:10,
#hists_name[24]:800,
#hists_name[25]:500,
#hists_name[26]:500,
#hists_name[27]:4,
#hists_name[28]:4,
#hists_name[29]:4,
#hists_name[30]:4,
#hists_name[31]:4,
#hists_name[32]:4,
}

def TTC_Analysis():

  histos = []

  lumi = 41480.

  DY_xs = 6077.22
  DY_ev = get_mcEventnumber(DY_list)

#  # 48.44*0.0623
#  GGHTaTa_xs = 3.018
#  GGHTaTa_ev = get_mcEventnumber(GGHTaTa_list)
#
#  # 48.44*0.218
#  GGHWW_xs = 10.56
#  GGHWW_ev = get_mcEventnumber(GGHWW_list)
#
#  # 48.44*0.0268*0.1*0.2*2
#  GGHZZ2L_xs = 0.052
#  GGHZZ2L_ev = get_mcEventnumber(GGHZZ2L_list)
#
#  # 48.44*0.0268*0.1*0.1
#  GGHZZ4L_xs = 0.013
#  GGHZZ4L_ev = get_mcEventnumber(GGHZZ4L_list)
#
#  # (1.365+0.88)*(1-0.578)
#  VH_xs = 0.947
#  VH_ev = get_mcEventnumber(VH_list)
#
#  # 3.776*0.0623
#  VBFHTaTa_xs = 0.239
#  VBFHTaTa_ev = get_mcEventnumber(VBFHTaTa_list)
#
#  # 3.776*0.218
#  VBFHWW_xs = 0.823
#  VBFHWW_ev = get_mcEventnumber(VBFHWW_list)
#
#  # 3.776*0.0268*0.1*0.2*2
#  VBFHZZ2L_xs = 0.004
#  VBFHZZ2L_ev = get_mcEventnumber(VBFHZZ2L_list)
#
#  # 3.776*0.0268*0.1*0.1
#  VBFHZZ4L_xs = 0.001
#  VBFHZZ4L_ev = get_mcEventnumber(VBFHZZ4L_list)

  osWW_xs = 11.09
  osWW_ev = get_mcEventnumber(osWW_list)

  ssWW_xs = 0.04932
  ssWW_ev = get_mcEventnumber(ssWW_list)

  WWdps_xs = 1.62
  WWdps_ev = get_mcEventnumber(WWdps_list)

  WZew_xs = 0.0163
  WZew_ev = get_mcEventnumber(WZew_list)

  WZqcd_xs = 5.213
  WZqcd_ev = get_mcEventnumber(WZqcd_list)

  ZZ_xs = 0.0086
  ZZ_ev = get_mcEventnumber(ZZ_list)

  ZG_xs = 0.1097
  ZG_ev = get_mcEventnumber(ZG_list)

  WWW_xs = 0.2086
  WWW_ev = get_mcEventnumber(WWW_list)

  WWZ_xs = 0.1707
  WWZ_ev = get_mcEventnumber(WWZ_list)

  WZZ_xs = 0.05709
  WZZ_ev = get_mcEventnumber(WZZ_list)

  ZZZ_xs = 0.01476
  ZZZ_ev = get_mcEventnumber(ZZZ_list)

  TTTo2L_xs = 88.3419
  TTTo2L_ev = get_mcEventnumber(TTTo2L_list)

  TTH_xs = 0.213
  TTH_ev = get_mcEventnumber(ttH_list)

  TTTT_xs = 0.008213
  TTTT_ev = get_mcEventnumber(tttt_list)

  TTTW_xs = 0.0007314
  TTTW_ev = get_mcEventnumber(tttW_list)

  TTTJ_xs = 0.0003974
  TTTJ_ev = get_mcEventnumber(tttJ_list)

  TTG_xs = 3.757
  TTG_ev = get_mcEventnumber(ttG_list)

  TTWH_xs = 0.001141
  TTWH_ev = get_mcEventnumber(ttWH_list)

  TTZH_xs = 0.00113
  TTZH_ev = get_mcEventnumber(ttZH_list)

  TTWtoLNu_xs = 0.1792
  TTWtoLNu_ev = get_mcEventnumber(ttWtoLNu_list)

  TTWtoQQ_xs = 0.3708
  TTWtoQQ_ev = get_mcEventnumber(ttWtoQQ_list)

  TTZ_xs = 0.2589
  TTZ_ev = get_mcEventnumber(ttZ_list)

  TTZtoQQ_xs = 0.6012
  TTZtoQQ_ev = get_mcEventnumber(ttZtoQQ_list)

  TTWW_xs = 0.007003
  TTWW_ev = get_mcEventnumber(ttWW_list)

  TTWZ_xs = 0.002453
  TTWZ_ev = get_mcEventnumber(ttWZ_list)

  TTZZ_xs = 0.001386
  TTZZ_ev = get_mcEventnumber(ttZZ_list)

  tZq_xs = 0.07561
  tZq_ev = get_mcEventnumber(tzq_list)

  tW_xs = 35.85
  tW_ev = get_mcEventnumber(tW_list)

  tbarW_xs = 35.85
  tbarW_ev = get_mcEventnumber(tbarW_list)

  # define the filters here, 1:2mu, 2:1e1m, 3:2ele
  filters_mc="ttc_jets && ttc_region==3 && ttc_l1_pt>40 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && ttc_2P0F && (ttc_mll<75 || ttc_mll>105)"
  filters_mc_fake="ttc_jets && ttc_region==3 && ttc_l1_pt>40 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (ttc_mll<75 || ttc_mll>105)"
  filters_data="ttc_jets && ttc_region==3 && ttc_l1_pt>40 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F && (ttc_mll<75 || ttc_mll>105)"
  filters_data_fake="ttc_jets && ttc_region==3 && ttc_l1_pt>40 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (ttc_mll<75 || ttc_mll>105)"

  
  ##############
  ## DY samples
  ##############
  df_DY_histos = histos_book(DY_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_DY_histos = histos_book(DY_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("DY both genuine and fake histo loading complete!")
  # print ("df_Fake_DY_histos[0] integral", df_Fake_DY_histos[0].Integral())
  
  ##############
  ## osWW samples
  ##############
  df_osWW_histos = histos_book(osWW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_osWW_histos = histos_book(osWW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("osWW both genuine and fake histo loading complete!")
  
  ##############
  ## ssWW samples
  ##############
  df_ssWW_histos = histos_book(ssWW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ssWW_histos = histos_book(ssWW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ssWW both genuine and fake histo loading complete!")
  
  ##############
  ## WWdps samples
  ##############
  df_WWdps_histos = histos_book(WWdps_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_WWdps_histos = histos_book(WWdps_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake 
  print ("WWdps both genuine and fake histo loading complete!")
  
  ##############
  ## WZew samples
  ##############
  df_WZew_histos = histos_book(WZew_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_WZew_histos = histos_book(WZew_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("WWew both genuine and fake histo loading complete!")
  
  ##############
  ## WZqcd samples
  ##############
  df_WZqcd_histos = histos_book(WZqcd_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_WZqcd_histos = histos_book(WZqcd_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("WZqcd both genuine and fake histo loading complete!")
  
  ##############
  ## ZZ samples
  ##############
  df_ZZ_histos = histos_book(ZZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ZZ_histos = histos_book(ZZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("zz both genuine and fake histo loading complete!")
  
  ##############
  ## ZG samples
  ##############
  df_ZG_histos = histos_book(ZG_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ZG_histos = histos_book(ZG_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ZG both genuine and fake histo loading complete!")
  
  ##############
  ## WWW samples
  ##############
  df_WWW_histos = histos_book(WWW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_WWW_histos = histos_book(WWW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("WWW both genuine and fake histo loading complete!")
  
  ##############
  ## WWZ samples
  ##############
  df_WWZ_histos = histos_book(WWZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_WWZ_histos = histos_book(WWZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("WWZ both genuine and fake histo loading complete!")
  
  ##############
  ## WZZ samples
  ##############
  df_WZZ_histos = histos_book(WZZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_WZZ_histos = histos_book(WZZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("WZZ both genuine and fake histo loading complete!")
  
  ##############
  ## ZZZ samples
  ##############
  df_ZZZ_histos = histos_book(ZZZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ZZZ_histos = histos_book(ZZZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ZZZ both genuine and fake histo loading complete!")
  
  ##############
  ## tW samples
  ##############
  df_tW_histos = histos_book(tW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_tW_histos = histos_book(tW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("tW both genuine and fake histo loading complete!")
  
  ##############
  ## tbarW samples
  ##############
  df_tbarW_histos = histos_book(tbarW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_tbarW_histos = histos_book(tbarW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("tbarW both genuine and fake histo loading complete!")
  
  ##############
  ## ttWtoLNu samples
  ##############
  df_ttWtoLNu_histos = histos_book(ttWtoLNu_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttWtoLNu_histos = histos_book(ttWtoLNu_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttWtoLNu both genuine and fake histo loading complete!")
  
  ##############
  ## ttWtoQQ samples
  ##############
  df_ttWtoQQ_histos = histos_book(ttWtoQQ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttWtoQQ_histos = histos_book(ttWtoQQ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake 
  print ("ttWtoQQ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZ samples
  ##############
  df_ttZ_histos = histos_book(ttZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttZ_histos = histos_book(ttZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttZ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZtoQQ samples
  ##############
  df_ttZtoQQ_histos = histos_book(ttZtoQQ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttZtoQQ_histos = histos_book(ttZtoQQ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttZtoQQ both genuine and fake histo loading complete!")
  
  ##############
  ## ttH samples
  ##############
  df_ttH_histos = histos_book(ttH_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttH_histos = histos_book(ttH_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake 
  print ("ttH both genuine and fake histo loading complete!")
  
  ##############
  ## tttW samples
  ##############
  df_tttW_histos = histos_book(tttW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_tttW_histos = histos_book(tttW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("tttW both genuine and fake histo loading complete!")
  
  ##############
  ## tttJ samples
  ##############
  df_tttJ_histos = histos_book(tttJ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_tttJ_histos = histos_book(tttJ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("tttJ both genuine and fake histo loading complete!")
  
  ##############
  ## ttG samples
  ##############
  df_ttG_histos = histos_book(ttG_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttG_histos = histos_book(ttG_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttG both genuine and fake histo loading complete!")
  
  ##############
  ## ttWH samples
  ##############
  df_ttWH_histos = histos_book(ttWH_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttWH_histos = histos_book(ttWH_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttWH both genuine and fake histo loading complete!")
  
  ##############
  ## ttZH samples
  ##############
  df_ttZH_histos = histos_book(ttZH_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttZH_histos = histos_book(ttZH_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttZH both genuine and fake histo loading complete!")
  
  ##############
  ## tttt samples
  ##############
  df_tttt_histos = histos_book(tttt_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_tttt_histos = histos_book(tttt_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("tttt both genuine and fake histo loading complete!")
  
  ##############
  ## ttWW samples
  ##############
  df_ttWW_histos = histos_book(ttWW_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttWW_histos = histos_book(ttWW_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttWW both genuine and fake histo loading complete!")
  
  ##############
  ## ttWZ samples
  ##############
  df_ttWZ_histos = histos_book(ttWZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttWZ_histos = histos_book(ttWZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttWZ both genuine and fake histo loading complete!")
  
  ##############
  ## ttZZ samples
  ##############
  df_ttZZ_histos = histos_book(ttZZ_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake
  df_Fake_ttZZ_histos = histos_book(ttZZ_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("ttZZ both genuine and fake histo loading complete!")
  
  ##############
  ## tzq samples
  ##############
  df_tzq_histos = histos_book(tzq_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_tzq_histos = histos_book(tzq_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("tzq both genuine and fake histo loading complete!")
  
  ##############
  ## TTTo2L samples
  ##############
  df_TTTo2L_histos = histos_book(TTTo2L_list, filters_mc, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, False) #isData, isFake 
  df_Fake_TTTo2L_histos = histos_book(TTTo2L_list, filters_mc_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, False, True) #isData, isFake
  print ("TTTo2L both genuine and fake histo loading complete!")

  
  ##############
  ## DoubleEle samples
  ##############
  df_DoubleEle_histos = histos_book(doubleEle_names, filters_data, hists_name, histos_bins, histos_bins_low, histos_bins_high, True, False) #isData, isFake
  df_FakeLep_DoubleEle_histos = histos_book(doubleEle_names, filters_data_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, True, True) #isData, isFake, what is data fake?
  print ("DoubleEle both genuine and fake histo loading complete!")
  
  ##############
  ## SingleEle samples
  ##############
  df_SingleEle_histos = histos_book(singleEle_names, filters_data, hists_name, histos_bins, histos_bins_low, histos_bins_high, True, False) #isData, isFake
  df_FakeLep_SingleEle_histos = histos_book(singleEle_names, filters_data_fake, hists_name, histos_bins, histos_bins_low, histos_bins_high, True, True) #isData, isFake
  print ("SingleEle both genuine and fake histo loading complete!")

  
  for ij in range(0,len(hists_name)):
  
# ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
#  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

    print ("Now get values")
    h_DY = df_DY_histos[ij].Clone()
    # print ("h_DY.Integral()", h_DY.Integral())
    # sys.exit(1)
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
    h_DoubleEle = df_DoubleEle_histos[ij].Clone()
    h_SingleEle = df_SingleEle_histos[ij].Clone()
    h_fakelep_DoubleEle = df_FakeLep_DoubleEle_histos[ij].Clone()
    h_fakelep_SingleEle = df_FakeLep_SingleEle_histos[ij].Clone()
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

    h_DY.Scale(DY_xs/DY_ev)
    h_osWW.Scale(osWW_xs/osWW_ev)
    h_ssWW.Scale(ssWW_xs/ssWW_ev)
    h_WWdps.Scale(WWdps_xs/WWdps_ev)
    h_WZew.Scale(WZew_xs/WZew_ev)
    h_WZqcd.Scale(WZqcd_xs/WZqcd_ev)
    h_ZZ.Scale(ZZ_xs/ZZ_ev)
    h_ZG.Scale(ZG_xs/ZG_ev)
    h_WWW.Scale(WWW_xs/WWW_ev)
    h_WWZ.Scale(WWZ_xs/WWZ_ev)
    h_WZZ.Scale(WZZ_xs/WZZ_ev)
    h_ZZZ.Scale(ZZZ_xs/ZZZ_ev)
    h_tW.Scale(tW_xs/tW_ev)
    h_tbarW.Scale(tbarW_xs/tbarW_ev)
    h_ttWtoLNu.Scale(TTWtoLNu_xs/TTWtoLNu_ev)
    h_ttWtoQQ.Scale(TTWtoQQ_xs/TTWtoQQ_ev)
    h_ttZ.Scale(TTZ_xs/TTZ_ev)
    h_ttZtoQQ.Scale(TTZtoQQ_xs/TTZtoQQ_ev)
    h_ttH.Scale(TTH_xs/TTH_ev)
    h_ttG.Scale(TTG_xs/TTG_ev)
    h_tttW.Scale(TTTW_xs/TTTW_ev)
    h_tttJ.Scale(TTTJ_xs/TTTJ_ev)
    h_tttt.Scale(TTTT_xs/TTTT_ev)
    h_ttZH.Scale(TTZH_xs/TTZH_ev)
    h_ttWH.Scale(TTWH_xs/TTWH_ev)
    h_ttWW.Scale(TTWW_xs/TTWW_ev)
    h_ttWZ.Scale(TTWZ_xs/TTWZ_ev)
    h_ttZZ.Scale(TTZZ_xs/TTZZ_ev)
    h_tzq.Scale(tZq_xs/tZq_ev)
    h_TTTo2L.Scale(TTTo2L_xs/TTTo2L_ev)

    h_fake_DY.Scale(DY_xs/DY_ev)
    h_fake_osWW.Scale(osWW_xs/osWW_ev)
    h_fake_ssWW.Scale(ssWW_xs/ssWW_ev)
    h_fake_WWdps.Scale(WWdps_xs/WWdps_ev)
    h_fake_WZew.Scale(WZew_xs/WZew_ev)
    h_fake_WZqcd.Scale(WZqcd_xs/WZqcd_ev)
    h_fake_ZZ.Scale(ZZ_xs/ZZ_ev)
    h_fake_ZG.Scale(ZG_xs/ZG_ev)
    h_fake_WWW.Scale(WWW_xs/WWW_ev)
    h_fake_WWZ.Scale(WWZ_xs/WWZ_ev)
    h_fake_WZZ.Scale(WZZ_xs/WZZ_ev)
    h_fake_ZZZ.Scale(ZZZ_xs/ZZZ_ev)
    h_fake_tW.Scale(tW_xs/tW_ev)
    h_fake_tbarW.Scale(tbarW_xs/tbarW_ev)
    h_fake_ttWtoLNu.Scale(TTWtoLNu_xs/TTWtoLNu_ev)
    h_fake_ttWtoQQ.Scale(TTWtoQQ_xs/TTWtoQQ_ev)
    h_fake_ttZ.Scale(TTZ_xs/TTZ_ev)
    h_fake_ttZtoQQ.Scale(TTZtoQQ_xs/TTZtoQQ_ev)
    h_fake_ttH.Scale(TTH_xs/TTH_ev)
    h_fake_ttG.Scale(TTG_xs/TTG_ev)
    h_fake_tttW.Scale(TTTW_xs/TTTW_ev)
    h_fake_tttJ.Scale(TTTJ_xs/TTTJ_ev)
    h_fake_tttt.Scale(TTTT_xs/TTTT_ev)
    h_fake_ttZH.Scale(TTZH_xs/TTZH_ev)
    h_fake_ttWH.Scale(TTWH_xs/TTWH_ev)
    h_fake_ttWW.Scale(TTWW_xs/TTWW_ev)
    h_fake_ttWZ.Scale(TTWZ_xs/TTWZ_ev)
    h_fake_ttZZ.Scale(TTZZ_xs/TTZZ_ev)
    h_fake_tzq.Scale(tZq_xs/tZq_ev)
    h_fake_TTTo2L.Scale(TTTo2L_xs/TTTo2L_ev)

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
    histos.append(h_fakelep_DoubleEle.Clone())
    histos.append(h_fakelep_SingleEle.Clone())
    histos.append(h_DoubleEle.Clone()) 
    histos.append(h_SingleEle.Clone())

    for i in range(0,64):
      histos[i]=overunder_flowbin(histos[i])

    c1 = plot.draw_plots(histos, 1, hists_name[ij], 0)
    del histos[:]
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  TTC_Analysis()
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

import ROOT
import time
import os
import math
from math import sqrt
import plot

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

#histograms bins
histos_bins = {
hists_name[0]:14,
hists_name[1]:12,
hists_name[2]:10,
hists_name[3]:10,
hists_name[4]:12,
hists_name[5]:10,
hists_name[6]:14,
hists_name[7]:12,
hists_name[8]:10,
hists_name[9]:10,
hists_name[10]:10,
hists_name[11]:12,
hists_name[12]:10,
hists_name[13]:10,
hists_name[14]:10,
hists_name[15]:8,
hists_name[16]:10,
hists_name[17]:10,
hists_name[18]:10,
hists_name[19]:8,
hists_name[20]:10,
hists_name[21]:10,
hists_name[22]:10,
hists_name[23]:10,
hists_name[24]:10,
hists_name[25]:10,
hists_name[26]:10,
hists_name[27]:10,
hists_name[28]:10,
hists_name[29]:10,
hists_name[30]:10,
hists_name[31]:10,
hists_name[32]:10,
}

#low edge
histos_bins_low = {
hists_name[0]:0,
hists_name[1]:-3,
hists_name[2]:-4,
hists_name[3]:0,
hists_name[4]:-3,
hists_name[5]:-4,
hists_name[6]:0,
hists_name[7]:0,
hists_name[8]:-4,
hists_name[9]:0,
hists_name[10]:-4,
hists_name[11]:0,
hists_name[12]:-3,
hists_name[13]:-4,
hists_name[14]:0,
hists_name[15]:0,
hists_name[16]:-3,
hists_name[17]:-4,
hists_name[18]:0,
hists_name[19]:0,
hists_name[20]:-3,
hists_name[21]:-4,
hists_name[22]:0,
hists_name[23]:0,
hists_name[24]:0,
hists_name[25]:0,
hists_name[26]:0,
hists_name[27]:0,
hists_name[28]:0,
hists_name[29]:0,
hists_name[30]:0,
hists_name[31]:0,
hists_name[32]:0,
}

#high edge
histos_bins_high = {
hists_name[0]:210,
hists_name[1]:3,
hists_name[2]:4,
hists_name[3]:100,
hists_name[4]:3,
hists_name[5]:4,
hists_name[6]:280,
hists_name[7]:3.6,
hists_name[8]:4,
hists_name[9]:300,
hists_name[10]:4,
hists_name[11]:360,
hists_name[12]:3,
hists_name[13]:4,
hists_name[14]:50,
hists_name[15]:240,
hists_name[16]:3,
hists_name[17]:4,
hists_name[18]:50,
hists_name[19]:240,
hists_name[20]:3,
hists_name[21]:4,
hists_name[22]:50,
hists_name[23]:10,
hists_name[24]:800,
hists_name[25]:500,
hists_name[26]:500,
hists_name[27]:4,
hists_name[28]:4,
hists_name[29]:4,
hists_name[30]:4,
hists_name[31]:4,
hists_name[32]:4,
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

  df_DY_tree = ROOT.RDataFrame("Events",DY_list)
  df_DY_tree = df_DY_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_DY_tree = df_DY_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_DY = df_DY_tree.Filter(filters_mc)
  df_DY_trigger = all_trigger(df_DY)
  df_DY_histos=[]
  for i in hists_name:
    df_DY_histo = df_DY_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_DY_histos.append(df_DY_histo)

  df_Fake_DY_tree = ROOT.RDataFrame("Events",DY_list)
  df_Fake_DY_tree = df_Fake_DY_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_DY_tree = df_Fake_DY_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_DY_tree = df_Fake_DY_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_DY = df_Fake_DY_tree.Filter(filters_mc_fake)
  df_Fake_DY_trigger = all_trigger(df_Fake_DY)
  df_Fake_DY_histos=[]
  for i in hists_name:
    df_Fake_DY_histo = df_Fake_DY_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_DY_histos.append(df_Fake_DY_histo)

  df_osWW_tree = ROOT.RDataFrame("Events",osWW_list)
  df_osWW_tree = df_osWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_osWW_tree = df_osWW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_osWW = df_osWW_tree.Filter(filters_mc)
  df_osWW_trigger = all_trigger(df_osWW)
  df_osWW_histos=[]
  for i in hists_name:
    df_osWW_histo = df_osWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_osWW_histos.append(df_osWW_histo)

  df_Fake_osWW_tree = ROOT.RDataFrame("Events",osWW_list)
  df_Fake_osWW_tree = df_Fake_osWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_osWW_tree = df_Fake_osWW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_osWW_tree = df_Fake_osWW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_osWW = df_Fake_osWW_tree.Filter(filters_mc_fake)
  df_Fake_osWW_trigger = all_trigger(df_Fake_osWW)
  df_Fake_osWW_histos=[]
  for i in hists_name:
    df_Fake_osWW_histo = df_Fake_osWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_osWW_histos.append(df_Fake_osWW_histo)

  df_ssWW_tree = ROOT.RDataFrame("Events",ssWW_list)
  df_ssWW_tree = df_ssWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ssWW_tree = df_ssWW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ssWW = df_ssWW_tree.Filter(filters_mc)
  df_ssWW_trigger = all_trigger(df_ssWW)
  df_ssWW_histos=[]
  for i in hists_name:
    df_ssWW_histo = df_ssWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ssWW_histos.append(df_ssWW_histo)

  df_Fake_ssWW_tree = ROOT.RDataFrame("Events",ssWW_list)
  df_Fake_ssWW_tree = df_Fake_ssWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ssWW_tree = df_Fake_ssWW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ssWW_tree = df_Fake_ssWW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ssWW = df_Fake_ssWW_tree.Filter(filters_mc_fake)
  df_Fake_ssWW_trigger = all_trigger(df_Fake_ssWW)
  df_Fake_ssWW_histos=[]
  for i in hists_name:
    df_Fake_ssWW_histo = df_Fake_ssWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ssWW_histos.append(df_Fake_ssWW_histo)

  df_WWdps_tree = ROOT.RDataFrame("Events",WWdps_list)
  df_WWdps_tree = df_WWdps_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_WWdps_tree = df_WWdps_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_WWdps = df_WWdps_tree.Filter(filters_mc)
  df_WWdps_trigger = all_trigger(df_WWdps)
  df_WWdps_histos=[]
  for i in hists_name:
    df_WWdps_histo = df_WWdps_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WWdps_histos.append(df_WWdps_histo)

  df_Fake_WWdps_tree = ROOT.RDataFrame("Events",WWdps_list)
  df_Fake_WWdps_tree = df_Fake_WWdps_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_WWdps_tree = df_Fake_WWdps_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_WWdps_tree = df_Fake_WWdps_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_WWdps = df_Fake_WWdps_tree.Filter(filters_mc_fake)
  df_Fake_WWdps_trigger = all_trigger(df_Fake_WWdps)
  df_Fake_WWdps_histos=[]
  for i in hists_name:
    df_Fake_WWdps_histo = df_Fake_WWdps_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_WWdps_histos.append(df_Fake_WWdps_histo)

  df_WZew_tree = ROOT.RDataFrame("Events",WZew_list)
  df_WZew_tree = df_WZew_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_WZew_tree = df_WZew_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_WZew = df_WZew_tree.Filter(filters_mc)
  df_WZew_trigger = all_trigger(df_WZew)
  df_WZew_histos=[]
  for i in hists_name:
    df_WZew_histo = df_WZew_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WZew_histos.append(df_WZew_histo)

  df_Fake_WZew_tree = ROOT.RDataFrame("Events",WZew_list)
  df_Fake_WZew_tree = df_Fake_WZew_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_WZew_tree = df_Fake_WZew_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_WZew_tree = df_Fake_WZew_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_WZew = df_Fake_WZew_tree.Filter(filters_mc_fake)
  df_Fake_WZew_trigger = all_trigger(df_Fake_WZew)
  df_Fake_WZew_histos=[]
  for i in hists_name:
    df_Fake_WZew_histo = df_Fake_WZew_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_WZew_histos.append(df_Fake_WZew_histo)

  df_WZqcd_tree = ROOT.RDataFrame("Events",WZqcd_list)
  df_WZqcd_tree = df_WZqcd_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_WZqcd_tree = df_WZqcd_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_WZqcd = df_WZqcd_tree.Filter(filters_mc)
  df_WZqcd_trigger = all_trigger(df_WZqcd)
  df_WZqcd_histos=[]
  for i in hists_name:
    df_WZqcd_histo = df_WZqcd_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WZqcd_histos.append(df_WZqcd_histo)

  df_Fake_WZqcd_tree = ROOT.RDataFrame("Events",WZqcd_list)
  df_Fake_WZqcd_tree = df_Fake_WZqcd_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_WZqcd_tree = df_Fake_WZqcd_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_WZqcd_tree = df_Fake_WZqcd_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_WZqcd = df_Fake_WZqcd_tree.Filter(filters_mc_fake)
  df_Fake_WZqcd_trigger = all_trigger(df_Fake_WZqcd)
  df_Fake_WZqcd_histos=[]
  for i in hists_name:
    df_Fake_WZqcd_histo = df_Fake_WZqcd_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_WZqcd_histos.append(df_Fake_WZqcd_histo)

  df_ZZ_tree = ROOT.RDataFrame("Events",ZZ_list)
  df_ZZ_tree = df_ZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ZZ_tree = df_ZZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ZZ = df_ZZ_tree.Filter(filters_mc)
  df_ZZ_trigger = all_trigger(df_ZZ)
  df_ZZ_histos=[]
  for i in hists_name:
    df_ZZ_histo = df_ZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ZZ_histos.append(df_ZZ_histo)

  df_Fake_ZZ_tree = ROOT.RDataFrame("Events",ZZ_list)
  df_Fake_ZZ_tree = df_Fake_ZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ZZ_tree = df_Fake_ZZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ZZ_tree = df_Fake_ZZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ZZ = df_Fake_ZZ_tree.Filter(filters_mc_fake)
  df_Fake_ZZ_trigger = all_trigger(df_Fake_ZZ)
  df_Fake_ZZ_histos=[]
  for i in hists_name:
    df_Fake_ZZ_histo = df_Fake_ZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ZZ_histos.append(df_Fake_ZZ_histo)

  df_ZG_tree = ROOT.RDataFrame("Events",ZG_list)
  df_ZG_tree = df_ZG_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ZG_tree = df_ZG_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ZG = df_ZG_tree.Filter(filters_mc)
  df_ZG_trigger = all_trigger(df_ZG)
  df_ZG_histos=[]
  for i in hists_name:
    df_ZG_histo = df_ZG_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ZG_histos.append(df_ZG_histo)

  df_Fake_ZG_tree = ROOT.RDataFrame("Events",ZG_list)
  df_Fake_ZG_tree = df_Fake_ZG_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ZG_tree = df_Fake_ZG_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ZG_tree = df_Fake_ZG_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ZG = df_Fake_ZG_tree.Filter(filters_mc_fake)
  df_Fake_ZG_trigger = all_trigger(df_Fake_ZG)
  df_Fake_ZG_histos=[]
  for i in hists_name:
    df_Fake_ZG_histo = df_Fake_ZG_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ZG_histos.append(df_Fake_ZG_histo)

  df_WWW_tree = ROOT.RDataFrame("Events",WWW_list)
  df_WWW_tree = df_WWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_WWW_tree = df_WWW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_WWW = df_WWW_tree.Filter(filters_mc)
  df_WWW_trigger = all_trigger(df_WWW)
  df_WWW_histos=[]
  for i in hists_name:
    df_WWW_histo = df_WWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WWW_histos.append(df_WWW_histo)

  df_Fake_WWW_tree = ROOT.RDataFrame("Events",WWW_list)
  df_Fake_WWW_tree = df_Fake_WWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_WWW_tree = df_Fake_WWW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_WWW_tree = df_Fake_WWW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_WWW = df_Fake_WWW_tree.Filter(filters_mc_fake)
  df_Fake_WWW_trigger = all_trigger(df_Fake_WWW)
  df_Fake_WWW_histos=[]
  for i in hists_name:
    df_Fake_WWW_histo = df_Fake_WWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_WWW_histos.append(df_Fake_WWW_histo)

  df_WWZ_tree = ROOT.RDataFrame("Events",WWZ_list)
  df_WWZ_tree = df_WWZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_WWZ_tree = df_WWZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_WWZ = df_WWZ_tree.Filter(filters_mc)
  df_WWZ_trigger = all_trigger(df_WWZ)
  df_WWZ_histos=[]
  for i in hists_name:
    df_WWZ_histo = df_WWZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WWZ_histos.append(df_WWZ_histo)

  df_Fake_WWZ_tree = ROOT.RDataFrame("Events",WWZ_list)
  df_Fake_WWZ_tree = df_Fake_WWZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_WWZ_tree = df_Fake_WWZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_WWZ_tree = df_Fake_WWZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_WWZ = df_Fake_WWZ_tree.Filter(filters_mc_fake)
  df_Fake_WWZ_trigger = all_trigger(df_Fake_WWZ)
  df_Fake_WWZ_histos=[]
  for i in hists_name:
    df_Fake_WWZ_histo = df_Fake_WWZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_WWZ_histos.append(df_Fake_WWZ_histo)

  df_WZZ_tree = ROOT.RDataFrame("Events",WZZ_list)
  df_WZZ_tree = df_WZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_WZZ_tree = df_WZZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_WZZ = df_WZZ_tree.Filter(filters_mc)
  df_WZZ_trigger = all_trigger(df_WZZ)
  df_WZZ_histos=[]
  for i in hists_name:
    df_WZZ_histo = df_WZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WZZ_histos.append(df_WZZ_histo)

  df_Fake_WZZ_tree = ROOT.RDataFrame("Events",WZZ_list)
  df_Fake_WZZ_tree = df_Fake_WZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_WZZ_tree = df_Fake_WZZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_WZZ_tree = df_Fake_WZZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_WZZ = df_Fake_WZZ_tree.Filter(filters_mc_fake)
  df_Fake_WZZ_trigger = all_trigger(df_Fake_WZZ)
  df_Fake_WZZ_histos=[]
  for i in hists_name:
    df_Fake_WZZ_histo = df_Fake_WZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_WZZ_histos.append(df_Fake_WZZ_histo)

  df_ZZZ_tree = ROOT.RDataFrame("Events",ZZZ_list)
  df_ZZZ_tree = df_ZZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ZZZ_tree = df_ZZZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ZZZ = df_ZZZ_tree.Filter(filters_mc)
  df_ZZZ_trigger = all_trigger(df_ZZZ)
  df_ZZZ_histos=[]
  for i in hists_name:
    df_ZZZ_histo = df_ZZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ZZZ_histos.append(df_ZZZ_histo)

  df_Fake_ZZZ_tree = ROOT.RDataFrame("Events",ZZZ_list)
  df_Fake_ZZZ_tree = df_Fake_ZZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ZZZ_tree = df_Fake_ZZZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ZZZ_tree = df_Fake_ZZZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ZZZ = df_Fake_ZZZ_tree.Filter(filters_mc_fake)
  df_Fake_ZZZ_trigger = all_trigger(df_Fake_ZZZ)
  df_Fake_ZZZ_histos=[]
  for i in hists_name:
    df_Fake_ZZZ_histo = df_Fake_ZZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ZZZ_histos.append(df_Fake_ZZZ_histo)

  df_tW_tree = ROOT.RDataFrame("Events",tW_list)
  df_tW_tree = df_tW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_tW_tree = df_tW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_tW = df_tW_tree.Filter(filters_mc)
  df_tW_trigger = all_trigger(df_tW)
  df_tW_histos=[]
  for i in hists_name:
    df_tW_histo = df_tW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_tW_histos.append(df_tW_histo)

  df_Fake_tW_tree = ROOT.RDataFrame("Events",tW_list)
  df_Fake_tW_tree = df_Fake_tW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_tW_tree = df_Fake_tW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_tW_tree = df_Fake_tW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_tW = df_Fake_tW_tree.Filter(filters_mc_fake)
  df_Fake_tW_trigger = all_trigger(df_Fake_tW)
  df_Fake_tW_histos=[]
  for i in hists_name:
    df_Fake_tW_histo = df_Fake_tW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_tW_histos.append(df_Fake_tW_histo)

  df_tbarW_tree = ROOT.RDataFrame("Events",tbarW_list)
  df_tbarW_tree = df_tbarW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_tbarW_tree = df_tbarW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_tbarW = df_tbarW_tree.Filter(filters_mc)
  df_tbarW_trigger = all_trigger(df_tbarW)
  df_tbarW_histos=[]
  for i in hists_name:
    df_tbarW_histo = df_tbarW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_tbarW_histos.append(df_tbarW_histo)

  df_Fake_tbarW_tree = ROOT.RDataFrame("Events",tbarW_list)
  df_Fake_tbarW_tree = df_Fake_tbarW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_tbarW_tree = df_Fake_tbarW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_tbarW_tree = df_Fake_tbarW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_tbarW = df_Fake_tbarW_tree.Filter(filters_mc_fake)
  df_Fake_tbarW_trigger = all_trigger(df_Fake_tbarW)
  df_Fake_tbarW_histos=[]
  for i in hists_name:
    df_Fake_tbarW_histo = df_Fake_tbarW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_tbarW_histos.append(df_Fake_tbarW_histo)

  df_ttWtoLNu_tree = ROOT.RDataFrame("Events",ttWtoLNu_list)
  df_ttWtoLNu_tree = df_ttWtoLNu_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttWtoLNu_tree = df_ttWtoLNu_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttWtoLNu = df_ttWtoLNu_tree.Filter(filters_mc)
  df_ttWtoLNu_trigger = all_trigger(df_ttWtoLNu)
  df_ttWtoLNu_histos=[]
  for i in hists_name:
    df_ttWtoLNu_histo = df_ttWtoLNu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWtoLNu_histos.append(df_ttWtoLNu_histo)

  df_Fake_ttWtoLNu_tree = ROOT.RDataFrame("Events",ttWtoLNu_list)
  df_Fake_ttWtoLNu_tree = df_Fake_ttWtoLNu_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttWtoLNu_tree = df_Fake_ttWtoLNu_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttWtoLNu_tree = df_Fake_ttWtoLNu_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttWtoLNu = df_Fake_ttWtoLNu_tree.Filter(filters_mc_fake)
  df_Fake_ttWtoLNu_trigger = all_trigger(df_Fake_ttWtoLNu)
  df_Fake_ttWtoLNu_histos=[]
  for i in hists_name:
    df_Fake_ttWtoLNu_histo = df_Fake_ttWtoLNu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttWtoLNu_histos.append(df_Fake_ttWtoLNu_histo)

  df_ttWtoQQ_tree = ROOT.RDataFrame("Events",ttWtoQQ_list)
  df_ttWtoQQ_tree = df_ttWtoQQ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttWtoQQ_tree = df_ttWtoQQ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttWtoQQ = df_ttWtoQQ_tree.Filter(filters_mc)
  df_ttWtoQQ_trigger = all_trigger(df_ttWtoQQ)
  df_ttWtoQQ_histos=[]
  for i in hists_name:
    df_ttWtoQQ_histo = df_ttWtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWtoQQ_histos.append(df_ttWtoQQ_histo)

  df_Fake_ttWtoQQ_tree = ROOT.RDataFrame("Events",ttWtoQQ_list)
  df_Fake_ttWtoQQ_tree = df_Fake_ttWtoQQ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttWtoQQ_tree = df_Fake_ttWtoQQ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttWtoQQ_tree = df_Fake_ttWtoQQ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttWtoQQ = df_Fake_ttWtoQQ_tree.Filter(filters_mc_fake)
  df_Fake_ttWtoQQ_trigger = all_trigger(df_Fake_ttWtoQQ)
  df_Fake_ttWtoQQ_histos=[]
  for i in hists_name:
    df_Fake_ttWtoQQ_histo = df_Fake_ttWtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttWtoQQ_histos.append(df_Fake_ttWtoQQ_histo)

  df_ttZ_tree = ROOT.RDataFrame("Events",ttZ_list)
  df_ttZ_tree = df_ttZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttZ_tree = df_ttZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttZ = df_ttZ_tree.Filter(filters_mc)
  df_ttZ_trigger = all_trigger(df_ttZ)
  df_ttZ_histos=[]
  for i in hists_name:
    df_ttZ_histo = df_ttZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZ_histos.append(df_ttZ_histo)

  df_Fake_ttZ_tree = ROOT.RDataFrame("Events",ttZ_list)
  df_Fake_ttZ_tree = df_Fake_ttZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttZ_tree = df_Fake_ttZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttZ_tree = df_Fake_ttZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttZ = df_Fake_ttZ_tree.Filter(filters_mc_fake)
  df_Fake_ttZ_trigger = all_trigger(df_Fake_ttZ)
  df_Fake_ttZ_histos=[]
  for i in hists_name:
    df_Fake_ttZ_histo = df_Fake_ttZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttZ_histos.append(df_Fake_ttZ_histo)

  df_ttZtoQQ_tree = ROOT.RDataFrame("Events",ttZtoQQ_list)
  df_ttZtoQQ_tree = df_ttZtoQQ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttZtoQQ_tree = df_ttZtoQQ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttZtoQQ = df_ttZtoQQ_tree.Filter(filters_mc)
  df_ttZtoQQ_trigger = all_trigger(df_ttZtoQQ)
  df_ttZtoQQ_histos=[]
  for i in hists_name:
    df_ttZtoQQ_histo = df_ttZtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZtoQQ_histos.append(df_ttZtoQQ_histo)

  df_Fake_ttZtoQQ_tree = ROOT.RDataFrame("Events",ttZtoQQ_list)
  df_Fake_ttZtoQQ_tree = df_Fake_ttZtoQQ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttZtoQQ_tree = df_Fake_ttZtoQQ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttZtoQQ_tree = df_Fake_ttZtoQQ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttZtoQQ = df_Fake_ttZtoQQ_tree.Filter(filters_mc_fake)
  df_Fake_ttZtoQQ_trigger = all_trigger(df_Fake_ttZtoQQ)
  df_Fake_ttZtoQQ_histos=[]
  for i in hists_name:
    df_Fake_ttZtoQQ_histo = df_Fake_ttZtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttZtoQQ_histos.append(df_Fake_ttZtoQQ_histo)

  df_ttH_tree = ROOT.RDataFrame("Events",ttH_list)
  df_ttH_tree = df_ttH_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttH_tree = df_ttH_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttH = df_ttH_tree.Filter(filters_mc)
  df_ttH_trigger = all_trigger(df_ttH)
  df_ttH_histos=[]
  for i in hists_name:
    df_ttH_histo = df_ttH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttH_histos.append(df_ttH_histo)

  df_Fake_ttH_tree = ROOT.RDataFrame("Events",ttH_list)
  df_Fake_ttH_tree = df_Fake_ttH_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttH_tree = df_Fake_ttH_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttH_tree = df_Fake_ttH_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttH = df_Fake_ttH_tree.Filter(filters_mc_fake)
  df_Fake_ttH_trigger = all_trigger(df_Fake_ttH)
  df_Fake_ttH_histos=[]
  for i in hists_name:
    df_Fake_ttH_histo = df_Fake_ttH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttH_histos.append(df_Fake_ttH_histo)

  df_tttW_tree = ROOT.RDataFrame("Events",tttW_list)
  df_tttW_tree = df_tttW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_tttW_tree = df_tttW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_tttW = df_tttW_tree.Filter(filters_mc)
  df_tttW_trigger = all_trigger(df_tttW)
  df_tttW_histos=[]
  for i in hists_name:
    df_tttW_histo = df_tttW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_tttW_histos.append(df_tttW_histo)

  df_Fake_tttW_tree = ROOT.RDataFrame("Events",tttW_list)
  df_Fake_tttW_tree = df_Fake_tttW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_tttW_tree = df_Fake_tttW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_tttW_tree = df_Fake_tttW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_tttW = df_Fake_tttW_tree.Filter(filters_mc_fake)
  df_Fake_tttW_trigger = all_trigger(df_Fake_tttW)
  df_Fake_tttW_histos=[]
  for i in hists_name:
    df_Fake_tttW_histo = df_Fake_tttW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_tttW_histos.append(df_Fake_tttW_histo)

  df_tttJ_tree = ROOT.RDataFrame("Events",tttJ_list)
  df_tttJ_tree = df_tttJ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_tttJ_tree = df_tttJ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_tttJ = df_tttJ_tree.Filter(filters_mc)
  df_tttJ_trigger = all_trigger(df_tttJ)
  df_tttJ_histos=[]
  for i in hists_name:
    df_tttJ_histo = df_tttJ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_tttJ_histos.append(df_tttJ_histo)

  df_Fake_tttJ_tree = ROOT.RDataFrame("Events",tttJ_list)
  df_Fake_tttJ_tree = df_Fake_tttJ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_tttJ_tree = df_Fake_tttJ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_tttJ_tree = df_Fake_tttJ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_tttJ = df_Fake_tttJ_tree.Filter(filters_mc_fake)
  df_Fake_tttJ_trigger = all_trigger(df_Fake_tttJ)
  df_Fake_tttJ_histos=[]
  for i in hists_name:
    df_Fake_tttJ_histo = df_Fake_tttJ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_tttJ_histos.append(df_Fake_tttJ_histo)

  df_ttG_tree = ROOT.RDataFrame("Events",ttG_list)
  df_ttG_tree = df_ttG_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttG_tree = df_ttG_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttG = df_ttG_tree.Filter(filters_mc)
  df_ttG_trigger = all_trigger(df_ttG)
  df_ttG_histos=[]
  for i in hists_name:
    df_ttG_histo = df_ttG_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttG_histos.append(df_ttG_histo)

  df_Fake_ttG_tree = ROOT.RDataFrame("Events",ttG_list)
  df_Fake_ttG_tree = df_Fake_ttG_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttG_tree = df_Fake_ttG_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttG_tree = df_Fake_ttG_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttG = df_Fake_ttG_tree.Filter(filters_mc_fake)
  df_Fake_ttG_trigger = all_trigger(df_Fake_ttG)
  df_Fake_ttG_histos=[]
  for i in hists_name:
    df_Fake_ttG_histo = df_Fake_ttG_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttG_histos.append(df_Fake_ttG_histo)

  df_ttWH_tree = ROOT.RDataFrame("Events",ttWH_list)
  df_ttWH_tree = df_ttWH_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttWH_tree = df_ttWH_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttWH = df_ttWH_tree.Filter(filters_mc)
  df_ttWH_trigger = all_trigger(df_ttWH)
  df_ttWH_histos=[]
  for i in hists_name:
    df_ttWH_histo = df_ttWH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWH_histos.append(df_ttWH_histo)

  df_Fake_ttWH_tree = ROOT.RDataFrame("Events",ttWH_list)
  df_Fake_ttWH_tree = df_Fake_ttWH_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttWH_tree = df_Fake_ttWH_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttWH_tree = df_Fake_ttWH_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttWH = df_Fake_ttWH_tree.Filter(filters_mc_fake)
  df_Fake_ttWH_trigger = all_trigger(df_Fake_ttWH)
  df_Fake_ttWH_histos=[]
  for i in hists_name:
    df_Fake_ttWH_histo = df_Fake_ttWH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttWH_histos.append(df_Fake_ttWH_histo)

  df_ttZH_tree = ROOT.RDataFrame("Events",ttZH_list)
  df_ttZH_tree = df_ttZH_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttZH_tree = df_ttZH_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttZH = df_ttZH_tree.Filter(filters_mc)
  df_ttZH_trigger = all_trigger(df_ttZH)
  df_ttZH_histos=[]
  for i in hists_name:
    df_ttZH_histo = df_ttZH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZH_histos.append(df_ttZH_histo)

  df_Fake_ttZH_tree = ROOT.RDataFrame("Events",ttZH_list)
  df_Fake_ttZH_tree = df_Fake_ttZH_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttZH_tree = df_Fake_ttZH_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttZH_tree = df_Fake_ttZH_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttZH = df_Fake_ttZH_tree.Filter(filters_mc_fake)
  df_Fake_ttZH_trigger = all_trigger(df_Fake_ttZH)
  df_Fake_ttZH_histos=[]
  for i in hists_name:
    df_Fake_ttZH_histo = df_Fake_ttZH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttZH_histos.append(df_Fake_ttZH_histo)

  df_tttt_tree = ROOT.RDataFrame("Events",tttt_list)
  df_tttt_tree = df_tttt_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_tttt_tree = df_tttt_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_tttt = df_tttt_tree.Filter(filters_mc)
  df_tttt_trigger = all_trigger(df_tttt)
  df_tttt_histos=[]
  for i in hists_name:
    df_tttt_histo = df_tttt_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_tttt_histos.append(df_tttt_histo)

  df_Fake_tttt_tree = ROOT.RDataFrame("Events",tttt_list)
  df_Fake_tttt_tree = df_Fake_tttt_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_tttt_tree = df_Fake_tttt_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_tttt_tree = df_Fake_tttt_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_tttt = df_Fake_tttt_tree.Filter(filters_mc_fake)
  df_Fake_tttt_trigger = all_trigger(df_Fake_tttt)
  df_Fake_tttt_histos=[]
  for i in hists_name:
    df_Fake_tttt_histo = df_Fake_tttt_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_tttt_histos.append(df_Fake_tttt_histo)

  df_ttWW_tree = ROOT.RDataFrame("Events",ttWW_list)
  df_ttWW_tree = df_ttWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttWW_tree = df_ttWW_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttWW = df_ttWW_tree.Filter(filters_mc)
  df_ttWW_trigger = all_trigger(df_ttWW)
  df_ttWW_histos=[]
  for i in hists_name:
    df_ttWW_histo = df_ttWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWW_histos.append(df_ttWW_histo)

  df_Fake_ttWW_tree = ROOT.RDataFrame("Events",ttWW_list)
  df_Fake_ttWW_tree = df_Fake_ttWW_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttWW_tree = df_Fake_ttWW_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttWW_tree = df_Fake_ttWW_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttWW = df_Fake_ttWW_tree.Filter(filters_mc_fake)
  df_Fake_ttWW_trigger = all_trigger(df_Fake_ttWW)
  df_Fake_ttWW_histos=[]
  for i in hists_name:
    df_Fake_ttWW_histo = df_Fake_ttWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttWW_histos.append(df_Fake_ttWW_histo)

  df_ttWZ_tree = ROOT.RDataFrame("Events",ttWZ_list)
  df_ttWZ_tree = df_ttWZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttWZ_tree = df_ttWZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttWZ = df_ttWZ_tree.Filter(filters_mc)
  df_ttWZ_trigger = all_trigger(df_ttWZ)
  df_ttWZ_histos=[]
  for i in hists_name:
    df_ttWZ_histo = df_ttWZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWZ_histos.append(df_ttWZ_histo)

  df_Fake_ttWZ_tree = ROOT.RDataFrame("Events",ttWZ_list)
  df_Fake_ttWZ_tree = df_Fake_ttWZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttWZ_tree = df_Fake_ttWZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttWZ_tree = df_Fake_ttWZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttWZ = df_Fake_ttWZ_tree.Filter(filters_mc_fake)
  df_Fake_ttWZ_trigger = all_trigger(df_Fake_ttWZ)
  df_Fake_ttWZ_histos=[]
  for i in hists_name:
    df_Fake_ttWZ_histo = df_Fake_ttWZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttWZ_histos.append(df_Fake_ttWZ_histo)

  df_ttZZ_tree = ROOT.RDataFrame("Events",ttZZ_list)
  df_ttZZ_tree = df_ttZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_ttZZ_tree = df_ttZZ_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_ttZZ = df_ttZZ_tree.Filter(filters_mc)
  df_ttZZ_trigger = all_trigger(df_ttZZ)
  df_ttZZ_histos=[]
  for i in hists_name:
    df_ttZZ_histo = df_ttZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZZ_histos.append(df_ttZZ_histo)

  df_Fake_ttZZ_tree = ROOT.RDataFrame("Events",ttZZ_list)
  df_Fake_ttZZ_tree = df_Fake_ttZZ_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_ttZZ_tree = df_Fake_ttZZ_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_ttZZ_tree = df_Fake_ttZZ_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_ttZZ = df_Fake_ttZZ_tree.Filter(filters_mc_fake)
  df_Fake_ttZZ_trigger = all_trigger(df_Fake_ttZZ)
  df_Fake_ttZZ_histos=[]
  for i in hists_name:
    df_Fake_ttZZ_histo = df_Fake_ttZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_ttZZ_histos.append(df_Fake_ttZZ_histo)

  df_tzq_tree = ROOT.RDataFrame("Events",tzq_list)
  df_tzq_tree = df_tzq_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_tzq_tree = df_tzq_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_tzq = df_tzq_tree.Filter(filters_mc)
  df_tzq_trigger = all_trigger(df_tzq)
  df_tzq_histos=[]
  for i in hists_name:
    df_tzq_histo = df_tzq_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_tzq_histos.append(df_tzq_histo)

  df_Fake_tzq_tree = ROOT.RDataFrame("Events",tzq_list)
  df_Fake_tzq_tree = df_Fake_tzq_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_tzq_tree = df_Fake_tzq_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_tzq_tree = df_Fake_tzq_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_tzq = df_Fake_tzq_tree.Filter(filters_mc_fake)
  df_Fake_tzq_trigger = all_trigger(df_Fake_tzq)
  df_Fake_tzq_histos=[]
  for i in hists_name:
    df_Fake_tzq_histo = df_Fake_tzq_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_tzq_histos.append(df_Fake_tzq_histo)

  df_TTTo2L_tree = ROOT.RDataFrame("Events",TTTo2L_list)
  df_TTTo2L_tree = df_TTTo2L_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_TTTo2L_tree = df_TTTo2L_tree.Define("genweight","puWeight*PrefireWeight*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  df_TTTo2L = df_TTTo2L_tree.Filter(filters_mc)
  df_TTTo2L_trigger = all_trigger(df_TTTo2L)
  df_TTTo2L_histos=[]
  for i in hists_name:
    df_TTTo2L_histo = df_TTTo2L_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_TTTo2L_histos.append(df_TTTo2L_histo)

  df_Fake_TTTo2L_tree = ROOT.RDataFrame("Events",TTTo2L_list)
  df_Fake_TTTo2L_tree = df_Fake_TTTo2L_tree.Define("trigger_SF","trigger_sf_ee(ttc_l1_pt,ttc_l2_pt,ttc_l1_eta,ttc_l2_eta)")
  df_Fake_TTTo2L_tree = df_Fake_TTTo2L_tree.Define("fakelep_weight","fakelepweight_ee_mc(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_Fake_TTTo2L_tree = df_Fake_TTTo2L_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
  df_Fake_TTTo2L = df_Fake_TTTo2L_tree.Filter(filters_mc_fake)
  df_Fake_TTTo2L_trigger = all_trigger(df_Fake_TTTo2L)
  df_Fake_TTTo2L_histos=[]
  for i in hists_name:
    df_Fake_TTTo2L_histo = df_Fake_TTTo2L_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_Fake_TTTo2L_histos.append(df_Fake_TTTo2L_histo)

  df_DoubleEle_tree = ROOT.RDataFrame("Events", doubleEle_names)
  df_DoubleEle = df_DoubleEle_tree.Filter(filters_data)
  df_DoubleEle_trigger = for_diele_trigger(df_DoubleEle)
  df_DoubleEle_histos=[]
  for i in hists_name:
    df_DoubleEle_histo = df_DoubleEle_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_DoubleEle_histos.append(df_DoubleEle_histo)

  df_SingleEle_tree = ROOT.RDataFrame("Events", singleEle_names)
  df_SingleEle = df_SingleEle_tree.Filter(filters_data)
  df_SingleEle_trigger = for_singleele_trigger_eechannel(df_SingleEle)
  df_SingleEle_histos=[]
  for i in hists_name:
    df_SingleEle_histo = df_SingleEle_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_SingleEle_histos.append(df_SingleEle_histo)

  df_FakeLep_DoubleEle_tree = ROOT.RDataFrame("Events", doubleEle_names)
  df_FakeLep_DoubleEle_tree = df_FakeLep_DoubleEle_tree.Define("fakelep_weight","fakelepweight_ee_data(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_FakeLep_DoubleEle = df_FakeLep_DoubleEle_tree.Filter(filters_data_fake)
  df_FakeLep_DoubleEle_trigger = for_diele_trigger(df_FakeLep_DoubleEle)
  df_FakeLep_DoubleEle_histos=[]
  for i in hists_name:
    df_FakeLep_DoubleEle_histo = df_FakeLep_DoubleEle_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i, 'fakelep_weight')
    df_FakeLep_DoubleEle_histos.append(df_FakeLep_DoubleEle_histo)

  df_FakeLep_SingleEle_tree = ROOT.RDataFrame("Events", singleEle_names)
  df_FakeLep_SingleEle_tree = df_FakeLep_SingleEle_tree.Define("fakelep_weight","fakelepweight_ee_data(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta)")
  df_FakeLep_SingleEle = df_FakeLep_SingleEle_tree.Filter(filters_data_fake)
  df_FakeLep_SingleEle_trigger = for_singleele_trigger_eechannel(df_FakeLep_SingleEle)
  df_FakeLep_SingleEle_histos=[]
  for i in hists_name:
    df_FakeLep_SingleEle_histo = df_FakeLep_SingleEle_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i, 'fakelep_weight')
    df_FakeLep_SingleEle_histos.append(df_FakeLep_SingleEle_histo)

  for ij in range(0,len(hists_name)):
    df_DY_histos[ij].Draw()
    df_osWW_histos[ij].Draw()
    df_ssWW_histos[ij].Draw()
    df_WWdps_histos[ij].Draw()
    df_WZew_histos[ij].Draw()
    df_WZqcd_histos[ij].Draw()
    df_ZZ_histos[ij].Draw()
    df_ZG_histos[ij].Draw()
    df_WWW_histos[ij].Draw()
    df_WWZ_histos[ij].Draw()
    df_WZZ_histos[ij].Draw()
    df_ZZZ_histos[ij].Draw()
    df_tW_histos[ij].Draw()
    df_tbarW_histos[ij].Draw()
    df_ttWtoLNu_histos[ij].Draw()
    df_ttWtoQQ_histos[ij].Draw()
    df_ttZ_histos[ij].Draw()
    df_ttZtoQQ_histos[ij].Draw()
    df_ttH_histos[ij].Draw()
    df_ttG_histos[ij].Draw()
    df_tttW_histos[ij].Draw()
    df_tttJ_histos[ij].Draw()
    df_tttt_histos[ij].Draw()
    df_ttZH_histos[ij].Draw()
    df_ttWH_histos[ij].Draw()
    df_ttWW_histos[ij].Draw()
    df_ttWZ_histos[ij].Draw()
    df_ttZZ_histos[ij].Draw()
    df_tzq_histos[ij].Draw()
    df_TTTo2L_histos[ij].Draw()
    df_DoubleEle_histos[ij].Draw()
    df_SingleEle_histos[ij].Draw()
    df_FakeLep_DoubleEle_histos[ij].Draw()
    df_FakeLep_SingleEle_histos[ij].Draw()
    df_Fake_DY_histos[ij].Draw()
    df_Fake_osWW_histos[ij].Draw()
    df_Fake_ssWW_histos[ij].Draw()
    df_Fake_WWdps_histos[ij].Draw()
    df_Fake_WZew_histos[ij].Draw()
    df_Fake_WZqcd_histos[ij].Draw()
    df_Fake_ZZ_histos[ij].Draw()
    df_Fake_ZG_histos[ij].Draw()
    df_Fake_WWW_histos[ij].Draw()
    df_Fake_WWZ_histos[ij].Draw()
    df_Fake_WZZ_histos[ij].Draw()
    df_Fake_ZZZ_histos[ij].Draw()
    df_Fake_tW_histos[ij].Draw()
    df_Fake_tbarW_histos[ij].Draw()
    df_Fake_ttWtoLNu_histos[ij].Draw()
    df_Fake_ttWtoQQ_histos[ij].Draw()
    df_Fake_ttZ_histos[ij].Draw()
    df_Fake_ttZtoQQ_histos[ij].Draw()
    df_Fake_ttH_histos[ij].Draw()
    df_Fake_ttG_histos[ij].Draw()
    df_Fake_tttW_histos[ij].Draw()
    df_Fake_tttJ_histos[ij].Draw()
    df_Fake_tttt_histos[ij].Draw()
    df_Fake_ttZH_histos[ij].Draw()
    df_Fake_ttWH_histos[ij].Draw()
    df_Fake_ttWW_histos[ij].Draw()
    df_Fake_ttWZ_histos[ij].Draw()
    df_Fake_ttZZ_histos[ij].Draw()
    df_Fake_tzq_histos[ij].Draw()
    df_Fake_TTTo2L_histos[ij].Draw()

# ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
#  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

    h_DY = df_DY_histos[ij].GetValue()
    h_osWW = df_osWW_histos[ij].GetValue()
    h_ssWW = df_ssWW_histos[ij].GetValue()
    h_WWdps = df_WWdps_histos[ij].GetValue()
    h_WZew = df_WZew_histos[ij].GetValue()
    h_WZqcd = df_WZqcd_histos[ij].GetValue()
    h_ZZ = df_ZZ_histos[ij].GetValue()
    h_ZG = df_ZG_histos[ij].GetValue()
    h_WWW = df_WWW_histos[ij].GetValue()
    h_WWZ = df_WWZ_histos[ij].GetValue()
    h_WZZ = df_WZZ_histos[ij].GetValue()
    h_ZZZ = df_ZZZ_histos[ij].GetValue()
    h_tW = df_tW_histos[ij].GetValue()
    h_tbarW = df_tbarW_histos[ij].GetValue()
    h_ttWtoLNu = df_ttWtoLNu_histos[ij].GetValue()
    h_ttWtoQQ = df_ttWtoQQ_histos[ij].GetValue()
    h_ttZ = df_ttZ_histos[ij].GetValue()
    h_ttZtoQQ = df_ttZtoQQ_histos[ij].GetValue()
    h_ttH = df_ttH_histos[ij].GetValue()
    h_ttG = df_ttG_histos[ij].GetValue()
    h_tttW = df_tttW_histos[ij].GetValue()
    h_tttJ = df_tttJ_histos[ij].GetValue()
    h_tttt = df_tttt_histos[ij].GetValue()
    h_ttZH = df_ttZH_histos[ij].GetValue()
    h_ttWH = df_ttWH_histos[ij].GetValue()
    h_ttWW = df_ttWW_histos[ij].GetValue()
    h_ttWZ = df_ttWZ_histos[ij].GetValue()
    h_ttZZ = df_ttZZ_histos[ij].GetValue()
    h_tzq = df_tzq_histos[ij].GetValue()
    h_TTTo2L = df_TTTo2L_histos[ij].GetValue()
    h_DoubleEle = df_DoubleEle_histos[ij].GetValue()
    h_SingleEle = df_SingleEle_histos[ij].GetValue()
    h_fakelep_DoubleEle = df_FakeLep_DoubleEle_histos[ij].GetValue()
    h_fakelep_SingleEle = df_FakeLep_SingleEle_histos[ij].GetValue()
    h_fake_DY = df_Fake_DY_histos[ij].GetValue()
    h_fake_osWW = df_Fake_osWW_histos[ij].GetValue()
    h_fake_ssWW = df_Fake_ssWW_histos[ij].GetValue()
    h_fake_WWdps = df_Fake_WWdps_histos[ij].GetValue()
    h_fake_WZew = df_Fake_WZew_histos[ij].GetValue()
    h_fake_WZqcd = df_Fake_WZqcd_histos[ij].GetValue()
    h_fake_ZZ = df_Fake_ZZ_histos[ij].GetValue()
    h_fake_ZG = df_Fake_ZG_histos[ij].GetValue()
    h_fake_WWW = df_Fake_WWW_histos[ij].GetValue()
    h_fake_WWZ = df_Fake_WWZ_histos[ij].GetValue()
    h_fake_WZZ = df_Fake_WZZ_histos[ij].GetValue()
    h_fake_ZZZ = df_Fake_ZZZ_histos[ij].GetValue()
    h_fake_tW = df_Fake_tW_histos[ij].GetValue()
    h_fake_tbarW = df_Fake_tbarW_histos[ij].GetValue()
    h_fake_ttWtoLNu = df_Fake_ttWtoLNu_histos[ij].GetValue()
    h_fake_ttWtoQQ = df_Fake_ttWtoQQ_histos[ij].GetValue()
    h_fake_ttZ = df_Fake_ttZ_histos[ij].GetValue()
    h_fake_ttZtoQQ = df_Fake_ttZtoQQ_histos[ij].GetValue()
    h_fake_ttH = df_Fake_ttH_histos[ij].GetValue()
    h_fake_ttG = df_Fake_ttG_histos[ij].GetValue()
    h_fake_tttW = df_Fake_tttW_histos[ij].GetValue()
    h_fake_tttJ = df_Fake_tttJ_histos[ij].GetValue()
    h_fake_tttt = df_Fake_tttt_histos[ij].GetValue()
    h_fake_ttZH = df_Fake_ttZH_histos[ij].GetValue()
    h_fake_ttWH = df_Fake_ttWH_histos[ij].GetValue()
    h_fake_ttWW = df_Fake_ttWW_histos[ij].GetValue()
    h_fake_ttWZ = df_Fake_ttWZ_histos[ij].GetValue()
    h_fake_ttZZ = df_Fake_ttZZ_histos[ij].GetValue()
    h_fake_tzq = df_Fake_tzq_histos[ij].GetValue()
    h_fake_TTTo2L = df_Fake_TTTo2L_histos[ij].GetValue()

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

import ROOT
import time
import os
import math
from math import sqrt
import plot_DYregion
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

path='/eos/cms/store/group/phys_top/ExtraYukawa/2018/'

#2018OK
doubleMu_names = ROOT.std.vector('string')()
for f in ["DoubleMuonA.root","DoubleMuonB.root","DoubleMuonC.root","DoubleMuonD_0.root","DoubleMuonD_1.root"]:
  doubleMu_names.push_back(path+f)

#2018OK
singleMu_names = ROOT.std.vector('string')()
for f in ["SingleMuonA.root","SingleMuonB.root","SingleMuonC.root","SingleMuonD_0.root","SingleMuonD_1.root"]:
  singleMu_names.push_back(path+f)

#This does not exist in 2018?
#doubleEle_names = ROOT.std.vector('string')()
#for f in ["DoubleEGA.root","DoubleEGB.root","DoubleEGC.root","DoubleEGD.root"]:
#  doubleEle_names.push_back(path+f)

#2018OK
singleEle_names = ROOT.std.vector('string')()
for f in ["EGammaA.root","EGammaB.root","EGammaC.root","EGammaD_0.root","EGammaD_1.root"]:
  singleEle_names.push_back(path+f)

#2018OK
muonEle_names = ROOT.std.vector('string')()
for f in ["MuonEGA.root","MuonEGB.root","MuonEGC.root","MuonEGD_0.root","MuonEGD_1.root"]:
  muonEle_names.push_back(path+f)

#2018OK
DY_list = ROOT.std.vector('string')()
for f in ['DY.root']:
  DY_list.push_back(path+f)

#2018OK
WJet_list = ROOT.std.vector('string')()
for f in ['WJets.root']:
  WJet_list.push_back(path+f)

#osWW_list = ROOT.std.vector('string')()
#for f in ['osWW.root']:
#  osWW_list.push_back(path+f)

#ssWW_list = ROOT.std.vector('string')()
#for f in ['ssWW.root']:
#  ssWW_list.push_back(path+f)
#
#WWdps_list = ROOT.std.vector('string')()
#for f in ['WWdps.root']:
#  WWdps_list.push_back(path+f)
#
#WZew_list = ROOT.std.vector('string')()
#for f in ['WZ_ew.root']:
#  WZew_list.push_back(path+f)
#
#WZqcd_list = ROOT.std.vector('string')()
#for f in ['WZ_qcd.root']:
#  WZqcd_list.push_back(path+f)

#2018OK
WW_list = ROOT.std.vector('string')()
for f in ['WW.root']:
  WW_list.push_back(path+f)

#2018OK
WZ_list = ROOT.std.vector('string')()
for f in ['WZ.root']:
  WZ_list.push_back(path+f)

#2018MISSING
#ZZ_list = ROOT.std.vector('string')()
#for f in ['ZZ.root']:
#  ZZ_list.push_back(path+f)

#ZG_list = ROOT.std.vector('string')()
#for f in ['ZG_ew.root']:
#  ZG_list.push_back(path+f)

#2018OK
WWW_list = ROOT.std.vector('string')()
for f in ['WWW.root']:
  WWW_list.push_back(path+f)

#2018OK
WWZ_list = ROOT.std.vector('string')()
for f in ['WWZ.root']:
  WWZ_list.push_back(path+f)

#2018OK
WZZ_list = ROOT.std.vector('string')()
for f in ['WZZ.root']:
  WZZ_list.push_back(path+f)

#2018OK
ZZZ_list = ROOT.std.vector('string')()
for f in ['ZZZ.root']:
  ZZZ_list.push_back(path+f)

#2018MISSING
#tsch_list = ROOT.std.vector('string')()
#for f in ['tsch.root']:
#  tsch_list.push_back(path+f)

#2018MISSING
#t_tch_list = ROOT.std.vector('string')()
#for f in ['t_tch.root']:
#  t_tch_list.push_back(path+f)

#2018MISSING
#tbar_tch_list = ROOT.std.vector('string')()
#for f in ['tbar_tch.root']:
#  tbar_tch_list.push_back(path+f)

#2018MISSING
#tW_list = ROOT.std.vector('string')()
#for f in ['tW.root']:
#  tW_list.push_back(path+f)

#2018MISSING
#tbarW_list = ROOT.std.vector('string')()
#for f in ['tbarW.root']:
#  tbarW_list.push_back(path+f)

#2018OK
ttWtoLNu_list = ROOT.std.vector('string')()
for f in ['ttWtoLNu.root']:
  ttWtoLNu_list.push_back(path+f)

#2018OK
ttWtoQQ_list = ROOT.std.vector('string')()
for f in ['ttWtoQQ.root']:
  ttWtoQQ_list.push_back(path+f)

#2018OK
ttZ_list = ROOT.std.vector('string')()
for f in ['ttZ.root']:
  ttZ_list.push_back(path+f)

#2018OK
ttZtoQQ_list = ROOT.std.vector('string')()
for f in ['ttZtoQQ.root']:
  ttZtoQQ_list.push_back(path+f)

#2018MISSING
#ttH_list = ROOT.std.vector('string')()
#for f in ['ttH.root']:
#  ttH_list.push_back(path+f)

#2018OK
ttWW_list = ROOT.std.vector('string')()
for f in ['ttWW.root']:
  ttWW_list.push_back(path+f)

#2018OK
ttWZ_list = ROOT.std.vector('string')()
for f in ['ttWZ.root']:
  ttWZ_list.push_back(path+f)

#2018OK
ttZZ_list = ROOT.std.vector('string')()
for f in ['ttZZ.root']:
  ttZZ_list.push_back(path+f)

#2018MISSING
#tzq_list = ROOT.std.vector('string')()
#for f in ['tzq.root']:
#  tzq_list.push_back(path+f)

#2018OK
TTTo2L_list = ROOT.std.vector('string')()
for f in ["TTTo2L.root"]:#,"TTTo2L_1.root"]:
  TTTo2L_list.push_back(path+f)

#2018OK
TTTo1L_list = ROOT.std.vector('string')()
for f in ['TTTo1L.root']:
  TTTo1L_list.push_back(path+f)

#2018MISSING
#TTWH_list = ROOT.std.vector('string')()
#for f in ['ttWH.root']:
#  TTWH_list.push_back(path+f)

#2018MISSING
#TTZH_list = ROOT.std.vector('string')()
#for f in ['ttZH.root']:
#  TTZH_list.push_back(path+f)

#2018MISSING
#TTTJ_list = ROOT.std.vector('string')()
#for f in ['tttJ.root']:
#  TTTJ_list.push_back(path+f)

#2018MISSING
#TTTW_list = ROOT.std.vector('string')()
#for f in ['tttW.root']:
#  TTTW_list.push_back(path+f)

#2018MISSING
#TTTT_list = ROOT.std.vector('string')()
#for f in ['tttt.root']:
#  TTTT_list.push_back(path+f)

#QCD50to80_list = ROOT.std.vector('string')()
#for f in ['QCD50to80.root']:
#  QCD50to80_list.push_back(path+f)
#
#QCD80to120_list = ROOT.std.vector('string')()
#for f in ['QCD80to120.root']:
#  QCD80to120_list.push_back(path+f)
#
#QCD120to170_list = ROOT.std.vector('string')()
#for f in ['QCD120to170.root']:
#  QCD120to170_list.push_back(path+f)
#
#QCD170to300_list = ROOT.std.vector('string')()
#for f in ['QCD170to300.root']:
#  QCD170to300_list.push_back(path+f)
#
#QCD300toinf_list = ROOT.std.vector('string')()
#for f in ['QCD300toinf.root']:
#  QCD300toinf_list.push_back(path+f)

#histograms name
hists_name = ['OPS_l1_pt','OPS_l1_eta','OPS_l1_phi','OPS_l2_pt','OPS_l2_eta','OPS_l2_phi','OPS_z_pt','OPS_z_eta','OPS_z_phi','OPS_z_mass']

#histograms bins
histos_bins = {
hists_name[0]:20,
hists_name[1]:20,
hists_name[2]:20,
hists_name[3]:20,
hists_name[4]:20,
hists_name[5]:20,
hists_name[6]:50,
hists_name[7]:20,
hists_name[8]:20,
hists_name[9]:60,
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
hists_name[7]:-3,
hists_name[8]:-4,
hists_name[9]:60,
}

#high edge
histos_bins_high = {
hists_name[0]:200,
hists_name[1]:3,
hists_name[2]:4,
hists_name[3]:100,
hists_name[4]:3,
hists_name[5]:4,
hists_name[6]:200,
hists_name[7]:3,
hists_name[8]:4,
hists_name[9]:120,
}

def TTC_Analysis():

  histos = []

  lumi = 59830.# from https://twiki.cern.ch/twiki/bin/view/CMS/TWikiLUM

  DY_xs = 6077.22
  DY_ev = get_mcEventnumber(DY_list)

  WJet_xs = 61526.7
  WJet_ev = get_mcEventnumber(WJet_list)
  
  WW_xs = 118.7
  WW_ev = get_mcEventnumber(WW_list)

  WZ_xs = 27.6 #to be checked - from XSDB
  WZ_ev = get_mcEventnumber(WZ_list)
  #osWW_xs = 11.09
  #osWW_ev = get_mcEventnumber(osWW_list)

  #ssWW_xs = 0.04932
  #ssWW_ev = get_mcEventnumber(ssWW_list)

  #WWdps_xs = 1.62
  #WWdps_ev = get_mcEventnumber(WWdps_list)

  #WZew_xs = 0.0163
  #WZew_ev = get_mcEventnumber(WZew_list)

  #WZqcd_xs = 5.213
  #WZqcd_ev = get_mcEventnumber(WZqcd_list)

  #ZZ_xs = 0.0086
  #ZZ_ev = get_mcEventnumber(ZZ_list)

  #ZG_xs = 0.1097
  #ZG_ev = get_mcEventnumber(ZG_list)

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

  TTTo1L_xs = 365.4574
  TTTo1L_ev = get_mcEventnumber(TTTo1L_list)

#  TTH_xs = 0.5269
#  TTH_ev = get_mcEventnumber(ttH_list)

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

#  tZq_xs = 0.07561
#  tZq_ev = get_mcEventnumber(tzq_list)

#  tW_xs = 35.85
#  tW_ev = get_mcEventnumber(tW_list)

#  tbarW_xs = 35.85
#  tbarW_ev = get_mcEventnumber(tbarW_list)

#  t_sch_xs = 3.36
#  t_sch_ev = get_mcEventnumber(tsch_list)

#  t_tch_xs = 136.02
#  t_tch_ev = get_mcEventnumber(t_tch_list)

#  tbar_tch_xs = 80.95
#  tbar_tch_ev = get_mcEventnumber(tbar_tch_list)

#  ttWH_xs = 0.00114
#  ttWH_ev = get_mcEventnumber(TTWH_list)

#  ttZH_xs = 0.00113
#  ttZH_ev = get_mcEventnumber(TTZH_list)

#  tttJ_xs = 0.0004
#  tttJ_ev = get_mcEventnumber(TTTJ_list)

#  tttW_xs = 0.00073
#  tttW_ev = get_mcEventnumber(TTTW_list)

#  tttt_xs = 0.0082
#  tttt_ev = get_mcEventnumber(TTTT_list)

#  QCD50to80_xs = 1984000.0
#  QCD50to80_ev = get_mcEventnumber(QCD50to80_list)
#
#  QCD80to120_xs = 366500.0
#  QCD80to120_ev = get_mcEventnumber(QCD80to120_list)
#
#  QCD120to170_xs = 66490.0
#  QCD120to170_ev = get_mcEventnumber(QCD120to170_list)
#
#  QCD170to300_xs = 16480.0
#  QCD170to300_ev = get_mcEventnumber(QCD170to300_list)
#
#  QCD300toinf_xs = 1097.0
#  QCD300toinf_ev = get_mcEventnumber(QCD300toinf_list)

  # define the filters here, 1:2mu, 2:1e1m, 3:2ele
  filters="OPS_region==1 && OPS_2P0F && OPS_z_mass>60 && OPS_z_mass<120 && OPS_l1_pt>30 && OPS_l2_pt>20 && OPS_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0"

#  weights_str = "puWeight*PrefireWeight*genWeight/abs(genWeight)" 
  weights_str = "puWeight*genWeight/abs(genWeight)"
  df_DY_tree = ROOT.RDataFrame("Events",DY_list)
  df_DY_tree = df_DY_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_DY_tree = df_DY_tree.Define("genweight",weights_str)
  df_DY = df_DY_tree.Filter(filters)
  df_DY_trigger = all_trigger(df_DY)
  df_DY_histos=[]
  for i in hists_name:
    df_DY_histo = df_DY_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_DY_histos.append(df_DY_histo)

  df_WJet_tree = ROOT.RDataFrame("Events",WJet_list)
  df_WJet_tree = df_WJet_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_WJet_tree = df_WJet_tree.Define("genweight",weights_str)
  df_WJet = df_WJet_tree.Filter(filters)
  df_WJet_trigger = all_trigger(df_WJet)
  df_WJet_histos=[]
  for i in hists_name:
    df_WJet_histo = df_WJet_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WJet_histos.append(df_WJet_histo)

  df_WW_tree = ROOT.RDataFrame("Events",WW_list)
  df_WW_tree = df_WW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_WW_tree = df_WW_tree.Define("genweight",weights_str)
  df_WW = df_WW_tree.Filter(filters)
  df_WW_trigger = all_trigger(df_WW)
  df_WW_histos=[]
  for i in hists_name:
    df_WW_histo = df_WW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WW_histos.append(df_WW_histo)

  df_WZ_tree = ROOT.RDataFrame("Events",WZ_list)
  df_WZ_tree = df_WZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_WZ_tree = df_WZ_tree.Define("genweight",weights_str)
  df_WZ = df_WZ_tree.Filter(filters)
  df_WZ_trigger = all_trigger(df_WZ)
  df_WZ_histos=[]
  for i in hists_name:
    df_WZ_histo = df_WZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WZ_histos.append(df_WZ_histo)

#  df_osWW_tree = ROOT.RDataFrame("Events",osWW_list)
#  df_osWW_tree = df_osWW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_osWW_tree = df_osWW_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_osWW = df_osWW_tree.Filter(filters)
#  df_osWW_trigger = all_trigger(df_osWW)
#  df_osWW_histos=[]
#  for i in hists_name:
#    df_osWW_histo = df_osWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_osWW_histos.append(df_osWW_histo)

#  df_ssWW_tree = ROOT.RDataFrame("Events",ssWW_list)
#  df_ssWW_tree = df_ssWW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_ssWW_tree = df_ssWW_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_ssWW = df_ssWW_tree.Filter(filters)
#  df_ssWW_trigger = all_trigger(df_ssWW)
#  df_ssWW_histos=[]
#  for i in hists_name:
#    df_ssWW_histo = df_ssWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ssWW_histos.append(df_ssWW_histo)

#  df_WWdps_tree = ROOT.RDataFrame("Events",WWdps_list)
#  df_WWdps_tree = df_WWdps_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_WWdps_tree = df_WWdps_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_WWdps = df_WWdps_tree.Filter(filters)
#  df_WWdps_trigger = all_trigger(df_WWdps)
#  df_WWdps_histos=[]
#  for i in hists_name:
#    df_WWdps_histo = df_WWdps_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_WWdps_histos.append(df_WWdps_histo)

#  df_WZew_tree = ROOT.RDataFrame("Events",WZew_list)
#  df_WZew_tree = df_WZew_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_WZew_tree = df_WZew_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_WZew = df_WZew_tree.Filter(filters)
#  df_WZew_trigger = all_trigger(df_WZew)
#  df_WZew_histos=[]
#  for i in hists_name:
#    df_WZew_histo = df_WZew_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_WZew_histos.append(df_WZew_histo)

#  df_WZqcd_tree = ROOT.RDataFrame("Events",WZqcd_list)
#  df_WZqcd_tree = df_WZqcd_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_WZqcd_tree = df_WZqcd_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_WZqcd = df_WZqcd_tree.Filter(filters)
#  df_WZqcd_trigger = all_trigger(df_WZqcd)
#  df_WZqcd_histos=[]
#  for i in hists_name:
#    df_WZqcd_histo = df_WZqcd_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_WZqcd_histos.append(df_WZqcd_histo)

#  df_ZZ_tree = ROOT.RDataFrame("Events",ZZ_list)
#  df_ZZ_tree = df_ZZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_ZZ_tree = df_ZZ_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_ZZ = df_ZZ_tree.Filter(filters)
#  df_ZZ_trigger = all_trigger(df_ZZ)
#  df_ZZ_histos=[]
#  for i in hists_name:
#    df_ZZ_histo = df_ZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ZZ_histos.append(df_ZZ_histo)

#  df_ZG_tree = ROOT.RDataFrame("Events",ZG_list)
#  df_ZG_tree = df_ZG_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_ZG_tree = df_ZG_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_ZG = df_ZG_tree.Filter(filters)
#  df_ZG_trigger = all_trigger(df_ZG)
#  df_ZG_histos=[]
#  for i in hists_name:
#    df_ZG_histo = df_ZG_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ZG_histos.append(df_ZG_histo)

  df_WWW_tree = ROOT.RDataFrame("Events",WWW_list)
  df_WWW_tree = df_WWW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_WWW_tree = df_WWW_tree.Define("genweight",weights_str)
  df_WWW = df_WWW_tree.Filter(filters)
  df_WWW_trigger = all_trigger(df_WWW)
  df_WWW_histos=[]
  for i in hists_name:
    df_WWW_histo = df_WWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WWW_histos.append(df_WWW_histo)

  df_WWZ_tree = ROOT.RDataFrame("Events",WWZ_list)
  df_WWZ_tree = df_WWZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_WWZ_tree = df_WWZ_tree.Define("genweight",weights_str)
  df_WWZ = df_WWZ_tree.Filter(filters)
  df_WWZ_trigger = all_trigger(df_WWZ)
  df_WWZ_histos=[]
  for i in hists_name:
    df_WWZ_histo = df_WWZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WWZ_histos.append(df_WWZ_histo)

  df_WZZ_tree = ROOT.RDataFrame("Events",WZZ_list)
  df_WZZ_tree = df_WZZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_WZZ_tree = df_WZZ_tree.Define("genweight",weights_str)
  df_WZZ = df_WZZ_tree.Filter(filters)
  df_WZZ_trigger = all_trigger(df_WZZ)
  df_WZZ_histos=[]
  for i in hists_name:
    df_WZZ_histo = df_WZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_WZZ_histos.append(df_WZZ_histo)

  df_ZZZ_tree = ROOT.RDataFrame("Events",ZZZ_list)
  df_ZZZ_tree = df_ZZZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ZZZ_tree = df_ZZZ_tree.Define("genweight",weights_str)
  df_ZZZ = df_ZZZ_tree.Filter(filters)
  df_ZZZ_trigger = all_trigger(df_ZZZ)
  df_ZZZ_histos=[]
  for i in hists_name:
    df_ZZZ_histo = df_ZZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ZZZ_histos.append(df_ZZZ_histo)

#  df_tsch_tree = ROOT.RDataFrame("Events",tsch_list)
#  df_tsch_tree = df_tsch_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tsch_tree = df_tsch_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tsch = df_tsch_tree.Filter(filters)
#  df_tsch_trigger = all_trigger(df_tsch)
#  df_tsch_histos=[]
#  for i in hists_name:
#    df_tsch_histo = df_tsch_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tsch_histos.append(df_tsch_histo)

#  df_t_tch_tree = ROOT.RDataFrame("Events",t_tch_list)
#  df_t_tch_tree = df_t_tch_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_t_tch_tree = df_t_tch_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_t_tch = df_t_tch_tree.Filter(filters)
#  df_t_tch_trigger = all_trigger(df_t_tch)
#  df_t_tch_histos=[]
#  for i in hists_name:
#    df_t_tch_histo = df_t_tch_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_t_tch_histos.append(df_t_tch_histo)

#  df_tbar_tch_tree = ROOT.RDataFrame("Events",tbar_tch_list)
#  df_tbar_tch_tree = df_tbar_tch_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tbar_tch_tree = df_tbar_tch_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tbar_tch = df_tbar_tch_tree.Filter(filters)
#  df_tbar_tch_trigger = all_trigger(df_tbar_tch)
#  df_tbar_tch_histos=[]
#  for i in hists_name:
#    df_tbar_tch_histo = df_tbar_tch_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tbar_tch_histos.append(df_tbar_tch_histo)

#  df_tW_tree = ROOT.RDataFrame("Events",tW_list)
#  df_tW_tree = df_tW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tW_tree = df_tW_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tW = df_tW_tree.Filter(filters)
#  df_tW_trigger = all_trigger(df_tW)
#  df_tW_histos=[]
#  for i in hists_name:
#    df_tW_histo = df_tW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tW_histos.append(df_tW_histo)

#  df_tbarW_tree = ROOT.RDataFrame("Events",tbarW_list)
#  df_tbarW_tree = df_tbarW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tbarW_tree = df_tbarW_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tbarW = df_tbarW_tree.Filter(filters)
#  df_tbarW_trigger = all_trigger(df_tbarW)
#  df_tbarW_histos=[]
#  for i in hists_name:
#    df_tbarW_histo = df_tbarW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tbarW_histos.append(df_tbarW_histo)

  df_ttWtoLNu_tree = ROOT.RDataFrame("Events",ttWtoLNu_list)
  df_ttWtoLNu_tree = df_ttWtoLNu_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttWtoLNu_tree = df_ttWtoLNu_tree.Define("genweight",weights_str)
  df_ttWtoLNu = df_ttWtoLNu_tree.Filter(filters)
  df_ttWtoLNu_trigger = all_trigger(df_ttWtoLNu)
  df_ttWtoLNu_histos=[]
  for i in hists_name:
    df_ttWtoLNu_histo = df_ttWtoLNu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWtoLNu_histos.append(df_ttWtoLNu_histo)

  df_ttWtoQQ_tree = ROOT.RDataFrame("Events",ttWtoQQ_list)
  df_ttWtoQQ_tree = df_ttWtoQQ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttWtoQQ_tree = df_ttWtoQQ_tree.Define("genweight",weights_str)
  df_ttWtoQQ = df_ttWtoQQ_tree.Filter(filters)
  df_ttWtoQQ_trigger = all_trigger(df_ttWtoQQ)
  df_ttWtoQQ_histos=[]
  for i in hists_name:
    df_ttWtoQQ_histo = df_ttWtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWtoQQ_histos.append(df_ttWtoQQ_histo)

  df_ttZ_tree = ROOT.RDataFrame("Events",ttZ_list)
  df_ttZ_tree = df_ttZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttZ_tree = df_ttZ_tree.Define("genweight",weights_str)
  df_ttZ = df_ttZ_tree.Filter(filters)
  df_ttZ_trigger = all_trigger(df_ttZ)
  df_ttZ_histos=[]
  for i in hists_name:
    df_ttZ_histo = df_ttZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZ_histos.append(df_ttZ_histo)

  df_ttZtoQQ_tree = ROOT.RDataFrame("Events",ttZtoQQ_list)
  df_ttZtoQQ_tree = df_ttZtoQQ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttZtoQQ_tree = df_ttZtoQQ_tree.Define("genweight",weights_str)
  df_ttZtoQQ = df_ttZtoQQ_tree.Filter(filters)
  df_ttZtoQQ_trigger = all_trigger(df_ttZtoQQ)
  df_ttZtoQQ_histos=[]
  for i in hists_name:
    df_ttZtoQQ_histo = df_ttZtoQQ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZtoQQ_histos.append(df_ttZtoQQ_histo)

#  df_ttH_tree = ROOT.RDataFrame("Events",ttH_list)
#  df_ttH_tree = df_ttH_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_ttH_tree = df_ttH_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_ttH = df_ttH_tree.Filter(filters)
#  df_ttH_trigger = all_trigger(df_ttH)
#  df_ttH_histos=[]
#  for i in hists_name:
#    df_ttH_histo = df_ttH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ttH_histos.append(df_ttH_histo)

  df_ttWW_tree = ROOT.RDataFrame("Events",ttWW_list)
  df_ttWW_tree = df_ttWW_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttWW_tree = df_ttWW_tree.Define("genweight",weights_str)
  df_ttWW = df_ttWW_tree.Filter(filters)
  df_ttWW_trigger = all_trigger(df_ttWW)
  df_ttWW_histos=[]
  for i in hists_name:
    df_ttWW_histo = df_ttWW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWW_histos.append(df_ttWW_histo)

  df_ttWZ_tree = ROOT.RDataFrame("Events",ttWZ_list)
  df_ttWZ_tree = df_ttWZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttWZ_tree = df_ttWZ_tree.Define("genweight",weights_str)
  df_ttWZ = df_ttWZ_tree.Filter(filters)
  df_ttWZ_trigger = all_trigger(df_ttWZ)
  df_ttWZ_histos=[]
  for i in hists_name:
    df_ttWZ_histo = df_ttWZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttWZ_histos.append(df_ttWZ_histo)

  df_ttZZ_tree = ROOT.RDataFrame("Events",ttZZ_list)
  df_ttZZ_tree = df_ttZZ_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_ttZZ_tree = df_ttZZ_tree.Define("genweight",weights_str)
  df_ttZZ = df_ttZZ_tree.Filter(filters)
  df_ttZZ_trigger = all_trigger(df_ttZZ)
  df_ttZZ_histos=[]
  for i in hists_name:
    df_ttZZ_histo = df_ttZZ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_ttZZ_histos.append(df_ttZZ_histo)

#  df_tzq_tree = ROOT.RDataFrame("Events",tzq_list)
#  df_tzq_tree = df_tzq_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tzq_tree = df_tzq_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tzq = df_tzq_tree.Filter(filters)
#  df_tzq_trigger = all_trigger(df_tzq)
#  df_tzq_histos=[]
#  for i in hists_name:
#    df_tzq_histo = df_tzq_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tzq_histos.append(df_tzq_histo)

#  df_ttWH_tree = ROOT.RDataFrame("Events",TTWH_list)
#  df_ttWH_tree = df_ttWH_tree.Define("trigger_SF","trigger_sf_ee(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_ttWH_tree = df_ttWH_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_ttWH = df_ttWH_tree.Filter(filters)
#  df_ttWH_trigger = all_trigger(df_ttWH)
#  df_ttWH_histos=[]
#  for i in hists_name:
#    df_ttWH_histo = df_ttWH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ttWH_histos.append(df_ttWH_histo)

#  df_ttZH_tree = ROOT.RDataFrame("Events",TTZH_list)
#  df_ttZH_tree = df_ttZH_tree.Define("trigger_SF","trigger_sf_ee(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_ttZH_tree = df_ttZH_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_ttZH = df_ttZH_tree.Filter(filters)
#  df_ttZH_trigger = all_trigger(df_ttZH)
#  df_ttZH_histos=[]
#  for i in hists_name:
#    df_ttZH_histo = df_ttZH_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_ttZH_histos.append(df_ttZH_histo)

#  df_tttJ_tree = ROOT.RDataFrame("Events",TTTJ_list)
#  df_tttJ_tree = df_tttJ_tree.Define("trigger_SF","trigger_sf_ee(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tttJ_tree = df_tttJ_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tttJ = df_tttJ_tree.Filter(filters)
#  df_tttJ_trigger = all_trigger(df_tttJ)
#  df_tttJ_histos=[]
#  for i in hists_name:
#    df_tttJ_histo = df_tttJ_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tttJ_histos.append(df_tttJ_histo)

#  df_tttW_tree = ROOT.RDataFrame("Events",TTTW_list)
#  df_tttW_tree = df_tttW_tree.Define("trigger_SF","trigger_sf_ee(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tttW_tree = df_tttW_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tttW = df_tttW_tree.Filter(filters)
#  df_tttW_trigger = all_trigger(df_tttW)
#  df_tttW_histos=[]
#  for i in hists_name:
#    df_tttW_histo = df_tttW_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tttW_histos.append(df_tttW_histo)

#  df_tttt_tree = ROOT.RDataFrame("Events",TTTT_list)
#  df_tttt_tree = df_tttt_tree.Define("trigger_SF","trigger_sf_ee(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_tttt_tree = df_tttt_tree.Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
#  df_tttt = df_tttt_tree.Filter(filters)
#  df_tttt_trigger = all_trigger(df_tttt)
#  df_tttt_histos=[]
#  for i in hists_name:
#    df_tttt_histo = df_tttt_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_tttt_histos.append(df_tttt_histo)

#  df_QCD50to80_tree = ROOT.RDataFrame("Events",QCD50to80_list)
#  df_QCD50to80_tree = df_QCD50to80_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
#  df_QCD50to80_tree = df_QCD50to80_tree.Define("genweight","puWeight*PrefireWeight*trigger_SF*genWeight/abs(genWeight)")
#  df_QCD50to80 = df_QCD50to80_tree.Filter(filters)
#  df_QCD50to80_trigger = all_trigger(df_QCD50to80)
#  df_QCD50to80_histos=[]
#  for i in hists_name:
#    df_QCD50to80_histo = df_QCD50to80_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_QCD50to80_histos.append(df_QCD50to80_histo)
#
#  df_QCD80to120_tree = ROOT.RDataFrame("Events",QCD80to120_list)
#  df_QCD80to120_tree = df_QCD80to120_tree.Define("trigger_SF","trigger_sf_mm(DY_l1_pt,DY_l2_pt,DY_l1_eta,DY_l2_eta)")
#  df_QCD80to120_tree = df_QCD80to120_tree.Define("genweight","puWeight*PrefireWeight*Muon_CutBased_TightID_SF[DY_l1_id]*Muon_CutBased_TightID_SF[DY_l2_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l1_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_QCD80to120 = df_QCD80to120_tree.Filter(filters)
#  df_QCD80to120_trigger = all_trigger(df_QCD80to120)
#  df_QCD80to120_histos=[]
#  for i in hists_name:
#    df_QCD80to120_histo = df_QCD80to120_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_QCD80to120_histos.append(df_QCD80to120_histo)
#
#  df_QCD120to170_tree = ROOT.RDataFrame("Events",QCD120to170_list)
#  df_QCD120to170_tree = df_QCD120to170_tree.Define("trigger_SF","trigger_sf_mm(DY_l1_pt,DY_l2_pt,DY_l1_eta,DY_l2_eta)")
#  df_QCD120to170_tree = df_QCD120to170_tree.Define("genweight","puWeight*PrefireWeight*Muon_CutBased_TightID_SF[DY_l1_id]*Muon_CutBased_TightID_SF[DY_l2_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l1_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_QCD120to170 = df_QCD120to170_tree.Filter(filters)
#  df_QCD120to170_trigger = all_trigger(df_QCD120to170)
#  df_QCD120to170_histos=[]
#  for i in hists_name:
#    df_QCD120to170_histo = df_QCD120to170_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_QCD120to170_histos.append(df_QCD120to170_histo)
#
#  df_QCD170to300_tree = ROOT.RDataFrame("Events",QCD170to300_list)
#  df_QCD170to300_tree = df_QCD170to300_tree.Define("trigger_SF","trigger_sf_mm(DY_l1_pt,DY_l2_pt,DY_l1_eta,DY_l2_eta)")
#  df_QCD170to300_tree = df_QCD170to300_tree.Define("genweight","puWeight*PrefireWeight*Muon_CutBased_TightID_SF[DY_l1_id]*Muon_CutBased_TightID_SF[DY_l2_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l1_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_QCD170to300 = df_QCD170to300_tree.Filter(filters)
#  df_QCD170to300_trigger = all_trigger(df_QCD170to300)
#  df_QCD170to300_histos=[]
#  for i in hists_name:
#    df_QCD170to300_histo = df_QCD170to300_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_QCD170to300_histos.append(df_QCD170to300_histo)
#
#  df_QCD300toinf_tree = ROOT.RDataFrame("Events",QCD300toinf_list)
#  df_QCD300toinf_tree = df_QCD300toinf_tree.Define("trigger_SF","trigger_sf_mm(DY_l1_pt,DY_l2_pt,DY_l1_eta,DY_l2_eta)")
#  df_QCD300toinf_tree = df_QCD300toinf_tree.Define("genweight","puWeight*PrefireWeight*Muon_CutBased_TightID_SF[DY_l1_id]*Muon_CutBased_TightID_SF[DY_l2_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l1_id]*Muon_TightRelIso_TightIDandIPCut_SF[DY_l2_id]*trigger_SF*genWeight/abs(genWeight)")
#  df_QCD300toinf = df_QCD300toinf_tree.Filter(filters)
#  df_QCD300toinf_trigger = all_trigger(df_QCD300toinf)
#  df_QCD300toinf_histos=[]
#  for i in hists_name:
#    df_QCD300toinf_histo = df_QCD300toinf_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
#    df_QCD300toinf_histos.append(df_QCD300toinf_histo)

  df_TTTo2L_tree = ROOT.RDataFrame("Events",TTTo2L_list)
  df_TTTo2L_tree = df_TTTo2L_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_TTTo2L_tree = df_TTTo2L_tree.Define("genweight",weights_str)
  df_TTTo2L = df_TTTo2L_tree.Filter(filters)
  df_TTTo2L_trigger = all_trigger(df_TTTo2L)
  df_TTTo2L_histos=[]
  for i in hists_name:
    df_TTTo2L_histo = df_TTTo2L_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_TTTo2L_histos.append(df_TTTo2L_histo)

  df_TTTo1L_tree = ROOT.RDataFrame("Events",TTTo1L_list)
  df_TTTo1L_tree = df_TTTo1L_tree.Define("trigger_SF","trigger_sf_mm(OPS_l1_pt,OPS_l2_pt,OPS_l1_eta,OPS_l2_eta)")
  df_TTTo1L_tree = df_TTTo1L_tree.Define("genweight",weights_str)
  df_TTTo1L = df_TTTo1L_tree.Filter(filters)
  df_TTTo1L_trigger = all_trigger(df_TTTo1L)
  df_TTTo1L_histos=[]
  for i in hists_name:
    df_TTTo1L_histo = df_TTTo1L_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i,'genweight')
    df_TTTo1L_histos.append(df_TTTo1L_histo)

  df_DoubleMu_tree = ROOT.RDataFrame("Events", doubleMu_names)
  df_DoubleMu = df_DoubleMu_tree.Filter(filters)
  df_DoubleMu_trigger = for_dimuon_trigger(df_DoubleMu) 
  df_DoubleMu_histos=[]
  for i in hists_name:
    df_DoubleMu_histo = df_DoubleMu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_DoubleMu_histos.append(df_DoubleMu_histo)

  df_SingleMu_tree = ROOT.RDataFrame("Events", singleMu_names)
  df_SingleMu = df_SingleMu_tree.Filter(filters)
  df_SingleMu_trigger = for_singlemuon_trigger_mumuchannel(df_SingleMu)
  df_SingleMu_histos=[]
  for i in hists_name:
    df_SingleMu_histo = df_SingleMu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_SingleMu_histos.append(df_SingleMu_histo)

  for ij in range(0,len(hists_name)):
    df_DY_histos[ij].Draw()
    df_WJet_histos[ij].Draw()
    df_WW_histos[ij].Draw()
    df_WZ_histos[ij].Draw()
#    df_osWW_histos[ij].Draw()
#    df_ssWW_histos[ij].Draw()
#    df_WWdps_histos[ij].Draw()
#    df_WZew_histos[ij].Draw()
#    df_WZqcd_histos[ij].Draw()
#    df_ZZ_histos[ij].Draw()
#    df_ZG_histos[ij].Draw()
    df_WWW_histos[ij].Draw()
    df_WWZ_histos[ij].Draw()
    df_WZZ_histos[ij].Draw()
    df_ZZZ_histos[ij].Draw()
#    df_tsch_histos[ij].Draw()
#    df_t_tch_histos[ij].Draw()
#    df_tbar_tch_histos[ij].Draw()
#    df_tW_histos[ij].Draw()
#    df_tbarW_histos[ij].Draw()
    df_ttWtoLNu_histos[ij].Draw()
    df_ttWtoQQ_histos[ij].Draw()
    df_ttZ_histos[ij].Draw()
    df_ttZtoQQ_histos[ij].Draw()
    df_ttH_histos[ij].Draw()
    df_ttWW_histos[ij].Draw()
    df_ttWZ_histos[ij].Draw()
    df_ttZZ_histos[ij].Draw()
#    df_tzq_histos[ij].Draw()
#    df_ttWH_histos[ij].Draw()
#    df_ttZH_histos[ij].Draw()
#    df_tttJ_histos[ij].Draw()
#    df_tttW_histos[ij].Draw()
#    df_tttt_histos[ij].Draw()
#    df_QCD50to80_histos[ij].Draw()
#    df_QCD80to120_histos[ij].Draw()
#    df_QCD120to170_histos[ij].Draw()
#    df_QCD170to300_histos[ij].Draw()
#    df_QCD300toinf_histos[ij].Draw()
    df_DoubleMu_histos[ij].Draw()
    df_SingleMu_histos[ij].Draw()

# ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
#  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

    h_DY = df_DY_histos[ij].GetValue()
    h_WJet = df_WJet_histos[ij].GetValue()
#    h_osWW = df_osWW_histos[ij].GetValue()
#    h_ssWW = df_ssWW_histos[ij].GetValue()
#    h_WWdps = df_WWdps_histos[ij].GetValue()
#    h_WZew = df_WZew_histos[ij].GetValue()
#    h_WZqcd = df_WZqcd_histos[ij].GetValue()
#    h_ZZ = df_ZZ_histos[ij].GetValue()
#    h_ZG = df_ZG_histos[ij].GetValue()
    h_WWW = df_WWW_histos[ij].GetValue()
    h_WWZ = df_WWZ_histos[ij].GetValue()
    h_WZZ = df_WZZ_histos[ij].GetValue()
    h_ZZZ = df_ZZZ_histos[ij].GetValue()
#    h_tsch = df_tsch_histos[ij].GetValue()
#    h_t_tch = df_t_tch_histos[ij].GetValue()
#    h_tbar_tch = df_tbar_tch_histos[ij].GetValue()
#    h_tW = df_tW_histos[ij].GetValue()
#    h_tbarW = df_tbarW_histos[ij].GetValue()
    h_ttWtoLNu = df_ttWtoLNu_histos[ij].GetValue()
    h_ttWtoQQ = df_ttWtoQQ_histos[ij].GetValue()
    h_ttZ = df_ttZ_histos[ij].GetValue()
    h_ttZtoQQ = df_ttZtoQQ_histos[ij].GetValue()
#    h_ttH = df_ttH_histos[ij].GetValue()
    h_ttWW = df_ttWW_histos[ij].GetValue()
    h_ttWZ = df_ttWZ_histos[ij].GetValue()
    h_ttZZ = df_ttZZ_histos[ij].GetValue()
#    h_tzq = df_tzq_histos[ij].GetValue()
#    h_ttWH = df_ttWH_histos[ij].GetValue()
#    h_ttZH = df_ttZH_histos[ij].GetValue()
#    h_tttJ = df_tttJ_histos[ij].GetValue()
#    h_tttW = df_tttW_histos[ij].GetValue()
#    h_tttt = df_tttt_histos[ij].GetValue()
#    h_QCD50to80 = df_QCD50to80_histos[ij].GetValue()
#    h_QCD80to120 = df_QCD80to120_histos[ij].GetValue()
#    h_QCD120to170 = df_QCD120to170_histos[ij].GetValue()
#    h_QCD170to300 = df_QCD170to300_histos[ij].GetValue()
#    h_QCD300toinf = df_QCD300toinf_histos[ij].GetValue()
    h_TTTo2L = df_TTTo2L_histos[ij].GetValue()
    h_TTTo1L = df_TTTo1L_histos[ij].GetValue()
    h_DoubleMu = df_DoubleMu_histos[ij].GetValue()
    h_SingleMu = df_SingleMu_histos[ij].GetValue()

    h_DY.Scale(DY_xs/DY_ev)
    h_WJet.Scale(WJet_xs/WJet_ev)
#    h_osWW.Scale(osWW_xs/osWW_ev)
#    h_ssWW.Scale(ssWW_xs/ssWW_ev)
#    h_WWdps.Scale(WWdps_xs/WWdps_ev)
#    h_WZew.Scale(WZew_xs/WZew_ev)
#    h_WZqcd.Scale(WZqcd_xs/WZqcd_ev)
#    h_ZZ.Scale(ZZ_xs/ZZ_ev)
#    h_ZG.Scale(ZG_xs/ZG_ev)
    h_WWW.Scale(WWW_xs/WWW_ev)
    h_WWZ.Scale(WWZ_xs/WWZ_ev)
    h_WZZ.Scale(WZZ_xs/WZZ_ev)
    h_ZZZ.Scale(ZZZ_xs/ZZZ_ev)
#    h_tsch.Scale(t_sch_xs/t_sch_ev)
#    h_t_tch.Scale(t_tch_xs/t_tch_ev)
#    h_tbar_tch.Scale(tbar_tch_xs/tbar_tch_ev)
#    h_tW.Scale(tW_xs/tW_ev)
#    h_tbarW.Scale(tbarW_xs/tbarW_ev)
    h_ttWtoLNu.Scale(TTWtoLNu_xs/TTWtoLNu_ev)
    h_ttWtoQQ.Scale(TTWtoQQ_xs/TTWtoQQ_ev)
    h_ttZ.Scale(TTZ_xs/TTZ_ev)
    h_ttZtoQQ.Scale(TTZtoQQ_xs/TTZtoQQ_ev)
#    h_ttH.Scale(TTH_xs/TTH_ev)
    h_ttWW.Scale(TTWW_xs/TTWW_ev)
    h_ttWZ.Scale(TTWZ_xs/TTWZ_ev)
    h_ttZZ.Scale(TTZZ_xs/TTZZ_ev)
#    h_tzq.Scale(tZq_xs/tZq_ev)
#    h_ttWH.Scale(ttWH_xs/ttWH_ev)
#    h_ttZH.Scale(ttZH_xs/ttZH_ev)
#    h_tttJ.Scale(tttJ_xs/tttJ_ev)
#    h_tttW.Scale(tttW_xs/tttW_ev)
#    h_tttt.Scale(tttt_xs/tttt_ev)
#    h_QCD50to80.Scale(QCD50to80_xs/QCD50to80_ev)
#    h_QCD80to120.Scale(QCD80to120_xs/QCD80to120_ev)
#    h_QCD120to170.Scale(QCD120to170_xs/QCD120to170_ev)
#    h_QCD170to300.Scale(QCD170to300_xs/QCD170to300_ev)
#    h_QCD300toinf.Scale(QCD300toinf_xs/QCD300toinf_ev)
    h_TTTo2L.Scale(TTTo2L_xs/TTTo2L_ev)
    h_TTTo1L.Scale(TTTo1L_xs/TTTo1L_ev)

    histos.append(h_DY.Clone())
    histos.append(h_WJet.Clone())
#    histos.append(h_osWW.Clone())
#    histos.append(h_ssWW.Clone())
#    histos.append(h_WWdps.Clone())
#    histos.append(h_WZew.Clone())
#    histos.append(h_WZqcd.Clone())
#    histos.append(h_ZZ.Clone())
#    histos.append(h_ZG.Clone())
    histos.append(h_WWW.Clone())
    histos.append(h_WWZ.Clone())
    histos.append(h_WZZ.Clone())
    histos.append(h_ZZZ.Clone())
#    histos.append(h_tsch.Clone())
#    histos.append(h_t_tch.Clone())
#    histos.append(h_tbar_tch.Clone())
#    histos.append(h_tW.Clone())
#    histos.append(h_tbarW.Clone())
    histos.append(h_ttWtoLNu.Clone())
    histos.append(h_ttWtoQQ.Clone())
    histos.append(h_ttZ.Clone())
    histos.append(h_ttZtoQQ.Clone())
#    histos.append(h_ttH.Clone())
    histos.append(h_ttWW.Clone())
    histos.append(h_ttWZ.Clone())
    histos.append(h_ttZZ.Clone())
#    histos.append(h_ttWH.Clone())
#    histos.append(h_ttZH.Clone())
#    histos.append(h_tttJ.Clone())
#    histos.append(h_tttW.Clone())
#    histos.append(h_tttt.Clone())
#    histos.append(h_tzq.Clone())
#    histos.append(h_QCD50to80.Clone())
#    histos.append(h_QCD80to120.Clone())
#    histos.append(h_QCD120to170.Clone())
#    histos.append(h_QCD170to300.Clone())
#    histos.append(h_QCD300toinf.Clone())
    histos.append(h_TTTo2L.Clone())
    histos.append(h_TTTo1L.Clone())
    histos.append(h_DoubleMu.Clone()) 
    histos.append(h_SingleMu.Clone())

    for i in range(0,36):
      histos[i]=overunder_flowbin(histos[i])

    c1 = plot_DYregion.draw_plots(histos, 1, hists_name[ij], 0)
    del histos[:]
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  TTC_Analysis()
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

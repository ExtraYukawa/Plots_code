import ROOT 
import sys, os
from math import sqrt
import array

lumi = 1.0

xsec = {}

xsec['DY']     = 6077.22
xsec['osWW']   = 11.09
xsec['ssWW']   = 0.04932
xsec['WWdps']  = 1.62
xsec['WZew']   = 0.0163
xsec['WZqcd']  = 5.213
xsec['ZZ']     = 0.0086 
xsec['ZG']     = 0.1097 
xsec['WWW']    = 0.2086 
xsec['WWZ']    = 0.1707 
xsec['WZZ']    = 0.05709 
xsec['ZZZ']    = 0.01476 
xsec['TTTo2L'] = 88.3419
xsec['TTH']    = 0.5638
xsec['TTTT']   = 0.008213 
xsec['TTTW']   = 0.0007314 
xsec['TTTJ']   = 0.0003974 
xsec['TTG']    = 3.757
xsec['TTWH']   = 0.001141 
xsec['TTZH']   = 0.00113
xsec['TTWtoLNu'] = 0.2352
xsec['TTWtoQQ'] = 0.4867
xsec['TTZ']    = 0.2589
xsec['TTZtoQQ'] = 0.6012
xsec['TTWW']   = 0.01141
xsec['TTWZ']   = 0.004157
xsec['TTZZ']   = 0.002117
xsec['tZq']    = 0.07561
xsec['tW']     = 35.85
xsec['tbarW']  = 35.85
xsec['WLLJJ']  = 0.01628  #AN2019_089_v8 (page #75) is large, took from xsdb
xsec['WpWpJJ_EWK']  = 0.02597 #AN2019_089_v8 (page #75) is large, took from xsdb
xsec['ZZJJTo4L']  = 0.008645 # https://mattermost.web.cern.ch/cms-exp/pl/eyi4qm4agbdp7rm8hwu6m59umo
xsec['WpWpJJ_QCD']  = 0.02221 # https://mattermost.web.cern.ch/cms-exp/pl/eyi4qm4agbdp7rm8hwu6m59umo

def selections(analtype="ee"):
  if analtype == "ee":
    # define the filters here, 1:2mu, 2:1e1m, 3:2ele
    filters_mc="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && (nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && ttc_2P0F && (ttc_mll<60 || ttc_mll>120)"
    filters_mc_fake="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && (nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (ttc_mll<60 || ttc_mll>120)"
    filters_data="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F && (ttc_mll<60 || ttc_mll>120)"
    filters_data_fake="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F) && (ttc_mll<60 || ttc_mll>120)"
  elif  analtype == "emu":
    # define the filters here, 1:2mu, 2:1e1m, 3:2ele
    filters_mc="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && (nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && ttc_2P0F"
    filters_mc_fake="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter &&(nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
    filters_data="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"
    filters_data_fake="ttc_jets && ttc_region==2 && (ttc_l1_pt>30 || ttc_l2_pt>30) && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
  elif analtype == "mm":
    # define the filters here, 1:2mu, 2:1e1m, 3:2ele
    filters_mc="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && (nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && ttc_2P0F"
    filters_mc_fake="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && (nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
    filters_data="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"
    filters_data_fake="ttc_jets && ttc_region==1 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
  elif analtype == "test":
    filters_mc="ttc_nl && ttc_region==3 && ttc_l1_pt>30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && (nGenDressedLepton>1 || lhe_nlepton>1) && nHad_tau==0 && ttc_2P0F"
    filters_mc_fake="ttc_nl && ttc_region==3 && ttc_l1_pt>30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
    filters_data="ttc_nl && ttc_region==3 && ttc_l1_pt>30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"
    filters_data_fake="ttc_nl && ttc_region==3 && ttc_l1_pt>30 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
  elif analtype == "eenomllcut":
    # define the filters here, 1:2mu, 2:1e1m, 3:2ele
    filters_mc="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && ttc_2P0F"
    filters_mc_fake="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && lhe_nlepton>1 && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
    filters_data="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && ttc_2P0F"
    filters_data_fake="ttc_jets && ttc_region==3 && ttc_l1_pt>30 && ttc_met>30 && ttc_mll>20 && ttc_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0 && (ttc_1P1F || ttc_0P2F)"
  elif analtype == "mujets":
    filters_mc="bh_nl==1 && bh_region==1 && nHad_tau==0 && bh_jets==1"
    filters_mc_fake="bh_nl==1 && bh_region==1 && nHad_tau==0 && bh_jets==1 && bh_met > 35 && n_bjet_DeepB_loose >= 3"
    filters_data="bh_nl==1 && bh_region==1 && nHad_tau==0 && bh_jets==1 && bh_met > 35 && n_bjet_DeepB_loose >= 3"
    filters_data_fake="bh_nl==1 && bh_region==1 && nHad_tau==0 && bh_jets==1 && bh_met > 35 && n_bjet_DeepB_loose >= 3"
  elif analtype == "elejets":
    filters_mc="bh_nl==1 && bh_region==2 && nHad_tau==0 && bh_jets==1 && bh_met > 35"
    filters_mc_fake="bh_nl==1 && bh_region==2 && nHad_tau==0 && bh_jets==1 && bh_met > 35 && n_bjet_DeepB_loose >= 3"
    filters_data="bh_nl==1 && bh_region==2 && nHad_tau==0 && bh_jets==1 && bh_met > 35 && n_bjet_DeepB_loose >= 3"
    filters_data_fake="bh_nl==1 && bh_region==2 && nHad_tau==0 && bh_jets==1 && bh_met > 35 && n_bjet_DeepB_loose >= 3"
    
  else:
    print ("select correct selection string")
    filters_mc = ""
    filters_mc_fake=""
    filters_data=""
    filters_data_fake=""
    
  return filters_mc, filters_mc_fake, filters_data, filters_data_fake


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

# Trigger are updated as per 
# https://github.com/ExtraYukawa/TriggerScaleFactor/blob/a864ff3cff31d2daa0257027b1e86078c8dd8d13/Trigger_SF/GenTriggers.py

def all_trigger(df, year="2017"):
  if year == "2016APV":
    all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPLoose_Gsf")
  elif year == "2016postAPV":
    all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPLoose_Gsf")
  elif year == "2017":
    all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf")
    # this is just a TEST (but not present this data)
    # https://github.com/ExtraYukawa/Tasks/issues/60
    # all_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf) && HLT_Ele115_CaloIdVT_GsfTrkIdT")
  else:
    all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf")

  return all_trigger

def for_diele_trigger(df, year="2017"):
  if year == "2016APV" or year == "2016postAPV":
    ditri_ele_trigger = df.Filter("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ")
  else:
    ditri_ele_trigger = df.Filter("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ")
  return ditri_ele_trigger

def for_singleele_trigger_eechannel(df, year="2017"):
  if year == "2016APV" or year == "2016postAPV":
    sin_ele_trigger = df.Filter("!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPLoose_Gsf)")
  elif year == "2017":
    sin_ele_trigger = df.Filter("!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)")
    # this is just a TEST
    # sin_ele_trigger = df.Filter("!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf) && HLT_Ele115_CaloIdVT_GsfTrkIdT")
  else:
    sin_ele_trigger = df.Filter("(!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)) || (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)")

  return sin_ele_trigger

def for_singleele_trigger_emuchannel(df, year="2017"):
  if year == "2016APV":
    sin_ele_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) && (HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)")
  elif year == "2016postAPV":
    sin_ele_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele27_WPTight_Gsf)")
  else:
    sin_ele_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)")
  return sin_ele_trigger

def for_dimuon_trigger(df, year="2017"):
  if year == "2016APV":
    ditri_mu_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ)")
  elif year == "2016postAPV":
    ditri_mu_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ)")
  else:
    ditri_mu_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)")
  return ditri_mu_trigger

def for_singlemuon_trigger_mumuchannel(df, year="2017"):
  if year == "2016APV":
    single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ) && HLT_IsoMu27")
  elif year == "2016postAPV":
    single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ) && HLT_IsoMu27")
  else:
    single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27")
  return single_mu_trigger

def for_singlemuon_trigger_emuchannel(df, year="2017"):

  if year == "2016APV":
    single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL) && HLT_IsoMu27")
  elif year == "2016postAPV":
    single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27")
  else:
    single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27")
  return single_mu_trigger

def for_cross_trigger(df, year="2017"):
  if year == "2016APV":
    x_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL)")
  else:
    x_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)")
  return x_trigger



# Define the binning of the different variables to histogram
ranges = {
  # "ttc_l1_pt"              : (array.array('d', [20, 35, 50, 80, 120, 160, 200, 260] )), #Just for testing coarse binning
  # "ttc_l1_pt"              : (array.array('d', [i for i in range(0, 210+15, 15)] )), 
#  "DeepB_loose_j1_pt"        : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
#  "DeepB_loose_j2_pt"        : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
#  "DeepB_loose_j3_pt"        : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
#  #"loose_DeepB_j1_pt"        : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
#  #"loose_DeepB_j2_pt"        : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
#  #"loose_DeepB_j3_pt"        : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
#  "DeepB_loose_j1_eta"       : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
#  "DeepB_loose_j2_eta"       : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
#  "DeepB_loose_j3_eta"       : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
  "j1_pt"                    : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
  "j2_pt"                    : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
  "j3_pt"                    : (array.array('d', [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300, 325, 350, 400, 450, 500] )),
  "j1_eta"                   : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
  "j2_eta"                   : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
  "j3_eta"                   : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
  "l1_pt"                    : (array.array('d', [10, 20, 30, 40, 50, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210, 225, 250, 275, 300] )),
  "l1_eta"                   : (array.array('d', [-2.6+i*0.2 for i in range(0, 26+1, 1)] )),
  "MET_T1Smear_pt"           : (array.array('d', [i for i in range(0, 500+10, 10)] ))
  
  # "ttc_mll"               : (30, 0, 300), 
  #  "ttc_l1_eta"            : (12, -3.0, 3.0),
  #  "n_bjet_DeepB"          : (10, 0, 10),
  #  "n_cjet_DeepB_medium"   : (10, 0, 10),
  #  "n_cjet_DeepB_loose"    : (10, 0, 10),
  #  "GoodFatJet_pt"        : (200, 0 , 2000),
}

ranges_emu = {
  "max_lep_pt": (array.array('d', [i for i in range(0, 210+15, 15)] )), #NOTE: max_lep_pt = max(ttc_l1_pt, ttc_l2_pt) is defined in the ttc_emu.py file
}


######################################################

'''

RootFiles = {}
Trees = {}

#outdir = "/data1/zdemirag/Exo_Higgs_Analyzer/CMSSW_5_3_9/src/Oct14_NewReso_Root/met_pog_reso_x/higgsHistograms_"
outdir = "/eos/user/m/melu/TTC_Nanov8_new/"

#Samples = ['efake_dd','SinglePhotonParked','PJets_15to30','PJets_30to50','PJets_50to80','PJets_80to120','PJets_120to170','PJets_170to300', 'PJets_300to470', 'PJets_470to800', 'PJets_800to1400', 'PJets_1400to1800','PJets_1800', 'WGamma','DiPhotonJets', 'DiphotonBox_Pt_250toInf', 'DiphotonBox_Pt_25to250', 'WtoLNuTau' , 'WtoLNuMu', 'qcd_dd', 'ZGamma_Inclusive','DM','GJets_HT_40_100','GJets_HT_100_200','GJets_HT_200_400','GJets_HT_400','MChi_70','MChi_120','ZGToLLG']

#Samples = ['efake_dd','SinglePhotonParked', 'WGamma','DiPhotonJets', 'DiphotonBox_Pt_250toInf', 'DiphotonBox_Pt_25to250', 'WtoLNuTau' , 'WtoLNuMu', 'qcd_dd', 'ZGamma_Inclusive','GJets_HT_40To100','GJets_HT_100To200','GJets_HT_200To400','GJets_HT_400','MChi_70','MChi_120','MChi_80','MChi_90','MChi_100','ZGToLLG','DM','DM_AxialVector_10','DM_AxialVector_100','DM_AxialVector_1000','DM_AxialVector_200','DM_AxialVector_300','DM_AxialVector_500','DM_Vector_1','DM_Vector_10','DM_Vector_100','DM_Vector_1000','DM_Vector_300','DM_Vector_500']

Samples = ['DY', 'WJets', 'DoubleEGB', 'DoubleEGC', 'DoubleEGD', 'DoubleEGE', 'DoubleEGF', 'ttWZ']

for bg in Samples:
        RootFiles[bg] = TFile(outdir+bg+".root")
        #Trees[bg]     = RootFiles[bg].Get("Analyzer/AnalyzerTree")
        Trees[bg]     = RootFiles[bg].Get("Events")

######################################################

Nevents = {}

Nevents['DY'] = get_mcEventnumber(outdir+"DY.root")
Nevents['WJets'] = 100000 #similarly fix this
Nevents['ttWZ'] = 10000
Nevents['DoubleEG'] = 1
Nevents['DoubleEGB'] = 1
Nevents['DoubleEGC'] = 1
Nevents['DoubleEGD'] = 1
Nevents['DoubleEGE'] = 1
Nevents['DoubleEGF'] = 1

Nevents['DM'] = 84000#100000.
Nevents['DM_AxialVector_1'] = 50000.
Nevents['DM_AxialVector_10'] = 50000.
Nevents['DM_AxialVector_100'] = 50000.
Nevents['DM_AxialVector_1000'] = 50000.
Nevents['DM_AxialVector_200'] = 50000.
Nevents['DM_AxialVector_300'] = 50000.
Nevents['DM_AxialVector_500'] = 50000.

Nevents['DM_Vector_1'] = 50000.
Nevents['DM_Vector_10'] = 50000.
Nevents['DM_Vector_100'] = 50000.
Nevents['DM_Vector_1000'] = 50000.
Nevents['DM_Vector_300'] = 50000.
Nevents['DM_Vector_500'] = 50000.


Nevents['MChi_70'] = 199079
Nevents['MChi_80'] = 191194
Nevents['MChi_90'] = 191633
Nevents['MChi_100'] = 198266

Nevents['GJets_HT_40To100'] = 19844808 #19857930
Nevents['GJets_HT_100To200'] = 9588849 #9612703
Nevents['GJets_HT_200To400'] = 58627147 #3020693
#Nevents['GJets_HT_200To400'] = 4262287 #3020693
Nevents['GJets_HT_400'] = 9539562#9453426 #1414007


#Nevents['GJets_HT_40To100'] = 19824979  #19844808 #19857930
#Nevents['GJets_HT_100To200'] = 9588849 #9588849 #9612703
#Nevents['GJets_HT_200To400'] = 58272731   #4262287 #3020693
#Nevents['GJets_HT_400'] = 9453426  #9453426 #1414007

Nevents['ZGamma_Inclusive']  = 3169111.0  #6.32155e+05#12076.
#Nevents['ZGamma_Inclusive']  = 1466144
#sushil's sample
#Nevents['ZGamma_Inclusive']  = 43401

Nevents['ZGToLLG'] = 6583032 #6588161

Nevents['MChi_120'] = 184388.

Nevents['Data_VBF_2012C']      = 1.0
Nevents['SinglePhotonParked']            = 1.0
Nevents['qcd_dd']         = 1.0
Nevents['efake_dd']         = 1.0

#Nevents['Signal_VBF']      = 98000.0
#Nevents['Signal_GluGlu']   = 98000.0

Nevents['WGamma']          = 5000000.0

Nevents['DiphotonBox_Pt_250toInf']     = 500352.0
Nevents['DiphotonBox_Pt_25to250'] = 500050.0



#forgot to run on a file
Nevents['QCD_80to170']  = 22639900#34542672.0

# a file is missing fix the # of events
Nevents['QCD_170to250'] = 31646986.0

Nevents['QCD_250to350'] = 42292370.
Nevents['QCD_350'] = 34080630.
'''

######################################################

'''
xsec['WJets'] = 6077.22
xsec['ttWZ'] = 0.002453

xsec['DoubleEG'] = 1
xsec['DoubleEGB'] = 1
xsec['DoubleEGC'] = 1
xsec['DoubleEGD'] = 1
xsec['DoubleEGE'] = 1
xsec['DoubleEGF'] = 1

xsec['GJets_HT_40To100'] = 20930.0
xsec['GJets_HT_100To200'] = 5212.0
xsec['GJets_HT_200To400'] = 960.5
xsec['GJets_HT_400'] = 107.5



xsec['DM_AxialVector_1'] = 1.
xsec['DM_AxialVector_10'] = 0.001
xsec['DM_AxialVector_100'] = 1.
xsec['DM_AxialVector_1000'] = 1.
xsec['DM_AxialVector_200'] = 1.
xsec['DM_AxialVector_300'] = 1.
xsec['DM_AxialVector_500'] = 1.

xsec['DM_Vector_1'] = 1.
xsec['DM_Vector_10'] = 1.
xsec['DM_Vector_100'] = 1.
xsec['DM_Vector_1000'] = 1.
xsec['DM_Vector_300'] = 1.
xsec['DM_Vector_500'] = 1.


xsec['DM'] = 1.63721e-06

xsec['ZGamma_Inclusive'] = 123.9
#xsec['ZGamma_Inclusive'] = 93
#xsec['ZGamma_Inclusive'] = 34.316
xsec['ZGToLLG'] = 132.6

#xsec['MChi_70'] = 1.0
#xsec['MChi_80'] = 1.0
#xsec['MChi_90'] = 1.0
#xsec['MChi_100'] = 1.0
#xsec['MChi_120'] = 1.0

# SM higgs
xsec['MChi_70'] = 19.27
xsec['MChi_80'] = 19.27
xsec['MChi_90'] = 19.27
xsec['MChi_100'] = 19.27
xsec['MChi_120'] = 19.27

#Theory
#xsec['MChi_70'] = 1.090253
#xsec['MChi_80'] = 0.820263
#xsec['MChi_90'] = 0.544212
#xsec['MChi_100'] = 0.303971
#xsec['MChi_120'] = 0.017900

xsec['Data_VBF_2012C']            = 1.0
xsec['SinglePhotonParked']            = 1.0

xsec['qcd_dd']         = 1.0
xsec['efake_dd']         = 1.0

#Glu : 19.27 pb * BR (1.55 E-03) * nunu (~%20)
#xsec['Signal_GluGlu']   = 5.9737E-03
#VBF : 1.578 pb  * BR (1.55 E-03) * nunu (~%20)
#xsec['Signal_VBF']      = 0.489E-03

xsec['WGamma']          =  461.6

##xsec['DiphotonBox_Pt_250toInf']     = 1.0
##xsec['DiphotonBox_Pt_25to250'] = 1.0

xsec['DiphotonBox_Pt_250toInf']     = 0.00032
xsec['DiphotonBox_Pt_25to250'] = 15.50



xsec['PJets_15to30']     =  200061.7 
xsec['PJets_30to50']     =  19931.62 
xsec['PJets_50to80']     =  3322.309 
xsec['PJets_80to120']    =  558.2865 
xsec['PJets_120to170']   =  108.0068 
xsec['PJets_170to300']   =  30.12207 
xsec['PJets_300to470']   =  2.138632 
xsec['PJets_470to800']   =  0.2119244 
xsec['PJets_800to1400']  =  0.007077847 
xsec['PJets_1400to1800'] =  4.510327E-5 
xsec['PJets_1800']       =  1.867141E-6 


xsec['DiPhotonJets']     = 1.0
xsec['W2lnuEl']      = 9170.0 
xsec['WtoLNuTau']     = 9170.0 
xsec['WtoLNuMu']      = 9170.0

# 2.886E8 *  0.0101 
xsec['QCD_20to30']   = 2.91486000000000000e+06
#  7.433E7 *  0.0621 
xsec['QCD_30to80']   = 4.61589300000000000e+06
# 1191000.0  *  0.1539 
xsec['QCD_80to170']  =  1.83294900000000023e+05
# 30990.0 *  0.148 
xsec['QCD_170to250'] =  4.58651999999999953e+03
#4250.0* 0.131
xsec['QCD_250to350'] = 556.75
#810.0 *0.11
xsec['QCD_350'] =  89.1
'''

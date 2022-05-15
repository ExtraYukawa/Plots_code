import ROOT
import time
import os
import math
from math import sqrt
import argparse

TTC_header_path = os.path.join("TTC.h")
ROOT.gInterpreter.ProcessLine('#include "TTC.h"')

RDataFrame = ROOT.RDataFrame

def main():
  usage = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(usage)
  parser.add_argument('-i', '--inputs',dest='inputs',help='input root file',default='dummy.root')
  args = parser.parse_args()
  inputroot=args.inputs
  output_name='output.root'
  TTC_Analysis(inputroot,output_name)

def overunder_flowbin(h1):
  h1.SetBinContent(1,h1.GetBinContent(0)+h1.GetBinContent(1))
  h1.SetBinError(1,sqrt(h1.GetBinError(0)*h1.GetBinError(0)+h1.GetBinError(1)*h1.GetBinError(1)))
  h1.SetBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX())+h1.GetBinContent(h1.GetNbinsX()+1))
  h1.SetBinError(h1.GetNbinsX(),sqrt(h1.GetBinError(h1.GetNbinsX())*h1.GetBinError(h1.GetNbinsX())+h1.GetBinError(h1.GetNbinsX()+1)*h1.GetBinError(h1.GetNbinsX()+1)))
  return h1

def all_trigger(df):
  all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf")
  return all_trigger

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


def TTC_Analysis(inputfile,outputname):
  fout = ROOT.TFile.Open(outputname,'recreate')

  filein=ROOT.TFile.Open(inputfile)
  hweight=ROOT.TH1D()
  hweight=filein.Get("nEventsGenWeighted")
  fout.cd()
  hweight.Write()
  filein.Close()

  filters_ee="FILTERS_EE"
  filters_em="FILTERS_EM"
  filters_mm="FILTERS_MM"

  df_histos=[]

  df_tree_ee = ROOT.RDataFrame("Events", inputfile)
  df_filter_ee = df_tree_ee.Filter(filters_ee)
  for i in hists_name:
    df_histo = df_filter_ee.Histo1D((i+'_ee','',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_histos.append(df_histo)

  df_tree_em = ROOT.RDataFrame("Events", inputfile)
  df_filter_em = df_tree_em.Filter(filters_em)
  for i in hists_name:
    df_histo = df_filter_em.Histo1D((i+'_em','',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_histos.append(df_histo)

  df_tree_mm = ROOT.RDataFrame("Events", inputfile)
  df_filter_mm = df_tree_mm.Filter(filters_mm)
  for i in hists_name:
    df_histo = df_filter_mm.Histo1D((i+'_mm','',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_histos.append(df_histo)

  fout.cd()
  for ij in range(0,3*len(hists_name)):
    h_temp = df_histos[ij].GetValue()
    h_temp.Write()

  fout.Close()

if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  print "Job starts"
  main()
  end = time.time()
  end1 = time.clock()
  print "wall time:", end-start
  print "process time:", end1-start1

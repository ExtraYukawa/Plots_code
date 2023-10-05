#==============
# Last used:
# python bhplus_kinematics.py --era 2017 --channel mujets --saveDir 2017_sel1_mujets_kinematics
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

SAVEFORMATS  = "png" #pdf,png,C"
SAVEDIR      = None

from argparse import ArgumentParser
parser = ArgumentParser()

parser.add_argument("--era", dest="era", default="2016APV",
                    help="When making the plots, read the files with this era(years), default: 2016APV")

parser.add_argument("--channel", dest="channel", default="mujets",
                    help="Channel for drawing plots [default: mujets]")

parser.add_argument("-s", "--saveFormats", dest="saveFormats", default = SAVEFORMATS,
                      help="Save formats for all plots [default: %s]" % SAVEFORMATS)

parser.add_argument("--saveDir", dest="saveDir", default=SAVEDIR, 
                      help="Directory where all pltos will be saved [default: %s]" % SAVEDIR)

parser.add_argument("-draw_data", "--draw_data", action="store_true", dest="draw_data", default=False,
                    help="make it to True if you want to draw_data on MC stacks")

opts = parser.parse_args()

TTC_header_path = os.path.join("TTC.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

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

  '''
  if not isData:
    df_xyz_tree = df_xyz_tree.Define("trigger_SF","trigger_sf_ee_"+opts.era+"(ttc_l1_pt,ttc_l2_pt)")
    if  "dy" in str(flist[0]).split('/')[-1].lower() or "ttto2l" in str(flist[0]).split('/')[-1].lower():
      print ("Input for CFlip (DY and TTTo2L): ", str(flist[0]).split('/')[-1])
      df_xyz_tree = df_xyz_tree.Define("CFlip_SF","chargeflip_SF_"+opts.era+"("+str(1)+", ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, "+str(3)+", "+str(0)+", GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")
    else:
      print ("Input for CFlip: ", str(flist[0]).split('/')[-1])
      df_xyz_tree = df_xyz_tree.Define("CFlip_SF","chargeflip_SF_"+opts.era+"("+str(0)+", ttc_l1_pt, ttc_l1_eta, ttc_l1_phi, ttc_l2_pt, ttc_l2_eta, ttc_l2_phi, "+str(3)+", "+str(0)+", GenDressedLepton_eta, GenDressedLepton_phi, GenDressedLepton_pdgId)")
    
    # check if the events are fake or not
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_ee_"+opts.era+"(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta, "+str(isData).lower()+")")
      if opts.era == "2017":
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*fakelep_weight*genWeight/abs(genWeight)")
      else:
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*fakelep_weight*genWeight/abs(genWeight)")
    else:
      if opts.era == "2017":
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*PrefireWeight*trigger_SF*CFlip_SF*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
      else:
        df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*trigger_SF*CFlip_SF*Electron_RECO_SF[ttc_l1_id]*Electron_RECO_SF[ttc_l2_id]*genWeight/abs(genWeight)")
  else:
    if isFake:
      df_xyz_tree = df_xyz_tree.Define("fakelep_weight","fakelepweight_ee_"+opts.era+"(ttc_1P1F,ttc_0P2F,ttc_lep1_faketag,electron_conePt[ttc_l1_id],ttc_l1_eta,electron_conePt[ttc_l2_id],ttc_l2_eta, "+str(isData).lower()+")")
  '''
  df_xyz_tree = df_xyz_tree.Define("genweight","puWeight*genWeight/abs(genWeight)")
  # common for data/MC
  df_xyz = df_xyz_tree.Filter(filters)
  
  '''
  if not isData:
    df_xyz_trigger = all_trigger(df_xyz, opts.era)
  else:
    if "doubleeg" in str(flist[0]).split('/')[-1].lower():
      print ("doubleEle")
      df_xyz_trigger = for_diele_trigger(df_xyz, opts.era)
    elif "singleeg" in str(flist[0]).split('/')[-1].lower():
      print ("singleEle")
      df_xyz_trigger = for_singleele_trigger_eechannel(df_xyz, opts.era)
    elif "egamma" in str(flist[0]).split('/')[-1].lower():
      print ("Egamma")
      df_xyz_trigger = for_singleele_trigger_eechannel(df_xyz, opts.era)
    else:
      print ("choose correct trigger function")
  '''
  # Histogram definition
  df_xyz = df_xyz.Define("loose_DeepB_j1_pt","Jet_pt_nom[tightJets_b_DeepJetloose_id[0]]")
  df_xyz = df_xyz.Define("loose_DeepB_j2_pt","Jet_pt_nom[tightJets_b_DeepJetloose_id[1]]")
  df_xyz = df_xyz.Define("loose_DeepB_j3_pt","Jet_pt_nom[tightJets_b_DeepJetloose_id[2]]")
  if opts.channel == "mujets":
    df_xyz = df_xyz.Define("l1_pt","Muon_corrected_pt[tightMuons_id[0]]")
    df_xyz = df_xyz.Define("l1_eta","Muon_eta[tightMuons_id[0]]")
  elif opts.channel == "ejets":
    df_xyz = df_xyz.Define("l1_pt","Electron_pt[tightElectrons_id[0]]")
    df_xyz = df_xyz.Define("l1_eta","Electron_eta[tightElectrons_id[0]]")
  else:
    pass

  # put histos in a list
  df_xyz_histos = []
  for variable in variables:
    print ("variable", variable)
    if not isData:
      #df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',ranges[variable][0], ranges[variable][1], ranges[variable][2]), variable,'genweight')
      # df_xyz_histo = df_xyz_trigger.Histo1D((variable,'',len(binning)-1 , binning), variable,'genweight')
      # print ("test1: ", ranges[variable])
      df_xyz_histo = df_xyz.Histo1D((variable,'',len(ranges[variable])-1, ranges[variable]), variable,'genweight')
    else:
      if isFake:
        df_xyz_histo = df_xyz.Histo1D((variable,'',len(ranges[variable])-1 , ranges[variable]), variable,'fakelep_weight')
      else:
        df_xyz_histo = df_xyz.Histo1D((variable,'',len(ranges[variable])-1 , ranges[variable]), variable)
    h = df_xyz_histo.GetValue()
    
    # print ("1="*50)
    # print ("binning: ", binning)
    # df_hh = df_xyz.Histo1D(("ttc_l1_pt",'',14,0,210), "ttc_l1_pt",'genweight')
    # df_hh = df_xyz.Histo1D(("ttc_l1_pt",'',len(binning)-1 , binning), "ttc_l1_pt",'genweight')
    # hh = df_hh.GetValue()
    # print ("hh Mean: ", hh.GetMean())
    # sys.exit(1)
    h.SetDirectory(0)
    df_xyz_histos.append(h.Clone())
    ROOT.TH1.AddDirectory(0)

  return df_xyz_histos


# Data paths
if opts.era == "2017":
  print ("Reading 2017 files")
  path=' /eos/cms/store/group/phys_b2g/ExYukawa/bHplus/2017/'
elif opts.era == "2018" or opts.era == "2016apv" or opts.era == "2016posrapv":
  print ("Not available yet")
  raise Exception ("select only 2017!")
else:
  raise Exception ("select correct era!")

singleEle_names = get_filelist(path, ["SingleEGB.root","SingleEGC.root","SingleEGD.root","SingleEGE.root","SingleEGF.root"])
doubleEle_names = get_filelist(path, ["DoubleEGB.root","DoubleEGC.root","DoubleEGD.root","DoubleEGE.root","DoubleEGF.root"])

egamma_names = get_filelist(path, ["EGammaA.root","EGammaB.root","EGammaC.root","EGammaD_0.root","EGammaD_1.root"])

# MC Location 
DY_list = get_filelist(path, ['DYnlo.root']) #after discussion with Meng on 14Jul2022

def bhplus_kinematics(opts):

  histos = []

  variables = ranges.keys()
  for ij in range(0,len(variables)):
    print (variables[ij])
  
  # Channel
  print ("channel:", opts.channel)
  # import selections
  filters_mc, filters_mc_fake, filters_data, filters_data_fake = selections(opts.channel)
  print ("filters_mc:        ", filters_mc)
  print ("filters_mc_fake:   ", filters_mc_fake)
  print ("filters_data:      ", filters_data)
  print ("filters_data_fake: ", filters_data_fake)

  # old test
  #df_DY_histos = histos_book(DY_list, filters_mc, variables, False, False) #isData, isFake
  
  ###############
  # Samples list
  samples = ["200","350","500","800","1000","TTTo1L"]
  
  h_prefit = {}
  for sample in samples:
    if sample == "TTTo1L":
      mfile = get_filelist(path, ['TTTo1L_default.root'])
    else:
      mfile = get_filelist(path, ['CGToBHpm_MH-'+sample+'_rtt06_rtc04.root'])
    h_prefit[sample] = histos_book(mfile, filters_mc, variables, False, False) #isData, isFake
    
  # print h_prefit
  # print ("df_DY_histos[0] integral", df_DY_histos[0].Integral())
  
  # Loop over histograms  
  for ij in range(0,len(variables)):
    for key in h_prefit:
      histos.append(h_prefit[key][ij].Clone(h_prefit[key][ij].GetName()+"_"+key)) #put name info before add to histos
    
    # save per-variable one root file
    c1 = plot.draw_1Dplot(opts, histos, variables[ij], 0)
    del histos[:]
    
    #print ("Now get values")
    #h_DY = df_DY_histos[ij].Clone()
    # print ("h_DY.Integral()", h_DY.Integral())
    # sys.exit(1)
    #h_DY.Scale(xsec['DY']/get_mcEventnumber(DY_list))
    #histos.append(h_DY.Clone())

    #for i in range(0,64):
    #  histos[i]=overunder_flowbin(histos[i])
 
if __name__ == "__main__":
  start = time.time()
  start1 = time.clock() 
  bhplus_kinematics(opts)
  end = time.time()
  end1 = time.clock()
  print ("wall time:", end-start)
  print ("process time:", end1-start1)

import ROOT
import time
import os
import math
import sys
from math import sqrt
from array import array
import plot_DYregion_2018
ROOT.gROOT.SetBatch(True)

import CMSTDRStyle
CMSTDRStyle.setTDRStyle().cd()
#import CMSstyle


from argparse import ArgumentParser
parser = ArgumentParser()

# https://martin-thoma.com/how-to-parse-command-line-arguments-in-python/
# Add more options if you like
parser.add_argument("--period", dest="period", default="B",
                    help="When making the plots, read the files with this string, default: B")

opts = parser.parse_args()


TTC_header_path = os.path.join("HEM_2018.h")
ROOT.gInterpreter.Declare('#include "{}"'.format(TTC_header_path))

# the EnableImplicitMT option should only use in cluster, at lxplus, it will make the code slower(my experience)
#ROOT.ROOT.EnableImplicitMT()

nthreads = 4
ROOT.ROOT.EnableImplicitMT(nthreads)

def overunder_flowbin(h1):
  h1.SetBinContent(1,h1.GetBinContent(0)+h1.GetBinContent(1))
  h1.SetBinError(1,sqrt(h1.GetBinError(0)*h1.GetBinError(0)+h1.GetBinError(1)*h1.GetBinError(1)))
  h1.SetBinContent(h1.GetNbinsX(),h1.GetBinContent(h1.GetNbinsX())+h1.GetBinContent(h1.GetNbinsX()+1))
  h1.SetBinError(h1.GetNbinsX(),sqrt(h1.GetBinError(h1.GetNbinsX())*h1.GetBinError(h1.GetNbinsX())+h1.GetBinError(h1.GetNbinsX()+1)*h1.GetBinError(h1.GetNbinsX()+1)))
  return h1

def get_mcEventnumber(filename):
  # print 'opening file ', filename
  print('opening file ', filename)
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

def for_singleele_trigger_eechannel(df): #fixme gkole
  sin_ele_trigger = df.Filter("(!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)) || (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)")
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

doubleMu_names = ROOT.std.vector('string')()
for f in ["DoubleMuonB.root"]: #,"DoubleMuonB.root","DoubleMuonC.root","DoubleMuonD_0.root","DoubleMuonD_1.root"]:
  doubleMu_names.push_back(path+f)

singleMu_names = ROOT.std.vector('string')()
for f in ["SingleMuonA.root","SingleMuonB.root","SingleMuonC.root","SingleMuonD_0.root","SingleMuonD_1.root"]:
  singleMu_names.push_back(path+f)

singleEle_names = ROOT.std.vector('string')()
#for f in ["EGammaA.root","EGammaB.root","EGammaC.root","EGammaD_0.root","EGammaD_1.root"]:
if opts.period == "B":
  for f in ["EGammaB.root"]:
    singleEle_names.push_back(path+f)
elif opts.period == "C":
  for f in ["EGammaC.root"]:
    singleEle_names.push_back(path+f)
elif opts.period == "D":
  for f in ["EGammaD_0.root", "EGammaD_1.root"]:
    singleEle_names.push_back(path+f)
else:
  raise Exception ("select correct era!")

muonEle_names = ROOT.std.vector('string')()
for f in ["MuonEGA.root","MuonEGB.root","MuonEGC.root","MuonEGD_0.root","MuonEGD_1.root"]:
  muonEle_names.push_back(path+f)

DY_list = ROOT.std.vector('string')()
for f in ['DY.root']:
  DY_list.push_back(path+f)


def HEM_Eta_Vs_Phi(opts):
  
  #etabin=array('d',[-2.5, -2.0, 0.0, 2.0, 2.5])  #array('d',[round(-5.0+i*0.2, 2) for i in range(0, 50+1, 1)]) 
  #phibin=array('d',[-3.5, -3.0, -2.0, 0.0, 2.0, 3.5]) #array('d',[round(-3.5+i*0.2, 2) for i in range(0, 35+1, 1)])
  etabin=array('d',[round(-5.0+i*0.2, 2) for i in range(0, 50+1, 1)])
  phibin=array('d',[round(-3.5+i*0.2, 2) for i in range(0, 35+1, 1)]) 
  
  # define histogram
  h2_deno=ROOT.TH2D('','',len(etabin)-1,etabin,len(phibin)-1,phibin)
  h2_nume=ROOT.TH2D('','',len(etabin)-1,etabin,len(phibin)-1,phibin)
  h2_deno_model=ROOT.RDF.TH2DModel(h2_deno)
  h2_nume_model=ROOT.RDF.TH2DModel(h2_nume)
  
  # define the filters here, 1:2mu, 2:1e1m, 3:2ele
  TTBARfilters="OPS_region==3 && OPS_2P0F && OPS_z_mass>20 && (OPS_z_mass<76 || OPS_z_mass>106) && n_tight_jet>1 && n_bjet_DeepB>0 && OPS_l1_pt>30 && OPS_l2_pt>20 && OPS_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0"
  
  print ("1")
  df_SingleEle_deno_tree = ROOT.RDataFrame("Events", singleEle_names)
  print(' '.join(map(str, singleEle_names)))
  
  # df_SingleEle_deno_tree = df_SingleEle_deno_tree.Define("abs_l1eta","abs(l1_eta)")
  df_SingleEle_deno_tree = df_SingleEle_deno_tree.Define("jet1_eta","Jet_eta[0]")
  df_SingleEle_deno_tree = df_SingleEle_deno_tree.Define("jet1_phi","Jet_phi[0]")
  
  df_SingleEle_deno = df_SingleEle_deno_tree.Filter(TTBARfilters)
  print ("3")
  df_SingleEle_deno_trigger = for_singleele_trigger_eechannel(df_SingleEle_deno)
  print ("4")
  df_SingleEle_deno_histo = df_SingleEle_deno_trigger.Histo2D(h2_deno_model,"jet1_eta","jet1_phi")
  print ("5")
  # sys.exit(1)
  #print "6"
  h_SingleEle_deno=df_SingleEle_deno_histo.GetValue()
  print ("7")
  

  c1 = ROOT.TCanvas() #'','',800,600)
  pad = ROOT.TPad()
  pad.Draw()
  print ("cavas draw")
  # h_SingleEle_deno.SetTitle('t#bar{t} region: 2018 '+opts.period+' data') # not working
  h_SingleEle_deno.GetXaxis().SetTitle("#eta")
  h_SingleEle_deno.GetYaxis().SetTitle("#phi")
  
  
  h_SingleEle_deno.Draw("colz")
  cms_label = ROOT.TLatex()
  cms_label.SetTextSize(0.04)
  cms_label.DrawLatexNDC(0.16, 0.96, "#bf{CMS Preliminary}")
  header = ROOT.TLatex()
  header.SetTextSize(0.03)
  hdrstring = '#sqrt{s} = 13 TeV,  2018 '+opts.period+' data'
  header.DrawLatexNDC(0.63, 0.96, hdrstring)
  
  print ("histo draw on canvas")
  c1.SaveAs('TTbar_HEM_'+opts.period+'.pdf')
  print ("save the canvas")
  
  # return c1
  #pad.Close()
  


# Draw the pt, eta, phi of the leading jet(in HEM and outside HEM region)
hists_name = ['jet1_pt','jet1_eta','jet1_phi']
hists_xtitle = ['Leading jet p_{T}', 'Leading jet #eta', 'Leading jet #phi']

#histograms bins
histos_bins = {
  hists_name[0]:20,
  hists_name[1]:50,
  hists_name[2]:20
}

#low edge
histos_bins_low = {
  hists_name[0]:0,
  hists_name[1]:-5,
  hists_name[2]:-4
}

#high edge
histos_bins_high = {
  hists_name[0]:200,
  hists_name[1]:5,
  hists_name[2]:4
}


def HEM_1D_plots(opts):

  TTBARfilters="OPS_region==3 && OPS_2P0F && OPS_z_mass>20 && (OPS_z_mass<76 || OPS_z_mass>106) && n_tight_jet>1 && n_bjet_DeepB>0 && OPS_l1_pt>30 && OPS_l2_pt>20 && OPS_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0"
  
  # TTBARfilters="Flag_goodVertices"
  # Becarefull about !(All(bla bla))
  # inHEM  = "All(Jet_eta > -3.2) && All(Jet_eta < -1.3)" #&& All(Jet_phi > -1.57)" # && All(Jet_phi < -0.87)" # All is working ROOT>6.20
  # outHEM = "All(Jet_eta < -3.2) && All(Jet_eta > -1.3)" #&& All(Jet_phi < -1.57)" # && All(Jet_phi > -0.87)" # All is working ROOT>6.20
  
  print ("1")
  df_SingleEle_tree = ROOT.RDataFrame("Events", singleEle_names)
  
  print(' '.join(map(str, singleEle_names)))
  
  df_SingleEle_tree = df_SingleEle_tree.Define("jet1_pt","Jet_pt[0]")
  df_SingleEle_tree = df_SingleEle_tree.Define("jet1_eta","Jet_eta[0]")
  df_SingleEle_tree = df_SingleEle_tree.Define("jet1_phi","Jet_phi[0]")
  
  
  df_SingleEle = df_SingleEle_tree.Filter(TTBARfilters)
  
  print ("1.5")
  df_SingleEle_inHEM  = df_SingleEle.Filter("filterHEM(Jet_eta, Jet_phi)","test")
  #df_z_dr = df_z_idx.Filter("filter_z_dr(Z_idx, Electron_eta, Electron_phi)",
   #                           "Delta R separation of Electrons building Z system")
  print ("1.6")
  df_SingleEle_outHEM = df_SingleEle.Filter("notHEM(Jet_eta, Jet_phi)","not HEM")

  print ("2")
  df_SingleEle_ttbar_trigger  = for_singleele_trigger_eechannel(df_SingleEle)
  df_SingleEle_inHEM_trigger  = for_singleele_trigger_eechannel(df_SingleEle_inHEM)
  df_SingleEle_outHEM_trigger = for_singleele_trigger_eechannel(df_SingleEle_outHEM)
  print ("3")

  df_SingleEle_inHEM_histos = []
  df_SingleEle_outHEM_histos = []

  for hist in hists_name:
    df_SingleEle_inHEM_histo  = df_SingleEle_inHEM_trigger.Histo1D((hist,"",histos_bins[hist] ,histos_bins_low[hist], histos_bins_high[hist]), hist)  
    df_SingleEle_inHEM_histos.append(df_SingleEle_inHEM_histo)
    
    df_SingleEle_outHEM_histo = df_SingleEle_outHEM_trigger.Histo1D((hist,"",histos_bins[hist] ,histos_bins_low[hist], histos_bins_high[hist]), hist)
    df_SingleEle_outHEM_histos.append(df_SingleEle_outHEM_histo)

  print ("4")
  #h_SingleEle_ttbar  = df_SingleEle_ttbar_histo.GetValue()
  
  histos = []
  histosoutHEM = []
  for ij in range(0,len(hists_name)):
    h_SingleEle_inHEM  = df_SingleEle_inHEM_histos[ij].GetValue()
    histos.append(h_SingleEle_inHEM)
    h_SingleEle_outHEM  = df_SingleEle_outHEM_histos[ij].GetValue()
    histosoutHEM.append(h_SingleEle_outHEM)
    
  #print ("Integral for inHEM",  h_SingleEle_inHEM.Integral())
  
  for ij in range(0, len(histos)):
    c1 = ROOT.TCanvas() #'','',800,600)
    pad = ROOT.TPad()
    c1.SetLogy(0)
    pad.Draw()
    histos[ij].SetLineColor(ROOT.kRed)
    histosoutHEM[ij].GetXaxis().SetTitle(hists_xtitle[ij])
    histosoutHEM[ij].SetLineColor(ROOT.kBlue)
    histosoutHEM[ij].Draw("hist")
    histos[ij].Draw("hist same")
    print ("Integral for in-HEM: ", histos[ij].Integral())
    print ("Integral for out-HEM: ", histosoutHEM[ij].Integral())

    # Add legend
    legend = ROOT.TLegend(0.62, 0.70, 0.82, 0.88)
    legend.SetFillColor(0)
    legend.SetBorderSize(0)
    legend.SetTextSize(0.03)
    legend.AddEntry(histos[ij], "in-HEM", "f")
    legend.AddEntry(histosoutHEM[ij], "out-HEM", "f")
    legend.Draw()

    c1.SaveAs('/eos/user/g/gkole/www/public/TTC/19Apr2022/TTbar_'+histos[ij].GetName()+'_'+opts.period+'.pdf')
    del c1
  # c1.SaveAs('TTbar_HEM_'+opts.period+'.pdf')
  print ("save the canvas")
  
  del histos[:]
    
def TTC_Analysis():

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

  df_SingleMu_tree = ROOT.RDataFrame("Events", singleMu_names)
  df_SingleMu = df_SingleMu_tree.Filter(filters)
  df_SingleMu_trigger = for_singlemuon_trigger_mumuchannel(df_SingleMu)
  df_SingleMu_histos=[]
  for i in hists_name:
    df_SingleMu_histo = df_SingleMu_trigger.Histo1D((i,'',histos_bins[i],histos_bins_low[i],histos_bins_high[i]), i)
    df_SingleMu_histos.append(df_SingleMu_histo)

  for ij in range(0,len(hists_name)):
    df_DY_histos[ij].Draw()
    df_SingleMu_histos[ij].Draw()

# ROOT version 6.14 don;t have function "ROOT.RDF.RunGraphs"
#  ROOT.RDF.RunGraphs({df_ZZG_histo, df_ZZ_histo, df_ggZZ_4e_histo,df_ggZZ_4mu_histo, df_ggZZ_4tau_histo, df_ggZZ_2e2mu_histo,df_ggZZ_2e2tau_histo, df_ggZZ_2mu2tau_histo, df_TTZ_histo,df_TTG_histo, df_WWZ_histo, df_WZG_histo,df_WZZ_histo, df_ZZZ_histo, df_WZTo3L_histo,df_WZTo2L_histo, df_ZG_histo})

    h_DY = df_DY_histos[ij].GetValue()
    h_SingleMu = df_SingleMu_histos[ij].GetValue()

    h_DY.Scale(DY_xs/DY_ev)

    histos.append(h_DY.Clone())
    histos.append(h_SingleMu.Clone())

    for i in range(0,36):
      histos[i]=overunder_flowbin(histos[i])

    c1 = plot_DYregion_2018.draw_plots(histos, 1, hists_name[ij], 0)
    del histos[:]
 
if __name__ == "__main__":
  #start = time.time()
  #start1 = time.clock() 


  # HEM_Eta_Vs_Phi(opts)
  # print ("HEM 2D plots are done!")

  HEM_1D_plots(opts)
  print ("back in main()")

  #end = time.time()
  #end1 = time.clock()
  #print "wall time:", end-start
  #print "process time:", end1-start1

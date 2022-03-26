#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TFile.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TStyle.h"
#include <string>
#include <iostream>
#include "TTC.h"
#include <time.h>
#include <chrono>


using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using namespace std;


RNode pass_AllTrigger(RNode df)
{
  auto all_trigger = df.Filter("HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8 || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_IsoMu27 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf");
  return all_trigger;
}

RNode pass_diele_trigger(RNode df)
{
  auto ditri_ele_trigger = df.Filter("HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ");
  return ditri_ele_trigger;
}

RNode for_singleele_trigger_eechannel(RNode df)
{
  auto sin_ele_trigger = df.Filter("!(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL) && !(HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)");
  return sin_ele_trigger;
}

RNode for_singleele_trigger_emuchannel(RNode df)
{
  auto sin_ele_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ) && !(HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && (HLT_passEle32WPTight || HLT_Ele35_WPTight_Gsf)");
  return sin_ele_trigger;
}

RNode for_dimuon_trigger(RNode df)
{
  auto ditri_mu_trigger = df.Filter("(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8)");
  return ditri_mu_trigger;
}

RNode for_singlemuon_trigger_mumuchannel(RNode df)
{
  auto single_mu_trigger = df.Filter("!(HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass8) && HLT_IsoMu27");
  return single_mu_trigger;
}

RNode for_singlemuon_trigger_emuchannel(RNode df)
{
  auto single_mu_trigger = df.Filter("!(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ) && HLT_IsoMu27");
  return single_mu_trigger;
}

RNode for_cross_trigger(RNode df)
{
  auto x_trigger = df.Filter("(HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ)");
  return x_trigger;
}

RNode Event_sel(RNode df)
{
  auto df_pass = df.Filter("OPS_region==1 && OPS_2P0F && OPS_z_mass>60 && OPS_z_mass<120 && OPS_l1_pt>30 && OPS_l2_pt>20 && OPS_drll>0.3 && Flag_goodVertices && Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter && Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && nHad_tau==0");
  return df_pass;
}

float get_mcEventnumber(std::string filename)
{
  std::cout<<"reading init events number of process "<<filename<<std::endl;
  float nevent_temp=0.;
  auto ftemp=TFile::Open("/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/MC_event.root");
  std::string hist_name="nEventsGenWeighted_"+filename;
  auto htemp=ftemp->Get<TH1D>(hist_name.c_str());
  nevent_temp=nevent_temp+htemp->GetBinContent(1);
  ftemp->Close();
  return nevent_temp;
}

std::string MC_list[33]={"DY","WJets","osWW","ssWW","WWdps","WZ_ew","WZ_qcd","ZZ","WWW","WWZ","WZZ","ZZZ","tsch","t_tch","tbar_tch","tW","tbarW","ttWtoLNu","ttWtoQQ","ttZ","ttZtoQQ","ttH","ttWW","ttWZ","ttZZ","ttWH","ttZH","tttW","tttJ","tttt","tzq","TTTo2L","TTTo1L"};
std::string MC_category[33]={"DY","WJet","VV","VV","VV","VV","VV","VV","VVV","VVV","VVV","VVV","SingleTop","SingleTop","SingleTop","SingleTop","SingleTop","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","TTXorXX","tZq","TT"};
float MC_xs[33]={6022.77, 61526.7, 11.09, 0.04932, 1.62, 0.0163, 5.213, 0.0086, 0.2086, 0.1707, 0.05709, 0.01476, 3.36, 136.02, 80.95, 35.85, 35.85, 0.1792, 0.3708, 0.2589, 0.6012, 0.5269, 0.007003, 0.002453, 0.001386, 0.00114, 0.00113, 0.00073, 0.0004, 0.0082, 0.07561, 88.3419, 365.4574};
int MC_color[33]={632, 593, 425, 425, 425, 425, 425, 425, 811, 811, 811, 811, 920, 920, 920, 920, 920, 876, 876, 876, 876, 876, 876, 876, 876, 876, 876, 876, 876, 876, 396, 600, 600};

void histo(std::string hist_name_in, int nbin_in, float binlow_in, float binhigh_in)
{
  // Enable multi-threading
  ROOT::EnableImplicitMT();

  std::string path = "/eos/cms/store/group/phys_top/ExtraYukawa/TTC_version9/";
  float lumi = 41800.;
  
  ROOT::RDataFrame di_mu("Events",{path+"DoubleMuonB.root",path+"DoubleMuonC.root",path+"DoubleMuonD.root",path+"DoubleMuonE.root",path+"DoubleMuonF.root"});
  auto di_mu_trigger = for_dimuon_trigger(di_mu);
  auto di_mu_sel = Event_sel(di_mu_trigger);
  std::cout<<"Processing DiMu"<<std::endl;
  std::string dimu_hist_name_emp = hist_name_in+"__DiMu";
  auto hist_dimu_temp = di_mu_sel.Histo1D({dimu_hist_name_emp.c_str(),dimu_hist_name_emp.c_str(),nbin_in,binlow_in,binhigh_in},hist_name_in.c_str());
  TH1D hist_dimu = hist_dimu_temp.GetValue();

  ROOT::RDataFrame single_mu("Events",{path+"SingleMuonB.root",path+"SingleMuonC.root",path+"SingleMuonD.root",path+"SingleMuonE.root",path+"SingleMuonF.root"});
  auto single_mu_trigger = for_singlemuon_trigger_mumuchannel(single_mu);
  auto single_mu_sel = Event_sel(single_mu_trigger);
  std::cout<<"Processing SingleMu"<<std::endl;
  std::string simu_hist_name_emp = hist_name_in+"__SiMu";
  auto hist_singlemu_temp = single_mu_sel.Histo1D({simu_hist_name_emp.c_str(),simu_hist_name_emp.c_str(),nbin_in,binlow_in,binhigh_in},hist_name_in.c_str());
  TH1D hist_singlemu = hist_singlemu_temp.GetValue();

  std::string appendix=".root";
  int n_MC=sizeof(MC_list)/sizeof(MC_list[0]);
  std::vector<TH1D> mc_histos;
  for (int im=0; im< n_MC;im++){
    ROOT::RDataFrame mc_temp("Events",path+MC_list[im]+".root");
    auto mc_trigger = pass_AllTrigger(mc_temp);
    auto mc_sel = Event_sel(mc_trigger);
    std::cout<<"Processing "<<MC_list[im]<<std::endl;
    std::string hist_name_temp=hist_name_in+"__"+MC_list[im];
    auto hist_mc = mc_sel.Define("trigger_SF",trigger_sf_mm,{"OPS_l1_pt","OPS_l2_pt","OPS_l1_eta","OPS_l2_eta"})
			 .Define("genweight","puWeight*PrefireWeight*genWeight/abs(genWeight)")
			 .Histo1D({hist_name_temp.c_str(),hist_name_temp.c_str(),nbin_in,binlow_in,binhigh_in},hist_name_in.c_str(),"genweight");
    TH1D hist_temp = hist_mc.GetValue();
    hist_temp.Scale(lumi*MC_xs[im]/get_mcEventnumber(MC_list[im]));
    mc_histos.push_back(hist_temp);
  }
  
  std::string output_name=hist_name_in+".root";
  TFile* fout=TFile::Open(output_name.c_str(),"recreate");
  fout->cd();
  std::cout<<"start write!"<<std::endl;
  hist_dimu.Write();
  hist_singlemu.Write();
  for(int im=0;im<mc_histos.size();im++){
    mc_histos[im].Write();
  }
  fout->Close();
  std::cout<<"finished!"<<std::endl;
}

int main()
{
  gROOT->SetBatch(1);
  std::string hist_name[10]= {"OPS_l1_pt","OPS_l1_eta","OPS_l1_phi","OPS_l2_pt","OPS_l2_eta","OPS_l2_phi","OPS_z_pt","OPS_z_eta","OPS_z_phi","OPS_z_mass"};
  int hist_Nbins[10]= {20, 20, 20, 20, 20, 20,50, 20, 20,60};
  float hist_low[10]= {0, -3, -4, 0, -3, -4, 0, -3, -4, 60};
  float hist_high[10]= {200, 3, 4, 100, 3, 4, 200, 3, 4, 120};
  clock_t start,end;
  auto t_start = std::chrono::steady_clock::now();
  start = clock();
  histo(hist_name[9],hist_Nbins[9],hist_low[9],hist_high[9]);
  end = clock();
  auto t_end = std::chrono::steady_clock::now();
  std::cout<<"CPU time = "<<double(end-start)/CLOCKS_PER_SEC<<"s"<<std::endl;
  std::cout<<"Wall time = "<<std::chrono::duration<double> (t_end-t_start).count()<<"s"<<std::endl;
  return 0;
}

#include "ROOT/RDataFrame.hxx"
#include "TString.h"
#include "TFile.h"
#include "TH2D.h"
#include "TMath.h"

#include "ROOT/RVec.hxx"

using namespace ROOT::VecOps;
using rvec_f = const RVec<float> &;

float dphi(float phi1, float phi2){
  if(abs(phi1-phi2)>3.1415926) return (6.2831852-abs(phi1-phi2));
  else return abs(phi1-phi2);
}


// CFlip input for 2016APV
TFile*f_chargeflip_2016APV=TFile::Open("data/ChargeFlipSFs/ChargeFlipProbability_2016apv_MLE.root");
TH2D*Prob_data_2016APV=(TH2D*)f_chargeflip_2016APV->Get("data_CFRate");
TH2D*Prob_mc_2016APV=(TH2D*)f_chargeflip_2016APV->Get("MC_CFRate");
TH1D*Chaflip_unc_2016APV=(TH1D*)f_chargeflip_2016APV->Get("overall_sys");
float Chaflip_unc_num_2016APV=Chaflip_unc_2016APV->GetBinContent(1);

// CFlip input for 2016postAPV
TFile*f_chargeflip_2016postAPV=TFile::Open("data/ChargeFlipSFs/ChargeFlipProbability_2016postapv_MLE.root");
TH2D*Prob_data_2016postAPV=(TH2D*)f_chargeflip_2016postAPV->Get("data_CFRate");
TH2D*Prob_mc_2016postAPV=(TH2D*)f_chargeflip_2016postAPV->Get("MC_CFRate");
TH1D*Chaflip_unc_2016postAPV=(TH1D*)f_chargeflip_2016postAPV->Get("overall_sys");
float Chaflip_unc_num_2016postAPV=Chaflip_unc_2016postAPV->GetBinContent(1);

// CFlip input for 2017
TFile*f_chargeflip_2017=TFile::Open("data/ChargeFlipSFs/ChargeFlipProbability_2017_MLE.root");
TH2D*Prob_data_2017=(TH2D*)f_chargeflip_2017->Get("data_CFRate");
TH2D*Prob_mc_2017=(TH2D*)f_chargeflip_2017->Get("MC_CFRate");
TH1D*Chaflip_unc_2017=(TH1D*)f_chargeflip_2017->Get("overall_sys");
float Chaflip_unc_num_2017=Chaflip_unc_2017->GetBinContent(1);

// CFlip input for 2018
TFile*f_chargeflip_2018=TFile::Open("data/ChargeFlipSFs/ChargeFlipProbability_2018_MLE.root");
TH2D*Prob_data_2018=(TH2D*)f_chargeflip_2018->Get("data_CFRate");
TH2D*Prob_mc_2018=(TH2D*)f_chargeflip_2018->Get("MC_CFRate");
TH1D*Chaflip_unc_2018=(TH1D*)f_chargeflip_2018->Get("overall_sys");
float Chaflip_unc_num_2018=Chaflip_unc_2018->GetBinContent(1);

// 2016APV TriggerSF
TFile*f_2016APV=TFile::Open("data/TriggerSF/TriggerSF_2016apvUL.root");
TH2D*h1_ee_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_ee_SF_l1pteta");
TH2D*h2_ee_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_ee_SF_l2pteta");
TH2D*h3_ee_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_ee_SF_l1l2pt");
TH2D*h1_mm_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_mumu_SF_l1pteta");
TH2D*h2_mm_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_mumu_SF_l2pteta");
TH2D*h3_mm_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_mumu_SF_l1l2pt");
TH2D*h1_em_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_emu_SF_l1pteta");
TH2D*h2_em_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_emu_SF_l2pteta");
TH2D*h3_em_2016APV=(TH2D*)f_2016APV->Get("h2D_SF_emu_SF_l1l2pt");

// 2016postAPV TriggerSF
TFile*f_2016postAPV=TFile::Open("data/TriggerSF/TriggerSF_2016postapvUL.root");
TH2D*h1_ee_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_ee_SF_l1pteta");
TH2D*h2_ee_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_ee_SF_l2pteta");
TH2D*h3_ee_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_ee_SF_l1l2pt");
TH2D*h1_mm_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_mumu_SF_l1pteta");
TH2D*h2_mm_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_mumu_SF_l2pteta");
TH2D*h3_mm_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_mumu_SF_l1l2pt");
TH2D*h1_em_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_emu_SF_l1pteta");
TH2D*h2_em_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_emu_SF_l2pteta");
TH2D*h3_em_2016postAPV=(TH2D*)f_2016postAPV->Get("h2D_SF_emu_SF_l1l2pt");

// 2017 TriggerSF
TFile*f=TFile::Open("data/TriggerSF/TriggerSF_2017UL.root");
TH2D*h1_ee=(TH2D*)f->Get("h2D_SF_ee_SF_l1pteta");
TH2D*h2_ee=(TH2D*)f->Get("h2D_SF_ee_SF_l2pteta");
TH2D*h3_ee=(TH2D*)f->Get("h2D_SF_ee_SF_l1l2pt");
TH2D*h1_mm=(TH2D*)f->Get("h2D_SF_mumu_SF_l1pteta");
TH2D*h2_mm=(TH2D*)f->Get("h2D_SF_mumu_SF_l2pteta");
TH2D*h3_mm=(TH2D*)f->Get("h2D_SF_mumu_SF_l1l2pt");
TH2D*h1_em=(TH2D*)f->Get("h2D_SF_emu_SF_l1pteta");
TH2D*h2_em=(TH2D*)f->Get("h2D_SF_emu_SF_l2pteta");
TH2D*h3_em=(TH2D*)f->Get("h2D_SF_emu_SF_l1l2pt");

// 2018 TriggerSF
TFile*f_2018=TFile::Open("data/TriggerSF/TriggerSF_2018UL.root");
TH2D*h1_ee_2018=(TH2D*)f_2018->Get("h2D_SF_ee_SF_l1pteta");
TH2D*h2_ee_2018=(TH2D*)f_2018->Get("h2D_SF_ee_SF_l2pteta");
TH2D*h3_ee_2018=(TH2D*)f_2018->Get("h2D_SF_ee_SF_l1l2pt");
TH2D*h1_mm_2018=(TH2D*)f_2018->Get("h2D_SF_mumu_SF_l1pteta");
TH2D*h2_mm_2018=(TH2D*)f_2018->Get("h2D_SF_mumu_SF_l2pteta");
TH2D*h3_mm_2018=(TH2D*)f_2018->Get("h2D_SF_mumu_SF_l1l2pt");
TH2D*h1_em_2018=(TH2D*)f_2018->Get("h2D_SF_emu_SF_l1pteta");
TH2D*h2_em_2018=(TH2D*)f_2018->Get("h2D_SF_emu_SF_l2pteta");
TH2D*h3_em_2018=(TH2D*)f_2018->Get("h2D_SF_emu_SF_l1l2pt");

// 2016APV Fakerare
TFile*f_m_2016APV=TFile::Open("data/fr_data_mu_2016APV.root"); 
TFile*f_e_2016APV=TFile::Open("data/fr_data_ele_2016APV.root");
TH2D*h_m_2016APV=(TH2D*)f_m_2016APV->Get("fakerate");
TH2D*h_e_2016APV=(TH2D*)f_e_2016APV->Get("fakerate");

// 2016postAPV Fakerare
TFile*f_m_2016postAPV=TFile::Open("data/fr_data_mu_2016postAPV.root"); 
TFile*f_e_2016postAPV=TFile::Open("data/fr_data_ele_2016postAPV.root");
TH2D*h_m_2016postAPV=(TH2D*)f_m_2016postAPV->Get("fakerate");
TH2D*h_e_2016postAPV=(TH2D*)f_e_2016postAPV->Get("fakerate");

// 2017 Fakerare
TFile*f_m=TFile::Open("data/fr_data_mu_2017.root"); 
TFile*f_e=TFile::Open("data/fr_data_ele_2017.root"); 
TH2D*h_m=(TH2D*)f_m->Get("fakerate");
TH2D*h_e=(TH2D*)f_e->Get("fakerate");

// 2018 Fakerare
TFile*f_m_2018=TFile::Open("data/fr_data_mu_2018.root"); 
TFile*f_e_2018=TFile::Open("data/fr_data_ele_2018.root");
TH2D*h_m_2018=(TH2D*)f_m_2018->Get("fakerate");
TH2D*h_e_2018=(TH2D*)f_e_2018->Get("fakerate");


float trigger_sf_ee_2016postAPV(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_ee_2016postAPV->GetBinContent(h3_ee_2016postAPV->FindBin(l1_pt,l2_pt));
}

float trigger_sf_ee_2016APV(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_ee_2016APV->GetBinContent(h3_ee_2016APV->FindBin(l1_pt,l2_pt));
}

float trigger_sf_ee_2017(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_ee->GetBinContent(h3_ee->FindBin(l1_pt,l2_pt));
}

float trigger_sf_ee_2018(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_ee_2018->GetBinContent(h3_ee_2018->FindBin(l1_pt,l2_pt));
}

float trigger_sf_mm_2016APV(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_mm_2016APV->GetBinContent(h3_mm_2016APV->FindBin(l1_pt,l2_pt));
}

float trigger_sf_mm_2016postAPV(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_mm_2016postAPV->GetBinContent(h3_mm_2016postAPV->FindBin(l1_pt,l2_pt));
}

float trigger_sf_mm_2017(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_mm->GetBinContent(h3_mm->FindBin(l1_pt,l2_pt));
}

float trigger_sf_mm_2018(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_mm_2018->GetBinContent(h3_mm_2018->FindBin(l1_pt,l2_pt));
}

float trigger_sf_em_2016APV(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_em_2016APV->GetBinContent(h3_em_2016APV->FindBin(l1_pt,l2_pt));
}

float trigger_sf_em_2016postAPV(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_em_2016postAPV->GetBinContent(h3_em_2016postAPV->FindBin(l1_pt,l2_pt));
}

float trigger_sf_em_2017(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_em->GetBinContent(h3_em->FindBin(l1_pt,l2_pt));
}

float trigger_sf_em_2018(float l1_pt, float l2_pt){
  if(l1_pt>200) l1_pt=199;
  if(l2_pt>200) l2_pt=199;
  return h3_em_2018->GetBinContent(h3_em_2018->FindBin(l1_pt,l2_pt));
}

float fakelepweight_ee_2017(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_e->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_e->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_e->GetNbinsX()) BinX = h_e->GetNbinsX();
                if (BinY > h_e->GetNbinsY()) BinY = h_e->GetNbinsY();
                fakerate1=h_e->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e->GetNbinsX()) BinX = h_e->GetNbinsX();
                if (BinY > h_e->GetNbinsY()) BinY = h_e->GetNbinsY();
                fakerate1=h_e->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }
	    
        }
        if(ttc_0P2F){
            BinX = h_e->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_e->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_e->GetNbinsX()) BinX = h_e->GetNbinsX();
            if (BinY > h_e->GetNbinsY()) BinY = h_e->GetNbinsY();
            fakerate1=h_e->GetBinContent(BinX, BinY);

            BinX = h_e->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e->GetNbinsX()) BinX = h_e->GetNbinsX();
            if (BinY > h_e->GetNbinsY()) BinY = h_e->GetNbinsY();
            fakerate2=h_e->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }
        }
        return w_temp;
}

float fakelepweight_ee_2018(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_e_2018->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_e_2018->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_e_2018->GetNbinsX()) BinX = h_e_2018->GetNbinsX();
                if (BinY > h_e_2018->GetNbinsY()) BinY = h_e_2018->GetNbinsY();
                fakerate1=h_e_2018->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e_2018->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e_2018->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e_2018->GetNbinsX()) BinX = h_e_2018->GetNbinsX();
                if (BinY > h_e_2018->GetNbinsY()) BinY = h_e_2018->GetNbinsY();
                fakerate1=h_e_2018->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }
	    
        }
        if(ttc_0P2F){
            BinX = h_e_2018->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_e_2018->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_e_2018->GetNbinsX()) BinX = h_e_2018->GetNbinsX();
            if (BinY > h_e_2018->GetNbinsY()) BinY = h_e_2018->GetNbinsY();
            fakerate1=h_e_2018->GetBinContent(BinX, BinY);

            BinX = h_e_2018->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e_2018->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e_2018->GetNbinsX()) BinX = h_e_2018->GetNbinsX();
            if (BinY > h_e_2018->GetNbinsY()) BinY = h_e_2018->GetNbinsY();
            fakerate2=h_e_2018->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }
        }
        return w_temp;
}

float fakelepweight_em_2016APV(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m_2016APV->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m_2016APV->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m_2016APV->GetNbinsX()) BinX = h_m_2016APV->GetNbinsX();
                if (BinY > h_m_2016APV->GetNbinsY()) BinY = h_m_2016APV->GetNbinsY();
                fakerate1=h_m_2016APV->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e_2016APV->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e_2016APV->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e_2016APV->GetNbinsX()) BinX = h_e_2016APV->GetNbinsX();
                if (BinY > h_e_2016APV->GetNbinsY()) BinY = h_e_2016APV->GetNbinsY();
                fakerate1=h_e_2016APV->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }

        }
        if(ttc_0P2F){
            BinX = h_m_2016APV->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m_2016APV->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m_2016APV->GetNbinsX()) BinX = h_m_2016APV->GetNbinsX();
            if (BinY > h_m_2016APV->GetNbinsY()) BinY = h_m_2016APV->GetNbinsY();
            fakerate1=h_m_2016APV->GetBinContent(BinX, BinY);

            BinX = h_e_2016APV->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e_2016APV->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e_2016APV->GetNbinsX()) BinX = h_e_2016APV->GetNbinsX();
            if (BinY > h_e_2016APV->GetNbinsY()) BinY = h_e_2016APV->GetNbinsY();
            fakerate2=h_e_2016APV->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }

        }
        return w_temp;
}

float fakelepweight_em_2016postAPV(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m_2016postAPV->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m_2016postAPV->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m_2016postAPV->GetNbinsX()) BinX = h_m_2016postAPV->GetNbinsX();
                if (BinY > h_m_2016postAPV->GetNbinsY()) BinY = h_m_2016postAPV->GetNbinsY();
                fakerate1=h_m_2016postAPV->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e_2016postAPV->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e_2016postAPV->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e_2016postAPV->GetNbinsX()) BinX = h_e_2016postAPV->GetNbinsX();
                if (BinY > h_e_2016postAPV->GetNbinsY()) BinY = h_e_2016postAPV->GetNbinsY();
                fakerate1=h_e_2016postAPV->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }

        }
        if(ttc_0P2F){
            BinX = h_m_2016postAPV->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m_2016postAPV->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m_2016postAPV->GetNbinsX()) BinX = h_m_2016postAPV->GetNbinsX();
            if (BinY > h_m_2016postAPV->GetNbinsY()) BinY = h_m_2016postAPV->GetNbinsY();
            fakerate1=h_m_2016postAPV->GetBinContent(BinX, BinY);

            BinX = h_e_2016postAPV->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e_2016postAPV->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e_2016postAPV->GetNbinsX()) BinX = h_e_2016postAPV->GetNbinsX();
            if (BinY > h_e_2016postAPV->GetNbinsY()) BinY = h_e_2016postAPV->GetNbinsY();
            fakerate2=h_e_2016postAPV->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }

        }
        return w_temp;
}


float fakelepweight_em_2017(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m->GetNbinsX()) BinX = h_m->GetNbinsX();
                if (BinY > h_m->GetNbinsY()) BinY = h_m->GetNbinsY();
                fakerate1=h_m->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e->GetNbinsX()) BinX = h_e->GetNbinsX();
                if (BinY > h_e->GetNbinsY()) BinY = h_e->GetNbinsY();
                fakerate1=h_e->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }

        }
        if(ttc_0P2F){
            BinX = h_m->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m->GetNbinsX()) BinX = h_m->GetNbinsX();
            if (BinY > h_m->GetNbinsY()) BinY = h_m->GetNbinsY();
            fakerate1=h_m->GetBinContent(BinX, BinY);

            BinX = h_e->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e->GetNbinsX()) BinX = h_e->GetNbinsX();
            if (BinY > h_e->GetNbinsY()) BinY = h_e->GetNbinsY();
            fakerate2=h_e->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }

        }
        return w_temp;
}

float fakelepweight_em_2018(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m_2018->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m_2018->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m_2018->GetNbinsX()) BinX = h_m_2018->GetNbinsX();
                if (BinY > h_m_2018->GetNbinsY()) BinY = h_m_2018->GetNbinsY();
                fakerate1=h_m_2018->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e_2018->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e_2018->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e_2018->GetNbinsX()) BinX = h_e_2018->GetNbinsX();
                if (BinY > h_e_2018->GetNbinsY()) BinY = h_e_2018->GetNbinsY();
                fakerate1=h_e_2018->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }

        }
        if(ttc_0P2F){
            BinX = h_m_2018->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m_2018->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m_2018->GetNbinsX()) BinX = h_m_2018->GetNbinsX();
            if (BinY > h_m_2018->GetNbinsY()) BinY = h_m_2018->GetNbinsY();
            fakerate1=h_m_2018->GetBinContent(BinX, BinY);

            BinX = h_e_2018->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e_2018->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e_2018->GetNbinsX()) BinX = h_e_2018->GetNbinsX();
            if (BinY > h_e_2018->GetNbinsY()) BinY = h_e_2018->GetNbinsY();
            fakerate2=h_e_2018->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }

        }
        return w_temp;
}

float fakelepweight_mm_2016APV(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m_2016APV->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m_2016APV->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m_2016APV->GetNbinsX()) BinX = h_m_2016APV->GetNbinsX();
                if (BinY > h_m_2016APV->GetNbinsY()) BinY = h_m_2016APV->GetNbinsY();
                fakerate1=h_m_2016APV->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_m_2016APV->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_m_2016APV->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_m_2016APV->GetNbinsX()) BinX = h_m_2016APV->GetNbinsX();
                if (BinY > h_m_2016APV->GetNbinsY()) BinY = h_m_2016APV->GetNbinsY();
                fakerate1=h_m_2016APV->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }
        }
        if(ttc_0P2F){
            BinX = h_m_2016APV->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m_2016APV->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m_2016APV->GetNbinsX()) BinX = h_m_2016APV->GetNbinsX();
            if (BinY > h_m_2016APV->GetNbinsY()) BinY = h_m_2016APV->GetNbinsY();
            fakerate1=h_m_2016APV->GetBinContent(BinX, BinY);

            BinX = h_m_2016APV->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_m_2016APV->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_m_2016APV->GetNbinsX()) BinX = h_m_2016APV->GetNbinsX();
            if (BinY > h_m_2016APV->GetNbinsY()) BinY = h_m_2016APV->GetNbinsY();
            fakerate2=h_m_2016APV->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }
        }
        return w_temp;
}

float fakelepweight_mm_2016postAPV(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m_2016postAPV->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m_2016postAPV->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m_2016postAPV->GetNbinsX()) BinX = h_m_2016postAPV->GetNbinsX();
                if (BinY > h_m_2016postAPV->GetNbinsY()) BinY = h_m_2016postAPV->GetNbinsY();
                fakerate1=h_m_2016postAPV->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_m_2016postAPV->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_m_2016postAPV->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_m_2016postAPV->GetNbinsX()) BinX = h_m_2016postAPV->GetNbinsX();
                if (BinY > h_m_2016postAPV->GetNbinsY()) BinY = h_m_2016postAPV->GetNbinsY();
                fakerate1=h_m_2016postAPV->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }
        }
        if(ttc_0P2F){
            BinX = h_m_2016postAPV->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m_2016postAPV->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m_2016postAPV->GetNbinsX()) BinX = h_m_2016postAPV->GetNbinsX();
            if (BinY > h_m_2016postAPV->GetNbinsY()) BinY = h_m_2016postAPV->GetNbinsY();
            fakerate1=h_m_2016postAPV->GetBinContent(BinX, BinY);

            BinX = h_m_2016postAPV->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_m_2016postAPV->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_m_2016postAPV->GetNbinsX()) BinX = h_m_2016postAPV->GetNbinsX();
            if (BinY > h_m_2016postAPV->GetNbinsY()) BinY = h_m_2016postAPV->GetNbinsY();
            fakerate2=h_m_2016postAPV->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }
        }
        return w_temp;
}

float fakelepweight_mm_2017(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m->GetNbinsX()) BinX = h_m->GetNbinsX();
                if (BinY > h_m->GetNbinsY()) BinY = h_m->GetNbinsY();
                fakerate1=h_m->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_m->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_m->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_m->GetNbinsX()) BinX = h_m->GetNbinsX();
                if (BinY > h_m->GetNbinsY()) BinY = h_m->GetNbinsY();
                fakerate1=h_m->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }
        }
        if(ttc_0P2F){
            BinX = h_m->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m->GetNbinsX()) BinX = h_m->GetNbinsX();
            if (BinY > h_m->GetNbinsY()) BinY = h_m->GetNbinsY();
            fakerate1=h_m->GetBinContent(BinX, BinY);

            BinX = h_m->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_m->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_m->GetNbinsX()) BinX = h_m->GetNbinsX();
            if (BinY > h_m->GetNbinsY()) BinY = h_m->GetNbinsY();
            fakerate2=h_m->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }
        }
        return w_temp;
}

float fakelepweight_mm_2018(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_m_2018->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_m_2018->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_m_2018->GetNbinsX()) BinX = h_m_2018->GetNbinsX();
                if (BinY > h_m_2018->GetNbinsY()) BinY = h_m_2018->GetNbinsY();
                fakerate1=h_m_2018->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_m_2018->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_m_2018->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_m_2018->GetNbinsX()) BinX = h_m_2018->GetNbinsX();
                if (BinY > h_m_2018->GetNbinsY()) BinY = h_m_2018->GetNbinsY();
                fakerate1=h_m_2018->GetBinContent(BinX, BinY);
            }
	    if(isData){
              w_temp=fakerate1/(1-fakerate1);
            }else{
              w_temp=-1*fakerate1/(1-fakerate1);
            }
        }
        if(ttc_0P2F){
            BinX = h_m_2018->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_m_2018->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_m_2018->GetNbinsX()) BinX = h_m_2018->GetNbinsX();
            if (BinY > h_m_2018->GetNbinsY()) BinY = h_m_2018->GetNbinsY();
            fakerate1=h_m_2018->GetBinContent(BinX, BinY);

            BinX = h_m_2018->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_m_2018->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_m_2018->GetNbinsX()) BinX = h_m_2018->GetNbinsX();
            if (BinY > h_m_2018->GetNbinsY()) BinY = h_m_2018->GetNbinsY();
            fakerate2=h_m_2018->GetBinContent(BinX, BinY);
	    if(isData){
              w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }else{
              w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
            }
        }
        return w_temp;
}

float fakelepweight_ee_2016APV(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
	//std::cout << "isData" << isData << std::endl;
	//return w_temp;
	//bool myBool = Convert.ToBoolean(sample);
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_e_2016APV->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_e_2016APV->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_e_2016APV->GetNbinsX()) BinX = h_e_2016APV->GetNbinsX();
                if (BinY > h_e_2016APV->GetNbinsY()) BinY = h_e_2016APV->GetNbinsY();
                fakerate1=h_e_2016APV->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e_2016APV->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e_2016APV->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e_2016APV->GetNbinsX()) BinX = h_e_2016APV->GetNbinsX();
                if (BinY > h_e_2016APV->GetNbinsY()) BinY = h_e_2016APV->GetNbinsY();
                fakerate1=h_e_2016APV->GetBinContent(BinX, BinY);
            }
	    if(isData){
	      w_temp=fakerate1/(1-fakerate1);
	    }else{
	      w_temp=-1*fakerate1/(1-fakerate1);
	    }
        }
        if(ttc_0P2F){
            BinX = h_e_2016APV->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_e_2016APV->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_e_2016APV->GetNbinsX()) BinX = h_e_2016APV->GetNbinsX();
            if (BinY > h_e_2016APV->GetNbinsY()) BinY = h_e_2016APV->GetNbinsY();
            fakerate1=h_e_2016APV->GetBinContent(BinX, BinY);

            BinX = h_e_2016APV->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e_2016APV->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e_2016APV->GetNbinsX()) BinX = h_e_2016APV->GetNbinsX();
            if (BinY > h_e_2016APV->GetNbinsY()) BinY = h_e_2016APV->GetNbinsY();
            fakerate2=h_e_2016APV->GetBinContent(BinX, BinY);
	    if(isData){
	      w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
	    }else{
	      w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
	    }
        }
        return w_temp;

}


float fakelepweight_ee_2016postAPV(bool ttc_1P1F, bool ttc_0P2F, bool ttc_lep1_faketag, float l1_pt, float l1_eta, float l2_pt, float l2_eta, bool isData){
        float w_temp=1.0;
        float fakerate1=1.0;
        float fakerate2=1.0;
        int BinX = 0;
	//std::cout << "isData" << isData << std::endl;
	//return w_temp;
	//bool myBool = Convert.ToBoolean(sample);
        int BinY = 0;
        if(ttc_1P1F){
            if(ttc_lep1_faketag){
                BinX = h_e_2016postAPV->GetXaxis()->FindBin(fabs(l1_eta));
                BinY = h_e_2016postAPV->GetYaxis()->FindBin(l1_pt);
                if (BinX > h_e_2016postAPV->GetNbinsX()) BinX = h_e_2016postAPV->GetNbinsX();
                if (BinY > h_e_2016postAPV->GetNbinsY()) BinY = h_e_2016postAPV->GetNbinsY();
                fakerate1=h_e_2016postAPV->GetBinContent(BinX, BinY);
            }
            else {
                BinX = h_e_2016postAPV->GetXaxis()->FindBin(fabs(l2_eta));
                BinY = h_e_2016postAPV->GetYaxis()->FindBin(l2_pt);
                if (BinX > h_e_2016postAPV->GetNbinsX()) BinX = h_e_2016postAPV->GetNbinsX();
                if (BinY > h_e_2016postAPV->GetNbinsY()) BinY = h_e_2016postAPV->GetNbinsY();
                fakerate1=h_e_2016postAPV->GetBinContent(BinX, BinY);
            }
	    if(isData){
	      w_temp=fakerate1/(1-fakerate1);
	    }else{
	      w_temp=-1*fakerate1/(1-fakerate1);
	    }
        }
        if(ttc_0P2F){
            BinX = h_e_2016postAPV->GetXaxis()->FindBin(fabs(l1_eta));
            BinY = h_e_2016postAPV->GetYaxis()->FindBin(l1_pt);
            if (BinX > h_e_2016postAPV->GetNbinsX()) BinX = h_e_2016postAPV->GetNbinsX();
            if (BinY > h_e_2016postAPV->GetNbinsY()) BinY = h_e_2016postAPV->GetNbinsY();
            fakerate1=h_e_2016postAPV->GetBinContent(BinX, BinY);

            BinX = h_e_2016postAPV->GetXaxis()->FindBin(fabs(l2_eta));
            BinY = h_e_2016postAPV->GetYaxis()->FindBin(l2_pt);
            if (BinX > h_e_2016postAPV->GetNbinsX()) BinX = h_e_2016postAPV->GetNbinsX();
            if (BinY > h_e_2016postAPV->GetNbinsY()) BinY = h_e_2016postAPV->GetNbinsY();
            fakerate2=h_e_2016postAPV->GetBinContent(BinX, BinY);
	    if(isData){
	      w_temp=-1.0*fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
	    }else{
	      w_temp=fakerate1*fakerate2/((1-fakerate1)*(1-fakerate2));
	    }
        }
        return w_temp;

}


// CFlip SF for 3 years

float chargeflip_SF_2016APV(int OS_flag, float lep1_pt, float lep1_eta, float lep1_phi, float lep2_pt, float lep2_eta, float lep2_phi, int channel, int iw, ROOT::VecOps::RVec<float> genlep_eta, ROOT::VecOps::RVec<float> genlep_phi, ROOT::VecOps::RVec<int> genlep_id){

  // for DY and TTTo2L, no need to gen matching
  if(OS_flag==0){
    int ngenlep=genlep_id.size();
    //std::cout << "1.1" << std::endl;
    if(ngenlep<2)return 1.;
    int l1_temp=-99;
    int l2_temp=-99;
    float dr1=100.;
    float dr1_temp=100.;
    float dr2=100.;
    float dr2_temp=100.;
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr1_temp=sqrt((lep1_eta-genlep_eta[iloop])*(lep1_eta-genlep_eta[iloop]) + dphi(lep1_phi, genlep_phi[iloop])*dphi(lep1_phi, genlep_phi[iloop]));
      if (dr1_temp<dr1) {dr1=dr1_temp;l1_temp=iloop;}
    }
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr2_temp=sqrt((lep2_eta-genlep_eta[iloop])*(lep2_eta-genlep_eta[iloop]) + dphi(lep2_phi, genlep_phi[iloop])*dphi(lep2_phi, genlep_phi[iloop]));
      if (dr2_temp<dr2) {dr2=dr2_temp;l2_temp=iloop;}
    }
    //std::cout << "1.2" << std::endl;
    if(!(l1_temp>-1 && l2_temp>-1 && dr1<0.3 && dr2<0.3 && genlep_id[l1_temp]*genlep_id[l2_temp]<0 && (l1_temp!=l2_temp)))return 1.;
  }

  //std::cout << "1.3" << std::endl;
  float sf=1.;
  if(lep1_pt>300.) lep1_pt=200.;
  if(lep2_pt>300.) lep2_pt=200.;
  if(abs(lep1_eta)>2.5) lep1_eta=2.0;
  if(abs(lep2_eta)>2.5) lep2_eta=2.0;
  if(channel==3){
    float prob1_data=Prob_data_2016APV->GetBinContent(Prob_data_2016APV->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_data=Prob_data_2016APV->GetBinContent(Prob_data_2016APV->FindBin(lep2_pt,abs(lep2_eta)));
    float prob1_mc=Prob_mc_2016APV->GetBinContent(Prob_mc_2016APV->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_mc=Prob_mc_2016APV->GetBinContent(Prob_mc_2016APV->FindBin(lep2_pt,abs(lep2_eta)));
    sf=(prob1_data+prob2_data-2*prob1_data*prob2_data)/(prob1_mc+prob2_mc-2*prob1_mc*prob2_mc);
    //std::cout << "sf: " << sf << std::endl;
    if(iw==0) return sf;
    if(iw==1) return (sf+Chaflip_unc_num_2016APV);
    if(iw==2) return (sf-Chaflip_unc_num_2016APV);
  }
  else {sf = 1.0; }
  return sf;
}


float chargeflip_SF_2016postAPV(int OS_flag, float lep1_pt, float lep1_eta, float lep1_phi, float lep2_pt, float lep2_eta, float lep2_phi, int channel, int iw, ROOT::VecOps::RVec<float> genlep_eta, ROOT::VecOps::RVec<float> genlep_phi, ROOT::VecOps::RVec<int> genlep_id){

  // for DY and TTTo2L, no need to gen matching
  if(OS_flag==0){
    int ngenlep=genlep_id.size();
    //std::cout << "1.1" << std::endl;
    if(ngenlep<2)return 1.;
    int l1_temp=-99;
    int l2_temp=-99;
    float dr1=100.;
    float dr1_temp=100.;
    float dr2=100.;
    float dr2_temp=100.;
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr1_temp=sqrt((lep1_eta-genlep_eta[iloop])*(lep1_eta-genlep_eta[iloop]) + dphi(lep1_phi, genlep_phi[iloop])*dphi(lep1_phi, genlep_phi[iloop]));
      if (dr1_temp<dr1) {dr1=dr1_temp;l1_temp=iloop;}
    }
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr2_temp=sqrt((lep2_eta-genlep_eta[iloop])*(lep2_eta-genlep_eta[iloop]) + dphi(lep2_phi, genlep_phi[iloop])*dphi(lep2_phi, genlep_phi[iloop]));
      if (dr2_temp<dr2) {dr2=dr2_temp;l2_temp=iloop;}
    }
    //std::cout << "1.2" << std::endl;
    if(!(l1_temp>-1 && l2_temp>-1 && dr1<0.3 && dr2<0.3 && genlep_id[l1_temp]*genlep_id[l2_temp]<0 && (l1_temp!=l2_temp)))return 1.;
  }

  //std::cout << "1.3" << std::endl;
  float sf=1.;
  if(lep1_pt>300.) lep1_pt=200.;
  if(lep2_pt>300.) lep2_pt=200.;
  if(abs(lep1_eta)>2.5) lep1_eta=2.0;
  if(abs(lep2_eta)>2.5) lep2_eta=2.0;
  if(channel==3){
    float prob1_data=Prob_data_2016postAPV->GetBinContent(Prob_data_2016postAPV->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_data=Prob_data_2016postAPV->GetBinContent(Prob_data_2016postAPV->FindBin(lep2_pt,abs(lep2_eta)));
    float prob1_mc=Prob_mc_2016postAPV->GetBinContent(Prob_mc_2016postAPV->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_mc=Prob_mc_2016postAPV->GetBinContent(Prob_mc_2016postAPV->FindBin(lep2_pt,abs(lep2_eta)));
    sf=(prob1_data+prob2_data-2*prob1_data*prob2_data)/(prob1_mc+prob2_mc-2*prob1_mc*prob2_mc);
    //std::cout << "sf: " << sf << std::endl;
    if(iw==0) return sf;
    if(iw==1) return (sf+Chaflip_unc_num_2016postAPV);
    if(iw==2) return (sf-Chaflip_unc_num_2016postAPV);
  }
  else {sf = 1.0; }
  return sf;
}


float chargeflip_SF_2017(int OS_flag, float lep1_pt, float lep1_eta, float lep1_phi, float lep2_pt, float lep2_eta, float lep2_phi, int channel, int iw, ROOT::VecOps::RVec<float> genlep_eta, ROOT::VecOps::RVec<float> genlep_phi, ROOT::VecOps::RVec<int> genlep_id){

  // for DY and TTTo2L, no need to gen matching
  if(OS_flag==0){
    int ngenlep=genlep_id.size();
    //std::cout << "1.1" << std::endl;
    if(ngenlep<2)return 1.;
    int l1_temp=-99;
    int l2_temp=-99;
    float dr1=100.;
    float dr1_temp=100.;
    float dr2=100.;
    float dr2_temp=100.;
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr1_temp=sqrt((lep1_eta-genlep_eta[iloop])*(lep1_eta-genlep_eta[iloop]) + dphi(lep1_phi, genlep_phi[iloop])*dphi(lep1_phi, genlep_phi[iloop]));
      if (dr1_temp<dr1) {dr1=dr1_temp;l1_temp=iloop;}
    }
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr2_temp=sqrt((lep2_eta-genlep_eta[iloop])*(lep2_eta-genlep_eta[iloop]) + dphi(lep2_phi, genlep_phi[iloop])*dphi(lep2_phi, genlep_phi[iloop]));
      if (dr2_temp<dr2) {dr2=dr2_temp;l2_temp=iloop;}
    }
    //std::cout << "1.2" << std::endl;
    if(!(l1_temp>-1 && l2_temp>-1 && dr1<0.3 && dr2<0.3 && genlep_id[l1_temp]*genlep_id[l2_temp]<0 && (l1_temp!=l2_temp)))return 1.;
  }

  //std::cout << "1.3" << std::endl;
  float sf=1.;
  if(lep1_pt>300.) lep1_pt=200.;
  if(lep2_pt>300.) lep2_pt=200.;
  if(abs(lep1_eta)>2.5) lep1_eta=2.0;
  if(abs(lep2_eta)>2.5) lep2_eta=2.0;
  if(channel==3){
    float prob1_data=Prob_data_2017->GetBinContent(Prob_data_2017->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_data=Prob_data_2017->GetBinContent(Prob_data_2017->FindBin(lep2_pt,abs(lep2_eta)));
    float prob1_mc=Prob_mc_2017->GetBinContent(Prob_mc_2017->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_mc=Prob_mc_2017->GetBinContent(Prob_mc_2017->FindBin(lep2_pt,abs(lep2_eta)));
    sf=(prob1_data+prob2_data-2*prob1_data*prob2_data)/(prob1_mc+prob2_mc-2*prob1_mc*prob2_mc);
    //std::cout << "sf: " << sf << std::endl;
    if(iw==0) return sf;
    if(iw==1) return (sf+Chaflip_unc_num_2017);
    if(iw==2) return (sf-Chaflip_unc_num_2017);
  }
  else {sf = 1.0; }
  return sf;
}


float chargeflip_SF_2018(int OS_flag, float lep1_pt, float lep1_eta, float lep1_phi, float lep2_pt, float lep2_eta, float lep2_phi, int channel, int iw, ROOT::VecOps::RVec<float> genlep_eta, ROOT::VecOps::RVec<float> genlep_phi, ROOT::VecOps::RVec<int> genlep_id){

  // for DY and TTTo2L, no need to gen matching
  if(OS_flag==0){
    int ngenlep=genlep_id.size();
    //std::cout << "1.1" << std::endl;
    if(ngenlep<2)return 1.;
    int l1_temp=-99;
    int l2_temp=-99;
    float dr1=100.;
    float dr1_temp=100.;
    float dr2=100.;
    float dr2_temp=100.;
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr1_temp=sqrt((lep1_eta-genlep_eta[iloop])*(lep1_eta-genlep_eta[iloop]) + dphi(lep1_phi, genlep_phi[iloop])*dphi(lep1_phi, genlep_phi[iloop]));
      if (dr1_temp<dr1) {dr1=dr1_temp;l1_temp=iloop;}
    }
    for(int iloop=0;iloop<ngenlep;iloop++){
      dr2_temp=sqrt((lep2_eta-genlep_eta[iloop])*(lep2_eta-genlep_eta[iloop]) + dphi(lep2_phi, genlep_phi[iloop])*dphi(lep2_phi, genlep_phi[iloop]));
      if (dr2_temp<dr2) {dr2=dr2_temp;l2_temp=iloop;}
    }
    //std::cout << "1.2" << std::endl;
    if(!(l1_temp>-1 && l2_temp>-1 && dr1<0.3 && dr2<0.3 && genlep_id[l1_temp]*genlep_id[l2_temp]<0 && (l1_temp!=l2_temp)))return 1.;
  }

  //std::cout << "1.3" << std::endl;
  float sf=1.;
  if(lep1_pt>300.) lep1_pt=200.;
  if(lep2_pt>300.) lep2_pt=200.;
  if(abs(lep1_eta)>2.5) lep1_eta=2.0;
  if(abs(lep2_eta)>2.5) lep2_eta=2.0;
  if(channel==3){
    float prob1_data=Prob_data_2018->GetBinContent(Prob_data_2018->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_data=Prob_data_2018->GetBinContent(Prob_data_2018->FindBin(lep2_pt,abs(lep2_eta)));
    float prob1_mc=Prob_mc_2018->GetBinContent(Prob_mc_2018->FindBin(lep1_pt,abs(lep1_eta)));
    float prob2_mc=Prob_mc_2018->GetBinContent(Prob_mc_2018->FindBin(lep2_pt,abs(lep2_eta)));
    sf=(prob1_data+prob2_data-2*prob1_data*prob2_data)/(prob1_mc+prob2_mc-2*prob1_mc*prob2_mc);
    //std::cout << "sf: " << sf << std::endl;
    if(iw==0) return sf;
    if(iw==1) return (sf+Chaflip_unc_num_2018);
    if(iw==2) return (sf-Chaflip_unc_num_2018);
  }
  else {sf = 1.0; }
  return sf;
}

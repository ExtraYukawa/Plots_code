#include "ROOT/RDataFrame.hxx"
#include "ROOT/RVec.hxx"
#include "TCanvas.h"
#include "TH1D.h"
#include "TLatex.h"
#include "Math/Vector4D.h"
#include "TStyle.h"
 
using namespace ROOT::VecOps;
using RNode = ROOT::RDF::RNode;
using rvec_f = const RVec<float> &;
using rvec_i = const RVec<int> &;
const auto z_mass = 91.2;

bool filter_z_dr(const RVec<RVec<size_t>> &idx, rvec_f eta, rvec_f phi)
{
  for (size_t i = 0; i < 2; i++) {
    const auto i1 = idx[i][0];
    const auto i2 = idx[i][1];
    const auto dr = DeltaR(eta[i1], eta[i2], phi[i1], phi[i2]);
    if (dr < 0.02) {
      return false;
    }
  }
  return true;
};

bool filterHEM( rvec_f eta, rvec_f phi)
{
  for (size_t i = 0; i< eta.size(); i++){
    //std::cout << "eta[i]: " << eta[i] << std::endl;
    if(eta[i] > -3.2 && eta[i] < -1.3 && phi[i] > -1.57 && phi[i] < -0.87){
      //std::cout << "eta[i]: " << eta[i] << std::endl;
      return true;
    }
  }
  return false;
};

bool notHEM( rvec_f eta, rvec_f phi)
{
  for (size_t i = 0; i< eta.size(); i++){
    ///std::cout << "not HEM eta[i] before selection: " << eta[i] << std::endl;
    if((eta[i] < -3.2 || eta[i] > -1.3) && (phi[i] < -1.57 || phi[i] > -0.87)){
      //std::cout << "not HEM eta[i]: " << eta[i] << std::endl;
      return true;
    }
  }
  return false;
};

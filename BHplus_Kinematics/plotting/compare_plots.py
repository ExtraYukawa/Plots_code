#==============
# Last used:
# python compare_plots.py
#==============

#!/usr/bin/env python

import sys
import os
import array
import shutil

thisdir = os.path.dirname(os.path.realpath(__file__))
basedir = os.path.dirname(thisdir)
sys.path.append(basedir)
print (thisdir)
#import config
#from datasets import allsamples
#from plotstyle import SimpleCanvas
from plotstyle import *

import ROOT
#from ROOT import *
ROOT.gROOT.SetBatch(True)
colors = {
    '200'    : ROOT.kRed,
    '350'    : ROOT.kGreen,
    '500'    : ROOT.kBlue,
    '800'    : ROOT.kCyan,
    '1000'   : ROOT.kOrange,
    'zg'     :"#99ffaa",
    'wg'     :"#99eeff",
    'efake'  :"#ffee99",
    'hfake'  :"#bbaaff",
    'halo'   :"#ff9933",
    'spike'  :"#666666",
    'vvg'    :"#ff4499",
    'gjets'  :"#ffaacc",
    'minor'  :"#bb66ff",
    'top'    :"#5544ff",
    'zjets'  :"#99ffaa",
    'wjets'  :"#222222",
    'gg'     :"#bb66ff"
    }

histo_xtitle = {
    "DeepB_loose_j1_pt"  : "Leading b-jet p_{T}",
    "DeepB_loose_j2_pt"  : "2^{nd} leading b-jet p_{T}",
    "DeepB_loose_j3_pt"  : "3^{rd} leading b-jet p_{T}",
    "DeepB_loose_j1_eta" : "Leading b-jet #eta",
    "DeepB_loose_j2_eta" : "2^{nd} leading b-jet #eta",
    "DeepB_loose_j3_eta" : "3^{rd} leading b-jet #eta",
    "j1_pt"              : "Leading jet p_{T}",
    "j2_pt"              : "2^{nd} leading jet p_{T}",
    "j3_pt"              : "3^{rd} leading jet p_{T}",
    "j1_eta"             : "Leading jet #eta",
    "j2_eta"             : "2^{nd} leading jet #eta",
    "j3_eta"             : "3^{rd} leading jet #eta"
}


def makePlot(folder, hname, xmin, xmax, year="2018", isNorm=True):
    
    wRatio = True
    
    #Get histograms
    root_file = ROOT.TFile("../%s/%s.root"%(folder,hname))
    h_all = {}
    masses = ["200","350","500","800","1000"]
    for mass in masses:
        #print ("adding histogram for mass: %s GeV",%(mass))
        # print ("mass: ", mass)
        h_all[mass] = root_file.Get("%s"%hname+"_"+mass)
    
    if wRatio:
        canvas = RatioCanvas(" "," ",41500)
        canvas.ytitle = 'Normalized to Unity'
        canvas.xtitle = histo_xtitle[hname]
    else:
        canvas = SimpleCanvas(" "," ",41500)
        canvas.ytitle = 'Normalized to Unity'
        canvas.xtitle = 'Jet Pt'
    canvas.legend.setPosition(0.7, 0.7, 0.9, 0.9)

    # Adding to canvas
    for i, key in enumerate(h_all):
        key = masses[i]
        print ("key: ", key)
        h_all[key].Scale(1.0/h_all[key].Integral()) #normalize histogram
        canvas.legend.add(h_all[key], title = key, opt = 'LP', color = colors[key], fstyle = 0, lwidth = 2)
        canvas.addHistogram(h_all[key], drawOpt = 'HIST E')

    canvas.applyStyles()
    if wRatio:
        canvas.printWeb('compare_wRatio', hname, logy = True)
    else:
        canvas.printWeb('compare', hname, logy = True)

# Main
if __name__ == "__main__":
    # plottting
    # makePlot("2017_sel1_mujets_kinematics_26Sep2023","DeepB_loose_j1_pt",30.0,200.0)
    # makePlot("2017_sel1_mujets_kinematics_26Sep2023","DeepB_loose_j2_pt",30.0,200.0)
    # makePlot("2017_sel1_mujets_kinematics_26Sep2023","DeepB_loose_j3_pt",30.0,200.0)
    # makePlot("2017_sel1_mujets_kinematics_26Sep2023","DeepB_loose_j1_eta",-2.5,2.5)
    # makePlot("2017_sel1_mujets_kinematics_26Sep2023","DeepB_loose_j2_eta",-2.5,2.5)
    # makePlot("2017_sel1_mujets_kinematics_26Sep2023","DeepB_loose_j3_eta",-2.5,2.5)
    makePlot("2017_sel2_mujets_kinematics","j1_pt",30.0,200.0)
    makePlot("2017_sel2_mujets_kinematics","j1_eta",-2.5,2.5)
    makePlot("2017_sel2_mujets_kinematics","j2_pt",30.0,200.0)
    makePlot("2017_sel2_mujets_kinematics","j2_eta",-2.5,2.5)
    makePlot("2017_sel2_mujets_kinematics","j3_pt",30.0,200.0)
    makePlot("2017_sel2_mujets_kinematics","j3_eta",-2.5,2.5)
    

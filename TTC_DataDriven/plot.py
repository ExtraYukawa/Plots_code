import ROOT
import numpy as np
from ROOT import kFALSE
import datetime
import os, sys

import CMSTDRStyle
CMSTDRStyle.setTDRStyle().cd()
import CMSstyle
from array import array

def set_axis(the_histo, coordinate, title, is_energy):

	if coordinate == 'x':
		axis = the_histo.GetXaxis()
	elif coordinate == 'y':
		axis = the_histo.GetYaxis()
	else:
		raise ValueError('x and y axis only')

	axis.SetLabelFont(42)
	axis.SetLabelOffset(0.015)
	axis.SetNdivisions(505)
	axis.SetTitleFont(42)
	axis.SetTitleOffset(1.15)
	axis.SetLabelSize(0.03)
	axis.SetTitleSize(0.04)
	if coordinate == 'x':
		axis.SetLabelSize(0.0)
		axis.SetTitleSize(0.0)
	if (coordinate == "y"):axis.SetTitleOffset(1.2)
	if is_energy:
		axis.SetTitle(title+' [GeV]')
	else:
		axis.SetTitle(title) 

def draw_plots(opts, hist_array =[], x_name='', isem=0):
        # save all output inside a directory
        if opts.saveDir == None:
                opts.saveDir = datetime.datetime.now().strftime("%d%b%YT%H%M")

        if not os.path.exists(opts.saveDir):
                print ("save direcotry does not exits! so creating", opts.saveDir)
                os.mkdir(opts.saveDir)
        
	fileout = ROOT.TFile(opts.saveDir+'/'+x_name+'.root', 'RECREATE')
	fileout.cd()
	for i in range(0,len(hist_array)):
		hist_array[i].Write() #Fixme: try to rename while save
	fileout.Close()
        
        # https://twiki.cern.ch/twiki/bin/viewauth/CMS/TopSystematics#Luminosity
        if opts.era == "2016APV":
                print ("year: 2016 APV")
                lumi=19520. 
        elif opts.era == "2016postAPV":
                print ("year: 2016 postAPV")
                lumi=16810.
        elif opts.era == "2017":
                print ("year: 2017")
                lumi=41480.
        elif opts.era == "2018":
                print ("year: 2018")
                lumi=59830.
        elif opts.era == "2016merged":
                print ("year: 2016")
                lumi=1.
        else:
                raise Exception ("select correct era!")

	DY = hist_array[0].Clone()
	DY.SetFillColor(ROOT.kRed)
	DY.Scale(lumi)

	VV = hist_array[1].Clone()
	# VV.Add(hist_array[2]) #ssWW
	VV.Add(hist_array[3])
	# VV.Add(hist_array[4]) #WZew
	VV.Add(hist_array[5])
	# VV.Add(hist_array[6]) #ZZ
	# VV.Add(hist_array[7]) #ZG
	VV.SetFillColor(ROOT.kCyan-9)
	VV.Scale(lumi)

	VVV = hist_array[8].Clone()
	VVV.Add(hist_array[9])
	VVV.Add(hist_array[10])
	VVV.Add(hist_array[11])
	VVV.SetFillColor(ROOT.kSpring-9)
	VVV.Scale(lumi)
        
	SingleTop = hist_array[12].Clone()
	SingleTop.Add(hist_array[13])
	SingleTop.SetFillColor(ROOT.kGray)
	SingleTop.Scale(lumi)
        
        ttW = hist_array[14].Clone()
        ttW.Add(hist_array[15])
        ttW.SetFillColor(ROOT.kGreen-2)
        ttW.Scale(lumi)
        
        ttZ = hist_array[16].Clone()
        ttZ.Add(hist_array[17])
        ttZ.SetFillColor(ROOT.kCyan-2)
        ttZ.Scale(lumi)

        ttVH = hist_array[18].Clone()
        ttVH.Add(hist_array[23])
        ttVH.Add(hist_array[24])
        ttVH.SetFillColor(ROOT.kRed-9)
        ttVH.Scale(lumi)
        
        tttX = hist_array[20].Clone()
        tttX.Add(hist_array[21])
        tttX.Add(hist_array[22])
        tttX.SetFillColor(ROOT.kPink-3)
        tttX.Scale(lumi)
        
        ttVV = hist_array[25].Clone()
        ttVV.Add(hist_array[26])
        ttVV.Add(hist_array[27])
        ttVV.SetFillColor(ROOT.kOrange+3)
        ttVV.Scale(lumi)
        
	# ttXorXX.Add(hist_array[19]) #not used in Limit
        
	tzq = hist_array[28].Clone()
	tzq.SetFillColor(ROOT.kYellow-4)
	tzq.Scale(lumi)

	TT = hist_array[29].Clone()
	TT.SetFillColor(ROOT.kBlue)
	TT.Scale(lumi)

        VBS = hist_array[64].Clone()
        VBS.SetFillColor(ROOT.kBlue-6)
        VBS.Add(hist_array[65])
        VBS.Add(hist_array[66])
        VBS.Add(hist_array[67])
        VBS.Scale(lumi)

	FakeLep_mc = hist_array[30].Clone()
	FakeLep_mc.Add(hist_array[31])
	FakeLep_mc.Add(hist_array[32])
	FakeLep_mc.Add(hist_array[33])
	FakeLep_mc.Add(hist_array[34])
	FakeLep_mc.Add(hist_array[35])
	FakeLep_mc.Add(hist_array[36])
	FakeLep_mc.Add(hist_array[37])
	FakeLep_mc.Add(hist_array[38])
	FakeLep_mc.Add(hist_array[39])
	FakeLep_mc.Add(hist_array[40])
	FakeLep_mc.Add(hist_array[41])
	FakeLep_mc.Add(hist_array[42])
	FakeLep_mc.Add(hist_array[43])
	FakeLep_mc.Add(hist_array[44])
	FakeLep_mc.Add(hist_array[45])
	FakeLep_mc.Add(hist_array[46])
	FakeLep_mc.Add(hist_array[47])
	FakeLep_mc.Add(hist_array[48])
	FakeLep_mc.Add(hist_array[49])
	FakeLep_mc.Add(hist_array[50])
	FakeLep_mc.Add(hist_array[51])
	FakeLep_mc.Add(hist_array[52])
	FakeLep_mc.Add(hist_array[53])
	FakeLep_mc.Add(hist_array[54])
	FakeLep_mc.Add(hist_array[55])
	FakeLep_mc.Add(hist_array[56])
	FakeLep_mc.Add(hist_array[57])
	FakeLep_mc.Add(hist_array[58])
	FakeLep_mc.Add(hist_array[59])
        #four fakeVBS
        FakeLep_mc.Add(hist_array[68])
        FakeLep_mc.Add(hist_array[69])
        FakeLep_mc.Add(hist_array[70])
        FakeLep_mc.Add(hist_array[71])
        
	FakeLep_mc.Scale(lumi)
        # print ("===================================================")
        # print ("Fakelep_mc integral final: ", FakeLep_mc.Integral())
        # print ("===================================================")

	FakeLep = hist_array[60].Clone() #this is data-fake
	FakeLep.Add(hist_array[61])      #this is data-fake
	if isem==1:
		FakeLep.Add(hist_array[72])#if emu channel
	FakeLep.Add(FakeLep_mc.Clone())
	FakeLep.SetFillColor(ROOT.kViolet-4)

        # print ("===================================================")
        # print ("Fakelep data1 integral(): ", hist_array[60].Integral())
        # print ("Fakelep data2 integral(): ", hist_array[61].Integral())
        # print ("Final FakeLep Integral(): ", FakeLep.Integral())
        # print ("===================================================")

	Data = hist_array[62].Clone()
	Data.Add(hist_array[63])
	if isem==1:
		Data.Add(hist_array[73])#if emu channel
	if not opts.draw_data: Data.Reset('ICE')
	Data.SetMarkerStyle(20)
	Data.SetMarkerSize(0.85)
	Data.SetMarkerColor(1)
	Data.SetLineWidth(1)
        
        # setting histoname for saving in root file(further extration and run-2 combination)
        Data.SetName('Data')
        DY.SetName('DY')
        TT.SetName('TT')
        FakeLep.SetName('FakeLep')
        VV.SetName('VV')
        VVV.SetName('VVV')
        SingleTop.SetName('SingleTop')
        ttW.SetName('ttW')
        ttZ.SetName('ttZ')
        ttVH.SetName('ttVH')
        tttX.SetName('tttX')
        ttVV.SetName('ttVV')
        tzq.SetName('tzq')
        VBS.SetName('VBS')
        
        fileout_final = ROOT.TFile(opts.saveDir+'/'+x_name+'_final.root', 'RECREATE')
	fileout_final.cd()
        Data.Write()
        DY.Write()
        TT.Write()
        FakeLep.Write()
        VV.Write()
        VVV.Write()
        SingleTop.Write()
        ttW.Write()
        ttZ.Write()
        ttVH.Write()
        tttX.Write()
        ttVV.Write()
        tzq.Write()
        VBS.Write()
	fileout_final.Close()


	h_stack = ROOT.THStack()
	h_stack.Add(DY)
	h_stack.Add(TT)
	h_stack.Add(FakeLep)
	h_stack.Add(VV)
	h_stack.Add(VVV)
	h_stack.Add(SingleTop)
	h_stack.Add(ttW)
        h_stack.Add(ttZ)
        h_stack.Add(ttVH)
        h_stack.Add(tttX)
        h_stack.Add(ttVV)
	h_stack.Add(tzq)
        h_stack.Add(VBS)
        
	max_yields = 0
	Nbins=h_stack.GetStack().Last().GetNbinsX()
	for i in range(1,Nbins+1):
		max_yields_temp = h_stack.GetStack().Last().GetBinContent(i)
		if max_yields_temp>max_yields:max_yields=max_yields_temp

	max_yields_data = 0
	for i in range(1,Nbins+1):
		max_yields_data_temp = Data.GetBinContent(i)
		if max_yields_data_temp>max_yields_data:max_yields_data=max_yields_data_temp

	h_stack.SetMaximum(max(max_yields, max_yields_data)*1.8)

	##MC error
	h_error = h_stack.GetStack().Last()
	h_error.SetBinErrorOption(ROOT.TH1.kPoisson);
	binsize = h_error.GetSize()-2;
	x = [];
	y = [];
	xerror_l = [];
	xerror_r = [];
	yerror_u = [];
	yerror_d = [];
	y_pad2 = [];
	y_pad2_error_u = [];
	y_pad2_error_d = [];
	for i in range(0,binsize):
		x.append(h_error.GetBinCenter(i+1))
		y.append(h_error.GetBinContent(i+1))
		y_pad2.append(1.0)
		xerror_l.append(0.5*h_error.GetBinWidth(i+1))
		xerror_r.append(0.5*h_error.GetBinWidth(i+1))
		yerror_u.append(h_error.GetBinErrorUp(i+1))
		yerror_d.append(h_error.GetBinErrorLow(i+1))
		if h_error.GetBinContent(i+1)<=0:
		  y_pad2_error_u.append(0)
		  y_pad2_error_d.append(0)
		else:
		  y_pad2_error_u.append(h_error.GetBinErrorUp(i+1)/(h_error.GetBinContent(i+1)))
		  y_pad2_error_d.append(h_error.GetBinErrorLow(i+1)/(h_error.GetBinContent(i+1)))
	gr = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y),np.array(xerror_l),np.array(xerror_r), np.array(yerror_d), np.array(yerror_u))
	gr_pad2 = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y_pad2),np.array(xerror_l),np.array(xerror_r), np.array(y_pad2_error_d), np.array(y_pad2_error_u))

	DY_yield =   round(DY.Integral(),1)
	TT_yield =   round(TT.Integral(),1)
	VV_yield =   round(VV.Integral(),1)
	VVV_yield =  round(VVV.Integral(),1)
	SingleTop_yield =round(SingleTop.Integral(),1)
        ttW_yield =  round(ttW.Integral(),1)
        ttZ_yield =  round(ttZ.Integral(),1)
        ttVH_yield = round(ttVH.Integral(),1)
        tttX_yield = round(tttX.Integral(),1)
        ttVV_yield = round(ttVV.Integral(),1)
	#ttXorXX_yield =round(ttXorXX.Integral(),1)
	tzq_yield =round(tzq.Integral(),1)
        VBS_yield =round(VBS.Integral(),1)
	FakeLep_yield =round(FakeLep.Integral(),1)
	Data_yield = round(Data.Integral())

	c = ROOT.TCanvas()
	pad1 = ROOT.TPad('pad1','',0.00, 0.22, 0.99, 0.99)
	pad2 = ROOT.TPad('pad1','',0.00, 0.00, 0.99, 0.22)
	pad1.SetBottomMargin(0.025);
        pad2.SetTopMargin(0.035);
        pad2.SetBottomMargin(0.45);
	pad1.Draw()
	pad2.Draw()
	pad1.cd()
	h_stack.Draw('HIST')
	Data.Draw("SAME pe")

	gr.SetFillColor(1)
	gr.SetFillStyle(3005)
	gr.Draw("SAME 2")
	if 'ttc_l1_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Leading lepton)', True)
        if 'max_lep_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Leading lepton)', True)
	if 'ttc_l1_eta' in x_name:set_axis(h_stack,'x', '#eta(Leading lepton)', False)
	if 'ttc_l1_phi' in x_name:set_axis(h_stack,'x', '#phi(leading lepton)', False)
	if 'ttc_l2_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Subleading lepton)', True)
	if 'ttc_l2_eta' in x_name:set_axis(h_stack,'x', '#eta(Subleading lepton)', False)
	if 'ttc_l2_phi' in x_name:set_axis(h_stack,'x', '#phi(Subleading lepton)', False)
	if 'ttc_mll' in x_name:set_axis(h_stack,'x', 'M_{ll}', True)
	if 'ttc_drll' in x_name:set_axis(h_stack,'x', '#DeltaR_{ll}', False)
	if 'ttc_dphill' in x_name:set_axis(h_stack,'x', '#Delta#phi_{ll}', False)
	if 'ttc_met' in x_name:set_axis(h_stack,'x', 'MET', True)
	if 'ttc_met_phi' in x_name:set_axis(h_stack,'x', '#phi(MET)', False)
	if 'j1_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(j1)', True)
	if 'j1_eta' in x_name:set_axis(h_stack,'x', '#eta(j1)', False)
	if 'j1_phi' in x_name:set_axis(h_stack,'x', '#phi(j1)', False)
	if 'j1_mass' in x_name:set_axis(h_stack,'x', 'M(j1)', True)
	if 'j2_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(j2)', True)
	if 'j2_eta' in x_name:set_axis(h_stack,'x', '#eta(j2)', False)
	if 'j2_phi' in x_name:set_axis(h_stack,'x', '#phi(j2)', False)
	if 'j2_mass' in x_name:set_axis(h_stack,'x', 'M(j2)', True)
	if 'j3_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(j3)', True)
	if 'j3_eta' in x_name:set_axis(h_stack,'x', '#eta(j3)', False)
	if 'j3_phi' in x_name:set_axis(h_stack,'x', '#phi(j3)', False)
	if 'j3_mass' in x_name:set_axis(h_stack,'x', 'M(j3)', True)
	if 'ttc_mllj1' in x_name:set_axis(h_stack,'x', 'M(ll, j1)', True)
	if 'ttc_mllj2' in x_name:set_axis(h_stack,'x', 'M(ll, j2)', True)
	if 'ttc_mllj3' in x_name:set_axis(h_stack,'x', 'M(ll, j3)', True)
	if 'ttc_dr_l1j1' in x_name:set_axis(h_stack,'x', '#DeltaR(l1, j1)', False)
	if 'ttc_dr_l1j2' in x_name:set_axis(h_stack,'x', '#DeltaR(l1, j2)', False)
	if 'ttc_dr_l1j3' in x_name:set_axis(h_stack,'x', '#DeltaR(l1, j3)', False)
	if 'ttc_dr_l2j1' in x_name:set_axis(h_stack,'x', '#DeltaR(l2, j1)', False)
	if 'ttc_dr_l2j2' in x_name:set_axis(h_stack,'x', '#DeltaR(l2, j2)', False)
	if 'ttc_dr_l2j3' in x_name:set_axis(h_stack,'x', '#DeltaR(l2, j3)', False)
	if 'n_tight_jet' in x_name:set_axis(h_stack,'x', 'Jet multiplicity', False)

	if 'DY_l1_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Leading lepton)', True)
	if 'DY_l1_eta' in x_name:set_axis(h_stack,'x', '#eta(Leading lepton)', False)
	if 'DY_l1_phi' in x_name:set_axis(h_stack,'x', '#phi(Leading lepton)', False)
	if 'DY_l2_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Subleading lepton)', True)
	if 'DY_l2_eta' in x_name:set_axis(h_stack,'x', '#eta(Subleading lepton)', False)
	if 'DY_l2_phi' in x_name:set_axis(h_stack,'x', '#phi(Subleading lepton)', False)
	if 'DY_z_mass' in x_name:set_axis(h_stack,'x', 'M(Z)', True)
	if 'DY_z_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Z)', True)
	if 'DY_z_eta' in x_name:set_axis(h_stack,'x', '#eta(Z)', False)
	if 'DY_z_phi' in x_name:set_axis(h_stack,'x', '#phi(Z)', False)
	# WZ region
	if 'wl_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(W lep)', True)
	if 'wl_eta' in x_name:set_axis(h_stack,'x', '#eta(W lep)', False)
	if 'zl1_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Z l1)', True)
	if 'zl1_eta' in x_name:set_axis(h_stack,'x', '#eta(Z l1)', False)
	if 'zl2_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Z l2)', True)
	if 'zl2_eta' in x_name:set_axis(h_stack,'x', '#eta(Z l2)', False)
	#if 'met' in x_name:set_axis(h_stack,'x', 'MET', True)
	if 'zmass' in x_name:set_axis(h_stack,'x', 'M(Z)', True)
	
	set_axis(h_stack,'y', 'Event/Bin', False)

	CMSstyle.SetStyle(pad1, opts.era)
        CMSstyle.addChannelText(pad1, opts.channel) #new
        
	##legend
	leg1 = ROOT.TLegend(0.66, 0.62, 0.94, 0.88)
        leg2 = ROOT.TLegend(0.44, 0.62, 0.64, 0.88)
        leg3 = ROOT.TLegend(0.17, 0.62, 0.40, 0.88)
        leg1.SetMargin(0.4)
        leg2.SetMargin(0.4)
        leg3.SetMargin(0.4)

        leg3.AddEntry(DY,'DY ['+str(DY_yield)+']','f')
        leg3.AddEntry(ttW,'ttW ['+str(ttW_yield)+']','f')
        leg3.AddEntry(ttZ,'ttZ ['+str(ttZ_yield)+']','f')
        leg3.AddEntry(gr,'Stat. unc','f')
        leg3.AddEntry(Data,'Data ['+str(Data_yield)+']','pe')
        leg2.AddEntry(TT,'TT ['+str(TT_yield)+']','f')
        leg2.AddEntry(FakeLep,'FakeLep ['+str(FakeLep_yield)+']','f')
        leg2.AddEntry(VV,'VV ['+str(VV_yield)+']','f')
        leg2.AddEntry(VBS,'VBS ['+str(VBS_yield)+']','f')
        leg2.AddEntry(ttVH,'ttVH ['+str(ttVH_yield)+']','f')
        leg1.AddEntry(VVV,'VVV ['+str(VVV_yield)+']','f')
        leg1.AddEntry(SingleTop,'SingleTop ['+str(SingleTop_yield)+']','f')
        leg1.AddEntry(tttX,'tttX ['+str(tttX_yield)+']','f')
        leg1.AddEntry(ttVV,'ttVV ['+str(ttVV_yield)+']','f')
        leg1.AddEntry(tzq,'tzq ['+str(tzq_yield)+']','f')
        
        leg1.SetFillColor(ROOT.kWhite)
        leg1.Draw('same')
        leg2.SetFillColor(ROOT.kWhite);
        leg2.Draw('same');
        leg3.SetFillColor(ROOT.kWhite);
        leg3.Draw('same');

	pad2.cd()
	hMC = h_stack.GetStack().Last()
	hData = Data.Clone()
	hData.Divide(hMC)
	hData.SetMarkerStyle(20)
        hData.SetMarkerSize(0.85)
        hData.SetMarkerColor(1)
        hData.SetLineWidth(1)

	hData.GetYaxis().SetTitle("Data/Pred.")
	hData.GetXaxis().SetTitle(h_stack.GetXaxis().GetTitle())
        hData.GetYaxis().CenterTitle()
	hData.SetMaximum(2.0)
	hData.SetMinimum(0.0)
        hData.GetYaxis().SetNdivisions(4,kFALSE)
        hData.GetYaxis().SetTitleOffset(0.3)
        hData.GetYaxis().SetTitleSize(0.13)
        hData.GetYaxis().SetLabelSize(0.1)
        hData.GetXaxis().SetTitleSize(0.14)
        hData.GetXaxis().SetLabelSize(0.1)
	hData.Draw()

	gr_pad2.SetFillColor(1)
        gr_pad2.SetFillStyle(3005)
        gr_pad2.Draw("SAME 2")

	c.Update()
	c.SaveAs(opts.saveDir+'/'+x_name+'.pdf')
	c.SaveAs(opts.saveDir+'/'+x_name+'.png')
	return c
	pad1.Close()
	pad2.Close()
	del hist_array


def run2combination(opts, x_name=''):
        # save all output inside a directory
        if opts.saveDir == None:
                opts.saveDir = datetime.datetime.now().strftime("%d%b%YT%H%M")

        if not os.path.exists(opts.saveDir):
                print ("save direcotry does not exits! so creating", opts.saveDir)
                os.mkdir(opts.saveDir)
        
        # fileout = ROOT.TFile(opts.saveDir+'/'+x_name+'.root', 'RECREATE')
	# fileout.cd()
	# for i in range(0,len(hist_array)):
	# 	hist_array[i].Write() #Fixme: try to rename while save
	# fileout.Close()
        f1 = ROOT.TFile(opts.fee)
        f2 = ROOT.TFile(opts.fem)
        f3 = ROOT.TFile(opts.fmm)
        
        DY = f1.Get("DY")
        DY.Add(f2.Get("DY"))
        DY.Add(f3.Get("DY"))
        DY.SetFillColor(ROOT.kRed)
        # print ("DY integral: ", DY.Integral())
        
        VV = f1.Get("VV")
        VV.Add(f2.Get("VV"))
        VV.Add(f3.Get("VV"))
        VV.SetFillColor(ROOT.kCyan-9)
        
        VVV = f1.Get("VVV")
        VVV.Add(f2.Get("VVV"))
        VVV.Add(f3.Get("VVV"))
        VVV.SetFillColor(ROOT.kSpring-9)
        
        SingleTop = f1.Get("SingleTop")
        SingleTop.Add(f2.Get("SingleTop"))
        SingleTop.Add(f3.Get("SingleTop"))
        SingleTop.SetFillColor(ROOT.kGray)

        ttW = f1.Get("ttW")
        ttW.Add(f2.Get("ttW"))
        ttW.Add(f3.Get("ttW"))
        ttW.SetFillColor(ROOT.kGreen-2)

        ttZ = f1.Get("ttZ")
        ttZ.Add(f2.Get("ttZ"))
        ttZ.Add(f3.Get("ttZ"))
        ttZ.SetFillColor(ROOT.kCyan-2)

        ttVH = f1.Get("ttVH")
        ttVH.Add(f2.Get("ttVH"))
        ttVH.Add(f3.Get("ttVH"))
        ttVH.SetFillColor(ROOT.kRed-9)

        tttX = f1.Get("tttX")
        tttX.Add(f2.Get("tttX"))
        tttX.Add(f3.Get("tttX"))
        tttX.SetFillColor(ROOT.kPink-3)

        ttVV = f1.Get("ttVV")
        ttVV.Add(f2.Get("ttVV"))
        ttVV.Add(f3.Get("ttVV"))
        ttVV.SetFillColor(ROOT.kOrange+3)

        tzq = f1.Get("tzq")
        tzq.Add(f2.Get("tzq"))
        tzq.Add(f3.Get("tzq"))
        tzq.SetFillColor(ROOT.kYellow-4)

        TT = f1.Get("TT")
        TT.Add(f2.Get("TT"))
        TT.Add(f3.Get("TT"))
        TT.SetFillColor(ROOT.kBlue)

        VBS = f1.Get("VBS")
        VBS.Add(f2.Get("VBS"))
        VBS.Add(f3.Get("VBS"))
        VBS.SetFillColor(ROOT.kBlue-6)
        
        FakeLep = f1.Get("FakeLep")
        FakeLep.Add(f2.Get("FakeLep"))
        FakeLep.Add(f3.Get("FakeLep"))
        FakeLep.SetFillColor(ROOT.kViolet-4)
        print ("here")
        sys.exit(1)
        
        # Define stack for Run-2 combination plot
        h_stack = ROOT.THStack()
	h_stack.Add(DY)
	h_stack.Add(TT)
	h_stack.Add(FakeLep)
	h_stack.Add(VV)
	h_stack.Add(VVV)
	h_stack.Add(SingleTop)
	h_stack.Add(ttW)
        h_stack.Add(ttZ)
        h_stack.Add(ttVH)
        h_stack.Add(tttX)
        h_stack.Add(ttVV)
	h_stack.Add(tzq)
        h_stack.Add(VBS)
        
	max_yields = 0
	Nbins=h_stack.GetStack().Last().GetNbinsX()
	for i in range(1,Nbins+1):
		max_yields_temp = h_stack.GetStack().Last().GetBinContent(i)
		if max_yields_temp>max_yields:max_yields=max_yields_temp

	max_yields_data = 0
	for i in range(1,Nbins+1):
		max_yields_data_temp = Data.GetBinContent(i)
		if max_yields_data_temp>max_yields_data:max_yields_data=max_yields_data_temp

	h_stack.SetMaximum(max(max_yields, max_yields_data)*1.8)

	##MC error
	h_error = h_stack.GetStack().Last()
	h_error.SetBinErrorOption(ROOT.TH1.kPoisson);
	binsize = h_error.GetSize()-2;
	x = [];
	y = [];
	xerror_l = [];
	xerror_r = [];
	yerror_u = [];
	yerror_d = [];
	y_pad2 = [];
	y_pad2_error_u = [];
	y_pad2_error_d = [];
	for i in range(0,binsize):
		x.append(h_error.GetBinCenter(i+1))
		y.append(h_error.GetBinContent(i+1))
		y_pad2.append(1.0)
		xerror_l.append(0.5*h_error.GetBinWidth(i+1))
		xerror_r.append(0.5*h_error.GetBinWidth(i+1))
		yerror_u.append(h_error.GetBinErrorUp(i+1))
		yerror_d.append(h_error.GetBinErrorLow(i+1))
		if h_error.GetBinContent(i+1)<=0:
		  y_pad2_error_u.append(0)
		  y_pad2_error_d.append(0)
		else:
		  y_pad2_error_u.append(h_error.GetBinErrorUp(i+1)/(h_error.GetBinContent(i+1)))
		  y_pad2_error_d.append(h_error.GetBinErrorLow(i+1)/(h_error.GetBinContent(i+1)))
	gr = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y),np.array(xerror_l),np.array(xerror_r), np.array(yerror_d), np.array(yerror_u))
	gr_pad2 = ROOT.TGraphAsymmErrors(len(x), np.array(x), np.array(y_pad2),np.array(xerror_l),np.array(xerror_r), np.array(y_pad2_error_d), np.array(y_pad2_error_u))

	DY_yield =   round(DY.Integral(),1)
	TT_yield =   round(TT.Integral(),1)
	VV_yield =   round(VV.Integral(),1)
	VVV_yield =  round(VVV.Integral(),1)
	SingleTop_yield =round(SingleTop.Integral(),1)
        ttW_yield =  round(ttW.Integral(),1)
        ttZ_yield =  round(ttZ.Integral(),1)
        ttVH_yield = round(ttVH.Integral(),1)
        tttX_yield = round(tttX.Integral(),1)
        ttVV_yield = round(ttVV.Integral(),1)
	tzq_yield =round(tzq.Integral(),1)
        VBS_yield =round(VBS.Integral(),1)
	FakeLep_yield =round(FakeLep.Integral(),1)
	Data_yield = round(Data.Integral())

	c = ROOT.TCanvas()
	pad1 = ROOT.TPad('pad1','',0.00, 0.22, 0.99, 0.99)
	pad2 = ROOT.TPad('pad1','',0.00, 0.00, 0.99, 0.22)
	pad1.SetBottomMargin(0.025);
        pad2.SetTopMargin(0.035);
        pad2.SetBottomMargin(0.45);
	pad1.Draw()
	pad2.Draw()
	pad1.cd()
	h_stack.Draw('HIST')
	Data.Draw("SAME pe")

	gr.SetFillColor(1)
	gr.SetFillStyle(3005)
	gr.Draw("SAME 2")
	if 'ttc_l1_pt' in x_name:set_axis(h_stack,'x', 'p_{T}(Leading lepton)', True)

	set_axis(h_stack,'y', 'Event/Bin', False)

	CMSstyle.SetStyle(pad1, opts.era)
        CMSstyle.addChannelText(pad1, opts.channel) #new
        
	##legend
	leg1 = ROOT.TLegend(0.66, 0.62, 0.94, 0.88)
        leg2 = ROOT.TLegend(0.44, 0.62, 0.64, 0.88)
        leg3 = ROOT.TLegend(0.17, 0.62, 0.40, 0.88)
        leg1.SetMargin(0.4)
        leg2.SetMargin(0.4)
        leg3.SetMargin(0.4)

        leg3.AddEntry(DY,'DY ['+str(DY_yield)+']','f')
        leg3.AddEntry(ttW,'ttW ['+str(ttW_yield)+']','f')
        leg3.AddEntry(ttZ,'ttZ ['+str(ttZ_yield)+']','f')
        leg3.AddEntry(gr,'Stat. unc','f')
        leg3.AddEntry(Data,'Data ['+str(Data_yield)+']','pe')
        leg2.AddEntry(TT,'TT ['+str(TT_yield)+']','f')
        leg2.AddEntry(FakeLep,'FakeLep ['+str(FakeLep_yield)+']','f')
        leg2.AddEntry(VV,'VV ['+str(VV_yield)+']','f')
        leg2.AddEntry(VBS,'VBS ['+str(VBS_yield)+']','f')
        leg2.AddEntry(ttVH,'ttVH ['+str(ttVH_yield)+']','f')
        leg1.AddEntry(VVV,'VVV ['+str(VVV_yield)+']','f')
        leg1.AddEntry(SingleTop,'SingleTop ['+str(SingleTop_yield)+']','f')
        leg1.AddEntry(tttX,'tttX ['+str(tttX_yield)+']','f')
        leg1.AddEntry(ttVV,'ttVV ['+str(ttVV_yield)+']','f')
        leg1.AddEntry(tzq,'tzq ['+str(tzq_yield)+']','f')
        
        leg1.SetFillColor(ROOT.kWhite)
        leg1.Draw('same')
        leg2.SetFillColor(ROOT.kWhite);
        leg2.Draw('same');
        leg3.SetFillColor(ROOT.kWhite);
        leg3.Draw('same');

	pad2.cd()
	hMC = h_stack.GetStack().Last()
	hData = Data.Clone()
	hData.Divide(hMC)
	hData.SetMarkerStyle(20)
        hData.SetMarkerSize(0.85)
        hData.SetMarkerColor(1)
        hData.SetLineWidth(1)

	hData.GetYaxis().SetTitle("Data/Pred.")
	hData.GetXaxis().SetTitle(h_stack.GetXaxis().GetTitle())
        hData.GetYaxis().CenterTitle()
	hData.SetMaximum(2.0)
	hData.SetMinimum(0.0)
        hData.GetYaxis().SetNdivisions(4,kFALSE)
        hData.GetYaxis().SetTitleOffset(0.3)
        hData.GetYaxis().SetTitleSize(0.13)
        hData.GetYaxis().SetLabelSize(0.1)
        hData.GetXaxis().SetTitleSize(0.14)
        hData.GetXaxis().SetLabelSize(0.1)
	hData.Draw()

	gr_pad2.SetFillColor(1)
        gr_pad2.SetFillStyle(3005)
        gr_pad2.Draw("SAME 2")

	c.Update()
	c.SaveAs(opts.saveDir+'/'+x_name+'.pdf')
	c.SaveAs(opts.saveDir+'/'+x_name+'.png')
	return c
	pad1.Close()
	pad2.Close()
	del hist_array
        

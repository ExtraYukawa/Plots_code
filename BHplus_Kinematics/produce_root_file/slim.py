import ROOT
import time
import os, sys
import math
import json
import optparse, argparse
from collections import OrderedDict
from math import sqrt
from common import inputFile_path

def Slim_module(filein,
                era,
                output_dir,
                channel = "ele",
                Labels=["Normal"],
                Black_list=[],
                POIs=[],
                sample_labels = [],
                weight_def="puWeight*genWeight/abs(genWeight)",
                region="signal_region",
                start = -1,
                end   = -1,
                index = -1):

  ###################
  ## Load Function ##
  ###################

  ROOT.gSystem.Load("libGenVector.so")
  header_path = os.path.join("script/slim_" + era + ".h")
  ROOT.gInterpreter.Declare('#include "{}"'.format(header_path))

  #################
  ##  Load File  ##
  #################

  path    = str(inputFile_path[era])
  fin     = os.path.join(path, filein)
  if not index == -1:
    fileOut = os.path.join(output_dir, str(index) + "_" + filein)
  else:
    fileOut = os.path.join(output_dir, filein) 
  treeOut = "SlimTree"

  if not os.path.isdir(output_dir):
    os.system("mkdir -p " + output_dir)

  jsonfile = open(os.path.join("../../data", "sample_%s.json"%era))
  samples = json.load(jsonfile, object_pairs_hook=OrderedDict)
  jsonfile.close()

  for sample in samples:
    if (((sample + ".") in filein) or ((sample + "_") in filein)):
      sample_name = sample
  #sample_name = filein.replace('.root', '').replace('-','')

  ##################
  ##  RDataFrame  ##
  ##################

  df_a   = ROOT.RDataFrame("Events", fin)
  if not start == -1:
    df = df_a.Range(start, end)
  else:
    df = df_a
  print(fin, start, end)

  #######################
  ##  Define Nuisance  ##
  #######################

  jsonfile = open(os.path.join("../../data", "nuisance.json"))
  nuisances = json.load(jsonfile, object_pairs_hook=OrderedDict)
  jsonfile.close()
  nuisances_valid = dict()

  for nuisance in nuisances:
    Flag = True
    for Label in nuisances[nuisance]["Label"]:
      if not(Label in sample_labels): Flag = False
    if not Flag: continue
    nuisances_valid[nuisances[nuisance]["Nominal"][-1]] = nuisance


  #######################
  ##  Define Variable  ##
  #######################

  jsonfile  = open(os.path.join("../../data", "variable.json"))
  variables = json.load(jsonfile, object_pairs_hook=OrderedDict)
  jsonfile.close()
  
  print(nuisances_valid)
  for variable in variables:

    Flag = False
    for Label in Labels:
      if Label in variables[variable]["Label"]: Flag = True
    for Label in Black_list:
      if Label in variables[variable]["Label"]: Flag = False
    Flag = True
    if not Flag: continue
    if "Data" in sample_labels and "MC" in variables[variable]["Label"]: continue

    if not (variables[variable]["Def"] == "Defined"):
      df = df.Define(str(variable), str(variables[variable]["Def"]))
    if variable in nuisances_valid:
      df = df.Vary(nuisances[nuisances_valid[variable]]["Nominal"], nuisances[nuisances_valid[variable]]["Def"], {"Down", "Up"}, nuisance)

  ##############
  ##  Weight  ##
  ##############
  if "Data" in sample_labels:
    weight_def = 1       # Data weight is also to be 1
    nuisances_valid = [] # Nuisances only affect MC
  df = df.Define("weight", str(weight_def))

  #########
  ## Cut ##
  #########

  cutflow = OrderedDict()

  jsonfile = open(os.path.join("../../data", "cut.json"))
  cuts  = json.load(jsonfile, object_pairs_hook=OrderedDict)
  jsonfile.close()

#  cutflow["all"] = df.Sum("weight").GetValue()

  for cut_name in cuts[region]["channel_cut"][channel]:
    df = df.Filter(str(cuts[region]["channel_cut"][channel][cut_name]), str(cut_name))
  cutflow["channel"] = df.Sum("weight").GetValue()

  for cut_name in cuts[region]["general_cut"]:
    df = df.Filter(str(cuts[region]["general_cut"][cut_name]), str(cut_name))
    cutflow[cut_name] = df.Sum("weight").GetValue()

  print(cutflow)

  #################
  ##  Histogram  ##
  #################

  Histos     = []
  jsonfile   = open(os.path.join("../../data", "histogram.json"))
  Histograms = json.load(jsonfile, object_pairs_hook=OrderedDict)
  jsonfile.close()

  for Histogram in Histograms:
    print("Generating", Histogram)
    Flag = False
    Label_trigger = ""
    for Label in Labels:
      if Label in Histograms[Histogram]["Label"]: Flag = True
    for Label in Black_list:
      if Label in Histograms[Histogram]["Label"]:
        Label_trigger = Label
        Flag = False
    if not Flag:
      print("Label do not satisfied the requirement. Black list label triggered:%s"%Label_trigger)
      continue

    Title  = str(Histograms[Histogram]["Title"])
    xlow   = Histograms[Histogram]["xlow"]
    xhigh  = Histograms[Histogram]["xhigh"]
    nbin   = Histograms[Histogram]["nbin"] * 600 # will be rebinned when plotting
    df_histo = df.Histo1D((str(Histogram), Title, nbin, xlow, xhigh), str(Histogram), "weight")
    Histos.append(df_histo.GetValue().Clone())

    ## Nuisance variation for POIs
    if Histogram in POIs:
      h_variation = ROOT.RDF.Experimental.VariationsFor(df_histo)
      print(h_variation.GetKeys())
      for nuisance in nuisances_valid:
        h_variation_do = h_variation[nuisance + ":Down"].Clone()
        h_variation_do.SetName(str(Histogram) + "_" + nuisance + "_down")
        h_variation_up = h_variation[nuisance + ":Up"].Clone()
        h_variation_up.SetName(str(Histogram) + "_" + nuisance + "_up")
        Histos.append(h_variation_do)
        Histos.append(h_variation_up)

  # Cutflow Histogram
  histo_cutflow = ROOT.TH1D('cutflow', ';;nEvents', len(cutflow), 0, len(cutflow))
  for idx, cut_name in enumerate(cutflow):
    histo_cutflow.SetBinContent(idx+1, cutflow[cut_name])
    histo_cutflow.GetXaxis().SetBinLabel(idx + 1, str(cut_name))
  Histos.append(histo_cutflow.Clone())

  ######################
  ##  Store Variable  ##
  ######################

  columns = ROOT.std.vector("string")()

  for variable in variables:

    Flag = False
    for Label in Labels:
      if Label in variables[variable]["Save"]: Flag = True
    if not Flag: continue
    columns.push_back(str(variable))

  df.Snapshot(treeOut, fileOut, columns)

  #######################
  ##  Store Histogram  ##
  #######################
  
  FileOut = ROOT.TFile.Open(fileOut, "Update")
  FileOut.cd()
  for ij in range(0, len(Histos)):
    h = Histos[ij].Clone()
    h.Write()
  FileOut.Close()


if __name__ == "__main__":

  usage  = 'usage: %prog [options]'
  parser = argparse.ArgumentParser(description=usage)
  parser.add_argument('-e', '--era',    dest='era', help='[2016apv/2106postapv/2017/2018]', default='2018', type=str)
  parser.add_argument('-i', '--iin',    dest='iin', help='input file name', default=None, type=str)
  parser.add_argument('-o', '--outdir', dest='out', help='ouput directory', default='./', type=str)
  parser.add_argument('--start',        dest='start', default=-1, type=int)
  parser.add_argument('--end',          dest='end',   default=-1, type=int)
  parser.add_argument('--index',        dest='index', default=-1, type=int)
  parser.add_argument('--channel',      dest='channel', default='ele', type=str)
  parser.add_argument('--region',       dest='region', default = 'signal_region', type = str)
  parser.add_argument("--Labels", dest = 'Labels', default = ['Normal'], nargs='+')
  parser.add_argument("--Black_list", dest = 'Black_list', default = [], nargs='+')
  parser.add_argument("--sample_labels", dest='sample_labels', default = ["MC", "Background"], nargs='+') 
  parser.add_argument("--POIs",   dest = 'POIs',   default = [], nargs='+') 
  args = parser.parse_args()

  #start = time.clock()
  Slim_module(args.iin, args.era, args.out, start = args.start, end = args.end, index = args.index, channel = args.channel, region = args.region, Labels = args.Labels,Black_list = args.Black_list, POIs = args.POIs, sample_labels = args.sample_labels)
  #end = time.clock()
  #print('process time', end - start)


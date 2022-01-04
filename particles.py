import ROOT
import numpy

f = ROOT.TFile("/data/DATA/data.lhcb/audurier/MCtracks-PbPbtest-100_1.root")
d = f.get("MCParticleNTuple")
tree = d.Tracks

for entriy in tree:
  test = entriy.HitTpos


try:
  cfg.lala
except AttributeError:
  print("erreur")
  
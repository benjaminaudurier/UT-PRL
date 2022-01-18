if __name__ == '__main__':
  import ROOT
  import numpy as np
  import matplotlib.pyplot as plt
  import Ostap.Kisa
  from matplotlib.colors import LogNorm
  
  
  #import files
  f = ROOT.TFile("/data/DATA/data.lhcb/audurier/MCtracks-PbPbtest-100_1.root")
  d = f.get("MCParticleNTuple")
  tree = d.Tracks
  
  #make subplots
  c = ROOT.TCanvas()
  c.SetWindowSize(1530,630)
  c.SetCanvasSize(1500,600)
  c.Divide(2,1)
  
  #count events
  eventNumbers = []
  val = 0
  for entriy in tree: 
    val = entriy.pvz
    if not (val in eventNumbers):  
      eventNumbers.append(val)
  eventNumber = len(eventNumbers)
    
  
  #give the characteristics of the detector (distance in cm)
  minx = -70
  maxx = 70
  nb_bin_x = 70
  miny = -80
  maxy = 80
  nb_bin_y = 80
  nb_bin_r = 140
  minr = 3
  maxr = 60
  
  #give the interesting values for z (first layer of the detector - distance in cm)
  minz = 1
  maxz = 237
  
  #subplot 1 - heatmap (TH2) of position in x and y - keep minz < z < maxz (first layer of detector) && r > minz
  h = ROOT.TH2F('h','titl',nb_bin_x,minx,maxx,nb_bin_y,miny,maxy)
  r2 = tree.Project ( h.GetName() , '(HitUTXpos_0/10):(HitUTYpos_0/10)','HitUTZpos_0/10>{} && HitUTZpos_0/10<{} && (HitUTXpos_0/10)**2 + (HitUTYpos_0/10)**2 > {}**2'.format(minz,maxz,minr))
  h.SetXTitle("X [cm]")
  h.SetYTitle("Y [cm]")
  ROOT.gStyle.SetPalette(1)
  c1 = c.cd(1)
  c1.SetRightMargin(0.17)
  h.Draw('COLZ')
  ROOT.gPad.SetLogz(1)
  ROOT.gPad.SetTitle("test")
  palette = h.GetListOfFunctions().FindObject("palette")
  c1.SetTitle("lalala")
  c1.Modified()
  c1.Update()
  c1.Draw()

  
  
  #subplot 2 - histogram (TH1) of number of hits for a given radius r - keep 0 < z < 2370 (first layer of detector)
  h = ROOT.TH1F('h','titl',nb_bin_r,minr,maxr)
  tree.Project (h.GetName() , '(HitUTXpos_0**2 + HitUTYpos_0**2)**0.5/10','HitUTZpos_0/10 >{} && HitUTZpos_0/10 <{}'.format(minz,maxz))
  f_radial = ROOT.TF1("f_radial", "1/x", minr, maxr)
  h.Multiply(f_radial, nb_bin_r/(2*np.pi*eventNumber*(maxr-minr)))
  h.SetXTitle("R [cm]")
  h.SetYTitle("Hits / cm**2 / BX")
  c2 = c.cd(2)
  h.Draw()
  ROOT.gPad.SetLogy(1)
  c2.SetTitle("lalala")
  c2.Modified()
  c2.Update()
  
  
  
  c.Print("Images/Heat_map_and_distribution_in_r.png")


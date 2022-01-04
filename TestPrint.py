import ROOT

c = ROOT.TCanvas()
c.SetWindowSize(1410,1410)
c.SetCanvasSize(1400,1400)

c1 = c.cd(1)

##size_ref = max(self.largeur_x, self.largeur_y) * 1.2
##marge_gauche = (1-(self.largeur_x/size_ref))/2.
##marge_bas = (1-(self.largeur_y/size_ref))/2.
#
#largeur_x = 1044
#largeur_y = 532
#size_ref = max(largeur_x, largeur_y) * 1.2
#marge_gauche = (1-(largeur_x/size_ref))/2.
#marge_bas = (1-(largeur_y/size_ref))/2.
#
#chip = ROOT.TBox(marge_gauche, marge_bas, 1-marge_gauche, 1-marge_bas)
#chip.SetFillColor(1)
#chip.Draw()
#c1.Modified()
#c1.Update()
#
##grid = ROOT.TBox(marge_gauche + self._zn_mrt_chp_gau/size_ref, marge_bas + self._zn_mrt_chp_bas/size_ref, 1 - marge_gauche - self._zn_mrt_chp_dro/size_ref, 1 - marge_bas - self._zn_mrt_chp_hau/size_ref)
#zn_mrt_chp_gau = 10
#zn_mrt_chp_dro = 10
#zn_mrt_chp_bas = 15
#zn_mrt_chp_hau = 5
#grid = ROOT.TBox(marge_gauche + zn_mrt_chp_gau/size_ref, marge_bas + zn_mrt_chp_bas/size_ref, 1 - marge_gauche - zn_mrt_chp_dro/size_ref, 1 - marge_bas - zn_mrt_chp_hau/size_ref)
#grid.SetFillColor(29)
#grid.Draw()
#c1.Modified()
#c1.Update()
#
#traits = [0] * 1578
#grid_delta_x = grid.GetX2() - grid.GetX1()
#grid_delta_y = grid.GetY2() - grid.GetY1()
#
#for i in range (1045):
#  x = grid.GetX1() + (float(i)/1045) * grid_delta_x
#  traits[i] = ROOT.TLine(x, grid.GetY1(), x, grid.GetY2())
#  traits[i].SetLineColor(50)
#  traits[i].Draw()
#  c1.Modified()
#  c1.Update()
#  
#for i in range(533):
#  y = grid.GetY1() + (float(i)/533) * grid_delta_y
#  traits[i+1045] = ROOT.TLine(grid.GetX1(), y, grid.GetX2(), y)
#  traits[i+1045].SetLineColor(50)
#  traits[i+1045].Draw()
#  c1.Modified()
#  c1.Update()
#  
#  
#c.Print("Boxes.png")

##########################################################################################################################################################################################################

chip_delta_x = 1044
chip_delta_y = 532

zn_mrt_chp_gau = 10
zn_mrt_chp_dro = 10
zn_mrt_chp_bas = 15
zn_mrt_chp_hau = 5

chip_active_delta_x = chip_delta_x - zn_mrt_chp_gau - zn_mrt_chp_dro
chip_active_delta_y = chip_delta_y - zn_mrt_chp_bas - zn_mrt_chp_hau

stave_delta_x = 4 * chip_delta_x
stave_delta_y = 4 * chip_delta_y

scale = max(stave_delta_x, stave_delta_y)/0.9

stave = ROOT.TBox((1 - stave_delta_x/scale)/2, (1 - stave_delta_y/scale)/2, (1 + stave_delta_x /scale)/2, (1 + stave_delta_y/scale)/2)
stave.SetFillColor(1)
stave.Draw()
c1.Modified()
c1.Update()

grid_chips = [0]*16

x = stave.GetX1() + zn_mrt_chp_gau/scale
y = stave.GetY1() + zn_mrt_chp_bas/scale
for i in range (4):
  for j in range(4):
    grid_chips[i*4 + j] = ROOT.TBox(x, y, x + chip_active_delta_x/scale, y + chip_active_delta_y/scale)
    grid_chips[i*4 + j].SetFillColor(29)
    grid_chips[i*4 + j].Draw()
    c1.Modified()
    c1.Update()
    y += chip_delta_y/scale
  y = stave.GetY1() + zn_mrt_chp_bas/scale
  x += chip_delta_x/scale
  
c.Print("Boxes.png")
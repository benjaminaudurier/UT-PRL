import ROOT

import sys
sys.path.insert(1, "/grid_mnt/data__DATA/data.lhcb/PRL/Classes/")

import ClassChip

fileName = "test_gauss.root"
treeName = "myTree"

chip = ClassChip.Chip(0, 0, 0, 1, 1, 10, 10, 0, 0, 0, 1, 1, 1, 1)

n = 120

x = [0.1*k for k in range(n)]
y = [0.1*k for k in range(n)]

x_in = []
y_in = []

for i in range(n):
  for j in range(n):
    if chip.hit_pos(x[i], y[j])[0]:
      x_in.append(x[i])
      y_in.append(y[i])

gr = ROOT.TGraph(n, x_in, y_in)

c = ROOT.TCanvas()

gr.Draw()

c.Modified()
c.Update()

c.Print("test.png")

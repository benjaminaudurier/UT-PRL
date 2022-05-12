import ROOT
import UTGeometry
import ClassParticle
import ClassConfigExperiment
import ClassConfigDetector
import numpy as np
import matplotlib.pyplot as plt
import os

folder = os.getcwd().replace('\\','/')[:-8]

################################ CONSTANT #####################################

f = ROOT.TFile(folder + "/MCtracks-pptest-5000.root")
#f = ROOT.TFile(folder + "/MCtracks-PbPbcentral.root")
d = f.Get("MCParticleNTuple")
tree = d.Tracks 

name_hist_chip = "hist_chip"
name_hist_module = "hist_module"
name_plot_stave = "hit_on_stave"

config_detector = "config_detector1pp"
config_experiment = "config_experiment_pp"
#config_experiment = "config_experiment_PbPb"


############################## DIRECTORIES #################################### 
path1 = folder + "/Pictures"
path2 = folder + "/Pictures/" + config_detector 

for path in [path1,path2]:
    if not os.path.exists(path):
        os.makedirs(path)
        print("Folder " + path + " created")



################################## MACRO ######################################
# main reads the config files, create the config objects
# it creates a detector from the config_detector object
# then, it reads the tree and create an object particle from the tree


if __name__ == '__main__':
  
    #creation of the config object for the detector
    print("\n \n Creation of the config object for the detector \n \n")
    cfg_detector = ClassConfigDetector.Config(folder + "/Configs/" + "config_detector1" + ".txt")

    print("Ratio of active zone : " + str(cfg_detector.get("active_ratio")))
  
    #creation of the config object for the experiment
    print("\n \n Creation of the config object for the experiment \n \n")
    cfg_exp = ClassConfigExperiment.Config(folder + "/Configs/" + config_experiment + ".txt")
  
    #creation of the detector object
    print("\n \n Creation of the detector object \n \n")
    det = UTGeometry.Detector(cfg_detector)
  
    #creation of the particle object
    print("\n \n Creation of the Particle object \n \n")
    particles = ClassParticle.Particle(tree, cfg_exp, cfg_detector)

    #creation of the results array
    print("\n \n Creation of the result array \n \n")
  
    wth_det = cfg_detector.get("wth_det")
    hgt_det = cfg_detector.get("hgt_det")
    copy_part = [[],[]]
    for a,b in zip(particles._list_x,particles._list_y):
        if -wth_det/2<a and a<wth_det/2 and -hgt_det/2<b and b<hgt_det:
            copy_part[0].append(a)
            copy_part[1].append(b)
    res = UTGeometry.hit_parts_precision(det, copy_part, precision = 3)
 
    missed_particle_inside_rectangle_wo_central_zone = len(copy_part[0])


    copy_part = [[a for a in particles._list_x],[a for a in particles._list_y]]
    total_number = UTGeometry.hit_parts_precision(det, copy_part, precision=0)
  
    res = np.array(res)

    res[0 ,len(res[0])//2, len(res[0][0])//2, 0, : ,: ] = 0
 
    #we have to normalize by number of event
    res_nb_event = res/float(particles._number_of_event)
  
    #we create a matrix called datarate of the same size than res, containing the datarate by chip  
    event_rate = cfg_exp.get("event_rate")*10**(3) 
    nb_bit_by_hit = cfg_exp.get("nb_of_bit_BX_id") + int(np.log(cfg_detector.get("nb_line_pxl_chp"))/np.log(2)) + int(np.log(cfg_detector.get("nb_coln_pxl_chp"))/np.log(2))
    print(nb_bit_by_hit)


    #calculation of the data rate
    data_rate = res_nb_event * nb_bit_by_hit * event_rate


    #drawing of the results
    print("\n =================================   \n Drawing of the results \n ================================= \n")
    UTGeometry.draw_detector(det, particles=particles, data_rate = data_rate, name = config_detector + "/final_result", missed_particles =  missed_particle_inside_rectangle_wo_central_zone , total_number = total_number)



    #plotting of the figures
    print("\n ================================= \n Final drawing \n ================================= \n")
    res = np.array(res_nb_event)
    res_flatten = res.flatten()
  

    plt.figure()
    plt.ylabel("Number of chips")
    plt.xlabel("Number of hits / Number of events")
    plt.yscale('log')
    y, bin_edges = np.histogram(res_flatten, bins=30)
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
    width = bin_centers[1] - bin_centers[0]
    plt.bar(bin_centers, y, width = width, yerr = y**0.5)
    plt.savefig("../Pictures/" + config_detector + "/" + name_hist_chip + ".png")
    plt.close()
  
  
    plt.figure()
    plt.ylabel("Number of modules")
    plt.xlabel("Number of hits / Number of events")
    plt.yscale('log')
    res_module_flatten = np.sum(np.array(res),axis=(4,5)).flatten()
    y, bin_edges = np.histogram(res_module_flatten, bins=15)
    bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
    width = bin_centers[1] - bin_centers[0]
    plt.bar(bin_centers, y, width = width, yerr = y**0.5)
    plt.savefig("../Pictures/" + config_detector + "/" + name_hist_module +".png")
    plt.close()
  
  
    plt.figure()
    res_stave = np.sum(np.array(res),axis=(0,2,3,4,5))
    plt.plot(np.arange(len(res_stave)),res_stave, 'x')
    plt.xlabel("Stave number")
    plt.ylabel("Number of hits / Number of events")
    plt.savefig("../Pictures/" + config_detector + "/" + name_plot_stave + ".png")
    plt.close()


    #give the characteristics of the detector
    eventNumber = particles._number_of_event
    x_bin_size = 1
    y_bin_size = 1
    minx = - det._wth * 10**-4 /2
    maxx = det._wth * 10**-4 /2
    nb_bin_x = int(det._wth * 10**-4 / x_bin_size)
    miny = - det._hgt * 10**-4 /2
    maxy = det._hgt * 10**-4/2
    nb_bin_y = int(det._hgt * 10**-4 / y_bin_size)
    nb_bin_r = 150
    minr = 0
    maxr = 75
    minz = cfg_exp.get("min_z")
    maxz = cfg_exp.get("max_z")


    #subplot 1 - heatmap (TH2) of position in x and y - keep minz < z < maxz (first layer of detector) && r > minz
    c1 = ROOT.TCanvas("c","", int(maxx-minx)*5, int(maxy-miny)*5)
    h = ROOT.TH2F('h','Occupancy',nb_bin_x, minx, maxx,nb_bin_y, miny, maxy)
    #r2 = tree.Project ( h.GetName() , '(HitUTXpos_0/10):(HitUTYpos_0/10)','HitUTZpos_0/10>{} && HitUTZpos_0/10<{} && (HitUTXpos_0/10)**2 + (HitUTYpos_0/10)**2 > {}**2'.format(minz,maxz,minr))
    r2 = tree.Project ( h.GetName() , '(HitUTXpos_0/10):(HitUTYpos_0/10)','HitUTZpos_0/10>{} && HitUTZpos_0/10<{}'.format(minz,maxz))
    xaxis = h.GetXaxis()
    yaxis = h.GetYaxis()
    h.Scale(1/(xaxis.GetBinWidth(1)*yaxis.GetBinWidth(1)*eventNumber))
    h.SetXTitle("X [cm]")
    h.SetYTitle("Y [cm]")
    h.SetZTitle("Hit/cm^2/event")
    h.SetStats(0)
    ROOT.gStyle.SetPalette(1)
    c1.SetRightMargin(0.17)
    h.Draw('COLZ')
    ROOT.gPad.SetLogz(1)
    palette = h.GetListOfFunctions().FindObject("palette")
    c1.Modified()
    c1.Update()
    c1.Print("../Pictures/" + config_detector + "/" + "occupancy" + ".png")


    #subplot 2 - histogram (TH1) of number of hits for a given radius r - keep 0 < z < 2370 (first layer of detector)
    c2 = ROOT.TCanvas("c2","")
    h2 = ROOT.TH1F('h2','Distribution of hits in r',nb_bin_r,minr,maxr)
    tree.Project (h2.GetName() , '(HitUTXpos_0**2 + HitUTYpos_0**2)**0.5/10','HitUTZpos_0/10 >{} && HitUTZpos_0/10 <{}'.format(minz,maxz))
    len_r_bin = (maxr-minr)/nb_bin_r
    f_radial = ROOT.TF1("f_radial", f"1/({eventNumber} *({np.pi}*(x+{len_r_bin})**2 - {np.pi}*x**2))", minr, maxr)
    h2.Multiply(f_radial)
    h2.SetXTitle("r [cm]")
    h2.SetYTitle("Hits / cm**2 / event")
    h2.Draw()
    h2.SetStats(0)
    ROOT.gPad.SetLogy(1)
    c2.Modified()
    c2.Update()
    c2.Print("../Pictures/" + config_detector + "/" + "hist" + ".png")

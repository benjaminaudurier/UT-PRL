#!/usr/bin/python

from matplotlib.colors import to_hex, to_rgb
import ROOT
import UTGeometry
import ClassParticle
import ClassConfigExperiment
import ClassConfigDetector
import numpy as np
import matplotlib.pyplot as plt
import os
import argparse
from tqdm import tqdm

folder = os.getcwd().replace("\\","/") + "/"

################################ CONSTANT #####################################
#f = ROOT.TFile(folder + "../MCtracks-pptest-5000.root")


name_hist_chip = "hist_chip"
name_hist_module = "hist_module"
name_plot_stave = "hit_on_stave"



beam_wth = 6e4 # in um
beam_hgt = 6e4

############################## DIRECTORIES #################################### 


############################### FUNCTIONS ##################################### 
def exclude_beam(res, det, wth_beam, hgt_beam):
    cfg_det = det._cfg
    wth_chp = cfg_det.get('wth_chp')
    hgt_chp = cfg_det.get('hgt_chp')
    nb_coln_stv = cfg_det.get('nb_coln_stv')
    nb_row_stv = cfg_det.get('nb_row_stv')
    nb_coln_mdl_stv = cfg_det.get('nb_coln_mdl_stv')
    nb_row_mdl_stv = cfg_det.get('nb_row_mdl_stv')

    if nb_coln_stv == 0:
        j_stvs = [0]
    elif nb_coln_stv % 2 == 0:
        j_stvs = [nb_coln_stv//2, nb_coln_stv//2 - 1]
    else: #nb_coln_stv % 2 =1
        j_stvs = [nb_coln_stv//2]

    if nb_row_stv == 0:
        i_stvs = [0]
    elif nb_row_stv % 2 == 0:
        i_stvs = [nb_row_stv//2, nb_row_stv//2 - 1]
    else: #nb_coln_stv % 2 =1
        i_stvs = [nb_row_stv//2]

    if nb_coln_mdl_stv == 0:
        j_mdls = 0
    elif nb_coln_mdl_stv % 2 == 0:
        j_mdls = [nb_coln_mdl_stv//2, nb_coln_mdl_stv//2 - 1]
    else: #nb_coln_stv % 2 =1
        j_mdls = [nb_coln_mdl_stv//2]

    if nb_row_mdl_stv == 0:
        i_mdls = 0
    elif nb_row_mdl_stv % 2 == 0:
        i_mdls = [nb_row_mdl_stv//2, nb_row_mdl_stv//2 - 1]
    else: #nb_coln_stv % 2 =1
        i_mdls = [nb_row_mdl_stv//2]

    for i_stv in i_stvs:
        for j_stv in j_stvs:
            for i_mdl in i_mdls:
                for j_mdl in j_mdls:
                    i_chps = len(det._matrix[i_stv][j_stv]._matrix[i_mdl][j_mdl]._matrix)
                    j_chps = len(det._matrix[i_stv][j_stv]._matrix[i_mdl][j_mdl]._matrix[0])
                    for i_chp in range(i_chps):
                        for j_chp in range(j_chps):
                            chp = det._matrix[i_stv][j_stv]._matrix[i_mdl][j_mdl]._matrix[i_chp][j_chp]
                            # top-right corner
                            if (chp._x_pos + wth_chp > -wth_beam/2 and chp._y_pos + hgt_chp > -hgt_beam/2 and chp._x_pos + wth_chp < wth_beam/2 and chp._y_pos + hgt_chp < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
                            # bottom-right corner
                            elif (chp._x_pos + wth_chp > -wth_beam/2 and chp._y_pos > -hgt_beam/2 and chp._x_pos + wth_chp < wth_beam/2 and chp._y_pos < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
                            # top-left corner
                            elif (chp._x_pos > -wth_beam/2 and chp._y_pos + hgt_chp > -hgt_beam/2 and chp._x_pos < wth_beam/2 and chp._y_pos + hgt_chp < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
                            # bottom-left corner
                            elif (chp._x_pos > -wth_beam/2 and chp._y_pos > -hgt_beam/2 and chp._x_pos  < wth_beam/2 and chp._y_pos < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
    return res


def exclude_masked_chip_in_module(res, det):
    cfg_det = det._cfg
    masked_chips = cfg_det.get('mask_dead_column')
    nb_coln_stv = cfg_det.get('nb_coln_stv')
    nb_row_stv = cfg_det.get('nb_row_stv')
    nb_coln_mdl_stv = cfg_det.get('nb_coln_mdl_stv')
    nb_row_mdl_stv = cfg_det.get('nb_row_mdl_stv')
    nb_coln_chp_mdl = cfg_det.get('nb_coln_chp_mdl')
    
    for i_stv in range(nb_row_stv):
        for j_stv in range(nb_coln_stv):
            for i_mdl in range(nb_row_mdl_stv):
                for j_mdl in range(nb_coln_mdl_stv):
                    for j_chp in range(nb_coln_chp_mdl):
                        if masked_chips[j_chp] == '0':
                            res[i_stv][j_stv][i_mdl][j_mdl][:,j_chp] = 0
    return res

def exclude_masked_modules(res):  
    res[0,0,2,0,:,:],res[0,0,7,0,:,:] = 0,0
    res[0,0,1,0,:,:],res[0,0,8,0,:,:] = 0,0
    res[0,0,0,0,:,:],res[0,0,9,0,:,:] = 0,0

    res[0,1,1,0,:,:],res[0,1,8,0,:,:] = 0,0
    res[0,1,0,0,:,:],res[0,1,9,0,:,:] = 0,0

    res[0,2,0,0,:,:],res[0,2,9,0,:,:] = 0,0

    res[0,5,0,0,:,:],res[0,5,9,0,:,:] = 0,0

    res[0,6,1,0,:,:],res[0,6,8,0,:,:] = 0,0
    res[0,6,0,0,:,:],res[0,6,9,0,:,:] = 0,0

    res[0,7,2,0,:,:],res[0,7,7,0,:,:] = 0,0
    res[0,7,1,0,:,:],res[0,7,8,0,:,:] = 0,0
    res[0,7,0,0,:,:],res[0,7,9,0,:,:] = 0,0
    return res


################################## MACRO ######################################
# main reads the config files, create the config objects
# it creates a detector from the config_detector object
# then, it reads the tree and create an object particle from the tree


def operations(detector = "UT", mc_tracks = "../MCtracks-PbPbcentral.root",
               cfg_detector_name = "config_detector_1", cfg_experiment_name = "config_experiment_PbPb",
               plot_mc = True, plot_hits = True, plot_geometry = True):

    # creation of the folders that will contain the results
    list_path = []
    list_path.append(folder + "../../Pictures")
    list_path.append(folder + "../../Pictures/" + cfg_detector_name) 
    if plot_mc or plot_hits:
        list_path.append(folder + "../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name)

    for path in list_path:
        if not os.path.exists(path):
            os.makedirs(path)
            print("Folder " + path + " created")

    #creation of the config object for the detector
    print("\n \n Creation of the config object for the detector \n \n")
    cfg_detector = ClassConfigDetector.Config(folder + "../Configs/" + cfg_detector_name +".txt", detector)
    
    #creation of the detector object
    print("\n \n Creation of the detector object \n \n")
    det = UTGeometry.Detector(cfg_detector)
  
    if plot_hits or plot_mc:

        # get the tree from the ROOT file
        f = ROOT.TFile(folder + mc_tracks)
        d = f.Get("MCParticleNTuple")
        tree = d.Tracks 

        #creation of the config object for the experiment
        print("\n \n Creation of the config object for the experiment \n \n")
        cfg_exp = ClassConfigExperiment.Config(folder + "../Configs/" + cfg_experiment_name +".txt")
    
        #creation of the particle object
        print("\n \n Creation of the Particle object \n \n")
        particles = ClassParticle.Particle(tree, cfg_exp, cfg_detector, detector)
    
        #taking information from cfg_exp
        event_rate = cfg_exp.get("event_rate")*10**(3) 
        nb_bit_by_hit = cfg_exp.get("nb_of_bit_BX_id") + int(np.log(cfg_detector.get("nb_row_pxl_chp"))/np.log(2)) + int(np.log(cfg_detector.get("nb_coln_pxl_chp"))/np.log(2))
    
    if plot_hits:

        #creation of the results array
        print("\n \n Creation of the result array \n \n")
    
        copy_part = [[],[]]
        for x,y in zip(particles._list_x,particles._list_y):
            if -det._wth/2<x and x<det._wth/2 and -det._hgt/2<y and y<det._hgt:
                copy_part[0].append(x)
                copy_part[1].append(y)

        total_number_particles = len(copy_part[0])
        with tqdm(total_number_particles) as pbar:
            res, missed_particle_inside_rectangle_wo_central_zone = UTGeometry.hit_parts_precision(det, copy_part, precision = 3, pbar=pbar)
    
        missed_particle_inside_rectangle_wo_central_zone += len(copy_part[0])

        copy_part = [[a for a in particles._list_x],[a for a in particles._list_y]]
        total_number, missed_part_detector = UTGeometry.hit_parts_precision(det, copy_part, precision=0, pbar=pbar)
    

        res = np.array(res)
        res = exclude_beam(res, det, beam_wth, beam_hgt)


        if detector == "MIGHTY":
            res = exclude_masked_chip_in_module(res, det)
            res = exclude_masked_modules(res)


        #we have to normalize by number of event
        res_nb_event = res/float(particles._number_of_event)
    
        #calculation of the data rate
        data_rate = res_nb_event * nb_bit_by_hit * event_rate


        #drawing of the results
        print("\n =================================   \n Drawing of the results \n ================================= \n")
        UTGeometry.draw_detector(det, particles=particles, data_rate = data_rate, name = cfg_detector_name + "/" + cfg_experiment_name + "/final_result",
                                 missed_particles =  missed_particle_inside_rectangle_wo_central_zone, total_number = total_number, detector = detector)



        #plotting of the figures
        print("\n ================================= \n Final drawing \n ================================= \n")
        res = np.array(res_nb_event)
        res_flatten = res.flatten()
  

        plt.figure()
        plt.ylabel("Number of chips")
        plt.xlabel("Number of hits / event")
        plt.yscale('log')
        y, bin_edges = np.histogram(res_flatten, bins=30)
        bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
        width = bin_centers[1] - bin_centers[0]
        plt.bar(bin_centers, y, width = width, yerr = y**0.5)
        plt.savefig("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + name_hist_chip + ".png")
        plt.close()
  
  
        plt.figure()
        plt.ylabel("Number of modules")
        plt.xlabel("Number of hits / event")
        plt.yscale('log')
        res_module_flatten = np.sum(np.array(res),axis=(4,5)).flatten()
        y, bin_edges = np.histogram(res_module_flatten, bins=15)
        bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
        width = bin_centers[1] - bin_centers[0]
        plt.bar(bin_centers, y, width = width, yerr = y**0.5)
        plt.savefig("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + name_hist_module +".png")
        plt.close()
  
  
        plt.figure()
        res_stave = np.sum(np.array(res),axis=(0,2,3,4,5))
        plt.plot(np.arange(len(res_stave)),res_stave, 'x')
        plt.xlabel("Stave number")
        plt.ylabel("Number of hits / event")
        plt.savefig("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + name_plot_stave + ".png")
        plt.close()
    

    if plot_mc:
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

        if detector == "UT":
            tree.Project ( h.GetName() , '(HitUTXpos_0/10):(HitUTYpos_0/10)','HitUTZpos_0/10>{} && HitUTZpos_0/10<{} && (HitUTXpos_0/10)**2 + (HitUTYpos_0/10)**2 > {}**2'.format(minz,maxz,minr))
        elif detector == "MIGHTY":
            tree.Project ( h.GetName() , '(HitXpos_0/10):(HitYpos_0/10)','HitZpos_0/10>{} && HitZpos_0/10<{} && (HitXpos_0/10)**2 + (HitYpos_0/10)**2 > {}**2'.format(minz,maxz, minr))
        xaxis = h.GetXaxis()
        yaxis = h.GetYaxis()
        h.Scale(1/(xaxis.GetBinWidth(1)*yaxis.GetBinWidth(1)*eventNumber))
        h.SetXTitle("X [cm]")
        h.SetYTitle("Y [cm]")
        h.SetZTitle("Hits / cm^2 / event")
        h.SetStats(0)
        ROOT.gStyle.SetPalette(1)
        c1.SetRightMargin(0.17)
        h.Draw('COLZ')
        ROOT.gPad.SetLogz(1)
        palette = h.GetListOfFunctions().FindObject("palette")
        c1.Modified()
        c1.Update()
        c1.Print("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + "occupancy" + ".png")


        #subplot 2 - histogram (TH1) of number of hits for a given radius r - keep 0 < z < 2370 (first layer of detector)
        c2 = ROOT.TCanvas("c2","")
        h2 = ROOT.TH1F('h2','Distribution of hits in r',nb_bin_r,minr,maxr)

        if detector == "UT":
            tree.Project (h2.GetName() , '(HitUTXpos_0**2 + HitUTYpos_0**2)**0.5/10','HitUTZpos_0/10 >{} && HitUTZpos_0/10 <{}'.format(minz,maxz))
        elif detector == "MIGHTY":
            tree.Project (h2.GetName() , '(HitXpos_0**2 + HitYpos_0**2)**0.5/10','HitZpos_0/10 >{} && HitZpos_0/10 <{}'.format(minz,maxz))
        len_r_bin = (maxr-minr)/nb_bin_r
        f_radial = ROOT.TF1("f_radial", f"1/({eventNumber} *({np.pi}*(x+{len_r_bin})**2 - {np.pi}*x**2))", minr, maxr)
        h2.Multiply(f_radial)
        h2.SetXTitle("r [cm]")
        h2.SetYTitle("Hits / cm^2 / event")
        h2.Draw()
        h2.SetStats(0)
        ROOT.gPad.SetLogy(1)
        c2.Modified()
        c2.Update()
        c2.Print("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + "hist" + ".png")


        #subplot 3 - heatmap (TH2) of position in x and y - keep minz < z < maxz (first layer of detector) && r > minz
        c3 = ROOT.TCanvas("c3","", int(maxx-minx)*5, int(maxy-miny)*5)
        h3 = ROOT.TH2F('h3','Occupancy',nb_bin_x, minx, maxx,nb_bin_y, miny, maxy)

        if detector == "UT":
            tree.Project ( h3.GetName() , '(HitUTXpos_0/10):(HitUTYpos_0/10)','HitUTZpos_0/10>{} && HitUTZpos_0/10<{} && (HitUTXpos_0/10)**2 + (HitUTYpos_0/10)**2 > {}**2'.format(minz,maxz,minr))
        elif detector == "MIGHTY":
            tree.Project ( h3.GetName() , '(HitXpos_0/10):(HitYpos_0/10)','HitZpos_0/10>{} && HitZpos_0/10<{} && (HitXpos_0/10)**2 + (HitYpos_0/10)**2 > {}**2'.format(minz,maxz, minr))
        xaxis = h3.GetXaxis()
        yaxis = h3.GetYaxis()
        h3.Scale(event_rate)
        h3.Scale(1/(xaxis.GetBinWidth(1)*yaxis.GetBinWidth(1)*eventNumber))
        h3.SetXTitle("X [cm]")
        h3.SetYTitle("Y [cm]")
        h3.SetZTitle("Hits / cm^2 / second")
        zaxis = h3.GetZaxis()
        zaxis.SetTitleOffset(1.2)
        h3.SetStats(0)
        ROOT.gStyle.SetPalette(1)
        c3.SetRightMargin(0.17)
        h3.Draw('COLZ')
        ROOT.gPad.SetLogz(1)
        palette = h.GetListOfFunctions().FindObject("palette")
        c3.Modified()
        c3.Update()
        c3.Print("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + "occupancy_by_second" + ".png")


        #subplot 4 - histogram (TH1) of number of hits for a given radius r - keep 0 < z < 2370 (first layer of detector)
        c4 = ROOT.TCanvas("c4","")
        h4 = ROOT.TH1F('h4','Distribution of hits in r',nb_bin_r,minr,maxr)
        if detector == "UT":
            tree.Project (h4.GetName() , '(HitUTXpos_0**2 + HitUTYpos_0**2)**0.5/10','HitUTZpos_0/10 >{} && HitUTZpos_0/10 <{}'.format(minz,maxz))
        elif detector == "MIGHTY":
            tree.Project (h4.GetName() , '(HitXpos_0**2 + HitYpos_0**2)**0.5/10','HitZpos_0/10 >{} && HitZpos_0/10 <{}'.format(minz,maxz))
        len_r_bin = (maxr-minr)/nb_bin_r
        f_radial = ROOT.TF1("f_radial", f"{event_rate}/({eventNumber} *({np.pi}*(x+{len_r_bin})**2 - {np.pi}*x**2))", minr, maxr)
        h4.Multiply(f_radial)
        h4.SetXTitle("r [cm]")
        h4.SetYTitle("Hits / cm^2 / second")
        h4.Draw()
        h4.SetStats(0)
        ROOT.gPad.SetLogy(1)
        c4.Modified()
        c4.Update()
        c4.Print("../../Pictures/" + cfg_detector_name + "/" + cfg_experiment_name + "/" + "hist_by_second" + ".png")

    if plot_geometry:
        if detector == "MIGHTY":
            UTGeometry.draw_detector_configuration_mighty(det, cfg_detector_name, cfg_detector.get("mask_dead_column"))
        elif detector == "UT":
            UTGeometry.draw_detector_configuration_UT(det, cfg_detector_name)



###############################################################################
# main reads the argiment and call the different previous function to create
# the wanted health books
def main():
    parser = argparse.ArgumentParser(formatter_class = argparse.RawTextHelpFormatter)
    parser.add_argument("-d", "--detector", required = True, type = str,
        default = "UT",
        help = "chosen detector 'UT' or 'MIGHTY'")    
    parser.add_argument("-mc","--MC_tracks", required = False, type = str,
        help = "path to the chosen root file containing the MC tracks. example : ../MCtracks-pptest-5000.root")
    parser.add_argument("-cd", "--config_detector", required = True, type = str,
        help = "title of the chosen config file for the detector that is in Configs/")
    parser.add_argument("-ce", "--config_experiment", required = False, type = str,
        help = "title of the chosen config file for the experiment that is in Configs/")
    parser.add_argument("--mc_plots", action = "store_true", default = False,
        help = "put to plot infos about the MC input - will create plot about the occupancy at the level of the detector")
    parser.add_argument("--hit_plots", action = "store_true", default = False,
        help = "put to plot the results of the hits in the detector - will create the map of datarate per chip, histograms about the hits, and the number of hit per stave")
    parser.add_argument("--geometry_plots",  action = "store_true", default = False,
        help = "put to plot the geometry of the detector")
    parser.add_argument("--all_plots",  action = "store_true", default = False,
        help = "put to plot all the plots mentioned before")

    args = parser.parse_args()
    
    mc_plots = args.mc_plots
    hit_plots = args.hit_plots
    geometry_plots = args.geometry_plots
    
    if args.all_plots:
        mc_plots = True
        hit_plots = True
        geometry_plots = True

    if mc_plots or hit_plots:
        if args.config_experiment == None or args.MC_tracks == None:
            print("Impossible to create the required plot without MC Tracks and config_experiment")
            return

    operations(detector = args.detector, mc_tracks = args.MC_tracks,
               cfg_detector_name = args.config_detector, cfg_experiment_name = args.config_experiment,
               plot_mc = mc_plots, plot_hits = hit_plots, plot_geometry = geometry_plots)


if __name__ == "__main__":
    main()
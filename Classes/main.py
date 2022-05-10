import ROOT
import UTGeometry
import ClassParticule
import ClassConfigExperiment
import ClassConfigDetector
import numpy as np
import matplotlib.pyplot as plt
import os

folder = os.getcwd().replace('\\','/')[:-8]

################################ CONSTANT #####################################

f = ROOT.TFile(folder + "/MCtracks-pptest-5000.root")
d = f.Get("MCParticleNTuple")
tree = d.Tracks 

name_hist_chip = "hist_chip"
name_hist_module = "hist_module"
name_plot_stave = "hit_on_stave"

config_detector = "config_detector2"
config_experiment = "config_experiment_pp"


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
  cfg_detector = ClassConfigDetector.Config(folder + "/Configs/" + config_detector + ".txt")
  
   #creation of the config object for the experiment
  print("\n \n Creation of the config object for the experiment \n \n")
  cfg_exp = ClassConfigExperiment.Config(folder + "/Configs/" + config_experiment + ".txt")
  
  #creation of the detector object
  print("\n \n Creation of the detector object \n \n")
  det = UTGeometry.Detector(cfg_detector)
  
  #creation of the particle object
  print("\n \n Creation of the particule object \n \n")
  particles = ClassParticule.Particule(tree, cfg_exp, cfg_detector)

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

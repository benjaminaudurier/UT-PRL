import ROOT
import UTGeometry
import ClassParticule
import ClassConfigExperiment
import ClassConfigDetector
import pickle
import numpy as np
import matplotlib.pyplot as plt

############### FUNCTIONS ###################

###############
# save_object takes an object and a filename and save it in Files/ with filename.pickle
def save_object(obj,filename):
  try:
    with open("/grid_mnt/data__DATA/data.lhcb/PRL/Files/"+filename+".pickle", "wb") as f:
      pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)
      

###############
# load_object takes a filename, search for Files/filename.pickle and return the object if it exists
def load_object(filename):
  try:
    with open("/grid_mnt/data__DATA/data.lhcb/PRL/Files/"+filename+".pickle", "rb") as f:
      return pickle.load(f)
  except Exception as ex:
    print("Error during pickling object (Possibly unsupported):", ex)
   



############### CONSTANT ###################

f = ROOT.TFile("/data/DATA/data.lhcb/audurier/MCtracks-PbPbtest-100_1.root")
d = f.get("MCParticleNTuple")
tree = d.Tracks 


name_hist_chip = "hist_chip"
name_hist_module = "hist_module"
name_plot_stave = "hit_on_stave"



############### MACRO ###################
# main reads the config files, create the config objects
# it creates a detector from the config_detector object
# then, it reads the tree and create an object particle from the tree


if __name__ == '__main__':

  #creation of the config object for the detector
  print("\n \n Creation of the config object for the detector \n \n")
  cfg_detector = ClassConfigDetector.Config("/grid_mnt/data__DATA/data.lhcb/PRL/Configs/config_detector1.txt")
  
   #creation of the config object for the experiment
  print("\n \n Creation of the config object for the experiment \n \n")
  cfg_exp = ClassConfigExperiment.Config("/grid_mnt/data__DATA/data.lhcb/PRL/Configs/config_experiment.txt")
  
  #creation of the detector object
  print("\n \n Creation of the detector object \n \n")
  det = UTGeometry.Detector(cfg_detector)
  
  #creation of the particle object
  print("\n \n Creation of the particule object \n \n")
  particule = ClassParticule.Particule(tree, cfg_exp, cfg_detector)
  
  #creation of the results array
  print("\n \n Creation of the results array \n \n")
  copy_part = [[a for a in particule._list_x],[a for a in particule._list_y]]
  res = UTGeometry.hit_parts_precision(det, copy_part, precision = 3)
  
  #we have to normalize by number of event
  res_nb_event = np.array(res)/float(particule._number_of_event)
  
  #we create a matrix called datarate of the same size than res, containing the datarate by chip  
  event_rate = cfg_exp.get("bx_rate")*10**(6) * cfg_exp.get("mu_factor")*10**(-3)
  nb_bit_by_hit = cfg_exp.get("nb_of_bit_BX_id") + int(np.log(cfg_detector.get("nb_lign_pxl_chp"))/np.log(2)) + int(np.log(cfg_detector.get("nb_coln_pxl_chp"))/np.log(2))
  
  #calculation of the data rate
  data_rate = res_nb_event * nb_bit_by_hit * event_rate
  
  #drawing of the results
  print("\n \n Drawing of the results \n \n")
  UTGeometry.draw_detector(det, res = res)
  
  #plotting of the figures
  print("\n \n Final drawing \n \n")
  res = load_object("res_nb_event1")
  res = np.array(res)
  res_flatten = res.flatten()
  
  plt.figure()
  plt.ylabel("Number of chips")
  plt.xlabel("Number of hits / Number of events")
  plt.yscale('log')
  y, bin_edges = np.histogram(res_flatten, bins=30)
  bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
  plt.bar(bin_centers, y,width = 0.3, yerr = y**0.5)
  plt.ylim(1,400)
  plt.savefig("../Pictures/" + name_hist_chip + ".png")
  
  
  plt.figure()
  plt.ylabel("Number of modules")
  plt.xlabel("Number of hits / Number of events")
  plt.yscale('log')
  res_module_flatten = np.sum(np.array(res),axis=(4,5)).flatten()
  y, bin_edges = np.histogram(res_module_flatten, bins=15)
  bin_centers = 0.5*(bin_edges[1:] + bin_edges[:-1])
  plt.bar(bin_centers, y,width = 2.4, yerr = y**0.5)
  plt.ylim(1,100)
  plt.savefig("../Pictures/" + name_hist_module +".png")
  
  
  
  plt.figure()
  res_stave = np.sum(np.array(res),axis=(0,2,3,4,5))
  plt.plot(np.arange(len(res_stave)),res_stave, 'x')
  plt.xlabel("Stave number")
  plt.ylabel("Number of hits / Number of events")
  plt.savefig("../Pictures/" + name_plot_stave + ".png")

  
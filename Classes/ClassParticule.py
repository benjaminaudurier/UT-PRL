from __future__ import print_function
import ROOT
import numpy as np


# the class Particule converts a tree of data in three lists containing the 
# x position, y position, and event number for each particle when they hit the detector
class Particule:

  def __init__(self, tree, cfg_sz, cfg_detector):
    list_x = []
    list_y = []
    list_eventNumber = []
    
    min_z = cfg_sz.get("min_z")
    max_z = cfg_sz.get("max_z")
    compteur = 0
    
    # data for the center module which will be dead to let pass the paritcles beam
    # we convert the wth_mdl from micrometer to millimeter to be adapted to the data contained in tree
    wth_mdl = cfg_detector.get("wth_mdl")*10**-3
    hgt_mdl = cfg_detector.get("hgt_mdl")*10**-3
    count_particle_hitting_central_zone = 0
    
    
    tab_result = [[],[], []]
    
    number_of_event = 0
    eventnumber = 0
    
    
    # we try if the config_sz file has the FThits characteristics
    try:
      #if it does :
      min_FTHit = cfg_sz.get("min_FTHit")
      max_FTHit = cfg_sz.get("max_FTHit")
      print("The config_study_zone file does the FTHit characteristics")
      
      for entry in tree: #we iterate on every leaf in the tree
        if entry.nFThits > min_FTHit and entry.nFThits < max_FTHit and entry.HitUTZpos_0/10 > min_z and entry.HitUTZpos_0/10 < max_z:
          
          if entry.HitUTXpos_0 < wth_mdl/2 and entry.HitUTXpos_0 > -wth_mdl/2 and entry.HitUTYpos_0 < hgt_mdl/2 and entry.HitUTYpos_0 > -hgt_mdl/2:
            #if the particle hits the central zone, it is dissmissed
            count_particle_hitting_central_zone += 1
            
          else:
            #if it hits elsewhere, its coordinates are added to the list of coordinates to study
            tab_result[0].append(entry.HitUTXpos_0*10e2)
            tab_result[1].append(entry.HitUTYpos_0*10e2)
            
            if entry.eventNumber != eventnumber: #these three lines of code count the number of events present in the experiment
              eventnumber = entry.eventNumber
              number_of_event += 1
            
            compteur+=1
            print("particle n {}".format(compteur) + " treated", end = '\r')
      
    except KeyError:
      print("The config file does not contain the FTHit characteristics")
      for entry in tree:#we iterate on every leaf in the tree
        if entry.HitUTZpos_0/10 > min_z and entry.HitUTZpos_0/10 < max_z:
        
          if entry.HitUTXpos_0 < wth_mdl/2 and entry.HitUTXpos_0 > -wth_mdl/2 and entry.HitUTYpos_0 < hgt_mdl/2 and entry.HitUTYpos_0 > -hgt_mdl/2:
            #if the particle hits the central zone, it is dissmissed
            count_particle_hitting_central_zone += 1
            
          else:
            #if it hits elsewhere, its coordinates are added to the list of coordinates to study
            tab_result[0].append(entry.HitUTXpos_0*10e2)
            tab_result[1].append(entry.HitUTYpos_0*10e2)
            tab_result[2].append(entry.eventNumber)
            
            if entry.eventNumber != eventnumber:#these three lines of code count the number of events present in the experiment
              eventnumber = entry.eventNumber
              number_of_event += 1
            
            compteur+=1
            print("particle n {}".format(compteur) + " treated", end = '\r')

    
    tab_result = np.array(tab_result)
    tab_result = np.array(sorted(tab_result,key = lambda x:x[0]))
    n = len(tab_result[0])
    parts = [[tab_result[0][i],tab_result[1][i],tab_result[2][i]] for i in range(n)]
    parts = np.array(parts)
    parts = np.array(sorted(parts,key = lambda x:x[0]))
    
    
    self._list_x = list(parts[:,0])
    self._list_y = list(parts[:,1])
    self._number_of_event = number_of_event
    self._count_particle_hitting_central_zone = count_particle_hitting_central_zone
    
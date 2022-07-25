###############################################################################
# the class Particle converts a tree of data in three lists containing the 
# x position, y position, and event number for each particle when they hit the detector
###############################################################################

from __future__ import print_function

from matplotlib.pyplot import table
import numpy as np
from tqdm import tqdm

###############################################################################
class Particle:

    def __init__(self, tree, cfg_exp, cfg_detector, detector = "UT"):

        min_z = cfg_exp.get("min_z")
        max_z = cfg_exp.get("max_z")
        compteur = 0
    
        count_particle_hitting_central_zone = 0
    
    
        tab_result = [[],[], []]
    
        number_of_event = 0
        eventnumber = 0
    
    
        # we try if the config_ file has the FThits characteristicsto know on what to filter
        try:
            min_FTHit = cfg_exp.get("min_FTHit")
            max_FTHit = cfg_exp.get("max_FTHit")
            contain_FT_hit = True
            print("The config_study_zone file does contain the FTHit characteristics \n")
        except KeyError:
            contain_FT_hit = False
            print("The config file does not contain the FTHit characteristics \n")

        for entry in tqdm(tree):

            # for each different configuration, we have to know on what characteristic we have to filter
            # entry_is_in_range represents that boolean stating that this entry is useful for the study or not
            if detector == "UT":
                if contain_FT_hit:
                    entry_is_in_range = entry.nFThits > min_FTHit and entry.nFThits < max_FTHit and entry.HitUTZpos_0/10 > min_z and entry.HitUTZpos_0/10 < max_z
                else:
                    entry_is_in_range = entry.HitUTZpos_0/10 > min_z and entry.HitUTZpos_0/10 < max_z
            elif detector == "MIGHTY":
                if contain_FT_hit:
                    entry_is_in_range = entry.nFThits > min_FTHit and entry.nFThits < max_FTHit and entry.HitZpos_0/10 > min_z and entry.HitZpos_0/10 < max_z
                else:
                    entry_is_in_range = entry.HitZpos_0/10 > min_z and entry.HitZpos_0/10 < max_z

            # if entry is in range, it is added to the list of interesting particles
            if entry_is_in_range:
                if detector == "UT":
                    tab_result[0].append(entry.HitUTXpos_0*10e2)
                    tab_result[1].append(entry.HitUTYpos_0*10e2)
                    tab_result[2].append(entry.eventNumber)
                if detector == "MIGHTY":
                    tab_result[0].append(entry.HitXpos_0*10e2)
                    tab_result[1].append(entry.HitYpos_0*10e2)
                    tab_result[2].append(entry.eventNumber)

                if entry.eventNumber != eventnumber: #these three lines of code count the number of events present in the experiment
                    eventnumber = entry.eventNumber
                    number_of_event += 1
            
                compteur+=1

    
        tab_result = np.array(tab_result)
        n = len(tab_result[0])
        parts = [[tab_result[0][i],tab_result[1][i],tab_result[2][i]] for i in range(n)]
        parts = np.array(parts)
        parts = np.array(sorted(parts,key = lambda x:x[0]))

        self._list_x = list(parts[:,0])
        self._list_y = list(parts[:,1])
        self._number_of_event = number_of_event
        self._count_particle_hitting_central_zone = count_particle_hitting_central_zone
    
    

from matplotlib.colors import is_color_like
import ROOT
import UTGeometry
import ClassParticle
import ClassConfigExperiment
import ClassConfigDetector
import numpy as np
import matplotlib.pyplot as plt
import os
import save_load

from matplotlib.colors import LogNorm

folder = os.path.dirname(os.getcwd()).replace("\\","/") + "/"

################################ CONSTANT #####################################
f = ROOT.TFile(folder + "../MCtracks-pptest-5000.root")
#f = ROOT.TFile(folder + "/MCtracks-PbPbcentral.root")
d = f.Get("MCParticleNTuple")
tree = d.Tracks 

config_experiment = "config_experiment_pp"
#config_experiment = "config_experiment_PbPb"

formats_pxl = ["0","1","2"]
row_numbers = ["128","143","256","512","1024"]
coln_numbers = ["128","256","404","512","1024"]

# give the size of thewindow we're interested with in um
# (the window is a rectangle around the center point
# where the hottest chip is expected to be)
window_wth = 50e4
window_hgt = 50e4

beam_wth = 6e4 # in um
beam_hgt = 6e4

# Higher than vmax, the data rate will appear in black
vmin = 0
vmax = 12 # Gbit/s 

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
                            if (chp._x_pos + wth_chp > -wth_beam/2 and chp._y_pos + hgt_chp > -hgt_beam/2 and chp._x_pos + wth_chp < wth_beam/2 and chp._y_pos + hgt_chp < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
                            elif (chp._x_pos + wth_chp > -wth_beam/2 and chp._y_pos > -hgt_beam/2 and chp._x_pos + wth_chp < wth_beam/2 and chp._y_pos < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
                            elif (chp._x_pos > -wth_beam/2 and chp._y_pos + hgt_chp > -hgt_beam/2 and chp._x_pos < wth_beam/2 and chp._y_pos + hgt_chp < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
                            elif (chp._x_pos > -wth_beam/2 and chp._y_pos > -hgt_beam/2 and chp._x_pos  < wth_beam/2 and chp._y_pos < hgt_beam/2):
                                res[i_stv][j_stv][i_mdl][j_mdl][i_chp][j_chp] = 0
    return res



def generate_config_file(format_pxl, nb_row_pxl, nb_coln_pxl):
    title = format_pxl + "_" + nb_row_pxl + "_" + nb_coln_pxl
    
    w,h = 0,0

    if (format_pxl=="0"):
      w=30
      h=30
    elif (format_pxl=="1"):
      w=50
      h=150
    elif (format_pxl=="2"):
      w=50
      h=300

    wth_chp = w * int(nb_coln_pxl)
    hgt_chp = h * int(nb_row_pxl)

    nb_row_chp = int(1.5*beam_hgt) // hgt_chp + 5
    nb_coln_chp = int(1.5*beam_wth) // wth_chp + 5

    
    with open(folder + 'Configs/hottest_chip/' + title + ".txt", 'w') as f:
        f.write("Configuration of the detector \n" + 
                "## This file allows the configuration of the detector\n" + 
                "## It allows to set the following characteristics\n" + 
                "#\n" + 
                "# Pixel format (0 = 30*30 - 1=50*150 - 2=50*300)\n" + 
                f"frmt_pxl:{format_pxl}\n" + 
                "#\n" + 
                "# Spacing between pixels (x and y in um)\n" + 
                "spcng_pxl_x:0\n" + 
                "spcng_pxl_y:0\n" + 
                "#\n" + 
                "# Nb of row/colon of pixel in a chip\n" + 
                f"nb_row_pxl_chp:{nb_row_pxl}\n" + 
                f"nb_coln_pxl_chp:{nb_coln_pxl}\n" + 
                "#\n" + 
                "# Dead zone of the chip in um\n" + 
                "dead_zone_chp_left:50\n" + 
                "dead_zone_chp_right:50\n" + 
                "dead_zone_chp_bottom:50\n" + 
                "dead_zone_chp_top:50\n" + 
                "#\n" + 
                "# Spacing between chips (x and y in um)\n" + 
                "spcng_chp_x:150\n" + 
                "spcng_chp_y:150\n" + 
                "#\n" + 
                "# Nb of row/colon of chip in a module\n" + 
                f"nb_row_chp_mdl:{nb_row_chp}\n" + 
                f"nb_coln_chp_mdl:{nb_coln_chp}\n" +
                "mask_dead_column:" + "1"*nb_coln_chp +"\n" +
                "#\n" + 
                "# Spacing between modules (x and y in um)\n" + 
                "spcng_mdl_x:300\n" + 
                "spcng_mdl_y:300\n" + 
                "#\n" + 
                "# Nb of row/colon of module in a stave\n" + 
                "nb_row_mdl_stv:1\n" + 
                "nb_coln_mdl_stv:1\n" + 
                "#\n" + 
                "# Spacing between staves (x and y in um)\n" + 
                "spcng_stv_x:100\n" + 
                "spcng_stv_y:100\n" + 
                "#\n" + 
                "# Nb of row/colon of stave\n" + 
                "nb_row_stv:1\n" + 
                "nb_coln_stv:1\n" )

################################## MACRO ######################################
# main reads the config files, create the config objects
# it creates a detector from the config_detector object
# then, it reads the tree and create an object particle from the tree


if __name__ == '__main__':
    fig, axs = plt.subplots(1, len(formats_pxl), figsize=(28,12))

    fig.suptitle(f'Data rate [Gbit/s] of the hottest chip for different configuration of detectors', fontsize = 20)    
    #creation of the config object for the experiment
    cfg_exp = ClassConfigExperiment.Config(folder + "Configs/" + config_experiment + ".txt")

    count = 1   

    for i_format_pxl in range(len(formats_pxl)):
        ax = axs[i_format_pxl]
        format_pxl = formats_pxl[i_format_pxl]

        tab = np.zeros((len(row_numbers),len(coln_numbers)))

        for i_row_number in range(len(row_numbers)):
            for i_coln_number in range(len(coln_numbers)):

                row_number = row_numbers[i_row_number]
                coln_number = coln_numbers[i_coln_number]

                config_detector = format_pxl + "_" + row_number + "_" + coln_number
                print(config_detector)

                if not os.path.exists(folder + "Configs/hottest_chip/" + config_detector + ".txt"):
                    generate_config_file(format_pxl,row_number,coln_number)

                #creation of the config object for the detector
                cfg_detector = ClassConfigDetector.Config(folder + "Configs/hottest_chip/" + config_detector + ".txt")
  
                #creation of the detector object
                det = UTGeometry.Detector(cfg_detector)

                particles = ClassParticle.Particle(tree, cfg_exp, cfg_detector)

                copy_part = [[],[]]
                for x,y in zip(particles._list_x,particles._list_y):
                    if -window_wth/2<x and x<window_wth/2 and -window_hgt/2<y and y<window_hgt/2:
                        copy_part[0].append(x)
                        copy_part[1].append(y)

                #creation of the results array
                total_number = len(formats_pxl)*len(row_numbers)*len(coln_numbers)
                print("\n \n Creation of the result array " + str(count) + f"/{total_number} \n \n")
                

                res, count_missed_part = UTGeometry.hit_parts_precision(det, copy_part, precision = 3)
                res = np.array(res)

                res = exclude_beam(res, det, beam_wth, beam_hgt)
    
                res_nb_event = res/float(particles._number_of_event)
    
                #we create a matrix called datarate of the same size than res, containing the datarate by chip  
                event_rate = cfg_exp.get("event_rate")*10**(3) 
                nb_bit_by_hit = cfg_exp.get("nb_of_bit_BX_id") + int(np.log(cfg_detector.get("nb_row_pxl_chp"))/np.log(2)) + int(np.log(cfg_detector.get("nb_coln_pxl_chp"))/np.log(2))


                #calculation of the data rate
                data_rate = res_nb_event * nb_bit_by_hit * event_rate * 10**-9
    
                hottest_chip = np.max(data_rate)



                tab[i_row_number,i_coln_number] = hottest_chip
                count += 1

                area_chip = cfg_detector.get("wth_chp")*cfg_detector.get("hgt_chp") * 10**-8 # convert from um2 to cm2
                ax.text(i_coln_number + 0.5, i_row_number + 0.5, str(round(area_chip,2)) + u" cm\u00b2" + "\n" + str(round(hottest_chip,2)), ha='center', va='center',  transform=ax.transData, fontsize = 13, color='gray')

        n = len(coln_numbers)
        ax.set_xticks(ticks = np.arange(0.5,n+0.5))
        ax.set_xticklabels(coln_numbers)
        ax.set_xlabel("Columns of pixel in chip")

        n = len(row_numbers)
        ax.set_yticks(ticks = np.arange(0.5,n+0.5))
        ax.set_yticklabels(row_numbers)
        ax.set_ylabel("Rows of pixel in chip")

        if format_pxl == "0":
            ax.set_title(u'Pixel size (30 \u03bcm x 30 \u03bcm)', fontsize = 15)
        elif format_pxl == "1":
            ax.set_title(u'Pixel size (50 \u03bcm x 150 \u03bcm)', fontsize = 15)
        elif format_pxl == "2":
            ax.set_title(u'Pixel size (50 \u03bcm x 300 \u03bcm)', fontsize = 15)

        ax.pcolor(tab, cmap="hot_r", vmin = vmin, vmax = vmax)
        
    pcm = ax.pcolormesh(tab,cmap = "hot_r", vmin = vmin, vmax = vmax)

    save_load.save(tab, "tab_hottest_chip_UT")

    fig.colorbar(pcm, ax = axs.ravel().tolist())
    plt.savefig("../../Pictures/" + "hottest_chip_map" + ".png")
    plt.close()
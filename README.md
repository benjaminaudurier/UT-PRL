# UT Datarate calculation (Python) 12/05/2022

Python 3.8.8
Project to study the future UT design.


## NEEDED
 - PyROOT, numpy, matplotlib, os, tqdm

## DESCRIPTION
The goal of the code is to simulate the datarate of the detector for
different given configurations of the UT.
We have inputs characterising the detector and the particles for whom
we want to test the detector, and it gives us in output a map of the 
datarate by chips, histograms of the distribution of pixel/chip by 
number of hit, and a plot and the number of hit/number of stave.

## HOW TO USE
- write a config file for the geometry detector, using as a canva an existing one;
- write a config file for the global experimental conditions, using as a canva an existing one;
- download a ROOT.TTree giving the results of a MonteCarlo simulation
- run `main.py`, which has several arguments :
  - `--detector` stands for 'MIGHTY' or 'UT'
  - `--MC_tracks` is the path of the root file containing the MC tracks (../../MCtracks-pptest-5000.root for example)
  - `--config_detector` is the title of the config file for the geometry of the detector. The config file should be in Config/
  - `--config_experiment` is the title of the text config file for the experimental conditions. The config file should be in Config/
  - `--mc_plots` allows plotting information about the MC_tracks input is wanted
  - `--hit_plots` allows plotting information about the hit of the tracks in the detector is wanted
  - `--geometry_plots` allows plotting information about the geometry of the detector
  - `--all_plots` allows plotting all previous plots
- the plots are stored in the Pictures/ folder created

### Examples :
- `python main.py --detector UT --MC_tracks ../../MCtracks-PbPbcentral.root --config_detector cfg_detector_ut1 --config_experiment config_experiment_PbPb_ut --all_plots` will create all the plots for a PbPb simulation and for the detector describe in config_detector1.txt
- `python main.py --detector MIGHTY --config_detector cfg_detector_mighty1 --geometry_plots will create the geometry plots for the detector describe in config_detector_mighty1.txt
- `python main.py --detector MIGHTY --MC_tracks ../../MCtracks-pptest-5000.root --config_detector cfg_detector_mighty3 --config_experiment config_experiment_pp_mighty --mc_plots --hit_plots` will create all the plots but the ones concerning the geometry for a pp simulation and for the detector describe in config_detector_mighty3.txt

## HOTTEST CHIPS SEVERAL GEOMETRIES

The project also allows creating a plot gathering the data rates of the hottest chips for different geometries.
The inputs of `compare_configs.py` script are in the header of the scripts. They are :
- a ROOT file containing a tree containing the results of a MC simulation
- the name of a config file for experiment
- lists allowing defining different chip geometries (format pxl + nb pxl)
- size of the window where the hottest chip should be
- size of the beam
- vmin and vmax for the data rate in order to define the scale of the colormap
To create a map, change the inputs of the file and launch `compare_configs.py`. Theplot will be saved in the Pictures folder.
This feature of the code is available only for UT detector.


## INPUTS
In input of this program, we have 
  - a ROOT.TTree file containing a simulation of particles by MonteCarlo
    that wil be used to artificially hit our detector
  - a config_detector file where we write the configuration we want for 
    the detector (size of pixel, number of pixel...)
  - a config_experiment file where we put some values for the experiment
    It gives some values to exclude some particles for the tree and some
    numerical values to calculate the datarate 

## CLASSES
  - ClassConfigDetector takes the config_detector file and gives an object
    containing all the elements from the config_detector
  - ClassConfigExperiment does the same for config_experiment
  - ClassParticule takes the particle TTree and gives an object 
    containing everything from the TTree, deleting the traces from 
    ConfigExperiment
  - UTGeometry constructs the detector from the preceding Classes, and 
    the functions where the particles hit the detector
  - main regroups all the different classes and construct the plots
  - compare_configs creates a list of config files and ses them to compare several geometries

## FOLDERS
  - Classes contains all the different classes
  - Configs contains the config files
  - Pictures will contain the generated pictures, if it doesn't exist, it will be created by the code





_______________
Yorgos Chatziantoniou
Arnaud Lafay
Pierre Olleon

Ecole polytechnique

# UT Datarate calculation (Python) 14/04/2022

Project to study the future UT design.

_______________
NEEDED
ROOT, numpy, matplotlib, os, tqdm

_______________
HOW TO USE
- change the configs files to make the tests you wanty
- put a MonteCarlo particle tree in the folder containing Classes, Configs...
- make sure the name in the constant section of main.py corresponds to the wanted config files
- go to the Classes folder
- run main.py
- the Pictures are stored in the Pictures folder created


_______________
DESCRIPTION
The goal of the code is to simulate the datarate of the detector for
different given configurations of the UT.
We have inputs characterising the detector and the particles for whom
we want to test the detector, and it gives us in output a map of the 
datarate by chips, histograms of the distribution of pixel/chip by 
number of hit, and a plot and the number of hit/number of stave


_______________
INPUTS
In input of this program, we have 
  - a ROOT.TTree file containing a simulation of particles by MonteCarlo
    that wil be used to artificially hit our detector
  - a config_detector file where we write the configuration we want for 
    the detector (size of pixel, number of pixel...)
  - a config_experiment file where we put some values for the experiment
    It gives some values to exclude some particles for the tree and some
    numerical values to calculate the datarate 


_______________
CLASSES
  - ClassConfigDetector takes the config_detector file and gives an object
    containing all the elements from the config_detector
  - ClassConfigExperiment does the same for config_experiment
  - ClassParticule takes the particle TTree and gives an object 
    containing everything from the TTree, deleting the traces from 
    ConfigExperiment
  - UTGeometry constructs the detector from the preceding Classes, and 
    the functions where the particles hit the detector
  - main regroups all the different classes and construct the plots
  
_______________
FOLDERS
  - Classes contains all the different classes
  - Configs contains the config files
  - Pictures will contain the generated pictures, if it doesn't exist, it will be created by the code






Yorgos Chatziantoniou
Arnaud Lafay
Pierre Olleon

Ecole polytechnique

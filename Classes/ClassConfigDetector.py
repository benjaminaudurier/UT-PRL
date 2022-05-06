###############################################################################
#creates the config objects, whose attributes caracterize the detector and the 
# simulated experiment (study zone, pixel size, amount of pixels per chip...)
#the format of the config file has to be the same as that of 
# "/grid_mnt/data__DATA/data.lhcb/PRL/Configs/config_detector.txt"
###############################################################################

class Config : 
  def __init__(self, cfgfile = ""):
    self._cfgfile = cfgfile
    self._dict = {} #Contains the keys and their values
    self._is_cfg_study_zone = False
    self._is_cfg_detector = True
    self.creation_config()
    self._fichier = None
    self._lines = [[]]
    self._keys = ["frmt_pxl",'spcng_pxl_x','spcng_pxl_y','nb_line_pxl_chp','nb_coln_pxl_chp','dead_zone_chp_left','dead_zone_chp_right','dead_zone_chp_bottom','dead_zone_chp_top','spcng_chp_x','spcng_chp_y','nb_line_chp_mdl','nb_coln_chp_mdl','spcng_mdl_x','spcng_mdl_y','nb_line_mdl_stv','nb_coln_mdl_stv','spcng_stv_x','spcng_stv_y', 'nb_line_stv','nb_coln_stv','dead_zone_center_x','dead_zone_center_y']
   
  #############################################################################
  def ouverture(self):
   #Checks that cfgfile is a text file, returns the opened file
    fichier = None
    try:
      fichier = open(self._cfgfile,"r")
    except:
      print("!!! The file provided is not a .txt file present in the current directory !!!")
    self._fichier = fichier
    
    
  #############################################################################
  def text_to_list(self):
    #intakes an opened .txt file, deletes the unnecessary lines, returns a list [("information type", "value")]
    #we remove the commentary lines - each line that starts with a # is a commentary
    try:
      lines = self._fichier.readlines()

    except: 
      print("ouverture(self) didnt return an opened .txt file")
    n = len(lines)
    lines_v2 = []
      
    for i in range(n):
      if lines[i][0] != "#":
        lines_v2.append(lines[i][:-1]) 

    n = len(lines_v2)
    #creation of the [("information type", "value")] list
    for i in range(n):
      lines_v2[i] = lines_v2[i].split(":")
    self._lines = lines_v2

    
  #############################################################################
  def verif_format(self):
    #checks the format of the config.txt file, returns error messages if it is not right
    keys = ["frmt_pxl",'spcng_pxl_x','spcng_pxl_y','nb_line_pxl_chp','nb_coln_pxl_chp','dead_zone_chp_left','dead_zone_chp_right','dead_zone_chp_bottom','dead_zone_chp_top','spcng_chp_x','spcng_chp_y','nb_line_chp_mdl','nb_coln_chp_mdl','spcng_mdl_x','spcng_mdl_y','nb_line_mdl_stv','nb_coln_mdl_stv','spcng_stv_x','spcng_stv_y', 'nb_line_stv','nb_coln_stv','dead_zone_center_x','dead_zone_center_y']
    lines = self._lines
    errorMessage = "The file does not correspond to a config file of the detector"
    bool = True
    try :
      assert lines[0][0] == "Configuration of the detector "
      print("Checking 1st line")
    except : 
      print(lines[0])
      print(errorMessage)
      print("Is it a config file of the detector?")
      bool = False
    for k in range(len(keys)): 
      try :
        assert lines[k+1][0] == keys[k]
        print("Verification "+keys[k])
      except :
        print(errorMessage)
        print("Check the format for  "+keys[k])
        bool = False
    return bool
    
  #############################################################################      
  def remplissage_dict_config_detector(self):
    #remplit les champs du dictionnaire
    #les champs peuvent etre laisses vides
    
    keys = ["frmt_pxl",'spcng_pxl_x','spcng_pxl_y','nb_line_pxl_chp','nb_coln_pxl_chp','dead_zone_chp_left','dead_zone_chp_right','dead_zone_chp_bottom','dead_zone_chp_top','spcng_chp_x','spcng_chp_y','nb_line_chp_mdl','nb_coln_chp_mdl','spcng_mdl_x','spcng_mdl_y','nb_line_mdl_stv','nb_coln_mdl_stv','spcng_stv_x','spcng_stv_y','nb_line_stv','nb_coln_stv','dead_zone_center_x','dead_zone_center_y']
    for k in range(len(keys)): #we fill the dictionary
      if self._lines[k+1][1] != "": #if the information is provided by the user
        self._dict[keys[k]] = int(self._lines[k+1][1])

    #We fill the width and height fields for every sub-ensemble of the detector
    w = 0
    h = 0
      
    if (self._dict["frmt_pxl"]==0):
      w=30
      h=30
    elif (self._dict["frmt_pxl"]==1):
      w=50
      h=150
    elif (self._dict["frmt_pxl"]==2):
      w=50
      h=300
    #width and height for chip
    self._dict["wth_chp"] = (w+self._dict["spcng_pxl_x"])*self._dict['nb_coln_pxl_chp'] - self._dict["spcng_pxl_x"] # n objects n-1 spaces between object
    self._dict["hgt_chp"] = (h+self._dict["spcng_pxl_y"])*self._dict['nb_line_pxl_chp'] - self._dict["spcng_pxl_y"] # n objects n-1 spaces between object
    #width and height for module
    self._dict["wth_mdl"] = (self._dict["wth_chp"]+self._dict["spcng_chp_x"]+ self._dict['dead_zone_chp_left'] + self._dict['dead_zone_chp_right'] )*self._dict['nb_coln_chp_mdl']  - self._dict["spcng_chp_x"] # n objects n-1 spaces between object
    self._dict["hgt_mdl"] = (self._dict["hgt_chp"]+self._dict["spcng_chp_y"] + self._dict['dead_zone_chp_top'] + self._dict['dead_zone_chp_bottom'])*self._dict['nb_line_chp_mdl'] - self._dict["spcng_chp_y"] # n objects n-1 spaces between object
    #width and height for stave
    self._dict["wth_stv"] = (self._dict["wth_mdl"]+self._dict["spcng_mdl_x"])*self._dict['nb_coln_mdl_stv'] - self._dict["spcng_mdl_x"] # n objects n-1 spaces between object
    self._dict["hgt_stv"] = (self._dict["hgt_mdl"]+self._dict["spcng_mdl_y"])*self._dict['nb_line_mdl_stv'] - self._dict["spcng_mdl_y"] # n objects n-1 spaces between object
    #width and height for detector
    self._dict["wth_det"] = (self._dict["wth_stv"]+self._dict["spcng_stv_x"])*self._dict['nb_coln_stv'] - self._dict["spcng_stv_x"] # n objects n-1 spaces between object
    self._dict["hgt_det"] = (self._dict["hgt_stv"]+self._dict["spcng_stv_y"])*self._dict['nb_line_stv'] - self._dict["spcng_stv_y"] # n objects n-1 spaces between object
    
    
  #############################################################################
  def creation_config(self):
    #Fills the dictionnary if the config.txt file had the right format
    self.ouverture()
    self.text_to_list()
    if self.verif_format():
      self.remplissage_dict_config_detector()
  
  #############################################################################      
  def get(self,arg):
    return self._dict[arg]

    
    
    

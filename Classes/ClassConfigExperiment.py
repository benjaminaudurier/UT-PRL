###############################################################################
#create the config object containing all the experimental data 
#the format of the config file must be that of 
# "/grid_mnt/data__DATA/data.lhcb/PRL/Configs/config_experiment.txt")
###############################################################################


###############################################################################
class Config : 
  def __init__(self, cfgfile = ""):
    self._cfgfile = cfgfile
    self._dict = {} #contains the keys and their values
    self._is_cfg_study_zone = True
    self._is_cfg_detector = False
    self._lines = [[]]
    self.creation_config()
    self._fichier = None
    self._keys = ["min_z","max_z","min_FTHit","max_FTHit","event_rate","nb_of_bit_BX_id"]
  
  #############################################################################
  def ouverture(self):
    #Verifies that cfgfile is a text file, returns the opened file
    fichier = None
    try:
      fichier = open(self._cfgfile,"r")
    except:
      print("#######ERROR#######")
      print("!!! The provided file is not in the current directory !!!")
    self._fichier = fichier
    
    
  #############################################################################
  def text_to_list(self):
    #takes an opened .txt file, removes the useless lines, returns a list [("info type", value)]
    #removes the commented lines in the entry; each line with a #is a commented line
    
    try:#checking that self is an open file
      lines = self._fichier.readlines()
    except: 
      print("#######ERROR#######")
      print("ouverture(self) did not return an open file")
    n = len(lines)
    lines_v2 = []
      
    for i in range(n):
      #turns the text file into a list
      if lines[i][0] != "#":
        lines_v2.append(lines[i][:-1]) 
            
    n = len(lines_v2)
    #creation of the [("info type", value)] list
    for i in range(n):
      lines_v2[i] = lines_v2[i].split(":")
    self._lines = lines_v2
    
    
  #############################################################################    
  def verif_format(self):
    #checks the format of config.txt, returns error messages if the format isn't right
    keys = ["min_z","max_z","min_FTHit","max_FTHit","event_rate","nb_of_bit_BX_id"]
    lines = self._lines
    errorMessage = "The file's format does not correspond to a configuration of the study zone file format"
    bool = True
    #checks if the file has the right format
    try :
      assert lines[0][0] == "Configuration of the study zone"
      print("Verification 1st line")
    except :
      print("#######ERROR#######") 
      print(errorMessage)
      print("Is it a study zone configuration file ?")
      bool = False
    for k in range(len(keys)): 
      try :
        assert lines[k+1][0] == keys[k]
        print("Verification "+keys[k])
      except :
        print("#######ERROR#######")
        print(errorMessage)
        print("Check the format for "+keys[k])
        bool = False
    return bool
   
  #############################################################################       
  def filling_dict_config_studyZone(self):
    #fills the dictionnary's fields
    #the fields can be left empty
    keys = ["min_z","max_z","min_FTHit","max_FTHit","event_rate","nb_of_bit_BX_id"]
    for k in range(len(keys)): #filling of the dictionnary
      if self._lines[k+1][1] != "": #if the info is provided
        self._dict[keys[k]] = int(self._lines[k+1][1])    
   
  #############################################################################
  def creation_config(self):
    #fills the dictionary if the format of the input is right
    self.ouverture()
    self.text_to_list()
    if self.verif_format():
      self.filling_dict_config_studyZone()
        
  #############################################################################
  def get(self,arg):
    return self._dict[arg]
      
    
    
    

    

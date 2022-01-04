class Config : 

  def __init__(self, cfgfile = ""):
    self._cfgfile = cfgfile
    try:
      self._file = open(cfgfile,"r")
    except:
      print("!!! Le fichier renseigne n'est pas un fichier texte present dans le repertoire actuel !!!")
    #on enleve les lignes avec des commentaires - chaque ligne commencant par # est un commentaire
    lines = self._file.readlines()
    n = len(lines)
    lines_v2 = []
    for i in range(n):
      if lines[i][0] != "#":
        lines_v2.append(lines[i][:-2])
    self._lines = lines_v2
    self._is_cfg_study_zone = False
    self._is_cfg_detector = False
      
    lines = self._lines
  
    if lines[0] == 'Configuration de la zone d etudes':    
      n = len(lines)
      for i in range(n):
        lines[i] = lines[i].split(":")
      
      #verification du format du fichier config.txt
      assert lines[1][0] == "min_z", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[2][0] == "max_z", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[3][0] == "min_t", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[4][0] == "max_t", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[5][0] == "min_FTHit", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[6][0] == "max_FTHit", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[7][0] == "obj", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[8][0] == "id", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
      assert lines[9][0] == "prec", "Le fichier correspondant ne correspond pas a un fichier config de la zone d etude"  
          
          
      #mise en caracteristique du fichier config des carac de la zone d'etude
      #les caracteres peuvent etre laisses vide
      if lines[1][1] != "":
        self._min_z = int(lines[1][1])
      if lines[2][1] != "":
        self._max_z = int(lines[2][1])
      if lines[3][1] != "":
        self._min_t = int(lines[3][1])
      if lines[4][1] != "":
        self._max_t = int(lines[4][1])
      if lines[5][1] != "":
        self._min_FTHit = int(lines[5][1])
      if lines[6][1] != "":
        self._max_FTHit = int(lines[6][1])
      if lines[7][1] != "":
        self._obj = int(lines[7][1])  
      if lines[8][1] != "":
        self._id = lines[8][1]
      if lines[9][1] != "":
        self._prec = int(lines[9][1])    
  
      # On met la caracteristique vraie pour savoir que la config est de type study_zone
      self._is_cfg_study_zone = True 
    
    
    
    
    elif lines[0] == 'Configuration du detecteur':
      n = len(lines)
      for i in range(n):
        lines[i] = lines[i].split(":")
      
      #verification du format du fichier config.txt
      assert lines[1][0] == "frmt_pxl", "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[2][0] ==  'spcng_pxl_x', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[3][0] == 'spcng_pxl_y', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[4][0] == 'nb_lign_pxl_chp', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[5][0] == 'nb_coln_pxl_chp', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[6][0] == 'zn_mrt_chp_gau', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[7][0] == 'zn_mrt_chp_dro', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[8][0] == 'zn_mrt_chp_bas', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[9][0] == 'zn_mrt_chp_hau', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[10][0] == 'spcng_chp_x', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[11][0] == 'spcng_chp_y', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[12][0] == 'nb_lign_chp_mdl', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[13][0] == 'nb_coln_chp_mdl', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[14][0] == 'spcng_mdl_x', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[15][0] == 'spcng_mdl_y', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[16][0] == 'nb_lign_mdl_stv', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[17][0] == 'nb_coln_mdl_stv', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"  
      assert lines[18][0] == 'spcng_stv_x', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[19][0] == 'spcng_stv_y', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[20][0] == 'nb_lign_stv', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[21][0] == 'nb_coln_stv', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"  
      assert lines[22][0] == 'zn_mrt_center_x', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
      assert lines[23][0] == 'zn_mrt_center_y', "Le fichier correspondant ne correspond pas a un fichier config du detecteur"    
          
          
      #mise en caracteristique du fichier config des carac de la zone d'etude
      #les caracteres peuvent etre laisses vide
      if lines[1][1] != "":
        frmts_pxl =[(30,30),(50,150),(50,300)]
        self._frmt_pxl = frmts_pxl[int(lines[1][1])]
        self._wth_pxl = self._frmt_pxl[0]
        self._hgt_pxl = self._frmt_pxl[1]
        
        
      if lines[2][1] != "":
        self._spcng_pxl_x = int(lines[2][1])
      if lines[3][1] != "":
        self._spcng_pxl_y = int(lines[3][1])
      if lines[4][1] != "":
        self._nb_lign_pxl_chp = int(lines[4][1])
      if lines[5][1] != "":
        self._nb_coln_pxl_chp = int(lines[5][1])
      if lines[6][1] != "":
        self._zn_mrt_chp_gau = int(lines[6][1])
      if lines[7][1] != "":
        self._zn_mrt_chp_dro = int(lines[7][1])  
      if lines[8][1] != "":
        self._zn_mrt_chp_bas = int(lines[8][1]) 
      if lines[9][1] != "":
        self._zn_mrt_chp_hau = int(lines[9][1])
        
      if lines[10][1] != "":
        self._spcng_chp_x = int(lines[10][1]) 
      if lines[11][1] != "":
        self._spcng_chp_y = int(lines[11][1]) 
      if lines[12][1] != "":
        self._nb_lign_chp_mdl = int(lines[12][1]) 
      if lines[13][1] != "":
        self._nb_coln_chp_mdl = int(lines[13][1])
         
      if lines[14][1] != "":
        self._spcng_mdl_x = int(lines[14][1]) 
      if lines[15][1] != "":
        self._spcng_mdl_y = int(lines[15][1]) 
      if lines[16][1] != "":
        self._nb_lign_mdl_stv = int(lines[16][1]) 
      if lines[17][1] != "":
        self._nb_coln_mdl_stv = int(lines[17][1]) 
        
      if lines[18][1] != "":
        self._spcng_stv_x = int(lines[18][1]) 
      if lines[19][1] != "":
        self._spcng_stv_y = int(lines[19][1]) 
      if lines[20][1] != "":
        self._nb_lign_stv = int(lines[20][1]) 
      if lines[21][1] != "":
        self._nb_coln_stv = int(lines[21][1])
        
      if lines[22][1] != "":
        self._zn_mrt_center_x = int(lines[22][1]) 
      if lines[23][1] != "":
        self._zn_mrt_center_y = int(lines[23][1]) 
  
      # On met la caracteristique vraie pour savoir que la config est de type detector
      self._is_cfg_detector = True
      
      
      #Calculer les dimensions des differentes parties du detecteur
      wth_chp = self._nb_coln_pxl_chp * self._frmt_pxl[0]  + (self._nb_coln_pxl_chp - 1) * self._spcng_pxl_x + self._zn_mrt_chp_gau + self._zn_mrt_chp_dro
      hgt_chp = self._nb_lign_pxl_chp * self._frmt_pxl[1]  + (self._nb_lign_pxl_chp - 1) * self._spcng_pxl_y + self._zn_mrt_chp_hau + self._zn_mrt_chp_bas
      self._wth_chp = wth_chp
      self._hgt_chp = hgt_chp
      
      wth_mdl = self._nb_coln_chp_mdl * wth_chp + (self._nb_coln_chp_mdl - 1) * self._spcng_chp_x
      hgt_mdl = self._nb_lign_chp_mdl * hgt_chp + (self._nb_lign_chp_mdl - 1) * self._spcng_chp_y
      self._wth_mdl = wth_mdl
      self._hgt_mdl = hgt_mdl
      
      wth_stv = self._nb_coln_mdl_stv * wth_mdl + (self._nb_coln_mdl_stv - 1) * self._spcng_mdl_x
      hgt_stv = self._nb_lign_mdl_stv * hgt_mdl + (self._nb_lign_mdl_stv - 1) * self._spcng_mdl_y
      self._wth_stv = wth_stv
      self._hgt_stv = hgt_stv  
      
      wth_det = self._nb_coln_stv * wth_stv + (self._nb_coln_stv - 1) * self._spcng_stv_x
      hgt_det = self._nb_lign_stv * hgt_stv + (self._nb_lign_stv - 1) * self._spcng_stv_y
      self._wth_det = wth_det
      self._hgt_det = hgt_det
      
      
      #Determiner la numerotation des objets
      #On veut numeroter les objets avec une numerotation sssmmccppp (s=stave, m=module, c=chip, p=pixel)
      #On regarde ici combien de charactere il faut pour numeroter tous les staves, les modules...
      def f(x):
        return(len(str(x)))
      
      
      array = [f(self._nb_lign_stv),f(self._nb_coln_stv),f(self._nb_lign_mdl_stv),f(self._nb_coln_mdl_stv), f(self._nb_lign_chp_mdl),f(self._nb_coln_chp_mdl),f(self._nb_lign_pxl_chp),f(self._nb_coln_pxl_chp)] 
      string = "S"*f(self._nb_lign_stv) + "s"*f(self._nb_coln_stv) + "M"*f(self._nb_lign_mdl_stv) + "m"*f(self._nb_coln_mdl_stv) + "C"*f(self._nb_lign_chp_mdl) + "c"*f(self._nb_coln_chp_mdl) + "P"*f(self._nb_lign_pxl_chp) + "p"*f(self._nb_coln_pxl_chp)
            
      self._numerotation_affichee = string
      self._numerotation = array
      
      
    else:
      print("Le fichier correspondant n'est pas un fichier config")

     
    
    
    
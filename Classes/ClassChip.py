import ClassConfig
import ClassParticule

try:
  reload(ClassPixel)
  import ClassPixel
except NameError:
  import ClassPixel

class Chip:

  def __init__(self, cfg, x_pos = 0, y_pos = 0):
    
    nb_coln_pxl_chp = cfg._nb_coln_pxl_chp
    nb_lign_pxl_chp = cfg._nb_lign_pxl_chp
    wth_pxl = cfg._wth_pxl
    hgt_pxl = cfg._hgt_pxl

    #les champs largeur_zm et ecart sont la pour rendre compte des zones mortes   
    matrice = [[[]for k in range(nb_coln_pxl_chp)] for j in range (nb_lign_pxl_chp)]
    x_courant = x_pos + cfg._zn_mrt_chp_gau
    y_courant = y_pos + cfg._zn_mrt_chp_bas
    
    for i in range(nb_lign_pxl_chp):
      for j in range(nb_coln_pxl_chp):
        #on rajoute le nouveau pixel, par abscisses et ordonnees croissantes
        #attention a ca, le premier pixel a etre rajoute est en [nb_lign_pxl_chp-1][0]
        pix = ClassPixel.Pixel(cfg, x_courant, y_courant)
        matrice[i][j] = pix
        #on actualise les donnees courantes 
        x_courant += wth_pxl
        
      x_courant = x_pos + cfg._zn_mrt_chp_gau
      y_courant += hgt_pxl
        
    #on definit les champs de la classe
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrice_pixels = matrice
    self._nb_hit = 0
    self._cfg = cfg
    
    
  def hit(self):
    self._nb_hit +=1
  
  def reset_hit(self):
    self._nb_hit = 0
    for i in range(nb_lign_pxl_chp):
      for j in range(nb_coln_pxl_chp):
        self._matrice_pixels[i][j].reset_hit()
  
  
  def hit_part(self, part):
    #piste d'amelioration: il pourrait etre interessant de recuperer les temps de hit
    
    cfg = self._cfg
    #on definit des constantes geometriques du chp utiles
    delta_x = cfg._spcng_pxl_x + self._matrice_pixels[0][0]._wth #la largeur en abscisse d'un pixel et de l'ecart en x
    delta_y = cfg._spcng_pxl_y + self._matrice_pixels[0][0]._hgt #la largeur en ordonnee d'un pixel et de l'ecart en y
    largeur_x = cfg._nb_coln_pxl_chp*delta_x + cfg._zn_mrt_chp_gau + cfg._zn_mrt_chp_dro #la taille en abscisse d'un chp
    largeur_y = cfg._nb_lign_pxl_chp*delta_y + cfg._zn_mrt_chp_bas + cfg._zn_mrt_chp_hau #la taille en ordonnee d'un chp
    
    n = len(part._list_x)
    
    for i in range(n):
      #on teste pour les positions successives de la particule
      #ca pourrait etre interessant de faire une recherche plus intelligente,  puisque la liste des positions est triee en z
      x = part._list_x[i]
      y = part._list_y[i]
      if (x>=self._x_pos) and (x<=(self._x_pos + largeur_x)) and (y>=self._y_pos) and(y<=(self._y_pos + largeur_y)):
        #si on touche la chp
        #on incremente le nombre de hits sur la chp
        #on cherche sur quel pixel la particule a tape 
        n_x = int((x - self._x_pos - cfg._zn_mrt_chp_gau)/delta_x)
        n_y = int((y - self._y_pos - cfg._zn_mrt_chp_bas)/delta_y)
        if (n_x<0) or (n_y<0):
        #on teste 
          n_x = 0
          n_y = 0
        if self._matrice_pixels[cfg._nb_lign_pxl_chp - n_y - 1][n_x].hit_part(part):
          #la particule a touche un pixel, on renvoie (True, Id du pixel touche(un entier))
          return (True, self._matrice_pixels[cfg._nb_lign_pxl_chp - n_y - 1][n_x]._id_)
        #La particule a touche une zone morte, on renvoie (True, -1)
        return (True, -1)
      #la particule n'a pas touche la chp, on renvoie (False, -1)
      return (False, -1)
      
      
  def hit_parts(self, part):
    #piste d'amelioration: il pourrait etre interessant de recuperer les temps de hit
    
    cfg = self._cfg
    largeur_x = cfg._wth_chp
    largeur_y = cfg._hgt_chp
    
    n = len(part._list_x)
    
    for i in range(n):
      #on teste pour les positions successives de la particule
      #ca pourrait etre interessant de faire une recherche plus intelligente,  puisque la liste des positions est triee en z
      x = part._list_x[i]
      y = part._list_y[i]
      if (x>=self._x_pos) and (x<=(self._x_pos + largeur_x)) and (y>=self._y_pos) and(y<=(self._y_pos + largeur_y)):
        self._nb_hit += 1
      
        
  def hit_pos(self, x, y):
    
    cfg = self._cfg
    #on definit des constantes geometriques du chp utiles
    delta_x = cfg._spcng_pxl_x + self._matrice_pixels[0][0]._wth #la largeur en abscisse d'un pixel et de l'ecart en x
    delta_y = cfg._spcng_pxl_y + self._matrice_pixels[0][0]._hgt #la largeur en ordonnee d'un pixel et de l'ecart en y
    largeur_x = cfg._nb_coln_pxl_chp*delta_x + cfg._zn_mrt_chp_gau + cfg._zn_mrt_chp_dro #la taille en abscisse d'un chp
    largeur_y = cfg._nb_lign_pxl_chp*delta_y + cfg._zn_mrt_chp_bas + cfg._zn_mrt_chp_hau #la taille en ordonnee d'un chp
        
    if (x>=self._x_pos) and (x<=(self._x_pos + largeur_x)) and (y>=self._y_pos) and(y<=(self._y_pos + largeur_y)):
      #si on touche la chp
      #on incremente le nombre de hits sur la chp
      #on cherche sur quel pixel la particule a tape 
      n_x = int((x - self._x_pos - cfg._zn_mrt_chp_gau)/delta_x)
      n_y = int((y - self._y_pos - cfg._zn_mrt_chp_bas)/delta_y)
      if (n_x<0) or (n_y<0):
      #on teste 
        n_x = 0
        n_y = 0
      if self._matrice_pixels[cfg._nb_lign_pxl_chp - n_y - 1][n_x].hit_part(part):
        #la particule a touche un pixel, on renvoie (True, Id du pixel touche(un entier))
        return (True, self._matrice_pixels[cfg._nb_lign_pxl_chp - n_y - 1][n_x]._id_)
      #La particule a touche une zone morte, on renvoie (True, -1)
      return (True, -1)
    #la particule n'a pas touche la chip, on renvoie (False, -1)
    return (False, -1)
    


  def hit_part_prec(self, part, prec):
    cfg = self._cfg
    if prec == 0:
      self._hit_parts(part)
      return self._nb_hit
    else:
      res = [[]for k in range(cfg._nb_lign_pxl_chp)]
      for i in range(cfg._nb_lign_pxl_chp):
        for j in range(cfg._nb_coln_pxl_chp):
          res[i].append(self._matrice_pixels[i][j].hit_part_prec(cfg,part,prec-1))
      return res   
      
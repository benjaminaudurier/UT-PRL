import ClassConfig
import ClassParticule

try:
  reload(ClassStave)
  import ClassStave
except NameError:
  import ClassStave


class Detector:

  def __init__(self, cfg, x_pos = 0, y_pos = 0):
    
    
    nb_lign_stv = cfg._nb_lign_stv
    nb_coln_stv = cfg._nb_coln_stv
    wth_stv = cfg._wth_stv
    hgt_stv = cfg._hgt_stv
    spcng_stv_x = cfg._spcng_stv_x
    spcng_stv_y = cfg._spcng_stv_y
    
    matrice = [[]for k in range(nb_lign_stv)]
    x_courant = x_pos
    y_courant = y_pos
      
    def f_coln(y):
      while len(y) < cfg._numerotation[0]:
        y = "0"+y
      return(y)
        
    def f_lign(y):
      while len(y) < cfg._numerotation[1]:
        y = "0"+y
      return(y)
    
    for i in range(nb_lign_stv):
      for j in range(nb_coln_stv):
      
        #on rajoute le nouveau pixel, par abscisses et ordonnees croissantes
        #attention a ca, le premier pixel a etre rajoute est en [nb_lign_pxl_stv-1][0]
        stv = ClassStave.Stave(cfg, x_courant, y_courant, f_lign(str(i)) + f_coln(str(j)))
        matrice[i].append(stv)
        #on actualise les donnees courantes 
        x_courant += wth_stv + spcng_stv_x
      
        
      x_courant = x_pos
      y_courant += hgt_stv + spcng_stv_y
        
      
        
    #on definit les champs de la classe
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrice_staves = matrice
    self._nb_hit = 0
    
    
  def hit_parts(self, part):
    #piste d'amelioration: il pourrait etre interessant de recuperer les temps de hit
    
    cfg = self._cfg
    largeur_x = cfg._wth_det
    largeur_y = cfg._hgt_det
    
    n = len(part._list_x)
    
    for i in range(n):
      #on teste pour les positions successives de la particule
      #ca pourrait etre interessant de faire une recherche plus intelligente,  puisque la liste des positions est triee en z
      x = part._list_x[i]
      y = part._list_y[i]
      if (x>=self._x_pos) and (x<=(self._x_pos + largeur_x)) and (y>=self._y_pos) and(y<=(self._y_pos + largeur_y)):
        self._nb_hit += 1
    
    
  def hit_part_prec(self, cfg, part, prec):
    if prec == 0:
      self._hit_parts(part)
      return self._nb_hit
    else:
      res = [[]for k in range(cfg._nb_lign_stv)]
      for i in range(cfg._nb_lign_stv):
        for j in range(cfg._nb_coln_stv):
          res[i].append(self._matrice_staves[i][j].hit_part_prec(cfg,part,prec-1))
      return res
        
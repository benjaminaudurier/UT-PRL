import ClassConfig
import ClassParticule

try:
  reload(ClassChip)
  import ClassChip
except NameError:
  import ClassChip


class Module:

  def __init__(self, cfg, x_pos = 0, y_pos = 0):
    
    
    nb_lign_chp_mdl = cfg._nb_lign_chp_mdl
    nb_coln_chp_mdl = cfg._nb_coln_chp_mdl
    wth_chp = cfg._wth_chp
    hgt_chp = cfg._hgt_chp
    spcng_chp_x = cfg._spcng_chp_x
    spcng_chp_y = cfg._spcng_chp_y
    
    matrice = [[[]for k in range(nb_coln_chp_mdl)] for j in range (nb_lign_chp_mdl)]
    x_courant = x_pos
    y_courant = y_pos

          
    for i in range(nb_lign_chp_mdl):
      for j in range(nb_coln_chp_mdl):
        #on rajoute le nouveau chip, par abscisses et ordonnees croissantes
        #attention a ca, le premier pixel a etre rajoute est en [nb_lign_pxl_chp-1][0]
        chp = ClassChip.Chip(cfg, x_courant, y_courant)
        matrice[i][j] = chp
        #on actualise les donnees courantes 
        x_courant += wth_chp + spcng_chp_x
        
      x_courant = x_pos
      y_courant += hgt_chp + spcng_chp_y
        
    #on definit les champs de la classe
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrice_chips = matrice
    self._nb_hit = 0
    self._cfg = cfg
    


  def hit(self):
    self._nb_hit += 1
    
  
  def hit_parts(self, part):
    #piste d'amelioration: il pourrait etre interessant de recuperer les temps de hit
    
    cfg = self._cfg
    largeur_x = cfg._wth_mdl
    largeur_y = cfg._hgt_mdl
    
    n = len(part._list_x)
    
    for i in range(n):
      #on teste pour les positions successives de la particule
      #ca pourrait etre interessant de faire une recherche plus intelligente,  puisque la liste des positions est triee en z
      x = part._list_x[i]
      y = part._list_y[i]
      if (x>=self._x_pos) and (x<=(self._x_pos + largeur_x)) and (y>=self._y_pos) and(y<=(self._y_pos + largeur_y)):
        self._nb_hit += 1
    
    
  def hit_part_prec(self, part, prec):
    cfg = self._cfg
    if prec == 0:
      self._hit_parts(part)
      return self._nb_hit
    else:
      res = [[]for k in range(cfg._nb_lign_chp_mdl)]
      for i in range(cfg._nb_lign_chp_mdl):
        for j in range(cfg._nb_coln_chp_mdl):
          res[i].append(self._matrice_chips[i][j].hit_part_prec(cfg,part,prec-1))
      return res        
        
        
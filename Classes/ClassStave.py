import ClassConfig
import ClassParticule

try:
  reload(ClassModule)
  import ClassModule
except NameError:
  import ClassModule

class Stave:

  def __init__(self, cfg, x_pos = 0, y_pos = 0):
    
    
    nb_lign_mdl_stv = cfg._nb_lign_mdl_stv
    nb_coln_mdl_stv = cfg._nb_coln_mdl_stv
    wth_mdl = cfg._wth_mdl
    hgt_mdl = cfg._hgt_mdl
    spcng_mdl_x = cfg._spcng_mdl_x
    spcng_mdl_y = cfg._spcng_mdl_y
    
    matrice = [[[]for k in range(nb_coln_mdl_stv)] for j in range (nb_lign_mdl_stv)]
    x_courant = x_pos
    y_courant = y_pos
        
    for i in range(nb_lign_mdl_stv):
      for j in range(nb_coln_mdl_stv):
      
        #on rajoute le nouveau pixel, par abscisses et ordonnees croissantes
        #attention a ca, le premier pixel a etre rajoute est en [nb_lign_pxl_mdl-1][0]
        mod = ClassModule.Module(cfg, x_courant, y_courant)
        matrice[i][j] = mod
        #on actualise les donnees courantes 
        x_courant += wth_mdl + spcng_mdl_x
        
      x_courant = x_pos
      y_courant += hgt_mdl + spcng_mdl_y
        
    #on definit les champs de la classe
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrice_modules = matrice
    self._nb_hit = 0
    self._cfg = cfg
    


  def hit(self):
    self._nb_hit += 1
    
  
  def hit_parts(self, part):
    #piste d'amelioration: il pourrait etre interessant de recuperer les temps de hit
    
    cfg = self._cfg
    largeur_x = cfg._wth_stv
    largeur_y = cfg._hgt_stv
    
    n = len(part._list_x)
    
    for i in range(n):
      #on teste pour les positions successives de la particule
      #ca pourrait etre interessant de faire une recherche plus intelligente,  puisque la liste des positions est triee en z
      x = part._list_x[i]
      y = part._list_y[i]
      if (x>=self._x_pos) and (x<=(self._x_pos + largeur_x)) and (y>=self._y_pos) and(y<=(self._y_pos + largeur_y)):
        self._nb_hit += 1
        
        
  def hit_part_prec(self, part, prec):
    if prec == 0:
      self._hit_parts(part)
      return self._nb_hit
    else:
      res = [[]for k in range(self._cfg._nb_lign_mdl_stv)]
      for i in range(self._cfg._nb_lign_mdl_stv):
        for j in range(self._cfg._nb_coln_mdl_stv):
          res[i].append(self._matrice_modules[i][j].hit_part_prec(self.cfg,part,prec-1))
      return res
    
  def draw(self, c):
    return
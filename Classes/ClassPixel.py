import ClassConfig
import ClassParticule

class Pixel:
  
  def __init__(self, cfg, x_pos = 0.0, y_pos = 0.0):
    self._wth = cfg._frmt_pxl[0]
    self._hgt = cfg._frmt_pxl[1]
    self._x_pos = x_pos
    self._y_pos = y_pos 
    self._nb_hit = 0

    #x_pos y_pos correspondent au coin inferieur gauche du pixel
    
    
  
  def hit(self):
    self._nb_hit += 1
    
  def reset_hit(self):
    self._nb_hit = 0
    
  def hit_parts(self, part):
    n = len(part._list_x)
    for i in range(n):
      x = part._list_x[i]
      y = part._list_y[i]
      if (x > self._x_pos) and (x < self._x_pos+ self._wth) and (y > self._y_pos) and (y < self._y_pos + self._hgt):
        self._nb_hit += 1
  
    
  def hit_pos(self, x_pos_part = 0.0, y_pos_part = 0.0):
    if x_pos_part > self._x_pos and x_pos_part < self._x_pos+ self._wth and y_pos_part > self._y_pos and y_pos_part < self._y_pos+ self._hgt:
      self._nb_hit += 1
      
  def hit_part_prec(self, part, prec):
    cfg = self._cfg
    if prec == 0:
      self.hit_parts(part)
      return self._nb_hit
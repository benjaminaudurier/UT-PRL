# UTGeometry contains all the geometry of the UT Detector
# it has 5 classes : Detector, Stave, Module, Chip, Pixel
# each class represents a subobject of the preceding one
from __future__ import print_function
import ClassConfigDetector
import ROOT
import numpy as np


####################  FUNCTIONS ##########################

###############################
# hit_parts gives the number of particles that hit the rectangle defined by the object self
def hit_parts(obj, copy_part):
  #particles.list_x and particles.list_y must be sorted (on the x-basis), to optimise the iterative treatment
  compteur = 0
  x_pos = obj._x_pos
  y_pos = obj._y_pos
  wth = obj._wth
  hgt = obj._hgt
  count = 0
  pop = 0
  #we look for the particles that hit the object that is being studied
  n = len(copy_part[0])
  i = 0
  while (copy_part[0][i]<=x_pos+wth) and (i!=n-1):
    print("{} particles left".format(n), end = '\r') #this line displays a counter
    x_part = copy_part[0][i]
    y_part = copy_part[1][i]
    if (x_part >= x_pos) and (x_part <= (x_pos + wth)) and (y_part >= y_pos) and (y_part <= (y_pos + hgt)): #if the particle hits
      count += 1 #the count is increased
      pop = copy_part[0].pop(i) # the particle is deleted from the  particles lists
      pop = copy_part[1].pop(i)
      n-=1
    else:
      i+=1
  return count


#############################
# hit_parts_precision gives a table of how many particles hit the object of the precision given (0:det - 1:stv - 2:mdl...)
def hit_parts_precision(obj, copy_part, precision = 3):
  #pos_particles is a list [pos_particles_x, pos_particles_y], and pos_particles_x is a copy of particles._list_x
  if precision == 0:
    #here we have reached the last level of the recursion, and the hitparts function is called
    return hit_parts(obj,copy_part)
  else:
    matrix = obj._matrix
    nb_lign = len(matrix)
    nb_coln = len(matrix[0])
  
    res = [[[]for j in range(nb_coln)] for i in range (nb_lign)]
    for j in range(nb_coln):
      for i in range(nb_lign):
        #we recursively call the function on every sub-element of the matrix
        res[i][j] = hit_parts_precision(matrix[i][j], copy_part, precision-1)
    return res


#############################
# Draw the detector, or subcomponent, as a heatmap representing the particles detected afgter one or more collisions
# obj = the object we want to draw, instance of one of the classes defined below
#res = impacts on each subcomponent of the object, it also indicates the level of precision of the represnetation (for a module, if res is a simple matrix, the representation will detail to the level of the pixel), np.ndarray
# name is the name of the file (directory is ../Pictures by default), if you want to use a dffierent directory you must change the last line, str

# USED ONLY IF res is not given, in this case only a detector can be represented
# particles = instance of the Particle class; 
# precision = level of precision to be used while drawng the detector with the impacts: 0 is the object itself, 1 is a level below etc.., int < 3

def draw_detector(obj, res = [], name = "Boxes", particles = [], precision = 3):

  if not res:
    copy_part = [[a for a in particule._list_x],[a for a in particule._list_y]]
    res = hit_parts_precision(det, copy_part, precision = 3)
  
  c = ROOT.TCanvas()
  c.SetWindowSize(5000,5000)
  c.SetCanvasSize(10000,10000)

  x_origins, y_origins = obj._x_pos, obj._y_pos # reference for the coordinates in the Canvas
  size_ref = max(obj._wth, obj._hgt) * 1.2 # spatial scale
  
  max_hits = float(np.max(res))
  boxes = draw_w_res(obj, size_ref, res, x_origins, y_origins, max_hits) # list of Tboxes representing the object and its subcomponents, colored in the way of a heatmap
  for box in boxes:
    box.Draw()
    c.Update()
    c.Modified()

  # We now want to draw a colorbar of the heatmap
  x_scale, y_scale = (4*boxes[-1].GetX2() + 1)/5, boxes[-1].GetY2() 
  scale = [0] * 42 # Colors
  grads = [0] * 42 # Graduations
  
  # draw the color scale on the right side
  if max_hits:
    for i in range (42):
      scale[i] = ROOT.TBox(x_scale, y_scale * i / 42., x_scale + .05, y_scale * (i+1) / 42.)
      scale[i].SetFillColor(57 + i)
      scale[i].Draw()
      
      grads[i] = ROOT.TText(x_scale + .06 , y_scale * i /42., str(int(float(max_hits)/(42.*10**6) * i))[:2])
      grads[i].SetTextSize(1./42)
      grads[i].Draw()
      
      c.Update()
      c.Modified()
  
  c.Print("../Pictures/" + name + ".png")
  

################################
# Representation of a measure, draws a component and eventually its subcomponents
#obj = component (one of the classes defined bellow)
#size_ref = spatial reference for a correct scaling: for exemple, 1.2 times the size of the component, float
#res = impacts on each subcomponent of the object, it also indicates the level of precision of the represnetation (for a module, if res is a simple matrix, the representation will detail to the level of the pixel), np.ndarray
#x_origins and y_origins gives a reference for the coordinates, float
#max_hits is the maximum number of hits on an individual subcompononent, typically np.max(res), int
def draw_w_res(obj, size_ref, res = np.array(), x_origins, y_origins, max_hits):

  box = ROOT.TBox((obj._x_pos - x_origins)/size_ref, (obj._y_pos - y_origins)/size_ref, (obj._x_pos + obj._wth - x_origins)/size_ref, (obj._y_pos + obj._hgt - y_origins)/size_ref)
  boxes = [box]
  if type(res) == list:
    res = np.array(res)
  
  if type(res) == np.ndarray: # res is an array, therefore we ask to draw the object at a smaller level of precision (module > pixel for example)
    box.SetFillColor(1)
    matrix = obj._matrix
    assert matrix.shape == res.shape, "La matrice de l'objet {} et de celle des impacts n'ont pas les mêmes dimensions : {}, {}".format(obj._type, matrix.shape, res.shape) 
    for i in range(len(matrix)):
      for j in range(len(matrix[0])):
        boxes += draw_w_res(matrix[i][j], size_ref, res[i][j], x_origins, y_origins, max_hits)
        print("{} number {} treated".format(matrix[i][j]._type, i*len(matrix[0])+j), '\r')
  
  else:
    if max_hits == 0: # max_hits = 0 only if no impacts, ie representation of the configuration of the component
      box.SetFillColor(17)
    else :
      box.SetFillColor(57 + int(res / max_hits * 42))
        
  return boxes # Returns a list of TBoxes, ordered in a coherent manner (from biggest to smallest)


################################  
#draw_detector_configuration allows us to vizualize the structure of the detector
def draw_detector_configuration(det):
  obj = det
  for i in range (3):
    res = [[0]*len(obj._matrix[0])]*len(obj._matrix) #Simulate an experiment with 0 impacts
    draw_detector(obj, precision = 1, res = res, name = obj._type)
    obj = obj._matrix[0][0]
  return



#################### PIXEL #####################
# a pixel is a rectangle in the plane
# x_pos and y_pos are the coordinates of the lower-left angle
# wth and hgt are the width and height of the rectangle

class Pixel:
  def __init__(self, cfg, x_pos = 0, y_pos = 0):
    self._type = "Pixel"
    self._x_pos = x_pos
    self._y_pos = y_pos 
    self._hgt = cfg.get("hgt_pxl")
    self._wth = cfg.get("wth_pxl")
    self._nb_hit = 0
    self._cfg = cfg
    
    
    
    
    
#################### CHIP #####################
# a Chip can be two things
#      - if pixel_precision: a Chip is a matrix of Pixel
#      - else: a Chip is a rectangle in the plane

class Chip:
  def __init__(self, cfg, x_pos = 0, y_pos = 0, pixel_precision = False):
  
    self._type = "Chip"
    
    
    # matrix of pixel
    if pixel_precision:
      
      # we read the parameters from the config object
      # nb_****_pxl_chp : how many line or column of pixel will be in the chip
      # ***_stv         : geometrical caracteristics of one pixel
      # zn_mrt_chp_gau  : geometrical dead zone of a chip at the bottom or on the left
      nb_coln_pxl_chp = cfg.get("nb_coln_pxl_chp")
      nb_lign_pxl_chp = cfg.get("nb_lign_pxl_chp")
      wth_pxl = cfg.get("wth_pxl")
      hgt_pxl = cfg.get("hgt_pxl")
      zn_mrt_chp_gau = cfg.get("zn_mrt_chp_gau")
      zn_mrt_chp_bas = cfg.get("zn_mrt_chp_bas")
        
      matrix = [[[]for k in range(nb_coln_pxl_chp)] for j in range (nb_lign_pxl_chp)]
      
      # *_current represents the place where to put a new pixel (bottom-left corner)
      x_current = x_pos + zn_mrt_chp_gau
      y_current = y_pos + zn_mrt_chp_bas
      
      
      for i in range(nb_lign_pxl_chp):
        for j in range(nb_coln_pxl_chp):
          pix = Pixel(cfg, x_current, y_current)
          matrix[i][j] = pix
          
          # we update the current value in x
          x_current += wth_pxl
          
        # x goes back to the first value
        # y is incremented
        x_current = x_pos + zn_mrt_chp_gau
        y_current += hgt_pxl
          
          
      # we attribute the value to the chip object
      self._x_pos = x_pos
      self._y_pos = y_pos
      self._matrix = matrix
      self._nb_hit = 0
      self._cfg = cfg
      self._hgt = cfg.get("hgt_chp")
      self._wth = cfg.get("wth_chp")
      
    # rectangle
    else:
      self._x_pos = x_pos
      self._y_pos = y_pos
      self._nb_hit = 0
      self._cfg = cfg    
      self._hgt = cfg.get("hgt_chp")
      self._wth = cfg.get("wth_chp")
      
      
       
      
      
################## MODULE ###################
# a Module is a matrix of Chip object

class Module:
  def __init__(self, cfg, x_pos = 0, y_pos = 0, pixel_precision = False):
    # we read the parameters from the config object
    # spcng_chp_* : space needed between two chips
    nb_coln_chp_mdl = cfg.get("nb_coln_chp_mdl")
    nb_lign_chp_mdl = cfg.get("nb_lign_chp_mdl")
    wth_chp = cfg.get("wth_chp")
    hgt_chp = cfg.get("hgt_chp")
    spcng_chp_x = cfg.get("spcng_chp_x")
    spcng_chp_y = cfg.get("spcng_chp_y")
      
      
    matrix = [[[]for k in range(nb_coln_chp_mdl)] for j in range (nb_lign_chp_mdl)]
    
    # *_current represents the place where to put a new chip (bottom-left corner)
    x_current = x_pos 
    y_current = y_pos 
    
    
    for i in range(nb_lign_chp_mdl):
      for j in range(nb_coln_chp_mdl):
        chp = Chip(cfg, x_current, y_current, pixel_precision)
        matrix[i][j] = chp
        
        # we update the current value in x
        x_current += wth_chp + spcng_chp_x
        
      # x goes back to the first value
      # y is incremented
      x_current = x_pos 
      y_current += hgt_chp + spcng_chp_y
        
        
    # we attribute the value to the module object
    self._type = "Module"
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrix = matrix
    self._nb_hit = 0
    self._cfg = cfg
    self._hgt = cfg.get("hgt_mdl")
    self._wth = cfg.get("wth_mdl")



################## STAVE ###################
# a Stave is a matrix of Module object

class Stave:
  def __init__(self, cfg, x_pos = 0, y_pos = 0, pixel_precision = False):
    # we read the parameters from the config object
    nb_coln_mdl_stv = cfg.get("nb_coln_mdl_stv")
    nb_lign_mdl_stv = cfg.get("nb_lign_mdl_stv")
    wth_mdl = cfg.get("wth_mdl")
    hgt_mdl = cfg.get("hgt_mdl")
    spcng_mdl_x = cfg.get("spcng_mdl_x")
    spcng_mdl_y = cfg.get("spcng_mdl_y")
      
      
    matrix = [[[]for k in range(nb_coln_mdl_stv)] for j in range (nb_lign_mdl_stv)]
    
    # *_current represents the place where to put a new module (bottom-left corner)
    x_current = x_pos 
    y_current = y_pos 
    
    
    for i in range(nb_lign_mdl_stv):
      for j in range(nb_coln_mdl_stv):
        mdl = Module(cfg, x_current, y_current, pixel_precision)
        matrix[i][j] = mdl
        
        # we update the current value in x
        x_current += wth_mdl + spcng_mdl_x
        
      # x goes back to the first value
      # y is incremented
      x_current = x_pos 
      y_current += hgt_mdl + spcng_mdl_y
        
        
    # we attribute the value to the stave object
    self._type = "Stave"
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrix = matrix
    self._nb_hit = 0
    self._cfg = cfg
    self._hgt = cfg.get("hgt_stv")
    self._wth = cfg.get("wth_stv")



############### DETECTOR #############
# a Detector is a matrice of Stave objects
  
class Detector:
  def __init__(self, cfg, pixel_precision = False):
    
    # we read the parameters from the config object
    # spcng_stv_* : spacing between different stave in x or y
    nb_lign_stv = cfg.get("nb_lign_stv")
    nb_coln_stv = cfg.get("nb_coln_stv")
    wth_stv = cfg.get("wth_stv")
    hgt_stv = cfg.get("hgt_stv")
    wth_det = cfg.get("wth_det")
    hgt_det = cfg.get("hgt_det")
    spcng_stv_x = cfg.get("spcng_stv_x")
    spcng_stv_y = cfg.get("spcng_stv_y")
    
    x_pos = - float(wth_det) / 2.
    y_pos = - float(hgt_det) / 2.
    
    matrix = [[[]for k in range(nb_coln_stv)] for j in range (nb_lign_stv)]
    x_current = x_pos
    y_current = y_pos
      

    for i in range(nb_lign_stv):
      for j in range(nb_coln_stv):
        stv = Stave(cfg, x_current, y_current, pixel_precision)
        matrix[i][j] = stv
        
        # we update the current values 
        x_current += wth_stv + spcng_stv_x
        print("Stave " + str(i*nb_coln_stv + j+1) + " out of " + str(nb_lign_stv * nb_coln_stv) + " created")
        
      x_current = x_pos
      y_current += hgt_stv + spcng_stv_y
        
      
        
    #on definit les champs de la classe
    self._type = "Detector"
    self._x_pos = x_pos
    self._y_pos = y_pos
    self._matrix = matrix
    self._cfg = cfg
    self._hgt = hgt_det
    self._wth = wth_det
        
    
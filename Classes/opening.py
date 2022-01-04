if __name__ == '__main__':
  import ROOT
  
  import ClassDetector
  import ClassParticule
  import ClassConfig
  
  cfg_detector = ClassConfig.Config("/grid_mnt/data__DATA/data.lhcb/PRL/Configs/config_detector_test2.txt")
  cfg_sz = ClassConfig.Config("/grid_mnt/data__DATA/data.lhcb/PRL/Configs/config_study_zone.txt")
  
  #import files
  f = ROOT.TFile("/data/DATA/data.lhcb/audurier/MCtracks-PbPbtest-100_1.root")
  d = f.get("MCParticleNTuple")
  tree = d.Tracks
  
  det = ClassDetector.Detector(cfg_detector)
  particule = ClassParticule.Particule(tree, cfg_sz)
  
  pixel = det._matrice_staves[0][0]._matrice_modules[0][0]._matrice_chips[0][0]._matrice_pixels[0][0]
  chip = det._matrice_staves[0][0]._matrice_modules[0][0]._matrice_chips[0][0]
  module = det._matrice_staves[0][0]._matrice_modules[0][0]
  stave = det._matrice_staves[0][0]

  num_objet = cfg_sz._obj
  id_ = cfg_sz._id 
  prec = cfg_sz._prec
  
  nums = cfg_detector._numerotation
  
  if num_objet == 0:
    res = det.hit_part_prec(cfg_detector, particule, prec)
  
  elif num_objet == 1:
    i_stv = int(id_[0:nums[0]])
    j_stv = int(id_[nums[0],nums[0]+nums[1]])
    
    stave = det._matrice_staves[i_stv][j_stv]
    res = stave.hit_part_prec(cfg_detector, particule, prec - num_objet)
    
  elif num_objet == 2:
    i_stv = int(id_[0:nums[0]])
    j_stv = int(id_[nums[0]:nums[0]+nums[1]])
    i_mdl = int(id_[nums[0]+nums[1]:nums[0]+nums[1]+nums[2]])
    j_mdl = int(id_[nums[0]+nums[1]+nums[2]:nums[0]+nums[1]+nums[2]+nums[3]])
    
    module = det._matrice_staves[i_stv][j_stv]._matrice_modules[i_mdl][j_mdl]
    res = module.hit_part_prec(cfg_detector, particule, prec - num_objet)
    
  elif num_objet == 3:
    i_stv = int(id_[0:nums[0]])
    j_stv = int(id_[nums[0]:nums[0]+nums[1]])
    i_mdl = int(id_[nums[0]+nums[1]:nums[0]+nums[1]+nums[2]])
    j_mdl = int(id_[nums[0]+nums[1]+nums[2]:nums[0]+nums[1]+nums[2]+nums[3]])
    i_chp = int(id_[nums[0]+nums[1]+nums[2]+nums[3]:nums[0]+nums[1]+nums[2]+nums[3]+nums[4]])
    j_chp = int(id_[nums[0]+nums[1]+nums[2]+nums[3]+nums[4]:nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]])
    
    chip = det._matrice_staves[i_stv][j_stv]._matrice_modules[i_mdl][j_mdl]._matrice_chips[i_chp][j_chp]
    res = chip.hit_part_prec(cfg_detector, particule, prec - num_objet)
    
  elif num_objet == 4:
    i_stv = int(id_[0:nums[0]])
    j_stv = int(id_[nums[0]:nums[0]+nums[1]])
    i_mdl = int(id_[nums[0]+nums[1]:nums[0]+nums[1]+nums[2]])
    j_mdl = int(id_[nums[0]+nums[1]+nums[2]:nums[0]+nums[1]+nums[2]+nums[3]])
    i_chp = int(id_[nums[0]+nums[1]+nums[2]+nums[3]:nums[0]+nums[1]+nums[2]+nums[3]+nums[4]])
    j_chp = int(id_[nums[0]+nums[1]+nums[2]+nums[3]+nums[4]:nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]])
    i_pxl = int(id_[nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]:nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]+nums[6]])
    j_pxl = int(id_[nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]+nums[6]:nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]+nums[6]+nums[7]])
    
    pixel = det._matrice_staves[i_stv][j_stv]._matrice_modules[i_mdl][j_mdl]._matrice_chips[i_chp][j_chp]._matrice_pixels[i_pxl][j_pxl]
    res =pixel.hit_part_prec(cfg_detector, particule, prec - num_objet)
if __name__ == '__main__':
  import pickle
  
  
  def save_object(obj,filename):
    try:
        with open("/grid_mnt/data__DATA/data.lhcb/PRL/Files/"+filename+".pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
        
  
  def load_object(filename):
    try:
        with open("/grid_mnt/data__DATA/data.lhcb/PRL/Files/"+filename+".pickle", "rb") as f:
            return pickle.load(f)"""
    except Exception as ex:
        print("Error during unpickling object (Possibly unsupported):", ex)

  def find_object_from_id(id_, det):
    cfg = det._cfg
  
    nums = cfg._numerotation
    nums_i_stv = nums[0]
    nums_j_stv = nums[0]+nums[1]
    nums_i_mdl = nums[0]+nums[1]+nums[2]
    nums_j_mdl = nums[0]+nums[1]+nums[2]+nums[3]
    nums_i_chp = nums[0]+nums[1]+nums[2]+nums[3]+nums[4]
    nums_j_chp = nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]
    nums_i_pxl = nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]+nums[6]
    nums_j_pxl = nums[0]+nums[1]+nums[2]+nums[3]+nums[4]+nums[5]+nums[6]+nums[7]
    
    if id_ == "":
      return det
    
    if len(id_) == nums_j_stv:
      i_stv = id_[0,nums_i_stv]
      j_stv = id_[nums_i_stv,nums_j_stv]
      
      return det._matrice_staves[i_stv][j_stv]
      
    elif len(id_) == nums_j_mdl:
      i_stv = id_[0,nums_i_stv]
      j_stv = id_[nums_i_stv,nums_j_stv]
      i_mdl = id_[nums_j_stv,nums_i_mdl]
      j_mdl = id_[nums_i_mdl,nums_j_mdl]
      
      return det._matrice_staves[i_stv][j_stv]._matrice_modules[i_mdl][j_mdl]
      
    elif len(id_) == nums_j_chp:
      i_stv = id_[0,nums_i_stv]
      j_stv = id_[nums_i_stv,nums_j_stv]
      i_mdl = id_[nums_j_stv,nums_i_mdl]
      j_mdl = id_[nums_i_mdl,nums_j_mdl]
      i_chp = id_[nums_j_mdl,nums_i_chp]
      j_chp = id_[nums_i_chp,nums_j_chp]          
      
      return det._matrice_staves[i_stv][j_stv]._matrice_modules[i_mdl][j_mdl]._matrice_chips[i_chp][j_chp]
      
    elif len(id_) == nums_j_pxl:
      i_stv = id_[0,nums_i_stv]
      j_stv = id_[nums_i_stv,nums_j_stv]
      i_mdl = id_[nums_j_stv,nums_i_mdl]
      j_mdl = id_[nums_i_mdl,nums_j_mdl]
      i_chp = id_[nums_j_mdl,nums_i_chp]
      j_chp = id_[nums_i_chp,nums_j_chp]
      i_pxl = id_[nums_j_chp,nums_i_pxl]
      j_pxl = id_[nums_i_pxl,nums_j_pxl]
      
      return det._matrice_staves[i_stv][j_stv]._matrice_modules[i_mdl][j_mdl]._matrice_chips[i_chp][j_chp]._matrice_pixels[i_pxl][j_pxl]
      
    else:
      print("The id given is not a valuable id")    
 """
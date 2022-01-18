if __name__ == '__main__':
  import pickle
  
  
  def save_object(obj,filename):
    try:
        with open("/grid_mnt/data__DATA/data.lhcb/PRL/Files/"+filename+".pickle", "wb") as f:
            pickle.dump(obj, f, protocol=pickle.HIGHEST_PROTOCOL)
    except Exception as ex:
        print("Error during pickling object (Possibly unsupported):", ex)
        
  
  def load_object(filename):
    with open("/grid_mnt/data__DATA/data.lhcb/PRL/Files/"+filename+".pickle", "rb") as f:
      return pickle.load(f)
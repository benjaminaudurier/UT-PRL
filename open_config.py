if __name__ == '__main__':
  f = open("config.txt","r")
  lines = f.readlines()
  
  list_format = [(30,30),(50,150),(50,300)]
  format_pixel = list_format[int(lines[0][-3])]
  
  nb_ligne = int(lines[1][14:-2])
  nb_colonne = int(lines[2][16:-2]) 
  
  range_FTHits = (int(lines[3][11:-2]),int(lines[4][11:-2]))
  range_x = (int(lines[5][6:-2]),int(lines[6][6:-2]))
  range_y = (int(lines[7][6:-2]),int(lines[8][6:-2]))
  range_z = (int(lines[9][6:-2]),int(lines[10][6:]))
  
  print("Format = ", format_pixel)

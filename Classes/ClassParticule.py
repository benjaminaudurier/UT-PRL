import ROOT

class Particule:

  def __init__(self,tree,cfg_sz):
    list_x = []
    list_y = []
    list_eventNumber = []
    
    try:
      for entry in tree:
        if entry.nFThits > cfg_sz._min_FTHit and entry.nFThits < cfg_sz._max_FTHit and entry.HitUTZpos_0/10 > cfg_sz._min_z and entry.HitUTZpos_0/10 < cfg_sz._max_z:
          list_x.append(entry.HitUTXpos_0)
          list_y.append(entry.HitUTYpos_0)
          list_eventNumber.append(entry.eventNumber)
    
    except AttributeError:      
      for entry in tree:
        if entry.HitUTZpos_0/10 > cfg_sz._min_z and entry.HitUTZpos_0/10 < cfg_sz._max_z:
          list_x.append(entry.HitUTXpos_0)
          list_y.append(entry.HitUTYpos_0)
          list_eventNumber.append(entry.eventNumber)
      
    self._list_x = list_x
    self._list_y = list_y
    self._list_eventNumber = list_eventNumber
    
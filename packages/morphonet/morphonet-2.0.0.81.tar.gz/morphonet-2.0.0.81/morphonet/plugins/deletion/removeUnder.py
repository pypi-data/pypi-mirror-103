# -*- coding: latin-1 -*-
from morphonet.plugins import MorphoPlugin
import operator


class RemoveUnder(MorphoPlugin):
    """ This plugin remove opbjects under a certain volume in the segmented image
  
    Parameters
    ----------
    Voxel Size: int, default 20
        The volume under which objecs as to be remove
    """

    def __init__(self): #PLUGIN DEFINITION 
        MorphoPlugin.__init__(self) 
        self.set_name("Remove Under")
        self.add_inputfield("Voxel Size",default=20)
        self.add_dropdown("Time points",["Current time","All times"])
        self.set_parent("Remove objects")
       

    def process(self,t,dataset,objects): #PLUGIN EXECUTION
        if not self.start(t,dataset,objects,True):
            return None

        import numpy as np
        data = []
        if str(self.get_dropdown("Time points")) == "All times":
            data=dataset.get_all_seg()
            cell_volume = dataset.get_info("cell_volume", info_type="float")
            if data is not None:
                backup_time_list = []
                sorted_info = sorted(cell_volume.data.items(), key=lambda x: x[1][0].value)
                for cell in sorted_info:
                    if cell[1][0].value < float(self.get_inputfield("Voxel Size")) :
                        if dataset.begin <= cell[0].t <= dataset.end:
                            if not cell[0].t in backup_time_list:
                                dataset.backup(self.get_log(), t, objects, True, [cell[0].t,])
                                backup_time_list.append(cell[0].t)
                            coords = np.where(data[t] == cell[0].id)
                            self.print_mn("     ----->>>  delete object " + str(cell[0].id) + " at " + str(cell[0].t) + " with " + str(
                                len(coords[0])) + " pixels")
                            data[cell[0].t][coords] = dataset.background
                            dataset.del_link(cell[0])
                            dataset.set_seg(cell[0].t, data[cell[0].t])
                    else :
                        break
        else :
            data=dataset.get_seg(t)
            cell_volume = dataset.get_info("cell_volume", info_type="float")
            if data is not None:
                backup_time_list = []
                sorted_info = sorted(cell_volume.data.items(), key=lambda x: x[1][0].value)
                for cell in sorted_info:
                    if cell[1][0].value < float(self.get_inputfield("Voxel Size")):
                        if cell[0].t == t:
                            if not cell[0].t in backup_time_list:
                                dataset.backup(self.get_log(), t, objects, True, [t, ])
                                backup_time_list.append(t)
                            coords = np.where(data[t] == cell[0].id)
                            self.print_mn("     ----->>>  delete object " + str(cell[0].id) + " at " + str(
                                cell[0].t) + " with " + str(
                                len(coords[0])) + " pixels")
                            data[cell[0].t][coords] = dataset.background
                            dataset.del_link(cell[0])
                            dataset.set_seg(cell[0].t, data[cell[0].t])
                    else:
                        break
              
        self.restart() #ADD At the end 
         





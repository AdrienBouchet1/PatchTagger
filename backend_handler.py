import ImageHandler
import os 
import numpy as np
from PIL import Image,ImageTk

class BackendHandler: 


    def __init__(self): 

        self.__instantiate_variables()
        pass


    def __instantiate_variables(self): 
        
        self.folder=None
        self.Image=Image.fromarray(np.full((768,1280), fill_value=255,dtype=np.uint8))
        self.patch=Image.fromarray(np.full((128,128), fill_value=255,dtype=np.uint8))
      


    def list_dir(self): 

        list_=[os.path.join(self.folder,file) for file in os.listdir(self.folder) if not file.endswith("masks.png")]
        self.list_files=list_
        self.current_file_path=self.list_files[0]
        self.ImageHandler=ImageHandler.ImageHandler(self.current_file_path)
        self.current_pos=[0,0]
        self.Image,self.patch=self.ImageHandler.get_box_image_patch(self.current_pos)


    def __change_image(self, way : int):
        
        """
        way : sens ou on change (image suivante ou précédente)
        """

        assert way in [1,-1]
        self.current_file_path=self.list_files[self.list_files.index(self.current_file_path)+way]
        self.ImageHandler=ImageHandler.ImageHandler(self.current_file_path)
        self.current_pos=[0,0]
        self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)

    def change_patch(self, way : int):
        assert way in [1,-1]
        if way==1 : 
            if self.current_pos[1]<9:
                self.current_pos[1]=self.current_pos[1]+1
                self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)

            else: 
                if self.current_pos[0]<5 : 
                   self.current_pos[0]=self.current_pos[0]+1
                   self.current_pos[1]=0
                   self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)
        elif way==-1 : 

            if self.current_pos[1]>0:
                self.current_pos[1]=self.current_pos[1]-1
                self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)

            else: 
                if self.current_pos[0]>0 : 
                   self.current_pos[0]=self.current_pos[0]-1
                   self.current_pos[1]=9
                   self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)
        print("pos: ",self.current_pos)


            
            
                
                

        











        



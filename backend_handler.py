import ImageHandler
import os 
import numpy as np
from PIL import Image,ImageTk
import pandas as pd 
class BackendHandler: 


    def __init__(self): 

        self.__instantiate_variables()
        


    def __instantiate_variables(self): 
        
        self.folder=None
        self.Image=Image.fromarray(np.full((768,1280), fill_value=255,dtype=np.uint8))
        self.patch=Image.fromarray(np.full((128,128), fill_value=255,dtype=np.uint8))
        self.prepared_output=False
        self.available_categories=self.__instantiate_default_categories()


    

    def __instantiate_default_categories(self): 


        dict={

            1 : {"name" : "floue,liss pas structure","color":"#235fff"},
            2 : {"name" : "floue & microfibres","color":"#cf9511"},
            3 : {"name" : "gros trous","color":"#f51515"},
            4 : {"name" : "grosses fibres","color":"#42cf11"},
             5 : {"name" : "granuleux net","color":"#cd23ff"}
            
  


        }
        return dict


    def add_category(self,int_:int,name:str,color:str) : 
            assert int_ not in self.available_categories.keys()
            assert (type(int_)==int)
            assert (int_<10),"can't handle more than 9 categories"
            self.available_categories[int_]={"name" : name, "color" : color}
            


    def list_dir(self): 

        list_=[os.path.join(self.folder,file) for file in os.listdir(self.folder) if not file.endswith("masks.png")]
        self.list_files=list_
        self.current_file_path=self.list_files[0]
        self.ImageHandler=ImageHandler.ImageHandler(self.current_file_path)
        self.current_pos=[0,0]
        self.Image,self.patch=self.ImageHandler.get_box_image_patch(self.current_pos)


    def change_image(self, way : int):
        
        """
        way : sens ou on change (image suivante ou précédente)
        """


        assert way in [1,-1]
        self.current_file_path=self.list_files[self.list_files.index(self.current_file_path)+way]
        self.ImageHandler=ImageHandler.ImageHandler(self.current_file_path)
        self.current_pos=[0,0]
        self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)
        print("sortie de change_image")


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

    
    def change_Image_color(self, cat) : 

        assert cat in self.available_categories.keys()
        color=self.available_categories[cat]["color"]
        self.ImageHandler.change_color_patch(self.current_pos,color)
        self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)
        

    def prepare_output(self,path : str) : 
        
        self.output_dir=os.path.join(path,"PatchTagger_Output")
        self.category_df_path=os.path.join(self.output_dir,"categories.xlsx")
        if not os.path.exists(self.output_dir) : 
            os.makedirs(self.output_dir)

        if not os.path.exists(self.category_df_path): 

            self.df_category=pd.DataFrame({"Image_name" : [],"Image_path" : [],"patch_pos" : [], "x_min" : [],"x_max" : [],"y_min" : [],"y_max" : [],"category" : []})
            self.df_category.to_excel(self.category_df_path)
        
        else: 
            self.df_category=pd.read_excel(self.category_df_path)
        
        self.prepared_output=True

    
    


        

             


        







        


            
            
                
                

        











        



import ImageHandler
import os 
import numpy as np
from PIL import Image,ImageTk
import pandas as pd 
import json 


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
    def __load_previous_config(self,dict : dict): 

        self.available_categories={int(i):val for i,val in dict["available_categories"].items()}
        print("nouvelles cat",self.available_categories)

    
        

    def __save_current_base_config(self):
        
        JS={"available_categories" : self.available_categories}
        with open(os.path.join(self.config_dir, "config.json"),"w") as f: 
                json.dump(JS,f)



    def add_category(self,int_:int,name:str,color:str) : 
            
            assert int_ not in self.available_categories.keys()
            assert (type(int_)==int)
            assert (int_<10),"can't handle more than 9 categories"

            self.available_categories[int_]={"name" : name, "color" : color}
            with open(os.path.join(self.config_dir, "config.json"),"r")as f: 
                data = json.load(f)
            data["available_categories"]=self.available_categories
            with open(os.path.join(self.config_dir, "config.json"),"w")as f: 
                json.dump(data,f)
            

            


    def list_dir(self): 

        list_=[os.path.join(self.folder,file) for file in os.listdir(self.folder) if not file.endswith("masks.png")]
        self.list_files=list_
        self.current_file_path=self.list_files[0]
        self.ImageHandler=ImageHandler.ImageHandler(self.current_file_path,self.df_category,self.available_categories)
        self.current_pos=[0,0]
        self.Image,self.patch=self.ImageHandler.get_box_image_patch(self.current_pos)


    def change_image(self, way : int):
        
        """
        way : sens ou on change (image suivante ou précédente)
        """


        assert way in [1,-1]
        self.current_file_path=self.list_files[self.list_files.index(self.current_file_path)+way]
        self.ImageHandler=ImageHandler.ImageHandler(self.current_file_path,self.df_category,self.available_categories)
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

    
    def change_Image_color(self, cat) : 
        """
        En fait c'est aussi la méthode qui permet de catégoriser
        
        """
        assert cat in self.available_categories.keys()
        color=self.available_categories[cat]["color"]
        self.ImageHandler.change_color_patch(self.current_pos,color)
        self.patch,self.Image=self.ImageHandler.get_box_image_patch(self.current_pos)

        if not ((self.df_category["Image_name"]==self.ImageHandler.ImageName) & (self.df_category["patch_pos"]==str(self.current_pos))).any() : 
          
            x_min, x_max, y_min, y_max=self.ImageHandler.get_pos_coord(self.current_pos)
            self.df_category=pd.concat([self.df_category,pd.DataFrame({"Image_name" : [self.ImageHandler.ImageName],"Image_path" : [self.ImageHandler.path],"patch_pos" : [str(self.current_pos)], "x_min" : [x_min],"x_max" : [x_max],"y_min" : [y_min],"y_max" : [y_max],"category" : [cat]})])
            self.df_category.to_excel(self.category_df_path,index=False) ### Comme ça on enregistre A CHAQUE FOIS
        
        elif (self.df_category.loc[(self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos)),"category"] != cat).any():

            

             self.df_category.loc[(self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos)),"category"] = cat
             self.df_category.to_excel(self.category_df_path,index=False)
        else :
 
             self.df_category = self.df_category[~((self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos))&(self.df_category["category"] == cat))]
             self.df_category.to_excel(self.category_df_path,index=False)
            






        

    def prepare_output(self,path : str) : 
        
        self.output_dir=os.path.join(path,"PatchTagger_Output")
        self.category_df_path=os.path.join(self.output_dir,"categories.xlsx")
        self.config_dir=os.path.join(self.output_dir,"config")

        if not os.path.exists(self.output_dir) : 
            os.makedirs(self.output_dir)

        if not os.path.exists(self.category_df_path): 
            
            self.df_category=pd.DataFrame({"Image_name" : [],"Image_path" : [],"patch_pos" : [], "x_min" : [],"x_max" : [],"y_min" : [],"y_max" : [],"category" : []})
            self.df_category.to_excel(self.category_df_path,index=False)
            
        
        else: 
            self.df_category=pd.read_excel(self.category_df_path)
        
        self.prepared_output=True

        if not os.path.exists(self.config_dir) : 
            os.makedirs(self.config_dir)

        if not os.path.exists(os.path.join(self.config_dir, "config.json")): 
            with open(os.path.join(self.config_dir, "config.json"),"w") as f: 
                json.dump(dict(),f)
            self.__save_current_base_config()
        else : 
            with open(os.path.join(self.config_dir, "config.json"),"r")as f: 
                data = json.load(f)

            self.__load_previous_config(data)
        

                

        
            


    
    


        

             


        







        


            
            
                
                

        











        



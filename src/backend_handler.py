import ImageHandler
import os 
import numpy as np
from PIL import Image,ImageTk
import pandas as pd 
import json 
import ast


class BackendHandler:


    def __init__(self): 

        self.__instantiate_variables()
        


    def __instantiate_variables(self): 
        

        self.display_context=True
        self.list_files=None
        self.folder=None
        self.Image=Image.fromarray(np.full((384,640), fill_value=255,dtype=np.uint8))
        self.patch=Image.fromarray(np.full((128,128), fill_value=255,dtype=np.uint8))
        self.prepared_output=False
        self.available_categories=self.__instantiate_default_categories()


    

    def __instantiate_default_categories(self): 


        # dict={

        #     1 : {"name" : "floue,liss pas structure","color":"#235fff"},
        #     2 : {"name" : "floue & microfibres","color":"#cf9511"},
        #     3 : {"name" : "gros trous","color":"#f51515"},
        #     4 : {"name" : "grosses fibres","color":"#42cf11"},
        #      5 : {"name" : "granuleux net","color":"#cd23ff"}

        # }

        # dict={

            
        #     1 : {"name" : "Ultra lisse","color":"#F2C458"},
        #     2 : {"name" : "lisse, plat, irrégulier","color":"#a68108"},
        #     3 : {"name" : "poilu","color":"#6ef07d"},
        #     4 : {"name" : "Grosses fibres désordonnées","color":"#099406"},
        #     5: {"name" : "Grosses fibres qui font stries","color":"#235fff"},
        #     6 : {"name" : "texture ouatée","color":"#ed73df"},
        #     7: {"name" : "Granuleux Fort","color":"#dc22dc"},
        #     8 : {"name" : "Stratifié ordonné régulier","color":"#ff8223"},
        #     9 : {"name" : "gros trous","color":"#e10017"},
             
        # }


        dict={

            
            1 : {"name" : "Totalement homogène","color":"#F2C458","key" : "a" },
            2 : {"name" : "Plutôt homogène","color":"#a68108","key" : "z" },
            3 : {"name" : "Faisceaux","color":"#6ef07d","key" : "e"},
            4 : {"name" : "Filaments","color":"#099406","key" : "r"},
            5: {"name" : "Stratifié rectiligne","color":"#235fff","key" : "t"},
            6 : {"name" : "Stratifié rectiligne","color":"#ed73df","key" : "y"},
            7: {"name" : "Granuleux","color":"#dc22dc","key" : "u"},
            8 : {"name" : "Sableux","color":"#ff8223","key" : "q"},
            9 : {"name" : "Trou","color":"#e10017","key" : "s"},
             10: {"name" : "Bactéries","color":"#dc22dc","key" : "d"},
            11 : {"name" : "(portion de) Cellule","color":"#2a2725","key" : "f"},
            12 : {"name" : "Calcification","color":"#480f44","key" : "g"},
            13 : {"name" : "Trou","color":"#e8e7e7","key" : "h"},
            
             
        }

        return dict
    def __load_previous_config(self,dict : dict): 

        self.available_categories={int(i):val for i,val in dict["available_categories"].items()}
        #print("nouvelles cat",self.available_categories)

    
        

    def __save_current_base_config(self):
        
        JS={"available_categories" : self.available_categories}
        with open(os.path.join(self.config_dir, "config.json"),"w") as f: 
                json.dump(JS,f)



    def add_category(self,int_:int,name:str,color:str) : 
            """
            
            
            
            """

            assert 1==2,"L'ajout de catégorie n'est plus fonctionnel, ajouter la possibilité de sélectionner les raccourcis claviers pour cela"
            
            assert int_ not in self.available_categories.keys()
            assert (type(int_)==int)
            #assert (int_<10),"can't handle more than 9 categories"

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
        #print("pos: ",self.current_pos)

    
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
            self.df_category=pd.concat([self.df_category,pd.DataFrame({"Image_name" : [self.ImageHandler.ImageName],"Image_path" : [self.ImageHandler.path],"patch_pos" : [str(self.current_pos)], "x_min" : [x_min],"x_max" : [x_max],"y_min" : [y_min],"y_max" : [y_max],"category" : [cat],"with-context": self.display_context})])
            self.df_category.to_excel(self.category_df_path,index=False) ### Comme ça on enregistre A CHAQUE FOIS
        
        elif (self.df_category.loc[(self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos)),"category"] != cat).any():

             self.df_category.loc[(self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos)),"category"] = cat
             self.df_category.loc[(self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos)),"with-context"] = self.display_context
             self.df_category.to_excel(self.category_df_path,index=False)
        else :
 
             self.df_category = self.df_category[~((self.df_category["Image_name"] == self.ImageHandler.ImageName) &(self.df_category["patch_pos"] == str(self.current_pos))&(self.df_category["category"] == cat))]
             self.df_category.to_excel(self.category_df_path,index=False)
            


    def save_patches(self,mask_extension): 
        
        df_mapping=pd.DataFrame()
        if not self.prepared_output : 
            print("Select an output folder before")
        elif self.list_files is None : 
            print("Select a data folder")
            
            
        else :
            folder_cat=os.path.join(self.output_dir,"patches")
            if not os.path.exists(folder_cat) : 
                os.makedirs(folder_cat) 
                
            for cat in self.available_categories.keys() :
                path_cat=os.path.join(folder_cat,"{}".format(cat))
                if not os.path.exists(path_cat) : 
                    os.makedirs(path_cat)
            full_image_folder=os.path.join(self.output_dir,"full_images")
            if not os.path.exists(full_image_folder) : 
                os.makedirs(full_image_folder)

            
                
            for image_path in self.list_files :

                subset_df=self.df_category.loc[self.df_category["Image_path"]==image_path]
                image_handler=ImageHandler.ImageHandler(image_path,self.df_category,self.available_categories,"_cp_masks.png")
                image_handler.load_mask()
                
                full_img_name=image_handler.ImageName

                if subset_df.shape[0] != 0 :
                        
                    img=image_handler.get_image_classified().convert("RGB")
                    
                    img.save(os.path.join(full_image_folder,full_img_name))

                
                
                for index,row in subset_df.iterrows() :
                    
                    pos,cat=tuple(ast.literal_eval(row["patch_pos"])),int(row["category"])
                    image,mask=image_handler.get_patch_patchMask(pos)
                    image_name="{}_({}_{}).tif".format(row["Image_name"].split(".tif")[0],pos[0],pos[1])
                    image.save(os.path.join(folder_cat,str(cat),image_name))
                    
                    mask_name="{}{}_({}_{}).{}".format(row["Image_name"].split(".tif")[0],mask_extension.split(".")[0],pos[0],pos[1],mask_extension.split(".")[1])
                    print("mask_name : {}, mask.size : {}".format(mask_name,np.array(mask).shape))
                    mask.save(os.path.join(folder_cat,str(cat),mask_name))

                    df_mapping=pd.concat([df_mapping,pd.DataFrame({"Image" : [os.path.join(folder_cat,str(cat),image_name)],"Mask" : [os.path.join(folder_cat,str(cat),mask_name)],"category" : [int(row["category"])]})])


        df_mapping.to_excel(os.path.join(self.output_dir,"mapping.xlsx"),index=False)


    def get_image_name(self) :
        
        return self.ImageHandler.ImageName
    
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
        

                

        
            


    
    


        

             


        







        


            
            
                
                

        











        



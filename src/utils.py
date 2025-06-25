
import os
import pandas as pd 
from ImageHandler import ImageHandler
from PIL import Image
import numpy as np

class Dataset_Extractor: 


    def __init__(self,input_folder,classif_df,output_folder,output_patch_size):

        assert os.path.isdir(input_folder), "le dossier d'input sélectionné n'existe pas"
        assert os.path.exists(classif_df),"le fichier de classif n'existe pas"

        self.input_folder=input_folder
        self.classif=pd.read_excel(classif_df)

        self.output_folder=output_folder
        self.output_patch_size=output_patch_size
        self.__prepare_output_folder()
        self.available_cat= dict={

            
            1 : {"name" : "Totalement homogène","color":"#6558F2","key" : "a", "vignette": "TotalementHomogene.tif" },
            2 : {"name" : "Plutôt homogène","color":"#7d12d4","key" : "z", "vignette": "PlutotHomogene.tif" },
            3 : {"name" : "Faisceaux","color":"#6ef07d","key" : "e", "vignette":"FibreuxFaisceaux.tif"},
            4 : {"name" : "Filaments","color":"#099406","key" : "r", "vignette":"FibreuxFilaments.tif"},
            5: {"name" : "Stratifié rectiligne","color":"#e409f7","key" : "t", "vignette":"StratifieRectiligne.tif"},
            6 : {"name" : "Stratifié sinueux","color":"#a9399c","key" : "y", "vignette":"StratifieSinueux.tif"},
            7: {"name" : "Granuleux","color":"#b55e07","key" : "u", "vignette":"Granuleux-Epais.tif"},
            8 : {"name" : "Sableux","color":"#ebcf6a","key" : "q", "vignette":"GranuleuxFinSable.tif"},
            9 : {"name" : "Trou","color":"#e10017","key" : "s", "vignette":"trou.tif"},
             10: {"name" : "Bactéries","color":"#03f4f8","key" : "d", "vignette":"bacterie.tif"},
            11 : {"name" : "(portion de) Cellule","color":"#2ba57e","key" : "f", "vignette":"CelluleOuPartieDeCellule.tif"},
            12 : {"name" : "Calcification","color":"#a0a0a0","key" : "g", "vignette":"calcification.tif"},
            13 : {"name" : "Nd","color":"#e8e7e7","key" : "h", "vignette":"nd.tif"},
            
             
        }

    def extract_patch(self,image_path,output_patch_size : int=256, input_patch_size : int=128) : 

        """
        
        """
        assert output_patch_size in [256,512]
        assert input_patch_size==128,"il faut implémenter la prise en compte de patchs classifiés d'une taille différente" 
    
        ImH=ImageHandler(path=image_path,df_category=self.classif,available_categories=self.available_cat)
        img_name=ImH.ImageName
        color_full_img=ImH.get_image_classified()
        img_df=self.__get_subset_df(img_name)
        img=Image.open(image_path)
        imgArray=np.array(img)
        mask=np.full(shape=imgArray.shape,fill_value=13,dtype=np.uint8)
        mask=self.__fill_mask(mask,img_df)
        if mask is not None : ### Si __fill_mask renvoie none, tous les patchs n'avaient pas été clasifiés

            if output_patch_size==256: 
                
                n_rows,n_cols=3,5
        
            height, width = imgArray.shape

            assert height % n_rows == 0, f"Hauteur de l'image ({height}) non divisible par {n_rows}"
            assert width % n_cols == 0, f"Largeur de l'image ({width}) non divisible par {n_cols}"

            patch_h = height // n_rows
            patch_w = width // n_cols

            patch_dict = {}

            for i in range(n_rows):
                for j in range(n_cols):
                    x_min = i * patch_h
                    x_max = x_min + patch_h
                    y_min = j * patch_w
                    y_max = y_min + patch_w

                    patch = Image.fromarray(imgArray[x_min:x_max, y_min:y_max])  
                    print("type !!!!!!!!",type(mask))
                    mask_=Image.fromarray(mask[x_min:x_max, y_min:y_max])
                    colored_image=Image.fromarray(np.array(color_full_img)[x_min:x_max, y_min:y_max])

                    patch.save(os.path.join(self.img_path,"{}_{}_{}.tif".format(img_name.split(".tif")[0],i,j)))
                    mask_.save(os.path.join(self.mask_path,"{}_{}_{}.png".format(img_name.split(".tif")[0],i,j)))
                    
                    colored_image.save(os.path.join(self.colored_path,"colored_{}_{}_{}.png".format(img_name,i,j)))

        else :
            pass

    def process_all_images(self): 

        list_img=os.listdir(self.input_folder)


        for im in list_img : 
            print("ok1")
            if im.endswith(".tif"): 
                print("ok2")
                self.extract_patch(os.path.join(self.input_folder,im),output_patch_size=self.output_patch_size)

    def __prepare_output_folder(self): 

        self.mask_path=os.path.join(self.output_folder,"raw","labels")
        self.img_path=os.path.join(self.output_folder,"raw","images")
        self.colored_path=os.path.join(self.output_folder,"raw","colored")
        if not os.path.isdir(self.mask_path) :
            os.makedirs(self.mask_path)
        else:  
            raise ("mask path existe déja")
        if not os.path.isdir(self.img_path) :
            os.makedirs(self.img_path)
        else:  
            raise ("img path existe déja")
        
        if not os.path.isdir(self.colored_path) :
            os.makedirs(self.colored_path)
        else:  
            raise ("colored path existe déja")
    def __get_subset_df(self,name : str) :


        subset_df=self.classif[self.classif["Image_name"]==name]
        return subset_df
    

    def __fill_mask(self,mask,df : pd.DataFrame): 

        if df.shape[0]!=60 : 
            print(df.shape)
            return None

        for index,row in df.iterrows(): 
            x_min,x_max,y_min,y_max=row["y_min"],row["y_max"],row["x_min"],row["y_max"] ### ATTENTION : Confusion dans le tableau excel
            mask[x_min:x_max,y_min:y_max]=row["category"]

        return mask





        
        





if __name__=="__main__" : 

        #DE=Dataset_Extractor(input_folder="/home/adrienb/Documents/Adrien/datasets/New_dataset/Dataset_commun_en_forme/commun",classif_df="/home/adrienb/Téléchargements/160625-JPB-Adrien/JP-OUTPUT-COMMUN/PatchTagger_Output/categories.xlsx",output_folder="/home/adrienb/Documents/Adrien/datasets/New_dataset/DataSet_256_256_classif_128_128")
        DE=Dataset_Extractor(input_folder="/home/adrienb/Documents/Adrien/datasets/New_dataset/Dataset_commun_en_forme/commun",classif_df="/home/adrienb/Documents/Adrien/datasets/New_dataset/Dataset_commun_en_forme/Output/PatchTagger_Output/categories.xlsx",output_folder="/home/adrienb/Documents/Adrien/datasets/New_dataset/DataSet_256_256_classif_128_128",output_patch_size=256)
        DE.process_all_images()



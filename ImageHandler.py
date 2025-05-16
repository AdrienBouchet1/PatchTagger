
from PIL import Image,ImageDraw,ImageTk
import numpy as np 
import copy
import os 
import pandas as pd 
import ast

class ImageHandler : 

    def __init__(self,path,df_category,available_categories,extension_mask:str=None): 
        """
        On considère que des images en 768x1280, avec du crop en 128x128
        
        """
        self.path=path
        self.ImageName=os.path.basename(self.path)
        self.extension_mask=extension_mask
        self.df_state=df_category.loc[df_category["Image_name"] == self.ImageName]
        print("à l'init: le df du handler est : {}".format(self.df_state) )
        self.available_categories=available_categories
        self.__open_image()
        self.__load_previous_categories()
    
    def  __load_previous_categories(self): 
         
         for index,row in self.df_state.iterrows() : 
        
              pos=tuple(ast.literal_eval(row["patch_pos"]))
              self.change_color_patch(pos,self.available_categories[row["category"]]["color"])
        
         


    def get_pos_coord(self, pos) : 
         (x_min, x_max, y_min, y_max) = tuple(self.image_patches_[tuple(pos)]["pos"])
         return x_min, x_max, y_min, y_max

    def __open_image(self) : 

        self.image=Image.open(self.path)
     
        self.im_array=np.array(self.image)

        assert self.im_array.shape==(768,1280), "the image must be of size 768x1280"
        self.image_patches_=self.__get_image_patches()
        
        

    def __get_image_patches(self,n_rows=6,n_cols=10) : 

        

            assert self.im_array.ndim == 2, "L'image doit être en 2D (grayscale)"
            height, width = self.im_array.shape

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

                    patch = Image.fromarray(self.im_array[x_min:x_max, y_min:y_max])
                    patch_dict[(i, j)] = {
                        'pos': (x_min, x_max, y_min, y_max),
                        'patch': patch
                    }
         
            return patch_dict

    def __draw_patch_box(self, tuple_coord: tuple) : 
         
         
         image=self.image.copy().convert("RGB")
         draw = ImageDraw.Draw(image)
   
         (x_min, x_max, y_min, y_max) = tuple_coord
         draw.rectangle([y_min, x_min, y_max, x_max], outline="red", width=2)


         return image
    
    def load_mask(self) : 
         """
         
         """
         extension_mask=self.extension_mask
         if extension_mask is not None : 
              image_pth=os.path.splitext(self.path)[0]
              mask_full_path="{}{}".format(image_pth,extension_mask)
              if os.path.exists(mask_full_path) : 
                   self.mask_type="original"
                   self.mask=np.array(Image.open(mask_full_path))
             
         else: 
               self.mask_type="new"      

         if self.mask_type=="new": 
              shape=np.array(self.im_array.shape)
              self.mask=np.full(shape=shape,fill_value=1)

         
    
          
    def get_patch_patchMask(self,pos: tuple): 

        patch=self.image_patches_[tuple(pos)]["patch"]
        x_min, x_max, y_min, y_max=self.image_patches_[tuple(pos)]["pos"]
        print("tout d'abord:  shape : {}".format((self.mask[x_min:x_max,y_max:y_max].shape)))
        mask_patch=Image.fromarray(self.mask[x_min:x_max,y_min:y_max])

        return patch,mask_patch
         


    def get_box_image_patch(self,pos : tuple):
         
         
         patch=self.image_patches_[tuple(pos)]["patch"]
         #patch_tk=ImageTk.PhotoImage(patch)
         boxed_image=self.__draw_patch_box(self.image_patches_[tuple(pos)]["pos"]).resize((640,384))
         #boxed_image_tk=ImageTk.PhotoImage(boxed_image)
         return patch, boxed_image   

        
    def change_color_patch(self,pos,color): 
      
        self.image=self.image.convert("RGBA")
        if "color" in self.image_patches_[tuple(pos)].keys():
             
             x_min, x_max, y_min, y_max=self.image_patches_[tuple(pos)]["pos"]
             original_patch=np.stack((np.array(self.image_patches_[tuple(pos)]["patch"]),)*3,axis=-1) ##Passage en RGB
             alpha=np.full((original_patch.shape[0], original_patch.shape[1], 1), 255, dtype=np.uint8)
             
             original_patch=np.concatenate((original_patch,alpha ), axis=-1)
             tab_image=np.array(self.image)
             tab_image[x_min:x_max,y_min:y_max]=original_patch
         
             self.image=Image.fromarray(tab_image)
               
             if self.image_patches_[tuple(pos)]["color"] == color : 
                del self.image_patches_[tuple(pos)]["color"]
                return 
     
        

        self.image_patches_[tuple(pos)]["color"]=color
        self.image=self.image.convert("RGBA")
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        opacity = int(0.3 * 255)
      
        (y_min, y_max, x_min, x_max) = tuple(self.image_patches_[tuple(pos)]["pos"])
        overlay = Image.new("RGBA", (x_max - x_min, y_max - y_min), rgb + (opacity,))

        # Appliquer l'overlay sur l'image
        self.image.paste(overlay, (x_min, y_min), overlay)








    



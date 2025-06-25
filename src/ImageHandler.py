
from PIL import Image,ImageDraw,ImageTk,ImageFont
import numpy as np 
import copy
import os 
import pandas as pd 
import ast


class ImageHandler : 

    def __init__(self,path,df_category,available_categories,extension_mask:str=None,patch_size : tuple =(256,256)): 
        """
        On considère que des images en 768x1280, avec du crop en 128x128
        
        """
        self.path=path
        self.ImageName=os.path.basename(self.path)
        self.extension_mask=extension_mask
        self.df_state=df_category.loc[df_category["Image_name"] == self.ImageName]
        #print("à l'init: le df du handler est : {}".format(self.df_state) )
        self.available_categories=available_categories
        self.__open_image()
        self.__load_previous_categories()
        self.patch_size=patch_size

    def  __load_previous_categories(self): 
         
         for index,row in self.df_state.iterrows() : 
        
              pos=tuple(ast.literal_eval(row["patch_pos"]))
              self.change_color_patch(pos,self.available_categories[row["category"]]["color"])
        
    def get_image_classified(self) : 

          return self.image     
     

    def get_pos_coord(self, pos) : 
         (x_min, x_max, y_min, y_max) = tuple(self.image_patches_[tuple(pos)]["pos"])
         return x_min, x_max, y_min, y_max

    def __open_image(self) : 

        self.image=Image.open(self.path)
     
        self.im_array=np.array(self.image)

        assert self.im_array.shape==(768,1280), "the image must be of size 768x1280"
        self.image=self.__add_ScaleBar(self.image)
        self.image_patches_=self.__get_image_patches()
        
     


    def __add_ScaleBar(self,image): 
         
          """ Fonction faite par ChatGpt
          """
 
          #### ATTENTION : Ces échelles sont spécifiques
          px_per_nm = 1 / 24.8        # pixels par nm 
          px_per_um = px_per_nm * 1000  # pixels par µm
          bar_length_um = 10
          bar_length_px = int(px_per_um * bar_length_um) 
          margin = 30
          bar_height = 8


          draw = ImageDraw.Draw(image)

          x2 = image.width - margin
          y2 = image.height - margin
          x1 = x2 - bar_length_px
          y1 = y2 - bar_height

          draw.rectangle([x1, y1, x2, y2], fill="white")
          
          base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
          font_path=os.path.join(base_dir,"src","OpenSans-VariableFont_wdth,wght.ttf")
          font = ImageFont.truetype(font_path, 40)


          text = f"{bar_length_um} µm"


          bbox = draw.textbbox((0, 0), text, font=font)
          text_width = bbox[2] - bbox[0]
          text_height = bbox[3] - bbox[1]

          text_x = x1 + (bar_length_px - text_width) // 2
          text_y = y1 - text_height - 15

          
          draw.text((text_x, text_y), text, fill="white", font=font)

          return image

        



    def __get_image_patches(self,n_rows=6,n_cols=10) : 

            """
            Permet de récupérer les patch ses infors

            """
        

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
              self.mask=np.full(shape=shape,fill_value=1,dtype=np.uint8)

         
    
          
    def get_patch_patchMask(self,pos: tuple): 

        patch=self.image_patches_[tuple(pos)]["patch"]
        x_min, x_max, y_min, y_max=self.image_patches_[tuple(pos)]["pos"]

        #print("tout d'abord:  shape : {}".format((self.mask[x_min:x_max,y_min:y_max])))
        mask_patch=Image.fromarray(self.mask[x_min:x_max,y_min:y_max])

        return patch,mask_patch
         


    def get_box_image_patch(self,pos : tuple):
         """
         C'est ici qu'on redimensionne l'image de patch pour l'avoir en + gros
         
         """



         
         patch=self.image_patches_[tuple(pos)]["patch"]
         patch=patch.resize(self.patch_size,Image.NEAREST)

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








    



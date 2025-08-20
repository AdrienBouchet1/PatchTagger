

import pandas as pd 


import numpy as np 



class transformator : 


    def __init__(self,input_path : str, output_path : str): 


        self.input=pd.read_excel(input_path)
        self.output_path=output_path

        self.output=pd.DataFrame()

    def transform_line(self, row):


            dic={"Image_name" : [], "Image_path" : [],"patch_pos" : [],"category" : [] , "with-context" : [],"x_min" : [],"x_max" : [],"y_min" : [],"y_max" : []} 

            for i in range(4): 
                 for j in range(4) : 
                    l=int(row["patch_pos"].split("[")[1].split(",")[0])*4 + i
                    c=int(row["patch_pos"].split("]")[0].split(",")[1])*4 + j
                    dic["Image_name"].append(row["Image_name"])
                    dic["Image_path"].append(row["Image_path"])
                    dic["patch_pos"].append("[{}, {}]".format(l,c))
                    dic["category"].append(row["category"])
                    dic["with-context"].append(row["with-context"])
                    dic["x_min"].append(None)
                    dic["x_max"].append(None)
                    dic["y_min"].append(None)
                    dic["y_max"].append(None)

  
            return  dic
    


    def process_all_lines(self) : 
         


         for index,row in self.input.iterrows() : 
              
            dic=self.transform_line(row)
            self.output=pd.concat([self.output,pd.DataFrame(dic)])



              





    def __call__(self): 

        self.process_all_lines()
        self.output.to_excel(self.output_path)




if __name__=="__main__": 


    p1="/home/abouchet/Documents/Datasets/Remontage_Dossier_JP/Classif_JeanPierre/Merge/PatchTagger_Output_1/categories.xlsx"
    p2="/home/abouchet/Documents/Datasets/Remontage_Dossier_JP/Classif_JeanPierre/Merge/PatchTagger_Output_1/categories_32.xlsx"

    t=transformator(p1,p2)
    t()
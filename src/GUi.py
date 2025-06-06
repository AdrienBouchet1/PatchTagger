import tkinter
from tkinter import colorchooser
from tkinter import ttk
import tkinter.filedialog
import backend_handler
from PIL import ImageTk,Image
import styles
import sv_ttk



class loader : 

    def __init__(self) : 
        super().__init__()
        self.backend_handler=backend_handler.BackendHandler()
        #print("au départ, les catégories sont : {} ".format(self.backend_handler.available_categories))
        self.__instantiate()
        
        

    def __instantiate(self):    
    
        
        self.root=tkinter.Tk()
        self.root.resizable(False,False)
        styles.apply_styles()
        self.root.title("PatchTagger")
        self.notebook=ttk.Notebook(self.root,style='notebook2.TNotebook')
        self.notebook.grid(row=0,column=0)
        self.notebook.add(main_window(self.notebook,backend_handler=self.backend_handler),text="main")
        self.notebook.add(config_window(self.notebook,backend_handler=self.backend_handler),text="settings")
    

        

        self.notebook.bind("<<NotebookTabChanged>>", self.__on_tab_change)
        

        

    def __call__(self) : 
        
        self.root.mainloop()

    def __on_tab_change(self, event):
      
  
        selected_tab = event.widget.select()
        tab_frame = event.widget.nametowidget(selected_tab)
        if self.backend_handler.prepared_output: ### De la sorte on peut rien faire si on n'a rien fait
            tab_frame.focus_set()



class main_window(tkinter.Frame) : 

    def __init__(self, master,backend_handler) : 
        super().__init__(master) 
        
        self.backend_handler=backend_handler
        self.__instantiate()
        self.__grid_components()

        



    def __instantiate(self): 
        

        #styles.apply_styles()

        self.left_frame=ttk.Frame(master=self,style="tab_1.TFrame")
        self.right_frame=ttk.Frame(master=self,style="tab_1.TFrame")
        self.categories_frame=ttk.Frame(master=self.right_frame,style="tab_1.TFrame")

        self.fvar=tkinter.StringVar()
        self.fvar.set("None")
        


        self.lab_main_image=ttk.Label(master=self.left_frame)
        self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
        self.lab_main_image["image"]=self.main_image
        self.bind("<Right>",lambda e:  self.__change_patch_pos(e, 1))
        self.bind("<Left>",lambda e:  self.__change_patch_pos(e, -1))

        
        
        self.next_image_button=ttk.Button(master=self.left_frame,text="Image suivante",command= lambda : self.__change_image(None,1))
        self.previous_image_button=ttk.Button(master=self.left_frame,text="Image précédente",command= lambda : self.__change_image(None,-1))
        self.bind("<Shift-Right>",lambda e:  self.__change_image(e, 1))
        self.bind("<Shift-Left>",lambda e: self.__change_image(e, -1))
       
        self.name_imageVar=tkinter.StringVar()
        self.name_imageVar.set("Current image : None")

        self.name_image_lab=ttk.Label(master=self.left_frame, textvariable=self.name_imageVar)

        self.context_checkvar=tkinter.BooleanVar()
        self.context_checkvar.set(True)
        self.lab_hide_context=ttk.Label(master=self.left_frame,text="Cacher le context")
        self.hide_context_checkbox=ttk.Checkbutton(master=self.left_frame,variable=self.context_checkvar,command=self.__on_check_hide_context)

        
        self.lab_patch=ttk.Label(master=self.left_frame)
        self.patch= ImageTk.PhotoImage(self.backend_handler.patch)
        self.lab_patch["image"]=self.patch
        self.bind("<Right>",lambda e:  self.__change_patch_pos(e, 1))
        self.bind("<Left>",lambda e:  self.__change_patch_pos(e, -1))

        # self.bind("<KP_1>", lambda e:self.__classify_patch(e,1) )
        # self.bind("<KP_2>", lambda e:self.__classify_patch(e,2) )
        # self.bind("<KP_3>", lambda e:self.__classify_patch(e,3) )
        # self.bind("<KP_4>", lambda e:self.__classify_patch(e,4) )
        # self.bind("<KP_5>", lambda e:self.__classify_patch(e,5) )
        # self.bind("<KP_6>", lambda e:self.__classify_patch(e,6) )
        # self.bind("<KP_7>", lambda e:self.__classify_patch(e,7) )
        # self.bind("<KP_8>", lambda e:self.__classify_patch(e,8) )
        # self.bind("<KP_9>", lambda e:self.__classify_patch(e,9) )
    


         ### Frame de visualisation des catégories instanciées
        
        self.__maj_categorie_frame()
        self.categories_title=ttk.Label(master=self.categories_frame,text="Catégories disponibles",style="title_.TLabel")
        self.button_refresh_cat=ttk.Button(master=self.categories_frame, text="Refresh categories", comman=self.__maj_categorie_frame )
        sv_ttk.set_theme("dark")
        

    def __maj_categorie_frame(self) : 
        
        self.vignettes=list()
        self.lab_keyboard=ttk.Label(master=self.categories_frame,text="Clavier")
        dic_classes=self.backend_handler.available_categories 
        for index,(key,dic) in enumerate(dic_classes.items())  : 

            #lab1=ttk.Label(master=self.categories_frame,text="{} : {}".format(key,dic["name"]),style="category_label.TLabel")
            #lab1.grid(row=index+2,column=0,sticky="we")

            but1=ttk.Button(master=self.categories_frame,text=dic["name"],command=lambda key=key :(self.__classify_patch(None,key),self.focus_set()))
            but1.grid(row=index+2,column=1)
            self.bind(dic["key"], lambda e,key=key:self.__classify_patch(e,key) )

            lab1=ttk.Label(master=self.categories_frame,text="{}".format(dic["key"]))
            lab1.grid(row=index+2,column=2)
            v_pil=Image.open(dic["vignette"])
            v_pil=v_pil.resize((45,45))
            v=ImageTk.PhotoImage(v_pil)
            self.vignettes.append(v)


            #### Ces deux lignes ne sont pas compatibles MacOs
            # lab_v=ttk.Label(master=self.categories_frame,image=self.vignettes[-1])
            # lab_v.grid(row=index+2,column=3,pady=10,padx=10)



            color_label = tkinter.Label(self.categories_frame, bg=dic["color"], width=4, height=2, relief="solid", bd=1)
            color_label.grid(row=index+2,column=0)

            
        print(dic_classes)
        
            


        self.focus_set()


    def __classify_patch(self,event,cat) : 
        """
        
        """
         
        if self.backend_handler.prepared_output :
            if cat in self.backend_handler.available_categories :  
                #print("avant classification, cats disops : {}".format(self.backend_handler.available_categories))
                self.backend_handler.change_Image_color(cat)
                self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
                self.lab_main_image.config(image=self.main_image)
                self.lab_main_image.image=self.main_image

                self.patch= ImageTk.PhotoImage(self.backend_handler.patch)
                self.lab_patch.config(image=self.patch)
                self.lab_patch.image=self.patch
            
            else : 
                print("cat {} not recognized".format(cat) )
        else: 
        
                print("Configure output before")


    


    def __grid_components(self) : 

        """
        """

        self.left_frame.grid(row=0,column=0,rowspan=3)
        self.right_frame.grid(row=0,column=1,rowspan=1)

        self.categories_frame.grid(row=3,column=0, columnspan=8,pady=(50,50))

        self.lab_main_image.grid(row=1,column=0,columnspan=10)
        self.name_image_lab.grid(row=2,column=1,columnspan=7)
        self.lab_patch.grid(row=3,column=3)



        self.next_image_button.grid(row=0,column=7)
        self.previous_image_button.grid(row=0,column=4)

        self.lab_hide_context.grid(row=0,column=0,columnspan=2)
        self.hide_context_checkbox.grid(row=0,column=3)

        
        self.categories_title.grid(row=0,column=0,pady=30,padx=20)
        self.lab_keyboard.grid(row=0,column=2,padx=30)

        ##self.button_refresh_cat.grid(row=0,column=0)
        

    def __on_check_hide_context(self) : 

        var=self.context_checkvar.get()
        if var : 
             self.lab_main_image.grid()
             self.backend_handler.display_context=True
    
        else : 
             self.lab_main_image.grid_remove()
             self.backend_handler.display_context=False
        self.focus_set()
        


    def __change_patch_pos(self,event,way) : 
        """
        
        """
        if self.backend_handler.prepared_output :
        
                self.backend_handler.change_patch(way)
                self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
                self.lab_main_image.config(image=self.main_image)
                self.lab_main_image.image=self.main_image

                self.patch= ImageTk.PhotoImage(self.backend_handler.patch)
                self.lab_patch.config(image=self.patch)
                self.lab_patch.image=self.patch
                
                self.focus_set()
        else : 
            print("configure output before")
        
    def __change_image(self,Event,way) : 

        if self.backend_handler.prepared_output :
                self.backend_handler.change_image(way)

                self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
                self.lab_main_image.config(image=self.main_image)
                self.lab_main_image.image=self.main_image
                self.patch= ImageTk.PhotoImage(self.backend_handler.patch)

                self.lab_patch.config(image=self.patch)
                self.lab_patch.image=self.patch

                self.name_imageVar.set(self.backend_handler.get_image_name())
                self.focus_set()

                
        else :
            print("configure output before")


class config_window(tkinter.Frame) : 


    def __init__(self,master,backend_handler) : 
        
        
        self.backend_handler=backend_handler
        super().__init__(master)
        self.__instantiate()
        self.__grid_components()

    

    def __instantiate(self) :
        ### Les frames principales du notebook
        self.add_categories_frame=ttk.Frame(master=self) 
        self.folder_selection_frame=ttk.Frame(master=self)
        self.saving_patches_frame=ttk.Frame(master=self)


        ### Frame de sélection du dossier
        self.button_folder_selection=tkinter.Button(master=self.folder_selection_frame,text="sélectionner un dossier",command=self.__folder_selection)
        
        self.folder_var=tkinter.StringVar()
        self.folder_var.set("Selected data folder : None")
        self.folder_label=tkinter.Label(master=self.folder_selection_frame,textvariable=self.folder_var,wraplength=200)

        self.output_folder_var=tkinter.StringVar()
        self.output_folder_var.set("Selected output folder : None")
        self.output_folder_label=tkinter.Label(master=self.folder_selection_frame,textvariable=self.output_folder_var,wraplength=200)
        self.button_output_folder_selection=tkinter.Button(master=self.folder_selection_frame,text="sélectionner un dossier d'output",command=self.__output_folder_selection)

        ### Frame d'ajout de catégorie
        self.entry_cat_name=tkinter.StringVar()
        self.entry_cat_name.set("Nom de la classe")
        self.cat_name_entry=tkinter.Entry(master=self.add_categories_frame,textvariable=self.entry_cat_name)
        self.colorselector=ttk.Button(master=self.add_categories_frame,text="Sélectionner une couleur",command=self.__select_color)
        self.save_class_Button=ttk.Button(master=self.add_categories_frame,text="Save the class", command=self.__add_class)

        ### Frame  de sauvegarde des patchs
        self.patches_saving_frame_label=ttk.Label(master=self.saving_patches_frame,text="Patchs saving")
        self.entry_mask_extension_var=tkinter.StringVar()
        self.entry_mask_extension_var.set("_cp_masks.png")
        self.entry_mask_extension=ttk.Entry(master=self.saving_patches_frame,textvariable=self.entry_mask_extension_var)
        self.saving_button=ttk.Button(master=self.saving_patches_frame,text="Save",command=self.__save_patches)

        

        ###Sauvegarder les patchs dans le dossier
    
       
    def __grid_components(self):



        ### Simplement désactivé l'ajout de nouvelle catégorie
        # self.add_categories_frame.grid(row=0,column=0)


        self.folder_selection_frame.grid(row=0,column=1)
        self.saving_patches_frame.grid(row=0,column=2)
       
        self.button_folder_selection.grid(column=1,row=0)
        self.folder_label.grid(column=1,row=1)

        self.button_output_folder_selection.grid(column=2,row=0)
        self.output_folder_label.grid(column=2,row=1)


        self.cat_name_entry.grid(column=0,row=0)
        self.colorselector.grid(column=0,row=1)
        self.save_class_Button.grid(column=0,row=2)


        self.patches_saving_frame_label.grid(row=0,column=0)
        self.entry_mask_extension.grid(row=1,column=0)
        self.saving_button.grid(row=2,column=0)
        



    


        
    def __save_patches(self):
        
        self.backend_handler.save_patches(self.entry_mask_extension_var.get())
        
    
    def __select_color(self): 
        
        
         self.current_color_code = colorchooser.askcolor(title="Choisir une couleur")[1]  # Retourne une tuple (couleur RGB, code hexadécimal)
         
        
    def __add_class(self) : 
        """
        
        """
        num_category=len(list(self.backend_handler.available_categories.keys()))+1
        self.backend_handler.add_category(num_category,self.entry_cat_name.get(),self.current_color_code)
       


    def __folder_selection(self) : 

       
        if self.backend_handler.prepared_output :

            self.file_folder=tkinter.filedialog.askdirectory(initialdir="/home/adrienb/Documents/Adrien/datasets/processed_128_128/croped_768x1280",title="Select a folder")
            self.folder_var.set("folder : {}".format(self.file_folder))
            self.backend_handler.folder=self.file_folder
            self.backend_handler.list_dir()

        else : 
            print("please choose output_folder before")

    def __output_folder_selection(self) : 

        self.output_file_folder=tkinter.filedialog.askdirectory(initialdir="/home/adrienb/Documents/Adrien/datasets/New_dataset/PatchTagger_Output",title="Select an output folder")
        self.output_folder_var.set("folder : {}".format(self.output_file_folder))
        self.backend_handler.prepare_output(self.output_file_folder)



    



    

    
       
        










    



import tkinter
from tkinter import ttk
import tkinter.filedialog
import backend_handler
from PIL import ImageTk,Image



class loader : 

    def __init__(self) : 
        super().__init__()
        self.backend_handler=backend_handler.BackendHandler()
        self.__instantiate()
        

    def __instantiate(self):    
    
        
        self.root=tkinter.Tk()
        self.root.title("PatchTagger")
        self.notebook=ttk.Notebook(self.root)
        self.notebook.grid(row=0,column=0)
        self.notebook.add(main_window(self.notebook,backend_handler=self.backend_handler),text="main")
        self.notebook.add(config_window(self.notebook,backend_handler=self.backend_handler),text="settings")
        self.notebook.bind("<<NotebookTabChanged>>", self.__on_tab_change)





    def __call__(self) : 
        
        self.root.mainloop()

    def __on_tab_change(self, event):
        selected_tab = event.widget.select()
        tab_frame = event.widget.nametowidget(selected_tab)
        tab_frame.focus_set()


class main_window(tkinter.Frame) : 

    def __init__(self, master,backend_handler) : 
        super().__init__(master) 
        
        self.backend_handler=backend_handler
        self.__instantiate()
        self.__grid_components()





    def __instantiate(self): 

        self.left_frame=ttk.Frame(master=self)
        self.right_frame=ttk.Frame(master=self)
        self.fvar=tkinter.StringVar()
        self.fvar.set("None")
        


        self.lab_main_image=ttk.Label(master=self.left_frame)
        self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
        self.lab_main_image["image"]=self.main_image
        self.bind("<Right>",lambda e:  self.__change_patch_pos(e, 1))
        self.bind("<Left>",lambda e:  self.__change_patch_pos(e, -1))
        
        self.next_image_button=ttk.Button(master=self.left_frame,text="Image suivante",command= lambda : self.__change_image(1))
        self.previous_image_button=ttk.Button(master=self.left_frame,text="Image précédente",command= lambda : self.__change_image(-1))
        


        self.lab_patch=ttk.Label(master=self.right_frame)
        self.patch= ImageTk.PhotoImage(self.backend_handler.patch)
        self.lab_patch["image"]=self.patch
        self.bind("<Right>",lambda e:  self.__change_patch_pos(e, 1))
        self.bind("<Left>",lambda e:  self.__change_patch_pos(e, -1))
        
        

        self.focus_set()


        
    def __grid_components(self) : 
        self.left_frame.grid(row=0,column=0)
        self.right_frame.grid(row=0,column=1)
        self.lab_main_image.grid(row=1,column=0,columnspan=6)
        self.lab_patch.grid(row=0,column=0)

        self.next_image_button.grid(row=0,column=4)
        self.previous_image_button.grid(row=0,column=2)

        pass


    def __change_patch_pos(self,event,way) : 
        """
        
        """
        print("appel")
        self.backend_handler.change_patch(way)
        self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
        self.lab_main_image.config(image=self.main_image)
        self.lab_main_image.image=self.main_image

        self.patch= ImageTk.PhotoImage(self.backend_handler.patch)
        self.lab_patch.config(image=self.patch)
        self.lab_patch.image=self.patch
        
        
    def __change_image(self,way) : 

    

      
        self.backend_handler.change_image(way)

        self.main_image= ImageTk.PhotoImage(self.backend_handler.Image)
        self.lab_main_image.config(image=self.main_image)
        self.lab_main_image.image=self.main_image

        self.patch= ImageTk.PhotoImage(self.backend_handler.patch)
        self.lab_patch.config(image=self.patch)
        self.lab_patch.image=self.patch
        self.focus_set()
      


class config_window(tkinter.Frame) : 


    def __init__(self,master,backend_handler) : 
        
        
        self.backend_handler=backend_handler
        super().__init__(master)
        self.__instantiate()
        self.__grid_components()

    

    def __instantiate(self) :
    


        self.button_folder_selection=tkinter.Button(self,text="sélectionner un dossier",command=self.__folder_selection)
        
        self.folder_var=tkinter.StringVar()
        self.folder_var.set("Selected folder : None")
        self.folder_label=tkinter.Label(master=self,textvariable=self.folder_var)

       

    def __grid_components(self):


        self.button_folder_selection.grid(column=1,row=0)
        self.folder_label.grid(column=1,row=1)

    def __folder_selection(self) : 

        self.file_folder=tkinter.filedialog.askdirectory(initialdir="/home/adrienb/Documents/Adrien/datasets/processed_128_128/croped_768x1280",title="Select a folder")
        self.folder_var.set("folder : {}".format(self.file_folder))
        self.backend_handler.folder=self.file_folder
        self.backend_handler.list_dir()
        










    



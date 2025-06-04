import tkinter.ttk as ttk


def apply_styles():
    style=ttk.Style()

    style.theme_use('clam')   
    
    style.configure('notebook2.TNotebook',background= "#29dceb")
    style.configure("notebook2.TNotebook.Tab",
                     background="#8FE3A4", 
                   )

    
    style.map("notebook2.TNotebook.Tab",
          background=[("selected", "white")],
          foreground=[("selected", "black")])
    

    style.configure("category_label.TLabel", 
                    font=('Helvetica', 8),
                    foreground="black",
                    anchor="w",
                    justify='left'
    )
    style.configure("title_.TLabel", 
                    font=('Helvetica', 12, 'bold'),
                    borderwidth=1,
                    relief='solid',
                    padding=4

    )

    style.configure(
        "tab_1.TFrame",
        background="#8FE3A4"

    )
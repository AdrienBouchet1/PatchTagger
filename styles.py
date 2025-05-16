import tkinter.ttk as ttk


def apply_styles():
    style=ttk.Style()

    style.theme_use('clam')   
    
    style.configure('notebook2.TNotebook',background= "#29dceb")

    style.configure("category_label.TLabel", 
                    font=('Helvetica', 8),
                    foreground='#000000',
                    anchor="w",
                    justify='left'
    )
    style.configure("title_.TLabel", 
                    font=('Helvetica', 12, 'bold'),
                    borderwidth=1,
                    relief='solid',
                    padding=4

    )

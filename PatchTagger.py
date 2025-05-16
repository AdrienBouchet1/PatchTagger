import sys
import os

sys.path.append(os.path.abspath("./src"))
import GUi






if __name__=='__main__' : 
    
    app=GUi.loader()
    app()
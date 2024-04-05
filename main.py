#September 28, 2023

from tkinter import ttk
from tkinter import *
from tkinter.ttk import *

import file
import styles

from file import File, Folder
from actionbar import ActionBar, EditActions
from container import Container
import container

from pathlib import Path
import os

class XPyExplorer:
    def __init__(self, path):
        self.root = Tk()
        self.root.title("Xplorer")
        #self.root.resizable(0, 1)
        self.startpath = self.path = path.resolve()
        file.visited["paths"].append(self.startpath)
        os.chdir(self.path)
        #self.root.iconbitmap("explore.ico")
        self.build_appframe()
        self.actionbar = ActionBar(self)
        self.build_containers()
        self.edit = EditActions(self)
        self.style()
        self.refresh()
        self.root.mainloop()
        
    def build_appframe(self):
        self.appframe = Frame(self.root, padding=(10))
        self.appframe.grid(column=0, row=0, sticky=(N, W, E, S))
        self.appframe.app = self
        self.appframe.columnconfigure(0, weight=1)
        
    def build_containers(self):
        #space separating
        styles.create_space(self.appframe, 0, 2)
        container.create_containerframe(self)
        self.foldercontainer = Container(self, 0)
        self.filecontainer = Container(self, 1)
    
    def style(self):
        #make it resize with the window
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        
        self.appframe.columnconfigure(0, weight=1)
        #self.appframe.rowconfigure(0, weight=1)
        #link some Widgets to selectors
        self.appframe["style"] = "PE.TFrame"
        styles.beautify()        
    
    def __getitem__(self, prop):
        return getattr(self.frame, prop)
    
    def refresh(self):
        #Check all the buttons if they should be uploaded or not
        #refresh(self)
        container.refresh(self)  #refresh files and folders
        self.actionbar.refresh() #refresh actionbar so that it disables unneeded buttons
        self.edit.refresh()
if __name__=="__main__":
    app = XPyExplorer(Path("."))

#tkinter stuff
from tkinter import *
from tkinter.ttk import *

from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror, showinfo, askokcancel
#end tkinter stuff

#other helpers
import os
#end other helpers

#XPlorer specific
import file
#end Xplorer specific


def create_containerframe(app):
    #spacing
    app.container = Frame(app.appframe, padding=(10))
    app.container.grid(row=2, column=0)
    app.container["style"] = "Container.TFrame"
    #the File and folder containers will be inside the frame

def sortby(file_list, manner, descending=False):
    #sort files by manner in descending order (HA!)
    match manner:
        case "Name":
            return sorted(file_list, key=lambda file: file.name, reverse=descending)
        case "Date Created":
            return sorted(file_list, key=os.path.getctime, reverse=descending)
        case "Date Modified":
            return sorted(file_list, key=os.path.getmtime, reverse=descending)
        case "Type":
            #get the file extension if it has one, then sort according
            #to that
            return sorted(file_list
            , key=lambda file: file.name
                          .split('.')[-1] if '.' in file
                          .name else '', reverse=descending)
        case "Size":
            return sorted(file_list, key=os.path.getsize, reverse=descending)

def refresh(app):
    file.build_files(app, os.getcwd())
    for cont in (app.filecontainer, app.foldercontainer):
        cont.refresh_scroll()

class Container:
    def __init__(self, app, n):
        self.app = app
        self.n = n
        self.build_parts()
        self.style()
        self.event()
        self.refresh_scroll()
        
    def build_parts(self):
        self.actions_frame = Frame(self.app.container)
        self.actions_frame.grid(row=0, column=self.n*2)
        #the plus button (the command will be set)
        self.add = Button(self.actions_frame, text="+")
        self.label = Label(self.actions_frame, text="Files" if self.n else "Folders")
        self.sortby_options = ["Name", "Name", "Date Created", "Date Modified"
                               ,"Type", "Size"]
        self.sortby_value = StringVar()
        self.sortby = OptionMenu(self.actions_frame, self.sortby_value
                                 , *self.sortby_options)
        self.descending = BooleanVar()
        self.reverser = Checkbutton(self.actions_frame, text="Ascending"
                                    , variable=self.descending)
        #make it scrollable
        # add it to a canvas
        maxsize = self.app.root.maxsize()
        height = maxsize[1] - 300
        width = maxsize[0]/2-150
        self.canvas = Canvas(self.app.container, height=height, width=width)
        self.canvas.grid(column=self.n*2, row=1, sticky=(N, S, E, W)) #self.n*2 leaves space for scrollbars
              
        self.content_frame = Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        #end add to canvas
        #add the scrollbar
        self.scr = Scrollbar(self.app.container, command=self.canvas.yview)
        self.scr.grid(row=1, column=2*self.n+1, sticky=(N, S))
        self.canvas["yscrollcommand"] = self.scr.set
        #end add the scrollbar

        
        # self.frame.update_idletasks()
        
    @property
    def children(self):
        return self.actions_frame.winfo_children()
        
    def style(self):
        ch = self.children
        for part in ch:
            part.grid(column=ch.index(part), row=0)
            part["padding"] = (0)
            part["style"] = "Cont.TButton"
        self.add["width"] = 4
        self.label["width"] = 30
        
    
    def __getitem__(self, prop):
        return getattr(self.content_frame, prop)
    
    def sortation_manner(self):
        #return tuple of len 2 indicating sortation manner
        #, to be passed to container.sortby
        manner = self.sortby_value.get()
        descending = self.descending.get()
        return (manner, descending)
        
    def event(self):
        #making anew
        def add_item(*event):
            item = "file" if self.n else "folder"
            Item = item.capitalize()
            new = askstring(f"New {Item} Creation", f"Enter the name of the {item}")
            if not new: # user cancelled action
                return
            #check for invalid characters in name
            invalids = ''.join(char for char in new if char in '\\/:*?"|<>')
            #LBYL
            if os.path.exists(new):
                showerror(f"{Item} Creation Error", f"{Item} {new} already exists")
            elif invalids: #check if name is invalid (string should be empty if not)
                showerror(f"{Item} Creation Error", f"{new} should not contain any of \\/:*?\"|<> ")
            else:
                #do different things for files and folders
                #EAFP
                try:
                    if self.n: #files
                        with open(new, 'x'): pass
                    else: # folders
                        os.mkdir(new)
                except PermissionError:
                    showerror(f"{item.upper()} Creation Error", "Permission Denied!")
            self.app.refresh()
        def reverse(*event):
            if self.descending.get():
                self.reverser["text"] = "Descending"
            else:
                self.reverser["text"] = "Ascending"
            self.app.refresh()
        #add the events
        self.sortby_value.trace('w', lambda *event: self.app.refresh())
        self.descending.trace('w', reverse)
        self.add["command"] = add_item
        
    def refresh_scroll(self):
        # get the number of files/folders, then times the number with height of 1 item
        len_items = len([
            item for item in os.scandir() if (item.is_file() if self.n else item.is_dir())
        ])
        self.canvas.config( scrollregion=(0, 0
                , int(self.canvas["width"]), len_items * 31) )

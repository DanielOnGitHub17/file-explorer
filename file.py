#tkinter stuff
from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror, showinfo, askokcancel
#end tkinter stuff

#other helpers
import os
from pathlib import Path
from datetime import datetime
#end other helpers

#XPlorer specific
import container
#end Xplorer specific

files = []
folders = []
def add_to_visited(path):
    if visited["current"]() != path:
        at = visited["at"]
        del visited["paths"][at+1: ] #delete paths in front
        visited["paths"].append(path) #add path to last place
        visited["at"] += 1 #increase at
        #move
        os.chdir(visited["current"]())

visited = {
    "paths": []
    ,"at": 0
    ,"current": lambda: visited["paths"][visited["at"]]
    ,"add": lambda path: add_to_visited(path)
}

        
file_types = {
    ".py": "Python FIle"
    , ".txt": "Plain text file"
    , ".docx": "Microsoft Word Document"
    , ".jpg": "JPEG image file"
    , ".png": "Portable Network Graphics file"
}        
        
class File():
    def __init__(self, app, path):
        files.append(self)
        self.app = app
        self.container = app.filecontainer
        self.start_build(app, path)
    def start_build(self, app, path):
        self.frame = Frame(self.container.content_frame)
        self.frame.grid(columnspan=3, sticky=(W, E))
        self.path = Path(path.path).resolve()
        self._name = path.name
        self.make_parts()
        self.arrange()
        self.functions()
        self.style()
        self.event()
    def make_parts(self):
        self.action_options = ["...", "Open", "Rename", "Delete", "Properties"]
        #, "Cut", "Copy", "MCut", "MCopy",
        self.action = StringVar()
        #self.action.set("...")
        self.actions = OptionMenu(self.frame, self.action
                                  , *self.action_options)
        #print(self._name)
        self.name = StringVar()
        self.name.set(self._name)
        self.namebox = Label(self.frame, textvariable=self.name, anchor=W)
        
        self.selected = BooleanVar()
        self.selectbox = Checkbutton(self.frame, variable=self.selected
                                     , onvalue=1, offvalue=0, text="select")
    def arrange(self):
        #self.frame.grid()
        c = 0
        for part in self["winfo_children"]():
            part.grid(row=0, column=c)
            c+=1

    def functions(self):
        pass
    
    def event(self):
        def action_chosen(*event):
            act = self.action.get()
            #print(act)
            match act:
                case "Open":
                    self.open()
                case "Rename":
                    new_name = askstring("File Renaming", f"Current Name: {self.name.get()}\nEnter a new name")
                    #EAFP
                    error= '';
                    try:
                        if new_name:
                            if os.path.exists(new_name): #change this LBYL to EAFP later
                                error = new_name+" already exists"
                                raise ValueError()
                            os.rename(self.path, new_name)
                        elif new_name is None:
                            error = "Rename Cancelled!"
                            raise ValueError()
                        else:
                            error = "Invalid Name!"
                            raise ValueError()
                    except BaseException:
                        #failed
                        showerror("Rename Error", error if error else "Rename failed!!!")
                    finally:
                        #refresh
                        self.app.refresh()
                case "Delete":
                    if askokcancel("Confirm delete", f"Are you SURE you want to delete {self.name.get()}"):
                        self.delete() #different for folders and files
                        self.app.refresh()
                case "Properties":
                    self.show_properties()
            self.action.set("...") # to reset the menu to the menu 'image'
        def select(*event):
            if self.selected.get():
                self.selectbox["text"] = "selected"
            else:
                self.selectbox["text"] = "select"
            self.app.edit.refresh()

        def select_only(*event):
            select_value = not self.selected.get()
            for item in files+folders:
                item.selected.set(False)
            self.selected.set(select_value) #select if, else disselect
        
        self.action.trace('w', action_chosen)
        self.namebox.bind("<Double-1>", lambda event: self.open())
        self.namebox.bind("<1>", select_only)
        self.selected.trace('w', select)

    def style(self):
        for child in self["winfo_children"]():
            child["padding"] = 0
            child["style"] = "Cont.TButton"
        self.actions["width"] = 4
        self.namebox["width"] = 30
        self.selectbox["width"] = ''

        self.frame["style"] = "File.TFrame"
        
    def __getitem__(self, prop):
        return getattr(self.frame, prop)
    #the open method
    def open(self):
        os.startfile(self.path)

    def show_properties(self):
        stats = self.path.stat()
        extension = os.path.splitext(self.path)[1]
        more_properties = ''
        if self.path.is_dir():
            file_type = "Folder"
            folders_in = [item.name for item in os.scandir(self.path) if item.is_dir()]
            files_in = [item.name for item in os.scandir(self.path) if item.is_file()]
            sp = self.app.edit.sp
            s = self.app.edit.s
            more_properties = f"""Sub folders: {sp(folders_in)}{s(len(sp(folders_in))>39, "")}
Files: {sp(files_in)[0:40]}{s(len(sp(files_in))>39, "...")}
Number of folders: {len(folders_in)}
Number of files: {len(files_in)}
"""
        elif extension in file_types:
            file_type = file_types[extension]
        else:
            file_type = f"{extension} file"
        property_text = f"""Name: {self.path.name}
Type: {file_type}
Size: {sizer(self.size())}
Date Created: {datetime.fromtimestamp(stats.st_ctime)}
Date Accessed: {datetime.fromtimestamp(stats.st_atime)}
Date Modified: {datetime.fromtimestamp(stats.st_mtime)}
Location: {self.path}
"""+more_properties
        
        showinfo(f"{self.name.get()} properties", property_text)

    def delete(self):
        try:
            os.remove(self.path)
        except PermissionError:
            showinfo("Deletion error", "Cannot delete"+self.name)
        
    def size(self):
        return os.path.getsize(self.path)


        

class Folder(File):
    def __init__(self, app, path):
        folders.append(self)
        self.app = app
        self.container = app.foldercontainer
        self.start_build(app, path)
        
    def open(self):
        try:
            visited["add"](self.path)
        except PermissionError:
            return
        finally:
            self.app.refresh()
        
    def delete(self):
        #walk
        for three in os.walk(self.path):
            #remember: 0: folder_path; 1=folders in; 2: files in folder_path
            path = three[0]
            #delete the files in each folder first
            for file in three[2]:
                try:
                    os.remove(path+"\\"+file)
                except:
                    continue
        #delete the folders, ...
        #[os.rmdir(three[0]) for three in reversed(list(os.walk(self.path))) ]
        dirs_in = reversed(list(os.walk(self.path)))
        for three in dirs_in:
            os.rmdir(three[0])
    
    def size(self):
        result = 0
        for three in os.walk(self.path):
            #remember: 0: folder_path; 1=folders in; 2: files in folder_path
            path = three[0]
            for file in three[2]:
                result += os.path.getsize(f"{path}\\{file}")
        return result
            


def build_files(app, path):
    #make path a Path
    path = Path(path)
    #clear everything from the containers
    for i in range(len(files)):
        files[0]["destroy"]()
        del files[0]
    #more clearifying
    for i in range(len(folders)):
        folders[0]["destroy"]()
        del folders[0]
    #then change the path to where you want to build new files
    #change the current path
    os.chdir(path)
    
    #then separate files from folders...
    current_paths = os.scandir()
    current_files = []
    current_folders = []
    
    for item in current_paths:
        if item.is_file():
            current_files.append(item)
        elif item.is_dir(): #change to else if confirmed that...
            current_folders.append(item)

    #sort the files with the manner of a file/foldercontainer
    sorted_files = container.sortby(current_files
                                , *app.filecontainer.sortation_manner())
    sorted_folders = container.sortby(current_folders
                                , *app.foldercontainer.sortation_manner())
    
    # build folders
    for folder in sorted_folders:
        Folder(app, folder)
        
    # build files
    for file in sorted_files:
        File(app, file)
    app.actionbar.location.set(os.getcwd()) #add path to the locationbar


def sizer(size):
    if size<1024:
        return f"{size} bytes"
    elif size < 1023*1024:
        return f"{size/1024} KB"
    elif size < 1023*1024*1024:
        return f"{size/1024/1024} MB"
    elif size < 1023*(1024**3):
        return f"{size/(1024**3)} GB"
from tkinter import ttk
from tkinter import *
from tkinter.ttk import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror, showinfo, askokcancel
import zipfile
from tarfile import TarFile

import file, container


from pathlib import Path
import os

class ActionBar:
    def __init__(self, app):
        self.frame = Frame(app.appframe, padding=(10))
        self.frame.grid(column=0, row=0)
        self.app = app
        self.commands = ["Backward", "Forward", "Refresh", ".."
                         , "Properties", "Delete", "Archive"]
        #  , "Copy", "Cut", "Paste"]
        self.location_ = self.app.path
        #command buttons
        for i in self.commands:
            setattr(self, i, Button(self.frame, text=i, style="PE.TButton"))
            getattr(self, i).grid(column=self.commands.index(i), row=0)
            getattr(self, i).grid_configure(padx=3, pady=(10, 20))
            #getattr(self, i).state(["disabled"])
        #Location bar
        self.location = StringVar()
        self.location.set(self.app.path)
        self.locationbar = Entry(self.frame, textvariable=self.location
                            , width=len(self.commands)*15)
        self.locationbar.grid(column=0, columnspan=len(self.commands), row=1)
        self.style()
        self.event()
    def __index__(self, what):
        return getattr(self.frame, what)
    @property
    def children(self):
        return self.frame.winfo_children()
    def command(self):
        pass
    def style(self):
        self.frame["style"] = "AB.TFrame"
    def __getitem__(self, prop):
        return getattr(self.frame, prop)
    def event(self):
        #all events written in (function, binding) manner
        def locate(event):
            test_path = Path(self.location.get()).resolve()
            #if path exists open if file, build_files if folder
            if test_path.exists():
                #good, now open, or ask for forgiveness if PermissonError
                try:
                    if test_path.is_dir():
                        file.visited["add"](test_path)
                        self.app.refresh()
                    elif test_path.is_file():
                        #open it
                        os.startfile(test_path)
                except PermissionError:
                    showerror(title="XPlorer", message="Permission denied")

        def locate_parent(*event):
            file.visited["add"](Path("..").resolve())
            self.app.refresh()

        def visit(*event, n=-1):
            #no need to check for position because actionbar.refresh will disable if it won't work
            file.visited["at"] += n #-1 for previous, 1 for next
            os.chdir(file.visited["current"]())
            self.app.refresh()

                

        def properties(*event):
            size = sum([item.size() for item in self.app.edit.selected])
            n = len(self.app.edit.selected)
            text = f"{n} selected\nsize: {file.sizer(size)}"
            showinfo("Properties of selected", text)

        def delete(*event):
            if askokcancel ("Multiple deletion"
                    , """Are you sure you want to delete the selected items
                    You will not be able to get them back"""):
                        for item in self.app.edit.selected:
                            item.delete()
                        self.app.refresh()

        def archive(*event):
            if len(self.app.edit.selected):
                arch_name = askstring("New Archive", "Name of archvie")
                arch_type = askstring("New Archive", "Type of archive: zip or tar")
                if not arch_name or not arch_type:
                    return
                else:
                    arch_type = arch_type.lower()
                if arch_type == "tar":
                    arch_name += ".tar"
                    with TarFile(arch_name, "w:gz") as tar_file:
                        for item in self.app.edit.selected:
                            tar_file.add(item.path.name)
                elif arch_type == "zip":
                    arch_name += ".zip"
                    with zipfile.ZipFile(arch_name, "w", compression=zipfile.ZIP_DEFLATED
                                           , compresslevel=9) as zip_file:
                        for item in self.app.edit.selected:
                            zip_file.write(item.path.name)
                self.app.refresh()
            
        self.func_locate = locate
        self.locationbar.bind("<Return>", locate)
        #refresh button
        self.Refresh["command"] = self.app.refresh
        #parent event
        getattr(self, "..")["command"] = locate_parent
        #previous
        self.Backward["command"] = lambda *event: visit(*event)
        self.Forward["command"] = lambda *event: visit(*event, n=1)
        #properties
        self.Properties["command"] = properties
        #archive
        self.Archive["command"] = archive
        #delete
        self.Delete["command"] = delete


    def refresh(self):
        #start from first button (Backward) and end at last
        # disable backward button if at is 0 else enable it
        self.Backward.state(["disabled"] if file.visited["at"]==0 else ["!disabled"])
        # disable forward button if at is visited last else enable it
        self.Forward.state(
            ["disabled"] if file.visited["at"] == len(file.visited["paths"])-1 else ["!disabled"])

class EditActions:
    def __init__(self, app):
        self.app = app
        self.frame = Frame(app.appframe, padding=(10))
        self.frame["style"] = "Container.TFrame"
        self.frame.grid()
        self.to_move = []
        self.to_copy = []
        self.text = StringVar()
        self.text_bar = Label(self.frame, textvariable=self.text)
        self.text_bar.grid()
        self.refresh()
    
    def add_to_copy(self, path, restart):
        if restart:
            self.to_copy.clear()
            self.to_copy.append(path)
        else:
            self.to_copy.append(path)
            
    def refresh(self):
        text = ''
        items_len = len(self.paths_here)
        s = self.s
        sp=self.sp
        if items_len:
            text += f"{items_len} item{s(items_len)}: "
            len_fols = len(file.folders)
            len_files = len(file.files)
            len_sel = len(self.selected)
            if len_fols:
                text += f"{len_fols} folder{s(len_fols)} "
            if len_files:
                text += f"{len_files} file{s(len_fols)} "
            if len_sel:
                text += f"{len_sel} selected"
            if len(self.to_move):
                move_str = s(self.to_move)
                text += f"\nMove { move_str[0:40] }{ s(len(move_str)>40, '...') }"
            if len(self.to_copy):
                move_str = s(self.copy)
                text += f"\nCopy { move_str[0:40] }{ s(len(move_str)>40, '...') }"
        else:
            text += "No items are in this folder"
            
        self.text.set(text)
        
    @property
    def selected(self):
        return [item for item in file.files+file.folders if item.selected.get()]
        
    @property
    def paths_here(self):
        return file.files+file.folders

    def sp(self, paths): #or int to string or path to string
        if type(paths)==int:
            return str(int)
        return ', '.join(os.path.relpath(path) for path in paths).strip()
    
    def s(self, should_write, string='s'):
        return string if should_write else ''
from tkinter import *
from tkinter import ttk
from pathlib import Path
import tkinter.simpledialog, tkinter, os
#use config for seting any setting so that you can use lambdas
#events i know: (<x> for each x) Enter, Leave, ButtonPress!<>
#add a button for creating new folder

def load(root):
    root = root.absolute().resolve();
    os.chdir(str(root))
    pathText['text'] = str(root)
    r = 3; c = 0;
    beforeList = [dd[1] for dd in AppFrame.children.items() if 'path' in dir(dd[1])]
    n = len(beforeList)
    for bt in beforeList:
        bt.destroy()
    for d in root.iterdir():
        link = ttk.Button(AppFrame, text=d.name)
        link.grid(row=r, column=2); r+=1;
        link.path = d;
        if d.is_dir(): link.bind('<ButtonRelease>', func=lambda event: load(event.widget.path))
        elif d.is_file(): link.bind('<ButtonRelease>', func=lambda event: os.startfile(str(event.widget.path)))
#functions functions
def addFolder(remove=False):
    try:
        name=tkinter.simpledialog.askstring('File Explore', 'Folder Name' if remove else 'New Folder Name')
        if remove:
            os.rmdir(name)
            beforeList = [dd[1] for dd in AppFrame.children.items() if 'path' in dir(dd[1])]
            for x in beforeList:
                if x['text'] == name:
                    x.destroy()
                    return
        else:
            os.mkdir(name)
            btn = ttk.Button(AppFrame, text=name)
            btn.grid()
    except BaseException:
        return

def openFile(name):
    print(name)
    os.system(name)
#end functions#

#create one tk instance for a window
App = Tk(className = 'File Explorer'); App['width'] = 1300; App['height'] = 700
#frame
AppFrame = ttk.Frame(App)
AppFrame.config(width=1200, height=600);
AppFrame.grid()

#header
pathText = ttk.Label(AppFrame, text='')
pathText.grid(row=0, column=1)

#back
back = ttk.Button(AppFrame, text='↑', command=lambda: load(Path('..')))
back.grid(row=1, column=0)

#remove
remove = ttk.Button(AppFrame, text='delete folder', command=lambda: addFolder(True))
remove.grid(row=1, column=1)

#refresh
refresh = ttk.Button(AppFrame, text='refresh', command=lambda: load(Path()))
refresh.grid(row=1, column=2)

#add
add = ttk.Button(AppFrame, text='add folder', command=addFolder)
add.grid(row=1, column=3)

#scroll
scr = ttk.Scrollbar(AppFrame)
scr.grid(row=2, column=9)

#start the party
load(Path('//'))
App.mainloop()

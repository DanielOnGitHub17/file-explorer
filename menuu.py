from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *

root = Tk()
canv = Canvas(root)
canv.grid()
appframe = Frame(canv)
appframe.grid(column=0)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)        
appframe.columnconfigure(0, weight=1)

plenty = Frame(appframe)
plenty.grid()
s = Style()
s.configure("S.TFrame", height="300")
#print(dir(canv.configure().keys()))
#canv["style"] = "S.TFrame"

for x in range(100):
    Label(plenty, text="Label"+str(x)).grid(column=0, row=x)

sc = Scrollbar(root, orient=VERTICAL, command=canv.yview)
sc.grid(column=1, row=0)

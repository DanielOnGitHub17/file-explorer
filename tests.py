from tkinter import *
from tkinter import ttk, messagebox
from tkinter.ttk import *
from random import randint

root = Tk()
appframe = Frame(root)
appframe.grid(sticky=(N, W, E, S))

scroll_help = Canvas(root)
scroll_help.grid()

cont = Frame(scroll_help)
cont.grid()

items = ["Name", "Date Modified", "Size"] * 20
row = 0
for x in items:
    child = Frame(cont)
    child.grid(column=0, row=row)
    Label(child, text=f"{randint(10000, 90000)}").grid(column=0, row=0)
    Label(child, text=f"{randint(10000, 90000)}").grid(column=1, row=0)
    Label(child, text=f"{randint(10000, 90000)}").grid(column=2, row=0)
    row += 1

scroll_help["height"] = 200

style = Style()
style.configure("SC.Canvas", border="relief", height="20")

scroll_help["relief"] = "raised"

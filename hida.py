from tkinter import *
from tkinter import ttk

root = Tk()

canvas = Canvas(root)
canvas.grid(row=0, column=0, sticky='nsew')

scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')

frame = Frame(canvas)
canvas.create_window((0,0), window=frame, anchor='nw')

for i in range(100):
    Label(frame, text=f"Item {i}").grid(row=i, column=0)

root.mainloop()

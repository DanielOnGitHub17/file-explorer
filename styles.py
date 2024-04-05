from tkinter.ttk import *
import json
from css import CSS
from style_css import style_text
#compute styles
def beautify():
    sstyles = []
    styles = CSS(text=style_text).style_dict
    for s in styles:
        style = Style()
        style.configure(s, **styles[s])
        sstyles.append(style)
    #print(styles)
def create_space(where, width=0, height=0):
    sp = Frame(where, padding=(width, height))
    sp.grid()
    sp["style"] = "space.TFrame"
    hh = Label(sp, text=".",)
    hh.grid()
    hh["style"] = "space.TFrame"

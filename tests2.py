from tkinter import *
from tkinter.ttk import *

# Create a tkinter window
root = Tk()
root.title("Scrollable Frame Example")
app = Frame(root)
app.grid()
# Create a Canvas widget to hold the frame and attach a vertical scrollbar
canvas = Canvas(app, height=80)
canvas.grid(row=0, column=0, sticky="nsew")

# Create a frame to contain your content
frame = Frame(canvas)
canvas.create_window((0, 0), window=frame, anchor="nw")

# Create a vertical scrollbar
scrollbar = Scrollbar(root, command=canvas.yview)
scrollbar.grid(row=0, column=1, sticky="ns")
canvas.configure(yscrollcommand=scrollbar.set)

# Add Frames with Label, Text Entry, and Button to the frame using grid
for i in range(50):
    item_frame = Frame(frame)
    item_frame.grid(row=i, column=0, sticky="w")

    label = Label(item_frame, text=f"Label {i}")
    label.grid(row=0, column=0, sticky="w")

    text_entry = Entry(item_frame)
    text_entry.grid(row=0, column=1, sticky="w")

    button = Button(item_frame, text="Click")
    button.grid(row=0, column=2, sticky="w")

# Configure grid weights for responsiveness
#root.grid_rowconfigure(0, weight=1)
#root.grid_columnconfigure(0, weight=1)

# Update the scroll region
frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"))

# Run the tkinter main loop
root.mainloop()


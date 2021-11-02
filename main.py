import tkinter as tk
from tkinter import *
from overlay import Window
import numpy
#from PIL import Image
import os


# Instancing the app
root = tk.Tk()
root.title("Tilted Zakyr Calculator")
root.attributes('-alpha', 0.6)
root.attributes('-topmost', 1)


# Function to add 1 to the specified field
def button_add(field):
    var = numpy.clip(int(field.__getitem__("text"))+1, 0, 10)
    field.config(text = str(var))


# Function to subtract 1 to the specified field
def button_sub(field):
    var = numpy.clip(int(field.__getitem__("text"))-1, 0, 10)
    field.config(text = str(var))


# End turn calculations
def button_end():
    used = int(e_used.__getitem__("text"))
    gained = int(e_gained.__getitem__("text"))
    destroyed = int(e_destroyed.__getitem__("text"))
    energy = int(e.__getitem__("text"))
    energy = numpy.clip(energy - used + gained - destroyed, 0, 10) + 2

    #saving current round state
    prev_round["round"] = round_num.__getitem__("text")
    prev_round["energy"] = e.__getitem__("text")

    e_used.config(text = "0")
    e_gained.config(text = "0")
    e_destroyed.config(text = "0")

    round_num.config(text= str(int(round_num.__getitem__("text"))+1))
    e.config(text = str(energy))


# Reset fuction
def reset_app():
    e.config(text = "3")
    round_num.config(text = "1")
    e_used.config(text = "0")
    e_gained.config(text = "0")
    e_destroyed.config(text = "0")

    prev_round["round"] = "1"
    prev_round["energy"] = "3"


# Return to the previous round state
def undo_round():
    if round_num.__getitem__("text") != prev_round["round"]:
        round_num.config(text = prev_round["round"])
        e.config(text = prev_round["energy"])
        e_used.config(text = "0")
        e_gained.config(text = "0")
        e_destroyed.config(text = "0")


# Dictionary of the prev round
prev_round = {
    "round":"1",
    "energy": "3",
}


# Text for the total energy
e = Label(root, text="3", width=15, borderwidth=5, font= ('Sans Serif', 13, 'bold'))
e.grid(row=1, column=1, columnspan=1, padx=5, pady=5)

# Text description for the energy used field 
e_used = Label(root, text="0", width=5, borderwidth=5, font= ('Sans Serif', 13, 'bold'))
e_used.grid(row=3, column=1, columnspan=1, padx=5, pady=10)
used_text= Label(root, text="Energy Used", width= 12, height= 1, font= ('Sans Serif', 13, 'italic bold'))
used_text.grid(row=2, column=0, columnspan=3)

# Text description for the energy gained field
e_gained = Label(root, text="0", width=5, borderwidth=5, font= ('Sans Serif', 13, 'bold'))
e_gained.grid(row=5, column=1, columnspan=1, padx=5, pady=10)
gained_text= Label(root, text="Energy Gained", width= 13, height= 1, font= ('Sans Serif', 13, 'italic bold'))
gained_text.grid(row=4, column=0, columnspan=3)

# ext decription for the energy destroyed field
e_destroyed = Label(root, text="0", width=5, borderwidth=5, font= ('Sans Serif', 13, 'bold'))
e_destroyed.grid(row=7, column=1, columnspan=1, padx=10, pady=10)
destroyed_text= Label(root, text="Energy Destroyed", width= 17, height= 1, font= ('Sans Serif', 13, 'italic bold'))
destroyed_text.grid(row=6, column=0, columnspan=3)

# Round Label and Number
round = Label(root, text="Round", width= 15, height= 1, font= ('Sans Serif', 13, 'bold'), padx=5)
round.grid(row=0, column=0, columnspan=2)
# Round number
round_num = Label(root, text="1", width= 1, height= 1, font= ('Sans Serif', 11, 'bold'))
round_num.grid(row=0, column=1, columnspan=3)


# Creation of the different buttons
e_used_sub = Button(root, text="-", padx=10, pady=10, command=lambda: button_sub(e_used))
e_used_add = Button(root, text="+", padx=10, pady=10, command=lambda: button_add(e_used))
e_gained_sub = Button(root, text="-", padx=10, pady=10, command=lambda: button_sub(e_gained))
e_gained_add = Button(root, text="+", padx=10, pady=10, command=lambda: button_add(e_gained))
e_destroyed_sub = Button(root, text="-",padx=10, pady=10, command=lambda: button_sub(e_destroyed))
e_destroyed_add = Button(root, text="+", padx=10, pady=10, command=lambda: button_add(e_destroyed))
end_turn_btn = Button(root, text="End Turn", padx=15, pady=20, command=button_end)
reset_btn = Button(root, text="reset", padx=10, pady=15, command=reset_app)
undo_btn = Button(root, text="undo", padx=10, pady=15, command=undo_round)


# Organization/placement of the buttons
e_used_sub.grid(row=3, column=0)
e_used_add.grid(row=3, column=2)
e_gained_sub.grid(row=5, column=0)
e_gained_add.grid(row=5, column=2)
e_destroyed_sub.grid(row=7, column=0)
e_destroyed_add.grid(row=7, column=2)

end_turn_btn.grid(row=8, column=1)
reset_btn.grid(row=8, column=0)
undo_btn.grid(row=8, column=2)


root.mainloop()
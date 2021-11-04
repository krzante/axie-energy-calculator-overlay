import tkinter as tk
from tkinter import *
from tkinter import ttk
from overlay import Window
import numpy
import pyglet
from pynput.keyboard import Key, Listener

e = 3
e_used = 0
e_gained = 0
e_destroyed = 0
round_num = 1


# End turn calculations
def end_round():
    used = int(canvas.itemcget(e_used_num, 'text'))
    gained = int(canvas.itemcget(e_gained_num, 'text'))
    destroyed = int(canvas.itemcget(e_destroyed_num, 'text'))
    energy = int(canvas.itemcget(energy_count, 'text'))
    round = int(canvas.itemcget(round_count, 'text'))

    #saving current round state
    prev_round["round"] = str(round)
    prev_round["energy"] = str(energy)

    energy = numpy.clip((energy - used + gained - destroyed), 0, 8) + 2

    canvas.itemconfig(round_count, text = str(round+1))
    canvas.itemconfig(energy_count, text = str(energy))
    canvas.itemconfig(e_used_num, text = 0)
    canvas.itemconfig(e_gained_num, text = 0)
    canvas.itemconfig(e_destroyed_num, text = 0)


# Reset fuction
def reset_app():
    canvas.itemconfig(round_count, text = 1)
    canvas.itemconfig(energy_count, text = 3)
    canvas.itemconfig(e_used_num, text = 0)
    canvas.itemconfig(e_gained_num, text = 0)
    canvas.itemconfig(e_destroyed_num, text = 0)

    prev_round["round"] = "1"
    prev_round["energy"] = "3"


# Return to the previous round state
def undo_round():
    if canvas.itemcget(round_count, 'text') != prev_round["round"]:
        canvas.itemconfig(round_count, text = prev_round["round"])
        canvas.itemconfig(energy_count, text = prev_round["energy"])

        canvas.itemconfig(e_used_num, text = 0)
        canvas.itemconfig(e_gained_num, text = 0)
        canvas.itemconfig(e_destroyed_num, text = 0)


# Dictionary of the prev round
prev_round = {
    "round":"1",
    "energy": "3",
}


def btn_add(id):
    num = str(numpy.clip(int(canvas.itemcget(id, 'text'))+1, 0, 50)) #getter ng item
    # num = str(int(num)+1)
    canvas.itemconfig(id, text = num) #setter function
    # print("Button Clicked")

def btn_minus(id):
    num = str(numpy.clip(int(canvas.itemcget(id, 'text'))-1, 0, 50)) #getter ng item
    # num = str(int(num)-1)
    canvas.itemconfig(id, text = num) #setter function 

def on_press(key):
    if key.char.upper() == "Q":
        btn_minus(e_used_num)
    elif key.char.upper() == "W":
        btn_add(e_used_num)
    elif key.char.upper() == "A":
        btn_minus(e_gained_num)
    elif key.char.upper() == "S":
        btn_add(e_gained_num)
    elif key.char.upper() == "Z":
        btn_minus(e_destroyed_num)
    elif key.char.upper() == "X":
        btn_add(e_destroyed_num)
    elif key.char.upper() == "E":
        end_round()
    elif key.char.upper() == "R":
        reset_app()
    elif key.char.upper() == "F":
        undo_round()                

# def on_press(key):
#     # print(key.char)
#     match key.char.upper():
#         case "Q":
#             btn_minus(e_used_num)
#         case "W":
#             btn_add(e_used_num)
#         case "A":
#             btn_minus(e_gained_num)
#         case "S":
#             btn_add(e_gained_num)
#         case "Z":
#             btn_minus(e_destroyed_num)
#         case "X":
#             btn_add(e_destroyed_num)
#         case "E":
#             end_round()
#         case "R":
#             reset_app()
#         case "F":
#             undo_round()




window = tk.Tk()
nb = ttk.Notebook(window)

pyglet.font.add_file('./fonts/AldotheApache.ttf')

window.geometry("300x475")
# window.configure(bg = "red")
window.title("Tilted Zakyr Calculator")
window.attributes('-alpha', 0.6)
window.attributes('-topmost', 1)

tab1 = Frame(nb, width=300, height=450)
tab2 = Frame(nb, width=300, height=450)

nb.add(tab1, text="CALCULATOR")
nb.add(tab2, text="WINRATE")
nb.pack()

canvas = Canvas(
    tab1,
    bg = "#ffffff",
    height = 450,
    width = 300,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
canvas.place(x = 0, y = 0)

background_img = PhotoImage(master=tab1, file = f"./images/background.png")
background = canvas.create_image(
    151.0, 225.5,
    image=background_img)

img0 = PhotoImage(master=tab1, file = f"./images/btn-end.png") # End turn button
b0 = Button(
    tab1,
    image = img0,
    borderwidth = 0,
    highlightthickness = 0,
    command = end_round,
    relief = "flat")
window.bind("<e>", on_press)


b0.place(
    x = 104, y = 393,
    width = 97,
    height = 52)

img1 = PhotoImage(master=tab1, file = f"./images/btn-reset.png")  # Reset Button
b1 = Button(
    tab1,
    image = img1,
    borderwidth = 0,
    highlightthickness = 0,
    command = reset_app,
    relief = "flat")
window.bind("<r>", on_press)

b1.place(
    x = 17, y = 389,
    width = 51,
    height = 53)

img2 = PhotoImage(master=tab1, file = f"./images/btn-undo.png")  # Undo Button
b2 = Button(
    tab1,
    image = img2,
    borderwidth = 0,
    highlightthickness = 0,
    command = undo_round,
    relief = "flat")
window.bind("<f>", on_press)

b2.place(
    x = 236, y = 389,
    width = 51,
    height = 53)

img3 = PhotoImage(master=tab1, file = f"./images/btn-minus.png")  # Energy Destroyed MINUS
b3 = Button(
    tab1,
    image = img3,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_minus(e_destroyed_num),
    relief = "flat")
window.bind("<z>", on_press)

b3.place(
    x = 66, y = 316,
    width = 51,
    height = 53)

img4 = PhotoImage(master=tab1, file = f"./images/btn-plus.png") # Energy Destroyed PLUS
b4 = Button(
    tab1,
    image = img4,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_add(e_destroyed_num),
    relief = "flat")
window.bind("<x>", on_press)

b4.place(
    x = 188, y = 318,
    width = 51,
    height = 53)

e_destroyed_num = canvas.create_text(
    150.5, 342.5,
    text = "0", # Energy Destroyed Field
    fill = "#ffffff",
    font = ("Aldo the Apache", int(30.0)))

canvas.create_text(
    151.0, 302.5,
    text = "ENERGY DESTROYED",
    fill = "#000000",
    font = ("Aldo the Apache", int(16.0)))

img5 = PhotoImage(master=tab1, file = f"./images/btn-minus.png") # Energy Gained MINUS
b5 = Button(
    tab1,
    image = img5,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_minus(e_gained_num),
    relief = "flat")
window.bind("<a>", on_press)

b5.place(
    x = 66, y = 233,
    width = 51,
    height = 53)

img6 = PhotoImage(master=tab1, file = f"./images/btn-plus.png") # Energy Gained PLUS
b6 = Button(
    tab1,
    image = img6,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_add(e_gained_num),
    relief = "flat")
window.bind("<s>", on_press)

b6.place(
    x = 188, y = 232,
    width = 51,
    height = 53)

canvas.create_text(
    151.0, 219.5,
    text = "ENERGY GAINED",
    fill = "#000000",
    font = ("Aldo the Apache", int(16.0)))

e_gained_num = canvas.create_text(
    150.0, 259.5,
    text = "0", # Energy Gained Number
    fill = "#ffffff",
    font = ("Aldo the Apache", int(30.0)))

img7 = PhotoImage(master=tab1, file = f"./images/btn-minus.png") # USED MINUS
b7 = Button(
    tab1,
    image = img7,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_minus(e_used_num),
    relief = "flat")
window.bind("<q>", on_press)

b7.place(
    x = 65, y = 150,
    width = 51,
    height = 53)

img8 = PhotoImage(master=tab1, file = f"./images/btn-plus.png") # USED PLUS
b8 = Button(
    tab1,
    image = img8,
    borderwidth = 0,
    highlightthickness = 0,
    command = lambda:btn_add(e_used_num),
    relief = "flat")
window.bind("<w>", on_press)

b8.place(
    x = 186, y = 150,
    width = 51,
    height = 53)

canvas.create_text(
    150.0, 136.5,
    text = "ENERGY USED",
    fill = "#000000",
    font = ("Aldo the Apache", int(16.0)))

e_used_num = canvas.create_text(
    149.5, 176.5,
    text = "0", # Energy Used Field
    fill = "#ffffff",
    font = ("Aldo the Apache", int(30.0)))

energy_count = canvas.create_text(
    149.0, 86.0,
    text = "3", # Energy count
    fill = "#ffffff",
    font = ("Aldo the Apache", int(48.0)))

round_count = canvas.create_text(
    90.5, 28.0,
    text = "1",
    fill = "#ffffff",
    font = ("Aldo the Apache", int(24.0)))




# def hotkeys():
#     with Listener(on_press=on_press) as listener :
#         listener.join()
    

# def main():
    
#     hotkeys()
#     print("Hotdog")
    

# main()
window.resizable(False, False)
window.mainloop()

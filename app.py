from textwrap import wrap
import tkinter as tk
from tkinter import *
from tkinter import ttk
# from overlay import Window
# import numpy
import pyglet
# from pynput.keyboard import Key, Listener
import sys

# Importing Custom functions
from scripts.create_buttons import CustomButton
from scripts.tab1 import Tab1 as t1
from scripts.tab2 import Tab2 as t2
from scripts.tab3 import Tab3 as t3
from scripts.tab4 import Tab4 as t4


# Setting up the window and tabs
window = tk.Tk()
nb = ttk.Notebook(window)

# Setting up defaults
pyglet.font.add_file('./resources/fonts/AldotheApache.ttf')
default_font = "Aldo the Apache"
color_white = "#ffffff"
color_black = "#000000"

# window.geometry("308x486")
window.title("zakyr's Energy Calculator")
window.iconbitmap("./resources/images/icon.ico")
# window.attributes('-alpha', 1)
window.attributes('-topmost', 1)

# Kahit isa nalng may width and height
tab1 = Frame(nb, width=308, height=461)
tab2 = Frame(nb)
tab3 = Frame(nb)
tab4 = Frame(nb)

nb.add(tab1, text="ENERGY")
nb.add(tab2, text="WINRATE")
nb.add(tab3, text="ABOUT")
nb.add(tab4, text="SETTINGS")
nb.pack()

# Text items of a canvas ay mayroong mga ID to identify them so itong dictionary na ito ay
# ipapasa para ito maging pangaccess dun sa specific text item ng canvas para mabago ang text
# 
# Kapag nagcrecreate ka ng text istore mo sa specified na index dito sa dictionary
tab1_text_tags = dict({
    'round' : 0,
    'energy' : 0,
    'used' : 0,
    'gained' : 0,
    'destroyed' : 0
})

def btn_clicked():
    print("Button Clicked")

################################## TAB 1 ############################################################
tab1_canvas = Canvas(
    tab1,
    bg = "#ffffff",
    height = 461,
    width = 308,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
tab1_canvas.place(x = 0, y = 0)
tab1_background_img = PhotoImage(master=tab1, file = f"./resources/images/backgrounds/tab1_background.png")
tab1_background = tab1_canvas.create_image(154.0, 230.5, image=tab1_background_img)

# Round Number Text
tab1_text_tags['round'] = tab1_canvas.create_text(192.0, 20.0,text = "1",fill = "#ffffff", font = (default_font, int(23.0)))
# Enemy Energy Text
tab1_text_tags['energy'] = tab1_canvas.create_text(153.5, 81.0, text = "3", fill = "#ffffff", font = (default_font, int(40.0)))
# energy_text_tag = tab1_canvas.create_text(153.5, 81.0, text = "3", fill = "#ffffff", font = (default_font, int(40.0)))

# Reset Button
tab1_reset_button_img = PhotoImage(master=tab1, file = f"./resources/images/buttons/reset_button_normal.png")
tab1_reset_button = CustomButton.lambda_button(tab1, tab1_reset_button_img, t1.reset_app, tab1_canvas, tab1_text_tags)
tab1_reset_button.place(x = 134, y = 131, width = 40, height = 42)

# Undo Button
tab1_undo_button_img = PhotoImage(master=tab1, file = f"./resources/images/buttons/undo_button_normal.png")
tab1_undo_button = CustomButton.lambda_button(tab1, tab1_undo_button_img, t1.undo, tab1_canvas, tab1_text_tags)
tab1_undo_button.place(x = 31, y = 405, width = 48, height = 50)

# Redo Button
tab1_redo_button_img = PhotoImage(master=tab1, file = f"./resources/images/buttons/redo_button_normal.png")
tab1_redo_button = CustomButton.lambda_button(tab1, tab1_redo_button_img, t1.redo, tab1_canvas, tab1_text_tags)
tab1_redo_button.place(x = 229, y = 405, width = 48, height = 50)

# Endturn Button
tab1_endturn_button_img = PhotoImage(master=tab1, file = f"./resources/images/buttons/endturn_button_normal.png")
tab1_endturn_button = CustomButton.lambda_button(tab1, tab1_endturn_button_img, t1.end_turn, tab1_canvas, tab1_text_tags)
tab1_endturn_button.place(x = 102, y = 405, width = 104, height = 50)

# Loading Minus and Plus Buttons
tab1_minus_button_img = PhotoImage(master=tab1, file = f"./resources/images/buttons/minus_button_normal.png")
tab1_plus_button_img = PhotoImage(master=tab1, file = f"./resources/images/buttons/plus_button_normal.png")

# Used Energy Row
tab1_text_tags['used'] = tab1_canvas.create_text(153.0, 200.5, text = "0",fill = "#ffffff",font = (default_font, int(30.0)))
# used_text_tag = tab1_canvas.create_text(153.0, 166.5,text = "0",fill = "#ffffff",font = (default_font, int(30.0)))

tab1_used_minus_button = CustomButton.lambda_button(tab1, tab1_minus_button_img, t1.return_energy, tab1_canvas, tab1_text_tags, tab1_text_tags['used'])
tab1_used_minus_button.place(x = 75, y = 178, width = 44, height = 46)

tab1_used_plus_button = CustomButton.lambda_button(tab1, tab1_plus_button_img, t1.remove_energy, tab1_canvas, tab1_text_tags, tab1_text_tags['used'])
tab1_used_plus_button.place(x = 188, y = 178, width = 45, height = 46)

# Gained Energy Row
tab1_text_tags['gained'] = tab1_canvas.create_text(153.0, 275.5,text = "0",fill = "#ffffff",font = (default_font, int(30.0)))
# gained_text_tag = tab1_canvas.create_text(153.0, 241.5,text = "0",fill = "#ffffff",font = (default_font, int(30.0)))

tab1_gained_minus_button = CustomButton.lambda_button(tab1, tab1_minus_button_img, t1.remove_gained_energy, tab1_canvas, tab1_text_tags, tab1_text_tags['gained'])
tab1_gained_minus_button.place(x = 75, y = 253, width = 44, height = 46)

tab1_gained_plus_button = CustomButton.lambda_button(tab1, tab1_plus_button_img, t1.add_energy, tab1_canvas, tab1_text_tags, tab1_text_tags['gained'])
tab1_gained_plus_button.place(x = 189, y = 253, width = 44, height = 46)

# Destroyed Energy Row
tab1_text_tags['destroyed'] = tab1_canvas.create_text(153.0, 351.5, text = "0",fill = "#ffffff",font = (default_font, int(30.0)))
# destroyed_text_tag = tab1_canvas.create_text(153.0, 316.5,text = "0",fill = "#ffffff",font = (default_font, int(30.0)))

tab1_destroyed_minus_button = CustomButton.lambda_button(tab1, tab1_minus_button_img, t1.return_energy, tab1_canvas, tab1_text_tags, tab1_text_tags['destroyed'])
tab1_destroyed_minus_button.place(x = 75, y = 328, width = 44, height = 46)

tab1_destroyed_plus_button = CustomButton.lambda_button(tab1, tab1_minus_button_img, t1.remove_energy, tab1_canvas, tab1_text_tags, tab1_text_tags['destroyed'])
tab1_destroyed_plus_button.place(x = 189, y = 328, width = 44, height = 46)

#####################################################################################################
################################## TAB 2 ############################################################
tab2_text_tags = dict({
    'win' : 0,
    'loss' : 0,
    'draw' : 0,
    'mmr' : 0,
    'rank' : 0,
    'tatal' : 0,
    'average' : 0,
    'today' : 0,
    'yesterday' : 0,
})

tab2_canvas = Canvas(
    tab2,
    bg = "#ffffff",
    height = 461,
    width = 308,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
tab2_canvas.place(x = 0, y = 0)

tab2_background_img = PhotoImage(master=tab2, file = f"./resources/images/backgrounds/tab2_background.png")
tab2_background = tab2_canvas.create_image(154.0, 230.5, image=tab2_background_img)

# Loading the Plus and Minus Buttons for the winrate counter
tab2_minus_button_img = PhotoImage(master=tab2, file = f"./resources/images/buttons/minus_button_small.png")
tab2_plus_button_img = PhotoImage(master=tab2, file = f"./resources/images/buttons/plus_button_small.png")

# Tab2 Reset Button
tab2_reset_button_img = PhotoImage(master=tab2, file = f"./resources/images/buttons/reset_button_top.png")
tab2_reset_button = CustomButton.lambda_button(tab2, tab2_reset_button_img, t2.reset_counters, tab2_canvas, tab2_text_tags)
tab2_reset_button.place(x = 134, y = 0, width = 40, height = 39)

# Tab2 Win Counter
tab2_text_tags['win'] = tab2_canvas.create_text(
    66.0, 82.0,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(36.0)))

tab2_win_minus_button = CustomButton.lambda_button(tab2, tab2_minus_button_img, t2.minus_to_counter, tab2_canvas, tab2_text_tags['win'], tab2_text_tags)
tab2_win_minus_button.place(x = 35, y = 130, width = 30, height = 33)
tab2_win_plus_button = CustomButton.lambda_button(tab2, tab2_plus_button_img, t2.add_to_counter, tab2_canvas, tab2_text_tags['win'], tab2_text_tags)
tab2_win_plus_button.place(x = 69, y = 130, width = 30, height = 32)

# Tab2 Loss Counter
tab2_text_tags['loss'] = tab2_canvas.create_text(
    153.0, 82.0,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(36.0)))

tab2_loss_minus_button = CustomButton.lambda_button(tab2, tab2_minus_button_img, t2.minus_to_counter, tab2_canvas, tab2_text_tags['loss'], tab2_text_tags)
tab2_loss_minus_button.place(x = 122, y = 130, width = 30, height = 33)
tab2_loss_plus_button = CustomButton.lambda_button(tab2, tab2_plus_button_img, t2.add_to_counter, tab2_canvas, tab2_text_tags['loss'], tab2_text_tags)
tab2_loss_plus_button.place(x = 156, y = 130, width = 30, height = 32)

# Tab2 Draw Counter
tab2_text_tags['draw'] = tab2_canvas.create_text(
    240.0, 82.0,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(36.0)))

tab2_draw_minus_button = CustomButton.lambda_button(tab2, tab2_minus_button_img, t2.minus_to_counter, tab2_canvas, tab2_text_tags['draw'], tab2_text_tags)
tab2_draw_minus_button.place(x = 209, y = 130, width = 30, height = 33)
tab2_draw_plus_button = CustomButton.lambda_button(tab2, tab2_plus_button_img, t2.add_to_counter, tab2_canvas, tab2_text_tags['draw'], tab2_text_tags)
tab2_draw_plus_button.place(x = 243, y = 130, width = 30, height = 32)

tab2_update_button_img = PhotoImage(master=tab2, file = f"./resources/images/buttons/update_button.png")
tab2_update_button = CustomButton.lambda_button(tab2, tab2_update_button_img, t2.update_data, tab2_canvas, tab2_text_tags)
tab2_update_button.place(x = 137, y = 404, width = 33, height = 36)

tab2_text_tags['mmr'] = tab2_canvas.create_text(
    100.0, 220.0,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(24.0)))

tab2_text_tags['rank'] = tab2_canvas.create_text(
    208.0, 220.0,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(13.0)))

tab2_text_tags['total'] = tab2_canvas.create_text(
    100.0, 304,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(24.0)))

tab2_text_tags['average'] = tab2_canvas.create_text(
    209.0, 368,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(24.0)))

tab2_text_tags['today'] = tab2_canvas.create_text(
    209.0, 304,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(24.0)))

tab2_text_tags['yesterday'] = tab2_canvas.create_text(
    100.0, 368,
    text = "0",
    fill = "#ffffff",
    font = (default_font, int(24.0)))


#####################################################################################################
################################## TAB 3 ############################################################
tab3_canvas = Canvas(
    tab3,
    bg = "#ffffff",
    height = 461,
    width = 308,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
tab3_canvas.place(x = 0, y = 0)

background_img = PhotoImage(master= tab3, file = f"./resources/images/backgrounds/tab3_background.png")
background = tab3_canvas.create_image(
    154.0, 230.5,
    image=background_img)

# GCASH
tab3_gcash = tab3_canvas = Text(
    tab3,
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font = (default_font, int(18.0)))
tab3_gcash.insert(INSERT, "09618491026")
tab3_gcash.configure(state='disabled')
tab3_gcash.place(
    x = 157, y = 294,
    width = 126,
    height = 36)

# RONIN
tab3_ronin_copy_buttom_img = PhotoImage(master=tab3, file = f"./resources/images/buttons/copy_button_normal.png")
tab3_ronin_copy_buttom = CustomButton.lambda_button(tab3, tab3_ronin_copy_buttom_img, t3.copy_address, window,'ronin')
tab3_ronin_copy_buttom.place(x = 245, y = 330, width = 40, height = 42)

tab3_ronin = tab3_canvas = Text(
    tab3,
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font = (default_font, int(18.0)))
tab3_ronin.insert(INSERT, "ronin:595529e52197c0b7630929f1f472eccbb9bdd3c1")
tab3_ronin.configure(state='disabled')
tab3_ronin.place(
    x = 157, y = 335,
    width = 85,
    height = 36)

# METAMASK
tab3_meta_copy_buttom_img = PhotoImage(master=tab3, file = f"./resources/images/buttons/copy_button_normal.png")
tab3_meta_copy_buttom = CustomButton.lambda_button(tab3, tab3_meta_copy_buttom_img, t3.copy_address, window,'meta')
tab3_meta_copy_buttom.place(x = 245, y = 374, width = 40, height = 42)

tab3_metamask = tab3_canvas = Text(
    tab3,
    bd = 0,
    bg = "#ffffff",
    highlightthickness = 0,
    font = (default_font, int(18.0)))
tab3_metamask.insert(INSERT, "0x03BB719E81444fd2292b6f99858EFedDEF78A4F4")
tab3_metamask.configure(state='disabled')
tab3_metamask.place(
    x = 157, y = 379,
    width = 85,
    height = 36)


#####################################################################################################
################################## TAB 4 ############################################################
tab4_text_tags = dict({
    'opacity' : 0,
})

tab4_canvas = Canvas(
    tab4,
    bg = "#ffffff",
    height = 461,
    width = 308,
    bd = 0,
    highlightthickness = 0,
    relief = "ridge")
tab4_canvas.place(x = 0, y = 0)

tab4_background_img = PhotoImage(master=tab4, file = f"./resources/images/backgrounds/tab4_background.png")
tab4_background = tab4_canvas.create_image(
    154.0, 230.5,
    image=tab4_background_img)

tab4_text_tags['opacity'] = tab4_canvas.create_text(
    153.5, 74.0,
    text = "100",
    fill = "#ffffff",
    font = (default_font, int(33.0)))

# SMALL MINUS BUTTON
tab4_minus_button_small_img = PhotoImage(master=tab4, file = f"./resources/images/buttons/minus_button_small.png")
tab4_minus_button_small = CustomButton.lambda_button(tab4, tab4_minus_button_small_img, t4.opacity_change, tab4_canvas, window, "minus-small", tab4_text_tags['opacity'])

tab4_minus_button_small.place(
    x = 37, y = 58,
    width = 30,
    height = 33)

# NORMAL MINUS BUTTON
tab4_minus_button_normal_img = PhotoImage(master=tab4, file = f"./resources/images/buttons/minus_button_normal.png")
tab4_minus_button_normal = CustomButton.lambda_button(tab4, tab4_minus_button_normal_img, t4.opacity_change, tab4_canvas, window, "minus-normal", tab4_text_tags['opacity'])

tab4_minus_button_normal.place(
    x = 69, y = 51,
    width = 44,
    height = 46)

# SMALL PLUS BUTTON
tab4_plus_button_small_img = PhotoImage(master=tab4, file = f"./resources/images/buttons/plus_button_small.png")
tab4_plus_button_small = CustomButton.lambda_button(tab4, tab4_plus_button_small_img, t4.opacity_change, tab4_canvas, window, "plus-small", tab4_text_tags['opacity'])

tab4_plus_button_small.place(
    x = 239, y = 58,
    width = 29,
    height = 32)

# NORMAL PLUS BUTTON
tab4_plus_button_normal_img = PhotoImage(master=tab4, file = f"./resources/images/buttons/plus_button_normal.png")
tab4_plus_button_normal = CustomButton.lambda_button(tab4, tab4_plus_button_normal_img, t4.opacity_change, tab4_canvas, window, "plus-normal", tab4_text_tags['opacity'])

tab4_plus_button_normal.place(
    x = 192, y = 51,
    width = 45,
    height = 46)
#####################################################################################################
################################## TAB X ############################################################

t2.tab2_load(tab2_canvas, tab2_text_tags)
t4.load_opacity(tab4_canvas, window, tab4_text_tags['opacity'])


# Function that is called to properly terminate the program from the background
def terminate_program():
    window.quit()
window.protocol('WM_DELETE_WINDOW', terminate_program)


window.resizable(False, False)
window.mainloop()
sys.exit()
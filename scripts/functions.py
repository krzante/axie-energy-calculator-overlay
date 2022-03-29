from tkinter import *
from tkinter import messagebox
import numpy
from asteval import Interpreter
import json

aeval = Interpreter()

# Dictionary of the prev round
undo_round = {
    "round":"1",
    "energy": "3",
    "base_energy": "3",
    "used": "0",
    "gained": "0",
    "destroyed": "0"
}

# Dictionary for the redo button
redo_round = {
    "round":"1",
    "energy": "3",
    "base_energy": "3",
    "used": "0",
    "gained": "0",
    "destroyed": "0"
}

# Dictionary for saving files
tab2_data = {
    "win":"0",
    "loss": "0",
    "draw": "0",
    "slp": "0"
}

tab4_data = {
    "opacity":0.6
}

# global current_base_energy
current_base_energy = "3"


class Tab1:
    def _reset_rows(canvas_arg, tab_tags_arg):
        canvas_arg.itemconfig(tab_tags_arg['used'], text = 0)
        canvas_arg.itemconfig(tab_tags_arg['gained'], text = 0)
        canvas_arg.itemconfig(tab_tags_arg['destroyed'], text = 0)
        
        
    def reset_app(canvas_arg, tab_tags_arg):
        global current_base_energy
        redo_round['round'] = canvas_arg.itemcget(tab_tags_arg['round'], 'text')
        redo_round['energy'] = canvas_arg.itemcget(tab_tags_arg['energy'], 'text')
        redo_round['used'] = canvas_arg.itemcget(tab_tags_arg['used'], 'text')
        redo_round['gained'] = canvas_arg.itemcget(tab_tags_arg['gained'], 'text')
        redo_round['destroyed'] = canvas_arg.itemcget(tab_tags_arg['destroyed'], 'text')

        canvas_arg.itemconfig(tab_tags_arg['round'], text = 1)
        canvas_arg.itemconfig(tab_tags_arg['energy'], text = 3)
        current_base_energy = 3

        Tab1._reset_rows(canvas_arg, tab_tags_arg)

        undo_round["round"] = "1"
        undo_round["energy"] = "3"
        undo_round['used'] = "0"
        undo_round['gained'] = "0"
        undo_round['destroyed'] = "0"

        print("[Reset]")
        print("Undo Base Energy: " + str(undo_round['base_energy']))
        print("Redo Base Energy: " + str(redo_round['base_energy']))
        print("Current Base Energy: " +str(current_base_energy))



    def end_turn(canvas_arg, tab_tags_arg):
        global current_base_energy
        round_num = int(canvas_arg.itemcget(tab_tags_arg['round'], 'text'))
        energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))

        undo_round["round"] = round_num
        undo_round["energy"] = energy_num
        undo_round['base_energy'] = current_base_energy
        undo_round['used'] = int(canvas_arg.itemcget(tab_tags_arg['used'], 'text'))
        undo_round['gained'] = int(canvas_arg.itemcget(tab_tags_arg['gained'], 'text'))
        undo_round['destroyed'] = int(canvas_arg.itemcget(tab_tags_arg['destroyed'], 'text'))

        energy_num = numpy.clip((energy_num + 2), 0, 10)
        redo_round['base_energy'] = energy_num
        current_base_energy = redo_round['base_energy']

        canvas_arg.itemconfig(tab_tags_arg['round'], text = str(round_num+1))
        canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num))
        Tab1._reset_rows(canvas_arg, tab_tags_arg)
        print("[End Turn]")
        print("Undo Base Energy: " + str(undo_round['base_energy']))
        print("Redo Base Energy: " + str(redo_round['base_energy']))
        print("Current Base Energy: " +str(current_base_energy))
    

    def undo(canvas_arg, tab_tags_arg):
        global current_base_energy
        if int(canvas_arg.itemcget(tab_tags_arg['round'], 'text')) != int(undo_round["round"]):
            redo_round['round'] = canvas_arg.itemcget(tab_tags_arg['round'], 'text')
            redo_round['energy'] = canvas_arg.itemcget(tab_tags_arg['energy'], 'text')
            redo_round['base_energy'] = current_base_energy
            redo_round['used'] = canvas_arg.itemcget(tab_tags_arg['used'], 'text')
            redo_round['gained'] = canvas_arg.itemcget(tab_tags_arg['gained'], 'text')
            redo_round['destroyed'] = canvas_arg.itemcget(tab_tags_arg['destroyed'], 'text')

            canvas_arg.itemconfig(tab_tags_arg['round'], text = undo_round["round"])
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = undo_round["energy"])
            current_base_energy = undo_round['base_energy']

            canvas_arg.itemconfig(tab_tags_arg['used'], text = undo_round["used"])
            canvas_arg.itemconfig(tab_tags_arg['gained'], text = undo_round["gained"])
            canvas_arg.itemconfig(tab_tags_arg['destroyed'], text = undo_round["destroyed"])
            print("[Undo]")
            print("Undo Base Energy: " + str(undo_round['base_energy']))
            print("Redo Base Energy: " + str(redo_round['base_energy']))
            print("Current Base Energy: " +str(current_base_energy))

    
    def redo(canvas_arg, tab_tags_arg):
        global current_base_energy
        if int(canvas_arg.itemcget(tab_tags_arg['round'], 'text')) != int(redo_round["round"]):
            canvas_arg.itemconfig(tab_tags_arg['round'], text = redo_round["round"])
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = redo_round["energy"])
            
            current_base_energy = redo_round['base_energy']

            canvas_arg.itemconfig(tab_tags_arg['used'], text = redo_round["used"])
            canvas_arg.itemconfig(tab_tags_arg['gained'], text = redo_round["gained"])
            canvas_arg.itemconfig(tab_tags_arg['destroyed'], text = redo_round["destroyed"])
            print("[Redo]")
            print("Undo Base Energy: " + str(undo_round['base_energy']))
            print("Redo Base Energy: " + str(redo_round['base_energy']))
            print("Current Base Energy: " +str(current_base_energy))

    

    def remove_energy(canvas_arg, tab_tags_arg, field_arg):
        energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
        if energy_num-1 >= 0:
            used_num = int(canvas_arg.itemcget(field_arg, 'text'))
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num - 1))
            canvas_arg.itemconfig(field_arg, text = str(used_num + 1))
    

    def return_energy(canvas_arg, tab_tags_arg, field_arg):
        used_num = int(canvas_arg.itemcget(field_arg, 'text'))
        if used_num-1 >= 0:
            energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
            if energy_num < int(current_base_energy):
                canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num + 1))
            canvas_arg.itemconfig(field_arg, text = str(used_num - 1))
    

    def add_energy(canvas_arg, tab_tags_arg, field_arg):
        energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
        if energy_num < 10:
            gained_num = int(canvas_arg.itemcget(field_arg, 'text'))
            canvas_arg.itemconfig(field_arg, text = str(gained_num + 1))
            energy_num = numpy.clip((energy_num  + 1), 0, 10)
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num))
        
    

    def remove_gained_energy(canvas_arg, tab_tags_arg, field_arg):
        gained_num = int(canvas_arg.itemcget(field_arg, 'text'))
        if gained_num - 1 >= 0:
            energy_num = int(canvas_arg.itemcget(tab_tags_arg['energy'], 'text'))
            if energy_num != int(current_base_energy):
                energy_num = numpy.clip((energy_num  - 1), 0, 10)
            canvas_arg.itemconfig(tab_tags_arg['energy'], text = str(energy_num))
            canvas_arg.itemconfig(field_arg, text = str(gained_num - 1))

############################################################################################################
############################################################################################################

class Tab2:
    def add_to_counter(canvas_arg, field_arg, tab_tags_arg):
        counter_num = int(canvas_arg.itemcget(field_arg, 'text')) + 1
        if counter_num >= 100:
            canvas_arg.itemconfig(field_arg, font = "{Aldo the Apache} 26")
        canvas_arg.itemconfig(field_arg, text = str(counter_num))
        Tab2.tab2_save(canvas_arg, tab_tags_arg)
        

    def minus_to_counter(canvas_arg, field_arg, tab_tags_arg):
        counter_num = int(canvas_arg.itemcget(field_arg, 'text'))
        if counter_num != 0:
            counter_num -= 1
            canvas_arg.itemconfig(field_arg, text = str(counter_num))
            if counter_num <= 99:
                canvas_arg.itemconfig(field_arg, font = "{Aldo the Apache} 36")
            Tab2.tab2_save(canvas_arg, tab_tags_arg)


    def reset_counters(canvas_arg, tab_tags_arg):
        canvas_arg.itemconfig(tab_tags_arg['win'], text = "0")
        canvas_arg.itemconfig(tab_tags_arg['loss'], text = "0")
        canvas_arg.itemconfig(tab_tags_arg['draw'], text = "0")
        Tab2.tab2_save(canvas_arg, tab_tags_arg)
    

    def add_to_calc(symbol, screen_arg):
        screen_content = screen_arg.get()
        if screen_content == "0" or screen_content == "None" or screen_content == "ERROR":
            Tab2.clear_calc(screen_arg)
        screen_arg.insert(END, symbol)
    

    def del_calc(screen_arg):
        screen_content = screen_arg.get()
        if screen_content != "":
            # https://stackoverflow.com/questions/51733663/how-to-delete-single-character-from-entry-widget-tkinter/51733802
            screen_arg.delete(len(screen_content)-1)
    

    def clear_calc(screen_arg):
        screen_arg.delete(0, END)
    

    def eval_calc(canvas_arg, tab_tags_arg):
        screen_content = tab_tags_arg['calc'].get()
        try:
            tab2_calculation = str(aeval(screen_content))
            Tab2.clear_calc(tab_tags_arg['calc'])
            tab_tags_arg['calc'].insert(INSERT, tab2_calculation)
        except:
            Tab2.clear_calc(tab_tags_arg['calc'])
            tab_tags_arg['calc'].insert(INSERT, "ERROR")
        Tab2.tab2_save(canvas_arg, tab_tags_arg)
    
    
    def tab2_save(canvas_arg, tab_tags_arg):
        tab2_data["win"] = canvas_arg.itemcget(tab_tags_arg['win'], 'text')
        tab2_data["loss"] = canvas_arg.itemcget(tab_tags_arg['loss'], 'text')
        tab2_data["draw"] = canvas_arg.itemcget(tab_tags_arg['draw'], 'text')
        screen_content = tab_tags_arg['calc'].get()
        if screen_content == "" or screen_content == 'None' or screen_content == 'ERROR':
            tab2_data["slp"] = "0"
        else:
            tab2_data["slp"] = screen_content
        with open('./resources/saves/tab2.json', 'w') as fjson:
            json.dump(tab2_data, fjson)


    def tab2_load(canvas_arg, tab_tags_args):
        data = {}
        with open('./resources/saves/tab2.json', 'r') as fjson:
            data = json.load(fjson)

        canvas_arg.itemconfig(tab_tags_args['win'], text = data["win"])
        canvas_arg.itemconfig(tab_tags_args['loss'], text = data["loss"])
        canvas_arg.itemconfig(tab_tags_args['draw'], text = data["draw"])
        Tab2.clear_calc(tab_tags_args['calc'])
        tab_tags_args['calc'].insert(INSERT, str(data['slp']))

############################################################################################################
############################################################################################################
class Tab3:
    def copy_address(window_arg, wallet):
        ronin_address = 'ronin:595529e52197c0b7630929f1f472eccbb9bdd3c1'
        meta_address = '0x03BB719E81444fd2292b6f99858EFedDEF78A4F4'
        current_address = ''
        if wallet == "ronin":
            current_address = ronin_address
        elif wallet == "meta":
            current_address = meta_address

        new_window = Tk()
        new_window.withdraw()
        new_window.clipboard_clear()
        new_window.clipboard_append(current_address)
        new_window.destroy()
        messagebox.showinfo(
            title="Successfully Copied", 
            message="--------------------------------------\nAddress Copied to Clipboard\n--------------------------------------\n{}".format(current_address), 
            parent=window_arg)

############################################################################################################
############################################################################################################

class Tab4:
    def opacity_change(canvas_arg, window_arg, operation_arg, opacity_tag):
        if operation_arg == "plus-normal":
            tab4_data["opacity"] = round(float(numpy.clip(tab4_data["opacity"] + 0.05, 0.1, 1.0)),2)
        elif operation_arg == "minus-normal":
            tab4_data["opacity"] = round(float(numpy.clip(tab4_data["opacity"] - 0.05, 0.1, 1.0)),2)
        elif operation_arg == "plus-small":
            tab4_data["opacity"] = round(float(numpy.clip(tab4_data["opacity"] + 0.01, 0.1, 1.0)),2)
        elif operation_arg == "minus-small":
            tab4_data["opacity"] = round(float(numpy.clip(tab4_data["opacity"] - 0.01, 0.1, 1.0)),2)

        canvas_arg.itemconfig(opacity_tag, text = str(int(round(float(tab4_data["opacity"])*100))))
        window_arg.attributes('-alpha', tab4_data["opacity"])
        Tab4.save_opacity()
        print("Opacity Changed")

    
    def save_opacity():
        with open('./resources/saves/tab4.json', 'w') as fjson:
            json.dump(tab4_data, fjson)


    def load_opacity(canvas_arg, window_arg, opactity_tag):
        data = {}
        with open('./resources/saves/tab4.json', 'r') as fjson:
            data = json.load(fjson)

        canvas_arg.itemconfig(opactity_tag, text = str(int(round(float(data["opacity"])*100))))
        tab4_data["opacity"] = data["opacity"]
        window_arg.attributes('-alpha', float(data["opacity"]))

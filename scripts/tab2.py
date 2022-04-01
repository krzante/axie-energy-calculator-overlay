# Tab 2 Functions
from tkinter import *
from asteval import Interpreter
import json

aeval = Interpreter()

# Dictionary for saving files
tab2_data = {
    "win":"0",
    "loss": "0",
    "draw": "0",
    "slp": "0"
}

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
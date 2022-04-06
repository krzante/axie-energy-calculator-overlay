# Tab 2 Functions
import os
from tkinter import *
from asteval import Interpreter
from dotenv import load_dotenv
from datetime import *
from tkinter import messagebox
load_dotenv()
import http.client
import json
import webbrowser

aeval = Interpreter()

# Dictionary for saving files
tab2_data = {
    "win":"0",
    "loss": "0",
    "draw": "0",
    "mmr": "0",
    "rank": "0", 
    "total": "0",
    "average": "0",
    "today": "0",
    "yesterday": "0"
}

wallet = ""
date_format_str = '%d/%m/%Y %H:%M:%S.%f'
timeout = dict({
    'time' : '01/1/0001 00:00:00.000000'
})

class Tab2:
    def add_to_counter(canvas_arg, field_arg, tab_tags_arg) -> None:
        counter_num = int(canvas_arg.itemcget(field_arg, 'text')) + 1
        if counter_num >= 100:
            canvas_arg.itemconfig(field_arg, font = "{Aldo the Apache} 26")
        canvas_arg.itemconfig(field_arg, text = str(counter_num))
        Tab2.tab2_save(canvas_arg, tab_tags_arg)
        

    def minus_to_counter(canvas_arg, field_arg, tab_tags_arg) -> None:
        counter_num = int(canvas_arg.itemcget(field_arg, 'text'))
        if counter_num != 0:
            counter_num -= 1
            canvas_arg.itemconfig(field_arg, text = str(counter_num))
            if counter_num <= 99:
                canvas_arg.itemconfig(field_arg, font = "{Aldo the Apache} 36")
            Tab2.tab2_save(canvas_arg, tab_tags_arg)


    def reset_counters(canvas_arg, tab_tags_arg) -> None:
        canvas_arg.itemconfig(tab_tags_arg['win'], text = "0")
        canvas_arg.itemconfig(tab_tags_arg['loss'], text = "0")
        canvas_arg.itemconfig(tab_tags_arg['draw'], text = "0")
        Tab2.tab2_save(canvas_arg, tab_tags_arg)

    
    def tab2_save(canvas_arg, tab_tags_arg) -> None:
        tab2_data["win"] = canvas_arg.itemcget(tab_tags_arg['win'], 'text')
        tab2_data["loss"] = canvas_arg.itemcget(tab_tags_arg['loss'], 'text')
        tab2_data["draw"] = canvas_arg.itemcget(tab_tags_arg['draw'], 'text')

        tab2_data["mmr"] = canvas_arg.itemcget(tab_tags_arg['mmr'], 'text')
        tab2_data["rank"] = canvas_arg.itemcget(tab_tags_arg['rank'], 'text')
        tab2_data["total"] = canvas_arg.itemcget(tab_tags_arg['total'], 'text')
        tab2_data["average"] = canvas_arg.itemcget(tab_tags_arg['average'], 'text')
        tab2_data["today"] = canvas_arg.itemcget(tab_tags_arg['today'], 'text')
        tab2_data["yesterday"] = canvas_arg.itemcget(tab_tags_arg['yesterday'], 'text')

        with open('./resources/saves/tab2.json', 'w') as fjson:
            json.dump(tab2_data, fjson)


    def tab2_load(canvas_arg, tab_tags_args) -> None:
        global wallet
        data = {}
        with open('./resources/saves/tab2.json', 'r') as fjson:
            data = json.load(fjson)

        canvas_arg.itemconfig(tab_tags_args['win'], text = data["win"])
        canvas_arg.itemconfig(tab_tags_args['loss'], text = data["loss"])
        canvas_arg.itemconfig(tab_tags_args['draw'], text = data["draw"])

        canvas_arg.itemconfig(tab_tags_args['mmr'], text = data["mmr"])
        # canvas_arg.itemconfig(tab_tags_args['rank'], text = data["rank"])
        canvas_arg.itemconfig(tab_tags_args['total'], text = data["total"])
        canvas_arg.itemconfig(tab_tags_args['average'], text = data["average"])
        canvas_arg.itemconfig(tab_tags_args['today'], text = data["today"])
        canvas_arg.itemconfig(tab_tags_args['yesterday'], text = data["yesterday"])

        tab2_data["mmr"] = data["mmr"]
        tab2_data["rank"] = data["rank"]
        tab2_data["total"] = data["total"]
        tab2_data["average"] = data["average"]
        tab2_data["today"] = data["today"]
        tab2_data["yesterday"] = data["yesterday"]

        rank = int(data["rank"].replace(',', ''))
        Tab2.__resize_rank_text(canvas_arg, tab_tags_args['rank'], rank)
    

    # Reusable function for resizing the font of the rank number
    def __resize_rank_text(canvas_arg, rank_tag_arg, rank_arg) -> None:
        if rank_arg <= 99999:
            font_and_size = "{Aldo the Apache} 24"
        elif rank_arg <= 999999:
            font_and_size = "{Aldo the Apache} 18"
        elif rank_arg <= 9999999:
            font_and_size = "{Aldo the Apache} 13"

        canvas_arg.itemconfig(rank_tag_arg, font = font_and_size)
        canvas_arg.itemconfig(rank_tag_arg, text = "{:,}".format(int(rank_arg)))


    def __get_wallet() -> str:
        with open('./resources/wallet.txt') as fwallet:
            wallet = fwallet.read()
        
        wallet = wallet.replace('"', '')
        wallet = wallet.replace(' ', '')
        return str(wallet.replace('ronin:', '0x'))
    

    def __get_slp_data() -> dict:
        global wallet
        wallet = Tab2.__get_wallet()

        # https://rapidapi.com/jchbasco/api/axie-infinity
        conn = http.client.HTTPSConnection("axie-infinity.p.rapidapi.com")

        headers = {
            'X-RapidAPI-Host': "axie-infinity.p.rapidapi.com",
            'X-RapidAPI-Key': str(os.getenv("RAPIDAPI_KEY"))
            }

        conn.request("GET", "/get-update/{}?id={}".format(str(wallet), str(wallet)), headers=headers)

        res = conn.getresponse()
        data = res.read()

        # Converts response from string to dictionary
        return json.loads(data.decode("utf-8"))


    def update_data(canvas_arg, tab_tags_arg) -> None:
        data = Tab2.__get_slp_data()
        if not 'message' in data.keys():
            Tab2.__check_changes(canvas_arg, tab_tags_arg, data)

            Tab2.tab2_save(canvas_arg, tab_tags_arg)
        else:
            messagebox.showinfo(title='ERROR', message="Invalid Wallet Address", parent=canvas_arg)
            webbrowser.open('https://youtu.be/6Q_6imLGi1k')
    

    def __check_changes(canvas_arg, tab_tags_arg, data_arg) -> None:
        message = ""

        for key in tab2_data:
            tab2_data[key] = str(tab2_data[key]).replace(',', '')

        if int(data_arg['leaderboard']['elo']) > int(tab2_data['mmr']):
            canvas_arg.itemconfig(tab_tags_arg['mmr'], text = "{:,}".format(int(data_arg['leaderboard']['elo'])))
            message += "MMR +{}\n".format(int(data_arg['leaderboard']['elo']) - int(tab2_data["mmr"]))
        elif int(data_arg['leaderboard']['elo']) < int(tab2_data['mmr']):
            canvas_arg.itemconfig(tab_tags_arg['mmr'], text = "{:,}".format(int(data_arg['leaderboard']['elo'])))
            message += "MMR -{}\n".format(int(tab2_data["mmr"]) - int(data_arg['leaderboard']['elo']))

        if int(data_arg['leaderboard']['rank']) > int(tab2_data['rank']):
            rank = int(data_arg['leaderboard']['rank'])
            Tab2.__resize_rank_text(canvas_arg, tab_tags_arg['rank'], rank)
            message += "RANK +{}\n".format(int(data_arg['leaderboard']['rank']) - int(tab2_data["rank"]))
        elif int(data_arg['leaderboard']['rank']) < int(tab2_data['rank']):
            if int(tab2_data['rank']) - int(data_arg['leaderboard']['rank']) != 0:
                rank = int(data_arg['leaderboard']['rank'])
                Tab2.__resize_rank_text(canvas_arg, tab_tags_arg['rank'], rank)
                message += "RANK -{}\n".format(int(tab2_data["rank"]) - int(data_arg['leaderboard']['rank']))

        if int(data_arg['slp']['total']) > int(tab2_data['total']):
            canvas_arg.itemconfig(tab_tags_arg['total'], text = "{:,}".format(int(data_arg['slp']['total'])))
            message += "TOTAL SLP +{}\n".format(int(data_arg['slp']['total']) - int(tab2_data['total']))
        
        if int(data_arg['slp']['average']) > int(tab2_data['average']):
            canvas_arg.itemconfig(tab_tags_arg['average'], text = "{:,}".format(int(data_arg['slp']['average'])))
            message += "AVERAGE SLP +{}\n".format(int(data_arg['slp']['average']) - int(tab2_data['average']))
        elif int(data_arg['slp']['average']) < int(tab2_data['average']):
            canvas_arg.itemconfig(tab_tags_arg['average'], text = "{:,}".format(int(data_arg['slp']['average'])))
            message += "AVERAGE SLP -{}\n".format(int(tab2_data['average']) - int(data_arg['slp']['average']))
        
        if int(data_arg['slp']['todaySoFar']) > int(tab2_data['today']):
            canvas_arg.itemconfig(tab_tags_arg['today'], text = "{:,}".format(int(data_arg['slp']['todaySoFar'])))
            message += "TODAY SLP +{}\n".format(int(data_arg['slp']['todaySoFar']) - int(tab2_data['today']))

        canvas_arg.itemconfig(tab_tags_arg['yesterday'], text = "{:,}".format(int(data_arg['slp']['yesterdaySLP'])))

        if message != "":
            messagebox.showinfo(title='UPDATE', message=message, parent=canvas_arg)
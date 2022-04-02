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
timeout = dict({
    'time' : '01/1/0001 00:00:00.000000'
})

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

    
    def tab2_save(canvas_arg, tab_tags_arg):
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


    def tab2_load(canvas_arg, tab_tags_args):
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

        # Optimize this. It has a duplicate in another function.
        font_and_size = ""
        rank = int(data["rank"].replace(',', ''))
        if rank <= 99999:
            font_and_size = "{Aldo the Apache} 24"
        elif rank <= 999999:
            font_and_size = "{Aldo the Apache} 18"
        elif rank <= 9999999:
            font_and_size = "{Aldo the Apache} 13"

        canvas_arg.itemconfig(tab_tags_args['rank'], font = font_and_size)
        canvas_arg.itemconfig(tab_tags_args['rank'], text = "{:,}".format(int(rank)))

        print(Tab2.__check_time_file())
        if not Tab2.__check_time_file():
            Tab2.__create_time_file()
        else:
            Tab2.__load_time_file()
    

    # Checks if the time.json file exists
    def __check_time_file() -> bool:
        return os.path.exists('./resources/saves/time.json')


    def __create_time_file():
        Tab2.__save_time_file()
        # open('./resources/saves/time.json', 'w+')

        os.system('attrib +h ./resources/saves/time.json')
        print("created file")

    
    def __load_time_file():
        global timeout
        with open('./resources/saves/time.json', 'r') as fjson:
            timeout = json.load(fjson)
        print(timeout)

    
    def __save_time_file():
        global timeout
        os.system('attrib -h ./resources/saves/time.json')
        with open('./resources/saves/time.json', 'w') as fjson:
            json.dump(timeout, fjson)
        os.system('attrib +h ./resources/saves/time.json')



    def __get_wallet() -> str:
        # Getting the user's ronin address
        with open('./resources/wallet.json', 'r') as fjson:
            data = json.load(fjson)
        print(str(data['wallet'].replace('ronin:', '0x')))
        return str(data['wallet'].replace('ronin:', '0x'))
    

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


    def __timeout_message():
        return"""
        The free API has limited requests
        I need to limit request calls
        ---------------------------------------
        Please try again in {} minutes
        ---------------------------------------
        Thank you for understanding
        """


    def update_data(canvas_arg, tab_tags_args):
        if Tab2.__process_timeout(canvas_arg):
            data = Tab2.__get_slp_data()
            if not 'message' in data.keys():
                # print(data)
                    canvas_arg.itemconfig(tab_tags_args['mmr'], text = "{:,}".format(int(data['leaderboard']['elo'])))
                    canvas_arg.itemconfig(tab_tags_args['total'], text = "{:,}".format(int(data['slp']['total'])))
                    canvas_arg.itemconfig(tab_tags_args['average'], text = "{:,}".format(int(data['slp']['average'])))
                    canvas_arg.itemconfig(tab_tags_args['today'], text = "{:,}".format(int(data['slp']['todaySoFar'])))
                    canvas_arg.itemconfig(tab_tags_args['yesterday'], text = "{:,}".format(int(data['slp']['yesterdaySLP'])))

                    # Adjusting the size of the font based on the user's rank
                    rank = int(data['leaderboard']['rank'])
                    font_and_size = ""
                    if rank <= 99999:
                        font_and_size = "{Aldo the Apache} 24"
                    elif rank <= 999999:
                        font_and_size = "{Aldo the Apache} 18"
                    elif rank <= 9999999:
                        font_and_size = "{Aldo the Apache} 13"

                    canvas_arg.itemconfig(tab_tags_args['rank'], font = font_and_size)
                    canvas_arg.itemconfig(tab_tags_args['rank'], text = "{:,}".format(int(rank)))

                    Tab2.tab2_save(canvas_arg, tab_tags_args) 
            else:
                messagebox.showinfo(title='ERROR', message="Invalid Wallet Address", parent=canvas_arg)


    def __process_timeout(canvas_arg):
        global timeout
        date_format_str = '%d/%m/%Y %H:%M:%S.%f'
        startTime = datetime.strptime(timeout['time'], date_format_str)
        currentTime = datetime.now()
        timeLeft = currentTime - startTime
        if timeLeft <= timedelta(minutes=10):
            seconds = timeLeft.seconds
            minutes = (seconds//60)%60 
            messagebox.showinfo(title='Timeout', message=Tab2.__timeout_message().format(10-minutes), parent=canvas_arg)
            return False
        else:
            # Get current time and convert it from time object to string
            currentTime = datetime.now()
            timeout['time'] = currentTime.strftime('%d/%m/%Y %H:%M:%S.%f')
            Tab2.__save_time_file()
            return True
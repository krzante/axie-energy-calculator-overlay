# Tab4 Functions
import numpy as np
import json

tab4_data = {
    "opacity":0.6
}

class Tab4:
    def opacity_change(canvas_arg, window_arg, operation_arg, opacity_tag):
        if operation_arg == "plus-normal":
            tab4_data["opacity"] = round(float(np.clip(tab4_data["opacity"] + 0.05, 0.1, 1.0)),2)
        elif operation_arg == "minus-normal":
            tab4_data["opacity"] = round(float(np.clip(tab4_data["opacity"] - 0.05, 0.1, 1.0)),2)
        elif operation_arg == "plus-small":
            tab4_data["opacity"] = round(float(np.clip(tab4_data["opacity"] + 0.01, 0.1, 1.0)),2)
        elif operation_arg == "minus-small":
            tab4_data["opacity"] = round(float(np.clip(tab4_data["opacity"] - 0.01, 0.1, 1.0)),2)

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
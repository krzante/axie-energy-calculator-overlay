from tkinter import *

class CustomButton:
    def normal_button(root, img, func):
        return Button(
            root,
            image = img,
            text = "~",
            borderwidth = 0,
            highlightthickness = 0,
            command = func,
            relief = "flat")


    def lambda_button(root, img, func, param, param2 = "NULL", param3 = "NULL", param4 = "NULL"):
        if param4 != "NULL":
            return Button(
                root,
                image = img,
                borderwidth = 0,
                highlightthickness = 0,
                command = lambda:func(param,param2,param3,param4),
                relief = "flat")
        elif param3 != "NULL":
            return Button(
                root,
                image = img,
                borderwidth = 0,
                highlightthickness = 0,
                command = lambda:func(param,param2,param3),
                relief = "flat")
        elif param2 != "NULL":
                return Button(
                    root,
                    image = img,
                    borderwidth = 0,
                    highlightthickness = 0,
                    command = lambda:func(param,param2),
                    relief = "flat")
        else:
            return Button(
                root,
                image = img,
                borderwidth = 0,
                highlightthickness = 0,
                command = lambda:func(param),
                relief = "flat")
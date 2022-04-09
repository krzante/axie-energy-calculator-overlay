# Tab3 Functions
from tkinter import *
from tkinter import messagebox

class Tab3:
    def __show_message(wallet_arg):
        return \
            """
            -------------------------------------------------------------------
                                 Address Copied to Clipboard
            -------------------------------------------------------------------
            {}
            """.format(wallet_arg)
    

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
        messagebox.showinfo(
            title="Successfully Copied", 
            message=Tab3.__show_message(current_address), 
            parent=window_arg)
        new_window.destroy()
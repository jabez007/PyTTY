from tkinter import *
import sys

from InteractiveSSH import ShellHandler

# # # # 


import getpass
username = raw_input("Username: ")
password = getpass.getpass("Password: ")

# # # #


class IORedirector(object):
    '''A general class for redirecting I/O to this Text widget.'''
    def __init__(self, text_area):
        self.text_area = text_area

    def flush(self):
        sys.__stdout__.flush()


class StdoutRedirector(IORedirector):
    '''A class for redirecting stdout to this Text widget.'''
    def write(self, message):
        self.text_area.config(state = "normal")
        self.text_area.insert("end", message)
        self.text_area.config(state = "disabled")
        self.text_area.see("end")

# # # #


def send_command(event):
    shell.execute(event.char)

# # # #


root = Tk()

text_box = Text(root)
text_box.pack()
sys.stdout = StdoutRedirector(text_box)
text_box.bind("<Key>", send_command)

shell = ShellHandler("epic-cde",
                     username=username,
                     password=password)

root.mainloop()

# To stop redirecting stdout:
sys.stdout = sys.__stdout__

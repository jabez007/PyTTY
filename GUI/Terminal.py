from Tkinter import *
import sys


class Terminal(Frame):

    def __init__(self, master=None, cnf={}, **kwargs):
        Frame.__init__(self, master, cnf, **kwargs)

        self.text = Text()

        self._init_ui_()

        sys.stdout = self

    def __del__(self):
        # To stop redirecting stdout:
        sys.stdout = sys.__stdout__

    def _init_ui_(self):
        self.pack(side=TOP,
                  fill=BOTH,
                  expand=True)

        self.text = Text()
        self.text.config(state="disabled")
        self.text.pack(fill=BOTH,
                       expand=True)

    def write(self, message):
        self.text.config(state="normal")
        self.text.insert("end", message)
        self.text.config(state="disabled")
        self.text.see("end")

    def flush(self):
        sys.__stdout__.flush()

# # # #

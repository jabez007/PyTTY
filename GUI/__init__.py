from Tkinter import *
import Login
import Terminal


class PyTTY(Frame):

    def __init__(self, master=None, cnf={}, **kwargs):
        Frame.__init__(self, master, cnf, **kwargs)

        self.pack(fill=BOTH,
                  expand=True)

        self.login = Login.Login(self)
        self.terminal = Terminal.Terminal(self)
        self.terminal.text.bind("<Key>", self. send_command)

    def send_command(self, event):
        if self.login.shell:
            self.login.shell.execute(event.char)

# # # #


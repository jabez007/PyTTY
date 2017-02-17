from Tkinter import *
import tkMessageBox
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
        self.command = ""

    def send_command(self, event):
        # http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/key-names.html
        modifiers = ["Alt_L",
                     "Alt_R",
                     "Control_L",
                     "Control_R",
                     "Shift_L",
                     "Shift_R"]
        if event.keysym in modifiers:
            return

        special_chars = {"BackSpace": "\x08",
                         "Cancel": "",  # break key
                         "Caps_Lock": "",
                         "Delete": "",
                         "Down": "",  # down arrow
                         "End": "",
                         "Escape": "",
                         "Execute": "",
                         "F1": "",
                         "F2": "",
                         "F3": "",
                         "F4": "",
                         "F5": "",
                         "F6": "",
                         "F7": "",
                         "F8": "",
                         "F9": "",
                         "F10": "",
                         "F11": "",
                         "F12": "",
                         "Home": "",
                         "Insert": "",
                         "Left": "",  # left arrow
                         "Linefeed": "",  # linefeed (Ctrl+J)
                         "KP_0": "",  # numpad 0
                         "KP_1": "",
                         "KP_2": "",
                         "KP_3": "",
                         "KP_4": "",
                         "KP_5": "",
                         "KP_6": "",
                         "KP_7": "",
                         "KP_8": "",
                         "KP_9": "",
                         "KP_Add": "",
                         "KP_Begin": "",  # center key of numpad
                         "KP_Decimal": "",
                         "KP_Delete": "",
                         "KP_Divide": "",
                         "KP_Down": "",
                         "KP_End": "",
                         "KP_Enter": "\r",
                         "KP_Home": "",
                         "KP_Insert": "",
                         "KP_Left": "",
                         "KP_Multiply": "",
                         "KP_Next": "",  # PgDn on numpad
                         "KP_Prior": "",  # PgUp on numpad
                         "KP_Right": "",
                         "KP_Subtract": "",
                         "KP_Up": "",
                         "Next": "",  # PgDn
                         "Num_Lock": "",
                         "Pause": "",
                         "Print": "",  # print screen
                         "Prior": "",  # PgUp
                         "Return": "\r",  # enter or Ctrl+M
                         "Right": "",  # right arrow
                         "Scroll_Lock": "",
                         "Tab": "\x09",  # ASCII horizontal tab
                         "Up": ""  # up arrow
                         }
        symbol = event.keysym
        if symbol in special_chars:
            character = special_chars[symbol]
        else:
            character = event.char
        """
        if character:
            tkMessageBox.showinfo(__name__,
                                  "%s: %s" % (symbol, repr(character)))
        """
        if self.login.shell and character:
            self.login.shell.execute(character)

# # # #


from Tkinter import *
import tkMessageBox
from getpass import getuser
from paramiko import AuthenticationException
import InteractiveSSH


class Login(Frame):

    def __init__(self, master=None, cnf={}, **kwargs):
        Frame.__init__(self, master, cnf, **kwargs)

        self.environment = Entry()
        self.port = Entry()
        self.username = Entry()
        self.password = Entry()
        self.shell = None

        self._init_ui_()

    def _init_ui_(self):
        self.pack(side=TOP,
                  fill=X,
                  expand=True)

        self.environment = self._make_entry_("Environment:")

        self.port = self._make_entry_("Port:", width=5)
        self.port.insert(END, "22")

        self.username = self._make_entry_("Username:")
        self.username.insert(END, getuser())

        self.password = self._make_entry_("Password:", show="*")

        self.button = Button(self, text="Connect", command=self.connect)
        self.button.pack(side=LEFT)
        self.button.bind("<Return>", self.connect)

    def connect(self, event=None):
        if self.environment.cget("state") == "disabled":
            return

        env = self.environment.get()
        self.environment.config(state="disabled")

        prt = self.port.get()
        self.port.config(state="disabled")

        usr = self.username.get()
        self.username.config(state="disabled")

        pswrd = self.password.get()
        self.password.delete(0, END)
        self.password.config(state="disabled")

        try:
            self.shell = InteractiveSSH.ShellHandler(host=env,
                                                     port=int(prt),
                                                     username=usr,
                                                     password=pswrd)
        except (AuthenticationException, ValueError):
            tkMessageBox.showerror(__name__,
                                   "Login Failed")
            self.environment.config(state="normal")
            self.port.config(state="normal")
            self.username.config(state="normal")
            self.password.config(state="normal")

    def _make_entry_(self, label, width=None, **options):
        Label(self, text=label).pack(side=LEFT)
        entry = Entry(self, **options)
        if width:
            entry.config(width=width)
        entry.pack(side=LEFT)
        entry.bind("<Return>", self.connect)
        return entry

# # # #


if __name__ == "__main__":
    root = Tk()
    Login(root)
    root.mainloop()

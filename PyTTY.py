from tkinter import *
import GUI


root = Tk()
root.title("PtTTY")
# root.protocol("WM_DELETE_WINDOW", on_exit)
gui = GUI.PyTTY(root)
root.mainloop()
root.quit()

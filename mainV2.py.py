import tkinter as tk

class AccountManager(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        frameContainer = tk.Frame(self)

        frameContainer.pack(side="top", fill="both", expand = True)
        
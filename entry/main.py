from rangeCalculator import RangeCalculator
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

window = tk.Tk()
window.title("BattleTracker")
window.columnconfigure(0, minsize=200)
window.rowconfigure([0, 1, 2], minsize=50)
style = ThemedStyle(window)
style.theme_use("equilux")
bg = style.lookup('TLabel', 'background')
fg = style.lookup('TLabel', 'foreground')
window.configure(bg=style.lookup('TLabel', 'background'))

class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.lblGreeting = ttk.Label(master, text="Welcome to the BattleTracker")
        self.lblGreeting.grid(row=0, column=0)
        self.btnOpen = ttk.Button(master, command=self.inputWindow, text="Input Stats")
        self.btnOpen.grid(row=1, column=0)
        self.btnShow = ttk.Button(master, command=self.showLabel, text="Show name")
        self.btnShow.grid(row=2, column=0)
        self.btnShow["state"] = "disabled"
    
    def inputWindow(self):
        self.inWin = RangeCalculator(self.master)
        self.btnOpen["state"] = "disabled"
        self.btnOpen["state"] = "normal"
        self.btnShow["state"] = "normal"

    def showLabel(self):
        lblTest = ttk.Label(master=window, text=self.inWin.stats["name"])
        lblTest.grid(row=3, column=0)
        lblTest = ttk.Label(master=window, text=self.inWin.stats["hP"])
        lblTest.grid(row=3, column=1)
        lblTest = ttk.Label(master=window, text=self.inWin.stats["coordinate"])
        lblTest.grid(row=4, column=0)
        lblTest = ttk.Label(master=window, text=self.inWin.stats["height"])
        lblTest.grid(row=4, column=1)
        lblTest = ttk.Label(master=window, text=self.inWin.stats["size"])
        lblTest.grid(row=5, column=0)
        lblTest = ttk.Label(master=window, text=self.inWin.stats["notes"])
        lblTest.grid(row=5, column=1)

battleWin = mainWindow(window)

window.mainloop()
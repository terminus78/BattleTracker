from statCollector import StatCollector
from battleMap import BattleMap
from tooltip import *
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

window = tk.Tk()
window.title("BattleTracker")
#window.iconphoto(True, tk.PhotoImage(file='entry/bin/allyToken.png'))
window.columnconfigure(0, minsize=200)
window.rowconfigure([0, 1, 2], minsize=50)
styleDark = ThemedStyle(window)
styleDark.theme_use("equilux")
bg = styleDark.lookup('TLabel', 'background')
fg = styleDark.lookup('TLabel', 'foreground')
window.configure(bg=styleDark.lookup('TLabel', 'background'))
papyrusFont = ('Papyrus', 14)

class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.countdown = 5
        self.lblGreeting = ttk.Label(master, text="Welcome to the BattleTracker", font=papyrusFont)
        self.lblGreeting.grid(row=0, column=0)
        #self.btnOpen = ttk.Button(master, command=self.inputWindow, text="Input Creatures")
        #self.btnOpen.grid(row=1, column=0)
        self.lblOpening = ttk.Label(master=self.master, text="", font=papyrusFont)
        self.lblOpening.grid(row=1, column=0)
        self.lblWarning = ttk.Label(master=self.master, text="Warning: Closing this window will close the entire program")
        self.lblWarning.grid(row=3, column=0)
        self.btnMap = ttk.Button(master, command=self.showMap, text="Re-open Map")
        self.delayOpen()
    
    def inputWindow(self):
        self.inWin = StatCollector(self.master)

    def delayOpen(self):
        if self.countdown > 0:
            self.lblOpening.config(text="Opening map in {0}...".format(self.countdown))
            self.countdown -= 1
            self.master.after(1000, self.delayOpen)
        else:
            self.lblOpening.config(text="Map Opened")
            self.btnMap.grid(row=2, column=0)
            self.showMap()
            self.master.iconify()

    def showMap(self):
        self.mapWin = BattleMap([32, 46], self.master)

battleWin = mainWindow(window)

window.mainloop()
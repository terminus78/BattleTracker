from statCollector import StatCollector
from battleMap import BattleMap
from tooltip import *
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle
from globals import Globals

window = tk.Tk()
window.title("BattleTracker")
window.iconphoto(True, tk.PhotoImage(file='bystanderToken.png'))
window.columnconfigure(0, minsize=200)
window.rowconfigure([0, 1, 2], minsize=50)
styleDark = ThemedStyle(window)
styleDark.theme_use("equilux")
bg = styleDark.lookup('TLabel', 'background')
fg = styleDark.lookup('TLabel', 'foreground')
window.configure(bg=styleDark.lookup('TLabel', 'background'))
papyrusFont = ('Papyrus', 14)
glbs = Globals()

class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.lblGreeting = ttk.Label(master, text="Welcome to the BattleTracker", font=papyrusFont)
        self.lblGreeting.grid(row=0, column=0)
        self.btnOpen = ttk.Button(master, command=self.inputWindow, text="Input Stats")
        self.btnOpen.grid(row=1, column=0)
        self.btnMap = ttk.Button(master, command=self.showMap, text="Show Map")
        self.btnMap.grid(row=2, column=0)
    
    def inputWindow(self):
        self.inWin = StatCollector(self.master)

    def showMap(self):
        self.mapWin = BattleMap([32, 46], self.master)

battleWin = mainWindow(window)

if glbs.getOpenBattleWin():
    if glbs.getRefresh():
        self.mapWin.refreshMap()

window.mainloop()
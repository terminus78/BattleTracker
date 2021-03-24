import math
import tkinter as tk
import pathlib
import json
import os
from tkinter import ttk, font
from ttkthemes import ThemedStyle
from tooltip import *

class BattleMap(object):
    def __init__(self, mapSize, master):
        self.mapSize = mapSize
        self.mapWin = tk.Toplevel(master)
        self.mapWin.title("Battle Map")
        style = ThemedStyle(self.mapWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.mapWin.configure(bg=style.lookup('TLabel', 'background'))
        self.mapWin.rowconfigure(0, minsize=100)
        self.mapWin.rowconfigure(1, weight=1, minsize=100)
        self.mapWin.columnconfigure(0, weight=1, minsize=100)
        lblMap = ttk.Label(master=self.mapWin, text="BattleMap", font=('Papyrus', '16'))
        lblMap.grid(row=0, column=0)
        gridFrame = ttk.Frame(master=self.mapWin)
        gridFrame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        
        mapFrames = []

        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                space = ttk.Frame(master=gridFrame, relief=tk.RAISED, borderwidth=1)
                space.grid(row=i, column=j, sticky='nsew')
                gridFrame.rowconfigure(i, weight=1, minsize=10)
                gridFrame.columnconfigure(j, weight=1, minsize=10)
                #lblGrid = ttk.Label(master=space, text=f"{i+1}, {j+1}")
                #lblGrid.grid(row=0, column=0, sticky='nw')
                CreateToolTip(space, text=f"{i+1}, {j+1}")
                mapFrames.append(space)
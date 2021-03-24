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
        self.mapWin.rowconfigure(0, weight=1, minsize=200)
        self.mapWin.columnconfigure(0, weight=1, minsize=200)
        gridFrame = ttk.Frame(master=self.mapWin)
        gridFrame.grid(row=0, column=0, sticky='nsew')
        
        mapFrames = []

        for i in range(self.mapSize[0]):
            for j in range(self.mapSize[1]):
                frame = ttk.Frame(master=gridFrame, relief=tk.RAISED, borderwidth=1)
                frame.grid(row=i, column=j, sticky='nsew')
                gridFrame.rowconfigure(i, weight=1, minsize=1)
                gridFrame.columnconfigure(j, weight=1, minsize=1)
                lblGrid = ttk.Label(master=frame, text=f"{i+1}, {j+1}")
                lblGrid.grid(row=0, column=0, sticky='nw')
                CreateToolTip(frame, text=f"{i+1}, {j+1}")
                mapFrames.append(frame)
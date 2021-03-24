import math
import tkinter as tk
import pathlib
import json
import os
from tkinter import ttk, font
from ttkthemes import ThemedStyle
from tooltip import *
from PIL import Image, ImageTk

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
        
        self.mapFrames = []

        for i in range(self.mapSize[0]):
            self.mapFrames.append([])
            for j in range(self.mapSize[1]):
                self.space = ttk.Frame(master=gridFrame, relief=tk.RAISED, borderwidth=1)
                self.space.grid(row=i, column=j, sticky='nsew')
                gridFrame.rowconfigure(i, weight=1, minsize=10)
                gridFrame.columnconfigure(j, weight=1, minsize=10)
                #lblGrid = ttk.Label(master=self.space, text=f"{i+1}, {j+1}")
                #lblGrid.grid(row=0, column=0, sticky='nw')
                CreateToolTip(self.space, text=f"{i+1}, {j+1}")
                #self.spaceUnit = ttk.Frame(master=self.space)
                #self.spaceUnit.grid(row=0, column=0, sticky='nw')
                self.mapFrames[i].append(self.space)
        
        self.tokenList = []
        self.initializeTokens()
        self.placeTokens()
    
    def initializeTokens(self):
        creatureCache = "./entry/bin/creatureCache.json"
        if os.path.exists(creatureCache) == True:
            with open(creatureCache, "r") as savefile:
                creatures = json.load(savefile)
        for being in creatures.keys():
            self.tokenList.append(creatures[being])
    
    def placeTokens(self):
        i = 0
        j = 0
        for being in self.tokenList:
            if being["coordinate"][0] != "" and being["coordinate"][1] != "":
                rowPos = int(being["coordinate"][1]) - 1
                colPos = int(being["coordinate"][0]) - 1
                allyImg = ImageTk.PhotoImage(Image.open("./entry/bin/allyToken.png").resize((16,16)))
                lblUnit = ttk.Label(master=self.mapFrames[colPos][rowPos], text="!img", image=allyImg)
                lblUnit.grid(row=i, column=j, sticky="w")
                i += 1
                if i >= 2:
                    j += 1
                    i = 0
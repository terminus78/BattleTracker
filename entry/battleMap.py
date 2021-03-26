import math
import tkinter as tk
import pathlib
import json
import os
from tkinter import ttk, font
from ttkthemes import ThemedStyle
from tooltip import *
from PIL import Image, ImageTk
from eventManager import EventManager

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
        self.mapWin.columnconfigure(0, minsize=50)
        self.mapWin.columnconfigure(1, weight=1, minsize=100)
        self.em = EventManager(self.mapWin)
        lblMap = ttk.Label(master=self.mapWin, text="BattleMap", font=('Papyrus', '16'))
        lblMap.grid(row=0, column=0)
        gridFrame = ttk.Frame(master=self.mapWin)
        gridFrame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        self.sideBoard = ttk.Frame(master=self.mapWin)
        self.sideBoard.grid(row=1, column=0, padx=5, pady=10, sticky="nsw")
        self.sideCount = 0
        allyPath = "allyToken.png"
        self.allyImg = ImageTk.PhotoImage(Image.open(allyPath).resize((20,20)))
        enemyPath = "enemyToken.png"
        self.enemyImg = ImageTk.PhotoImage(Image.open(enemyPath).resize((20,20)))
        bystanderPath = "bystanderToken.png"
        self.bystanderImg = ImageTk.PhotoImage(Image.open(bystanderPath).resize((20,20)))
        deadPath = "deadToken.png"
        self.deadImg = ImageTk.PhotoImage(Image.open(deadPath).resize((20,20)))
        
        self.mapFrames = []

        for i in range(self.mapSize[0]):
            self.mapFrames.append([])
            gridFrame.rowconfigure(i, weight=1, minsize=10)
            for j in range(self.mapSize[1]):
                self.space = ttk.Frame(master=gridFrame, relief=tk.RAISED, borderwidth=1)
                self.space.grid(row=i, column=j, sticky='nsew')
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
        #i = 0
        #j = 0
        for being in self.tokenList:
            tokenType = being["type"]
            if tokenType == "ally":
                    tokenImg = self.allyImg
            elif tokenType == "enemy":
                tokenImg = self.enemyImg
            elif tokenType == "bystander":
                tokenImg = self.bystanderImg
            elif tokenType == "dead":
                tokenImg = self.deadImg
            else:
                raise NameError("Token type not specified.")
            
            if being["coordinate"][0] != "" and being["coordinate"][1] != "":
                rowPos = int(being["coordinate"][1]) - 1
                colPos = int(being["coordinate"][0]) - 1
                self.mapFrames[colPos][rowPos].columnconfigure(0, weight=1, minsize=5)
                self.mapFrames[colPos][rowPos].rowconfigure(0, weight=1, minsize=5)
                lblUnit = tk.Label(master=self.mapFrames[colPos][rowPos], image=tokenImg, bg="gray37", borderwidth=0)
                lblUnit.image = tokenImg
                lblUnit.grid(row=0, column=0, padx=2, pady=2, sticky="nsew")
                lblUnit.bind("<Button-3>", self.em.rightClickMenu)
                CreateToolTip(lblUnit, text=being["name"])
                '''
                i += 1
                if i >= 2:
                    j += 1
                    i = 0
                '''
            else:
                self.unusedTokens(being, tokenImg)
    
    def unusedTokens(self, creature, tokenImg):
        nextRow = int(self.sideCount / 2)
        nextCol = self.sideCount % 2
        lblSideUnit = tk.Label(master=self.sideBoard, image=tokenImg, bg="gray37", borderwidth=0)
        lblSideUnit.grid(row=nextRow, column=nextCol, padx=5, pady=5, sticky="ne")
        lblSideUnit.image = tokenImg
        CreateToolTip(lblSideUnit, text=creature["name"])
        self.sideCount += 1
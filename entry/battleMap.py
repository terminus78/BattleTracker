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
from calc import Calculator
from statCollector import StatCollector

class BattleMap(object):
    def __init__(self, mapSize, master):
        # Window definition
        self.master = master
        self.mapSize = mapSize
        self.mapWin = tk.Toplevel(self.master)
        self.mapWin.title("Battle Map")
        style = ThemedStyle(self.mapWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.mapWin.configure(bg=style.lookup('TLabel', 'background'))
        self.topFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge')
        self.topFrame.pack(side='top', fill='x')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.rowconfigure(0, minsize=100)
        self.bottomFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge')
        self.bottomFrame.pack(side='top', fill='both', expand=True)
        self.bottomFrame.columnconfigure(0, minsize=50)
        self.bottomFrame.columnconfigure(1, weight=1, minsize=100)
        self.bottomFrame.columnconfigure(2, minsize=50)
        self.bottomFrame.rowconfigure(0, weight=1, minsize=100)
        self.em = EventManager(self.mapWin)
        self.calculator = Calculator(self.mapWin)

        # Board Setup
        lblMap = ttk.Label(master=self.topFrame, text="BattleMap", font=('Papyrus', '16'))
        lblMap.grid(row=0, column=0)
        btnSave = ttk.Button(master=self.topFrame, command=self.saveGame, text="Save")
        btnSave.grid(row=0, column=1, sticky='se')
        btnClear = ttk.Button(master=self.topFrame, command=self.clearMap, text="Clear Map")
        btnClear.grid(row=0, column=2, sticky='se')
        btnInput = ttk.Button(master=self.topFrame, command=self.inputCreatureWindow, text="Input Creature")
        btnInput.grid(row=0, column=3, sticky='se')
        btnReset = ttk.Button(master=self.topFrame, command=lambda: self.refreshMap(reset=True), text="Reset Map")
        btnReset.grid(row=0, column=4, sticky='se')
        gridFrame = ttk.Frame(master=self.bottomFrame)
        gridFrame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.sideBoard = ttk.Frame(master=self.bottomFrame)
        self.sideBoard.grid(row=0, column=0, padx=5, pady=10, sticky="nsw")
        self.sideCount = 0
        self.toolBar = ttk.Frame(master=self.bottomFrame)
        self.toolBar.grid(row=0, column=2, padx=5, pady=10, sticky="nse")
        moveIconPath = "icons8-circled-down-left-32.png"
        moveIcon = ImageTk.PhotoImage(Image.open(moveIconPath).resize((20,20)))
        trigIconPath = "3228996421547464107-128.png"
        trigIcon = ImageTk.PhotoImage(Image.open(trigIconPath).resize((20,20)))

        # Image paths
        allyPath = "allyToken.png"
        self.allyImg = ImageTk.PhotoImage(Image.open(allyPath).resize((15,15)))
        enemyPath = "enemyToken.png"
        self.enemyImg = ImageTk.PhotoImage(Image.open(enemyPath).resize((15,15)))
        bystanderPath = "bystanderToken.png"
        self.bystanderImg = ImageTk.PhotoImage(Image.open(bystanderPath).resize((15,15)))
        deadPath = "deadToken.png"
        self.deadImg = ImageTk.PhotoImage(Image.open(deadPath).resize((15,15)))
        
        self.mapFrames = []
        self.tokenList = []

        # Space frames
        for i in range(self.mapSize[0]):
            self.mapFrames.append([])
            gridFrame.rowconfigure(i, weight=1, minsize=10)
            for j in range(self.mapSize[1]):
                self.space = ttk.Frame(master=gridFrame, relief=tk.RAISED, borderwidth=1)
                self.space.grid(row=i, column=j, sticky='nsew')
                gridFrame.columnconfigure(j, weight=1, minsize=10)
                CreateToolTip(self.space, text=f"{i+1}, {j+1}")
                self.mapFrames[i].append(self.space)
        
        self.initializeTokens()

        # Toolbar Buttons
        self.btnMove = ttk.Button(master=self.toolBar, command=self.moveToken, image=moveIcon)
        self.btnMove.grid(row=0, column=0, sticky="n")
        self.btnMove.image = moveIcon
        CreateToolTip(self.btnMove, text="Move Token", leftDisp=True)

        self.btnTrig = ttk.Button(master=self.toolBar, command=self.openTrig, image=trigIcon)
        self.btnTrig.grid(row=1, column=0, sticky='n')
        self.btnTrig.image = trigIcon
        CreateToolTip(self.btnTrig, text="Distance", leftDisp=True)

        self.placeTokens()
    
    def initializeTokens(self):
        self.tokenList = []
        creatureCache = "./entry/bin/creatureCache.json"
        if os.path.exists(creatureCache) == True:
            with open(creatureCache, "r") as savefile:
                creatures = json.load(savefile)
        for being in creatures.values():
            self.tokenList.append(being)
    
    def placeTokens(self):
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
                rowPos = int(being["coordinate"][1])
                colPos = int(being["coordinate"][0])
                lblUnit = tk.Label(master=self.mapFrames[colPos][rowPos], image=tokenImg, bg="gray37", borderwidth=0)
                lblUnit.image = tokenImg
                spaceCount = len(self.mapFrames[colPos][rowPos].grid_slaves())
                rowCount = int(spaceCount / 3)
                colCount = spaceCount % 3
                lblUnit.grid(row=rowCount, column=colCount, sticky='n')
                lblUnit.bind("<Button-3>", self.em.rightClickMenu)
                CreateToolTip(lblUnit, text="{0}, {1}".format(being["name"], being["coordinate"][2]))
            else:
                self.unusedTokens(being, tokenImg)
    
    def unusedTokens(self, creature, tokenImg):
        nextRow = int(self.sideCount / 2)
        nextCol = self.sideCount % 2
        lblSideUnit = tk.Label(master=self.sideBoard, image=tokenImg, bg="gray37", borderwidth=0)
        lblSideUnit.grid(row=nextRow, column=nextCol, padx=5, pady=5, sticky="ne")
        lblSideUnit.bind("<Button-3>", self.em.rightClickMenu)
        lblSideUnit.image = tokenImg
        CreateToolTip(lblSideUnit, text=creature["name"])
        self.sideCount += 1

    def refreshMap(self, tokens=None, reset=False):
        if tokens is not None:
            self.tokenList = tokens
        for row in self.mapFrames:
            for col in row:
                removeTokens = col.grid_slaves()
                if len(removeTokens) > 0:
                    for token in removeTokens:
                        token.destroy()
        removeSideList = self.sideBoard.grid_slaves()
        if len(removeSideList) > 0:
            for sideToken in removeSideList:
                sideToken.destroy()
        self.sideCount = 0
        
        if tokens is not None:
            self.em.moveWin.destroy()

        if reset:
            self.initializeTokens()

        self.placeTokens()

    def saveGame(self):
        newTokenDict = {}
        for being in self.tokenList:
            name = being["name"]
            newTokenDict[name] = being
        creatureCache = "./entry/bin/creatureCache.json"
        if os.path.exists(creatureCache) == False:
            with open(creatureCache, "w") as savefile:
                json.dump(newTokenDict, savefile, indent=4)
        else:
            with open(creatureCache, "w") as savefile:
                json.dump(newTokenDict, savefile, indent=4)

    def clearMap(self):
        for being in self.tokenList:
            being["coordinate"] = ['', '', '']
        self.refreshMap()

    def getTokenList(self):
        return self.tokenList

    def waitDestroyMoveWin(self):
        self.em.moveWin.protocol("WM_DELETE_WINDOW", lambda stuff=(self.em.tokenList): self.refreshMap(tokens=stuff))

    def inputCreatureWindow(self):
        self.inWin = StatCollector(self.master)

    def moveToken(self):
        self.em.moveToken([self.tokenList, self.mapSize])
        self.waitDestroyMoveWin()

    def openTrig(self):
        self.calculator.trigWin(self.tokenList)
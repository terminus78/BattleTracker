import math
import random
import pathlib
import json
import os

import PIL.Image
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from tooltip import *
from eventManager import EventManager
from calc import Calculator
from statCollector import StatCollector
from quotes import Quote
from target import Target
from conditionInfo import InfoClass


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
        self.quoteFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge')
        self.quoteFrame.pack(side='top', fill='x')
        self.quoteFrame.columnconfigure(0, minsize=20)
        self.bottomFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge')
        self.bottomFrame.pack(side='top', fill='both', expand=True)
        self.bottomFrame.columnconfigure(0, minsize=50)
        self.bottomFrame.columnconfigure(1, weight=1, minsize=100)
        self.bottomFrame.columnconfigure(2, minsize=50)
        self.bottomFrame.rowconfigure(0, weight=1, minsize=100)
        self.em = EventManager(self.mapWin)
        self.calculator = Calculator(self.mapWin)
        self.quoter = Quote()
        self.countQuotes = 0
        self.target = Target(self.mapWin)
        self.info = InfoClass(self.mapWin)

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
        btnRestart = ttk.Button(master=self.topFrame, command=self.fullReset, text="Reset Battle")
        btnRestart.grid(row=0, column=5, sticky='se')
        btnCloseAll = ttk.Button(master=self.topFrame, command=self.master.destroy, text="Close All")
        btnCloseAll.grid(row=0, column=6, sticky='se')
        self.lblQuote = ttk.Label(master=self.quoteFrame, text="", font=('Papyrus', '12'))
        self.lblQuote.grid(row=0, column=0, sticky='w', pady=5)
        self.findQuote()
        gridFrame = ttk.Frame(master=self.bottomFrame)
        gridFrame.grid(row=0, column=1, padx=10, pady=10, sticky='nsew')
        self.sideBoard = ttk.Frame(master=self.bottomFrame)
        self.sideBoard.grid(row=0, column=0, padx=5, pady=10, sticky="nsw")
        self.sideCount = 0
        self.toolBar = ttk.Frame(master=self.bottomFrame)
        self.toolBar.grid(row=0, column=2, padx=5, pady=10, sticky="nse")
        moveIconPath = "entry/bin/icons8-circled-down-left-32.png"
        moveIcon = ImageTk.PhotoImage(image=PIL.Image.open(moveIconPath).resize((20,20)))
        trigIconPath = "entry/bin/3228996421547464107-128.png"
        trigIcon = ImageTk.PhotoImage(image=PIL.Image.open(trigIconPath).resize((20,20)))
        targetIconPath = "entry/bin/11749495271547546487-128.png"
        targetIcon = ImageTk.PhotoImage(image=PIL.Image.open(targetIconPath).resize((20,20)))

        # Image paths
        allyPath = "entry/bin/allyToken.png"
        self.allyImg = ImageTk.PhotoImage(image=PIL.Image.open(allyPath).resize((15,15)))
        enemyPath = "entry/bin/enemyToken.png"
        self.enemyImg = ImageTk.PhotoImage(image=PIL.Image.open(enemyPath).resize((15,15)))
        bystanderPath = "entry/bin/bystanderToken.png"
        self.bystanderImg = ImageTk.PhotoImage(image=PIL.Image.open(bystanderPath).resize((15,15)))
        deadPath = "entry/bin/deadToken.png"
        self.deadImg = ImageTk.PhotoImage(image=PIL.Image.open(deadPath).resize((15,15)))
        
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

        self.btnTarget = ttk.Button(master=self.toolBar, command=self.targetItem,image=targetIcon)
        self.btnTarget.grid(row=2, column=0, sticky='n')
        self.btnTarget.image = targetIcon
        CreateToolTip(self.btnTarget, text="Target", leftDisp=True)

        self.btnCondInfo = ttk.Button(master=self.toolBar, command=self.showCondInfo, text="Conditions")
        self.btnCondInfo.grid(row=3, column=0, sticky='n')
        #self.btnCondInfo.image = targetIcon
        CreateToolTip(self.btnCondInfo, text="Condition Info", leftDisp=True)

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
                spaceTaken = 1
                if being["size"] == "large" or being["size"] == "huge" or being["size"] == "gargantuan":
                    if being["size"] == "large":
                        spaceNeed = 4
                    elif being["size"] == "huge":
                        spaceNeed = 9
                    else:
                        spaceNeed = 16
                    rowOffset = 0
                    colOffset = 0
                    goToNextRow = math.sqrt(spaceNeed)
                    for i in range(1, spaceNeed):
                        if i < spaceNeed:
                            colOffset += 1
                            if colOffset == goToNextRow:
                                colOffset = 0
                                rowOffset += 1
                            rowPos = int(being["coordinate"][1]) + rowOffset
                            colPos = int(being["coordinate"][0]) + colOffset
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

    def refreshMap(self, tokens=None, reset=False, origWin=None):
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

        if origWin == 'em':
            self.em.moveWin.destroy()
        
        if origWin == 'target':
            self.target.targetWin.destroy()

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
        self.em.moveWin.protocol("WM_DELETE_WINDOW", lambda stuff=(self.em.tokenList): self.refreshMap(tokens=stuff, origWin='em'))

    def inputCreatureWindow(self):
        self.inWin = StatCollector(self.master)

    def moveToken(self):
        self.em.moveToken([self.tokenList, self.mapSize])
        self.waitDestroyMoveWin()

    def openTrig(self):
        self.calculator.trigWin(self.tokenList)

    def targetItem(self):
        self.target.targetWindow(self.tokenList)
        self.target.targetWin.protocol("WM_DELETE_WINDOW", lambda stuff=(self.target.tokenList): self.refreshMap(tokens=stuff, origWin='target'))

    def fullReset(self):
        emptyDict = {}
        creatureCache = "./entry/bin/creatureCache.json"
        makeSure = messagebox.askokcancel("Warning", "Confirm request to delete ALL tokens and FULL RESET MAP.")
        if makeSure:
            if os.path.exists(creatureCache) == True:
                with open(creatureCache, "w") as savefile:
                    json.dump(emptyDict, savefile, indent=4)
                self.refreshMap(reset=True)

    def findQuote(self):
        lastIndex = len(self.quoter.quoteList) - 1
        randIndex = random.randint(0, lastIndex)
        randomQuote = self.quoter.getQuote(randIndex)
        self.lblQuote.config(text=randomQuote)

    def showCondInfo(self):
        self.info.explainConditions()
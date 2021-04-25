import math
import random
import pathlib
import json
import os
from zipfile import ZipFile

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
from dice import DiceRoller


class BattleMap(object):
    def __init__(self, master):
        self.master = master
        self.regFont = ('Papyrus', '14')
        self.smallFont = ("Papyrus", "9")
        self.bigFont = ("Papyrus", "16")
        gameTitle = self.master.gameName
        if len(gameTitle) > 32:
            gameTitle = gameTitle[0:31] + "..."
        # Window definition
        with ZipFile(self.master.filename, 'r') as savefile:
            battleBytes = savefile.read('battleInfo.json')
            battleObj = json.loads(battleBytes.decode('utf-8'))
            self.mapSize = battleObj['mapSize']
            self.round = battleObj['round']
            self.turn = battleObj['turn']
        self.mapWin = tk.Toplevel(self.master)
        self.mapWin.title(f"Battle Map | {gameTitle}")
        style = ThemedStyle(self.mapWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.mapWin.configure(bg=style.lookup('TLabel', 'background'))
        self.topFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge',)# bg='dark green')
        self.topFrame.pack(side='top', fill='x')
        self.topFrame.columnconfigure(0, weight=1)
        self.topFrame.rowconfigure(0, minsize=100)
        self.quoteFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge')
        self.quoteFrame.pack(side='top', fill='x')
        self.quoteFrame.columnconfigure(0, minsize=20)
        self.bottomFrame = ttk.Frame(master=self.mapWin, borderwidth=2, relief='ridge')#, bg='dark green')
        self.bottomFrame.pack(side='top', fill='both', expand=True)
        self.bottomFrame.columnconfigure(0, minsize=100)
        self.bottomFrame.columnconfigure(1, weight=1, minsize=200)
        self.bottomFrame.columnconfigure(2, minsize=150)
        self.bottomFrame.columnconfigure(3, minsize=50)
        self.bottomFrame.rowconfigure(0, weight=1, minsize=200)
        self.em = EventManager(self.mapWin)
        self.calculator = Calculator(self.mapWin)
        self.quoter = Quote()
        self.countQuotes = 0
        self.target = Target(self.mapWin)
        self.info = InfoClass(self.mapWin)
        self.diceRoll = DiceRoller(self.mapWin)

        # Board Setup
        lblMap = ttk.Label(master=self.topFrame, text=gameTitle, font=('Papyrus', '16'))
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
        self.lblQuote = ttk.Label(master=self.quoteFrame, text="", font=self.regFont)
        self.lblQuote.grid(row=0, column=0, sticky='w', pady=5)
        self.findQuote()
        '''
        topGridLabelFrame = ttk.Frame(master=self.bottomFrame)
        topGridLabelFrame.grid(row=0, column=2)
        leftGridLabelFrame = ttk.Frame(master=self.bottomFrame)
        leftGridLabelFrame.grid(row=1, column=1)
        '''
        self.sideBoard = ttk.Frame(master=self.bottomFrame)
        self.sideCount = 0
        gridFrame = ttk.Frame(master=self.bottomFrame, borderwidth=2, relief='ridge')
        self.roundBar = ttk.Frame(master=self.bottomFrame)
        self.toolBar = ttk.Frame(master=self.bottomFrame)
        self.sideBoard.grid(row=0, column=0, padx=5, pady=10, sticky="nw")
        gridFrame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.roundBar.grid(row=0, column=2, padx=5, pady=10, sticky="nw")
        self.toolBar.grid(row=0, column=3, padx=5, pady=10, sticky="nw")

        # Image paths
        moveIconPath = "entry\\bin\\icons8-circled-down-left-32.png"
        moveIcon = ImageTk.PhotoImage(image=PIL.Image.open(moveIconPath).resize((20,20)))
        trigIconPath = "entry\\bin\\3228996421547464107-128.png"
        trigIcon = ImageTk.PhotoImage(image=PIL.Image.open(trigIconPath).resize((20,20)))
        targetIconPath = "entry\\bin\\11749495271547546487-128.png"
        targetIcon = ImageTk.PhotoImage(image=PIL.Image.open(targetIconPath).resize((20,20)))
        condInfoIconPath = "entry\\bin\\2780604101548336129-128.png"
        condInfoIcon = ImageTk.PhotoImage(image=PIL.Image.open(condInfoIconPath).resize((20,20)))
        turnIconPath = "entry\\bin\\swords.png"
        self.turnIcon = ImageTk.PhotoImage(image=PIL.Image.open(turnIconPath).resize((20,20)))
        d20IconPath = "entry\\bin\\role-playing.png"
        d20Icon = ImageTk.PhotoImage(image=PIL.Image.open(d20IconPath).resize((20,20)))

        allyPath = "entry\\bin\\allyToken.png"
        self.allyImg = ImageTk.PhotoImage(image=PIL.Image.open(allyPath).resize((15,15)))
        enemyPath = "entry\\bin\\enemyToken.png"
        self.enemyImg = ImageTk.PhotoImage(image=PIL.Image.open(enemyPath).resize((15,15)))
        bystanderPath = "entry\\bin\\bystanderToken.png"
        self.bystanderImg = ImageTk.PhotoImage(image=PIL.Image.open(bystanderPath).resize((15,15)))
        deadPath = "entry\\bin\\deadToken.png"
        self.deadImg = ImageTk.PhotoImage(image=PIL.Image.open(deadPath).resize((15,15)))
        
        self.mapFrames = []
        self.mapWin.tokenList = []

        # Grid labels
        for colSpot in range(self.mapSize[1]):
            lblGridTop = ttk.Label(master=gridFrame, text=colSpot+1, font=self.smallFont)
            lblGridTop.grid(row=0, column=colSpot+1)
            gridFrame.columnconfigure(colSpot+1, weight=1, minsize=20)

        for rowSpot in range(self.mapSize[0]):
            lblGridSide = ttk.Label(master=gridFrame, text=rowSpot+1, font=self.smallFont)
            lblGridSide.grid(row=rowSpot+1, column=0)
            gridFrame.rowconfigure(rowSpot+1, weight=1, minsize=20)

        gridFrame.columnconfigure(0, weight=1, minsize=20)
        gridFrame.rowconfigure(0, weight=1, minsize=20)

        # Space frames
        for i in range(self.mapSize[0]):
            self.mapFrames.append([])
            for j in range(self.mapSize[1]):
                self.space = ttk.Frame(master=gridFrame, relief=tk.RAISED, borderwidth=1)
                self.space.grid(row=i+1, column=j+1, sticky='nsew')
                CreateToolTip(self.space, text=f"{i+1}, {j+1}")
                self.mapFrames[i].append(self.space)
        
        self.initializeTokens()

        # Roundbar
        lblRoundTitle = ttk.Label(master=self.roundBar, text="Round: ", font=self.bigFont)
        lblRoundTitle.grid(row=0, column=0, sticky='e')
        self.lblRound = ttk.Label(master=self.roundBar, text=self.round, font=self.bigFont, borderwidth=1, relief=tk.RAISED, width=3, anchor=tk.CENTER)
        self.lblRound.grid(row=0, column=1, sticky='w')
        self.initiativeFrame = ttk.Frame(master=self.roundBar)
        self.initiativeFrame.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.initiativeFrame.columnconfigure([0,1], weight=1)
        btnNextTurn = ttk.Button(master=self.roundBar, text="Turn Complete", command=self.nextTurn)
        btnNextTurn.grid(row=2, column=0, columnspan=2)
        btnNextRound = ttk.Button(master=self.roundBar, text="Round Complete", command=self.nextRound)
        btnNextRound.grid(row=3, column=0, columnspan=2)

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

        self.btnCondInfo = ttk.Button(master=self.toolBar, command=self.showCondInfo, image=condInfoIcon)
        self.btnCondInfo.grid(row=3, column=0, sticky='n')
        self.btnCondInfo.image = condInfoIcon
        CreateToolTip(self.btnCondInfo, text="Condition Info", leftDisp=True)

        self.btnDiceRoller = ttk.Button(master=self.toolBar, command=self.openDiceRoller, image=d20Icon)
        self.btnDiceRoller.grid(row=4, column=0, sticky='n')
        self.btnDiceRoller.image = d20Icon
        CreateToolTip(self.btnDiceRoller, text="Dice Roller", leftDisp=True)

        self.placeTokens()

    def initializeTokens(self):
        self.mapWin.tokenList = []
        with ZipFile(self.master.filename, "r") as savefile:
            creatBytes = savefile.read('creatures.json')
            creatStr = creatBytes.decode('utf-8')
            creatures = json.loads(creatStr)
        for being in creatures.values():
            self.mapWin.tokenList.append(being)
    
    def placeTokens(self):
        self.initiativeHolder = {}
        for being in self.mapWin.tokenList:
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
                lblUnit = tk.Label(master=self.mapFrames[colPos][rowPos], image=tokenImg, bg="gray28", borderwidth=0)
                lblUnit.image = tokenImg
                spaceCount = len(self.mapFrames[colPos][rowPos].grid_slaves())
                rowCount = int(spaceCount / 3)
                colCount = spaceCount % 3
                lblUnit.grid(row=rowCount, column=colCount)
                lblUnit.bind("<Button-3>", self.em.rightClickMenu)
                CreateToolTip(lblUnit, text="{0}, {1}".format(being["name"], being["coordinate"][2]))
                spaceTaken = 1
                if being['initiative'] != -math.inf:
                    self.initiativeHolder[being['name']] = being['initiative']
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
                            lblUnit = tk.Label(master=self.mapFrames[colPos][rowPos], image=tokenImg, bg="gray28", borderwidth=0)
                            lblUnit.image = tokenImg
                            spaceCount = len(self.mapFrames[colPos][rowPos].grid_slaves())
                            rowCount = int(spaceCount / 3)
                            colCount = spaceCount % 3
                            lblUnit.grid(row=rowCount, column=colCount)
                            lblUnit.bind("<Button-3>", self.em.rightClickMenu)
                            CreateToolTip(lblUnit, text="{0}, {1}".format(being["name"], being["coordinate"][2]))

            else:
                self.unusedTokens(being, tokenImg)
            self.refreshInitiatives()
    
    def unusedTokens(self, creature, tokenImg):
        nextRow = int(self.sideCount / 2)
        nextCol = self.sideCount % 2
        lblSideUnit = tk.Label(master=self.sideBoard, image=tokenImg, bg="gray28", borderwidth=0)
        lblSideUnit.grid(row=nextRow, column=nextCol, padx=5, pady=5, sticky="ne")
        lblSideUnit.bind("<Button-3>", self.em.rightClickMenu)
        lblSideUnit.image = tokenImg
        CreateToolTip(lblSideUnit, text=creature["name"])
        self.sideCount += 1
    
    def postInitiatives(self):
        initDictInOrder = {k:v for k, v in sorted(self.initiativeHolder.items(), key= lambda item: item[1], reverse=True)}
        orderCount = 0
        lblTurnImg = tk.Label(master=self.initiativeFrame, image=self.turnIcon, bg="gray28", borderwidth=0)
        lblTurnImg.grid(row=self.turn, column=0, sticky='w')
        lblTurnImg.image = self.turnIcon

        for nextUp in initDictInOrder.items():
            if nextUp[1] != math.inf:
                lblYourTurn = ttk.Label(master=self.initiativeFrame, text=f"{nextUp[0]}: ", font=self.smallFont)
                lblYourTurn.grid(row=orderCount, column=1, sticky='w')
                lblYourInit = ttk.Label(master=self.initiativeFrame, text=nextUp[1], font=self.smallFont)
                lblYourInit.grid(row=orderCount, column=2, sticky='e')
                orderCount += 1

    def refreshInitiatives(self):
        initFrameSlaves = self.initiativeFrame.grid_slaves()
        if len(initFrameSlaves):
            for item in initFrameSlaves:
                item.destroy()
        self.postInitiatives()

    def nextTurn(self):
        onBoardInits = self.initiativeHolder
        infExists = True
        fuckedUp = 30
        while infExists and fuckedUp > 0:
            for key, value in onBoardInits.items():
                if value == math.inf:
                    del onBoardInits[key]
                    break
            if math.inf not in onBoardInits:
                infExists = False
            fuckedUp -= 1
        self.turn += 1
        if self.turn > len(self.initiativeHolder) - 1:
            self.nextRound()
        else:
            self.refreshInitiatives()

    def nextRound(self):
        self.round += 1
        self.lblRound.config(text=self.round)
        self.turn = 0
        self.refreshInitiatives()

    def refreshMap(self, reset=False):
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

        if reset:
            self.initializeTokens()

        self.refreshInitiatives()
        self.placeTokens()

    def saveGame(self):
        newTokenDict = {}
        for being in self.mapWin.tokenList:
            name = being["name"]
            newTokenDict[name] = being
        battleDict = {
            "mapSize": self.mapSize,
            "round": self.round,
            "turn": self.turn
        }
        battleJSON = json.dumps(battleDict, indent=4)
        with ZipFile(self.master.filename, "w") as savefile:
            creatJSON = json.dumps(newTokenDict, indent=4)
            savefile.writestr('battleInfo.json', battleJSON)
            savefile.writestr('creatures.json', creatJSON)

    def clearMap(self):
        for being in self.mapWin.tokenList:
            being["coordinate"] = ['', '', '']
        self.refreshMap()

    def inputCreatureWindow(self):
        self.inWin = StatCollector(self.mapWin, self.mapSize, self.round, self.turn)
        self.inWin.btnSubmit.configure(command=lambda arg=['inWin', 'submit']: self.changeTokenList(arg))

    def changeTokenList(self, arg):
        origin = arg[0]
        selBtn = arg[1]
        if origin == 'moveWin':
            if selBtn == 'set':
                setComplete = self.em.setNewCoord()
                if setComplete:
                    self.em.moveWin.destroy()
                    self.refreshMap()
            elif selBtn == 'remove':
                remComplete = self.em.removeToken()
                if remComplete:
                    self.em.moveWin.destroy()
                    self.refreshMap()
        elif origin == 'targetWin':
            if selBtn == 'submit':
                submitComplete = self.target.onSubmit()
                if submitComplete:
                    self.target.targetWin.destroy()
                    self.refreshMap()
            elif selBtn == 'delete':
                deleteComplete = self.target.deleteToken()
                if deleteComplete:
                    self.target.targetWin.destroy()
                    self.refreshMap()
        elif origin == 'inWin':
            if selBtn == 'submit':
                submitComplete = self.inWin.submit()
                if submitComplete:
                    self.inWin.rangeWin.destroy()
                    self.refreshMap()

    def moveToken(self):
        self.em.moveToken(self.mapSize)
        self.em.btnSet.configure(command=lambda arg=['moveWin', 'set']: self.changeTokenList(arg))
        self.em.btnRemove.configure(command=lambda arg=['moveWin', 'remove']: self.changeTokenList(arg))
        #self.waitDestroyMoveWin()

    def openTrig(self):
        self.calculator.trigWin()

    def targetItem(self):
        self.target.targetWindow()
        self.target.btnSubmit.configure(command=lambda arg=['targetWin', 'submit']: self.changeTokenList(arg))
        self.target.btnDeleteTarget.configure(command=lambda arg=['targetWin', 'delete']: self.changeTokenList(arg))
        #self.target.targetWin.protocol("WM_DELETE_WINDOW", lambda stuff=(self.target.tokenList): self.refreshMap(tokens=stuff, origWin='target'))

    def openDiceRoller(self):
        self.diceRoll.dicePane()

    def fullReset(self):
        emptyDict = {}
        makeSure = messagebox.askokcancel("Warning", "Confirm request to delete ALL tokens and FULL RESET MAP.\nIf confirmed, this action cannot be undone.")
        if makeSure:
            battleDict = {
                "mapSize": self.mapSize,
                "round": 0,
                "turn": 0
            }
            battleJSON = json.dumps(battleDict, indent=4)
            with ZipFile(self.master.filename, "w") as savefile:
                creatJSON = json.dumps(emptyDict)
                savefile.writestr('battleInfo.json', battleJSON)
                savefile.writestr('creatures.json', creatJSON)
            self.refreshMap(reset=True)

    def findQuote(self):
        lastIndex = len(self.quoter.quoteList) - 1
        randIndex = random.randint(0, lastIndex)
        randomQuote = self.quoter.getQuote(randIndex)
        self.lblQuote.config(text=randomQuote)

    def showCondInfo(self):
        self.info.explainConditions()
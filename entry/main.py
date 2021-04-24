import os
import json
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle

from statCollector import StatCollector
from battleMap import BattleMap
from tooltip import *

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
windowWidth = window.winfo_reqwidth()
windowHeight = window.winfo_reqheight()
positionHorizontal = int(window.winfo_screenwidth()/2 - windowWidth/2)
positionVertical = int(window.winfo_screenheight()/2 - windowHeight/2)
window.geometry("+{}+{}".format(positionHorizontal, positionVertical))


class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.countdown = 3
        self.master.cwd = os.getcwd()
        #print(self.master.cwd)
        self.cacheLoc = self.master.cwd + "\\entry\\bin\\cache.json"
        #print(self.cacheLoc)
        try:
            with open(self.cacheLoc, 'r') as cachefile:
                self.cacheInfo = json.load(cachefile)
        except IOError:
            with open(self.cacheLoc, 'w') as cachefile:
                defaultLoc = {
                    'lastDir': 'C:\\'
                }
                json.dump(defaultLoc, cachefile, indent=4)
            with open(self.cacheLoc, 'r') as cachefile:
                self.cacheInfo = json.load(cachefile)

        self.topFrame = ttk.Frame(master=self.master)
        self.topFrame.grid(row=0, column=0)
        self.bottomFrame = ttk.Frame(master=self.master)
        self.bottomFrame.grid(row=1, column=0)
        self.warningFrame = ttk.Frame(master=self.master)
        self.warningFrame.grid(row=2, column=0)
        self.lblGreeting = ttk.Label(master=self.topFrame, text="Welcome to the BattleTracker", font=papyrusFont)
        self.lblGreeting.grid(row=0, column=0)
        self.btnNewFile = ttk.Button(master=self.bottomFrame, text="New Game", command=self.newFile)
        self.btnNewFile.grid(row=0, column=0, sticky='e')
        self.btnOpenExisting = ttk.Button(master=self.bottomFrame, text="Open Existing", command=self.openFile)
        self.btnOpenExisting.grid(row=0, column=1, sticky='w')
        self.lblWarning = ttk.Label(master=self.warningFrame, text="Warning: Closing this window will close the entire program")
        self.lblWarning.grid(row=0, column=0, sticky='s')
    
    # Unused
    def inputWindow(self):
        self.inWin = StatCollector(self.master)

    # Unused
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

    # Unused
    def showMap(self):
        self.mapWin = BattleMap([32, 46], self.master)

    def newFile(self):
        self.gameStartWin = tk.Toplevel(master=self.master)
        self.gameStartWin.title("New Game")
        style = ThemedStyle(self.gameStartWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.gameStartWin.configure(bg=style.lookup('TLabel', 'background'))
        containerFrame = ttk.Frame(master=self.gameStartWin)
        containerFrame.pack(padx=15, pady=15)
        upperFrame = ttk.Frame(master=containerFrame)
        upperFrame.grid(row=0, column=0)
        fileFrame = ttk.Frame(master=containerFrame)
        fileFrame.grid(row=1, column=0)
        finishFrame = ttk.Frame(master=containerFrame)
        finishFrame.grid(row=2, column=0, sticky='e')
        lblTop = ttk.Label(master=upperFrame, text="New Game", font=papyrusFont)
        lblTop.grid(row=0, column=0)
        lblSelectFileLoc = ttk.Label(master=fileFrame, text="Select file location", font=papyrusFont)
        lblSelectFileLoc.grid(row=0, column=0, sticky='w')
        self.entFileLoc = ttk.Entry(master=fileFrame, width=50)
        self.entFileLoc.insert(0, self.cacheInfo['lastDir'])
        self.entFileLoc.grid(row=1, column=0, sticky='w')
        btnLookUpFile = ttk.Button(master=fileFrame, text="...", width=2, command=self.lookUpCommand)
        btnLookUpFile.grid(row=1, column=1, sticky='w')
        lblNewName = ttk.Label(master=fileFrame, text="Enter file name", font=papyrusFont)
        lblNewName.grid(row=2, column=0, sticky='w')
        self.entNewFilename = ttk.Entry(master=fileFrame, width=27)
        self.entNewFilename.grid(row=3, column=0, sticky='w')
        lblMapSizeSelect = ttk.Label(master=fileFrame, text="Select map size", font=papyrusFont)
        lblMapSizeSelect.grid(row=2, column=1, sticky='w')
        self.mapChoice = ["Tiny (8 X 12)", "Small (16 X 24)", "Medium (24 X 36)", "Large (32 X 46)"]
        self.cbxMapSizes = ttk.Combobox(master=fileFrame, width=27, values=self.mapChoice)
        self.cbxMapSizes.grid(row=3, column=1, sticky='w')
        btnStartGame = ttk.Button(master=finishFrame, text="Start Game", command=self.startNewBattle)
        btnCancel = ttk.Button(master=finishFrame, text="Cancel", command=self.gameStartWin.destroy)
        btnCancel.pack(side=tk.RIGHT)
        btnStartGame.pack(side=tk.RIGHT)

    def startNewBattle(self):
        fileLocation = self.entFileLoc.get()
        if os.path.isdir(fileLocation) == False:
            messagebox.showerror("New Game", "File location does not exist or your access level requires elevation.")
            return
        self.master.gameName = self.entNewFilename.get()
        if fileLocation == "" or self.master.gameName == "":
            messagebox.showwarning("New Game", "File location and name fields cannot be empty.")
            return
        self.master.filename = fileLocation + "\\" + self.master.gameName + ".brpg"

        selectedMap = self.cbxMapSizes.get()
        if selectedMap == "Tiny (8 X 12)":
            mapSize = [8, 12]
        elif selectedMap == "Small (16 X 24)":
            mapSize = [16, 24]
        elif selectedMap == "Medium (24 X 36)":
            mapSize = [24, 36]
        elif selectedMap == "Large (32 X 46)":
            mapSize = [32, 46]
        else:
            messagebox.showwarning("New Game", "Map size must be selected.")
            return

        battleDict = {
            "mapSize": mapSize,
            "round": 0,
            "turn": 0
        }
        battleJSON = json.dumps(battleDict, indent=4)
        with ZipFile(self.master.filename, 'w') as brpgFile:
            brpgFile.writestr("battleInfo.json", battleJSON)
            brpgFile.writestr("creatures.json", "{}")
        saveDir = os.path.dirname(self.master.filename)
        if saveDir != self.cacheInfo['lastDir']:
            self.cacheInfo['lastDir'] = saveDir
            with open(self.cacheLoc, 'w') as cachefile:
                json.dump(self.cacheInfo, cachefile, indent=4)
        self.mapWin = BattleMap(self.master)
        self.gameStartWin.destroy()
        self.master.iconify()

    def lookUpCommand(self):
        self.master.filedir = filedialog.askdirectory()
        self.entFileLoc.delete(0, 'end')
        self.entFileLoc.insert(0, self.master.filedir)

    def openFile(self):
        self.master.filename = filedialog.askopenfilename(initialdir=self.cacheInfo['lastDir'], title='Select File', filetypes=(('BRPG files', '*.brpg'),))
        if type(self.master.filename) is str and self.master.filename != "":
            if os.path.exists(self.master.filename) == False:
                messagebox.showerror("Start Game", "File location does not exist or your access level requires elevation.")
            saveDir = os.path.dirname(self.master.filename)
            if saveDir != self.cacheInfo['lastDir']:
                self.cacheInfo['lastDir'] = saveDir
                with open(self.cacheLoc, 'w') as cachefile:
                    json.dump(self.cacheInfo, cachefile, indent=4)
            gameFile = os.path.split(self.master.filename)[-1]
            self.master.gameName = gameFile.split('.')[0]
            self.mapWin = BattleMap(self.master)
            self.master.iconify()

battleWin = mainWindow(window)

window.mainloop()
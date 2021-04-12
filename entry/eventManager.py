import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

class EventManager():
    def __init__(self, root):
        self.root = root
        self.font = ('Papyrus', '14')
        
    def rightClickMenu(self, event):
        self.event = event
        self.tokenMenu = tk.Menu(self.root, tearoff=0)
        #self.trigMenu = tk.Menu(self.tokenMenu, tearoff=0)
        self.aoeMenu = tk.Menu(self.tokenMenu, tearoff=0)
        self.tokenMenu.add_command(label="Stats")
        self.tokenMenu.add_command(label="Damage")
        self.tokenMenu.add_command(label="Heal")
        self.tokenMenu.add_separator()
        #self.tokenMenu.add_cascade(label="Trig Functions", menu=self.trigMenu)
        #self.trigMenu.add_command(label="Distance", command=findDistance)
        #self.trigMenu.add_command(label="Find All in Range")
        #self.trigMenu.add_command(label="Spread Width")
        self.tokenMenu.add_cascade(label="AOE", menu=self.aoeMenu)
        self.aoeMenu.add_command(label="Circle")
        self.aoeMenu.add_command(label="Square")
        self.aoeMenu.add_command(label="Cone")
        self.aoeMenu.add_command(label="Line")
        self.aoeMenu.add_command(label="Ring Wall")
        self.aoeMenu.add_command(label="Line Wall")
        try:
            self.tokenMenu.tk_popup(self.event.x_root, self.event.y_root)
        finally:
            self.tokenMenu.grab_release()

    def moveToken(self, arg):
        self.tokenList = arg[0]
        self.mapSize = arg[1]
        self.moveWin = tk.Toplevel(master=self.root)
        self.moveWin.title("Move Token")
        style = ThemedStyle(self.moveWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.moveWin.configure(bg=style.lookup('TLabel', 'background'))
        #self.moveWin.protocol("WM_DELETE_WINDOW", super().refreshMap)
        self.moveWin.rowconfigure(0, minsize=100)
        self.moveWin.columnconfigure([0,1], minsize=100)
        self.selectionFrame = ttk.Frame(master=self.moveWin)
        self.selectionFrame.grid(row=0, column=0, sticky='nw')
        self.moveToFrame = ttk.Frame(master=self.moveWin)
        self.moveToFrame.grid(row=0, column=1, sticky='nw')
        lblSelected = ttk.Label(master=self.selectionFrame, text="Selected Token", font=self.font)
        lblSelected.grid(row=0, column=0, sticky='w')
        names = []
        coordinates = []
        for being in self.tokenList:
            names.append(being["name"])
            coordinates.append(being["coordinate"])
        selOption = tk.StringVar()
        selOption.set(names[0])
        dropSelection = ttk.OptionMenu(self.selectionFrame, selOption, *names)
        dropSelection.grid(row=0, column=1, sticky='w')
        self.btnCurrCoord = ttk.Button(master=self.selectionFrame, text="Show Current Coordinate", command=lambda arg=[selOption, names, coordinates]: self.showCoord(arg))
        self.btnCurrCoord.grid(row=1, column=0, sticky='w')
        self.lblActCoord = ttk.Label(master=self.selectionFrame, text=" ", font=self.font)
        self.lblActCoord.grid(row=1, column=1, sticky='w')
        lblSetNewCoord = ttk.Label(master=self.moveToFrame, text="Set New Coordinate", font=self.font)
        lblSetNewCoord.grid(row=0, column=0, sticky='w')
        self.entRowCoord = ttk.Entry(master=self.moveToFrame, width=5)
        self.entColCoord = ttk.Entry(master=self.moveToFrame, width=5)
        self.entZCoord = ttk.Entry(master=self.moveToFrame, width=5)
        self.entRowCoord.grid(row=0, column=1, sticky='w')
        self.entColCoord.grid(row=0, column=2, sticky='w')
        self.entZCoord.grid(row=0, column=3, sticky='w')
        self.btnSet = ttk.Button(master=self.moveToFrame, text="Set Position", command=lambda arg=(selOption): self.setNewCoord(arg))
        self.btnSet.grid(row=1, column=0)
        self.lblSetFinished = ttk.Label(master=self.moveToFrame, text=" ", font=self.font)
        self.lblSetFinished.grid(row=1, column=1)

    def showCoord(self, arg):
        selOption = arg[0]
        names = arg[1]
        coordinates = arg[2]
        index = names.index(selOption.get())
        row = coordinates[index][0]
        col = coordinates[index][1]
        z = coordinates[index][2]
        self.lblActCoord.config(text="{0}: {1}: {2}".format(row, col, z))

    def setNewCoord(self, arg):
        newCoord = [int(self.entRowCoord.get()), int(self.entColCoord.get()), int(self.entZCoord.get())]
        if newCoord[0] > self.mapSize[0] or newCoord[0] < 0:
            messagebox.showerror("Error", "Row Coordinate Out of Range of Map!")
            return
        if newCoord[1] > self.mapSize[1] or newCoord[1] < 0:
            messagebox.showerror("Error", "Column Coordinate Out of Range of Map!")
            return
        selOption = arg
        name = selOption.get()
        for being in self.tokenList:
            if being["name"] == name:
                being["coordinate"] = [str(newCoord[0]), str(newCoord[1]), str(newCoord[2])]
        self.lblSetFinished.config(text="Position Set!")
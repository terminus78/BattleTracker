import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

class Calculator():
    def __init__(self, root):
        self.root = root
        self.font = ("Papyrus", "14")

    def trigWin(self, arg):
        self.tokenList = arg
        self.trig = tk.Toplevel(self.root)
        self.trig.title("Trig Calculator")
        style = ThemedStyle(self.trig)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.trig.configure(bg=style.lookup('TLabel', 'background'))
        self.trig.rowconfigure(0, minsize=100)
        self.trig.columnconfigure([0,1], minsize=100)
        self.fromFrame = ttk.Frame(master=self.trig)
        self.fromFrame.grid(row=0, column=0, padx=5)
        self.toFrame = ttk.Frame(master=self.trig)
        self.toFrame.grid(row=0, column=1, padx=5)
        names = []
        coordinates = []
        for being in self.tokenList:
            names.append(being["name"])
            coordinates.append(being["coordinate"])
        selOrigin = tk.StringVar()
        selOrigin.set(names[0])
        selDestination = tk.StringVar()
        selDestination.set(names[0])
        lblFrom = ttk.Label(master=self.fromFrame, text="Origin", font=self.font)
        lblFrom.grid(row=0, column=0, sticky='w')
        dropOrigin = ttk.OptionMenu(self.fromFrame, selOrigin, *names)
        dropOrigin.grid(row=0, column=1, sticky='w')
        btnSelectOrig = ttk.Button(master=self.fromFrame, text="Select Origin", command=lambda arg=[selOrigin, names, coordinates]: self.showOrigin(arg))
        btnSelectOrig.grid(row=1, column=0, sticky='w')
        self.lblOrigCoord = ttk.Label(master=self.fromFrame, text=" ", font=self.font)
        self.lblOrigCoord.grid(row=1, column=1, sticky='w')
        lblTo = ttk.Label(master=self.toFrame, text="Destination", font=self.font)
        lblTo.grid(row=0, column=0, sticky='w')
        dropDestination = ttk.OptionMenu(self.toFrame, selDestination, *names)
        dropDestination.grid(row=0, column=1, sticky='w')
        btnSelectDest = ttk.Button(master=self.toFrame, text="Select Destination", command=lambda arg=[selDestination, names, coordinates]: self.showDestination(arg))
        btnSelectDest.grid(row=1, column=0, sticky='w')
        self.lblDestCoord = ttk.Label(master=self.toFrame, text=" ", font=self.font)
        self.lblDestCoord.grid(row=1, column=1, sticky='w')

    def showOrigin(self, arg):
        selOrigin = arg[0]
        names = arg[1]
        coordinates = arg[2]
        index = names.index(selOrigin.get())
        if coordinates[index][0] != "" and coordinates[index][1] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1
        else:
            row = coordinates[index][0]
            col = coordinates[index][1]
        z = coordinates[index][2]
        self.lblOrigCoord.config(text="{0}: {1}: {2}".format(row, col, z))

    def showDestination(self, arg):
        selDestination = arg[0]
        names = arg[1]
        coordinates = arg[2]
        index = names.index(selDestination.get())
        if coordinates[index][0] != "" and coordinates[index][1] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1
        else:
            row = coordinates[index][0]
            col = coordinates[index][1]
        z = coordinates[index][2]
        self.lblDestCoord.config(text="{0}: {1}: {2}".format(row, col, z))
    
    '''
    def findDist(self, arg):
        deltaX = entity.coordinate[0] - self.coordinate[0]
        deltaY = entity.coordinate[1] - self.coordinate[1]
        deltaZ = entity.coordinate[2] - self.coordinate[2]
        
        if deltaX == 0:
            grndHypo = deltaY
        elif deltaY == 0:
            grndHypo = deltaX
        else:
            grndHypo = math.sqrt(deltaX**2 + deltaY**2)

        if grndHypo == 0:
            distance = deltaZ
        else:
            distance = math.sqrt(grndHypo**2 + deltaZ**2)
        
        return distance
    '''
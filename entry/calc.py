import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

class Calculator():
    def __init__(self, root):
        self.root = root
        self.font = ("Papyrus", "14")
        self.fontSmall = ("Papyrus", "12")

    def trigWin(self, arg):
        self.tokenList = arg
        print("#############")
        print(self.tokenList)
        print(" ")
        self.trig = tk.Toplevel(self.root)
        self.trig.title("Trig Calculator")
        style = ThemedStyle(self.trig)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.trig.configure(bg=style.lookup('TLabel', 'background'))
        self.trig.rowconfigure([0,1], minsize=100)
        self.trig.columnconfigure([0,1], minsize=100)
        self.fromFrame = ttk.Frame(master=self.trig)
        self.fromFrame.grid(row=0, column=0, padx=5)
        self.toFrame = ttk.Frame(master=self.trig)
        self.toFrame.grid(row=0, column=1, padx=5)
        self.resultFrame = ttk.Frame(master=self.trig)
        self.resultFrame.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.infoFrame = ttk.Frame(master=self.trig, borderwidth=2, relief='ridge')
        self.infoFrame.grid(row=2, column=0, columnspan=2)
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
        self.btnCalculate = ttk.Button(master=self.resultFrame, text="Calculate Distance", command=lambda arg=[selOrigin, selDestination, names, coordinates]: self.findDist(arg))
        self.btnCalculate.grid(row=0, column=0)
        self.lblActCalcResult = ttk.Label(master=self.resultFrame, text="Ready", font=self.font)
        self.lblActCalcResult.grid(row=1, column=0)
        self.lblCalcInfo1 = ttk.Label(master=self.infoFrame, text="Calculation is based on true trigonometry.", font=self.fontSmall)
        self.lblCalcInfo1.grid(row=0, column=0)
        self.lblCalcInfo2 = ttk.Label(master=self.infoFrame, text="Values may not correspond to grid distance counting.", font=self.fontSmall)
        self.lblCalcInfo2.grid(row=1, column=0)
        self.lblCalcInfo3 = ttk.Label(master=self.infoFrame, text="This is best used for attack ranges. Do not use for movement.", font=self.fontSmall)
        self.lblCalcInfo3.grid(row=2, column=0)

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
    
    def findDist(self, arg):
        origin = arg[0]
        destination = arg[1]
        names = arg[2]
        coordinates = arg[3]
        indexOrigin = names.index(origin.get())
        indexDest = names.index(destination.get())
        coordOrigin = coordinates[indexOrigin]
        coordDest = coordinates[indexDest]
        if coordOrigin[0] == "" or coordOrigin[1] == "" or coordOrigin[2] == "":
            messagebox.showerror("Error", "Selected Origin Not on Map!")
            return
        if coordDest[0] == "" or coordDest[1] == "" or coordDest[2] == "":
            messagebox.showerror("Error", "Selected Destination Not on Map!")
            return
        
        # Actual distance calculation and display
        deltaX = abs((int(coordDest[1]) * 5) - (int(coordOrigin[1]) * 5))
        deltaY = abs((int(coordDest[0]) * 5) - (int(coordOrigin[0]) * 5))
        deltaZ = abs((int(coordDest[2]) * 5) - (int(coordOrigin[2]) * 5))
        
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
        distanceFT = math.floor(distance)
        distanceINCH = round((distance - distanceFT) * 12)

        self.lblActCalcResult.config(text="True Distance: {0}ft, {1}in".format(distanceFT, distanceINCH))
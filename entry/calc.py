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
        lblFrom = ttk.Label(master=self.fromFrame, text="Origin", font=self.font)
        lblFrom.grid(row=0, column=0, sticky='w')
        self.dropOrigin = ttk.Combobox(self.fromFrame, width=27, values=names)
        self.dropOrigin.grid(row=0, column=1, sticky='w')
        btnSelectOrig = ttk.Button(master=self.fromFrame, text="Show Origin", command=lambda arg=[names, coordinates]: self.showOrigin(arg))
        btnSelectOrig.grid(row=1, column=0, sticky='w')
        self.lblOrigCoord = ttk.Label(master=self.fromFrame, text=" ", font=self.font)
        self.lblOrigCoord.grid(row=1, column=1, sticky='w')
        lblTo = ttk.Label(master=self.toFrame, text="Destination", font=self.font)
        lblTo.grid(row=0, column=0, sticky='w')
        self.dropDestination = ttk.Combobox(self.toFrame, width=27, values=names)
        self.dropDestination.grid(row=0, column=1, sticky='w')
        btnSelectDest = ttk.Button(master=self.toFrame, text="Show Destination", command=lambda arg=[names, coordinates]: self.showDestination(arg))
        btnSelectDest.grid(row=1, column=0, sticky='w')
        self.lblDestCoord = ttk.Label(master=self.toFrame, text=" ", font=self.font)
        self.lblDestCoord.grid(row=1, column=1, sticky='w')
        self.btnCalculate = ttk.Button(master=self.resultFrame, text="Calculate Distance", command=lambda arg=[names, coordinates]: self.distBtn(arg))
        self.btnCalculate.grid(row=0, column=0)
        lblAct = ttk.Label(master=self.resultFrame, text="True distance: ", font=self.font)
        lblAct.grid(row=1, column=0)
        self.lblActCalcResult = ttk.Label(master=self.resultFrame, text="Ready", font=self.font)
        self.lblActCalcResult.grid(row=1, column=1)
        lblRel = ttk.Label(master=self.resultFrame, text="Relative distance: ", font=self.font)
        lblRel.grid(row=2, column=0)
        self.lblRelCalcResult = ttk.Label(master=self.resultFrame, text="Ready", font=self.font, borderwidth=1, relief='groove')
        self.lblRelCalcResult.grid(row=2, column=1)
        self.lblCalcInfo1 = ttk.Label(master=self.infoFrame, text="True distance is based on real-world trigonometry.", font=self.fontSmall)
        self.lblCalcInfo1.grid(row=0, column=0)
        self.lblCalcInfo2 = ttk.Label(master=self.infoFrame, text="True distance may not correspond to grid distance counting.", font=self.fontSmall)
        self.lblCalcInfo2.grid(row=1, column=0)
        self.lblCalcInfo3 = ttk.Label(master=self.infoFrame, text="Relative distance mimics the game-specific way of adding up blocks.", font=self.fontSmall)
        self.lblCalcInfo3.grid(row=2, column=0)
        self.lblCalcInfo3 = ttk.Label(master=self.infoFrame, text="For most situations, relative distance follows the rules of D&D more closely.", font=self.fontSmall)
        self.lblCalcInfo3.grid(row=3, column=0)

    def showOrigin(self, arg):
        selOrigin = self.dropOrigin.get()
        names = arg[0]
        coordinates = arg[1]
        index = names.index(selOrigin)
        if coordinates[index][0] != "" and coordinates[index][1] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1
        else:
            row = coordinates[index][0]
            col = coordinates[index][1]
        z = coordinates[index][2]
        self.lblOrigCoord.config(text="{0}: {1}: {2}".format(row, col, z))

    def showDestination(self, arg):
        selDestination = self.dropDestination.get()
        names = arg[0]
        coordinates = arg[1]
        index = names.index(selDestination)
        if coordinates[index][0] != "" and coordinates[index][1] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1
        else:
            row = coordinates[index][0]
            col = coordinates[index][1]
        z = coordinates[index][2]
        self.lblDestCoord.config(text="{0}: {1}: {2}".format(row, col, z))
    
    def distBtn(self, arg):
        origin = self.dropOrigin.get()
        destination = self.dropDestination.get()
        if origin == "" or destination == "":
            messagebox.showwarning("Input Error", "Please select an origin and a destination.")
            return
        names = arg[0]
        coordinates = arg[1]
        indexOrigin = names.index(origin)
        indexDest = names.index(destination)
        coordOrigin = coordinates[indexOrigin]
        coordDest = coordinates[indexDest]
        if coordOrigin[0] == "" or coordOrigin[1] == "" or coordOrigin[2] == "":
            messagebox.showwarning("Map Coordinate Failure", "Selected Origin Not on Map!")
            return
        if coordDest[0] == "" or coordDest[1] == "" or coordDest[2] == "":
            messagebox.showwarning("Map Coordinate Failure", "Selected Destination Not on Map!")
            return
        
        self.actualDistance(coordOrigin, coordDest)
        self.relativeDistance(coordOrigin, coordDest)

    def calcDist(self, start, end):
        deltaX = abs((int(end[1]) * 5) - (int(start[1]) * 5))
        deltaY = abs((int(end[0]) * 5) - (int(start[0]) * 5))
        deltaZ = abs((int(end[2]) * 5) - (int(start[2]) * 5))
        
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
    
    def relativeDistance(self, start, end):
        startX, startY, startZ = int(start[1]), int(start[0]), int(start[2])
        endX, endY, endZ = int(end[1]), int(end[0]), int(end[2])
        endAsInts = [int(end[1]), int(end[0]), int(end[2])]
        currCoord = [startX, startY, startZ]
        diffX = endX - startX
        diffY = endY - startY
        diffZ = endZ - startZ
        if diffX == 0 and diffY == 0 and diffZ == 0:
            distFound = True
            distance = 0
            self.lblRelCalcResult.config(text=f"{distance}ft")
            return
        else:
            distFound = False

        # Counterclockwise rotation
        rotationOffset = [-1, -1, 1, 1]
        distanceTraveled = 0
        countRounds = 0
        while distFound == False:
            currX, currY, currZ = currCoord
            diffX = endX - currX
            diffY = endY - currY
            diffZ = endZ - currZ
            if diffX > 0 or diffX < 0:
                signX = diffX / abs(diffX)
            else:
                signX = 0
            if diffY > 0 or diffY < 0:
                signY = diffY / abs(diffY)
            else:
                signY = 0
            if diffZ > 0 or diffZ < 0:
                signZ = diffZ / abs(diffZ)
            else:
                signZ = 0

            octant = [signX, signY, signZ]
            shortestDistance = math.inf
            if octant[0] != 0 and octant[1] != 0 and octant[2] != 0:
                if octant[0] > 0 and octant[1] > 0:
                    index = 2
                elif octant[0] < 0 and octant[1] > 0:
                    index = 3
                elif octant[0] < 0 and octant[1] < 0:
                    index = 0
                else:
                    index = 1
                if octant[2] > 0:
                    checkUp = True
                else:
                    checkUp = False
                for i in range(7):
                    if index == 0 or index == 2:
                        currX += rotationOffset[index]
                    elif index == 1 or index == 3:
                        currY += rotationOffset[index]
                    else:
                        index = 0
                        currX += rotationOffset[index]
                    if i == 3:
                        if checkUp:
                            currZ += 1
                        else:
                            currZ -= 1
                    checkDist = self.calcDist([str(currY), str(currX), str(currZ)], end)
                    if checkDist < shortestDistance:
                        shortestDistance = checkDist
                        currCoord = [currX, currY, currZ]
                    index += 1

            elif octant[0] == 0:
                if octant[1] == 0:
                    currCoord = [currX, currY, currZ + signZ]
                elif octant[2] == 0:
                    currCoord = [currX, currY + signY, currZ]
                else:
                    if octant[1] > 0 and octant[2] > 0:
                        index = 2
                    elif octant[1] < 0 and octant[2] > 0:
                        index = 3
                    elif octant[1] < 0 and octant[2] < 0:
                        index = 0
                    else:
                        index = 1
                    for i in range(3):
                        if index == 0 or index == 2:
                            currZ += rotationOffset[index]
                        elif index == 1 or index == 3:
                            currY += rotationOffset[index]
                        else:
                            index = 0
                            currZ += rotationOffset[index]
                        checkDist = self.calcDist([str(currY), str(currX), str(currZ)], end)
                        if checkDist < shortestDistance:
                            shortestDistance = checkDist
                            currCoord = [currX, currY, currZ]
                        index += 1

            elif octant[1] == 0:
                if octant[2] == 0:
                    currCoord = [currX + signX, currY, currZ]
                else:
                    if octant[0] > 0 and octant[2] > 0:
                        index = 2
                    elif octant[0] < 0 and octant[2] > 0:
                        index = 3
                    elif octant[0] < 0 and octant[2] < 0:
                        index = 0
                    else:
                        index = 1
                    for i in range(3):
                        if index == 0 or index == 2:
                            currX += rotationOffset[index]
                        elif index == 1 or index == 3:
                            currZ += rotationOffset[index]
                        else:
                            index = 0
                            currX += rotationOffset[index]
                        checkDist = self.calcDist([str(currY), str(currX), str(currZ)], end)
                        if checkDist < shortestDistance:
                            shortestDistance = checkDist
                            currCoord = [currX, currY, currZ]
                        index += 1

            else:
                if octant[0] > 0 and octant[1] > 0:
                    index = 2
                elif octant[0] < 0 and octant[1] > 0:
                    index = 3
                elif octant[0] < 0 and octant[1] < 0:
                    index = 0
                else:
                    index = 1
                for i in range(3):
                    if index == 0 or index == 2:
                        currX += rotationOffset[index]
                    elif index == 1 or index == 3:
                        currY += rotationOffset[index]
                    else:
                        index = 0
                        currX += rotationOffset[index]
                    checkDist = self.calcDist([str(currY), str(currX), str(currZ)], end)
                    if checkDist < shortestDistance:
                        shortestDistance = checkDist
                        currCoord = [currX, currY, currZ]
                    index += 1
            distanceTraveled += 5
            if currCoord == endAsInts:
                distFound = True
            if countRounds == 50:
                distFound = True
                messagebox.showerror("Calculation Failure", "Restart program.\nError 0x001")
            countRounds += 1
        self.lblRelCalcResult.config(text=f"{distanceTraveled}ft")

    def actualDistance(self, start, end):
        distance = self.calcDist(start, end)
        distanceFT = math.floor(distance)
        distanceINCH = round((distance - distanceFT) * 12)
        self.lblActCalcResult.config(text="{0}ft, {1}in".format(distanceFT, distanceINCH))
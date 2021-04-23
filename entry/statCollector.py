import pathlib
import json
import os
import math
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from dice import DiceRoller

papyrusFont = ('Papyrus', '14')


class StatCollector(object):
    def __init__(self, master, mapSize, roundNum, turn):
        self.master = master
        self.mapSize = mapSize
        self.round = roundNum
        self.turn = turn
        self.rangeWin = tk.Toplevel(self.master)
        self.rangeWin.title("Range Calculator")
        style = ThemedStyle(self.rangeWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.rangeWin.configure(bg=style.lookup('TLabel', 'background'))
        self.dice = DiceRoller()

        upperFrame = ttk.Frame(master=self.rangeWin)
        lowerFrame = ttk.Frame(master=self.rangeWin)
        underFrame = ttk.Frame(master=self.rangeWin)

        frame1_1 = ttk.Frame(master=upperFrame)
        frame1_2 = ttk.Frame(master=upperFrame)
        frame2_1 = ttk.Frame(master=upperFrame)
        frame2_2 = ttk.Frame(master=upperFrame)
        frame3_1 = ttk.Frame(master=upperFrame)
        frame3_2 = ttk.Frame(master=upperFrame)

        frameList = [frame1_1, frame1_2, frame2_1, frame2_2, frame3_1, frame3_2]

        upperFrame.grid(row=0, column=0, sticky="w")
        lowerFrame.grid(row=1, column=0, sticky="w")
        underFrame.grid(row=2, column=0, pady=8)

        frRow = 0
        frCol = 0
        for fr in frameList:
            fr.grid(row=frRow, column = frCol, padx=5, pady=5, sticky="w")
            frCol += 1
            if frCol == 2:
                frCol = 0
                frRow += 1
        
        self.radSize = tk.StringVar()
        self.radFoeFriend = tk.StringVar()
        self.stats = {}

        lblName = ttk.Label(master=frame1_1, text="Name", font=papyrusFont)
        self.entName = ttk.Entry(master=frame1_1, width=10)
        lblName.grid(row=0, column=0, sticky="w")
        self.entName.grid(row=0, column=1, sticky="e")

        lblHP = ttk.Label(master=frame1_2, text="Max HP", font=papyrusFont)
        self.entHP = ttk.Entry(master=frame1_2, width=8)
        lblHP.grid(row=0, column=0, sticky="w")
        self.entHP.grid(row=0, column=1, sticky="e")
        lblTempHP = ttk.Label(master=frame1_2, text="Temp HP", font=papyrusFont)
        self.entTempHP = ttk.Entry(master=frame1_2, width=8)
        lblTempHP.grid(row=1, column=0, sticky="w")
        self.entTempHP.grid(row=1, column=1, sticky="e")

        '''
        lblCoord = ttk.Label(master=frame2_1, text="Coordinate", font=papyrusFont)
        self.entXCoord = ttk.Entry(master=frame2_1, width=2)
        lblX = ttk.Label(master=frame2_1, text="X", font=papyrusFont)
        self.entYCoord = ttk.Entry(master=frame2_1, width=2)
        lblY = ttk.Label(master=frame2_1, text="Y", font=papyrusFont)
        self.entZCoord = ttk.Entry(master=frame2_1, width=2)
        lblZ = ttk.Label(master=frame2_1, text="Z", font=papyrusFont)
        lblCoord.grid(row=0, column=0, sticky="w")
        self.entXCoord.grid(row=0, column=1, sticky="e")
        lblX.grid(row=0, column=2, sticky="e")
        self.entYCoord.grid(row=0, column=3, sticky="e")
        lblY.grid(row=0, column=4, sticky="e")
        self.entZCoord.grid(row=0, column=5, sticky="e")
        lblZ.grid(row=0, column=6, sticky="e")
        '''

        frameFFUpper = ttk.Frame(master=frame2_1)
        frameFFLower = ttk.Frame(master=frame2_1)
        lblFF = ttk.Label(master=frameFFUpper, text="Strategic Status", font=papyrusFont)
        rbnAlly = ttk.Radiobutton(master=frameFFLower, text="Ally", variable= self.radFoeFriend, value="ally")
        rbnEnemy = ttk.Radiobutton(master=frameFFLower, text="Enemy", variable= self.radFoeFriend, value="enemy")
        rbnBystander = ttk.Radiobutton(master=frameFFLower, text="Bystander", variable= self.radFoeFriend, value="bystander")
        rbnDead = ttk.Radiobutton(master=frameFFLower, text="Dead", variable= self.radFoeFriend, value="dead")
        frameFFUpper.grid(row=0, column=0, sticky="w")
        frameFFLower.grid(row=1, column=0, sticky="w")
        lblFF.grid(row=0, column=0, sticky="w")
        rbnAlly.grid(row=0, column=0, sticky="w")
        rbnEnemy.grid(row=0, column=1, sticky="w")
        rbnBystander.grid(row=0, column=2, sticky="w")
        rbnDead.grid(row=0, column=3, sticky="w")

        lblHeight = ttk.Label(master=frame2_2, text="Height (Feet)", font=papyrusFont)
        self.entHeight = ttk.Entry(master=frame2_2, width=8)
        lblHeight.grid(row=0, column=0, sticky="w")
        self.entHeight.grid(row=0, column=1, sticky="e")

        frameSizeLeft = ttk.Frame(master=frame3_1)
        frameSizeRight = ttk.Frame(master=frame3_1)
        lblSize = ttk.Label(master=frame3_1, text="Size Class", font=papyrusFont)
        rbnTiny = ttk.Radiobutton(master=frameSizeLeft, text="Tiny", variable= self.radSize, value="tiny")
        rbnSmall = ttk.Radiobutton(master=frameSizeRight, text="Small", variable= self.radSize, value="small")
        rbnMedium = ttk.Radiobutton(master=frameSizeLeft, text="Medium", variable= self.radSize, value="medium")
        rbnLarge = ttk.Radiobutton(master=frameSizeRight, text="Large", variable= self.radSize, value="large")
        rbnHuge = ttk.Radiobutton(master=frameSizeLeft, text="Huge", variable= self.radSize, value="huge")
        rbnGargantuan = ttk.Radiobutton(master=frameSizeRight, text="Gargantuan", variable= self.radSize, value="gargantuan")
        lblSize.grid(row=0, column=0)
        frameSizeLeft.grid(row=1, column=0)
        frameSizeRight.grid(row=1, column=1)
        rbnTiny.grid(row=0, column=0, sticky="w")
        rbnSmall.grid(row=0, column=0, sticky="w")
        rbnMedium.grid(row=1, column=0, sticky="w")
        rbnLarge.grid(row=1, column=0, sticky="w")
        rbnHuge.grid(row=2, column=0, sticky="w")
        rbnGargantuan.grid(row=2, column=0, sticky="w")

        lblInit = ttk.Label(master=frame3_2, text="Initiative", font=papyrusFont)
        lblInit.grid(row=0, column=0, sticky='e')
        self.entInit = ttk.Entry(master=frame3_2, width=8)
        self.entInit.grid(row=0, column=1, sticky='w')
        btnRollInit = ttk.Button(master=frame3_2, text="Roll", command=self.rolldice)
        btnRollInit.grid(row=0, column=2, sticky='w')

        lblNotes = ttk.Label(master=lowerFrame, text="Notes", font=papyrusFont)
        self.txtNotes = tk.Text(master=lowerFrame, height=5, width=52)
        self.txtNotes.configure(font=("Papyrus", "12"))
        lblNotes.grid(row=0, column=0)
        self.txtNotes.grid(row=1, column=0, sticky="w")

        self.btnSubmit = ttk.Button(master=underFrame, text="Submit")#command=self.submit,
        self.btnSubmit.grid(row=0, column=0)
        btnCancel = ttk.Button(master=underFrame, text="Cancel", command=self.rangeWin.destroy)
        btnCancel.grid(row=0, column=1)

    def submit(self):
        specialChar = ['[','@','_','!','#','$','%','^','&','*','(',')','<','>','?','/','\\','|','}','{','~',':',']']
        nameGet = self.entName.get()
        maxHPGet = self.entHP.get()
        tempHPGet = self.entTempHP.get()
        foeFriendGet = self.radFoeFriend.get()
        heightGet = self.entHeight.get()
        sizeGet = self.radSize.get()
        initGet = self.entInit.get()
        notesGet = self.txtNotes.get(1.0, tk.END)
        if nameGet == "":
            messagebox.showinfo("Character Input", "Must input a name.")
            return False
        for i in range(len(specialChar)):
            if specialChar[i] in nameGet:
                messagebox.showwarning("Character Input", "Name cannot contain special characters.")
                return False
        if foeFriendGet == "":
            messagebox.showwarning("Character Input", "Must select a strategic status.")
            return False
        if sizeGet == "":
            messagebox.showwarning("Character Input", "Must select a size.")
            return False
        if initGet == "":
            initFlt = math.inf
        else:
            try:
                initFlt = float(initGet)
            except ValueError:
                messagebox.showwarning("Character Input", "Initiative must be a number.")
                return False
            except TypeError:
                messagebox.showwarning("Character Input", "Initiative must be a number.")
                return False
        '''
        if notesGet == "Easter Egg 1234 ABC":
            messagebox.showinfo("Character Input", "In the deepest dungeon of the darkest realm,\nYou will find the creature of brightest light and darkest story.\nIf only the heroes could brave true horror and near insurmountable doom,\nThey might find all the hope they would ever need.")
            return False
        '''
        try:
            if maxHPGet != "":
                maxHPInt = int(maxHPGet)
                if maxHPInt <= 0:
                    messagebox.showinfo("Character Input", "Max HP must be a positive whole number.")
                    return False
            else:
                messagebox.showinfo("Character Input", "Max HP cannot be undefined.")
                return False
            if tempHPGet != "":
                tempHPInt = int(maxHPGet)
                if tempHPInt < 0:
                    messagebox.showinfo("Character Input", "Temp HP must be a positive whole number or zero.")
                    return False
            else:
                tempHPInt = 0
        except ValueError:
            messagebox.showwarning("Character Input", "Max HP must be a positive whole number. If entered, Temp HP must be a positive whole number or zero.")
            return False
        except TypeError:
            messagebox.showwarning("Character Input", "Max HP must be a positive whole number. If entered, Temp HP must be a positive whole number or zero.")
            return False
        try:
            if heightGet == "":
                messagebox.showwarning("Character Input", "Height cannot be undefined.")
                return False
            heightFlt = float(heightGet)
            if heightFlt < 0:
                messagebox.showinfo("Character Input", "Height must be a positive number or zero.")
                return False
        except ValueError:
            messagebox.showwarning("Character Input", "Height must be a positive number or zero.")
            return False
        except TypeError:
            messagebox.showwarning("Character Input", "Height must be a positive number or zero.")
            return False

        self.stats = {
            "name": nameGet,
            "maxHP": maxHPInt,
            "tempHP": tempHPInt,
            "currentHP": maxHPInt,
            "type": foeFriendGet,
            "height": heightFlt,
            "size": sizeGet,
            "coordinate": ["", "", ""],
            "condition": ["normal"],
            "initiative": initFlt,
            "notes": notesGet
        }
        for being in self.master.tokenList:
            if being['name'] == nameGet:
                messagebox.showwarning("Character Input", "The name that was entered matches an existing creature.\nCreature must have a unique name.")
                return False
        self.master.tokenList.append(self.stats)
        return True
        #self.writeFile()
        #self.rangeWin.destroy()

    # Unused
    def writeFile(self):
        battleDict = {
            "mapSize": self.mapSize,
            "round": self.round,
            "turn": self.turn
        }
        battleJSON = json.dumps(battleDict, indent=4)
        with ZipFile(self.master.filename, "r") as savefile:
            readBytes = savefile.read('creatures.json')
            readObj = json.loads(readBytes.decode('utf-8'))
            readObj.update(self.stats)
        with ZipFile(self.master.filename, "w") as savefile:
            readJSON = json.dumps(readObj, indent=4)
            savefile.writestr('battleInfo.json', battleJSON)
            savefile.writestr('creatures.json', readJSON)

    def rolldice(self):
        dieFace = self.dice.roll()[0]
        self.entInit.delete(0, tk.END)
        self.entInit.insert(0, str(dieFace))
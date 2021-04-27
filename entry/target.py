import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle


class Target():
    def __init__(self, root):
        self.root = root

    def targetWindow(self):
        self.regFont = ("Papyrus", "14")
        self.smallFont = ("Papyrus", "11")
        self.bigFont = ("Papyrus", "16")
        self.targetWin = tk.Toplevel(self.root)
        self.targetWin.title("Target Creature")
        style = ThemedStyle(self.targetWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.targetWin.configure(bg=style.lookup('TLabel', 'background'))
        self.topFrame = ttk.Frame(master=self.targetWin)
        self.topFrame.grid(row=0, column=0, columnspan=2)
        self.selectFrame = ttk.Frame(master=self.targetWin)
        self.selectFrame.grid(row=1, column=0, columnspan=2)
        self.statFrame = ttk.Frame(master=self.targetWin, borderwidth=2, relief='ridge')
        self.statFrame.grid(row=2, column=0, sticky='nw', padx=5)
        self.statFrame.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
        self.targetWin.rowconfigure(2, weight=1)
        self.targetWin.columnconfigure([0,1], weight=1)
        self.actionFrame = ttk.Frame(master=self.targetWin, borderwidth=2, relief='ridge')
        self.actionFrame.grid(row=2, column=1, sticky='nw', padx=5)
        self.submitFrame = ttk.Frame(master=self.targetWin)
        self.submitFrame.grid(row=3, column=0, columnspan=2)
        self.names = []
        for being in self.root.tokenList:
            self.names.append(being["name"])
        lblTopInfo = ttk.Label(master=self.topFrame, text="Select target creature and desired action.", font=self.regFont)
        lblTopInfo.grid(row=0, column=0)
        self.dropTargets = ttk.Combobox(master=self.selectFrame, width=27, values=self.names)
        self.dropTargets.grid(row=0, column=0, sticky='w')
        btnSelect = ttk.Button(master=self.selectFrame, command=self.selectTarget, text="Select")
        btnSelect.grid(row=0, column=1, sticky='w')

        lblStaticName = ttk.Label(self.statFrame, text="Name: ", font=self.regFont)
        lblStaticName.grid(row=0, column=0, sticky='nw')
        lblStaticMaxHP = ttk.Label(self.statFrame, text="Max HP: ", font=self.regFont)
        lblStaticMaxHP.grid(row=1, column=0, sticky='nw')
        lblStaticTempHP = ttk.Label(self.statFrame, text="Temp HP: ", font=self.regFont)
        lblStaticTempHP.grid(row=2, column=0, sticky='nw')
        lblStaticHP = ttk.Label(self.statFrame, text="Current HP: ", font=self.regFont)
        lblStaticHP.grid(row=3, column=0, sticky='nw')
        lblStaticType = ttk.Label(self.statFrame, text="Type: ", font=self.regFont)
        lblStaticType.grid(row=4, column=0, sticky='nw')
        lblStaticHeight = ttk.Label(self.statFrame, text="Height: ", font=self.regFont)
        lblStaticHeight.grid(row=5, column=0, sticky='nw')
        lblStaticSize = ttk.Label(self.statFrame, text="Size: ", font=self.regFont)
        lblStaticSize.grid(row=6, column=0, sticky='nw')
        lblStaticCoord = ttk.Label(self.statFrame, text="Coordinate: ", font=self.regFont)
        lblStaticCoord.grid(row=7, column=0, sticky='nw')
        lblStaticInit = ttk.Label(self.statFrame, text="Initiative: ", font=self.regFont)
        lblStaticInit.grid(row=8, column=0, sticky='nw')
        lblStaticCondition = ttk.Label(self.statFrame, text="Condition: ", font=self.regFont)
        lblStaticCondition.grid(row=9, column=0, sticky='nw')
        lblStaticNotes = ttk.Label(self.statFrame, text="Notes: ", font=self.regFont)
        lblStaticNotes.grid(row=10, column=0, sticky='nw')

        self.lblActName = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActName.grid(row=0, column=1, sticky='nw')
        self.lblActMaxHP = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActMaxHP.grid(row=1, column=1, sticky='nw')
        self.lblActTempHP = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActTempHP.grid(row=2, column=1, sticky='nw')
        self.lblActHP = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActHP.grid(row=3, column=1, sticky='nw')
        self.lblActType = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActType.grid(row=4, column=1, sticky='nw')
        self.lblActHeight = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActHeight.grid(row=5, column=1, sticky='nw')
        self.lblActSize = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActSize.grid(row=6, column=1, sticky='nw')
        self.lblActCoord = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActCoord.grid(row=7, column=1, sticky='nw')
        self.lblActInit = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActInit.grid(row=8, column=1, sticky='nw')
        self.lblActCondition = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActCondition.grid(row=9, column=1, sticky='nw')
        self.lblActNotes = ttk.Label(self.statFrame, text=" ", font=self.regFont)
        self.lblActNotes.grid(row=10, column=1, sticky='nw')

        lblChangeName = ttk.Label(master=self.actionFrame, text="Change Name", font=self.regFont)
        lblChangeName.grid(row=0, column=0, sticky='nw')
        self.entChangeName = ttk.Entry(master=self.actionFrame, width=27)
        self.entChangeName.grid(row=0, column=1, sticky='nw')

        lblChangeMaxHP = ttk.Label(master=self.actionFrame, text="Change Max HP", font=self.regFont)
        lblChangeMaxHP.grid(row=1, column=0, sticky='nw')
        self.entNewMaxHP = ttk.Entry(master=self.actionFrame, width=27)
        self.entNewMaxHP.grid(row=1, column=1, sticky='nw')
        lblChangeTempHP = ttk.Label(master=self.actionFrame, text="Set Temp HP", font=self.regFont)
        lblChangeTempHP.grid(row=2, column=0, sticky='nw')
        self.entSetTempHP = ttk.Entry(master=self.actionFrame, width=27)
        self.entSetTempHP.grid(row=2, column=1, sticky='nw')
        self.setTempHP = tk.StringVar()
        rbnSetTHP = ttk.Radiobutton(master=self.actionFrame, text="Set", variable=self.setTempHP, value='set')
        rbnSetTHP.grid(row=2, column=2, sticky='nw')
        rbnRemoveTHP = ttk.Radiobutton(master=self.actionFrame, text="Remove", variable=self.setTempHP, value='remove')
        rbnRemoveTHP.grid(row=2, column=3, sticky='nw')
        lblChangeHP = ttk.Label(master=self.actionFrame, text="Heal/Damage HP", font=self.regFont)
        lblChangeHP.grid(row=3, column=0, sticky='nw')
        self.entHPDelta = ttk.Entry(master=self.actionFrame, width=27)
        self.entHPDelta.grid(row=3, column=1, sticky='nw')
        self.healHurt = tk.StringVar()
        rbnHeal = ttk.Radiobutton(master=self.actionFrame, text="Heal", variable=self.healHurt, value='heal')
        rbnHeal.grid(row=3, column=2, sticky='nw')
        rbnDamage = ttk.Radiobutton(master=self.actionFrame, text="Damage", variable=self.healHurt, value='damage')
        rbnDamage.grid(row=3, column=3, sticky='nw')

        lblChangeType = ttk.Label(master=self.actionFrame, text="Change Type", font=self.regFont)
        lblChangeType.grid(row=4, column=0, sticky='nw')
        self.type = tk.StringVar()
        self.rbnAlly = ttk.Radiobutton(master=self.actionFrame, text="Ally", variable= self.type, value="ally")
        self.rbnAlly.grid(row=4, column=2, sticky='nw')
        self.rbnEnemy = ttk.Radiobutton(master=self.actionFrame, text="Enemy", variable= self.type, value="enemy")
        self.rbnEnemy.grid(row=4, column=3, sticky='nw')
        self.rbnBystander = ttk.Radiobutton(master=self.actionFrame, text="Bystander", variable= self.type, value="bystander")
        self.rbnBystander.grid(row=5, column=2, sticky='nw')
        self.rbnDead = ttk.Radiobutton(master=self.actionFrame, text="Dead", variable= self.type, value="dead")
        self.rbnDead.grid(row=5, column=3, sticky='nw')

        lblChangeInit = ttk.Label(master=self.actionFrame, text="Change Initiative", font=self.regFont)
        lblChangeInit.grid(row=6, column=0, sticky='nw')
        self.entInitiative = ttk.Entry(master=self.actionFrame, width=27)
        self.entInitiative.grid(row=6, column=1, sticky='nw')

        lblChangeCondition = ttk.Label(master=self.actionFrame, text="Change Condition", font=self.regFont)
        lblChangeCondition.grid(row=7, column=0, sticky='nw')
        self.condNormal = tk.IntVar()
        self.condBlind = tk.IntVar()
        self.condCharmed = tk.IntVar()
        self.condDeaf = tk.IntVar()
        self.condFright = tk.IntVar()
        self.condGrappled = tk.IntVar()
        self.condIncapacitated = tk.IntVar()
        self.condInvisible = tk.IntVar()
        self.condParalyzed = tk.IntVar()
        self.condPetrified = tk.IntVar()
        self.condPoisoned = tk.IntVar()
        self.condProne = tk.IntVar()
        self.condRestrained = tk.IntVar()
        self.condStunned = tk.IntVar()
        self.condUnconscious = tk.IntVar()
        self.cbnNormal = ttk.Checkbutton(master=self.actionFrame, text="Normal", variable=self.condNormal, command=self.onOffButtons)
        self.cbnNormal.grid(row=7, column=2, columnspan=2,sticky='nw')
        self.cbnBlind = ttk.Checkbutton(master=self.actionFrame, text="Blinded", variable=self.condBlind)
        self.cbnBlind.grid(row=8, column=2, sticky='nw')
        self.cbnCharmed = ttk.Checkbutton(master=self.actionFrame, text="Charmed", variable=self.condCharmed)
        self.cbnCharmed.grid(row=8, column=3, sticky='nw')
        self.cbnDeaf = ttk.Checkbutton(master=self.actionFrame, text="Deafened", variable=self.condDeaf)
        self.cbnDeaf.grid(row=9, column=2, sticky='nw')
        self.cbnFright = ttk.Checkbutton(master=self.actionFrame, text="Frightened", variable=self.condFright)
        self.cbnFright.grid(row=9, column=3, sticky='nw')
        self.cbnGrappled = ttk.Checkbutton(master=self.actionFrame, text="Grappled", variable=self.condGrappled)
        self.cbnGrappled.grid(row=10, column=2, sticky='nw')
        self.cbnIncapacitated = ttk.Checkbutton(master=self.actionFrame, text="Incapacitated", variable=self.condIncapacitated, command=self.connectedCond)
        self.cbnIncapacitated.grid(row=10, column=3, sticky='nw')
        self.cbnInvisible = ttk.Checkbutton(master=self.actionFrame, text="Invisible", variable=self.condInvisible)
        self.cbnInvisible.grid(row=11, column=2, sticky='nw')
        self.cbnParalyzed = ttk.Checkbutton(master=self.actionFrame, text="Paralyzed", variable=self.condParalyzed, command=self.connectedCond)
        self.cbnParalyzed.grid(row=11, column=3, sticky='nw')
        self.cbnPetrified = ttk.Checkbutton(master=self.actionFrame, text="Petrified", variable=self.condPetrified, command=self.connectedCond)
        self.cbnPetrified.grid(row=12, column=2, sticky='nw')
        self.cbnPoisoned = ttk.Checkbutton(master=self.actionFrame, text="Poisoned", variable=self.condPoisoned)
        self.cbnPoisoned.grid(row=12, column=3, sticky='nw')
        self.cbnProne = ttk.Checkbutton(master=self.actionFrame, text="Prone", variable=self.condProne)
        self.cbnProne.grid(row=13, column=2, sticky='nw')
        self.cbnRestrained = ttk.Checkbutton(master=self.actionFrame, text="Restrained", variable=self.condRestrained)
        self.cbnRestrained.grid(row=13, column=3, sticky='nw')
        self.cbnStunned = ttk.Checkbutton(master=self.actionFrame, text="Stunned", variable=self.condStunned, command=self.connectedCond)
        self.cbnStunned.grid(row=14, column=2, sticky='nw')
        self.cbnUnconscious = ttk.Checkbutton(master=self.actionFrame, text="Unconscious", variable=self.condUnconscious, command=self.connectedCond)
        self.cbnUnconscious.grid(row=14, column=3, sticky='nw')
        lblExhaustion = ttk.Label(master=self.actionFrame, text="Exhaustion", font=self.regFont)
        lblExhaustion.grid(row=15, column=2, columnspan=2)
        self.exhaustionLevel = tk.IntVar()
        self.sldrExhaustion = tk.Scale(master=self.actionFrame, from_=0, to=6, variable=self.exhaustionLevel, orient=tk.HORIZONTAL, tickinterval=1, bg='gray28', fg='gray70', font=self.smallFont, highlightbackground='gray28', highlightcolor='gray28')
        self.sldrExhaustion.grid(row=16, column=2, columnspan=2)

        lblChangeNotes = ttk.Label(master=self.actionFrame, text="Change Notes", font=self.regFont)
        lblChangeNotes.grid(row=17, column=0, sticky='nw')
        self.checkDelete = tk.IntVar()
        cbnDeleteNotes = ttk.Checkbutton(master=self.actionFrame, text="Delete Notes", variable=self.checkDelete)
        cbnDeleteNotes.grid(row=17, column=1, sticky='ne')
        self.txtChangeNotes = tk.Text(master=self.actionFrame, height=5, width=52)
        self.txtChangeNotes.configure(font=self.smallFont)
        self.txtChangeNotes.grid(row=18, column=0, columnspan=4)

        self.btnSubmit = ttk.Button(master=self.submitFrame, text="Submit", width=20)#, command=self.onSubmit)
        self.btnSubmit.grid(row=0, column=0, sticky='e')
        self.btnDeleteTarget = ttk.Button(master=self.submitFrame, text="Delete", width=20)#, command=self.deleteToken)
        self.btnDeleteTarget.grid(row=0, column=1, sticky='w')
        self.lblCloseWindow = ttk.Label(master=self.submitFrame, text="Please close this window to finalize.", font=self.regFont)

    def selectTarget(self):
        selTarget = self.dropTargets.get()
        index = self.names.index(selTarget)
        objTarget = self.root.tokenList[index]
        self.lblActName.config(text=objTarget['name'])
        self.lblActMaxHP.config(text=objTarget['maxHP'])
        self.lblActTempHP.config(text=objTarget['tempHP'])
        self.lblActHP.config(text=objTarget['currentHP'])
        self.lblActType.config(text=objTarget['type'])
        self.lblActHeight.config(text=objTarget['height'])
        self.lblActSize.config(text=objTarget['size'])
        if objTarget['coordinate'][0] != "" and objTarget['coordinate'][1] != "" and objTarget['coordinate'][2] != "":
            row = int(objTarget['coordinate'][0]) + 1
            col = int(objTarget['coordinate'][1]) + 1
            z = int(objTarget['coordinate'][2])
        else:
            row = ""
            col = ""
            z = ""
        self.lblActCoord.config(text="{0}: {1}: {2}".format(row, col, z))
        allConditions = ""
        for cond in objTarget['condition']:
            if allConditions == "":
                allConditions += cond
            else:
                allConditions = allConditions + ", " + cond
        initCheck = objTarget['initiative']
        if initCheck == math.inf:
            initCheck = "Out of Initiative"
        self.lblActInit.config(text=initCheck)
        self.lblActCondition.config(text=allConditions)
        self.lblActNotes.config(text=objTarget['notes'])

    def onOffButtons(self):
        normValue = self.condNormal.get()
        if normValue == 1:
            self.cbnBlind.state(['disabled'])
            self.cbnCharmed.state(['disabled'])
            self.cbnDeaf.state(['disabled'])
            self.cbnFright.state(['disabled'])
            self.cbnGrappled.state(['disabled'])
            self.cbnIncapacitated.state(['disabled'])
            self.cbnInvisible.state(['disabled'])
            self.cbnParalyzed.state(['disabled'])
            self.cbnPetrified.state(['disabled'])
            self.cbnPoisoned.state(['disabled'])
            self.cbnProne.state(['disabled'])
            self.cbnRestrained.state(['disabled'])
            self.cbnStunned.state(['disabled'])
            self.cbnUnconscious.state(['disabled'])
            self.sldrExhaustion.config(state=tk.DISABLED, fg='gray40')
        else:
            self.cbnBlind.state(['!disabled'])
            self.cbnCharmed.state(['!disabled'])
            self.cbnDeaf.state(['!disabled'])
            self.cbnFright.state(['!disabled'])
            self.cbnGrappled.state(['!disabled'])
            self.cbnIncapacitated.state(['!disabled'])
            self.cbnInvisible.state(['!disabled'])
            self.cbnParalyzed.state(['!disabled'])
            self.cbnPetrified.state(['!disabled'])
            self.cbnPoisoned.state(['!disabled'])
            self.cbnProne.state(['!disabled'])
            self.cbnRestrained.state(['!disabled'])
            self.cbnStunned.state(['!disabled'])
            self.cbnUnconscious.state(['!disabled'])
            self.sldrExhaustion.config(state=tk.NORMAL, fg='gray70')

    def onSubmit(self):
        selTarget = self.dropTargets.get()
        if selTarget == "" or selTarget is None:
            messagebox.showinfo("Info", "Must select target creature.")
            return False

        index = self.names.index(selTarget)
        objTarget = self.root.tokenList[index]

        newName = self.entChangeName.get()
        if newName == "":
            newName = objTarget['name']

        newType = self.type.get()
        if newType == "":
            newType = objTarget['type']

        testMaxHP = self.entNewMaxHP.get()
        if testMaxHP == "":
            newMaxHP = objTarget['maxHP']
        else:
            try:
                newMaxHP = int(testMaxHP)
                if newMaxHP <= 0:
                    newMaxHP = 0
                    newType = 'dead'
            except ValueError:
                messagebox.showwarning("Target Creature", "Max HP must be a whole number.")
                return False
            except TypeError:
                messagebox.showwarning("Target Creature", "Max HP must be a whole number.")
                return False
        testTempHP = self.entSetTempHP.get()
        hPSetting = self.setTempHP.get()
        if testTempHP == "":
            newTempHP = objTarget['tempHP']
        elif hPSetting == 'remove':
            newTempHP = 0
        elif hPSetting == 'set':
            try:
                newTempHP = int(testTempHP)
                if newTempHP < 0:
                    newTempHP = 0
            except ValueError:
                messagebox.showwarning("Target Creature", "Temp HP must be a whole number.")
                return False
            except TypeError:
                messagebox.showwarning("Target Creature", "Temp HP must be a whole number.")
                return False
        else:
            messagebox.showwarning("Target Creature", "Must select \"Set\" or \"Remove\".")
            return False
        testHPDelta = self.entHPDelta.get()
        try:
            hPDelta = int(testHPDelta)
        except ValueError:
            hPDelta = 0
        except TypeError:
            hPDelta = 0
        if self.healHurt.get() == 'heal':
            newCurrHP = hPDelta + objTarget['currentHP']
            if newCurrHP > newMaxHP:
                newCurrHP = newMaxHP
        elif self.healHurt.get() == 'damage':
            newCurrHP = objTarget['currentHP'] - hPDelta
            if newCurrHP < newMaxHP * -1:
                newType = 'dead'
        else:
            newCurrHP = objTarget['currentHP']

        newInit = self.entInitiative.get()
        if newInit == "":
            newInit = objTarget['initiative']
        else:
            try:
                newInit = float(newInit)
            except ValueError:
                newInit = objTarget['initiative']
            except TypeError:
                newInit = objTarget['initiative']
        
        newCondition = []
        if self.condNormal.get() == 1 and newType != 'dead':
            newCondition.append("normal")
        elif self.condNormal.get() == 0 and self.condBlind.get() == 0 and self.condCharmed.get() == 0 and self.condDeaf.get() == 0 and self.condFright.get() == 0 and self.condGrappled.get() == 0 and self.condIncapacitated.get() == 0 and self.condInvisible.get() == 0 and self.condParalyzed.get() == 0 and self.condPetrified.get() == 0 and self.condPoisoned.get() == 0 and self.condProne.get() == 0 and self.condRestrained.get() == 0 and self.condStunned.get() == 0 and self.condUnconscious.get() == 0:
            newCondition = objTarget['condition']
        else:
            if self.condBlind.get() == 1:
                newCondition.append("blinded")
            if self.condCharmed.get() == 1:
                newCondition.append("charmed")
            if self.condDeaf.get() == 1:
                newCondition.append("deafened")
            if self.condFright.get() == 1:
                newCondition.append("frightened")
            if self.condGrappled.get() == 1:
                newCondition.append("grappled")
            if self.condIncapacitated.get() == 1:
                newCondition.append("incapacitated")
            if self.condInvisible.get() == 1:
                newCondition.append("invisible")
            if self.condParalyzed.get() == 1:
                newCondition.append("paralyzed")
            if self.condPetrified.get() == 1:
                newCondition.append("petrified")
            if self.condPoisoned.get() == 1:
                newCondition.append("poisoned")
            if self.condProne.get() == 1:
                newCondition.append("prone")
            if self.condRestrained.get() == 1:
                newCondition.append("restrained")
            if self.condStunned.get() == 1:
                newCondition.append("stunned")
            if self.condUnconscious.get() == 1:
                newCondition.append("unconscious")
            lvlExh = self.exhaustionLevel.get()
            if lvlExh > 0:
                newCondition.append("exhaustion level " + str(lvlExh))
            if lvlExh == 6:
                newType = 'dead'

        noNotes = self.checkDelete.get()
        newNotes = self.txtChangeNotes.get(1.0, tk.END)
        if noNotes == 0 and newNotes == "":
            newNotes = objTarget['notes']
        elif noNotes == 1:
            newNotes = ""

        newObjTarget = {
            "name": newName,
            "maxHP": newMaxHP,
            "tempHP": newTempHP,
            "currentHP": newCurrHP,
            "type": newType,
            "height": objTarget['height'],
            "size": objTarget['size'],
            "coordinate": objTarget['coordinate'],
            "condition": newCondition,
            "initiative": newInit,
            "notes": newNotes
        }
        if newObjTarget['name'] != objTarget['name']:
            self.root.tokenList.pop(index)
            self.root.tokenList.append(newObjTarget)
        else:
            self.root.tokenList[index] = newObjTarget
        
        return True
        #self.btnSubmit.state(['disabled'])
        #self.btnDeleteTarget.state(['disabled'])
        #self.lblCloseWindow.grid(row=1, column=0, columnspan=2)

    def deleteToken(self):
        selTarget = self.dropTargets.get()
        if selTarget != "" and selTarget is not None:
            goAhead = messagebox.askokcancel("Warning", "You are about to delete this creature.\nAre you sure?")
            if goAhead:
                index = self.names.index(selTarget)
                self.root.tokenList.pop(index)
                self.btnSubmit.state(['disabled'])
                self.btnDeleteTarget.state(['disabled'])
                self.lblCloseWindow.grid(row=1, column=0, columnspan=2)
                return True
            else:
                return False
        else:
            messagebox.showinfo("Info", "Must select a target creature.")
            return False
        
    def connectedCond(self):
        incap = self.condIncapacitated.get()
        parlz = self.condParalyzed.get()
        petr = self.condPetrified.get()
        stun = self.condStunned.get()
        aslp = self.condUnconscious.get()
        if parlz == 1 or petr == 1 or stun == 1 or aslp == 1:
            self.condIncapacitated.set(1)
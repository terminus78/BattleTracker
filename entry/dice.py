import math
import random

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle
import PIL.Image
from PIL import ImageTk


class DiceRoller():
    def __init__(self, root=None):
        self.dieOptions = [2, 4, 6, 8, 10, 12, 20, 100]
        self.root = root
        self.titleFont = ("Papyrus", "18")
        self.font = ("Papyrus", "14")
        self.fontSmall = ("Papyrus", "9")
    
    def roll(self, dieSize=20, numDice=1):
        if dieSize not in self.dieOptions:
            return [0]
        if type(numDice) != int or numDice < 1:
            return [0]
        diceResults = []
        for i in range(numDice):
            rollDie = random.randint(1, dieSize)
            diceResults.append(rollDie)
        return diceResults

    def dicePane(self):
        self.diceWin = tk.Toplevel(self.root)
        self.diceWin.title("Trig Calculator")
        style = ThemedStyle(self.diceWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.diceWin.configure(bg=style.lookup('TLabel', 'background'))
        lblTitle = ttk.Label(master=self.diceWin, text="Dice Roller", font=self.titleFont)
        lblTitle.grid(row=0, column=0)
        lblInstructions = ttk.Label(master=self.diceWin, text="Select the type and number of each that you would like to roll.", font=self.fontSmall)
        lblInstructions.grid(row=1, column=0)
        diceSelectionFrame = ttk.Frame(master=self.diceWin)
        diceSelectionFrame.grid(row=2, column=0)
        resultFrame = ttk.Frame(master=self.diceWin)
        resultFrame.grid(row=3, column=0, pady=10)

        # Image paths
        d20Path = "entry\\bin\\dice-twenty-faces-twenty.png"
        d20Pic = ImageTk.PhotoImage(image=PIL.Image.open(d20Path).resize((50,50)))
        d12Path = "entry\\bin\\d12.png"
        d12Pic = ImageTk.PhotoImage(image=PIL.Image.open(d12Path).resize((50,50)))
        d10Path = "entry\\bin\\d10.png"
        d10Pic = ImageTk.PhotoImage(image=PIL.Image.open(d10Path).resize((50,50)))
        d8Path = "entry\\bin\\dice-eight-faces-eight.png"
        d8Pic = ImageTk.PhotoImage(image=PIL.Image.open(d8Path).resize((50,50)))
        d6Path = "entry\\bin\\perspective-dice-six-faces-six.png"
        d6Pic = ImageTk.PhotoImage(image=PIL.Image.open(d6Path).resize((50,50)))
        d4Path = "entry\\bin\\d4.png"
        d4Pic = ImageTk.PhotoImage(image=PIL.Image.open(d4Path).resize((50,50)))
        #coinPath = "entry\\bin\\coin.png"
        #coinPic = ImageTk.PhotoImage(image=PIL.Image.open(coinPath).resize((50,50)))
        redD20Path = "entry\\bin\\red-dice-twenty-faces-twenty.png"
        redD20Pic = ImageTk.PhotoImage(image=PIL.Image.open(redD20Path).resize((50,50)))
        redD12Path = "entry\\bin\\red-d12.png"
        redD12Pic = ImageTk.PhotoImage(image=PIL.Image.open(redD12Path).resize((50,50)))
        redD10Path = "entry\\bin\\red-d10.png"
        redD10Pic = ImageTk.PhotoImage(image=PIL.Image.open(redD10Path).resize((50,50)))
        redD8Path = "entry\\bin\\red-dice-eight-faces-eight.png"
        redD8Pic = ImageTk.PhotoImage(image=PIL.Image.open(redD8Path).resize((50,50)))
        redD6Path = "entry\\bin\\red-perspective-dice-six-faces-six.png"
        redD6Pic = ImageTk.PhotoImage(image=PIL.Image.open(redD6Path).resize((50,50)))
        redD4Path = "entry\\bin\\red-d4.png"
        redD4Pic = ImageTk.PhotoImage(image=PIL.Image.open(redD4Path).resize((50,50)))

        lblD100Title = ttk.Label(master=diceSelectionFrame, text="D100", font=self.font)
        lblD100Title.image = redD10Pic
        lblD100Title.grid(row=0, column=0)
        lblD20Title = ttk.Label(master=diceSelectionFrame, text="D20", font=self.font)
        lblD20Title.image = redD20Pic
        lblD20Title.grid(row=0, column=1)
        lblD12Title = ttk.Label(master=diceSelectionFrame, text="D12", font=self.font)
        lblD12Title.image = redD12Pic
        lblD12Title.grid(row=0, column=2)
        lblD10Title = ttk.Label(master=diceSelectionFrame, text="D10", font=self.font)
        lblD10Title.image = redD10Pic
        lblD10Title.grid(row=0, column=3)
        lblD8Title = ttk.Label(master=diceSelectionFrame, text="D8", font=self.font)
        lblD8Title.image = redD8Pic
        lblD8Title.grid(row=0, column=4)
        lblD6Title = ttk.Label(master=diceSelectionFrame, text="D6", font=self.font)
        lblD6Title.image = redD6Pic
        lblD6Title.grid(row=0, column=5)
        lblD4Title = ttk.Label(master=diceSelectionFrame, text="D4", font=self.font)
        lblD4Title.image = redD4Pic
        lblD4Title.grid(row=0, column=6)
        #lblCoinTitle = ttk.Label(master=diceSelectionFrame, text="Coin", font=self.font)
        #lblCoinTitle.image = coinPic
        #lblCoinTitle.grid(row=0, column=7)

        lblD100 = ttk.Label(master=diceSelectionFrame, image=redD10Pic)
        lblD100.image = redD10Pic
        lblD100.grid(row=1, column=0)
        lblD20 = ttk.Label(master=diceSelectionFrame, image=redD20Pic)
        lblD20.image = redD20Pic
        lblD20.grid(row=1, column=1)
        lblD12 = ttk.Label(master=diceSelectionFrame, image=redD12Pic)
        lblD12.image = redD12Pic
        lblD12.grid(row=1, column=2)
        lblD10 = ttk.Label(master=diceSelectionFrame, image=redD10Pic)
        lblD10.image = redD10Pic
        lblD10.grid(row=1, column=3)
        lblD8 = ttk.Label(master=diceSelectionFrame, image=redD8Pic)
        lblD8.image = redD8Pic
        lblD8.grid(row=1, column=4)
        lblD6 = ttk.Label(master=diceSelectionFrame, image=redD6Pic)
        lblD6.image = redD6Pic
        lblD6.grid(row=1, column=5)
        lblD4 = ttk.Label(master=diceSelectionFrame, image=redD4Pic)
        lblD4.image = redD4Pic
        lblD4.grid(row=1, column=6)
        #lblCoin = ttk.Label(master=diceSelectionFrame, image=coinPic)
        #lblCoin.image = coinPic
        #lblCoin.grid(row=1, column=7)

        frameD100 = ttk.Frame(master=diceSelectionFrame)
        frameD100.grid(row=2, column=0)
        frameD20 = ttk.Frame(master=diceSelectionFrame)
        frameD20.grid(row=2, column=1)
        frameD12 = ttk.Frame(master=diceSelectionFrame)
        frameD12.grid(row=2, column=2)
        frameD10 = ttk.Frame(master=diceSelectionFrame)
        frameD10.grid(row=2, column=3)
        frameD8 = ttk.Frame(master=diceSelectionFrame)
        frameD8.grid(row=2, column=4)
        frameD6 = ttk.Frame(master=diceSelectionFrame)
        frameD6.grid(row=2, column=5)
        frameD4 = ttk.Frame(master=diceSelectionFrame)
        frameD4.grid(row=2, column=6)
        #frameCoin = ttk.Frame(master=diceSelectionFrame)
        #frameCoin.grid(row=2, column=7)

        # Modifiers
        lbl100Mod = ttk.Label(master=frameD100, text="Mod", font=self.fontSmall)
        lbl100Mod.grid(row=0, column=0, columnspan=3)
        btn100Lower = ttk.Button(master=frameD100, text="-", command=lambda: self.modifyMod(die='100', dir='-'), width=2)
        btn100Lower.grid(row=1, column=0)
        self.ent100Mod = ttk.Entry(master=frameD100, width=5)
        self.ent100Mod.grid(row=1, column=1)
        self.ent100Mod.insert(0, '0')
        btn100Raise = ttk.Button(master=frameD100, text="+", command=lambda: self.modifyMod(die='100', dir='+'), width=2)
        btn100Raise.grid(row=1, column=2)

        lbl20Mod = ttk.Label(master=frameD20, text="Mod", font=self.fontSmall)
        lbl20Mod.grid(row=0, column=0, columnspan=3)
        btn20Lower = ttk.Button(master=frameD20, text="-", command=lambda: self.modifyMod(die='20', dir='-'), width=2)
        btn20Lower.grid(row=1, column=0)
        self.ent20Mod = ttk.Entry(master=frameD20, width=5)
        self.ent20Mod.grid(row=1, column=1)
        self.ent20Mod.insert(0, '0')
        btn20Raise = ttk.Button(master=frameD20, text="+", command=lambda: self.modifyMod(die='20', dir='+'), width=2)
        btn20Raise.grid(row=1, column=2)

        lbl12Mod = ttk.Label(master=frameD12, text="Mod", font=self.fontSmall)
        lbl12Mod.grid(row=0, column=0, columnspan=3)
        btn12Lower = ttk.Button(master=frameD12, text="-", command=lambda: self.modifyMod(die='12', dir='-'), width=2)
        btn12Lower.grid(row=1, column=0)
        self.ent12Mod = ttk.Entry(master=frameD12, width=5)
        self.ent12Mod.grid(row=1, column=1)
        self.ent12Mod.insert(0, '0')
        btn12Raise = ttk.Button(master=frameD12, text="+", command=lambda: self.modifyMod(die='12', dir='+'), width=2)
        btn12Raise.grid(row=1, column=2)

        lbl10Mod = ttk.Label(master=frameD10, text="Mod", font=self.fontSmall)
        lbl10Mod.grid(row=0, column=0, columnspan=3)
        btn10Lower = ttk.Button(master=frameD10, text="-", command=lambda: self.modifyMod(die='10', dir='-'), width=2)
        btn10Lower.grid(row=1, column=0)
        self.ent10Mod = ttk.Entry(master=frameD10, width=5)
        self.ent10Mod.grid(row=1, column=1)
        self.ent10Mod.insert(0, '0')
        btn10Raise = ttk.Button(master=frameD10, text="+", command=lambda: self.modifyMod(die='10', dir='+'), width=2)
        btn10Raise.grid(row=1, column=2)

        lbl8Mod = ttk.Label(master=frameD8, text="Mod", font=self.fontSmall)
        lbl8Mod.grid(row=0, column=0, columnspan=3)
        btn8Lower = ttk.Button(master=frameD8, text="-", command=lambda: self.modifyMod(die='8', dir='-'), width=2)
        btn8Lower.grid(row=1, column=0)
        self.ent8Mod = ttk.Entry(master=frameD8, width=5)
        self.ent8Mod.grid(row=1, column=1)
        self.ent8Mod.insert(0, '0')
        btn8Raise = ttk.Button(master=frameD8, text="+", command=lambda: self.modifyMod(die='8', dir='+'), width=2)
        btn8Raise.grid(row=1, column=2)

        lbl6Mod = ttk.Label(master=frameD6, text="Mod", font=self.fontSmall)
        lbl6Mod.grid(row=0, column=0, columnspan=3)
        btn6Lower = ttk.Button(master=frameD6, text="-", command=lambda: self.modifyMod(die='6', dir='-'), width=2)
        btn6Lower.grid(row=1, column=0)
        self.ent6Mod = ttk.Entry(master=frameD6, width=5)
        self.ent6Mod.grid(row=1, column=1)
        self.ent6Mod.insert(0, '0')
        btn6Raise = ttk.Button(master=frameD6, text="+", command=lambda: self.modifyMod(die='6', dir='+'), width=2)
        btn6Raise.grid(row=1, column=2)

        lbl4Mod = ttk.Label(master=frameD4, text="Mod", font=self.fontSmall)
        lbl4Mod.grid(row=0, column=0, columnspan=3)
        btn4Lower = ttk.Button(master=frameD4, text="-", command=lambda: self.modifyMod(die='4', dir='-'), width=2)
        btn4Lower.grid(row=1, column=0)
        self.ent4Mod = ttk.Entry(master=frameD4, width=5)
        self.ent4Mod.grid(row=1, column=1)
        self.ent4Mod.insert(0, '0')
        btn4Raise = ttk.Button(master=frameD4, text="+", command=lambda: self.modifyMod(die='4', dir='+'), width=2)
        btn4Raise.grid(row=1, column=2)

        # Number to roll
        lbl100Num = ttk.Label(master=frameD100, text="Num", font=self.fontSmall)
        lbl100Num.grid(row=2, column=0, columnspan=3)
        btn100Lower = ttk.Button(master=frameD100, text="-", command=lambda: self.modifyNum(die='100', dir='-'), width=2)
        btn100Lower.grid(row=3, column=0)
        self.ent100Num = ttk.Entry(master=frameD100, width=5)
        self.ent100Num.grid(row=3, column=1)
        self.ent100Num.insert(0, '0')
        btn100Raise = ttk.Button(master=frameD100, text="+", command=lambda: self.modifyNum(die='100', dir='+'), width=2)
        btn100Raise.grid(row=3, column=2)

        lbl20Num = ttk.Label(master=frameD20, text="Num", font=self.fontSmall)
        lbl20Num.grid(row=2, column=0, columnspan=3)
        btn20Lower = ttk.Button(master=frameD20, text="-", command=lambda: self.modifyNum(die='20', dir='-'), width=2)
        btn20Lower.grid(row=3, column=0)
        self.ent20Num = ttk.Entry(master=frameD20, width=5)
        self.ent20Num.grid(row=3, column=1)
        self.ent20Num.insert(0, '0')
        btn20Raise = ttk.Button(master=frameD20, text="+", command=lambda: self.modifyNum(die='20', dir='+'), width=2)
        btn20Raise.grid(row=3, column=2)

        lbl12Num = ttk.Label(master=frameD12, text="Num", font=self.fontSmall)
        lbl12Num.grid(row=2, column=0, columnspan=3)
        btn12Lower = ttk.Button(master=frameD12, text="-", command=lambda: self.modifyNum(die='12', dir='-'), width=2)
        btn12Lower.grid(row=3, column=0)
        self.ent12Num = ttk.Entry(master=frameD12, width=5)
        self.ent12Num.grid(row=3, column=1)
        self.ent12Num.insert(0, '0')
        btn12Raise = ttk.Button(master=frameD12, text="+", command=lambda: self.modifyNum(die='12', dir='+'), width=2)
        btn12Raise.grid(row=3, column=2)

        lbl10Num = ttk.Label(master=frameD10, text="Num", font=self.fontSmall)
        lbl10Num.grid(row=2, column=0, columnspan=3)
        btn10Lower = ttk.Button(master=frameD10, text="-", command=lambda: self.modifyNum(die='10', dir='-'), width=2)
        btn10Lower.grid(row=3, column=0)
        self.ent10Num = ttk.Entry(master=frameD10, width=5)
        self.ent10Num.grid(row=3, column=1)
        self.ent10Num.insert(0, '0')
        btn10Raise = ttk.Button(master=frameD10, text="+", command=lambda: self.modifyNum(die='10', dir='+'), width=2)
        btn10Raise.grid(row=3, column=2)

        lbl8Num = ttk.Label(master=frameD8, text="Num", font=self.fontSmall)
        lbl8Num.grid(row=2, column=0, columnspan=3)
        btn8Lower = ttk.Button(master=frameD8, text="-", command=lambda: self.modifyNum(die='8', dir='-'), width=2)
        btn8Lower.grid(row=3, column=0)
        self.ent8Num = ttk.Entry(master=frameD8, width=5)
        self.ent8Num.grid(row=3, column=1)
        self.ent8Num.insert(0, '0')
        btn8Raise = ttk.Button(master=frameD8, text="+", command=lambda: self.modifyNum(die='8', dir='+'), width=2)
        btn8Raise.grid(row=3, column=2)

        lbl6Num = ttk.Label(master=frameD6, text="Num", font=self.fontSmall)
        lbl6Num.grid(row=2, column=0, columnspan=3)
        btn6Lower = ttk.Button(master=frameD6, text="-", command=lambda: self.modifyNum(die='6', dir='-'), width=2)
        btn6Lower.grid(row=3, column=0)
        self.ent6Num = ttk.Entry(master=frameD6, width=5)
        self.ent6Num.grid(row=3, column=1)
        self.ent6Num.insert(0, '0')
        btn6Raise = ttk.Button(master=frameD6, text="+", command=lambda: self.modifyNum(die='6', dir='+'), width=2)
        btn6Raise.grid(row=3, column=2)

        lbl4Num = ttk.Label(master=frameD4, text="Num", font=self.fontSmall)
        lbl4Num.grid(row=2, column=0, columnspan=3)
        btn4Lower = ttk.Button(master=frameD4, text="-", command=lambda: self.modifyNum(die='4', dir='-'), width=2)
        btn4Lower.grid(row=3, column=0)
        self.ent4Num = ttk.Entry(master=frameD4, width=5)
        self.ent4Num.grid(row=3, column=1)
        self.ent4Num.insert(0, '0')
        btn4Raise = ttk.Button(master=frameD4, text="+", command=lambda: self.modifyNum(die='4', dir='+'), width=2)
        btn4Raise.grid(row=3, column=2)

        # Roll buttons
        btn100Roll = ttk.Button(master=frameD100, text="Roll", command=lambda: self.rollWinBtn('100'))
        btn100Roll.grid(row=4, column=0, columnspan=3, pady=10)
        btn20Roll = ttk.Button(master=frameD20, text="Roll", command=lambda: self.rollWinBtn('20'))
        btn20Roll.grid(row=4, column=0, columnspan=3, pady=10)
        btn12Roll = ttk.Button(master=frameD12, text="Roll", command=lambda: self.rollWinBtn('12'))
        btn12Roll.grid(row=4, column=0, columnspan=3, pady=10)
        btn10Roll = ttk.Button(master=frameD10, text="Roll", command=lambda: self.rollWinBtn('10'))
        btn10Roll.grid(row=4, column=0, columnspan=3, pady=10)
        btn8Roll = ttk.Button(master=frameD8, text="Roll", command=lambda: self.rollWinBtn('8'))
        btn8Roll.grid(row=4, column=0, columnspan=3, pady=10)
        btn6Roll = ttk.Button(master=frameD6, text="Roll", command=lambda: self.rollWinBtn('6'))
        btn6Roll.grid(row=4, column=0, columnspan=3, pady=10)
        btn4Roll = ttk.Button(master=frameD4, text="Roll", command=lambda: self.rollWinBtn('4'))
        btn4Roll.grid(row=4, column=0, columnspan=3, pady=10)
        #btnCoinRoll = ttk.Button(master=frameCoin, text="Roll", command=lambda: self.rollWinBtn('coin'))
        #btnCoinRoll.grid(row=4, column=0, columnspan=3, pady=10)

        self.d100sRolled = ttk.Label(master=frameD100, text="", font=self.fontSmall)
        self.d20sRolled = ttk.Label(master=frameD20, text="", font=self.fontSmall)
        self.d12sRolled = ttk.Label(master=frameD12, text="", font=self.fontSmall)
        self.d10sRolled = ttk.Label(master=frameD10, text="", font=self.fontSmall)
        self.d8sRolled = ttk.Label(master=frameD8, text="", font=self.fontSmall)
        self.d6sRolled = ttk.Label(master=frameD6, text="", font=self.fontSmall)
        self.d4sRolled = ttk.Label(master=frameD4, text="", font=self.fontSmall)

        # Results
        frameRes1 = ttk.Frame(master=frameD100)
        frameRes1.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes1.columnconfigure([0,1], weight=1)
        frameRes2 = ttk.Frame(master=frameD20)
        frameRes2.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes2.columnconfigure([0,1], weight=1)
        frameRes3 = ttk.Frame(master=frameD12)
        frameRes3.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes3.columnconfigure([0,1], weight=1)
        frameRes4 = ttk.Frame(master=frameD10)
        frameRes4.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes4.columnconfigure([0,1], weight=1)
        frameRes5 = ttk.Frame(master=frameD8)
        frameRes5.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes5.columnconfigure([0,1], weight=1)
        frameRes6 = ttk.Frame(master=frameD6)
        frameRes6.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes6.columnconfigure([0,1], weight=1)
        frameRes7 = ttk.Frame(master=frameD4)
        frameRes7.grid(row=6, column=0, columnspan=3, pady=10)
        frameRes7.columnconfigure([0,1], weight=1)
        #frameRes8 = ttk.Frame(master=frameCoin)
        #frameRes8.grid(row=6, column=0, columnspan=3, pady=10)
        #frameRes8.columnconfigure([0,1], weight=1)

        lbl100Marker = ttk.Label(master=frameRes1, text="Roll: ", font=self.font)
        lbl100Marker.grid(row=0, column=0, sticky='w')
        self.lbl100Result = ttk.Label(master=frameRes1, text="0", font=self.font, width=3, anchor='center')
        self.lbl100Result.grid(row=0, column=1, sticky='e')
        lbl100OMark = ttk.Label(master=frameRes1, text="Mod: ", font=self.font)
        lbl100OMark.grid(row=1, column=0, sticky='w')
        self.lbl100Offset = ttk.Label(master=frameRes1, text="0", font=self.font, width=3, anchor='center')
        self.lbl100Offset.grid(row=1, column=1, sticky='e')
        lbl100TMark = ttk.Label(master=frameRes1, text="Total: ", font=self.font)
        lbl100TMark.grid(row=2, column=0, sticky='w')
        self.lbl100Total = ttk.Label(master=frameRes1, text="0", font=self.font, width=3, anchor='center')
        self.lbl100Total.grid(row=2, column=1, sticky='e')

        lbl20Marker = ttk.Label(master=frameRes2, text="Roll: ", font=self.font)
        lbl20Marker.grid(row=0, column=0, sticky='w')
        self.lbl20Result = ttk.Label(master=frameRes2, text="0", font=self.font, width=3, anchor='center')
        self.lbl20Result.grid(row=0, column=1, sticky='e')
        lbl20OMark = ttk.Label(master=frameRes2, text="Mod: ", font=self.font)
        lbl20OMark.grid(row=1, column=0, sticky='w')
        self.lbl20Offset = ttk.Label(master=frameRes2, text="0", font=self.font, width=3, anchor='center')
        self.lbl20Offset.grid(row=1, column=1, sticky='e')
        lbl20TMark = ttk.Label(master=frameRes2, text="Total: ", font=self.font)
        lbl20TMark.grid(row=2, column=0, sticky='w')
        self.lbl20Total = ttk.Label(master=frameRes2, text="0", font=self.font, width=3, anchor='center')
        self.lbl20Total.grid(row=2, column=1, sticky='e')

        lbl12Marker = ttk.Label(master=frameRes3, text="Roll: ", font=self.font)
        lbl12Marker.grid(row=0, column=0, sticky='w')
        self.lbl12Result = ttk.Label(master=frameRes3, text="0", font=self.font, width=3, anchor='center')
        self.lbl12Result.grid(row=0, column=1, sticky='e')
        lbl12OMark = ttk.Label(master=frameRes3, text="Mod: ", font=self.font)
        lbl12OMark.grid(row=1, column=0, sticky='w')
        self.lbl12Offset = ttk.Label(master=frameRes3, text="0", font=self.font, width=3, anchor='center')
        self.lbl12Offset.grid(row=1, column=1, sticky='e')
        lbl12TMark = ttk.Label(master=frameRes3, text="Total: ", font=self.font)
        lbl12TMark.grid(row=2, column=0, sticky='w')
        self.lbl12Total = ttk.Label(master=frameRes3, text="0", font=self.font, width=3, anchor='center')
        self.lbl12Total.grid(row=2, column=1, sticky='e')

        lbl10Marker = ttk.Label(master=frameRes4, text="Roll: ", font=self.font)
        lbl10Marker.grid(row=0, column=0, sticky='w')
        self.lbl10Result = ttk.Label(master=frameRes4, text="0", font=self.font, width=3, anchor='center')
        self.lbl10Result.grid(row=0, column=1, sticky='e')
        lbl10OMark = ttk.Label(master=frameRes4, text="Mod: ", font=self.font)
        lbl10OMark.grid(row=1, column=0, sticky='w')
        self.lbl10Offset = ttk.Label(master=frameRes4, text="0", font=self.font, width=3, anchor='center')
        self.lbl10Offset.grid(row=1, column=1, sticky='e')
        lbl10TMark = ttk.Label(master=frameRes4, text="Total: ", font=self.font)
        lbl10TMark.grid(row=2, column=0, sticky='w')
        self.lbl10Total = ttk.Label(master=frameRes4, text="0", font=self.font, width=3, anchor='center')
        self.lbl10Total.grid(row=2, column=1, sticky='e')

        lbl8Marker = ttk.Label(master=frameRes5, text="Roll: ", font=self.font)
        lbl8Marker.grid(row=0, column=0, sticky='w')
        self.lbl8Result = ttk.Label(master=frameRes5, text="0", font=self.font, width=3, anchor='center')
        self.lbl8Result.grid(row=0, column=1, sticky='e')
        lbl8OMark = ttk.Label(master=frameRes5, text="Mod: ", font=self.font)
        lbl8OMark.grid(row=1, column=0, sticky='w')
        self.lbl8Offset = ttk.Label(master=frameRes5, text="0", font=self.font, width=3, anchor='center')
        self.lbl8Offset.grid(row=1, column=1, sticky='e')
        lbl8TMark = ttk.Label(master=frameRes5, text="Total: ", font=self.font)
        lbl8TMark.grid(row=2, column=0, sticky='w')
        self.lbl8Total = ttk.Label(master=frameRes5, text="0", font=self.font, width=3, anchor='center')
        self.lbl8Total.grid(row=2, column=1, sticky='e')

        lbl6Marker = ttk.Label(master=frameRes6, text="Roll: ", font=self.font)
        lbl6Marker.grid(row=0, column=0, sticky='w')
        self.lbl6Result = ttk.Label(master=frameRes6, text="0", font=self.font, width=3, anchor='center')
        self.lbl6Result.grid(row=0, column=1, sticky='e')
        lbl6OMark = ttk.Label(master=frameRes6, text="Mod: ", font=self.font)
        lbl6OMark.grid(row=1, column=0, sticky='w')
        self.lbl6Offset = ttk.Label(master=frameRes6, text="0", font=self.font, width=3, anchor='center')
        self.lbl6Offset.grid(row=1, column=1, sticky='e')
        lbl6TMark = ttk.Label(master=frameRes6, text="Total: ", font=self.font)
        lbl6TMark.grid(row=2, column=0, sticky='w')
        self.lbl6Total = ttk.Label(master=frameRes6, text="0", font=self.font, width=3, anchor='center')
        self.lbl6Total.grid(row=2, column=1, sticky='e')

        lbl4Marker = ttk.Label(master=frameRes7, text="Roll: ", font=self.font)
        lbl4Marker.grid(row=0, column=0, sticky='w')
        self.lbl4Result = ttk.Label(master=frameRes7, text="0", font=self.font, width=3, anchor='center')
        self.lbl4Result.grid(row=0, column=1, sticky='e')
        lbl4OMark = ttk.Label(master=frameRes7, text="Mod: ", font=self.font)
        lbl4OMark.grid(row=1, column=0, sticky='w')
        self.lbl4Offset = ttk.Label(master=frameRes7, text="0", font=self.font, width=3, anchor='center')
        self.lbl4Offset.grid(row=1, column=1, sticky='e')
        lbl4TMark = ttk.Label(master=frameRes7, text="Total: ", font=self.font)
        lbl4TMark.grid(row=2, column=0, sticky='w')
        self.lbl4Total = ttk.Label(master=frameRes7, text="0", font=self.font, width=3, anchor='center')
        self.lbl4Total.grid(row=2, column=1, sticky='e')

        '''
        lblCoinMarker = ttk.Label(master=frameRes8, text="Roll: ", font=self.font)
        lblCoinMarker.grid(row=0, column=0, sticky='w')
        self.lblCoinResult = ttk.Label(master=frameRes8, text="0", font=self.font, width=3, anchor='center')
        self.lblCoinResult.grid(row=0, column=1, sticky='e')
        lblCoinOMark = ttk.Label(master=frameRes8, text="Mod: ", font=self.font)
        lblCoinOMark.grid(row=1, column=0, sticky='w')
        self.lblCoinOffset = ttk.Label(master=frameRes8, text="0", font=self.font, width=3, anchor='center')
        self.lblCoinOffset.grid(row=1, column=1, sticky='e')
        lblCoinTMark = ttk.Label(master=frameRes8, text="Total: ", font=self.font)
        lblCoinTMark.grid(row=2, column=0, sticky='w')
        self.lblCoinTotal = ttk.Label(master=frameRes8, text="0", font=self.font, width=3, anchor='center')
        self.lblCoinTotal.grid(row=2, column=1, sticky='e')
        '''

        lblNetMarker = ttk.Label(master=resultFrame, text="Net Total", font=self.font)
        lblNetMarker.grid(row=1, column=0, columnspan=7)
        self.lblNetTotal = ttk.Label(master=resultFrame, text="0", font=self.font, width=3, anchor='center')
        self.lblNetTotal.grid(row=2, column=0, columnspan=7)
        btnCalcNet = ttk.Button(master=resultFrame, text="Calculate Total", command=self.calcNet)
        btnCalcNet.grid(row=3, column=0, columnspan=7, pady=5)
        btnClearOut = ttk.Button(master=resultFrame, text="Clear Board", command=self.clearOut)
        btnClearOut.grid(row=4, column=0, columnspan=7, pady=5)
        
    def modifyMod(self, die, dir):
        if die == '100':
            try:
                modVal = int(self.ent100Mod.get())
            except ValueError:
                modVal = 0
                self.ent100Mod.delete(0, tk.END)
                self.ent100Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent100Mod.delete(0, tk.END)
                self.ent100Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent100Mod.delete(0, tk.END)
                self.ent100Mod.insert(0, modVal)
        elif die == '20':
            try:
                modVal = int(self.ent20Mod.get())
            except ValueError:
                modVal = 0
                self.ent20Mod.delete(0, tk.END)
                self.ent20Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent20Mod.delete(0, tk.END)
                self.ent20Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent20Mod.delete(0, tk.END)
                self.ent20Mod.insert(0, modVal)
        elif die == '12':
            try:
                modVal = int(self.ent12Mod.get())
            except ValueError:
                modVal = 0
                self.ent12Mod.delete(0, tk.END)
                self.ent12Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent12Mod.delete(0, tk.END)
                self.ent12Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent12Mod.delete(0, tk.END)
                self.ent12Mod.insert(0, modVal)
        elif die == '10':
            try:
                modVal = int(self.ent10Mod.get())
            except ValueError:
                modVal = 0
                self.ent10Mod.delete(0, tk.END)
                self.ent10Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent10Mod.delete(0, tk.END)
                self.ent10Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent10Mod.delete(0, tk.END)
                self.ent10Mod.insert(0, modVal)
        elif die == '8':
            try:
                modVal = int(self.ent8Mod.get())
            except ValueError:
                modVal = 0
                self.ent8Mod.delete(0, tk.END)
                self.ent8Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent8Mod.delete(0, tk.END)
                self.ent8Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent8Mod.delete(0, tk.END)
                self.ent8Mod.insert(0, modVal)
        elif die == '6':
            try:
                modVal = int(self.ent6Mod.get())
            except ValueError:
                modVal = 0
                self.ent6Mod.delete(0, tk.END)
                self.ent6Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent6Mod.delete(0, tk.END)
                self.ent6Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent6Mod.delete(0, tk.END)
                self.ent6Mod.insert(0, modVal)
        elif die == '4':
            try:
                modVal = int(self.ent4Mod.get())
            except ValueError:
                modVal = 0
                self.ent4Mod.delete(0, tk.END)
                self.ent4Mod.insert(0, modVal)
                return
            if dir == '+':
                modVal += 1
                self.ent4Mod.delete(0, tk.END)
                self.ent4Mod.insert(0, modVal)
            else:
                modVal -= 1
                self.ent4Mod.delete(0, tk.END)
                self.ent4Mod.insert(0, modVal)
        else:
            messagebox.showerror("Dice Roller", "Internal system error. File may be corrupted.")
            return

    def modifyNum(self, die, dir):
        if die == '100':
            try:
                numVal = int(self.ent100Num.get())
            except ValueError:
                numVal = 0
                self.ent100Num.delete(0, tk.END)
                self.ent100Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent100Num.delete(0, tk.END)
                self.ent100Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent100Num.delete(0, tk.END)
                self.ent100Num.insert(0, numVal)
        elif die == '20':
            try:
                numVal = int(self.ent20Num.get())
            except ValueError:
                numVal = 0
                self.ent20Num.delete(0, tk.END)
                self.ent20Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent20Num.delete(0, tk.END)
                self.ent20Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent20Num.delete(0, tk.END)
                self.ent20Num.insert(0, numVal)
        elif die == '12':
            try:
                numVal = int(self.ent12Num.get())
            except ValueError:
                numVal = 0
                self.ent12Num.delete(0, tk.END)
                self.ent12Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent12Num.delete(0, tk.END)
                self.ent12Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent12Num.delete(0, tk.END)
                self.ent12Num.insert(0, numVal)
        elif die == '10':
            try:
                numVal = int(self.ent10Num.get())
            except ValueError:
                numVal = 0
                self.ent10Num.delete(0, tk.END)
                self.ent10Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent10Num.delete(0, tk.END)
                self.ent10Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent10Num.delete(0, tk.END)
                self.ent10Num.insert(0, numVal)
        elif die == '8':
            try:
                numVal = int(self.ent8Num.get())
            except ValueError:
                numVal = 0
                self.ent8Num.delete(0, tk.END)
                self.ent8Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent8Num.delete(0, tk.END)
                self.ent8Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent8Num.delete(0, tk.END)
                self.ent8Num.insert(0, numVal)
        elif die == '6':
            try:
                numVal = int(self.ent6Num.get())
            except ValueError:
                numVal = 0
                self.ent6Num.delete(0, tk.END)
                self.ent6Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent6Num.delete(0, tk.END)
                self.ent6Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent6Num.delete(0, tk.END)
                self.ent6Num.insert(0, numVal)
        elif die == '4':
            try:
                numVal = int(self.ent4Num.get())
            except ValueError:
                numVal = 0
                self.ent4Num.delete(0, tk.END)
                self.ent4Num.insert(0, numVal)
                return
            if dir == '+':
                numVal += 1
                self.ent4Num.delete(0, tk.END)
                self.ent4Num.insert(0, numVal)
            else:
                numVal -= 1
                if numVal < 0:
                    numVal = 0
                self.ent4Num.delete(0, tk.END)
                self.ent4Num.insert(0, numVal)
        else:
            messagebox.showerror("Dice Roller", "Internal system error. File may be corrupted.")
            return

    def rollWinBtn(self, die):
        if die == '100':
            try:
                mod100 = int(self.ent100Mod.get())
                num100 = int(self.ent100Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result100List = self.roll(dieSize=100, numDice=num100)
            dice100Sum = 0
            rollValues = str(result100List[0])
            numOfLoops = 0
            for res in result100List:
                dice100Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num100 - 1:
                    rollValues = rollValues + f" {res}"
            if num100 > 0:
                self.d100sRolled.config(text=rollValues)
                self.d100sRolled.grid(row=5, column=0)
            else:
                self.d100sRolled.grid_forget()
            mod100Str = str(mod100)
            if mod100 > 0:
                mod100Str = "+" + mod100Str
            self.lbl100Result.config(text=dice100Sum)
            self.lbl100Offset.config(text=mod100Str)
            dice100Total = dice100Sum + mod100
            self.lbl100Total.config(text=dice100Total)
        elif die == '20':
            try:
                mod20 = int(self.ent20Mod.get())
                num20 = int(self.ent20Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result20List = self.roll(dieSize=20, numDice=num20)
            dice20Sum = 0
            rollValues = str(result20List[0])
            numOfLoops = 0
            for res in result20List:
                dice20Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num20 - 1:
                    rollValues = rollValues + f" {res}"
            if num20 > 0:
                self.d20sRolled.config(text=rollValues)
                self.d20sRolled.grid(row=5, column=0)
            else:
                self.d20sRolled.grid_forget()
            mod20Str = str(mod20)
            if mod20 > 0:
                mod20Str = "+" + mod20Str
            self.lbl20Result.config(text=dice20Sum)
            self.lbl20Offset.config(text=mod20Str)
            dice20Total = dice20Sum + mod20
            self.lbl20Total.config(text=dice20Total)
        elif die == '12':
            try:
                mod12 = int(self.ent12Mod.get())
                num12 = int(self.ent12Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result12List = self.roll(dieSize=12, numDice=num12)
            dice12Sum = 0
            rollValues = str(result12List[0])
            numOfLoops = 0
            for res in result12List:
                dice12Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num12 - 1:
                    rollValues = rollValues + f" {res}"
            if num12 > 0:
                self.d12sRolled.config(text=rollValues)
                self.d12sRolled.grid(row=5, column=0)
            else:
                self.d12sRolled.grid_forget()
            mod12Str = str(mod12)
            if mod12 > 0:
                mod12Str = "+" + mod12Str
            self.lbl12Result.config(text=dice12Sum)
            self.lbl12Offset.config(text=mod12Str)
            dice12Total = dice12Sum + mod12
            self.lbl12Total.config(text=dice12Total)
        elif die == '10':
            try:
                mod10 = int(self.ent10Mod.get())
                num10 = int(self.ent10Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result10List = self.roll(dieSize=10, numDice=num10)
            dice10Sum = 0
            rollValues = str(result10List[0])
            numOfLoops = 0
            for res in result10List:
                dice10Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num10 - 1:
                    rollValues = rollValues + f" {res}"
            if num10 > 0:
                self.d10sRolled.config(text=rollValues)
                self.d10sRolled.grid(row=5, column=0)
            else:
                self.d10sRolled.grid_forget()
            mod10Str = str(mod10)
            if mod10 > 0:
                mod10Str = "+" + mod10Str
            self.lbl10Result.config(text=dice10Sum)
            self.lbl10Offset.config(text=mod10Str)
            dice10Total = dice10Sum + mod10
            self.lbl10Total.config(text=dice10Total)
        elif die == '8':
            try:
                mod8 = int(self.ent8Mod.get())
                num8 = int(self.ent8Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result8List = self.roll(dieSize=8, numDice=num8)
            dice8Sum = 0
            rollValues = str(result8List[0])
            numOfLoops = 0
            for res in result8List:
                dice8Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num8 - 1:
                    rollValues = rollValues + f" {res}"
            if num8 > 0:
                self.d8sRolled.config(text=rollValues)
                self.d8sRolled.grid(row=5, column=0)
            else:
                self.d8sRolled.grid_forget()
            mod8Str = str(mod8)
            if mod8 > 0:
                mod8Str = "+" + mod8Str
            self.lbl8Result.config(text=dice8Sum)
            self.lbl8Offset.config(text=mod8Str)
            dice8Total = dice8Sum + mod8
            self.lbl8Total.config(text=dice8Total)
        elif die == '6':
            try:
                mod6 = int(self.ent6Mod.get())
                num6 = int(self.ent6Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result6List = self.roll(dieSize=6, numDice=num6)
            dice6Sum = 0
            rollValues = str(result6List[0])
            numOfLoops = 0
            for res in result6List:
                dice6Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num6 - 1:
                    rollValues = rollValues + f" {res}"
            if num6 > 0:
                self.d6sRolled.config(text=rollValues)
                self.d6sRolled.grid(row=5, column=0)
            else:
                self.d6sRolled.grid_forget()
            mod6Str = str(mod6)
            if mod6 > 0:
                mod6Str = "+" + mod6Str
            self.lbl6Result.config(text=dice6Sum)
            self.lbl6Offset.config(text=mod6Str)
            dice6Total = dice6Sum + mod6
            self.lbl6Total.config(text=dice6Total)
        elif die == '4':
            try:
                mod4 = int(self.ent4Mod.get())
                num4 = int(self.ent4Num.get())
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result4List = self.roll(dieSize=4, numDice=num4)
            dice4Sum = 0
            rollValues = str(result4List[0])
            numOfLoops = 0
            for res in result4List:
                dice4Sum += res
                if numOfLoops > 0:
                    rollValues = rollValues + f" {res},"
                elif numOfLoops == num4 - 1:
                    rollValues = rollValues + f" {res}"
            if num4 > 0:
                self.d4sRolled.config(text=rollValues)
                self.d4sRolled.grid(row=5, column=0)
            else:
                self.d4sRolled.grid_forget()
            mod4Str = str(mod4)
            if mod4 > 0:
                mod4Str = "+" + mod4Str
            self.lbl4Result.config(text=dice4Sum)
            self.lbl4Offset.config(text=mod4Str)
            dice4Total = dice4Sum + mod4
            self.lbl4Total.config(text=dice4Total)
        else:
            messagebox.showerror("Dice Roller", "Internal system error. File may be corrupted.")
            return

    def calcNet(self):
        try:
            total100 = int(self.lbl100Total.cget("text"))
            total20 = int(self.lbl20Total.cget("text"))
            total12 = int(self.lbl12Total.cget("text"))
            total10 = int(self.lbl10Total.cget("text"))
            total8 = int(self.lbl8Total.cget("text"))
            total6 = int(self.lbl6Total.cget("text"))
            total4 = int(self.lbl4Total.cget("text"))
        except ValueError:
            messagebox.showwarning("Dice Roller", "Dice totals must be whole numbers.")
            return
        netTotal = total100 + total20 + total12 + total10 + total8 + total6 + total4
        self.lblNetTotal.config(text=netTotal)

    def clearOut(self):
        self.ent100Mod.delete(0, tk.END)
        self.ent100Mod.insert(0, "0")
        self.ent100Num.delete(0, tk.END)
        self.ent100Num.insert(0, "0")
        self.ent20Mod.delete(0, tk.END)
        self.ent20Mod.insert(0, "0")
        self.ent20Num.delete(0, tk.END)
        self.ent20Num.insert(0, "0")
        self.ent12Mod.delete(0, tk.END)
        self.ent12Mod.insert(0, "0")
        self.ent12Num.delete(0, tk.END)
        self.ent12Num.insert(0, "0")
        self.ent10Mod.delete(0, tk.END)
        self.ent10Mod.insert(0, "0")
        self.ent10Num.delete(0, tk.END)
        self.ent10Num.insert(0, "0")
        self.ent8Mod.delete(0, tk.END)
        self.ent8Mod.insert(0, "0")
        self.ent8Num.delete(0, tk.END)
        self.ent8Num.insert(0, "0")
        self.ent6Mod.delete(0, tk.END)
        self.ent6Mod.insert(0, "0")
        self.ent6Num.delete(0, tk.END)
        self.ent6Num.insert(0, "0")
        self.ent4Mod.delete(0, tk.END)
        self.ent4Mod.insert(0, "0")
        self.ent4Num.delete(0, tk.END)
        self.ent4Num.insert(0, "0")

        self.lbl100Total.config(text="0")
        self.lbl100Offset.config(text="0")
        self.lbl100Result.config(text="0")
        self.lbl20Total.config(text="0")
        self.lbl20Offset.config(text="0")
        self.lbl20Result.config(text="0")
        self.lbl12Total.config(text="0")
        self.lbl12Offset.config(text="0")
        self.lbl12Result.config(text="0")
        self.lbl10Total.config(text="0")
        self.lbl10Offset.config(text="0")
        self.lbl10Result.config(text="0")
        self.lbl8Total.config(text="0")
        self.lbl8Offset.config(text="0")
        self.lbl8Result.config(text="0")
        self.lbl6Total.config(text="0")
        self.lbl6Offset.config(text="0")
        self.lbl6Result.config(text="0")
        self.lbl4Total.config(text="0")
        self.lbl4Offset.config(text="0")
        self.lbl4Result.config(text="0")
        self.lblNetTotal.config(text="0")
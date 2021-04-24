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
        resultFrame.grid(row=3, column=0)

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
        coinPath = "entry\\bin\\coin.png"
        coinPic = ImageTk.PhotoImage(image=PIL.Image.open(coinPath).resize((50,50)))

        lblD100Title = ttk.Label(master=diceSelectionFrame, text="D100", font=self.font)
        lblD100Title.image = d10Pic
        lblD100Title.grid(row=0, column=0)
        lblD20Title = ttk.Label(master=diceSelectionFrame, text="D20", font=self.font)
        lblD20Title.image = d20Pic
        lblD20Title.grid(row=0, column=1)
        lblD12Title = ttk.Label(master=diceSelectionFrame, text="D12", font=self.font)
        lblD12Title.image = d12Pic
        lblD12Title.grid(row=0, column=2)
        lblD10Title = ttk.Label(master=diceSelectionFrame, text="D10", font=self.font)
        lblD10Title.image = d10Pic
        lblD10Title.grid(row=0, column=3)
        lblD8Title = ttk.Label(master=diceSelectionFrame, text="D8", font=self.font)
        lblD8Title.image = d8Pic
        lblD8Title.grid(row=0, column=4)
        lblD6Title = ttk.Label(master=diceSelectionFrame, text="D6", font=self.font)
        lblD6Title.image = d6Pic
        lblD6Title.grid(row=0, column=5)
        lblD4Title = ttk.Label(master=diceSelectionFrame, text="D4", font=self.font)
        lblD4Title.image = d4Pic
        lblD4Title.grid(row=0, column=6)
        lblCoinTitle = ttk.Label(master=diceSelectionFrame, text="Coin\nFlip", font=self.font)
        lblCoinTitle.image = coinPic
        lblCoinTitle.grid(row=0, column=7)

        lblD100 = ttk.Label(master=diceSelectionFrame, image=d10Pic)
        lblD100.image = d10Pic
        lblD100.grid(row=1, column=0)
        lblD20 = ttk.Label(master=diceSelectionFrame, image=d20Pic)
        lblD20.image = d20Pic
        lblD20.grid(row=1, column=1)
        lblD12 = ttk.Label(master=diceSelectionFrame, image=d12Pic)
        lblD12.image = d12Pic
        lblD12.grid(row=1, column=2)
        lblD10 = ttk.Label(master=diceSelectionFrame, image=d10Pic)
        lblD10.image = d10Pic
        lblD10.grid(row=1, column=3)
        lblD8 = ttk.Label(master=diceSelectionFrame, image=d8Pic)
        lblD8.image = d8Pic
        lblD8.grid(row=1, column=4)
        lblD6 = ttk.Label(master=diceSelectionFrame, image=d6Pic)
        lblD6.image = d6Pic
        lblD6.grid(row=1, column=5)
        lblD4 = ttk.Label(master=diceSelectionFrame, image=d4Pic)
        lblD4.image = d4Pic
        lblD4.grid(row=1, column=6)
        lblCoin = ttk.Label(master=diceSelectionFrame, image=coinPic)
        lblCoin.image = coinPic
        lblCoin.grid(row=1, column=7)

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
        frameCoin = ttk.Frame(master=diceSelectionFrame)
        frameCoin.grid(row=2, column=7)

        # Modifiers
        lbl100Mod = ttk.Label(master=frameD100, text="Mod", font=self.fontSmall)
        lbl100Mod.grid(row=0, column=0, columnspan=3)
        btn100Lower = ttk.Button(master=frameD100, text="-", command=lambda: self.modifyMod(die='100', dir='-'), width=2)
        btn100Lower.grid(row=1, column=0)
        self.ent100Mod = ttk.Entry(master=frameD100, width=5)
        self.ent100Mod.grid(row=1, column=1)
        btn100Raise = ttk.Button(master=frameD100, text="+", command=lambda: self.modifyMod(die='100', dir='+'), width=2)
        btn100Raise.grid(row=1, column=2)

        lbl20Mod = ttk.Label(master=frameD20, text="Mod", font=self.fontSmall)
        lbl20Mod.grid(row=0, column=0, columnspan=3)
        btn20Lower = ttk.Button(master=frameD20, text="-", command=lambda: self.modifyMod(die='20', dir='-'), width=2)
        btn20Lower.grid(row=1, column=0)
        self.ent20Mod = ttk.Entry(master=frameD20, width=5)
        self.ent20Mod.grid(row=1, column=1)
        btn20Raise = ttk.Button(master=frameD20, text="+", command=lambda: self.modifyMod(die='20', dir='+'), width=2)
        btn20Raise.grid(row=1, column=2)

        lbl12Mod = ttk.Label(master=frameD12, text="Mod", font=self.fontSmall)
        lbl12Mod.grid(row=0, column=0, columnspan=3)
        btn12Lower = ttk.Button(master=frameD12, text="-", command=lambda: self.modifyMod(die='12', dir='-'), width=2)
        btn12Lower.grid(row=1, column=0)
        self.ent12Mod = ttk.Entry(master=frameD12, width=5)
        self.ent12Mod.grid(row=1, column=1)
        btn12Raise = ttk.Button(master=frameD12, text="+", command=lambda: self.modifyMod(die='12', dir='+'), width=2)
        btn12Raise.grid(row=1, column=2)

        lbl10Mod = ttk.Label(master=frameD10, text="Mod", font=self.fontSmall)
        lbl10Mod.grid(row=0, column=0, columnspan=3)
        btn10Lower = ttk.Button(master=frameD10, text="-", command=lambda: self.modifyMod(die='10', dir='-'), width=2)
        btn10Lower.grid(row=1, column=0)
        self.ent10Mod = ttk.Entry(master=frameD10, width=5)
        self.ent10Mod.grid(row=1, column=1)
        btn10Raise = ttk.Button(master=frameD10, text="+", command=lambda: self.modifyMod(die='10', dir='+'), width=2)
        btn10Raise.grid(row=1, column=2)

        lbl8Mod = ttk.Label(master=frameD8, text="Mod", font=self.fontSmall)
        lbl8Mod.grid(row=0, column=0, columnspan=3)
        btn8Lower = ttk.Button(master=frameD8, text="-", command=lambda: self.modifyMod(die='8', dir='-'), width=2)
        btn8Lower.grid(row=1, column=0)
        self.ent8Mod = ttk.Entry(master=frameD8, width=5)
        self.ent8Mod.grid(row=1, column=1)
        btn8Raise = ttk.Button(master=frameD8, text="+", command=lambda: self.modifyMod(die='8', dir='+'), width=2)
        btn8Raise.grid(row=1, column=2)

        lbl6Mod = ttk.Label(master=frameD6, text="Mod", font=self.fontSmall)
        lbl6Mod.grid(row=0, column=0, columnspan=3)
        btn6Lower = ttk.Button(master=frameD6, text="-", command=lambda: self.modifyMod(die='6', dir='-'), width=2)
        btn6Lower.grid(row=1, column=0)
        self.ent6Mod = ttk.Entry(master=frameD6, width=5)
        self.ent6Mod.grid(row=1, column=1)
        btn6Raise = ttk.Button(master=frameD6, text="+", command=lambda: self.modifyMod(die='6', dir='+'), width=2)
        btn6Raise.grid(row=1, column=2)

        lbl4Mod = ttk.Label(master=frameD4, text="Mod", font=self.fontSmall)
        lbl4Mod.grid(row=0, column=0, columnspan=3)
        btn4Lower = ttk.Button(master=frameD4, text="-", command=lambda: self.modifyMod(die='4', dir='-'), width=2)
        btn4Lower.grid(row=1, column=0)
        self.ent4Mod = ttk.Entry(master=frameD4, width=5)
        self.ent4Mod.grid(row=1, column=1)
        btn4Raise = ttk.Button(master=frameD4, text="+", command=lambda: self.modifyMod(die='4', dir='+'), width=2)
        btn4Raise.grid(row=1, column=2)

        # Number to roll
        lbl100Num = ttk.Label(master=frameD100, text="Num", font=self.fontSmall)
        lbl100Num.grid(row=0, column=0, columnspan=3)
        btn100Lower = ttk.Button(master=frameD100, text="-", command=lambda: self.modifyNum(die='100', dir='-'), width=2)
        btn100Lower.grid(row=1, column=0)
        self.ent100Num = ttk.Entry(master=frameD100, width=5)
        self.ent100Num.grid(row=1, column=1)
        btn100Raise = ttk.Button(master=frameD100, text="+", command=lambda: self.modifyNum(die='100', dir='+'), width=2)
        btn100Raise.grid(row=1, column=2)

        lbl20Num = ttk.Label(master=frameD20, text="Num", font=self.fontSmall)
        lbl20Num.grid(row=0, column=0, columnspan=3)
        btn20Lower = ttk.Button(master=frameD20, text="-", command=lambda: self.modifyNum(die='20', dir='-'), width=2)
        btn20Lower.grid(row=1, column=0)
        self.ent20Num = ttk.Entry(master=frameD20, width=5)
        self.ent20Num.grid(row=1, column=1)
        btn20Raise = ttk.Button(master=frameD20, text="+", command=lambda: self.modifyNum(die='20', dir='+'), width=2)
        btn20Raise.grid(row=1, column=2)

        lbl12Num = ttk.Label(master=frameD12, text="Num", font=self.fontSmall)
        lbl12Num.grid(row=0, column=0, columnspan=3)
        btn12Lower = ttk.Button(master=frameD12, text="-", command=lambda: self.modifyNum(die='12', dir='-'), width=2)
        btn12Lower.grid(row=1, column=0)
        self.ent12Num = ttk.Entry(master=frameD12, width=5)
        self.ent12Num.grid(row=1, column=1)
        btn12Raise = ttk.Button(master=frameD12, text="+", command=lambda: self.modifyNum(die='12', dir='+'), width=2)
        btn12Raise.grid(row=1, column=2)

        lbl10Num = ttk.Label(master=frameD10, text="Num", font=self.fontSmall)
        lbl10Num.grid(row=0, column=0, columnspan=3)
        btn10Lower = ttk.Button(master=frameD10, text="-", command=lambda: self.modifyNum(die='10', dir='-'), width=2)
        btn10Lower.grid(row=1, column=0)
        self.ent10Num = ttk.Entry(master=frameD10, width=5)
        self.ent10Num.grid(row=1, column=1)
        btn10Raise = ttk.Button(master=frameD10, text="+", command=lambda: self.modifyNum(die='10', dir='+'), width=2)
        btn10Raise.grid(row=1, column=2)

        lbl8Num = ttk.Label(master=frameD8, text="Num", font=self.fontSmall)
        lbl8Num.grid(row=0, column=0, columnspan=3)
        btn8Lower = ttk.Button(master=frameD8, text="-", command=lambda: self.modifyNum(die='8', dir='-'), width=2)
        btn8Lower.grid(row=1, column=0)
        self.ent8Num = ttk.Entry(master=frameD8, width=5)
        self.ent8Num.grid(row=1, column=1)
        btn8Raise = ttk.Button(master=frameD8, text="+", command=lambda: self.modifyNum(die='8', dir='+'), width=2)
        btn8Raise.grid(row=1, column=2)

        lbl6Num = ttk.Label(master=frameD6, text="Num", font=self.fontSmall)
        lbl6Num.grid(row=0, column=0, columnspan=3)
        btn6Lower = ttk.Button(master=frameD6, text="-", command=lambda: self.modifyNum(die='6', dir='-'), width=2)
        btn6Lower.grid(row=1, column=0)
        self.ent6Num = ttk.Entry(master=frameD6, width=5)
        self.ent6Num.grid(row=1, column=1)
        btn6Raise = ttk.Button(master=frameD6, text="+", command=lambda: self.modifyNum(die='6', dir='+'), width=2)
        btn6Raise.grid(row=1, column=2)

        lbl4Num = ttk.Label(master=frameD4, text="Num", font=self.fontSmall)
        lbl4Num.grid(row=0, column=0, columnspan=3)
        btn4Lower = ttk.Button(master=frameD4, text="-", command=lambda: self.modifyNum(die='4', dir='-'), width=2)
        btn4Lower.grid(row=1, column=0)
        self.ent4Num = ttk.Entry(master=frameD4, width=5)
        self.ent4Num.grid(row=1, column=1)
        btn4Raise = ttk.Button(master=frameD4, text="+", command=lambda: self.modifyNum(die='4', dir='+'), width=2)
        btn4Raise.grid(row=1, column=2)

        # Roll buttons
        btn100Roll = ttk.Button(master=frameD100, text="Roll", command=lambda: self.rollWinBtn('100'))
        btn100Roll.grid(row=2, column=0)
        btn20Roll = ttk.Button(master=frameD20, text="Roll", command=lambda: self.rollWinBtn('20'))
        btn20Roll.grid(row=2, column=0)
        btn12Roll = ttk.Button(master=frameD12, text="Roll", command=lambda: self.rollWinBtn('12'))
        btn12Roll.grid(row=2, column=0)
        btn10Roll = ttk.Button(master=frameD10, text="Roll", command=lambda: self.rollWinBtn('10'))
        btn10Roll.grid(row=2, column=0)
        btn8Roll = ttk.Button(master=frameD8, text="Roll", command=lambda: self.rollWinBtn('8'))
        btn8Roll.grid(row=2, column=0)
        btn6Roll = ttk.Button(master=frameD6, text="Roll", command=lambda: self.rollWinBtn('6'))
        btn6Roll.grid(row=2, column=0)
        btn4Roll = ttk.Button(master=frameD4, text="Roll", command=lambda: self.rollWinBtn('4'))
        btn4Roll.grid(row=2, column=0)
        btnCoinRoll = ttk.Button(master=frameCoin, text="Roll", command=lambda: self.rollWinBtn('coin'))
        btnCoinRoll.grid(row=2, column=0)

        # Results
        frame100Result = ttk.Frame(master=resultFrame)
        frame100Result.grid(row=0, column=0)
        frame20Result = ttk.Frame(master=resultFrame)
        frame20Result.grid(row=0, column=1)
        frame12Result = ttk.Frame(master=resultFrame)
        frame12Result.grid(row=0, column=2)
        frame10Result = ttk.Frame(master=resultFrame)
        frame10Result.grid(row=0, column=3)
        frame8Result = ttk.Frame(master=resultFrame)
        frame8Result.grid(row=0, column=4)
        frame6Result = ttk.Frame(master=resultFrame)
        frame6Result.grid(row=0, column=5)
        frame4Result = ttk.Frame(master=resultFrame)
        frame4Result.grid(row=0, column=6)
        frameCoinResult = ttk.Frame(master=resultFrame)
        frameCoinResult.grid(row=0, column=7)

        lbl100Marker = ttk.Label(master=frame100Result, text="Roll:", font=self.font)
        lbl100Marker.grid(row=0, column=0, sticky='w')
        self.lbl100Result = ttk.Label(master=frame100Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl100Result.grid(row=0, column=1, sticky='e')
        lbl100OMark = ttk.Label(master=frame100Result, text="Mod:", font=self.font)
        lbl100OMark.grid(row=1, column=0, sticky='w')
        self.lbl100Offset = ttk.Label(master=frame100Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl100Offset.grid(row=1, column=1, sticky='e')
        lbl100TMark = ttk.Label(master=frame100Result, text="Total", font=self.font)
        lbl100TMark.grid(row=2, column=0, sticky='w')
        self.lbl100Total = ttk.Label(master=frame100Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl100Total.grid(row=2, column=1, sticky='e')

        lbl20Marker = ttk.Label(master=frame20Result, text="Roll:", font=self.font)
        lbl20Marker.grid(row=0, column=0, sticky='w')
        self.lbl20Result = ttk.Label(master=frame20Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl20Result.grid(row=0, column=1, sticky='e')
        lbl20OMark = ttk.Label(master=frame20Result, text="Mod:", font=self.font)
        lbl20OMark.grid(row=1, column=0, sticky='w')
        self.lbl20Offset = ttk.Label(master=frame20Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl20Offset.grid(row=1, column=1, sticky='e')
        lbl20TMark = ttk.Label(master=frame20Result, text="Total", font=self.font)
        lbl20TMark.grid(row=2, column=0, sticky='w')
        self.lbl20Total = ttk.Label(master=frame20Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl20Total.grid(row=2, column=1, sticky='e')

        lbl12Marker = ttk.Label(master=frame12Result, text="Roll:", font=self.font)
        lbl12Marker.grid(row=0, column=0, sticky='w')
        self.lbl12Result = ttk.Label(master=frame12Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl12Result.grid(row=0, column=1, sticky='e')
        lbl12OMark = ttk.Label(master=frame12Result, text="Mod:", font=self.font)
        lbl12OMark.grid(row=1, column=0, sticky='w')
        self.lbl12Offset = ttk.Label(master=frame12Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl12Offset.grid(row=1, column=1, sticky='e')
        lbl12TMark = ttk.Label(master=frame12Result, text="Total", font=self.font)
        lbl12TMark.grid(row=2, column=0, sticky='w')
        self.lbl12Total = ttk.Label(master=frame12Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl12Total.grid(row=2, column=1, sticky='e')

        lbl10Marker = ttk.Label(master=frame10Result, text="Roll:", font=self.font)
        lbl10Marker.grid(row=0, column=0, sticky='w')
        self.lbl10Result = ttk.Label(master=frame10Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl10Result.grid(row=0, column=1, sticky='e')
        lbl10OMark = ttk.Label(master=frame10Result, text="Mod:", font=self.font)
        lbl10OMark.grid(row=1, column=0, sticky='w')
        self.lbl10Offset = ttk.Label(master=frame10Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl10Offset.grid(row=1, column=1, sticky='e')
        lbl10TMark = ttk.Label(master=frame10Result, text="Total", font=self.font)
        lbl10TMark.grid(row=2, column=0, sticky='w')
        self.lbl10Total = ttk.Label(master=frame10Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl10Total.grid(row=2, column=1, sticky='e')

        lbl8Marker = ttk.Label(master=frame8Result, text="Roll:", font=self.font)
        lbl8Marker.grid(row=0, column=0, sticky='w')
        self.lbl8Result = ttk.Label(master=frame8Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl8Result.grid(row=0, column=1, sticky='e')
        lbl8OMark = ttk.Label(master=frame8Result, text="Mod:", font=self.font)
        lbl8OMark.grid(row=1, column=0, sticky='w')
        self.lbl8Offset = ttk.Label(master=frame8Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl8Offset.grid(row=1, column=1, sticky='e')
        lbl8TMark = ttk.Label(master=frame8Result, text="Total", font=self.font)
        lbl8TMark.grid(row=2, column=0, sticky='w')
        self.lbl8Total = ttk.Label(master=frame8Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl8Total.grid(row=2, column=1, sticky='e')

        lbl6Marker = ttk.Label(master=frame6Result, text="Roll:", font=self.font)
        lbl6Marker.grid(row=0, column=0, sticky='w')
        self.lbl6Result = ttk.Label(master=frame6Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl6Result.grid(row=0, column=1, sticky='e')
        lbl6OMark = ttk.Label(master=frame6Result, text="Mod:", font=self.font)
        lbl6OMark.grid(row=1, column=0, sticky='w')
        self.lbl6Offset = ttk.Label(master=frame6Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl6Offset.grid(row=1, column=1, sticky='e')
        lbl6TMark = ttk.Label(master=frame6Result, text="Total", font=self.font)
        lbl6TMark.grid(row=2, column=0, sticky='w')
        self.lbl6Total = ttk.Label(master=frame6Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl6Total.grid(row=2, column=1, sticky='e')

        lbl4Marker = ttk.Label(master=frame4Result, text="Roll:", font=self.font)
        lbl4Marker.grid(row=0, column=0, sticky='w')
        self.lbl4Result = ttk.Label(master=frame4Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl4Result.grid(row=0, column=1, sticky='e')
        lbl4OMark = ttk.Label(master=frame4Result, text="Mod:", font=self.font)
        lbl4OMark.grid(row=1, column=0, sticky='w')
        self.lbl4Offset = ttk.Label(master=frame4Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl4Offset.grid(row=1, column=1, sticky='e')
        lbl4TMark = ttk.Label(master=frame4Result, text="Total", font=self.font)
        lbl4TMark.grid(row=2, column=0, sticky='w')
        self.lbl4Total = ttk.Label(master=frame4Result, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lbl4Total.grid(row=2, column=1, sticky='e')

        lblCoinMarker = ttk.Label(master=frameCoinResult, text="Roll:", font=self.font)
        lblCoinMarker.grid(row=0, column=0, sticky='w')
        self.lblCoinResult = ttk.Label(master=frameCoinResult, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lblCoinResult.grid(row=0, column=1, sticky='e')
        lblCoinOMark = ttk.Label(master=frameCoinResult, text="Mod:", font=self.font)
        lblCoinOMark.grid(row=1, column=0, sticky='w')
        self.lblCoinOffset = ttk.Label(master=frameCoinResult, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lblCoinOffset.grid(row=1, column=1, sticky='e')
        lblCoinTMark = ttk.Label(master=frameCoinResult, text="Total", font=self.font)
        lblCoinTMark.grid(row=2, column=0, sticky='w')
        self.lblCoinTotal = ttk.Label(master=frameCoinResult, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lblCoinTotal.grid(row=2, column=1, sticky='e')

        lblNetMarker = ttk.Label(master=resultFrame, text="Net Total", font=self.font)
        lblNetMarker.grid(row=1, column=0, columnspan=8)
        self.lblNetTotal = ttk.Label(master=resultFrame, text="0", font=self.font, borderwidth=1, relief=tk.RAISED, width=3, anchor='e')
        self.lblNetTotal.grid(row=2, column=0, columnspan=8)
        btnCalcNet = ttk.Button(master=resultFrame, text="Calculate Total", command=self.calcNet)
        
    def modifyMod(self, die, dir):
        pass

    def modifyNum(self, die, dir):
        pass

    def rollWinBtn(self, die):
        pass

    def calcNet(self):
        pass
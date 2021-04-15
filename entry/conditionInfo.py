import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedStyle

def explainConditions(root):
    regFont = ('Papyrus', '12')
    bigFont = ('Papyrus', '16')
    titleFont = ('Papyrus', '18')
    condWin = tk.Toplevel(master=root)
    condWin.title("Target Creature")
    style = ThemedStyle(condWin)
    style.theme_use("equilux")
    bg = style.lookup('TLabel', 'background')
    fg = style.lookup('TLabel', 'foreground')
    condWin.configure(bg=style.lookup('TLabel', 'background'))
    infoFrame = ttk.Frame(master=condWin)
    infoFrame.pack(side='left', pady=15, padx=15)
    infoFrame.columnconfigure([0,1], weight=1)
    infoFrame.rowconfigure([0,1,2], weight=1)
    vertScroll = ttk.Scrollbar(master=infoFrame)
    vertScroll.grid(row=1, column=3, rowspan=29)
    lblTitle = ttk.Label(master=infoFrame, text="Conditions Explained", font=titleFont)
    lblTitle.grid(row=0, column=0, columnspan=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=1, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=2, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=3, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=4, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=5, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=6, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=7, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=8, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=9, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=10, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=11, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=12, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=13, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=14, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=15, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=16, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=17, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=18, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=19, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=20, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=21, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=22, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=23, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=24, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=25, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=26, column=2, sticky='w')
    lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=bigFont)
    lblBlind.grid(row=27, column=1, sticky='w')
    lblBlindInfo = ttk.Label(
        master=infoFrame,
        text="\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.",
        font=regFont
        )
    lblBlindInfo.grid(row=28, column=2, sticky='w')
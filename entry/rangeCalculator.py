import math
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle


class RangeCalculator:
    def __init__(self, win = None):
        self.win = win
        self.radValue = ""
        self.stats = {}

    def generateWindow(self):
        rangeWin = tk.Toplevel(master=self.win)
        rangeWin.title("Range Calculator")
        style = ThemedStyle(rangeWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        rangeWin.configure(bg=style.lookup('TLabel', 'background'))
        upperFrame = ttk.Frame(master=rangeWin)
        lowerFrame = ttk.Frame(master=rangeWin)
        underFrame = ttk.Frame(master=rangeWin)

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

        lblName = ttk.Label(master=frame1_1, text="Name")
        entName = ttk.Entry(master=frame1_1, width=10)
        lblName.grid(row=0, column=0, sticky="w")
        entName.grid(row=0, column=1, sticky="e")

        lblHP = ttk.Label(master=frame1_2, text="HP")
        entHP = ttk.Entry(master=frame1_2, width=8)
        lblHP.grid(row=0, column=0, sticky="w")
        entHP.grid(row=0, column=1, sticky="e")

        lblCoord = ttk.Label(master=frame2_1, text="Coordinate")
        entXCoord = ttk.Entry(master=frame2_1, width=2)
        lblX = ttk.Label(master=frame2_1, text="X")
        entYCoord = ttk.Entry(master=frame2_1, width=2)
        lblY = ttk.Label(master=frame2_1, text="Y")
        entZCoord = ttk.Entry(master=frame2_1, width=2)
        lblZ = ttk.Label(master=frame2_1, text="Z")
        lblCoord.grid(row=0, column=0, sticky="w")
        entXCoord.grid(row=0, column=1, sticky="e")
        lblX.grid(row=0, column=2, sticky="e")
        entYCoord.grid(row=0, column=3, sticky="e")
        lblY.grid(row=0, column=4, sticky="e")
        entZCoord.grid(row=0, column=5, sticky="e")
        lblZ.grid(row=0, column=6, sticky="e")

        lblHeight = ttk.Label(master=frame2_2, text="Height (Blocks)")
        entHeight = ttk.Entry(master=frame2_2, width=8)
        lblHeight.grid(row=0, column=0, sticky="w")
        entHeight.grid(row=0, column=1, sticky="e")

        frameSizeLeft = ttk.Frame(master=frame3_1)
        frameSizeRight = ttk.Frame(master=frame3_1)
        lblSize = ttk.Label(master=frame3_1, text="Size Class")
        rbnTiny = ttk.Radiobutton(master=frameSizeLeft, text="Tiny", variable= self.radValue, value="Tiny")
        rbnSmall = ttk.Radiobutton(master=frameSizeRight, text="Small", variable= self.radValue, value="Small")
        rbnMedium = ttk.Radiobutton(master=frameSizeLeft, text="Medium", variable= self.radValue, value="Medium")
        rbnLarge = ttk.Radiobutton(master=frameSizeRight, text="Large", variable= self.radValue, value="Large")
        rbnHuge = ttk.Radiobutton(master=frameSizeLeft, text="Huge", variable= self.radValue, value="Huge")
        rbnGargantuan = ttk.Radiobutton(master=frameSizeRight, text="Gargantuan", variable= self.radValue, value="Gargantuan")
        lblSize.grid(row=0, column=0)
        frameSizeLeft.grid(row=1, column=0)
        frameSizeRight.grid(row=1, column=1)
        rbnTiny.grid(row=0, column=0, sticky="w")
        rbnSmall.grid(row=0, column=0, sticky="w")
        rbnMedium.grid(row=1, column=0, sticky="w")
        rbnLarge.grid(row=1, column=0, sticky="w")
        rbnHuge.grid(row=2, column=0, sticky="w")
        rbnGargantuan.grid(row=2, column=0, sticky="w")

        lblNotes = ttk.Label(master=lowerFrame, text="Notes")
        txtNotes = tk.Text(master=lowerFrame)
        lblNotes.grid(row=0, column=0)
        txtNotes.grid(row=1, column=0, sticky="w")

        btnSubmit = ttk.Button(master=underFrame, command=rangeWin.destroy, text="Submit")
        btnSubmit.grid(row=0, column=0)

    def collectStats(self):
        stats = {
            "name": self.entName.get(),
            "hP": self.entHP.get(),
            "coordinate": [self.entXCoord.get(), self.entYCoord.get(), self.entZCoord.get()],
            "height": self.entHeight.get(),
            "size": self.radValue,
            "notes": self.txtNotes.get(1.0, tk.END)
        }
    
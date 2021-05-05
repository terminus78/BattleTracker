import pathlib
import json
import os
import math
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from dice import DiceRoller

class Press():
    def __init__(self, root):
        self.root = root
        self.reg_font = ('Papyrus', '14')
        self.small_font = ('Papyrus', '9')
        self.title_font = ('Papyrus', '18')

    def init_press(self):
        self.press_box = tk.Toplevel(self.root)
        self.press_box.title("Creature Generator")
        style = ThemedStyle(self.press_box)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.press_box.configure(bg=style.lookup('TLabel', 'background'))
        self.press_box.rowconfigure(0, minsize=50)
        self.press_box.rowconfigure(1, minsize=150)
        self.press_box.columnconfigure(0, minsize=600)
        self.build_frame = ttk.Frame(master=self.press_box, anchor='center')
        self.build_frame.grid(row=1, column=0)
        lbl_title = ttk.Label(master=self.press_box, text="Battle Forge", font=self.title_font, borderwidth=2, relief='ridge', anchor='center')
        lbl_title.grid(row=0, column=0, sticky='nsew')
        self.step_1()

    def step_1(self):
        self.build_frame.rowconfigure(1, minsize=100)
        lbl_step_1_description = ttk.Label(master=self.build_frame, text="Step 1: Select Type", font=self.reg_font)
        lbl_step_1_description.grid(row=0, column=0, columnspan=3)
        btn_pc = ttk.Button(master=self.build_frame, command=lambda: self.step_2('pc'), text="Player", width=12)
        btn_pc.grid(row=1, column=0, sticky='nsew', pady=30, padx=5)
        btn_npc = ttk.Button(master=self.build_frame, command=lambda: self.step_2('npc'), text="NPC", width=12)
        btn_npc.grid(row=1, column=1, sticky='nsew', pady=30, padx=5)
        btn_monster = ttk.Button(master=self.build_frame, command=lambda: self.step_2('monster'), text="Monster", width=10)
        btn_monster.grid(row=1, column=2, sticky='nsew', pady=30, padx=5)

    def step_2(self, type):
        old_widg = self.build_frame.grid_slaves()
        for widg in old_widg:
            widg.destroy()
        
        lbl_step_2_description = ttk.Label(master=self.build_frame, text="", font=self.reg_font)
        lbl_step_2_description.grid(row=0, column=0)

        if type == 'pc':
            lbl_step_2_description.config(text='Step 2: Choose race and stat input method')

        elif type == 'npc':
            lbl_step_2_description.config(text='Step 2: Select full or template')
        
        else:
            lbl_step_2_description.config(text='Step 2: Select monster')
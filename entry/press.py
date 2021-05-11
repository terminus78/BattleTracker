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
        self.template_loc = 'entry\\bin\\template_library.json'
        self.class_loc = 'entry\\bin\\class_lib.json'
        self.race_loc = 'entry\\bin\\race_lib.json'
        self.bkgd_loc = 'entry\\bin\\background_lib.json'
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
        self.build_frame = ttk.Frame(master=self.press_box)
        self.build_frame.grid(row=1, column=0, padx=10, pady=10)
        lbl_title = ttk.Label(master=self.press_box, text="Battle Forge", font=self.title_font, borderwidth=2, relief='ridge', anchor='center')
        lbl_title.grid(row=0, column=0, sticky='nsew')
        self.start()

    def start(self):
        self.build_frame.rowconfigure(1, minsize=100)
        lbl_step_1_description = ttk.Label(master=self.build_frame, text="Select Type", font=self.reg_font)
        lbl_step_1_description.grid(row=0, column=0, columnspan=3)
        btn_pc = ttk.Button(master=self.build_frame, command=lambda: self.fork('full'), text="Full Character", width=13)
        btn_pc.grid(row=1, column=0, sticky='nsew', pady=30, padx=5)
        btn_npc = ttk.Button(master=self.build_frame, command=lambda: self.fork('fast'), text="Fast NPC", width=13)
        btn_npc.grid(row=1, column=1, sticky='nsew', pady=30, padx=5)
        btn_monster = ttk.Button(master=self.build_frame, command=lambda: self.fork('monster'), text="Monster", width=13)
        btn_monster.grid(row=1, column=2, sticky='nsew', pady=30, padx=5)

    def fork(self, type):
        if type == 'fast' or type == 'monster':
            if os.path.exists(self.template_loc) == False:
                messagebox.showerror("Forge", "Missing template library. Please use the template builder to generate usable templates.")
                return
            with open(self.template_loc, 'r') as template_file:
                self.template_lib = json.load(template_file)
        old_widg = self.build_frame.grid_slaves()
        for widg in old_widg:
            widg.destroy()
        self.build_frame.rowconfigure(1, minsize=0)
        
        if type == 'full':
            self.full_build()

        else:
            self.template_build(type)

    def full_build(self):
        try:
            with open(self.class_loc, 'r') as class_file:
                self.class_lib = json.load(class_file)
        except IOError:
            messagebox.showerror("Forge", "Fatal error\nError 0x007")
            return
        try:
            with open(self.race_loc, 'r') as race_file:
                self.race_lib = json.load(race_file)
        except IOError:
            messagebox.showerror("Forge", "Fatal error\nError 0x008")
            return
        try:
            with open(self.bkgd_loc, 'r') as bkgd_file:
                self.bkgd_lib = json.load(bkgd_file)
        except IOError:
            messagebox.showerror("Forge", "Fatal error\nError 0x008")
            return
        self.races = []
        self.subraces = []
        self.classes = []
        self.backgrounds = []
        for race in self.race_lib.keys():
            self.races.append(race)
        for class_single in self.class_lib.keys():
            self.classes.append(class_single)
        for bkgd in self.bkgd_lib.keys():
            self.backgrounds.append(bkgd)
        lbl_choice_1 = ttk.Label(master=self.build_frame, text="Choose your race, background, and class.", font=self.reg_font)
        lbl_choice_1.grid(row=0, column=0)
        lbl_race = ttk.Label(master=self.build_frame, text="Race: ", font=self.reg_font)
        lbl_race.grid(row=1, column=0, sticky='w')
        self.cbox_race = ttk.Combobox(master=self.build_frame, values=self.races, state='readonly')
        self.cbox_race.grid(row=1, column=1, sticky='w')
        self.cbox_race.bind("<<ComboboxSelected>>", self._on_select_race)
        lbl_subrace = ttk.Label(master=self.build_frame, text="Subrace: ", font=self.reg_font)
        lbl_subrace.grid(row=2, column=0, sticky='w')
        self.cbox_subrace = ttk.Combobox(master=self.build_frame, values=self.subraces, state='readonly')
        self.cbox_subrace.grid(row=2, column=1, sticky='w')
        lbl_bkgd = ttk.Label(master=self.build_frame, text="Background: ", font=self.reg_font)
        lbl_bkgd.grid(row=3, column=0, sticky='w')
        self.cbox_bkgd = ttk.Combobox(master=self.build_frame, values=self.backgrounds, state='readonly')
        self.cbox_bkgd.grid(row=3, column=1, sticky='w')

    def template_build(self, type):
        pass

    def _on_select_race(self, event):
        select_race = self.cbox_race.get()
        if len(self.race_lib[select_race]['subrace']) > 0:
            for subrace in self.race_lib[select_race]['subrace']:
                self.subraces.append(subrace)
        else:
            self.subraces = []
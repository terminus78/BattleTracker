import json
import os
import math

import PIL.Image
from PIL import ImageTk
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
        stat_box_path = 'entry\\bin\\frame.png'
        self.stat_box = ImageTk.PhotoImage(image=PIL.Image.open(stat_box_path).resize((40,40)))
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
        self.dice = DiceRoller()
        self.start()

    def start(self, rtrn=False):
        if rtrn:
            self.clear_build_frame()
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
        self.clear_build_frame()
        self.build_frame.rowconfigure(1, minsize=0)
        
        if type == 'full':
            self.full_build_1()

        else:
            self.template_build(type)

    def full_build_1(self):
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
        lbl_choice = ttk.Label(master=self.build_frame, text="Choose your race, background, and class.", font=self.reg_font)
        lbl_choice.grid(row=0, column=0, columnspan=3)
        lbl_race = ttk.Label(master=self.build_frame, text="Race: ", font=self.reg_font)
        lbl_race.grid(row=1, column=0, sticky='w')
        self.cbox_race = ttk.Combobox(master=self.build_frame, values=self.races, state='readonly')
        self.cbox_race.grid(row=1, column=1, sticky='w')
        self.cbox_race.bind("<<ComboboxSelected>>", self._on_select_race)
        self.lbl_race_ben = ttk.Label(master=self.build_frame, text="", font=self.small_font)
        self.lbl_race_ben.grid(row=1, column=2, sticky='w')
        lbl_subrace = ttk.Label(master=self.build_frame, text="Subrace: ", font=self.reg_font)
        lbl_subrace.grid(row=2, column=0, sticky='w')
        self.cbox_subrace = ttk.Combobox(master=self.build_frame, values=self.subraces, state='readonly')
        self.cbox_subrace.grid(row=2, column=1, sticky='w')
        self.cbox_subrace.bind("<<ComboboxSelected>>", self._on_select_subrace)
        self.lbl_subrace_ben = ttk.Label(master=self.build_frame, text="", font=self.small_font)
        self.lbl_subrace_ben.grid(row=2, column=2, sticky='w')
        lbl_class = ttk.Label(master=self.build_frame, text="Class: ", font=self.reg_font)
        lbl_class.grid(row=3, column=0, sticky='w')
        self.cbox_class = ttk.Combobox(master=self.build_frame, values=self.classes, state='readonly')
        self.cbox_class.grid(row=3, column=1, sticky='w')
        self.cbox_class.bind("<<ComboboxSelected>>", self._on_select_class)
        self.lbl_class_desc = ttk.Label(master=self.build_frame, text="", font=self.small_font)
        self.lbl_class_desc.grid(row=3, column=2, sticky='w')
        lbl_bkgd = ttk.Label(master=self.build_frame, text="Background: ", font=self.reg_font)
        lbl_bkgd.grid(row=4, column=0, sticky='w')
        self.cbox_bkgd = ttk.Combobox(master=self.build_frame, values=self.backgrounds, state='readonly')
        self.cbox_bkgd.grid(row=4, column=1, sticky='w')
        self.cbox_bkgd.bind("<<ComboboxSelected>>", self._on_select_bkgd)
        self.lbl_bkgd_ben = ttk.Label(master=self.build_frame, text="", font=self.small_font)
        self.lbl_bkgd_ben.grid(row=4, column=2, sticky='w')

        temp_btn_frame = ttk.Frame(master=self.build_frame)
        temp_btn_frame.grid(row=5, column=0, columnspan=3, pady=10)
        btn_continue = ttk.Button(master=temp_btn_frame, command=self.full_build_2a, text="Next", width=13)
        btn_continue.grid(row=0, column=0, padx=5)
        btn_cancel = ttk.Button(master=temp_btn_frame, command=lambda: self.start(True), text="Previous", width=13)
        btn_cancel.grid(row=0, column=1, padx=5)

    def full_build_2a(self, rtrn=False):
        if rtrn == False:
            self.sel_race = self.cbox_race.get()
            self.sel_sub = self.cbox_subrace.get()
            self.sel_class = self.cbox_class.get()
            self.sel_bkgd = self.cbox_bkgd.get()
            if self.sel_race == "" or self.sel_class == "" or self.sel_bkgd == "" or (self.sel_sub == "" and len(self.subraces) > 0):
                messagebox.showwarning("Forge", "Must select all applicable fields.")
                return
        self.clear_build_frame()

        lbl_input_method = ttk.Label(master=self.build_frame, text="Choose stat input method.", font=self.reg_font)
        lbl_input_method.grid(row=0, column=0, columnspan=4)
        btn_roll = ttk.Button(master=self.build_frame, command=lambda: self.full_build_2b('roll'), text="Roll", width=13)
        btn_roll.grid(row=1, column=0, padx=5, pady=5)
        btn_point_buy = ttk.Button(master=self.build_frame, command=lambda: self.full_build_2b('point'), text="Point Buy", width=13)
        btn_point_buy.grid(row=1, column=1, padx=5, pady=5)
        btn_standard = ttk.Button(master=self.build_frame, command=lambda: self.full_build_2b('standard'), text="Standard", width=13)
        btn_standard.grid(row=1, column=2, padx=5, pady=5)
        btn_custom = ttk.Button(master=self.build_frame, command=lambda: self.full_build_2b('custom'), text="Custom", width=13)
        btn_custom.grid(row=1, column=3, padx=5, pady=5)

    def full_build_2b(self, sel_in):
        self.clear_build_frame()
        lbl_input_title = ttk.Label(master=self.build_frame, text="", font=self.reg_font)
        lbl_input_title.grid(row=0, column=0, columnspan=2)
        for i in range(1, 7):
            lbl_stat_frame = tk.Label(master=self.build_frame, image=self.stat_box, bg='gray28')
            lbl_stat_frame.grid(row=i, column=0, pady=5)
            lbl_stat_frame.image=self.stat_box
        self.stat_block = []
        for i in range(6):
            lbl_stat = tk.Label(master=self.build_frame, text="8", font=self.reg_font, anchor='center', bg='gray28', fg='white')
            lbl_stat.grid(row=i+1, column=0)
            self.stat_block.append(lbl_stat)

        if sel_in == 'roll':
            self.roll_labels = []
            for i in range(1, 7):
                lbl_rolls = ttk.Label(master=self.build_frame, text="", font=self.small_font, width=17)
                lbl_rolls.grid(row=i, column=1, sticky='w')
                self.roll_labels.append(lbl_rolls)
            self.dice_per_roll = tk.IntVar()
            under_frame = ttk.Frame(master=self.build_frame)
            under_frame.grid(row=8, column=0, columnspan=2)
            rbn_4d6 = ttk.Radiobutton(master=under_frame, text="4d6", variable=self.dice_per_roll, value=4)
            rbn_4d6.grid(row=0, column=0, padx=5)
            rbn_3d6 = ttk.Radiobutton(master=under_frame, text="3d6", variable=self.dice_per_roll, value=3)
            rbn_3d6.grid(row=0, column=1, padx=5)
            self.dice_per_roll.set(4)
            btn_roll = ttk.Button(master=under_frame, command=self.roll_stats, text="Roll", width=13)
            btn_roll.grid(row=1, column=0, columnspan=2)
        btn_frame = ttk.Frame(master=self.build_frame)
        btn_frame.grid(row=9, column=0, columnspan=2)
        self.btn_next = ttk.Button(master=btn_frame, command=self.full_build_3, text="Next", width=13)
        self.btn_next.grid(row=0, column=0, padx=5)
        self.btn_next.state(['disabled'])
        btn_prev = ttk.Button(master=btn_frame, command=lambda: self.full_build_2a(True), text="Previous", width=13)
        btn_prev.grid(row=0, column=1, padx=5)

    def full_build_3(self):
        pass

    def template_build(self, type):
        pass

    def clear_build_frame(self):
        old_widg = self.build_frame.grid_slaves()
        for widg in old_widg:
            widg.destroy()

    def roll_stats(self):
        self.btn_next.state(['!disabled'])
        dpr = self.dice_per_roll.get()
        self.set_1 = self.dice.roll(die_size=6, num_dice=dpr)
        self.set_2 = self.dice.roll(die_size=6, num_dice=dpr)
        self.set_3 = self.dice.roll(die_size=6, num_dice=dpr)
        self.set_4 = self.dice.roll(die_size=6, num_dice=dpr)
        self.set_5 = self.dice.roll(die_size=6, num_dice=dpr)
        self.set_6 = self.dice.roll(die_size=6, num_dice=dpr)
        mid_1 = self.set_1
        mid_2 = self.set_2
        mid_3 = self.set_3
        mid_4 = self.set_4
        mid_5 = self.set_5
        mid_6 = self.set_6
        if dpr == 4:
            mid_1.pop(mid_1.index(min(mid_1)))
            mid_2.pop(mid_2.index(min(mid_2)))
            mid_3.pop(mid_3.index(min(mid_3)))
            mid_4.pop(mid_4.index(min(mid_4)))
            mid_5.pop(mid_5.index(min(mid_5)))
            mid_6.pop(mid_6.index(min(mid_6)))
        mid_sums = [
            mid_1,
            mid_2,
            mid_3,
            mid_4,
            mid_5,
            mid_6
        ]
        set_list = [self.set_1, self.set_2, self.set_3, self.set_4, self.set_5, self.set_6]
        for i in range(6):
            total = 0
            roll_add = ""
            for j in range(6):
                total += mid_sums[i][j]
                roll_add += f"{set_list[i][j]}, "
            roll_add = roll_add[:-2]
            self.roll_labels[i].config(text=roll_add)
            self.stat_block[i].config(text=total)

    # Events
    def _on_select_race(self, event):
        select_race = self.cbox_race.get()
        if len(self.race_lib[select_race]['subrace']) > 0:
            for subrace in self.race_lib[select_race]['subrace']:
                self.subraces.append(subrace)
        else:
            self.subraces = []
        stat_order = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
        benefit = ""
        for i in range(len(self.race_lib[select_race]['stat_bonus'])):
            if self.race_lib[select_race]['stat_bonus'][i] != 0:
                benefit += f"{self.race_lib[select_race]['stat_bonus'][i]} {stat_order[i]}, "
        benefit = benefit[:-2]
        self.lbl_race_ben.config(text=benefit)

    def _on_select_subrace(self, event):
        select_sub = self.cbox_subrace.get()
        select_race = self.cbox_race.get()
        if select_race == "":
            return
        stat_order = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
        benefit = ""
        for i in range(len(self.race_lib[select_race][select_sub]['stat_bonus'])):
            if self.race_lib[select_race][select_sub]['stat_bonus'][i] != 0:
                benefit += f"{self.race_lib[select_race][select_sub]['stat_bonus'][i]} {stat_order[i]}, "
        benefit = benefit[:-2]
        self.lbl_subrace_ben.config(text=benefit)

    def _on_select_class(self, event):
        select_class = self.cbox_class.get()
        self.lbl_class_desc.config(text=self.class_lib[select_class]['base']['desc'])

    def _on_select_bkgd(self, event):
        select_bkgd = self.cbox_bkgd.get()
        skill_string = ""
        for skill in self.bkgd_lib[select_bkgd]['skills']:
            skill_string += f"{skill.title()}, "
        skill_string = skill_string[:-2]
        self.lbl_bkgd_ben.config(text=skill_string)
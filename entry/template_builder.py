import pathlib
import json
import os
import math
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk,font,messagebox
from ttkthemes import ThemedStyle
import PIL.Image
from PIL import ImageTk


'''
root = tk.Tk()
root.title("Template Builder")
root_width = root.winfo_reqwidth()
root_height = root.winfo_reqheight()
position_horizontal = int(root.winfo_screenwidth()/2 - root_width/2)
position_vertical = int(root.winfo_screenheight()/2 - root_height/2)
root.geometry("+{}+{}".format(position_horizontal, position_vertical))
'''

class TemplateBuilder():
    def __init__(self, root):
        self.root = root
        self.file_loc = 'entry\\bin\\template_library.json'
        catg_frame = ttk.Frame(master=self.root)
        catg_frame.grid(row=0, column=0)
        self.input_frame = ttk.Frame(master=self.root)
        self.input_frame.grid(row=1, column=0)
        self.send_it_frame = ttk.Frame(master=self.root)
        self.send_it_frame.grid(row=2, column=0)
        btn_npc = ttk.Button(master=catg_frame, command=lambda: self.build_form('npc'), text="Fast NPC")
        btn_npc.grid(row=0, column=0, sticky='w', padx=5, pady=10)
        btn_monster = ttk.Button(master=catg_frame, command=lambda: self.build_form('monster'), text="Monster")
        btn_monster.grid(row=0, column=1, sticky='w', padx=5, pady=10)
        lbl_waiting = ttk.Label(master=self.input_frame, text="Waiting...").grid(row=0, column=0)
        on_img_path = 'entry\\bin\\on.png'
        self.on_img = ImageTk.PhotoImage(image=PIL.Image.open(on_img_path))
        off_img_path = 'entry\\bin\\off.png'
        self.off_img = ImageTk.PhotoImage(image=PIL.Image.open(off_img_path))

    def build_form(self, catg):
        try:
            old_widg = self.input_frame.grid_slaves()
            if old_widg is not None:
                for widg in old_widg:
                    widg.destroy()
        except AttributeError:
            pass

        lbl_catg = ttk.Label(master=self.input_frame, text="")
        lbl_catg.grid(row=0, column=0, sticky='w')
        underline_font = font.Font(lbl_catg, lbl_catg.cget("font"))
        underline_font.configure(underline = True)
        lbl_catg.config(font=underline_font)
        if catg == 'npc':
            lbl_catg.config(text='NPC')
        else:
            lbl_catg.config(text="Monster")
        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=1, column=0, sticky='w')
        self.ent_name = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name.grid(row=1, column=1, sticky='w')
        lbl_type = ttk.Label(master=self.input_frame, text="Type: ")
        lbl_type.grid(row=2, column=0, sticky='w')
        self.ent_type = ttk.Entry(master=self.input_frame, width=20)
        self.ent_type.grid(row=2, column=1, sticky='w')
        lbl_size = ttk.Label(master=self.input_frame, text="Size: ")
        lbl_size.grid(row=3, column=0, sticky='w')
        self.size = tk.StringVar()
        size_frame = ttk.Frame(master=self.input_frame)
        size_frame.grid(row=3, column=1, sticky='w')
        rbn_tiny = ttk.Radiobutton(master=size_frame, text="tiny", variable=self.size, value='tiny')
        rbn_tiny.grid(row=0, column=0, sticky='w')
        rbn_small = ttk.Radiobutton(master=size_frame, text="small", variable=self.size, value='small')
        rbn_small.grid(row=0, column=1, sticky='w')
        rbn_medium = ttk.Radiobutton(master=size_frame, text="medium", variable=self.size, value='medium')
        rbn_medium.grid(row=1, column=0, sticky='w')
        rbn_large = ttk.Radiobutton(master=size_frame, text="large", variable=self.size, value='large')
        rbn_large.grid(row=1, column=1, sticky='w')
        rbn_huge = ttk.Radiobutton(master=size_frame, text="huge", variable=self.size, value='huge')
        rbn_huge.grid(row=2, column=0, sticky='w')
        rbn_gargantuan = ttk.Radiobutton(master=size_frame, text="garg", variable=self.size, value='gargantuan')
        rbn_gargantuan.grid(row=2, column=1, sticky='w')
        self.size.set("medium")
        lbl_ac = ttk.Label(master=self.input_frame, text="AC: ")
        lbl_ac.grid(row=4, column=0, sticky='w')
        self.ent_ac = ttk.Entry(master=self.input_frame, width=20)
        self.ent_ac.grid(row=4, column=1, sticky='w')
        self.ent_ac.insert(0, "14")
        lbl_hp_avg = ttk.Label(master=self.input_frame, text="Average HP")
        lbl_hp_avg.grid(row=5, column=0, sticky='w')
        self.ent_hp_avg = ttk.Entry(master=self.input_frame, width=20)
        self.ent_hp_avg.grid(row=5, column=1, sticky='w')
        lbl_hp_dice = ttk.Label(master=self.input_frame, text="HP Dice")
        lbl_hp_dice.grid(row=6, column=0, sticky='w')
        hp_dice_frame = ttk.Frame(master=self.input_frame)
        hp_dice_frame.grid(row=6, column=1, sticky='w')
        self.ent_num_hp_dice = ttk.Entry(master=hp_dice_frame, width=5)
        self.ent_num_hp_dice.grid(row=0, column=0, sticky='w')
        lbl_d = ttk.Label(master=hp_dice_frame, text="d")
        lbl_d.grid(row=0, column=1, sticky='w', padx=2)
        self.ent_hp_die = ttk.Entry(master=hp_dice_frame, width=5)
        self.ent_hp_die.grid(row=0, column=2, sticky='w')
        lbl_mod_hp = ttk.Label(master=hp_dice_frame, text='Mod:')
        lbl_mod_hp.grid(row=0, column=3, sticky='w', padx=2)
        self.ent_mod_hp = ttk.Entry(master=hp_dice_frame, width=5)
        self.ent_mod_hp.grid(row=0, column=4, sticky='w')
        lbl_speed = ttk.Label(master=self.input_frame, text="Speed: ")
        lbl_speed.grid(row=7, column=0, sticky='w')
        self.ent_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_speed.grid(row=7, column=1, sticky='w')
        self.ent_speed.insert(0, "30")
        lbl_stats = ttk.Label(master=self.input_frame, text="Stats: ")
        lbl_stats.grid(row=8, column=0, sticky='w')
        stat_frame = ttk.Frame(master=self.input_frame)
        stat_frame.grid(row=8, column=1)
        lbl_str = ttk.Label(master=stat_frame, text="STR")
        lbl_str.grid(row=0, column=0)
        lbl_dex = ttk.Label(master=stat_frame, text="DEX")
        lbl_dex.grid(row=0, column=1)
        lbl_con = ttk.Label(master=stat_frame, text="CON")
        lbl_con.grid(row=0, column=2)
        self.ent_str = ttk.Entry(master=stat_frame, width=5)
        self.ent_str.grid(row=1, column=0)
        self.ent_dex = ttk.Entry(master=stat_frame, width=5)
        self.ent_dex.grid(row=1, column=1)
        self.ent_con = ttk.Entry(master=stat_frame, width=5)
        self.ent_con.grid(row=1, column=2)
        lbl_int = ttk.Label(master=stat_frame, text="INT")
        lbl_int.grid(row=2, column=0)
        lbl_wis = ttk.Label(master=stat_frame, text="WIS")
        lbl_wis.grid(row=2, column=1)
        lbl_cha = ttk.Label(master=stat_frame, text="CHA")
        lbl_cha.grid(row=2, column=2)
        self.ent_int = ttk.Entry(master=stat_frame, width=5)
        self.ent_int.grid(row=3, column=0)
        self.ent_wis = ttk.Entry(master=stat_frame, width=5)
        self.ent_wis.grid(row=3, column=1)
        self.ent_cha = ttk.Entry(master=stat_frame, width=5)
        self.ent_cha.grid(row=3, column=2)

        lbl_skills = ttk.Label(master=self.input_frame, text="Proficient Skills: ")
        lbl_skills.grid(row=1, column=2, sticky='w')
        lbl_prof_1 = ttk.Label(master=self.input_frame, text="Prof", relief=tk.RIDGE)
        lbl_prof_1.grid(row=2, column=4, sticky='w')
        lbl_dbl_1 = ttk.Label(master=self.input_frame, text="Double", relief=tk.RIDGE)
        lbl_dbl_1.grid(row=2, column=3, sticky='w')
        lbl_prof_2 = ttk.Label(master=self.input_frame, text="Prof", relief=tk.RIDGE)
        lbl_prof_2.grid(row=2, column=6, sticky='w')
        lbl_dbl_2 = ttk.Label(master=self.input_frame, text="Double", relief=tk.RIDGE)
        lbl_dbl_2.grid(row=2, column=5, sticky='w')
        #lbl_skill_mod = ttk.Label(master=self.input_frame, text="Modifier: ")
        #lbl_skill_mod.grid(row=2, column=3, sticky='w')
        #self.ent_skill_mod = ttk.Entry(master=self.input_frame, width=5)
        #self.ent_skill_mod.grid(row=2, column=4, sticky='w')
        #self.ent_skill_mod.insert(0, "0")
        self.athletics = tk.IntVar()
        self.acrobatics = tk.IntVar()
        self.sleight_of_hand = tk.IntVar()
        self.stealth = tk.IntVar()
        self.arcana = tk.IntVar()
        self.history = tk.IntVar()
        self.investigation = tk.IntVar()
        self.nature = tk.IntVar()
        self.religion = tk.IntVar()
        self.animal_handling = tk.IntVar()
        self.insight = tk.IntVar()
        self.medicine = tk.IntVar()
        self.perception = tk.IntVar()
        self.survival = tk.IntVar()
        self.deception = tk.IntVar()
        self.intimidation = tk.IntVar()
        self.performance = tk.IntVar()
        self.persuasion = tk.IntVar()

        self.dbl_athletics = tk.IntVar()
        self.dbl_acrobatics = tk.IntVar()
        self.dbl_sleight_of_hand = tk.IntVar()
        self.dbl_stealth = tk.IntVar()
        self.dbl_arcana = tk.IntVar()
        self.dbl_history = tk.IntVar()
        self.dbl_investigation = tk.IntVar()
        self.dbl_nature = tk.IntVar()
        self.dbl_religion = tk.IntVar()
        self.dbl_animal_handling = tk.IntVar()
        self.dbl_insight = tk.IntVar()
        self.dbl_medicine = tk.IntVar()
        self.dbl_perception = tk.IntVar()
        self.dbl_survival = tk.IntVar()
        self.dbl_deception = tk.IntVar()
        self.dbl_intimidation = tk.IntVar()
        self.dbl_performance = tk.IntVar()
        self.dbl_persuasion = tk.IntVar()

        cbn_athletics = ttk.Checkbutton(master=self.input_frame, text="Athletics", variable=self.athletics)
        cbn_acrobatics = ttk.Checkbutton(master=self.input_frame, text="Acrobatics", variable=self.acrobatics)
        cbn_sleight_of_hand = ttk.Checkbutton(master=self.input_frame, text="Sleight of Hand", variable=self.sleight_of_hand)
        cbn_stealth = ttk.Checkbutton(master=self.input_frame, text="Stealth", variable=self.stealth)
        cbn_arcana = ttk.Checkbutton(master=self.input_frame, text="Arcana", variable=self.arcana)
        cbn_history = ttk.Checkbutton(master=self.input_frame, text="History", variable=self.history)
        cbn_investigation = ttk.Checkbutton(master=self.input_frame, text="Investigation", variable=self.investigation)
        cbn_nature = ttk.Checkbutton(master=self.input_frame, text="Nature", variable=self.nature)
        cbn_religion = ttk.Checkbutton(master=self.input_frame, text="Religion", variable=self.religion)
        cbn_animal_handling = ttk.Checkbutton(master=self.input_frame, text="Animal Handling", variable=self.animal_handling)
        cbn_insight = ttk.Checkbutton(master=self.input_frame, text="Insight", variable=self.insight)
        cbn_medicine = ttk.Checkbutton(master=self.input_frame, text="Medicine", variable=self.medicine)
        cbn_perception = ttk.Checkbutton(master=self.input_frame, text="Perception", variable=self.perception)
        cbn_survival = ttk.Checkbutton(master=self.input_frame, text="Survival", variable=self.survival)
        cbn_deception = ttk.Checkbutton(master=self.input_frame, text="Deception", variable=self.deception)
        cbn_intimidation = ttk.Checkbutton(master=self.input_frame, text="Intimidation", variable=self.intimidation)
        cbn_performance = ttk.Checkbutton(master=self.input_frame, text="Performance", variable=self.performance)
        cbn_persuasion = ttk.Checkbutton(master=self.input_frame, text="Persuasion", variable=self.persuasion)

        cbn_dbl_athletics = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_athletics)
        cbn_dbl_acrobatics = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_acrobatics)
        cbn_dbl_sleight_of_hand = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_sleight_of_hand)
        cbn_dbl_stealth = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_stealth)
        cbn_dbl_arcana = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_arcana)
        cbn_dbl_history = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_history)
        cbn_dbl_investigation = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_investigation)
        cbn_dbl_nature = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_nature)
        cbn_dbl_religion = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_religion)
        cbn_dbl_animal_handling = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_animal_handling)
        cbn_dbl_insight = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_insight)
        cbn_dbl_medicine = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_medicine)
        cbn_dbl_perception = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_perception)
        cbn_dbl_survival = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_survival)
        cbn_dbl_deception = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_deception)
        cbn_dbl_intimidation = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_intimidation)
        cbn_dbl_performance = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_performance)
        cbn_dbl_persuasion = ttk.Checkbutton(master=self.input_frame, variable=self.dbl_persuasion)
        
        cbn_athletics.grid(row=3, column=4, sticky='w')
        cbn_acrobatics.grid(row=3, column=6, sticky='w')
        cbn_sleight_of_hand.grid(row=4, column=4, sticky='w')
        cbn_stealth.grid(row=4, column=6, sticky='w')
        cbn_arcana.grid(row=5, column=4, sticky='w')
        cbn_history.grid(row=5, column=6, sticky='w')
        cbn_investigation.grid(row=6, column=4, sticky='w')
        cbn_nature.grid(row=6, column=6, sticky='w')
        cbn_religion.grid(row=7, column=4, sticky='w')
        cbn_animal_handling.grid(row=7, column=6, sticky='w')
        cbn_insight.grid(row=8, column=4, sticky='w')
        cbn_medicine.grid(row=8, column=6, sticky='w')
        cbn_perception.grid(row=9, column=4, sticky='w')
        cbn_survival.grid(row=9, column=6, sticky='w')
        cbn_deception.grid(row=10, column=4, sticky='w')
        cbn_intimidation.grid(row=10, column=6, sticky='w')
        cbn_performance.grid(row=11, column=4, sticky='w')
        cbn_persuasion.grid(row=11, column=6, sticky='w')

        cbn_dbl_athletics.grid(row=3, column=3, sticky='w')
        cbn_dbl_acrobatics.grid(row=3, column=5, sticky='w')
        cbn_dbl_sleight_of_hand.grid(row=4, column=3, sticky='w')
        cbn_dbl_stealth.grid(row=4, column=5, sticky='w')
        cbn_dbl_arcana.grid(row=5, column=3, sticky='w')
        cbn_dbl_history.grid(row=5, column=5, sticky='w')
        cbn_dbl_investigation.grid(row=6, column=3, sticky='w')
        cbn_dbl_nature.grid(row=6, column=5, sticky='w')
        cbn_dbl_religion.grid(row=7, column=3, sticky='w')
        cbn_dbl_animal_handling.grid(row=7, column=5, sticky='w')
        cbn_dbl_insight.grid(row=8, column=3, sticky='w')
        cbn_dbl_medicine.grid(row=8, column=5, sticky='w')
        cbn_dbl_perception.grid(row=9, column=3, sticky='w')
        cbn_dbl_survival.grid(row=9, column=5, sticky='w')
        cbn_dbl_deception.grid(row=10, column=3, sticky='w')
        cbn_dbl_intimidation.grid(row=10, column=5, sticky='w')
        cbn_dbl_performance.grid(row=11, column=3, sticky='w')
        cbn_dbl_persuasion.grid(row=11, column=5, sticky='w')

        lbl_senses = ttk.Label(master=self.input_frame, text="Senses: ")
        lbl_senses.grid(row=9, column=0, sticky='w')
        self.txt_senses = tk.Text(master=self.input_frame, height=4, width=30)
        self.txt_senses.grid(row=9, column=1, sticky='w')
        lbl_languages = ttk.Label(master=self.input_frame, text="Languages: ")
        lbl_languages.grid(row=10, column=0, sticky='w')
        self.txt_languages = tk.Text(master=self.input_frame, height=4, width=30)
        self.txt_languages.grid(row=10, column=1, sticky='w')
        lbl_cr = ttk.Label(master=self.input_frame, text="CR: ")
        lbl_cr.grid(row=11, column=0, sticky='w')
        self.ent_cr = ttk.Entry(master=self.input_frame, width=20)
        self.ent_cr.grid(row=11, column=1, sticky='w')
        self.ent_cr.insert(0, "1")
        
        lbl_look_ma = ttk.Label(master=self.input_frame, text="Combat: ")
        lbl_look_ma.grid(row=1, column=7, sticky='w')
        lbl_abilities = ttk.Label(master=self.input_frame, text="Abilities/Features: ")
        lbl_abilities.grid(row=2, column=7, sticky='nw')
        self.txt_abilities = tk.Text(master=self.input_frame, height=6)
        self.txt_abilities.grid(row=2, column=8, rowspan=4, sticky='nw')
        lbl_actions = ttk.Label(master=self.input_frame, text="Actions/Legendary Actions: ")
        lbl_actions.grid(row=4, column=7, sticky='nw')
        self.txt_actions = tk.Text(master=self.input_frame, height=6)
        self.txt_actions.grid(row=4, column=8, rowspan=4, sticky='nw')
        lbl_reactions = ttk.Label(master=self.input_frame, text="Reactions/Legendary Reactions: ")
        lbl_reactions.grid(row=8, column=7, sticky='nw')
        self.txt_reactions = tk.Text(master=self.input_frame, height=6)
        self.txt_reactions.grid(row=8, column=8, sticky='nw')

        lbl_mean_mode = ttk.Label(master=self.input_frame, text="Mean Mode")
        lbl_mean_mode.grid(row=10, column=8)
        self.btn_mean_mode = tk.Button(master=self.input_frame, image=self.off_img, bd=0, bg='gray28', activebackground='gray28', relief=tk.SUNKEN, command=self.on_off_switch)
        self.btn_mean_mode.grid(row=11, column=8)
        self.btn_mean_mode.image = self.off_img
        self.mean_mode = False
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_it, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def on_off_switch(self):
        if self.mean_mode:
            self.mean_mode = False
            self.btn_mean_mode.config(image=self.off_img)
            self.btn_mean_mode.image = self.off_img
        else:
            self.mean_mode = True
            self.btn_mean_mode.config(image=self.on_img)
            self.btn_mean_mode.image = self.on_img

    def send_it(self):
        get_name = self.ent_name.get()
        get_type = self.ent_type.get()
        get_size = self.size.get()
        get_ac = self.ent_ac.get()
        get_hp_avg = self.ent_hp_avg.get()
        get_hp_num_dice = self.ent_num_hp_dice.get()
        get_hp_die = self.ent_hp_die.get()
        get_mod_hp = self.ent_mod_hp.get()
        get_speed = self.ent_speed.get()
        get_str = self.ent_str.get()
        get_dex = self.ent_dex.get()
        get_con = self.ent_con.get()
        get_int = self.ent_int.get()
        get_wis = self.ent_wis.get()
        get_cha = self.ent_cha.get()
        get_senses = self.txt_senses.get(1.0, 'end-1c')
        get_lang = self.txt_languages.get(1.0, 'end-1c')
        get_cr = self.ent_cr.get()

        #get_skill_mod = self.ent_skill_mod.get()
        get_athl = self.athletics.get()
        get_acro = self.acrobatics.get()
        get_slgt = self.sleight_of_hand.get()
        get_stlh = self.stealth.get()
        get_arcn = self.arcana.get()
        get_hist = self.history.get()
        get_invs = self.investigation.get()
        get_natr = self.nature.get()
        get_relg = self.religion.get()
        get_anhn = self.animal_handling.get()
        get_insg = self.insight.get()
        get_medc = self.medicine.get()
        get_perc = self.perception.get()
        get_surv = self.survival.get()
        get_dect = self.deception.get()
        get_intm = self.intimidation.get()
        get_perf = self.performance.get()
        get_pers = self.persuasion.get()

        get_dbl_athl = self.dbl_athletics.get()
        get_dbl_acro = self.dbl_acrobatics.get()
        get_dbl_slgt = self.dbl_sleight_of_hand.get()
        get_dbl_stlh = self.dbl_stealth.get()
        get_dbl_arcn = self.dbl_arcana.get()
        get_dbl_hist = self.dbl_history.get()
        get_dbl_invs = self.dbl_investigation.get()
        get_dbl_natr = self.dbl_nature.get()
        get_dbl_relg = self.dbl_religion.get()
        get_dbl_anhn = self.dbl_animal_handling.get()
        get_dbl_insg = self.dbl_insight.get()
        get_dbl_medc = self.dbl_medicine.get()
        get_dbl_perc = self.dbl_perception.get()
        get_dbl_surv = self.dbl_survival.get()
        get_dbl_dect = self.dbl_deception.get()
        get_dbl_intm = self.dbl_intimidation.get()
        get_dbl_perf = self.dbl_performance.get()
        get_dbl_pers = self.dbl_persuasion.get()

        get_abil = self.txt_abilities.get(1.0, 'end-1c')
        get_actn = self.txt_actions.get(1.0, 'end-1c')
        get_reac = self.txt_reactions.get(1.0, 'end-1c')

        try:
            get_ac = int(get_ac)
            get_hp_avg = int(get_hp_avg)
            get_hp_num_dice = int(get_hp_num_dice)
            get_hp_die = int(get_hp_die)
            get_mod_hp = int(get_mod_hp)
            get_speed = int(get_speed)
            get_str = int(get_str)
            get_dex = int(get_dex)
            get_con = int(get_con)
            get_int = int(get_int)
            get_wis = int(get_wis)
            get_cha = int(get_cha)
            #get_skill_mod = int(get_cha)
        except ValueError:
            if self.mean_mode:
                messagebox.showwarning("Dumbass Alert", "Stop fuckin up the numbers and put the shit in right.")
                return
            else:
                messagebox.showwarning("Template Creator", "All value inputs must be whole numbers.")
                return
        
        if get_name == "" or get_type == "" or get_size == "" or get_senses == "" or get_lang == "" or get_cr == "" or get_actn == "":
            if self.mean_mode:
                messagebox.showwarning("Dumbass Alert", "Fill out all the fields dumbass.")
                return
            else:
                messagebox.showwarning("Template Creator", "All fields except Abilities and Reactions must be filled out.")
                return

        if get_hp_die != 100 and get_hp_die != 20 and get_hp_die != 12 and get_hp_die != 10 and get_hp_die != 8 and get_hp_die != 6 and get_hp_die != 4:
            if self.mean_mode:
                messagebox.showwarning("Dumbass Alert", "Pick a real fucking die.")
                return
            else:
                messagebox.showwarning("Template Creator", "HP Die value does not exist.")
                return

        if len(get_cr) < 3:
            try:
                get_cr = int(get_cr)
                if get_cr < 0:
                    if self.mean_mode:
                        messagebox.showwarning("Dumbass Alert", "Did you mean to put in your CR, cause it's negative?")
                        return
                    else:
                        messagebox.showwarning("Template Creator", "CR cannot be a negative value.")
                        return
            except ValueError:
                if self.mean_mode:
                    messagebox.showwarning("Dumbass Alert", "Can't even put in the damn CR correctly. Just give up.")
                    return
                else:
                    messagebox.showwarning("Template Creator", "CR must be a number.")
                    return
        else:
            if get_cr == "1/2":
                get_cr = 0.5
            elif get_cr == "1/4":
                get_cr = 0.25
            elif get_cr == "1/8":
                get_cr = 0.125
            else:
                if self.mean_mode:
                    messagebox.showwarning("Dumbass Alert", "Not an existing CR dumbass.")
                    return
                else:
                    messagebox.showwarning("Template Creator", "The only allowed CR values between 0 and 1 are 1/8, 1/4, and 1/2.")
                    return
        if get_cr == 0:
            cr_prof_mod = 2
        else:
            cr_prof_mod = math.ceil(1 + (get_cr / 4))

        stat_list = [get_str, get_dex, get_con, get_int, get_wis, get_cha]
        stat_matrix = []
        for stat in stat_list:
            stat = math.floor((stat - 10) / 2)
            stat_matrix.append(stat)

        skill_list = [
            get_athl,
            get_acro,
            get_slgt,
            get_stlh,
            get_arcn,
            get_hist,
            get_invs,
            get_natr,
            get_relg,
            get_anhn,
            get_insg,
            get_medc,
            get_perc,
            get_surv,
            get_dect,
            get_intm,
            get_perf,
            get_pers
        ]
        dbl_skills = [
            get_dbl_athl,
            get_dbl_acro,
            get_dbl_slgt,
            get_dbl_stlh,
            get_dbl_arcn,
            get_dbl_hist,
            get_dbl_invs,
            get_dbl_natr,
            get_dbl_relg,
            get_dbl_anhn,
            get_dbl_insg,
            get_dbl_medc,
            get_dbl_perc,
            get_dbl_surv,
            get_dbl_dect,
            get_dbl_intm,
            get_dbl_perf,
            get_dbl_pers
        ]
        skill_matrix = []

        ath_skill = stat_matrix[0]
        if skill_list[0] == 1:
            ath_skill += cr_prof_mod + (cr_prof_mod * dbl_skills[0])
        skill_matrix.append(ath_skill)

        for i in range(1, 4): #skill_list[1:4]:
            dex_skill = stat_matrix[1]
            if skill_list[i] == 1:
                dex_skill += cr_prof_mod + (cr_prof_mod * dbl_skills[i])
            skill_matrix.append(dex_skill)

        for i in range(4, 9): #skill_list[4:9]:
            int_skill = stat_matrix[3]
            if skill_list[i] == 1:
                int_skill += cr_prof_mod + (cr_prof_mod * dbl_skills[i])
            skill_matrix.append(int_skill)

        for i in range(9, 14): #skill_list[9:14]:
            wis_skill = stat_matrix[4]
            if skill_list[i] == 1:
                wis_skill += cr_prof_mod + (cr_prof_mod * dbl_skills[i])
            skill_matrix.append(wis_skill)

        for i in range(14, 18): #skill_list[14:]:
            cha_skill = stat_matrix[5]
            if skill_list[i] == 1:
                cha_skill += cr_prof_mod + (cr_prof_mod * dbl_skills[i])
            skill_matrix.append(cha_skill)

        template_dict = {
            get_name: {
                'type': get_type,
                'size': get_size,
                'ac': get_ac,
                'hp': [get_hp_avg, get_hp_num_dice, get_hp_die, get_mod_hp],
                'speed': get_speed,
                'raw_stats': [
                    get_str,
                    get_dex,
                    get_con,
                    get_int,
                    get_wis, 
                    get_cha
                ],
                'mod_stats': stat_matrix,
                'senses': get_senses,
                'languages': get_lang,
                'cr': [get_cr, cr_prof_mod],
                'skills': {
                    'athletics': skill_matrix[0],
                    'acrobatics': skill_matrix[1],
                    'sleight_of_hand': skill_matrix[2],
                    'stealth': skill_matrix[3],
                    'arcane': skill_matrix[4],
                    'history': skill_matrix[5],
                    'investigation': skill_matrix[6],
                    'nature': skill_matrix[7],
                    'religion': skill_matrix[8],
                    'animal_handling': skill_matrix[9],
                    'insight': skill_matrix[10],
                    'medicine': skill_matrix[11],
                    'perception': skill_matrix[12],
                    'survival': skill_matrix[13],
                    'deception': skill_matrix[14],
                    'intimidation': skill_matrix[15],
                    'performance': skill_matrix[16],
                    'persuasion': skill_matrix[17],
                },
                'abilities': get_abil,
                'actions': get_actn,
                'reactions': get_reac
            }
        }
        # Temporary jump out to keep from making unnecessary files
        #return
        self.template_info = {}
        try:
            with open(self.file_loc, 'r') as template_file:
                self.template_info = json.load(template_file)
        except IOError:
            with open(self.file_loc, 'w') as template_file:
                json.dump(template_dict, template_file, indent=4)
            return
        self.template_info.update(template_dict)
        with open(self.file_loc, 'w') as template_file:
            json.dump(self.template_info, template_file, indent=4)

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Template Builder")
    style_dark = ThemedStyle(root)
    style_dark.theme_use("equilux")
    bg = style_dark.lookup('TLabel', 'background')
    fg = style_dark.lookup('TLabel', 'foreground')
    root.configure(bg=style_dark.lookup('TLabel', 'background'))
    root_width = root.winfo_reqwidth()
    root_height = root.winfo_reqheight()
    position_horizontal = int(root.winfo_screenwidth()/2 - root_width/2)
    position_vertical = int(root.winfo_screenheight()/2 - root_height/2)
    root.geometry("+{}+{}".format(position_horizontal, position_vertical))
    builder = TemplateBuilder(root)
    root.mainloop()
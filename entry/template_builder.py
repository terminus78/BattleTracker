import pathlib
import json
import os
import math
import copy
from tkinter.constants import S
from typing import Sized, cast
from zipfile import ZipFile

import tkinter as tk
from tkinter import Text, ttk,font,messagebox
from ttkthemes import ThemedStyle
import PIL.Image
from PIL import ImageTk


class TemplateBuilder():
    def __init__(self, root):
        self.root = root
        self.npc_m_loc = 'entry\\bin\\npc_monster.json'
        self.race_loc = 'entry\\bin\\race_lib.json'
        self.class_loc = 'entry\\bin\\class_lib.json'
        self.feat_loc = 'entry\\bin\\feat_lib.json'
        self.bkgd_loc = 'entry\\bin\\background_lib.json'
        self.weap_loc = 'entry\\bin\\weapon_lib.json'
        self.prop_list = ["Ammunition", "Finesse", "Heavy", "Light", "Loading", "Special", "Thrown", "Two-Handed", "Versatile", "Improvised", "Silvered", "Magical"]
        self.skill_list = ['athletics', 'acrobatics', 'sleight_of_hand', 'stealth', 'arcana', 'history', 'investigation', 'nature', 'religion', 'animal_handling', 'insight', 'medicine', 'perception', 'survival', 'deception', 'intimidation', 'performance', 'persuasion', 'choice']
        self.stat_list = ['STR', 'DEX', 'CON', 'INT', 'WIS', 'CHA']
        lbl_title = ttk.Label(master=self.root, text="What would you like to build?")
        lbl_title.grid(row=0, column=0)
        self.underline_font = font.Font(lbl_title, lbl_title.cget("font"))
        self.underline_font.configure(underline = True)
        self.small_font = font.Font(lbl_title, lbl_title.cget("font"))
        self.small_font.configure(size=7)
        catg_frame = ttk.Frame(master=self.root)
        catg_frame.grid(row=1, column=0)
        self.input_frame = ttk.Frame(master=self.root)
        self.input_frame.grid(row=2, column=0, padx=10, pady=10)
        self.send_it_frame = ttk.Frame(master=self.root)
        self.send_it_frame.grid(row=3, column=0)
        btn_npc = ttk.Button(master=catg_frame, command=lambda: self.build_form('npc'), text="Fast NPC")
        btn_npc.grid(row=0, column=0, sticky='w', padx=5, pady=10)
        btn_monster = ttk.Button(master=catg_frame, command=lambda: self.build_form('monster'), text="Monster")
        btn_monster.grid(row=0, column=1, sticky='w', padx=5, pady=10)
        btn_race = ttk.Button(master=catg_frame, command=self.build_race, text="Race")
        btn_race.grid(row=0, column=2, sticky='w', padx=5, pady=10)
        btn_subrace = ttk.Button(master=catg_frame, command=self.build_subrace, text="Subrace")
        btn_subrace.grid(row=0, column=3, sticky='w', padx=5, pady=10)
        btn_class = ttk.Button(master=catg_frame, command=self.build_class, text="Class")
        btn_class.grid(row=0, column=4, sticky='w', padx=5, pady=10)
        btn_archtype = ttk.Button(master=catg_frame, command=self.build_arch, text="Archetype")
        btn_archtype.grid(row=0, column=5, sticky='w', padx=5, pady=10)
        btn_feat = ttk.Button(master=catg_frame, command=self.build_feat, text="Feat")
        btn_feat.grid(row=0, column=6, sticky='w', padx=5, pady=10)
        btn_bkgd = ttk.Button(master=catg_frame, command=self.build_bkgd, text="Background")
        btn_bkgd.grid(row=0, column=7, sticky='w', padx=5, pady=10)
        btn_weap = ttk.Button(master=catg_frame, command=self.build_weap, text="Weapon")
        btn_weap.grid(row=0, column=8, sticky='w', padx=5, pady=10)
        lbl_waiting = ttk.Label(master=self.input_frame, text="Waiting...")
        lbl_waiting.grid(row=0, column=0)
        on_img_path = 'entry\\bin\\on.png'
        self.on_img = ImageTk.PhotoImage(image=PIL.Image.open(on_img_path))
        off_img_path = 'entry\\bin\\off.png'
        self.off_img = ImageTk.PhotoImage(image=PIL.Image.open(off_img_path))

    def build_form(self, catg):
        self.catg = catg
        self.wipe_off()

        lbl_catg = ttk.Label(master=self.input_frame, text="")
        lbl_catg.grid(row=0, column=0, sticky='w')
        lbl_catg.config(font=self.underline_font)
        if self.catg == 'npc':
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
        stat_frame.grid(row=8, column=1, sticky='w')
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

        skill_frame = ttk.Frame(master=self.input_frame)
        skill_frame.grid(row=2, column=3, rowspan=9, columnspan=4, sticky='nsew')
        skill_frame.rowconfigure([0,1,2,3,4,5,6,7,8,9], weight=1)
        skill_frame.columnconfigure([0,1,2,3], weight=1)
        lbl_prof_1 = ttk.Label(master=skill_frame, text="Prof")
        lbl_prof_1.grid(row=0, column=0, sticky='w')
        lbl_dbl_1 = ttk.Label(master=skill_frame, text="Double")
        lbl_dbl_1.grid(row=0, column=1, sticky='w')
        lbl_prof_2 = ttk.Label(master=skill_frame, text="Prof")
        lbl_prof_2.grid(row=0, column=2, sticky='w')
        lbl_dbl_2 = ttk.Label(master=skill_frame, text="Double")
        lbl_dbl_2.grid(row=0, column=3, sticky='w')
        #lbl_skill_mod = ttk.Label(master=skill_frame, text="Modifier: ")
        #lbl_skill_mod.grid(row=2, column=3, sticky='w')
        #self.ent_skill_mod = ttk.Entry(master=skill_frame, width=5)
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

        cbn_dbl_athletics = ttk.Checkbutton(master=skill_frame, text="Athletics", variable=self.athletics)
        cbn_dbl_acrobatics = ttk.Checkbutton(master=skill_frame, text="Acrobatics", variable=self.acrobatics)
        cbn_dbl_sleight_of_hand = ttk.Checkbutton(master=skill_frame, text="Sleight of Hand", variable=self.sleight_of_hand)
        cbn_dbl_stealth = ttk.Checkbutton(master=skill_frame, text="Stealth", variable=self.stealth)
        cbn_dbl_arcana = ttk.Checkbutton(master=skill_frame, text="Arcana", variable=self.arcana)
        cbn_dbl_history = ttk.Checkbutton(master=skill_frame, text="History", variable=self.history)
        cbn_dbl_investigation = ttk.Checkbutton(master=skill_frame, text="Investigation", variable=self.investigation)
        cbn_dbl_nature = ttk.Checkbutton(master=skill_frame, text="Nature", variable=self.nature)
        cbn_dbl_religion = ttk.Checkbutton(master=skill_frame, text="Religion", variable=self.religion)
        cbn_dbl_animal_handling = ttk.Checkbutton(master=skill_frame, text="Animal Handling", variable=self.animal_handling)
        cbn_dbl_insight = ttk.Checkbutton(master=skill_frame, text="Insight", variable=self.insight)
        cbn_dbl_medicine = ttk.Checkbutton(master=skill_frame, text="Medicine", variable=self.medicine)
        cbn_dbl_perception = ttk.Checkbutton(master=skill_frame, text="Perception", variable=self.perception)
        cbn_dbl_survival = ttk.Checkbutton(master=skill_frame, text="Survival", variable=self.survival)
        cbn_dbl_deception = ttk.Checkbutton(master=skill_frame, text="Deception", variable=self.deception)
        cbn_dbl_intimidation = ttk.Checkbutton(master=skill_frame, text="Intimidation", variable=self.intimidation)
        cbn_dbl_performance = ttk.Checkbutton(master=skill_frame, text="Performance", variable=self.performance)
        cbn_dbl_persuasion = ttk.Checkbutton(master=skill_frame, text="Persuasion", variable=self.persuasion)

        cbn_athletics = ttk.Checkbutton(master=skill_frame, variable=self.dbl_athletics)
        cbn_acrobatics = ttk.Checkbutton(master=skill_frame, variable=self.dbl_acrobatics)
        cbn_sleight_of_hand = ttk.Checkbutton(master=skill_frame, variable=self.dbl_sleight_of_hand)
        cbn_stealth = ttk.Checkbutton(master=skill_frame, variable=self.dbl_stealth)
        cbn_arcana = ttk.Checkbutton(master=skill_frame, variable=self.dbl_arcana)
        cbn_history = ttk.Checkbutton(master=skill_frame, variable=self.dbl_history)
        cbn_investigation = ttk.Checkbutton(master=skill_frame, variable=self.dbl_investigation)
        cbn_nature = ttk.Checkbutton(master=skill_frame, variable=self.dbl_nature)
        cbn_religion = ttk.Checkbutton(master=skill_frame, variable=self.dbl_religion)
        cbn_animal_handling = ttk.Checkbutton(master=skill_frame, variable=self.dbl_animal_handling)
        cbn_insight = ttk.Checkbutton(master=skill_frame, variable=self.dbl_insight)
        cbn_medicine = ttk.Checkbutton(master=skill_frame, variable=self.dbl_medicine)
        cbn_perception = ttk.Checkbutton(master=skill_frame, variable=self.dbl_perception)
        cbn_survival = ttk.Checkbutton(master=skill_frame, variable=self.dbl_survival)
        cbn_deception = ttk.Checkbutton(master=skill_frame, variable=self.dbl_deception)
        cbn_intimidation = ttk.Checkbutton(master=skill_frame, variable=self.dbl_intimidation)
        cbn_performance = ttk.Checkbutton(master=skill_frame, variable=self.dbl_performance)
        cbn_persuasion = ttk.Checkbutton(master=skill_frame, variable=self.dbl_persuasion)
        
        cbn_dbl_athletics.grid(row=1, column=1, sticky='w')
        cbn_dbl_acrobatics.grid(row=1, column=3, sticky='w')
        cbn_dbl_sleight_of_hand.grid(row=2, column=1, sticky='w')
        cbn_dbl_stealth.grid(row=2, column=3, sticky='w')
        cbn_dbl_arcana.grid(row=3, column=1, sticky='w')
        cbn_dbl_history.grid(row=3, column=3, sticky='w')
        cbn_dbl_investigation.grid(row=4, column=1, sticky='w')
        cbn_dbl_nature.grid(row=4, column=3, sticky='w')
        cbn_dbl_religion.grid(row=5, column=1, sticky='w')
        cbn_dbl_animal_handling.grid(row=5, column=3, sticky='w')
        cbn_dbl_insight.grid(row=6, column=1, sticky='w')
        cbn_dbl_medicine.grid(row=6, column=3, sticky='w')
        cbn_dbl_perception.grid(row=7, column=1, sticky='w')
        cbn_dbl_survival.grid(row=7, column=3, sticky='w')
        cbn_dbl_deception.grid(row=8, column=1, sticky='w')
        cbn_dbl_intimidation.grid(row=8, column=3, sticky='w')
        cbn_dbl_performance.grid(row=9, column=1, sticky='w')
        cbn_dbl_persuasion.grid(row=9, column=3, sticky='w')

        cbn_athletics.grid(row=1, column=0, sticky='w')
        cbn_acrobatics.grid(row=1, column=2, sticky='w')
        cbn_sleight_of_hand.grid(row=2, column=0, sticky='w')
        cbn_stealth.grid(row=2, column=2, sticky='w')
        cbn_arcana.grid(row=3, column=0, sticky='w')
        cbn_history.grid(row=3, column=2, sticky='w')
        cbn_investigation.grid(row=4, column=0, sticky='w')
        cbn_nature.grid(row=4, column=2, sticky='w')
        cbn_religion.grid(row=5, column=0, sticky='w')
        cbn_animal_handling.grid(row=5, column=2, sticky='w')
        cbn_insight.grid(row=6, column=0, sticky='w')
        cbn_medicine.grid(row=6, column=2, sticky='w')
        cbn_perception.grid(row=7, column=0, sticky='w')
        cbn_survival.grid(row=7, column=2, sticky='w')
        cbn_deception.grid(row=8, column=0, sticky='w')
        cbn_intimidation.grid(row=8, column=2, sticky='w')
        cbn_performance.grid(row=9, column=0, sticky='w')
        cbn_persuasion.grid(row=9, column=2, sticky='w')

        lbl_saving_throws = ttk.Label(master=self.input_frame, text="Proficient Saves: ")
        lbl_saving_throws.grid(row=11, column=2, sticky='w')

        saves_frame = ttk.Frame(master=self.input_frame)
        saves_frame.grid(row=12, column=3, rowspan=2, columnspan=3, sticky='w')

        self.prof_str = tk.IntVar()
        self.prof_dex = tk.IntVar()
        self.prof_con = tk.IntVar()
        self.prof_int = tk.IntVar()
        self.prof_wis = tk.IntVar()
        self.prof_cha = tk.IntVar()

        cbn_str_save = ttk.Checkbutton(master=saves_frame, text="STR", variable=self.prof_str)
        cbn_dex_save = ttk.Checkbutton(master=saves_frame, text="DEX", variable=self.prof_dex)
        cbn_con_save = ttk.Checkbutton(master=saves_frame, text="CON", variable=self.prof_con)
        cbn_int_save = ttk.Checkbutton(master=saves_frame, text="INT", variable=self.prof_int)
        cbn_wis_save = ttk.Checkbutton(master=saves_frame, text="WIS", variable=self.prof_wis)
        cbn_cha_save = ttk.Checkbutton(master=saves_frame, text="CHA", variable=self.prof_cha)

        cbn_str_save.grid(row=0, column=0, sticky='w')
        cbn_dex_save.grid(row=0, column=1, sticky='w')
        cbn_con_save.grid(row=0, column=2, sticky='w')
        cbn_int_save.grid(row=1, column=0, sticky='w')
        cbn_wis_save.grid(row=1, column=1, sticky='w')
        cbn_cha_save.grid(row=1, column=2, sticky='w')

        lbl_senses = ttk.Label(master=self.input_frame, text="Senses: ")
        lbl_senses.grid(row=9, column=0, sticky='w')
        self.txt_senses = tk.Text(master=self.input_frame, height=4, width=30, bg='gray28', fg='white')
        self.txt_senses.grid(row=9, column=1, sticky='w')
        lbl_languages = ttk.Label(master=self.input_frame, text="Languages: ")
        lbl_languages.grid(row=10, column=0, sticky='w')
        self.txt_languages = tk.Text(master=self.input_frame, height=4, width=30, bg='gray28', fg='white')
        self.txt_languages.grid(row=10, column=1, sticky='w')
        lbl_cr = ttk.Label(master=self.input_frame, text="CR: ")
        lbl_cr.grid(row=11, column=0, sticky='w')
        self.ent_cr = ttk.Entry(master=self.input_frame, width=20)
        self.ent_cr.grid(row=11, column=1, sticky='w')
        self.ent_cr.insert(0, "1")
        lbl_init = ttk.Label(master=self.input_frame, text="Special Initiative Bonuses: ")
        lbl_init.grid(row=12, column=0, sticky='w')
        self.ent_init = ttk.Entry(master=self.input_frame, width=20)
        self.ent_init.grid(row=12, column=1, sticky='w')
        self.ent_init.insert(0, "0")
        lbl_dmg_vuln = ttk.Label(master=self.input_frame, text="Damage Vulnerabilities: ")
        lbl_dmg_vuln.grid(row=13, column=0, sticky='w')
        self.txt_dmg_vuln = tk.Text(master=self.input_frame, height=2, width=30, bg='gray28', fg='white')
        self.txt_dmg_vuln.grid(row=13, column=1, sticky='w')
        lbl_dmg_res = ttk.Label(master=self.input_frame, text="Damage Resistances: ")
        lbl_dmg_res.grid(row=14, column=0, sticky='w')
        self.txt_dmg_res = tk.Text(master=self.input_frame, height=2, width=30, bg='gray28', fg='white')
        self.txt_dmg_res.grid(row=14, column=1, sticky='w')
        lbl_dmg_immn = ttk.Label(master=self.input_frame, text="Damage Immunities: ")
        lbl_dmg_immn.grid(row=15, column=0, sticky='w')
        self.txt_dmg_immn = tk.Text(master=self.input_frame, height=2, width=30, bg='gray28', fg='white')
        self.txt_dmg_immn.grid(row=15, column=1, sticky='w')
        lbl_cond_immn = ttk.Label(master=self.input_frame, text="Condition Immunities: ")
        lbl_cond_immn.grid(row=16, column=0, sticky='w')
        self.txt_cond_immn = tk.Text(master=self.input_frame, height=2, width=30, bg='gray28', fg='white')
        self.txt_cond_immn.grid(row=16, column=1, sticky='w')
        
        lbl_look_ma = ttk.Label(master=self.input_frame, text="Combat: ")
        lbl_look_ma.grid(row=1, column=7, sticky='w')
        lbl_abilities = ttk.Label(master=self.input_frame, text="Abilities/Features: ")
        lbl_abilities.grid(row=2, column=7, sticky='nw')
        self.txt_abilities = tk.Text(master=self.input_frame, height=6, bg='gray28', fg='white')
        self.txt_abilities.grid(row=2, column=8, rowspan=4, sticky='nw')
        lbl_actions = ttk.Label(master=self.input_frame, text="Actions/Legendary Actions: ")
        lbl_actions.grid(row=4, column=7, sticky='nw')
        self.txt_actions = tk.Text(master=self.input_frame, height=6, bg='gray28', fg='white')
        self.txt_actions.grid(row=4, column=8, rowspan=4, sticky='nw')
        lbl_reactions = ttk.Label(master=self.input_frame, text="Reactions/Legendary Reactions: ")
        lbl_reactions.grid(row=8, column=7, sticky='nw')
        self.txt_reactions = tk.Text(master=self.input_frame, height=6, bg='gray28', fg='white')
        self.txt_reactions.grid(row=8, column=8, sticky='nw')

        lbl_mean_mode = ttk.Label(master=self.input_frame, text="Mean Mode")
        lbl_mean_mode.grid(row=10, column=8)
        self.btn_mean_mode = tk.Button(master=self.input_frame, image=self.off_img, bd=0, bg='gray28', activebackground='gray28', relief=tk.SUNKEN, command=self.on_off_switch)
        self.btn_mean_mode.grid(row=11, column=8)
        self.btn_mean_mode.image = self.off_img
        self.mean_mode = False
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_npc_m, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def build_race(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Race", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')
        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=1, column=0, sticky='w')
        self.ent_name_race = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name_race.grid(row=1, column=1, sticky='w')
        lbl_size = ttk.Label(master=self.input_frame, text="Size: ")
        lbl_size.grid(row=2, column=0, sticky='w')
        self.size_race = tk.StringVar()
        size_frame = ttk.Frame(master=self.input_frame)
        size_frame.grid(row=2, column=1, sticky='w')
        rbn_tiny = ttk.Radiobutton(master=size_frame, text="tiny", variable=self.size_race, value='tiny')
        rbn_tiny.grid(row=0, column=0, sticky='w')
        rbn_small = ttk.Radiobutton(master=size_frame, text="small", variable=self.size_race, value='small')
        rbn_small.grid(row=0, column=1, sticky='w')
        rbn_medium = ttk.Radiobutton(master=size_frame, text="medium", variable=self.size_race, value='medium')
        rbn_medium.grid(row=1, column=0, sticky='w')
        rbn_large = ttk.Radiobutton(master=size_frame, text="large", variable=self.size_race, value='large')
        rbn_large.grid(row=1, column=1, sticky='w')
        rbn_huge = ttk.Radiobutton(master=size_frame, text="huge", variable=self.size_race, value='huge')
        rbn_huge.grid(row=2, column=0, sticky='w')
        rbn_gargantuan = ttk.Radiobutton(master=size_frame, text="garg", variable=self.size_race, value='gargantuan')
        rbn_gargantuan.grid(row=2, column=1, sticky='w')
        self.size_race.set("medium")
        lbl_walk_speed = ttk.Label(master=self.input_frame, text="Walking Speed: ")
        lbl_walk_speed.grid(row=3, column=0, sticky='w')
        self.ent_gnd_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_gnd_speed.grid(row=3, column=1, sticky='w')
        self.ent_gnd_speed.insert(0, "30")
        lbl_fly_speed = ttk.Label(master=self.input_frame, text="Flying Speed: ")
        lbl_fly_speed.grid(row=4, column=0, sticky='w')
        self.ent_fly_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_fly_speed.grid(row=4, column=1, sticky='w')
        #self.ent_fly_speed.insert(0, "0")
        lbl_swim_speed = ttk.Label(master=self.input_frame, text="Swim Speed: ")
        lbl_swim_speed.grid(row=5, column=0, sticky='w')
        self.ent_swim_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_swim_speed.grid(row=5, column=1, sticky='w')
        #self.ent_swim_speed.insert(0, "0")
        lbl_burrow_speed = ttk.Label(master=self.input_frame, text="Burrow Speed: ")
        lbl_burrow_speed.grid(row=6, column=0, sticky='w')
        self.ent_burrow_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_burrow_speed.grid(row=6, column=1, sticky='w')
        #self.ent_burrow_speed.insert(0, "0")
        lbl_stats = ttk.Label(master=self.input_frame, text="Bonuses: ")
        lbl_stats.grid(row=7, column=0, columnspan=2)
        stat_frame = ttk.Frame(master=self.input_frame)
        stat_frame.grid(row=8, column=0, columnspan=2)
        lbl_str_mod = ttk.Label(master=stat_frame, text="STR")
        lbl_str_mod.grid(row=0, column=0)
        lbl_dex_mod = ttk.Label(master=stat_frame, text="DEX")
        lbl_dex_mod.grid(row=0, column=1)
        lbl_con_mod = ttk.Label(master=stat_frame, text="CON")
        lbl_con_mod.grid(row=0, column=2)
        self.ent_str_mod = ttk.Entry(master=stat_frame, width=5)
        self.ent_str_mod.grid(row=1, column=0)
        self.ent_dex_mod = ttk.Entry(master=stat_frame, width=5)
        self.ent_dex_mod.grid(row=1, column=1)
        self.ent_con_mod = ttk.Entry(master=stat_frame, width=5)
        self.ent_con_mod.grid(row=1, column=2)
        self.ent_str_mod.insert(0, "0")
        self.ent_dex_mod.insert(0, "0")
        self.ent_con_mod.insert(0, "0")
        lbl_int_mod = ttk.Label(master=stat_frame, text="INT")
        lbl_int_mod.grid(row=2, column=0)
        lbl_wis_mod = ttk.Label(master=stat_frame, text="WIS")
        lbl_wis_mod.grid(row=2, column=1)
        lbl_cha_mod = ttk.Label(master=stat_frame, text="CHA")
        lbl_cha_mod.grid(row=2, column=2)
        self.ent_int_mod = ttk.Entry(master=stat_frame, width=5)
        self.ent_int_mod.grid(row=3, column=0)
        self.ent_wis_mod = ttk.Entry(master=stat_frame, width=5)
        self.ent_wis_mod.grid(row=3, column=1)
        self.ent_cha_mod = ttk.Entry(master=stat_frame, width=5)
        self.ent_cha_mod.grid(row=3, column=2)
        self.ent_int_mod.insert(0, "0")
        self.ent_wis_mod.insert(0, "0")
        self.ent_cha_mod.insert(0, "0")
        lbl_langs = ttk.Label(master=self.input_frame, text="Languages: ")
        lbl_langs.grid(row=9, column=0, sticky='w')
        lbl_lang_1 = ttk.Label(master=self.input_frame, text="1: ")
        lbl_lang_1.grid(row=10, column=0, sticky='e')
        self.ent_lang_1 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_1.grid(row=10, column=1, sticky='w')
        self.ent_lang_1.insert(0, "Common")
        lbl_lang_2 = ttk.Label(master=self.input_frame, text="2: ")
        lbl_lang_2.grid(row=11, column=0, sticky='e')
        self.ent_lang_2 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_2.grid(row=11, column=1, sticky='w')
        lbl_lang_3 = ttk.Label(master=self.input_frame, text="3: ")
        lbl_lang_3.grid(row=12, column=0, sticky='e')
        self.ent_lang_3 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_3.grid(row=12, column=1, sticky='w')
        lbl_lang_4 = ttk.Label(master=self.input_frame, text="4: ")
        lbl_lang_4.grid(row=13, column=0, sticky='e')
        self.ent_lang_4 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_4.grid(row=13, column=1, sticky='w')
        lbl_abilities = ttk.Label(master=self.input_frame, text="Abilities: ")
        lbl_abilities.grid(row=0, column=2, sticky='w', padx=30)
        self.txt_racials = tk.Text(master=self.input_frame, bg='gray28', fg='white')
        self.txt_racials.grid(row=1, column=2, rowspan=13, sticky='w', padx=30)
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_race, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def build_subrace(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Subrace", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

        if os.path.exists(self.race_loc) == False:
            messagebox.showwarning("Forge", "Must build base races before subraces.")
            return
        else:
            with open(self.race_loc, 'r') as race_file:
                self.race_info_sub = json.load(race_file)
            if len(self.race_info_sub) == 0:
                messagebox.showwarning("Forge", "Must build base races before subraces.")
                return
            race_list_sub = []
            for race in self.race_info_sub.keys():
                race_list_sub.append(race)

        lbl_select_race_sub = ttk.Label(master=self.input_frame, text="Select Race: ")
        lbl_select_race_sub.grid(row=1, column=0, sticky='w')
        self.cbx_races_sub = ttk.Combobox(master=self.input_frame, width=20, values=race_list_sub, state='readonly')
        self.cbx_races_sub.grid(row=1, column=1, sticky='w')
        self.cbx_races_sub.bind("<<ComboboxSelected>>", self._on_select_race)
        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=2, column=0, sticky='w')
        self.ent_name_race_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name_race_sub.grid(row=2, column=1, sticky='w')
        lbl_size = ttk.Label(master=self.input_frame, text="Size: ")
        lbl_size.grid(row=3, column=0, sticky='w')
        self.size_race_sub = tk.StringVar()
        size_frame = ttk.Frame(master=self.input_frame)
        size_frame.grid(row=3, column=1, sticky='w')
        rbn_tiny = ttk.Radiobutton(master=size_frame, text="tiny", variable=self.size_race_sub, value='tiny')
        rbn_tiny.grid(row=0, column=0, sticky='w')
        rbn_small = ttk.Radiobutton(master=size_frame, text="small", variable=self.size_race_sub, value='small')
        rbn_small.grid(row=0, column=1, sticky='w')
        rbn_medium = ttk.Radiobutton(master=size_frame, text="medium", variable=self.size_race_sub, value='medium')
        rbn_medium.grid(row=1, column=0, sticky='w')
        rbn_large = ttk.Radiobutton(master=size_frame, text="large", variable=self.size_race_sub, value='large')
        rbn_large.grid(row=1, column=1, sticky='w')
        rbn_huge = ttk.Radiobutton(master=size_frame, text="huge", variable=self.size_race_sub, value='huge')
        rbn_huge.grid(row=2, column=0, sticky='w')
        rbn_gargantuan = ttk.Radiobutton(master=size_frame, text="garg", variable=self.size_race_sub, value='gargantuan')
        rbn_gargantuan.grid(row=2, column=1, sticky='w')
        self.size_race_sub.set("medium")
        lbl_walk_speed = ttk.Label(master=self.input_frame, text="Walking Speed: ")
        lbl_walk_speed.grid(row=4, column=0, sticky='w')
        self.ent_gnd_speed_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_gnd_speed_sub.grid(row=4, column=1, sticky='w')
        self.ent_gnd_speed_sub.insert(0, "30")
        lbl_fly_speed = ttk.Label(master=self.input_frame, text="Flying Speed: ")
        lbl_fly_speed.grid(row=5, column=0, sticky='w')
        self.ent_fly_speed_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_fly_speed_sub.grid(row=5, column=1, sticky='w')
        #self.ent_fly_speed_sub.insert(0, "0")
        lbl_swim_speed = ttk.Label(master=self.input_frame, text="Swim Speed: ")
        lbl_swim_speed.grid(row=6, column=0, sticky='w')
        self.ent_swim_speed_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_swim_speed_sub.grid(row=6, column=1, sticky='w')
        #self.ent_swim_speed_sub.insert(0, "0")
        lbl_burrow_speed = ttk.Label(master=self.input_frame, text="Burrow Speed: ")
        lbl_burrow_speed.grid(row=7, column=0, sticky='w')
        self.ent_burrow_speed_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_burrow_speed_sub.grid(row=7, column=1, sticky='w')
        #self.ent_burrow_speed_sub.insert(0, "0")
        lbl_stats = ttk.Label(master=self.input_frame, text="Bonuses: ")
        lbl_stats.grid(row=8, column=0, columnspan=2)
        stat_frame = ttk.Frame(master=self.input_frame)
        stat_frame.grid(row=9, column=0, columnspan=2)
        lbl_str_mod = ttk.Label(master=stat_frame, text="STR")
        lbl_str_mod.grid(row=0, column=0)
        lbl_dex_mod = ttk.Label(master=stat_frame, text="DEX")
        lbl_dex_mod.grid(row=0, column=1)
        lbl_con_mod = ttk.Label(master=stat_frame, text="CON")
        lbl_con_mod.grid(row=0, column=2)
        self.ent_str_mod_sub = ttk.Entry(master=stat_frame, width=5)
        self.ent_str_mod_sub.grid(row=1, column=0)
        self.ent_dex_mod_sub = ttk.Entry(master=stat_frame, width=5)
        self.ent_dex_mod_sub.grid(row=1, column=1)
        self.ent_con_mod_sub = ttk.Entry(master=stat_frame, width=5)
        self.ent_con_mod_sub.grid(row=1, column=2)
        self.ent_str_mod_sub.insert(0, "0")
        self.ent_dex_mod_sub.insert(0, "0")
        self.ent_con_mod_sub.insert(0, "0")
        lbl_int_mod = ttk.Label(master=stat_frame, text="INT")
        lbl_int_mod.grid(row=2, column=0)
        lbl_wis_mod = ttk.Label(master=stat_frame, text="WIS")
        lbl_wis_mod.grid(row=2, column=1)
        lbl_cha_mod = ttk.Label(master=stat_frame, text="CHA")
        lbl_cha_mod.grid(row=2, column=2)
        self.ent_int_mod_sub = ttk.Entry(master=stat_frame, width=5)
        self.ent_int_mod_sub.grid(row=3, column=0)
        self.ent_wis_mod_sub = ttk.Entry(master=stat_frame, width=5)
        self.ent_wis_mod_sub.grid(row=3, column=1)
        self.ent_cha_mod_sub = ttk.Entry(master=stat_frame, width=5)
        self.ent_cha_mod_sub.grid(row=3, column=2)
        self.ent_int_mod_sub.insert(0, "0")
        self.ent_wis_mod_sub.insert(0, "0")
        self.ent_cha_mod_sub.insert(0, "0")
        lbl_langs = ttk.Label(master=self.input_frame, text="Languages: ")
        lbl_langs.grid(row=10, column=0, sticky='w')
        lbl_lang_1 = ttk.Label(master=self.input_frame, text="1: ")
        lbl_lang_1.grid(row=11, column=0, sticky='e')
        self.ent_lang_1_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_1_sub.grid(row=11, column=1, sticky='w')
        self.ent_lang_1_sub.insert(0, "Common")
        lbl_lang_2 = ttk.Label(master=self.input_frame, text="2: ")
        lbl_lang_2.grid(row=12, column=0, sticky='e')
        self.ent_lang_2_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_2_sub.grid(row=12, column=1, sticky='w')
        lbl_lang_3 = ttk.Label(master=self.input_frame, text="3: ")
        lbl_lang_3.grid(row=13, column=0, sticky='e')
        self.ent_lang_3_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_3_sub.grid(row=13, column=1, sticky='w')
        lbl_lang_4 = ttk.Label(master=self.input_frame, text="4: ")
        lbl_lang_4.grid(row=14, column=0, sticky='e')
        self.ent_lang_4_sub = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_4_sub.grid(row=14, column=1, sticky='w')
        lbl_abilities = ttk.Label(master=self.input_frame, text="Abilities: ")
        lbl_abilities.grid(row=0, column=2, sticky='w', padx=30)
        self.txt_racials_sub = tk.Text(master=self.input_frame, bg='gray28', fg='white')
        self.txt_racials_sub.grid(row=1, column=2, rowspan=13, sticky='w', padx=30)
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_subrace, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def build_class(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Class", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

        if os.path.exists(self.weap_loc) == False:
            messagebox.showwarning("Forge", "Must build base races before subraces.")
            return
        else:
            with open(self.weap_loc, 'r') as weap_file:
                self.weap_info = json.load(weap_file)
            if len(self.weap_info) == 0:
                messagebox.showwarning("Forge", "Must build weapons before classes.")
                return
            weap_list = []
            for weap in self.weap_info['simple']['melee'].keys():
                weap_list.append(weap)
            for weap in self.weap_info['simple']['ranged'].keys():
                weap_list.append(weap)
            for weap in self.weap_info['martial']['melee'].keys():
                weap_list.append(weap)
            for weap in self.weap_info['martial']['ranged'].keys():
                weap_list.append(weap)

        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=1, column=0, sticky='w')
        self.ent_name_class = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name_class.grid(row=1, column=1, sticky='w')
        lbl_hit_dice = ttk.Label(master=self.input_frame, text="Hit Dice: ")
        lbl_hit_dice.grid(row=2, column=0, sticky='w')
        self.hit_die = tk.IntVar()
        self.past = 4
        self.sldr_hit_dice = tk.Scale(master=self.input_frame, from_=4, to=12, variable=self.hit_die, orient=tk.HORIZONTAL, tickinterval=2, bg='gray28', fg='gray70', highlightbackground='gray28', highlightcolor='gray28', activebackground='gray28', troughcolor='gray28', length=125, command=self.make_even)
        self.sldr_hit_dice.grid(row=2, column=1, sticky='w')
        lbl_hp_stat = ttk.Label(master=self.input_frame, text="HP Modifier: ")
        lbl_hp_stat.grid(row=3, column=0, sticky='w')
        self.cbx_hp_stat = ttk.Combobox(master=self.input_frame, width=20, values=self.stat_list, state='readonly')
        self.cbx_hp_stat.grid(row=3, column=1, sticky='w')
        lbl_prof_armor = ttk.Label(master=self.input_frame, text="Armor Proficiencies: ")
        lbl_prof_armor.grid(row=4, column=0, sticky='nw', pady=5)
        self.txt_class_armor = tk.Text(master=self.input_frame, height=4, width=48, bg='gray28', fg='white')
        self.txt_class_armor.grid(row=4, column=1, sticky='nw', pady=5)
        lbl_prof_tools = ttk.Label(master=self.input_frame, text="Tool Proficiencies: ")
        lbl_prof_tools.grid(row=5, column=0, sticky='nw', pady=5)
        self.txt_class_tools = tk.Text(master=self.input_frame, height=4, width=48, bg='gray28', fg='white')
        self.txt_class_tools.grid(row=5, column=1, sticky='nw', pady=5)
        lbl_prof_weap = ttk.Label(master=self.input_frame, text="Weapon Proficiencies: ")
        lbl_prof_weap.grid(row=6, column=0, sticky='w')
        weap_type_frame = ttk.Frame(master=self.input_frame)
        weap_type_frame.grid(row=6, column=1, sticky='w')
        self.class_simple = tk.IntVar()
        self.class_martial = tk.IntVar()
        self.class_limited = tk.IntVar()
        self.cbn_class_simple = ttk.Checkbutton(master=weap_type_frame, text="Simple", variable=self.class_simple)
        self.cbn_class_simple.grid(row=0, column=0, sticky='w')
        self.cbn_class_martial = ttk.Checkbutton(master=weap_type_frame, text="Martial", variable=self.class_martial)
        self.cbn_class_martial.grid(row=0, column=1, sticky='w')
        self.cbn_class_limited = ttk.Checkbutton(master=weap_type_frame, text="Limited", variable=self.class_limited, command=lambda: self._toggle_limited('c'))
        self.cbn_class_limited.grid(row=0, column=2, sticky='w')
        limited_lframe = ttk.Labelframe(master=self.input_frame, text="Limited Weapon Proficiency Selection")
        limited_lframe.grid(row=7, column=1, sticky='w', pady=10)
        from_frame = ttk.Frame(master=limited_lframe)
        from_frame.grid(row=0, column=0, rowspan=2, sticky='w', padx=10, pady=10)
        self.opt_weap_list = tk.Listbox(master=from_frame, selectmode='multiple', bg='gray28', fg='white', highlightthickness=0)
        self.opt_weap_list.grid(row=0, column=0, sticky='w')
        scr_from_lst = ttk.Scrollbar(master=from_frame, orient='vertical')
        scr_from_lst.config(command=self.opt_weap_list.yview)
        scr_from_lst.grid(row=0, column=1, sticky='w')
        self.opt_weap_list.config(yscrollcommand=scr_from_lst.set)
        for item in weap_list:
            self.opt_weap_list.insert('end', item)
        self.opt_weap_list.config(state='disabled')
        self.opt_weap_list.bind('<Enter>', lambda e: self._on_enter_canvas(event=e, lst='f', orig='c'))
        self.opt_weap_list.bind('<Leave>', lambda e: self._on_leave_canvas(event=e, lst='f', orig='c'))
        self.btn_move_to_char = ttk.Button(master=limited_lframe, text="=>", width=5, command=lambda: self.move_box('to', 'c'))
        self.btn_move_to_char.grid(row=0, column=1, padx=15)
        self.btn_move_to_char.state(['disabled'])
        self.btn_move_from_char = ttk.Button(master=limited_lframe, text="<=", width=5, command=lambda: self.move_box('from', 'c'))
        self.btn_move_from_char.grid(row=1, column=1, padx=15)
        self.btn_move_from_char.state(['disabled'])
        to_frame = ttk.Frame(master=limited_lframe)
        to_frame.grid(row=0, column=2, rowspan=2, sticky='w', padx=10, pady=10)
        self.has_weap_list = tk.Listbox(master=to_frame, selectmode='multiple', bg='gray28', fg='white', highlightthickness=0)
        self.has_weap_list.grid(row=0, column=0, sticky='w')
        scr_to_lst = ttk.Scrollbar(master=to_frame, orient='vertical')
        scr_to_lst.config(command=self.has_weap_list.yview)
        scr_to_lst.grid(row=0, column=1, sticky='w')
        self.has_weap_list.config(yscrollcommand=scr_to_lst.set)
        self.has_weap_list.config(state='disabled')
        self.has_weap_list.bind('<Enter>', lambda e: self._on_enter_canvas(event=e, lst='t', orig='c'))
        self.has_weap_list.bind('<Leave>', lambda e: self._on_leave_canvas(event=e, lst='t', orig='c'))
        lbl_saves = ttk.Label(master=self.input_frame, text="Saving Throws: ")
        lbl_saves.grid(row=8, column=0, sticky='w')
        save_frame = ttk.Frame(master=self.input_frame)
        save_frame.grid(row=8, column=1, sticky='w')
        self.class_saves = []
        row_num = 0
        col_num = 0
        for i in range(6):
            self.class_saves.append(tk.IntVar())
            cbn_save = ttk.Checkbutton(master=save_frame, text=self.stat_list[i], variable=self.class_saves[i])
            cbn_save.grid(row=row_num, column=col_num, sticky='w')
            col_num += 1
            if col_num >= 3:
                col_num = 0
                row_num += 1
        lbl_prof_stat = ttk.Label(master=self.input_frame, text="Possible Stat Proficiencies: ")
        lbl_prof_stat.grid(row=9, column=0, sticky='w')
        skill_frame = ttk.Frame(master=self.input_frame)
        skill_frame.grid(row=10, column=1, sticky='w')
        skill_titles = []
        for item in self.skill_list:
            if "_" in item:
                item = item.split("_")
                item = " ".join(item)
            skill_titles.append(item.title())
        self.class_skills = []
        row_num = 0
        col_num = 0
        for i in range(18):
            self.class_skills.append(tk.IntVar())
            cbn_skill = ttk.Checkbutton(master=skill_frame, text=skill_titles[i], variable=self.class_skills[i])
            cbn_skill.grid(row=row_num, column=col_num, sticky='w')
            row_num += 1
            if row_num >= 5:
                row_num = 0
                col_num += 1
        lbl_skill_choice = ttk.Label(master=self.input_frame, text="Number of Choices: ")
        lbl_skill_choice.grid(row=11, column=0, sticky='w')
        self.ent_skill_choices = ttk.Entry(master=self.input_frame, width=10)
        self.ent_skill_choices.grid(row=11, column=1, sticky='w')
        lbl_equipment = ttk.Label(master=self.input_frame, text="Equipment: ")
        lbl_equipment.grid(row=0, column=2, sticky='nw', pady=5)
        self.txt_class_equip = tk.Text(master=self.input_frame, height=4, width=48, bg='gray28', fg='white')
        self.txt_class_equip.grid(row=0, column=3, sticky='w', pady=5)
        lbl_magic = ttk.Label(master=self.input_frame, text="Magical Affinity: ")
        lbl_magic.grid(row=1, column=2, sticky='w')
        caster_frame = ttk.Frame(master=self.input_frame)
        caster_frame.grid(row=1, column=3, sticky='w')
        self.class_magic = tk.StringVar()
        rbn_full_caster = ttk.Radiobutton(master=caster_frame, text="Full Caster", variable=self.class_magic, value='full')
        rbn_full_caster.grid(row=0, column=0, sticky='w', padx=5)
        rbn_half_caster = ttk.Radiobutton(master=caster_frame, text="Half Caster", variable=self.class_magic, value='half')
        rbn_half_caster.grid(row=0, column=1, sticky='w', padx=5)
        rbn_pact_magic = ttk.Radiobutton(master=caster_frame, text="Pact Magic")
        rbn_pact_magic.grid(row=0, column=2, sticky='w', padx=5)
        lbl_cast_stat = ttk.Label(master=self.input_frame, text="Casting Stat: ")
        lbl_cast_stat.grid(row=2, column=2, sticky='w')
        self.ent_cast_stat = ttk.Entry(master=self.input_frame, width=20)
        self.ent_cast_stat.grid(row=2, column=3, sticky='w')
        lbl_rituals = ttk.Label(master=self.input_frame, text="Ritual Caster: ")
        lbl_rituals.grid(row=3, column=2, sticky='w')
        self.ritual_caster = tk.IntVar()
        cbn_rituals = ttk.Checkbutton(master=self.input_frame, variable=self.ritual_caster)
        cbn_rituals.grid(row=3, column=3, sticky='w')
        self.ritual_caster.set(0)
        lbl_abil_improv = ttk.Label(master=self.input_frame, text="Ability Score Improvements: ")
        lbl_abil_improv.grid(row=4, column=2, sticky='w')
        improv_frame = ttk.Frame(master=self.input_frame)
        improv_frame.grid(row=4, column=3, sticky='w')
        self.improv_ents = []
        next_row = 0
        next_col = 0
        for i in range(7):
            lbl_at_lvl = ttk.Label(master=improv_frame, text="Level: ")
            lbl_at_lvl.grid(row=next_row, column=next_col, sticky='w')
            ent_improv = ttk.Entry(master=improv_frame, width=5)
            ent_improv.grid(row=next_row, column=next_col+1, sticky='w')
            ent_improv.state(['disabled'])
            self.improv_ents.append(ent_improv)
            next_row += 1
            if next_row >= 4:
                next_row = 0
                next_col += 2
        lbl_improv_info = ttk.Label(master=improv_frame, text="Leave unnecessary improvement fields empty.", font=self.small_font)
        lbl_improv_info.grid(row=4, column=0, columnspan=4, sticky='w')
        btn_add_improv = ttk.Button(master=improv_frame, text="Add Improvement", command=self.add_improv)
        btn_add_improv.grid(row=0, column=4, rowspan=4)

    def build_arch(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Archetype", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

    def build_feat(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Feat", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

        if os.path.exists(self.weap_loc) == False:
            messagebox.showwarning("Forge", "Must build base races before subraces.")
            return
        else:
            with open(self.weap_loc, 'r') as weap_file:
                self.weap_info = json.load(weap_file)
            if len(self.weap_info) == 0:
                messagebox.showwarning("Forge", "Must build weapons before feats.")
                return
            weap_list = []
            for weap in self.weap_info['simple']['melee'].keys():
                weap_list.append(weap)
            for weap in self.weap_info['simple']['ranged'].keys():
                weap_list.append(weap)
            for weap in self.weap_info['martial']['melee'].keys():
                weap_list.append(weap)
            for weap in self.weap_info['martial']['ranged'].keys():
                weap_list.append(weap)

        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=1, column=0, sticky='w')
        self.ent_name_feat = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name_feat.grid(row=1, column=1, sticky='w')
        self.stat_inc = tk.IntVar()
        cbn_stat_inc = ttk.Checkbutton(master=self.input_frame, variable=self.stat_inc, command=self._toggle_stats)
        cbn_stat_inc.grid(row=2, column=0, sticky='nw')
        lbl_stat_inc = ttk.Label(master=self.input_frame, text="Stat Increase: ")
        lbl_stat_inc.grid(row=2, column=1, sticky='nw', pady=5)
        stat_pick_frame = ttk.Frame(master=self.input_frame)
        stat_pick_frame.grid(row=2, column=2, sticky='w')
        self.stat_vars = []
        self.stat_cbns = []
        row_pos = 0
        col_pos = 0
        for i in range(6):
            self.stat_vars.append(tk.IntVar())
            self.stat_cbns.append(
                ttk.Checkbutton(master=stat_pick_frame, text=self.stat_list[i], variable=self.stat_vars[i])
            )
            self.stat_cbns[i].grid(row=row_pos, column=col_pos, sticky='w')
            self.stat_cbns[i].state(['disabled'])
            col_pos += 1
            if col_pos >= 3:
                col_pos = 0
                row_pos += 1
        self.prof_weap = tk.IntVar()
        cbn_prof_weap = ttk.Checkbutton(master=self.input_frame, variable=self.prof_weap, command=self._toggle_weap)
        cbn_prof_weap.grid(row=3, column=0, sticky='w')
        lbl_prof_weap = ttk.Label(master=self.input_frame, text="Weapon Proficiencies: ")
        lbl_prof_weap.grid(row=3, column=1, sticky='w')
        weap_type_frame = ttk.Frame(master=self.input_frame)
        weap_type_frame.grid(row=3, column=2, sticky='w')
        self.feat_simple = tk.IntVar()
        self.feat_martial = tk.IntVar()
        self.feat_limited = tk.IntVar()
        self.cbn_feat_simple = ttk.Checkbutton(master=weap_type_frame, text="Simple", variable=self.feat_simple)
        self.cbn_feat_simple.grid(row=0, column=0, sticky='w')
        self.cbn_feat_simple.state(['disabled'])
        self.cbn_feat_martial = ttk.Checkbutton(master=weap_type_frame, text="Martial", variable=self.feat_martial)
        self.cbn_feat_martial.grid(row=0, column=1, sticky='w')
        self.cbn_feat_martial.state(['disabled'])
        self.cbn_feat_limited = ttk.Checkbutton(master=weap_type_frame, text="Limited", variable=self.feat_limited, command=lambda: self._toggle_limited('f'))
        self.cbn_feat_limited.grid(row=0, column=2, sticky='w')
        self.cbn_feat_limited.state(['disabled'])
        limited_lframe = ttk.Labelframe(master=self.input_frame, text="Limited Weapon Proficiency Selection")
        limited_lframe.grid(row=4, column=1, columnspan=2, sticky='w', pady=10)
        from_frame = ttk.Frame(master=limited_lframe)
        from_frame.grid(row=0, column=0, rowspan=2, sticky='w', padx=10, pady=10)
        self.from_weap_list = tk.Listbox(master=from_frame, selectmode='multiple', bg='gray28', fg='white', highlightthickness=0)
        self.from_weap_list.grid(row=0, column=0, sticky='w')
        scr_from_lst = ttk.Scrollbar(master=from_frame, orient='vertical')
        scr_from_lst.config(command=self.from_weap_list.yview)
        scr_from_lst.grid(row=0, column=1, sticky='w')
        self.from_weap_list.config(yscrollcommand=scr_from_lst.set)
        for item in weap_list:
            self.from_weap_list.insert('end', item)
        self.from_weap_list.config(state='disabled')
        self.from_weap_list.bind('<Enter>', lambda e: self._on_enter_canvas(event=e, lst='f', orig='f'))
        self.from_weap_list.bind('<Leave>', lambda e: self._on_leave_canvas(event=e, lst='f', orig='f'))
        self.btn_move_to_you = ttk.Button(master=limited_lframe, text="=>", width=5, command=lambda: self.move_box('to', 'f'))
        self.btn_move_to_you.grid(row=0, column=1, padx=15)
        self.btn_move_to_you.state(['disabled'])
        self.btn_move_from_you = ttk.Button(master=limited_lframe, text="<=", width=5, command=lambda: self.move_box('from', 'f'))
        self.btn_move_from_you.grid(row=1, column=1, padx=15)
        self.btn_move_from_you.state(['disabled'])
        to_frame = ttk.Frame(master=limited_lframe)
        to_frame.grid(row=0, column=2, rowspan=2, sticky='w', padx=10, pady=10)
        self.char_weap_list = tk.Listbox(master=to_frame, selectmode='multiple', bg='gray28', fg='white', highlightthickness=0)
        self.char_weap_list.grid(row=0, column=0, sticky='w')
        scr_to_lst = ttk.Scrollbar(master=to_frame, orient='vertical')
        scr_to_lst.config(command=self.char_weap_list.yview)
        scr_to_lst.grid(row=0, column=1, sticky='w')
        self.char_weap_list.config(yscrollcommand=scr_to_lst.set)
        self.char_weap_list.config(state='disabled')
        self.char_weap_list.bind('<Enter>', lambda e: self._on_enter_canvas(event=e, lst='t', orig='f'))
        self.char_weap_list.bind('<Leave>', lambda e: self._on_leave_canvas(event=e, lst='t', orig='f'))
        self.stat_prof = tk.IntVar()
        cbn_prof_stat = ttk.Checkbutton(master=self.input_frame, variable=self.stat_prof, command=self._toggle_prof_stat)
        cbn_prof_stat.grid(row=5, column=0, sticky='w')
        lbl_prof_stat = ttk.Label(master=self.input_frame, text="Stat Proficiencies: ")
        lbl_prof_stat.grid(row=5, column=1, sticky='w')
        skill_frame = ttk.Frame(master=self.input_frame)
        skill_frame.grid(row=6, column=1, columnspan=2, sticky='w')
        skill_titles = []
        for item in self.skill_list:
            if "_" in item:
                item = item.split("_")
                item = " ".join(item)
            skill_titles.append(item.title())
        self.skill_prof = []
        self.cbn_prof = []
        row_num = 0
        col_num = 0
        for i in range(18):
            self.skill_prof.append(tk.IntVar())
            cbn_skill = ttk.Checkbutton(master=skill_frame, text=skill_titles[i], variable=self.skill_prof[i])
            cbn_skill.grid(row=row_num, column=col_num, sticky='w')
            cbn_skill.state(['disabled'])
            self.cbn_prof.append(cbn_skill)
            row_num += 1
            if row_num >= 5:
                row_num = 0
                col_num += 1
        lbl_skill_choice = ttk.Label(master=self.input_frame, text="Number of Choices: ")
        lbl_skill_choice.grid(row=7, column=1, sticky='e')
        self.ent_skill_choices = ttk.Entry(master=self.input_frame, width=10)
        self.ent_skill_choices.grid(row=7, column=2, sticky='w')
        self.ent_skill_choices.state(['disabled'])
        self.prof_tool = tk.IntVar()
        cbn_prof_tool = ttk.Checkbutton(master=self.input_frame, variable=self.prof_tool, command=self._toggle_prof_tool)
        cbn_prof_tool.grid(row=1, column=3, sticky='w')
        lbl_prof_tool = ttk.Label(master=self.input_frame, text="Tool Proficiencies: ")
        lbl_prof_tool.grid(row=1, column=4, sticky='w')
        self.txt_feat_tools = tk.Text(master=self.input_frame, height=4, width=70, bg='gray28', fg='white')
        self.txt_feat_tools.grid(row=2, column=4, columnspan=2, sticky='w')
        self.txt_feat_tools.config(state='disabled')
        self.feat_armor = tk.IntVar()
        cbn_feat_armor = ttk.Checkbutton(master=self.input_frame, variable=self.feat_armor, command=self._toggle_feat_armor)
        cbn_feat_armor.grid(row=3, column=3, sticky='w')
        lbl_feat_armor = ttk.Label(master=self.input_frame, text="Armor Proficiencies: ")
        lbl_feat_armor.grid(row=3, column=4, sticky='w')
        self.txt_feat_armor = tk.Text(master=self.input_frame, height=4, width=70, bg='gray28', fg='white')
        self.txt_feat_armor.grid(row=4, column=4, columnspan=2)
        self.txt_feat_armor.config(state='disabled')
        self.feat_lang = tk.IntVar()
        cbn_feat_lang = ttk.Checkbutton(master=self.input_frame, variable=self.feat_lang, command=self._toggle_feat_lang)
        cbn_feat_lang.grid(row=5, column=3, sticky='w')
        lbl_feat_lang = ttk.Label(master=self.input_frame, text="Languages: ")
        lbl_feat_lang.grid(row=5, column=4, sticky='w')
        lang_frame = ttk.Frame(master=self.input_frame)
        lang_frame.grid(row=6, column=4, columnspan=2, sticky='w')
        lbl_l1 = ttk.Label(master=lang_frame, text="1: ")
        lbl_l1.grid(row=0, column=0)
        self.ent_flang_1 = ttk.Entry(master=lang_frame, width=20)
        self.ent_flang_1.grid(row=0, column=1, padx=10, pady=10)
        self.ent_flang_1.state(['disabled'])
        lbl_l2 = ttk.Label(master=lang_frame, text="2: ")
        lbl_l2.grid(row=0, column=2)
        self.ent_flang_2 = ttk.Entry(master=lang_frame, width=20)
        self.ent_flang_2.grid(row=0, column=3, padx=10, pady=10)
        self.ent_flang_2.state(['disabled'])
        lbl_l3 = ttk.Label(master=lang_frame, text="3: ")
        lbl_l3.grid(row=1, column=0)
        self.ent_flang_3 = ttk.Entry(master=lang_frame, width=20)
        self.ent_flang_3.grid(row=1, column=1, padx=10, pady=10)
        self.ent_flang_3.state(['disabled'])
        lbl_l4 = ttk.Label(master=lang_frame, text="4: ")
        lbl_l4.grid(row=1, column=2)
        self.ent_flang_4 = ttk.Entry(master=lang_frame, width=20)
        self.ent_flang_4.grid(row=1, column=3, padx=10, pady=10)
        self.ent_flang_4.state(['disabled'])
        self.feat_feats = tk.IntVar()
        cbn_features = ttk.Checkbutton(master=self.input_frame, variable=self.feat_feats, command=self._toggle_feat_feats)
        cbn_features.grid(row=7, column=3, sticky='w')
        lbl_features = ttk.Label(master=self.input_frame, text="Features: ")
        lbl_features.grid(row=7, column=4, sticky='w')
        self.txt_feat_feats = tk.Text(master=self.input_frame, height=8, width=70, bg='gray28', fg='white')
        self.txt_feat_feats.grid(row=8, column=4, columnspan=2, sticky='w')
        self.txt_feat_feats.config(state='disabled')
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_feat, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def build_bkgd(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Background", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, columnspan=2, sticky='w')
        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=1, column=0, sticky='w')
        self.ent_name_bkgd = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name_bkgd.grid(row=1, column=1, sticky='w')
        lbl_prof = ttk.Label(master=self.input_frame, text="Proficiencies: ")
        lbl_prof.grid(row=1, column=2, sticky='w')
        self.ent_prof = ttk.Entry(master=self.input_frame, width=40)
        self.ent_prof.grid(row=1, column=3, sticky='w')
        #lbl_skills = ttk.Label(master=self.input_frame, text="")
        #lbl_skills.grid(row=2, column=0, columnspan=4)
        skill_titles = []
        for item in self.skill_list:
            if "_" in item:
                item = item.split("_")
                item = " ".join(item)
            skill_titles.append(item.title())
        
        lbl_skill_1 = ttk.Label(master=self.input_frame, text="Skill 1: ")
        lbl_skill_1.grid(row=3, column=0, sticky='w')
        self.cbx_skill_1 = ttk.Combobox(master=self.input_frame, width=20, values=skill_titles, state='readonly')
        self.cbx_skill_1.grid(row=3, column=1, sticky='w')
        self.cbx_skill_1.bind("<<ComboboxSelected>>", lambda e: self._on_select_skill(box=1))
        lbl_skill_2 = ttk.Label(master=self.input_frame, text="Skill 2: ")
        lbl_skill_2.grid(row=3, column=2, sticky='w')
        self.cbx_skill_2 = ttk.Combobox(master=self.input_frame, width=20, values=skill_titles, state='readonly')
        self.cbx_skill_2.grid(row=3, column=3, sticky='w')
        self.cbx_skill_2.bind("<<ComboboxSelected>>", lambda e: self._on_select_skill(box=2))
        lbl_choice_1 = ttk.Label(master=self.input_frame, text="Choice: ")
        lbl_choice_1.grid(row=4, column=0, sticky='nw')
        skill_frame_1 = ttk.Frame(master=self.input_frame)
        skill_frame_1.grid(row=4, column=1, sticky='w', padx=10)
        lbl_choice_2 = ttk.Label(master=self.input_frame, text="Choice: ")
        lbl_choice_2.grid(row=4, column=2, sticky='nw')
        skill_frame_2 = ttk.Frame(master=self.input_frame)
        skill_frame_2.grid(row=4, column=3, sticky='w', padx=10)
        self.skill_var_1 = []
        self.skill_var_2 = []
        self.cbn_1 = []
        self.cbn_2 = []
        row_num = 0
        col_num = 0
        for i in range(18):
            self.skill_var_1.append(tk.IntVar())
            self.skill_var_2.append(tk.IntVar())
            cbn_skill_1 = ttk.Checkbutton(master=skill_frame_1, text=skill_titles[i], variable=self.skill_var_1[i])
            cbn_skill_1.grid(row=row_num, column=col_num, sticky='w')
            cbn_skill_1.state(['disabled'])
            self.cbn_1.append(cbn_skill_1)
            cbn_skill_2 = ttk.Checkbutton(master=skill_frame_2, text=skill_titles[i], variable=self.skill_var_2[i])
            cbn_skill_2.grid(row=row_num, column=col_num, sticky='w')
            cbn_skill_2.state(['disabled'])
            self.cbn_2.append(cbn_skill_2)
            row_num += 1
            if row_num >= 5:
                row_num = 0
                col_num += 1
        
        lbl_languages = ttk.Label(master=self.input_frame, text="Number of Languages: ")
        lbl_languages.grid(row=5, column=0, sticky='w', pady=5)
        self.ent_lang_num = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_num.grid(row=5, column=1, sticky='w')
        self.ent_lang_num.insert(0, '0')
        lbl_gold = ttk.Label(master=self.input_frame, text="Gold: ")
        lbl_gold.grid(row=5, column=2, sticky='w')
        self.ent_gold = ttk.Entry(master=self.input_frame, width=20)
        self.ent_gold.grid(row=5, column=3, sticky='w')
        self.ent_gold.insert(0, '0')
        lbl_equip = ttk.Label(master=self.input_frame, text="Equipment: ")
        lbl_equip.grid(row=6, column=0, sticky='w')
        self.txt_equip = tk.Text(master=self.input_frame, height=5, width=110, bg='gray28', fg='white')
        self.txt_equip.grid(row=7, column=0, columnspan=4, pady=15)
        lbl_feature = ttk.Label(master=self.input_frame, text="Feature: ")
        lbl_feature.grid(row=8, column=0, sticky='w')
        self.txt_feature = tk.Text(master=self.input_frame, height=10, width=110, bg='gray28', fg='white')
        self.txt_feature.grid(row=9, column=0, columnspan=4, pady=15)
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_bkgd, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def build_weap(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Weapon", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, columnspan=2, sticky='w')
        lbl_name = ttk.Label(master=self.input_frame, text="Name: ")
        lbl_name.grid(row=1, column=0, sticky='w')
        self.ent_name_weap = ttk.Entry(master=self.input_frame, width=20)
        self.ent_name_weap.grid(row=1, column=1, sticky='w')
        lbl_catg_weap = ttk.Label(master=self.input_frame, text="Category: ")
        lbl_catg_weap.grid(row=2, column=0, sticky='w')
        self.catg_weap = tk.StringVar()
        rbn_simple = ttk.Radiobutton(master=self.input_frame, text="Simple", variable=self.catg_weap, value='s')
        rbn_simple.grid(row=2, column=1, sticky='w')
        rbn_martial = ttk.Radiobutton(master=self.input_frame, text="Martial", variable=self.catg_weap, value='m')
        rbn_martial.grid(row=2, column=2, sticky='w')
        self.catg_weap.set('s')
        lbl_range = ttk.Label(master=self.input_frame, text="Range: ")
        lbl_range.grid(row=3, column=0, sticky='w')
        self.range = tk.StringVar()
        rbn_melee = ttk.Radiobutton(master=self.input_frame, text="Melee", variable=self.range, value='m', command=self._toggle_range)
        rbn_melee.grid(row=3, column=1, sticky='w')
        rbn_ranged = ttk.Radiobutton(master=self.input_frame, text="Ranged", variable=self.range, value='r', command=self._toggle_range)
        rbn_ranged.grid(row=3, column=2, sticky='w')
        self.reach = tk.IntVar()
        self.cbn_reach = ttk.Checkbutton(master=self.input_frame, text="Reach", variable=self.reach)
        self.cbn_reach.grid(row=4, column=1, sticky='w')
        self.cbn_reach.state(['disabled'])
        range_frame = ttk.Frame(master=self.input_frame)
        range_frame.grid(row=4, column=2, sticky='w')
        self.ent_range_norm = ttk.Entry(master=range_frame, width=5)
        self.ent_range_norm.grid(row=0, column=0, sticky='w')
        self.ent_range_norm.state(['disabled'])
        lbl_slash = ttk.Label(master=range_frame, text="/")
        lbl_slash.grid(row=0, column=1, sticky='w')
        self.ent_range_dis = ttk.Entry(master=range_frame, width=5)
        self.ent_range_dis.grid(row=0, column=2, sticky='w')
        self.ent_range_dis.state(['disabled'])
        rbn_melee.invoke()
        lbl_dmg_weap = ttk.Label(master=self.input_frame, text="Damage: ")
        lbl_dmg_weap.grid(row=5, column=0, sticky='w')
        dmg_frame = ttk.Frame(master=self.input_frame)
        dmg_frame.grid(row=5, column=1, columnspan=2, sticky='w')
        self.ent_dmg_num = ttk.Entry(master=dmg_frame, width=5)
        self.ent_dmg_num.grid(row=0, column=0)
        lbl_d = ttk.Label(master=dmg_frame, text='d')
        lbl_d.grid(row=0, column=1, padx=5)
        self.ent_dmg_die = ttk.Entry(master=dmg_frame, width=5)
        self.ent_dmg_die.grid(row=0, column=2)
        self.no_dmg = tk.IntVar()
        self.cbn_no_damage = ttk.Checkbutton(master=self.input_frame, text="No Damage", variable=self.no_dmg, command=self._toggle_no_dmg)
        self.cbn_no_damage.grid(row=5, column=2, sticky='w')
        lbl_vers = ttk.Label(master=self.input_frame, text="(If versatile, use one-hand damage.)", font=self.small_font)
        lbl_vers.grid(row=6, column=0, columnspan=3, sticky='w')
        lbl_weap_prop = ttk.Label(master=self.input_frame, text="Properties: ")
        lbl_weap_prop.grid(row=1, column=3, sticky='w')
        prop_frame = ttk.Frame(master=self.input_frame)
        prop_frame.grid(row=1, column=4, rowspan=6)
        self.weap_props = []
        row_pos = 0
        col_pos = 0
        for i in range(12):
            self.weap_props.append(tk.IntVar())
            cbn_prop = ttk.Checkbutton(
                master=prop_frame,
                text=self.prop_list[i],
                variable=self.weap_props[i]
            )
            cbn_prop.grid(row=row_pos, column=col_pos, sticky='w', padx=5, pady=5)
            col_pos += 1
            if col_pos >= 4:
                col_pos = 0
                row_pos += 1
        lbl_dmg_weap_type = ttk.Label(master=self.input_frame, text="Damage Type: ")
        lbl_dmg_weap_type.grid(row=7, column=0, sticky='w')
        self.dmg_weap_type = tk.StringVar()
        self.rbn_bludg = ttk.Radiobutton(master=self.input_frame, text="Bludgeoning", variable=self.dmg_weap_type, value='b')
        self.rbn_bludg.grid(row=7, column=1, sticky='w')
        self.rbn_pierc = ttk.Radiobutton(master=self.input_frame, text="Piercing", variable=self.dmg_weap_type, value='p')
        self.rbn_pierc.grid(row=8, column=1, sticky='w')
        self.rbn_slash = ttk.Radiobutton(master=self.input_frame, text="Slashing", variable=self.dmg_weap_type, value='s')
        self.rbn_slash.grid(row=9, column=1, sticky='w')
        self.dmg_weap_type.set('b')
        btn_send = ttk.Button(master=self.send_it_frame, text="Send", command=self.send_weap)
        btn_send.grid(row=0, column=0, pady=15)

    def on_off_switch(self):
        if self.mean_mode:
            self.mean_mode = False
            self.btn_mean_mode.config(image=self.off_img)
            self.btn_mean_mode.image = self.off_img
        else:
            self.mean_mode = True
            self.btn_mean_mode.config(image=self.on_img)
            self.btn_mean_mode.image = self.on_img

    def send_npc_m(self):
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
        get_init = self.ent_init.get()
        get_dmg_vuln = self.txt_dmg_vuln.get(1.0, 'end-1c')
        get_dmg_res = self.txt_dmg_res.get(1.0, 'end-1c')
        get_dmg_immn = self.txt_dmg_immn.get(1.0, 'end-1c')
        get_cond_immn = self.txt_cond_immn.get(1.0, 'end-1c')

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

        get_prof_str = self.prof_str.get()
        get_prof_dex = self.prof_dex.get()
        get_prof_con = self.prof_con.get()
        get_prof_int = self.prof_int.get()
        get_prof_wis = self.prof_wis.get()
        get_prof_cha = self.prof_cha.get()

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
            get_init = int(get_init)
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
        get_name = get_name.title()
        get_type = get_type.lower()

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

        stat_array = [get_str, get_dex, get_con, get_int, get_wis, get_cha]
        stat_matrix = []
        for stat in stat_array:
            stat = math.floor((stat - 10) / 2)
            stat_matrix.append(stat)

        save_list = []
        get_saves = [get_prof_str, get_prof_dex, get_prof_con, get_prof_int, get_prof_wis, get_prof_cha]
        for i in range(6):
            save_mod = stat_matrix[i]
            if get_saves[i] == 1:
                save_mod += cr_prof_mod
            save_list.append(save_mod)

        init_bonus = stat_matrix[1] + get_init

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
                'initiative': [None, init_bonus],
                'raw_stats': [
                    get_str,
                    get_dex,
                    get_con,
                    get_int,
                    get_wis, 
                    get_cha
                ],
                'mod_stats': stat_matrix,
                'saves': save_list,
                'dmg_vuln': get_dmg_vuln,
                'dmg_res': get_dmg_res,
                'dmg_immn': get_dmg_immn,
                'cond_immn': get_cond_immn,
                'senses': get_senses,
                'languages': get_lang,
                'cr': [get_cr, cr_prof_mod],
                'skills': {
                    'athletics': skill_matrix[0],
                    'acrobatics': skill_matrix[1],
                    'sleight_of_hand': skill_matrix[2],
                    'stealth': skill_matrix[3],
                    'arcana': skill_matrix[4],
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

        if os.path.exists(self.npc_m_loc) == False:
            with open(self.npc_m_loc, 'w') as template_file:
                json.dump({'npc':{}, 'monster': {}}, template_file, indent=4)
        with open(self.npc_m_loc, 'r') as template_file:
            self.template_info = json.load(template_file)
        self.template_info[self.catg].update(template_dict)
        with open(self.npc_m_loc, 'w') as template_file:
            json.dump(self.template_info, template_file, indent=4)

    def send_race(self):
        race_name = self.ent_name_race.get()
        race_size = self.size_race.get()
        speed_walk = self.ent_gnd_speed.get()
        speed_fly = self.ent_fly_speed.get()
        speed_swim = self.ent_swim_speed.get()
        speed_burrow = self.ent_burrow_speed.get()
        get_str_mod = self.ent_str_mod.get()
        get_dex_mod = self.ent_dex_mod.get()
        get_con_mod = self.ent_con_mod.get()
        get_int_mod = self.ent_int_mod.get()
        get_wis_mod = self.ent_wis_mod.get()
        get_cha_mod = self.ent_cha_mod.get()
        lang_1 = self.ent_lang_1.get()
        lang_2 = self.ent_lang_2.get()
        lang_3 = self.ent_lang_3.get()
        lang_4 = self.ent_lang_4.get()
        racial_abil = self.txt_racials.get(1.0, 'end-1c')

        if race_name == "" or race_size == "" or racial_abil == "":
            messagebox.showwarning("Forge", "Name, size, and abilities cannot be empty.")
            return

        race_name = race_name.title()

        try:
            speed_walk = int(speed_walk)
            get_str_mod = int(get_str_mod)
            get_dex_mod = int(get_dex_mod)
            get_con_mod = int(get_con_mod)
            get_int_mod = int(get_int_mod)
            get_wis_mod = int(get_wis_mod)
            get_cha_mod = int(get_cha_mod)
        except ValueError:
            messagebox.showwarning("Forge", "Walking speed and modifier fields must be whole numbers")
            return

        if speed_fly != "":
            try:
                speed_fly = int(speed_fly)
            except:
                messagebox.showwarning("Forge", "If entered, flying speed must be a whole number.")
                return
        else:
            speed_fly = None

        if speed_swim != "":
            try:
                speed_swim = int(speed_swim)
            except:
                messagebox.showwarning("Forge", "If entered, swim speed must be a whole number.")
                return
        else:
            speed_swim = None

        if speed_burrow != "":
            try:
                speed_burrow = int(speed_burrow)
            except:
                messagebox.showwarning("Forge", "If entered, burrow speed must be a whole number.")
                return
        else:
            speed_burrow = None
        
        race_dict = {
            race_name: {
                "stat_bonus": [
                    get_str_mod,
                    get_dex_mod,
                    get_con_mod,
                    get_int_mod,
                    get_wis_mod,
                    get_cha_mod
                ],
                "size": race_size,
                "speed_walk": speed_walk,
                "speed_fly": speed_fly,
                "speed_swim": speed_swim,
                "speed_burrow": speed_burrow,
                "languages": [
                    lang_1,
                    lang_2,
                    lang_3,
                    lang_4
                ],
                "notes": racial_abil,
                "subrace": {}
            }
        }

        if os.path.exists(self.race_loc) == False:
            with open(self.race_loc, 'w') as race_file:
                json.dump(race_dict, race_file, indent=4)
        else:
            with open(self.race_loc, 'r') as race_file:
                race_info = json.load(race_file)
            race_info.update(race_dict)
            with open(self.race_loc, 'w') as race_file:
                json.dump(race_info, race_file, indent=4)

    def send_subrace(self):
        sel_race = self.cbx_races_sub.get()
        subrace_name = self.ent_name_race_sub.get()
        subrace_size = self.size_race_sub.get()
        speed_walk = self.ent_gnd_speed_sub.get()
        speed_fly = self.ent_fly_speed_sub.get()
        speed_swim = self.ent_swim_speed_sub.get()
        speed_burrow = self.ent_burrow_speed_sub.get()
        get_str_mod = self.ent_str_mod_sub.get()
        get_dex_mod = self.ent_dex_mod_sub.get()
        get_con_mod = self.ent_con_mod_sub.get()
        get_int_mod = self.ent_int_mod_sub.get()
        get_wis_mod = self.ent_wis_mod_sub.get()
        get_cha_mod = self.ent_cha_mod_sub.get()
        lang_1 = self.ent_lang_1_sub.get()
        lang_2 = self.ent_lang_2_sub.get()
        lang_3 = self.ent_lang_3_sub.get()
        lang_4 = self.ent_lang_4_sub.get()
        racial_abil = self.txt_racials_sub.get(1.0, 'end-1c')

        if sel_race == "":
            messagebox.showwarning("Forge", "Must select base race.")
            return

        if subrace_name == "" or subrace_size == "" or racial_abil == "":
            messagebox.showwarning("Forge", "Name, size, and abilities cannot be empty.")
            return

        subrace_name = subrace_name.title()

        try:
            speed_walk = int(speed_walk)
            get_str_mod = int(get_str_mod)
            get_dex_mod = int(get_dex_mod)
            get_con_mod = int(get_con_mod)
            get_int_mod = int(get_int_mod)
            get_wis_mod = int(get_wis_mod)
            get_cha_mod = int(get_cha_mod)
        except ValueError:
            messagebox.showwarning("Forge", "Walking speed and modifier fields must be whole numbers")
            return

        if speed_fly != "":
            try:
                speed_fly = int(speed_fly)
            except:
                messagebox.showwarning("Forge", "If entered, flying speed must be a whole number.")
                return
        else:
            speed_fly = None

        if speed_swim != "":
            try:
                speed_swim = int(speed_swim)
            except:
                messagebox.showwarning("Forge", "If entered, swim speed must be a whole number.")
                return
        else:
            speed_swim = None

        if speed_burrow != "":
            try:
                speed_burrow = int(speed_burrow)
            except:
                messagebox.showwarning("Forge", "If entered, burrow speed must be a whole number.")
                return
        else:
            speed_burrow = None
        
        subrace_dict = {
            subrace_name: {
                "stat_bonus": [
                    get_str_mod,
                    get_dex_mod,
                    get_con_mod,
                    get_int_mod,
                    get_wis_mod,
                    get_cha_mod
                ],
                "size": subrace_size,
                "speed_walk": speed_walk,
                "speed_fly": speed_fly,
                "speed_swim": speed_swim,
                "speed_burrow": speed_burrow,
                "languages": [
                    lang_1,
                    lang_2,
                    lang_3,
                    lang_4
                ],
                "notes": racial_abil
            }
        }

        with open(self.race_loc, 'r') as race_file:
            race_info = json.load(race_file)
        race_info[sel_race]["subrace"].update(subrace_dict)
        with open(self.race_loc, 'w') as race_file:
            json.dump(race_info, race_file, indent=4)

    def send_feat(self):
        feat_name = self.ent_name_feat.get()
        feat_has_stat = self.stat_inc.get()
        feat_has_weap = self.prof_weap.get()
        feat_has_skill = self.stat_prof.get()
        feat_has_tool = self.prof_tool.get()
        feat_has_armor = self.feat_armor.get()
        feat_has_lang = self.feat_lang.get()
        feat_has_feat = self.feat_feats.get()

        if feat_name == "":
            messagebox.showwarning("Forge", "Enter a name for the feat.")
            return
        feat_name = feat_name.title()

        if feat_has_stat == 1:
            inc_stat_choice = []
            for i in range(6):
                inc_stat_choice.append(self.stat_vars[i].get())
            if 1 not in inc_stat_choice:
                messagebox.showwarning("Forge", "Select possible stat increase choices.")
                return
        else:
            inc_stat_choice = None
        
        if feat_has_weap == 1:
            limited_opt = None
            if self.feat_limited.get() == 1:
                weap_list = []
                for wp in self.char_weap_list.curselection():
                    weap_list.append(wp)
                if len(wp) < 1:
                    messagebox.showwarning("Forge", "Add limited weapon proficiencies.")
                    return
                limited_opt = weap_list
                simple_opt = False
                martial_opt = False
            else:
                simple_opt = self.feat_simple.get() == 1
                martial_opt = self.feat_martial.get() == 1
                if simple_opt == False and martial_opt == False:
                    messagebox.showwarning("Forge", "Select weapon proficiencies.")
                    return
            weap_options = {
                "simple": simple_opt,
                "martial": martial_opt,
                "limited": limited_opt
            }
        else:
            weap_options = None
        
        if feat_has_skill == 1:
            skill_profs = {}
            for i in range(18):
                skill_profs[self.skill_list[i]] = self.skill_prof[i].get()
            if 1 not in skill_profs.values():
                messagebox.showwarning("Forge", "Select skill proficiencies.")
                return
            skill_choices = self.ent_skill_choices.get()
            if skill_choices == "":
                skill_choices = 0
            else:
                try:
                    skill_choices = int(skill_choices)
                    if skill_choices < 0:
                        messagebox.showwarning("Forge", "Skill proficiency choices must be a positive whole number.")
                        return
                    elif skill_choices > 18:
                        messagebox.showwarning("Forge", "Number of skill proficiency choices out of range.")
                        return
                except ValueError:
                    messagebox.showwarning("Forge", "Skill proficiency choices must be a positive whole number.")
                    return
        else:
            skill_profs = None
            skill_choices = 0

        if feat_has_tool == 1:
            tool_profs = self.txt_feat_tools.get(1.0, 'end-1c')
            if tool_profs == "":
                messagebox.showwarning("Forge", "Enter at least one tool proficiency.")
                return
        else:
            tool_profs = None

        if feat_has_armor == 1:
            armor_profs = self.txt_feat_armor.get(1.0, 'end-1c')
            if armor_profs == "":
                messagebox.showwarning("Forge", "Enter at least one armor proficiency.")
                return
        else:
            armor_profs = None

        if feat_has_lang == 1:
            lang_profs = [
                self.ent_flang_1.get(),
                self.ent_flang_2.get(),
                self.ent_flang_3.get(),
                self.ent_flang_4.get()
            ]
            if lang_profs == ["", "", "", ""]:
                messagebox.showwarning("Forge", "Enter at least one language.")
                return
        else:
            lang_profs = None

        if feat_has_feat == 1:
            features = self.txt_feat_feats.get(1.0, 'end-1c')
            if features == "":
                messagebox.showwarning("Forge", "Enter at least one feature.")
                return
        else:
            features = None

        if feat_has_stat == 0 and feat_has_weap == 0 and feat_has_skill == 0 and feat_has_tool == 0 and feat_has_lang == 0 and feat_has_feat == 0:
            messagebox.showwarning("Forge", "Cannot enter a feat with only a name.")
            return

        feat_dict = {
            feat_name: {
                "stat_inc": inc_stat_choice,
                "weap_prof": weap_options,
                "skill_prof": (skill_profs, skill_choices),
                "tool_prof": tool_profs,
                "armor_prof": armor_profs,
                "lang_prof": lang_profs,
                "features": features
            }
        }

        if os.path.exists(self.feat_loc) == False:
            with open(self.feat_loc, 'w') as feat_file:
                json.dump(feat_dict, feat_file, indent=4)
        else:
            with open(self.feat_loc, 'r') as feat_file:
                feat_info = json.load(feat_file)
            feat_info.update(feat_dict)
            with open(self.feat_loc, 'w') as feat_file:
                json.dump(feat_info, feat_file, indent=4)

    def send_bkgd(self):
        bkgd_name = self.ent_name_bkgd.get()
        bkgd_prof = self.ent_prof.get()
        skill_1 = self.cbx_skill_1.get()
        skill_2 = self.cbx_skill_2.get()
        num_lang = self.ent_lang_num.get()
        gold = self.ent_gold.get()
        bkgd_equip = self.txt_equip.get(1.0, 'end-1c')
        bkgd_feature = self.txt_feature.get(1.0, 'end-1c')

        if bkgd_name == "" or skill_1 == "" or skill_2 == "" or num_lang == "" or gold == "":
            messagebox.showwarning("Forge", "Name, skills, number of languages, and gold fields cannot be empty.")
            return
        bkgd_name = bkgd_name.title()
        try:
            num_lang = int(num_lang)
            gold = int(gold)
        except ValueError:
            messagebox.showwarning("Forge", "Number of languages and gold must be whole numbers.")
            return

        pick_skills_1 = []
        if skill_1 == "Choice":
            for i in range(18):
                if self.skill_var_1[i] == 1:
                    pick_skills_1.append(self.skill_list[i])
        pick_skills_2 = []
        if skill_2 == "Choice":
            for i in range(18):
                if self.skill_var_2[i] == 1:
                    pick_skills_2.append(self.skill_list[i])

        skill_1 = skill_1.lower()
        if " " in skill_1:
            skill_1 = skill_1.split()
            skill_1 = "_".join(skill_1)

        skill_2 = skill_2.lower()
        if " " in skill_2:
            skill_2 = skill_2.split()
            skill_2 = "_".join(skill_2)

        bkgd_dict = {
            bkgd_name: {
                "skills": {
                    skill_1: pick_skills_1,
                    skill_2: pick_skills_2
                },
                "proficiencies": bkgd_prof,
                "num_lang": num_lang,
                "gold": gold,
                "equipment": bkgd_equip,
                "feature": bkgd_feature
            }
        }

        if os.path.exists(self.bkgd_loc) == False:
            with open(self.bkgd_loc, 'w') as bkgd_file:
                json.dump(bkgd_dict, bkgd_file, indent=4)
        else:
            with open(self.bkgd_loc, 'r') as bkgd_file:
                bkgd_info = json.load(bkgd_file)
            bkgd_info.update(bkgd_dict)
            with open(self.bkgd_loc, 'w') as bkgd_file:
                json.dump(bkgd_info, bkgd_file, indent=4)

    def send_weap(self):
        weap_name = self.ent_name_weap.get()
        if weap_name == "":
            messagebox.showwarning("Forge", "Name cannot be empty.")
            return
        weap_name = weap_name.title()
        weap_catg = self.catg_weap.get()
        weap_range = self.range.get()
        if weap_range == 'm':
            weap_dist = 5 + (5 * self.reach.get())
        else:
            try:
                norm_range = int(self.ent_range_norm.get())
                dis_range = int(self.ent_range_dis.get())
            except ValueError:
                messagebox.showwarning("Forge", "Range values must be whole numbers.")
                return
            weap_dist = (norm_range, dis_range)
        try:
            dmg_dice_num = int(self.ent_dmg_num.get())
            dmg_dice = int(self.ent_dmg_die.get())
            if dmg_dice != 1 or dmg_dice != 4 or dmg_dice != 6 or dmg_dice != 8 or dmg_dice != 10 or dmg_dice != 12 or dmg_dice != 20 or dmg_dice != 100:
                messagebox.showwarning("Forge", "Damage die size must be a valid option.")
                return
            weap_dmg = (dmg_dice_num, dmg_dice)
        except ValueError:
            if self.no_dmg.get() == 1:
                weap_dmg = None
            else:
                messagebox.showwarning("Forge", "Damage dice number and size must be whole numbers.")
                return
        prop_array = []
        dmg_type = self.dmg_weap_type.get()
        for prop in self.weap_props:
            prop_array.append(prop.get())

        if prop_array[2] == 1 and prop_array[3] == 1:
            messagebox.showwarning("Forge", "Weapons cannot be both heavy and light.")
            return

        if prop_array[7] == 1 and prop_array[8] == 1:
            messagebox.showwarning("Forge", "Weapons cannot be both two-handed and versatile.")

        weap_dict = {
            weap_name: {
                "distance": weap_dist,
                "damage": weap_dmg,
                "type": dmg_type,
                "properties": prop_array
            }
        }

        if os.path.exists(self.weap_loc) == False:
            with open(self.weap_loc, 'w') as weap_file:
                json.dump({
                        "simple":{
                            "melee":{},
                            "ranged":{}
                        },
                        "martial":{
                            "melee":{},
                            "ranged":{}
                        }
                    },
                    weap_file,
                    indent=4
                    )

        with open(self.weap_loc, 'r') as weap_file:
            weap_info = json.load(weap_file)
        if weap_catg == 's':
            if weap_range == 'm':
                weap_info['simple']['melee'].update(weap_dict)
            else:
                weap_info['simple']['ranged'].update(weap_dict)
        else:
            if weap_range == 'm':
                weap_info['martial']['melee'].update(weap_dict)
            else:
                weap_info['martial']['ranged'].update(weap_dict)
        with open(self.weap_loc, 'w') as weap_file:
            json.dump(weap_info, weap_file, indent=4)

    def wipe_off(self):
        try:
            old_widg = self.input_frame.grid_slaves()
            if old_widg is not None:
                for widg in old_widg:
                    widg.destroy()
            send_btn = self.send_it_frame.grid_slaves()
            if send_btn is not None:
                for btn in send_btn:
                    btn.destroy()
        except AttributeError:
            pass

    def move_box(self, dir, orig):
        if orig == 'f':
            if dir == 'to':
                for i in self.from_weap_list.curselection():
                    self.char_weap_list.insert('end', self.from_weap_list.get(i))
                    self.from_weap_list.delete(i)
            else:
                for i in self.char_weap_list.curselection():
                    self.from_weap_list.insert('end', self.char_weap_list.get(i))
                    self.char_weap_list.delete(i)
        if orig == 'c':
            if dir == 'to':
                for i in self.opt_weap_list.curselection():
                    self.has_weap_list.insert('end', self.opt_weap_list.get(i))
                    self.opt_weap_list.delete(i)
            else:
                for i in self.has_weap_list.curselection():
                    self.opt_weap_list.insert('end', self.has_weap_list.get(i))
                    self.has_weap_list.delete(i)

    def make_even(self, value):
        value = int(value)
        if value % 2:
            self.sldr_hit_dice.set(value+1 if value > self.past else value-1)
            self.past = self.sldr_hit_dice.get()

    def add_improv(self):
        enabled = True
        index = 0
        while enabled:
            if len(self.improv_ents[index].state()) > 0:
                self.improv_ents[index].state(['!disabled'])
                enabled = False
            elif index == 6:
                enabled = False
            index += 1

    def _on_select_race(self, event):
        mod_ent_list = [self.ent_str_mod_sub, self.ent_dex_mod_sub, self.ent_con_mod_sub, self.ent_int_mod_sub, self.ent_wis_mod_sub, self.ent_cha_mod_sub]
        sel_race = self.cbx_races_sub.get()
        for i in range(6):
            if self.race_info_sub[sel_race]['stat_bonus'][i] != 0:
                mod_ent_list[i].state(['disabled'])
            else:
                mod_ent_list[i].state(['!disabled'])

    def _on_select_skill(self, box):
        if box == 1:
            sel_skill = self.cbx_skill_1.get()
        else:
            sel_skill = self.cbx_skill_2.get()

        for i in range(18):
            if sel_skill == 'Choice':
                if box == 1:
                    self.cbn_1[i].state(['!disabled'])
                else:
                    self.cbn_2[i].state(['!disabled'])
            else:
                if box == 1:
                    self.cbn_1[i].state(['disabled'])
                else:
                    self.cbn_2[i].state(['disabled'])

    def _on_enter_canvas(self, event, lst, orig):
        if orig == 'f':
            if self.feat_limited.get() == 1:
                if lst == 'f':
                    self.from_weap_list.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e, lst))
                else:
                    self.char_weap_list.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e, lst))
        elif orig == 'c':
            if self.class_limited.get() == 1:
                if lst == 'f':
                    self.opt_weap_list.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e, lst))
                else:
                    self.has_weap_list.bind_all('<MouseWheel>', lambda e: self._on_mousewheel(e, lst))
    
    def _on_leave_canvas(self, event, lst, orig):
        if orig == 'f':
            if self.feat_limited.get() == 1:
                if lst == 'f':
                    self.from_weap_list.unbind_all('<MouseWheel>')
                else:
                    self.char_weap_list.unbind_all('<MouseWheel>')
        elif orig == 'c':
            if self.class_limited.get() == 1:
                if lst == 'f':
                    self.opt_weap_list.unbind_all('<MouseWheel>')
                else:
                    self.has_weap_list.unbind_all('<MouseWheel>')

    def _on_mousewheel(self, event, lst, orig):
        if orig == 'f':
            if lst == 'f':
                self.from_weap_list.yview_scroll(int(-1*(event.delta/120)), 'units')
            else:
                self.char_weap_list.yview_scroll(int(-1*(event.delta/120)), 'units')
        elif orig == 'c':
            if lst == 'f':
                self.opt_weap_list.yview_scroll(int(-1*(event.delta/120)), 'units')
            else:
                self.has_weap_list.yview_scroll(int(-1*(event.delta/120)), 'units')

    def _toggle_stats(self):
        if self.stat_inc.get() == 1:
            state = '!disabled'
        else:
            state = 'disabled'
        for stat in self.stat_cbns:
            stat.state([state])

    def _toggle_weap(self):
        if self.prof_weap.get() == 1:
            self.cbn_feat_simple.state(['!disabled'])
            self.cbn_feat_martial.state(['!disabled'])
            self.cbn_feat_limited.state(['!disabled'])
        else:
            self.cbn_feat_simple.state(['!selected', 'disabled'])
            self.cbn_feat_martial.state(['!selected', 'disabled'])
            self.cbn_feat_limited.state(['!selected', 'disabled'])
            self.from_weap_list.config(state='disabled')
            self.char_weap_list.config(state='disabled')
            self.btn_move_to_you.state(['disabled'])
            self.btn_move_from_you.state(['disabled'])

    def _toggle_limited(self, orig):
        if orig == 'f':
            if self.feat_limited.get() == 1:
                self.cbn_feat_simple.state(['!selected', 'disabled'])
                self.cbn_feat_martial.state(['!selected', 'disabled'])
                self.from_weap_list.config(state='normal')
                self.char_weap_list.config(state='normal')
                self.btn_move_to_you.state(['!disabled'])
                self.btn_move_from_you.state(['!disabled'])
            else:
                self.cbn_feat_simple.state(['!disabled'])
                self.cbn_feat_martial.state(['!disabled'])
                self.from_weap_list.config(state='disabled')
                self.char_weap_list.config(state='disabled')
                self.btn_move_to_you.state(['disabled'])
                self.btn_move_from_you.state(['disabled'])
        elif orig == 'c':
            if self.class_limited.get() == 1:
                self.cbn_class_simple.state(['!selected', 'disabled'])
                self.cbn_class_martial.state(['!selected', 'disabled'])
                self.opt_weap_list.config(state='normal')
                self.has_weap_list.config(state='normal')
                self.btn_move_to_char.state(['!disabled'])
                self.btn_move_from_char.state(['!disabled'])
            else:
                self.cbn_class_simple.state(['!disabled'])
                self.cbn_class_martial.state(['!disabled'])
                self.opt_weap_list.config(state='disabled')
                self.has_weap_list.config(state='disabled')
                self.btn_move_to_char.state(['disabled'])
                self.btn_move_from_char.state(['disabled'])

    def _toggle_range(self):
        if self.range.get() == 'm':
            self.cbn_reach.state(['!disabled'])
            self.ent_range_norm.delete(0, 'end')
            self.ent_range_norm.state(['disabled'])
            self.ent_range_dis.delete(0, 'end')
            self.ent_range_dis.state(['disabled'])
        else:
            self.cbn_reach.state(['disabled', '!selected'])
            self.ent_range_norm.state(['!disabled'])
            self.ent_range_dis.state(['!disabled'])

    def _toggle_no_dmg(self):
        if self.no_dmg.get() == 1:
            self.dmg_weap_type.set('')
            self.rbn_bludg.state(['disabled'])
            self.rbn_pierc.state(['disabled'])
            self.rbn_slash.state(['disabled'])
            self.ent_dmg_num.delete(0, 'end')
            self.ent_dmg_num.state(['disabled'])
            self.ent_dmg_die.delete(0, 'end')
            self.ent_dmg_die.state(['disabled'])
        else:
            self.dmg_weap_type.set('b')
            self.rbn_bludg.state(['!disabled'])
            self.rbn_pierc.state(['!disabled'])
            self.rbn_slash.state(['!disabled'])
            self.ent_dmg_num.state(['!disabled'])
            self.ent_dmg_die.state(['!disabled'])

    def _toggle_prof_stat(self):
        for i in range(18):
            if self.stat_prof.get() == 1:
                self.cbn_prof[i].state(['!disabled'])
            else:
                self.cbn_prof[i].state(['!selected','disabled'])
        if self.stat_prof.get() == 1:
            self.ent_skill_choices.state(['!disabled'])
        else:
            self.ent_skill_choices.delete(0, 'end')
            self.ent_skill_choices.state(['disabled'])

    def _toggle_prof_tool(self):
        if self.prof_tool.get() == 1:
            self.txt_feat_tools.config(state='normal')
        else:
            self.txt_feat_tools.delete(1.0, 'end')
            self.txt_feat_tools.config(state='disabled')

    def _toggle_feat_armor(self):
        if self.feat_armor.get() == 1:
            self.txt_feat_armor.config(state='normal')
        else:
            self.txt_feat_armor.delete(1.0, 'end')
            self.txt_feat_armor.config(state='disabled')

    def _toggle_feat_lang(self):
        if self.feat_lang.get() == 1:
            self.ent_flang_1.state(['!disabled'])
            self.ent_flang_2.state(['!disabled'])
            self.ent_flang_3.state(['!disabled'])
            self.ent_flang_4.state(['!disabled'])
        else:
            self.ent_flang_1.delete(0, 'end')
            self.ent_flang_2.delete(0, 'end')
            self.ent_flang_3.delete(0, 'end')
            self.ent_flang_4.delete(0, 'end')
            self.ent_flang_1.state(['disabled'])
            self.ent_flang_2.state(['disabled'])
            self.ent_flang_3.state(['disabled'])
            self.ent_flang_4.state(['disabled'])

    def _toggle_feat_feats(self):
        if self.feat_feats.get() == 1:
            self.txt_feat_feats.config(state='normal')
        else:
            self.txt_feat_feats.delete(1.0, 'end')
            self.txt_feat_feats.config(state='disabled')

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
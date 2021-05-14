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


class TemplateBuilder():
    def __init__(self, root):
        self.root = root
        self.npc_m_loc = 'entry\\bin\\npc_monster.json'
        self.race_loc = 'entry\\bin\\race_lib.json'
        self.class_loc = 'entry\\bin\\class_lib.json'
        self.feat_loc = 'entry\\bin\\feat_lib.json'
        self.bkgd_loc = 'entry\\bin\\background_lib.json'
        lbl_title = ttk.Label(master=self.root, text="What would you like to build?")
        lbl_title.grid(row=0, column=0)
        self.underline_font = font.Font(lbl_title, lbl_title.cget("font"))
        self.underline_font.configure(underline = True)
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
        btn_class = ttk.Button(master=catg_frame, command=lambda: self.build_class('c'), text="Class")
        btn_class.grid(row=0, column=3, sticky='w', padx=5, pady=10)
        btn_archtype = ttk.Button(master=catg_frame, command=lambda: self.build_class('a'), text="Arch Type")
        btn_archtype.grid(row=0, column=4, sticky='w', padx=5, pady=10)
        btn_feat = ttk.Button(master=catg_frame, command=self.build_feat, text="Feat")
        btn_feat.grid(row=0, column=5, sticky='w', padx=5, pady=10)
        btn_bkgd = ttk.Button(master=catg_frame, command=self.build_bkgd, text="Background")
        btn_bkgd.grid(row=0, column=6, sticky='w', padx=5, pady=10)
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
        lbl_init = ttk.Label(master=self.input_frame, text="Special Initiative Bonuses: ")
        lbl_init.grid(row=12, column=0, sticky='w')
        self.ent_init = ttk.Entry(master=self.input_frame, width=20)
        self.ent_init.grid(row=12, column=1, sticky='w')
        self.ent_init.insert(0, "0")
        lbl_dmg_vuln = ttk.Label(master=self.input_frame, text="Damage Vulnerabilities: ")
        lbl_dmg_vuln.grid(row=13, column=0, sticky='w')
        self.txt_dmg_vuln = tk.Text(master=self.input_frame, height=2, width=30)
        self.txt_dmg_vuln.grid(row=13, column=1, sticky='w')
        lbl_dmg_res = ttk.Label(master=self.input_frame, text="Damage Resistances: ")
        lbl_dmg_res.grid(row=14, column=0, sticky='w')
        self.txt_dmg_res = tk.Text(master=self.input_frame, height=2, width=30)
        self.txt_dmg_res.grid(row=14, column=1, sticky='w')
        lbl_dmg_immn = ttk.Label(master=self.input_frame, text="Damage Immunities: ")
        lbl_dmg_immn.grid(row=15, column=0, sticky='w')
        self.txt_dmg_immn = tk.Text(master=self.input_frame, height=2, width=30)
        self.txt_dmg_immn.grid(row=15, column=1, sticky='w')
        lbl_cond_immn = ttk.Label(master=self.input_frame, text="Condition Immunities: ")
        lbl_cond_immn.grid(row=16, column=0, sticky='w')
        self.txt_cond_immn = tk.Text(master=self.input_frame, height=2, width=30)
        self.txt_cond_immn.grid(row=16, column=1, sticky='w')
        
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
        btn_send_it = ttk.Button(master=self.send_it_frame, command=self.send_npc_m, text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)

    def build_race(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Race", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')
        lbl_size = ttk.Label(master=self.input_frame, text="Size: ")
        lbl_size.grid(row=1, column=0, sticky='w')
        self.ent_size = ttk.Entry(master=self.input_frame, width=20)
        self.ent_size.grid(row=1, column=1, sticky='w')
        lbl_walk_speed = ttk.Label(master=self.input_frame, text="Walking Speed: ")
        lbl_walk_speed.grid(row=2, column=0, sticky='w')
        self.ent_gnd_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_gnd_speed.grid(row=2, column=1, sticky='w')
        lbl_fly_speed = ttk.Label(master=self.input_frame, text="Flying Speed: ")
        lbl_fly_speed.grid(row=3, column=0, sticky='w')
        self.ent_fly_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_fly_speed.grid(row=3, column=1, sticky='w')
        lbl_swim_speed = ttk.Label(master=self.input_frame, text="Swim Speed: ")
        lbl_swim_speed.grid(row=4, column=0, sticky='w')
        self.ent_swim_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_swim_speed.grid(row=4, column=1, sticky='w')
        lbl_burrow_speed = ttk.Label(master=self.input_frame, text="Burrow Speed: ")
        lbl_burrow_speed.grid(row=5, column=0, sticky='w')
        self.ent_burrow_speed = ttk.Entry(master=self.input_frame, width=20)
        self.ent_burrow_speed.grid(row=5, column=1, sticky='w')
        lbl_stats = ttk.Label(master=self.input_frame, text="Bonuses: ")
        lbl_stats.grid(row=6, column=0, columnspan=2)
        stat_frame = ttk.Frame(master=self.input_frame)
        stat_frame.grid(row=7, column=0, columnspan=2)
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
        lbl_langs.grid(row=8, column=0, sticky='w')
        lbl_lang_1 = ttk.Label(master=self.input_frame, text="1: ")
        lbl_lang_1.grid(row=9, column=0, sticky='e')
        self.ent_lang_1 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_1.grid(row=9, column=1, sticky='w')
        lbl_lang_2 = ttk.Label(master=self.input_frame, text="2: ")
        lbl_lang_2.grid(row=10, column=0, sticky='e')
        self.ent_lang_2 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_2.grid(row=10, column=1, sticky='w')
        lbl_lang_3 = ttk.Label(master=self.input_frame, text="3: ")
        lbl_lang_3.grid(row=11, column=0, sticky='e')
        self.ent_lang_3 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_3.grid(row=11, column=1, sticky='w')
        lbl_lang_4 = ttk.Label(master=self.input_frame, text="4: ")
        lbl_lang_4.grid(row=12, column=0, sticky='e')
        self.ent_lang_4 = ttk.Entry(master=self.input_frame, width=20)
        self.ent_lang_4.grid(row=12, column=1, sticky='w')
        lbl_abilities = ttk.Label(master=self.input_frame, text="Abilities: ")
        lbl_abilities.grid(row=0, column=2, sticky='w', padx=30)
        self.txt_racials = tk.Text(master=self.input_frame)
        self.txt_racials.grid(row=1, column=2, rowspan=12, sticky='w', padx=30)
        btn_send_it = ttk.Button(master=self.send_it_frame, command=lambda: self.send_it('race'), text="Send", width=20)
        btn_send_it.grid(row=0, column=0, pady=15)
        

    def build_class(self, layer):
        self.wipe_off()
        if layer == 'c':
            mode = "Class"
        else:
            mode = "Arch Type"
        lbl_mode = ttk.Label(master=self.input_frame, text=mode, font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

    def build_feat(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Feat", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

    def build_bkgd(self):
        self.wipe_off()
        lbl_mode = ttk.Label(master=self.input_frame, text="Background", font=self.underline_font)
        lbl_mode.grid(row=0, column=0, sticky='w')

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

        stat_list = [get_str, get_dex, get_con, get_int, get_wis, get_cha]
        stat_matrix = []
        for stat in stat_list:
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
        pass

    def wipe_off(self):
        try:
            old_widg = self.input_frame.grid_slaves()
            if old_widg is not None:
                for widg in old_widg:
                    widg.destroy()
        except AttributeError:
            pass

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
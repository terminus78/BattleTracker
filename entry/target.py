import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle
from collections import deque

from dice import DiceRoller


class Target():
    def __init__(self, root):
        self.root = root
        self.dice = DiceRoller()

    def target_window(self):
        self.reg_font = ("Papyrus", "12")
        self.small_font = ("Papyrus", "11")
        self.big_font = ("Papyrus", "16")
        self.target_win = tk.Toplevel(self.root)
        self.target_win.title("Target Creature")
        style = ThemedStyle(self.target_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.target_win.configure(bg=style.lookup('TLabel', 'background'))
        self.top_frame = ttk.Frame(master=self.target_win)
        self.top_frame.grid(row=0, column=0, columnspan=2)
        self.select_frame = ttk.Frame(master=self.target_win)
        self.select_frame.grid(row=1, column=0, columnspan=2)
        self.stat_frame = ttk.Frame(master=self.target_win, borderwidth=2, relief='ridge')
        self.stat_frame.grid(row=2, column=0, sticky='nw', padx=5)
        self.stat_frame.rowconfigure([0,1,2,3,4,5,6,7], weight=1)
        self.target_win.rowconfigure(2, weight=1)
        self.target_win.columnconfigure([0,1], weight=1)
        self.action_frame = ttk.Frame(master=self.target_win, borderwidth=2, relief='ridge')
        self.action_frame.grid(row=2, column=1, sticky='nw', padx=5)
        self.submit_frame = ttk.Frame(master=self.target_win)
        self.submit_frame.grid(row=3, column=0, columnspan=2)
        self.names = []
        for being in self.root.token_list:
            self.names.append(being["name"])
        lbl_top_info = ttk.Label(master=self.top_frame, text="Select target creature and desired action.", font=self.reg_font)
        lbl_top_info.grid(row=0, column=0)
        self.drop_targets = ttk.Combobox(master=self.select_frame, width=27, values=self.names, state='readonly')
        self.drop_targets.grid(row=0, column=0, sticky='w')
        self.drop_targets.bind("<<ComboboxSelected>>", self.select_target)

        lbl_static_name = ttk.Label(self.stat_frame, text="Name: ", font=self.reg_font)
        lbl_static_name.grid(row=0, column=0, sticky='nw')
        lbl_static_status = ttk.Label(self.stat_frame, text="Status: ", font=self.reg_font)
        lbl_static_status.grid(row=1, column=0, sticky='nw')
        lbl_static_max_HP = ttk.Label(self.stat_frame, text="Max HP: ", font=self.reg_font)
        lbl_static_max_HP.grid(row=2, column=0, sticky='nw')
        lbl_static_temp_HP = ttk.Label(self.stat_frame, text="Temp HP: ", font=self.reg_font)
        lbl_static_temp_HP.grid(row=3, column=0, sticky='nw')
        lbl_static_HP = ttk.Label(self.stat_frame, text="Current HP: ", font=self.reg_font)
        lbl_static_HP.grid(row=4, column=0, sticky='nw')
        lbl_static_type = ttk.Label(self.stat_frame, text="Type: ", font=self.reg_font)
        lbl_static_type.grid(row=5, column=0, sticky='nw')
        lbl_static_ac = ttk.Label(self.stat_frame, text="AC: ", font=self.reg_font)
        lbl_static_ac.grid(row=6, column=0, sticky='nw')
        lbl_static_speed = ttk.Label(master=self.stat_frame, text="Speed: ", font=self.reg_font)
        lbl_static_speed.grid(row=7, column=0, sticky='nw')
        lbl_static_size = ttk.Label(self.stat_frame, text="Size: ", font=self.reg_font)
        lbl_static_size.grid(row=8, column=0, sticky='nw')
        lbl_static_coord = ttk.Label(self.stat_frame, text="Coordinate: ", font=self.reg_font)
        lbl_static_coord.grid(row=9, column=0, sticky='nw')
        lbl_static_init = ttk.Label(self.stat_frame, text="Initiative: ", font=self.reg_font)
        lbl_static_init.grid(row=10, column=0, sticky='nw')
        lbl_static_condition = ttk.Label(self.stat_frame, text="Condition: ", font=self.reg_font)
        lbl_static_condition.grid(row=11, column=0, sticky='nw')
        lbl_static_notes = ttk.Label(self.stat_frame, text="Notes: ", font=self.reg_font)
        lbl_static_notes.grid(row=12, column=0, sticky='nw')

        self.lbl_act_name = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_name.grid(row=0, column=1, sticky='nw')
        self.lbl_act_status = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_status.grid(row=1, column=1, sticky='nw')
        self.lbl_act_max_HP = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_max_HP.grid(row=2, column=1, sticky='nw')
        self.lbl_act_temp_HP = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_temp_HP.grid(row=3, column=1, sticky='nw')
        self.lbl_act_HP = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_HP.grid(row=4, column=1, sticky='nw')
        self.lbl_act_type = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_type.grid(row=5, column=1, sticky='nw')
        self.lbl_act_ac = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_ac.grid(row=6, column=1, sticky='nw')
        self.lbl_act_speed = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_speed.grid(row=7, column=1, sticky='nw')
        self.lbl_act_size = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_size.grid(row=8, column=1, sticky='nw')
        self.lbl_act_coord = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_coord.grid(row=9, column=1, sticky='nw')
        self.lbl_act_init = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_init.grid(row=10, column=1, sticky='nw')
        self.lbl_act_condition = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_condition.grid(row=11, column=1, sticky='nw')
        self.lbl_act_notes = ttk.Label(self.stat_frame, text=" ", font=self.reg_font)
        self.lbl_act_notes.grid(row=12, column=1, sticky='nw')

        lbl_change_name = ttk.Label(master=self.action_frame, text="Change Name", font=self.reg_font)
        lbl_change_name.grid(row=0, column=0, sticky='nw')
        self.ent_change_name = ttk.Entry(master=self.action_frame, width=27)
        self.ent_change_name.grid(row=0, column=1, sticky='nw')

        lbl_change_max_HP = ttk.Label(master=self.action_frame, text="Change Max HP", font=self.reg_font)
        lbl_change_max_HP.grid(row=1, column=0, sticky='nw')
        self.ent_new_max_HP = ttk.Entry(master=self.action_frame, width=27)
        self.ent_new_max_HP.grid(row=1, column=1, sticky='nw')
        lbl_change_temp_HP = ttk.Label(master=self.action_frame, text="Set Temp HP", font=self.reg_font)
        lbl_change_temp_HP.grid(row=2, column=0, sticky='nw')
        self.ent_set_temp_HP = ttk.Entry(master=self.action_frame, width=27)
        self.ent_set_temp_HP.grid(row=2, column=1, sticky='nw')
        self.set_temp_HP = tk.StringVar()
        rbn_set_tmp_HP = ttk.Radiobutton(master=self.action_frame, text="Set", variable=self.set_temp_HP, value='set')
        rbn_set_tmp_HP.grid(row=2, column=2, sticky='nw')
        rbn_remove_tmp_HP = ttk.Radiobutton(master=self.action_frame, text="Remove", variable=self.set_temp_HP, value='remove')
        rbn_remove_tmp_HP.grid(row=2, column=3, sticky='nw')
        lbl_change_HP = ttk.Label(master=self.action_frame, text="Heal/Damage HP", font=self.reg_font)
        lbl_change_HP.grid(row=3, column=0, sticky='nw')
        self.ent_HP_delta = ttk.Entry(master=self.action_frame, width=27)
        self.ent_HP_delta.grid(row=3, column=1, sticky='nw')
        self.heal_hurt = tk.StringVar()
        rbn_heal = ttk.Radiobutton(master=self.action_frame, text="Heal", variable=self.heal_hurt, value='heal')
        rbn_heal.grid(row=3, column=2, sticky='nw')
        rbn_damage = ttk.Radiobutton(master=self.action_frame, text="Damage", variable=self.heal_hurt, value='damage')
        rbn_damage.grid(row=3, column=3, sticky='nw')

        lbl_change_type = ttk.Label(master=self.action_frame, text="Change Type", font=self.reg_font)
        lbl_change_type.grid(row=4, column=0, sticky='nw')
        self.type = tk.StringVar()
        self.rbn_ally = ttk.Radiobutton(master=self.action_frame, text="Ally", variable= self.type, value="ally")
        self.rbn_ally.grid(row=4, column=2, sticky='nw')
        self.rbn_enemy = ttk.Radiobutton(master=self.action_frame, text="Enemy", variable= self.type, value="enemy")
        self.rbn_enemy.grid(row=4, column=3, sticky='nw')
        self.rbn_bystander = ttk.Radiobutton(master=self.action_frame, text="Bystander", variable= self.type, value="bystander")
        self.rbn_bystander.grid(row=5, column=2, sticky='nw')
        self.rbn_dead = ttk.Radiobutton(master=self.action_frame, text="Dead", variable= self.type, value="dead")
        self.rbn_dead.grid(row=5, column=3, sticky='nw')

        lbl_change_ac = ttk.Label(master=self.action_frame, text="Change AC", font=self.reg_font)
        lbl_change_ac.grid(row=6, column=0, sticky='w')
        self.ent_change_ac = ttk.Entry(master=self.action_frame, width=27)
        self.ent_change_ac.grid(row=6, column=1, sticky='w'),

        lbl_change_speed = ttk.Label(master=self.action_frame, text="Change Speed", font=self.reg_font)
        lbl_change_speed.grid(row=7, column=0, sticky='w')
        self.ent_change_speed = ttk.Entry(master=self.action_frame, width=27)
        self.ent_change_speed.grid(row=7, column=1, sticky='w')

        lbl_change_init = ttk.Label(master=self.action_frame, text="Change Initiative", font=self.reg_font)
        lbl_change_init.grid(row=8, column=0, sticky='nw')
        self.ent_initiative = ttk.Entry(master=self.action_frame, width=27)
        self.ent_initiative.grid(row=8, column=1, sticky='nw')
        btn_roll_init = ttk.Button(master=self.action_frame, text="Roll", command=self.roll_init, width=20)
        btn_roll_init.grid(row=8, column=2, columnspan=2, sticky='nw')

        lbl_change_condition = ttk.Label(master=self.action_frame, text="Change Condition", font=self.reg_font)
        lbl_change_condition.grid(row=9, column=0, sticky='nw')
        self.cond_normal = tk.IntVar()
        self.cond_blind = tk.IntVar()
        self.cond_charmed = tk.IntVar()
        self.cond_deaf = tk.IntVar()
        self.cond_fright = tk.IntVar()
        self.cond_grappled = tk.IntVar()
        self.cond_incapacitated = tk.IntVar()
        self.cond_invisible = tk.IntVar()
        self.cond_paralyzed = tk.IntVar()
        self.cond_petrified = tk.IntVar()
        self.cond_poisoned = tk.IntVar()
        self.cond_prone = tk.IntVar()
        self.cond_restrained = tk.IntVar()
        self.cond_stunned = tk.IntVar()
        self.cond_unconscious = tk.IntVar()
        self.cbn_normal = ttk.Checkbutton(master=self.action_frame, text="Normal", variable=self.cond_normal, command=self.on_off_buttons)
        self.cbn_normal.grid(row=9, column=2, columnspan=2,sticky='nw')
        self.cbn_blind = ttk.Checkbutton(master=self.action_frame, text="Blinded", variable=self.cond_blind)
        self.cbn_blind.grid(row=10, column=2, sticky='nw')
        self.cbn_charmed = ttk.Checkbutton(master=self.action_frame, text="Charmed", variable=self.cond_charmed)
        self.cbn_charmed.grid(row=10, column=3, sticky='nw')
        self.cbn_deaf = ttk.Checkbutton(master=self.action_frame, text="Deafened", variable=self.cond_deaf)
        self.cbn_deaf.grid(row=11, column=2, sticky='nw')
        self.cbn_fright = ttk.Checkbutton(master=self.action_frame, text="Frightened", variable=self.cond_fright)
        self.cbn_fright.grid(row=11, column=3, sticky='nw')
        self.cbn_grappled = ttk.Checkbutton(master=self.action_frame, text="Grappled", variable=self.cond_grappled)
        self.cbn_grappled.grid(row=12, column=2, sticky='nw')
        self.cbn_incapacitated = ttk.Checkbutton(master=self.action_frame, text="Incapacitated", variable=self.cond_incapacitated, command=self.connected_cond)
        self.cbn_incapacitated.grid(row=12, column=3, sticky='nw')
        self.cbn_invisible = ttk.Checkbutton(master=self.action_frame, text="Invisible", variable=self.cond_invisible)
        self.cbn_invisible.grid(row=13, column=2, sticky='nw')
        self.cbn_paralyzed = ttk.Checkbutton(master=self.action_frame, text="Paralyzed", variable=self.cond_paralyzed, command=self.connected_cond)
        self.cbn_paralyzed.grid(row=13, column=3, sticky='nw')
        self.cbn_petrified = ttk.Checkbutton(master=self.action_frame, text="Petrified", variable=self.cond_petrified, command=self.connected_cond)
        self.cbn_petrified.grid(row=14, column=2, sticky='nw')
        self.cbn_poisoned = ttk.Checkbutton(master=self.action_frame, text="Poisoned", variable=self.cond_poisoned)
        self.cbn_poisoned.grid(row=14, column=3, sticky='nw')
        self.cbn_prone = ttk.Checkbutton(master=self.action_frame, text="Prone", variable=self.cond_prone)
        self.cbn_prone.grid(row=15, column=2, sticky='nw')
        self.cbn_restrained = ttk.Checkbutton(master=self.action_frame, text="Restrained", variable=self.cond_restrained)
        self.cbn_restrained.grid(row=15, column=3, sticky='nw')
        self.cbn_stunned = ttk.Checkbutton(master=self.action_frame, text="Stunned", variable=self.cond_stunned, command=self.connected_cond)
        self.cbn_stunned.grid(row=16, column=2, sticky='nw')
        self.cbn_unconscious = ttk.Checkbutton(master=self.action_frame, text="Unconscious", variable=self.cond_unconscious, command=self.connected_cond)
        self.cbn_unconscious.grid(row=16, column=3, sticky='nw')
        lbl_exhaustion = ttk.Label(master=self.action_frame, text="Exhaustion", font=self.reg_font)
        lbl_exhaustion.grid(row=17, column=2, columnspan=2)
        self.exhaustion_level = tk.IntVar()
        self.sldr_exhaustion = tk.Scale(master=self.action_frame, from_=0, to=6, variable=self.exhaustion_level, orient=tk.HORIZONTAL, tickinterval=1, bg='gray28', fg='gray70', font=self.small_font, highlightbackground='gray28', highlightcolor='gray28')
        self.sldr_exhaustion.grid(row=18, column=2, columnspan=2)

        lbl_change_notes = ttk.Label(master=self.action_frame, text="Change Notes", font=self.reg_font)
        lbl_change_notes.grid(row=19, column=0, sticky='nw')
        self.check_delete = tk.IntVar()
        cbn_delete_notes = ttk.Checkbutton(master=self.action_frame, text="Delete Notes", variable=self.check_delete)
        cbn_delete_notes.grid(row=19, column=1, sticky='ne')
        self.txt_change_notes = tk.Text(master=self.action_frame, height=5, width=52)
        self.txt_change_notes.configure(font=self.small_font)
        self.txt_change_notes.grid(row=20, column=0, columnspan=4)

        self.btn_submit = ttk.Button(master=self.submit_frame, text="Submit", width=20)#, command=self.on_submit)
        self.btn_submit.grid(row=0, column=0, sticky='e')
        self.btn_delete_target = ttk.Button(master=self.submit_frame, text="Delete", width=20)#, command=self.delete_token)
        self.btn_delete_target.grid(row=0, column=1, sticky='w')
        self.lbl_close_window = ttk.Label(master=self.submit_frame, text="Please close this window to finalize.", font=self.reg_font)

    def select_target(self, event):
        selected_target = self.drop_targets.get()
        index = self.names.index(selected_target)
        object_target = self.root.token_list[index]
        self.lbl_act_name.config(text=object_target['name'])
        self.lbl_act_status.config(text=object_target['status'])
        self.lbl_act_max_HP.config(text=object_target['max_HP'])
        self.lbl_act_temp_HP.config(text=object_target['temp_HP'])
        self.lbl_act_HP.config(text=object_target['current_HP'])
        self.lbl_act_type.config(text=object_target['type'])
        self.lbl_act_ac.config(text=object_target['ac'])
        self.lbl_act_speed.config(text=object_target['speed'])
        self.lbl_act_size.config(text=object_target['size'])
        if object_target['coordinate'][0] != "" and object_target['coordinate'][1] != "" and object_target['coordinate'][2] != "":
            row = int(object_target['coordinate'][0]) + 1
            col = int(object_target['coordinate'][1]) + 1
            z = int(object_target['coordinate'][2])
        else:
            row = ""
            col = ""
            z = ""
        self.lbl_act_coord.config(text="{0}: {1}: {2}".format(row, col, z))
        all_conditions = ""
        for cond in object_target['condition']:
            if all_conditions == "":
                all_conditions += cond
            else:
                all_conditions = all_conditions + ", " + cond
        init_check = object_target['initiative']
        if init_check == math.inf:
            init_check = "Out of Initiative"
        self.lbl_act_init.config(text=init_check)
        self.lbl_act_condition.config(text=all_conditions)
        self.lbl_act_notes.config(text=object_target['notes'])

    def on_off_buttons(self):
        norm_value = self.cond_normal.get()
        if norm_value == 1:
            self.cbn_blind.state(['disabled'])
            self.cbn_charmed.state(['disabled'])
            self.cbn_deaf.state(['disabled'])
            self.cbn_fright.state(['disabled'])
            self.cbn_grappled.state(['disabled'])
            self.cbn_incapacitated.state(['disabled'])
            self.cbn_invisible.state(['disabled'])
            self.cbn_paralyzed.state(['disabled'])
            self.cbn_petrified.state(['disabled'])
            self.cbn_poisoned.state(['disabled'])
            self.cbn_prone.state(['disabled'])
            self.cbn_restrained.state(['disabled'])
            self.cbn_stunned.state(['disabled'])
            self.cbn_unconscious.state(['disabled'])
            self.sldr_exhaustion.config(state=tk.DISABLED, fg='gray40')
        else:
            self.cbn_blind.state(['!disabled'])
            self.cbn_charmed.state(['!disabled'])
            self.cbn_deaf.state(['!disabled'])
            self.cbn_fright.state(['!disabled'])
            self.cbn_grappled.state(['!disabled'])
            self.cbn_incapacitated.state(['!disabled'])
            self.cbn_invisible.state(['!disabled'])
            self.cbn_paralyzed.state(['!disabled'])
            self.cbn_petrified.state(['!disabled'])
            self.cbn_poisoned.state(['!disabled'])
            self.cbn_prone.state(['!disabled'])
            self.cbn_restrained.state(['!disabled'])
            self.cbn_stunned.state(['!disabled'])
            self.cbn_unconscious.state(['!disabled'])
            self.sldr_exhaustion.config(state=tk.NORMAL, fg='gray70')

    def on_submit(self):
        selected_target = self.drop_targets.get()
        if selected_target == "" or selected_target is None:
            messagebox.showinfo("Info", "Must select target creature.")
            return False

        index = self.names.index(selected_target)
        object_target = self.root.token_list[index]

        new_name = self.ent_change_name.get()
        if new_name == "":
            new_name = object_target['name']

        new_type = self.type.get()
        if new_type == "":
            new_type = object_target['type']

        test_max_HP = self.ent_new_max_HP.get()
        if test_max_HP == "":
            new_max_HP = object_target['max_HP']
        else:
            try:
                new_max_HP = int(test_max_HP)
                if new_max_HP <= 0:
                    new_max_HP = 0
                    new_type = 'dead'
            except ValueError:
                messagebox.showwarning("Target Creature", "Max HP must be a whole number.")
                return False
            except TypeError:
                messagebox.showwarning("Target Creature", "Max HP must be a whole number.")
                return False
        test_temp_HP = self.ent_set_temp_HP.get()
        setting_HP = self.set_temp_HP.get()
        if test_temp_HP == "":
            new_temp_HP = object_target['temp_HP']
        elif setting_HP == 'remove':
            new_temp_HP = 0
        elif setting_HP == 'set':
            try:
                new_temp_HP = int(test_temp_HP)
                if new_temp_HP < 0:
                    new_temp_HP = 0
            except ValueError:
                messagebox.showwarning("Target Creature", "Temp HP must be a whole number.")
                return False
            except TypeError:
                messagebox.showwarning("Target Creature", "Temp HP must be a whole number.")
                return False
        else:
            messagebox.showwarning("Target Creature", "Must select \"Set\" or \"Remove\".")
            return False
        test_HP_delta = self.ent_HP_delta.get()
        try:
            delta_HP = int(test_HP_delta)
        except ValueError:
            delta_HP = 0
        except TypeError:
            delta_HP = 0
        if self.heal_hurt.get() == 'heal':
            new_curr_HP = delta_HP + object_target['current_HP']
            if new_curr_HP > new_max_HP:
                new_curr_HP = new_max_HP
        elif self.heal_hurt.get() == 'damage':
            new_curr_HP = object_target['current_HP'] - delta_HP
            if new_curr_HP < new_max_HP * -1:
                new_type = 'dead'
        else:
            new_curr_HP = object_target['current_HP']

        new_ac = self.ent_change_ac.get()
        if new_ac == "":
            new_ac = object_target['ac']
        else:
            try:
                new_ac = int(new_ac)
                if new_ac < 0:
                    messagebox.showwarning("Target Creature", "AC value must be a positive whole number.")
                    return False
            except ValueError:
                messagebox.showwarning("Target Creature", "AC value must be a positive whole number.")
                return False
            except TypeError:
                messagebox.showwarning("Target Creature", "AC value must be a positive whole number.")
                return False

        new_speed = self.ent_change_speed.get()
        if new_speed == "":
            new_speed = object_target['speed']
        else:
            try:
                new_speed = int(new_speed)
                if new_speed < 0:
                    messagebox.showwarning("Target Creature", "Speed value must be a positive whole number.")
                    return False
            except ValueError:
                messagebox.showwarning("Target Creature", "Speed value must be a positive whole number.")
                return False
            except TypeError:
                messagebox.showwarning("Target Creature", "Speed value must be a positive whole number.")
                return False

        new_init = self.ent_initiative.get()
        if new_init == "":
            new_init = object_target['initiative']
        else:
            try:
                new_init = float(new_init)
                check_not_finished = True
                loop_counter = 0
                while check_not_finished:
                    for being in self.root.token_list:
                        loop_counter += 1
                        if being['initiative'] == new_init:
                            not_resolved = True
                            multiplier = 0.1
                            sub_offset = 5
                            inner_fail = 0
                            while not_resolved:
                                multiplier *= 0.1
                                sub_offset *= 0.1
                                roll_new_guy = self.dice.roll(dieSize=100)[0]
                                new_init = round(new_init + (roll_new_guy * multiplier - sub_offset), 8)
                                if new_init != being['initiative']:
                                    not_resolved = False
                                if inner_fail == 100:
                                    messagebox.showerror("Fatal Error", "Restart Program\nError 0x004")
                                    not_resolved = False
                                    check_not_finished = False
                                inner_fail += 1
                            break
                        elif loop_counter >= len(self.root.token_list):
                            check_not_finished = False
                        elif loop_counter > 100:
                            messagebox.showerror("Fatal Error", "Restart Program\nError 0x005")
                            check_not_finished = False
            except ValueError:
                new_init = object_target['initiative']
            except TypeError:
                new_init = object_target['initiative']
        
        new_condition = []
        if self.cond_normal.get() == 1 and new_type != 'dead':
            new_condition.append("normal")
        elif self.cond_normal.get() == 0 and self.cond_blind.get() == 0 and self.cond_charmed.get() == 0 and self.cond_deaf.get() == 0 and self.cond_fright.get() == 0 and self.cond_grappled.get() == 0 and self.cond_incapacitated.get() == 0 and self.cond_invisible.get() == 0 and self.cond_paralyzed.get() == 0 and self.cond_petrified.get() == 0 and self.cond_poisoned.get() == 0 and self.cond_prone.get() == 0 and self.cond_restrained.get() == 0 and self.cond_stunned.get() == 0 and self.cond_unconscious.get() == 0:
            new_condition = object_target['condition']
        else:
            if self.cond_blind.get() == 1:
                new_condition.append("blinded")
            if self.cond_charmed.get() == 1:
                new_condition.append("charmed")
            if self.cond_deaf.get() == 1:
                new_condition.append("deafened")
            if self.cond_fright.get() == 1:
                new_condition.append("frightened")
            if self.cond_grappled.get() == 1:
                new_condition.append("grappled")
            if self.cond_incapacitated.get() == 1:
                new_condition.append("incapacitated")
            if self.cond_invisible.get() == 1:
                new_condition.append("invisible")
            if self.cond_paralyzed.get() == 1:
                new_condition.append("paralyzed")
            if self.cond_petrified.get() == 1:
                new_condition.append("petrified")
            if self.cond_poisoned.get() == 1:
                new_condition.append("poisoned")
            if self.cond_prone.get() == 1:
                new_condition.append("prone")
            if self.cond_restrained.get() == 1:
                new_condition.append("restrained")
            if self.cond_stunned.get() == 1:
                new_condition.append("stunned")
            if self.cond_unconscious.get() == 1:
                new_condition.append("unconscious")
            lvl_exh = self.exhaustion_level.get()
            if lvl_exh > 0:
                new_condition.append("exhaustion level " + str(lvl_exh))
            if lvl_exh == 6:
                new_type = 'dead'

        no_notes = self.check_delete.get()
        new_notes = self.txt_change_notes.get(1.0, 'end-1c')
        if no_notes == 0 and new_notes == "":
            new_notes = object_target['notes']
        elif no_notes == 1:
            new_notes = ""

        new_obj_target = {
            "name": new_name,
            "status": object_target['status'],
            "max_HP": new_max_HP,
            "temp_HP": new_temp_HP,
            "current_HP": new_curr_HP,
            "type": new_type,
            "ac": object_target['ac'],
            "speed": new_speed,
            "size": object_target['size'],
            "coordinate": object_target['coordinate'],
            "condition": new_condition,
            "initiative": new_init,
            "notes": new_notes
        }
        if new_obj_target['name'] != object_target['name']:
            self.root.token_list.pop(index)
            self.root.token_list.append(new_obj_target)
        else:
            self.root.token_list[index] = new_obj_target
        
        return True
        #self.btn_submit.state(['disabled'])
        #self.btn_delete_target.state(['disabled'])
        #self.lbl_close_window.grid(row=1, column=0, columnspan=2)

    def delete_token(self):
        selected_target = self.drop_targets.get()
        if selected_target != "" and selected_target is not None:
            go_ahead = messagebox.askokcancel("Warning", "You are about to delete this creature.\nAre you sure?")
            if go_ahead:
                index = self.names.index(selected_target)
                self.root.token_list.pop(index)
                self.btn_submit.state(['disabled'])
                self.btn_delete_target.state(['disabled'])
                self.lbl_close_window.grid(row=1, column=0, columnspan=2)
                return True
            else:
                return False
        else:
            messagebox.showinfo("Info", "Must select a target creature.")
            return False
        
    def connected_cond(self):
        incap = self.cond_incapacitated.get()
        parlz = self.cond_paralyzed.get()
        petr = self.cond_petrified.get()
        stun = self.cond_stunned.get()
        aslp = self.cond_unconscious.get()
        if parlz == 1 or petr == 1 or stun == 1 or aslp == 1:
            self.cond_incapacitated.set(1)

    def roll_init(self):
        dice_roll = self.dice.roll()[0]
        self.ent_initiative.delete(0, tk.END)
        self.ent_initiative.insert(0, dice_roll)
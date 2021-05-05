import pathlib
import json
import os
import math
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from dice import DiceRoller
from press import Press

papyrus_font = ('Papyrus', '14')


class StatCollector(object):
    def __init__(self, master, map_size, round_num, turn):
        self.master = master
        self.map_size = map_size
        self.round = round_num
        self.turn = turn
        self.range_win = tk.Toplevel(self.master)
        self.range_win.title("Input Creature")
        style = ThemedStyle(self.range_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.range_win.configure(bg=style.lookup('TLabel', 'background'))
        self.dice = DiceRoller()
        self.forge = Press(self.master)

        btn_forge = ttk.Button(master=self.range_win, command=self.forge.init_press, text="Use Forge")
        btn_forge.grid(row=0, column=0)

        upper_frame = ttk.Frame(master=self.range_win)
        lower_frame = ttk.Frame(master=self.range_win)
        under_frame = ttk.Frame(master=self.range_win)

        frame1_1 = ttk.Frame(master=upper_frame)
        frame1_2 = ttk.Frame(master=upper_frame)
        frame2_1 = ttk.Frame(master=upper_frame)
        frame2_2 = ttk.Frame(master=upper_frame)
        frame3_1 = ttk.Frame(master=upper_frame)
        frame3_2 = ttk.Frame(master=upper_frame)

        frame_list = [frame1_1, frame1_2, frame2_1, frame2_2, frame3_1, frame3_2]

        upper_frame.grid(row=1, column=0, sticky="w")
        lower_frame.grid(row=2, column=0, sticky="w")
        under_frame.grid(row=3, column=0, pady=8)

        fr_row = 0
        fr_col = 0
        for fr in frame_list:
            fr.grid(row=fr_row, column = fr_col, padx=5, pady=5, sticky="w")
            fr_col += 1
            if fr_col == 2:
                fr_col = 0
                fr_row += 1
        
        self.rad_size = tk.StringVar()
        self.rad_foe_friend = tk.StringVar()
        self.stats = {}

        lbl_name = ttk.Label(master=frame1_1, text="Name", font=papyrus_font)
        self.ent_name = ttk.Entry(master=frame1_1, width=10)
        lbl_name.grid(row=0, column=0, sticky="w")
        self.ent_name.grid(row=0, column=1, sticky="e")

        lbl_HP = ttk.Label(master=frame1_2, text="Max HP", font=papyrus_font)
        self.ent_HP = ttk.Entry(master=frame1_2, width=8)
        lbl_HP.grid(row=0, column=0, sticky="w")
        self.ent_HP.grid(row=0, column=1, sticky="e")
        lbl_temp_HP = ttk.Label(master=frame1_2, text="Temp HP", font=papyrus_font)
        self.ent_temp_HP = ttk.Entry(master=frame1_2, width=8)
        lbl_temp_HP.grid(row=1, column=0, sticky="w")
        self.ent_temp_HP.grid(row=1, column=1, sticky="e")

        '''
        lbl_coord = ttk.Label(master=frame2_1, text="Coordinate", font=papyrus_font)
        self.ent_x_coord = ttk.Entry(master=frame2_1, width=2)
        lblX = ttk.Label(master=frame2_1, text="X", font=papyrus_font)
        self.ent_y_coord = ttk.Entry(master=frame2_1, width=2)
        lblY = ttk.Label(master=frame2_1, text="Y", font=papyrus_font)
        self.ent_z_coord = ttk.Entry(master=frame2_1, width=2)
        lblZ = ttk.Label(master=frame2_1, text="Z", font=papyrus_font)
        lbl_coord.grid(row=0, column=0, sticky="w")
        self.ent_x_coord.grid(row=0, column=1, sticky="e")
        lblX.grid(row=0, column=2, sticky="e")
        self.ent_y_coord.grid(row=0, column=3, sticky="e")
        lblY.grid(row=0, column=4, sticky="e")
        self.ent_z_coord.grid(row=0, column=5, sticky="e")
        lblZ.grid(row=0, column=6, sticky="e")
        '''

        frame_FF_upper = ttk.Frame(master=frame2_1)
        frame_FF_lower = ttk.Frame(master=frame2_1)
        lbl_FF = ttk.Label(master=frame_FF_upper, text="Strategic Status", font=papyrus_font)
        rbn_ally = ttk.Radiobutton(master=frame_FF_lower, text="Ally", variable= self.rad_foe_friend, value="ally")
        rbn_enemy = ttk.Radiobutton(master=frame_FF_lower, text="Enemy", variable= self.rad_foe_friend, value="enemy")
        rbn_bystander = ttk.Radiobutton(master=frame_FF_lower, text="Bystander", variable= self.rad_foe_friend, value="bystander")
        rbn_dead = ttk.Radiobutton(master=frame_FF_lower, text="Dead", variable= self.rad_foe_friend, value="dead")
        frame_FF_upper.grid(row=0, column=0, sticky="w")
        frame_FF_lower.grid(row=1, column=0, sticky="w")
        lbl_FF.grid(row=0, column=0, sticky="w")
        rbn_ally.grid(row=0, column=0, sticky="w")
        rbn_enemy.grid(row=0, column=1, sticky="w")
        rbn_bystander.grid(row=0, column=2, sticky="w")
        rbn_dead.grid(row=0, column=3, sticky="w")

        lbl_height = ttk.Label(master=frame2_2, text="Height (Feet)", font=papyrus_font)
        self.ent_height = ttk.Entry(master=frame2_2, width=8)
        lbl_height.grid(row=0, column=0, sticky="w")
        self.ent_height.grid(row=0, column=1, sticky="e")

        frame_size_left = ttk.Frame(master=frame3_1)
        frame_size_right = ttk.Frame(master=frame3_1)
        lbl_size = ttk.Label(master=frame3_1, text="Size Class", font=papyrus_font)
        rbn_tiny = ttk.Radiobutton(master=frame_size_left, text="Tiny", variable= self.rad_size, value="tiny")
        rbn_small = ttk.Radiobutton(master=frame_size_right, text="Small", variable= self.rad_size, value="small")
        rbn_medium = ttk.Radiobutton(master=frame_size_left, text="Medium", variable= self.rad_size, value="medium")
        rbn_large = ttk.Radiobutton(master=frame_size_right, text="Large", variable= self.rad_size, value="large")
        rbn_huge = ttk.Radiobutton(master=frame_size_left, text="Huge", variable= self.rad_size, value="huge")
        rbn_gargantuan = ttk.Radiobutton(master=frame_size_right, text="Gargantuan", variable= self.rad_size, value="gargantuan")
        lbl_size.grid(row=0, column=0)
        frame_size_left.grid(row=1, column=0)
        frame_size_right.grid(row=1, column=1)
        rbn_tiny.grid(row=0, column=0, sticky="w")
        rbn_small.grid(row=0, column=0, sticky="w")
        rbn_medium.grid(row=1, column=0, sticky="w")
        rbn_large.grid(row=1, column=0, sticky="w")
        rbn_huge.grid(row=2, column=0, sticky="w")
        rbn_gargantuan.grid(row=2, column=0, sticky="w")

        lbl_init = ttk.Label(master=frame3_2, text="Initiative", font=papyrus_font)
        lbl_init.grid(row=0, column=0, sticky='e')
        self.ent_init = ttk.Entry(master=frame3_2, width=8)
        self.ent_init.grid(row=0, column=1, sticky='w')
        btn_roll_init = ttk.Button(master=frame3_2, text="Roll", command=self.roll_dice)
        btn_roll_init.grid(row=0, column=2, sticky='w')

        lbl_notes = ttk.Label(master=lower_frame, text="Notes", font=papyrus_font)
        self.txt_notes = tk.Text(master=lower_frame, height=5, width=52)
        self.txt_notes.configure(font=("Papyrus", "12"))
        lbl_notes.grid(row=0, column=0)
        self.txt_notes.grid(row=1, column=0, sticky="w")

        self.btn_submit = ttk.Button(master=under_frame, text="Submit")#command=self.submit,
        self.btn_submit.grid(row=0, column=0)
        btn_cancel = ttk.Button(master=under_frame, text="Cancel", command=self.range_win.destroy)
        btn_cancel.grid(row=0, column=1)

    def submit(self):
        special_char = ['[','@','_','!','#','$','%','^','&','*','(',')','<','>','?','/','\\','|','}','{','~',':',']']
        name_get = self.ent_name.get()
        max_HP_get = self.ent_HP.get()
        temp_HP_get = self.ent_temp_HP.get()
        foe_friend_get = self.rad_foe_friend.get()
        height_get = self.ent_height.get()
        size_get = self.rad_size.get()
        init_get = self.ent_init.get()
        notes_get = self.txt_notes.get(1.0, tk.END)
        if name_get == "":
            messagebox.showinfo("Character Input", "Must input a name.")
            return False
        for i in range(len(special_char)):
            if special_char[i] in name_get:
                messagebox.showwarning("Character Input", "Name cannot contain special characters.")
                return False
        if foe_friend_get == "":
            messagebox.showwarning("Character Input", "Must select a strategic status.")
            return False
        if size_get == "":
            messagebox.showwarning("Character Input", "Must select a size.")
            return False
        if init_get == "":
            init_flt = math.inf
        else:
            try:
                init_flt = float(init_get)
                check_not_finished = True
                loop_counter = 0
                while check_not_finished:
                    for being in self.master.token_list:
                        loop_counter += 1
                        if being['initiative'] == init_flt:
                            not_resolved = True
                            multiplyer = 0.1
                            sub_offset = 5
                            inner_fail = 0
                            while not_resolved:
                                multiplyer *= 0.1
                                sub_offset *= 0.1
                                roll_new_guy = self.dice.roll(dieSize=100)[0]
                                init_flt = init_flt + (roll_new_guy * multiplyer - sub_offset)
                                if init_flt != being['initiative']:
                                    not_resolved = False
                                if inner_fail == 100:
                                    messagebox.showerror("System Error", "Restart Program\nError 0x002")
                                    not_resolved = False
                                    check_not_finished = False
                                inner_fail += 1
                            break
                        elif loop_counter >= len(self.master.token_list):
                            check_not_finished = False
                        elif loop_counter > 100:
                            messagebox.showerror("System Error", "Restart Program\nError 0x003")
                            check_not_finished = False

            except ValueError:
                messagebox.showwarning("Character Input", "Initiative must be a number.")
                return False
            except TypeError:
                messagebox.showwarning("Character Input", "Initiative must be a number.")
                return False
        '''
        if notes_get == "Easter Egg 1234 ABC":
            messagebox.showinfo("Character Input", "In the deepest dungeon of the darkest realm,\nYou will find the creature of brightest light and darkest story.\nIf only the heroes could brave true horror and near insurmountable doom,\nThey might find all the hope they would ever need.")
            return False
        '''
        try:
            if max_HP_get != "":
                max_HP_int = int(max_HP_get)
                if max_HP_int <= 0:
                    messagebox.showinfo("Character Input", "Max HP must be a positive whole number.")
                    return False
            else:
                messagebox.showinfo("Character Input", "Max HP cannot be undefined.")
                return False
            if temp_HP_get != "":
                temp_HP_int = int(max_HP_get)
                if temp_HP_int < 0:
                    messagebox.showinfo("Character Input", "Temp HP must be a positive whole number or zero.")
                    return False
            else:
                temp_HP_int = 0
        except ValueError:
            messagebox.showwarning("Character Input", "Max HP must be a positive whole number. If entered, Temp HP must be a positive whole number or zero.")
            return False
        except TypeError:
            messagebox.showwarning("Character Input", "Max HP must be a positive whole number. If entered, Temp HP must be a positive whole number or zero.")
            return False
        try:
            if height_get == "":
                messagebox.showwarning("Character Input", "Height cannot be undefined.")
                return False
            height_flt = float(height_get)
            if height_flt < 0:
                messagebox.showinfo("Character Input", "Height must be a positive number or zero.")
                return False
        except ValueError:
            messagebox.showwarning("Character Input", "Height must be a positive number or zero.")
            return False
        except TypeError:
            messagebox.showwarning("Character Input", "Height must be a positive number or zero.")
            return False

        self.stats = {
            "name": name_get,
            "max_HP": max_HP_int,
            "temp_HP": temp_HP_int,
            "current_HP": max_HP_int,
            "type": foe_friend_get,
            "height": height_flt,
            "size": size_get,
            "coordinate": ["", "", ""],
            "condition": ["normal"],
            "initiative": init_flt,
            "notes": notes_get
        }
        for being in self.master.token_list:
            if being['name'] == name_get:
                messagebox.showwarning("Character Input", "The name that was entered matches an existing creature.\nCreature must have a unique name.")
                return False
        self.master.token_list.append(self.stats)
        return True
        #self.write_file()
        #self.range_win.destroy()

    # Unused
    def write_file(self):
        battle_dict = {
            "map_size": self.map_size,
            "round": self.round,
            "turn": self.turn
        }
        battleJSON = json.dumps(battle_dict, indent=4)
        with ZipFile(self.master.filename, "r") as savefile:
            read_bytes = savefile.read('creatures.json')
            read_obj = json.loads(read_bytes.decode('utf-8'))
            read_obj.update(self.stats)
        with ZipFile(self.master.filename, "w") as savefile:
            readJSON = json.dumps(read_obj, indent=4)
            savefile.writestr('battle_info.json', battleJSON)
            savefile.writestr('creatures.json', readJSON)

    def roll_dice(self):
        die_face = self.dice.roll()[0]
        self.ent_init.delete(0, tk.END)
        self.ent_init.insert(0, str(die_face))
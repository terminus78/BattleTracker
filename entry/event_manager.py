import math
import copy

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from big_helper_2D import correct_placement
from dice import DiceRoller

class EventManager():
    def __init__(self, root):
        self.root = root
        self.font = ('Papyrus', '14')
        self.dice = DiceRoller()
        
    def right_click_menu(self, event):
        self.event = event
        self.token_menu = tk.Menu(self.root, tearoff=0)
        #self.trig_menu = tk.Menu(self.token_menu, tearoff=0)
        #self.aoe_menu = tk.Menu(self.token_menu, tearoff=0)
        #self.token_menu.add_command(label="Target Creature")
        #self.token_menu.add_command(label="Damage")
        #self.token_menu.add_command(label="Heal")
        self.token_menu.add_command(label="Conditions Info")
        self.token_menu.add_separator()
        #self.token_menu.add_cascade(label="Trig Functions", menu=self.trig_menu)
        #self.trig_menu.add_command(label="Distance", command=findDistance)
        #self.trig_menu.add_command(label="Find All in Range")
        #self.trig_menu.add_command(label="Spread Width")
        #self.token_menu.add_cascade(label="AOE", menu=self.aoe_menu)
        #self.aoe_menu.add_command(label="Circle")
        #self.aoe_menu.add_command(label="Square")
        #self.aoe_menu.add_command(label="Cone")
        #self.aoe_menu.add_command(label="Line")
        #self.aoe_menu.add_command(label="Ring Wall")
        #self.aoe_menu.add_command(label="Line Wall")
        try:
            self.token_menu.tk_popup(self.event.x_root, self.event.y_root)
        finally:
            self.token_menu.grab_release()

    def move_token(self, map_size):
        self.map_size = map_size
        self.move_win = tk.Toplevel(master=self.root)
        self.move_win.title("Move Token")
        style = ThemedStyle(self.move_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.move_win.configure(bg=style.lookup('TLabel', 'background'))
        self.move_win.rowconfigure(0, minsize=100)
        self.move_win.columnconfigure([0,1], minsize=100)
        self.selection_frame = ttk.Frame(master=self.move_win)
        self.selection_frame.grid(row=0, column=0, rowspan=2, sticky='nw')
        self.move_to_frame = ttk.Frame(master=self.move_win)
        self.move_to_frame.grid(row=0, column=1, sticky='nw')
        self.move_finish_frame = ttk.Frame(master=self.move_win)
        self.move_finish_frame.grid(row=1, column=1)
        lbl_selected = ttk.Label(master=self.selection_frame, text="Selected Token", font=self.font)
        lbl_selected.grid(row=0, column=0, sticky='w')
        self.names = []
        self.coordinates = []
        self.drop_selection = ttk.Combobox(self.selection_frame, width=27, values=self.names, state='readonly')
        self.drop_selection.grid(row=0, column=1, sticky='w')
        self.drop_selection.current()
        self.drop_selection.bind("<<ComboboxSelected>>", lambda e: self.show_coord(event=e, arg=[self.names, self.coordinates]))
        self.lbl_act_coord = ttk.Label(master=self.selection_frame, text=" ", font=self.font)
        self.lbl_act_coord.grid(row=1, column=1, sticky='w', columnspan=2)
        self.creat_or_obj = tk.StringVar()
        self.rbn_creature = ttk.Radiobutton(self.selection_frame, text="Creature", variable=self.creat_or_obj, value='creature', command=self.fill_drop_select)
        self.rbn_creature.grid(row=0, column=2, sticky='w')
        self.rbn_object = ttk.Radiobutton(self.selection_frame, text="Object", variable=self.creat_or_obj, value='object', command=self.fill_drop_select)
        self.rbn_object.grid(row=0, column=3, sticky='w')
        self.rbn_creature.invoke()
        lbl_set_new_coord = ttk.Label(master=self.move_to_frame, text="Set New Coordinate", font=self.font)
        lbl_set_new_coord.grid(row=0, column=0, sticky='w')
        coord_frame = ttk.Frame(master=self.move_to_frame)
        coord_frame.grid(row=0, column=1, columnspan=3, sticky='w')
        self.ent_row_coord = ttk.Entry(master=coord_frame, width=5)
        self.ent_col_coord = ttk.Entry(master=coord_frame, width=5)
        self.ent_z_coord = ttk.Entry(master=coord_frame, width=5)
        self.ent_row_coord.grid(row=0, column=0, sticky='w')
        self.ent_col_coord.grid(row=0, column=1, sticky='w')
        self.ent_z_coord.grid(row=0, column=2, sticky='w')

        self.lbl_or_this = ttk.Label(master=self.move_to_frame, text="or move a number of spaces", font=self.font)

        self.lbl_fwd_back = ttk.Label(master=self.move_to_frame, text="Forward/Back", font=self.font)
        self.ent_row_delta = ttk.Entry(master=self.move_to_frame, width=5)
        self.fwd_or_back = tk.StringVar()
        self.rbn_move_fwd = ttk.Radiobutton(master=self.move_to_frame, text="Forward", variable=self.fwd_or_back, value='forward')
        self.rbn_move_back = ttk.Radiobutton(master=self.move_to_frame, text="Back", variable=self.fwd_or_back, value='back')
        self.lbl_left_right = ttk.Label(master=self.move_to_frame, text="Left/Right", font=self.font)
        self.ent_col_delta = ttk.Entry(master=self.move_to_frame, width=5)
        self.left_or_right = tk.StringVar()
        self.rbn_move_left = ttk.Radiobutton(master=self.move_to_frame, text="Left", variable=self.left_or_right, value='left')
        self.rbn_move_right = ttk.Radiobutton(master=self.move_to_frame, text="Right", variable=self.left_or_right, value='right')
        self.lbl_up_down = ttk.Label(master=self.move_to_frame, text="Up/Down", font=self.font)
        self.ent_z_delta = ttk.Entry(master=self.move_to_frame, width=5)
        self.up_or_down = tk.StringVar()
        self.rbn_move_up = ttk.Radiobutton(master=self.move_to_frame, text="Up", variable=self.up_or_down, value='up')
        self.rbn_move_down = ttk.Radiobutton(master=self.move_to_frame, text="Down", variable=self.up_or_down, value='down')

        self.btn_set = ttk.Button(master=self.move_finish_frame, text="Set Position")#, command=lambda arg=[False]: self.set_new_coord(arg))
        self.btn_set.grid(row=0, column=0, sticky='w')
        self.btn_remove = ttk.Button(master=self.move_finish_frame, text="Remove Token")#, command=lambda arg=[True]: self.set_new_coord(arg))
        self.btn_remove.grid(row=0, column=1, sticky='w')
        self.lbl_set_finished = ttk.Label(master=self.move_finish_frame, text=" ", font=self.font)
        self.lbl_set_finished.grid(row=0, column=2, sticky='w')

    def fill_drop_select(self):
        self.names = []
        self.coordinates = []
        cr_or_obj = self.creat_or_obj.get()
        if cr_or_obj == "creature":
            for being in self.root.token_list:
                self.names.append(being["name"])
                self.coordinates.append(being["coordinate"])
        else:
            for thing in self.root.obj_list:
                self.names.append(thing["name"])
                self.coordinates.append(thing["coordinate"])
        self.drop_selection.config(values=self.names)

    def show_coord(self, arg, event):
        selected_option = self.drop_selection.get()
        names = arg[0]
        coordinates = arg[1]
        index = names.index(selected_option)
        if coordinates[index][0] != "" and coordinates[index][1] != "" and coordinates[index][2] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1

            self.lbl_or_this.grid(row=1, column=0, columnspan=4)
            self.lbl_fwd_back.grid(row=2, column=0, sticky='w')
            self.ent_row_delta.grid(row=2, column=1, sticky='w')
            self.rbn_move_fwd.grid(row=2, column=2, sticky='w')
            self.rbn_move_back.grid(row=2, column=3, sticky='w')
            self.lbl_left_right.grid(row=3, column=0, sticky='w')
            self.ent_col_delta.grid(row=3, column=1, sticky='w')
            self.rbn_move_left.grid(row=3, column=2, sticky='w')
            self.rbn_move_right.grid(row=3, column=3, sticky='w')
            self.lbl_up_down.grid(row=4, column=0, sticky='w')
            self.ent_z_delta.grid(row=4, column=1, sticky='w')
            self.rbn_move_up.grid(row=4, column=2, sticky='w')
            self.rbn_move_down.grid(row=4, column=3, sticky='w')
            z = coordinates[index][2]
            self.lbl_act_coord.config(text="{0}: {1}: {2}".format(row, col, z))

        else:
            row = coordinates[index][0]
            col = coordinates[index][1]
            if len(self.move_to_frame.grid_slaves()) > 2:
                self.lbl_or_this.grid_forget()
                self.lbl_fwd_back.grid_forget()
                self.ent_row_delta.grid_forget()
                self.rbn_move_fwd.grid_forget()
                self.rbn_move_back.grid_forget()
                self.lbl_left_right.grid_forget()
                self.ent_col_delta.grid_forget()
                self.rbn_move_left.grid_forget()
                self.rbn_move_right.grid_forget()
                self.lbl_up_down.grid_forget()
                self.ent_z_delta.grid_forget()
                self.rbn_move_up.grid_forget()
                self.rbn_move_down.grid_forget()
            self.lbl_act_coord.config(text="Off Map")

    def set_new_coord(self):
        #removing_token = arg[0]
        selected_option = self.drop_selection.get()
        if selected_option == "":
            messagebox.showinfo("Info", "Must select a creature or object.")
            return False

        name_list = []
        name_exists = False
        if self.creat_or_obj.get() == 'creature':
            for being in self.root.token_list:
                name_list.append(being['name'])
                if being['name'] == selected_option:
                    name_exists = True
            if name_exists == False:
                messagebox.showinfo("Info", "Creature does not exist in current game.")
                return False
        else:
            for thing in self.root.obj_list:
                name_list.append(thing['name'])
                if thing['name'] == selected_option:
                    name_exists = True
            if name_exists == False:
                messagebox.showinfo("Info", "Object does not exist in current game.")
                return False
        index = name_list.index(selected_option)
        if self.creat_or_obj.get() == 'creature':
            size = self.root.token_list[index]['size']
        else:
            size = self.root.obj_list[index]['size']
        one_space = False
        if size == 'tiny' or size == 'small' or size == 'medium':
            one_space = True
        any_move_allowed = False
        go_forward_back = self.fwd_or_back.get()
        go_left_right = self.left_or_right.get()
        go_up_down = self.up_or_down.get()
        delta_fwd_bck_str = self.ent_row_delta.get()
        delta_left_right_str = self.ent_col_delta.get()
        delta_up_down_str = self.ent_z_delta.get()

        if go_forward_back != "" or go_left_right != "" or go_up_down != "":
            if self.creat_or_obj.get() == 'creature':
                coordinate = self.root.token_list[index]['coordinate']
            else:
                coordinate = self.root.obj_list[index]['coordinate']
            if coordinate[0] != "" and coordinate[1] != "" and coordinate[2] != "":
                any_move_allowed = True

        if any_move_allowed == False and (self.ent_row_coord.get() == "" or self.ent_col_coord.get() == "" or self.ent_z_coord.get() == ""):
            messagebox.showwarning("Warning", "Coordinate Fields Can't Be Empty!")
            return False

        #if removing_token == False:
        if any_move_allowed:
            for i in range(3):
                coordinate[i] = int(coordinate[i])
            try:
                delta_FB = int(delta_fwd_bck_str)
            except ValueError:
                delta_FB = 0
            try:
                delta_LR = int(delta_left_right_str)
            except ValueError:
                delta_LR = 0
            try:
                delta_UD = int(delta_up_down_str)
            except ValueError:
                delta_UD = 0

            if delta_FB < 0 or delta_LR < 0 or delta_UD < 0:
                messagebox.showwarning("Warning", "Move fields cannot be negative!")
                return False
            if go_forward_back == 'forward':
                coordinate[0] -= delta_FB
                if one_space:
                    if coordinate[0] < 0:
                        coordinate[0] = 0
                else:
                    coordinate = correct_placement(coordinate, size, self.map_size)
            if go_forward_back == 'back':
                coordinate[0] += delta_FB
                if one_space:
                    if coordinate[0] > self.map_size[0] - 1:
                        coordinate[0] = self.map_size[0] - 1
                else:
                    coordinate = correct_placement(coordinate, size, self.map_size)
            if go_left_right == 'left':
                coordinate[1] -= delta_LR
                if one_space:
                    if coordinate[1] < 0:
                        coordinate[1] = 0
                else:
                    coordinate = correct_placement(coordinate, size, self.map_size)
            if go_left_right == 'right':
                coordinate[1] += delta_LR
                if one_space:
                    if coordinate[1] > self.map_size[1] - 1:
                        coordinate[1] = self.map_size[1] - 1
                else:
                    coordinate = correct_placement(coordinate, size, self.map_size)
            if go_up_down == 'down':
                coordinate[2] -= delta_UD
            if go_up_down == 'up':
                coordinate[2] += delta_UD

            new_coord = (str(coordinate[0]), str(coordinate[1]), str(coordinate[2]))
        
        else:
            try:
                new_row = int(self.ent_row_coord.get()) - 1
                new_col = int(self.ent_col_coord.get()) - 1
                new_z = int(self.ent_z_coord.get())
            except ValueError:
                messagebox.showwarning("Warning", "Set Coordinate fields must be whole numbers!")
                return False
            if new_row > self.map_size[0] - 1 or new_row < 0:
                messagebox.showerror("Error", "Row Coordinate Out of Range of Map!")
                return False
            if new_col > self.map_size[1] - 1 or new_col < 0:
                messagebox.showerror("Error", "Column Coordinate Out of Range of Map!")
                return False
            new_coord = [str(new_row), str(new_col), str(new_z)]
        #else:
            #new_coord = ["", "", ""]

        '''
        new_init = self.ent_init.get()
        if new_init == "":
            new_init = self.root.token_list[index]['initiative']
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
                            multiplyer = 0.1
                            sub_offset = 5
                            inner_fail = 0
                            while not_resolved:
                                multiplyer *= 0.1
                                sub_offset *= 0.1
                                roll_new_guy = self.dice.roll(dieSize=100)[0]
                                new_init = new_init + (roll_new_guy * multiplyer - sub_offset)
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
                new_init = self.root.token_list[index]['initiative']
            except TypeError:
                new_init = self.root.token_list[index]['initiative']
        
        for being in self.root.token_list:
            if being["coordinate"] == new_coord:
                    messagebox.showerror("Error", "Space already taken!")
                    return
        '''
        
        if self.creat_or_obj.get() == 'creature':
            self.root.token_list[index]['coordinate'] = new_coord
        else:
            self.root.obj_list[index]['coordinate'] = new_coord
        return True
    
    def remove_token(self):
        selected_option = self.drop_selection.get()
        if selected_option == "":
            messagebox.showinfo("Info", "Must select a creature or object.")
            return False
        new_coord = ["", "", ""]
        if self.creat_or_obj.get() == 'creature':
            for being in self.root.token_list:
                if being["name"] == selected_option:
                    being["coordinate"] = [new_coord[0], new_coord[1], new_coord[2]]
        else:
            name_list = []
            for thing in self.root.obj_list:
                name_list.append(thing['name'])
            self.root.obj_list.pop(name_list.index(selected_option))
        return True

    # Unused
    def roll_init(self):
        rolled_value = self.dice.roll()[0]
        self.ent_init.delete(0, tk.END)
        self.ent_init.insert(0, rolled_value)
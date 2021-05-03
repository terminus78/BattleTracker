import math
import random
import pathlib
import json
import os
from zipfile import ZipFile

import PIL.Image
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from tooltip import *
from eventManager import EventManager
from calc import Calculator
from statCollector import StatCollector
from quotes import Quote
from target import Target
from conditionInfo import InfoClass
from dice import DiceRoller


class BattleMap(object):
    def __init__(self, master):
        self.master = master
        self.reg_font = ('Papyrus', '14')
        self.small_font = ("Papyrus", "9")
        self.big_font = ("Papyrus", "16")
        game_title = self.master.game_name
        if len(game_title) > 32:
            game_title = game_title[0:31] + "..."
        # Window definition
        with ZipFile(self.master.filename, 'r') as savefile:
            battle_bytes = savefile.read('battleInfo.json')
            battle_obj = json.loads(battle_bytes.decode('utf-8'))
            self.map_size = battle_obj['mapSize']
            self.round = battle_obj['round']
            self.turn = battle_obj['turn']
        self.map_win = tk.Toplevel(self.master)
        self.map_win.title(f"Battle Map | {game_title}")
        style = ThemedStyle(self.map_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.map_win.configure(bg=style.lookup('TLabel', 'background'))
        self.top_frame = ttk.Frame(master=self.map_win, borderwidth=2, relief='ridge',)# bg='dark green')
        self.top_frame.pack(side='top', fill='x')
        self.top_frame.columnconfigure(0, weight=1)
        self.top_frame.rowconfigure(0, minsize=100)
        self.quote_frame = ttk.Frame(master=self.map_win, borderwidth=2, relief='ridge')
        self.quote_frame.pack(side='top', fill='x')
        self.quote_frame.columnconfigure(0, minsize=20)
        self.bottom_frame = ttk.Frame(master=self.map_win, borderwidth=2, relief='ridge')#, bg='dark green')
        self.bottom_frame.pack(side='top', fill='both', expand=True)
        self.bottom_frame.columnconfigure(0, minsize=100)
        self.bottom_frame.columnconfigure(1, weight=1, minsize=200)
        self.bottom_frame.columnconfigure(2, minsize=150)
        self.bottom_frame.columnconfigure(3, minsize=50)
        self.bottom_frame.rowconfigure(0, weight=1, minsize=200)
        self.em = EventManager(self.map_win)
        self.calculator = Calculator(self.map_win)
        self.quoter = Quote()
        self.count_quotes = 0
        self.target = Target(self.map_win)
        self.info = InfoClass(self.map_win)
        self.dice_roll = DiceRoller(self.map_win)

        # Board Setup
        lbl_map = ttk.Label(master=self.top_frame, text=game_title, font=('Papyrus', '16'))
        lbl_map.grid(row=0, column=0)
        btn_save = ttk.Button(master=self.top_frame, command=self.save_game, text="Save")
        btn_save.grid(row=0, column=1, sticky='se')
        btn_clear = ttk.Button(master=self.top_frame, command=self.clear_map, text="Clear Map")
        btn_clear.grid(row=0, column=2, sticky='se')
        btn_input = ttk.Button(master=self.top_frame, command=self.input_creature_window, text="Input Creature")
        btn_input.grid(row=0, column=3, sticky='se')
        btn_reset = ttk.Button(master=self.top_frame, command=lambda: self.refresh_map(reset=True), text="Reset Map")
        btn_reset.grid(row=0, column=4, sticky='se')
        btn_restart = ttk.Button(master=self.top_frame, command=self.full_reset, text="Reset Battle")
        btn_restart.grid(row=0, column=5, sticky='se')
        btn_close_all = ttk.Button(master=self.top_frame, command=self.master.destroy, text="Close All")
        btn_close_all.grid(row=0, column=6, sticky='se')
        self.lbl_quote = ttk.Label(master=self.quote_frame, text="", font=self.reg_font)
        self.lbl_quote.grid(row=0, column=0, sticky='w', pady=5)
        self.find_quote()
        '''
        top_grid_label_frame = ttk.Frame(master=self.bottom_frame)
        top_grid_label_frame.grid(row=0, column=2)
        left_grid_label_frame = ttk.Frame(master=self.bottom_frame)
        left_grid_label_frame.grid(row=1, column=1)
        '''
        self.side_board = ttk.Frame(master=self.bottom_frame)
        self.side_count = 0
        grid_frame = ttk.Frame(master=self.bottom_frame, borderwidth=2, relief='ridge')
        self.round_bar = ttk.Frame(master=self.bottom_frame)
        self.tool_bar = ttk.Frame(master=self.bottom_frame)
        self.side_board.grid(row=0, column=0, padx=5, pady=10, sticky="nw")
        grid_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self.round_bar.grid(row=0, column=2, padx=5, pady=10, sticky="nw")
        self.tool_bar.grid(row=0, column=3, padx=5, pady=10, sticky="nw")

        # Image paths
        move_icon_path = "entry\\bin\\icons8-circled-down-left-32.png"
        move_icon = ImageTk.PhotoImage(image=PIL.Image.open(move_icon_path).resize((20,20)))
        trig_icon_path = "entry\\bin\\3228996421547464107-128.png"
        trig_icon = ImageTk.PhotoImage(image=PIL.Image.open(trig_icon_path).resize((20,20)))
        target_icon_path = "entry\\bin\\11749495271547546487-128.png"
        target_icon = ImageTk.PhotoImage(image=PIL.Image.open(target_icon_path).resize((20,20)))
        cond_info_icon_path = "entry\\bin\\2780604101548336129-128.png"
        cond_info_icon = ImageTk.PhotoImage(image=PIL.Image.open(cond_info_icon_path).resize((20,20)))
        turn_icon_path = "entry\\bin\\swords.png"
        self.turn_icon = ImageTk.PhotoImage(image=PIL.Image.open(turn_icon_path).resize((20,20)))
        d20_icon_path = "entry\\bin\\role-playing.png"
        d20_icon = ImageTk.PhotoImage(image=PIL.Image.open(d20_icon_path).resize((20,20)))

        ally_path = "entry\\bin\\allyToken.png"
        self.ally_img = ImageTk.PhotoImage(image=PIL.Image.open(ally_path).resize((15,15)))
        enemy_path = "entry\\bin\\enemyToken.png"
        self.enemy_img = ImageTk.PhotoImage(image=PIL.Image.open(enemy_path).resize((15,15)))
        bystander_path = "entry\\bin\\bystanderToken.png"
        self.bystander_img = ImageTk.PhotoImage(image=PIL.Image.open(bystander_path).resize((15,15)))
        dead_path = "entry\\bin\\deadToken.png"
        self.dead_img = ImageTk.PhotoImage(image=PIL.Image.open(dead_path).resize((15,15)))
        
        self.map_frames = []
        self.map_win.token_list = []

        # Grid labels
        for col_spot in range(self.map_size[1]):
            lbl_grid_top = ttk.Label(master=grid_frame, text=col_spot+1, font=self.small_font)
            lbl_grid_top.grid(row=0, column=col_spot+1)
            grid_frame.columnconfigure(col_spot+1, weight=1, minsize=20)

        for row_spot in range(self.map_size[0]):
            lbl_grid_side = ttk.Label(master=grid_frame, text=row_spot+1, font=self.small_font)
            lbl_grid_side.grid(row=row_spot+1, column=0)
            grid_frame.rowconfigure(row_spot+1, weight=1, minsize=20)

        grid_frame.columnconfigure(0, weight=1, minsize=20)
        grid_frame.rowconfigure(0, weight=1, minsize=20)

        # Space frames
        for i in range(self.map_size[0]):
            self.map_frames.append([])
            for j in range(self.map_size[1]):
                self.space = ttk.Frame(master=grid_frame, relief=tk.RAISED, borderwidth=1)
                self.space.grid(row=i+1, column=j+1, sticky='nsew')
                CreateToolTip(self.space, text=f"{i+1}, {j+1}")
                self.map_frames[i].append(self.space)
        
        self.initialize_tokens()

        # Round bar
        lbl_round_title = ttk.Label(master=self.round_bar, text="Round: ", font=self.big_font)
        lbl_round_title.grid(row=0, column=0, sticky='e')
        if self.round == 0:
            tmp_round = "S"
        else:
            tmp_round = self.round
        self.lbl_round = ttk.Label(master=self.round_bar, text=tmp_round, font=self.big_font, borderwidth=1, relief=tk.RAISED, width=3, anchor=tk.CENTER)
        self.lbl_round.grid(row=0, column=1, sticky='w')
        self.initiative_frame = ttk.Frame(master=self.round_bar)
        self.initiative_frame.grid(row=1, column=0, columnspan=2, sticky='ew')
        self.initiative_frame.columnconfigure([0,1], weight=1)
        btn_next_turn = ttk.Button(master=self.round_bar, text="Turn Complete", command=self.next_turn, width=18)
        btn_next_turn.grid(row=2, column=0, columnspan=2)
        btn_next_round = ttk.Button(master=self.round_bar, text="Round Complete", command=self.next_round, width=18)
        btn_next_round.grid(row=3, column=0, columnspan=2)
        btn_reset_rounds = ttk.Button(master=self.round_bar, text="Reset Rounds", command=self.reset_round, width=18)
        btn_reset_rounds.grid(row=4, column=0, columnspan=2)

        # Tool bar Buttons
        self.btn_move = ttk.Button(master=self.tool_bar, command=self.move_token, image=move_icon)
        self.btn_move.grid(row=0, column=0, sticky="n")
        self.btn_move.image = move_icon
        CreateToolTip(self.btn_move, text="Move Token", left_disp=True)

        self.btn_trig = ttk.Button(master=self.tool_bar, command=self.open_trig, image=trig_icon)
        self.btn_trig.grid(row=1, column=0, sticky='n')
        self.btn_trig.image = trig_icon
        CreateToolTip(self.btn_trig, text="Distance", left_disp=True)

        self.btn_target = ttk.Button(master=self.tool_bar, command=self.target_item,image=target_icon)
        self.btn_target.grid(row=2, column=0, sticky='n')
        self.btn_target.image = target_icon
        CreateToolTip(self.btn_target, text="Target", left_disp=True)

        self.btn_cond_info = ttk.Button(master=self.tool_bar, command=self.show_cond_info, image=cond_info_icon)
        self.btn_cond_info.grid(row=3, column=0, sticky='n')
        self.btn_cond_info.image = cond_info_icon
        CreateToolTip(self.btn_cond_info, text="Condition Info", left_disp=True)

        self.btn_dice_roller = ttk.Button(master=self.tool_bar, command=self.open_dice_roller, image=d20_icon)
        self.btn_dice_roller.grid(row=4, column=0, sticky='n')
        self.btn_dice_roller.image = d20_icon
        CreateToolTip(self.btn_dice_roller, text="Dice Roller", left_disp=True)

        self.place_tokens()

    def initialize_tokens(self):
        self.map_win.token_list = []
        with ZipFile(self.master.filename, "r") as savefile:
            creat_bytes = savefile.read('creatures.json')
            creat_str = creat_bytes.decode('utf-8')
            creatures = json.loads(creat_str)
        for being in creatures.values():
            self.map_win.token_list.append(being)
    
    def place_tokens(self):
        self.initiative_holder = {}
        spaces_taken = []
        for being in self.map_win.token_list:
            token_type = being["type"]
            if token_type == "ally":
                token_img = self.ally_img
            elif token_type == "enemy":
                token_img = self.enemy_img
            elif token_type == "bystander":
                token_img = self.bystander_img
            elif token_type == "dead":
                token_img = self.dead_img
            else:
                raise NameError("Token type not specified.")
            
            occupied = False
            if being["coordinate"][0] != "" and being["coordinate"][1] != "":
                row_pos = int(being["coordinate"][1])
                col_pos = int(being["coordinate"][0])
                for space_tuple in spaces_taken:
                    if space_tuple[0] == row_pos and space_tuple[1] == col_pos and space_tuple[2] == int(being["coordinate"][2]):
                        occupied = True
                if occupied == False:
                    spaces_taken.append((row_pos, col_pos, int(being["coordinate"][2])))
                    lbl_unit = tk.Label(master=self.map_frames[col_pos][row_pos], image=token_img, bg="gray28", borderwidth=0)
                    lbl_unit.image = token_img
                    #space_count = len(self.map_frames[col_pos][row_pos].grid_slaves())
                    #row_count = int(space_count / 3)
                    #col_count = space_count % 3
                    #lbl_unit.grid(row=row_count, column=col_count, sticky='nsew')
                    lbl_unit.pack(fill='both', expand=True)
                    lbl_unit.bind("<Button-3>", self.em.right_click_menu)
                    CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                    if being['initiative'] != -math.inf:
                        self.initiative_holder[being['name']] = (being['initiative'], being['type'])
                    if being["size"] == "large" or being["size"] == "huge" or being["size"] == "gargantuan":
                        if being["size"] == "large":
                            space_need = 4
                        elif being["size"] == "huge":
                            space_need = 9
                        else:
                            space_need = 16
                        row_offset = 0
                        col_offset = 0
                        go_to_next_row = math.sqrt(space_need)
                        for i in range(1, space_need):
                            if i < space_need:
                                col_offset += 1
                                if col_offset == go_to_next_row:
                                    col_offset = 0
                                    row_offset += 1
                                row_pos = int(being["coordinate"][1]) + row_offset
                                col_pos = int(being["coordinate"][0]) + col_offset
                                lbl_unit = tk.Label(master=self.map_frames[col_pos][row_pos], image=token_img, bg="gray28", borderwidth=0)
                                lbl_unit.image = token_img
                                #space_count = len(self.map_frames[col_pos][row_pos].grid_slaves())
                                #row_count = int(space_count / 3)
                                #col_count = space_count % 3
                                #lbl_unit.grid(row=row_count, column=col_count)
                                lbl_unit.pack(fill='both', expand=True)
                                lbl_unit.bind("<Button-3>", self.em.right_click_menu)
                                CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                else:
                    messagebox.showerror("Internal Error", "Restart program\nError 0x006")
                    return

            else:
                self.unused_tokens(being, token_img)
            self.refresh_initiatives()
    
    def unused_tokens(self, creature, token_img):
        next_row = int(self.side_count / 2)
        next_col = self.side_count % 2
        lbl_side_unit = tk.Label(master=self.side_board, image=token_img, bg="gray28", borderwidth=0)
        lbl_side_unit.grid(row=next_row, column=next_col, padx=5, pady=5, sticky="ne")
        lbl_side_unit.bind("<Button-3>", self.em.right_click_menu)
        lbl_side_unit.image = token_img
        CreateToolTip(lbl_side_unit, text=creature["name"])
        self.side_count += 1
    
    def post_initiatives(self):
        init_dict_in_order = {k:v for k, v in sorted(self.initiative_holder.items(), key= lambda item: item[1][0], reverse=True)}
        order_count = 0
        lbl_turn_img = tk.Label(master=self.initiative_frame, image=self.turn_icon, bg="gray28", borderwidth=0)
        lbl_turn_img.grid(row=self.turn, column=0, sticky='w')
        lbl_turn_img.image = self.turn_icon

        for next_up in init_dict_in_order.items():
            if next_up[1][0] != math.inf and next_up[1][1] != 'dead':
                lbl_your_turn = ttk.Label(master=self.initiative_frame, text=f"{next_up[0]}: ", font=self.small_font)
                lbl_your_turn.grid(row=order_count, column=1, sticky='w')
                lbl_your_init = ttk.Label(master=self.initiative_frame, text=next_up[1][0], font=self.small_font)
                lbl_your_init.grid(row=order_count, column=2, sticky='e')
                order_count += 1

    def refresh_initiatives(self):
        init_frame_slaves = self.initiative_frame.grid_slaves()
        if len(init_frame_slaves):
            for item in init_frame_slaves:
                item.destroy()
        self.post_initiatives()

    def next_turn(self):
        on_board_inits = self.initiative_holder
        inf_exists = True
        fucked_up = 30
        while inf_exists and fucked_up > 0:
            for key, value in on_board_inits.items():
                if value == math.inf:
                    del on_board_inits[key]
                    break
            if math.inf not in on_board_inits:
                inf_exists = False
            fucked_up -= 1
        self.turn += 1
        if self.turn > len(self.initiative_holder) - 1:
            self.next_round()
        else:
            self.refresh_initiatives()

    def next_round(self):
        self.round += 1
        self.lbl_round.config(text=self.round)
        self.turn = 0
        self.refresh_initiatives()

    def reset_round(self):
        self.round = 0
        self.lbl_round.config(text="S")
        self.turn = 0
        self.refresh_initiatives()

    def refresh_map(self, reset=False):
        for row in self.map_frames:
            for col in row:
                remove_tokens = col.pack_slaves()#grid_slaves()
                if len(remove_tokens) > 0:
                    for token in remove_tokens:
                        token.destroy()
        remove_side_list = self.side_board.grid_slaves()
        if len(remove_side_list) > 0:
            for side_token in remove_side_list:
                side_token.destroy()
        self.side_count = 0

        if reset:
            self.initialize_tokens()

        self.refresh_initiatives()
        self.place_tokens()

    def save_game(self):
        new_token_dict = {}
        for being in self.map_win.token_list:
            name = being["name"]
            new_token_dict[name] = being
        battle_dict = {
            "mapSize": self.map_size,
            "round": self.round,
            "turn": self.turn
        }
        battleJSON = json.dumps(battle_dict, indent=4)
        with ZipFile(self.master.filename, "w") as savefile:
            creatJSON = json.dumps(new_token_dict, indent=4)
            savefile.writestr('battleInfo.json', battleJSON)
            savefile.writestr('creatures.json', creatJSON)

    def clear_map(self):
        for being in self.map_win.token_list:
            being["coordinate"] = ['', '', '']
        self.refresh_map()

    def input_creature_window(self):
        self.in_win = StatCollector(self.map_win, self.map_size, self.round, self.turn)
        self.in_win.btn_submit.configure(command=lambda arg=['in_win', 'submit']: self.change_token_list(arg))

    def change_token_list(self, arg):
        origin = arg[0]
        select_btn = arg[1]
        if origin == 'move_win':
            if select_btn == 'set':
                set_complete = self.em.set_new_coord()
                if set_complete:
                    self.em.move_win.destroy()
                    self.refresh_map()
            elif select_btn == 'remove':
                rem_complete = self.em.remove_token()
                if rem_complete:
                    self.em.move_win.destroy()
                    self.refresh_map()
        elif origin == 'target_win':
            if select_btn == 'submit':
                submit_complete = self.target.on_submit()
                if submit_complete:
                    self.target.target_win.destroy()
                    self.refresh_map()
            elif select_btn == 'delete':
                delete_complete = self.target.delete_token()
                if delete_complete:
                    self.target.target_win.destroy()
                    self.refresh_map()
        elif origin == 'in_win':
            if select_btn == 'submit':
                submit_complete = self.in_win.submit()
                if submit_complete:
                    self.in_win.range_win.destroy()
                    self.refresh_map()

    def move_token(self):
        self.em.move_token(self.map_size)
        self.em.btn_set.configure(command=lambda arg=['move_win', 'set']: self.change_token_list(arg))
        self.em.btn_remove.configure(command=lambda arg=['move_win', 'remove']: self.change_token_list(arg))
        #self.wait_destroy_move_win()

    def open_trig(self):
        self.calculator.trig_win()

    def target_item(self):
        self.target.target_window()
        self.target.btn_submit.configure(command=lambda arg=['target_win', 'submit']: self.change_token_list(arg))
        self.target.btn_delete_target.configure(command=lambda arg=['target_win', 'delete']: self.change_token_list(arg))
        #self.target.target_win.protocol("WM_DELETE_WINDOW", lambda stuff=(self.target.token_list): self.refresh_map(tokens=stuff, origWin='target'))

    def open_dice_roller(self):
        self.dice_roll.dice_pane()

    def full_reset(self):
        empty_dict = {}
        make_sure = messagebox.askokcancel("Warning", "Confirm request to delete ALL tokens and FULL RESET MAP.\nIf confirmed, this action cannot be undone.")
        if make_sure:
            battle_dict = {
                "mapSize": self.map_size,
                "round": 0,
                "turn": 0
            }
            battleJSON = json.dumps(battle_dict, indent=4)
            with ZipFile(self.master.filename, "w") as savefile:
                creatJSON = json.dumps(empty_dict)
                savefile.writestr('battleInfo.json', battleJSON)
                savefile.writestr('creatures.json', creatJSON)
            self.refresh_map(reset=True)

    def find_quote(self):
        last_index = len(self.quoter.quote_list) - 1
        rand_index = random.randint(0, last_index)
        random_quote = self.quoter.get_quote(rand_index)
        self.lbl_quote.config(text=random_quote)

    def show_cond_info(self):
        self.info.explain_conditions()
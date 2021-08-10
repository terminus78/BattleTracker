import math
import random
import json
import copy
from tkinter.constants import COMMAND

from zipfile import ZipFile
import PIL.Image
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from tooltip import *
from event_manager import EventManager
from calc import Calculator
from stat_collector import StatCollector
from quotes import Quote
from target import Target
from condition_info import InfoClass
from dice import DiceRoller
from player_window import PlayerWin
from starter import *
from undo_redo import ActionStack
from light_menu import *
from object_builder import ObjectBuilder


map_win = tk.Tk()
map_win.overrideredirect(1)
map_win.withdraw()

class BattleMap():
    def __init__(self, root):
        self.root = root
        self.reg_font = ('Papyrus', '14')
        self.small_font = ("Papyrus", "9")
        self.big_font = ("Papyrus", "16")
        self.start_win = StartWindow(self.root)
        self.start_win.btn_new_file.config(command=lambda: self.start_up_seq('new'))
        self.start_win.btn_open_existing.config(command=lambda: self.start_up_seq('open'))
        self.start_win.win_start.protocol('WM_DELETE_WINDOW', lambda: self.root.destroy())
        
    def start_up_seq(self, opt):
        if opt == 'new':
            self.start_win.new_file()
            self.start_win.btn_start_game.config(command=lambda: self.new_game_btns('start'))
            self.start_win.btn_cancel.config(command=lambda: self.new_game_btns('cancel'))
        elif opt == 'open':
            open_complete = self.start_win.open_file()
            if open_complete:
                self.start_win.win_start.destroy()
                self.main_window()

    def new_game_btns(self, btn):
        if btn == 'start':
            start_complete = self.start_win.start_new_battle()
            if start_complete:
                self.start_win.win_start.destroy()
                self.main_window()
        elif btn == 'cancel':
            self.start_win.game_start_win.destroy()
    
    def main_window(self):
        self.root.overrideredirect(0)

        game_title = self.root.game_name
        if len(game_title) > 32:
            game_title = game_title[0:32] + "..."
        self.root.title(f"Battle Map | {game_title}")
        style = ThemedStyle(self.root)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.root.configure(bg=style.lookup('TLabel', 'background'))

        # Window definition
        with ZipFile(self.root.filename, 'r') as savefile:
            battle_bytes = savefile.read('battle_info.json')
            battle_obj = json.loads(battle_bytes.decode('utf-8'))
            self.map_size = battle_obj['map_size']
            self.round = battle_obj['round']
            self.turn = battle_obj['turn']

        self.top_frame = ttk.Frame(master=self.root, borderwidth=2, relief='ridge')
        self.top_frame.pack(side='top', fill='both')
        self.top_frame.columnconfigure(1, weight=1)
        self.top_frame.rowconfigure(0, minsize=100, weight=1)
        self.quote_frame = ttk.Frame(master=self.root)
        self.quote_frame.pack(side='top', fill='x')
        self.quote_frame.columnconfigure(0, minsize=20)
        self.bottom_frame = ttk.Frame(master=self.root, borderwidth=2, relief='ridge')
        self.bottom_frame.pack(side='top', fill='both', expand=True)
        self.bottom_frame.columnconfigure(0, minsize=100)
        self.bottom_frame.columnconfigure(1, weight=1, minsize=500)
        self.bottom_frame.columnconfigure(2, minsize=150)
        self.bottom_frame.columnconfigure(3, minsize=50)
        self.bottom_frame.rowconfigure(0, weight=1, minsize=350)
        self.controller_frame = ttk.Frame(master=self.root)
        self.controller_frame.pack(side='top', fill='x')

        self.em = EventManager(self.root)
        self.calculator = Calculator(self.root)
        self.quoter = Quote()
        self.count_quotes = 0
        self.target = Target(self.root)
        self.info = InfoClass(self.root)
        self.dice_roll = DiceRoller(self.root)
        self.copy_win = PlayerWin(self.root, self.map_size, game_title)
        self.go_back = ActionStack(self.root)

        # Board Setup
        lbl_map = ttk.Label(master=self.top_frame, text=game_title, font=('Papyrus', '16'))
        lbl_map.grid(row=0, column=1)
        btn_player_win = ttk.Button(master=self.top_frame, command=self.open_for_players, text="Player Window")
        btn_player_win.grid(row=0, column=2, sticky='se')
        btn_save = ttk.Button(master=self.top_frame, command=self.save_game, text="Save")
        btn_save.grid(row=0, column=3, sticky='se')
        btn_clear = ttk.Button(master=self.top_frame, command=self.clear_map, text="Clear Map")
        btn_clear.grid(row=0, column=4, sticky='se')
        btn_input = ttk.Button(master=self.top_frame, command=self.input_creature_window, text="New Creature")
        btn_input.grid(row=0, column=5, sticky='se')
        btn_obj = ttk.Button(master=self.top_frame, command=self.input_object_window, text="New Object")
        btn_obj.grid(row=0, column=6, sticky='se')
        btn_reset = ttk.Button(master=self.top_frame, command=lambda: self.refresh_map(reset=True), text="Reset Map")
        btn_reset.grid(row=0, column=7, sticky='se')
        btn_restart = ttk.Button(master=self.top_frame, command=self.full_reset, text="Reset Battle")
        btn_restart.grid(row=0, column=8, sticky='se')
        btn_close_all = ttk.Button(master=self.top_frame, command=self.root.destroy, text="Close All")
        btn_close_all.grid(row=0, column=9, sticky='se')
        self.lbl_quote = ttk.Label(master=self.quote_frame, text="", font=self.reg_font)
        self.lbl_quote.grid(row=0, column=0, sticky='w', pady=5)
        self.find_quote()

        self.side_board = ttk.Frame(master=self.bottom_frame)
        self.side_board.grid(row=0, column=0, padx=5, pady=10, sticky="nw")
        self.side_count = 0

        canvas_frame = ttk.Frame(master=self.bottom_frame, borderwidth=2, relief='ridge')
        self.grid_canvas = tk.Canvas(master=canvas_frame, bg='gray28', bd=0, highlightthickness=0)
        grid_scroll_vert = ttk.Scrollbar(master=canvas_frame, command=self.grid_canvas.yview)
        grid_scroll_horz = ttk.Scrollbar(master=self.bottom_frame, orient='horizontal', command=self.grid_canvas.xview)
        self.grid_frame = ttk.Frame(master=self.grid_canvas)
        canvas_frame.grid(row=0, column=1, sticky="nsew")
        self.grid_canvas.pack(side='left', fill='both', expand=True)
        self.grid_canvas.config(yscrollcommand=grid_scroll_vert.set, xscrollcommand=grid_scroll_horz.set)
        grid_scroll_vert.pack(side='right', fill='y')
        grid_scroll_horz.grid(row=1, column=1, sticky='ew')
        self.grid_canvas.create_window((4,4), window=self.grid_frame, anchor='nw', tags='self.grid_frame')
        self.grid_frame.bind("<Configure>", self._on_config)
        self.grid_canvas.bind('<Enter>', self._on_enter_canvas)
        self.grid_canvas.bind('<Leave>', self._on_leave_canvas)
        self.grid_frame.lower()

        self.round_bar = ttk.Frame(master=self.bottom_frame)
        self.tool_bar = ttk.Frame(master=self.bottom_frame)
        self.round_bar.grid(row=0, column=2, padx=5, pady=10, sticky="nw")
        self.tool_bar.grid(row=0, column=3, padx=5, pady=10, sticky="nw")

        # Image paths
        undo_icon_path = "entry\\bin\\red_undo.png"
        undo_icon = ImageTk.PhotoImage(image=PIL.Image.open(undo_icon_path).resize((20,20)))
        redo_icon_path = "entry\\bin\\red_redo.png"
        redo_icon = ImageTk.PhotoImage(image=PIL.Image.open(redo_icon_path).resize((20,20)))
        move_icon_path = "entry\\bin\\red_icons8-circled-down-left-32.png"
        move_icon = ImageTk.PhotoImage(image=PIL.Image.open(move_icon_path).resize((20,20)))
        trig_icon_path = "entry\\bin\\red_trig.png"
        trig_icon = ImageTk.PhotoImage(image=PIL.Image.open(trig_icon_path).resize((20,20)))
        target_icon_path = "entry\\bin\\red_target.png"
        target_icon = ImageTk.PhotoImage(image=PIL.Image.open(target_icon_path).resize((20,20)))
        cond_info_icon_path = "entry\\bin\\red_page_icon.png"
        cond_info_icon = ImageTk.PhotoImage(image=PIL.Image.open(cond_info_icon_path).resize((20,20)))
        turn_icon_path = "entry\\bin\\swords.png"
        self.turn_icon = ImageTk.PhotoImage(image=PIL.Image.open(turn_icon_path).resize((20,20)))
        d20_icon_path = "entry\\bin\\red_role-playing.png"
        d20_icon = ImageTk.PhotoImage(image=PIL.Image.open(d20_icon_path).resize((20,20)))
        highlight_path = "entry\\bin\\highlight.png"
        highlight_img = ImageTk.PhotoImage(image=PIL.Image.open(highlight_path).resize((20,20)))

        ally_path = "entry\\bin\\ally_token.png"
        self.ally_img = ImageTk.PhotoImage(image=PIL.Image.open(ally_path).resize((30,30)))
        enemy_path = "entry\\bin\\enemy_token.png"
        self.enemy_img = ImageTk.PhotoImage(image=PIL.Image.open(enemy_path).resize((30,30)))
        bystander_path = "entry\\bin\\bystander_token.png"
        self.bystander_img = ImageTk.PhotoImage(image=PIL.Image.open(bystander_path).resize((30,30)))
        dead_path = "entry\\bin\\dead_token.png"
        self.dead_img = ImageTk.PhotoImage(image=PIL.Image.open(dead_path).resize((30,30)))

        up_btn_path = "entry\\bin\\up_button.png"
        down_btn_path = "entry\\bin\\down_button.png"
        left_btn_path = "entry\\bin\\left_button.png"
        right_btn_path = "entry\\bin\\right_button.png"
        nw_btn_path = "entry\\bin\\nw_button.png"
        ne_btn_path = "entry\\bin\\ne_button.png"
        sw_btn_path = "entry\\bin\\sw_button.png"
        se_btn_path = "entry\\bin\\se_button.png"
        z_up_btn_path = "entry\\bin\\z_up.png"
        undo_move_path = "entry\\bin\\undo_move.png"
        z_down_btn_path = "entry\\bin\\z_down.png"
        self.up_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(up_btn_path).resize((40,40)))
        self.down_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(down_btn_path).resize((40,40)))
        self.left_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(left_btn_path).resize((40,40)))
        self.right_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(right_btn_path).resize((40,40)))
        self.nw_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(nw_btn_path).resize((40,40)))
        self.ne_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(ne_btn_path).resize((40,40)))
        self.sw_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(sw_btn_path).resize((40,40)))
        self.se_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(se_btn_path).resize((40,40)))
        self.z_up_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(z_up_btn_path).resize((40,40)))
        self.undo_move_img = ImageTk.PhotoImage(image=PIL.Image.open(undo_move_path).resize((40,40)))
        self.z_down_btn_img = ImageTk.PhotoImage(image=PIL.Image.open(z_down_btn_path).resize((40,40)))
        
        self.map_frames = []
        self.root.token_list = []
        self.root.obj_list = []
        self.root.copy_win_open = False
        self.root.light_params = {}

        # Grid labels
        for col_spot in range(self.map_size[1]):
            lbl_grid_top = ttk.Label(master=self.grid_frame, text=col_spot+1, font=self.small_font)
            lbl_grid_top.grid(row=0, column=col_spot+1)
            self.grid_frame.columnconfigure(col_spot+1, minsize=33)#, weight=1)

        for row_spot in range(self.map_size[0]):
            lbl_grid_side = ttk.Label(master=self.grid_frame, text=row_spot+1, font=self.small_font)
            lbl_grid_side.grid(row=row_spot+1, column=0)
            self.grid_frame.rowconfigure(row_spot+1, minsize=33)#, weight=1)

        self.grid_frame.columnconfigure(0, minsize=33)#, weight=1)
        self.grid_frame.rowconfigure(0, minsize=33)#, weight=1)

        # Space frames
        self.token_labels = []
        for i in range(self.map_size[0]):
            self.map_frames.append([])
            self.token_labels.append([])
            for j in range(self.map_size[1]):
                self.space = tk.Frame(master=self.grid_frame, relief=tk.RAISED, borderwidth=1, bg='gray28')
                self.space.grid(row=i+1, column=j+1, sticky='nsew')
                self.space.coord = (j, i)
                CreateToolTip(self.space, text=f"{i+1}, {j+1}")
                self.map_frames[i].append(self.space)
                self.token_labels[i].append(None)
        
        self.initialize()

        go_back_frame = ttk.Frame(master=self.top_frame)
        go_back_frame.grid(row=0, column=0, sticky='nw')
        self.btn_undo = tk.Button(master=go_back_frame, command=lambda: self.time_travel(True), image=undo_icon, bd=0, bg='gray28', activebackground='gray28')
        self.btn_undo.grid(row=0, column=0, padx=5, pady=5, sticky='nw')
        self.btn_undo.image = undo_icon
        self.btn_undo['state'] = 'disabled'
        self.btn_redo = tk.Button(master=go_back_frame, command=lambda: self.time_travel(False), image=redo_icon, bd=0, bg='gray28', activebackground='gray28')
        self.btn_redo.grid(row=0, column=1, padx=5, pady=5, sticky='nw')
        self.btn_redo.image = redo_icon
        self.btn_redo['state'] = 'disabled'

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

        self.btn_field_light = ttk.Button(master=self.tool_bar, command=self.field_light, image=highlight_img)
        self.btn_field_light.grid(row=5, column=0, sticky='n')
        self.btn_field_light.image = highlight_img
        CreateToolTip(self.btn_field_light, text="Field Highlight", left_disp=True)

        #Controller Pane
        self.controller_frame.columnconfigure(0, weight=1)
        dpad_frame = ttk.Frame(master=self.controller_frame)
        dpad_frame.grid(row=0, column=0, rowspan=4, sticky='w', padx=100)
        btn_nw = tk.Button(master=dpad_frame, image=self.nw_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('nw'))
        btn_nw.grid(row=0, column=0)
        btn_nw.image = self.nw_btn_img
        btn_nw.name = 'nw'
        btn_up = tk.Button(master=dpad_frame, image=self.up_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('n'))
        btn_up.grid(row=0, column=1)
        btn_up.image = self.up_btn_img
        btn_up.name = 'up'
        btn_ne = tk.Button(master=dpad_frame, image=self.ne_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('ne'))
        btn_ne.grid(row=0, column=2)
        btn_ne.image = self.ne_btn_img
        btn_ne.name = 'ne'
        btn_left = tk.Button(master=dpad_frame, image=self.left_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('w'))
        btn_left.grid(row=1, column=0)
        btn_left.image = self.left_btn_img
        btn_left.name = 'w'
        btn_right = tk.Button(master=dpad_frame, image=self.right_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('e'))
        btn_right.grid(row=1, column=2)
        btn_right.image = self.right_btn_img
        btn_right.name = 'e'
        btn_sw = tk.Button(master=dpad_frame, image=self.sw_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('sw'))
        btn_sw.grid(row=2, column=0)
        btn_sw.image = self.sw_btn_img
        btn_sw.name = 'sw'
        btn_down = tk.Button(master=dpad_frame, image=self.down_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('s'))
        btn_down.grid(row=2, column=1)
        btn_down.image = self.down_btn_img
        btn_down.name = 's'
        btn_se = tk.Button(master=dpad_frame, image=self.se_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.dpad_move('se'))
        btn_se.grid(row=2, column=2)
        btn_se.image = self.se_btn_img
        btn_se.name = 'se'
        btn_z_up = tk.Button(master=dpad_frame, image=self.z_up_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.zpad('+'))
        btn_z_up.grid(row=0, column=3, padx=10)
        btn_z_up.image = self.z_up_btn_img
        btn_undo_move = tk.Button(master=dpad_frame, image=self.undo_move_img, bg='gray28', bd=0, activebackground='gray28', command=self.undo_move)
        btn_undo_move.grid(row=1, column=3, padx=10)
        btn_undo_move.image = self.undo_move_img
        btn_undo_move.name = 'undom'
        btn_z_down = tk.Button(master=dpad_frame, image=self.z_down_btn_img, bg='gray28', bd=0, activebackground='gray28', command=lambda: self.zpad('-'))
        btn_z_down.grid(row=2, column=3, padx=10)
        btn_z_down.image = self.z_down_btn_img
        self.z_frame = tk.Frame(master=dpad_frame, bg='gray28')
        self.z_frame.grid(row=1, column=1, sticky='nsew')
        self.z_frame.name = 'zf'

        cont_btn_frame = ttk.Frame(master=self.controller_frame)
        cont_btn_frame.grid(row=0, column=1, rowspan=4, sticky='e', padx=20)
        btn_turn_complete = ttk.Button(master=cont_btn_frame, text="Turn Complete", command=self.next_turn, width=19)
        btn_turn_complete.grid(row=0, column=0, columnspan=2)
        self.cont_targets = ttk.Combobox(master=cont_btn_frame, width=18, state='readonly')
        self.cont_targets.grid(row=1, column=0, columnspan=2)
        self.cont_targets.bind("<<ComboboxSelected>>", self._on_select_target)
        self.target_names = []
        self.ent_target_delta = ttk.Entry(master=cont_btn_frame, width=20)
        self.ent_target_delta.grid(row=2, column=0, columnspan=2, pady=5)
        self.ent_target_delta.insert(0, '0')
        self.ent_target_delta.bind("<FocusIn>", lambda e: self._on_delta_focus(event=e, typ='in'))
        self.ent_target_delta.bind("<FocusOut>", lambda e: self._on_delta_focus(event=e, typ='out'))
        btn_heal = ttk.Button(master=cont_btn_frame, text='Heal', command=lambda: self.target_hp('heal'), width=8)
        btn_heal.grid(row=3, column=0, padx=5, pady=5)
        btn_dmg = ttk.Button(master=cont_btn_frame, text='Damage', command=lambda: self.target_hp('dmg'), width=8)
        btn_dmg.grid(row=3, column=1, padx=5, pady=5)
        lbl_ac = ttk.Label(master=cont_btn_frame, text="AC: ", font=self.reg_font)
        lbl_ac.grid(row=0, column=2, sticky='w', pady=5)
        lbl_max_hp = ttk.Label(master=cont_btn_frame, text="Max HP: ", font=self.reg_font)
        lbl_max_hp.grid(row=1, column=2, sticky='w', pady=5)
        lbl_curr_hp = ttk.Label(master=cont_btn_frame, text="Current HP: ", font=self.reg_font)
        lbl_curr_hp.grid(row=2, column=2, sticky='w', pady=5)
        lbl_temp_hp = ttk.Label(master=cont_btn_frame, text="Temp HP: ", font=self.reg_font)
        lbl_temp_hp.grid(row=3, column=2, sticky='w', pady=5)
        self.lbl_target_ac = ttk.Label(master=cont_btn_frame, text="", font=self.reg_font)
        self.lbl_target_ac.grid(row=0, column=3, sticky='w', padx=5, pady=5)
        self.lbl_target_max_hp = ttk.Label(master=cont_btn_frame, text="", font=self.reg_font)
        self.lbl_target_max_hp.grid(row=1, column=3, sticky='w', padx=5, pady=5)
        self.lbl_target_hp = ttk.Label(master=cont_btn_frame, text="", font=self.reg_font)
        self.lbl_target_hp.grid(row=2, column=3, sticky='w', padx=5, pady=5)
        self.lbl_target_temp_hp = ttk.Label(master=cont_btn_frame, text="", font=self.reg_font)
        self.lbl_target_temp_hp.grid(row=3, column=3, sticky='w', padx=5, pady=5)

        lbl_title_turn = ttk.Label(master=self.controller_frame, text="Current Turn", font=self.big_font)
        lbl_title_turn.grid(row=0, column=2, sticky='e', padx=20)
        self.lbl_current_turn = tk.Label(master=self.controller_frame, text="", font=self.reg_font, bg='gray28')
        self.lbl_current_turn.grid(row=1, column=2, sticky='e', padx=20)
        lbl_title_pos = ttk.Label(master=self.controller_frame, text="Position", font=self.big_font)
        lbl_title_pos.grid(row=2, column=2, sticky='e', padx=20)
        self.lbl_position = ttk.Label(master=self.controller_frame, text="", font=self.reg_font)
        self.lbl_position.grid(row=3, column=2, sticky='e', padx=20)
        lbl_max_move_title = ttk.Label(master=self.controller_frame, text="Movement Speed", font=self.big_font)
        lbl_max_move_title.grid(row=0, column=3, sticky='e', padx=20)
        self.lbl_max_move = tk.Label(master=self.controller_frame, text="", font=self.reg_font, bg='gray28', fg='gray70')
        self.lbl_max_move.grid(row=1, column=3, sticky='e', padx=20)
        lbl_amount_move_title = ttk.Label(master=self.controller_frame, text="Feet Moved", font=self.big_font)
        lbl_amount_move_title.grid(row=2, column=3, sticky='e', padx=20)
        self.lbl_amount_moved = tk.Label(master=self.controller_frame, text="", font=self.reg_font, bg='gray28', fg='gray70')
        self.lbl_amount_moved.grid(row=3, column=3, sticky='e', padx=20)

        self.z_delta = 0

        self.root.bind("<Key>", self._on_numpad_keys)
        self.controller_frame.bind("<Button-1>", self._on_defocus)

        self.place_tokens()
        self.root.deiconify()

    def _on_config(self, event):
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox('all'))

    def _on_enter_canvas(self, event):
        self.grid_canvas.bind_all('<MouseWheel>', self._on_mousewheel)
        self.grid_canvas.bind_all('<Shift-MouseWheel>', self._on_shift_mousewheel)
    
    def _on_leave_canvas(self, event):
        self.grid_canvas.unbind_all('<MouseWheel>')
        self.grid_canvas.unbind_all('<Shift-MouseWheel>')

    def _on_mousewheel(self, event):
        self.grid_canvas.yview_scroll(int(-1*(event.delta/120)), 'units')

    def _on_shift_mousewheel(self, event):
        self.grid_canvas.xview_scroll(int(-1*(event.delta/120)), 'units')

    def _on_select_target(self, event):
        for being in self.root.token_list:
            if being['name'] == self.cont_targets.get():
                sel_obj = being
        self.lbl_target_ac.config(text=sel_obj['ac'])
        self.lbl_target_max_hp.config(text=sel_obj['max_HP'])
        self.lbl_target_hp.config(text=sel_obj['current_HP'])
        self.lbl_target_temp_hp.config(text=sel_obj['temp_HP'])

    def _on_numpad_keys(self, event):
        # Controller movements
        if event.keysym == '0' or event.keysym == 'Insert':
            self.undo_move()
        elif event.keysym == '1' or event.keysym == 'End':
            self.dpad_move('sw')
        elif event.keysym == '2' or event.keysym == 'Down':
            self.dpad_move('s')
        elif event.keysym == '3' or event.keysym == 'Next':
            self.dpad_move('se')
        elif event.keysym == '4' or event.keysym == 'Left':
            self.dpad_move('w')
        elif event.keysym == '5' or event.keysym == 'Clear':
            if self.z_delta != 0:
                if self.z_delta == 1:
                    self.dpad_move('+')
                elif self.z_delta == -1:
                    self.dpad_move('-')
        elif event.keysym == '6' or event.keysym == 'Right':
            self.dpad_move('e')
        elif event.keysym == '7' or event.keysym == 'Home':
            self.dpad_move('nw')
        elif event.keysym == '8' or event.keysym == 'Up':
            self.dpad_move('n')
        elif event.keysym == '9' or event.keysym == 'Prior':
            self.dpad_move('ne')
        elif event.keysym == 'minus':
            self.zpad('-')
        elif event.keysym == 'plus':
            self.zpad('+')
        elif event.keysym == 'Return':
            self.next_turn()
        
        if self.z_delta == 0:
            self.z_frame.config(bg='gray28')
            self.root.unbind_all("<Button-1>")

    def _on_delta_focus(self, event, typ):
        if typ == 'in':
            self.root.unbind("<Key>")
        elif typ == 'out':
            self.root.bind("<Key>", self._on_numpad_keys)

    def _on_defocus(self, event):
        event.widget.focus_set()

    def initialize(self):
        self.root.token_list = []
        self.root.obj_list = []
        with ZipFile(self.root.filename, "r") as savefile:
            creat_bytes = savefile.read('creatures.json')
            creat_str = creat_bytes.decode('utf-8')
            creatures = json.loads(creat_str)
            obj_bytes = savefile.read('objects.json')
            obj_str = obj_bytes.decode('utf-8')
            objects = json.loads(obj_str)
        for being in creatures.values():
            self.root.token_list.append(being)
        for thing in objects.values():
            self.root.obj_list.append(thing)

    def place_tokens(self):
        self.initiative_holder = {}
        spaces_taken = []
        self.target_names = []
        for item in self.root.obj_list:
            for key in item.keys():
                obj = item[key]
                occupied = False
                if obj["coordinate"][0] != "" and obj["coordinate"][1] != "":
                    row_pos = int(obj["coordinate"][1])
                    col_pos = int(obj["coordinate"][0])
                    self.target_names.append(key)
                    for space_tuple in spaces_taken:
                        if space_tuple[0] == row_pos and space_tuple[1] == col_pos and space_tuple[2] == int(obj["coordinate"][2]):
                            occupied = True
                    if occupied == False:
                        spaces_taken.append((row_pos, col_pos, int(obj["coordinate"][2])))
                        o_length = obj["length"]
                        o_width = obj["width"]
                        f_len = 5 * round(o_length / 5)
                        if f_len < 5:
                            f_len = 5
                        f_wid = 5 * round(o_width / 5)
                        if f_wid < 5:
                            f_wid = 5
                        o_col = int(f_wid / 5)
                        o_row = int(f_len / 5)
                        for x in range(o_col):
                            col_pos = obj["coordinate"][0] + x - 1
                            for y in range(o_row):
                                row_pos = obj["coordinate"][1] + y - 1
                                obj_img = ImageTk.PhotoImage(image=PIL.Image.open(obj["img_ref"]).resize((30,30)))
                                lbl_unit = tk.Label(master=self.map_frames[col_pos][row_pos], image=obj_img, bg="gray28", borderwidth=0)
                                lbl_unit.image = obj_img
                                lbl_unit.coord = (row_pos, col_pos)
                                lbl_unit.pack(fill='both', expand=True, padx=2, pady=2)
                                CreateToolTip(lbl_unit, text=f"{key}: {row_pos}, {col_pos}", left_disp=True)

        for being in self.root.token_list:
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
                self.target_names.append(being['name'])
                for space_tuple in spaces_taken:
                    if space_tuple[0] == row_pos and space_tuple[1] == col_pos and space_tuple[2] == int(being["coordinate"][2]):
                        occupied = True
                if occupied == False:
                    spaces_taken.append((row_pos, col_pos, int(being["coordinate"][2])))
                    lbl_unit = tk.Label(master=self.map_frames[col_pos][row_pos], image=token_img, bg="gray28", borderwidth=0)
                    lbl_unit.image = token_img
                    lbl_unit.coord = (row_pos, col_pos)
                    #space_count = len(self.map_frames[col_pos][row_pos].grid_slaves())
                    #row_count = int(space_count / 3)
                    #col_count = space_count % 3
                    #lbl_unit.grid(row=row_count, column=col_count, sticky='nsew')
                    lbl_unit.pack(fill='both', expand=True, padx=2, pady=2)
                    #lbl_unit.bind("<Button-3>", self.em.right_click_menu)
                    self.token_labels[col_pos][row_pos] = lbl_unit
                    CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                    if being['initiative'] != math.inf:
                        self.initiative_holder[being['name']] = being
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
                                lbl_unit.coord = (row_pos, col_pos)
                                #space_count = len(self.map_frames[col_pos][row_pos].grid_slaves())
                                #row_count = int(space_count / 3)
                                #col_count = space_count % 3
                                #lbl_unit.grid(row=row_count, column=col_count)
                                lbl_unit.pack(fill='both', expand=True)
                                #lbl_unit.bind("<Button-3>", self.em.right_click_menu)
                                #self.token_labels[row_pos][col_pos] = lbl_unit
                                CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                else:
                    messagebox.showerror("Internal Error", "Restart program\nError 0x006")
                    return

            else:
                self.unused_tokens(being, token_img)
        self.cont_targets.config(values=self.target_names)
        self.refresh_initiatives()
    
    def unused_tokens(self, creature, token_img):
        next_row = int(self.side_count / 2)
        next_col = self.side_count % 2
        lbl_side_unit = tk.Label(master=self.side_board, image=token_img, bg="gray28", borderwidth=0)
        lbl_side_unit.grid(row=next_row, column=next_col, padx=5, pady=5, sticky="ne")
        #lbl_side_unit.bind("<Button-3>", self.em.right_click_menu)
        lbl_side_unit.image = token_img
        CreateToolTip(lbl_side_unit, text=creature["name"])
        self.side_count += 1
    
    def post_initiatives(self):
        init_dict_in_order = {k:v for k, v in sorted(self.initiative_holder.items(), key= lambda item: item[1]['initiative'], reverse=True)}
        order_count = 0
        lbl_turn_img = tk.Label(master=self.initiative_frame, image=self.turn_icon, bg="gray28", borderwidth=0)
        lbl_turn_img.grid(row=self.turn, column=0, sticky='w')
        lbl_turn_img.image = self.turn_icon
        self.move_path = []

        for next_up in init_dict_in_order.items():
            if next_up[1]['initiative'] != math.inf and next_up[1]['type'] != 'dead':
                lbl_your_turn = ttk.Label(master=self.initiative_frame, text=f"{next_up[0]}: ", font=self.small_font)
                lbl_your_turn.grid(row=order_count, column=1, sticky='w')
                lbl_your_init = ttk.Label(master=self.initiative_frame, text=next_up[1]['initiative'], font=self.small_font)
                lbl_your_init.grid(row=order_count, column=2, sticky='e')
                if order_count == self.turn:
                    self.turn_obj = next_up[1]
                    curr_pos = (int(self.turn_obj['coordinate'][0]), int(self.turn_obj['coordinate'][1]), int(self.turn_obj['coordinate'][2]))
                    self.move_path.append(curr_pos)
                    self.lbl_current_turn.config(text=self.turn_obj['name'])
                    self.lbl_max_move.config(text=self.turn_obj['speed'])
                    self.lbl_position.config(text=f"{curr_pos[0]+1}: {curr_pos[1]+1}: {curr_pos[2]}")
                    self.lbl_amount_moved.config(text="0")
                    self.map_frames[curr_pos[0]][curr_pos[1]].config(bg='orange3')
                    if self.turn_obj['status'] == 'PC':
                        self.lbl_current_turn.config(fg='green3')
                    elif self.turn_obj['status'] == 'Monster':
                        self.lbl_current_turn.config(fg='orange3')
                    else:
                        self.lbl_current_turn.config(fg='DodgerBlue2')

                    if self.root.copy_win_open:
                        if self.turn_obj['status'] != 'PC':
                            self.copy_win.set_turn_lbl("X")
                        else:
                            self.copy_win.set_turn_lbl(self.turn_obj['name'])
                order_count += 1

    def refresh_initiatives(self):
        init_frame_slaves = self.initiative_frame.grid_slaves()
        if len(init_frame_slaves):
            for item in init_frame_slaves:
                item.destroy()
        for i in range(len(self.map_frames)):
            for frm in self.map_frames[i]:
                frm.config(bg='gray28')
        self.post_initiatives()

    def next_turn(self, not_from_redo=True):
        self.lbl_amount_moved.config(bg='gray28')
        if not_from_redo:
            self.log_action('turn button')
        on_board_inits = self.initiative_holder
        inf_exists = True
        fucked_up = 100
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
            for being in self.root.token_list:
                if being['name'] == self.turn_obj['name']:
                    being['coordinate'] = [str(self.move_path[-1][0]), str(self.move_path[-1][1]), str(self.move_path[-1][2])]
            self.refresh_map()
            #self.refresh_initiatives()

    def next_round(self, not_from_redo=True):
        if not_from_redo:
            self.log_action('round button', {'turn': self.turn})
        self.round += 1
        self.lbl_round.config(text=self.round)
        self.turn = 0
        for being in self.root.token_list:
            if being['name'] == self.turn_obj['name']:
                being['coordinate'] = [str(self.move_path[-1][0]), str(self.move_path[-1][1]), str(self.move_path[-1][2])]
        self.refresh_map()
        #self.refresh_initiatives()

    def reset_round(self, not_from_redo=True):
        if not_from_redo:
            restore_round = {
                'round': self.round,
                'turn': self.turn
            }
            self.log_action('reset round', restore_round)
        self.round = 0
        self.lbl_round.config(text="S")
        self.turn = 0
        self.refresh_map()
        #self.refresh_initiatives()

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
            self.initialize()
        self.place_tokens()
        if self.root.copy_win_open:
            self.copy_win.update_players()
        self.refresh_initiatives()

    def open_for_players(self):
        self.copy_win.start_win()
        self.refresh_map()

    def save_game(self):
        new_token_dict = {}
        for being in self.root.token_list:
            name = being["name"]
            new_token_dict[name] = being
        battle_dict = {
            "map_size": self.map_size,
            "round": self.round,
            "turn": self.turn
        }
        battleJSON = json.dumps(battle_dict, indent=4)
        with ZipFile(self.root.filename, "w") as savefile:
            creatJSON = json.dumps(new_token_dict, indent=4)
            savefile.writestr('battle_info.json', battleJSON)
            savefile.writestr('creatures.json', creatJSON)
        self.go_back.clear_all()

    def clear_map(self):
        restore_tokens = copy.deepcopy(self.root.token_list)
        self.log_action('list', restore_tokens)
        for being in self.root.token_list:
            being["coordinate"] = ['', '', '']
        self.refresh_map()

    def dpad_move(self, dir):
        last_pos = copy.deepcopy(self.move_path[-1])
        if dir == 'n':
            curr_pos = (last_pos[0] - 1, last_pos[1], last_pos[2] + self.z_delta)
        elif dir == 's':
            curr_pos = (last_pos[0] + 1, last_pos[1], last_pos[2] + self.z_delta)
        elif dir == 'w':
            curr_pos = (last_pos[0], last_pos[1] - 1, last_pos[2] + self.z_delta)
        elif dir == 'e':
            curr_pos = (last_pos[0], last_pos[1] + 1, last_pos[2] + self.z_delta)
        elif dir == 'ne':
            curr_pos = (last_pos[0] - 1, last_pos[1] + 1, last_pos[2] + self.z_delta)
        elif dir == 'se':
            curr_pos = (last_pos[0] + 1, last_pos[1] + 1, last_pos[2] + self.z_delta)
        elif dir == 'sw':
            curr_pos = (last_pos[0] + 1, last_pos[1] - 1, last_pos[2] + self.z_delta)
        elif dir == 'nw':
            curr_pos = (last_pos[0] - 1, last_pos[1] - 1, last_pos[2] + self.z_delta)
        else:
            curr_pos = (last_pos[0], last_pos[1], last_pos[2] + self.z_delta)
        
        if curr_pos[0] < 0 or curr_pos[0] > self.map_size[0] - 1 or curr_pos[1] < 0 or curr_pos[1] > self.map_size[1] - 1:
            messagebox.showwarning("BattleTracker", "Cannot move off map.")
            return
        
        self.z_delta = 0

        if self.turn_obj['size'] == 'large':
            space_need = 4
        elif self.turn_obj['size'] == 'huge':
            space_need = 9
        elif self.turn_obj['size'] == 'gargantuan':
            space_need = 16
        else:
            space_need = 1
        next_row_num = math.sqrt(space_need)
        row_offset = 0
        col_offset = 0

        if dir == '+':
            for i in range(space_need):
                self.map_frames[curr_pos[0] + col_offset][curr_pos[1] + row_offset].config(bg='orange1')
                col_offset += 1
                if col_offset == next_row_num:
                    col_offset = 0
                    row_offset += 1
        elif dir == '-':
            for i in range(space_need):
                self.map_frames[curr_pos[0] + col_offset][curr_pos[1] + row_offset].config(bg='DarkOrange4')
                col_offset += 1
                if col_offset == next_row_num:
                    col_offset = 0
                    row_offset += 1
        else:
            for i in range(space_need):
                self.map_frames[last_pos[0] + col_offset][last_pos[1] + row_offset].config(bg='orange4')
                col_offset += 1
                if col_offset == next_row_num:
                    col_offset = 0
                    row_offset += 1
            col_offset = 0
            row_offset = 0
            for i in range(space_need):
                self.map_frames[curr_pos[0] + col_offset][curr_pos[1] + row_offset].config(bg='orange3')
                col_offset += 1
                if col_offset == next_row_num:
                    col_offset = 0
                    row_offset += 1

        self.move_path.append(curr_pos)
        feet_moved = int(self.lbl_amount_moved.cget('text'))
        feet_moved += 5
        self.lbl_amount_moved.config(text=feet_moved)
        self.lbl_position.config(text=f"{curr_pos[0]+1}: {curr_pos[1]+1}: {curr_pos[2]}")
        if feet_moved > int(self.lbl_max_move.cget('text')):
            self.lbl_amount_moved.config(bg='red4')
        else:
            self.lbl_amount_moved.config(bg='gray28')

    def zpad(self, dir):
        if dir == '+':
            self.z_delta = 1
        else:
            self.z_delta = -1
        self.z_frame.config(bg='green3')
        self.root.bind_all("<Button-1>", self.green_handle)

    def green_handle(self, event):
        try:
            name = event.widget.name
            if name == 'zf':
                if self.z_delta == 1:
                    self.dpad_move('+')
                elif self.z_delta == -1:
                    self.dpad_move('-')
        except:
            pass
        self.z_frame.config(bg='gray28')
        self.root.unbind_all("<Button-1>")

    def target_hp(self, type):
        sel_target = self.cont_targets.get()
        tgt_delta = self.ent_target_delta.get()
        try:
            tgt_delta = int(tgt_delta)
            if type == 'dmg':
                tgt_delta *= -1
        except ValueError:
            messagebox.showwarning("BattleTracker", "HP difference must be a whole number.")
            return
        for being in self.root.token_list:
            if being['name'] == sel_target:
                if type == 'dmg' and abs(tgt_delta) > being['temp_HP']:
                    tgt_delta += being['temp_HP']
                    being['temp_HP'] = 0
                else:
                    being['temp_HP'] += tgt_delta
                    break
                being['current_HP'] += tgt_delta
                if being['current_HP'] > being['max_HP']:
                    being['current_HP'] = being['max_HP']
                elif being['current_HP'] <= 0:
                    being['type'] = 'dead'
        self._on_select_target(None)

    def input_creature_window(self):
        self.in_win = StatCollector(self.root, self.map_size, self.round, self.turn)
        self.in_win.btn_submit.configure(command=lambda arg=['in_win', 'submit']: self.change_token_list(arg))

    def input_object_window(self):
        self.obj_win = ObjectBuilder(self.root)
        try:
            self.obj_win.btn_submit.configure(command=lambda e: self.change_obj_list())
        except AttributeError:
            self.root.destroy()

    def change_obj_list(self):
        change_complete = self.obj_win.obj_win.submit()
        if change_complete:
            self.obj_win.obj_win.destroy()
            self.refresh_map()

    def change_token_list(self, arg):
        origin = arg[0]
        select_btn = arg[1]
        if origin == 'move_win':
            if select_btn == 'set':
                old_copy = copy.deepcopy(self.root.token_list)
                self.log_action('list', old_copy)
                set_complete = self.em.set_new_coord()
                if set_complete:
                    self.em.move_win.destroy()
                    self.refresh_map()
            elif select_btn == 'remove':
                old_copy = copy.deepcopy(self.root.token_list)
                self.log_action('list', old_copy)
                rem_complete = self.em.remove_token()
                if rem_complete:
                    self.em.move_win.destroy()
                    self.refresh_map()
        elif origin == 'target_win':
            if select_btn == 'submit':
                old_copy = copy.deepcopy(self.root.token_list)
                self.log_action('list', old_copy)
                submit_complete = self.target.on_submit()
                if submit_complete:
                    self.target.target_win.destroy()
                    self.refresh_map()
            elif select_btn == 'delete':
                old_copy = copy.deepcopy(self.root.token_list)
                self.log_action('list', old_copy)
                delete_complete = self.target.delete_token()
                if delete_complete:
                    self.target.target_win.destroy()
                    self.refresh_map()
        elif origin == 'in_win':
            if select_btn == 'submit':
                old_copy = copy.deepcopy(self.root.token_list)
                self.log_action('list', old_copy)
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

    def field_light(self):
        try:
            self.lighter.escape()
        except AttributeError:
            pass
        self.lighter = GenLightWin(self.root, self.btn_field_light)
        self.lighter.open_light_win()
        self.lighter.btn_confirm.config(command=self.get_offsets)

    def get_offsets(self):
        self.light_list, self.light_shape = self.lighter.collect()
        self.lighter.escape()
        if len(self.light_list) == 0:
            return
        for sect in range(len(self.map_frames)):
            for item in self.map_frames[sect]:
                item.bind("<Button-1>", self.on_light)
                pieces = item.pack_slaves()
                for piece in pieces:
                    piece.bind("<Button-1>", self.on_light)
        
    def on_light(self, event):
        start = list(event.widget.coord)
        if self.light_shape == 'Square':
            self.map_frames[start[1]][start[0]].config(bg='SpringGreen3')
        curr_pos = start
        for i in range(len(self.light_list)):
            curr_pos[0] += self.light_list[i][0]
            curr_pos[1] += self.light_list[i][1]
            if curr_pos[0] < self.map_size[1] and curr_pos[1] < self.map_size[0] and curr_pos[0] >= 0 and curr_pos[1] >= 0:
                self.map_frames[curr_pos[1]][curr_pos[0]].config(bg='SpringGreen3')
        start = list(event.widget.coord)
        if self.light_shape == 'Line':
            self.map_frames[start[1]][start[0]].config(bg='gray28')
        self.root.bind_all("<Escape>", self.clear_light)
        self.root.bind_all("<Button-3>", self.clear_light)

    def clear_light(self, event):
        for sect in range(len(self.map_frames)):
            for item in self.map_frames[sect]:
                item.config(bg='gray28')
                item.unbind("<Button-1>")
                pieces = item.pack_slaves()
                for piece in pieces:
                    piece.unbind("<Button-1>")
                self.root.unbind_all("<Escape>")
                self.root.unbind_all("<Button-3>")

    def full_reset(self):
        empty_dict = {}
        make_sure = messagebox.askokcancel("Warning", "Confirm request to delete ALL tokens and FULL RESET MAP.\nIf confirmed, this action cannot be undone.")
        if make_sure:
            battle_dict = {
                "map_size": self.map_size,
                "round": 0,
                "turn": 0
            }
            battleJSON = json.dumps(battle_dict, indent=4)
            with ZipFile(self.root.filename, "w") as savefile:
                creatJSON = json.dumps(empty_dict)
                savefile.writestr('battle_info.json', battleJSON)
                savefile.writestr('creatures.json', creatJSON)
            self.refresh_map(reset=True)
        self.go_back.clear_all()

    def find_quote(self):
        last_index = len(self.quoter.quote_list) - 1
        rand_index = random.randint(0, last_index)
        random_quote = self.quoter.get_quote(rand_index)
        self.lbl_quote.config(text=random_quote)

    def show_cond_info(self):
        self.info.explain_conditions()

    def time_travel(self, do_undo):
        if do_undo:
            hist_action = self.go_back.undo()
            if self.go_back.undo_empty():
                self.btn_undo['state'] = 'disabled'
            self.btn_redo['state'] = 'normal'
        else:
            hist_action = self.go_back.redo()
            if self.go_back.redo_empty():
                self.btn_redo['state'] = 'disabled'
            self.btn_undo['state'] = 'normal'

        action_name = hist_action['origin']
        
        if action_name == 'turn button':
            if do_undo:
                self.turn -= 1
                if self.turn < 0:
                    self.turn = len(self.initiative_holder) - 1
                    self.round -= 1
                    if self.round <= 0:
                        self.round = 0
                        self.lbl_round.config(text="S")
                    else:
                        self.lbl_round.config(text=self.round)
                    self.refresh_initiatives()
            else:
                self.next_turn(False)
        
        elif action_name == 'round button':
            if do_undo:
                self.round -= 1
                if self.round <= 0:
                    self.round = 0
                    self.lbl_round.config(text="S")
                else:
                    self.lbl_round.config(text=self.round)
                self.turn = hist_action['restore']['turn']
                self.refresh_initiatives()
            else:
                self.next_round(False)
        
        elif action_name == 'reset round':
            if do_undo:
                self.round = hist_action['restore']['round']
                self.turn = hist_action['restore']['turn']
                if self.round <= 0:
                    self.round = 0
                    self.lbl_round.config(text="S")
                else:
                    self.lbl_round.config(text=self.round)
                self.refresh_initiatives()
            else:
                self.reset_round(False)

        elif action_name == 'list':
                self.root.token_list = copy.deepcopy(hist_action['restore'])
                self.refresh_map()

    def undo_move(self):
        if len(self.move_path) > 1:
            last_move = self.move_path.pop()
        else:
            return
        if self.turn_obj['size'] == 'large':
            space_need = 4
        elif self.turn_obj['size'] == 'huge':
            space_need = 9
        elif self.turn_obj['size'] == 'gargantuan':
            space_need = 16
        else:
            space_need = 1
        next_row_num = math.sqrt(space_need)
        row_offset = 0
        col_offset = 0

        for i in range(space_need):
            self.map_frames[last_move[0] + col_offset][last_move[1] + row_offset].config(bg='gray28')
            col_offset += 1
            if col_offset == next_row_num:
                col_offset = 0
                row_offset += 1

        feet_moved = int(self.lbl_amount_moved.cget('text'))
        feet_moved -= 5
        self.lbl_amount_moved.config(text=feet_moved)
        if feet_moved > int(self.lbl_max_move.cget('text')):
            self.lbl_amount_moved.config(bg='red4')
        else:
            self.lbl_amount_moved.config(bg='gray28')
        new_curr_move = self.move_path[-1]
        self.lbl_position.config(text=f"{new_curr_move[0]+1}: {new_curr_move[1]+1}: {new_curr_move[2]}")
        row_offset = 0
        col_offset = 0
        for i in range(space_need):
            self.map_frames[new_curr_move[0] + col_offset][new_curr_move[1] + row_offset].config(bg='orange3')
            col_offset += 1
            if col_offset == next_row_num:
                col_offset = 0
                row_offset += 1

    def log_action(self, origin, restore_data=None):
        if self.btn_undo['state'] == 'disabled':
            self.btn_undo['state'] = 'normal'
        self.go_back.add_undo(origin, restore_data)
        if self.go_back.redo_empty() == False:
            self.go_back.clear_redo()
            self.btn_redo['state'] = 'disabled'

battle = BattleMap(map_win)

if __name__ == '__main__':
    map_win.mainloop()
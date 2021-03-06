import math

import PIL.Image
from PIL import ImageTk
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

from tooltip import *


class PlayerWin():
    def __init__(self, root, map_size, title):
        self.root = root
        self.title = title
        self.map_size = map_size
        self.reg_font = ('Papyrus', '14')
        self.small_font = ("Papyrus", "9")
        self.big_font = ("Papyrus", "16")

    def start_win(self):
        self.play_window = tk.Toplevel(self.root)
        self.play_window.title(f"Battle Map | {self.title}")
        style = ThemedStyle(self.play_window)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.play_window.configure(bg=style.lookup('TLabel', 'background'))
        self.root.copy_win_open = True
        self.play_window.protocol('WM_DELETE_WINDOW', self.destroy_play_window)
        '''
        self.play_window.columnconfigure(0, minsize=100)
        self.play_window.columnconfigure(1, weight=1, minsize=700)
        self.play_window.rowconfigure(0, weight=1, minsize=200)
        self.play_window.rowconfigure(2, weight=1, minsize=700)
        '''
        lbl_title = ttk.Label(master=self.play_window, text=self.title, font=self.big_font, borderwidth=2, relief='ridge')
        # lbl_title.grid(row=0, column=0, columnspan=2)
        lbl_title.pack(side='top', fill='both', ipady=20, ipadx=20)
        self.lbl_turn = tk.Label(master=self.play_window, text="", bg='gray28', fg='gray70', borderwidth=2, relief='ridge', anchor='center')
        # self.lbl_turn.grid(row=1, column=1, sticky='e', padx=30, pady=20)
        self.lbl_turn.pack(side='top', fill='both')
        self.lbl_turn.config(font=self.big_font)

        self.bottom_frame = ttk.Frame(master=self.play_window, borderwidth=2, relief='ridge')
        self.bottom_frame.pack(side='top', fill='both', expand=True)
        self.bottom_frame.columnconfigure(0, minsize=100)
        self.bottom_frame.columnconfigure(1, minsize=200, weight=1)
        self.bottom_frame.rowconfigure(0, minsize=200, weight=1)
        #self.bottom_frame.rowconfigure(1, minsize=700, weight=1)
        self.side_board = ttk.Frame(master=self.bottom_frame)
        self.side_board.grid(row=0, column=0, padx=5, pady=10, sticky="nw")
        self.side_count = 0
        canvas_frame = ttk.Frame(master=self.bottom_frame, borderwidth=2, relief='ridge')
        self.grid_canvas = tk.Canvas(master=canvas_frame, bg='gray28', borderwidth=0, highlightthickness=0)
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

        ally_path = "entry\\bin\\ally_token.png"
        self.ally_img = ImageTk.PhotoImage(image=PIL.Image.open(ally_path).resize((27,27)))
        enemy_path = "entry\\bin\\enemy_token.png"
        self.enemy_img = ImageTk.PhotoImage(image=PIL.Image.open(enemy_path).resize((27,27)))
        bystander_path = "entry\\bin\\bystander_token.png"
        self.bystander_img = ImageTk.PhotoImage(image=PIL.Image.open(bystander_path).resize((27,27)))
        dead_path = "entry\\bin\\dead_token.png"
        self.dead_img = ImageTk.PhotoImage(image=PIL.Image.open(dead_path).resize((27,27)))

        self.map_frames = []

        # Grid labels
        for col_spot in range(self.map_size[1]):
            lbl_grid_top = ttk.Label(master=self.grid_frame, text=col_spot+1, font=self.small_font)
            lbl_grid_top.grid(row=0, column=col_spot+1)
            self.grid_frame.columnconfigure(col_spot+1, weight=1, minsize=33)

        for row_spot in range(self.map_size[0]):
            lbl_grid_side = ttk.Label(master=self.grid_frame, text=row_spot+1, font=self.small_font)
            lbl_grid_side.grid(row=row_spot+1, column=0)
            self.grid_frame.rowconfigure(row_spot+1, weight=1, minsize=33)

        self.grid_frame.columnconfigure(0, weight=1, minsize=33)
        self.grid_frame.rowconfigure(0, weight=1, minsize=33)

        # Space frames
        for i in range(self.map_size[0]):
            self.map_frames.append([])
            for j in range(self.map_size[1]):
                self.space = tk.Frame(master=self.grid_frame, relief=tk.RAISED, borderwidth=1, bg='gray28')
                self.space.grid(row=i+1, column=j+1, sticky='nsew')
                CreateToolTip(self.space, text=f"{i+1}, {j+1}")
                self.map_frames[i].append(self.space)

        #self.set_board()

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

    def set_board(self):
        spaces_taken = []
        for item in self.root.obj_list:
            occupied = False
            if item["coordinate"][0] != "" and item["coordinate"][1] != "":
                row_pos = int(item["coordinate"][1])
                col_pos = int(item["coordinate"][0])
                for space_tuple in spaces_taken:
                    if space_tuple[0] == row_pos and space_tuple[1] == col_pos and space_tuple[2] == int(item["coordinate"][2]):
                        occupied = True
                if occupied == False:
                    spaces_taken.append((row_pos, col_pos, int(item["coordinate"][2])))
                    o_length = item["length"]
                    o_width = item["width"]
                    f_len = 5 * round(o_length / 5)
                    if f_len < 5:
                        f_len = 5
                    f_wid = 5 * round(o_width / 5)
                    if f_wid < 5:
                        f_wid = 5
                    o_col = int(f_wid / 5)
                    o_row = int(f_len / 5)
                    for x in range(o_col):
                        col_pos = int(item["coordinate"][0]) + x
                        for y in range(o_row):
                            row_pos = int(item["coordinate"][1]) + y
                            obj_img = ImageTk.PhotoImage(image=PIL.Image.open(item["img_ref"]).resize((30,30)))
                            lbl_unit = tk.Label(master=self.map_frames[col_pos][row_pos], image=obj_img, bg="gray28", borderwidth=0)
                            lbl_unit.image = obj_img
                            lbl_unit.coord = (row_pos, col_pos)
                            lbl_unit.pack(fill='both', expand=True, padx=2, pady=2)
                            CreateToolTip(lbl_unit, text=f"{item['name']}: {row_pos}, {col_pos}", left_disp=True)

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
                for space_tuple in spaces_taken:
                    if space_tuple[0] == row_pos and space_tuple[1] == col_pos and space_tuple[2] == int(being["coordinate"][2]):
                        occupied = True
                if occupied == False:
                    spaces_taken.append((row_pos, col_pos, int(being["coordinate"][2])))
                    lbl_unit = tk.Label(master=self.map_frames[col_pos][row_pos], image=token_img, bg="gray28", borderwidth=0)
                    lbl_unit.image = token_img
                    lbl_unit.coord = (row_pos, col_pos)
                    lbl_unit.pack(fill='both', expand=True, padx=2, pady=2)
                    CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
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
                                lbl_unit.pack(fill='both', expand=True)
                                CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                else:
                    messagebox.showerror("Internal Error", "Restart program\nError 0x006")
                    return

            else:
                self.unused_tokens(being, token_img)

    def set_turn_lbl(self, name):
        self.lbl_turn.config(text=name)
        if name != 'X':
            self.lbl_turn.config(fg='green3')
        else:
            self.lbl_turn.config(fg='gray70')

    def unused_tokens(self, creature, token_img):
        next_row = int(self.side_count / 2)
        next_col = self.side_count % 2
        lbl_side_unit = tk.Label(master=self.side_board, image=token_img, bg="gray28", borderwidth=0)
        lbl_side_unit.grid(row=next_row, column=next_col, padx=5, pady=5, sticky="ne")
        #lbl_side_unit.bind("<Button-3>", self.em.right_click_menu)
        lbl_side_unit.image = token_img
        CreateToolTip(lbl_side_unit, text=creature["name"])
        self.side_count += 1

    def update_players(self):
        for row in self.map_frames:
            for col in row:
                remove_tokens = col.pack_slaves()
                if len(remove_tokens) > 0:
                    for token in remove_tokens:
                        token.destroy()
        remove_side_list = self.side_board.grid_slaves()
        if len(remove_side_list) > 0:
            for side_token in remove_side_list:
                side_token.destroy()
        self.side_count = 0

        self.set_board()

    def track_moves(self, move_path):
        if len(move_path) < 1:
            return
        for coord in move_path:
            self.map_frames[coord[0]][coord[1]].config(bg='DarkOrange4')
        path_end = move_path[-1]
        self.map_frames[path_end[0]][path_end[1]].config(bg='orange1')

    def gray_map(self):
        for i in range(len(self.map_frames)):
            for j in range(len(self.map_frames[i])):
                self.map_frames[i][j].config(bg='gray28')

    def destroy_play_window(self):
        self.play_window.destroy()
        self.root.copy_win_open = False
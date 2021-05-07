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
        self.play_window.columnconfigure(0, minsize=100)
        self.play_window.columnconfigure(1, weight=1, minsize=200)
        self.play_window.rowconfigure(0, weight=1, minsize=100)
        lbl_title = ttk.Label(master=self.play_window, text=self.title, font=self.big_font)
        lbl_title.grid(row=0, column=0, columnspan=2)

        self.side_board = ttk.Frame(master=self.play_window)
        self.side_board.grid(row=1, column=0, padx=5, pady=10, sticky="nw")
        self.side_count = 0
        grid_frame = ttk.Frame(master=self.play_window, borderwidth=2, relief='ridge')
        grid_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

        ally_path = "entry\\bin\\ally_token.png"
        self.ally_img = ImageTk.PhotoImage(image=PIL.Image.open(ally_path).resize((15,15)))
        enemy_path = "entry\\bin\\enemy_token.png"
        self.enemy_img = ImageTk.PhotoImage(image=PIL.Image.open(enemy_path).resize((15,15)))
        bystander_path = "entry\\bin\\bystander_token.png"
        self.bystander_img = ImageTk.PhotoImage(image=PIL.Image.open(bystander_path).resize((15,15)))
        dead_path = "entry\\bin\\dead_token.png"
        self.dead_img = ImageTk.PhotoImage(image=PIL.Image.open(dead_path).resize((15,15)))

        self.map_frames = []

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

        self.set_board()

    def set_board(self):
        spaces_taken = []
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
                    #space_count = len(self.map_frames[col_pos][row_pos].grid_slaves())
                    #row_count = int(space_count / 3)
                    #col_count = space_count % 3
                    #lbl_unit.grid(row=row_count, column=col_count, sticky='nsew')
                    lbl_unit.pack(fill='both', expand=True)
                    #lbl_unit.bind("<Button-3>", self.em.right_click_menu)
                    CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                    #if being['initiative'] != -math.inf:
                        #self.initiative_holder[being['name']] = (being['initiative'], being['type'])
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
                                #lbl_unit.bind("<Button-3>", self.em.right_click_menu)
                                CreateToolTip(lbl_unit, text="{0}, {1}".format(being["name"], being["coordinate"][2]), left_disp=True)
                else:
                    messagebox.showerror("Internal Error", "Restart program\nError 0x006")
                    return

            else:
                self.unused_tokens(being, token_img)

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
                remove_tokens = col.pack_slaves()#grid_slaves()
                if len(remove_tokens) > 0:
                    for token in remove_tokens:
                        token.destroy()
        remove_side_list = self.side_board.grid_slaves()
        if len(remove_side_list) > 0:
            for side_token in remove_side_list:
                side_token.destroy()
        self.side_count = 0

        self.set_board()

    def destroy_play_window(self):
        self.play_window.destroy()
        self.root.copy_win_open = False
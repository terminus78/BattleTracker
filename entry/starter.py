import os
import json
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ttkthemes import ThemedStyle

from stat_collector import StatCollector
from tooltip import *


'''
window = tk.Tk()
window.title("Battle Tracker")
#window.iconphoto(True, tk.PhotoImage(file='entry/bin/allyToken.png'))
window.columnconfigure(0, minsize=200)
window.rowconfigure([0, 1, 2], minsize=50)
style_dark = ThemedStyle(window)
style_dark.theme_use("equilux")
bg = style_dark.lookup('TLabel', 'background')
fg = style_dark.lookup('TLabel', 'foreground')
window.configure(bg=style_dark.lookup('TLabel', 'background'))
papyrus_font = ('Papyrus', 14)
window_width = window.winfo_reqwidth()
window_height = window.winfo_reqheight()
position_horizontal = int(window.winfo_screenwidth()/2 - window_width/2)
position_vertical = int(window.winfo_screenheight()/2 - window_height/2)
window.geometry("+{}+{}".format(position_horizontal, position_vertical))
'''

class StartWindow():
    def __init__(self, master):
        self.master = master
        self.win_start = tk.Toplevel(self.master)
        self.win_start.title("Battle Tracker")
        self.win_start.columnconfigure(0, minsize=200)
        self.win_start.rowconfigure([0, 1, 2], minsize=50)
        style_dark = ThemedStyle(self.win_start)
        style_dark.theme_use("equilux")
        bg = style_dark.lookup('TLabel', 'background')
        fg = style_dark.lookup('TLabel', 'foreground')
        self.win_start.configure(bg=style_dark.lookup('TLabel', 'background'))
        self.papyrus_font = ('Papyrus', 14)
        self.countdown = 3
        self.master.cwd = os.getcwd()
        self.cache_loc = self.master.cwd + "\\entry\\bin\\cache.json"
        self.done = False
        try:
            with open(self.cache_loc, 'r') as cache_file:
                self.cache_info = json.load(cache_file)
        except IOError:
            with open(self.cache_loc, 'w') as cache_file:
                default_loc = {
                    'last_dir': 'C:\\'
                }
                json.dump(default_loc, cache_file, indent=4)
            with open(self.cache_loc, 'r') as cache_file:
                self.cache_info = json.load(cache_file)

        self.top_frame = ttk.Frame(master=self.win_start)
        self.top_frame.grid(row=0, column=0)
        self.bottom_frame = ttk.Frame(master=self.win_start)
        self.bottom_frame.grid(row=1, column=0)
        self.warning_frame = ttk.Frame(master=self.win_start)
        self.warning_frame.grid(row=2, column=0)
        self.lbl_greeting = ttk.Label(master=self.top_frame, text="Welcome to the BattleTracker", font=self.papyrus_font)
        self.lbl_greeting.grid(row=0, column=0)
        self.btn_new_file = ttk.Button(master=self.bottom_frame, text="New Game")#, command=self.new_file)
        self.btn_new_file.grid(row=0, column=0, sticky='e')
        self.btn_open_existing = ttk.Button(master=self.bottom_frame, text="Open Existing")#, command=self.open_file)
        self.btn_open_existing.grid(row=0, column=1, sticky='w')

    def new_file(self):
        self.game_start_win = tk.Toplevel(master=self.win_start)
        self.game_start_win.title("New Game")
        style = ThemedStyle(self.game_start_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.game_start_win.configure(bg=style.lookup('TLabel', 'background'))
        container_frame = ttk.Frame(master=self.game_start_win)
        container_frame.pack(padx=15, pady=15)
        upper_frame = ttk.Frame(master=container_frame)
        upper_frame.grid(row=0, column=0)
        file_frame = ttk.Frame(master=container_frame)
        file_frame.grid(row=1, column=0)
        finish_frame = ttk.Frame(master=container_frame)
        finish_frame.grid(row=2, column=0, sticky='e')
        lbl_top = ttk.Label(master=upper_frame, text="New Game", font=self.papyrus_font)
        lbl_top.grid(row=0, column=0)
        lbl_select_file_loc = ttk.Label(master=file_frame, text="Select file location", font=self.papyrus_font)
        lbl_select_file_loc.grid(row=0, column=0, sticky='w')
        self.ent_file_loc = ttk.Entry(master=file_frame, width=50)
        self.ent_file_loc.insert(0, self.cache_info['last_dir'])
        self.ent_file_loc.grid(row=1, column=0, sticky='w')
        btn_look_up_file = ttk.Button(master=file_frame, text="...", width=2, command=self.look_up_command)
        btn_look_up_file.grid(row=1, column=1, sticky='w')
        lbl_new_name = ttk.Label(master=file_frame, text="Enter file name", font=self.papyrus_font)
        lbl_new_name.grid(row=2, column=0, sticky='w')
        self.entnew_filename = ttk.Entry(master=file_frame, width=27)
        self.entnew_filename.grid(row=3, column=0, sticky='w')
        lbl_map_size_select = ttk.Label(master=file_frame, text="Select map size", font=self.papyrus_font)
        lbl_map_size_select.grid(row=2, column=1, sticky='w')
        self.map_choice = ["Tiny (8 X 12)", "Small (16 X 24)", "Medium (24 X 36)", "Large (32 X 46)"]
        self.cbx_map_sizes = ttk.Combobox(master=file_frame, width=27, values=self.map_choice, state='readonly')
        self.cbx_map_sizes.grid(row=3, column=1, sticky='w')
        self.btn_start_game = ttk.Button(master=finish_frame, text="Start Game")#, command=self.start_new_battle)
        self.btn_cancel = ttk.Button(master=finish_frame, text="Cancel")#, command=self.game_start_win.destroy)
        self.btn_cancel.pack(side=tk.RIGHT)
        self.btn_start_game.pack(side=tk.RIGHT)

    def start_new_battle(self):
        file_location = self.ent_file_loc.get()
        if os.path.isdir(file_location) == False:
            messagebox.showerror("New Game", "File location does not exist or your access level requires elevation.")
            return False
        self.master.game_name = self.entnew_filename.get()
        if file_location == "" or self.master.game_name == "":
            messagebox.showwarning("New Game", "File location and name fields cannot be empty.")
            return False
        self.master.filename = file_location + "\\" + self.master.game_name + ".brpg"

        selected_map = self.cbx_map_sizes.get()
        if selected_map == "Tiny (8 X 12)":
            map_size = [8, 12]
        elif selected_map == "Small (16 X 24)":
            map_size = [16, 24]
        elif selected_map == "Medium (24 X 36)":
            map_size = [24, 36]
        elif selected_map == "Large (32 X 46)":
            map_size = [32, 46]
        else:
            messagebox.showwarning("New Game", "Map size must be selected.")
            return False

        battle_dict = {
            "map_size": map_size,
            "round": 0,
            "turn": 0
        }
        battleJSON = json.dumps(battle_dict, indent=4)
        with ZipFile(self.master.filename, 'w') as brpg_file:
            brpg_file.writestr("battle_info.json", battleJSON)
            brpg_file.writestr("creatures.json", "{}")
        save_dir = os.path.dirname(self.master.filename)
        if save_dir != self.cache_info['last_dir']:
            self.cache_info['last_dir'] = save_dir
            with open(self.cache_loc, 'w') as cache_file:
                json.dump(self.cache_info, cache_file, indent=4)
        return True

    def look_up_command(self):
        self.master.filedir = filedialog.askdirectory()
        self.ent_file_loc.delete(0, 'end')
        self.ent_file_loc.insert(0, self.master.filedir)

    def open_file(self):
        self.master.filename = filedialog.askopenfilename(initialdir=self.cache_info['last_dir'], title='Select File', filetypes=(('BRPG files', '*.brpg'),))
        if type(self.master.filename) is str and self.master.filename != "":
            if os.path.exists(self.master.filename) == False:
                messagebox.showerror("Start Game", "File location does not exist or your access level requires elevation.")
                return False
            save_dir = os.path.dirname(self.master.filename)
            if save_dir != self.cache_info['last_dir']:
                self.cache_info['last_dir'] = save_dir
                with open(self.cache_loc, 'w') as cache_file:
                    json.dump(self.cache_info, cache_file, indent=4)
            game_file = os.path.split(self.master.filename)[-1]
            self.master.game_name = game_file.split('.')[0]
        return True
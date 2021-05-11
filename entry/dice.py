import math
import random

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle
import PIL.Image
from PIL import ImageTk


class DiceRoller():
    def __init__(self, root=None):
        self.die_options = [2, 4, 6, 8, 10, 12, 20, 100]
        self.root = root
        self.title_font = ("Papyrus", "18")
        self.font = ("Papyrus", "14")
        self.font_small = ("Papyrus", "9")
    
    def roll(self, die_size=20, num_dice=1):
        if die_size not in self.die_options:
            return [0]
        if type(num_dice) != int or num_dice < 1:
            return [0]
        dice_results = []
        for i in range(num_dice):
            roll_die = random.randint(1, die_size)
            dice_results.append(roll_die)
        return dice_results

    def dice_pane(self):
        self.dice_win = tk.Toplevel(self.root)
        self.dice_win.title("Trig Calculator")
        style = ThemedStyle(self.dice_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.dice_win.configure(bg=style.lookup('TLabel', 'background'))
        screen_width = self.dice_win.winfo_screenwidth()
        screen_height = self.dice_win.winfo_screenheight()
        self.dice_win.maxsize(screen_width, screen_height)
        lbl_title = ttk.Label(master=self.dice_win, text="Dice Roller", font=self.title_font)
        lbl_title.grid(row=0, column=0)
        self.dice_win.rowconfigure(1, weight=1)
        lbl_instructions = ttk.Label(master=self.dice_win, text="Select the type and number of each that you would like to roll.", font=self.font_small)
        lbl_instructions.grid(row=1, column=0)
        dice_selection_frame = ttk.Frame(master=self.dice_win)
        dice_selection_frame.grid(row=2, column=0)
        dice_selection_frame.rowconfigure(3, weight=1)
        dice_selection_frame.columnconfigure([0,1,2,3,4,5,6], weight=1)
        result_frame = ttk.Frame(master=self.dice_win)
        result_frame.grid(row=3, column=0, pady=10)

        # Image paths
        d20_path = "entry\\bin\\dice-twenty-faces-twenty.png"
        d20_pic = ImageTk.PhotoImage(image=PIL.Image.open(d20_path).resize((50,50)))
        d12_path = "entry\\bin\\d12.png"
        d12_pic = ImageTk.PhotoImage(image=PIL.Image.open(d12_path).resize((50,50)))
        d10_path = "entry\\bin\\d10.png"
        d10_pic = ImageTk.PhotoImage(image=PIL.Image.open(d10_path).resize((50,50)))
        d8_path = "entry\\bin\\dice-eight-faces-eight.png"
        d8_pic = ImageTk.PhotoImage(image=PIL.Image.open(d8_path).resize((50,50)))
        d6_path = "entry\\bin\\perspective-dice-six-faces-six.png"
        d6_pic = ImageTk.PhotoImage(image=PIL.Image.open(d6_path).resize((50,50)))
        d4_path = "entry\\bin\\d4.png"
        d4_pic = ImageTk.PhotoImage(image=PIL.Image.open(d4_path).resize((50,50)))
        #coin_path = "entry\\bin\\coin.png"
        #coin_pic = ImageTk.PhotoImage(image=PIL.Image.open(coin_path).resize((50,50)))
        red_d20_path = "entry\\bin\\red-dice-twenty-faces-twenty.png"
        red_d20_pic = ImageTk.PhotoImage(image=PIL.Image.open(red_d20_path).resize((50,50)))
        red_d12_path = "entry\\bin\\red-d12.png"
        red_d12_pic = ImageTk.PhotoImage(image=PIL.Image.open(red_d12_path).resize((50,50)))
        red_d10_path = "entry\\bin\\red-d10.png"
        red_d10_pic = ImageTk.PhotoImage(image=PIL.Image.open(red_d10_path).resize((50,50)))
        red_d8_path = "entry\\bin\\red-dice-eight-faces-eight.png"
        red_d8_pic = ImageTk.PhotoImage(image=PIL.Image.open(red_d8_path).resize((50,50)))
        red_d6_path = "entry\\bin\\red-perspective-dice-six-faces-six.png"
        red_d6_pic = ImageTk.PhotoImage(image=PIL.Image.open(red_d6_path).resize((50,50)))
        red_d4_path = "entry\\bin\\red-d4.png"
        red_d4_pic = ImageTk.PhotoImage(image=PIL.Image.open(red_d4_path).resize((50,50)))

        lbl_d100_title = ttk.Label(master=dice_selection_frame, text="D100", font=self.font)
        lbl_d100_title.image = red_d10_pic
        lbl_d100_title.grid(row=0, column=0)
        lbl_d20_title = ttk.Label(master=dice_selection_frame, text="D20", font=self.font)
        lbl_d20_title.image = red_d20_pic
        lbl_d20_title.grid(row=0, column=1)
        lbl_d12_title = ttk.Label(master=dice_selection_frame, text="D12", font=self.font)
        lbl_d12_title.image = red_d12_pic
        lbl_d12_title.grid(row=0, column=2)
        lbl_d10_title = ttk.Label(master=dice_selection_frame, text="D10", font=self.font)
        lbl_d10_title.image = red_d10_pic
        lbl_d10_title.grid(row=0, column=3)
        lbl_d8_title = ttk.Label(master=dice_selection_frame, text="D8", font=self.font)
        lbl_d8_title.image = red_d8_pic
        lbl_d8_title.grid(row=0, column=4)
        lbl_d6_title = ttk.Label(master=dice_selection_frame, text="D6", font=self.font)
        lbl_d6_title.image = red_d6_pic
        lbl_d6_title.grid(row=0, column=5)
        lbl_d4_title = ttk.Label(master=dice_selection_frame, text="D4", font=self.font)
        lbl_d4_title.image = red_d4_pic
        lbl_d4_title.grid(row=0, column=6)
        #lbl_coin_title = ttk.Label(master=dice_selection_frame, text="Coin", font=self.font)
        #lbl_coin_title.image = coin_pic
        #lbl_coin_title.grid(row=0, column=7)

        lbl_d100 = ttk.Label(master=dice_selection_frame, image=red_d10_pic)
        lbl_d100.image = red_d10_pic
        lbl_d100.grid(row=1, column=0)
        lbl_d20 = ttk.Label(master=dice_selection_frame, image=red_d20_pic)
        lbl_d20.image = red_d20_pic
        lbl_d20.grid(row=1, column=1)
        lbl_d12 = ttk.Label(master=dice_selection_frame, image=red_d12_pic)
        lbl_d12.image = red_d12_pic
        lbl_d12.grid(row=1, column=2)
        lbl_d10 = ttk.Label(master=dice_selection_frame, image=red_d10_pic)
        lbl_d10.image = red_d10_pic
        lbl_d10.grid(row=1, column=3)
        lbl_d8 = ttk.Label(master=dice_selection_frame, image=red_d8_pic)
        lbl_d8.image = red_d8_pic
        lbl_d8.grid(row=1, column=4)
        lbl_d6 = ttk.Label(master=dice_selection_frame, image=red_d6_pic)
        lbl_d6.image = red_d6_pic
        lbl_d6.grid(row=1, column=5)
        lbl_d4 = ttk.Label(master=dice_selection_frame, image=red_d4_pic)
        lbl_d4.image = red_d4_pic
        lbl_d4.grid(row=1, column=6)
        #lbl_coin = ttk.Label(master=dice_selection_frame, image=coin_pic)
        #lbl_coin.image = coin_pic
        #lbl_coin.grid(row=1, column=7)

        frame_d100 = ttk.Frame(master=dice_selection_frame)
        frame_d100.grid(row=2, column=0, padx=10)
        frame_d20 = ttk.Frame(master=dice_selection_frame)
        frame_d20.grid(row=2, column=1, padx=10)
        frame_d12 = ttk.Frame(master=dice_selection_frame)
        frame_d12.grid(row=2, column=2, padx=10)
        frame_d10 = ttk.Frame(master=dice_selection_frame)
        frame_d10.grid(row=2, column=3, padx=10)
        frame_d8 = ttk.Frame(master=dice_selection_frame)
        frame_d8.grid(row=2, column=4, padx=10)
        frame_d6 = ttk.Frame(master=dice_selection_frame)
        frame_d6.grid(row=2, column=5, padx=10)
        frame_d4 = ttk.Frame(master=dice_selection_frame)
        frame_d4.grid(row=2, column=6, padx=10)
        #frame_coin = ttk.Frame(master=dice_selection_frame)
        #frame_coin.grid(row=2, column=7, padx=10)

        # Modifiers
        lbl_100_mod = ttk.Label(master=frame_d100, text="Mod", font=self.font_small)
        lbl_100_mod.grid(row=0, column=0, columnspan=3)
        btn_100_lower_mod = ttk.Button(master=frame_d100, text="-", command=lambda: self.modify_mod(die='100', dir='-'), width=2)
        btn_100_lower_mod.grid(row=1, column=0)
        self.ent_100_mod = ttk.Entry(master=frame_d100, width=5)
        self.ent_100_mod.grid(row=1, column=1)
        self.ent_100_mod.insert(0, '0')
        btn_100_raise_mod = ttk.Button(master=frame_d100, text="+", command=lambda: self.modify_mod(die='100', dir='+'), width=2)
        btn_100_raise_mod.grid(row=1, column=2)

        lbl_20_mod = ttk.Label(master=frame_d20, text="Mod", font=self.font_small)
        lbl_20_mod.grid(row=0, column=0, columnspan=3)
        btn_20_lower_mod = ttk.Button(master=frame_d20, text="-", command=lambda: self.modify_mod(die='20', dir='-'), width=2)
        btn_20_lower_mod.grid(row=1, column=0)
        self.ent_20_mod = ttk.Entry(master=frame_d20, width=5)
        self.ent_20_mod.grid(row=1, column=1)
        self.ent_20_mod.insert(0, '0')
        btn_20_raise_mod = ttk.Button(master=frame_d20, text="+", command=lambda: self.modify_mod(die='20', dir='+'), width=2)
        btn_20_raise_mod.grid(row=1, column=2)

        lbl_12_mod = ttk.Label(master=frame_d12, text="Mod", font=self.font_small)
        lbl_12_mod.grid(row=0, column=0, columnspan=3)
        btn_12_lower_mod = ttk.Button(master=frame_d12, text="-", command=lambda: self.modify_mod(die='12', dir='-'), width=2)
        btn_12_lower_mod.grid(row=1, column=0)
        self.ent_12_mod = ttk.Entry(master=frame_d12, width=5)
        self.ent_12_mod.grid(row=1, column=1)
        self.ent_12_mod.insert(0, '0')
        btn_12_raise_mod = ttk.Button(master=frame_d12, text="+", command=lambda: self.modify_mod(die='12', dir='+'), width=2)
        btn_12_raise_mod.grid(row=1, column=2)

        lbl_10_mod = ttk.Label(master=frame_d10, text="Mod", font=self.font_small)
        lbl_10_mod.grid(row=0, column=0, columnspan=3)
        btn_10_lower_mod = ttk.Button(master=frame_d10, text="-", command=lambda: self.modify_mod(die='10', dir='-'), width=2)
        btn_10_lower_mod.grid(row=1, column=0)
        self.ent_10_mod = ttk.Entry(master=frame_d10, width=5)
        self.ent_10_mod.grid(row=1, column=1)
        self.ent_10_mod.insert(0, '0')
        btn_10_raise_mod = ttk.Button(master=frame_d10, text="+", command=lambda: self.modify_mod(die='10', dir='+'), width=2)
        btn_10_raise_mod.grid(row=1, column=2)

        lbl_8_mod = ttk.Label(master=frame_d8, text="Mod", font=self.font_small)
        lbl_8_mod.grid(row=0, column=0, columnspan=3)
        btn_8_lower_mod = ttk.Button(master=frame_d8, text="-", command=lambda: self.modify_mod(die='8', dir='-'), width=2)
        btn_8_lower_mod.grid(row=1, column=0)
        self.ent_8_mod = ttk.Entry(master=frame_d8, width=5)
        self.ent_8_mod.grid(row=1, column=1)
        self.ent_8_mod.insert(0, '0')
        btn_8_raise_mod = ttk.Button(master=frame_d8, text="+", command=lambda: self.modify_mod(die='8', dir='+'), width=2)
        btn_8_raise_mod.grid(row=1, column=2)

        lbl_6_mod = ttk.Label(master=frame_d6, text="Mod", font=self.font_small)
        lbl_6_mod.grid(row=0, column=0, columnspan=3)
        btn_6_lower_mod = ttk.Button(master=frame_d6, text="-", command=lambda: self.modify_mod(die='6', dir='-'), width=2)
        btn_6_lower_mod.grid(row=1, column=0)
        self.ent_6_mod = ttk.Entry(master=frame_d6, width=5)
        self.ent_6_mod.grid(row=1, column=1)
        self.ent_6_mod.insert(0, '0')
        btn_6_raise_mod = ttk.Button(master=frame_d6, text="+", command=lambda: self.modify_mod(die='6', dir='+'), width=2)
        btn_6_raise_mod.grid(row=1, column=2)

        lbl_4_mod = ttk.Label(master=frame_d4, text="Mod", font=self.font_small)
        lbl_4_mod.grid(row=0, column=0, columnspan=3)
        btn_4_lower_mod = ttk.Button(master=frame_d4, text="-", command=lambda: self.modify_mod(die='4', dir='-'), width=2)
        btn_4_lower_mod.grid(row=1, column=0)
        self.ent_4_mod = ttk.Entry(master=frame_d4, width=5)
        self.ent_4_mod.grid(row=1, column=1)
        self.ent_4_mod.insert(0, '0')
        btn_4_raise_mod = ttk.Button(master=frame_d4, text="+", command=lambda: self.modify_mod(die='4', dir='+'), width=2)
        btn_4_raise_mod.grid(row=1, column=2)

        # Number to roll
        lbl_100_num = ttk.Label(master=frame_d100, text="Num", font=self.font_small)
        lbl_100_num.grid(row=2, column=0, columnspan=3)
        btn_100_lower_num = ttk.Button(master=frame_d100, text="-", command=lambda: self.modify_num(die='100', dir='-'), width=2)
        btn_100_lower_num.grid(row=3, column=0)
        self.ent_100_num = ttk.Entry(master=frame_d100, width=5)
        self.ent_100_num.grid(row=3, column=1)
        self.ent_100_num.insert(0, '0')
        btn_100_raise_num = ttk.Button(master=frame_d100, text="+", command=lambda: self.modify_num(die='100', dir='+'), width=2)
        btn_100_raise_num.grid(row=3, column=2)

        lbl_20_num = ttk.Label(master=frame_d20, text="Num", font=self.font_small)
        lbl_20_num.grid(row=2, column=0, columnspan=3)
        btn_20_lower_num = ttk.Button(master=frame_d20, text="-", command=lambda: self.modify_num(die='20', dir='-'), width=2)
        btn_20_lower_num.grid(row=3, column=0)
        self.ent_20_num = ttk.Entry(master=frame_d20, width=5)
        self.ent_20_num.grid(row=3, column=1)
        self.ent_20_num.insert(0, '0')
        btn_20_raise_num = ttk.Button(master=frame_d20, text="+", command=lambda: self.modify_num(die='20', dir='+'), width=2)
        btn_20_raise_num.grid(row=3, column=2)

        lbl_12_num = ttk.Label(master=frame_d12, text="Num", font=self.font_small)
        lbl_12_num.grid(row=2, column=0, columnspan=3)
        btn_12_lower_num = ttk.Button(master=frame_d12, text="-", command=lambda: self.modify_num(die='12', dir='-'), width=2)
        btn_12_lower_num.grid(row=3, column=0)
        self.ent_12_num = ttk.Entry(master=frame_d12, width=5)
        self.ent_12_num.grid(row=3, column=1)
        self.ent_12_num.insert(0, '0')
        btn_12_raise_num = ttk.Button(master=frame_d12, text="+", command=lambda: self.modify_num(die='12', dir='+'), width=2)
        btn_12_raise_num.grid(row=3, column=2)

        lbl_10_num = ttk.Label(master=frame_d10, text="Num", font=self.font_small)
        lbl_10_num.grid(row=2, column=0, columnspan=3)
        btn_10_lower_num = ttk.Button(master=frame_d10, text="-", command=lambda: self.modify_num(die='10', dir='-'), width=2)
        btn_10_lower_num.grid(row=3, column=0)
        self.ent_10_num = ttk.Entry(master=frame_d10, width=5)
        self.ent_10_num.grid(row=3, column=1)
        self.ent_10_num.insert(0, '0')
        btn_10_raise_num = ttk.Button(master=frame_d10, text="+", command=lambda: self.modify_num(die='10', dir='+'), width=2)
        btn_10_raise_num.grid(row=3, column=2)

        lbl_8_num = ttk.Label(master=frame_d8, text="Num", font=self.font_small)
        lbl_8_num.grid(row=2, column=0, columnspan=3)
        btn_8_lower_num = ttk.Button(master=frame_d8, text="-", command=lambda: self.modify_num(die='8', dir='-'), width=2)
        btn_8_lower_num.grid(row=3, column=0)
        self.ent_8_num = ttk.Entry(master=frame_d8, width=5)
        self.ent_8_num.grid(row=3, column=1)
        self.ent_8_num.insert(0, '0')
        btn_8_raise_num = ttk.Button(master=frame_d8, text="+", command=lambda: self.modify_num(die='8', dir='+'), width=2)
        btn_8_raise_num.grid(row=3, column=2)

        lbl_6_num = ttk.Label(master=frame_d6, text="Num", font=self.font_small)
        lbl_6_num.grid(row=2, column=0, columnspan=3)
        btn_6_lower_num = ttk.Button(master=frame_d6, text="-", command=lambda: self.modify_num(die='6', dir='-'), width=2)
        btn_6_lower_num.grid(row=3, column=0)
        self.ent_6_num = ttk.Entry(master=frame_d6, width=5)
        self.ent_6_num.grid(row=3, column=1)
        self.ent_6_num.insert(0, '0')
        btn_6_raise_num = ttk.Button(master=frame_d6, text="+", command=lambda: self.modify_num(die='6', dir='+'), width=2)
        btn_6_raise_num.grid(row=3, column=2)

        lbl_4_num = ttk.Label(master=frame_d4, text="Num", font=self.font_small)
        lbl_4_num.grid(row=2, column=0, columnspan=3)
        btn_4_lower_num = ttk.Button(master=frame_d4, text="-", command=lambda: self.modify_num(die='4', dir='-'), width=2)
        btn_4_lower_num.grid(row=3, column=0)
        self.ent_4_num = ttk.Entry(master=frame_d4, width=5)
        self.ent_4_num.grid(row=3, column=1)
        self.ent_4_num.insert(0, '0')
        btn_4_raise_num = ttk.Button(master=frame_d4, text="+", command=lambda: self.modify_num(die='4', dir='+'), width=2)
        btn_4_raise_num.grid(row=3, column=2)

        # Radio-button modifiers
        self.vuln_res_100 = tk.StringVar()
        self.vuln_res_20 = tk.StringVar()
        self.vuln_res_12 = tk.StringVar()
        self.vuln_res_10 = tk.StringVar()
        self.vuln_res_8 = tk.StringVar()
        self.vuln_res_6 = tk.StringVar()
        self.vuln_res_4 = tk.StringVar()

        rbn_frame_100 = ttk.Frame(master=frame_d100)
        rbn_frame_100.grid(row=4, column=0, columnspan=3)
        rbn_frame_20 = ttk.Frame(master=frame_d20)
        rbn_frame_20.grid(row=4, column=0, columnspan=3)
        rbn_frame_12 = ttk.Frame(master=frame_d12)
        rbn_frame_12.grid(row=4, column=0, columnspan=3)
        rbn_frame_10 = ttk.Frame(master=frame_d10)
        rbn_frame_10.grid(row=4, column=0, columnspan=3)
        rbn_frame_8 = ttk.Frame(master=frame_d8)
        rbn_frame_8.grid(row=4, column=0, columnspan=3)
        rbn_frame_6 = ttk.Frame(master=frame_d6)
        rbn_frame_6.grid(row=4, column=0, columnspan=3)
        rbn_frame_4 = ttk.Frame(master=frame_d4)
        rbn_frame_4.grid(row=4, column=0, columnspan=3)

        self.rbn_vuln_100 = ttk.Radiobutton(master=rbn_frame_100, text="Vuln", variable=self.vuln_res_100, value="v")
        self.rbn_vuln_100.grid(row=0, column=0)
        self.rbn_norm_100 = ttk.Radiobutton(master=rbn_frame_100, text="Norm", variable=self.vuln_res_100, value="n")
        self.rbn_norm_100.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_100 = ttk.Radiobutton(master=rbn_frame_100, text="Rsst", variable=self.vuln_res_100, value="r")
        self.rbn_rsst_100.grid(row=0, column=1)
        self.rbn_norm_100.state(['selected'])

        self.rbn_vuln_20 = ttk.Radiobutton(master=rbn_frame_20, text="Vuln", variable=self.vuln_res_20, value="v")
        self.rbn_vuln_20.grid(row=0, column=0)
        self.rbn_norm_20 = ttk.Radiobutton(master=rbn_frame_20, text="Norm", variable=self.vuln_res_20, value="n")
        self.rbn_norm_20.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_20 = ttk.Radiobutton(master=rbn_frame_20, text="Rsst", variable=self.vuln_res_20, value="r")
        self.rbn_rsst_20.grid(row=0, column=1)
        self.rbn_norm_20.state(['selected'])

        self.rbn_vuln_12 = ttk.Radiobutton(master=rbn_frame_12, text="Vuln", variable=self.vuln_res_12, value="v")
        self.rbn_vuln_12.grid(row=0, column=0)
        self.rbn_norm_12 = ttk.Radiobutton(master=rbn_frame_12, text="Norm", variable=self.vuln_res_12, value="n")
        self.rbn_norm_12.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_12 = ttk.Radiobutton(master=rbn_frame_12, text="Rsst", variable=self.vuln_res_12, value="r")
        self.rbn_rsst_12.grid(row=0, column=1)
        self.rbn_norm_12.state(['selected'])

        self.rbn_vuln_10 = ttk.Radiobutton(master=rbn_frame_10, text="Vuln", variable=self.vuln_res_10, value="v")
        self.rbn_vuln_10.grid(row=0, column=0)
        self.rbn_norm_10 = ttk.Radiobutton(master=rbn_frame_10, text="Norm", variable=self.vuln_res_10, value="n")
        self.rbn_norm_10.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_10 = ttk.Radiobutton(master=rbn_frame_10, text="Rsst", variable=self.vuln_res_10, value="r")
        self.rbn_rsst_10.grid(row=0, column=1)
        self.rbn_norm_10.state(['selected'])

        self.rbn_vuln_8 = ttk.Radiobutton(master=rbn_frame_8, text="Vuln", variable=self.vuln_res_8, value="v")
        self.rbn_vuln_8.grid(row=0, column=0)
        self.rbn_norm_8 = ttk.Radiobutton(master=rbn_frame_8, text="Norm", variable=self.vuln_res_8, value="n")
        self.rbn_norm_8.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_8 = ttk.Radiobutton(master=rbn_frame_8, text="Rsst", variable=self.vuln_res_8, value="r")
        self.rbn_rsst_8.grid(row=0, column=1)
        self.rbn_norm_8.state(['selected'])

        self.rbn_vuln_6 = ttk.Radiobutton(master=rbn_frame_6, text="Vuln", variable=self.vuln_res_6, value="v")
        self.rbn_vuln_6.grid(row=0, column=0)
        self.rbn_norm_6 = ttk.Radiobutton(master=rbn_frame_6, text="Norm", variable=self.vuln_res_6, value="n")
        self.rbn_norm_6.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_6 = ttk.Radiobutton(master=rbn_frame_6, text="Rsst", variable=self.vuln_res_6, value="r")
        self.rbn_rsst_6.grid(row=0, column=1)
        self.rbn_norm_6.state(['selected'])

        self.rbn_vuln_4 = ttk.Radiobutton(master=rbn_frame_4, text="Vuln", variable=self.vuln_res_4, value="v")
        self.rbn_vuln_4.grid(row=0, column=0)
        self.rbn_norm_4 = ttk.Radiobutton(master=rbn_frame_4, text="Norm", variable=self.vuln_res_4, value="n")
        self.rbn_norm_4.grid(row=1, column=0, columnspan=2)
        self.rbn_rsst_4 = ttk.Radiobutton(master=rbn_frame_4, text="Rsst", variable=self.vuln_res_4, value="r")
        self.rbn_rsst_4.grid(row=0, column=1)
        self.rbn_norm_4.state(['selected'])

        # Roll buttons
        btn_100_roll = ttk.Button(master=frame_d100, text="Roll", command=lambda: self.roll_win_btn('100'))
        btn_100_roll.grid(row=5, column=0, columnspan=3, pady=10)
        btn_20_roll = ttk.Button(master=frame_d20, text="Roll", command=lambda: self.roll_win_btn('20'))
        btn_20_roll.grid(row=5, column=0, columnspan=3, pady=10)
        btn_12_roll = ttk.Button(master=frame_d12, text="Roll", command=lambda: self.roll_win_btn('12'))
        btn_12_roll.grid(row=5, column=0, columnspan=3, pady=10)
        btn_10_roll = ttk.Button(master=frame_d10, text="Roll", command=lambda: self.roll_win_btn('10'))
        btn_10_roll.grid(row=5, column=0, columnspan=3, pady=10)
        btn_8_roll = ttk.Button(master=frame_d8, text="Roll", command=lambda: self.roll_win_btn('8'))
        btn_8_roll.grid(row=5, column=0, columnspan=3, pady=10)
        btn_6_roll = ttk.Button(master=frame_d6, text="Roll", command=lambda: self.roll_win_btn('6'))
        btn_6_roll.grid(row=5, column=0, columnspan=3, pady=10)
        btn_4_roll = ttk.Button(master=frame_d4, text="Roll", command=lambda: self.roll_win_btn('4'))
        btn_4_roll.grid(row=5, column=0, columnspan=3, pady=10)
        #btn_coin_roll = ttk.Button(master=frame_coin, text="Roll", command=lambda: self.roll_win_btn('coin'))
        #btn_coin_roll.grid(row=5, column=0, columnspan=3, pady=10)

        self.btn_100_roll_again = ttk.Button(master=frame_d100, text="Add Roll", command=lambda: self.roll_win_btn('100', True))
        self.btn_20_roll_again = ttk.Button(master=frame_d20, text="Add Roll", command=lambda: self.roll_win_btn('20', True))
        self.btn_12_roll_again = ttk.Button(master=frame_d12, text="Add Roll", command=lambda: self.roll_win_btn('12', True))
        self.btn_10_roll_again = ttk.Button(master=frame_d10, text="Add Roll", command=lambda: self.roll_win_btn('10', True))
        self.btn_8_roll_again = ttk.Button(master=frame_d8, text="Add Roll", command=lambda: self.roll_win_btn('8', True))
        self.btn_6_roll_again = ttk.Button(master=frame_d6, text="Add Roll", command=lambda: self.roll_win_btn('6', True))
        self.btn_4_roll_again = ttk.Button(master=frame_d4, text="Add Roll", command=lambda: self.roll_win_btn('4', True))
        self.btn_100_roll_again.grid(row=6, column=0, columnspan=3)
        self.btn_20_roll_again.grid(row=6, column=0, columnspan=3)
        self.btn_12_roll_again.grid(row=6, column=0, columnspan=3)
        self.btn_10_roll_again.grid(row=6, column=0, columnspan=3)
        self.btn_8_roll_again.grid(row=6, column=0, columnspan=3)
        self.btn_6_roll_again.grid(row=6, column=0, columnspan=3)
        self.btn_4_roll_again.grid(row=6, column=0, columnspan=3)

        self.d100s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')
        self.d20s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')
        self.d12s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')
        self.d10s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')
        self.d8s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')
        self.d6s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')
        self.d4s_rolled = ttk.Label(master=dice_selection_frame, text="", font=self.font_small, anchor='center')

        # Results
        frame_res_1 = ttk.Frame(master=frame_d100)
        frame_res_1.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_1.columnconfigure([0,1], weight=1)
        frame_res_2 = ttk.Frame(master=frame_d20)
        frame_res_2.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_2.columnconfigure([0,1], weight=1)
        frame_res_3 = ttk.Frame(master=frame_d12)
        frame_res_3.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_3.columnconfigure([0,1], weight=1)
        frame_res_4 = ttk.Frame(master=frame_d10)
        frame_res_4.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_4.columnconfigure([0,1], weight=1)
        frame_res_5 = ttk.Frame(master=frame_d8)
        frame_res_5.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_5.columnconfigure([0,1], weight=1)
        frame_res_6 = ttk.Frame(master=frame_d6)
        frame_res_6.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_6.columnconfigure([0,1], weight=1)
        frame_res_7 = ttk.Frame(master=frame_d4)
        frame_res_7.grid(row=7, column=0, columnspan=3, pady=10)
        frame_res_7.columnconfigure([0,1], weight=1)
        #frame_res_8 = ttk.Frame(master=frame_coin)
        #frame_res_8.grid(row=7, column=0, columnspan=3, pady=10)
        #frame_res_8.columnconfigure([0,1], weight=1)

        lbl_100_marker = ttk.Label(master=frame_res_1, text="Roll: ", font=self.font)
        lbl_100_marker.grid(row=0, column=0, sticky='w')
        self.lbl_100_result = ttk.Label(master=frame_res_1, text="0", font=self.font, width=3, anchor='center')
        self.lbl_100_result.grid(row=0, column=1, sticky='e')
        lbl_100_offset_mark = ttk.Label(master=frame_res_1, text="Mod: ", font=self.font)
        lbl_100_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_100_offset = ttk.Label(master=frame_res_1, text="0", font=self.font, width=3, anchor='center')
        self.lbl_100_offset.grid(row=1, column=1, sticky='e')
        lbl_100_total_mark = ttk.Label(master=frame_res_1, text="Total: ", font=self.font)
        lbl_100_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_100_total = ttk.Label(master=frame_res_1, text="0", font=self.font, width=3, anchor='center')
        self.lbl_100_total.grid(row=2, column=1, sticky='e')

        lbl_20_marker = ttk.Label(master=frame_res_2, text="Roll: ", font=self.font)
        lbl_20_marker.grid(row=0, column=0, sticky='w')
        self.lbl_20_result = ttk.Label(master=frame_res_2, text="0", font=self.font, width=3, anchor='center')
        self.lbl_20_result.grid(row=0, column=1, sticky='e')
        lbl_20_offset_mark = ttk.Label(master=frame_res_2, text="Mod: ", font=self.font)
        lbl_20_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_20_offset = ttk.Label(master=frame_res_2, text="0", font=self.font, width=3, anchor='center')
        self.lbl_20_offset.grid(row=1, column=1, sticky='e')
        lbl_20_total_mark = ttk.Label(master=frame_res_2, text="Total: ", font=self.font)
        lbl_20_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_20_total = ttk.Label(master=frame_res_2, text="0", font=self.font, width=3, anchor='center')
        self.lbl_20_total.grid(row=2, column=1, sticky='e')

        lbl_12_marker = ttk.Label(master=frame_res_3, text="Roll: ", font=self.font)
        lbl_12_marker.grid(row=0, column=0, sticky='w')
        self.lbl_12_result = ttk.Label(master=frame_res_3, text="0", font=self.font, width=3, anchor='center')
        self.lbl_12_result.grid(row=0, column=1, sticky='e')
        lbl_12_offset_mark = ttk.Label(master=frame_res_3, text="Mod: ", font=self.font)
        lbl_12_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_12_offset = ttk.Label(master=frame_res_3, text="0", font=self.font, width=3, anchor='center')
        self.lbl_12_offset.grid(row=1, column=1, sticky='e')
        lbl_12_total_mark = ttk.Label(master=frame_res_3, text="Total: ", font=self.font)
        lbl_12_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_12_total = ttk.Label(master=frame_res_3, text="0", font=self.font, width=3, anchor='center')
        self.lbl_12_total.grid(row=2, column=1, sticky='e')

        lbl_10_marker = ttk.Label(master=frame_res_4, text="Roll: ", font=self.font)
        lbl_10_marker.grid(row=0, column=0, sticky='w')
        self.lbl_10_result = ttk.Label(master=frame_res_4, text="0", font=self.font, width=3, anchor='center')
        self.lbl_10_result.grid(row=0, column=1, sticky='e')
        lbl_10_offset_mark = ttk.Label(master=frame_res_4, text="Mod: ", font=self.font)
        lbl_10_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_10_offset = ttk.Label(master=frame_res_4, text="0", font=self.font, width=3, anchor='center')
        self.lbl_10_offset.grid(row=1, column=1, sticky='e')
        lbl_10_total_mark = ttk.Label(master=frame_res_4, text="Total: ", font=self.font)
        lbl_10_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_10_total = ttk.Label(master=frame_res_4, text="0", font=self.font, width=3, anchor='center')
        self.lbl_10_total.grid(row=2, column=1, sticky='e')

        lbl_8_marker = ttk.Label(master=frame_res_5, text="Roll: ", font=self.font)
        lbl_8_marker.grid(row=0, column=0, sticky='w')
        self.lbl_8_result = ttk.Label(master=frame_res_5, text="0", font=self.font, width=3, anchor='center')
        self.lbl_8_result.grid(row=0, column=1, sticky='e')
        lbl_8_offset_mark = ttk.Label(master=frame_res_5, text="Mod: ", font=self.font)
        lbl_8_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_8_offset = ttk.Label(master=frame_res_5, text="0", font=self.font, width=3, anchor='center')
        self.lbl_8_offset.grid(row=1, column=1, sticky='e')
        lbl_8_total_mark = ttk.Label(master=frame_res_5, text="Total: ", font=self.font)
        lbl_8_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_8_total = ttk.Label(master=frame_res_5, text="0", font=self.font, width=3, anchor='center')
        self.lbl_8_total.grid(row=2, column=1, sticky='e')

        lbl_6_marker = ttk.Label(master=frame_res_6, text="Roll: ", font=self.font)
        lbl_6_marker.grid(row=0, column=0, sticky='w')
        self.lbl_6_result = ttk.Label(master=frame_res_6, text="0", font=self.font, width=3, anchor='center')
        self.lbl_6_result.grid(row=0, column=1, sticky='e')
        lbl_6_offset_mark = ttk.Label(master=frame_res_6, text="Mod: ", font=self.font)
        lbl_6_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_6_offset = ttk.Label(master=frame_res_6, text="0", font=self.font, width=3, anchor='center')
        self.lbl_6_offset.grid(row=1, column=1, sticky='e')
        lbl_6_total_mark = ttk.Label(master=frame_res_6, text="Total: ", font=self.font)
        lbl_6_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_6_total = ttk.Label(master=frame_res_6, text="0", font=self.font, width=3, anchor='center')
        self.lbl_6_total.grid(row=2, column=1, sticky='e')

        lbl_4_marker = ttk.Label(master=frame_res_7, text="Roll: ", font=self.font)
        lbl_4_marker.grid(row=0, column=0, sticky='w')
        self.lbl_4_result = ttk.Label(master=frame_res_7, text="0", font=self.font, width=3, anchor='center')
        self.lbl_4_result.grid(row=0, column=1, sticky='e')
        lbl_4_offset_mark = ttk.Label(master=frame_res_7, text="Mod: ", font=self.font)
        lbl_4_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_4_offset = ttk.Label(master=frame_res_7, text="0", font=self.font, width=3, anchor='center')
        self.lbl_4_offset.grid(row=1, column=1, sticky='e')
        lbl_4_total_mark = ttk.Label(master=frame_res_7, text="Total: ", font=self.font)
        lbl_4_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_4_total = ttk.Label(master=frame_res_7, text="0", font=self.font, width=3, anchor='center')
        self.lbl_4_total.grid(row=2, column=1, sticky='e')

        '''
        lbl_coin_marker = ttk.Label(master=frame_res_8, text="Roll: ", font=self.font)
        lbl_coin_marker.grid(row=0, column=0, sticky='w')
        self.lbl_coin_result = ttk.Label(master=frame_res_8, text="0", font=self.font, width=3, anchor='center')
        self.lbl_coin_result.grid(row=0, column=1, sticky='e')
        lbl_coin_offset_mark = ttk.Label(master=frame_res_8, text="Mod: ", font=self.font)
        lbl_coin_offset_mark.grid(row=1, column=0, sticky='w')
        self.lbl_coin_offset = ttk.Label(master=frame_res_8, text="0", font=self.font, width=3, anchor='center')
        self.lbl_coin_offset.grid(row=1, column=1, sticky='e')
        lbl_coin_total_mark = ttk.Label(master=frame_res_8, text="Total: ", font=self.font)
        lbl_coin_total_mark.grid(row=2, column=0, sticky='w')
        self.lbl_coin_total = ttk.Label(master=frame_res_8, text="0", font=self.font, width=3, anchor='center')
        self.lbl_coin_total.grid(row=2, column=1, sticky='e')
        '''

        lbl_net_marker = ttk.Label(master=result_frame, text="Net Total", font=self.font)
        lbl_net_marker.grid(row=1, column=0, columnspan=7)
        self.lbl_net_total = ttk.Label(master=result_frame, text="0", font=self.font, width=3, anchor='center')
        self.lbl_net_total.grid(row=2, column=0, columnspan=7)
        btn_calc_net = ttk.Button(master=result_frame, text="Calculate Total", command=self.calc_net)
        btn_calc_net.grid(row=3, column=0, columnspan=7, pady=5)
        btn_clear_out = ttk.Button(master=result_frame, text="Clear Board", command=self.clear_out)
        btn_clear_out.grid(row=4, column=0, columnspan=7, pady=5)
        
    def modify_mod(self, die, dir):
        if die == '100':
            try:
                mod_val = int(self.ent_100_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_100_mod.delete(0, tk.END)
                self.ent_100_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_100_mod.delete(0, tk.END)
                self.ent_100_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_100_mod.delete(0, tk.END)
                self.ent_100_mod.insert(0, mod_val)
        elif die == '20':
            try:
                mod_val = int(self.ent_20_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_20_mod.delete(0, tk.END)
                self.ent_20_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_20_mod.delete(0, tk.END)
                self.ent_20_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_20_mod.delete(0, tk.END)
                self.ent_20_mod.insert(0, mod_val)
        elif die == '12':
            try:
                mod_val = int(self.ent_12_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_12_mod.delete(0, tk.END)
                self.ent_12_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_12_mod.delete(0, tk.END)
                self.ent_12_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_12_mod.delete(0, tk.END)
                self.ent_12_mod.insert(0, mod_val)
        elif die == '10':
            try:
                mod_val = int(self.ent_10_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_10_mod.delete(0, tk.END)
                self.ent_10_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_10_mod.delete(0, tk.END)
                self.ent_10_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_10_mod.delete(0, tk.END)
                self.ent_10_mod.insert(0, mod_val)
        elif die == '8':
            try:
                mod_val = int(self.ent_8_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_8_mod.delete(0, tk.END)
                self.ent_8_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_8_mod.delete(0, tk.END)
                self.ent_8_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_8_mod.delete(0, tk.END)
                self.ent_8_mod.insert(0, mod_val)
        elif die == '6':
            try:
                mod_val = int(self.ent_6_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_6_mod.delete(0, tk.END)
                self.ent_6_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_6_mod.delete(0, tk.END)
                self.ent_6_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_6_mod.delete(0, tk.END)
                self.ent_6_mod.insert(0, mod_val)
        elif die == '4':
            try:
                mod_val = int(self.ent_4_mod.get())
            except ValueError:
                mod_val = 0
                self.ent_4_mod.delete(0, tk.END)
                self.ent_4_mod.insert(0, mod_val)
                return
            if dir == '+':
                mod_val += 1
                if mod_val > 100:
                    mod_val = 100
                self.ent_4_mod.delete(0, tk.END)
                self.ent_4_mod.insert(0, mod_val)
            else:
                mod_val -= 1
                if mod_val < -999:
                    mod_val = -999
                self.ent_4_mod.delete(0, tk.END)
                self.ent_4_mod.insert(0, mod_val)
        else:
            messagebox.showerror("Dice Roller", "Fatal error. File may be corrupted.")
            return

    def modify_num(self, die, dir):
        if die == '100':
            try:
                num_val = int(self.ent_100_num.get())
            except ValueError:
                num_val = 0
                self.ent_100_num.delete(0, tk.END)
                self.ent_100_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 10:
                    num_val = 10
                self.ent_100_num.delete(0, tk.END)
                self.ent_100_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_100_num.delete(0, tk.END)
                self.ent_100_num.insert(0, num_val)
        elif die == '20':
            try:
                num_val = int(self.ent_20_num.get())
            except ValueError:
                num_val = 0
                self.ent_20_num.delete(0, tk.END)
                self.ent_20_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 50:
                    num_val = 50
                self.ent_20_num.delete(0, tk.END)
                self.ent_20_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_20_num.delete(0, tk.END)
                self.ent_20_num.insert(0, num_val)
        elif die == '12':
            try:
                num_val = int(self.ent_12_num.get())
            except ValueError:
                num_val = 0
                self.ent_12_num.delete(0, tk.END)
                self.ent_12_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 80:
                    num_val = 80
                self.ent_12_num.delete(0, tk.END)
                self.ent_12_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_12_num.delete(0, tk.END)
                self.ent_12_num.insert(0, num_val)
        elif die == '10':
            try:
                num_val = int(self.ent_10_num.get())
            except ValueError:
                num_val = 0
                self.ent_10_num.delete(0, tk.END)
                self.ent_10_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 100:
                    num_val = 100
                self.ent_10_num.delete(0, tk.END)
                self.ent_10_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_10_num.delete(0, tk.END)
                self.ent_10_num.insert(0, num_val)
        elif die == '8':
            try:
                num_val = int(self.ent_8_num.get())
            except ValueError:
                num_val = 0
                self.ent_8_num.delete(0, tk.END)
                self.ent_8_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 125:
                    num_val = 125
                self.ent_8_num.delete(0, tk.END)
                self.ent_8_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_8_num.delete(0, tk.END)
                self.ent_8_num.insert(0, num_val)
        elif die == '6':
            try:
                num_val = int(self.ent_6_num.get())
            except ValueError:
                num_val = 0
                self.ent_6_num.delete(0, tk.END)
                self.ent_6_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 160:
                    num_val = 160
                self.ent_6_num.delete(0, tk.END)
                self.ent_6_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_6_num.delete(0, tk.END)
                self.ent_6_num.insert(0, num_val)
        elif die == '4':
            try:
                num_val = int(self.ent_4_num.get())
            except ValueError:
                num_val = 0
                self.ent_4_num.delete(0, tk.END)
                self.ent_4_num.insert(0, num_val)
                return
            if dir == '+':
                num_val += 1
                if num_val > 250:
                    num_val = 250
                self.ent_4_num.delete(0, tk.END)
                self.ent_4_num.insert(0, num_val)
            else:
                num_val -= 1
                if num_val < 0:
                    num_val = 0
                self.ent_4_num.delete(0, tk.END)
                self.ent_4_num.insert(0, num_val)
        else:
            messagebox.showerror("Dice Roller", "Fatal error. File may be corrupted.")
            return

    def roll_win_btn(self, die, add_to_roll=False):
        if die == '100':
            try:
                mod_100 = int(self.ent_100_mod.get())
                num_100 = int(self.ent_100_num.get())
                if mod_100 > 100:
                    mod_100 = 100
                    self.ent_100_mod.delete(0, tk.END)
                    self.ent_100_mod.insert(0, mod_100)
                elif mod_100 < -999:
                    mod_100 = -999
                    self.ent_100_mod.delete(0, tk.END)
                    self.ent_100_mod.insert(0, mod_100)
                if num_100 > 10:
                    num_100 = 10
                    self.ent_100_num.delete(0, tk.END)
                    self.ent_100_num.insert(0, num_100)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_100_list = self.roll(die_size=100, num_dice=num_100)
            dice_100_sum = 0
            if add_to_roll:
                dice_100_sum_last = int(self.lbl_100_total.cget('text'))
            else:
                dice_100_sum_last = 0
            roll_values = str(result_100_list[0])
            num_of_loops = 0
            for res in result_100_list:
                dice_100_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_100 > 0:
                self.d100s_rolled.config(text=roll_values)
                self.d100s_rolled.grid(row=3, column=0)
            else:
                self.d100s_rolled.grid_forget()
            mod_100_str = str(mod_100)
            if mod_100 > 0:
                mod_100_str = "+" + mod_100_str
            self.lbl_100_result.config(text=dice_100_sum)
            self.lbl_100_offset.config(text=mod_100_str)
            dice_100_total = dice_100_sum + mod_100 + dice_100_sum_last
            if self.vuln_res_100.get() == 'v':
                dice_100_total = math.floor(dice_100_total * 2)
            elif self.vuln_res_100.get() == 'r':
                dice_100_total = math.floor(dice_100_total / 2)
            self.lbl_100_total.config(text=dice_100_total)
        elif die == '20':
            try:
                mod_20 = int(self.ent_20_mod.get())
                num_20 = int(self.ent_20_num.get())
                if mod_20 > 100:
                    mod_20 = 100
                    self.ent_20_mod.delete(0, tk.END)
                    self.ent_20_mod.insert(0, mod_20)
                elif mod_20 < -999:
                    mod_20 = -999
                    self.ent_20_mod.delete(0, tk.END)
                    self.ent_20_mod.insert(0, mod_20)
                if num_20 > 50:
                    num_20 = 50
                    self.ent_20_num.delete(0, tk.END)
                    self.ent_20_num.insert(0, num_20)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_20_list = self.roll(die_size=20, num_dice=num_20)
            dice_20_sum = 0
            if add_to_roll:
                dice_20_sum_last = int(self.lbl_20_total.cget('text'))
            else:
                dice_20_sum_last = 0
            roll_values = str(result_20_list[0])
            num_of_loops = 0
            for res in result_20_list:
                dice_20_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_20 > 0:
                self.d20s_rolled.config(text=roll_values)
                self.d20s_rolled.grid(row=3, column=1)
            else:
                self.d20s_rolled.grid_forget()
            mod_20_str = str(mod_20)
            if mod_20 > 0:
                mod_20_str = "+" + mod_20_str
            self.lbl_20_result.config(text=dice_20_sum)
            self.lbl_20_offset.config(text=mod_20_str)
            dice_20_total = dice_20_sum + mod_20 + dice_20_sum_last
            if self.vuln_res_20.get() == 'v':
                dice_20_total = math.floor(dice_20_total * 2)
            elif self.vuln_res_20.get() == 'r':
                dice_20_total = math.floor(dice_20_total / 2)
            self.lbl_20_total.config(text=dice_20_total)
        elif die == '12':
            try:
                mod_12 = int(self.ent_12_mod.get())
                num_12 = int(self.ent_12_num.get())
                if mod_12 > 100:
                    mod_12 = 100
                    self.ent_12_mod.delete(0, tk.END)
                    self.ent_12_mod.insert(0, mod_12)
                elif mod_12 < -999:
                    mod_12 = -999
                    self.ent_12_mod.delete(0, tk.END)
                    self.ent_12_mod.insert(0, mod_12)
                if num_12 > 80:
                    num_12 = 80
                    self.ent_12_num.delete(0, tk.END)
                    self.ent_12_num.insert(0, num_12)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_12_list = self.roll(die_size=12, num_dice=num_12)
            dice_12_sum = 0
            if add_to_roll:
                dice_12_sum_last = int(self.lbl_12_total.cget('text'))
            else:
                dice_12_sum_last = 0
            roll_values = str(result_12_list[0])
            num_of_loops = 0
            for res in result_12_list:
                dice_12_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_12 > 0:
                self.d12s_rolled.config(text=roll_values)
                self.d12s_rolled.grid(row=3, column=2)
            else:
                self.d12s_rolled.grid_forget()
            mod_12_str = str(mod_12)
            if mod_12 > 0:
                mod_12_str = "+" + mod_12_str
            self.lbl_12_result.config(text=dice_12_sum)
            self.lbl_12_offset.config(text=mod_12_str)
            dice_12_total = dice_12_sum + mod_12 + dice_12_sum_last
            if self.vuln_res_12.get() == 'v':
                dice_12_total = math.floor(dice_12_total * 2)
            elif self.vuln_res_12.get() == 'r':
                dice_12_total = math.floor(dice_12_total / 2)
            self.lbl_12_total.config(text=dice_12_total)
        elif die == '10':
            try:
                mod_10 = int(self.ent_10_mod.get())
                num_10 = int(self.ent_10_num.get())
                if mod_10 > 100:
                    mod_10 = 100
                    self.ent_10_mod.delete(0, tk.END)
                    self.ent_10_mod.insert(0, mod_10)
                elif mod_10 < -999:
                    mod_10 = -999
                    self.ent_10_mod.delete(0, tk.END)
                    self.ent_10_mod.insert(0, mod_10)
                if num_10 > 100:
                    num_10 = 100
                    self.ent_10_num.delete(0, tk.END)
                    self.ent_10_num.insert(0, num_10)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_10_list = self.roll(die_size=10, num_dice=num_10)
            dice_10_sum = 0
            if add_to_roll:
                dice_10_sum_last = int(self.lbl_10_total.cget('text'))
            else:
                dice_10_sum_last = 0
            roll_values = str(result_10_list[0])
            num_of_loops = 0
            for res in result_10_list:
                dice_10_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_10 > 0:
                self.d10s_rolled.config(text=roll_values)
                self.d10s_rolled.grid(row=3, column=3)
            else:
                self.d10s_rolled.grid_forget()
            mod_10_str = str(mod_10)
            if mod_10 > 0:
                mod_10_str = "+" + mod_10_str
            self.lbl_10_result.config(text=dice_10_sum)
            self.lbl_10_offset.config(text=mod_10_str)
            dice_10_total = dice_10_sum + mod_10 + dice_10_sum_last
            if self.vuln_res_10.get() == 'v':
                dice_10_total = math.floor(dice_10_total * 2)
            elif self.vuln_res_10.get() == 'r':
                dice_10_total = math.floor(dice_10_total / 2)
            self.lbl_10_total.config(text=dice_10_total)
        elif die == '8':
            try:
                mod_8 = int(self.ent_8_mod.get())
                num_8 = int(self.ent_8_num.get())
                if mod_8 > 100:
                    mod_8 = 100
                    self.ent_8_mod.delete(0, tk.END)
                    self.ent_8_mod.insert(0, mod_8)
                elif mod_8 < -999:
                    mod_8 = -999
                    self.ent_8_mod.delete(0, tk.END)
                    self.ent_8_mod.insert(0, mod_8)
                if num_8 > 125:
                    num_8 = 125
                    self.ent_8_num.delete(0, tk.END)
                    self.ent_8_num.insert(0, num_8)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_8_list = self.roll(die_size=8, num_dice=num_8)
            dice_8_sum = 0
            if add_to_roll:
                dice_8_sum_last = int(self.lbl_8_total.cget('text'))
            else:
                dice_8_sum_last = 0
            roll_values = str(result_8_list[0])
            num_of_loops = 0
            for res in result_8_list:
                dice_8_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_8 > 0:
                self.d8s_rolled.config(text=roll_values)
                self.d8s_rolled.grid(row=3, column=4)
            else:
                self.d8s_rolled.grid_forget()
            mod_8_str = str(mod_8)
            if mod_8 > 0:
                mod_8_str = "+" + mod_8_str
            self.lbl_8_result.config(text=dice_8_sum)
            self.lbl_8_offset.config(text=mod_8_str)
            dice_8_total = dice_8_sum + mod_8 + dice_8_sum_last
            if self.vuln_res_8.get() == 'v':
                dice_8_total = math.floor(dice_8_total * 2)
            elif self.vuln_res_8.get() == 'r':
                dice_8_total = math.floor(dice_8_total / 2)
            self.lbl_8_total.config(text=dice_8_total)
        elif die == '6':
            try:
                mod_6 = int(self.ent_6_mod.get())
                num_6 = int(self.ent_6_num.get())
                if mod_6 > 100:
                    mod_6 = 100
                    self.ent_6_mod.delete(0, tk.END)
                    self.ent_6_mod.insert(0, mod_6)
                elif mod_6 < -999:
                    mod_6 = -999
                    self.ent_6_mod.delete(0, tk.END)
                    self.ent_6_mod.insert(0, mod_6)
                if num_6 > 160:
                    num_6 = 160
                    self.ent_6_num.delete(0, tk.END)
                    self.ent_6_num.insert(0, num_6)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_6_list = self.roll(die_size=6, num_dice=num_6)
            dice_6_sum = 0
            if add_to_roll:
                dice_6_sum_last = int(self.lbl_6_total.cget('text'))
            else:
                dice_6_sum_last = 0
            roll_values = str(result_6_list[0])
            num_of_loops = 0
            for res in result_6_list:
                dice_6_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_6 > 0:
                self.d6s_rolled.config(text=roll_values)
                self.d6s_rolled.grid(row=3, column=5)
            else:
                self.d6s_rolled.grid_forget()
            mod_6_str = str(mod_6)
            if mod_6 > 0:
                mod_6_str = "+" + mod_6_str
            self.lbl_6_result.config(text=dice_6_sum)
            self.lbl_6_offset.config(text=mod_6_str)
            dice_6_total = dice_6_sum + mod_6 + dice_6_sum_last
            if self.vuln_res_6.get() == 'v':
                dice_6_total = math.floor(dice_6_total * 2)
            elif self.vuln_res_6.get() == 'r':
                dice_6_total = math.floor(dice_6_total / 2)
            self.lbl_6_total.config(text=dice_6_total)
        elif die == '4':
            try:
                mod_4 = int(self.ent_4_mod.get())
                num_4 = int(self.ent_4_num.get())
                if mod_4 > 100:
                    mod_4 = 100
                    self.ent_4_mod.delete(0, tk.END)
                    self.ent_4_mod.insert(0, mod_4)
                elif mod_4 < -999:
                    mod_4 = -999
                    self.ent_4_mod.delete(0, tk.END)
                    self.ent_4_mod.insert(0, mod_4)
                if num_4 > 250:
                    num_4 = 250
                    self.ent_4_num.delete(0, tk.END)
                    self.ent_4_num.insert(0, num_4)
            except ValueError:
                messagebox.showwarning("Dice Roller", "Mod and Num values must be whole numbers.")
                return
            result_4_list = self.roll(die_size=4, num_dice=num_4)
            dice_4_sum = 0
            if add_to_roll:
                dice_4_sum_last = int(self.lbl_4_total.cget('text'))
            else:
                dice_4_sum_last = 0
            roll_values = str(result_4_list[0])
            num_of_loops = 0
            for res in result_4_list:
                dice_4_sum += res
                if num_of_loops > 0:
                    roll_values = roll_values + f", {res}"
                if (num_of_loops + 1) % 4 == 0:
                    roll_values += "\n"
                num_of_loops += 1
            if num_4 > 0:
                self.d4s_rolled.config(text=roll_values)
                self.d4s_rolled.grid(row=3, column=6)
            else:
                self.d4s_rolled.grid_forget()
            mod_4_str = str(mod_4)
            if mod_4 > 0:
                mod_4_str = "+" + mod_4_str
            self.lbl_4_result.config(text=dice_4_sum)
            self.lbl_4_offset.config(text=mod_4_str)
            dice_4_total = dice_4_sum + mod_4 + dice_4_sum_last
            if self.vuln_res_4.get() == 'v':
                dice_4_total = math.floor(dice_4_total * 2)
            elif self.vuln_res_4.get() == 'r':
                dice_4_total = math.floor(dice_4_total / 2)
            self.lbl_4_total.config(text=dice_4_total)
        else:
            messagebox.showerror("Dice Roller", "Fatal error. File may be corrupted.")
            return

    def calc_net(self):
        try:
            total_100 = int(self.lbl_100_total.cget("text"))
            total_20 = int(self.lbl_20_total.cget("text"))
            total_12 = int(self.lbl_12_total.cget("text"))
            total_10 = int(self.lbl_10_total.cget("text"))
            total_8 = int(self.lbl_8_total.cget("text"))
            total_6 = int(self.lbl_6_total.cget("text"))
            total_4 = int(self.lbl_4_total.cget("text"))
        except ValueError:
            messagebox.showwarning("Dice Roller", "Dice totals must be whole numbers.")
            return
        net_total = total_100 + total_20 + total_12 + total_10 + total_8 + total_6 + total_4
        self.lbl_net_total.config(text=net_total)

    def clear_out(self):
        self.ent_100_mod.delete(0, tk.END)
        self.ent_100_mod.insert(0, "0")
        self.ent_100_num.delete(0, tk.END)
        self.ent_100_num.insert(0, "0")
        self.ent_20_mod.delete(0, tk.END)
        self.ent_20_mod.insert(0, "0")
        self.ent_20_num.delete(0, tk.END)
        self.ent_20_num.insert(0, "0")
        self.ent_12_mod.delete(0, tk.END)
        self.ent_12_mod.insert(0, "0")
        self.ent_12_num.delete(0, tk.END)
        self.ent_12_num.insert(0, "0")
        self.ent_10_mod.delete(0, tk.END)
        self.ent_10_mod.insert(0, "0")
        self.ent_10_num.delete(0, tk.END)
        self.ent_10_num.insert(0, "0")
        self.ent_8_mod.delete(0, tk.END)
        self.ent_8_mod.insert(0, "0")
        self.ent_8_num.delete(0, tk.END)
        self.ent_8_num.insert(0, "0")
        self.ent_6_mod.delete(0, tk.END)
        self.ent_6_mod.insert(0, "0")
        self.ent_6_num.delete(0, tk.END)
        self.ent_6_num.insert(0, "0")
        self.ent_4_mod.delete(0, tk.END)
        self.ent_4_mod.insert(0, "0")
        self.ent_4_num.delete(0, tk.END)
        self.ent_4_num.insert(0, "0")

        self.d100s_rolled.config(text="")
        self.d20s_rolled.config(text="")
        self.d12s_rolled.config(text="")
        self.d10s_rolled.config(text="")
        self.d8s_rolled.config(text="")
        self.d6s_rolled.config(text="")
        self.d4s_rolled.config(text="")

        if self.d100s_rolled.winfo_ismapped():
            self.d100s_rolled.grid_forget()
        if self.d20s_rolled.winfo_ismapped():
            self.d20s_rolled.grid_forget()
        if self.d12s_rolled.winfo_ismapped():
            self.d12s_rolled.grid_forget()
        if self.d10s_rolled.winfo_ismapped():
            self.d10s_rolled.grid_forget()
        if self.d8s_rolled.winfo_ismapped():
            self.d8s_rolled.grid_forget()
        if self.d6s_rolled.winfo_ismapped():
            self.d6s_rolled.grid_forget()
        if self.d4s_rolled.winfo_ismapped():
            self.d4s_rolled.grid_forget()

        '''
        if self.btn_100_roll_again.winfo_ismapped():
            self.btn_100_roll_again.grid_forget()
        if self.btn_20_roll_again.winfo_ismapped():
            self.btn_20_roll_again.grid_forget()
        if self.btn_12_roll_again.winfo_ismapped():
            self.btn_12_roll_again.grid_forget()
        if self.btn_10_roll_again.winfo_ismapped():
            self.btn_10_roll_again.grid_forget()
        if self.btn_8_roll_again.winfo_ismapped():
            self.btn_8_roll_again.grid_forget()
        if self.btn_6_roll_again.winfo_ismapped():
            self.btn_6_roll_again.grid_forget()
        if self.btn_4_roll_again.winfo_ismapped():
            self.btn_4_roll_again.grid_forget()
        '''

        self.lbl_100_total.config(text="0")
        self.lbl_100_offset.config(text="0")
        self.lbl_100_result.config(text="0")
        self.lbl_20_total.config(text="0")
        self.lbl_20_offset.config(text="0")
        self.lbl_20_result.config(text="0")
        self.lbl_12_total.config(text="0")
        self.lbl_12_offset.config(text="0")
        self.lbl_12_result.config(text="0")
        self.lbl_10_total.config(text="0")
        self.lbl_10_offset.config(text="0")
        self.lbl_10_result.config(text="0")
        self.lbl_8_total.config(text="0")
        self.lbl_8_offset.config(text="0")
        self.lbl_8_result.config(text="0")
        self.lbl_6_total.config(text="0")
        self.lbl_6_offset.config(text="0")
        self.lbl_6_result.config(text="0")
        self.lbl_4_total.config(text="0")
        self.lbl_4_offset.config(text="0")
        self.lbl_4_result.config(text="0")
        self.lbl_net_total.config(text="0")

        self.rbn_vuln_100.state(["!selected"])
        self.rbn_rsst_100.state(["!selected"])
        self.rbn_norm_100.state(["selected"])
        self.rbn_vuln_20.state(["!selected"])
        self.rbn_rsst_20.state(["!selected"])
        self.rbn_norm_20.state(["selected"])
        self.rbn_vuln_12.state(["!selected"])
        self.rbn_rsst_12.state(["!selected"])
        self.rbn_norm_12.state(["selected"])
        self.rbn_vuln_10.state(["!selected"])
        self.rbn_rsst_10.state(["!selected"])
        self.rbn_norm_10.state(["selected"])
        self.rbn_vuln_8.state(["!selected"])
        self.rbn_rsst_8.state(["!selected"])
        self.rbn_norm_8.state(["selected"])
        self.rbn_vuln_6.state(["!selected"])
        self.rbn_rsst_6.state(["!selected"])
        self.rbn_norm_6.state(["selected"])
        self.rbn_vuln_4.state(["!selected"])
        self.rbn_rsst_4.state(["!selected"])
        self.rbn_norm_4.state(["selected"])
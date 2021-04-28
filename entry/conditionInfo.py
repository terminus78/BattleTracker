import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedStyle


class InfoClass():
    def __init__(self, root):
        self.root = root

    def explain_conditions(self):
        self.reg_font = ('Papyrus', '12')
        self.big_font = ('Papyrus', '16')
        self.title_font = ('Papyrus', '18')
        self.cond_win = tk.Toplevel(master=self.root)
        self.cond_win.title("Target Creature")
        style = ThemedStyle(self.cond_win)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.cond_win.configure(bg=style.lookup('TLabel', 'background'))
        self.condition_canvas = tk.Canvas(master=self.cond_win, bg='gray28', width=1000)
        self.condition_canvas.pack(side='left', fill='both', expand=True)
        vert_scroll = ttk.Scrollbar(master=self.cond_win, command=self.condition_canvas.yview)
        vert_scroll.pack(side='right', fill='y')
        info_frame = ttk.Frame(master=self.condition_canvas)
        info_frame.pack(side='left', pady=15, padx=15)
        info_frame.bind('<Configure>', lambda e: self.condition_canvas.configure(scrollregion=self.condition_canvas.bbox('all')))
        self.condition_canvas.create_window((0,0), window=info_frame, anchor='nw')
        self.condition_canvas.configure(yscrollcommand=vert_scroll.set)
        self.cond_win.bind('<MouseWheel>', self.on_mouse_wheel)
        info_frame.columnconfigure(2, minsize=50, weight=1)
        lbl_title = ttk.Label(master=info_frame, text="Conditions Explained", font=self.title_font)
        lbl_title.grid(row=0, column=0, columnspan=2, sticky='w')
        lbl_blind = ttk.Label(master=info_frame, text="Blinded", font=self.big_font)
        lbl_blind.grid(row=1, column=1, sticky='w')
        txt_blind_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        #txt_blind_info.insert(tk.INSERT, "\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.")
        txt_blind_info.grid(row=2, column=2, sticky='w')
        lbl_charmed = ttk.Label(master=info_frame, text="Charmed", font=self.big_font)
        lbl_charmed.grid(row=3, column=1, sticky='w')
        txt_charmed_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txt_charmed_info.insert(tk.INSERT, "\u2022 A charmed creature can't Attack the charmer of target the charmer with harmful Abilities or magical Effects.\n\u2022 The charmer has advantage on any ability check to interact socially with the creature.")
        txt_charmed_info.grid(row=4, column=2, sticky='w')
        lbl_deaf = ttk.Label(master=info_frame, text="Deafened", font=self.big_font)
        lbl_deaf.grid(row=5, column=1, sticky='w')
        txt_deaf_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=1,
            width=80
            )
        #txt_deaf_info.insert(tk.INSERT, "\u2022 A deafened creature can't hear and automatically fails any ability check that requires hearing.")
        txt_deaf_info.grid(row=6, column=2, sticky='w')
        lbl_fright = ttk.Label(master=info_frame, text="Frightened", font=self.big_font)
        lbl_fright.grid(row=7, column=1, sticky='w')
        txt_fright_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txt_fright_info.insert(tk.INSERT, "\u2022 A frightened creature has disadvantage on Ability Checks and AttackRools while the source of its fear is within Line of Sight.\n\u2022 The creature can't willingly move closer to the source of its fear.")
        txt_fright_info.grid(row=8, column=2, sticky='w')
        lbl_grappled = ttk.Label(master=info_frame, text="Grappled", font=self.big_font)
        lbl_grappled.grid(row=9, column=1, sticky='w')
        txt_grappled_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txt_grappled_info.insert(tk.INSERT, "\u2022 A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n\u2022 The condition ends if the Grappler is incapacitated (see the condition).\n\u2022 the condition also ends if an Effect removes the grappled creature from the reach of the Grappler or Grappling Effect, such as when a creature is hurled away by the Thunderwave spell.")
        txt_grappled_info.grid(row=10, column=2, sticky='w')
        lbl_incapacitated = ttk.Label(master=info_frame, text="Incapacitated", font=self.big_font)
        lbl_incapacitated.grid(row=11, column=1, sticky='w')
        txt_incapacitated_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=1,
            width=80
            )
        #txt_incapacitated_info.insert(tk.INSERT, "\u2022 An incapacitated creature can't take Actions or Reactions.")
        txt_incapacitated_info.grid(row=12, column=2, sticky='w')
        lbl_invisible = ttk.Label(master=info_frame, text="Invisible", font=self.big_font)
        lbl_invisible.grid(row=13, column=1, sticky='w')
        txt_invisible_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txt_invisible_info.insert(tk.INSERT, "\u2022 An invisible creature is impossible to see without the aid of magic or a Special sense. For the Purpose of Hiding, the creature is heavily obscured. The creature's location can be detected by any noise it makes or any tracks it leaves.\n\u2022 Attack Rolls against the creature have disadvantage, and the creature's Attack Rolls have advantage.")
        txt_invisible_info.grid(row=14, column=2, sticky='w')
        lbl_paralyzed = ttk.Label(master=info_frame, text="Paralyzed", font=self.big_font)
        lbl_paralyzed.grid(row=15, column=1, sticky='w')
        txt_paralyzed_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txt_paralyzed_info.insert(tk.INSERT, "\u2022 A paralyzed creature is incapacitated (see the condition) and can't move or speak.\n\u2022 the creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 Attack Rolls against the creature have advantage.\n\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.")
        txt_paralyzed_info.grid(row=16, column=2, sticky='w')
        lbl_petrified = ttk.Label(master=info_frame, text="Petrified", font=self.big_font)
        lbl_petrified.grid(row=17, column=1, sticky='w')
        txt_petrified_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=9,
            width=80
            )
        #txt_petrified_info.insert(tk.INSERT, "\u2022 A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into a solid inanimate substance (usually stone). Its weight increases by a factor of ten, and it ceases aging.\n\u2022 The creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n\u2022 Attack Rolls against the creature have advantage.\n\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 The creature has Resistance to all damage.\n\u2022 The creature is immune to poison and disease, although a poison or disease already in its system is suspended, not neutralized.")
        txt_petrified_info.grid(row=18, column=2, sticky='w')
        lbl_poisoned = ttk.Label(master=info_frame, text="Poisoned", font=self.big_font)
        lbl_poisoned.grid(row=19, column=1, sticky='w')
        txt_poisoned_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=1,
            width=80
            )
        #txt_poisoned_info.insert(tk.INSERT, "\u2022 A poisoned creature has disadvantage on Attack Rolls and Ability Checks.")
        txt_poisoned_info.grid(row=20, column=2, sticky='w')
        lbl_prone = ttk.Label(master=info_frame, text="Prone", font=self.big_font)
        lbl_prone.grid(row=21, column=1, sticky='w')
        txt_prone_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txt_prone_info.insert(tk.INSERT, "\u2022 A prone creature's only Movement option is to crawl, unless it stands up and thereby ends the condition.\n\u2022 The creature has disadvantage on Attack Rolls.\n\u2022 An Attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the Attack roll has disavantage.")
        txt_prone_info.grid(row=22, column=2, sticky='w')
        lbl_restrained = ttk.Label(master=info_frame, text="Restrained", font=self.big_font)
        lbl_restrained.grid(row=23, column=1, sticky='w')
        txt_restrained_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txt_restrained_info.insert(tk.INSERT, "\u2022 A restrained creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.\n\u2022 The creature has disadvantage on Dexterity Saving Throws.")
        txt_restrained_info.grid(row=24, column=2, sticky='w')
        lbl_stunned = ttk.Label(master=info_frame, text="Stunned", font=self.big_font)
        lbl_stunned.grid(row=25, column=1, sticky='w')
        txt_stunned_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txt_stunned_info.insert(tk.INSERT, "\u2022 A stunned creature is incapacitated (see the condition), can't move, and can speak only falteringly.\n\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 Attack Rolls against the creature have advantage.")
        txt_stunned_info.grid(row=26, column=2, sticky='w')
        lbl_unconscious = ttk.Label(master=info_frame, text="Unconscious", font=self.big_font)
        lbl_unconscious.grid(row=27, column=1, sticky='w')
        txt_unconscious_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=6,
            width=80
            )
        #txt_unconscious_info.insert(tk.INSERT, "\u2022 An unconscious creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n\u2022 The creature drops whatever it's holding and falls prone.\n\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 Attack Rolls against the creature have advantage.\n\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.")
        txt_unconscious_info.grid(row=28, column=2, sticky='w')
        lbl_exhaustion = ttk.Label(master=info_frame, text="Exhaustion", font=self.title_font)
        lbl_exhaustion.grid(row=29, column=0, sticky='w', columnspan=2)
        txt_exhaustion_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=6,
            width=80
            )
        txt_exhaustion_info.grid(row=30, column=2, sticky='w')
        lbl_level_1 = ttk.Label(master=info_frame, text="Level 1", font=self.big_font)
        lbl_level_1.grid(row=31, column=1, sticky='w')
        txt_level_1_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txt_level_1_info.grid(row=32, column=2, sticky='w')
        lbl_level_2 = ttk.Label(master=info_frame, text="Level 2", font=self.big_font)
        lbl_level_2.grid(row=33, column=1, sticky='w')
        txt_level_2_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txt_level_2_info.grid(row=34, column=2, sticky='w')
        lbl_level_3 = ttk.Label(master=info_frame, text="Level 3", font=self.big_font)
        lbl_level_3.grid(row=35, column=1, sticky='w')
        txt_level_3_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txt_level_3_info.grid(row=36, column=2, sticky='w')
        lbl_level_4 = ttk.Label(master=info_frame, text="Level 4", font=self.big_font)
        lbl_level_4.grid(row=37, column=1, sticky='w')
        txt_level_4_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txt_level_4_info.grid(row=38, column=2, sticky='w')
        lbl_level_5 = ttk.Label(master=info_frame, text="Level 5", font=self.big_font)
        lbl_level_5.grid(row=39, column=1, sticky='w')
        txt_level_5_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txt_level_5_info.grid(row=40, column=2, sticky='w')
        lbl_level_6 = ttk.Label(master=info_frame, text="Level 6", font=self.big_font)
        lbl_level_6.grid(row=41, column=1, sticky='w')
        txt_level_6_info = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        txt_level_6_info.grid(row=42, column=2, sticky='w')
        txt_exhaustion_continued = tk.Text(
            master=info_frame,
            font=self.reg_font,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=12,
            width=80
            )
        txt_exhaustion_continued.grid(row=43, column=2, sticky='w')

        font_to_check = tk.font.Font(family='Papyrus', size='12')
        bullet_width = font_to_check.measure("\u2022 ")
        em = font_to_check.measure("m")
        txt_blind_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_charmed_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_deaf_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_fright_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_grappled_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_incapacitated_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_invisible_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_paralyzed_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_petrified_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_poisoned_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_prone_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_restrained_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_stunned_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txt_unconscious_info.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)

        txt_blind_info.insert(tk.END, "\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n", 'bulleted')
        txt_blind_info.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.", 'bulleted')

        txt_charmed_info.insert(tk.END, "\u2022 A charmed creature can't Attack the charmer of target the charmer with harmful Abilities or magical Effects.\n", 'bulleted')
        txt_charmed_info.insert(tk.END, "\u2022 The charmer has advantage on any ability check to interact socially with the creature.", 'bulleted')

        txt_deaf_info.insert(tk.END, "\u2022 A deafened creature can't hear and automatically fails any ability check that requires hearing.", 'bulleted')

        txt_fright_info.insert(tk.END, "\u2022 A frightened creature has disadvantage on Ability Checks and AttackRools while the source of its fear is within Line of Sight.\n.", 'bulleted')
        txt_fright_info.insert(tk.END, "\u2022 The creature can't willingly move closer to the source of its fear.", 'bulleted')

        txt_grappled_info.insert(tk.END, "\u2022 A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n", 'bulleted')
        txt_grappled_info.insert(tk.END, "\u2022 The condition ends if the Grappler is incapacitated (see the condition).\n", 'bulleted')
        txt_grappled_info.insert(tk.END, "\u2022 The condition also ends if an Effect removes the grappled creature from the reach of the Grappler or Grappling Effect, such as when a creature is hurled away by the Thunderwave spell.", 'bulleted')

        txt_incapacitated_info.insert(tk.END, "\u2022 An incapacitated creature can't take Actions or Reactions.", 'bulleted')

        txt_invisible_info.insert(tk.END, "\u2022 An invisible creature is impossible to see without the aid of magic or a Special sense. For the Purpose of Hiding, the creature is heavily obscured. The creature's location can be detected by any noise it makes or any tracks it leaves.\n", 'bulleted')
        txt_invisible_info.insert(tk.END, "\u2022 Attack Rolls against the creature have disadvantage, and the creature's Attack Rolls have advantage.", 'bulleted')

        txt_paralyzed_info.insert(tk.END, "\u2022 A paralyzed creature is incapacitated (see the condition) and can't move or speak.\n", 'bulleted')
        txt_paralyzed_info.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n", 'bulleted')
        txt_paralyzed_info.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.\n", 'bulleted')
        txt_paralyzed_info.insert(tk.END, "\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.", 'bulleted')

        txt_petrified_info.insert(tk.END, "\u2022 A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into a solid inanimate substance (usually stone). Its weight increases by a factor of ten, and it ceases aging.\n", 'bulleted')
        txt_petrified_info.insert(tk.END, "\u2022 The creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n", 'bulleted')
        txt_petrified_info.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.\n", 'bulleted')
        txt_petrified_info.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 The creature has Resistance to all damage.\n", 'bulleted')
        txt_petrified_info.insert(tk.END, "\u2022 The creature has Resistance to all damage.\n", 'bulleted')
        txt_petrified_info.insert(tk.END, "\u2022 The creature is immune to poison and disease, although a poison or disease already in its system is suspended, not neutralized.", 'bulleted')

        txt_poisoned_info.insert(tk.END, "\u2022 A poisoned creature has disadvantage on Attack Rolls and Ability Checks.", 'bulleted')

        txt_prone_info.insert(tk.END, "\u2022 A prone creature's only Movement option is to crawl, unless it stands up and thereby ends the condition.\n", 'bulleted')
        txt_prone_info.insert(tk.END, "\u2022 The creature has disadvantage on Attack Rolls.\n", 'bulleted')
        txt_prone_info.insert(tk.END, "\u2022 An Attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the Attack roll has disavantage.", 'bulleted')

        txt_restrained_info.insert(tk.END, "\u2022 A restrained creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n", 'bulleted')
        txt_restrained_info.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.\n", 'bulleted')
        txt_restrained_info.insert(tk.END, "\u2022 The creature has disadvantage on Dexterity Saving Throws.", 'bulleted')

        txt_stunned_info.insert(tk.END, "\u2022 A stunned creature is incapacitated (see the condition), can't move, and can speak only falteringly.\n.", 'bulleted')
        txt_stunned_info.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n", 'bulleted')
        txt_stunned_info.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.", 'bulleted')

        txt_unconscious_info.insert(tk.END, "\u2022 An unconscious creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n", 'bulleted')
        txt_unconscious_info.insert(tk.END, "\u2022 The creature drops whatever it's holding and falls prone.\n", 'bulleted')
        txt_unconscious_info.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n", 'bulleted')
        txt_unconscious_info.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.\n", 'bulleted')
        txt_unconscious_info.insert(tk.END, "\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.", 'bulleted')

        txt_exhaustion_info.insert(tk.END, "Some Special Abilities and Environmental Hazards, such as starvation and the long-term Effects of freezing or scorching temperatures, can lead to a Special condition call exhaustion. Exhaustion is measured in six levels. An Effect can give a creature one or more levels of exhaustion, as specified in the effect's description.")

        txt_level_1_info.insert(tk.END, "\u2022 Disadvantage on Ability Checks.", 'bulleted')
        txt_level_2_info.insert(tk.END, "\u2022 Speed halved.", 'bulleted')
        txt_level_3_info.insert(tk.END, "\u2022 Disadvantage on Attack Rolls and Saving Throws.", 'bulleted')
        txt_level_4_info.insert(tk.END, "\u2022 Hit point maximum halved.", 'bulleted')
        txt_level_5_info.insert(tk.END, "\u2022 Speed reduced to 0.", 'bulleted')
        txt_level_6_info.insert(tk.END, "\u2022 Death.", 'bulleted')

        txt_exhaustion_continued.insert(tk.END, "If an already exhausted creature suffers another Effect that causes exhaustion, its current level of exhaustion increases by the amount specified in the effect's description.\n\n")
        txt_exhaustion_continued.insert(tk.END, "A creature suffers the Effect of its current level of exhaustion as well as all lower levels. For example, a creature suffering level 2 exhaustion has its speed halved and has disadvantage on Ability Checks.\n\n")
        txt_exhaustion_continued.insert(tk.END, "An Effect that removes exhaustion reduces its level as specified in the effect's description, with all exhaustion Effects Ending if a creature's exhaustion level is reduced below 1.\n\n")
        txt_exhaustion_continued.insert(tk.END, "Finishing a Long Rest reduces a creature's exhaustion level by 1, provided that the creature has also ingested some food and drink.")

        txt_blind_info.configure(state='disabled')
        txt_charmed_info.configure(state='disabled')
        txt_deaf_info.configure(state='disabled')
        txt_fright_info.configure(state='disabled')
        txt_grappled_info.configure(state='disabled')
        txt_incapacitated_info.configure(state='disabled')
        txt_invisible_info.configure(state='disabled')
        txt_paralyzed_info.configure(state='disabled')
        txt_petrified_info.configure(state='disabled')
        txt_poisoned_info.configure(state='disabled')
        txt_prone_info.configure(state='disabled')
        txt_restrained_info.configure(state='disabled')
        txt_stunned_info.configure(state='disabled')
        txt_unconscious_info.configure(state='disabled')
        txt_exhaustion_info.configure(state='disabled')
        txt_level_1_info.configure(state='disabled')
        txt_level_2_info.configure(state='disabled')
        txt_level_3_info.configure(state='disabled')
        txt_level_4_info.configure(state='disabled')
        txt_level_5_info.configure(state='disabled')
        txt_level_6_info.configure(state='disabled')
        txt_exhaustion_continued.configure(state='disabled')

    def on_mouse_wheel(self, event):
        self.condition_canvas.yview_scroll(int(-1 * (event.delta/120)), 'units')
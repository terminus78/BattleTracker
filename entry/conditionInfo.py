import tkinter as tk
from tkinter import ttk, font
from ttkthemes import ThemedStyle


class InfoClass():
    def __init__(self, root):
        self.root = root

    def explainConditions(self):
        self.regFont = ('Papyrus', '12')
        self.bigFont = ('Papyrus', '16')
        self.titleFont = ('Papyrus', '18')
        self.condWin = tk.Toplevel(master=self.root)
        self.condWin.title("Target Creature")
        style = ThemedStyle(self.condWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.condWin.configure(bg=style.lookup('TLabel', 'background'))
        self.conditionCanvas = tk.Canvas(master=self.condWin, bg='gray28', width=1000)
        self.conditionCanvas.pack(side='left', fill='both', expand=True)
        vertScroll = ttk.Scrollbar(master=self.condWin, command=self.conditionCanvas.yview)
        vertScroll.pack(side='right', fill='y')
        infoFrame = ttk.Frame(master=self.conditionCanvas)
        infoFrame.pack(side='left', pady=15, padx=15)
        infoFrame.bind('<Configure>', lambda e: self.conditionCanvas.configure(scrollregion=self.conditionCanvas.bbox('all')))
        self.conditionCanvas.create_window((0,0), window=infoFrame, anchor='nw')
        self.conditionCanvas.configure(yscrollcommand=vertScroll.set)
        self.condWin.bind('<MouseWheel>', self.onMousewheel)
        infoFrame.columnconfigure(2, minsize=50, weight=1)
        lblTitle = ttk.Label(master=infoFrame, text="Conditions Explained", font=self.titleFont)
        lblTitle.grid(row=0, column=0, columnspan=2, sticky='w')
        lblBlind = ttk.Label(master=infoFrame, text="Blinded", font=self.bigFont)
        lblBlind.grid(row=1, column=1, sticky='w')
        txtBlindInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        #txtBlindInfo.insert(tk.INSERT, "\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.")
        txtBlindInfo.grid(row=2, column=2, sticky='w')
        lblCharmed = ttk.Label(master=infoFrame, text="Charmed", font=self.bigFont)
        lblCharmed.grid(row=3, column=1, sticky='w')
        txtCharmedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txtCharmedInfo.insert(tk.INSERT, "\u2022 A charmed creature can't Attack the charmer of target the charmer with harmful Abilities or magical Effects.\n\u2022 The charmer has advantage on any ability check to interact socially with the creature.")
        txtCharmedInfo.grid(row=4, column=2, sticky='w')
        lblDeaf = ttk.Label(master=infoFrame, text="Deafened", font=self.bigFont)
        lblDeaf.grid(row=5, column=1, sticky='w')
        txtDeafInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=1,
            width=80
            )
        #txtDeafInfo.insert(tk.INSERT, "\u2022 A deafened creature can't hear and automatically fails any ability check that requires hearing.")
        txtDeafInfo.grid(row=6, column=2, sticky='w')
        lblFright = ttk.Label(master=infoFrame, text="Frightened", font=self.bigFont)
        lblFright.grid(row=7, column=1, sticky='w')
        txtFrightInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txtFrightInfo.insert(tk.INSERT, "\u2022 A frightened creature has disadvantage on Ability Checks and AttackRools while the source of its fear is within Line of Sight.\n\u2022 The creature can't willingly move closer to the source of its fear.")
        txtFrightInfo.grid(row=8, column=2, sticky='w')
        lblGrappled = ttk.Label(master=infoFrame, text="Grappled", font=self.bigFont)
        lblGrappled.grid(row=9, column=1, sticky='w')
        txtGrappledInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txtGrappledInfo.insert(tk.INSERT, "\u2022 A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n\u2022 The condition ends if the Grappler is incapacitated (see the condition).\n\u2022 the condition also ends if an Effect removes the grappled creature from the reach of the Grappler or Grappling Effect, such as when a creature is hurled away by the Thunderwave spell.")
        txtGrappledInfo.grid(row=10, column=2, sticky='w')
        lblIncapacitated = ttk.Label(master=infoFrame, text="Incapacitated", font=self.bigFont)
        lblIncapacitated.grid(row=11, column=1, sticky='w')
        txtIncapacitatedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=1,
            width=80
            )
        #txtIncapacitatedInfo.insert(tk.INSERT, "\u2022 An incapacitated creature can't take Actions or Reactions.")
        txtIncapacitatedInfo.grid(row=12, column=2, sticky='w')
        lblInvisible = ttk.Label(master=infoFrame, text="Invisible", font=self.bigFont)
        lblInvisible.grid(row=13, column=1, sticky='w')
        txtInvisibleInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txtInvisibleInfo.insert(tk.INSERT, "\u2022 An invisible creature is impossible to see without the aid of magic or a Special sense. For the Purpose of Hiding, the creature is heavily obscured. The creature's location can be detected by any noise it makes or any tracks it leaves.\n\u2022 Attack Rolls against the creature have disadvantage, and the creature's Attack Rolls have advantage.")
        txtInvisibleInfo.grid(row=14, column=2, sticky='w')
        lblParalyzed = ttk.Label(master=infoFrame, text="Paralyzed", font=self.bigFont)
        lblParalyzed.grid(row=15, column=1, sticky='w')
        txtParalyzedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txtParalyzedInfo.insert(tk.INSERT, "\u2022 A paralyzed creature is incapacitated (see the condition) and can't move or speak.\n\u2022 the creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 Attack Rolls against the creature have advantage.\n\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.")
        txtParalyzedInfo.grid(row=16, column=2, sticky='w')
        lblPetrified = ttk.Label(master=infoFrame, text="Petrified", font=self.bigFont)
        lblPetrified.grid(row=17, column=1, sticky='w')
        txtPetrifiedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=9,
            width=80
            )
        #txtPetrifiedInfo.insert(tk.INSERT, "\u2022 A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into a solid inanimate substance (usually stone). Its weight increases by a factor of ten, and it ceases aging.\n\u2022 The creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n\u2022 Attack Rolls against the creature have advantage.\n\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 The creature has Resistance to all damage.\n\u2022 The creature is immune to poison and disease, although a poison or disease already in its system is suspended, not neutralized.")
        txtPetrifiedInfo.grid(row=18, column=2, sticky='w')
        lblPoisoned = ttk.Label(master=infoFrame, text="Poisoned", font=self.bigFont)
        lblPoisoned.grid(row=19, column=1, sticky='w')
        txtPoisonedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=1,
            width=80
            )
        #txtPoisonedInfo.insert(tk.INSERT, "\u2022 A poisoned creature has disadvantage on Attack Rolls and Ability Checks.")
        txtPoisonedInfo.grid(row=20, column=2, sticky='w')
        lblProne = ttk.Label(master=infoFrame, text="Prone", font=self.bigFont)
        lblProne.grid(row=21, column=1, sticky='w')
        txtProneInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=4,
            width=80
            )
        #txtProneInfo.insert(tk.INSERT, "\u2022 A prone creature's only Movement option is to crawl, unless it stands up and thereby ends the condition.\n\u2022 The creature has disadvantage on Attack Rolls.\n\u2022 An Attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the Attack roll has disavantage.")
        txtProneInfo.grid(row=22, column=2, sticky='w')
        lblRestrained = ttk.Label(master=infoFrame, text="Restrained", font=self.bigFont)
        lblRestrained.grid(row=23, column=1, sticky='w')
        txtRestrainedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txtRestrainedInfo.insert(tk.INSERT, "\u2022 A restrained creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.\n\u2022 The creature has disadvantage on Dexterity Saving Throws.")
        txtRestrainedInfo.grid(row=24, column=2, sticky='w')
        lblStunned = ttk.Label(master=infoFrame, text="Stunned", font=self.bigFont)
        lblStunned.grid(row=25, column=1, sticky='w')
        txtStunnedInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        #txtStunnedInfo.insert(tk.INSERT, "\u2022 A stunned creature is incapacitated (see the condition), can't move, and can speak only falteringly.\n\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 Attack Rolls against the creature have advantage.")
        txtStunnedInfo.grid(row=26, column=2, sticky='w')
        lblUnconscious = ttk.Label(master=infoFrame, text="Unconscious", font=self.bigFont)
        lblUnconscious.grid(row=27, column=1, sticky='w')
        txtUnconsciousInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=6,
            width=80
            )
        #txtUnconsciousInfo.insert(tk.INSERT, "\u2022 An unconscious creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n\u2022 The creature drops whatever it's holding and falls prone.\n\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 Attack Rolls against the creature have advantage.\n\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.")
        txtUnconsciousInfo.grid(row=28, column=2, sticky='w')
        lblExhaustion = ttk.Label(master=infoFrame, text="Exhaustion", font=self.titleFont)
        lblExhaustion.grid(row=29, column=0, sticky='w', columnspan=2)
        txtExhaustionInfo = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=6,
            width=80
            )
        txtExhaustionInfo.grid(row=30, column=2, sticky='w')
        lblLevel1 = ttk.Label(master=infoFrame, text="Level 1", font=self.bigFont)
        lblLevel1.grid(row=31, column=1, sticky='w')
        txtLevel1Info = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txtLevel1Info.grid(row=32, column=2, sticky='w')
        lblLevel2 = ttk.Label(master=infoFrame, text="Level 2", font=self.bigFont)
        lblLevel2.grid(row=33, column=1, sticky='w')
        txtLevel2Info = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txtLevel2Info.grid(row=34, column=2, sticky='w')
        lblLevel3 = ttk.Label(master=infoFrame, text="Level 3", font=self.bigFont)
        lblLevel3.grid(row=35, column=1, sticky='w')
        txtLevel3Info = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txtLevel3Info.grid(row=36, column=2, sticky='w')
        lblLevel4 = ttk.Label(master=infoFrame, text="Level 4", font=self.bigFont)
        lblLevel4.grid(row=37, column=1, sticky='w')
        txtLevel4Info = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txtLevel4Info.grid(row=38, column=2, sticky='w')
        lblLevel5 = ttk.Label(master=infoFrame, text="Level 5", font=self.bigFont)
        lblLevel5.grid(row=39, column=1, sticky='w')
        txtLevel5Info = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=2,
            width=80
            )
        txtLevel5Info.grid(row=40, column=2, sticky='w')
        lblLevel6 = ttk.Label(master=infoFrame, text="Level 6", font=self.bigFont)
        lblLevel6.grid(row=41, column=1, sticky='w')
        txtLevel6Info = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=3,
            width=80
            )
        txtLevel6Info.grid(row=42, column=2, sticky='w')
        txtExhaustionContinued = tk.Text(
            master=infoFrame,
            font=self.regFont,
            wrap=tk.WORD,
            bg='gray28',
            fg='gray70',
            bd=0,
            height=12,
            width=80
            )
        txtExhaustionContinued.grid(row=43, column=2, sticky='w')

        fontToCheck = tk.font.Font(family='Papyrus', size='12')
        bullet_width = fontToCheck.measure("\u2022 ")
        em = fontToCheck.measure("m")
        txtBlindInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtCharmedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtDeafInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtFrightInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtGrappledInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtIncapacitatedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtInvisibleInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtParalyzedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtPetrifiedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtPoisonedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtProneInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtRestrainedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtStunnedInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)
        txtUnconsciousInfo.tag_configure("bulleted", lmargin1=em, lmargin2=em+bullet_width)

        txtBlindInfo.insert(tk.END, "\u2022 A blinded creature can't see and automatically fails any ability check that requires sight.\n", 'bulleted')
        txtBlindInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.", 'bulleted')

        txtCharmedInfo.insert(tk.END, "\u2022 A charmed creature can't Attack the charmer of target the charmer with harmful Abilities or magical Effects.\n", 'bulleted')
        txtCharmedInfo.insert(tk.END, "\u2022 The charmer has advantage on any ability check to interact socially with the creature.", 'bulleted')

        txtDeafInfo.insert(tk.END, "\u2022 A deafened creature can't hear and automatically fails any ability check that requires hearing.", 'bulleted')

        txtFrightInfo.insert(tk.END, "\u2022 A frightened creature has disadvantage on Ability Checks and AttackRools while the source of its fear is within Line of Sight.\n.", 'bulleted')
        txtFrightInfo.insert(tk.END, "\u2022 The creature can't willingly move closer to the source of its fear.", 'bulleted')

        txtGrappledInfo.insert(tk.END, "\u2022 A grappled creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n", 'bulleted')
        txtGrappledInfo.insert(tk.END, "\u2022 The condition ends if the Grappler is incapacitated (see the condition).\n", 'bulleted')
        txtGrappledInfo.insert(tk.END, "\u2022 The condition also ends if an Effect removes the grappled creature from the reach of the Grappler or Grappling Effect, such as when a creature is hurled away by the Thunderwave spell.", 'bulleted')

        txtIncapacitatedInfo.insert(tk.END, "\u2022 An incapacitated creature can't take Actions or Reactions.", 'bulleted')

        txtInvisibleInfo.insert(tk.END, "\u2022 An invisible creature is impossible to see without the aid of magic or a Special sense. For the Purpose of Hiding, the creature is heavily obscured. The creature's location can be detected by any noise it makes or any tracks it leaves.\n", 'bulleted')
        txtInvisibleInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have disadvantage, and the creature's Attack Rolls have advantage.", 'bulleted')

        txtParalyzedInfo.insert(tk.END, "\u2022 A paralyzed creature is incapacitated (see the condition) and can't move or speak.\n", 'bulleted')
        txtParalyzedInfo.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n", 'bulleted')
        txtParalyzedInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.\n", 'bulleted')
        txtParalyzedInfo.insert(tk.END, "\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.", 'bulleted')

        txtPetrifiedInfo.insert(tk.END, "\u2022 A petrified creature is transformed, along with any nonmagical object it is wearing or carrying, into a solid inanimate substance (usually stone). Its weight increases by a factor of ten, and it ceases aging.\n", 'bulleted')
        txtPetrifiedInfo.insert(tk.END, "\u2022 The creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n", 'bulleted')
        txtPetrifiedInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.\n", 'bulleted')
        txtPetrifiedInfo.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n\u2022 The creature has Resistance to all damage.\n", 'bulleted')
        txtPetrifiedInfo.insert(tk.END, "\u2022 The creature has Resistance to all damage.\n", 'bulleted')
        txtPetrifiedInfo.insert(tk.END, "\u2022 The creature is immune to poison and disease, although a poison or disease already in its system is suspended, not neutralized.", 'bulleted')

        txtPoisonedInfo.insert(tk.END, "\u2022 A poisoned creature has disadvantage on Attack Rolls and Ability Checks.", 'bulleted')

        txtProneInfo.insert(tk.END, "\u2022 A prone creature's only Movement option is to crawl, unless it stands up and thereby ends the condition.\n", 'bulleted')
        txtProneInfo.insert(tk.END, "\u2022 The creature has disadvantage on Attack Rolls.\n", 'bulleted')
        txtProneInfo.insert(tk.END, "\u2022 An Attack roll against the creature has advantage if the attacker is within 5 feet of the creature. Otherwise, the Attack roll has disavantage.", 'bulleted')

        txtRestrainedInfo.insert(tk.END, "\u2022 A restrained creature's speed becomes 0, and it can't benefit from any bonus to its speed.\n", 'bulleted')
        txtRestrainedInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage, and the creature's Attack Rolls have disadvantage.\n", 'bulleted')
        txtRestrainedInfo.insert(tk.END, "\u2022 The creature has disadvantage on Dexterity Saving Throws.", 'bulleted')

        txtStunnedInfo.insert(tk.END, "\u2022 A stunned creature is incapacitated (see the condition), can't move, and can speak only falteringly.\n.", 'bulleted')
        txtStunnedInfo.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n", 'bulleted')
        txtStunnedInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.", 'bulleted')

        txtUnconsciousInfo.insert(tk.END, "\u2022 An unconscious creature is incapacitated (see the condition), can't move or speak, and is unaware of its surroundings.\n", 'bulleted')
        txtUnconsciousInfo.insert(tk.END, "\u2022 The creature drops whatever it's holding and falls prone.\n", 'bulleted')
        txtUnconsciousInfo.insert(tk.END, "\u2022 The creature automatically fails Strength and Dexterity Saving Throws.\n", 'bulleted')
        txtUnconsciousInfo.insert(tk.END, "\u2022 Attack Rolls against the creature have advantage.\n", 'bulleted')
        txtUnconsciousInfo.insert(tk.END, "\u2022 Any Attack that hits the creature is a critical hit if the attacker is within 5 feet of the creature.", 'bulleted')

        txtExhaustionInfo.insert(tk.END, "Some Special Abilities and Environmental Hazards, such as starvation and the long-term Effects of freezing or scorching temperatures, can lead to a Special condition call exhaustion. Exhaustion is measured in six levels. An Effect can give a creature one or more levels of exhaustion, as specified in the effect's description.")

        txtLevel1Info.insert(tk.END, "\u2022 Disadvantage on Ability Checks.", 'bulleted')
        txtLevel2Info.insert(tk.END, "\u2022 Speed halved.", 'bulleted')
        txtLevel3Info.insert(tk.END, "\u2022 Disadvantage on Attack Rolls and Saving Throws.", 'bulleted')
        txtLevel4Info.insert(tk.END, "\u2022 Hit point maximum halved.", 'bulleted')
        txtLevel5Info.insert(tk.END, "\u2022 Speed reduced to 0.", 'bulleted')
        txtLevel6Info.insert(tk.END, "\u2022 Death.", 'bulleted')

        txtExhaustionContinued.insert(tk.END, "If an already exhausted creature suffers another Effect that causes exhaustion, its current level of exhaustion increases by the amount specified in the effect's description.\n\n")
        txtExhaustionContinued.insert(tk.END, "A creature suffers the Effect of its current level of exhaustion as well as all lower levels. For example, a creature suffering level 2 exhaustion has its speed halved and has disadvantage on Ability Checks.\n\n")
        txtExhaustionContinued.insert(tk.END, "An Effect that removes exhaustion reduces its level as specified in the effect's description, with all exhaustion Effects Ending if a creature's exhaustion level is reduced below 1.\n\n")
        txtExhaustionContinued.insert(tk.END, "Finishing a Long Rest reduces a creature's exhaustion level by 1, provided that the creature has also ingested some food and drink.")

        txtBlindInfo.configure(state='disabled')
        txtCharmedInfo.configure(state='disabled')
        txtDeafInfo.configure(state='disabled')
        txtFrightInfo.configure(state='disabled')
        txtGrappledInfo.configure(state='disabled')
        txtIncapacitatedInfo.configure(state='disabled')
        txtInvisibleInfo.configure(state='disabled')
        txtParalyzedInfo.configure(state='disabled')
        txtPetrifiedInfo.configure(state='disabled')
        txtPoisonedInfo.configure(state='disabled')
        txtProneInfo.configure(state='disabled')
        txtRestrainedInfo.configure(state='disabled')
        txtStunnedInfo.configure(state='disabled')
        txtUnconsciousInfo.configure(state='disabled')
        txtExhaustionInfo.configure(state='disabled')
        txtLevel1Info.configure(state='disabled')
        txtLevel2Info.configure(state='disabled')
        txtLevel3Info.configure(state='disabled')
        txtLevel4Info.configure(state='disabled')
        txtLevel5Info.configure(state='disabled')
        txtLevel6Info.configure(state='disabled')
        txtExhaustionContinued.configure(state='disabled')

    def onMousewheel(self, event):
        self.conditionCanvas.yview_scroll(int(-1 * (event.delta/120)), 'units')
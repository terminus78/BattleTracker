import math
import tkinter as tk
from tkinter import ttk

class EventManager:
    def __init__(self, root):
        super()
        self.root = root
        
    def rightClickMenu(self, event):
        self.event = event
        self.tokenMenu = tk.Menu(self.root, tearoff=0)
        #self.trigMenu = tk.Menu(self.tokenMenu, tearoff=0)
        self.aoeMenu = tk.Menu(self.tokenMenu, tearoff=0)
        self.tokenMenu.add_command(label="Stats")
        self.tokenMenu.add_command(label="Damage")
        self.tokenMenu.add_command(label="Heal")
        self.tokenMenu.add_separator()
        #self.tokenMenu.add_cascade(label="Trig Functions", menu=self.trigMenu)
        #self.trigMenu.add_command(label="Distance", command=findDistance)
        #self.trigMenu.add_command(label="Find All in Range")
        #self.trigMenu.add_command(label="Spread Width")
        self.tokenMenu.add_cascade(label="AOE", menu=self.aoeMenu)
        self.aoeMenu.add_command(label="Circle")
        self.aoeMenu.add_command(label="Square")
        self.aoeMenu.add_command(label="Cone")
        self.aoeMenu.add_command(label="Line")
        self.aoeMenu.add_command(label="Ring Wall")
        self.aoeMenu.add_command(label="Line Wall")
        try:
            self.tokenMenu.tk_popup(self.event.x_root, self.event.y_root)
        finally:
            self.tokenMenu.grab_release()

    #def focusShiftOut(self):

    #def focusShiftIn(self):
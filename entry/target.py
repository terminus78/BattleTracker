import math
import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle

class Target():
    def __init__(self, root):
        self.root = root

    def targetWindow(self, tokens):
        self.tokenList = tokens
        self.targetWin = tk.Toplevel(self.root)
        self.targetWin.title("Target Creature")
        style = ThemedStyle(self.targetWin)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.targetWin.configure(bg=style.lookup('TLabel', 'background'))
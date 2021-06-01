import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

class PickLight():
    def __init__(self, root, widg=None):
        self.root = root
        self.widg = widg

    def open_light_win(self):
        self.light_win = tk.Toplevel(self.root)
        style = ThemedStyle(self.root)
        style.theme_use("equilux")
        self.light_win.configure(bg=style.lookup('TLabel', 'background'))
        self.light_win.wm_overrideredirect(1)
        self.light_win.wm_geometry("+-300+0")
        self.pfont = ('Papyrus', '14')
        border_frame = ttk.Frame(master=self.light_win)
        border_frame.grid(row=0, column=0, padx=20, pady=20)
        lbl_light_shape = ttk.Label(master=border_frame, text="Shape", font=self.pfont)
        lbl_light_shape.grid(row=0, column=0, sticky='w')
        shape_list = [
            'Square',
            'Circle',
            'Cone',
            'Line',
            'Ring'
        ]
        self.cbx_light_shape = ttk.Combobox(master=border_frame, values=shape_list, width=18, state='readonly')
        self.cbx_light_shape.grid(row=0, column=1, sticky='w', padx=5)
        self.cbx_light_shape.bind("<<ComboboxSelected>>", self.shape_select)
        lbl_size = ttk.Label(master=border_frame, text="Size", font=self.pfont)
        lbl_size.grid(row=1, column=0, sticky='w')
        self.cbx_light_size = ttk.Combobox(master=border_frame, width=18, state='readonly')
        self.cbx_light_size.grid(row=1, column=1, sticky='w', padx=5)
        lbl_angle = ttk.Label(master=border_frame, text="Angle", font=self.pfont)
        lbl_angle.grid(row=2, column=0, sticky='w')
        self.cbx_light_angle = ttk.Combobox(master=border_frame, width=18, state='readonly')
        self.cbx_light_angle.grid(row=2, column=1, sticky='w', padx=5)

    def shape_select(self):
        shape = self.cbx_light_shape.get()
        len_list = []
        if shape == 'Square':
            for i in range(5, 125, 5):
                len_list.append(i)
        elif shape == 'Circle' or shape == 'Ring':
            len_list = [
                10,
                15,
                20,
                30,
                40,
                50,
                60,
                80,
                100,
                120
            ]
        elif shape == 'Cone':
            for i in range(5, 105, 5):
                len_list.append(i)
        elif shape == 'Line':
            for i in range(5, 305, 5):
                len_list.append(i)

        self.cbx_light_size.config(values=len_list)
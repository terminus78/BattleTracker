import json
import math
import os

from tkinter import font
from tkinter.constants import S
from typing import MutableSet
from zipfile import ZipFile

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle


class ObjectBuilder():
    def __init__(self, root):
        if os.path.exists('entry\\bin\\object_lib.json') == False:
            messagebox.showwarning("Object Error", "Missing object library.")
            return
        else:
            with open('entry\\bin\\object_lib.json', 'r') as object_file:
                self.object_lib = json.load(object_file)

        self.root = root
        self.reg_font = ('Papyrus', '14')
        self.small_font = ('Papyrus', '9')
        self.obj_win = tk.Toplevel(self.root)
        self.obj_win.title("New Object")
        style = ThemedStyle(self.obj_win)
        style.theme_use("equilux")
        self.obj_win.configure(bg=style.lookup('TLabel', 'background'))

        collect_frame = ttk.Frame(master=self.obj_win)
        collect_frame.grid(row=0, column=0, padx=5)
        show_frame = ttk.Frame(master=self.obj_win)
        show_frame.grid(row=0, column=1, padx=5)
        sub_frame = ttk.Frame(master=self.obj_win)
        sub_frame.grid(row=1, column=0, columnspan=2, pady=10)

        lbl_select_obj = ttk.Label(master=collect_frame, text="Select Object: ", font=self.reg_font)
        lbl_select_obj.grid(row=0, column=0, sticky='w')
        self.object_list = []
        for obj in self.object_lib.keys():
            self.object_list.append(obj)
        self.cbx_object = ttk.Combobox(master=collect_frame, width=18, values=self.object_list, state='readonly')
        self.cbx_object.grid(row=0, column=1, sticky='e')

        lbl_obj_coord = ttk.Label(master=collect_frame, text="Position: ", font=self.reg_font)
        lbl_obj_coord.grid(row=1, column=0, sticky='w')
        coord_frame = ttk.Frame(master=collect_frame)
        coord_frame.grid(row=1, column=1, sticky='e')
        self.ent_obj_row = ttk.Entry(master=coord_frame, width=5)
        self.ent_obj_row.grid(row=0, column=0)
        self.ent_obj_col = ttk.Entry(master=coord_frame, width=5)
        self.ent_obj_col.grid(row=0, column=1, padx=5)
        self.ent_obj_z = ttk.Entry(master=coord_frame, width=5)
        self.ent_obj_z.grid(row=0, column=2)

        lbl_material = ttk.Label(master=collect_frame, text="Material: ", font=self.reg_font)
        lbl_material.grid(row=2, column=0, sticky='w')
        self.ent_material = ttk.Entry(master=collect_frame, width=18)
        self.ent_material.grid(row=2, column=1, sticky='e')

        lbl_ac = ttk.Label(master=collect_frame, text="AC: ", font=self.reg_font)
        lbl_ac.grid(row=3, column=0, sticky='w')
        self.ent_ac = ttk.Entry(master=collect_frame, width=18)
        self.ent_ac.grid(row=3, column=1, sticky='e')

        lbl_obj_hp = ttk.Label(master=collect_frame, text="Object HP: ", font=self.reg_font)
        lbl_obj_hp.grid(row=4, column=0, sticky='w')
        self.ent_obj_hp = ttk.Entry(master=collect_frame, width=18)
        self.ent_obj_hp.grid(row=4, column=1, sticky='e')

        lbl_obj_dim = ttk.Label(master=collect_frame, text="Dimensions: ", font=self.reg_font)
        lbl_obj_dim.grid(row=5, column=0, sticky='w')
        dim_frame = ttk.Frame(master=collect_frame)
        dim_frame.grid(row=5, column=1, sticky='ew')
        dim_frame.columnconfigure(0, weight=1)
        lbl_L = ttk.Label(master=dim_frame, text="L: ", font=self.small_font)
        lbl_L.grid(row=0, column=0, sticky='w', padx=20)
        self.ent_L = ttk.Entry(master=dim_frame, width=5, state='readonly')
        self.ent_L.grid(row=0, column=1, sticky='e')
        lbl_W = ttk.Label(master=dim_frame, text="W: ", font=self.small_font)
        lbl_W.grid(row=1, column=0, sticky='w', padx=20)
        self.ent_W = ttk.Entry(master=dim_frame, width=5, state='readonly')
        self.ent_W.grid(row=1, column=1, sticky='e')

        self.obj_canvas = tk.Canvas(master=show_frame, bg='gray28', width=200, height=200, highlightthickness=1)
        self.obj_canvas.grid(row=0, column=0)

        self.btn_submit = ttk.Button(master=sub_frame, text="Submit")
        self.btn_submit.grid(row=0, column=0)

    def submit(self):
        obj_name = self.cbx_object.get()
        if obj_name == "":
            messagebox.showwarning("Object Error", "Must select an object.")
            return False
        obj_num = len(self.root.obj_list[obj_name].values())
        obj_sub_name = f"{obj_name}_{obj_num+1}"

        obj_row = self.ent_obj_row.get()
        obj_col = self.ent_obj_col.get()
        obj_z = self.ent_obj_z.get()
        obj_mat = self.ent_material.get()
        obj_ac = self.ent_ac.get()
        obj_hp = self.ent_obj_hp.get()

        try:
            obj_row = int(obj_row)
            obj_col = int(obj_col)
            obj_z = int(obj_z)
            obj_ac = int(obj_ac)
            obj_hp = int(obj_hp)
        except ValueError:
            messagebox.showwarning("Object Error", "All fields that accept a number value must be positive whole numbers.")
            return False

        obj_dict = {
            "img_ref": self.object_lib[obj_name]['img_ref'],
            "coordinate": [obj_col, obj_row, obj_z],
            "material": obj_mat,
            "ac": obj_ac,
            "hp": obj_hp
        }

        self.root.obj_list[obj_name][obj_sub_name] = obj_dict
        return True
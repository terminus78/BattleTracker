from copy import Error
import json
import math
import os

import PIL.Image
from PIL import ImageTk
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
        self.cbx_object.bind("<<ComboboxSelected>>", self._on_select_object)

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
        self.cbx_material = ttk.Combobox(master=collect_frame, width=18, state='readonly')
        self.cbx_material.grid(row=2, column=1, sticky='e')
        self.cbx_material.bind("<<ComboboxSelected>>", self._on_select_mat)

        lbl_obj_size = ttk.Label(master=collect_frame, text="Size: ", font=self.reg_font)
        lbl_obj_size.grid(row=3, column=0, sticky='w')
        self.cbx_size = ttk.Combobox(master=collect_frame, width=18, state='readonly')
        self.cbx_size.grid(row=3, column=1, sticky='w')
        self.cbx_size.bind("<<ComboboxSelected>>", self._on_select_size)

        lbl_direction = ttk.Label(master=collect_frame, text="Direction: ", font=self.reg_font)
        lbl_direction.grid(row=4, column=0, sticky='w')
        self.cbx_direction = ttk.Combobox(master=collect_frame, width=18,  state='readonly')
        self.cbx_direction.grid(row=4, column=1, sticky='w')
        self.cbx_direction.bind("<<ComboboxSelected>>", self._on_select_direction)

        self.obj_canvas = tk.Canvas(master=show_frame, bg='gray28', width=200, height=200, highlightthickness=1)
        self.obj_canvas.grid(row=0, column=0)

        self.btn_submit = ttk.Button(master=sub_frame, text="Submit")
        self.btn_submit.grid(row=0, column=0)

    def _on_select_object(self, event):
        if self.cbx_material.get() != '' or self.cbx_size.get() != '' or self.cbx_direction.get() != '':
            self.cbx_material.set('')
            self.cbx_material.config(values=[])
            self.cbx_size.set('')
            self.cbx_size.config(values=[])
            self.cbx_direction.set('')
            self.cbx_direction.config(values=[])

        self.sel_object = self.cbx_object.get()
        mat_list = []
        for mat in self.object_lib[self.sel_object]['material'].keys():
            mat_list.append(mat)
        self.cbx_material.config(values=mat_list)

        try:
            self.obj_canvas.delete('all')
        except AttributeError:
            print('excepted')

    def _on_select_mat(self, event):
        if self.cbx_size.get() != '' or self.cbx_direction.get() != '':
            self.cbx_size.set('')
            self.cbx_size.config(values=[])
            self.cbx_direction.set('')
            self.cbx_direction.config(values=[])

        self.sel_material = self.cbx_material.get()
        size_list = []
        for size in self.object_lib[self.sel_object]['material'][self.sel_material]['size'].keys():
            size_list.append(size)
        self.cbx_size.config(values=size_list)

        try:
            self.obj_canvas.delete('all')
        except AttributeError:
            print('excepted')

    def _on_select_size(self, event):
        if self.cbx_direction.get() != '':
            self.cbx_direction.set('')
            self.cbx_direction.config(values=[])
        
        self.sel_size = self.cbx_size.get()
        dir_list = []
        for dir in self.object_lib[self.sel_object]['material'][self.sel_material]['size'][self.sel_size]['image'].keys():
            dir_list.append(dir)
        self.cbx_direction.config(values=dir_list)

        try:
            self.obj_canvas.delete('all')
        except AttributeError:
            print('excepted')

    def _on_select_direction(self, event):
        try:
            self.obj_canvas.delete('all')
        except AttributeError:
            print('excepted')

        sel_dir = self.cbx_direction.get()
        obj_image_path = self.object_lib[self.sel_object]['material'][self.sel_material]['size'][self.sel_size]['image'][sel_dir]
        object_image = ImageTk.PhotoImage(image=PIL.Image.open(obj_image_path).resize((150,150)))
        self.canvas_image = self.obj_canvas.create_image(0, 5, anchor='nw', image=object_image)
        self.canvas_image = object_image

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
        obj_L = self.ent_L.get()
        obj_W = self.ent_W.get()

        try:
            obj_row = int(obj_row)
            obj_col = int(obj_col)
            obj_z = int(obj_z)
            obj_ac = int(obj_ac)
            obj_hp = int(obj_hp)
            obj_L = int(obj_L)
            obj_W = int(obj_W)
        except ValueError:
            messagebox.showwarning("Object Error", "All fields that accept a number value must be positive whole numbers.")
            return False

        obj_row -= 1
        obj_col -= 1
        if obj_row < 0 or obj_row > self.root.mapsize[0] - 1 or obj_col < 0 or obj_col > self.root.mapsize[1] - 1:
            messagebox.showwarning("Object Error", "Coordinate out of range of map.")
            return False

        obj_dict = {
            "img_ref": self.object_lib[obj_name]['img_ref'],
            "coordinate": [obj_col, obj_row, obj_z],
            "material": obj_mat,
            "ac": obj_ac,
            "hp": obj_hp,
            "length": obj_L,
            "width": obj_W
        }

        self.root.obj_list[obj_name][obj_sub_name] = obj_dict
        return True
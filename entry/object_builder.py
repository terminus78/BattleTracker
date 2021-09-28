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
    def __init__(self, root, map_size):
        if os.path.exists('entry\\bin\\object_lib.json') == False:
            messagebox.showwarning("Object Error", "Missing object library.")
            return
        else:
            with open('entry\\bin\\object_lib.json', 'r') as object_file:
                self.object_lib = json.load(object_file)

        self.root = root
        self.map_size = map_size
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

        lbl_rename = ttk.Label(master=collect_frame, text="Rename: ", font=self.reg_font)
        lbl_rename.grid(row=5, column=0, sticky='w')
        self.ent_rename = ttk.Entry(master=collect_frame, width=18)
        self.ent_rename.grid(row=5, column=1, sticky='w')

        self.obj_canvas = tk.Canvas(master=show_frame, bg='gray28', width=200, height=200, highlightthickness=0, borderwidth=0)
        self.obj_canvas.grid(row=0, column=0)

        self.btn_submit = ttk.Button(master=sub_frame, text="Submit", state=['disabled'])
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
        self.btn_submit.state(['disabled'])

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
        self.btn_submit.state(['disabled'])

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
        self.btn_submit.state(['disabled'])

    def _on_select_direction(self, event):
        try:
            self.obj_canvas.delete('all')
        except AttributeError:
            print('excepted')

        self.sel_dir = self.cbx_direction.get()
        canvas_width = self.obj_canvas.winfo_width()
        canvas_height = self.obj_canvas.winfo_height()
        obj_image_path = self.object_lib[self.sel_object]['material'][self.sel_material]['size'][self.sel_size]['image'][self.sel_dir]
        object_image = ImageTk.PhotoImage(image=PIL.Image.open(obj_image_path).resize((canvas_width,canvas_height)))
        self.canvas_image = self.obj_canvas.create_image(canvas_width/2, canvas_height/2, anchor='center', image=object_image)
        self.canvas_image = object_image
        
        if self.ent_obj_row.get() != "" and self.ent_obj_col.get() != "" and self.ent_obj_z.get() != "":
            self.btn_submit.state(['!disabled'])

    def generate_obj_name(self):
        obj_in_list = False
        for item in self.root.obj_list:
            name_len = len(self.obj_name)
            if self.obj_name == item[:name_len]:
                obj_in_list = True
        suffix = 1
        if obj_in_list:
            for item in self.root.obj_list:
                if self.obj_name == item[:name_len]:
                    if int(item[(name_len+1):]) == suffix:
                        suffix += 1
        return f"{self.obj_name}_{suffix}"

    def submit(self):
        self.obj_name = self.cbx_object.get()
        if self.obj_name == "":
            messagebox.showwarning("Object Error", "Must select an object.")
            return False
        given_name = self.ent_rename.get()
        if given_name == "":
            act_name = self.generate_obj_name()
        else:
            act_name = given_name

        obj_row = self.ent_obj_row.get()
        obj_col = self.ent_obj_col.get()
        obj_z = self.ent_obj_z.get()
        obj_mat = self.sel_material
        obj_size = self.sel_size

        obj_L = self.object_lib[self.sel_object]['material'][self.sel_material]['size'][self.sel_size]['dim'][1]
        obj_W = self.object_lib[self.sel_object]['material'][self.sel_material]['size'][self.sel_size]['dim'][0]
        obj_img = self.object_lib[self.sel_object]['material'][self.sel_material]['size'][self.sel_size]['image'][self.sel_dir]

        if obj_mat == "" or obj_size == "" or obj_L == "" or obj_W == "":
            messagebox.showwarning("Object Error", "All required fields must be filled out.")
            return False

        try:
            obj_row = int(obj_row)
            obj_col = int(obj_col)
            obj_z = int(obj_z)
            
            obj_row -= 1
            obj_col -= 1
 
        except ValueError:
            messagebox.showwarning("Object Error", "All fields that accept a number value must be positive whole numbers.")
            return False

        if obj_row < 0 or obj_row > self.map_size[0] - 1 or obj_col < 0 or obj_col > self.map_size[1] - 1:
            messagebox.showwarning("Object Error", "Coordinate out of range of map.")
            return False

        obj_dict = {
            "name": act_name,
            "img_ref": obj_img,
            "coordinate": [obj_col, obj_row, obj_z],
            "material": obj_mat,
            "size": obj_size,
            "length": obj_L,
            "width": obj_W
        }

        self.root.obj_list.append(obj_dict)
        return True
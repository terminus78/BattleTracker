import math

import tkinter as tk
from tkinter import ttk, messagebox
from ttkthemes import ThemedStyle

class PickLight():
    def __init__(self, root, widg):
        self.root = root
        self.widg = widg
        self.x = self.root.winfo_pointerx()
        self.y = self.root.winfo_pointery()

    def open_light_win(self):
        x_offset = -340
        y_offset = 20
        self.light_win = tk.Toplevel(self.widg)
        style = ThemedStyle(self.root)
        style.theme_use("equilux")
        self.light_win.configure(bg=style.lookup('TLabel', 'background'))
        self.light_win.wm_overrideredirect(1)
        self.light_win.wm_geometry(f"+{self.x + x_offset}+{self.y + y_offset}")
        self.pfont = ('Papyrus', '14')
        self.light_win.focus_set()
        self.light_win.focus_force()
        self.light_win.attributes('-topmost', True)
        border_frame = ttk.Frame(master=self.light_win, borderwidth=2, relief='sunken')
        border_frame.grid(row=0, column=0, padx=20, pady=20)#, ipadx=10, ipady=10)
        btn_close = tk.Button(master=border_frame, text="X", command=self.light_win.destroy, bg='gray18', fg='gray70', activebackground='red3', bd=0, relief='sunken', font=('Papyrus', '8'), width=2, height=1, anchor='center')
        btn_close.grid(row=0, column=1, sticky='e', padx=5)
        lbl_light_shape = ttk.Label(master=border_frame, text="Shape", font=self.pfont)
        lbl_light_shape.grid(row=1, column=0, sticky='w')
        shape_list = [
            'Square',
            'Circle',
            'Cone',
            'Line',
            'Ring'
        ]
        self.cbx_light_shape = ttk.Combobox(master=border_frame, values=shape_list, width=18, state='readonly')
        self.cbx_light_shape.grid(row=1, column=1, sticky='w', padx=5)
        self.cbx_light_shape.bind("<<ComboboxSelected>>", self.shape_select)
        lbl_size = ttk.Label(master=border_frame, text="Size", font=self.pfont)
        lbl_size.grid(row=2, column=0, sticky='w')
        self.cbx_light_size = ttk.Combobox(master=border_frame, width=18, state='readonly')
        self.cbx_light_size.grid(row=2, column=1, sticky='w', padx=5)
        lbl_angle = ttk.Label(master=border_frame, text="Angle from North", font=self.pfont)
        lbl_angle.grid(row=3, column=0, sticky='w')
        self.cbx_light_angle = ttk.Combobox(master=border_frame, width=18, state='readonly')
        self.cbx_light_angle.grid(row=3, column=1, sticky='w', padx=5)
        self.btn_confirm = ttk.Button(master=border_frame, text="Confirm")
        self.btn_confirm.grid(row=4, column=0, columnspan=2, pady=5)

    def shape_select(self, event):
        shape = self.cbx_light_shape.get()
        len_list = []
        angle_list = []
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
                90,
                100,
                120
            ]
        elif shape == 'Cone':
            for i in range(5, 105, 5):
                len_list.append(i)
            for i in range(0, 361, 45):
                angle_list.append(i)
        elif shape == 'Line':
            for i in range(5, 305, 5):
                len_list.append(i)
            for i in range(0, 361, 45):
                angle_list.append(i)

        self.cbx_light_size.config(values=len_list)
        self.cbx_light_size.set('')
        self.cbx_light_angle.config(values=angle_list)
        self.cbx_light_angle.set(''),

    def collect(self):
        shape = self.cbx_light_shape.get()
        size = self.cbx_light_size.get()
        angle = self.cbx_light_angle.get()
        offset_array = []

        if shape == '':
            return
        if size == '':
            return

        size = int(int(size) / 5)
        if shape == 'Square':
            offset_array = self.fill_square(size)
        elif shape == 'Circle':
            points = self.fill_circle(size)
            offset_array = self.points_to_offsets(points)
        elif shape == 'Ring':
            #points = self.get_ring_8th(size)
            points = self.brute_ring(size)
            offset_array = self.points_to_offsets(points)
        
        return offset_array, shape

    def points_to_offsets(self, points):
        pos = [0,0]
        offsets = []
        for point in points:
            dist = [point[0]-pos[0], point[1]-pos[1]]
            offsets.append(dist)
            pos = point
        return offsets

    def fill_square(self, size):
        points = []
        col = 1
        area = int(size**2)
        for i in range(1, area):
            if col < size:
                points.append((1,0))
                col += 1
            elif col == size:
                points.append((-1 * (col-1), 1))
                col = 1
        return points

    def fill_circle(self, r, center=[0.5, 0.5]):
        #r += 0.5
        top = int(center[1] - r)
        bottom = int(center[1] + r)
        points = []

        for y in range(top, bottom+1):
            dy = y - center[1]
            dx = math.sqrt(r*r - dy*dy)
            left = math.ceil(center[0] - dx)
            right = math.floor(center[0] + dx)
            for x in range(left, right+1):
                points.append([x,y])

        return points

    def transform_ring_points(self, x, y):
        x = int(x)
        y = int(y)
        return [( x,  y),
                ( y,  x),
                (-x,  y),
                (-y,  x),
                ( x, -y),
                ( y, -x),
                (-x, -y),
                (-y, -x)]

    def get_ring_8th(self, r):
        points = []
        x = 0
        y = -r
        F_M = 1 - r
        d_e = 3
        d_ne = -(2 * r) + 5
        points.extend(self.transform_ring_points(x, y))
        while x < -y:
            if F_M <= 0:
                F_M += d_e
            else:
                F_M += d_ne
                d_ne += 2
                y += 1
            d_e += 2
            d_ne += 2
            x += 1
            points.extend(self.transform_ring_points(x, y))
        return points

    def brute_ring(self, r):
        points = []
        center = [0.5, 0.5]
        f = 1 - r
        dx = 1
        dy = -2 * r
        x = 0
        y = r
        # points.append([center[0], center[1] + r])
        # points.append([center[0], center[1] + r])
        # points.append([center[0], center[1] + r])
        # points.append([center[0], center[1] + r])

        while x < y:
            if f >= 0:
                y -= 1
                dy += 2
                f += dy
            x += 1
            dx += 2
            f += dx
            points.append([center[0] + x, center[1] + y])
            points.append([center[0] - x, center[1] + y])
            points.append([center[0] + x, center[1] - y])
            points.append([center[0] - x, center[1] - y])
            points.append([center[0] + y, center[1] + x])
            points.append([center[0] - y, center[1] + x])
            points.append([center[0] + y, center[1] - x])
            points.append([center[0] - y, center[1] - x])
        return points

    def escape(self):
        self.light_win.destroy()


def GenLightWin(root, widg):
    light_win = PickLight(root, widg)
    return light_win
import math

import tkinter as tk
from tkinter import ttk, messagebox
from tkinter.constants import X, Y
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
            for i in range(0, 346, 15):
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
            #points = self.brute_ring(size)
            points = self.no_fill_circle(size)
            offset_array = self.points_to_offsets(points)
        elif shape == 'Line':
            angle_diff = 0
            octant = 1
            if angle == '':
                return
            angle = int(angle)
            if angle == 0:
                octant = 0
                end_x = size
                end_y = 0
            elif angle == 180:
                octant = 0
                end_x = -size
                end_y = 0

            if octant > 0:
                if angle > 45 and angle < 90:
                    angle_diff = 45
                    octant = 2
                elif angle >= 90 and angle < 135:
                    angle_diff = 90
                    octant = 3
                elif angle >= 135 and angle < 180:
                    angle_diff = 135
                    octant = 4
                elif angle >= 180 and angle < 225:
                    angle_diff = 180
                    octant = 5
                elif angle >= 225 and angle < 270:
                    angle_diff = 225
                    octant = 6
                elif angle >= 270 and angle < 315:
                    angle_diff = 270
                    octant = 7
                elif angle >= 315 and angle < 360:
                    angle_diff = 315
                    octant = 8
                angle -= angle_diff
                # Flip odd octant angles to simplify math
                if octant % 2 == 0:
                    angle = abs(angle - 45)
                short_leg = int((angle * size) / 45)
                if octant == 1:
                    end_x = size
                    end_y = short_leg
                elif octant == 2:
                    end_x = short_leg
                    end_y = size
                elif octant == 3:
                    end_x = -short_leg
                    end_y = size
                elif octant == 4:
                    end_x = -size
                    end_y = short_leg
                elif octant == 5:
                    end_x = -size
                    end_y = -short_leg
                elif octant == 6:
                    end_x = -short_leg
                    end_y = -size
                elif octant == 7:
                    end_x = short_leg
                    end_y = -size
                elif octant == 8:
                    end_x = size
                    end_y = -short_leg
            points = self.draw_line(0, 0, end_x, end_y)
            offset_array = self.points_to_offsets(points)
        else:
            return
        
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

    def no_fill_circle(self, r):
        points = []
        y = 1
        x = r

        while x > y:
            dy = y - 0.5
            dx = math.sqrt(r*r - dy*dy)
            left = math.ceil(0.5 - dx)
            right = math.floor(0.5 + dx)
            points.extend(self.transform_no_fill(left, y))
            points.extend(self.transform_no_fill(right, y))
            y += 1

        return points

    def transform_no_fill(self, x, y):
        x = int(x)
        y = int(y)
        return [
            (  x,   y),
            (1-y,   x),
            (1-x, 1-y),
            (  y, 1-x)
        ]

    def draw_line(self, x1, y1, x2, y2):
        points = []
        # undef is for a vertical line
        undef = False
        small_slope = True
        m_error = 0
        if x1 > x2:
            start_x = x2
            start_y = y2
            end_x = x1
            end_y = y1
            x1 = start_x
            x2 = end_x
            y1 = start_y
            y2 = end_y
        elif x1 == x2:
            undef = True
            if y1 > y2:
                start_x = x2
                start_y = y2
                end_x = x1
                end_y = y1
                x1 = start_x
                x2 = end_x
                y1 = start_y
                y2 = end_y

        if not undef:
            dx = x2 - x1
            dy = y2 - y1
            m = dy / dx
            if m > 1 or m < -1:
                small_slope = False
                if m < -1:
                    start_x = x2
                    start_y = y2
                    end_x = x1
                    end_y = y1
                    x1 = start_x
                    x2 = end_x
                    y1 = start_y
                    y2 = end_y

            if small_slope:
                y = y1
                if m >= 0:
                    for x in range(x1, x2+1):
                        points.append([x, y])
                        m_error += dy
                        if (m_error * 2) >= dx:
                            y += 1
                            m_error -= dx
                else:
                    for x in range(x1, x2+1):
                        points.append([x, y])
                        if (m_error + m) > -0.5:
                            m_error += m
                        else:
                            y -= 1
                            m_error = m_error + m + 1
            else:
                x = x1
                if m > 0:
                    for y in range(y1, y2+1):
                        points.append([x, y])
                        m_error += dx
                        if (m_error * 2) >= dy:
                            x += 1
                            m_error -= dy
                else:
                    m = 1/m
                    for y in range(y1, y2+1):
                        points.append([x, y])
                        if (m_error + m) > -0.5:
                            m_error += m
                        else:
                            x -= 1
                            m_error = m_error + m + 1
        else:
            x = x1
            for y in range(y1, y2+1):
                points.append([x, y])

        return points

    def escape(self):
        self.light_win.destroy()


def GenLightWin(root, widg):
    light_win = PickLight(root, widg)
    return light_win
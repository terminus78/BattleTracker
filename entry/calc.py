import math
import copy

import tkinter as tk
from tkinter import ttk, font, messagebox
from ttkthemes import ThemedStyle


class Calculator():
    def __init__(self, root):
        self.root = root
        self.font = ("Papyrus", "14")
        self.font_small = ("Papyrus", "12")

    def trig_win(self):
        self.trig = tk.Toplevel(self.root)
        self.trig.title("Trig Calculator")
        style = ThemedStyle(self.trig)
        style.theme_use("equilux")
        bg = style.lookup('TLabel', 'background')
        fg = style.lookup('TLabel', 'foreground')
        self.trig.configure(bg=style.lookup('TLabel', 'background'))
        self.trig.rowconfigure([0,1], minsize=100)
        self.trig.columnconfigure([0,1], minsize=100)
        self.from_frame = ttk.Frame(master=self.trig)
        self.from_frame.grid(row=0, column=0, padx=5)
        self.to_frame = ttk.Frame(master=self.trig)
        self.to_frame.grid(row=0, column=1, padx=5)
        self.result_frame = ttk.Frame(master=self.trig)
        self.result_frame.grid(row=1, column=0, columnspan=2, pady=5, padx=5)
        self.info_frame = ttk.Frame(master=self.trig, borderwidth=2, relief='ridge')
        self.info_frame.grid(row=2, column=0, columnspan=2)
        names = []
        coordinates = []
        for being in self.root.token_list:
            names.append(being["name"])
            coordinates.append(being["coordinate"])
            
        lbl_from = ttk.Label(master=self.from_frame, text="Origin", font=self.font)
        lbl_from.grid(row=0, column=0, sticky='w')
        lbl_creature_start = ttk.Label(master=self.from_frame, text="Creature/Object", font=self.font)
        lbl_creature_start.grid(row=0, column=1)
        self.drop_origin = ttk.Combobox(self.from_frame, width=27, values=names, state='readonly')
        self.drop_origin.grid(row=1, column=1, sticky='w')
        self.drop_origin.bind("<<ComboboxSelected>>", lambda e: self.show_origin(event=e, arg=[names, coordinates]))
        self.lbl_orig_coord = ttk.Label(master=self.from_frame, text=" ", font=self.font)
        self.lbl_orig_coord.grid(row=2, column=1, sticky='w')
        lbl_space_start = ttk.Label(master=self.from_frame, text="Coordinate", font=self.font)
        lbl_space_start.grid(row=3, column=1)
        origin_frame = ttk.Frame(master=self.from_frame)
        origin_frame.grid(row=4, column=1, sticky='w')
        self.ent_orig_row = ttk.Entry(master=origin_frame, width=5)
        self.ent_orig_row.grid(row=0, column=0, sticky='w')
        self.ent_orig_col = ttk.Entry(master=origin_frame, width=5)
        self.ent_orig_col.grid(row=0, column=1, sticky='w')
        self.ent_orig_z = ttk.Entry(master=origin_frame, width=5)
        self.ent_orig_z.grid(row=0, column=2, sticky='w')

        lbl_to = ttk.Label(master=self.to_frame, text="Destination", font=self.font)
        lbl_to.grid(row=0, column=0, sticky='w')
        lbl_creature_end = ttk.Label(master=self.to_frame, text="Creature/Object", font=self.font)
        lbl_creature_end.grid(row=0, column=1)
        self.drop_destination = ttk.Combobox(self.to_frame, width=27, values=names, state='readonly')
        self.drop_destination.grid(row=1, column=1, sticky='w')
        self.drop_destination.bind("<<ComboboxSelected>>", lambda e: self.show_destination(event=e, arg=[names, coordinates]))
        self.lbl_dest_coord = ttk.Label(master=self.to_frame, text=" ", font=self.font)
        self.lbl_dest_coord.grid(row=2, column=1, sticky='w')
        lbl_space_end = ttk.Label(master=self.to_frame, text="Coordinate", font=self.font)
        lbl_space_end.grid(row=3, column=1)
        dest_frame = ttk.Frame(master=self.to_frame)
        dest_frame.grid(row=4, column=1, sticky='w')
        self.ent_dest_row = ttk.Entry(master=dest_frame, width=5)
        self.ent_dest_row.grid(row=0, column=0, sticky='w')
        self.ent_dest_col = ttk.Entry(master=dest_frame, width=5)
        self.ent_dest_col.grid(row=0, column=1, sticky='w')
        self.ent_dest_z = ttk.Entry(master=dest_frame, width=5)
        self.ent_dest_z.grid(row=0, column=2, sticky='w')

        self.btn_calculate = ttk.Button(master=self.result_frame, text="Calculate Distance", command=lambda arg=[names, coordinates]: self.dist_btn(arg))
        self.btn_calculate.grid(row=0, column=0)
        lbl_act = ttk.Label(master=self.result_frame, text="True distance: ", font=self.font)
        lbl_act.grid(row=1, column=0)
        self.lbl_act_calc_result = ttk.Label(master=self.result_frame, text="Ready", font=self.font)
        self.lbl_act_calc_result.grid(row=1, column=1)
        lbl_rel = ttk.Label(master=self.result_frame, text="Relative distance: ", font=self.font)
        lbl_rel.grid(row=2, column=0)
        self.lbl_rel_calc_result = ttk.Label(master=self.result_frame, text="Ready", font=self.font, borderwidth=1, relief='groove')
        self.lbl_rel_calc_result.grid(row=2, column=1)
        self.lbl_calc_info_1 = ttk.Label(master=self.info_frame, text="True distance is based on real-world trigonometry.", font=self.font_small)
        self.lbl_calc_info_1.grid(row=0, column=0)
        self.lbl_calc_info_2 = ttk.Label(master=self.info_frame, text="True distance may not correspond to grid distance counting.", font=self.font_small)
        self.lbl_calc_info_2.grid(row=1, column=0)
        self.lbl_calc_info_3 = ttk.Label(master=self.info_frame, text="Relative distance mimics the game-specific way of adding up blocks.", font=self.font_small)
        self.lbl_calc_info_3.grid(row=2, column=0)
        self.lbl_calc_info_4 = ttk.Label(master=self.info_frame, text="For most situations, relative distance follows the rules of D&D more closely.", font=self.font_small)
        self.lbl_calc_info_4.grid(row=3, column=0)

    def show_origin(self, arg, event):
        select_origin = self.drop_origin.get()
        names = arg[0]
        coordinates = arg[1]
        index = names.index(select_origin)
        if coordinates[index][0] != "" and coordinates[index][1] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1
            z = coordinates[index][2]
            self.lbl_orig_coord.config(text="{0}: {1}: {2}".format(row, col, z))
        else:
            self.lbl_orig_coord.config(text="Off Map")

    def show_destination(self, arg, event):
        select_destination = self.drop_destination.get()
        names = arg[0]
        coordinates = arg[1]
        index = names.index(select_destination)
        if coordinates[index][0] != "" and coordinates[index][1] != "":
            row = int(coordinates[index][0]) + 1
            col = int(coordinates[index][1]) + 1
            z = coordinates[index][2]
            self.lbl_dest_coord.config(text="{0}: {1}: {2}".format(row, col, z))
        else:
            self.lbl_dest_coord.config(text="Off Map")
    
    def dist_btn(self, arg):
        origin_creat = self.drop_origin.get()
        destination_creat = self.drop_destination.get()
        origin_row = self.ent_orig_row.get()
        origin_col = self.ent_orig_col.get()
        origin_z = self.ent_orig_z.get()
        dest_row = self.ent_dest_row.get()
        dest_col = self.ent_dest_col.get()
        dest_z = self.ent_dest_z.get()
        coord_origin = None
        coord_dest = None
        index_creat_origin = None
        index_creat_dest = None
        if origin_creat != "" or destination_creat != "":
            names = arg[0]
            coordinates = arg[1]
            if origin_creat != "":
                index_creat_origin = names.index(origin_creat)
                coord_origin = coordinates[index_creat_origin]
                print(coord_origin)
            if destination_creat != "":
                index_creat_dest = names.index(destination_creat)
                coord_dest = coordinates[index_creat_dest]
        if (origin_row != "" and origin_col != "" and origin_z != "") or (dest_row != "" and dest_col != "" and dest_z != ""):
            if origin_row != "" and origin_col != "" and origin_z != "":
                try:
                    origin_row_int = int(origin_row) - 1
                    origin_col_int = int(origin_col) - 1
                    origin_z_int = int(origin_z)
                except ValueError:
                    messagebox.showwarning("Input Error", "Origin coordinates must be whole numbers.")
                    return
                coord_origin = [origin_row_int, origin_col_int, origin_z_int]
            if dest_row != "" and dest_col != "" and dest_z != "":
                try:
                    dest_row_int = int(dest_row) - 1
                    dest_col_int = int(dest_col) - 1
                    dest_z_int = int(dest_z)
                except ValueError:
                    messagebox.showwarning("Input Error", "Destination coordinates must be whole numbers.")
                    return
                coord_dest = [dest_row_int, dest_col_int, dest_z_int]
                print(coord_dest)
        if coord_origin is None or coord_dest is None:
            messagebox.showwarning("Input Error", "Please select or input an origin and a destination.")
            return
        if coord_origin[0] == "" or coord_origin[1] == "" or coord_origin[2] == "":
            messagebox.showwarning("Map Coordinate Failure", "Selected Origin Not on Map!")
            return
        if coord_dest[0] == "" or coord_dest[1] == "" or coord_dest[2] == "":
            messagebox.showwarning("Map Coordinate Failure", "Selected Destination Not on Map!")
            return
        
        self.actual_distance(coord_origin, coord_dest)
        self.relative_distance(coord_origin, coord_dest, index_creat_origin, index_creat_dest)

    def calc_dist(self, start, end):
        delta_x = abs((int(end[1]) * 5) - (int(start[1]) * 5))
        delta_y = abs((int(end[0]) * 5) - (int(start[0]) * 5))
        delta_z = abs((int(end[2]) * 5) - (int(start[2]) * 5))
        
        if delta_x == 0:
            grnd_hypo = delta_y
        elif delta_y == 0:
            grnd_hypo = delta_x
        else:
            grnd_hypo = math.sqrt(delta_x**2 + delta_y**2)

        if grnd_hypo == 0:
            distance = delta_z
        else:
            distance = math.sqrt(grnd_hypo**2 + delta_z**2)
        
        return distance
    
    def relative_distance(self, start, end, start_index, end_index):
        start_x, start_y, start_z = int(start[1]), int(start[0]), int(start[2])
        end_x, end_y, end_z = int(end[1]), int(end[0]), int(end[2])
        end_as_ints = [int(end[1]), int(end[0]), int(end[2])]
        curr_coord = [start_x, start_y, start_z]
        diff_x = end_x - start_x
        diff_y = end_y - start_y
        diff_z = end_z - start_z
        if diff_x == 0 and diff_y == 0 and diff_z == 0:
            #dist_found = True
            distance = 0
            self.lbl_rel_calc_result.config(text=f"{distance}ft")
            return
        '''
        else:
            dist_found = False
        '''
        start_corners = [curr_coord]
        end_corners = [end_as_ints]
        rotation_offset = [1, 1, -1, -1]
        if start_index is not None:
            start_size = self.root.token_list[start_index]['size']
            if start_size == 'large' or start_size == 'huge' or start_size == 'gargantuan':
                if start_size == 'large':
                    mod_plus_min = 1
                elif start_size == 'huge':
                    mod_plus_min = 2
                else:
                    mod_plus_min = 3
                row_mover = start_corners[0][0]
                col_mover = start_corners[0][1]
                z_mover = start_corners[0][2]
                indexer = 0
                for i in range(7):
                    if i % 2 == 0:
                        row_mover += rotation_offset[indexer]
                    else:
                        col_mover += rotation_offset[indexer]
                    if i == 3:
                        z_mover += 1
                        indexer = -1
                    start_corners.append([row_mover, col_mover, z_mover])
                    indexer += 1

        if end_index is not None:
            end_size = self.root.token_list[end_index]['size']
            if end_size == 'large' or end_size == 'huge' or end_size == 'gargantuan':
                if end_size == 'large':
                    mod_plus_min = 1
                elif end_size == 'huge':
                    mod_plus_min = 2
                else:
                    mod_plus_min = 3
                row_mover = end_corners[0][0]
                col_mover = end_corners[0][1]
                z_mover = end_corners[0][2]
                indexer = 0
                for i in range(7):
                    if i % 2 == 0:
                        row_mover += rotation_offset[indexer]
                    else:
                        col_mover += rotation_offset[indexer]
                    if i == 3:
                        z_mover += 1
                        indexer = -1
                    end_corners.append([row_mover, col_mover, z_mover])
                    indexer += 1

        if len(start_corners) < 8 and len(end_corners) < 8:
            diff_x = abs(end_corners[0][1] - start_corners[0][1])
            diff_y = abs(end_corners[0][0] - start_corners[0][0])
            diff_z = abs(end_corners[0][2] - start_corners[0][2])
            max_diff = max(diff_x, diff_y, diff_z)
            distance_traveled = max_diff * 5
        elif len(start_corners) == 8 and len(end_corners) < 8:
            distance_list = []
            for start_point in start_corners:
                diff_x = abs(end_corners[0][1] - start_point[1])
                diff_y = abs(end_corners[0][0] - start_point[0])
                diff_z = abs(end_corners[0][2] - start_point[2])
                distance_list.append(max(diff_x, diff_y, diff_z))
            min_dist_corner = min(distance_list)
            distance_traveled = min_dist_corner * 5
        elif len(start_corners) < 8 and len(end_corners) == 8:
            distance_list = []
            for end_point in end_corners:
                diff_x = abs(end_point[1] - start_corners[0][1])
                diff_y = abs(end_point[0] - start_corners[0][0])
                diff_z = abs(end_point[2] - start_corners[0][2])
                distance_list.append(max(diff_x, diff_y, diff_z))
            min_dist_corner = min(distance_list)
            distance_traveled = min_dist_corner * 5
        else:
            distance_list = []
            for start_point in start_corners:
                for end_point in end_corners:
                    diff_x = abs(end_point[1] - start_point[1])
                    diff_y = abs(end_point[0] - start_point[0])
                    diff_z = abs(end_point[2] - start_point[2])
                    distance_list.append(max(diff_x, diff_y, diff_z))
            min_dist_corner = min(distance_list)
            distance_traveled = min_dist_corner * 5

        
        self.lbl_rel_calc_result.config(text=f"{distance_traveled}ft")

        '''
        # Counterclockwise rotation
        rotation_offset = [-1, -1, 1, 1]
        distance_traveled = 0
        count_rounds = 0
        while dist_found == False:
            curr_x, curr_y, curr_z = curr_coord
            diff_x = end_x - curr_x
            diff_y = end_y - curr_y
            diff_z = end_z - curr_z
            if diff_x > 0 or diff_x < 0:
                sign_x = diff_x / abs(diff_x)
            else:
                sign_x = 0
            if diff_y > 0 or diff_y < 0:
                sign_y = diff_y / abs(diff_y)
            else:
                sign_y = 0
            if diff_z > 0 or diff_z < 0:
                sign_z = diff_z / abs(diff_z)
            else:
                sign_z = 0

            octant = [sign_x, sign_y, sign_z]
            shortest_distance = math.inf
            if octant[0] != 0 and octant[1] != 0 and octant[2] != 0:
                if octant[0] > 0 and octant[1] > 0:
                    index = 2
                elif octant[0] < 0 and octant[1] > 0:
                    index = 3
                elif octant[0] < 0 and octant[1] < 0:
                    index = 0
                else:
                    index = 1
                if octant[2] > 0:
                    check_up = True
                else:
                    check_up = False
                for i in range(7):
                    if index == 0 or index == 2:
                        curr_x += rotation_offset[index]
                    elif index == 1 or index == 3:
                        curr_y += rotation_offset[index]
                    else:
                        index = 0
                        curr_x += rotation_offset[index]
                    if i == 3:
                        if check_up:
                            curr_z += 1
                        else:
                            curr_z -= 1
                    check_dist = self.calc_dist([str(curr_y), str(curr_x), str(curr_z)], end)
                    if check_dist < shortest_distance:
                        shortest_distance = check_dist
                        curr_coord = [curr_x, curr_y, curr_z]
                    index += 1

            elif octant[0] == 0:
                if octant[1] == 0:
                    curr_coord = [curr_x, curr_y, curr_z + sign_z]
                elif octant[2] == 0:
                    curr_coord = [curr_x, curr_y + sign_y, curr_z]
                else:
                    if octant[1] > 0 and octant[2] > 0:
                        index = 2
                    elif octant[1] < 0 and octant[2] > 0:
                        index = 3
                    elif octant[1] < 0 and octant[2] < 0:
                        index = 0
                    else:
                        index = 1
                    for i in range(3):
                        if index == 0 or index == 2:
                            curr_z += rotation_offset[index]
                        elif index == 1 or index == 3:
                            curr_y += rotation_offset[index]
                        else:
                            index = 0
                            curr_z += rotation_offset[index]
                        check_dist = self.calc_dist([str(curr_y), str(curr_x), str(curr_z)], end)
                        if check_dist < shortest_distance:
                            shortest_distance = check_dist
                            curr_coord = [curr_x, curr_y, curr_z]
                        index += 1

            elif octant[1] == 0:
                if octant[2] == 0:
                    curr_coord = [curr_x + sign_x, curr_y, curr_z]
                else:
                    if octant[0] > 0 and octant[2] > 0:
                        index = 2
                    elif octant[0] < 0 and octant[2] > 0:
                        index = 3
                    elif octant[0] < 0 and octant[2] < 0:
                        index = 0
                    else:
                        index = 1
                    for i in range(3):
                        if index == 0 or index == 2:
                            curr_x += rotation_offset[index]
                        elif index == 1 or index == 3:
                            curr_z += rotation_offset[index]
                        else:
                            index = 0
                            curr_x += rotation_offset[index]
                        check_dist = self.calc_dist([str(curr_y), str(curr_x), str(curr_z)], end)
                        if check_dist < shortest_distance:
                            shortest_distance = check_dist
                            curr_coord = [curr_x, curr_y, curr_z]
                        index += 1

            else:
                if octant[0] > 0 and octant[1] > 0:
                    index = 2
                elif octant[0] < 0 and octant[1] > 0:
                    index = 3
                elif octant[0] < 0 and octant[1] < 0:
                    index = 0
                else:
                    index = 1
                for i in range(3):
                    if index == 0 or index == 2:
                        curr_x += rotation_offset[index]
                    elif index == 1 or index == 3:
                        curr_y += rotation_offset[index]
                    else:
                        index = 0
                        curr_x += rotation_offset[index]
                    check_dist = self.calc_dist([str(curr_y), str(curr_x), str(curr_z)], end)
                    if check_dist < shortest_distance:
                        shortest_distance = check_dist
                        curr_coord = [curr_x, curr_y, curr_z]
                    index += 1
            distance_traveled += 5
            if curr_coord == end_as_ints:
                dist_found = True
            if count_rounds == 50:
                dist_found = True
                messagebox.showerror("Fatal Error", "Restart program.\nError 0x001")
            count_rounds += 1
        self.lbl_rel_calc_result.config(text=f"{distance_traveled}ft")
        '''

    def actual_distance(self, start, end):
        distance = self.calc_dist(start, end)
        distance_FT = math.floor(distance)
        distance_INCH = round((distance - distance_FT) * 12)
        self.lbl_act_calc_result.config(text="{0}ft, {1}in".format(distance_FT, distance_INCH))
import math

import tkinter as tk

class Circle():
    def __init__(self, root):
        self.root = root
        self.map_frames = []
        for i in range(15):
            self.map_frames.append([])
            self.root.rowconfigure(i, minsize=33)
            for j in range(15):
                self.root.columnconfigure(j, minsize=33)
                space = tk.Frame(master=self.root, relief='raised', borderwidth=1, bg='gray28')
                space.grid(row=i, column=j, sticky='nsew')
                self.map_frames[i].append(space)

    def circle_points(self, radius):
        points = []
        x = 0
        y = -radius
        F_M = 1 - radius
        d_e = 3
        d_ne = -(2 * radius) + 5
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

    def points_to_offsets(self, points):
        pos = [0,0]
        offsets = []
        for point in points:
            dist = [point[0]-pos[0], point[1]-pos[1]]
            offsets.append(dist)
            pos = point
        return offsets

    def highlight(self, radius):
        curr_pos = [7, 7]
        points = self.circle_points(radius)
        offsets = self.points_to_offsets(points)
        
        for i in range(len(offsets)):
            curr_pos[0] += offsets[i][0]
            curr_pos[1] += offsets[i][1]
            if curr_pos[0] < 15 and curr_pos[1] < 15 and curr_pos[0] >= 0 and curr_pos[1] >= 0:
                self.map_frames[curr_pos[1]][curr_pos[0]].config(bg='SpringGreen3')

if __name__ == '__main__':
    window = tk.Tk()
    circ = Circle(window)
    circ.highlight(3)
    window.mainloop()
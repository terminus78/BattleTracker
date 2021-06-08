import math

import tkinter as tk

class Circle():
    def __init__(self, root):
        self.root = root
        self.map_frames = []
        for i in range(14):
            self.map_frames.append([])
            self.root.rowconfigure(i, minsize=33)
            for j in range(14):
                self.root.columnconfigure(j, minsize=33)
                space = tk.Frame(master=self.root, relief='raised', borderwidth=1, bg='gray28')
                space.grid(row=i, column=j, sticky='nsew')
                self.map_frames[i].append(space)

    def circle_points(self, radius):
        points = []
        y = 1
        x = radius

        while x > y:
            dy = y - 0.5
            dx = math.sqrt(radius*radius - dy*dy)
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

    def points_to_offsets(self, points):
        pos = [0,0]
        offsets = []
        for point in points:
            dist = [point[0]-pos[0], point[1]-pos[1]]
            offsets.append(dist)
            pos = point
        return offsets

    def highlight(self, radius):
        curr_pos = [6, 6]
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
    circ.highlight(4)
    window.mainloop()
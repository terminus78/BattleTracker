from tkinter import *


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, left_disp):
        "Display text in tooltip window"
        self.text = text
        x_offset = 17
        y_offset = 7
        if self.tipwindow or not self.text:
            return
        if left_disp:
            x_offset = -75
            y_offset = 20
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + x_offset
        y = y + cy + self.widget.winfo_rooty() + y_offset
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("Papyrus", "8", "normal"))
        label.pack(ipadx=1)
        self.tipwindow.attributes("-alpha", 0.0)
        self.fade_in()

    def fade_in(self):
        alpha = self.tipwindow.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.1
            self.tipwindow.attributes("-alpha", alpha)
            self.tipwindow.after(100, self.fade_in)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text, left_disp=False):
    tool_tip = ToolTip(widget)
    def enter(event):
        tool_tip.showtip(text, left_disp)
    def leave(event):
        tool_tip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
from tkinter import *


class ToolTip(object):

    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text, leftDisp):
        "Display text in tooltip window"
        self.text = text
        xOffset = 17
        yOffset = 7
        if self.tipwindow or not self.text:
            return
        if leftDisp:
            xOffset = -75
            yOffset = 20
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + xOffset
        y = y + cy + self.widget.winfo_rooty() + yOffset
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,
                      background="#ffffe0", relief=SOLID, borderwidth=1,
                      font=("Papyrus", "8", "normal"))
        label.pack(ipadx=1)
        self.tipwindow.attributes("-alpha", 0.0)
        self.fadeIn()

    def fadeIn(self):
        alpha = self.tipwindow.attributes("-alpha")
        if alpha < 1.0:
            alpha += 0.1
            self.tipwindow.attributes("-alpha", alpha)
            self.tipwindow.after(100, self.fadeIn)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text, leftDisp=False):
    toolTip = ToolTip(widget)
    def enter(event):
        toolTip.showtip(text, leftDisp)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)
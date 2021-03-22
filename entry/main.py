from rangeCalculator import RangeCalculator
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

window = tk.Tk()
window.title("BattleTracker")
#window.geometry("200x200")
style = ThemedStyle(window)
style.theme_use("equilux")
bg = style.lookup('TLabel', 'background')
fg = style.lookup('TLabel', 'foreground')
window.configure(bg=style.lookup('TLabel', 'background'))

newChar = RangeCalculator(window)

lblGreeting = ttk.Label(master=window, text="Welcome to the BattleTracker")
lblGreeting.grid(row=0, column=0)
btnOpen = ttk.Button(master=window, text="Input Stats")
btnOpen.bind("<Button>", lambda e: newChar.generateWindow())
btnOpen.grid(row=1, column=0)

def showLabel(label):
    lblTest = ttk.Label(master=window, text=newChar.collectStats()["name"])
    lblTest.grid(row=3, column=0)
    lblTest = ttk.Label(master=window, text=newChar.collectStats()["hP"])
    lblTest.grid(row=3, column=1)
    lblTest = ttk.Label(master=window, text=newChar.collectStats()["coordinate"])
    lblTest.grid(row=4, column=0)
    lblTest = ttk.Label(master=window, text=newChar.collectStats()["height"])
    lblTest.grid(row=4, column=1)
    lblTest = ttk.Label(master=window, text=newChar.collectStats()["size"])
    lblTest.grid(row=5, column=0)
    lblTest = ttk.Label(master=window, text=newChar.collectStats()["notes"])
    lblTest.grid(row=5, column=1)

btnShow = ttk.Button(master=window, text="Show name")
btnShow.bind("<Button>", lambda e: showLabel(e))
btnShow.grid(row=2, column=0)

window.mainloop()
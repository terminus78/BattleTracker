'''
from zipfile import ZipFile
import json


with ZipFile("H:\\Projects\\Programs\\Calculator\\First Battle.brpg", "w") as savefile:
    test_obj = {
        "TestDog": {
            "name": "TestDog",
            "hP": "5",
            "type": "ally",
            "height": "1",
            "size": "small",
            "coordinate": [
                "1",
                "1",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "\n"
        },
        "TestBird": {
            "name": "TestBird",
            "hP": "1",
            "type": "enemy",
            "height": "1",
            "size": "tiny",
            "coordinate": [
                "",
                "",
                ""
            ],
            "condition": [
                "normal"
            ],
            "notes": "Skwauk\n"
        },
        "TestCat": {
            "name": "TestCat",
            "hP": "6",
            "type": "dead",
            "height": "1",
            "size": "small",
            "coordinate": [
                "20",
                "32",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "Aww sad kitty\n"
        },
        "TestChicken": {
            "name": "TestChicken",
            "hP": "1",
            "type": "bystander",
            "height": "1",
            "size": "tiny",
            "coordinate": [
                "5",
                "16",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "He never wanted this\n"
        },
        "TestPig": {
            "name": "TestPig",
            "hP": "10",
            "type": "ally",
            "height": "1",
            "size": "medium",
            "coordinate": [
                "19",
                "7",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "An unlikely but hardy friend\n"
        },
        "TestShark": {
            "name": "TestShark",
            "hP": "15",
            "type": "enemy",
            "height": "1",
            "size": "medium",
            "coordinate": [
                "29",
                "29",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "What the hell is a shark doing here?\n"
        },
        "TestLemming": {
            "name": "TestLemming",
            "hP": "0",
            "type": "dead",
            "height": "1",
            "size": "tiny",
            "coordinate": [
                "",
                "",
                ""
            ],
            "condition": [
                "normal"
            ],
            "notes": "Well, we saw that coming\n"
        },
        "TestBigBad": {
            "name": "TestBigBad",
            "hP": "50",
            "type": "enemy",
            "height": "3",
            "size": "huge",
            "coordinate": [
                "16",
                "23",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "Oof\n"
        },
        "TestFox": {
            "name": "TestFox",
            "hP": "5",
            "type": "bystander",
            "height": "1",
            "size": "small",
            "coordinate": [
                "",
                "",
                ""
            ],
            "condition": [
                "normal"
            ],
            "notes": "Foxy\n"
        },
        "TestApe": {
            "name": "TestApe",
            "hP": "10",
            "type": "enemy",
            "height": "1",
            "size": "medium",
            "coordinate": [
                "1",
                "1",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "\n"
        },
        "TestBiggerGooder": {
            "name": "TestBiggerGooder",
            "hP": "400",
            "type": "ally",
            "height": "4",
            "size": "gargantuan",
            "coordinate": [
                "7",
                "5",
                "0"
            ],
            "condition": [
                "normal"
            ],
            "notes": "When godzilla decides to help...\n"
        }
    }
    testJSON = json.dumps(test_obj, indent=4)
    pref_dict = {
        "mapSize": [32, 46]
    }
    prefJSON = json.dumps(pref_dict, indent=4)
    savefile.writestr('preferences.json', prefJSON)
    savefile.writestr('creatures.json', testJSON)

var1, var2, var3 = [1, 2, 3]
print("{0} {1} {2}".format(var1, var2, var3))

import tkinter as tk
import tkinter.ttk as ttk

def iter_layout(layout, tab_amnt=0, elements=[]):
    """Recursively prints the layout children."""
    el_tabs = '  '*tab_amnt
    val_tabs = '  '*(tab_amnt + 1)

    for element, child in layout:
        elements.append(element)
        print(el_tabs+ '\'{}\': {}'.format(element, '{'))
        for key, value in child.items():
            if type(value) == str:
                print(val_tabs + '\'{}\' : \'{}\','.format(key, value))
            else:
                print(val_tabs + '\'{}\' : [('.format(key))
                iter_layout(value, tab_amnt=tab_amnt+3)
                print(val_tabs + ')]')

        print(el_tabs + '{}{}'.format('} // ', element))

    return elements

def stylename_elements_options(stylename, widget):
    """Function to expose the options of every element associated to a widget stylename."""

    try:
        # Get widget elements
        style = ttk.Style()
        layout = style.layout(stylename)
        config = widget.configure()

        print('{:*^50}\n'.format(f'Style = {stylename}'))

        print('{:*^50}'.format('Config'))
        for key, value in config.items():
            print('{:<15}{:^10}{}'.format(key, '=>', value))

        print('\n{:*^50}'.format('Layout'))
        elements = iter_layout(layout)

        # Get options of widget elements
        print('\n{:*^50}'.format('element options'))
        for element in elements:
            print('{0:30} options: {1}'.format(
                element, style.element_options(element)))

    except tk.TclError:
        print('_tkinter.TclError: "{0}" in function'
                'widget_elements_options({0}) is not a regonised stylename.'
                .format(stylename))

widget = ttk.Button(None)
class_ = widget.winfo_class()
stylename_elements_options(class_, widget)


import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, background="#ffffff")
        self.frame = tk.Frame(self.canvas, background="#ffffff")
        self.vsb = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")

        self.frame.bind("<Configure>", self.onFrameConfigure)

        self.populate()

    def populate(self):
        # Put in some fake data
        for row in range(100):
            tk.Label(self.frame, text="%s" % row, width=3, borderwidth="1",
                     relief="solid").grid(row=row, column=0)
            t="this is the second column for row %s" %row
            tk.Label(self.frame, text=t).grid(row=row, column=1)

    def onFrameConfigure(self, event):
        # Reset the scroll region to encompass the inner frame
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

if __name__ == "__main__":
    root=tk.Tk()
    example = Example(root)
    example.pack(side="top", fill="both", expand=True)
    root.mainloop()



def get_capslock_state():
    import ctypes
    hllDll = ctypes.WinDLL ("User32.dll")
    VK_CAPITAL = 0x90
    return hllDll.GetKeyState(VK_CAPITAL),

print(get_capslock_state())


import tkinter as tk

root = tk.Tk()

def key(event):
    #print(repr(event.char), repr(event.keysym), repr(event.keycode))
    print(event.char, event.keysym, event.keycode)

root.bind("<Key>", key)
root.mainloop()
'''

import tkinter as tk

class Example(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.main = tk.Canvas(self, width=400, height=400, 
                              borderwidth=0, highlightthickness=0,
                              background="bisque")
        self.main.pack(side="top", fill="both", expand=True)

        # add a callback for button events on the main canvas
        self.main.bind("<1>", self.on_main_click)

        for x in range(10):
            for y in range(10):
                canvas = tk.Canvas(self.main, width=48, height=48, 
                                   borderwidth=1, highlightthickness=0,
                                   relief="raised")
                if ((x+y)%2 == 0):
                    canvas.configure(bg="pink")

                self.main.create_window(x*50, y*50, anchor="nw", window=canvas)

                # adjust the bindtags of the sub-canvas to include
                # the parent canvas
                #bindtags = list(canvas.bindtags())
                bindtags = list(canvas.bindtags())
                bindtags.insert(1, self.main)
                canvas.bindtags(tuple(bindtags))

                # add a callback for button events on the inner canvas
                canvas.bind("<1>", self.on_sub_click)


    def on_sub_click(self, event):
        print ("sub-canvas binding")
        if event.widget.cget("background") == "pink":
            return "break"

    def on_main_click(self, event):
        print ("main widget binding")

if __name__ == "__main__":
    root = tk.Tk()
    Example(root).pack (fill="both", expand=True)
    root.mainloop()
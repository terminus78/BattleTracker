import math
import tkinter as tk
from tkinter import ttk
from globals import Globals

glbs = Globals()

class EventManager():
    def __init__(self, root):
        self.root = root
        self.moveFlag = False
        
    def rightClickMenu(self, event):
        self.event = event
        self.tokenMenu = tk.Menu(self.root, tearoff=0)
        #self.trigMenu = tk.Menu(self.tokenMenu, tearoff=0)
        self.aoeMenu = tk.Menu(self.tokenMenu, tearoff=0)
        self.tokenMenu.add_command(label="Stats")
        self.tokenMenu.add_command(label="Damage")
        self.tokenMenu.add_command(label="Heal")
        self.tokenMenu.add_separator()
        #self.tokenMenu.add_cascade(label="Trig Functions", menu=self.trigMenu)
        #self.trigMenu.add_command(label="Distance", command=findDistance)
        #self.trigMenu.add_command(label="Find All in Range")
        #self.trigMenu.add_command(label="Spread Width")
        self.tokenMenu.add_cascade(label="AOE", menu=self.aoeMenu)
        self.aoeMenu.add_command(label="Circle")
        self.aoeMenu.add_command(label="Square")
        self.aoeMenu.add_command(label="Cone")
        self.aoeMenu.add_command(label="Line")
        self.aoeMenu.add_command(label="Ring Wall")
        self.aoeMenu.add_command(label="Line Wall")
        try:
            self.tokenMenu.tk_popup(self.event.x_root, self.event.y_root)
        finally:
            self.tokenMenu.grab_release()

    def tokenSelect(self, event, arg):
        print("Called tokenSelect")
        eventInfo = event.widget.grid_info()
        #position = [eventInfo["row"], eventInfo["column"]]
        position = arg[1]
        occupied = False
        glbs.setFoundIndex(0)
        index = glbs.getFoundIndex()
        tokenList = arg[0]
        if self.moveFlag:
            if glbs.getFirstSelected() is None:
                for being in tokenList:
                    if being["coordinate"][0] != "" and being["coordinate"][1] != "":
                        rowPos = int(being["coordinate"][1])
                        colPos = int(being["coordinate"][0])

                        if rowPos == position[0] and colPos == position[1]:
                            glbs.setFirstSelected(being)
                            print(glbs.getFirstSelected())
                            break
                    index += 1
                    glbs.setFoundIndex(index)
            else:
                for being in tokenList:
                    if being["coordinate"][0] != "" and being["coordinate"][1] != "":
                        rowPos = int(being["coordinate"][1])
                        colPos = int(being["coordinate"][0])

                        if rowPos == position[0] and colPos == position[1]:
                            occupied = True
                if not occupied:
                    glbs.setSecondSelected(position)
                    print(glbs.getFirstSelected())

            if glbs.getFirstSelected() is not None and glbs.getSecondSelected() is not None:
                refreshNecessary = True
                self.moveFlag = False
        print(f"Move flag {self.moveFlag}")

    def moveToken(self):
        self.moveFlag = True
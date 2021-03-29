class Globals:
    def __init__(self):
        self.battleWindowOpen = False
        self.statInputWindowOpen = False
        self.refreshNecessary = False
        self.firstSelected = None
        self.secondSelected = None
        self.foundIndex = 0

    def getOpenBattleWin(self):
        return self.battleWindowOpen
    def setOpenBattleWin(self, isOpen):
        self.battleWindowOpen = isOpen

    def getInputWinOpen(self):
        return self.statInputWindowOpen
    def setInputWinOpen(self, isOpen):
        self.statInputWindowOpen = isOpen
    
    def getRefresh(self):
        return self.refreshNecessary
    def setRefresh(self, isNeeded):
        self.refreshNecessary = isNeeded

    def getFirstSelected(self):
        return self.firstSelected
    def setFirstSelected(self, sel):
        self.firstSelected = sel
    
    def getSecondSelected(self):
        return self.secondSelected
    def setSecondSelected(self, sel):
        self.secondSelected = sel

    def getFoundIndex(self):
        return self.foundIndex
    def setFoundIndex(self, index):
        self.foundIndex = index
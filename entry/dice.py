import math
import random


class DiceRoller():
    def __init__(self):
        self.dieOptions = [2, 4, 6, 8, 10, 12, 20, 100]
    
    def roll(self, dieSize=20, numDice=1):
        if dieSize not in self.dieOptions:
            return [0]
        if type(numDice) != int or numDice < 1:
            return [0]
        diceResults = []
        for i in range(numDice):
            rollDie = random.randint(1, dieSize)
            diceResults.append(rollDie)
        return diceResults
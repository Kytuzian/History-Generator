from Tkinter import *

import random

import utility

class Continent:
    def __init__(self, rootCell):
        self.rootCell = rootCell
        self.cells = []
        self.nations = []

    def add_nation(self, nation):
        self.nations.append(nation)

    def add_cell(self, cell):
        self.cells.append(cell)



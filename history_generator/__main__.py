from Tkinter import *
import tkMessageBox

import sys

import internal.gui as gui
import internal.utility as utility

from simulation import Main

class StartUp:
    def __init__(self):
        self.parent = Tk()
        self.parent.title('History Generator')
        self.parent.geometry("450x260+0+0")

        self.parent.config(background='white')

        self.main_label = gui.Label(self.parent, text='History Generator:')
        self.main_label.config(font=(None, 32), fg='#f4ce42')
        self.main_label.pack()

        self.start_new_button = gui.Button(self.parent, text='[S]tart New', command=self.start_new)
        self.start_new_button.pack()

        self.load_var = StringVar()
        self.load_entry = Entry(self.parent, textvariable=self.load_var)
        self.load_entry.pack()
        self.load_button = gui.Button(self.parent, text='[L]oad', command=self.load)
        self.load_button.pack()

        self.archaeology_button = gui.Button(self.parent, text='[A]rchaeology', command=self.archaeology)
        self.archaeology_button.pack()

        self.exit_button = gui.Button(self.parent, text='[E]xit', command=self.parent.destroy)
        self.exit_button.pack()

        # Set up the hot keys
        self.parent.bind('S', lambda _: self.start_new())
        self.parent.bind('s', lambda _: self.start_new())
        self.parent.bind('L', lambda _: self.load())
        self.parent.bind('l', lambda _: self.load())
        self.parent.bind('A', lambda _: self.archaeology())
        self.parent.bind('a', lambda _: self.archaeology())
        self.parent.bind('E', lambda _: self.parent.destroy())
        self.parent.bind('e', lambda _: self.parent.destroy())

        self.parent.mainloop()

    def start_new(self):
        Main().start()

    def load(self):
        Main().load(self.load_var.get())

    def archaeology(self):
        return

# TODO: Improve argument handling (e.g., use argparse)
if len(sys.argv) > 1:
    for arg in sys.argv[1:]:
        params = arg.split('=')

        if params[0] == "width":
            utility.S_WIDTH = int(params[1])
        elif params[0] == "height":
            utility.S_HEIGHT = int(params[1])
        elif params[0] == "size":
            utility.CELL_SIZE = int(params[1])

StartUp()


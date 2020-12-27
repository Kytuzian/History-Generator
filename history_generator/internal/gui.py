import tkinter as tk

# Slightly customized widgets.
# Mostly just making their background white by default.

class Button(tk.Button):
    def __init__(self, parent, **kwargs):
        tk.Button.__init__(self, parent, background='white', **kwargs)

class Label(tk.Label):
    def __init__(self, parent, **kwargs):
        tk.Label.__init__(self, parent, background='white', **kwargs)

class Checkbutton(tk.Checkbutton):
    def __init__(self, parent, **kwargs):
        tk.Checkbutton.__init__(self, parent, background='white', **kwargs)

class Scale(tk.Scale):
    def __init__(self, parent, **kwargs):
        tk.Scale.__init__(self, parent, background='white', **kwargs)


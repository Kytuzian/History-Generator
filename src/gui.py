import Tkinter

# Slightly customized widgets.
# Mostly just making their background white by default.

class Button(Tkinter.Button):
    def __init__(self, parent, **kwargs):
        Tkinter.Button.__init__(self, parent, background='white', **kwargs)

class Label(Tkinter.Label):
    def __init__(self, parent, **kwargs):
        Tkinter.Label.__init__(self, parent, background='white', **kwargs)

class Checkbutton(Tkinter.Checkbutton):
    def __init__(self, parent, **kwargs):
        Tkinter.Checkbutton.__init__(self, parent, background='white', **kwargs)

class Scale(Tkinter.Scale):
    def __init__(self, parent, **kwargs):
        Tkinter.Scale.__init__(self, parent, background='white', **kwargs)

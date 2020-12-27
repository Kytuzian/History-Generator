from tkinter import Tk, Text
from tkinter.constants import W, WORD, END, N, E, S

from internal import gui as gui


class Art:
    def __init__(self, nation, creator, name, subject, category, style, sub_category, content, material, location, gen):
        self.creating_nation = nation
        self.nation = nation
        self.creator = creator

        self.style = style

        self.category = category
        self.sub_category = sub_category

        self.name = name
        self.subject = subject
        self.content = content

        self.material = material

        self.location = None

        self.gen = gen

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('{}'.format(self.name))
        self.gui_window.geometry('700x500+0+0')
        self.gui_window.config(background='white')

        i = 0
        self.title_label = gui.Label(self.gui_window, text='Translated Title: {}'.format(self.subject))
        self.title_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.creator_label = gui.Label(self.gui_window, text='Creator: {}'.format(self.creator.name))
        self.creator_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.creating_nation_label = gui.Label(self.gui_window,
                                               text='Creating Nation: {}'.format(self.creating_nation.name))
        self.creating_nation_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.current_nation_label = gui.Label(self.gui_window, text='Current Nation: {}'.format(self.nation.name))
        self.current_nation_label.grid(row=i, column=0, sticky=W)
        i += 1

        if self.location is None:
            location_name = 'Lost'
        else:
            location_name = self.location.name

        self.location_label = gui.Label(self.gui_window, text='Location: {}'.format(location_name))
        self.location_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.category_label = gui.Label(self.gui_window, text='Category: {}'.format(self.category))
        self.category_label.grid(row=i, column=0, sticky=W)
        i += 1

        if self.category == 'drawing':
            self.sub_category_label = gui.Label(self.gui_window, text='Subcategory: {}'.format(self.sub_category))
            self.sub_category_label.grid(row=i, column=0, sticky=W)
            i += 1

            self.style_label = gui.Label(self.gui_window, text='Style: {}'.format(self.style))
            self.style_label.grid(row=i, column=0, sticky=W)
            i += 1

            self.material_label = gui.Label(self.gui_window, text='Material: {}'.format(self.material))
            self.material_label.grid(row=i, column=0, sticky=W)
            i += 1
        elif self.category == 'statue':
            self.material_label = gui.Label(self.gui_window, text='Material: {}'.format(self.material))
            self.material_label.grid(row=i, column=0, sticky=W)
            i += 1

        self.content_label = gui.Label(self.gui_window, text='Content:')
        self.content_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.content_box = Text(self.gui_window)
        self.content_box.config(wrap=WORD)
        self.content_box.insert(END, self.content)
        self.content_box.grid(row=i, column=0, sticky=N + W + E + S)
        i += 1

    def get_info(self):
        res = {}
        res['creating_nation'] = self.creating_nation.id
        res['nation'] = self.nation.id
        res['creator'] = self.creator.name

        res['style'] = self.style
        res['category'] = self.category
        res['sub_category'] = self.sub_category

        res['name'] = self.name
        res['subject'] = self.subject
        res['content'] = self.content
        res['material'] = self.material

        if self.location is not None:
            res['location'] = self.location.name
        else:
            res['location'] = None

        res['gen'] = self.gen.get_info()

        return res

    def __repr__(self):
        if self.category == 'drawing':
            return '{} ({}) by {}. It is a {} {}, made with {}. {}'.format(self.name, self.subject, self.creator.name,
                                                                           self.sub_category, self.style, self.material,
                                                                           self.content)
        elif self.category == 'statue':
            return '{} ({}) by {}. It is a {}, made of {}. {}'.format(self.name, self.subject, self.creator.name,
                                                                      self.category, self.material, self.content)
        else:
            return '{} ({}) by {}. It is a {}. {}'.format(self.name, self.subject, self.creator.name, self.category,
                                                          self.content)

import re

import events
import gui

from Tkinter import *

class Result:
    def __init__(self, event_list):
        self.event_list = event_list

    def multi_search(self, datums, regexes):
        if len(datums) > 1:
            return self.search(datums[0], regexes[0])
        else:
            return self.search(datums[0], regexes[0]).multi_search(datums[1:], regexes[1:])

    #Only for event data
    def search_or(self, data_names, search_regex=r'.*'):
        results = set()

        for data_name in data_names:
            results = results.union(self.search(data_name, search_regex).event_list)

        return Result(list(results))

    def search(self, data_name, search_regex=r'.*', comp = lambda a, b: a > b, date=(0,)):
        if not data_name in ['name', 'date']:
            return Result(filter(lambda e: data_name in e.event_data and len(re.findall(search_regex, e.event_data[data_name])) > 0, self.event_list))
        elif data_name == 'name':
            return Result(filter(lambda e: len(re.findall(search_regex, e.name)) > 0, self.event_list))
        elif data_name == 'date':
            return Result(filter(lambda e: comp(date, e.date), self.event_list))

    def __repr__(self):
        return str(self.event_list)

class Analyser:
    def __init__(self, event_log=None, fname='event_log.txt'):
        if event_log == None:
            self.event_list = self.load_events(fname)
        else:
            self.event_list = event_log

    #Only for event data
    def search_or(self, data_names, search_regex=r'.*'):
        return Result(self.event_list).search_or(data_names, search_regex)

    def search(self, data_name, search_regex=r'.*', comp = lambda a, b: a > b, date=(0,)):
        return Result(self.event_list).search(data_name, search_regex, comp, date)

    def load_events(self, fname):
        event_list = []

        with open(fname) as f:
            lines = f.read().split('\n')[:-1]
            event_list = map(events.Event.from_str, lines)

        return event_list

class HistoryWindow:
    def __init__(self, title, event_types):
        self.title = title

        self.event_types = event_types
        self.display_event_types = event_types

        self.event_log = Analyser().search('name', '|'.join(self.event_types))

        self.show_information_gui()

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title(self.title)
        self.gui_window.geometry("800x400+0+0")
        self.gui_window.config(background='white')

        self.gui_window.columnconfigure(1, weight=1)
        self.gui_window.rowconfigure(3, weight=1)

        self.event_check_buttons = []

        self.event_check_display = Listbox(self.gui_window, selectmode=MULTIPLE)
        self.event_check_display.bind('<<ListboxSelect>>', self.change_selection)

        for (i, event_type) in enumerate(self.event_types):
            self.event_check_display.insert(END, event_type)

        self.event_check_display.grid(row=0, sticky=W+E)

        self.event_log_display = Listbox(self.gui_window)
        self.event_log_display.grid(row=2, columnspan=2, rowspan=2, sticky=N + S + W + E)

        self.refresh_event_log_display()

    def change_selection(self, event):
        self.refresh_event_log_display()

    def refresh_event_log_display(self):
        self.display_event_types = list([self.event_check_display.get(i) for i in self.event_check_display.curselection()])
        all_events = self.get_sorted_events(self.event_log.search('name', '|'.join(self.display_event_types)))

        self.event_log_display.delete(0, END)
        for event in all_events:
            self.event_log_display.insert(END, event.text_version())

    def get_sorted_events(self, analyser):
        return sorted(analyser.event_list, key=lambda event: event.date)

def find_nation_mentions(name):
    return Analyser().search_or(['nation_a', 'nation_b'], name)

def find_city_mentions(names):
    return Analyser().search_or(['city_a', 'city_b'], '|'.join(names))

def find_religion_mentions(name):
    return Analyser().search_or(['religion_a', 'religion_b'], name)

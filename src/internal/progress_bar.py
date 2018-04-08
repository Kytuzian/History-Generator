from Tkinter import *
import ttk

import time

from internal import utility


def sequence_tasks(tasks, delta=100):
    i = [0]

    def f():
        if i[0] < len(tasks):
            while i[0] < len(tasks) and tasks[i[0]].done():
                i[0] += 1

            if i[0] < len(tasks):
                tasks[i[0]].last_val = tasks[i[0]].f()

        return i[0]

    return Task(f, len(tasks), delta=delta)


def map_task(f, l, delta=100):
    # Because we can't mutate things from inside a closure
    i = [0]

    def new_f():
        if i[0] < len(l):
            f(l[i[0]])
            i[0] += 1

        return i[0]

    return Task(new_f, len(l), delta)


def call_task(f, args, delta=100):
    # Because we can't mutate things from inside a closure
    i = [0]

    def new_f():
        if i[0] == 0:
            f(*args)
            i[0] += 1

        return i[0]

    return Task(new_f, 1, delta)


# If only I could make Task a monoid...
class Task:
    def __init__(self, f, max_val, delta=100):
        self.f = f
        self.max_val = max_val

        self.delta = delta

        self.last_val = 0

    def do_work(self):
        start_time = time.time() * 1000.0

        while time.time() * 1000.0 - start_time < self.delta and not self.done():
            self.last_val = self.f()

        return self.last_val

    def done(self):
        return self.last_val >= self.max_val

    def combine(self, other):
        def new_f():
            if not self.done():
                return self.f()
            else:
                return self.max_val + other.f()

        return Task(new_f, self.max_val + other.max_val)


class ProgressBar:
    def __init__(self, title, task):
        self.parent = Tk()
        self.parent.title(title)
        self.parent.geometry("{}x25+0+0".format(utility.DISPLAY_WIDTH))

        self.parent.config(background='white')

        self.progress_bar = ttk.Progressbar(self.parent, orient='horizontal', length=utility.DISPLAY_WIDTH - 20, mode='determinate')
        self.progress_bar.pack()

        self.progress_bar['maximum'] = task.max_val

        self.title = title
        self.task = task

    def loop(self):
        self.progress_bar['value'] = self.task.do_work()

        if not self.task.done():
            # Give the gui time to update.
            self.parent.after(1, self.loop)
        else:
            self.parent.destroy()

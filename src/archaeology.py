from Tkinter import *

import language
import utility
import gui

class Translation:
    def __init__(self, alien_lang, text_to_translate):
        self.parent = Tk()
        self.parent.title('Archaeology')
        self.parent.geometry('{}x{}+0+0'.format(utility.DISPLAY_WIDTH, utility.DISPLAY_HEIGHT))
        self.parent.config(background='white')

        self.text_to_translate = text_to_translate
        self.alien_lang = alien_lang

        # Create the actual gui
        self.alien_text = gui.Label(self.parent, text=text_to_translate)
        self.alien_text.grid(row=0, column=3, rowspan=6, sticky=W)

        self.english_text = gui.Label(self.parent, text=text_to_translate)
        self.english_text.grid(row=7, column=3, rowspan=6, sticky=W)
        self.alien_var = StringVar()
        self.alien_label = gui.Label(self.parent, text='Alien:')
        self.alien_label.grid(row=0, column=0, sticky=W + S)
        self.alien_box = Entry(self.parent, textvariable=self.alien_var)
        self.alien_box.grid(row=1, column=0, sticky=N)

        self.english_var = StringVar()
        self.english_label = gui.Label(self.parent, text='English:')
        self.english_label.grid(row=0, column=1, sticky=W + S)
        self.english_box = Entry(self.parent, textvariable=self.english_var)
        self.english_box.grid(row=1, column=1, sticky=N)

        self.translate_button = gui.Button(self.parent, text='Translate', command=self.test_translation)
        self.translate_button.grid(row=2, column=0, sticky=N)

        # All of the things we've guessed so far
        self.replacements = {}

        self.refresh_text()

    def test_translation(self):
        self.replacements[self.alien_var.get()] = self.english_var.get()
        self.refresh_text()

    def refresh_text(self):
        # Redo the translations we've tried so far, so we can see what we've got.
        res = self.alien_text['text']
        for rep, repval in self.replacements.iteritems():
            res = res.replace(rep, repval)

        self.english_text['text'] = res

    def start(self):
        self.parent.mainloop()

# base_text = 'text to be translated goes here'
base_text = ''
lang = language.Language()
translated_text = lang.translateTo(base_text)
print(lang.translateFrom(translated_text))

Translation(lang, translated_text).start()

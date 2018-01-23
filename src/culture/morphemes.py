import random

from culture.language import analyze_word


class Morphemes:
    def __init__(self, language):
        self.language = language

        self.morph = {}

    def add(self, name):
        is_morph = random.choice([True, False])
        is_pre = random.choice([True, False])

        self.morph[name] = {}
        self.morph[name]['chars'] = self.language.make_word(3)
        self.morph[name]['is_morph'] = is_morph
        self.morph[name]['is_pre'] = is_pre

    def create_morph(self, word):
        analysis = analyze_word(word)
        res = ''
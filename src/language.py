import utility
from nation import *

import random

from math import *

vowel_sounds = ['ah', 'ae', 'aa', 'uh', 'eh', 'ee', 'ar', 'er', 'ow', 'ih', 'aw', 'oi',
                'oo', 'ou', 'or', 'our', 'i']
consonant_sounds = ['b', 'k', 's', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'ng',
                    'p', 'kw', 'r', 't', 'v', 'w', 'x', 'y', 'z', 'ch', 'sh', 'th']



#Chances (1 in x)
LOSE_PLACE_CITY_NAME = 8 #Only applies if the nation no longer owns the city.
LOSE_NAME_MODIFIER = 30 #Per modifier
GAIN_NAME_MODIFIER = 30 #Per history step

def generate_sound_word(length):
    res = []
    consonants = 0
    for sound in xrange(length):
        l = random.choice([vowel_sounds, consonant_sounds])

        if random.choice([False, True]) or consonants > 1:
            consonants = 0
            res.append(random.choice(vowel_sounds))
        else:
            consonants += 1
            res.append(random.choice(consonant_sounds))
    return '-'.join(res)

# for i in xrange(10):
#     print(generate_sound_word(random.randint(2, 8)))

MODIFIERS = ["Grand", "Federated", "Democratic", "People's", "Free", "Illustrious", "Glorious", "United"]

class NationName:
    def __init__(self, modifiers, government_type, places):
        self.modifiers = modifiers
        self.government_type = government_type
        self.places = places

    def history_step(self, parent):
        parent_cities_names = map(lambda city: city.name, parent.cities)

        for place in self.places:
            #We can't get rid of the last one.
            if not place in parent_cities_names and len(self.places) > 1:
                if random.randint(0, LOSE_PLACE_CITY_NAME) == 0:
                    self.remove_place(place)

        for modifier in self.modifiers:
            if random.randint(0, LOSE_NAME_MODIFIER) == 0:
                self.remove_modifier(modifier)

        if random.randint(0, GAIN_NAME_MODIFIER) == 0:
            self.add_modifier(random.choice(MODIFIERS))

    def add_modifier(self, modifier_name):
        self.modifiers.append(modifier_name)

    def remove_modifier(self, modifier_name):
        self.modifiers.remove(modifier_name)

    def add_place(self, place_name):
        self.places.append(place_name)

    def remove_place(self, place_name):
        self.places.remove(place_name)

    def short_name(self):
        return self.places[0]

    def get_name(self):
        modifier_part = ' '.join(self.modifiers)

        if len(self.places) > 2:
            place_part = '{}, and {}'.format(', '.join(self.places[:-1]), self.places[-1])
        elif len(self.places) == 2:
            place_part = '{} and {}'.format(self.places[0], self.places[1])
        else:
            place_part = self.places[0]

        if len(self.modifiers) > 0:
            return 'The {} {} of {}'.format(modifier_part, self.government_type, place_part)
        else:
            return 'The {} of {}'.format(self.government_type, place_part)

    def __repr__(self):
        return self.get_name()

class Language:
    def __init__(self, name_length=random.randint(4, 10), base_language = None):
        self.letters = []
        self.startLetters = []
        self.endLetters = []
        self.letterSections = []
        self.vowels = []

        self.first_names = []
        self.last_names = []

        self.toDictionary = {}
        self.fromDictionary = {}

        self.vowel_frequency = 0

        self.name_length = name_length

        if base_language != None:
            self.create_from_language(base_language)
        else:
            self.create()

    def __repr__(self):
        print("Letters", self.letters)
        print("Start Letters", self.startLetters)
        print("End Letters", self.endLetters)
        print("Letter Sections", self.letterSections)
        print("Vowels", self.vowels)
        print("Vowel Frequency", self.vowel_frequency)

        return ""

    def create_from_language(self, base_language):
        self.letters = utility.mutate(base_language.letters, 5)

        self.startLetters = utility.mutate(base_language.startLetters, 5, self.chooseFromLetters())
        self.endLetters = utility.mutate(base_language.endLetters, 5, self.chooseFromLetters())

        self.letterSections = utility.mutate(base_language.letterSections, 5, self.chooseLetterSections())

        self.vowels = self.getVowels()

        if self.vowels == []:
            self.vowels = ['a']

        self.vowel_frequency = random.randint(4, 10)

    def create(self):
        self.letters = self.chooseLetters()
        #print("Letters", self.letters)

        self.startLetters = self.chooseFromLetters()
        #print("Start Letters", self.startLetters)
        self.endLetters = self.chooseFromLetters()
        #print("End Letters", self.endLetters)

        self.letterSections = self.chooseLetterSections()
        #print("Letter Sections", self.letterSections)

        self.vowels = self.getVowels()

        if self.vowels == []:
            self.vowels = ['a']
        #print("Vowels", self.vowels)

        self.vowel_frequency = random.randint(4, 10)
        #print("Vowel Frequency", self.vowel_frequency)

    def generate_name(self):
        first_name = ""
        last_name = ""

        if len(self.first_names) == 0:
            self.first_names.append(self.make_word(self.name_length, True))

        if len(self.last_names) == 0:
            self.last_names.append(self.make_word(self.name_length, True))

        if random.randint(0, 10) == 0:
            first_name = self.make_word(self.name_length, True)
            self.first_names.append(first_name)
        else:
            first_name = random.choice(self.first_names)

        if random.randint(0, 10) == 0:
            last_name = self.make_word(self.name_length, True)
            self.last_names.append(last_name)
        else:
            last_name = random.choice(self.last_names)

        return "{0} {1}".format(first_name, last_name)

    def getVowels(self):
        return [i for i in self.letters if i in "aeiouy"]

    def chooseLetters(self):
        letters = "qwertyuiopasdfghjklzxcvbnm"

        letterCount = random.randint(6, 2000)

        result = []

        for i in xrange(letterCount):
            result.append(random.choice(letters))

        return result

    def chooseFromLetters(self):
        count = random.randint(2, int(log(len(self.letters)) / log(1.1)))

        result = []

        for i in xrange(count):
            result.append(random.choice(self.letters))

        return result

    def chooseLetterSections(self):
        count = random.randint(10, 200)

        result = []

        for i in xrange(count):
            sectionLength = random.randint(1, 2)

            section = ""

            for x in xrange(sectionLength):
                section += random.choice(self.letters)

            result.append(section)

        return result

    def make_name_word(self):
        return self.make_word(self.name_length, True)

    def make_word(self, rough_length, capitalize_first_letter=False):
        result = ""

        variance = random.randint(0, rough_length / 2)
        length = random.randint(rough_length - variance, rough_length + variance)

        result += random.choice(self.startLetters)

        for i in xrange(1, length - 1):
            useSection = random.randint(0, 10)

            if useSection > self.vowel_frequency:
                result += random.choice(self.letterSections)
            else:
                result += random.choice(self.vowels)

        if length > 1:
            result += random.choice(self.endLetters)

        if capitalize_first_letter:
            result = result[0].upper() + result[1:]

        return result

    def make_words(self, count):
        result = []

        for i in xrange(count):
            result.append(self.make_word(random.randint(1, 10)))

        return result

    def translateToLanguage(self, otherWord):
        if otherWord in self.toDictionary:
            return self.toDictionary[otherWord]
        elif otherWord in self.firstNames or otherWord in self.middleNames or otherWord in self.lastNames:
            return otherWord
        else:
            result = self.make_word(len(otherWord))

            self.toDictionary[otherWord] = result
            self.fromDictionary[result] = otherWord

            return result

    def translateFromLanguage(self, word):
        if word in self.fromDictionary:
            return self.fromDictionary[word]
        else:
            print("Not a word!")
            return None

    def translateTo(self, sentence):
        sentence = sentence.replace(",", "").replace(".", "").replace("*", "").replace("/", "")
        sentence = sentence.replace("\"", "").replace(":", "").replace("!", "").replace("\\", "")
        sentence = sentence.replace("-", "").replace("?", "").replace("(", "").replace(")", "").lower()

        return self.translate(sentence, self.translateToLanguage)

    def translateFrom(self, sentence):
        return self.translate(sentence, self.translateFromLanguage)

    def translate(self, sentence, f):
        result = ""

        for i in sentence.split():
            result += f(i) + " "

        return result[:-1] + "."

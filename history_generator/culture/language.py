from math import *
import random

import culture.generator as generator

import internal.utility as utility

from culture.morphemes import Morphemes

vowel_sounds = ['ah', 'ae', 'aa', 'uh', 'eh', 'ee', 'ar', 'er', 'ow', 'ih', 'aw', 'oi',
                'oo', 'ou', 'or', 'our', 'i']
consonant_sounds = ['b', 'k', 's', 'd', 'f', 'g', 'h', 'j', 'l', 'm', 'n', 'ng',
                    'p', 'kw', 'r', 't', 'v', 'w', 'x', 'y', 'z', 'ch', 'sh', 'th']

STARTING_NAME_COUNT = 100


def generate_sound_word(length):
    res = []
    consonants = 0
    for sound in range(length):
        l = random.choice([vowel_sounds, consonant_sounds])

        if random.choice([False, True]) or consonants > 1:
            consonants = 0
            res.append(random.choice(vowel_sounds))
        else:
            consonants += 1
            res.append(random.choice(consonant_sounds))
    return '-'.join(res)


class Language:
    def __init__(self, start_words=generator.base_words, name_length=random.randint(4, 10), base_language=None):
        self.letters = []
        self.startLetters = []
        self.endLetters = []
        self.letterSections = []
        self.vowels = []

        self.first_names = []
        self.last_names = []
        self.names = []  # Names for things like gods, cities, things that only have one name

        self.to_dictionary = {}
        self.to_prefix_dictionary = {}
        self.to_suffix_dictionary = {}
        self.from_dictionary = {}
        self.from_prefix_dictionary = {}
        self.from_suffix_dictionary = {}

        self.vowel_frequency = 0

        self.name_length = name_length

        if base_language is not None:
            self.create_from_language(base_language)
        else:
            self.create()

        for i in range(STARTING_NAME_COUNT):
            self.generate_name()

        # Initialize it with all the base words.
        # for word in start_words:
        #     print('{}: {}'.format(word, self.translateTo(word)))

        # Generate morphemes/whether we use morphemes
        self.morph = Morphemes(self)
        self.morph.add('singular')
        self.morph.add('plural')

    def create_from_language(self, base_language):
        self.letters = utility.mutate(base_language.letters, 5)

        self.startLetters = utility.mutate(base_language.startLetters, 5, self.chooseFromLetters())
        self.endLetters = utility.mutate(base_language.endLetters, 5, self.chooseFromLetters())

        self.letterSections = utility.mutate(base_language.letterSections, 5, self.chooseLetterSections())

        self.vowels = self.getVowels()

        if not self.vowels:
            self.vowels = ['a']

        self.vowel_frequency = random.randint(4, 10)

    def create(self):
        self.letters = self.chooseLetters()
        # print("Letters", self.letters)

        self.startLetters = self.chooseFromLetters()
        # print("Start Letters", self.startLetters)
        self.endLetters = self.chooseFromLetters()
        # print("End Letters", self.endLetters)

        self.letterSections = self.chooseLetterSections()
        # print("Letter Sections", self.letterSections)

        self.vowels = self.getVowels()

        if not self.vowels:
            self.vowels = ['a']

        self.vowel_frequency = random.randint(4, 10)

    def generate_name(self):
        first_name = ""
        last_name = ""

        if len(self.first_names) == 0:
            self.first_names.append(self.make_word(self.name_length, True))

        if len(self.last_names) == 0:
            self.last_names.append(self.make_word(self.name_length, True))

        if random.randint(0, 2) == 0:
            first_name = self.make_word(self.name_length, True)
            self.first_names.append(first_name)
        else:
            first_name = random.choice(self.first_names)

        if random.randint(0, 2) == 0:
            last_name = self.make_word(self.name_length, True)
            self.last_names.append(last_name)
        else:
            last_name = random.choice(self.last_names)

        return "{} {}".format(first_name, last_name)

    def getVowels(self):
        return [i for i in self.letters if i in "aeiouy"]

    def chooseLetters(self):
        letters = "qwertyuiopasdfghjklzxcvbnm"

        letterCount = random.randint(6, 1000)

        result = []

        for i in range(letterCount):
            result.append(random.choice(letters))

        return result

    def chooseFromLetters(self):
        count = random.randint(2, int(log(len(self.letters)) / log(1.1)))

        result = []

        for i in range(count):
            result.append(random.choice(self.letters))

        return result

    def chooseLetterSections(self):
        count = random.randint(10, 100)

        result = []

        for i in range(count):
            sectionLength = random.randint(1, 2)

            section = ""

            for x in range(sectionLength):
                section += random.choice(self.letters)

            result.append(section)

        return result

    def make_name_word(self):
        self.names.append(self.make_word(self.name_length, True))
        self.from_dictionary[self.names[-1]] = self.names[-1]
        self.to_dictionary[self.names[-1]] = self.names[-1]

        return self.names[-1]

    def make_word(self, rough_length, capitalize_first_letter=False):
        # To make sure we don't have too many vowels in a row while creating a word.
        def consec_vowels_at_end(word):
            count = 0
            for c in word[::-1]:
                if c in 'aeiouy':
                    count += 1
                else:
                    return count

            return count

        # To make sure we don't have too many consonants in a row while creating a word.
        def consec_consonants_at_end(word):
            count = 0
            for c in word[::-1]:
                if not (c in 'aeiouy'):
                    count += 1
                else:
                    return count

            return count

        result = ""

        variance = random.randint(0, rough_length + 1)
        length = random.randint(rough_length - variance + 1, rough_length + variance + 1)

        if rough_length > 1 and length == 1:
            length = 2

        result += random.choice(self.startLetters)

        while len(result) < length:
            useSection = random.randint(0, 10)

            if (useSection > self.vowel_frequency and consec_consonants_at_end(result) < 3) or (
                    consec_vowels_at_end(result) > 2):
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

        for i in range(count):
            result.append(self.make_word(random.randint(1, 10)))

        return result

    def translateToLanguage(self, other_word):
        if other_word in self.to_dictionary:
            return self.to_dictionary[other_word]
        elif other_word in list(map(lambda i: i.lower(), self.first_names)) or\
             other_word in list(map(lambda i: i.lower(), self.last_names)):
            return other_word
        else:
            # Check for near matches (for example, jump might be in the dictionary, but jumping might not be).
            # This should allow for more sensible plurals and possession.

            for word in self.to_dictionary:
                if other_word.startswith(word):
                    suffix = other_word[len(word):]
                    if not suffix in self.to_suffix_dictionary:
                        self.to_suffix_dictionary[suffix] = self.make_word(len(suffix))

                    return self.to_dictionary[word] + self.to_suffix_dictionary[suffix]
                # elif other_word.endswith(word):
                #     prefix = other_word[:len(other_word) - len(word)]
                #     if not prefix in self.to_prefix_dictionary:
                #         self.to_prefix_dictionary[prefix] = self.make_word(len(prefix))
                #
                #     return self.to_prefix_dictionary[prefix] + self.to_dictionary[word]

            result = self.make_word(len(other_word))

            self.to_dictionary[other_word] = result
            self.from_dictionary[result] = other_word

            return result

    def translateFromLanguage(self, word):
        if word in self.from_dictionary:
            return self.from_dictionary[word]
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

        return result[:-1]


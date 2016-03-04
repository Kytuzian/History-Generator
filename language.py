import utility
from civil import *
from martial import *

from math import *

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

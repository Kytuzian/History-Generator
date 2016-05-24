from Tkinter import *

import random

import re

ART_CATEGORIES = {'artist': ['drawing', 'statue'],
                  'writer': ['play', 'novel', 'essay', 'poem'],
                  'composer': ['song', 'musical'],
                  'philosopher': ['essay']}

# Painting intentionally included twice, because it makes art more likely to be a painting.
ART_STYLES = {'drawing': ['painting', 'painting', 'fresco', 'woodblock print', 'sketch']}
ART_SUBCATEGORIES = {'drawing': ['portrait', 'landscape', 'allegorical', 'abstract']}

ART_MATERIALS = {'painting': ['<paint> on <medium>'],
                 'sketch': ['<sketch> on <medium>'],
                 'statue': ['<material>']}

ART_SUBJECTS = {'landscape': ['<cap><nature>'],
                'portrait': ['<cap><god|notable_person|notable_person_role>'],
                'allegorical': ['<cap><taste|touch|smell|hearing|sight>'],
                'statue': ['<cap><god|animal|notable_person|notable_person_role>'],
                'song': ['<cap><animal|nature|n|god|name|notable_person|notable_person_role>'],
                'musical': ['<Sir,> <name>', 'The <Tale|Story|Song> of <notable_person|god|notable_person_role|place>',
                            'The <Song|Story> of the <cap><animal>',
                            '<name|notable_person|notable_person_role> in <place>',
                            '<name|notable_person|notable_person_role>',
                            'The <cap><n> of <name|notable_person|notable_person_role>'],
                'play': ['The Tale of <notable_person|god|notable_person_role>',
                         'The Story of the <cap><animal>',
                         '<name|notable_person|notable_person_role>',
                         'The <cap><n> of <name|notable_person|notable_person_role|place>'],
                'novel': ['<cap><article> <Tale|Story> of <notable_person|god|notable_person_role|place>',
                          'The Story of the <cap><animal>', '<cap><article> <adj,> <cap><n>',
                          '<cap><article> <gerund,> <cap><n>',
                          '<name|notable_person|notable_person_role>',
                          '<cap><place>',
                          'The <cap><n> of <name|notable_person|notable_person_role>',
                          '<name|notable_person|notable_person_role> with <name|notable_person|notable_person_role>'],
                'essay': ['<On|Concerning> the <cap><animal|nature|philosophy>',
                          'A Critique of <cap><philosophy|art>',
                          '<cap><philosophy> in <cap><art|art_creator|philosophy|art>',
                          '<Defending|Against> <cap><art|art_creator|philosophy>',
                          'The <Rise|Fall> of <cap><philosophy>',
                          'Letter from <place>'],
                'poem': ['<cap><animal|nature>', '<Ode|Song> <on|to> <notable_person|god|place>',
                         '<Ode|Song> <on|to> <article> <animal|nature>'
                         '<cap><gerund> <indef> <cap><n>', '<cap><article> <adj,> <cap><n>',
                         '<name|notable_person|notable_person_role>',
                         'The <cap><n> of <name|notable_person|notable_person_role>']}

# Canvas intentionally included twice, because it makes the medium more likely to be a canvas, which is more accurate
MEDIUMS = ['canvas', 'canvas', 'beaverboard', 'wood', 'paper', 'panel']
PAINTS = ['tempera', 'oil', 'watercolor']
SKETCHING = ['charcoal', 'pencil']

# For statues
MATERIALS = ['marble', 'rock', 'bronze', 'copper', 'tin', 'wood', 'glass']

ANIMALS = ['dog', 'cat', 'bear', 'wolf', 'bird', 'sparrow', 'hawk', 'eagle',
           'tiger', 'lion', 'elephant', 'alligator', 'pig', 'spider', 'ant',
           'bee', 'panther', 'snake', 'crocodile', 'worm', 'fish', 'shark', 'elk',
           'fox', 'squirrel', 'cardinal', 'beetle']
NATURE = ['tree', 'flower', 'rose', 'grass', 'trees', 'stump', 'cactus', 'wind',
          'sky', 'ground', 'earth', 'sun', 'ocean', 'sea', 'lake', 'pond',
          'water', 'mountain', 'cliff', 'shore', 'bay', 'prairie', 'savannah']
PHILOSOPHIES = ['skepticism', 'romanticism', 'modernism', 'stoicism', 'altruism',
                'capitalism', 'socialism']

NOUNS = ['dog', 'cat', 'bear', 'wolf', 'cabinet', 'table', 'paper', 'light',
         'forest', 'trees', 'tree', 'time', 'society', 'bird', 'robin', 'sparrow',
         'snow', 'rain', 'library', 'python', 'sword', 'book', 'emptiness', 'hollowness',
         'chair', 'shirt', 'dress', 'floor', 'bee', 'grapefruit', 'fight', 'battle',
         'art', 'anger', 'joy', 'sadness', 'jealousy',
         'pomegranate', 'clock', 'warrior', 'fighter', 'soldier', 'artist',
         'tailor', 'king', 'queen', 'prince', 'princess', 'duke', 'merchant',
         'beggar', 'craftsman', 'spear', 'dagger', 'cart', 'wagon', 'horse',
         'building', 'tower', 'castle', 'hail', 'water', 'skeptic', 'capital',
         'altruist', 'romantic']
ADJECTIVES = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'white',
              'black', 'fast', 'intelligent', 'blank', 'empty', 'hollow',
              'poetic', 'short', 'tall', 'epic', 'scarlet', 'wide', 'long',
              'narrow', 'grey', 'violet', 'small', 'great', 'strong', 'mighty',
              'romantic', 'social', 'stoic', 'modern', 'jealous']
BASE_VERBS = ['run', 'walk', 'look', 'drop', 'cause', 'rain', 'fly', 'make',
              'precipitate', 'fight', 'take', 'snow',
              'write', 'read', 'talk', 'speak', 'transfix', 'roll']
VERBS = ['runs', 'walks', 'looks', 'drops', 'causes', 'rains', 'flies', 'makes',
         'precipitates', 'fights', 'takes', 'snows',
         'writes', 'reads', 'talks', 'speaks', 'transfixes', 'rolls']
GERUNDS = ['running', 'walking', 'looking', 'causing', 'raining', 'flying', 'making',
           'precipitating', 'writing', 'reading', 'talking', 'speaking', 'rolling',
           'fighting', 'taking', 'snowing']
PAST_PARTICIPLES = ['ran', 'walked', 'looked', 'dropped', 'caused', 'rained', 'flown',
                    'made', 'precipitated', 'wrote', 'read', 'talked', 'spoken', 'rolled',
                    'fought', 'taken', 'snowed']
PREPOSITIONS = ['around', 'in', 'of', 'by', 'under', 'above', 'before', 'at', 'with']

PREPOSITION_FORMS = ['<article> <gerund> <n>', '<article> <n>',
                     '<article> <adj> <n>',
                     '<article> <adj,adj,> <n>',
                     '<article> <n>\'s <adj,> <n>']

BEGINNING_FORMS = ['<article> <adj,adj,gerund> <n> <v,>']

CONJUCTIONS = ['and', 'or', 'while', 'because']

# This order matters.
# Verbs, gerunds, and past participles must be after base verbs, to properly get the -ing suffix.
# Philosophies must be at the end to get the -ism suffix.
base_words = MEDIUMS + PAINTS + SKETCHING + MATERIALS + ANIMALS + NATURE +\
             NOUNS + ADJECTIVES + BASE_VERBS + VERBS + GERUNDS + PAST_PARTICIPLES + PREPOSITIONS +\
             CONJUCTIONS + PHILOSOPHIES

def is_valid(nation):
    def f(choice):
        if choice in ['god', 'notable_person', 'notable_person_role', 'name', 'art',
                 'art_creator']:
            if nation != None:
                if choice in ['art', 'art_creator']:
                    if len(nation.culture.art) == 0:
                        return False
            else:
                return False
        return True
    return f

def gen_form(form, nation=None):
    choiceTags = filter(lambda i: len(i) > 1, map(lambda i: i.split('|'), re.findall(r'<(.*?)>', form)))

    for choice in choiceTags:
        valid_choice = filter(is_valid(nation), choice)
        form = form.replace('|'.join(choice), random.choice(valid_choice), 1)

    selectTags = filter(lambda i: len(i) > 1, map(lambda i: i.split(','), re.findall(r'<(.*?)>', form)))

    for select in selectTags:
        valid_select = filter(is_valid(nation), select)
        search = '<' + ','.join(select) + '>'
        replacement = '<{}>'.format('> <'.join(random.sample(valid_select, random.randint(1, len(valid_select)))))

        form = form.replace(search, replacement, 1)

    form = form.replace('<> ', '')
    form = form.replace('<>', '')

    while '<paint>' in form:
        form = form.replace('<paint>', random.choice(PAINTS), 1)
    while '<medium>' in form:
        form = form.replace('<medium>', random.choice(MEDIUMS), 1)
    while '<sketch>' in form:
        form = form.replace('<sketch>', random.choice(SKETCHING), 1)
    while '<material>' in form:
        form = form.replace('<material>', random.choice(MATERIALS), 1)
    while '<animal>' in form:
        form = form.replace('<animal>', random.choice(ANIMALS), 1)
    while '<nature>' in form:
        form = form.replace('<nature>', random.choice(NATURE), 1)
    while '<philosophy>' in form:
        form = form.replace('<philosophy>', random.choice(PHILOSOPHIES), 1)
    while '<notable_person>' in form:
        if nation != None:
            form = form.replace('<notable_person>', random.choice(nation.notable_people).name, 1)
        else:
            form = form.replace('<notable_person>', '')
    while '<notable_person_role>' in form:
        if nation != None:
            person = random.choice(nation.notable_people)
            form = form.replace('<notable_person_role>', '{} the {}'.format(person.name, person.role), 1)
        else:
            form = form.replace('<notable_person_role>', '')
    while '<god>' in form:
        if nation != None:
            form = form.replace('<god>', random.choice(nation.religion.gods).name, 1)
        else:
            form = form.replace('<god>', '')
    while '<name>' in form:
        if nation != None:
            form = form.replace('<name>', nation.language.generate_name(), 1)
        else:
            form = form.replace('<name>', '')
    while '<art>' in form:
        if nation != None and len(nation.culture.art) > 0:
            form = form.replace('<art>', '\'{}\''.format(random.choice(nation.culture.art).subject), 1)
        else:
            form = form.replace('<art>', '')
    while '<art_creator>' in form:
        if nation != None and len(nation.culture.art) > 0:
            art = random.choice(nation.culture.art)
            form = form.replace('<art_creator>', '{}\'s \'{}\''.format(art.creator.name, art.subject), 1)
        else:
            form = form.replace('<art_creator>', '')
    while '<place>' in form:
        if nation != None:
            form = form.replace('<place>', random.choice(nation.parent.get_all_cities()).name, 1)
        else:
            form = form.replace('<place>', '')
    while '<nation_place>' in form:
        if nation != None:
            form = form.replace('<nation_place>', random.choice(nation.cities).name, 1)
        else:
            form = form.replace('<nation_place>', '')
    while '<n>' in form:
        form = form.replace('<n>', random.choice(NOUNS), 1)
    while '<v>' in form:
        form = form.replace('<v>', random.choice(VERBS), 1)
    while '<prep>' in form:
        form = form.replace('<prep>', random.choice(PREPOSITIONS), 1)
    while '<ppart>' in form:
        form = form.replace('<ppart>', random.choice(PAST_PARTICIPLES), 1)
    while '<gerund>' in form:
        form = form.replace('<gerund>', random.choice(GERUNDS), 1)
    while '<adj>' in form:
        form = form.replace('<adj>', random.choice(ADJECTIVES), 1)
    while True:
        try:
            i = form.index('<article>')

            form = form[:i] + form[i + len('<article>'):]

            article = random.choice(['<indef>', 'the'])

            form = form[:i] + article + form[i:]
        except:
            break
    while True:
        try:
            i = form.index('<indef> ')

            form = form[:i] + form[i + len('<indef> '):]

            if form[i] in 'aeiou':
                article = 'an '
            else:
                article = 'a '

            form = form[:i] + article + form[i:]
        except:
            break
    while True:
        try:
            i = form.index('<cap>')

            form = form[:i] + form[i + len('<cap>'):]
            form = form[:i] + form[i].upper() + form[i + 1:]
        except:
            break

    # Get rid of all of the rest of brackets
    # This is so we can do stuff like <on|off>, and get either on or off
    # despite the fact that neither is a recognized tag
    form = form.replace('<', '')
    form = form.replace('>', '')

    return form

def generate_abstract_subject():
    beginning = gen_form(random.choice(BEGINNING_FORMS))

    prepositions = []

    preposition_count = int(random.random()**6 * 10)

    for i in xrange(preposition_count):
        prep = random.choice(PREPOSITIONS)
        prep_form = gen_form(random.choice(PREPOSITION_FORMS))

        prepositions.append('{} {}'.format(prep, prep_form))

    res = '{} {}'.format(beginning, ' '.join(prepositions))

    if random.randint(0, 8) == 0:
        return '{} {} {}'.format(res, random.choice(CONJUCTIONS), generate_abstract_subject()).replace('  ', ' ')
    else:
        return res.replace('  ', ' ')

def create_art(nation, creator):
    category = random.choice(ART_CATEGORIES[creator.role])

    style = ''
    sub_category = ''
    subject = ''
    material = ''

    if category == 'drawing':
        style = random.choice(ART_STYLES[category])
        sub_category = random.choice(ART_SUBCATEGORIES[category])

        if sub_category == 'abstract':
            subject = generate_abstract_subject()
        else:
            subject = gen_form(random.choice(ART_SUBJECTS[sub_category]), nation=nation)
    else:
        form = random.choice(ART_SUBJECTS[category])
        subject = gen_form(form, nation=nation)
        # print(form, subject)

    if style in ART_MATERIALS:
        material = gen_form(random.choice(ART_MATERIALS[style]), nation=nation)
    elif category in ART_MATERIALS:
        material = gen_form(random.choice(ART_MATERIALS[category]), nation=nation)

    name = nation.language.translateTo(subject)

    return Art(nation, creator, name, subject, category, style, sub_category, material)

class Culture:
    def __init__(self, nation, art=[]):
        self.nation = nation

        self.art = []

        self.art_display = None

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('Culture of {}'.format(self.nation.name))
        self.gui_window.geometry("500x400+0+0")

        self.gui_window.columnconfigure(2, weight=1)

        self.nation_label = Label(self.gui_window, text='Nation:')
        self.nation_label.grid(row=0, column=0)

        self.nation_button = Button(self.gui_window, text=self.nation.name.short_name(), command=self.nation.show_information_gui)
        self.nation_button.grid(row=0, column=1)

        self.art_label = Label(self.gui_window, text='Art:')
        self.art_label.grid(row=1, column=0)

        self.art_display = Listbox(self.gui_window)
        self.art_display.grid(row=2, column=0, columnspan=3, sticky=E+W)

        self.update_art_display()

    def update_art_display(self):
        self.art_display.delete(0, END)
        for art in self.art:
            self.art_display.insert(END, self.art)

    def add_art(self, work):
        self.art.append(work)

        if self.art_display != None:
            self.update_art_display()

class Art:
    def __init__(self, nation, creator, name, subject, category, style, sub_category, material):
        self.nation = nation
        self.creator = creator

        self.style = style

        self.category = category
        self.sub_category = sub_category

        self.name = name

        self.subject = subject

        self.material = material

    def __repr__(self):
        if self.category in ['drawing']:
            return '{} ({}) by {}. It is a {} {}, made with {}.'.format(self.name, self.subject, self.creator.name, self.sub_category, self.style, self.material)
        elif self.category in ['statue']:
            return '{} ({}) by {}. It is a {}, made of {}.'.format(self.name, self.subject, self.creator.name, self.category, self.material)
        elif self.category in ['song', 'musical']:
            return '{} ({}) by {}. It is a {}.'.format(self.name, self.subject, self.creator.name, self.category)
        elif self.category in ['play', 'novel', 'essay', 'poem']:
            return '{} ({}) by {}. It is a {}.'.format(self.name, self.subject, self.creator.name, self.category)

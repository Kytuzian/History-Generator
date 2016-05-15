import random

import re

ART_CATEGORIES = {'artist': ['drawing', 'statue'],
                  'writer': ['play', 'novel', 'essay', 'poem'],
                  'composer': ['song', 'musical']}

# Painting intentionally included twice, because it makes art more likely to be a painting.
ART_STYLES = {'drawing': ['painting', 'painting', 'fresco', 'woodblock print', 'sketch']}
ART_SUBCATEGORIES = {'drawing': ['portrait', 'landscape', 'allegorical', 'abstract']}

ART_SUBJECTS = {'landscape': ['<cap><nature>'],
                'portrait': ['<cap><notable_person>'],
                'allegorical': ['<cap><taste|touch|smell|hearing|sight>'],
                'statue': ['<cap><god|animal|notable_person>'],
                'song': ['Song'],
                'musical': ['Sir <name>', 'The <Tale|Story|Song> of <notable_person|god>', 'The <Song|Story> of the <cap><animal>'],
                'play': ['The Tale of <notable_person|god>', 'The Story of the <cap><animal>'],
                'novel': ['The Tale of <notable_person|god>', 'The Story of the <cap><animal>'],
                'essay': ['<On|Concerning> the <cap><animal|nature|philosophy>', 'A Critique of <cap><philosophy>', 'Defending <cap><philosophy>'],
                'poem': ['<cap><animal|nature>', '<Ode|Song> <on|to> <article> <notable_person|animal|nature|god>', '<cap><gerund> <indef> <n>']}

ANIMALS = ['dog', 'cat', 'bear', 'wolf', 'bird', 'sparrow', 'hawk', 'eagle',
           'tiger', 'lion', 'elephant', 'alligator', 'pig', 'spider', 'ant',
           'bee', 'panther', 'snake', 'crocodile', 'worm', 'fish', 'shark']
NATURE = ['tree', 'flower', 'rose', 'grass', 'trees', 'stump', 'cactus', 'wind',
          'sky', 'ground', 'earth', 'sun']
PHILOSOPHIES = ['skepticism', 'romanticism', 'modernism', 'altruism']

NOUNS = ['dog', 'cat', 'bear', 'wolf', 'cabinet', 'table', 'paper', 'light',
         'forest', 'trees', 'tree', 'time', 'society', 'bird', 'robin', 'sparrow',
         'snow', 'rain', 'library', 'python', 'sword', 'book', 'emptiness', 'hollowness',
         'chair', 'shirt', 'dress', 'floor', 'bee', 'grapefruit',
         'pomegranate', 'clock', 'warrior', 'fighter', 'soldier', 'artist',
         'tailor', 'king', 'queen', 'prince', 'princess', 'duke', 'merchant',
         'beggar', 'craftsman', 'spear', 'dagger', 'cart', 'wagon', 'horse',
         'building', 'tower', 'castle']
ADJECTIVES = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'white',
              'black', 'fast', 'intelligent', 'blank', 'empty', 'hollow',
              'poetic', 'short', 'tall', 'epic', 'scarlet', 'wide', 'long',
              'narrow', 'grey']
VERBS = ['runs', 'walks', 'looks', 'drops', 'causes', 'rains', 'flies', 'makes',
         'precipitates', 'fights',
         'writes', 'reads', 'talks', 'speaks', 'transfixes', 'rolls']
GERUNDS = ['running', 'walking', 'looking', 'causing', 'raining', 'flying', 'making',
           'precipitating', 'writing', 'reading', 'talking', 'speaking', 'rolling',
           'fighting']
PAST_PARTICIPLES = ['ran', 'walked', 'looked', 'dropped', 'caused', 'rained', 'flown',
              'made', 'precipitated', 'wrote', 'read', 'talked', 'spoken', 'rolled',
              'fought']
PREPOSITIONS = ['around', 'in', 'of', 'by', 'under', 'above', 'before', 'at', 'with']

PREPOSITION_FORMS = ['<article> <gerund> <n>', '<article> <n>',
                     '<article> <adj> <n>',
                     '<article> <ppart|gerund> <adj,adj,> <n>',
                     '<article> <n>\'s <n>', '<article> <n>\'s <adj,gerund,ppart> <n>']

BEGINNING_FORMS = ['<article> <adj,adj,gerund> <n> <v,>']

CONJUCTIONS = ['and', 'or', 'while', 'because']

def gen_form(form, nation=None):
    choiceTags = filter(lambda i: len(i) > 1, map(lambda i: i.split('|'), re.findall(r'<(.*?)>', form)))

    for choice in choiceTags:
        form = form.replace('|'.join(choice), random.choice(choice), 1)

    selectTags = filter(lambda i: len(i) > 1, map(lambda i: i.split(','), re.findall(r'<(.*?)>', form)))

    for select in selectTags:
        search = '<' + ','.join(select) + '>'
        replacement = '<{}>'.format('> <'.join(random.sample(select, random.randint(0, len(select)))))

        form = form.replace(search, replacement, 1)

    form = form.replace('<> ', '')
    form = form.replace('<>', '')

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
    while '<n>' in form:
        form = form.replace('<n>', random.choice(NOUNS), 1)
    while '<v>' in form:
        form = form.replace('<v>', random.choice(VERBS), 1)
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

    if category == 'drawing':
        style = random.choice(ART_STYLES[category])
        sub_category = random.choice(ART_SUBCATEGORIES[category])

        if sub_category == 'abstract':
            subject = generate_abstract_subject()
        else:
            subject = gen_form(random.choice(ART_SUBJECTS[sub_category]), nation=nation)
    else:
        subject = gen_form(random.choice(ART_SUBJECTS[category]), nation=nation)

    name = nation.language.translateTo(subject)

    return Art(nation, creator, name, subject, category, style, sub_category)

class Art:
    def __init__(self, nation, creator, name, subject, category, style, sub_category):
        self.nation = nation
        self.creator = creator

        self.style = style

        self.category = category
        self.sub_category = sub_category

        self.name = name

        self.subject = subject

    def __repr__(self):
        if self.category in ['drawing']:
            return '{} ({}) by {}. It is a {} {}.'.format(self.name, self.subject, self.creator.name, self.sub_category, self.style)
        elif self.category in ['statue']:
            return '{} ({}) by {}. This {} is a {}.'.format(self.name, self.subject, self.creator.name, self.category, self.category)
        elif self.category in ['song', 'musical']:
            return '{} ({}) by {}. It is a {}.'.format(self.name, self.subject, self.creator.name, self.category)
        elif self.category in ['play', 'novel', 'essay', 'poem']:
            return '{} ({}) by {}. It is a {}.'.format(self.name, self.subject, self.creator.name, self.category)

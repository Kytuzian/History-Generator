from Tkinter import *

import random
import re

import research
import utility

ART_CATEGORIES = {'artist': ['drawing', 'statue'],
                  'writer': ['play', 'novel', 'essay', 'poem'],
                  'composer': ['song', 'musical'],
                  'philosopher': ['essay'],
                  'historian': ['historical essay', 'history', 'epic'],
                  'scientist': ['scientific essay'],
                  'oracle': ['prophesy']}

# Painting intentionally included multiple times, because it makes art more likely to be a painting.
ART_STYLES = {'drawing': ['painting', 'painting', 'painting', 'fresco', 'woodblock print', 'sketch']}
ART_SUBCATEGORIES = {'drawing': ['portrait', 'landscape', 'allegorical', 'abstract']}

ART_MATERIALS = {'painting': ['<paint> on <medium>'],
                 'woodblock print': ['<paint> on wood'],
                 'fresco': ['<paint> on <medium>'],
                 'sketch': ['<sketch> on <medium>'],
                 'statue': ['<material>']}

ART_SUBJECTS = {'landscape': [[['<cap><nature>'], ['']]],
                'portrait': [[['<cap><<god>|<notable_person>|<notable_person_role>>'], ['']]],
                'allegorical': [[['<Taste|Touch|Smell|Hearing|Sight>'], ['']]],
                'statue': [[['<cap><<god>|<animal>|<notable_person>|<notable_person_role>>'], ['']]],
                'song': [[['<cap><<animal>|<nature>|<n>|<god>|<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'musical': [[['<char_name:(<Sir,> <name>)>'], ['It is a <comedy|tragedy|romance> about <char_name>.']],
                            [['The <Tale|Story|Song> of <<notable_person>|<god>|<notable_person_role>|<place>>'], ['']],
                            [['The <Song|Story> of the <cap><animal>'], ['']],
                            [['<titlecase><<name>|<notable_person>|<notable_person_role>> in <place>'], ['']],
                            [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                            [['The <cap><n> of <titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'play': [[['The Tale of <<notable_person>|<god>|<notable_person_role>>'], ['']],
                         [['The Story of the <cap><animal>'], ['']],
                         [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                         [['The <cap><n> of <<name>|<notable_person>|<notable_person_role>|<place>>'], ['']]],
                'novel': [[['<cap><article><Tale|Story> of <<notable_person>|<god>|<notable_person_role>|<place>>'], ['']],
                          [['The Story of the <cap><animal>'], ['']], [['<cap><article><adj,> <cap><n>'], ['']],
                          [['<cap><article><gerund,> <cap><n>'], ['']],
                          [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                          [['<cap><place>'], ['']],
                          [['The <cap><n> of <<name>|<notable_person>|<notable_person_role>>'], ['']],
                          [['<titlecase><<name>|<notable_person>|<notable_person_role>> with <titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'essay': [[['<On|Concerning> <article><cap><<animal>|<nature>>'], ['']],
                          [['<On|Concerning> <cap><philosophy>'], ['']],
                          [['A Critique of <cap><<philosophy>|<art>>'], ['']],
                          [['<cap><philosophy> in <cap><<art>|<art_creator>|<philosophy>|<art>>'], ['']],
                          [['<Defending|Against> <cap><<art>|<art_creator>|<philosophy>|<art>>'], ['']],
                          [['The <Rise|Fall> of <cap><philosophy>'], ['']],
                          [['Letter from <place>'], ['']]],
                'poem': [[['<cap><animal|nature>'], ['']],
                         [['<Ode|Song> <on|to> <cap><<notable_person>|<god>|<place>>'], ['']],
                         [['<Ode|Song> <on|to> <subject:article><cap><<animal>|<nature>>'], ['It is about <all_lower><subject>.']],
                         [['<cap><gerund>'], ['']],
                         [['<cap><gerund> <indef><cap><n>'], ['']],
                         [['<cap><article><cap><adj,> <cap><n>'], ['']],
                         [['<titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']],
                         [['The <cap><n> of <titlecase><<name>|<notable_person>|<notable_person_role>>'], ['']]],
                'historical essay': [[['<cap><article>History of <<place>|<notable_person>|<notable_person_role>>'], ['']],
                                     [['A Study of <<place>|<notable_person>|<notable_person_role>>'], ['']],
                                     [['<On the|The> Effectiveness of the <chosen_weapon:cap><weapon>'],
                                      ['It states the author\'s opinion that <chosen_weapon> is <|highly|marginally|sort of|very|extremely> <overrated|underappreciated|overused|underused>.',
                                       'It states the author\'s opinion that <chosen_weapon> is <savage|noble|effective|practical|ineffective|useless>.']],
                                     [['<On the|The> Effectiveness of <cap><armor>'], ['']],
                                     [['<Strengths and Weaknesses|Strengths|Weaknesses> of the <chosen_weapon:cap><weapon>'],
                                      ['It <states|says> that the <all_lower><chosen_weapon> <<excels|fails|succeeds> at|performs <poorly|well> when> <attacking|defending>.']],
                                     [['<Strengths and Weaknesses|Strengths|Weaknesses> of <cap><armor>'], ['']]],
                'history': [[['<cap><article>History of <<place>|<notable_person>|<notable_person_role>>'], ['']]],
                'epic': [[['The Epic of <<place>|<notable_person>|<notable_person_role>>'], ['']]],
                'scientific essay': [[['The <self> Experiment'], ['The experiment was <|marginally|sort of|very|extremely> <|un>successful.']],
                                     [['An Inquiry into <cap><scientific_subject>'], ['It goes into great depth discussing the finer points of <0>.']],
                                     [['A Study of <cap><scientific_subject>'], ['']]],
                'prophesy': [[['A <Prophesy|Foretelling> of <prophesy_type:a Good Harvest|a Bad Harvest|Victory|Peace|a War>'],
                              ['It predicts <that <all_lower><prophesy_type> will come|there will be <all_lower><prophesy_type>> in <randint;1;10> years.']],
                             [['<The|A> Prophesy of <chosen_nation:nation>'],
                              ['This prophesy predicts that <chosen_nation> will <fall|gain <|great> glory|achieve peace|go to war> in <randint;5;25> years.']],
                             [['A <Prophesy|Foretelling> of <prophesy_type:Destruction|Armageddon|Judgement|Final Peace>'],
                              ['This prophesy predicts that there will be <all_lower><prophesy_type> in <randint;10;1000> years in the <spring|summer|warm season|fall|autumn|winter|cold season>.',
                               'This prophesy predicts that <all_lower><prophesy_type> will come in <randint;10;1000> years in the <spring|summer|warm season|fall|autumn|winter|cold season>.',
                               'This prophesy predicts that <all_lower><prophesy_type> will come in <randint;10;1000> years.',
                               'This prophesy predicts that there will be <all_lower><prophesy_type> in <randint;10;1000> years.']]]}

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
          'sky', 'ground', 'earth', 'Sun', 'ocean', 'sea', 'lake', 'pond',
          'water', 'mountain', 'cliff', 'shore', 'bay', 'prairie', 'savannah',
          'star']
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
              'romantic', 'social', 'stoic', 'modern', 'jealous', 'quick']
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

PREPOSITION_FORMS = ['<article><gerund> <n>', '<article><n>',
                     '<article><adj> <n>',
                     '<article><adj,adj,> <n>',
                     '<article><n>\'s <adj,> <n>']

BEGINNING_FORMS = ['<article><adj,adj,gerund> <n> <v,>']

CONJUCTIONS = ['and', 'or', 'while', 'because']

SCIENTIFIC_SUBJECTS = ['mechanics', 'optics', 'physics']

COUNTABLE_WORDS = ['canvas', 'beaverboard', 'paper', 'panel', 'oil', 'watercolor', 'pencil',
                   'rock', 'dog', 'cat', 'bear', 'wolf', 'cabinet', 'table', 'light', 'forest',
                   'tree', 'time', 'society', 'bird', 'robin', 'sparrow', 'library', 'python',
                   'hawk', 'eagle', 'tiger', 'lion', 'elephant', 'alligator', 'pig', 'spider', 'ant',
                   'bee', 'panther', 'snake', 'crocodile', 'worm', 'fish', 'shark', 'elk',
                   'fox', 'squirrel', 'cardinal', 'beetle', 'flower', 'rose', 'stump', 'cactus',
                   'star', 'ocean', 'sea', 'lake', 'pond', 'mountain', 'cliff', 'shore', 'bay', 'prairie',
                   'savannah', 'dog', 'cat', 'bear', 'wolf', 'cabinet', 'table', 'paper', 'light',
                   'forest', 'trees', 'tree', 'time', 'society', 'bird', 'robin', 'sparrow',
                   'sword', 'book', 'chair', 'shirt', 'dress', 'floor', 'bee', 'grapefruit',
                   'fight', 'battle', 'art', 'pomegranate', 'clock', 'warrior', 'fighter',
                   'soldier', 'artist', 'tailor', 'king', 'queen', 'prince', 'princess',
                   'duke', 'merchant', 'beggar', 'craftsman', 'spear', 'dagger', 'cart', 'wagon',
                   'horse', 'building', 'tower', 'castle', 'hail', 'water', 'skeptic', 'capital',
                   'altruist', 'romantic']

# This order matters.
# Verbs, gerunds, and past participles must be after base verbs, to properly get the -ing suffix.
# Philosophies must be at the end to get the -ism suffix.
base_words = MEDIUMS + PAINTS + SKETCHING + MATERIALS + ANIMALS + NATURE +\
             NOUNS + ADJECTIVES + BASE_VERBS + VERBS + GERUNDS + PAST_PARTICIPLES + PREPOSITIONS +\
             CONJUCTIONS + PHILOSOPHIES

def is_valid(nation):
    def f(choice):
        if choice in ['<god>', '<notable_person>', '<notable_person_role>', '<name>', '<art>',
                 '<art_creator>', '<battle>']:
            if nation != None:
                if choice in ['art', 'art_creator']:
                    if len(nation.culture.art) == 0:
                        return False
                elif choice == 'battle':
                    if len(nation.parent.battle_history) == 0:
                        return False
            else:
                return False
        return True
    return f

class Form:
    def __init__(self, texts):
        self.tags = {}
        self.chosen_tags = {}

        self.forms = []

        for text_choices in texts:
            self.forms.append([])
            for text in text_choices:
                self.forms[-1].append(self.separate_text(text))

    def copy(self):
        return Form(dict(self.tags), dict(self.chosen_tags), list(self.form))

    def separate_text(self, text):
        current = ''

        new_form = []

        while len(text) > 0:
            start_pos = text.find('<')

            if start_pos == -1:
                new_form.append(text)
                break
            else:
                if start_pos > 0:
                    new_form.append(text[:start_pos])

                level = 1
                end_pos = start_pos + 1
                while end_pos < len(text):
                    if text[end_pos] == '<':
                        level += 1
                    elif text[end_pos] == '>':
                        # If two tags are right next to each other, it will grab both
                        if len(text) > end_pos + 1:
                            if text[end_pos + 1] == '<':
                                level += 1

                                end_pos += 1

                        level -= 1
                        if level == 0:
                            break

                    end_pos += 1

                tag_text = text[start_pos:end_pos + 1]
                tag_name = str(len(self.tags))

                split_tag = tag_text.split(':')

                if len(split_tag) > 1:
                    tag_name = split_tag[0][1:]
                    tag_text = '<' + split_tag[1]

                self.tags[tag_name] = tag_text
                new_form.append('tag:{}'.format(tag_name))

                text = text[end_pos + 1:]

        return new_form

    def generate(self, nation=None, creator=None):
        self.chosen_tags = {}

        actual_forms = map(lambda form_choices: random.choice(form_choices), self.forms)
        self.generate_tags(actual_forms, nation=nation, creator=creator)

        result = []
        for form in actual_forms:
            form_result = ''

            for part in form:
                if part.startswith('tag:'):
                    tag_name = part.split(':')[1]

                    form_result += self.chosen_tags[tag_name]
                else:
                    form_result += part

            form_result = form_result.replace('  ', ' ').strip()

            result.append(form_result)

        return result

    def generate_tags(self, actual_forms, nation=None, creator=None):
        # So that tags are generated in the correct order.
        tag_order = []
        for form in actual_forms:
            for part in form:
                if part.startswith('tag:'):
                    tag_order.append(part.split(':')[1])

        for tag in tag_order:
            base = self.tags[tag]

            # () allow you to name text without using any actual tag
            # For example, <test:(<animal>'s hair)> allows you to give the name 'test' to 'lion's hair'
            while '<(' in base:
                i = base.find('<(')

                # Get the full tag and remove the brackets
                group = utility.get_container(base, '<', '>', i)
                base = base.replace(group, group[2:-2]) # Remove the containing stuff

            # Checks if tags exist. Replaces the tag's text with the first tag that exists. Otherwise replaces it with nothing.
            while '<tagexists' in base:
                i = base.find('<tagexists')
                section = utility.get_container(base, '<', '>', i)
                check_tags = section[1:-1].split(';')[1:]
                replacement = ''

                for tag_name in check_tags:
                    if tag_name in self.chosen_tags:
                        replacement = self.chosen_tags[tag_name]

                base = base.replace(section, replacement)

            while '|' in base:
                start_pos, end_pos = utility.find_container_of(base, '<', '>', '|')
                choice_section = base[start_pos + 1:end_pos]

                choice = utility.separate_container(choice_section, '<', '>', '|')
                valid_choice = filter(is_valid(nation), choice)
                base = base.replace('<' + choice_section + '>', random.choice(valid_choice), 1)

            while ',' in base:
                start_pos, end_pos = utility.find_container_of(base, '<', '>', ',')
                select_section = base[start_pos + 1:end_pos]

                select = utility.separate_container(select_section, '<', '>', ',')
                valid_select = filter(is_valid(nation), select)
                search = '<' + select_section + '>'
                replacement = '<{}>'.format('> <'.join(random.sample(valid_select, random.randint(1, len(valid_select)))))

                base = base.replace(search, replacement)

            base = base.replace('<> ', '')
            base = base.replace('<>', '')

            while '<paint>' in base:
                base = base.replace('<paint>', random.choice(PAINTS), 1)
            while '<medium>' in base:
                base = base.replace('<medium>', random.choice(MEDIUMS), 1)
            while '<sketch>' in base:
                base = base.replace('<sketch>', random.choice(SKETCHING), 1)
            while '<material>' in base:
                base = base.replace('<material>', random.choice(MATERIALS), 1)
            while '<animal>' in base:
                base = base.replace('<animal>', random.choice(ANIMALS), 1)
            while '<nature>' in base:
                base = base.replace('<nature>', random.choice(NATURE), 1)
            while '<philosophy>' in base:
                base = base.replace('<philosophy>', random.choice(PHILOSOPHIES), 1)
            while '<nation>' in base:
                if nation != None:
                    base = base.replace('<nation>', str(random.choice(nation.parent.nations).name), 1)
                else:
                    base = base.replace('<nation>', '')
            while '<notable_person>' in base:
                if nation != None:
                    base = base.replace('<notable_person>', random.choice(nation.notable_people).name, 1)
                else:
                    base = base.replace('<notable_person>', '')
            while '<notable_person_role>' in base:
                if nation != None:
                    person = random.choice(nation.notable_people)
                    base = base.replace('<notable_person_role>', '{} the {}'.format(person.name, person.role), 1)
                else:
                    base = base.replace('<notable_person_role>', '')
            while '<god>' in base:
                if nation != None:
                    base = base.replace('<god>', random.choice(nation.religion.gods).name, 1)
                else:
                    base = base.replace('<god>', '')
            while '<name>' in base:
                if nation != None:
                    base = base.replace('<name>', nation.language.generate_name(), 1)
                else:
                    base = base.replace('<name>', '')
            while '<art>' in base:
                if nation != None and len(nation.culture.art) > 0:
                        base = base.replace('<art>', '\'{}\''.format(random.choice(nation.culture.art).subject), 1)
                else:
                    base = base.replace('<art>', '')
            while '<art_creator>' in base:
                if nation != None and len(nation.culture.art) > 0:
                    art = random.choice(nation.culture.art)
                    base = base.replace('<art_creator>', '{}\'s \'{}\''.format(art.creator.name, art.subject), 1)
                else:
                    base = base.replace('<art_creator>', '')
            while '<place>' in base:
                if nation != None:
                    base = base.replace('<place>', random.choice(nation.parent.get_all_cities()).name, 1)
                else:
                    base = base.replace('<place>', '')
            while '<nation_place>' in base:
                if nation != None:
                    base = base.replace('<nation_place>', random.choice(nation.cities).name, 1)
                else:
                    base = base.replace('<nation_place>', '')
            while '<battle>' in base:
                if nation != None and len(nation.parent.battle_history) > 0:
                        battle = random.choice(nation.parent.battle_history)

                        battle_bases = ['<The Battle of|The Battle for|>{}'.format(battle.location.name)]
                        base = base.replace('<battle>', gen_base(random.choice(battle_bases)), 1)
                else:
                    base = base.replace('<battle>', '')
            while '<weapon>' in base:
                base = base.replace('<weapon>', random.choice(research.weapon_list).name, 1)
            while '<armor>' in base:
                base = base.replace('<armor>', random.choice(research.armor_list).name, 1)
            while '<scientific_subject>' in base:
                base = base.replace('<scientific_subject>', random.choice(SCIENTIFIC_SUBJECTS), 1)
            while '<n>' in base:
                base = base.replace('<n>', random.choice(NOUNS), 1)
            while '<v>' in base:
                base = base.replace('<v>', random.choice(VERBS), 1)
            while '<prep>' in base:
                base = base.replace('<prep>', random.choice(PREPOSITIONS), 1)
            while '<ppart>' in base:
                base = base.replace('<ppart>', random.choice(PAST_PARTICIPLES), 1)
            while '<gerund>' in base:
                base = base.replace('<gerund>', random.choice(GERUNDS), 1)
            while '<adj>' in base:
                base = base.replace('<adj>', random.choice(ADJECTIVES), 1)

            if creator != None:
                base = base.replace('<self>', creator.name)
                base = base.replace('<self_role>', '{} the {}'.format(creator.name, creator.role))

            randoms = re.findall(r'<rand(.*?);(.*?);(.*?)>', base)

            for rand_type, minimum, maximum in randoms:
                if rand_type == 'int':
                    minimum, maximum = int(minimum), int(maximum)
                    res = random.randint(minimum, maximum)
                elif rand_type == 'om': # Float
                    minimum, maximum = float(minimum), float(maximum)
                    res = random.random() * (maximum - minimum) + minimum

                base = base.replace('<rand{};{};{}>'.format(rand_type, minimum, maximum), str(res))

            # So we can access the previously used tags
            remaining_tags = re.findall(r'<(.*?)>', base)

            for check_tag in remaining_tags:
                if check_tag in self.chosen_tags:
                    base = base.replace('<' + check_tag + '>', self.chosen_tags[check_tag])
                elif not check_tag in ['article', 'indef', 'cap', 'lower', 'all_lower', 'titlecase']:
                    # Get rid of all of tags
                    # This is so we can do stuff like <on|off>, and get either on or off, despite the fact that neither is a recognized tag
                    base = base.replace('<' + check_tag + '>', check_tag)

            while True:
                try:
                    i = base.index('<article>')

                    base = base[:i] + base[i + len('<article>'):]

                    next_word = base[i:].split()[0]
                    next_word = re.sub(r'<.*?>', '', next_word)

                    if next_word.lower() in COUNTABLE_WORDS:
                        article = random.choice(['<indef>', 'the '])
                    else:
                        article = 'the '

                    base = base[:i] + article + base[i:]
                except:
                    break
            while True:
                try:
                    i = base.index('<indef>')

                    base = base[:i] + base[i + len('<indef>'):]

                    test = re.sub(r'<.*?>', '', str(base))
                    if test[i].lower() in 'aeiou':
                        article = 'an '
                    else:
                        article = 'a '

                    base = base[:i] + article + base[i:]
                except:
                    break
            while True:
                try:
                    i = base.index('<cap>')

                    base = base[:i] + base[i + len('<cap>'):]

                    test = re.sub(r'<.*?>', '', str(base))
                    base = base[:i] + test[i].upper() + base[i + 1:]
                except:
                    break
            while True:
                try:
                    i = base.index('<lower>')

                    base = base[:i] + base[i + len('<lower>'):]

                    test = re.sub(r'<.*?>', '', str(base))
                    base = base[:i] + test[i].lower() + base[i + 1:]
                except:
                    break
            while True:
                try:
                    i = base.index('<all_lower>')

                    base = base[:i] + base[i + len('<all_lower>'):]

                    test = re.sub(r'<.*?>', '', str(base))
                    base = base[:i] + test[i:].lower()
                except:
                    break
            while True:
                try:
                    i = base.index('<titlecase>')

                    base = base[:i] + base[i + len('<titlecase>'):]

                    test = re.sub(r'<.*?>', '', str(base))
                    base = base[:i] + utility.title_case(test[i:])
                except:
                    break

            base = base.replace('  ', ' ').strip()

            self.chosen_tags[tag] = base

def gen_simple_form(form, nation=None, creator=None):
    gen = Form([form])

    return gen.generate(nation=nation, creator=creator)[0]

def generate_abstract_subject():
    beginning = gen_simple_form(random.choice(BEGINNING_FORMS))

    prepositions = []

    preposition_count = int(random.random()**6 * 10)

    for i in xrange(preposition_count):
        prep = random.choice(PREPOSITIONS)
        prep_form = gen_simple_form(random.choice(PREPOSITION_FORMS))

        prepositions.append('{} {}'.format(prep, prep_form))

    res = '{} {}'.format(beginning, ' '.join(prepositions))

    if random.randint(0, 8) == 0:
        return '{} {} {}'.format(res, random.choice(CONJUCTIONS), generate_abstract_subject()).replace('  ', ' ')
    else:
        return res.replace('  ', ' ').strip()

def create_art(nation, creator):
    category = random.choice(ART_CATEGORIES[creator.role])

    style = ''
    sub_category = ''
    subject = ''
    material = ''
    content = ''

    if category == 'drawing':
        style = random.choice(ART_STYLES[category])
        sub_category = random.choice(ART_SUBCATEGORIES[category])

        if sub_category == 'abstract':
            subject = generate_abstract_subject()
        else:
            gen_forms = random.choice(ART_SUBJECTS[sub_category])
            gen = Form(gen_forms)
            subject, content = gen.generate(nation=nation, creator=creator)
    else:
        forms = list(ART_SUBJECTS[category])
        random.shuffle(forms)

        for gen_forms in forms:
            gen = Form(gen_forms)
            subject, content = gen.generate(nation=nation, creator=creator)

            if subject != None:
                break

    if subject != None:
        if style in ART_MATERIALS:
            material = gen_simple_form(ART_MATERIALS[style], nation=nation, creator=creator)
        elif category in ART_MATERIALS:
            material = gen_simple_form(ART_MATERIALS[category], nation=nation, creator=creator)

        name = utility.titlecase(nation.language.translateTo(subject))

        return Art(nation, creator, name, subject, category, style, sub_category, content, material, None)
    else:
        return None

class Culture:
    def __init__(self, nation, art=[]):
        self.nation = nation

        self.art = []

        self.art_display = None

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('Culture of {}'.format(self.nation.name))
        self.gui_window.geometry("700x750+0+0")

        self.gui_window.columnconfigure(2, weight=1)
        self.gui_window.rowconfigure(2, weight=1)

        self.nation_label = Label(self.gui_window, text='Nation:')
        self.nation_label.grid(row=0, column=0, sticky=W)

        self.nation_button = Button(self.gui_window, text=self.nation.name.short_name(), command=self.nation.show_information_gui)
        self.nation_button.grid(row=0, column=1, sticky=W)

        self.art_label = Label(self.gui_window, text='Art:')
        self.art_label.grid(row=1, column=0, sticky=W)

        self.art_display = Listbox(self.gui_window)
        self.art_display.grid(row=2, column=0, columnspan=3, sticky=N+S+E+W)
        self.art_display.bind('<Double-Button-1>', self.select_art)

        self.update_art_display()

    def select_art(self, event):
        selected_item = self.art_display.get(self.art_display.curselection())
        for art in self.art:
            if '{} ({})'.format(art.name, art.subject) == selected_item:
                art.show_information_gui()
                break

    def update_art_display(self):
        self.art_display.delete(0, END)
        for art in self.art:
            self.art_display.insert(END, '{} ({})'.format(art.name, art.subject))

    def combine(self, other):
        for art in other.art:
            self.add_art(art)

    def add_art(self, work):
        work.nation = self.nation
        self.art.append(work)

class Art:
    def __init__(self, nation, creator, name, subject, category, style, sub_category, content, material, location):
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

    def show_information_gui(self):
        self.gui_window = Tk()
        self.gui_window.title('{}'.format(self.name))
        self.gui_window.geometry('700x500+0+0')

        i = 0
        self.title_label = Label(self.gui_window, text='Translated Title: {}'.format(self.subject))
        self.title_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.creator_label = Label(self.gui_window, text='Creator: {}'.format(self.creator.name))
        self.creator_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.creating_nation_label = Label(self.gui_window, text='Creating Nation: {}'.format(self.creating_nation.name))
        self.creating_nation_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.current_nation_label = Label(self.gui_window, text='Current Nation: {}'.format(self.nation.name))
        self.current_nation_label.grid(row=i, column=0, sticky=W)
        i += 1

        if self.location == None:
            location_name = 'Lost'
        else:
            location_name = self.location.name

        self.location_label = Label(self.gui_window, text='Location: {}'.format(location_name))
        self.location_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.category_label = Label(self.gui_window, text='Category: {}'.format(self.category))
        self.category_label.grid(row=i, column=0, sticky=W)
        i += 1

        if self.category == 'drawing':
            self.sub_category_label = Label(self.gui_window, text='Subcategory: {}'.format(self.sub_category))
            self.sub_category_label.grid(row=i, column=0, sticky=W)
            i += 1

            self.style_label = Label(self.gui_window, text='Style: {}'.format(self.style))
            self.style_label.grid(row=i, column=0, sticky=W)
            i += 1

            self.material_label = Label(self.gui_window, text='Material: {}'.format(self.material))
            self.material_label.grid(row=i, column=0, sticky=W)
            i += 1
        elif self.category == 'statue':
            self.material_label = Label(self.gui_window, text='Material: {}'.format(self.material))
            self.material_label.grid(row=i, column=0, sticky=W)
            i += 1

        self.content_label = Label(self.gui_window, text='Content:')
        self.content_label.grid(row=i, column=0, sticky=W)
        i += 1

        self.content_box = Text(self.gui_window)
        self.content_box.config(wrap=WORD)
        self.content_box.insert(END, self.content)
        self.content_box.grid(row=i, column=0, sticky=N+W+E+S)
        i += 1

    def __repr__(self):
        if self.category == 'drawing':
            return '{} ({}) by {}. It is a {} {}, made with {}. {}'.format(self.name, self.subject, self.creator.name, self.sub_category, self.style, self.material, self.content)
        elif self.category == 'statue':
            return '{} ({}) by {}. It is a {}, made of {}. {}'.format(self.name, self.subject, self.creator.name, self.category, self.material, self.content)
        else:
            return '{} ({}) by {}. It is a {}. {}'.format(self.name, self.subject, self.creator.name, self.category, self.content)

if __name__ == '__main__':
    a = Form([['<cap><philosophy> in <cap><<art>|<art_creator>|<philosophy>|<art>>'], ['']])
    print(a.generate())

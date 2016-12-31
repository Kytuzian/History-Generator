import re
import random

import research
import utility

# Canvas intentionally included twice, because it makes the medium more likely to be a canvas, which is more accurate
MEDIUMS = ['canvas', 'canvas', 'beaverboard', 'wood', 'paper', 'panel']
PAINTS = ['tempera', 'oil', 'watercolor']
SKETCHING = ['charcoal', 'pencil']

# For statues
MATERIALS = ['marble', 'rock', 'bronze', 'copper', 'tin', 'wood', 'glass']
ANIMALS = ['dog', 'cat', 'bear', 'wolf', 'bird', 'sparrow', 'hawk', 'eagle',
           'tiger', 'lion', 'elephant', 'alligator', 'pig', 'spider', 'ant',
           'bee', 'panther', 'snake', 'crocodile', 'worm', 'fish', 'shark', 'elk',
           'fox', 'squirrel', 'cardinal', 'beetle', 'goose', 'ox', 'mouse', 'owl',
           'moose']
NATURE = ['tree', 'flower', 'rose', 'grass', 'stump', 'cactus', 'wind',
          'sky', 'ground', 'earth', 'Sun', 'ocean', 'sea', 'lake', 'pond',
          'water', 'mountain', 'cliff', 'shore', 'bay', 'prairie', 'savannah',
          'star', 'river', 'creek']

PHILOSOPHIES = ['skepticism', 'romanticism', 'modernism', 'stoicism', 'altruism',
                'capitalism', 'socialism', 'animism', 'cynicism', 'pacifism',
                'idealism', 'utilitarianism']

COLORS = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'white',
          'black', 'scarlet', 'gold', 'navy', 'periwinkle', 'peridot', 'violet',
          'grey', 'chartreuse', 'indigo', 'sky blue']

FLOWERS = ['rose', 'daffodil', '']

NOUNS = ['dog', 'cat', 'bear', 'wolf', 'cabinet', 'table', 'paper', 'light',
         'forest', 'tree', 'time', 'society', 'bird', 'robin', 'sparrow',
         'snow', 'rain', 'library', 'python', 'sword', 'book', 'emptiness', 'hollowness',
         'chair', 'shirt', 'dress', 'floor', 'bee', 'grapefruit', 'fight', 'battle',
         'art', 'anger', 'joy', 'sadness', 'jealousy', 'mouse', 'philosophy',
         'pomegranate', 'clock', 'warrior', 'fighter', 'soldier', 'artist',
         'tailor', 'king', 'queen', 'prince', 'princess', 'duke', 'merchant',
         'beggar', 'craftsman', 'spear', 'dagger', 'cart', 'wagon', 'horse',
         'building', 'tower', 'castle', 'hail', 'water', 'skeptic', 'capital',
         'altruist', 'romantic', 'goose', 'ox', 'mouse', 'owl', 'skepticism', 'romanticism',
         'modernism', 'stoicism', 'altruism', 'capitalism', 'socialism',
         'animism', 'cynicism', 'pacifism', 'idealism', 'pacfist', 'utilitarianism']
ADJECTIVES = ['red', 'blue', 'green', 'yellow', 'orange', 'purple', 'white',
              'black', 'fast', 'intelligent', 'blank', 'empty', 'hollow',
              'poetic', 'short', 'tall', 'epic', 'scarlet', 'wide', 'long',
              'narrow', 'grey', 'violet', 'small', 'great', 'strong', 'mighty',
              'romantic', 'social', 'stoic', 'modern', 'jealous', 'quick',
              'devious', 'mischievous', 'noble', 'smart', 'scarlet', 'gold', 'navy',
              'periwinkle', 'peridot', 'violet', 'grey', 'chartreuse', 'indigo', 'sky blue']
VERBS = ['run', 'walk', 'look', 'drop', 'cause', 'rain', 'fly', 'make',
              'precipitate', 'fight', 'take', 'snow',
              'write', 'read', 'talk', 'speak', 'transfix', 'roll']
PREPOSITIONS = ['around', 'in', 'of', 'by', 'under', 'above', 'before', 'at', 'with']

PREPOSITION_FORMS = ['<article><gerund> <n>', '<article><n>',
                     '<article><adj> <n>',
                     '<article><adj,adj,> <n>',
                     '<article><n>\'s <adj,> <n>']

BEGINNING_FORMS = ['<article><adj,adj,gerund> <n> <v,>']

CONJUCTIONS = ['and', 'or', 'while', 'because', 'but']

SCIENTIFIC_SUBJECTS = ['mechanics', 'optics', 'physics', 'biology', 'chemistry',
                       'geology']

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
                   'altruist', 'romantic', 'dagger', 'rondel', 'dirk', 'kopis', 'shortsword', 'club', 'hammer',
                   'mace', 'axe', 'morning star', 'sword', 'bastard sword', 'claymore', 'bill', 'flail',
                   'falx', 'polehammer', 'staff', 'spear', 'pike', 'sarissa', 'sling', 'javelin', 'bow',
                   'atlatl', 'shortbow', 'longbow', 'crossbow', 'sling staff', 'goose', 'ox', 'mouse', 'owl',
                   'moose', 'pacifist', 'river', 'creek']

IRREGULAR_PLURALS = {'goose': 'geese',
                     'ox': 'oxen',
                     'mouse': 'mice',
                     'moose': 'moose'}

# Any of the irregular forms should be include in the following format:
# 'person(s);tense(s);number(s)': 'form' OR 'type': 'form'
# e.g. '1,2,3;pres;pl': 'run' OR 'all;pres;pl': 'run'
# e.g. 'gerund': 'running' OR 'infinitive': 'to run'
# Only specify the ones that need specification
IRREGULAR_VERBS = {'run': {'all;past;all': 'ran'}}

# This order matters.
# Verbs, gerunds, and past participles must be after base verbs, to properly get the -ing suffix.
# Philosophies must be at the end to get the -ism suffix.
base_words = MEDIUMS + PAINTS + SKETCHING + MATERIALS + ANIMALS + NATURE +\
             NOUNS + ADJECTIVES + VERBS + PREPOSITIONS +\
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
    def __init__(self, texts, custom_tags={}, custom_weights={}):
        self.tags = {}
        self.chosen_tags = {}

        self.custom_tags = custom_tags
        self.custom_weights = dict(custom_weights)

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
                continue_until_space = False

                while end_pos < len(text):
                    if text[end_pos] == '<':
                        level += 1
                    elif text[end_pos] == ' ':
                        if continue_until_space and level == 0:
                            end_pos -= 1
                            break
                    elif text[end_pos] == '>':
                        level -= 1
                        if level == 0:
                            # If two tags are right next to each other, it will grab both
                            if len(text) > end_pos + 1:
                                if text[end_pos + 1] == '<':
                                    level += 1

                                    end_pos += 1
                                elif not text[end_pos + 1] in '.,?!|; ':
                                    continue_until_space = True
                                else:
                                    break
                            else:
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

    def do_conjugate(self, verb, person, tense, number):
        if verb in IRREGULAR_VERBS:
            for conj in IRREGULAR_VERBS[verb]:
                conj_person, conj_tense, conj_number = conj.split(';')

                if conj_person == 'all' or person in conj_person.split(','):
                    if conj_tense == 'all' or tense in conj_tense.split(','):
                        if conj_number == 'all' or number in conj_number.split(','):
                            return IRREGULAR_VERBS[verb][conj]

        # Handle regular verbs
        if tense == 'pres':
            if number == 'pl' or person == '2': # Second person is always plural because English
                return verb
            else:
                return verb + 's'
        elif tense == 'past':
            return verb + 'ed'
        elif tense == 'future':
            return 'will ' + verb

    def do_conjugate_type(self, verb, conj_type):
        if verb in IRREGULAR_VERBS:
            if conj_type in IRREGULAR_VERBS[verb]:
                return IRREGULAR_VERBS[verb][conj_type]

        if conj_type == 'gerund':
            if len(verb) >= 3:
                if not verb[-1] in 'aeiou' and verb[-2] in 'aeiou' and not verb[-3] in 'aeiou':
                    return verb + verb[-1] + 'ing'
                else:
                    return verb + 'ing'
            else:
                return verb + 'ing'
        elif conj_type == 'infintive':
            return 'to ' + verb

    # A replacement for random.choice, so we can keep track of what we chose and use it to
    def choice(self, options, amount=1):
        def weight(_, v):
            if v in self.custom_weights:
                return self.custom_weights[v]
            else:
                return 1

        converted = {}
        for i in xrange(len(options)):
            if isinstance(options[i], list):
                converted[utility.tuplize(options[i])] = options[i]
                options[i] = utility.tuplize(options[i])

        chosen_item = utility.weighted_random_choice(options, weight=weight)

        if chosen_item in self.custom_weights:
            self.custom_weights[chosen_item] += amount
        else:
            self.custom_weights[chosen_item] = 1 + amount

        if chosen_item in converted:
            return converted[chosen_item]
        else:
            return chosen_item

    def generate(self, nation=None, creator=None):
        self.chosen_tags = {}

        actual_forms = map(lambda form_choices: self.choice(form_choices), self.forms)
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

            # () allow you to group text without using any actual tag
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

                base = base.replace('<' + choice_section + '>', self.choice(valid_choice), 1)

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
                base = base.replace('<paint>', self.choice(PAINTS), 1)
            while '<medium>' in base:
                base = base.replace('<medium>', self.choice(MEDIUMS), 1)
            while '<sketch>' in base:
                base = base.replace('<sketch>', self.choice(SKETCHING), 1)
            while '<material>' in base:
                base = base.replace('<material>', self.choice(MATERIALS), 1)
            while '<animal>' in base:
                base = base.replace('<animal>', self.choice(ANIMALS), 1)
            while '<nature>' in base:
                base = base.replace('<nature>', self.choice(NATURE), 1)
            while '<philosophy>' in base:
                base = base.replace('<philosophy>', self.choice(PHILOSOPHIES), 1)
            while '<nation>' in base:
                if nation != None:
                    base = base.replace('<nation>', str(self.choice(nation.parent.nations).name), 1)
                else:
                    base = base.replace('<nation>', '')
            while '<notable_person>' in base:
                if nation != None:
                    base = base.replace('<notable_person>', self.choice(nation.notable_people).name, 1)
                else:
                    base = base.replace('<notable_person>', '')
            while '<notable_person_role>' in base:
                if nation != None:
                    person = self.choice(nation.notable_people)
                    base = base.replace('<notable_person_role>', '{} the {}'.format(person.name, person.periods[-1].role), 1)
                else:
                    base = base.replace('<notable_person_role>', '')
            while '<god>' in base:
                if nation != None:
                    religion_populations = nation.get_nation_religion_populations()
                    if len(religion_populations) > 0:
                        religion,_ = utility.weighted_random_choice(religion_populations, weight=lambda i,(_,adherents): adherents)
                        base = base.replace('<god>', self.choice(religion.gods).name, 1)
                    else:
                        base = base.replace('<god>', '')
                else:
                    base = base.replace('<god>', '')
            while '<name>' in base:
                if nation != None:
                    base = base.replace('<name>', nation.language.generate_name(), 1)
                else:
                    base = base.replace('<name>', '')
            while '<art>' in base:
                if nation != None and len(nation.culture.art) > 0:
                    base = base.replace('<art>', '\'{}\''.format(self.choice(nation.culture.art).subject), 1)
                else:
                    base = base.replace('<art>', '')
            while '<art_creator>' in base:
                if nation != None and len(nation.culture.art) > 0:
                    art = self.choice(nation.culture.art)
                    base = base.replace('<art_creator>', '{}\'s \'{}\''.format(art.creator.name, art.subject), 1)
                else:
                    base = base.replace('<art_creator>', '')
            while '<place>' in base:
                if nation != None and len(nation.parent.get_all_cities()) > 0:
                    base = base.replace('<place>', self.choice(nation.parent.get_all_cities()).name, 1)
                else:
                    base = base.replace('<place>', '')
            while '<nation_place>' in base:
                if nation != None and len(nation.cities) > 0:
                    base = base.replace('<nation_place>', self.choice(nation.cities).name, 1)
                else:
                    base = base.replace('<nation_place>', '')
            while '<battle>' in base:
                if nation != None and len(nation.parent.battle_history) > 0:
                    battle = self.choice(nation.parent.battle_history)

                    battle_bases = ['<The Battle of|The Battle for|>{}'.format(battle.location.name)]
                    base = base.replace('<battle>', gen_simple_form(self.choice(battle_bases)), 1)
                else:
                    base = base.replace('<battle>', '')
            while '<treaty>' in base:
                if nation != None and len(nation.parent.treaties) > 0:
                    treaty = self.choice(nation.parent.treaties).get_treaty_name(nation.parent.get_current_date(), nation)
                    base = base.replace('<treaty>', treaty)
                else:
                    base = base.replace('<treaty>', '')
            while '<nation_treaty>' in base:
                if nation != None and len(nation.treaties) > 0:
                    treaty = self.choice(nation.treaties).get_treaty_name(nation.parent.get_current_date(), nation)
                    base = base.replace('<nation_treaty>', treaty)
                else:
                    base = base.replace('<nation_treaty>', '')
            while '<weapon>' in base:
                base = base.replace('<weapon>', self.choice(research.weapon_list).name, 1)
            while '<armor>' in base:
                base = base.replace('<armor>', self.choice(research.armor_list).name, 1)
            while '<color>' in base:
                base = base.replace('<color>', self.choice(COLORS), 1)
            while '<flower>' in base:
                base = base.replace('<flower>', self.choice(FLOWERS), 1)
            while '<scientific_subject>' in base:
                base = base.replace('<scientific_subject>', self.choice(SCIENTIFIC_SUBJECTS), 1)
            while '<n>' in base:
                base = base.replace('<n>', self.choice(NOUNS), 1)
            while '<v>' in base:
                base = base.replace('<v>', self.choice(VERBS), 1)
            while '<prep>' in base:
                base = base.replace('<prep>', self.choice(PREPOSITIONS), 1)
            while '<adj>' in base:
                base = base.replace('<adj>', self.choice(ADJECTIVES), 1)

            if creator != None:
                if '<self>' in base:
                    base = base.replace('<self>', creator.name)
                if '<self_role>' in base:
                    base = base.replace('<self_role>', '{} the {}'.format(creator.name, creator.periods[-1].role))

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
                elif check_tag in self.custom_tags:
                    base = base.replace('<' + check_tag + '>', self.choice(self.custom_tags[check_tag]))

            while True:
                try:
                    i = base.index('<article>')

                    base = base[:i] + base[i + len('<article>'):]

                    next_word = re.sub(r'<.*?>', '', base)

                    article = 'the '
                    for word in COUNTABLE_WORDS:
                        if next_word.startswith(word):
                            article = random.choice(['<indef>', 'the '])
                            break

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
                    base = base[:i] + utility.titlecase(test[i:])
                except:
                    break
            while True:
                try:
                    i = base.index('<pl>')

                    base = base[:i] + base[i + len('<pl>'):]

                    test = re.sub(r'<.*?>', '', str(base[i:]))
                    words = test.split()
                    if len(words) > 0:
                        next_word = words[0]
                        if next_word in COUNTABLE_WORDS:
                            if next_word in irregular_plurals:
                                pluralized = irregular_plurals[next_word]
                            else:
                                pluralized = str(next_word)
                                if next_word.endswith('s') or next_word.endswith('x') or next_word.endswith('ch') or next_word.endswith('sh'):
                                    pluralized += 'es'
                                elif next_word.endswith('y'):
                                    pluralized = pluralized[:-1] + 'ies'
                                else:
                                    pluralized += 's'

                            base = base.replace(next_word, pluralized)
                except:
                    break

            conjugate = re.findall(r'<conj;(.*?);(.*?);(.*?);(.*?)>', base)

            for person, tense, number, verb in conjugate:
                conjugated = self.do_conjugate(verb, person, tense, number)

                base = base.replace('<conj;{};{};{};{}>'.format(person, tense, number, verb), conjugated)

            conjugate = re.findall(r'<conj;(.*?);(.*?)>', base)
            for conj_type, verb in conjugate:
                conjugated = self.do_conjugate_type(verb, conj_type)

                base = base.replace('<conj;{};{}>'.format(conj_type, verb), conjugated)

            base = base.replace('  ', ' ').strip()

            self.chosen_tags[tag] = base

def gen_simple_form(form, nation=None, creator=None, custom_tags={}, custom_weights={}):
    gen = Form([[form]], custom_tags=custom_tags, custom_weights=custom_weights)

    return gen.generate(nation=nation, creator=creator)[0]

if __name__ == '__main__':
    a = Form([['<pl>goose']])
    print(a.generate())

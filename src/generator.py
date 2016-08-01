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
           'fox', 'squirrel', 'cardinal', 'beetle']
NATURE = ['tree', 'flower', 'rose', 'grass', 'stump', 'cactus', 'wind',
          'sky', 'ground', 'earth', 'Sun', 'ocean', 'sea', 'lake', 'pond',
          'water', 'mountain', 'cliff', 'shore', 'bay', 'prairie', 'savannah',
          'star']
PHILOSOPHIES = ['skepticism', 'romanticism', 'modernism', 'stoicism', 'altruism',
                'capitalism', 'socialism']

NOUNS = ['dog', 'cat', 'bear', 'wolf', 'cabinet', 'table', 'paper', 'light',
         'forest', 'tree', 'time', 'society', 'bird', 'robin', 'sparrow',
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
                   'altruist', 'romantic', 'dagger', 'rondel', 'dirk', 'kopis', 'shortsword', 'club', 'hammer',
                   'mace', 'axe', 'morning star', 'sword', 'bastard sword', 'claymore', 'bill', 'flail',
                   'falx', 'polehammer', 'staff', 'spear', 'pike', 'sarissa', 'sling', 'javelin', 'bow',
                   'atlatl', 'shortbow', 'longbow', 'crossbow', 'sling staff']

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
    def __init__(self, texts, custom_tags={}):
        self.tags = {}
        self.chosen_tags = {}

        self.custom_tags = custom_tags

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
                    base = base.replace('<battle>', gen_simple_form(random.choice(battle_bases)), 1)
                else:
                    base = base.replace('<battle>', '')
            while '<treaty>' in base:
                if nation != None and len(nation.parent.treaties) > 0:
                    treaty = random.choice(nation.parent.treaties).get_treaty_name(nation.parent.get_current_date(), nation)
                    base = base.replace('<treaty>', treaty)
                else:
                    base = base.replace('<treaty>', '')
            while '<nation_treaty>' in base:
                if nation != None and len(nation.treaties) > 0:
                    treaty = random.choice(nation.treaties).get_treaty_name(nation.parent.get_current_date(), nation)
                    base = base.replace('<nation_treaty>', treaty)
                else:
                    base = base.replace('<nation_treaty>', '')
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
                elif check_tag in self.custom_tags:
                    base = base.replace('<' + check_tag + '>', random.choice(self.custom_tags[check_tag]))
                elif not check_tag in ['article', 'indef', 'cap', 'lower', 'all_lower', 'titlecase', 'pl']:
                    # Get rid of all of tags
                    # This is so we can do stuff like <on|off>, and get either on or off, despite the fact that neither is a recognized tag
                    base = base.replace('<' + check_tag + '>', check_tag)

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

            base = base.replace('  ', ' ').strip()

            self.chosen_tags[tag] = base

def gen_simple_form(form, nation=None, creator=None, custom_tags={}):
    gen = Form([form], custom_tags=custom_tags)

    return gen.generate(nation=nation, creator=creator)[0]

if __name__ == '__main__':
    a = Form([['<On the|The> Effectiveness of <armor_type:cap><armor>'],
     ['<This|The> <essay|paper> <<discusses|talks about> the <strengths|weaknesses> of <all_lower><armor_type>.|<states|says> that <all_lower><armor_type> is <exceedingly|extremely|barely|adequately|sort of|very> <useful|useless|effective|ineffective>.>']])
    print(a.generate())

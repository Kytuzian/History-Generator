from culture.form import Form

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

CONJUNCTIONS = ['and', 'or', 'while', 'because', 'but']

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
base_words = MEDIUMS + PAINTS + SKETCHING + MATERIALS + ANIMALS + NATURE + \
             NOUNS + ADJECTIVES + VERBS + PREPOSITIONS + \
             CONJUNCTIONS + PHILOSOPHIES


def is_valid(nation):
    def f(choice):
        if choice in ['<god>', '<notable_person>', '<notable_person_role>', '<name>', '<art>',
                      '<art_creator>', '<battle>']:
            if nation is not None:
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


def gen_simple_form(form, nation=None, creator=None, custom_tags=None, custom_weights=None):
    if custom_tags is None:
        custom_tags = {}
    if custom_weights is None:
        custom_weights = {}
    gen = Form([[form]], custom_tags=custom_tags, custom_weights=custom_weights)

    return gen.generate(nation=nation, creator=creator)[0]

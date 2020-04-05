import random

import internal.utility as utility

from internal import events as events

IMPORTANCE_CHANGE_CHANCE = 30  # In percent
IMPORTANCE_CHANGE_AMOUNT = 2

# in percent
DOMAIN_GAIN_CHANCE = 1
DOMAIN_LOSE_CHANCE = 1

MAX_DOMAIN_COUNT = 5


MAX_IMPORTANCE = 10
TOLERANCE_MULTIPLIER = 1


INTOLERANT_DOMAINS = ['war', 'fire', 'death', 'lightning', 'thunder',
                      'wind', 'chaos', 'the underworld',  # Kenny - Addition
                      'blight', 'disease', 'conquest', 'sacrifice',
                      'lust', 'revenge', 'gluttony', 'envy', 'wrath',
                      'xenophobia', 'zeal', 'apathy'
                      ]
TOLERANT_DOMAINS = ['peace', 'wisdom', 'children', 'knowledge',
                    'writing', 'music', 'storytelling', 'friendship',
                    'the hearth', 'unity',  # Kenny - Addition
                    'piety', 'charity', 'books', 'writing',
                    'tales', 'mastery', 'observations', 'understanding',
                    'morale', 'fervor', 'keen', 'passion'
                    ]

DOMAINS = {'fire': {'general': 0.5},
           'wind': {'artist': 1},
           'water': {'artist': 1},
           'air': {'artist': 1},
           'lightning': {'artist': 1},
           'death': {'general': 0.5},
           'children': {},
           'fertility': {},
           'harvest': {'administrator': 1},
           'wisdom': {'oracle': 1, 'scientist': 1, 'historian': 1, 'philosopher': 1},
           'war': {'general': 1},
           'smithing': {},
           'animals': {'artist': 1},
           'earth': {'artist': 1},
           'rivers': {'artist': 1},
           'peace': {'administrator': 1},
           'knowledge': {'historian': 1, 'scientist': 1},
           'writing': {'writer': 1, 'historian': 1, 'philosopher': 1},
           'music': {'composer': 1},
           'storytelling': {'writer': 1, 'oracle': 1, 'hero': 1},
           'luck': {},
           'thunder': {'artist': 1},
           'friendship': {},
           'wine': {},
           'weaving': {'seneschal': 1},
           'the sun': {},
           'the hearth': {},
           'the moon': {},
           'the sky': {},
           'messenger': {},
           'chaos': {'revolutionary': 1},
           'unity': {'drillmaster': 1, 'quartermaster': 1},
           'the underworld': {'conqueror': 1},
           'creation': {'emperor': 1},
           'everything': {},  # For monotheistic religions

           'blight': {'revolutionary': 0.5},
           'disease': {},
           'conquest': {'scientist': 0.5, 'general': 0.5},
           'sacrifice': {'oracle': 0.5},
           'lust': {'artist': 0.5},
           'revenge': {'hero': 0.5, 'revolutionary': 0.5},
           'gluttony': {'composer': 1, 'artist': 1, 'writer': 1},
           'envy': {'historian': 0.5, 'oracle': 1},
           'wrath': {'revolutionary': 0.5, 'hero': 1},
           'xenophobia': {'hero': 1, 'general': 1},
           'zeal': {'revolutionary': 0.5, 'hero': 0.5, 'general': 0.5},
           'apathy': {'philosopher': 0.5, 'scientist': 0.5},

           'piety': {'oracle': 1, 'prophet': 0.5, 'priest': 1, 'bishop': 0.75},
           'charity': {'hero': 1, 'professor': 1},
           'books': {'writer': 1, 'bard': 1},
           'mastery': {'master': 1, 'professional': 1},
           'observations': {'philosopher': 0.5, 'scientist': 0.5, 'professor': 0.5},
           'understanding': {'philosopher': 1, 'professor': 1},
           'morale': {'singer': 1, 'lord': 1},
           'fervor': {'revolutionary': 0.5, 'scientist': 0.5},
           'keen': {'general': 0.5, 'administrator': 0.5},
           'passion': {'hero': 1, 'administrator': 1}
           }

class God:
    def __init__(self, name, religion, domains):
        self.name = name
        self.is_male = random.choice([False, True])
        self.religion = religion
        self.domains = domains

        self.age = 0

        self.importance = random.randint(0, MAX_IMPORTANCE)

    def history_step(self, parent):
        self.age += 1

        if random.randint(0, 100) < IMPORTANCE_CHANGE_CHANCE:
            self.importance += random.randint(-IMPORTANCE_CHANGE_AMOUNT, IMPORTANCE_CHANGE_AMOUNT)

            self.importance = utility.clamp(self.importance, MAX_IMPORTANCE, 0)

        #We can't lose our last domain of course
        if len(self.domains) > 1 and random.randint(0, 100) < DOMAIN_LOSE_CHANCE:
            lost_domain = random.choice(self.domains)

            self.domains.remove(lost_domain)

            parent.event_log.add_event('ReligionDomainRemoved',
                                       {'god_a': self.name,
                                        'religion_a': self.religion.name,
                                        'domain_a': lost_domain},
                                       parent.get_current_date())

        if len(self.domains) <= MAX_DOMAIN_COUNT and random.randint(0, 100) < DOMAIN_GAIN_CHANCE:
            gained_domain = random.choice(DOMAINS.keys())

            if not gained_domain in self.domains:
                self.domains.append(gained_domain)

                parent.event_log.add_event('ReligionDomainAdded',
                                           {'god_a': self.name,
                                            'religion_a': self.religion.name,
                                            'domain_a': gained_domain},
                                           parent.get_current_date())

    def get_tolerance_score(self):
        score = 0

        for i, domain in enumerate(self.domains):
            #Some domains are neutral, like smithing and animals
            if domain in TOLERANT_DOMAINS:
                score += TOLERANCE_MULTIPLIER * self.importance
            elif domain in INTOLERANT_DOMAINS:
                score -= TOLERANCE_MULTIPLIER * self.importance

        return score

    def get_gender(self):
        if self.is_male:
            return 'god'
        else:
            return 'goddess'

    def __repr__(self):
        if len(self.domains) > 2:
            return "{} ({}): {} of {}".format(self.name, self.importance, self.get_gender(), (", ".join(self.domains[:-1]) + ', and {}'.format(self.domains[-1])))
        elif len(self.domains) == 2:
            return '{} ({}): {} of {} and {}'.format(self.name, self.importance, self.get_gender(), self.domains[0], self.domains[1])
        elif len(self.domains) == 1:
            return '{} ({}): {} of {}'.format(self.name, self.importance, self.get_gender(), self.domains[0])

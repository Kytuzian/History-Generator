import random

import utility

from culture.religion import MAX_IMPORTANCE, IMPORTANCE_CHANGE_CHANCE, IMPORTANCE_CHANGE_AMOUNT, DOMAIN_LOSE_CHANCE, \
    MAX_DOMAIN_COUNT, DOMAIN_GAIN_CHANCE, DOMAINS, TOLERANT_DOMAINS, TOLERANCE_MULTIPLIER, INTOLERANT_DOMAINS
from internal import events as events


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

            parent.events.append(events.EventReligionDomainRemoved('ReligionDomainRemoved', {'god_a': self.name, 'religion_a': self.religion.name, 'domain_a': lost_domain}, parent.get_current_date()))
            # print(parent.events[-1].text_version())

        if len(self.domains) <= MAX_DOMAIN_COUNT and random.randint(0, 100) < DOMAIN_GAIN_CHANCE:
            gained_domain = random.choice(DOMAINS.keys())

            if not gained_domain in self.domains:
                self.domains.append(gained_domain)

                parent.events.append(events.EventReligionDomainAdded('ReligionDomainAdded', {'god_a': self.name, 'religion_a': self.religion.name, 'domain_a': gained_domain}, parent.get_current_date()))
                # print(parent.events[-1].text_version())

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
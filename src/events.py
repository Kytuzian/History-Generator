import ast

main = None

def get_nation_name(id):
    for nation in main.nations:
        if nation.id == id:
            return nation.name

    for nation in main.old_nations:
        if nation == id:
            return main.old_nations[nation]

    raise Exception('{} not found in {}'.format(id, map(lambda nation: (nation.id, nation.name), main.nations)))

    return None

class Event:
    def __init__(self, name, event_data, date):
        self.name = name

        self.event_data = event_data

        self.date = date

        self.setup()

    def setup(self):
        return

    def to_dict(self):
        return {'name': self.name, 'event_data': self.event_data, 'date': self.date}

    @staticmethod
    def from_str(strdata):
        return Event.from_dict(ast.literal_eval(strdata))

    @staticmethod
    def from_dict(dict):
        if dict['name'] == 'NationFounded':
            return EventNationFounded(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'CityFounded':
            return EventCityFounded(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'CityMerged':
            return EventCityMerged(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionGodAdded':
            return EventReligionGodAdded(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionGodRemoved':
            return EventReligionGodRemoved(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionDomainAdded':
            return EventReligionDomainAdded(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionDomainRemoved':
            return EventReligionDomainRemoved(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'DiplomacyTrade':
            return EventDiplomacyTrade(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'DiplomacyWar':
            return EventDiplomacyWar(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ArmyDispatched':
            return EventArmyDispatched(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'Attack':
            return EventAttack(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'Revolt':
            return EventRevolt(dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'TechResearch':
            return EventTechResearch(dict['name'], dict['event_data'], dict['date'])
        else:
            return Event(dict['name'], dict['event_data'], dict['date'])

    def text_version(self):
        return ''

    def __repr__(self):
        return str(self.to_dict())

class EventNationFounded(Event):
    def setup(self):
        self.nation_name = self.event_data['nation_a']

    def text_version(self):
        return '{} was founded on {}.'.format(get_nation_name(self.nation_name), self.date)

class EventReligionGodAdded(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']

        self.religion_name = self.event_data['religion_a']

    def text_version(self):
        return 'A new god, {}, has been added to the pantheon of {} on {}.'.format(self.god_name, self.religion_name, self.date)

class EventReligionGodRemoved(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']

        self.religion_name = self.event_data['religion_a']

    def text_version(self):
        return 'A god, {}, has been removed from the pantheon of {} on {}.'.format(self.god_name, self.religion_name, self.date)

class EventReligionDomainAdded(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']
        self.religion_name = self.event_data['religion_a']

        self.domain_name = self.event_data['domain_a']

    def text_version(self):
        return '{} of {} has gained the domain of {} on {}.'.format(self.god_name, self.religion_name, self.domain_name, self.date)

class EventReligionDomainRemoved(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']
        self.religion_name = self.event_data['religion_a']

        self.domain_name = self.event_data['domain_a']

    def text_version(self):
        return '{} of {} has lost the domain of {} on {}.'.format(self.god_name, self.religion_name, self.domain_name, self.date)

class EventCityMerged(Event):
    def setup(self):
        self.merger = self.event_data['city_a']
        self.mergee = self.event_data['city_b']

        self.nation_name = self.event_data['nation_a']

    def text_version(self):
        return 'The cities of {} and {} in {} merged with each other on {}.'.format(self.merger, self.mergee, get_nation_name(self.nation_name), self.date)

class EventCityFounded(Event):
    def setup(self):
        self.nation_name = self.event_data['nation_a']

        self.city_name = self.event_data['city_a']

    def text_version(self):
        return '{} was founded in {} on {}.'.format(self.city_name, get_nation_name(self.nation_name), self.date)

class EventDiplomacyTrade(Event):
    def setup(self):
        self.offerer = self.event_data['nation_a']
        self.offeree = self.event_data['nation_b']

    def text_version(self):
        return '{} has formed a trade agreement with {}'.format(get_nation_name(self.offerer), get_nation_name(self.offeree))

class EventDiplomacyWar(Event):
    def setup(self):
        self.attacker = self.event_data['nation_a']
        self.defender = self.event_data['nation_b']

        self.reason = self.event_data['reason']

    def text_version(self):
        return '{} declared war on {} for {} reasons'.format(get_nation_name(self.attacker), get_nation_name(self.defender), self.reason)

class EventArmyDispatched(Event):
    def setup(self):
        self.attacker = self.event_data['nation_a']
        self.defender = self.event_data['nation_b']

        self.city_a = self.event_data['city_a']
        self.city_b = self.event_data['city_b']

        self.reason = self.event_data['reason']

        self.army_size = self.event_data['army_size']

    def text_version(self):
        return '{} has dispatched an army of {} from {} to {} {}\'s city of {}'.format(get_nation_name(self.attacker), self.army_size, self.city_a, self.reason, get_nation_name(self.defender), self.city_b)

class EventAttack(Event):
    def setup(self):
        self.attacker = self.event_data['nation_a']
        self.defender = self.event_data['nation_b']

        self.city_b = self.event_data['city_b']
        self.success = 'succeeded' if self.event_data['success'] else 'failed'

        self.remaining_soldiers = self.event_data['remaining_soldiers']

    def text_version(self):
        return '{} attacked {}\'s city of {} on {}. They {}, and the winner had {} soldiers remaining.'.format(get_nation_name(self.attacker), get_nation_name(self.defender), self.city_b, self.date, self.success, self.remaining_soldiers)

class EventRevolt(Event):
    def setup(self):
        self.parent_nation = self.event_data['nation_a']
        self.new_name = self.event_data['nation_b']

        self.cities = self.event_data['cities']

    def text_version(self):
        return 'A revolt occurred in {}, resulting in the creation of {} made up of {}'.format(get_nation_name(self.parent_nation), get_nation_name(self.new_name), self.cities)

class EventTechResearch(Event):
    def setup(self):
        self.research_nation = self.event_data['nation_a']
        self.tech_name = self.event_data['tech_a']

    def text_version(self):
        return '{}: The nation of {} has researched the technology of {}.'.format(self.date, get_nation_name(self.research_nation), self.tech_name)

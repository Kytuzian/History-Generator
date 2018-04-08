import ast

import culture.culture as culture

main = None
EVENT_LOAD_SCRIPT = 'db/internal/event/load_event.sql'
EVENT_LOG_INSERT_SCRIPT = 'db/internal/event/insert_event_data.sql'
EVENT_INSERT_SCRIPT = 'db/internal/event/insert_event.sql'
EVENT_TYPE_GET_SCRIPT = 'db/internal/event/event_type_get.sql'


def get_nation_name(id):
    for nation in main.nations:
        if nation.id == id:
            return nation.name

    for nation in main.old_nations:
        if nation == id:
            return main.old_nations[nation]

    raise Exception('{} not found in {}'.format(id, map(lambda nation: (nation.id, nation.name), main.nations)))


class Event:
    def __init__(self, event_id, name, event_data, date):
        self.name = name

        self.event_id = event_id

        self.event_data = event_data

        self.date = date

        self.setup()

    def setup(self):
        return

    def to_dict(self):
        return {'name': self.name, 'event_data': self.event_data, 'date': self.date}

    @staticmethod
    def from_db(db, event_id):
        dict = {'event_data': {}, 'id': event_id}

        for event_data in db.query(EVENT_LOAD_SCRIPT, {'event_id': event_id}):
            dict['name'] = event_data['event_type']
            dict['date'] = ast.literal_eval(event_data['event_date'])
            dict['event_data'][event_data['field_name']] = ast.literal_eval(event_data['field_value'])

        return Event.from_dict(dict)

    def save(self, db):
        event_type_id = db.query(EVENT_TYPE_GET_SCRIPT, {'name': self.name})[0]['id']
        db.execute(EVENT_INSERT_SCRIPT, {'event_id': self.event_id, 'event_type_id': event_type_id, 'event_date': str(self.date)})

        for key in self.event_data:
            db.execute(EVENT_LOG_INSERT_SCRIPT, {'event_id': self.event_id, 'field_name': key, 'field_value': str(self.event_data[key])})

    @staticmethod
    def from_dict(dict):
        if dict['name'] == 'NationFounded':
            return EventNationFounded(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'NationEliminated':
            return EventNationEliminated(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'CityFounded':
            return EventCityFounded(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'CityMerged':
            return EventCityMerged(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionCreated':
            return EventReligionCreated(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionGodAdded':
            return EventReligionGodAdded(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionGodRemoved':
            return EventReligionGodRemoved(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionDomainAdded':
            return EventReligionDomainAdded(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ReligionDomainRemoved':
            return EventReligionDomainRemoved(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'DiplomacyTrade':
            return EventDiplomacyTrade(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'DiplomacyTradeEnd':
            return EventDiplomacyTradeEnd(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'DiplomacyWar':
            return EventDiplomacyWar(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'DiplomacyWarEnd':
            return EventDiplomacyWarEnd(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ArmyDispatched':
            return EventArmyDispatched(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'Attack':
            return EventAttack(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'Revolt':
            return EventRevolt(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'TechResearch':
            return EventTechResearch(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'RearmUnit':
            return EventRearmUnit(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'NotablePersonBirth':
            return EventNotablePersonBirth(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'NotablePersonDeath':
            return EventNotablePersonDeath(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'NotablePersonPeriod':
            return EventNotablePersonPeriod(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ArtCreated':
            return EventArtCreated(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'ArmyRaised':
            return EventArmyRaised(dict['id'], dict['name'], dict['event_data'], dict['date'])
        elif dict['name'] == 'TroopCreated':
            return EventTroopCreated(dict['id'], dict['name'], dict['event_data'], dict['date'])
        else:
            return Event(dict['id'], dict['name'], dict['event_data'], dict['date'])

    def text_version(self):
        return ''

    def __repr__(self):
        return str(self.to_dict())


class EventArmyRaised(Event):
    def setup(self):
        self.nation_name = self.event_data['nation_a']
        self.army_name = self.event_data['army_a']
        self.number_raised = self.event_data['raised_a']
        self.equipment_name = self.event_data['equipment']

    def text_version(self):
        return '{} raised an army of {} {} on {}.'.format(get_nation_name(self.nation_name), self.number_raised,
                                                          self.army_name, self.equipment_name, self.date)


class EventTroopCreated(Event):
    def setup(self):
        self.nation_name = self.event_data['nation_a']
        self.army_name = self.event_data['army_a']
        self.equipment_name = self.event_data['equip_a']
        self.armor_name = self.event_data['armor_a']

    def text_version(self):
        return '{} created a new troop, {}, wielding {}, {}, and {} on {}.'.format(get_nation_name(self.nation_name),
                                                                                   self.army_name,
                                                                                   self.equipment_name[0].name,
                                                                                   self.equipment_name[1].name,
                                                                                   self.armor_name.name, self.date)


class EventNationFounded(Event):
    def setup(self):
        self.nation_name = self.event_data['nation_a']

    def text_version(self):
        return '{} was founded on {}.'.format(get_nation_name(self.nation_name), self.date)


class EventNationEliminated(Event):
    def setup(self):
        self.nation_name = self.event_data['nation_a']

    def text_version(self):
        return '{}: {} was eliminated.'.format(self.date, get_nation_name(self.nation_name))


class EventReligionCreated(Event):
    def setup(self):
        self.nation = self.event_data['nation_a']
        self.city = self.event_data['city_a']
        self.founder = self.event_data['person_a']

        self.religion_name = self.event_data['religion_a']

    def text_version(self):
        if self.founder is not None:
            return '{}: The religion of {} was founded in the city of {} in the nation of {} by {}.'.format(self.date,
                                                                                                            self.religion_name,
                                                                                                            get_nation_name(
                                                                                                                self.nation),
                                                                                                            self.city,
                                                                                                            self.nation,
                                                                                                            self.founder)
        else:
            return '{}: The religion of {} was founded in the city of {} in the nation of {}.'.format(self.date,
                                                                                                      self.religion_name,
                                                                                                      get_nation_name(
                                                                                                          self.nation),
                                                                                                      self.city,
                                                                                                      self.nation)


class EventReligionGodAdded(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']

        self.religion_name = self.event_data['religion_a']

    def text_version(self):
        return 'A new god, {}, has been added to the pantheon of {} on {}.'.format(self.god_name, self.religion_name,
                                                                                   self.date)


class EventReligionGodRemoved(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']

        self.religion_name = self.event_data['religion_a']

    def text_version(self):
        return 'A god, {}, has been removed from the pantheon of {} on {}.'.format(self.god_name, self.religion_name,
                                                                                   self.date)


class EventReligionDomainAdded(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']
        self.religion_name = self.event_data['religion_a']

        self.domain_name = self.event_data['domain_a']

    def text_version(self):
        return '{} of {} has gained the domain of {} on {}.'.format(self.god_name, self.religion_name, self.domain_name,
                                                                    self.date)


class EventReligionDomainRemoved(Event):
    def setup(self):
        self.god_name = self.event_data['god_a']
        self.religion_name = self.event_data['religion_a']

        self.domain_name = self.event_data['domain_a']

    def text_version(self):
        return '{} of {} has lost the domain of {} on {}.'.format(self.god_name, self.religion_name, self.domain_name,
                                                                  self.date)


class EventCityMerged(Event):
    def setup(self):
        self.merger = self.event_data['city_a']
        self.mergee = self.event_data['city_b']

        self.nation_name = self.event_data['nation_a']

    def text_version(self):
        return 'The cities of {} and {} in {} merged with each other on {}.'.format(self.merger, self.mergee,
                                                                                    get_nation_name(self.nation_name),
                                                                                    self.date)


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
        return '{} has formed a trade agreement with {}.'.format(get_nation_name(self.offerer),
                                                                 get_nation_name(self.offeree))


class EventDiplomacyTradeEnd(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.nation_b = self.event_data['nation_b']

    def text_version(self):
        return '{}: The trade agreement between {} and {} has ended.'.format(self.date, get_nation_name(self.nation_a),
                                                                             get_nation_name(self.nation_b))


class EventDiplomacyWar(Event):
    def setup(self):
        self.attacker = self.event_data['nation_a']
        self.defender = self.event_data['nation_b']

        self.reason = self.event_data['reason']

    def text_version(self):
        return '{} declared war on {} for {} reasons'.format(get_nation_name(self.attacker),
                                                             get_nation_name(self.defender), self.reason)


class EventDiplomacyWarEnd(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.nation_b = self.event_data['nation_b']

    def text_version(self):
        return '{}: The war between {} and {} has ended.'.format(self.date, get_nation_name(self.nation_a),
                                                                 get_nation_name(self.nation_b))


class EventArmyDispatched(Event):
    def setup(self):
        self.attacker = self.event_data['nation_a']
        self.defender = self.event_data['nation_b']

        self.city_a = self.event_data['city_a']
        self.city_b = self.event_data['city_b']

        self.reason = self.event_data['reason']

        self.army_size = self.event_data['army_size']

    def text_version(self):
        return '{} has dispatched an army of {} from {} to {} {}\'s city of {}'.format(get_nation_name(self.attacker),
                                                                                       self.army_size, self.city_a,
                                                                                       self.reason,
                                                                                       get_nation_name(self.defender),
                                                                                       self.city_b)


class EventAttack(Event):
    def setup(self):
        self.attacker = self.event_data['nation_a']
        self.defender = self.event_data['nation_b']

        self.city_b = self.event_data['city_b']
        self.success = 'succeeded' if self.event_data['success'] else 'failed'

        self.remaining_soldiers = self.event_data['remaining_soldiers']

    def text_version(self):
        return '{} attacked {}\'s city of {} on {}. They {}, and the winner had {} soldiers remaining.'.format(
            get_nation_name(self.attacker), get_nation_name(self.defender), self.city_b, self.date, self.success,
            self.remaining_soldiers)


class EventRevolt(Event):
    def setup(self):
        self.parent_nation = self.event_data['nation_a']
        self.new_name = self.event_data['nation_b']

        self.cities = self.event_data['cities']

    def text_version(self):
        return 'A revolt occurred in {}, resulting in the creation of {} made up of {}'.format(
            get_nation_name(self.parent_nation), get_nation_name(self.new_name), self.cities)


class EventTechResearch(Event):
    def setup(self):
        self.research_nation = self.event_data['nation_a']
        self.tech_name = self.event_data['tech_a']

    def text_version(self):
        return '{}: The nation of {} has researched the technology of {}.'.format(self.date,
                                                                                  get_nation_name(self.research_nation),
                                                                                  self.tech_name)


class EventRearmUnit(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.unit_name = self.event_data['unit_a']
        self.new_weapons = self.event_data['weapons']
        self.new_armor = self.event_data['armor']

    def text_version(self):
        return '{}: The nation of {} has rearmed it\'s unit of {} with {} and {}.'.format(self.date, get_nation_name(
            self.nation_a), self.unit_name, self.new_weapons, self.new_armor)


class EventNotablePersonBirth(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.person_name = self.event_data['person_a']
        self.person_role = self.event_data['person_a_role']

    def text_version(self):
        return '{}: {}, a {}, was born in the nation of {}'.format(self.date, self.person_name, self.person_role,
                                                                   get_nation_name(self.nation_a))


class EventNotablePersonDeath(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.person_name = self.event_data['person_a']
        self.person_role = self.event_data['person_a_role']

    def text_version(self):
        return '{}: {}, a {} from the nation of {}, has died.'.format(self.date, self.person_name, self.person_role,
                                                                      get_nation_name(self.nation_a))


class EventNotablePersonPeriod(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.person_name = self.event_data['person_a']
        self.person_prev_role = self.event_data['person_a_prev_role']
        self.person_role = self.event_data['person_a_role']
        self.period_name = self.event_data['period_name']

    def text_version(self):
        if self.person_prev_role == '':
            return '{}: {} became a {}.'.format(self.date, self.person_name, self.person_role)
        elif self.person_prev_role == self.person_role:
            return '{}: {} has begun a new period, called his {}.'.format(self.date, self.person_name, self.period_name)
        else:
            if self.person_role in culture.ART_CATEGORIES.keys():
                return '{}: {}, who was previously a {}, is now a {}, and has started his {}.'.format(self.date,
                                                                                                      self.person_name,
                                                                                                      self.person_prev_role,
                                                                                                      self.person_role,
                                                                                                      self.period_name)
            else:
                return '{}: {}, who was previously a {}, is now a {}.'.format(self.date, self.person_name,
                                                                              self.person_prev_role, self.person_role)


class EventArtCreated(Event):
    def setup(self):
        self.nation_a = self.event_data['nation_a']
        self.person_name = self.event_data['person_a']
        self.person_role = self.event_data['person_a_role']

        self.art = self.event_data['art']

    def text_version(self):
        return '{}: In the nation of {}, the {} {} created: {}'.format(self.date, get_nation_name(self.nation_a),
                                                                       self.person_role, self.person_name, self.art)

import random

from culture.language import LOSE_PLACE_CITY_NAME, LOSE_NAME_MODIFIER, GAIN_NAME_MODIFIER, MODIFIERS


class NationName:
    def __init__(self, modifiers, government_type, places):
        self.modifiers = modifiers
        self.government_type = government_type
        self.places = places

    @classmethod
    def load(cls, info):
        return cls(info['modifiers'], info['government_type'], info['places'])

    def get_info(self):
        res = {}
        res['modifiers'] = self.modifiers
        res['government_type'] = self.government_type
        res['places'] = self.places

        return res

    def history_step(self, parent):
        parent_cities_names = map(lambda city: city.name, parent.cities)

        for place in self.places:
            #We can't get rid of the last one.
            if not place in parent_cities_names and len(self.places) > 1:
                if random.randint(0, LOSE_PLACE_CITY_NAME) == 0:
                    self.remove_place(place)

        for modifier in self.modifiers:
            if random.randint(0, LOSE_NAME_MODIFIER) == 0:
                self.remove_modifier(modifier)

        if random.randint(0, GAIN_NAME_MODIFIER) == 0:
            self.add_modifier(random.choice(MODIFIERS))

    def add_modifier(self, modifier_name):
        self.modifiers.append(modifier_name)

    def remove_modifier(self, modifier_name):
        self.modifiers.remove(modifier_name)

    def add_place(self, place_name):
        self.places.append(place_name)

    def remove_place(self, place_name):
        self.places.remove(place_name)

    def short_name(self):
        return self.places[0]

    def get_name(self):
        modifier_part = ' '.join(self.modifiers)

        if len(self.places) > 2:
            place_part = '{}, and {}'.format(', '.join(self.places[:-1]), self.places[-1])
        elif len(self.places) == 2:
            place_part = '{} and {}'.format(self.places[0], self.places[1])
        else:
            place_part = self.places[0]

        if len(self.modifiers) > 0:
            return 'The {} {} of {}'.format(modifier_part, self.government_type, place_part)
        else:
            return 'The {} of {}'.format(self.government_type, place_part)

    def __repr__(self):
        return self.get_name()
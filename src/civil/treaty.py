import math
import random

from culture.form import Form
from civil.diplomacy import TRADE_CARAVAN_MULTIPLIER, WAR_CITY_MULTIPLIER, TRADE_END_DIVISOR, TREATY_NAMES

import internal.utility as utility
import internal.events as events

class Treaty:
    def __init__(self, parent, starting_date, nation_a, nation_b, treaty_type, signing_city=None, treaty_details=None):
        if treaty_details is None:
            treaty_details = {}
        self.parent = parent

        self.treaty_id = self.parent.get_next_id('treaty')

        self.starting_date = starting_date
        self.ending_date = None

        self.nation_a = nation_a
        self.nation_b = nation_b

        self.names = {}
        self.last_requested_date = self.starting_date
        self.status_changed = False

        if signing_city is not None:
            self.signing_city = signing_city
        else:
            capitals = []
            if nation_a.has_capital():
                capitals.append(nation_a.get_capital())
            elif nation_b.has_capital():
                capitals.append(nation_b.get_capital())

            if len(capitals) > 0:
                self.signing_city = random.choice(capitals)
            elif len(nation_a.cities + nation_b.cities) > 0:
                self.signing_city = random.choice(nation_a.cities + nation_b.cities)
            else:
                self.signing_city = None

        self.treaty_type = treaty_type

        if treaty_details != {}:
            self.treaty_details = treaty_details
        else:
            self.treaty_details = {}
            if treaty_type == 'trade':
                self.treaty_details[nation_a.id] = {}
                self.treaty_details[nation_a.id]['caravans_sent'] = 0
                self.treaty_details[nation_a.id]['caravans_received'] = 0
                self.treaty_details[nation_a.id]['money'] = 0

                self.treaty_details[nation_b.id] = {}
                self.treaty_details[nation_b.id]['caravans_sent'] = 0
                self.treaty_details[nation_b.id]['caravans_received'] = 0
                self.treaty_details[nation_b.id]['money'] = 0
            elif treaty_type == 'war':
                self.treaty_details[nation_a.id] = {}
                self.treaty_details[nation_a.id]['troops_killed'] = 0
                self.treaty_details[nation_a.id]['troops_lost'] = 0
                self.treaty_details[nation_a.id]['cities_conquered'] = 0
                self.treaty_details[nation_a.id]['cities_lost'] = 0

                self.treaty_details[nation_b.id] = {}
                self.treaty_details[nation_b.id]['troops_killed'] = 0
                self.treaty_details[nation_b.id]['troops_lost'] = 0
                self.treaty_details[nation_b.id]['cities_conquered'] = 0
                self.treaty_details[nation_b.id]['cities_lost'] = 0

        self.is_current = True

    def save(self, path):
        res = {'id': self.treaty_id, 'starting_date': self.starting_date, 'ending_date': self.ending_date,
               'nation_a': self.nation_a.id, 'nation_b': self.nation_b.id, 'names': self.names,
               'last_requested_date': self.last_requested_date, 'status_changed': self.status_changed}

        if self.signing_city is not None:
            res['signing_city'] = self.signing_city.name
        else:
            res['signing_city'] = self.signing_city

        res['treaty_type'] = self.treaty_type
        res['treaty_details'] = self.treaty_details
        res['is_current'] = self.is_current

        with open(path + self.treaty_id + '.txt', 'w') as f:
            f.write(str(res))

    def __getitem__(self, key):
        return self.treaty_details[key]

    def length(self, current_date):
        year_len, month_len, day_len = utility.get_time_span_length(self.starting_date, current_date)

        # There are only 360 days in a year in our world, because life is so much simpler that way
        actual_len = year_len + month_len / 12.0 + day_len / 360.0

        # If treaty has only been in effect for 0 time, then let's just say it's been one day.
        return max(actual_len, 1.0 / 360.0)

    def get_score(self, nation, current_date):
        if self.treaty_type == 'trade':
            details = self.treaty_details[nation.id]
            base_score = details['money'] + (details['caravans_received'] - details['caravans_sent']) * TRADE_CARAVAN_MULTIPLIER

            return base_score / self.length(current_date)
        elif self.treaty_type == 'war':
            details = self.treaty_details[nation.id]
            base_score = (details['cities_conquered'] - details['cities_lost']) * WAR_CITY_MULTIPLIER + (details['troops_killed'] - details['troops_lost'])

            return base_score

    def history_step(self, nation, current_date):
        # Treaties must last at least one year to give them time to happen and such
        if self.length(current_date) > 1 and self.is_current:
            if self.treaty_type == 'trade':
                # We can end a trade treaty with the agreement of only one side.
                score = self.get_score(nation, current_date)
                if score < 0:
                    end_chance = 0.5 + math.log(-score+1) / TRADE_END_DIVISOR
                else:
                    end_chance = 0.5 - math.log(score+1) / TRADE_END_DIVISOR

                # print('trade', end_chance)

                val = random.random()
                if val < end_chance:
                    self.end(current_date, ender=nation)
            elif self.treaty_type == 'war':
                # Both parties have to agree to end a war, obviously
                a_score = self.get_score(self.nation_a, current_date)
                if a_score < 0:
                    nation_a_end_chance = 0.5 + math.log(-a_score+1) / TRADE_END_DIVISOR
                else:
                    nation_a_end_chance = 0.5 - math.log(a_score+1) / TRADE_END_DIVISOR

                b_score = self.get_score(self.nation_b, current_date)
                if b_score < 0:
                    nation_b_end_chance = 0.5 + math.log(-b_score+1) / TRADE_END_DIVISOR
                else:
                    nation_b_end_chance = 0.5 - math.log(b_score+1) / TRADE_END_DIVISOR

                end_chance = nation_a_end_chance * nation_b_end_chance
                # print('war', end_chance)

                val = random.random()
                if val < end_chance:
                    self.end(current_date)

    def get_other_nation(self, nation):
        if nation == self.nation_a:
            return self.nation_b
        else:
            return self.nation_a

    def get_other_side_details(self, nation):
        if nation == self.nation_a:
            return self.treaty_details[self.nation_b.id]
        else:
            return self.treaty_details[self.nation_a.id]

    def end(self, current_date, ender=None):
        self.is_current = False
        self.ending_date = current_date

        self.status_changed = True

        if self.treaty_type == 'trade':
            self.nation_a.trading.remove(self.nation_b)
            self.nation_b.trading.remove(self.nation_a)

            if ender is None:
                ender = self.nation_a
            self.parent.events.append(events.EventDiplomacyTradeEnd('DiplomacyTradeEnd', {'nation_a': ender.id, 'nation_b': self.get_other_nation(ender).id}, self.parent.get_current_date()))
            self.parent.write_to_gen_log(self.parent.events[-1].text_version())
        elif self.treaty_type == 'war':
            self.nation_a.at_war.remove(self.nation_b)
            self.nation_b.at_war.remove(self.nation_a)

            self.parent.events.append(events.EventDiplomacyWarEnd('DiplomacyWarEnd', {'nation_a': self.nation_a.id, 'nation_b': self.nation_b.id}, self.parent.get_current_date()))
            self.parent.write_to_gen_log(self.parent.events[-1].text_version())

    def get_treaty_names(self, current_date, requesting_nation):
        if not requesting_nation.id in self.names or len(self.names[requesting_nation.id]) == 0:
            self.get_treaty_name(current_date, requesting_nation)

        return self.names[requesting_nation.id]

    def get_treaty_name(self, current_date, requesting_nation):
        if self.status_changed or current_date > self.last_requested_date or not requesting_nation.id in self.names or len(self.names[requesting_nation.id]) == 0:
            custom_tags = {}
            if self.signing_city is not None:
                custom_tags['signing_city'] = [self.signing_city.name]
            else:
                custom_tags['signing_city'] = [str(self.nation_a.name), str(self.nation_b.name)]
            custom_tags['signing_year'] = [str(self.starting_date[0])]
            custom_tags['nation_a'] = [str(self.nation_a.name)]
            custom_tags['nation_b'] = [str(self.nation_b.name)]

            if self.ending_date is not None:
                treaty_length = utility.get_time_span_length(self.starting_date, self.ending_date)
            else:
                treaty_length = utility.get_time_span_length(self.starting_date, current_date)
            custom_tags['treaty_length_years'] = ['{} years'.format(treaty_length[0])]
            custom_tags['treaty_length'] = ['{} years and {} months'.format(treaty_length[0], treaty_length[1])]

            gen = culture.form.Form(TREATY_NAMES[self.treaty_type], custom_tags=custom_tags)

            name = gen.generate(nation=requesting_nation)[0]

            if not requesting_nation.id in self.names:
                self.names[requesting_nation.id] = []

            self.names[requesting_nation.id].append(name)

            self.last_requested_date = current_date
            self.status_changed = False

        return self.names[requesting_nation.id][-1]
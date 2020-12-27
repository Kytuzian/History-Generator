import math
import random

from civil.resources import base_resource_prices
from internal.group.group import Group
from internal import utility

# The maximum number of people that can be converted per religion per caravan
CARAVAN_CONVERSION_MAGNITUDE = 5
TRADE_GOOD_PRICE = 25


class Caravan(Group):
    def __init__(self, parent, religion, from_city, destination_city, has_boat):
        self.from_city = from_city
        self.destination_city = destination_city

        self.religion = religion

        self.resources_sent = {}

        # Find out what they need
        resource_diff = from_city.get_resource_differences(destination_city)

        for resource in resource_diff:
            if resource_diff[resource] > 0:
                self.resources_sent[resource] = random.randint(1, int(resource_diff[resource]))

        # This is to ensure that all caravans make at least some money
        self.resources_sent['trade_goods'] = random.randint(1, int(math.log(from_city.population)) ** 2 + 1)

        # Set up the rest of the information we need to be a proper group object
        Group.__init__(self, parent, 'caravan', (religion, self.resources_sent), from_city.position,
                       destination_city.position, from_city.nation.color, lambda _: False,
                       self.receive_caravan, has_boat)

    def receive_caravan(self, _):
        receiving_city = self.destination_city
        receiving_nation = receiving_city.nation

        sending_city = self.from_city
        sending_nation = sending_city.nation

        self.from_city.caravans.remove(self)

        # Construct a demand ranking
        consumption_ranking = sorted(self.destination_city.consumed_resources.items(), key=utility.snd)
        res_count = float(len(consumption_ranking))
        resource_mults = {k: (res_count / 2.0 - i) / res_count for i, (k, v) in enumerate(consumption_ranking)}
        prices = base_resource_prices()

        for resource in prices:
            prices[resource] *= resource_mults[resource]

        profit = 0
        for resource in self.resources_sent:
            if resource in prices:
                profit += self.resources_sent[resource] * prices[resource]
            elif resource == 'trade_goods':
                profit += TRADE_GOOD_PRICE * self.resources_sent[resource]

        profit = int(profit)

        receiving_nation.money += profit

        if sending_nation != receiving_nation:  # Trading with ourselves doesn't give any bonus
            receiving_city.nation.money += profit

            trade_treaty = sending_nation.get_treaty_with(receiving_city.nation, 'trade')

            if trade_treaty is not None:  # Although this should always be the case, really.
                trade_treaty[receiving_nation.id]['caravans_received'] += 1
                trade_treaty[receiving_nation.id]['money'] += profit
                trade_treaty[receiving_city.nation.id]['money'] += profit

        # The religion of the caravan influences the religion of this city (but only if they have a different
        # religion than the caravan)
        receiving_city.handle_religious_conversion(self.religion, CARAVAN_CONVERSION_MAGNITUDE)


# This file contains some basic "AI" stuff, so that we can determine what buildings to build, and that sort of stuff
# Pretty much for anything that involves producing and consuming goods.

import math

class Producer:
    def __init__(self, name, produce, buy):
        self.name = name

        self.produce = produce
        self.buy = buy

        self.goods = self.get_supply().keys()

    def get_supply(self):
        return self.produce()

class Consumer:
    def __init__(self, name, consume):
        self.name = name

        self.consume = consume

        self.goods = self.get_consumption().keys()

    def get_consumption(self):
        return self.consume()

class SupplyDemand:
    def __init__(self, goods, producers, consumers):
        self.goods = dict(goods)

        self.producers = producers
        self.consumers = consumers

    def get_net_goods(self):
        net = dict(self.goods)

        for producer in self.producers:
            supply = producer.get_supply()

            for good in supply:
                net[good] += supply[good]

        for consumer in self.consumers:
            consumption = consumer.get_consumption()

            for good in consumption:
                net[good] -= consumption[good]

        return net

    def get_required_producers(self):
        net = self.get_net_goods()

        required_producers = {}

        for good in net:
            if net[good] < 0:
                for producer in self.producers:
                    if good in producer.goods:
                        supply = producer.get_supply()

                        required_amount = int(math.ceil(float(abs(net[good])) / supply[good]))

                        if producer.name in required_producers:
                            required_producers[producer.name] += required_amount
                        else:
                            required_producers[producer.name] = required_amount

        return required_producers

    def purchase_required_producers(self):
        return

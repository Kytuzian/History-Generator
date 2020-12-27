def base_tech_tree():
    return Tech('Agriculture', 'agriculture', 0, 1.0,
                [
                    Tech('Stone Working', 'material', 400, 1.1,
                         [
                             Tech('Copper', 'material', 1600, 1.5,
                                  [
                                      Tech('Bronze', 'material', 3200, 2.0,
                                           [
                                               Tech('Iron', 'material', 6400, 2.5,
                                                    [
                                                        Tech('Steel', 'material', 12800, 3.0,
                                                             [
                                                                 Tech('Refined Steel', 'material', 12800 * (3 / 2),
                                                                      3.25,
                                                                      [

                                                                      ])
                                                             ])
                                                    ])
                                           ])
                                  ])
                         ]),
                    Tech('Housing I', 'housing', 250, 1.25,
                         [
                             Tech('Housing II', 'housing', 400, 1.5,
                                  [
                                      Tech('Housing III', 'housing', 600, 1.75,
                                           [
                                               Tech('Housing IV', 'housing', 800, 2.0,
                                                    [
                                                        Tech('Housing V', 'housing', 1200, 2.5, [])
                                                    ])
                                           ])
                                  ]),
                             Tech('Compact Building I', 'compact_building', 800, 1.15,
                                  [
                                      Tech('Compact Building II', 'compact_building', 1600, 1.5, [])
                                  ])
                         ]),
                    Tech('Mining I', 'mining', 400, 1.25,
                         [
                             Tech('Mining II', 'mining', 600, 1.5,
                                  [
                                      Tech('Mining III', 'mining', 700, 1.75,
                                           [
                                               Tech('Mining IV', 'mining', 900, 2.0,
                                                    [
                                                        Tech('Mining V', 'mining', 1200, 2.5, [])
                                                    ])
                                           ])
                                  ])
                         ]),
                    Tech('Agriculture I', 'agriculture', 200, 1.1,
                         [
                             Tech('Agriculture II', 'agriculture', 300, 1.2,
                                  [
                                      Tech('Agriculture III', 'agriculture', 400, 1.3,
                                           [
                                               Tech('Agriculture IV', 'agriculture', 600, 1.4,
                                                    [
                                                        Tech('Agriculture V', 'agriculture', 800, 1.5, [])
                                                    ])
                                           ])
                                  ])
                         ]),
                ])


def tech_categories():
    return ['agriculture', 'material', 'housing', 'mining']


class Tech:
    def __init__(self, name, category, research_points, effect_strength, next_techs):
        self.name = name
        self.category = category

        self.current_research_points = 0
        self.research_points = research_points

        self.effect_strength = effect_strength

        self.next_techs = next_techs

        self.best_techs = {}

        self.get_best_in_categories()

    def get_info(self):
        res = {}
        res['name'] = self.name
        res['category'] = self.category
        res['current_research_points'] = self.current_research_points
        res['research_points'] = self.research_points

        res['effect_strength'] = self.effect_strength
        res['next_techs'] = list(map(lambda tech: tech.get_info(), self.next_techs))
        # We don't need to save best_techs, we can just recalculate them when we load.

        return res

    def save(self, path):
        with open(path + 'tech.txt', 'w') as f:
            f.write(str(self.get_info()))

    def is_unlocked(self):
        return self.current_research_points >= self.research_points

    def get_tech(self, tech_name):
        if self.name == tech_name and self.is_unlocked():
            return self
        else:
            for next_tech in self.next_techs:
                res = next_tech.get_tech(tech_name)
                if res is not None:
                    return res

            return None

    def has_tech(self, tech_name):
        if self.name == tech_name:
            return self.is_unlocked()
        else:
            for next_tech in self.next_techs:
                if next_tech.has_tech(tech_name):
                    return True

            return False

    def get_best_in_categories(self):
        for category in tech_categories():
            self.best_techs[category] = self.get_best_in_category(category, True)

    def get_best_in_category(self, category_name, calc=False):
        if calc or not category_name in self.best_techs:
            for i in self.next_techs:
                if i.category == category_name and i.is_unlocked():
                    return i.get_best_in_category(category_name)

            if self.category == category_name:
                return self

            return None
        else:
            return self.best_techs[category_name]

    def get_available_research(self):
        if self.is_unlocked():
            result = []
            for next_tech in self.next_techs:
                result.extend(next_tech.get_available_research())
            return result
        else:
            return [self]

    def do_research(self, research_amount):
        if not self.is_unlocked():
            self.current_research_points += research_amount

            self.get_best_in_categories()

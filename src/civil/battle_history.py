class BattleHistory:
    def __init__(self, parent, location, winner, nation_a, nation_b, date, a_stats, b_stats):
        self.parent = parent
        self.battle_id = self.parent.get_next_id('battle')

        self.location = location

        self.winner = winner

        self.nation_a = nation_a
        self.nation_b = nation_b

        self.date = date

        self.a_stats = a_stats
        self.b_stats = b_stats

    def save(self, path):
        res = {'id': self.battle_id, 'location': self.location.name, 'winner': self.winner.id,
               'nation_a': self.nation_a.id, 'nation_b': self.nation_b.id, 'date': self.date, 'a_stats': self.a_stats,
               'b_stats': self.b_stats}

        with open(path + self.battle_id + '.txt', 'w') as f:
            f.write(str(res))
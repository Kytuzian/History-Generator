import sqlite3


class DB:
    def __init__(self, name):
        self.name = name

        self.conn = sqlite3.connect('saves/' + name + '.db')

    def query(self, fname, params=None):
        with open(fname) as f:
            query = f.read()

        result = []

        cursor = self.conn.cursor()

        if params is None:
            res = list(cursor.execute(query))
        else:
            res = list(cursor.execute(query, params))

        if len(res) > 0:
            columns = res[0]

            for row in res[1:]:
                result.append({})

                for i, col in enumerate(columns):
                    result[col] = row[i]

        return result

    def execute(self, fname, params=None):
        with open(fname) as f:
            statement = f.read()

        cursor = self.conn.cursor()

        if params is None:
            cursor.execute(statement)
        else:
            cursor.execute(statement, params)

        self.conn.commit()

    def setup(self):
        # Create all the tables
        self.execute('db/setup/gen_log.sql')
        self.execute('db/setup/nations.sql')
        self.execute('db/setup/names.sql')
        self.execute('db/setup/name_modifiers.sql')
        self.execute('db/setup/name_places.sql')
        self.execute('db/setup/relations.sql')
        self.execute('db/setup/nation_relationship.sql')
        self.execute('db/setup/groups.sql')
        self.execute('db/setup/weapons.sql')
        self.execute('db/setup/weapon_stats.sql')
        self.execute('db/setup/armors.sql')
        self.execute('db/setup/equipment_list.sql')
        self.execute('db/setup/treaties.sql')

        self.conn.commit()


import sqlite3
import os

class DB:
    def __init__(self, name):
        self.name = name

        self.conn = sqlite3.connect('saves/{}.db'.format(self.name))

    def save(self):
        # Clear the old db.
        self.conn.close()
        os.remove('saves/{}.db'.format(self.name))
        self.conn = sqlite3.connect('saves/{}.db'.format(self.name))
        self.setup()

    def query(self, fname, params=None):
        with open(fname) as f:
            contents = f.read()

        result = []
        cursor = self.conn.cursor()

        for query in contents.split(';'):
            if params is None:
                cursor.execute(query)
            else:
                cursor.execute(query, params)

            res = cursor.fetchall()

            if len(res) > 0:
                for row in res:
                    result.append({})

                    for i, col in enumerate(cursor.description):
                        result[-1][col[0]] = row[i]

        return result

    def execute(self, fname, params=None):
        with open(fname) as f:
            contents = f.read()

        for statement in contents.split(';'):
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
        self.execute('db/setup/events.sql')
        self.execute('db/setup/event_types.sql')
        self.execute('db/setup/event_data.sql')

        self.conn.commit()

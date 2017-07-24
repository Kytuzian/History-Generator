import sqlite3

class DB:
    def __init__(self, name):
        self.name = name

        self.conn = sqlite3.connect(name + '.db')

    def query(self, fname, params=None):
        with open(fname) as f:
            query = f.read()
        
        result = []

        cursor = self.conn.cursor()
        
        res = []
        if params == None:
            res = list(cursor.execute(query))
        else:
            res = list(cursor.execute(query, params))

        columns = res[0]

        for row in res[1:]:
            result.append({})

            for i, col in zip(len(columns), columns):
                result[col] = row[i]

        return result

    def execute(self, fname, params=None):
        with open(fname) as f:
            statement = f.read()

        cursor = self.conn.cursor()
        
        if params == None:
            cursor.execute(statement)
        else:
            cursor.execute(statement, params)

        self.conn.commit()

    def setup(self):
        cursor = self.conn.cursor()
    
        # Create all the tables
        self.execute('db/setup/gen_log.sql')
        self.execute('db/setup/nations.sql')
        self.execute('db/setup/relations.sql')
        self.execute('db/setup/nation_relationship.sql')
        self.execute('db/setup/groups.sql')
        self.execute('db/setup/weapons.sql')
        self.execute('db/setup/weapon_stats.sql')
        self.execute('db/setup/armors.sql')
        self.execute('db/setup/equipment_list.sql')
        self.execute('db/setup/treaties.sql')

        self.conn.commit()

    def gen_log_insert(self, date, message):
        self.execute('db/gen_log_insert.sql', [date, message])


import sqlite3

import vlbimon_types


vlbi_types = vlbimon_types.get_types()
to_sql_types = {
    int: 'INTEGER',
    float: 'REAL',
    str: 'TEXT',
    bool: 'BOOLEAN',
}
vlbi_types = dict([(name, to_sql_types[ty]) for name, ty in vlbi_types.items()])

stations = ['ALMA', 'APEX', 'GLT', 'JCMT', 'KP', 'LMT', 'NOEMA', 'PICO', 'SMA', 'SMTO', 'SPT']

con = sqlite3.connect('vlbimon.db')

cur = con.cursor()

for param, vlbi_type in vlbi_types.items():
    param = param.split('.')[0]
    print(param, vlbi_type)
    cur.execute('CREATE TABLE ts_param_{} (time INTEGER NOT NULL, station TEXT NOT NULL, value {})'.format(param, vlbi_type))
    cur.execute('CREATE INDEX idx_ts_param_{}_time ON ts_param_{}(time)'.format(param, param))
    cur.execute('CREATE INDEX idx_ts_param_{}_station ON ts_param_{}(station)'.format(param, param))

res = cur.execute('SELECT name FROM sqlite_master')
names = res.fetchall()
if len(names) != len(vlbi_types)*3:  # tables and indices have names
    print('Surprised by some extra tables.')
    print(' Expected {}, found {}'.format(len(vlbi_types)*3, len(names)))
    print('Here are all of their names:', *names)

import sys
import glob
import os.path
import sqlite3

import vlbimon_types


all_stations = ['ALMA', 'APEX', 'GLT', 'JCMT', 'KP', 'LMT', 'NOEMA', 'PICO', 'SMA', 'SMTO', 'SPT']

basedir = sys.argv[1]

if len(sys.argv) > 2:
    stations = sys.argv[2:]
else:
    stations = all_stations
vlbi_types = vlbimon_types.get_types()

con = sqlite3.connect('vlbimon.db')
cur = con.cursor()

for station in stations:
    print('station', station)
    csvs = glob.glob(basedir + '/' + station + '/*.csv')
    for fname in csvs:
        head, param = os.path.split(fname)
        if param not in vlbi_types:
            raise ValueError('file {} is not in vlbi_types.csv'.format(param))
        value_type = vlbi_types[param]
        param = param.split('.')[0]
        print(' ', param)

        last_ts = 0
        data = []
        with open(fname, 'r') as fd:
            for line in fd:
                parts = line.split(',')

                if len(parts) != 2:
                    raise ValueError('invalid line: '+line)
                ts, value = parts
                if not ts.isdigit():
                    raise ValueError('invalid timestamp in line: '+line)
                ts = int(ts)
                if ts < last_ts:
                    raise ValueError('saw backword in time, {} and {} in line {}'.format(last_ts, ts, line))
                if ts == last_ts:
                    # silently drop dup. might want to check if value is ==
                    print('skipping dup', ts)
                    continue
                last_ts = ts

                value = value_type(value)
                data.append((ts, station, value))
        cur.executemany('INSERT INTO ts_param_{} VALUES(?, ?, ?)'.format(param), data)
        con.commit()

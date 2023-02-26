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
                line = line.rstrip()
                if line == '':
                    # ../vlbimon-bridge/data/PICO/telescope_pointingCorrection.csv has extra \n
                    continue
                parts = line.split(',', 1)

                if value_type != str and ',' in parts[1]:
                    raise ValueError('invalid line: '+fname+' '+line)
                if len(parts) == 1:
                    raise ValueError('invalid line: '+fname+' '+line)
                ts, value = parts
                if ts == '946684800':
                    # Jan 1 2000 bug
                    continue
                if not ts.isdigit():
                    raise ValueError('invalid timestamp in line: '+fname+' '+line)
                ts = int(ts)
                if ts < 1647543720:
                    # get rid of early data points
                    continue
                if ts < last_ts:
                    print('{} saw backword in time, {} and {} in line {}'.format(fname, last_ts, ts, line))
                    #raise ValueError('{} saw backword in time, {} and {} in line {}'.format(fname, last_ts, ts, line))
                if ts == last_ts:
                    # silently drop dup. might want to check if value is ==
                    #print('skipping dup', ts)
                    continue
                last_ts = ts

                try:
                    value = value_type(value)
                except Exception as e:
                    print(fname, repr(e))
                    continue

                data.append((ts, station, value))
        cur.executemany('INSERT INTO ts_param_{} VALUES(?, ?, ?)'.format(param), data)
        con.commit()

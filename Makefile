vlbimon.db:
	rm vlbimon.db
	python generate_types.py  > vlbimon_types.csv
	python create_tables.py
	python insert_station.py ../vlbimon-bridge/data

# eht-monitor-demo

This repo contains the code to create a sqlite3 database with time-series data
downloaded from the vlbimon database, and then spin up a Grafana instance.

## Data source

The time-series data is downloaded by https://github.com/wumpus/vlbimon-bridge

The output should be a file tree that looks something like:

```
data/
  ALMA/
    weatherMap_waterVapor_url.csv
    ...
```

## Create the sqlite3 db with downloaded vlbimon data

Using python3,

```
python create_tables.py
python insert_station.py /path/to/vlbimon-bridge/data
```

You should end up with a `vlbimon.db` file. One day of 2022 vlbimon
data is 17 megabytes.

## Install Grafana

I chose to install on Ubuntu from the [Grafana APT repository instructions.](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/#install-from-apt-repository)

This means that the configuration files are in the usual system directories.

I also installed the sqlite plugin:

```
sudo grafana-cli plugins install frser-sqlite-datasource
```

## Configure nginx and grafana

An example nginx.conf file can be found in [conf/nginx.conf]

An example /etc/grafana/grafana.ini file can be found in [conf/grafana.ini]

To start the grafana server once, use:

```
sudo /bin/systemctl daemon-reload
sudo /bin/systemctl start grafana-server
sudo /bin/systemctl status grafana-server
```

And to start it every boot:

```
sudo /bin/systemctl enable grafana-server
```



# eht-grafana

This repo contains configuration information to set up a Grafana
server to display data downloaded from vlbimon. The download code is
in the vlbimon-bridge repo.

## Getting a login

Please contact Greg, either via email or EHT Slack (@Greg Lindahl), to ask
for an account. Usernames and passwords are in the same style as
vlbimonitor. Having an account means you can make new dashboards and
charts.

There's also a group login for the AOC, which is read-only.

## How to find interesting plots

If you look in the Dashboards section, you can find dashboards
with charts made by various people. You can also make your own!
Charts have a list of time series on them, and can be applied
to one of the many data sources.

You are encouraged to create your own dashboards and charts.
The best way to learn is to look at existing dashboards -- the
code for them is under the 3 vertical dots icon in the upper right
of every chart.

### What data sources are there?

In addition to a "live.db" dataset which contains a mirror of the
current vlbimonitor data, there are also individual databases
representing single days of previous observations, named by the
experiment name. For example, e24j25.db is the 2024 dress rehearsal.
Also, the old "live" dataset from previous years is renamed to the
year.

### What column names are there?




## If you need to make a new Grafana instance...

### Installing Grafana

I chose to install on Ubuntu from the [Grafana APT repository instructions.](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/#install-from-apt-repository)

This means that the configuration files are in the usual system directories.

I also installed the sqlite plugin:

```
sudo grafana-cli plugins install frser-sqlite-datasource
```

### Configure nginx and grafana

An example nginx.conf file can be found in [conf/nginx.conf]. This configuration
assumes that grafana is on its own subdomain (e.g. grafana.ehtcc.org.)

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

### Database location

The grafana config looks for its databases in the `/var/lib/grafana/` directory.

Note that grafana itself uses the `/var/lib/grafana.db` database to
store configuration information, so do not place any vlbi data in that
database.


previous introduction doc, on google drive greg.lindahl@gmail account
https://docs.google.com/document/d/1Qgits4hJ-XHQcqdGi95dky_BeozCq1bbHfbztNfYn2s/edit?usp=sharing

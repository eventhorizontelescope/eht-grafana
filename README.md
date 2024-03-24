# eht-grafana

The EHT has a monitoring data collection system, and two user interfaces
for it: [VLBI Monitor](https://vlbimon1.science.ru.nl/) and
[Grafana](https://grafana.ehtcc.org/).

This document contains instructions for viewing and creating new
dashboards in Grafana.

During the observation, you can discuss vlbimonitor and Grafana in
the #vlbimonitor Slack channel.

## Screenshots (system temperature and weather)

![alt txt](https://grafana.ehtcc.orgstatic/grafana-system-temp.png)

![alt txt](https://grafana.ehtcc.orgstatic/grafana-weather.png)

## Getting a login

Please contact Greg, either via email or EHT Slack (@Greg Lindahl), to ask
for an account. Usernames and passwords are in the same style as
vlbimonitor. Having your own account means you can make new dashboards and
panels.

There's also a group login for the AOC, which is read-only.

## How to find interesting dashboards

If you look in the Dashboards section (to the left), you can find a
list of all of the dashboards in the system. You can also make your
own! Dashboards are made up of panels, and panels have a list of time
series on them, and can be applied to one of the many data sources.

All of the dashboards at the top level are looking at live vlbimon
data. The dashboards in folders are either using historical data
("Historical Demo") or are prototypes made by other EHT users.

## Creating your own

You are encouraged to create your own dashboards and panels. The best
way to learn what various database queries look like is to look at
existing dashboards -- the code for them is under the 3 vertical dots
icon in the upper right of every panel. The dashboards in production
use are set to read-only, but you can still click on "explore"
see what the current settings are.

You can even change these settings, and save changed panel in your own
new dashboard. Starting from an existing panel is usually the fastest
method of creating a new one.

To create your new panel while exploring, use "Add to dashboard" in
the upper right. Choose "New Dashboard", then "Open". You'll see your
new dashboard with your new panel in it. It won't be saved until you
save it, by using the floppy disk icon in the upper right. But before
that, click on the gear (next to the floppy), change the title, and
select the Prototypes folder.

If you end up with a dashboard named "New dashboard" not in the
Prototypes folder, no worries, just ask on #vlbimon or contact
Greg.

### What are the things you can change?

A panel has a format, usually a time series, an SQL query, and a data
source.

### The query

The SQL query has to match the details of the database, which has a
separate table for every vlbimonitor "parameter", containing all of the stations
in the same table. The columns of this table are the station name, a
time, and the value for that station at that time. As a result, the
main thing you need to specify, for a normal time series showing all
of the stations in a single panel, is the of the parameter. The
rest is just boilerplate.

In this example, the name is `if_1_systemTemp`:

<pre>
SELECT time, station, value from ts_param_<span style="color:blue">if_1_systemTemp</span>
WHERE time >= $__from / 1000 AND time < $__to / 1000 ORDER BY time ASC
</pre>

```text
SELECT time, station, value from ts_param_❗if_1_systemTemp❗
WHERE time >= $__from / 1000 AND time < $__to / 1000 ORDER BY time ASC
```

and if you just wanted one station, KP, add to the WHERE clause:

<pre>
SELECT time, station, value from ts_param_<span style="color:blue">if_1_systemTemp</span>
WHERE time >= $__from / 1000 AND time < $__to / 1000 <span style="color:blue">AND station = 'KP'</span>
ORDER BY time ASC
</pre>



### What column names are there?

This summary shows all of the parameter names, and how many data points
each station has for them:

https://grafana.ehtcc.org/static/summary2023.txt

### What data sources are there?

The production dashboards all use "live.db" as the data source,
which is a real-time updated copy of the vlbimonitor database.

Last year's live.db is renamed to eht2023.db

There are also individual databases representing single days of
previous observations, named by the experiment name. For example,
e24j25.db is the 2024 dress rehearsal.

### Transformers


## Grafana Alerts


## XXX vlbimon-bridge repo


## If you need to make a new Grafana instance...

### Installing Grafana

I chose to install on Ubuntu from the
[Grafana APT repository instructions.](https://grafana.com/docs/grafana/latest/setup-grafana/installation/debian/#install-from-apt-repository)

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

When you add a new database, a Grafana an admin needs to add it to
Connections -> Data Sources before it is visible to users as a datasource.

  make a new chart
  who to ask for help
transfomers exist
  list of them and their column names
  more documentation in vlbimon-bridge repo
  refe
  that transformers run in the bridge
  how to make a new transformer
    debug it in the past
	get a code review from greg
	pull request

document how to add an upper right hand link "explainer"
  go to dashboard
  settings (the gear icon in the upper right) -> links -> + New Link

Flask-InfluxDB
==============
Extension to add InfluxDB support to Flask framework [(external documentation)](https://flask-influxdb.readthedocs.org/en/latest/).

## Installation
Install the extension via *pip*:

```sh
$ pip install Flask-InfluxDB
```

## Set Up
Flask-InfluxDB can be accessed via ``InfluxDB`` class:

```python
from flask import Flask
from flask_influxdb import InfluxDB

app = Flask(__name__)
influx_db = InfluxDB(app=app)
```

Delayed configuration of ``InfluxDB`` is also supported using the **init_app** method:

```python
influx_db = InfluxDB()

app = Flask(__name__)
influxdb.init_app(app=app)
```
This allows to use `InfluxDB` with Flask app factory pattern (check examples).

The `InfluxDB.connection` instance provides the functionality of
`InfluxDBClient`. Additionally there is a simple API to `InfluxDBClient`:
```python
influx = InfluxDB()

influx.query()                      # InfluxDBClient.query()
influx.write()                      # InfluxDBClient.write()
influx.write_points()               # InfluxDBClient.write_points()

influx.user.create()                # InfluxDBClient.create_user()
influx.user.drop()                  # InfluxDBClient.drop_user()
influx.user.switch()                # InfluxDBClient.switch_user()
influx.user.all()                   # InfluxDBClient.get_list_users()

influx.database.drop()              # InfluxDBClient.drop_database()
influx.database.switch()            # InfluxDBClient.switch_database()
influx.database.create()            # InfluxDBClient.create_database()
influx.database.all()               # InfluxDBClient.get_list_database()

influx.measurement.drop()           # InfluxDBClient.drop_measurement()
influx.measurement.all()            # InfluxDBClient.get_list_measurements()
influx.measurement.tag_values()     # Returns tag values for a given key
influx.measurement.tag_keys()       # Returns tag keys in a measurement

```

An included example demonstrates how a database can be created and how data can be written and queried.


## Configuring Flask-InfluxDB
The following configuration values can be set for Flask-InfluxDB extension:

```
INFLUXDB_HOST               Host for the InfluxDB host. Default is localhost.

INFLUXDB_PORT               InfluxDB HTTP API port. Default is 8086.

INFLUXDB_USER               InfluxDB server user. Default is root.

INFLUXDB_PASSWORD           InfluxDB server password. Default is root.

INFLUXDB_DATABASE           Optional database to connect to.  Defaults to None.

INFLUXDB_SSL                Enables using HTTPS instead of http. Defaults to False.

INFLUXDB_VERIFY_SSL         Enables checking HTTPS certificate. Defaults to False.

INFLUXDB_RETRIES            Number of retries your client will try before aborting, 0 indicates try until success.
                            Defaults to 3

INFLUXDB_TIMEOUT            Sets request timeout. Defaults to None.

INFLUXDB_USE_UDP            Use the UDP interfaces instead of http. Defaults to False.

INFLUXDB_UDP_PORT           UDP api port number. Defaults to 4444.

INFLUXDB_PROXIES            HTTP(S) proxy to use for Requests. Defaults to None.

INFLUXDB_POOL_SIZE          urllib3 connection pool size. Defaults to 10.
```
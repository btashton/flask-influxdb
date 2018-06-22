Flask-InfluxDB
==========================================

.. module:: flask_influxdb

Installation
------------

Install the extension via pip::

    $ pip install Flask-InfluxDB

Set Up
------

Influxdb can be accessed via ``InfluxDB`` class::

    from flask import Flask
    from flask_influxdb import InfluxDB

    app = Flask(__name__)
    influx_db = InfluxDB(app=app)

Delayed configuration of ``InfluxDB`` is also supported using the **init_app** method::

    influx_db = Influxdb()

    app = Flask(__name__)
    influxdb.init_app(app=app)

Currently the ``InfluxDB.connection`` instance provides the functionality of ``InfluxDBClient`` . InfluxDB may provide better wrappers to extend this class.

An included example shows how a database can be created and how data can be written and queried.

Configuring Flask-InfluxDB
--------------------------

The following configuration values can be set for Flask-InfluxDB extension:

.. tabularcolumns:: |p{6.5cm|p{8.5cm}|

=============================== ==================================================================
``INFLUXDB_HOST``               Host for the InfluxDB host. Default is localhost.

``INFLUXDB_PORT``               InfluxDB HTTP api port. Default is 8086.

``INFLUXDB_USER``               InfluxDB server user. Default is root.

``INFLUXDB_PASSWORD``           InfluxDB server password. Default is root.

``INFLUXDB_DATABASE``           Optional database to connect to.  Defaults to None.

``INFLUXDB_SSL``                Enables using HTTPS instead of http. Defaults to False.

``INFLUXDB_VERIFY_SSL``         Enables checking HTTPS certificate. Defaults to False.

``INFLUXDB_RETRIES``            Number of retries your client will try before aborting, 0 indicates try until success.
                                Defaults to 3

``INFLUXDB_TIMEOUT``            Sets request timeout. Defaults to None.

``INFLUXDB_USE_UDP``            Use the UDP interfaces instead of http. Defaults to False.

``INFLUXDB_UDP_PORT``           UDP api port number. Defaults to 4444.

``INFLUXDB_PROXIES``            HTTP(S) proxy to use for Requests. Defaults to None.

``INFLUXDB_POOL_SIZE``          urllib3 connection pool size. Defaults to 10.
=============================== ==================================================================
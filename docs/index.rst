Flask-InfluxDB
==========================================

.. module:: flask.ext.influxdb

Installation
------------

Install the extension via pip::

    $ pip install Flask-InfluxDB

Set Up
------

Influxdb is accessed via ``InfluxDB``::

    from flask import Flask
    from flask.ext.influxdb import InfluxDB

    app = Flask(__name__)
    influx_db = InfluxDB(app)

Delayed configuration of ``InfluxDB`` is also support using **init_app** method::

    influx_db = Influxdb()

    app = Flask(__name__)
    influxdb.init_app(app)

Currently the ``InfluxDB.connection`` instance provides the functionality of
``InfluxDBClient`` . InfluxDB may later provide better wrappers to extend this class.

An included examples shows how a database can be created and data written and queried.


Configuring Flask-InfluxDB
--------------------------

The following configuration values exist for Flask-InfluxDB:

.. tabularcolumns:: |p{6.5cm|p{8.5cm}|

=============================== ==================================================================
``INFLUXDB_HOST``               Host for the InfluxDB host. Default is localhost.

``INFLUXDB_PORT``               InfluxDB HTTP api port. Default is 8086.

``INFLUXDB_USER``               InfluxDB server user. Default is root.

``INFLUXDB_PASSWORD``           InfluxDB server password. Default is root.

``INFLUXDB_DATABASE``           Optional database to connect to.  Defaults to None.

``INFLUXDB_SSL``                Enables using HTTPS instead of http. Defaults to False.

``INFLUXDB_VERIFY_SSL``         Enables checking HTTPS certificate. Defaults to False.

``INFLUXDB_TIMEOUT``            Sets request timeout. Defaults to None.

``INFLUXDB_USE_UDP``            Use the UDP interfaces instead of http. Defaults to False.

``INFLUXDB_UDP_PORT``           UDP api port number. Defaults to 4444.

=============================== ==================================================================

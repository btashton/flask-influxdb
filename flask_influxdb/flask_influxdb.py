import influxdb
from flask import current_app, _app_ctx_stack, Flask
from flask.globals import _app_ctx_err_msg
from typing import Generator

_no_influx_msg = """\
No Influx connection is present.

This means that something has overwritten _app_ctx_stack.top.influxdb_db.
"""


class InfluxDB(object):
    def __init__(self, app: Flask = None) -> None:
        """
        Class constructor
        :param app: Flask Application object
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        """
        Initialize extension for application
        :param app: Flask Application object
        :return:
        """
        app.config.setdefault('INFLUXDB_HOST', 'localhost')
        app.config.setdefault('INFLUXDB_PORT', '8086')
        app.config.setdefault('INFLUXDB_USER', 'root')
        app.config.setdefault('INFLUXDB_PASSWORD', 'root')
        app.config.setdefault('INFLUXDB_DATABASE', None)
        app.config.setdefault('INFLUXDB_SSL', False)
        app.config.setdefault('INFLUXDB_VERIFY_SSL', False)
        app.config.setdefault('INFLUXDB_RETRIES', 3)
        app.config.setdefault('INFLUXDB_TIMEOUT', None)
        app.config.setdefault('INFLUXDB_USE_UDP', False)
        app.config.setdefault('INFLUXDB_UDP_PORT', 4444)
        app.config.setdefault('INFLUXDB_PROXIES', None)
        app.config.setdefault('INFLUXDB_POOL_SIZE', 10)

        app.teardown_appcontext(self.teardown)

        with app.app_context():
            database = app.config['INFLUXDB_DATABASE']
            if database is not None:
                self.database.create(database)

    @staticmethod
    def connect() -> influxdb.InfluxDBClient:
        """
        Connect to InfluxDB using configuration parameters
        :return: InfluxDBClient object
        """
        return influxdb.InfluxDBClient(
            host=current_app.config['INFLUXDB_HOST'],
            port=current_app.config['INFLUXDB_PORT'],
            username=current_app.config['INFLUXDB_USER'],
            password=current_app.config['INFLUXDB_PASSWORD'],
            database=current_app.config['INFLUXDB_DATABASE'],
            ssl=current_app.config['INFLUXDB_SSL'],
            verify_ssl=current_app.config['INFLUXDB_VERIFY_SSL'],
            timeout=current_app.config['INFLUXDB_TIMEOUT'],
            retries=current_app.config['INFLUXDB_RETRIES'],
            use_udp=current_app.config['INFLUXDB_USE_UDP'],
            udp_port=current_app.config['INFLUXDB_UDP_PORT'],
            proxies=current_app.config['INFLUXDB_PROXIES'],
            pool_size=current_app.config['INFLUXDB_POOL_SIZE']
        )

    @staticmethod
    def teardown(exception) -> None:
        """
        This is really a sub in case a influxdb input actually does need
        to be able to be torn down
        """
        ctx = _app_ctx_stack.top
        if hasattr(ctx, 'influxdb_db') and ctx.influxdb_db is not None:
            ctx.influxdb_db.close()

    @property
    def connection(self) -> influxdb.InfluxDBClient:
        """
        InfluxDBClient object
        :return:
        """
        ctx = _app_ctx_stack.top
        if ctx is None:
            raise RuntimeError(_app_ctx_err_msg)

        if not hasattr(ctx, 'influxdb_db'):
            ctx.influxdb_db = self.connect()

        if ctx.influxdb_db is None:
            raise RuntimeError(_no_influx_msg)

        return ctx.influxdb_db

    @property
    def close(self) -> callable:
        return self.connection.close

    @property
    def query(self) -> callable:
        return self.connection.query

    @property
    def write(self) -> callable:
        return self.connection.write

    @property
    def write_points(self) -> callable:
        return self.connection.write_points

    @property
    def database(self):
        class Database:
            switch = self.connection.switch_database
            create = self.connection.create_database
            drop = self.connection.drop_database
            all = self.connection.get_list_database

        return Database()

    @property
    def user(self):
        class User:
            switch = self.connection.switch_user
            create = self.connection.create_user
            drop = self.connection.drop_user
            all = self.connection.get_list_users
            password = self.connection.set_user_password

        return User()

    @property
    def policy(self):
        class RetentionPolicy:
            alter = self.connection.alter_retention_policy
            create = self.connection.create_retention_policy
            drop = self.connection.drop_retention_policy
            all = self.connection.get_list_retention_policies

        return RetentionPolicy()

    @property
    def measurement(self):
        class Measurement:
            tag_values = self._tag_values
            tag_keys = self._tag_keys
            drop = self.connection.drop_measurement
            all = self.connection.get_list_measurements

        return Measurement()

    def _tag_values(self,
                    measurement: str,
                    key: str,
                    *args, **kwargs) -> Generator:
        """
        Returns generator with tag's values for measurement.
        :param measurement: name of the measurement
        :param key: tag key
        :return:
        """
        conn = self.connection
        q = f"SHOW TAG VALUES ON {conn._database} FROM {measurement} WITH KEY = {key}"
        result = conn.query(query=q, *args, **kwargs)
        values = (p['value'] for p in result.get_points())
        return values

    def _tag_keys(self,
                  measurement: str,
                  *args, **kwargs) -> Generator:
        """
        Returns generator with tag's keys for measurement.
        :param measurement: name of the measurement
        :return:
        """
        conn = self.connection
        q = f'SHOW TAG KEYS ON {conn._database} FROM {measurement}'
        result = conn.query(query=q, *args, **kwargs)
        keys = (p['tagKey'] for p in result.get_points())
        return keys

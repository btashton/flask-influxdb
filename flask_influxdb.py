import influxdb
from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class InfluxDB(object):
    def __init__(self, app=None):
        """
        Class constructor
        :param app: Flask Application object
        """
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
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

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
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

    def teardown(self, exception):
        """This is really a sub in case a influxdb input actually does need
        to be able to be torn down"""
        ctx = stack.top
        if hasattr(ctx, 'influxdb_db'):
            ctx.influxdb_db = None

    @property
    def connection(self):
        """
        InfluxDBClient object
        :return:
        """
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'influxdb_db'):
                ctx.influxdb_db = self.connect()
            return ctx.influxdb_db

import influxdb
from flask import current_app

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class InfluxDB(object):

    def __init__(self, app=None):
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        app.config.setdefault('INFLUXDB_HOST','localhost')
        app.config.setdefault('INFLUXDB_PORT','8086')
        app.config.setdefault('INFLUXDB_USER','root')
        app.config.setdefault('INFLUXDB_PASSWORD','root')
        app.config.setdefault('INFLUXDB_DATABASE',None)
        app.config.setdefault('INFLUXDB_SSL',False)
        app.config.setdefault('INFLUXDB_VERIFY_SSL',False)
        app.config.setdefault('INFLUXDB_TIMEOUT',None)
        app.config.setdefault('INFLUXDB_USE_UDP',False)
        app.config.setdefault('INFLUXDB_UDP_PORT',4444)

        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

    def connect(self):
        return influxdb.InfluxDBClient(current_app.config['INFLUXDB_HOST'],
                                       current_app.config['INFLUXDB_PORT'],
                                       current_app.config['INFLUXDB_USER'],
                                       current_app.config['INFLUXDB_PASSWORD'],
                                       current_app.config['INFLUXDB_DATABASE'],
                                       current_app.config['INFLUXDB_SSL'],
                                       current_app.config['INFLUXDB_VERIFY_SSL'],
                                       current_app.config['INFLUXDB_TIMEOUT'],
                                       current_app.config['INFLUXDB_USE_UDP'],
                                       current_app.config['INFLUXDB_UDP_PORT'])
    def teardown(self, exception):
        """This is really a sub in case a influxdb input actually does need
        to be able to be torn down"""
        ctx = stack.top
        if hasattr(ctx, 'influxdb_db'):
            ctx.influxdb_db = None

    @property
    def connection(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 'influxdb_db'):
                ctx.influxdb_db = self.connect()
            return ctx.influxdb_db

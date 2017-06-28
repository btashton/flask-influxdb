import influxdb

try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack


class InfluxDB(object):
    def __init__(self, app=None):
        self.client_init_kwargs = {}
        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        if hasattr(app, 'teardown_appcontext'):
            app.teardown_appcontext(self.teardown)
        else:
            app.teardown_request(self.teardown)

        # Create init kwargs for InfluxDBClient by transforming all
        # INFLUXDB_X = Y directives to a dict with: {X.lower(): Y}
        for k, v in app.config.items():
            if k.startswith('INFLUXDB_'):
                self.client_init_kwargs[
                    k.replace('INFLUXDB_', '').lower()] = v

    def connect(self):
        return influxdb.InfluxDBClient(**self.client_init_kwargs)

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

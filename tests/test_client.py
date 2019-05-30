import pytest
import influxdb
import types

from flask import _app_ctx_stack
from flask.globals import _app_ctx_err_msg

from flask_influxdb.flask_influxdb import _no_influx_msg


class TestBase:
    def test_outside_ctx(self, influx):
        with pytest.raises(RuntimeError) as excinfo:
            influx.measurement.all()

        assert str(excinfo.value) == _app_ctx_err_msg

    def test_overwrite_influxdb(self, app_no_cleanup, influx):
        app = app_no_cleanup

        with app.ctx as ctx, pytest.raises(RuntimeError) as excinfo:
            ctx = _app_ctx_stack.top
            ctx.influxdb_db = None
            influx.measurement.all()

        assert str(excinfo.value) == _no_influx_msg

    def test_instance(self, app, influx):
        with app.ctx:
            influx.measurement.all()

            ctx = _app_ctx_stack.top
            flux = ctx.influxdb_db

        assert isinstance(flux, influxdb.InfluxDBClient)


class TestAPI:
    def test_base(self, app, influx):
        with app.ctx:
            assert hasattr(influx, 'close')
            assert hasattr(influx, 'query')
            assert hasattr(influx, 'write')
            assert hasattr(influx, 'write_points')
            assert hasattr(influx, 'database')
            assert hasattr(influx, 'user')
            assert hasattr(influx, 'write')
            assert hasattr(influx, 'policy')
            assert hasattr(influx, 'measurement')

    def test_database(self, app, influx):
        with app.ctx:
            assert hasattr(influx.database, 'create')
            assert hasattr(influx.database, 'drop')
            assert hasattr(influx.database, 'switch')
            assert hasattr(influx.database, 'all')

    def test_measurement(self, app, influx):
        with app.ctx:
            assert hasattr(influx.measurement, 'drop')
            assert hasattr(influx.measurement, 'all')
            assert hasattr(influx.measurement, 'tag_values')
            assert hasattr(influx.measurement, 'tag_keys')

    def test_user(self, app, influx):
        with app.ctx:
            assert hasattr(influx.user, 'create')
            assert hasattr(influx.user, 'drop')
            assert hasattr(influx.user, 'switch')
            assert hasattr(influx.user, 'all')
            assert hasattr(influx.user, 'password')

    def test_policy(self, app, influx):
        with app.ctx:
            assert hasattr(influx.policy, 'create')
            assert hasattr(influx.policy, 'drop')
            assert hasattr(influx.policy, 'alter')
            assert hasattr(influx.policy, 'all')


class TestTags:
    def test_values(self, app, influx):
        measurement = 'test_tags'
        points = [
            {
                "fields": {'index': 1},
                "tags": {'info': 'test1'},
                "measurement": measurement
            },
            {
                "fields": {'index': 2},
                "tags": {'info': 'test2'},
                "measurement": measurement
            }
        ]

        with app.ctx:
            influx.write_points(points)
            result = influx.measurement.tag_values(measurement=measurement, key='info')

        assert isinstance(result, types.GeneratorType)

        result = list(result)
        assert len(result) == 2
        assert 'test1' in result
        assert 'test2' in result

    def test_keys(self, app, influx):
        measurement = 'test_tags'
        points = [
            {
                "fields": {'index': 1},
                "tags": {'info': 'test1'},
                "measurement": measurement
            },
            {
                "fields": {'index': 2},
                "tags": {'info': 'test2'},
                "measurement": measurement
            }
        ]

        with app.ctx:
            influx.write_points(points)
            result = influx.measurement.tag_keys(measurement=measurement)

        assert isinstance(result, types.GeneratorType)
        assert list(result) == ['info']


class TestApp:
    def test_response(self, app):
        result = app.client.get('add/test2/1')

        assert result.status_code == 200

        response = result.get_json()
        assert 'result' in response.keys()
        assert response['result'] is True

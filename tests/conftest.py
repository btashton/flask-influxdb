import pytest
import os
from collections import namedtuple
from flask import Flask, jsonify
from flask_influxdb import InfluxDB


App = namedtuple("App", ["ctx", "client"])

influx_db = InfluxDB()


def create_app(config: str) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(config)

    influx_db.init_app(app)

    @app.route("/add/<measurement>/<idx>")
    def write(measurement: str, idx: int):
        result = influx_db.write_points(
            [
                {
                    "fields": {
                        "index": idx,
                    },
                    "tags": {
                        "info": "test",
                    },
                    "measurement": measurement,
                }
            ]
        )

        return jsonify(result=result)

    return app


@pytest.fixture(scope="session")
def influx():
    return influx_db


@pytest.fixture()
def app(request):
    """Session-wide test application."""
    rel_dir = os.path.dirname(__file__)
    config = os.path.join(rel_dir, "config.cfg")

    # Create app
    app = create_app(config)

    client = app.test_client()
    ctx = app.app_context()

    yield App(ctx, client)

    # Cleanup
    with ctx:
        influx_db.database.drop("test")


@pytest.fixture()
def app_no_cleanup(request):
    """Session-wide test application."""
    rel_dir = os.path.dirname(__file__)
    config = os.path.join(rel_dir, "config.cfg")

    # Create app
    app = create_app(config)

    client = app.test_client()
    ctx = app.app_context()

    yield App(ctx, client)

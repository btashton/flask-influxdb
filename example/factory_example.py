from flask_influxdb import InfluxDB
from flask import Flask, render_template

influx = InfluxDB()


def create_app(config: str) -> Flask:
    app = Flask(__name__)
    app.config.from_pyfile(config)

    influx.init_app(app)

    @app.route("/newdb/<dbname>")
    def newdb(dbname):
        influx.database.create(dbname)
        return ""

    @app.route("/example")
    def write():
        data_measurement = "testseries"
        data_tags = ["time", "value_1", "value_2", "value_3"]

        influx.database.switch(database="test")
        tabledata = influx.query(
            "SELECT {0} from {1}".format(", ".join(data_tags), data_measurement)
        )

        data_points = []
        for measurement, tags in tabledata.keys():
            for p in tabledata.get_points(measurement=measurement, tags=tags):
                data_points.append(p)

        return render_template(
            "table.html",
            measurement=data_measurement,
            columns=data_tags,
            points=data_points,
        )

    return app


if __name__ == "__main__":
    import random

    app = create_app("example.cfg")

    # Insert sample data
    points = [
        {
            "fields": {"value_1": 0.5, "value_2": 1, "value_3": random.random()},
            "tags": {"tag_1": "tag_string1", "tag_2": "tag_string2"},
            "measurement": "testseries",
        }
    ]

    # Remember to work inside the context
    with app.app_context():
        influx.database.switch(database="test")
        influx.write_points(points)

    app.run()

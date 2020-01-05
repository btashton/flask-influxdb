from flask_influxdb import InfluxDB
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile("example.cfg")
influx_db = InfluxDB(app=app)


@app.route("/newdb/<dbname>")
def newdb(dbname):
    influx_db.database.create(dbname)
    return "Database {} created".format(dbname)


@app.route("/write/<dbname>")
def write(dbname):
    data_measurement = "testseries"
    data_tags = ["time", "value_1", "value_2", "value_3"]

    influx_db.database.switch(database=dbname)
    influx_db.write_points(
        [
            {
                "fields": {"value_1": 0.5, "value_2": 1, "value_3": 1.8858},
                "tags": {"tag_1": "tag_string1", "tag_2": "tag_string2"},
                "measurement": "testseries",
            }
        ]
    )
    tabledata = influx_db.query(
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


app.run()

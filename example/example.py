from flask_influxdb import InfluxDB
from flask import Flask, render_template

app = Flask(__name__)
app.config.from_pyfile('example.cfg')
influx_db = InfluxDB(app=app)


@app.route('/newdb/<dbname>')
def newdb(dbname):
    dbcon = influx_db.connection
    dbcon.create_database(dbname)
    return ''


@app.route('/write/<dbname>')
def write(dbname):
    data_measurement = 'testseries'
    data_tags = ['time', 'value_1', 'value_2', 'value_3']

    dbcon = influx_db.connection
    dbcon.switch_database(database=dbname)
    dbcon.write_points([
        {
            "fields": {
                'value_1': 0.5,
                'value_2': 1,
                'value_3': 1.8858
            },
            "tags": {
                'tag_1': 'tag_string',
                'tag_2': 'tag_string'
            },
            "measurement": "testseries"
        }
    ])
    tabledata = dbcon.query('SELECT {0} from {1}'.format(', '.join(data_tags), data_measurement))

    data_points = []
    for measurement, tags in tabledata.keys():
        for p in tabledata.get_points(measurement=measurement, tags=tags):
            data_points.append(p)

    return render_template('table.html',
                           measurement=data_measurement,
                           columns=data_tags,
                           points=data_points)


app.run()

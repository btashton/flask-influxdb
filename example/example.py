from flask import Flask, render_template
from flask.ext.influxdb import InfluxDB


app = Flask(__name__)
app.config.from_pyfile('example.cfg')
influx_db = InfluxDB(app)

@app.route('/newdb/<dbname>')
def newdb(dbname):
    dbcon = influx_db.connection
    dbcon.create_database(dbname)

@app.route('/write/<dbname>')
def write(dbname):
    dbcon = influx_db.connection
    dbcon.switch_db(dbname)
    dbcon.write_points([{"points":[[1],[2],[3]],"name":"testseries","columns":["value"]}])
    tabledata = dbcon.query('select value from testseries;')
    return render_template('table.html',data=tabledata[0])
app.run()

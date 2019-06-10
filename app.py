from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from random import randrange
import csv
import pyodbc
from datetime import datetime, timedelta
import time
from math import sin, cos, sqrt, atan2, radians
db_uid=''
db_pwd=''
db_server=''
db_database=''
sql_config = """Driver=ODBC Driver 17 for SQL Server;
                      Server={};
                      Database={};
                      Trusted_Connection=no;
                      UID={};
                      PWD={};""".format(db_server,db_database,db_uid,db_pwd)

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
Bootstrap(app)


def get_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    dlon = radians(abs(lon2)) - radians(abs(lon1))
    dlat = radians(abs(lat2)) - radians(abs(lat1))
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance


def set_generator(min=10, max=40, count=10):
    data_list = []
    for i in range(0, count):
        data_list.append(randrange(min, max))
    return data_list


def csv_to_list(path):
    with open(path, 'r') as f:
        reader = csv.reader(f)
        temp = list(reader)
    return temp


def get_sensor_data():
    temp_list = []
    with pyodbc.connect(sql_config) as conn:
        with conn.cursor() as cursor:
            probe_cur = cursor.execute('select name from probes')
            probe_list = probe_cur.fetchall()
            for x in probe_list:
                c = cursor.execute('select top 1 * from sensors where probe_name = ? order by id desc', x[0])
                d = list(c.fetchall())
                temp_list.append(d)
    return temp_list


def get_probe_data():
    with pyodbc.connect(sql_config) as conn:
        with conn.cursor() as cursor:
            probe_cur = cursor.execute('select * from probes')
            probe_list = probe_cur.fetchall()
    return probe_list


def get_sensor_probe_data():
    result_list = []
    with pyodbc.connect(sql_config) as conn:
        with conn.cursor() as cursor:
            probe_cur = cursor.execute('select name from probes')
            probe_list = probe_cur.fetchall()
            for x in probe_list:
                result_cur = cursor.execute("""SELECT top 1 Probes.name, Probes.last_lat,Probes.last_lng, temperature,
                    humidity, pressure,Probes.last_seen
                    FROM Sensors
                    LEFT JOIN Probes
                    ON Sensors.probe_name = Probes.name
                    WHERE name = ?
                    order by id desc;""", (x[0],))
                d = result_cur.fetchall()
                result_list.extend(d)
            return result_list

def get_column_data(column, flag, start, end):
    with pyodbc.connect(sql_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute('select ' + flag + '(' + column + ') from sensors where timestamp between ? and ?',
                           (start, end))
            data = cursor.fetchval()
    return data

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r

@app.route('/')
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/map')
def map():
    probes = get_probe_data()
    sensors = get_sensor_data()
    return render_template('map.html', probes=probes, sensors=sensors)

@app.route('/status')
def status():
    # ('probe_01', -33.8333, 151.017, 47.5, 27.98, 1027.09, datetime.datetime(2019, 5, 13, 23, 11, 46, 137000))
    sensor_probe = get_sensor_probe_data()
    status_list = []
    for probe in sensor_probe:
        recal_temp = 0
        recal_humid = 0
        recal_pressure = 0
        if (datetime.now()-probe[6]).total_seconds() > 360:
            state = 'OFFLINE'
        else:
            state = 'ONLINE'
        for p in sensor_probe:
            distance = get_distance(probe[1], probe[2], p[1], p[2])
            if distance < 8 and not distance == 0:
                if abs(probe[3]-p[3]) > 5:
                    recal_temp +=1
                if abs(probe[4]-p[4]) > 5:
                    recal_humid +=1
                if abs(probe[5]-p[5]) > 5:
                    recal_pressure +=1
        if recal_temp > 1:
            recal_temp = 'BAD'
        else:
            recal_temp = 'GOOD'
        if recal_humid > 1:
            recal_humid = 'BAD'
        else:
            recal_humid = 'GOOD'
        if recal_pressure > 1:
            recal_pressure = 'BAD'
        else:
            recal_pressure = 'GOOD'
        status_list.append([probe[0], state, recal_temp, recal_humid, recal_pressure])
    return render_template('status.html', status_list=status_list)

@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/realtime')
def realtime():
    sensor = get_sensor_data()
    return render_template('realtime.html', sensor=sensor)


@app.route('/chart')
def chart():
    labels = []
    low_temp = []
    high_temp = []
    mid_temp = []
    low_humid = []
    high_humid = []
    mid_humid = []
    low_pres = []
    high_pres = []
    mid_pres = []
    last_7d = datetime.now().date() - timedelta(days=6)
    # range of data, for our use we check last 7days
    for i in range(0, 7):
        labels.append((last_7d + timedelta(days=i)).strftime('%a %Y-%m-%d'))
        low_temp.append(
            get_column_data('temperature', 'min', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        high_temp.append(
            get_column_data('temperature', 'max', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        mid_temp.append(
            get_column_data('temperature', 'avg', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        low_humid.append(
            get_column_data('humidity', 'min', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        high_humid.append(
            get_column_data('humidity', 'max', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        mid_humid.append(
            get_column_data('humidity', 'avg', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        low_pres.append(
            get_column_data('pressure', 'min', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        high_pres.append(
            get_column_data('pressure', 'max', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))
        mid_pres.append(
            get_column_data('pressure', 'avg', last_7d + timedelta(days=i), last_7d + timedelta(days=i + 1)))

    data_set = {'labels': labels,
                'temp': {'low': low_temp,
                         'mid': mid_temp,
                         'high': high_temp},
                'humidity': {'low': low_humid,
                             'mid': mid_humid,
                             'high': high_humid},
                'pressure': {'low': low_pres,
                             'mid': mid_pres,
                             'high': high_pres}}
    return render_template('chart.html', data_set=data_set)


if __name__ == '__main__':
    app.run(host='0.0.0.0')


from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from random import randrange
import csv
import pyodbc
from datetime import datetime, timedelta
sql_config = """Driver=ODBC Driver 17 for SQL Server;
                      Server=182.161.64.23,1433;
                      Database=utms;
                      Trusted_Connection=no;
                      UID=sa;
                      PWD=fjh&*3k.xc*2nm;"""


app = Flask(__name__)
Bootstrap(app)

def set_generator(min=10,max=40,count=10):
    data_list = []
    for i in range(0,count):
        data_list.append(randrange(min,max))
    return data_list

def csv_to_list(path):
    with open (path, 'r') as f:
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

def get_column_data(column,flag,start,end):
    with pyodbc.connect(sql_config) as conn:
        with conn.cursor() as cursor:
            cursor.execute('select '+flag+'('+column+') from sensors where timestamp between ? and ?', (start, end))
            data = cursor.fetchval()
    return data

@app.route('/')
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/map')
def map():
    probes = get_probe_data()
    sensors = get_sensor_data()
    return render_template('map.html',probes=probes,sensors=sensors)

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/realtime')
def realtime():
    sensor = get_sensor_data()
    return render_template('realtime.html',sensor=sensor)

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
    for i in range(0,7):
        labels.append((last_7d+timedelta(days=i)).strftime('%a %Y-%m-%d'))
        low_temp.append(get_column_data('temperature','min',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        high_temp.append(get_column_data('temperature','max',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        mid_temp.append(get_column_data('temperature','avg',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        low_humid.append(get_column_data('humidity','min',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        high_humid.append(get_column_data('humidity','max',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        mid_humid.append(get_column_data('humidity','avg',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        low_pres.append(get_column_data('pressure','min',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        high_pres.append(get_column_data('pressure','max',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))
        mid_pres.append(get_column_data('pressure','avg',last_7d+timedelta(days=i),last_7d+timedelta(days=i+1)))

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
    return render_template('chart.html',data_set=data_set)


if __name__ == '__main__':
    app.run(debug=True)
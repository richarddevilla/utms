from flask import Flask, render_template, url_for
from flask_bootstrap import Bootstrap
from random import randrange
import csv

app = Flask(__name__)
Bootstrap(app)

weekly_label = ['Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday']


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




@app.route('/')
@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/map')
def map():
    probes = csv_to_list('probe.csv')
    return render_template('map.html',probes=probes)

@app.route('/team')
def team():
    return render_template('team.html')

@app.route('/realtime')
def realtime():
    sensor = csv_to_list('sensor.csv')
    return render_template('realtime.html',sensor=sensor)

@app.route('/chart')
def chart():
    set_A1 = set_generator(min=0, max=10)
    set_B1 = set_generator(min=11, max=20)
    set_C1 = set_generator(min=21, max=30)
    set_A2 = set_generator(min=30, max=35)
    set_B2 = set_generator(min=35, max=40)
    set_C2 = set_generator(min=40, max=45)
    set_A3 = set_generator(min=1000, max=1005)
    set_B3 = set_generator(min=1005, max=1010)
    set_C3 = set_generator(min=1010, max=1015)
    data_set = {'labels': weekly_label,
                'temp': {'low': set_A1,
                         'mid': set_B1,
                         'high': set_C1},
                'humidity': {'low': set_A2,
                             'mid': set_B2,
                             'high': set_C2},
                'pressure': {'low': set_A3,
                             'mid': set_B3,
                             'high': set_C3}}
    return render_template('chart.html',data_set=data_set)

@app.route('/test')
def test():
    set_A1 = set_generator(min=0,max=10)
    set_B1 = set_generator(min=11,max=20)
    set_C1 = set_generator(min=21,max=30)
    set_A2 = set_generator(min=30, max=35)
    set_B2 = set_generator(min=35, max=40)
    set_C2 = set_generator(min=40, max=45)
    set_A3 = set_generator(min=1000, max=1005)
    set_B3 = set_generator(min=1005, max=1010)
    set_C3 = set_generator(min=1010, max=1015)
    data_set = {'labels':weekly_label,
                'temp':{'low':set_A1,
                        'mid':set_B1,
                        'high':set_C1},
                'humidity':{'low': set_A2,
                         'mid': set_B2,
                         'high': set_C2},
                'pressure':{'low': set_A3,
                         'mid': set_B3,
                         'high': set_C3}}

    return render_template('test.html',data_set=data_set)

if __name__ == '__main__':
    app.run(host = '0.0.0.0')
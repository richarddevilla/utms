import pyodbc
import csv
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=utms.tk,1433;'
                      'Database=utms;'
                      'Trusted_Connection=No;'
                      'UID=sa;'
                      'PWD=fjh&*3k.xc*2nm;')
with open('probe.csv', 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        print(', '.join(row))

cursor = conn.cursor()
cursor.execute('show tables;')
#fdfed3r1gfs4e	Jdl39)j3mnd73mD3@
#'UID=sa;'
#'PWD=fjh&*3k.xc*2nm;')
for row in cursor:
    print(row)
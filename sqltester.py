import pyodbc
import time

while True:
    conn = pyodbc.connect('ServerName=mssql;Driver=FreeTDS;PORT=1433;Database=utms;UID=sa;PWD=fjh&*3k.xc*2nm;')
    cursor = conn.cursor()
    conn.close()
    print('Connected...')
    time.sleep(10)
import pyodbc

conn = pyodbc.connect('Driver=ODBC Driver 17 for SQL Server;'
                      'Server=utms.tk,1433;'
                      'Database=utms;'
                      'Trusted_Connection=no;'
                      'UID=sa;'
                      'PWD=fjh&*3k.xc*2nm;')
cursor = conn.cursor()



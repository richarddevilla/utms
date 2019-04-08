import pyodbc

conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                      'Server=utms.tk,1433;'
                      'Database=utms;'
                      'Trusted_Connection=no;'
                      'UID=sa;'
                      'PWD=fjh&*3k.xc*2nm;')
                      #'UID=utmsadministrator;'
                      #'PWD=jklHD73Lhs#F#;'
                      #'Authentication = ActiveDirectoryPassword')
cursor = conn.cursor()

cursor.execute('show tables;')
#fdfed3r1gfs4e	Jdl39)j3mnd73mD3@
#'UID=sa;'
#'PWD=fjh&*3k.xc*2nm;')

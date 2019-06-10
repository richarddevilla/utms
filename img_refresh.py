import pyodbc
import time
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

def save_image(probe):
    with open('static\\img\\'+probe[0]+'.jpg', 'wb') as output_file:
        output_file.write(probe[-1])
        
def get_probe_data():
    with pyodbc.connect(sql_config) as conn:
        with conn.cursor() as cursor:
            probe_cur = cursor.execute('SET TEXTSIZE 2147483647 select * from probes')
            probe_list = probe_cur.fetchall()
            for probe in probe_list:
                save_image(probe)
    return probe_list
while 1:
    get_probe_data()
    print('refreshing...')
    time.sleep(120)

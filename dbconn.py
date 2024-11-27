import getpass
import traceback

import oracledb as bd

global connection, cursor, res

user = 'onlyread'
oraclepwd = 'read'
serveraddrs = 'BRCWBVR136/magnofarm'

try:
    connection = bd.connect(user=user, password=oraclepwd, dsn=serveraddrs)
    cursor = connection.cursor()
    cursor.execute("""SELECT endpoints.LASTPACKETRECEIVED, endpointdata.METERNO, endpoints.LASTPROGRAMDATE, endpoints.LASTSTATUSCHANGED
                    FROM CENTRALSERVICES.ENDPOINTS endpoints 
                    JOIN CENTRALSERVICES.ENDPOINTDATA endpointdata
                    USING (SERIALNUMBER) where METERNO = '40056591'""")

    res = cursor.fetchall()

    for row in res:
        print(row)

except bd.Error as e:
    error, = e.args
    traceback.print_tb(e.__traceback__)
    print(error.message)




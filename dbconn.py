import getpass
import traceback
import files.var.globalVar as var

import oracledb as bd

global connection, cursor, res

queryDb = """SELECT endpoints.LASTPACKETRECEIVED, endpointdata.METERNO, endpoints.LASTPROGRAMDATE, endpoints.LASTSTATUSCHANGED
          FROM CENTRALSERVICES.ENDPOINTS endpoints 
          JOIN CENTRALSERVICES.ENDPOINTDATA endpointdata
          USING (SERIALNUMBER) where METERNO = :lanID"""

def getMeterlastpackage(lanId):

    if lanId != '':
        try:
            connection = bd.connect(user=var.user, password=var.oraclepwd, dsn=var.serveraddrs)
            cursor = connection.cursor()
            cursor.execute(queryDb,[str(lanId)])

            res = cursor.fetchall()

            for row in res:
                print('BDmessage response:\n',row)
            return res

        except bd.Error as e:
            error, = e.args
            traceback.print_tb(e.__traceback__)
            print(error.message)




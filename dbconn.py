import getpass
import traceback
import files.var.globalVar as var

import oracledb as bd

global connection, cursor, res

queryDb = """SELECT endpoints.LASTPACKETRECEIVED, endpointdata.METERNO, endpoints.LASTPROGRAMDATE, endpoints.LASTSTATUSCHANGED
          FROM CENTRALSERVICES.ENDPOINTS endpoints 
          JOIN CENTRALSERVICES.ENDPOINTDATA endpointdata
          USING (SERIALNUMBER) where METERNO = :lanID"""

queryDb1 = """SELECT SERIALNO, PARENTSERIALNO, SLOTNO, PHASE, LASTUPDATEDDATE
              FROM CENTRALSERVICES.METERCHILDREN chield
              where chield.PARENTSERIALNO LIKE :lanID"""

def getMeterlastpackage(lanId):
    if lanId != '':
        try:
            connection = bd.connect(user=var.user, password=var.oraclepwd, dsn=var.serveraddrs)
            cursor = connection.cursor()
            cursor.execute(queryDb,[str(lanId)])

            res = cursor.fetchall()
            # for row in res:
            #     print('BDmessage response:\n',row)
            return res

        except bd.Error as e:
            error, = e.args
            traceback.print_tb(e.__traceback__)
            print(error.message)

def checkLastPackage(lastpackageReceived, hora, minuto):
    dateTimenow = datetime.datetime.now().strftime('%y-%m-%d %H:%M')
    lastpackageReceived = lastpackageReceived.strftime('%y-%m-%d %H:%M')
    FMT = '%y-%m-%d %H:%M'

    print('Tempo sistema: ' + dateTimenow)
    print('Tempo ultimo pacote: ' + lastpackageReceived)

    timedif = datetime.datetime.strptime(dateTimenow, FMT) - datetime.datetime.strptime(lastpackageReceived, FMT)

    print(timedif)

    if timedelta(hours=hora, minutes=minuto) <= timedif:
        print('Tempo execedido')
        return True
    else:
        print('Pacote recebido')
        return False

def getMeterEndpointParent(lanId):
    if lanId != '':
        try:
            connection = bd.connect(user=var.user, password=var.oraclepwd, dsn=var.serveraddrs)
            cursor = connection.cursor()
            cursor.execute(queryDb1,[str(lanId)])

            res = cursor.fetchall()
            # for row in res:
            #     print('BDmessage response:\n',row)
            return res

        except bd.Error as e:
            error, = e.args
            traceback.print_tb(e.__traceback__)
            print(error.message)
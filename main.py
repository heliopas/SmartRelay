#python imports
import datetime
import time
from datetime import timedelta
from idlelib.debugger_r import restart_subprocess_debugger
import serial
import errno
from colorama import Fore, Back, Style
from time import sleep
import logging
import csv

#internal classes imports
import dbconn
import serialLayer
import metercpuFormater as mmmifileFormater
import readwriteFiles
import chromeAutomation

                                  ######switch de testes#######

#switch de teste para gerar outages 'Relay box' e pegar do banco de dados o tempo de recebimento do ultimo pacote do CC
def checkLastPackage():
    serialLayer.openportRelayBox()

    landId = ['40056591', '40056589', '400565B0', '4005957B', '40056596', '400565EE']

    # variaveis de controle da aplicação
    aux = True
    checkpackageReceived = True
    outageEnable = True

    while aux:

        if outageEnable is True:  # variavel de controle gera outage só depois das CPUS receberem algum pacote no CC
            serialLayer.openRelayBox_ch1()
            print('Relay aberto!!!')
            # logging.info("interation: %d" % aux)
            sleep(250)  # 250, desligado por 4 minutos
            serialLayer.closeRelayBox_ch1()
            print('                 Relay fechado!!!')
            sleep(600)  # 1200, ligado 25 min

        checkpackageReceived = True

        for row in landId:
            if checkpackageReceived is False:
                break

            dbreturn = dbconn.getMeterlastpackage(row)
            for row in dbreturn:
                print(row)
                if dbconn.checkLastPackage(row[0], 0, 15) == True:
                    checkpackageReceived = False
                    outageEnable = False
                    sleep(120)  # espera 2 minutos para realizar leitura novamente do recebimento dos pacotes
                    break
                else:
                    checkpackageReceived = True  # executa outage se todas CPU enviaram algum pacote para o CC
                    outageEnable = True

# cria csv de importação para meter e CPU baseado na lista de enpoints
def metercpuFormater():
    mmmifileFormater.generateMMIMMcsvFile()

#obtem lista de medidores a partir de lanIds das cpus cadastradas no arquivo cpumeter/endpointcpu.txt
def getmetersbyLanIDfromBD():
    meters = []
    endpointsIds = readwriteFiles.getendpoint()
    #obtem quantidade de endpoints
    #print(len(endpointsIds))
    #print(len(dbconn.getMeterEndpointParent(int(endpointsIds[0], 16))))
    #print(dbconn.getMeterEndpointParent(int(endpointsIds[0], 16))[0][0])
    #print(dbconn.getMeterEndpointParent(int(endpointsIds[0], 16))[1][0])

    #coleta medidores baseado no lanID da CPU
    for aux in range(len(endpointsIds)):
       for aux1 in range(len(dbconn.getMeterEndpointParent(int(endpointsIds[aux], 16)))):
           meters.append(dbconn.getMeterEndpointParent(int(endpointsIds[aux], 16))[aux1][0])

    print('Numero de medidores encontrados:',len(meters))
    readwriteFiles.writemeterFiles(meters)

if __name__ == '__main__':
    #getmetersbyLanIDfromBD()
    metercpuFormater()

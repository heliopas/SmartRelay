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

                                  ######switch de testes#######

#switch de teste para gerar outages e pegar do banco de dados o tempo de recebimento do ultimo pacote do CC
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



if __name__ == '__main__':
    print('hello')
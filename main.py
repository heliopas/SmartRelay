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
import dbconn

#define COM ports and devices
comRelayBox = 'COM80'
comMeterWT210 = 'COM4'
comMeterHP34401A = 'COM1'
delay = 30
global comportRelayBox, comportMeterWT210

# #logging config
# logging.basicConfig(filename='files/log.txt', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.NOTSET)
# logging.Formatter(fmt='%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d,%H:%M:%S')

def openportRelayBox():
    global comportRelayBox
    try:
        comportRelayBox = serial.Serial(port=comRelayBox, baudrate=38400, timeout=2, stopbits=serial.STOPBITS_ONE)
    except serial.SerialException as e:
        logging.error("Error during open port RelayBox: %s" % e)

def openportMeterWT210():
    global comportMeterWT210
    try:
        comportMeterWT210 = serial.Serial(port=comMeterWT210, baudrate=9600, timeout=2, stopbits=serial.STOPBITS_ONE)
    except serial.SerialException as e:
        logging.error("Error during open port MeterWT210: %s" % e)

def openportMeterHP34401A():
    global comportMeterHP34401A
    try:
        comportMeterHP34401A = serial.Serial(port=comMeterHP34401A, baudrate=9600, timeout=2, stopbits=serial.STOPBITS_ONE)
    except serial.SerialException as e:
        logging.error("Error during open port MeterWT210: %s" % e)

def closeportRelayBox():
    global comportRelayBox
    comportRelayBox.close()

def closeportMeterWT210():
    global comportMeterWT210
    comportMeterWT210.close()

def closeportMeterHP34401A():
    global comportMeterHP34401A
    comportMeterHP34401A.close()

def openRelayBox_ch1():
    global comportRelayBox
    try:
        #comportRelayBox.write(b"\n\rROUTe:OPEN (@ 402)\n\r")
        comportRelayBox.write(b"\n\rHP34970:route:open (@ 407)\n\r")
        logging.info("Rele open")
    except serial.SerialException as e:
        logging.error("Error during open RelayBox_ch1: %s" % e)

def closeRelayBox_ch1():
    global comportRelayBox
    try:
        #comportRelayBox.write(b"\n\rROUTe:CLOSE (@ 402)\n\r")
        comportRelayBox.write(b"\n\rHP34970:route:close (@ 407)\n\r")
        logging.info("Rele close")
    except serial.SerialException as e:
        logging.error("Error during close RelayBox_ch1: %s" % e)

def sedDataReadMeterWT210():
    global comportMeterWT210
    try:
        comportMeterWT210.write(b':MEASURE:NORMAL:VALUE?')
        sleep(1)
        comportMeterWT210.write(b'\r\n')
    except serial.SerialException as e:
        logging.error("Error during read data MeterWT210: %s" % e)

def DataReadMeterWT210():
    global comportMeterWT210
    try:
        data = comportMeterWT210.readline()
        logging.info(data)
    except serial.SerialException as e:
        logging.error("Error during read data MeterWT210: %s" % e)


def sedDataReadMeterHP34401A():
    global comportMeterHP34401A
    try:
        comportMeterHP34401A.write(b'syst:rem')
        comportMeterHP34401A.write(b'\r\n')
        #comportMeterHP34401A.write(b':meas:curr:dc?')
        comportMeterHP34401A.write(b':meas:volt:dc?')
        comportMeterHP34401A.write(b'\r\n')
    except serial.SerialException as e:
        logging.error("Error during read data MeterWT210: %s" % e)

def beepOffHP34401A():
    global comportMeterHP34401A
    try:
        comportMeterHP34401A.write(b'syst:rem')
        comportMeterHP34401A.write(b'\r\n')
        comportMeterHP34401A.write(b'SYSTem:BEEPer:STATe OFF')
        comportMeterHP34401A.write(b'\r\n')
    except serial.SerialException as e:
        logging.error("Error during disable beep: %s" % e)

def DataReadMeterHP34401A():
    global comportMeterHP34401A
    try:
        data = comportMeterHP34401A.readline()
        logging.info(data)
    except serial.SerialException as e:
        logging.error("Error during read data MeterWT210: %s" % e)

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


if __name__ == '__main__':
    openportRelayBox()

    landId = ['40056591', '40056589', '400565B0', '4005957B', '40056596', '400565EE']

    #variaveis de controle da aplicação
    aux = True
    checkpackageReceived = True

    while aux:

        if checkpackageReceived is True: # variavel de controle gera outage só depois das CPUS receberem algum pacote no CC
            openRelayBox_ch1()
            print('Relay aberto!!!')
            #logging.info("interation: %d" % aux)
            sleep(250) #250, desligado por 4 minutos
            closeRelayBox_ch1()
            print('                 Relay fechado!!!')
            sleep(600) #1200, ligado 25 min


        for row in landId:
            dbreturn = dbconn.getMeterlastpackage(row)
            for row in dbreturn:
                print(row)
                if checkLastPackage(row[0], 0, 10) == True:
                    checkpackageReceived = False
                    sleep(120) # espera 2 minutos para realizar leitura novamente do recebimento dos pacotes
                    break
                else:
                    checkpackageReceived = True # executa outage se todas CPU enviaram algum pacote para o CC
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

#defirne COM ports and devices
comRelayBox = 'COM77'
comMeterWT210 = 'COM4'
comMeterHP34401A = 'COM1'
delay = 30
global comportRelayBox, comportMeterWT210

#logging config
logging.basicConfig(filename='files/log.txt', format='%(asctime)s %(levelname)-8s %(message)s', level=logging.NOTSET)
logging.Formatter(fmt='%(asctime)s.%(msecs)03d', datefmt='%Y-%m-%d,%H:%M:%S')

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
        comportRelayBox.write(b"\n\rROUTe:OPEN (@ 401)\n\r")
        logging.info("Rele open")
    except serial.SerialException as e:
        logging.error("Error during open RelayBox_ch1: %s" % e)

def closeRelayBox_ch1():
    global comportRelayBox
    try:
        comportRelayBox.write(b"\n\rROUTe:CLOSE (@ 401)\n\r")
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

    print(dateTimenow)
    print(lastpackageReceived)

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
    # while True:
    #     openRelayBox_ch1()
    #     sleep(1)
    #     closeRelayBox_ch1()
    landId = ['40056591', '40056589', '400565B0', '4005957B', '40056596', '400565EE']

    while True:

        openRelayBox_ch1()
        sleep(5) #250
        closeRelayBox_ch1()
        sleep(5) #1200

        for row in landId:
            dbreturn = dbconn.getMeterlastpackage(row)
            for row in dbreturn:
                print(row)
                if checkLastPackage(row[0], 0, 15) == True:
                    break











import serial
import errno
from colorama import Fore, Back, Style
from time import sleep
import logging
import csv

#defirne COM ports and devices
comRelayBox = 'COM15'
comMeterWT210 = 'COM5'
comMeterHP34401A = 'COM6'
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
        comportMeterHP34401A.write(b':meas:curr:dc?')
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

if __name__ == '__main__':
    for aux in range(1000):
        print('Iniciando teste.....')
        openportMeterHP34401A()
        openportRelayBox()
        openportMeterWT210()

        openRelayBox_ch1()
        print('Rele open')
        sleep(delay)

        sedDataReadMeterWT210()
        DataReadMeterWT210()

        sedDataReadMeterHP34401A()
        DataReadMeterHP34401A()

        closeRelayBox_ch1()
        print('Rele close')
        sleep(delay)

        sedDataReadMeterWT210()
        DataReadMeterWT210()

        sedDataReadMeterHP34401A()
        DataReadMeterHP34401A()

        closeportRelayBox()
        closeportMeterWT210()
        closeportMeterHP34401A()

        logging.info("interation: %d" % aux)
        print("interation: %d" % aux)







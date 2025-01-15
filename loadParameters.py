import os
import csv

helpMenu = 'files/var/help.txt'
configFile = 'files/var/config.txt'
endPointfilePath = 'files/cpumeterCSV/endpointcpu.csv'
metersfilePath = 'files/cpumeterCSV/meters.csv'

#txt function reader
def loadHelptFile():
    with open(helpMenu, "r", encoding="utf8") as file1:
        return file1.read()

def loadConfigFile():
    with open(configFile, "r", encoding="utf8") as file1:
        aux = file1.read().removeprefix('tipoProduto=[').removesuffix(']')
        aux = aux.split(',')
        return aux

#csv file function reader
def checkPath():
    if os.path.isfile(endPointfilePath) and os.path.isfile(metersfilePath) and (os.path.getsize(endPointfilePath) > 0) \
            and (os.path.getsize(metersfilePath) > 0):
        return True
    else:
        return False

def loadFiles():
    with open(endPointfilePath, "r", encoding="utf8") as file1:
        global endpoint
        endpoint= file1.read()
    with open(metersfilePath, "r", encoding="utf8") as file2:
        global meters
        meters = file2.read()
    return 'Arquivos carregados!!!'

def getendpoint():
    return endpoint

def getmeters():
    return meters

import os
import csv

endPointfilePath = 'files/cpumeter/endpointcpu.txt'
metersfilePath = 'files/cpumeter/meters.txt'

#txt file function reader
def checkPath():
    if os.path.isfile(endPointfilePath) and os.path.isfile(metersfilePath) and (os.path.getsize(endPointfilePath) > 0) \
            and (os.path.getsize(metersfilePath) > 0):
        return True
    else:
        return False

def loadFiles():
    if(checkPath()):
        with open(endPointfilePath, "r", encoding="utf8") as file1:
            global endpoint
            endpoint= file1.read().split('\n')
        with open(metersfilePath, "r", encoding="utf8") as file2:
            global meters
            meters = file2.read().split('\n')
        return 'Arquivos carregados!!!'
    else:
        print(" Erro ao carregar arquivos!!!")

def writemeterFiles(meterIds):
    if(checkPath()):
        with open(metersfilePath, "w", encoding="utf8") as file:
            for aux in range(len(meterIds)):
                file.write(((hex(int(meterIds[aux])) + ',' + '\n').removeprefix('0x')).zfill(10))
                #file.write(((hex(int(meterIds[aux]))+'\n').removeprefix('0x')).zfill(9))
        print("Arquivo gravado com sucesso")
    else:
        print("Erro ao gravar o arquivo!!!")




def getendpoint():
    if(loadFiles()):
        return endpoint

def getmeters():
    if (loadFiles()):
        return meters

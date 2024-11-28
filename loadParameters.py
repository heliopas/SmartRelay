import os

helpMenu = 'files/var/help.txt'
configFile = 'files/var/config.txt'

def loadHelptFile():
    with open(helpMenu, "r", encoding="utf8") as file1:
        return file1.read()

def loadConfigFile():
    with open(configFile, "r", encoding="utf8") as file1:
        aux = file1.read().removeprefix('tipoProduto=[').removesuffix(']')
        aux = aux.split(',')
        return aux
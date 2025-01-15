import time
from datetime import datetime

import selenium.common.exceptions
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import files.var.globalVar as var

#variaveis locais de programas
pageAddress = "http://brcwbvr134/CC/default.aspx?initial=MessageCenter"
navigatorDriver = 'files/ChromeDRV/chromedriver.exe' # driver do MS Edge
resultTable = [] # tabela de resultados do site CC
username = var.usernameCC
passwd = var.CCpwd

def set_CONF():
    global program, driver
    options = webdriver.ChromeOptions()
    options.binary_location = 'ChromeDRV/chrome.exe' #r'C:\Users\RompkoH\OneDrive - Landis+Gyr\SW_BKP\Chrome\Application\chrome.exe'
    program = Service(navigatorDriver)
    driver = webdriver.Chrome(service=program, chrome_options=options)

def set_PAGE(page):
    driver.get(page)
    set_txtBoxBYID(id="LoginName", msg=username) #set user
    set_txtBoxBYID(id="Password", msg=passwd) #set password
    send_clickBYID(id="LoginBtn")

def set_txtBoxBYID(id, msg):
    driver.find_element(By.ID, id).send_keys(msg)

def send_clickBYID(id):
    driver.find_element(By.ID, id).click()

def set_FULLSCR():
    driver.fullscreen_window()

def set_BACKPAGE():
    driver.back()

def set_UPDATEPAGE():
    driver.refresh()

def funclosePage():
    driver.close()
    driver.quit()

def get_textBYID(param):
    return driver.find_elements(By.XPATH, value=param)

def get_generalTable(param, param2): # obtem valores da tabela geral do medidor
    count = 0
    genVector = []
    while True:
        stringaux = param.replace('_ctl00_', '_ctl' + str(count).zfill(2) + '_')
        stringaux = driver.find_elements(By.XPATH, value=stringaux)
        for e in stringaux:
            genVector.append(e)
        stringaux = param2.replace('_ctl00_', '_ctl' + str(count).zfill(2) + '_')
        stringaux = driver.find_elements(By.XPATH, value=stringaux)
        for e in stringaux:
            genVector.append(e)
        if count >= 200:
            return genVector
        count += 1

def setConfiguration():
    set_CONF()
    set_PAGE(pageAddress)

def funcdoorMonitor(param1): #monitora estado da porta dos CS
    # set_CONF()
    # set_PAGE(pageAddress)
    set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    send_clickBYID(id="AppSearchBtn")

    try:
        tableGeral = get_generalTable('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl00_DataLabel"]', '//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl00_DataValueSpan"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor ou CPU com falha:"+param1)
        return 'None'

    for e in tableGeral:
        resultTable.append(e.text)
        # print(e.text)

    indexVet = resultTable.index("Door State")
    indexVet += 1

    if resultTable[indexVet] == "Closed":
        tableGeral.clear()
        resultTable.clear()
        #funclosePage()
        return 'Door closed /' + param1 + str(datetime.now())
    else:
        tableGeral.clear()
        resultTable.clear()
        #funclosePage()
        return 'Door open /' + param1 + str(datetime.now())

def funcGetStatus(): #monitora Status dos medidores e CPU
    # set_CONF()
    # set_PAGE(pageAddress)

    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_header_StatusCell"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor ou CPU com falha:"+param1)
        return 'None'

    return status[0].accessible_name.removeprefix('Status: ').removesuffix(' [View History]')

def funcGetLogs():
    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")
    send_clickBYID(id="ctl00_PageBody_TabContainer1_HistoryTab_tab")

    status = []

    while status.__len__() == 0:
        try:
            status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_HistoryTab_historyctrl_EventsGridDiv"]')
        except selenium.common.exceptions.UnexpectedAlertPresentException as e:
            print("Medidor ou CPU com falha:")

    listLog = status[0].text.split('\n')

    powerUpOff = []

    # get Power on and off strings
    for aux in listLog:
        if aux.__contains__('Power off') or aux.__contains__('Power up'):
            aux = re.findall("([A-z]{5} [A-za-z]* counter.?:.?[0-9]+)", aux)
            print(aux)
            powerUpOff.append(aux)

    powerUpOffAux = []

    for aux in powerUpOff:
        numb = re.findall("\d+", str(aux))
        powerUpOffAux.append(numb)

    for aux in range(len(powerUpOffAux)):
        if powerUpOffAux.count(powerUpOffAux[aux])>=2:
            print('Pass:' + str(aux))
        else:
            return 'Power counter FAIL'

    return 'Power counter PASS'

def funcGetModel():
    # set_CONF()
    # set_PAGE(pageAddress)
    #
    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_header_ModelFamilyCell"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Modelo CPU ou medidor vazio:")
        return 'None'

    return status[0].accessible_name.removeprefix('Model: ')

def funcGetKWh(param1): #monitora consumo medidor
    # set_CONF()
    # set_PAGE(pageAddress)
    #
    set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl05_DataItem"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor ou CPU com falha:")
        return 'None'

    return status[0].text

def funcGetLastReading(): #Obtem data/hora ultima leitura medidor e CPU
    # set_CONF()
    # set_PAGE(pageAddress)
    #
    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_header_LastKwhReadingCell"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor ou CPU com falha:")
        return 'None'

    return status[0].text

def funcGetLastGoodPacket(): #Obtem data/hora ultima leitura medidor e CPU
    # set_CONF()
    # set_PAGE(pageAddress)
    #
    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_header_ModelFamilyCell"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor ou CPU com falha:")
        return 'None'

    if(status[0].text.__contains__('M710')):
        status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl10_DataValueSpan"]')
    else:
        status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl13_DataValueSpan"]')

    return status[0].text

def funcGetFWVersion():
    # set_CONF()
    # set_PAGE(pageAddress)
    #
    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_header_ModelFamilyCell"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor ou CPU com falha:")
        return 'None'


    # if (status[0].text.__contains__('M710')):
    #     status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl05_DataValueSpan"]')
    # else:
    #     status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl07_DataValueSpan"]')

    if (status[0].text.__contains__('Magno Grid - E')):
        status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl07_DataValueSpan"]')
    else:
        status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl05_DataValueSpan"]')

    return status[0].text

def funcGetreleStatus():
    # set_CONF()
    # set_PAGE(pageAddress)

    # set_txtBoxBYID(id="AppSearchTxtBx", msg=param1)
    # send_clickBYID(id="AppSearchBtn")

    try:
        status = get_textBYID('//*[@id="ctl00_PageBody_TabContainer1_GeneralTab_generalctrl_EndpointDataList_ctl00_DataValueSpan"]')
    except selenium.common.exceptions.UnexpectedAlertPresentException as e:
        print("Medidor com falha no rele:")
        return 'None'

    return status[0].text
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os
import pandas as pd
import numpy as np
import time

datos_externos_origen = 'C:/Users/Andrés/Documents/AGUATHON_AEMET/'
datos_externos_destino = 'datos_externos/procesados/'
path_datos_antiguos = 'https://datosclima.es/Aemethistorico/Lluviasol.php'
def aemet_to_csv():

    lista = []
    for mes in os.listdir(datos_externos_origen):
        print(mes)
        for dia in os.listdir(datos_externos_origen + mes):
            print(dia)
            year = dia[5:9]
            month = dia[10:12]
            day = dia[13:15]
            fecha = year + month + day
            try:
                df = pd.read_excel(datos_externos_origen + mes + '/' + dia, header = 4)
                df = df.fillna(0)

                zrg = df[df['Estación'] == 'Zaragoza, Canal']
                prec = zrg['Precipitación 00-24h (mm)'].values
                prec = prec[0]
                lista.append((fecha, prec))

            except:
                print('error de mierda en el dia ' + dia)
                lista.append((fecha, 0.0))

    lista = np.asarray(lista)
    datos_a_exportar = pd.DataFrame(lista, columns=['fecha', 'precipitacion'])
    datos_a_exportar.to_csv(datos_externos_destino + 'datos_externos.csv', index=False)
#------------------------------------------------------
#------------------------------------------------------
def aemet_observatorios():
    # qutiar imagenes
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.managed_default_content_settings.images": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    # el navegador
    browser = webdriver.Chrome("driver/chromedriver.exe", chrome_options=chrome_options)
    browser.get(path_datos_antiguos)

    celda_ciudad = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="col2"]/div[1]/div/form/select[1]')))
    celda_ciudad.click()

    time.sleep(2)

    zrg_celda = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="col2"]/div[1]/div/form/select[1]/option[53]')))
    zrg_celda.click()

    time.sleep(2)

    celda_estacion = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/select[2]')
    celda_estacion.click()
    time.sleep(2)
    zrg_est_celda = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/select[2]/option[6]')
    zrg_est_celda.click()

    time.sleep(2)

    # rellenamos
    #fecha inicial
    dia_ini = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/div/table/tbody/tr/td[2]/input[1]')
    dia_ini.send_keys('01')
    mes_ini= browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/div/table/tbody/tr/td[2]/input[2]')
    mes_ini.send_keys('01')
    año_ini = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/div/table/tbody/tr/td[2]/input[3]')
    año_ini.send_keys('2008')
    #fecha hasta
    dia_hasta = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/div/table/tbody/tr/td[5]/input[1]')
    dia_hasta.send_keys('06')
    mes_hasta = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/div/table/tbody/tr/td[5]/input[2]')
    mes_hasta.send_keys('05')
    año_hasta = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/div/table/tbody/tr/td[5]/input[3]')
    año_hasta.send_keys('2013')

    boton_buscar = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/input[5]')
    boton_buscar.click()

    time.sleep(3)

    # leemos dias
    # TODO

    browser.close()



#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
aemet_observatorios()
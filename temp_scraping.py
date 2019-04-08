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
#------------------------------------------------------
#------------------------------------------------------
def tratar_fecha(fecha):
    #02-01-2008
    dia = fecha[:2]
    mes = fecha[3:5]
    año = fecha[6:10]

    return año + mes + dia
#------------------------------------------------------
#------------------------------------------------------
def aemet_csvs_to_lista():

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
                if zrg.empty:
                    zrg = df[df['Estación'] == 'Zaragoza, Valdespartera']

                prec = zrg['Precipitación 00-24h (mm)'].values
                prec = prec[0]
                lista.append((fecha, prec))

            except:
                print('error de mierda en el dia ' + dia)
                lista.append((fecha, 0.0))

    return lista

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
    browser.maximize_window()

    celda_ciudad = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="col2"]/div[1]/div/form/select[1]')))
    celda_ciudad.click()

    time.sleep(1)

    zrg_celda = WebDriverWait(browser, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="col2"]/div[1]/div/form/select[1]/option[53]')))
    zrg_celda.click()

    time.sleep(1)

    celda_estacion = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/select[2]')
    celda_estacion.click()
    time.sleep(1)
    #aeropuerto
    zrg_est_celda = browser.find_element_by_xpath('//*[@id="col2"]/div[1]/div/form/select[2]/option[5]')
    zrg_est_celda.click()

    time.sleep(1)

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

    time.sleep(1)

    # leemos dias
    tablas_totales = 6 * 3
    cuerpo_tabla_xpath = '//*[@id="col2"]/div/div/'
    medio_tabla_xpath = 'table/tbody/tr/td['
    fin_tabla_xpath = ']/table/tbody/tr'
    fin_tabla1_xpath = ']/div/table/tbody/tr'

    indice_tabla = 1

    lista = []

    for tabla in range(0, tablas_totales):

        if indice_tabla > 3:
            indice_tabla = 1

        print('Indice:', indice_tabla)

        if indice_tabla == 1:
            tabla_xpath = cuerpo_tabla_xpath + medio_tabla_xpath + '1' + fin_tabla1_xpath
        else:
            tabla_xpath = cuerpo_tabla_xpath + medio_tabla_xpath + str(indice_tabla) + fin_tabla_xpath
        print(tabla_xpath)

        #tabla 1
        lista_elementos_tabla = browser.find_elements_by_xpath(tabla_xpath)

        idx_elements_lista = 0
        for e_tabla1 in lista_elementos_tabla:
            datos_elemento = e_tabla1.text
            fecha = datos_elemento.split(' ')[0]
            fecha = tratar_fecha(fecha)
            precipitacion = datos_elemento.split(' ')[1]
            if precipitacion == 'Ip':
                precipitacion = '0.0'

            if idx_elements_lista >0 :
                lista.append((fecha, precipitacion))

            idx_elements_lista +=1

        if indice_tabla == 3:
            cuerpo_tabla_xpath = cuerpo_tabla_xpath + 'div[2]/'

        indice_tabla +=1

        # tabla2
        #//*[@id="col2"]/div/div[1]/table[2]/tbody/tr/td[1]/div/table/tbody/tr[2]/td[2]

        # tabla3

        #//*[@id="col2"]/div/div/table[2]/tbody/tr/td[1]/div/table/tbody/tr
        #//*[@id="col2"]/div/div/table[2]/tbody/tr/td[2]/table/tbody
        #//*[@id="col2"]/div/div/table[2]/tbody/tr/td[3]/table/tbody

        #2009
        #//*[@id="col2"]/div/div/div[2]/table/tbody/tr/td[1]/div/table/tbody
        #//*[@id="col2"]/div/div/div[2]/table/tbody/tr/td[2]/table/tbody
        #//*[@id="col2"]/div/div/div[2]/table/tbody/tr/td[3]/table/tbody

        #2010
        #//*[@id="col2"]/div/div/div[2]/div[2]/table/tbody/tr/td[1]/div/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/table/tbody/tr/td[2]/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/table/tbody/tr/td[3]/table/tbody

        #2011
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/table/tbody/tr/td[3]/table/tbody

        #2012
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[3]/table/tbody

        #2013
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[1]/div/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[2]/table/tbody
        #//*[@id="col2"]/div/div/div[2]/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[3]/table

    print(lista[-5:])
    print(len(lista))

    browser.close()

    return lista

#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
def aemet_to_csv():

    lista = []

    lista_obs = aemet_observatorios()
    lista_csvs = aemet_csvs_to_lista()
    lista = lista_obs + lista_csvs

    lista = np.asarray(lista)
    datos_a_exportar = pd.DataFrame(lista, columns=['fecha', 'precipitacion'])
    datos_a_exportar.to_csv(datos_externos_destino + 'datos_externos.csv', index=False)
#------------------------------------------------------
#------------------------------------------------------
#------------------------------------------------------
aemet_to_csv()
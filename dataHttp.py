import bs4
from bs4 import BeautifulSoup
from requests.exceptions import ChunkedEncodingError
from datetime import datetime
import requests
import datetime
import json
import time
import pandas as pd
import csv
import locale
import re

def saveData_CSV(dictionary, file_Name):
    file_Name = file_Name
    csv_filename = f"{file_Name}.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(dictionary.keys())
        data_rows = zip(*dictionary.values())
        csv_writer.writerows(data_rows)
    print(f"Los datos se han guardado en '{csv_filename}'.")

def urlsvD_Generator():
    urlBase = 'https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/'
    response = requests.get(urlBase)
    soup = BeautifulSoup(response.text,"html.parser")
    tRow = (soup.find('tbody')).find_all('tr')
    urls = []
    for tr in tRow[1:]:
        for tdIntr in tr.find_all('td'):
            urlDate = tdIntr.find('a')
            if urlDate:
                urlDateSuccess = urlDate['href']
                replace_url = "https://www.servir.gob.pe"
                if urlDateSuccess.startswith(replace_url):
                    urlDateSuccess = urlDateSuccess.replace(replace_url, "")
                urls.append(urlDateSuccess)
    return urls

def dataRecollection():
    urls = urlsvD_Generator()
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    servir_resolution_data = {
        "fecha_extraction": [],
        "resolution": [],
        "resolution_url": [],
        "nombre": [],
        "entidad": [],
        "fecha": [],
        "sesion": []
    }
    headers = {"user-agent":"Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/117.0"}
    signal = False
    valorReturnIt = ''
    for urlTrans in urls:
        numero = re.search(r'\d{4}', urlTrans)
        year_found = numero.group()
        yearF = int(year_found)
        pagParse = "https://www.servir.gob.pe"+urlTrans
        if signal == True:
            pagParse = valorReturnIt
        print(f"{yearF} -> las urls son {pagParse}")

        # response = requests.get(pagParse)
        # for i in range(2):
        #     response = requests.get(pagParse)
        # if response.status_code == 404:
        #     print(f"{pagParse} con status_code 404")
        #     continue
        try:
            start_time = time.time()
            for i in range(2):
                response = requests.get(pagParse, timeout = 10)
            response.raise_for_status()
            #Medimos tiempo, quiero verificar algo
            elapsed_time = time.time() - start_time
            print(f"Tiempo transcurrido: {elapsed_time} segundos")
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        else:
            # El código aquí se ejecutará solo si la solicitud es exitosa.
            # Puedes procesar la respuesta aquí.
            # time.sleep(1)
            soupDpage = BeautifulSoup(response.text,"html.parser")
            # print("paso el soup")
            trInTable = soupDpage.find_all('tr')
            if trInTable:
                print("Si existe trInTable")
                signal = False
            else:
                if response.status_code == 200:
                    signal = True
                    valorReturnIt = pagParse
                print(f"ERROR -> {pagParse}")
            sessionValue = ''
            dateS = ''
            for tr in trInTable[1:]:
                thT =  tr.find('th')
                if thT:
                    sessionValue = ' '.join(tr.stripped_strings)
                    if yearF < 2014:
                        if tr.b:
                            date_text = tr.b.get_text()
                        if tr.strong:
                            date_text = tr.strong.get_text()
                        if "SETIEMBRE" in date_text:
                            date_text = date_text.replace("SETIEMBRE", "SEPTIEMBRE")
                        dateS = datetime.datetime.strptime(date_text, '%d %B %Y').date()
                    continue
                elif tr.find('td',colspan="4"):
                    print(f"entro en el anyo: {pagParse}")
                    sessionValue = ' '.join(tr.stripped_strings)
                    continue
                resolution = tr.find('a')
                if resolution:
                    resolution_text = resolution.get_text()
                    resolution_url = resolution['href']
                    # print(resolution_url)
                    name = (tr.find_all('td')[1]).get_text()
                    entity = (tr.find_all('td')[2]).get_text()
                    # print(f"El anio es {yearF} ")
                    if yearF >= 2014:
                        date_text = (tr.find_all('td')[3]).get_text()
                        wordsDate = date_text.split()
                        subStringDate = ' '.join(wordsDate[:3])
                        date_text = subStringDate+" "+str(yearF) 
                        date_text = date_text.lower()
                        if "setiembre"in date_text:
                            date_text = date_text.replace("setiembre", "septiembre")
                        if "DE " in date_text:
                            dateS = datetime.datetime.strptime(date_text, '%d DE %B %Y').date()
                        elif "de " in date_text:
                            dateS = datetime.datetime.strptime(date_text, '%d de %B %Y').date()
                        elif "del " in date_text:
                            dateS = datetime.datetime.strptime(date_text, '%d %B del %Y').date()
                        # print(f"EL valor de date es: {date_text} y su dateS: {dateS}")
                    date_Today = datetime.date.today().strftime("%d/%m/%Y")
                    dateExt = date_Today
                    index = [dateExt,resolution_text,resolution_url,name,entity,dateS,sessionValue]
                    for k,v in zip(servir_resolution_data.keys(),index):
                        servir_resolution_data[k].append(v)
            saveData_CSV(servir_resolution_data,"primerTest")

dataRecollection()
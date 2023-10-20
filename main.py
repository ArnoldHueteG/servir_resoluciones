import bs4
from bs4 import BeautifulSoup
from requests.exceptions import ChunkedEncodingError
import requests
from datetime import datetime
import time
import datetime
import pandas as pd
import json
import csv
import locale
import re
from selenium import webdriver
from bs4 import BeautifulSoup

driver = webdriver.Firefox()
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

def saveData_CSV(dictionary, file_Name):
    file_Name = file_Name
    csv_filename = f"{file_Name}.csv"
    with open(csv_filename, mode='w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(dictionary.keys())
        data_rows = zip(*dictionary.values())
        csv_writer.writerows(data_rows)
    print(f"Los datos se han guardado en '{csv_filename}'.")

def urlsvD_Generator(urlBase): 
    response = requests.get(urlBase)
    soup = BeautifulSoup(response.text,"html.parser")
    tRow = (soup.find('tbody')).find_all('tr')
    urls = []
    if "/primera-sala/" in urlBase:
        tRow = tRow[1:]
    for tr in tRow:
        for tdIntr in tr.find_all('td'):
            urlDate = tdIntr.find('a')
            if urlDate:
                urlDateSuccess = urlDate['href']
                replace_url = "https://www.servir.gob.pe"
                if urlDateSuccess.startswith(replace_url):
                    urlDateSuccess = urlDateSuccess.replace(replace_url, "")
                urls.append(urlDateSuccess)
    return urls

def dataRecollection(urlBase):
    urls = urlsvD_Generator(urlBase)
    pattern = r'/([^/]+)/$'
    match = re.search(pattern, urlBase)
    file_Name = match.group(1)+"-Resolution-CSV"
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
    valorReturnIt = ''
    for urlTrans in urls:
        numero = re.search(r'\d{4}', urlTrans)
        year_found = numero.group()
        yearF = int(year_found)
        pagParse = "https://www.servir.gob.pe"+urlTrans
        print(f"{yearF} -> las urls son {pagParse}")
        try:
            driver.get(pagParse)
            html = driver.page_source
        except requests.exceptions.RequestException as e:
            print(f"Error en la solicitud: {e}")
        else:
            soupDpage = BeautifulSoup(html,"html.parser")
            trInTable = soupDpage.find_all('tr')
            if trInTable:
                print("Si existe trInTable")
            else:
                print(f"ERROR en la Pag -> {pagParse}")
                continue
            sessionValue = ''
            dateS = ''
            for tr in trInTable[1:]:
                thT =  tr.find('th')
                if thT or tr.find('td',colspan='3'):
                    sessionValue = ' '.join(tr.stripped_strings)
                    if yearF < 2014:
                        print(f"el anio es {yearF}")
                        if tr.b:
                            date_text = tr.b.get_text()
                        if tr.strong:
                            date_text = tr.strong.get_text()
                        if "SETIEMBRE" in date_text:
                            date_text = date_text.replace("SETIEMBRE", "SEPTIEMBRE")
                        dateS = datetime.datetime.strptime(date_text, '%d %B %Y').date()
                    continue
                elif tr.find('td',colspan="4"):
                    # print(f"entro en el anyo: {pagParse}")
                    sessionValue = ' '.join(tr.stripped_strings)
                    continue
                resolution = tr.find('a')
                if resolution:
                    resolution_text = resolution.get_text()
                    resolution_url = resolution['href']
                    # print(resolution_url)
                    name = (tr.find_all('td')[1]).get_text()
                    name = name.replace('\n','')
                    entity = (tr.find_all('td')[2]).get_text()
                    entity = entity.replace('\n','')
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
            saveData_CSV(servir_resolution_data,file_Name)

urls = [
    'https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/',
    'https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/segunda-sala/'
]

dataRecollection()

driver.quit()
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

TABLE_NAME = "Servir.Resolution"

months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre']

def parse_url(date_extraction_str):
    date_extraction = datetime.datetime.strptime(date_extraction_str, '%Y-%m-%d').date()
    month_name = months[date_extraction.month]
    url = f"https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-{date_extraction.year}-{month_name}/"
    print(url)
    response = requests.get(url)
    soupDpage = BeautifulSoup(response.text,"html.parser")
    rows = soupDpage.find_all('tr')[1:]
    if not rows:
        print(f"No existen elementos tr en url")
        print(rows)
    sessionValue = ""
    # Iterate over all <tr> elements within the <tbody>
    ls_data = []
    for row in rows:
        if row.find('th') or row.find('td',colspan="4"):
            # sessionValue = row.find('th').get_text()
            sessionValue = row.get_text()
            continue    
        anchor_tag = row.find('a')
        if anchor_tag:
            resolution = anchor_tag.get_text()
            resolution_url = anchor_tag['href']
            name = row.find_all('td')[1].get_text()
            entity = row.find_all('td')[2].get_text()
            index = {
                "fecha_extraction": date_extraction_str,
                "resolucion": resolution,
                "resolucion_url": resolution_url,
                "nombre": name,
                "entidad": entity,
                "fecha": date_extraction_str, # TODO: change to parse from title th tag
                "sesion": sessionValue # TODO: trim the string
            }
            ls_data.append(index)

    print(len(ls_data))
    print(json.dumps(ls_data[:10], indent=4, sort_keys=True))





#parse_url('2011-01-01')
servir_resolution_data = {
        "fecha_extraction": [],
        "resolution": [],
        "resolution_url": [],
        "nombre": [],
        "entidad": [],
        "fecha": [],
        "sesion": []
    }
dataTH = []
stringPrincipal = "https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/"
def dataExtraction():
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    for yearF in range(19,24):
        for monTH in months:
            pagParse = f"https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/resoluciones-20{yearF}-{monTH}/"
            print(f'Entrando en f{pagParse}')
            response = requests.get(pagParse)
            soupDpage = BeautifulSoup(response.text,"html.parser")
            table = soupDpage.find('table')
            trInTable = soupDpage.find_all('tr')
            sessionValue = ''
            dateS = ''
            for tr in trInTable[1:]:
                thT =  tr.find('th')
                if thT:
                    sessionValue = ' '.join(tr.stripped_strings)
                    if yearF < 14:
                        if tr.b:
                            date_text = tr.b.get_text()
                        if tr.strong:
                            date_text = tr.strong.get_text()
                        if "SETIEMBRE" in date_text:
                            date_text = date_text.replace("SETIEMBRE", "SEPTIEMBRE")
                        dateS = datetime.datetime.strptime(date_text, '%d %B %Y').date()
                    continue
                resolution = tr.find('a')
                if resolution:
                    resolution_text = resolution.get_text()
                    resolution_url = resolution['href']
                    # print(resolution_url)
                    name = (tr.find_all('td')[1]).get_text()
                    entity = (tr.find_all('td')[2]).get_text()
                    if yearF>= 14 and yearF<20:
                        date_text = (tr.find_all('td')[3]).get_text()
                        wordsDate = date_text.split()
                        subStringDate = ' '.join(wordsDate[:3])
                        date_text = subStringDate+" 20"+str(yearF) 
                        if "SETIEMBRE" in date_text:
                            date_text = date_text.replace("SETIEMBRE", "SEPTIEMBRE")
                        if "DE" in date_text:
                            dateS = datetime.datetime.strptime(date_text, '%d DE %B %Y').date()
                        if "de" in date_text and "del" in date_text:
                            dateS = datetime.datetime.strptime(date_text, '%d de %B del %Y').date()
                        if "del" in date_text and (not "de" in date_text or "DE" in date_text):
                            dateS = datetime.datetime.strptime(date_text, '%d %B del %Y').date()

                    date_Today = datetime.date.today().strftime("%d/%m/%Y")
                    dateExt = date_Today
                    index = [dateExt,resolution_text,resolution_url,name,entity,dateS,sessionValue]
                    for k,v in zip(servir_resolution_data.keys(),index):
                        servir_resolution_data[k].append(v)

            file_Name = "SeguimientoD"
            csv_filename = f"{file_Name}.csv"
            with open(csv_filename, mode='w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(servir_resolution_data.keys())
                data_rows = zip(*servir_resolution_data.values())
                csv_writer.writerows(data_rows)
            print(f"Los datos se han guardado en '{csv_filename}'.")

dataExtraction()

# print(servir_resolution_data)
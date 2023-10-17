import bs4
from bs4 import BeautifulSoup
from requests.exceptions import ChunkedEncodingError
import requests
import datetime
import json
import time
import pandas as pd
import csv

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

parse_url('2011-01-01')
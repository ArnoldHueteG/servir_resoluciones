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


def getDateWithParse(posRoom,fin_Date,file_Name,debug = False):
    months = ['enero','febrero','marzo','abril','mayo','junio','julio','agosto','setiembre','octubre','noviembre','diciembre']
    servir_resolution_data = {
        "fecha_extraction": [],
        "resolucion": [],
        "resolucion_url": [],
        "nombre": [],
        "entidad": [],
        "fecha": [],
        "sesion": []
    }
    dateExt = datetime.date.today()
    for i in range(11,fin_Date+1):
        if i%3 == 0 :
            time.sleep(10)
        for month in months:
            pageDate =  f"{posRoom}resoluciones-20{i}-{month}/"
            getOrder = 0
            # Número máximo de intentos
            max_intentos = 3
            # Valor de timeout en segundos
            timeout = 10
            intentos = 0
            # errorConsec = 0
            response = requests.get(pageDate)
            while intentos < max_intentos:
                try:
                    # Realiza la solicitud HTTP
                    getOrder = requests.get(pageDate, timeout=timeout)
                    # Verifica si la respuesta tiene un estado exitoso (código 200)
                    if response.status_code == 200:
                        # Procesa la respuesta aquí
                        if debug:
                            print(f"Entrando a la pag página web -> {pageDate}")
                            print("Respuesta exitosa:")
                        break  # Sale del bucle si la solicitud es exitosa
                    # elif response.status_code == 404:
                    #     if debug:
                    #         print(f"No se encontro la pagina -> {pageDate}, devuelve estado: {response.status_code}")
                        # break
                    else:
                        if month == "setiembre":
                            pageDate = f"{posRoom}resoluciones-20{i}-septiembre/"
                            response = requests.get(pageDate)
                            if debug: print(f"Cambiando setiembre por septiembre: {response.status_code}")
                        else:
                            print(f"Respuesta no exitosa sobre la web -> {pageDate}. Código de estado: {response.status_code}")
                            break
                except ChunkedEncodingError as e:
                    print("Error ChunkedEncodingError:", e)
                    intentos += 1
                    print(f"Reintentando ({intentos}/{max_intentos})...")

                except requests.exceptions.RequestException as e:
                    print("Error de solicitud:", e)
                    intentos += 1
                    print(f"Reintentando ({intentos}/{max_intentos})...")

            if intentos >= max_intentos:
                print("Se agotaron los intentos. No se pudo completar la solicitud.")
            if response.status_code == 404:
                break
            getHtml = getOrder.text
            # Parse Html-PageDate
            soupDpage = BeautifulSoup(getHtml,"html.parser")
            rows = soupDpage.find_all('tr')[1:]
            if not rows:
                print(f"No existen elementos tr en 20{i}-{month}")
                print(rows)
                continue
            sessionValue = ""
            # Iterate over all <tr> elements within the <tbody>
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
                    index = [dateExt,resolution,resolution_url,name,entity,dateExt,sessionValue]
                    for k,v in zip(servir_resolution_data.keys(),index):
                        servir_resolution_data[k].append(v)
                    # Procesar los datos obtenidos aquí
                else:
                    # La etiqueta <a> no está presente en esta fila, es vacía
                    # Puedes manejarla o ignorarla según tus necesidades
                    continue
    # Nombre del archivo CSV de salida
    csv_filename = f"{file_Name}.csv"
    # Abre el archivo CSV en modo de escritura
    with open(csv_filename, mode='w', newline='') as csv_file:
        # Crea un escritor CSV
        csv_writer = csv.writer(csv_file)
        # Escribe el encabezado (las claves del diccionario) en el archivo CSV
        csv_writer.writerow(servir_resolution_data.keys())
        # Combina los valores de las listas en una lista de tuplas
        data_rows = zip(*servir_resolution_data.values())
        # Escribe los datos en el archivo CSV
        csv_writer.writerows(data_rows)
    print(f"Los datos se han guardado en '{csv_filename}'.")


specialCase = "http://files.servir.gob.pe/WWW/files/Tribunal/TSC-Resoluciones-2010.html"
urlsBase = ["https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/primera-sala/","https://www.servir.gob.pe/tribunal-sc/resoluciones-de-salas/segunda-sala/"]
getDateWithParse(urlsBase[0],20,"Primera Sala",False)
# getDateWithParse(urlsBase[1],23,"Segunda Sala",True)



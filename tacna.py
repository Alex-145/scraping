import requests
from bs4 import BeautifulSoup
import re
import csv

# URL objetivo
url = 'https://diariosinfronteras.com.pe/category/tacna/'

# Crear una sesión de requests para reutilizar conexiones
with requests.Session() as session:
    # Realizar la solicitud HTTP
    respuesta = session.get(url)
    
    # Verificar que la solicitud fue exitosa
    if respuesta.status_code != 200:
        print(f'Error al acceder a la página principal: {respuesta.status_code}')
        exit()
    
    # Analizar el contenido HTML
    dom_html = BeautifulSoup(respuesta.content, 'html.parser')
    
    # Encontrar todos los elementos <h3> con la clase 'entry-title'
    secciones = dom_html.find_all('h3', class_='entry-title')
    
    titulos = []
    enlaces = []
    fechas = []
    contenidos = []

    print('Iniciando scraping...')
    
    for seccion in secciones:
        try:
            enlace = seccion.find('a')['href']
            titulo = seccion.find('a')['title']
            
            titulos.append(titulo)
            enlaces.append(enlace)
            
            # Extraer la fecha del enlace
            patron = r'/(\d{4})/(\d{2})/(\d{2})/'
            match = re.search(patron, enlace)
            if match:
                anio = match.group(1)
                mes = match.group(2)
                dia = match.group(3)
                fecha = f'{anio}/{mes}/{dia}'
                fechas.append(fecha)
            else:
                fechas.append('No disponible')
            
            # Solicitar la página interna
            solicitud_interna = session.get(enlace)
            if solicitud_interna.status_code == 200:
                dom_html_interno = BeautifulSoup(solicitud_interna.content, 'html.parser')
                el_div = dom_html_interno.find('div', class_='post-content-bd')
                if el_div:
                    contenidos.append(el_div.get_text(strip=True))
                else:
                    contenidos.append('Contenido no encontrado')
            else:
                contenidos.append('Error al acceder al contenido')
        
        except Exception as e:
            print(f'Error al procesar una sección: {e}')
            titulos.append('Error')
            enlaces.append('Error')
            fechas.append('Error')
            contenidos.append('Error')

    # Guardar los datos en un archivo CSV
    with open('noticias_extraidas15.csv', 'w', newline='', encoding='utf-8-sig') as csvfile:
        csvWrite = csv.writer(csvfile, delimiter='|')
        csvWrite.writerow(['TITULO', 'ENLACE', 'FECHA', 'CONTENIDO'])
        for t, e, f, c in zip(titulos, enlaces, fechas, contenidos):
            csvWrite.writerow([t, e, f, c])

    print('Proceso terminado')

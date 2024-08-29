import requests
from bs4 import BeautifulSoup
import re
import codecs
import csv


url = 'https://diariosinfronteras.com.pe/category/tacna/'

# Realizar la solicitud HTTP
solicitud = requests.get(url)

# Analizar el contenido HTML
dom_html = BeautifulSoup(solicitud.content, 'html.parser')

# Encontrar todos los elementos <h3> con la clase 'entry-title'
secciones = dom_html.find_all('h3', class_='entry-title')


titulos=[]
enlaces=[]
fechas=[]
contenidos=[]

print ('iniciando scraping')
# Iterar sobre cada elemento y extraer el texto
for seccion in secciones:
    #print(seccion.get_text(), "\n\n")
    enlace = seccion.find('a').get('href')
    titulo = seccion.find('a').get('title')
    titulos.append(titulo)
    #print(titulo)
    enlaces.append(enlace)
    #print(enlace)
    patron = r'/(\d{4})/(\d{2})/(\d{2})/'
    match = re.search(patron, enlace)


    if match:
        anio = match.group(1)
        mes = match.group(2)
        dia = match.group(3)
        fecha = f'{anio}/{mes}/{dia}'
        #print(f'Fecha: {fecha}')
        fechas.append(fecha)
    

    solicitud_interna = requests.get(enlace)
    dom_html_interno = BeautifulSoup(solicitud_interna.content,'html.parser')
    el_div = dom_html_interno.find('div',class_ = 'post-content-bd')
    contenidos.append(el_div.get_text(strip=True))
    #print(el_div.text)

with codecs.open('noticias_extraidas14.csv', 'w', 'utf-8-sig') as csvfile:
    csvWrite = csv.writer(csvfile,delimiter="|")
    csvWrite.writerow(['TITULO', 'ENLACE', 'FECHA', 'CONTENIDO'])

    for t,e,f,c in zip(titulos, enlaces, fechas, contenidos):
        csvWrite.writerow([t,e,f,c])

print('proceso terminado')
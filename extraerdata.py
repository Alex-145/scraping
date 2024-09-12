import time
import requests
from bs4 import BeautifulSoup
import os
import csv
import re


titulos=[]
fechas=[]
enlaces=[]
contenidos=[]

for i in range(1,30):
    url=f"https://diariosinfronteras.com.pe/category/puno/page/{i}/"
    print(url)
    solicitud = requests.get(url)
    dom_html=BeautifulSoup(solicitud.content,'html.parser')
    secciones=dom_html.find_all('h3',class_="entry-title")

    for seccion in secciones[:-5]:
        titulo=seccion.find('a').get('title')        
        enlace=seccion.find('a').get('href')        
        
        patron_fecha=r"\b(\d{4})/(\d{2})/(\d{2})\b"
        fecha = re.search(patron_fecha,enlace)
        #print(fecha.group())        
        
        contenido_interno=requests.get(enlace)
        html_interno = BeautifulSoup(contenido_interno.content,'html.parser')
        texto_noticia = html_interno.find('div',class_='post-content-bd')
        noticia_limpia = re.sub(r'[^a-zA-Z0-9|\s|á|é|í|ó|ú|Á|É|Í|Ó|Ú|ñ|Ñ]', '', texto_noticia.text)
        noticia_limpia = re.sub(r'\s+',' ', texto_noticia.text).strip()

        titulos.append(titulo)
        fechas.append(fecha.group())
        enlaces.append(enlace)
        contenidos.append(noticia_limpia)

with open('noticias_extraidas_01.csv',mode='w',newline='',encoding='utf-8-sig') as archivo:
    escritor = csv.writer(archivo,delimiter='|')
    escritor.writerow(["titulo","fecha","enlace","contenido"])

    for i1,i2,i3,i4 in zip(titulos,fechas,enlaces,contenidos):
        escritor.writerow([i1,i2,i3,i4])

print("proceseso terminado ")

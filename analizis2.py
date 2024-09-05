import pandas as pd
import spacy 
from datetime import datetime
import matplotlib.pyplot as plt


# Cargar el modelo de spaCy
nlp = spacy.load('es_core_news_md')

# Cargar el archivo CSV
df = pd.read_csv('noticias_extraidas_01.csv', delimiter="|")

# Función para lematizar el contenido
def lematizar(texto):
    doc = nlp(texto)
    pbases = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(pbases)

# Aplicar lematización
df['contenido_lematizado'] = df['contenido'].apply(lematizar)

# Palabras clave para filtrar accidentes
palabras_clave = ['accidente', 'choque', 'herido', 'muerto', 'colision', 'colisión']

# Función para verificar si una noticia contiene alguna palabra clave
def contiene_palabra_clave(noticia, palabras_clave):
    noticia = noticia.lower()
    return any(palabra in noticia for palabra in palabras_clave)

# Filtrar las noticias relacionadas con accidentes
df_accidentes = df[df['contenido_lematizado'].apply(lambda x: contiene_palabra_clave(x, palabras_clave))]
# Convertir la columna 'fecha' al formato de fecha si no lo está ya
df_accidentes['fecha'] = pd.to_datetime(df_accidentes['fecha'], format='%Y/%m/%d')

# Crear una columna 'mes' para extraer el mes de cada fecha
df_accidentes['mes'] = df_accidentes['fecha'].dt.to_period('M')

# Contar la frecuencia de noticias por mes
frecuencia_mensual = df_accidentes['mes'].value_counts().sort_index()

# Guardar el resultado a un archivo CSV si se desea
frecuencia_mensual.to_csv('frecuencia_accidentes_por_mes.csv', sep='|', encoding='utf-8-sig')

# Generar un gráfico de barras
plt.figure(figsize=(10,6))
frecuencia_mensual.plot(kind='bar', color='skyblue')
plt.title('Frecuencia de Noticias de Accidentes por Mes')
plt.xlabel('Mes')
plt.ylabel('Número de Noticias')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar el gráfico como imagen si se desea
plt.savefig('frecuencia_accidentes_por_mes.png')

# Mostrar el gráfico
plt.show()

print("Proceso terminado")
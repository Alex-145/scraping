import pandas as pd
import spacy
import matplotlib.pyplot as plt
from datetime import datetime

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
def contiene_palabra_clave(noticia, palabra_clave):
    noticia = noticia.lower()
    return palabra_clave in noticia

# Convertir la columna 'fecha' al formato de fecha si no lo está ya
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y/%m/%d')

# Crear una columna 'mes' para extraer el mes de cada fecha
df['mes'] = df['fecha'].dt.to_period('M')

# Crear un dataframe vacío para almacenar los conteos
frecuencia_mensual_palabra = pd.DataFrame()

# Contar la frecuencia por cada palabra clave
for palabra in palabras_clave:
    df_accidentes_palabra = df[df['contenido_lematizado'].apply(lambda x: contiene_palabra_clave(x, palabra))]
    frecuencia_mensual_palabra[palabra] = df_accidentes_palabra['mes'].value_counts().sort_index()

# Rellenar valores NaN con 0 (si no hay noticias en ciertos meses para algunas palabras clave)
frecuencia_mensual_palabra = frecuencia_mensual_palabra.fillna(0)

# Crear un gráfico de barras con diferentes colores para cada palabra clave
ax = frecuencia_mensual_palabra.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')

# Configuraciones del gráfico
plt.title('Frecuencia de Noticias de Accidentes por Mes y Palabra Clave')
plt.xlabel('Mes')
plt.ylabel('Número de Noticias')
plt.xticks(rotation=45)
plt.tight_layout()

# Guardar el gráfico como imagen si se desea
plt.savefig('frecuencia_accidentes_por_mes_palabra.png')

# Mostrar el gráfico
plt.show()

print("Proceso terminado")

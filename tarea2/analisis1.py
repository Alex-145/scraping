import pandas as pd
import spacy
import matplotlib.pyplot as plt
from datetime import datetime

# Cargar el modelo de spaCy
nlp = spacy.load('es_core_news_md')

# Cargar el archivo CSV
df = pd.read_csv(f'noticias_extraidas_300.csv', delimiter="|")

# Reemplazar valores NaN en la columna 'contenido' con una cadena vacía
df['contenido'] = df['contenido'].fillna('')

# Función para lematizar el contenido
def lematizar(texto):
    doc = nlp(texto)
    pbases = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(pbases)

# Aplicar lematización
df['contenido_lematizado'] = df['contenido'].apply(lematizar)

# Palabras clave para filtrar noticias relacionadas con política y pobreza
palabras_clave = ['política', 'gobierno', 'corrupción', 'pobreza', 'desigualdad', 'economía', 'social']

# Función para verificar si una noticia contiene una palabra clave específica
def contiene_palabra_clave(noticia, palabra):
    noticia = noticia.lower()
    return palabra in noticia

# Convertir la columna 'fecha' al formato de fecha
df['fecha'] = pd.to_datetime(df['fecha'], format='%Y/%m/%d')

# Crear una columna 'mes' para extraer el mes de cada fecha
df['mes'] = df['fecha'].dt.to_period('M')

# Crear un DataFrame vacío para almacenar las frecuencias por palabra clave
frecuencia_palabras = pd.DataFrame()

# Calcular las frecuencias por palabra clave y mes
for palabra in palabras_clave:
    df_palabra = df[df['contenido_lematizado'].apply(lambda x: contiene_palabra_clave(x, palabra))]
    frecuencia_mensual_palabra = df_palabra['mes'].value_counts().sort_index()
    frecuencia_palabras[palabra] = frecuencia_mensual_palabra

# Generar el gráfico de barras apiladas con diferentes colores para cada palabra clave
ax = frecuencia_palabras.plot(kind='bar', stacked=True, figsize=(10, 6), colormap='tab20')
plt.title('Frecuencia de Noticias sobre Política y Pobreza por Mes')
plt.xlabel('Mes')
plt.ylabel('Número de Noticias')
plt.xticks(rotation=45)
plt.legend(title='Palabras Clave')

# Guardar el gráfico como imagen si se desea
plt.tight_layout()
plt.savefig('frecuencia_politica_pobreza_por_mes.png')

# Mostrar el gráfico
plt.show()

print("Proceso terminado")

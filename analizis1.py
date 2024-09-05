import pandas as pd
import spacy 
nlp = spacy.load('es_core_news_md', )

df = pd.read_csv('noticias_extraidas_01.csv',delimiter="|")

def lematizar(texto):
    doc = nlp(texto)
    pbases = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(pbases)


df['contenido_lematizado'] = df['contenido'].apply(lematizar)

print(df['contenido_lematizado'])

palabras_clave = ['accidente', 'choque', 'herido', 'muerto', 'colision','colisión']

def contiene_palabra_clave(noticia, palabras_clave):
    noticia = noticia.lower()
    return any(palabra in noticia for palabra in palabras_clave)

#creamos un nuevo dataframe denominado 'df_accidentes'

df_accidentes = df[df['contenido_lematizado'].apply(lambda x:contiene_palabra_clave(x,palabras_clave))]
df_accidentes.to_csv('noticia_accidentes.csv', sep='|', encoding='utf-8-sig', index=False)


print("proceso terminado")
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import re
import nltk
import unicodedata
from nltk import word_tokenize, sent_tokenize
import textract
import unidecode


# Filtro el corpus de caracteres y palabras que puedan generar inconvenientes al comparar.
def filtrar_corpus(corpus):
    corpus_final =[]

    corpus_filtrado = re.sub('á', 'a', corpus.strip())
    corpus_filtrado = re.sub('é', 'e', corpus_filtrado.strip())
    corpus_filtrado = re.sub('í', 'i', corpus_filtrado.strip())
    corpus_filtrado = re.sub('ó', 'o', corpus_filtrado.strip())
    corpus_filtrado = re.sub('ú', 'u', corpus_filtrado.strip())
    corpus_filtrado = re.sub('●', '', corpus_filtrado.strip())
    corpus_filtrado = re.sub(r'\t+', ' ', corpus_filtrado.strip())
    corpus_filtrado = re.sub(r'\n+', '\n', corpus_filtrado.strip())
    corpus_filtrado = re.sub('\n', '. ', corpus_filtrado.strip())
    corpus_filtrado = re.sub(r'\r+', '\r', corpus_filtrado.strip())
    corpus_filtrado = re.sub('\r', '. ', corpus_filtrado.strip())
    corpus_filtrado = re.sub(r'[.][.]+', '.', corpus_filtrado.strip())
    corpus_filtrado = re.sub(r'[ ][ ]+', ' ', corpus_filtrado.strip())
    corpus_filtrado = re.sub('\xa0', ' ', corpus_filtrado.strip())
    corpus_filtrado = re.sub('\x0c', ' ', corpus_filtrado.strip())
    corpus_filtrado = re.sub('\u200b', ' ', corpus_filtrado.strip())
    corpus_filtrado = re.sub('”', '"', corpus_filtrado.strip())
    corpus_filtrado = re.sub('“', '"', corpus_filtrado.strip())
    
# Tokenizo el corpus en oraciones mediante sent_tokenize
    corpus_tokenizado =  sent_tokenize(corpus_filtrado.strip(), "spanish")
# Filtro el corpus según las expresiones regulares
    corpus_post_regex = [frase for frase in corpus_tokenizado if not filtrar_expresiones_regulares(frase)]
# Reemplazo puntos del corpus
    for x in corpus_post_regex:
            for y in x:
                x = x.replace(".", "")
            corpus_final.append(x)
    
    return corpus_final

# Mediante textract y unicode se convierte el texto en formato utf-8
# Hago uso de NLTK para  tokenizar el corpus 
def unificar_archivo(path):
    archivos_path = os.listdir(path)
    return [(f, filtrar_corpus(textract.process(path + f).decode('utf-8'))) for f in archivos_path]

# Creo lista de expresiones regulares ya que no quiero considerar puntuaciones, inicio de oraciones con números 
# y determinados tokens a la hora de comparar
lista_expresiones_regulares=[
    r"universidad tecnologica nacional|utn|frba|facultad regional buenos aires|ingenieria en sistemas de informacion|fuente|ingenieria en sistemas",
    r"grafique|marketing en internet y nueva economia|nueva economia|marketing en internet|y nueva economia",
    r"^fecha de entrega|cuatrimestre|curso|profesor|legajo|ayudante|email|mail|trabajo practico",
    r"(^|\s)[0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]*(\)|.-|\s-)", 
    r"^\s*[0,1,2,3,4,5,6,7,8,9,a,b,c,d,e,f,g,h,i,j,k,l,m,n,o,p,q,r,s,t,u,v,w,x,y,z]*.-",
    r"^consigna",
    r"^$", 
    r"^\s$",
    r"hernan borre",
    r"alejandro prince",
    r"\[pic\]"
]

def filtrar_expresiones_regulares(oracion):
    for x in lista_expresiones_regulares:
        if re.search(x, unidecode.unidecode(oracion.lower())): 
            return True
    return False







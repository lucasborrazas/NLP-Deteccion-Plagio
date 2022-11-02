#!/usr/bin/env python
# coding: utf-8

# In[1]:


from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
import nltk
from nameparser.parser import HumanName
from nltk.corpus import treebank
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import LatentDirichletAllocation as LDA
from nltk.corpus import stopwords
import nltk.stem

# Lógica de comparación entre archivos
def procesar_plagio(dataset, tp_a_evaluar):
    lista_frases_plagiadas = []
    text_tp = ""
    text_dataset = ""
    sentence_tp = ""
    sentence_dataset = ""
    lista_porcentaje = []

    for t_dataset in dataset:
        for s_dataset in t_dataset[1]:
            for t_tp in tp_a_evaluar:
                for s_tp in t_tp[1]:
                    s_tp_stem = aplicar_stem(s_tp)
                    s_dataset_stem = aplicar_stem(s_dataset)
                    porcentaje_parcial = calculo_similitud_coseno(s_tp_stem, s_dataset_stem)
                    if porcentaje_parcial > 0.6:
                        lista_porcentaje.append(porcentaje_parcial)
                        sentence_tp = s_tp
                        sentence_tp_order = str(t_tp[1].index(s_tp) + 1)
                        text_dataset = t_dataset[0]
                        sentence_dataset = s_dataset
                        sentence_dataset_order = str(t_dataset[1].index(s_dataset) + 1)
                        lista_frases_plagiadas.append((sentence_tp, sentence_tp_order, sentence_dataset, text_dataset, sentence_dataset_order))
            nombre_alumno = nombre_estudiante(t_tp[1])
            text_tp = t_tp[0]
        main_topics = identificar_topicos(t_tp[1])
    porcentaje_plagio_final = str(round((sum(lista_porcentaje) / len(t_tp[1]) *100))) + '%'
    topicos = [item for x in main_topics for item in x]
    nombre_archivo_tp = text_tp
    
    return (nombre_archivo_tp, nombre_alumno, lista_frases_plagiadas, porcentaje_plagio_final, main_topics)




#La similitud coseno es una medida de similitud entre dos vectores 
#en un espacio que posee un producto interior con el que se evalúa el valor
#del coseno del ángulo comprendido entre ellos. 
#Si el valor = 1, el ángulo comprendido es cero, es decir las dos frases son iguales
def calculo_similitud_coseno(frase1, frase2):
    X_list = word_tokenize(frase1.lower())  
    Y_list = word_tokenize(frase2.lower()) 
  
    stopwords_spanish = stopwords.words('spanish')
    other_words = ['preguntas', 'respuestas', 'nombre', 'practico', 'legajo', 'universidad tecnologica nacional', 'utn', 'frba','lucas', 'nahuel', 'cero', ':', '?', 'trabajo',  'cuatrimestre', 'catedra', 'hernan borre', 'alejandro prince', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez']
    for x in other_words:
        stopwords_spanish.append(x)

    l1 =[];l2 =[] 
  
    X_set = {w for w in X_list if not w in stopwords_spanish}  
    Y_set = {w for w in Y_list if not w in stopwords_spanish} 
  
    rvector = X_set.union(Y_set)  
    for w in rvector: 
        if w in X_set: l1.append(1) 
        else: l1.append(0) 
        if w in Y_set: l2.append(1) 
        else: l2.append(0) 

    c = 0
  
    for i in range(len(rvector)): 
        c+= l1[i]*l2[i] 
    
    if (sum(l1)*sum(l2) == 0):
        cosine = 0
    else: 
        cosine = c / float((sum(l1)*sum(l2))**0.5) 

    return cosine

# Funcion para identificar nombres propios tokenizando la cadena mediante word_tokenize
# y el uso de NLTK trees
def nombres_propios(texto):
    tokens = nltk.tokenize.word_tokenize(texto)
    pos = nltk.pos_tag(tokens)
    sentt = nltk.ne_chunk(pos, binary = False)
    person_list = []
    person = []
    name = ""
    for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
        for leaf in subtree.leaves():
            person.append(leaf[0])
        if len(person) > 1: 
            for part in person:
                name += part + ' '
            if name[:-1] not in person_list:
                person_list.append(name[:-1])
            name = ''
        person = []
    return person_list

# Detección de nombre de alumnos
def nombre_estudiante(frases):
    nombres = []
    oraciones_posibles = []
    for frase in frases:
        if "nombre" in frase.lower() or "alumno" in frase.lower() or "integrantes" in frase.lower() or "estudiante" in frase.lower():
            oraciones_posibles.append(frase)

    for x in oraciones_posibles:
        lista_nombres = nombres_propios(x)
        for name in lista_nombres: 
            last_first = HumanName(name).first + ' ' + HumanName(name).last
            nombres.append(last_first)
    return nombres



# Identifico los tópicos del texto mediante la creación de una bolsa de palabras con  el uso defit_transform

def identificar_topicos(texto):
    stp_words = stopwords.words('spanish')
    otras_stp_words = ['fuente', 'proceso', 'procesos', 'memoria', 'trabajo', 'practico', 'legajo', 'fuente', 'universidad tecnologica nacional', 'utn', 'frba', 'email', 'cuatrimestre', 'catedra', 'hernan borre', 'alejandro prince', 'preguntas', 'respuestas', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez',]
    for x in otras_stp_words:
        stp_words.append(x)

    count_vect = CountVectorizer(stop_words=stp_words, lowercase=True)
    x_counts = count_vect.fit_transform(texto)

    tfidf_transformer = TfidfTransformer()
    x_tfidf = tfidf_transformer.fit_transform(x_counts)

    dimension = 1
    lda = LDA(n_components = dimension)
    lda_array = lda.fit_transform(x_tfidf)
    lda_array

    componentes = [lda.components_[i] for i in range(len(lda.components_))]
    features = count_vect.get_feature_names()
    lista_topicos = [sorted(features, key = lambda x: componentes[j][features.index(x)], reverse = True)[:3] for j in range(len(componentes))]
    return lista_topicos

# Mediante el stemmer podemos obtener la raíz de los tokens para luego evaluar posibles parafraseos
spanish_stemmer	= nltk.stem.SnowballStemmer('spanish')
class StemmedCountVectorizer(CountVectorizer):
    def build_analyzer(self):
        analyzer = super(StemmedCountVectorizer, self).build_analyzer()
        return lambda doc: (spanish_stemmer.stem(w) for w in analyzer(doc))
    
def aplicar_stem(oracion):
    oracion_stemeada = []
    stopwords_spanish = stopwords.words('spanish')
    other_words = ['preguntas', 'respuestas', 'nombre', 'practico', 'legajo', 'universidad tecnologica nacional', 'utn', 'frba','lucas', 'nahuel', 'cero', ':', '?', 'trabajo',  'cuatrimestre', 'catedra', 'hernan borre', 'alejandro prince', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete', 'ocho', 'nueve', 'diez']
    for x in other_words:
        stopwords_spanish.append(x)
    
    stem_vectorizer_spanish = StemmedCountVectorizer(min_df=1, stop_words=stopwords_spanish)
    stem_analyze_spanish = stem_vectorizer_spanish.build_analyzer()
    Z = stem_analyze_spanish(oracion)
    for tok in Z:
        oracion_stemeada.append(tok)
    
    oracion_stemeada_concat = ' '.join(str(e) for e in oracion_stemeada)
    
    return oracion_stemeada_concat






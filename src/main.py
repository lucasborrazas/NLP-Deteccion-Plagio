#!/usr/bin/env python
# coding: utf-8

# In[1]:


import configparser
import sys
from funciones_plagio import procesar_plagio 
from funciones_pdf import exportar_a_pdf
from funciones_archivos import unificar_archivo

def main():
    print("*****Comienza el programa de deteccion de plagio*****", flush=True)
    archivo_config = configparser.ConfigParser()
    
#   Lectura del archivo de configuración. En el mismo tendremos los path de interés (entrenamiento, tp a evaluar y resultado)
    archivo_config.read('../config.ini')
    path_entrenamiento = archivo_config['PATH']['ENTRENAMIENTO']
    path_tp_alumno = archivo_config['PATH']['TP_ALUMNO']
    
#  Mediante unificar_archivo envío cada directorio y obtengo los archivos unificados sin tildes, caracteres especiales, saltos de línea, entre otros
    tp_archivo_alumno = unificar_archivo(path_tp_alumno)
    dataset_archivos = unificar_archivo(path_entrenamiento)
    
# Valido existencia de archivos
    if tp_archivo_alumno == []:
        sys.exit('No se ha encontrado ningun TP para procesar.\n Por favor cargue un archivo.')
    elif dataset_archivos ==[]:
        sys.exit('No se ha encontrado ningun dataset para analizar.\n Por favor cargue los archivos necesarios.')
    else:
        archivo_a_procesar = tp_archivo_alumno[0][0]
        mensaje_archivo_proceso = 'Procesando archivo ' + archivo_a_procesar + '...'
        print(mensaje_archivo_proceso, flush=True)

# Una vez unificado cada corpus, se procede a analizarlos para detectar frases plagiadas, extraer el nombre del alumno,
# lista de oraciones, el porcentaje general de plagio y tópicos del TP
    (nombre_archivo, nombre_alumno, lista_frases, porcentaje, los_topicos) = procesar_plagio(dataset_archivos, tp_archivo_alumno)
    print('*****El analisis ha finalizado de forma correcta*****', flush=True)

# La función exportar_a_pdf genera el archivo, lo sube al path indicado en config y retorna la ubicación para imprimirla por pantalla
    ubicacion_pdf = exportar_a_pdf(nombre_archivo, nombre_alumno, lista_frases, porcentaje, los_topicos)
    mensaje_fin = 'El resultado se encuentra disponible en: '+ ubicacion_pdf
    print(mensaje_fin, flush=True)

if __name__ == "__main__":
    main()


# In[ ]:





# In[ ]:





# In[ ]:





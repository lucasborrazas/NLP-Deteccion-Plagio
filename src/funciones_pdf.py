#!/usr/bin/env python
# coding: utf-8

# In[1]:


from fpdf import FPDF
from pathlib import Path
import datetime
import configparser
import os.path

config = configparser.ConfigParser()

# Creo clase PDF con funciones header y footer para que aparezcan en todas las páginas
class PDF(FPDF):
    def header(self):
        current_time = datetime.datetime.now()
        fecha_hoy = str(current_time.day) + "-" + str(current_time.month) + "-" + str(current_time.year)
        self.image('../logo-utn.png', 5, 8, 50)
        self.set_font('helvetica', '', 11)
        self.cell(0, 15, fecha_hoy, border=False, ln=1, align='R')
        self.ln(1)
        
    def footer(self):
        self.set_y(-15)
        self.set_font('helvetica', 'I', 9)
        self.set_text_color(84, 84, 84)
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='R')
        self.set_font('helvetica', 'BI', 10)
        self.set_text_color(196, 12, 46)
        self.cell(-375, 10, 'PLN - 2022', border=False, ln=1, align='C')    
    

def exportar_a_pdf(archivo, alumno, frases, porcentaje, topicos_tp):
    config.read('../config.ini')
    path_entrena = config['PATH']['ENTRENAMIENTO']

    nombre_tp_archivo_evaluar = "       Archivo procesado: " + archivo
    estudiante_nombre = "       Estudiante: " + alumno[0]
    plagio_general = "       Porcentaje general de plagio: " + porcentaje
    lista_topicos = ", ".join(topicos_tp[0])
    topicos_tp_evaluar = "       Tópicos: " + lista_topicos

#   Creación de PDF en formato Letter
    pdf = PDF('P', 'mm', 'Letter')

#   Agrego página
    pdf.add_page()

#   especifico fuente y ubicación del título
    pdf.set_font('helvetica', 'BU', 24)
    pdf.cell(190, 30, "Análisis de detección de plagio", ln = 0, align = 'C')
    pdf.ln(25)

#   Completos datos generales
    pdf.set_font('helvetica', '', 15)
    pdf.image('../logo-file.png', 10, 54, 8)
    pdf.cell(10, 15, nombre_tp_archivo_evaluar, ln = 1, align = 'L')
    pdf.image('../logo-student.png', 10, 68, 9)
    pdf.cell(10, 15, estudiante_nombre, ln = 1, align = 'L')
    pdf.image('../logo-topics.png', 10, 84, 8)
    pdf.cell(10, 15, topicos_tp_evaluar, ln = 1, align = 'L')
    pdf.image('../logo-kpi.png', 10, 99, 8)
    pdf.cell(10, 15, plagio_general, ln = 1, align = 'L')
    pdf.ln(5)

# Fuente y colores del encabezado de la tabla
    pdf.set_font('helvetica', 'B', 11)
    pdf.set_fill_color(196, 12, 46)
    pdf.set_text_color(255, 255, 255)

    pdf.multi_cell(60, 15, txt = 'Frase plagiada', border = 'T',ln=3,
             align = 'C', fill = 1)

    pdf.multi_cell(20, 15, txt = 'N° frase', border = 'T',ln=3,
             align = 'C', fill = 1)

    pdf.multi_cell(60, 15, txt = 'Frase original', border = 'T',ln=3,
             align = 'C', fill = 1)

    pdf.multi_cell(35, 15, txt = 'Archivo original', border = 'T',ln=3,
             align = 'C', fill = 1)

    pdf.multi_cell(20, 15, txt = 'N° frase', border = 'T',ln=1,
             align = 'C', fill = 1)


#   Creación de tabla con frases plagiadas    
    line_height = pdf.font_size
    col_width = pdf.epw / 4
    pdf.set_font('helvetica', '', 11)
    pdf.set_text_color(0, 0, 0)

    for valor in frases:
#       Creo link para los archivos que fueron plagiados
        new_link = path_entrena + valor[3]
        hipervinculo = os.path.abspath(new_link)
    
        pdf.set_font('helvetica', 'I', 11)
        pdf.multi_cell(60, pdf.font_size, txt = valor[0], border = 'T',ln=3,  max_line_height=pdf.font_size,
                  align = 'L', fill = 0)
        cant_frase_plagiada = len(valor[0])
    
        pdf.set_font('helvetica', '', 11)
        pdf.multi_cell(20, pdf.font_size, txt = valor[1], border = 'T',ln=3, max_line_height=pdf.font_size,
            align = 'C', fill = 0)
    
        pdf.set_font('helvetica', 'I', 11)
        pdf.multi_cell(60, pdf.font_size, txt = valor[2], border = 'T',ln=3, max_line_height=pdf.font_size,
            align = 'L', fill = 0)
        cant_frase_original = len(valor[2])
    
        pdf.set_font('helvetica', 'U', 11)
        pdf.set_text_color(28, 59, 255)
        pdf.multi_cell(35, pdf.font_size, txt = valor[3], border = 'T',ln=3, max_line_height=pdf.font_size,
            align = 'C', fill = 0, link = hipervinculo)
    
        cant_titulo_original = len(valor[3])
        pdf.set_font('helvetica', '', 11)
        pdf.set_text_color(0, 0, 0)

        pdf.multi_cell(20, pdf.font_size, txt = valor[4], border = 'T',ln=3, max_line_height=pdf.font_size,
            align = 'C', fill = 0)

#       Lógica para calcular el alto máximo de cada fila
        list_frases = [cant_frase_plagiada, cant_frase_original, cant_titulo_original]
        max_list_frases = max(list_frases)
        if max_list_frases < 21:
            line_height = pdf.font_size * 3
        else:
            line_height = pdf.font_size * max_list_frases / 25
    
        pdf.ln(line_height)
#   Lectura del path en donde queremos exportar el resultado
    config.read('../config.ini')
    path_output = config['PATH']['OUTPUT']
    archivo_pdf_final = path_output + 'Analisis_plagio_' + archivo.split(".")[0] + '.pdf'
    pdf.output(archivo_pdf_final)
    return archivo_pdf_final






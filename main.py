import numpy as np
import csv
import matplotlib.pyplot as plt

#convertir CSV to Array text
csv_filename = './dataset/dataset_3.csv'
with open(csv_filename,newline='', encoding='utf-8') as f:
    reader = csv.reader(f,delimiter=';') 
    next(reader) #omite el encabezado
    array_csv_lista = list(reader)
    array_text_lista = np.array(array_csv_lista) #convierte lista en array

# Crear una matriz para almacenar los valores de punto flotante
matriz_float = np.empty_like(array_text_lista, dtype=float)

# Recorrer la matriz y convertir las cadenas en números de punto flotante
for i in range(array_text_lista.shape[0]):
    for j in range(array_text_lista.shape[1]):
        elemento_str = array_text_lista[i, j]
        elemento_float = float(elemento_str.replace(',', '.'))
        matriz_float[i, j] = elemento_float

#graficar los puntos recorriendo la matriz matriz_float
for fila in matriz_float:
    plt.plot(fila[0],fila[1],marker ="o",color ="green")

plt.show()
import numpy as np
import csv
import matplotlib.pyplot as plt

# Cargar y preprocesar el dataset desde un archivo CSV
def cargar_dataset(csv_filename):
    with open(csv_filename, newline='', encoding='utf-8') as f:
        reader = csv.reader(f, delimiter=';')
        next(reader)  
        array_csv_lista = list(reader)
        array_text_lista = np.array(array_csv_lista)  

    # Almacenar los numeros en float
    matriz = np.empty_like(array_text_lista, dtype=float)
    for i in range(array_text_lista.shape[0]):
        for j in range(array_text_lista.shape[1]):
            elemento_str = array_text_lista[i, j]
            elemento_float = float(elemento_str.replace(',', '.'))
            matriz[i, j] = elemento_float

    return matriz

def graficar_resultados(matriz, asignaciones, centroides):

    k = len(centroides)

    for i in range(k):
        puntos_cluster_i = matriz[asignaciones == i]
        #los colores se asignan automaticamente
        plt.scatter(puntos_cluster_i[:, 0], puntos_cluster_i[:, 1], label=f'Cluster {i + 1}')

    plt.scatter(centroides[:, 0], centroides[:, 1], marker='X', s=100, c='black', label='Centroides')
    plt.legend()
    plt.title('Resultados de K-Means')
    plt.xlabel('Eje X')
    plt.ylabel('Eje Y')
    plt.show()

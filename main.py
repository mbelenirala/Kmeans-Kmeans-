import ControladorDataset
import ControladorKmeans
import numpy as np


# Definir el número del dataset que deseas cargar (1, 2 o 3)
dataset = 1
csv = f'./dataset/dataset_{dataset}.csv'
matriz = ControladorDataset.cargar_dataset(csv)


#VER: si es necesario estandarizar los valores del dataset (segun la teoria recomendaba estadarizar)
min_val = np.min(matriz, axis=0)
max_val = np.max(matriz, axis=0)
matriz_estandarizada = (matriz - min_val) / (max_val - min_val)

#Valores de k a considerar (de 2 a 5)
valores_k = [2, 3, 4, 5]

# Criterio de parada (1: No haya ninguna reasignación, 2: No haya ningún cambio de centroides)
# VER: criterio de parada 3
criterioParada = 1  

# print("Matriz estandarizada:")
# for fila in matriz_estandarizada:
#     print(fila)

for k in valores_k:
    centroides, asignaciones = ControladorKmeans.k_means(matriz_estandarizada, k, criterioParada)
    
    inercia = 0
    for i in range(len(matriz_estandarizada)):
        punto = matriz_estandarizada[i]
        cluster_id = asignaciones[i]
        centroide = centroides[cluster_id]
        distancia_cuadrada = sum((punto - centroide)**2)
        inercia += distancia_cuadrada
    
    print(f'Clusters para k={k}, Inercia: {inercia}')
    ControladorDataset.graficar_resultados(matriz_estandarizada, asignaciones, centroides)

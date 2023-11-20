import numpy as np
import math
import ControladorDataset
from sklearn.datasets import load_iris
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score
import matplotlib.pyplot as plt

def mostrar_resultados_kmeans(matriz_estandarizada, k, criterio_parada):
    centroides, asignaciones = k_means(matriz_estandarizada, k, criterio_parada)
    ControladorDataset.graficar_resultados(matriz_estandarizada, asignaciones, centroides)

def distanciaEuclidiana(a, b):
    sumaCuadrados = sum((x - y) ** 2 for x, y in zip(a, b))
    distancia = math.sqrt(sumaCuadrados)
    return distancia

# Función para encontrar el centroide más cercano
def centroideMasCercano(punto, centroides):
    distancia_minima = float('inf')
    centroideCercano = None

    for i, centroide in enumerate(centroides):
        distancia = distanciaEuclidiana(punto, centroide)
        if distancia < distancia_minima:
            distancia_minima = distancia
            centroideCercano = i

    return centroideCercano

# Función para obtener la media de los puntos de un cluster (para luego definir el nuevo centroide)
def mediaDatos(puntos):
    suma = [0,0]

    for dato in puntos:
        suma += dato
    media = suma/len(puntos)

    return media

# Fución para la inicializacion heurística de k means ++
def heuristica(datos, k):

    # Elegir el primer centroide
    # centroides = datos[np.random.choice(range(len(datos)), 1, replace=False)]      #ELEGIDO ALEATORIAMENTE
    punto_medio = mediaDatos(datos)
    distancia_minima = float('inf')
    datoCercano = None
    for dato in datos:
        distancia = distanciaEuclidiana(dato,punto_medio)
        if distancia<distancia_minima:
            distancia_minima = distancia
            datoCercano = dato
    centroides = [datoCercano]

    k_restantes = k-1

    while(k_restantes):
        distancias_maximas = np.full(len(datos), np.inf)
        
        for i, centroide in enumerate(centroides):
            for j, dato in enumerate(datos):
                distancia_nueva = distanciaEuclidiana(dato,centroide)
                if(distancia_nueva <= distancias_maximas[j]):
                    distancias_maximas[j] = distancia_nueva
        
        centroides = np.vstack([centroides, datos[np.argmax(distancias_maximas)]])
        print(np.argmax(distancias_maximas))
        print(datos[np.argmax(distancias_maximas)])

        k_restantes -=1

    print(centroides)   #centroides iniciales
    return centroides

def k_means(datos, k, inicializacion):

    #aqui se ejecuta condicionalmente la inicializacion elegida
    if(inicializacion):
        centroides = datos[np.random.choice(range(len(datos)), k, replace=False)]   #k means normal
        print(centroides)   #centroides iniciales
    else:
        centroides = heuristica(datos, k)   #k means ++

    asignaciones_previas = np.empty(0)
    centroides_iniciales = centroides.copy() 
    iteracion = 1
    paso_a_paso = f'Centroides iniciales:\n'
    for i, centroide in enumerate(centroides):
        paso_a_paso += f'Centroide {i + 1}: {tuple(map(lambda x: round(x, 2), centroide))}\n'
    paso_a_paso += "\n"

    while True:
        
        # Asigna cada punto al centroide más cercano
        asignaciones = []
        for punto in datos:
            centroideCercano = centroideMasCercano(punto, centroides)
            asignaciones.append(centroideCercano)
        
        asignaciones = np.array(asignaciones)
        
        # Actualizar los centroides como el promedio de los puntos asignados
        nuevos_centroides = []
        for i in range(k):
            cluster_points = datos[asignaciones == i]
            if len(cluster_points) > 0:
                nuevo_centroide = mediaDatos(cluster_points)
                nuevos_centroides.append(nuevo_centroide)
            else:
                nuevos_centroides.append(centroides[i])
        
        nuevos_centroides = np.array(nuevos_centroides)
        #print ("Centroides actualizados:\n")
        #paso_a_paso += "Centroides actualizados:\n"
        
        
        if np.all(centroides == nuevos_centroides) or np.array_equal(asignaciones, asignaciones_previas):
            
            if np.array_equal(asignaciones, asignaciones_previas): 
              print("Criterio de parada 1 alcanzado: No hay reasignaciones en los cluster.")
              paso_a_paso += "Criterio de parada 1 alcanzado: No hay reasignaciones en los cluster.\n"
            else: 
                if np.all(centroides == nuevos_centroides):
                    print("Criterio de parada 2 alcanzado: No hay cambios en los centroides.")
                    paso_a_paso += "Criterio de parada 2 alcanzado: No hay cambios en los centroides.\n"
            break
        
        print (f'Iteración {iteracion}')
        paso_a_paso += f'Iteración {iteracion}\n'
        iteracion += 1

        for i, centroide in enumerate(nuevos_centroides):
            print(f'Centroide {i + 1}: {centroide}')
            paso_a_paso += f'Centroide {i + 1}: {tuple(map(lambda x: round(x, 2), centroide))}\n'
            

        centroides = nuevos_centroides
        
        asignaciones_previas = asignaciones.copy()
    
    paso_a_paso += "\n\nRESULTADOS:\n"
    paso_a_paso += f'Cantidad de iteraciones necesarias: {(iteracion-1)}\n\n'
    paso_a_paso += "Porcentaje de elementos agrupados en:"

    for i in range(k):
        cluster_points = datos[asignaciones == i]
        porcentaje_agrupados = len(cluster_points)*100/len(datos)
        porcentaje_agrupados = round(porcentaje_agrupados,2)
        paso_a_paso += f'\nCluster {(i+1)}: {porcentaje_agrupados}'
    
    #ch_score = scoreCalisnkiHarabasz(datos,asignaciones)
    #paso_a_paso += f'Calinski-Harabasz Score: {ch_score}\n'
    
    return centroides_iniciales, centroides, asignaciones, paso_a_paso

# Función para calcular el Calinski-Harabasz Score
def scoreCalisnkiHarabasz(datos, asignaciones):
    ch_score = calinski_harabasz_score(datos, asignaciones)
    #print(f'C-H Score: {ch_score}')
    ch_score = round(ch_score,2)
    print(f'C-H Score: {ch_score}')
    
    return ch_score
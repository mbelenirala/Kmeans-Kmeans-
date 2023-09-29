import numpy as np
import math

def distanciaEuclidiana(a, b):
    sumaCuadrados = sum((x - y) ** 2 for x, y in zip(a, b))
    distancia = math.sqrt(sumaCuadrados)
    return distancia

# Función para encontrar el centroide más cercano
def centroideMasCercano(punto, centroides):
    distancia_minima = float('inf')
    centroide_mas_cercano = None

    for i, centroide in enumerate(centroides):
        distancia = distanciaEuclidiana(punto, centroide)
        if distancia < distancia_minima:
            distancia_minima = distancia
            centroide_mas_cercano = i

    return centroide_mas_cercano

def k_means(datos, k, criterio_parada):

    #VER capaz hay que definir otra manera de iniciar aleatoriamente segun lo planteado en el tp
    centroides = datos[np.random.choice(range(len(datos)), k, replace=False)]
    asignaciones_previas = np.empty(0)
    
    iteracion = 1
    while True:
        print(f'Iteración {iteracion}:')
        
        # Asigna cada punto al centroide más cercano
        asignaciones = []
        for punto in datos:
            centroide_mas_cercano = centroideMasCercano(punto, centroides)
            asignaciones.append(centroide_mas_cercano)
        
        asignaciones = np.array(asignaciones)
        
        # Criterio de parada 1: No haya ninguna reasignación de datos a diferentes clusters
        if criterio_parada == 1 and np.array_equal(asignaciones, asignaciones_previas):
            print("Criterio de parada 1 alcanzado: No hay reasignaciones.")
            break
        
        # Actualizar los centroides como el promedio de los puntos asignados
        nuevos_centroides = []
        for i in range(k):
            cluster_points = datos[asignaciones == i]
            if len(cluster_points) > 0:
                nuevo_centroide = np.mean(cluster_points, axis=0)
                nuevos_centroides.append(nuevo_centroide)
            else:
                nuevos_centroides.append(centroides[i])
        
        nuevos_centroides = np.array(nuevos_centroides)
        
        print("Centroides actualizados:")
        for i, centroide in enumerate(nuevos_centroides):
            print(f'Centroide {i + 1}: {centroide}')
        
        # Criterio de parada 2: No haya ningún cambio en los centroides
        if criterio_parada == 2 and np.all(centroides == nuevos_centroides):
            print("Criterio de parada 2 alcanzado: No hay cambios en los centroides.")
            break
        
        centroides = nuevos_centroides
        
        asignaciones_previas = asignaciones.copy()
        
        iteracion += 1
    
    return centroides, asignaciones

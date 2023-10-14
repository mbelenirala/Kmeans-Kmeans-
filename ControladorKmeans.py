import numpy as np
import math
import ControladorDataset

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

def k_means(datos, k, criterio_parada):

    centroides = datos[np.random.choice(range(len(datos)), k, replace=False)]
    asignaciones_previas = np.empty(0)

    iteracion = 1
    paso_a_paso = f'Centroides iniciales:\n'
    for i, centroide in enumerate(centroides):
        paso_a_paso += f'Centroide {i + 1}: {centroide}\n'

    while True:
        print (f'Iteración {iteracion}')
        paso_a_paso += f'Iteración {iteracion}\n'
        
        # Asigna cada punto al centroide más cercano
        asignaciones = []
        for punto in datos:
            centroideCercano = centroideMasCercano(punto, centroides)
            asignaciones.append(centroideCercano)
        
        asignaciones = np.array(asignaciones)
        
        # Criterio de parada 1: No haya ninguna reasignación de datos a diferentes clusters
        if criterio_parada == 1 and np.array_equal(asignaciones, asignaciones_previas):
            print ("Criterio de parada 1 alcanzado: No hay reasignaciones.\n")
            paso_a_paso += "Criterio de parada 1 alcanzado: No hay reasignaciones.\n"
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
        #print ("Centroides actualizados:\n")
        #paso_a_paso += "Centroides actualizados:\n"
        for i, centroide in enumerate(nuevos_centroides):
            print(f'Centroide {i + 1}: {centroide}')
            paso_a_paso += f'Centroide {i + 1}: {centroide}\n'
        
        # Criterio de parada 2: No haya ningún cambio en los centroides
        if criterio_parada == 2 and np.all(centroides == nuevos_centroides):
            print("Criterio de parada 2 alcanzado: No hay cambios en los centroides.")
            paso_a_paso += "Criterio de parada 2 alcanzado: No hay cambios en los centroides.\n"
            break
        
        centroides = nuevos_centroides
        
        asignaciones_previas = asignaciones.copy()
        
        iteracion += 1

    return centroides, asignaciones, paso_a_paso

def mostrar_resultados_kmeans_plus_plus(matriz_estandarizada, k, criterio_parada):
    # Por ahora, no hacemos nada en esta función
    pass
import numpy as np
import matplotlib.pyplot as plt

def calcular_punto_medio(puntos):
    """
    Calcula el punto medio de un conjunto de puntos usando NumPy para optimización.
    
    Args:
        puntos: Lista de tuplas (x, y) que representan las coordenadas de los puntos
        
    Returns:
        Tupla (x, y) con las coordenadas del punto medio
    """
    # Convertir a array de NumPy y calcular la media
    puntos_array = np.array(puntos)
    punto_medio = puntos_array.mean(axis=0)
    
    # Devolver como tupla para mantener consistencia
    return tuple(punto_medio)

def subdividir_triangulo(ids_triangulo, puntos, id_contador):
    """
    Subdivide un triángulo en 3 triángulos utilizando el punto medio.
    
    Args:
        ids_triangulo: Lista de 3 IDs que identifican los vértices del triángulo
        puntos: Diccionario con los puntos actuales {id: (x, y)}
        id_contador: Contador para asignar nuevos IDs
        
    Returns:
        Tupla con:
        - Lista de nuevos triángulos (cada uno como lista de 3 IDs)
        - Diccionario actualizado de puntos
        - Nuevo valor del contador de IDs
        - ID del punto medio creado
    """
    # Obtener coordenadas de los vértices
    coords_triangulo = [puntos[id_punto] for id_punto in ids_triangulo]
    
    # Calcular el punto medio
    punto_medio = calcular_punto_medio(coords_triangulo)
    
    # Asignar ID al nuevo punto (punto medio)
    id_punto_medio = id_contador
    id_contador += 1
    
    # Añadir el nuevo punto al diccionario
    puntos[id_punto_medio] = punto_medio
    
    # Crear los 3 nuevos triángulos (usando IDs)
    triangulo1 = [ids_triangulo[0], ids_triangulo[1], id_punto_medio]
    triangulo2 = [ids_triangulo[1], ids_triangulo[2], id_punto_medio]
    triangulo3 = [ids_triangulo[2], ids_triangulo[0], id_punto_medio]
    
    return [triangulo1, triangulo2, triangulo3], puntos, id_contador, id_punto_medio

def triangulacion_iterativa(triangulo_inicial, nivel_max):
    """
    Realiza la triangulación de manera iterativa hasta un nivel máximo.
    
    Args:
        triangulo_inicial: Lista de 3 tuplas (x, y) que representan los vértices del triángulo inicial
        nivel_max: Número máximo de niveles de subdivisión
        
    Returns:
        Tupla con tres elementos:
        - puntos: Diccionario {id: (x, y)} con todas las coordenadas
        - vertices: Lista con los IDs de los 3 vértices principales originales
        - adyacencias: Diccionario {id: [id1, id2, ...]} con las conexiones entre puntos
    """
    # Inicializar el diccionario de puntos con los vértices originales
    puntos = {0: triangulo_inicial[0], 1: triangulo_inicial[1], 2: triangulo_inicial[2]}
    
    # Guardar los IDs de los vértices principales
    vertices = [0, 1, 2]
    
    # Inicializar con el triángulo inicial (usando IDs)
    triangulos_actuales = [[0, 1, 2]]
    
    # Inicializar contador para nuevos IDs
    id_contador = 3
    
    # Inicializar diccionario de adyacencias
    adyacencias = {0: [1, 2], 1: [0, 2], 2: [0, 1]}
    
    # Si no hay subdivisiones, devolver directamente
    if nivel_max == 0:
        return puntos, vertices, adyacencias
    
    # Procesar cada nivel
    for nivel in range(nivel_max):
        nuevos_triangulos = []
        
        # Subdividir cada triángulo del nivel actual
        for triangulo in triangulos_actuales:
            nuevos_triangs, puntos, id_contador, id_medio = subdividir_triangulo(triangulo, puntos, id_contador)
            nuevos_triangulos.extend(nuevos_triangs)
            
            # Actualizar adyacencias
            # Conectar el punto medio con los vértices del triángulo original
            adyacencias[id_medio] = triangulo.copy()
            
            # Conectar los vértices originales con el punto medio
            for v_id in triangulo:
                if v_id in adyacencias:
                    adyacencias[v_id].append(id_medio)
                else:
                    adyacencias[v_id] = [id_medio]
        
        # Actualizar la lista de triángulos para el siguiente nivel
        triangulos_actuales = nuevos_triangulos
    
    # Asegurar que no hay duplicados en las listas de adyacencias
    for punto_id in adyacencias:
        adyacencias[punto_id] = list(set(adyacencias[punto_id]))
    
    return puntos, vertices, adyacencias
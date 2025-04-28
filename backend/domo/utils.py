import numpy as np

def transformar_puntos_baricentricos(puntos_triangulo_antiguo, vertices_triangulo_antiguo, vertices_triangulo_nuevo):
    """
    Transforma puntos desde un triángulo de origen a un triángulo destino usando coordenadas baricéntricas.
    Implementación completamente vectorizada para máxima eficiencia.
    
    Args:
        puntos_triangulo_antiguo: Diccionario donde la clave es el id del punto y el valor es una tupla (x, y)
        vertices_triangulo_antiguo: Lista de tuplas [(x1, y1), (x2, y2), (x3, y3)] del triángulo de origen
        vertices_triangulo_nuevo: Lista de tuplas [(x1, y1), (x2, y2), (x3, y3)] del triángulo destino
        
    Returns:
        Diccionario con los mismos ids pero con coordenadas transformadas
    """
    # Convertir vértices a arrays de numpy
    v_origen = np.array(vertices_triangulo_antiguo)
    v_destino = np.array(vertices_triangulo_nuevo)
    
    # Preparar matriz de transformación para coordenadas baricéntricas
    matriz_origen = np.vstack([
        v_origen.T,  # Transpuesta de los vértices (x,y como filas)
        np.ones(3)   # Fila de unos
    ])
    matriz_origen_inv = np.linalg.inv(matriz_origen)
    
    # Extraer los IDs y coordenadas
    ids = list(puntos_triangulo_antiguo.keys())
    puntos = np.array([puntos_triangulo_antiguo[id_punto] for id_punto in ids])
    
    # Añadir columna de unos para hacer homogéneas las coordenadas
    puntos_homogeneos = np.column_stack([puntos, np.ones(len(puntos))])
    
    # Calcular coordenadas baricéntricas para todos los puntos a la vez
    # (n_puntos, 3) = (n_puntos, 3) @ (3, 3)
    lambdas = puntos_homogeneos @ matriz_origen_inv.T
    
    # Transformar al nuevo triángulo usando coordenadas baricéntricas
    # (n_puntos, 2) = (n_puntos, 3) @ (3, 2)
    nuevos_puntos = lambdas @ v_destino
    
    # Reconstruir el diccionario de resultados
    puntos_transformados = {ids[i]: tuple(nuevos_puntos[i]) for i in range(len(ids))}
    
    return puntos_transformados

def generar_poligono_regular(n_lados):
    """
    Genera los vértices de un polígono regular con el número de lados especificado
    y longitud de lado igual a 1, donde los dos primeros puntos son (0,0) y (1,0).
    
    Args:
        n_lados: Número de lados del polígono
        
    Returns:
        Una lista de tuplas (x, y) con las coordenadas de los vértices
    """
    if n_lados < 3:
        raise ValueError("El número de lados debe ser al menos 3")
    
    vertices = []
    
    # Añadir los dos primeros puntos fijos
    vertices.append((0, 0))
    vertices.append((1, 0))
    
    # Calcular el ángulo interior de un polígono regular
    angulo_interior = np.pi * (n_lados - 2) / n_lados
    # El ángulo exterior (el complemento del ángulo interior)
    angulo_exterior = np.pi - angulo_interior
    
    # Posición actual
    x_actual, y_actual = 1, 0
    # Dirección actual (empezamos hacia la derecha, ahora necesitamos girar)
    dx, dy = 1, 0
    
    # Para cada lado restante, calcular el siguiente vértice
    for _ in range(2, n_lados):
        # Rotar la dirección actual según el ángulo exterior
        dx_nuevo = dx * np.cos(angulo_exterior) - dy * np.sin(angulo_exterior)
        dy_nuevo = dx * np.sin(angulo_exterior) + dy * np.cos(angulo_exterior)
        
        # Normalizar para asegurar que la longitud sea 1
        longitud = np.sqrt(dx_nuevo**2 + dy_nuevo**2)
        dx = dx_nuevo / longitud
        dy = dy_nuevo / longitud
        
        # Calcular el siguiente punto
        x_actual += dx
        y_actual += dy
        
        # Añadir el nuevo vértice
        vertices.append((x_actual, y_actual))
    
    return vertices

def generar_triangulacion_poligono(n_lados):
    """
    Genera un polígono regular de n lados y lo triangulariza conectando
    cada par de vértices adyacentes con el centro del polígono.
    
    Args:
        n_lados: Número de lados del polígono
        
    Returns:
        Una lista de listas, donde cada sublista contiene 3 tuplas con las coordenadas
        de los vértices de un triángulo
    """
    # Generar los vértices del polígono
    vertices = generar_poligono_regular(n_lados)
    
    # Calcular el centro como promedio de todos los vértices
    vertices_array = np.array(vertices)
    centro = tuple(np.mean(vertices_array, axis=0))
    
    # Crear los triángulos (vértice actual, vértice siguiente, centro)
    triangulos = []
    
    for i in range(n_lados):
        vertice_actual = vertices[i]
        vertice_siguiente = vertices[(i + 1) % n_lados]  # Volvemos al primero al final
        
        triangulo = [vertice_actual, vertice_siguiente, centro]
        triangulos.append(triangulo)
    
    return triangulos

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
def puntos_en_recta(punto_inicial, vector_director, diccionario_puntos, tolerancia=1e-10):
    """
    Encuentra puntos que caen sobre una recta definida por un punto inicial y un vector director.
    
    Args:
        punto_inicial (tuple): Punto inicial (x, y) de la recta.
        vector_director (tuple): Vector director (dx, dy) de la recta.
        diccionario_puntos (dict): Diccionario con formato {id: (x, y)}.
        tolerancia (float, opcional): Tolerancia para considerar si un punto está en la recta.
        
    Returns:
        list: Lista de IDs de puntos ordenados según su posición en la recta.
    """
    # Normalizar el vector director para cálculos más precisos
    magnitud = (vector_director[0]**2 + vector_director[1]**2)**0.5
    vector_normalizado = (vector_director[0]/magnitud, vector_director[1]/magnitud)
    
    # Lista para almacenar puntos en la recta con su parámetro t
    puntos_en_recta = []
    
    for punto_id, coordenadas in diccionario_puntos.items():
        # Vector desde el punto inicial al punto candidato
        vector_a_punto = (coordenadas[0] - punto_inicial[0], coordenadas[1] - punto_inicial[1])
        
        # Para que un punto esté en la recta, el vector desde el punto inicial al punto candidato
        # debe ser colineal con el vector director (proporcional)
        
        # Si vector_director = (a, b) y vector_a_punto = (c, d), entonces para ser colineales:
        # a*d - b*c = 0 (producto cruz igual a cero)
        producto_cruz = vector_director[0] * vector_a_punto[1] - vector_director[1] * vector_a_punto[0]
        
        if abs(producto_cruz) <= tolerancia:
            # Calcular el parámetro t del punto en la ecuación paramétrica de la recta
            # Punto = punto_inicial + t * vector_director
            
            # Para evitar división por cero, usamos la componente no nula del vector director
            if abs(vector_director[0]) > tolerancia:
                t = vector_a_punto[0] / vector_director[0]
            else:
                t = vector_a_punto[1] / vector_director[1]
            
            # Solo considerar puntos adelante en la dirección del vector (t >= 0)
            if t >= 0:
                puntos_en_recta.append((punto_id, t))
    
    # Ordenar los puntos por su parámetro t (distancia a lo largo de la recta)
    puntos_en_recta.sort(key=lambda x: x[1])
    
    # Devolver solo los IDs en el orden correcto
    return [punto_id for punto_id, _ in puntos_en_recta]

# Ejemplo de uso
if __name__ == "__main__":
    # Punto inicial y vector director
    punto_inicial = (1, 2)
    vector_director = (2, 3)
    
    # Diccionario de puntos
    puntos = {
        "A": (1, 2),     # Punto inicial
        "B": (3, 5),     # En la recta: punto_inicial + 1*vector_director
        "C": (5, 8),     # En la recta: punto_inicial + 2*vector_director
        "D": (7, 11),    # En la recta: punto_inicial + 3*vector_director
        "E": (4, 4),     # No está en la recta
        "F": (-1, -1),   # En la recta pero en dirección opuesta al vector (t < 0)
        "G": (0, 0.5),   # No está en la recta
    }
    
    # Encontrar puntos en la recta y su orden
    resultado = puntos_en_recta(punto_inicial, vector_director, puntos)
    print("Puntos en la recta (ordenados):", resultado)
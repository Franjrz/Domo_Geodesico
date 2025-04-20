import numpy as np

def generar_triangulo_base_alternado(frecuencia):
    """
    Genera los puntos de un triángulo equilátero con una frecuencia determinada.
    Los puntos se distribuyen de manera uniforme dentro del triángulo y se calculan
    las aristas entre puntos adyacentes.
    
    Args:
        frecuencia: La frecuencia de división del triángulo
        
    Returns:
        - Un diccionario de puntos donde la clave es str(i) + "_" + str(j) y el valor 
          son las coordenadas (x,y)
        - Una lista con los IDs de los vértices exteriores del triángulo completo
        - Un diccionario donde las claves son los ids de los puntos y los valores
          son listas con los ids de los puntos adyacentes
    """
    # Factores de escala
    factor_x = 1/(2*frecuencia)
    factor_y = factor_x * np.sqrt(3)
    
    # Inicializar el diccionario de puntos
    puntos = {}
    
    # Lista para almacenar los IDs de los vértices del triángulo completo
    vertices = ["0_0", "0_" + str(frecuencia), str(frecuencia) + "_0"]
    
    # Diccionario para almacenar las aristas
    aristas = {}
    
    # Generar todos los puntos
    for i in range(frecuencia + 1):
        for j in range(frecuencia + 1 - i):
            # Generar el ID del punto
            punto_id = str(i) + "_" + str(j)

            # Calcular coordenadas
            x = factor_x * (i + 2 * j)
            y = factor_y * i
            
            # Almacenar en el diccionario
            puntos[punto_id] = (x, y)

            # Generar y seleccionar aristas
            a_derecha = [str(i) + "_" + str(j+1)] * (i+j != frecuencia)
            a_arriba_derecha = [str(i+1) + "_" + str(j)] * (i+j != frecuencia)
            a_arriba_izquierda = [str(i+1) + "_" + str(j-1)] * (j != 0)
            a_izquierda = [str(i) + "_" + str(j-1)] * (j != 0)
            a_debajo_izquierda = [str(i-1) + "_" + str(j)] * (i != 0)
            a_debajo_derecha = [str(i-1) + "_" + str(j+1)] * (i != 0)
            
            # Inicializar la lista de aristas para este punto
            aristas[punto_id] = a_derecha + a_arriba_derecha + a_arriba_izquierda + \
                a_izquierda + a_debajo_izquierda + a_debajo_derecha
    
    return puntos, vertices, aristas
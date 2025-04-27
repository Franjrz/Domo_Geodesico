import numpy as np

from utils import *

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

def subdividir_triangulo_punto_medio(ids_triangulo, puntos, id_contador):
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
    id_punto_medio = str(id_contador)
    id_contador += 1
    
    # Añadir el nuevo punto al diccionario
    puntos[id_punto_medio] = punto_medio
    
    # Crear los 3 nuevos triángulos (usando IDs)
    triangulo1 = [ids_triangulo[0], ids_triangulo[1], id_punto_medio]
    triangulo2 = [ids_triangulo[1], ids_triangulo[2], id_punto_medio]
    triangulo3 = [ids_triangulo[2], ids_triangulo[0], id_punto_medio]
    
    return [triangulo1, triangulo2, triangulo3], puntos, id_contador, id_punto_medio

def generar_triangulo_base_punto_medio(frecuencia):
    """
    Realiza la triangulación de manera iterativa hasta un nivel máximo.
    
    Args:
        triangulo_inicial: Lista de 3 tuplas (x, y) que representan los vértices del triángulo inicial
        frecuencia: Número máximo de niveles de subdivisión
        
    Returns:
        Tupla con tres elementos:
        - puntos: Diccionario {id: (x, y)} con todas las coordenadas
        - vertices: Lista con los IDs de los 3 vértices principales originales
        - adyacencias: Diccionario {id: [id1, id2, ...]} con las conexiones entre puntos
    """
    # Generar triangulo inicial
    triangulo_inicial = [(0,0), (1,0), (0.5, np.sqrt(3)/2)]

    # Inicializar el diccionario de puntos con los vértices originales
    puntos = {"0": triangulo_inicial[0], "1": triangulo_inicial[1], "2": triangulo_inicial[2]}
    
    # Guardar los IDs de los vértices principales
    vertices = ["0", "1", "2"]
    
    # Inicializar con el triángulo inicial (usando IDs)
    triangulos_actuales = [["0", "1", "2"]]
    
    # Inicializar contador para nuevos IDs
    id_contador = 3
    
    # Inicializar diccionario de adyacencias
    adyacencias = {"0": ["1", "2"], "1": ["0", "2"], "2": ["0", "1"]}
    
    # Si no hay subdivisiones, devolver directamente
    if frecuencia == 1:
        return puntos, vertices, adyacencias
    
    # Procesar cada nivel
    for nivel in range(frecuencia-1):
        nuevos_triangulos = []
        
        # Subdividir cada triángulo del nivel actual
        for triangulo in triangulos_actuales:
            nuevos_triangs, puntos, id_contador, id_medio = subdividir_triangulo_punto_medio(triangulo, puntos, id_contador)
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

def generar_puntos_y_rectas_triangulo_triacon(frecuencia):
    """
    Genera los puntos de un triángulo equilátero con subdivisiones según la frecuencia
    y las rectas perpendiculares a cada lado que pasan por los puntos de subdivisión.
    
    Args:
        frecuencia: Determina el número de divisiones por lado (2^frecuencia)
    
    Returns:
        Tupla (vertices, puntos, rectas)
        - vertices: Lista de IDs de los vértices originales ["0", "1", "2"]
        - puntos: Diccionario {id: (x, y)} con las coordenadas de cada punto
          donde id para vértices es "0", "1", "2" y para puntos en lados es "lado_indice"
        - rectas: Diccionario {id: (punto, vector_direccion)} con las rectas perpendiculares
          asociadas a cada punto de subdivisión
    """
    # 1. Calcular las coordenadas del triángulo equilátero
    v1 = (0.0, 0.0)
    v2 = (1.0, 0.0)
    altura = np.sqrt(3) / 2
    v3 = (0.5, altura)
    
    vertices_coords = [v1, v2, v3]
    
    # 2. Inicializar estructuras de datos
    vertices = ["0", "1", "2"]
    puntos = {
        "0": v1,
        "1": v2,
        "2": v3
    }
    rectas = {}

    # Si la frecuencia es la mínima no calcular las rectas
    if frecuencia == 0:
        return vertices, puntos, rectas
    
    # 3. Calcular subdivisiones en cada lado según la frecuencia
    divisiones = 2 ** frecuencia
    
    for lado in range(3):
        inicio = vertices_coords[lado]
        fin = vertices_coords[(lado + 1) % 3]
        
        # Calcular el vector del lado
        vector_lado = (fin[0] - inicio[0], fin[1] - inicio[1])
        
        # Calcular el vector perpendicular (rotación de 90 grados)
        vector_perpendicular = (-vector_lado[1], vector_lado[0])
        
        # Normalizar el vector perpendicular
        norma = np.sqrt(vector_perpendicular[0]**2 + vector_perpendicular[1]**2)
        vector_perpendicular_norm = (vector_perpendicular[0] / norma, vector_perpendicular[1] / norma)
        
        for i in range(1, divisiones):
            t = i / divisiones
            x = inicio[0] + t * (fin[0] - inicio[0])
            y = inicio[1] + t * (fin[1] - inicio[1])
            
            # Formato del ID: "lado_indice"
            punto_id = f"{lado}_{i-1}"
            punto = (x, y)
            puntos[punto_id] = punto
            
            # Almacenar la recta perpendicular asociada al punto
            # La recta se representa como (punto, vector_direccion)
            rectas[punto_id] = (punto, vector_perpendicular_norm)
    
    return vertices, puntos, rectas

def calcular_intersecciones_triacon(vertices, puntos, rectas):
    """
    Calcula las intersecciones entre pares de rectas perpendiculares.
    Si la intersección está dentro del triángulo y no coincide con puntos existentes,
    la añade al diccionario de puntos.
    
    Args:
        vertices: Lista de IDs de los vértices originales
        puntos: Diccionario {id: (x, y)} con las coordenadas de cada punto
        rectas: Diccionario {id: (punto, vector_direccion)} con las rectas perpendiculares
    
    Returns:
        puntos: Diccionario actualizado con las intersecciones añadidas
    """
    # Obtener coordenadas de los vértices para el cálculo de "punto en triángulo"
    vertices_coords = [puntos[v] for v in vertices]
    
    # Función auxiliar para verificar si un punto está dentro del triángulo
    def punto_en_triangulo(punto):
        x, y = punto
        (x1, y1), (x2, y2), (x3, y3) = vertices_coords
        
        denominador = ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
        a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / denominador
        b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / denominador
        c = 1 - a - b
        
        # Si todas las coordenadas baricéntricas están entre 0 y 1, el punto está dentro
        epsilon = 1e-10  # Tolerancia para errores de punto flotante
        return (a >= -epsilon and a <= 1 + epsilon and 
                b >= -epsilon and b <= 1 + epsilon and 
                c >= -epsilon and c <= 1 + epsilon)
    
    # Función auxiliar para calcular la intersección entre dos rectas
    def calcular_interseccion(recta1, recta2):
        (p1x, p1y), (d1x, d1y) = recta1
        (p2x, p2y), (d2x, d2y) = recta2
        
        # Verificamos si las direcciones son paralelas
        det = d1x * d2y - d1y * d2x
        if abs(det) < 1e-10:
            return None  # Rectas paralelas o coincidentes
        
        # Calculamos los parámetros t1 y t2
        dx = p2x - p1x
        dy = p2y - p1y
        
        t1 = (dx * d2y - dy * d2x) / det
        
        # Calculamos el punto de intersección
        interseccion = (
            round(p1x + t1 * d1x, 10),  # Redondeamos a 10 decimales
            round(p1y + t1 * d1y, 10)
        )
        
        return interseccion
    
    # Función auxiliar para verificar si un punto es igual a otro con tolerancia
    def puntos_iguales(p1, p2, decimales=10):
        x1, y1 = p1
        x2, y2 = p2
        return (round(x1, decimales) == round(x2, decimales) and 
                round(y1, decimales) == round(y2, decimales))
    
    # Para cada par de rectas, calcular su intersección
    ids_rectas = list(rectas.keys())
    
    for i in range(len(ids_rectas)):
        for j in range(i + 1, len(ids_rectas)):
            id_recta1 = ids_rectas[i]
            id_recta2 = ids_rectas[j]
            
            recta1 = rectas[id_recta1]
            recta2 = rectas[id_recta2]
            
            # Calcular la intersección
            interseccion = calcular_interseccion(recta1, recta2)
            
            if interseccion is not None and punto_en_triangulo(interseccion):
                # Verificar que la intersección no coincide con puntos existentes
                es_punto_existente = False
                for coord in puntos.values():
                    if puntos_iguales(interseccion, coord):
                        es_punto_existente = True
                        break
                
                # Si no es un punto existente, lo añadimos al diccionario
                if not es_punto_existente:
                    nuevo_id = f"{id_recta1}_{id_recta2}"
                    puntos[nuevo_id] = interseccion
    
    return puntos

def puntos_en_recta_triacon(punto_inicial, vector_director, diccionario_puntos, tolerancia=1e-10):
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

def agregar_arista_si_no(aristas, id_pre, id_post):
    """
    Añade una arista unidireccional de id_pre a id_post en el diccionario de aristas.
    Si el nodo id_pre no existe en el diccionario, crea una nueva entrada.
    
    Args:
        aristas: Diccionario de aristas donde la clave es el ID del nodo origen
                y el valor es una lista de IDs de nodos destino
        id_pre: ID del nodo origen
        id_post: ID del nodo destino
        
    Returns:
        El diccionario de aristas actualizado
    """
    if id_pre not in aristas.keys():
        aristas[id_pre] = [id_post]
    else:
        aristas[id_pre].append(id_post)
    return aristas


def rellenar_aristas(aristas, id_pre, id_post):
    """
    Añade una arista bidireccional entre id_pre e id_post en el diccionario de aristas.
    Crea una conexión de id_pre a id_post y otra de id_post a id_pre.
    
    Args:
        aristas: Diccionario de aristas donde la clave es el ID del nodo
                y el valor es una lista de IDs de nodos conectados
        id_pre: ID del primer nodo
        id_post: ID del segundo nodo
        
    Returns:
        El diccionario de aristas actualizado con la conexión bidireccional
    """
    aristas = agregar_arista_si_no(aristas, id_pre, id_post)
    aristas = agregar_arista_si_no(aristas, id_post, id_pre)
    return aristas


def generar_triangulo_base_triacon(frecuencia):
    """
    Genera un triángulo base triacon con sus puntos, vértices y aristas.
    
    El proceso consiste en:
    1. Generar los puntos y rectas iniciales del triángulo
    2. Calcular todas las intersecciones entre las rectas
    3. Construir las aristas que conectan los puntos del triángulo
    
    Args:
        frecuencia: Determina la complejidad del triángulo (2^frecuencia divisiones por lado)
        
    Returns:
        tuple: (puntos, vertices, aristas)
            - puntos: Diccionario {id: (x, y)} con las coordenadas de cada punto
            - vertices: Lista con los IDs de los vértices del triángulo ["0", "1", "2"]
            - aristas: Diccionario {id: [id1, id2, ...]} con las conexiones entre puntos
    """
    frecuencia -= 1
    # Generar los puntos y rectas iniciales del triángulo
    vertices, puntos, rectas = generar_puntos_y_rectas_triangulo_triacon(frecuencia)

    if frecuencia == 0:
        aristas = {"0": ["1", "2"],
                   "1": ["0", "2"],
                   "2": ["0", "1"]}
        return puntos, vertices, aristas
    
    # Calcular las intersecciones entre rectas
    puntos = calcular_intersecciones_triacon(vertices, puntos, rectas)

    # Inicializar el diccionario de aristas
    aristas = {}
    
    # Crear aristas para cada lado del triángulo (0, 1, 2)
    for i in range(3):
        # Crear aristas a lo largo de las rectas perpendiculares
        for j in range(1, 2**frecuencia):
            # Obtener el ID del punto en el lado
            id_punto = f"{i}_{j-1}"
            # Obtener coordenadas y vector director de la recta perpendicular
            coord_punto, vec = rectas[id_punto]
            # Obtener puntos ordenados que están en esta recta
            ids_orden = puntos_en_recta_triacon(coord_punto, vec, puntos)
            # Crear aristas entre puntos consecutivos en la recta
            for k in range(len(ids_orden) - 1):
                aristas = rellenar_aristas(aristas, ids_orden[k], ids_orden[k+1])
        
        # Crear aristas entre puntos consecutivos en cada lado del triángulo
        for j in range(1, 2**frecuencia-1):
            id_punto = f"{i}_{j-1}"
            id_punto_siguiente = f"{i}_{j}"
            aristas = rellenar_aristas(aristas, id_punto, id_punto_siguiente)
        
        # Conectar los vértices del triángulo con los puntos adyacentes
        id_punto = str(i)  # Vértice actual
        id_punto_siguiente = f"{i}_0"  # Primer punto en este lado
        id_punto_anterior = f"{(i - 1) % 3}_{2**frecuencia-2}"  # Último punto del lado anterior
        
        # Conectar el vértice con puntos adyacentes
        if id_punto not in aristas.keys():      
            aristas[id_punto] = [id_punto_siguiente, id_punto_anterior]
        else:
            aristas[id_punto] += [id_punto_siguiente, id_punto_anterior]
        
        # Asegurar que el último punto del lado anterior esté conectado al vértice
        aristas = agregar_arista_si_no(aristas, id_punto_anterior, id_punto)
    
    return puntos, vertices, aristas
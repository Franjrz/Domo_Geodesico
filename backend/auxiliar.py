import numpy as np
import matplotlib.pyplot as plt
from graficos import *

def generar_puntos_y_rectas_triangulo(frecuencia):
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

def calcular_intersecciones(vertices, puntos, rectas):
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

def dibujar_triangulo_con_rectas_e_intersecciones(vertices, puntos, rectas, longitud_recta=0.5):
    """
    Dibuja el triángulo, todos los puntos, sus rectas perpendiculares asociadas y
    las intersecciones entre rectas.
    
    Args:
        vertices: Lista de IDs de los vértices originales
        puntos: Diccionario {id: (x, y)} con las coordenadas de cada punto
        rectas: Diccionario {id: (punto, vector_direccion)} con las rectas perpendiculares
        longitud_recta: Longitud de las rectas perpendiculares a dibujar
    """
    # Crear una nueva figura
    plt.figure(figsize=(10, 8))
    
    # Obtener las coordenadas de los vértices del triángulo
    vertices_coords = [puntos[v] for v in vertices]
    
    # Dibujar el triángulo (conectar los vértices)
    for i in range(3):
        x1, y1 = vertices_coords[i]
        x2, y2 = vertices_coords[(i+1) % 3]
        plt.plot([x1, x2], [y1, y2], 'b-', linewidth=2)
    
    # Dibujar todos los puntos
    for punto_id, coords in puntos.items():
        x, y = coords
        
        # Dibujar según el tipo de punto
        if punto_id in vertices:
            # Vértices originales
            plt.plot(x, y, 'ro', markersize=8)
            plt.text(x+0.02, y+0.02, punto_id, fontsize=12)
        elif "_" in punto_id and punto_id.count("_") > 1:
            # Puntos de intersección entre rectas (con formato id_recta1_id_recta2)
            plt.plot(x, y, 'mo', markersize=6)  # Color magenta para intersecciones
            plt.text(x+0.01, y+0.01, punto_id, fontsize=6)
        else:
            # Puntos de subdivisión en lados
            plt.plot(x, y, 'go', markersize=6)
            plt.text(x+0.01, y+0.01, punto_id, fontsize=8)
    
    # Dibujar las rectas perpendiculares
    for punto_id, recta in rectas.items():
        punto, vector = recta
        x, y = punto
        dx, dy = vector
        
        # Dibujar la recta (usamos un segmento con longitud especificada)
        # La recta pasa por el punto hacia ambos lados
        plt.arrow(x - dx * longitud_recta/2, y - dy * longitud_recta/2, 
                  dx * longitud_recta, dy * longitud_recta, 
                  head_width=0.02, head_length=0.03, fc='red', ec='red', 
                  length_includes_head=True)
    
    # Configurar el gráfico
    plt.grid(True)
    plt.axis('equal')
    plt.title(f'Triángulo equilátero con puntos, rectas perpendiculares e intersecciones')
    plt.xlabel('X')
    plt.ylabel('Y')
    
    # Ajustar los límites para mostrar todo el triángulo con un poco de margen
    plt.xlim(-0.2, 1.2)
    plt.ylim(-0.2, 1.0)
    
    plt.show()

# Ejemplo de uso
if __name__ == "__main__":
    frecuencia = 2  # Cambia este valor para ver diferentes niveles de subdivisión
    vertices, puntos, rectas = generar_puntos_y_rectas_triangulo(frecuencia)
    
    # Calcular las intersecciones entre rectas
    puntos = calcular_intersecciones(vertices, puntos, rectas)

    aristas = {}
    for i in range(3):
        for j in range(1, 2**frecuencia):
            id_punto = f"{i}_{j-1}"
            coord_punto, vec = rectas[id_punto]
            ids_orden = puntos_en_recta(coord_punto, vec, puntos)
            for k in range(len(ids_orden)-1):
                if ids_orden[k] not in aristas.keys():
                    aristas[ids_orden[k]] = [ids_orden[k+1]]
                else:
                    aristas[ids_orden[k]].append(ids_orden[k+1])
                if ids_orden[k+1] not in aristas.keys():
                    aristas[ids_orden[k+1]] = [ids_orden[k]]
                else:
                    aristas[ids_orden[k+1]].append(ids_orden[k])
        for j in range(1, 2**frecuencia-1):
            id_punto = f"{i}_{j-1}"
            id_punto_siguiente = f"{i}_{j}"
            print(id_punto, id_punto_siguiente)
            if id_punto not in aristas.keys():
                aristas[id_punto] = [id_punto_siguiente]
            else:
                aristas[id_punto].append(id_punto_siguiente)
            if id_punto_siguiente not in aristas.keys():
                aristas[id_punto_siguiente] = [id_punto]
            else:
                aristas[id_punto_siguiente].append(id_punto)
        print()
        id_punto = str(i)
        id_punto_siguiente = str(i) + "_0"
        id_punto_anterior = str((i - 1) % 3) + "_" + str(2**frecuencia-2)
        print(id_punto, id_punto_siguiente, id_punto_anterior)
        if id_punto not in aristas.keys():
            aristas[id_punto] = [id_punto_siguiente, id_punto_anterior]
        aristas[id_punto_siguiente].append(id_punto)
        aristas[id_punto_anterior] = [id_punto]
        
            
    
    print(f"Vértices: {vertices}")
    print(f"Total de puntos (incluyendo intersecciones): {len(puntos)}")
    
    print("\nPuntos originales y de subdivisión:")
    for punto_id, coords in puntos.items():
        if "_" not in punto_id or punto_id.count("_") == 1:  # Vértices y puntos de subdivisión
            print(f"{punto_id}: {coords}")
    
    print("\nPuntos de intersección:")
    for punto_id, coords in puntos.items():
        if "_" in punto_id and punto_id.count("_") > 1:  # Puntos de intersección
            print(f"{punto_id}: {coords}")
    
    print("\nPuntos de intersección:")
    for punto_id, coords in aristas.items():
        print(f"{punto_id}: {coords}")
    
    # Dibujar el triángulo con todos los puntos, rectas e intersecciones
    visualizar_cara_final(puntos, vertices, aristas)
    #dibujar_triangulo_con_rectas_e_intersecciones(vertices, puntos, rectas)
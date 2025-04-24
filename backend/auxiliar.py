from utils import *
from triangulos_base import *

def renombrar_puntos(puntos, cara):
    """
    Renombra las claves de un diccionario de puntos añadiendo el prefijo del número de cara.
    
    Args:
        puntos: Diccionario donde las claves son identificadores de puntos y los valores son sus coordenadas
        cara: Número que identifica la cara actual
        
    Returns:
        Diccionario con los identificadores renombrados con el formato "cara_id"
    """
    return {str(cara) + "_" + id : puntos[id] for id in puntos.keys()}

def renombrar_vertices(vertices, cara):
    """
    Renombra los identificadores de vértices añadiendo el prefijo del número de cara.
    
    Args:
        vertices: Lista de identificadores de vértices
        cara: Número que identifica la cara actual
        
    Returns:
        Lista de identificadores renombrados con el formato "cara_id"
    """
    return [str(cara) + "_" + id for id in vertices]

def renombrar_aristas(aristas, cara):
    """
    Renombra las claves y valores de un diccionario de aristas añadiendo el prefijo del número de cara.
    
    Args:
        aristas: Diccionario donde las claves son identificadores de puntos y los valores son listas
                de identificadores de puntos conectados (adyacencias)
        cara: Número que identifica la cara actual
        
    Returns:
        Diccionario de aristas con todos los identificadores renombrados con el formato "cara_id"
    """
    nuevas_aristas = {}

    for id in aristas.keys():
        nuevas_aristas[str(cara) + "_" + id] = [str(cara) + "_" + id for id in aristas[id]]

    return nuevas_aristas

generar_triangulo_base = [generar_triangulo_base_alternado, 
                          generar_triangulo_base_punto_medio,
                          generar_triangulo_base_triacon]

def obtener_fila_izquierda_alternado(frecuencia, lado):
    return [str(lado) + "_" + str(i) + "_" + str(frecuencia - i) for i in range(frecuencia)]

def obtener_fila_derecha_alternado(frecuencia, lado):
    return [str(lado) + "_" + str(i) + "_0" for i in range(frecuencia)]

def obtener_fila_izquierda_punto_medio(frecuencia, lado):
    return [str(lado) + "_1"]

def obtener_fila_derecha_punto_medio(frecuencia, lado):
    return [str(lado) + "_0"]

def obtener_fila_izquierda_triacon(frecuencia, lado):
    return [str(lado) + "_1"] + [str(lado) + "_1_" + str(i) for i in range(2**frecuencia-1)]

def obtener_fila_derecha_triacon(frecuencia, lado):
    return [str(lado) + "_0"] + [str(lado) + "_2_" + str(i) for i in range(2**frecuencia-2, -1, -1)]

generar_fila_derecha = [obtener_fila_derecha_alternado,
                        obtener_fila_derecha_punto_medio,
                        obtener_fila_derecha_triacon]

generar_fila_izquierda = [obtener_fila_izquierda_alternado,
                          obtener_fila_izquierda_punto_medio,
                          obtener_fila_izquierda_triacon]

def fusionar_par_puntos(puntos, vertices, aristas, id_derecha, id_izquierda):
    """    
    print("puntos: " + str(puntos))
    print("vertices: " + str(vertices))
    print("aristas: " + str(aristas))
    print("id_derecha: " + str(id_derecha))
    print("id_izquierda: " + str(id_izquierda))
    """
    aristas[id_derecha] += aristas[id_izquierda]
    aristas[id_derecha] = list(set(aristas[id_derecha]))

    # Conectar todas esas aristas al punto de la derecha
    for k in aristas[id_izquierda]:
        aristas[k].append(id_derecha)
        aristas[k] = list(set(aristas[k]))

    # Eliminar la conexión de las aristas al punto de la izquierda
    del aristas[id_izquierda]

    # Eliminar de los vértices del polígono al punto de la izquierda
    if id_izquierda in vertices:
        vertices.remove(id_izquierda)
    
    # Eliminar el punto central a eliminar
    del puntos[id_izquierda]
    
    # Eliminar cualquier posible conexión de un nodo al punto de la izquierda
    for k in aristas.keys():
        if id_izquierda in aristas[k]:
            aristas[k].remove(id_izquierda)
    
    return puntos, vertices, aristas

def fusionar_triangulos_base(frecuencia, lados, tipo):
    """
    Genera una estructura geométrica formada por la unión de múltiples triángulos base,
    organizados en un polígono de N lados.
    
    Args:
        frecuencia: Determina la densidad de puntos en cada triángulo base
        lados: Número de lados del polígono (número de triángulos base a fusionar)
        
    Returns:
        Tupla con tres elementos:
        - puntos: Diccionario de puntos con sus coordenadas
        - vertices: Lista de identificadores de los vértices principales
        - aristas: Diccionario que define las conexiones entre puntos
    """
    # Genera la triangulación del polígono de N lados
    subcaras_base = generar_triangulacion_poligono(lados)
    
    # Genera el triángulo base con la frecuencia indicada
    puntos_base, vertices_base, aristas_base = generar_triangulo_base[tipo](frecuencia)
    
    # Si solo se pide un triángulo, devuelve directamente el triángulo base
    if lados == 3:
        return puntos_base, vertices_base, aristas_base

    # Transformar y renombrar elementos por caras
    puntos = {}
    vertices = []
    aristas = {}
    for i in range(len(subcaras_base)):
        # Transformar los puntos del triángulo base según las coordenadas baricéntricas
        # de la subcara actual
        subpuntos_base = transformar_puntos_baricentricos(
            puntos_base, 
            [puntos_base[vb] for vb in vertices_base], 
            subcaras_base[i]
        )
        
        # Renombrar puntos, vértices y aristas con el prefijo de la cara actual
        subpuntos_base = renombrar_puntos(subpuntos_base, i)
        puntos = puntos | subpuntos_base
        subvertices_base = renombrar_vertices(vertices_base, i)
        vertices += subvertices_base
        subaristas_base = renombrar_aristas(aristas_base, i)
        aristas = aristas | subaristas_base

    # Conectar todos los puntos a un solo punto central
    tipos_id_punto_central = ["0_" + str(frecuencia) + "_0", "0_2", "0_2"]
    id_punto_central = tipos_id_punto_central[tipo]

    # Eliminar de los vértices del polígono al punto central
    vertices.remove(id_punto_central)
    for i in range(1, lados):

        # Traspasar todas las posibles aristas del siguiente punto al punto central
        tipos_id_siguiente_punto_central = [str(i) + "_" + str(frecuencia) + "_0", str(i) + "_2", str(i) + "_2"]
        sig_centro = tipos_id_siguiente_punto_central[tipo]
        puntos, vertices, aristas = fusionar_par_puntos(puntos, vertices, aristas, id_punto_central, sig_centro)

    # Coser las aristas de un triángulo y el siguiente
    for i in range(lados):
        # id cara actual
        id = i
        # id cara anterior (vuelve a la última asi la actual es la primera)
        id_anterior = (i - 1) % lados

        # Obtener las dos listas de ids a fusionar, la izquierda desaparece y la derecha le sustituye
        ids_nodos_izquierda = generar_fila_izquierda[tipo](frecuencia, id_anterior)
        ids_nodos_derecha = generar_fila_derecha[tipo](frecuencia, id)

        # Por cada unión entre triangulos
        for j in range(len(ids_nodos_derecha)):

            # Traspasar todas las posibles aristas del punto al punto equivalente de la derecha
            id_izquierda = ids_nodos_izquierda[j]
            id_derecha = ids_nodos_derecha[j]
            # j == len(ids_nodos_derecha)-1
            puntos, vertices, aristas = fusionar_par_puntos(puntos, vertices, aristas, id_derecha, id_izquierda)
    
    return puntos, vertices, aristas
import numpy as np

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

def fusionar_triangulos_base_alternado(frecuencia, lados):
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
    puntos_base, vertices_base, aristas_base = generar_triangulo_base_alternado(frecuencia)
    
    # Si solo se pide un triángulo, devuelve directamente el triángulo base
    if lados == 3:
        return puntos_base, vertices_base, aristas_base

    # Transformar y renombrar elementos por caras
    subcaras = []
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
        subvertices_base = renombrar_vertices(vertices_base, i)
        subaristas_base = renombrar_aristas(aristas_base, i)
        
        # Guardar la información de esta subcara
        subcaras.append({"p": subpuntos_base, "v": subvertices_base, "a": subaristas_base})
    
    # Fusionar límites entre caras adyacentes
    id_punto_central = "0_" + str(frecuencia) + "_0"
    coordenadas_punto_central = subcaras[0]["p"][id_punto_central]
    del_puntos = []  # Lista para almacenar puntos a eliminar (duplicados entre caras)
    
    # Recorrer todas las caras para establecer las "costuras" entre ellas
    for c in range(len(subcaras)):
        id = c
        id_siguiente = (c + 1) % lados  # Cara siguiente (vuelve a la primera al final)
        
        # Para cada nivel de la "costura"
        for i in range(frecuencia + 1):
            # Calcular identificadores de puntos clave para la costura
            id_del = str(id) + "_" + str(i) + "_" + str(frecuencia-i)  # Punto en el borde actual
            id_sus = str(id_siguiente) + "_" + str(i) + "_" + str(0)   # Punto correspondiente en la cara siguiente
            id_arriba = str(id) + "_" + str(i) + "_" + str(frecuencia-i-1)  # Punto adyacente superior
            id_debajo = str(id) + "_" + str(i-1) + "_" + str(frecuencia-i)  # Punto adyacente inferior
            
            # Evitar conectar el último punto con el primero en el caso especial
            if not(id_siguiente == 0 and i == frecuencia):
                # Crear conexiones por encima (excepto en el último nivel)
                if i != frecuencia:
                    subcaras[id]["a"][id_arriba].append(id_sus)
                    subcaras[id_siguiente]["a"][id_sus].append(id_arriba)
                
                # Crear conexiones por debajo (excepto en el primer nivel)
                if i != 0:
                    subcaras[id]["a"][id_debajo].append(id_sus)
                    subcaras[id_siguiente]["a"][id_sus].append(id_debajo)
            
            # Eliminar el punto duplicado del borde actual
            del subcaras[id]["p"][id_del]
            
            # Eliminar referencias al punto duplicado
            if id_del in subcaras[id]["v"]:
                subcaras[id]["v"].remove(id_del)
            
            del subcaras[id]["a"][id_del]
            for id_punto in subcaras[id]["a"].keys():
                if id_del in subcaras[id]["a"][id_punto]:
                    subcaras[id]["a"][id_punto].remove(id_del)
            
            del_puntos.append(id_del)
    
    # Eliminar todas las referencias a puntos duplicados en las aristas
    conjunto_a_eliminar = set(del_puntos)
    for c in range(len(subcaras)):
        for id_punto in subcaras[c]["a"].keys():
            subcaras[c]["a"][id_punto] = [elemento for elemento in subcaras[c]["a"][id_punto] 
                                         if elemento not in conjunto_a_eliminar]
    
    # Añadir el punto central (común a todas las caras)
    subcaras[0]["p"][id_punto_central] = coordenadas_punto_central
    
    # Crear el anillo de puntos conectados al punto central
    anillo_central = [str(c) + "_" + str(frecuencia-1) + "_0" for c in range(len(subcaras))]
    subcaras[0]["a"][id_punto_central] = anillo_central
    
    # Conectar cada punto del anillo con el punto central
    for c in range(len(subcaras)):
        subcaras[c]["a"][str(c) + "_" + str(frecuencia-1) + "_0"].append(id_punto_central)
    
    # Fusionar todos los elementos de las caras en una única estructura
    puntos = {}
    vertices = []
    aristas = {}
    
    for c in range(len(subcaras)):
        # Añadir puntos
        for punto_cara in subcaras[c]["p"].keys():
            puntos[punto_cara] = subcaras[c]["p"][punto_cara]
        
        # Añadir vértices
        vertices += subcaras[c]["v"]
        
        # Añadir aristas
        for punto_cara in subcaras[c]["a"].keys():
            aristas[punto_cara] = subcaras[c]["a"][punto_cara]
    
    return puntos, vertices, aristas

def fusionar_triangulos_base_punto_medio(frecuencia, lados):
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
    puntos_base, vertices_base, aristas_base = generar_triangulo_base_punto_medio(frecuencia)
    
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
    id_punto_central = "0_2"
    vertices.remove(id_punto_central)
    for i in range(1, lados):
        sig_centro = str(i) + "_2"
        aristas[id_punto_central] += aristas[sig_centro]

        for j in aristas[sig_centro]:
            aristas[j].append(id_punto_central)

        del aristas[sig_centro]
        vertices.remove(sig_centro)
        del puntos[sig_centro]

        for j in aristas.keys():
            if sig_centro in aristas[j]:
                aristas[j].remove(sig_centro)

    for i in range(lados):
        id = i
        id_anterior = (i - 1) % lados  # Cara anterior (vuelve a la primera al final)

        anterior_derecha = str(id_anterior) + "_1"
        actual_izquierda = str(id) + "_0"
        conexiones_anterior_derecha = aristas[anterior_derecha]
        conexiones_anterior_derecha.remove("0_2")
        aristas[actual_izquierda] += conexiones_anterior_derecha

        for j in conexiones_anterior_derecha:
            aristas[j].append(actual_izquierda)
            aristas[j].remove(anterior_derecha)

        del aristas[anterior_derecha]
        vertices.remove(anterior_derecha)
        del puntos[anterior_derecha]
        aristas[id_punto_central].remove(anterior_derecha)

    
    return puntos, vertices, aristas
def generar_info_aristas(caras):
    """
    Genera información detallada sobre las aristas compartidas entre caras de un poliedro.
    
    Parámetros:
    - caras: lista de listas donde cada lista contiene los IDs de vértices de una cara en orden
    
    Retorna:
    - lista de listas, cada una con 4 elementos:
      [id_cara1 + "_" + id_local_v1, id_cara2 + "_" + id_local_v2, 
       id_cara1 + "_" + id_local_v1_next, id_cara2 + "_" + id_local_v2_next]
      donde:
      - id_cara1, id_cara2: IDs de las caras que comparten la arista
      - id_local_v1, id_local_v2: Posiciones locales del primer vértice en cada cara
      - id_local_v1_next, id_local_v2_next: Posiciones locales del segundo vértice en cada cara
    """
    # Diccionario para mapear pares de vértices a las caras que los contienen
    # Clave: tupla ordenada (v1, v2) de vértices que forman una arista
    # Valor: lista de tuplas (id_cara, id_local_v1, id_local_v2) que contienen esa arista
    arista_a_caras = {}
    
    # Recorrer todas las caras
    for id_cara, cara in enumerate(caras):
        n_vertices = len(cara)
        
        # Recorrer todas las aristas de la cara
        for i in range(n_vertices):
            # Guardar la información: (id_cara, posición local de v1, posición local de v2)
            pos_v1 = i
            pos_v2 = (i + 1) % n_vertices # El siguiente vértice (cíclico)

            v1 = cara[pos_v1]
            v2 = cara[pos_v2]  
            
            # Ordenar los vértices para asegurar consistencia en las claves del diccionario
            arista = tuple(sorted([v1, v2]))
            
            # Si v1 > v2, invertimos las posiciones locales porque ordenamos la arista
            if v1 > v2:
                pos_v1, pos_v2 = pos_v2, pos_v1
            
            if arista not in arista_a_caras:
                arista_a_caras[arista] = []
            
            arista_a_caras[arista].append((id_cara, pos_v1, pos_v2))
    
    # Generar la lista final de información de aristas
    resultado = []
    
    for arista, ocurrencias in arista_a_caras.items():
        # Solo considerar aristas que aparecen exactamente en 2 caras
        if len(ocurrencias) == 2:
            v1, v2 = arista
            (id_cara1, pos_v1_cara1, pos_v2_cara1) = ocurrencias[0]
            (id_cara2, pos_v1_cara2, pos_v2_cara2) = ocurrencias[1]
            
            # Verificar que las posiciones locales corresponden a los vértices correctos
            # Esto es necesario porque pueden haber cambiado debido al ordenamiento
            vertice1_cara1 = caras[id_cara1][pos_v1_cara1]
            vertice1_cara2 = caras[id_cara2][pos_v1_cara2]
            
            # Corregir las posiciones si no coinciden con v1
            if vertice1_cara1 != v1:
                pos_v1_cara1, pos_v2_cara1 = pos_v2_cara1, pos_v1_cara1
            
            if vertice1_cara2 != v1:
                pos_v1_cara2, pos_v2_cara2 = pos_v2_cara2, pos_v1_cara2
            
            # Crear entrada en el formato requerido
            info_arista = [
                f"{id_cara1}_{pos_v1_cara1}",
                f"{id_cara2}_{pos_v1_cara2}",
                f"{id_cara1}_{pos_v2_cara1}",
                f"{id_cara2}_{pos_v2_cara2}"
            ]
            resultado.append(info_arista)
    
    return resultado

# Ejemplo de uso
if __name__ == "__main__":
    caras_tetraedro = [
        [0, 1, 2],  # Cara 0
        [0, 2, 3],  # Cara 1
        [0, 3, 1],  # Cara 2
        [1, 3, 2]   # Cara 3
    ]

    info_aristas = generar_info_aristas(caras_tetraedro)

    print("Información de aristas compartidas en el tetraedro:")
    for i, arista in enumerate(info_aristas):
        print(f"Arista {i+1}: {arista}")
    """    
    # Ejemplo: caras de un cubo
    caras_cubo = [
        [0, 1, 3, 2],  # Cara 0
        [4, 6, 7, 5],  # Cara 1
        [0, 4, 5, 1],  # Cara 2
        [2, 3, 7, 6],  # Cara 3
        [0, 2, 6, 4],  # Cara 4
        [1, 5, 7, 3]   # Cara 5
    ]
    
    info_aristas = generar_info_aristas(caras_cubo)
    
    for i, arista in enumerate(info_aristas):
        print(f"Arista {i+1}: {arista}")
        """
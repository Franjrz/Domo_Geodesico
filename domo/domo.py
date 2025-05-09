
from scipy.spatial import Delaunay
from matplotlib.patches import Polygon

from domo.poliedro import *
from domo.fusion_triangulos import *

class Domo():
    def __init__(self, semilla, frecuencia, tipo, radio):
        self.semilla = semilla
        self.tipo = tipo
        self.frecuencia = frecuencia
        self.radio = radio
        self.poliedro = Poliedro(semilla)
        self.puntos = {}
        self.vertices = []
        self.aristas = {}
        self.vertices_aristas = {}
        self.__generar_caras_trianguladas()
        self.__generar_info_aristas()
        self.__fusionar_caras()
        self.__proyectar_puntos_a_esfera()
        self.__encontrar_ciclos()
        del self.vertices
        del self.vertices_aristas
        del self.conexiones_aristas

    def actualizar_puntos_a_3d(self, puntos, vertices, vertices_3d):
        # Extraer las coordenadas 2D de los vértices
        coords_2d_vertices = np.array([puntos[v] for v in vertices])
        
        # Convertir las coordenadas 3D de los vértices a un array numpy
        coords_3d_vertices = np.array(vertices_3d)
        
        # Crear una triangulación Delaunay con los vértices 2D
        triangulacion = Delaunay(coords_2d_vertices)
        
        # Inicializar el diccionario de puntos actualizados
        puntos_actualizados = {}
        
        # Para cada punto en el diccionario original
        for id_punto, coord_2d in puntos.items():
            # Si el punto es un vértice, simplemente usar sus coordenadas 3D
            if id_punto in vertices:
                idx = vertices.index(id_punto)
                puntos_actualizados[id_punto] = tuple(coords_3d_vertices[idx])
            else:
                # Encontrar en qué triángulo se encuentra el punto
                coord_2d_array = np.array([coord_2d])
                simplex = triangulacion.find_simplex(coord_2d_array)[0]
                
                if simplex == -1:
                    # El punto está fuera de la triangulación, usar el triángulo más cercano
                    dist = np.sum((coords_2d_vertices - coord_2d)**2, axis=1)
                    indices = np.argsort(dist)[:3]  # Usar los 3 vértices más cercanos
                    
                    # Calcular las coordenadas baricéntricas para los vértices más cercanos
                    total_dist = np.sum(1.0 / dist[indices])
                    pesos = (1.0 / dist[indices]) / total_dist
                    
                    # Interpolar la coordenada 3D
                    coord_3d = np.zeros(3)
                    for i, idx in enumerate(indices):
                        coord_3d += pesos[i] * coords_3d_vertices[idx]
                    
                    puntos_actualizados[id_punto] = tuple(coord_3d)
                else:
                    # Obtener las coordenadas baricéntricas
                    b = triangulacion.transform[simplex, :2].dot(np.transpose(coord_2d_array - triangulacion.transform[simplex, 2]))
                    b = np.append(b, 1 - np.sum(b))
                    
                    # Obtener los vértices del triángulo
                    vertices_triangulo = triangulacion.simplices[simplex]
                    
                    # Interpolar la coordenada 3D usando las coordenadas baricéntricas
                    coord_3d = np.zeros(3)
                    for i, v_idx in enumerate(vertices_triangulo):
                        coord_3d += b[i] * coords_3d_vertices[v_idx]
                    
                    puntos_actualizados[id_punto] = tuple(coord_3d)
        
        return puntos_actualizados

    def __generar_caras_trianguladas(self):
        caras_trianguladas = {longitud_ciclo:fusionar_triangulos_base(self.frecuencia, longitud_ciclo, self.tipo) for longitud_ciclo in self.poliedro.longitud_ciclos}
        for i in range(len(self.poliedro.caras)):
            puntos_cara, vertices_cara, aristas_cara, vertices_aristas_cara = caras_trianguladas[len(self.poliedro.caras[i])]
            vertices_3d = [self.poliedro.vertices[j] for j in self.poliedro.caras[i]]
            puntos_cara = self.actualizar_puntos_a_3d(puntos_cara, vertices_cara, vertices_3d)
            puntos_cara = renombrar_puntos(puntos_cara, i)
            self.puntos = self.puntos | puntos_cara
            vertices_cara = renombrar_vertices(vertices_cara, i)
            self.vertices += vertices_cara
            aristas_cara = renombrar_aristas(aristas_cara, i)
            self.aristas = self.aristas | aristas_cara
            for j in vertices_aristas_cara.keys():
                self.vertices_aristas[(str(i) + "_" + str(j[0]), str(i) + "_" + str(j[1]))] = [str(i) + "_" + id for id in vertices_aristas_cara[j]]

    def __generar_info_aristas(self):
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
        for id_cara, cara in enumerate(self.poliedro.caras):
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
        self.conexiones_aristas = []
        
        for arista, ocurrencias in arista_a_caras.items():
            # Solo considerar aristas que aparecen exactamente en 2 caras
            if len(ocurrencias) == 2:
                v1, v2 = arista
                (id_cara1, pos_v1_cara1, pos_v2_cara1) = ocurrencias[0]
                (id_cara2, pos_v1_cara2, pos_v2_cara2) = ocurrencias[1]
                
                # Verificar que las posiciones locales corresponden a los vértices correctos
                # Esto es necesario porque pueden haber cambiado debido al ordenamiento
                vertice1_cara1 = self.poliedro.caras[id_cara1][pos_v1_cara1]
                vertice1_cara2 = self.poliedro.caras[id_cara2][pos_v1_cara2]
                
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
                self.conexiones_aristas.append(info_arista)

    def combinar_nodos(self, lista1, lista2):
        """
        Combina pares de nodos correspondientes entre dos listas, unificando sus conexiones.
        
        Parámetros:
        - lista1: lista de IDs de nodos (primera ruta)
        - lista2: lista de IDs de nodos (segunda ruta)
        - aristas: diccionario donde las claves son IDs de nodos y los valores son listas de IDs 
                de nodos adyacentes
        
        Efecto:
        - Añade todas las uniones del nodo de lista2 al nodo correspondiente de lista1
        - Elimina cualquier referencia a los nodos de lista2 de las listas de adyacencia
        - Modifica el diccionario aristas in-place
        
        Retorna:
        - Diccionario aristas actualizado
        """

        if len(lista1) != len(lista2):
            raise ValueError("Las listas deben tener el mismo número de elementos")
        
        # Iterar sobre los pares de nodos correspondientes
        for i in range(len(lista1)):
            nodo_destino = lista1[i]  # Nodo que mantendremos
            nodo_origen = lista2[i]   # Nodo que "fusionaremos" con el destino
            
            # 1. Añadir todas las conexiones del nodo_origen al nodo_destino
            # Excluir la autoconexión que se crearía si nodo_origen está conectado a nodo_destino
            for conexion in self.aristas[nodo_origen]:
                if conexion != nodo_destino and conexion not in self.aristas[nodo_destino]:
                    self.aristas[nodo_destino].append(conexion)
            
            # 2. Para cada nodo en el diccionario, reemplazar las referencias a nodo_origen por nodo_destino
            for nodo, conexiones in self.aristas.items():
                # Saltamos el nodo origen y destino para evitar autoconexiones
                if nodo == nodo_origen or nodo == nodo_destino:
                    continue
                    
                # Si el nodo está conectado al nodo_origen
                if nodo_origen != nodo_destino and nodo_origen in conexiones:
                    # Eliminar la conexión al nodo_origen
                    conexiones.remove(nodo_origen)
                    
                    # Añadir conexión al nodo_destino si no existe ya
                    if nodo_destino not in conexiones:
                        conexiones.append(nodo_destino)
            
            # 3. Eliminar el nodo_origen del diccionario (opcional, depende de tus requisitos)
            # Si quieres mantener el nodo pero sin conexiones, comenta esta línea
            # Si necesitas mantener este nodo por alguna razón, comenta esta línea
            if nodo_origen != nodo_destino and nodo_origen in self.aristas:
                del self.aristas[nodo_origen]
                del self.puntos[nodo_origen]

    def __fusionar_caras(self):
        for i in self.conexiones_aristas:
            extremos_lista_1 = (i[0], i[2])
            extremos_lista_2 = (i[1], i[3])
            if extremos_lista_1 in self.vertices_aristas:
                lista_1 = self.vertices_aristas[extremos_lista_1]
            else:
                lista_1 = self.vertices_aristas[(i[2], i[0])]
                lista_1.reverse()
            if extremos_lista_2 in self.vertices_aristas:
                lista_2 = self.vertices_aristas[extremos_lista_2]
            else:
                lista_2 = self.vertices_aristas[(i[3], i[1])]
                lista_2.reverse()

            id_viejo_1 = lista_2[0]
            id_viejo_2 = lista_2[-1]
            id_nuevo_1 = lista_1[0]
            id_nuevo_2 = lista_1[-1]

            self.combinar_nodos(lista_1, lista_2)

            for lista in self.vertices_aristas.values():
                if lista[0] == id_viejo_1:
                    lista[0] = id_nuevo_1
                if lista[-1] == id_viejo_1:
                    lista[-1] = id_nuevo_1
                if lista[0] == id_viejo_2:
                    lista[0] = id_nuevo_2
                if lista[-1] == id_viejo_2:
                    lista[-1] = id_nuevo_2

    def __proyectar_puntos_a_esfera(self):
        puntos_proyectados = {}
        for id_punto, coords in self.puntos.items():
            # Convertir las coordenadas a un array numpy
            punto = np.array(coords)
            
            # Calcular la distancia desde el origen al punto
            distancia = np.linalg.norm(punto)
            
            # Evitar división por cero
            if distancia < 1e-10:  # Si el punto está muy cerca del origen
                # Asignar una dirección aleatoria
                direccion = np.random.randn(3)
                direccion = direccion / np.linalg.norm(direccion)
                punto_proyectado = self.radio * direccion
            else:
                # Normalizar el vector (obtener el vector unitario en la dirección del punto)
                vector_unitario = punto / distancia
                
                # Escalar el vector unitario por el radio deseado
                punto_proyectado = self.radio * vector_unitario
            
            # Guardar el punto proyectado en el diccionario resultado
            puntos_proyectados[id_punto] = tuple(punto_proyectado)
        self.puntos = puntos_proyectados

    # Método privado para realizar una búsqueda en profundidad buscando ciclos de una longitud específica
    def __busqueda_en_profundidad(self, camino, inicio, profundidad):
        if profundidad == 0 and inicio == camino[-1]:
            # Si alcanza profundidad 0 y vuelve al inicio, se encontró un ciclo
            self.ciclos.append(camino[:-1])  # Guarda el ciclo encontrado
            return
        
        if profundidad < 0:
            return  # Fin de la rama de búsqueda

        # Explora los vecinos conectados al último nodo del camino
        for vecino in self.aristas[camino[-1]]:
            if vecino not in camino or (vecino == inicio and profundidad == 1):
                # Solo avanza si no ha visitado el vecino o si puede cerrar el ciclo
                self.__busqueda_en_profundidad(camino + [vecino], inicio, profundidad - 1)

    # Método privado para limpiar ciclos duplicados y no coplanarios
    def __limpiar_ciclos(self):
        ciclos_limpios = []
        for ciclo_1 in range(len(self.ciclos)):
            iguales = False
            for ciclo_2 in range(ciclo_1 + 1, len(self.ciclos)):
                # Compara si dos ciclos tienen los mismos vértices (sin importar el orden)
                if set(self.ciclos[ciclo_1]) == set(self.ciclos[ciclo_2]):
                    iguales = True
                    break
            if not iguales:
                ciclos_limpios.append(self.ciclos[ciclo_1])

        self.ciclos = ciclos_limpios  # Mantiene solo un ciclo único por conjunto de vértices

    # Método privado para encontrar todas las caras del poliedro
    def __encontrar_ciclos(self):
        # Inicializa el diccionario de caras separadas por su longitud
        self.caras = []

        # Para cada posible longitud de cara
        for nodo in self.aristas:
            self.ciclos = []
            # Busca ciclos partiendo de cada nodo
            self.__busqueda_en_profundidad([nodo], nodo, 3)
            # Limpia los ciclos encontrados
            self.__limpiar_ciclos()
            self.caras += self.ciclos

        del self.ciclos

    # Método para dibujar el poliedro
    def dibujar(self, ids = False, alpha_caras = 0.8):
        # Crear figura y ejes 3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Extraer coordenadas x, y, z de todos los vértices
        x = [self.puntos[v][0] for v in self.puntos]
        y = [self.puntos[v][1] for v in self.puntos]
        z = [self.puntos[v][2] for v in self.puntos]

        # Dibujar las aristas si se proporcionan
        if self.aristas:
            for vertice_id, conexiones in self.aristas.items():
                v1 = self.puntos[vertice_id]
                for vecino_id in conexiones:
                    if vertice_id < vecino_id:
                        v2 = self.puntos[vecino_id]
                        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]],
                                color='#2F5F8A', linestyle='-', linewidth=1)

        # Añadir etiquetas de identificadores si ids es True
        if ids:
            for idx, (xi, yi, zi) in enumerate(self.puntos):
                ax.text(xi, yi, zi, str(idx), color='black', fontsize=20, ha='left', va='bottom')
    
        # Dibujar caras
        poly3d = []
        for cara in self.caras:
            # Obtener coordenadas de vértices para esta cara
            vertices_cara = [self.puntos[id_v] for id_v in cara]
            poly3d.append(vertices_cara)
        
        # Crear colección de polígonos 3D y añadirla a los ejes
        cara_collection = Poly3DCollection(poly3d, 
                                        facecolors=["#0F52BA" for _ in range(len(self.caras))], 
                                        alpha=alpha_caras,
                                        edgecolor='black',
                                        linewidth=0.5)
        ax.add_collection3d(cara_collection)

        # Configurar aspecto del gráfico
        ax.set_box_aspect([1, 1, 1])
        titulo = self.semilla
        titulo = titulo.split()
        titulo = [palabra.capitalize() for palabra in titulo]
        ax.set_title(" ".join(titulo))
        ax.set_axis_off()

        # Establecer límites de ejes en un cubo para mejor visualización
        max_range = np.max([np.ptp(x), np.ptp(y), np.ptp(z)]) / 2.0
        mid_x = np.mean([np.max(x), np.min(x)])
        mid_y = np.mean([np.max(y), np.min(y)])
        mid_z = np.mean([np.max(z), np.min(z)])

        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)

        plt.tight_layout()
        plt.show()
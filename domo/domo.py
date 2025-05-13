
from scipy.spatial import Delaunay
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors

from domo.poliedro import *
from domo.fusion_triangulos import *

particion = ["alternado","punto_medio","triacon"]

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
        
        # print(lista1)
        # print(lista2)
        # print(self.aristas)
        
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

    def generar_rotaciones(self, n):
        """
        Calcula n rotaciones equidistantes (360°) alrededor del eje terrestre (inclinado 23.44°).

        Retorna:
        --------
        List[np.ndarray]
            Lista de arreglos Nx3 con los puntos rotados.
        """
        ids = list(self.puntos.keys())
        coords = np.array([self.puntos[i] for i in ids])

        inclinacion = np.radians(23.44)
        eje_tierra = np.array([np.sin(inclinacion), 0, np.cos(inclinacion)])

        def rot(theta):
            return matriz_rotacion_eje(eje_tierra, theta)

        angulos = np.linspace(0, 2*np.pi, n, endpoint=False)
        rotadas = [coords @ rot(a).T for a in angulos]

        return rotadas  # lista de arrays Nx3
    
    def calcular_colores_caras_rotadas(self, rotaciones, fuente_luz, color_base_rgb, min_intensidad=0.15, factor_distancia=0.45):
        """
        Calcula el color iluminado de cada cara en cada rotación del poliedro, 
        ajustando la intensidad por distancia a la fuente de luz.

        Parámetros:
        -----------
        rotaciones : list[np.ndarray]
            Lista de matrices Nx3 con coordenadas rotadas por frame.
        fuente_luz : np.ndarray
            Posición fija de la fuente de luz.
        color_base_rgb : np.ndarray or str
            Color base RGB normalizado (o string hexadecimal).
        min_intensidad : float
            Intensidad mínima.
        factor_distancia : float
            Ponderador para cuánto afecta la distancia al brillo.
        """
        if isinstance(color_base_rgb, str):
            color_base_rgb = np.array(mcolors.to_rgb(color_base_rgb))

        colores_por_rotacion = []
        puntos_ids = list(self.puntos.keys())
        id_to_index = {pid: i for i, pid in enumerate(puntos_ids)}

        for coords in rotaciones:
            intensidades = []
            distancias = []
            colores_cara = []

            for cara in self.caras:
                vertices = [coords[id_to_index[vid]] for vid in cara]

                # Normal e iluminación base (como tu versión original)
                v1, v2, v3 = np.array(vertices[0]), np.array(vertices[1]), np.array(vertices[2])
                normal = np.cross(v2 - v1, v3 - v1)
                normal = normal / np.linalg.norm(normal)

                centroide = np.mean([v1, v2, v3], axis=0)
                vector_luz = fuente_luz - centroide

                if np.dot(normal, vector_luz) < 0:
                    normal = -normal  # Inversión como hacías antes

                vector_luz = vector_luz / np.linalg.norm(vector_luz)
                intensidad_base = np.clip(np.dot(normal, vector_luz), min_intensidad, 1.0)

                # Calcular distancia
                distancia = np.linalg.norm(fuente_luz - centroide)

                intensidades.append(intensidad_base)
                distancias.append(distancia)

            # Normalizar distancias para ajustar brillo
            distancias = np.array(distancias)
            d_min, d_max = np.min(distancias), np.max(distancias)
            d_norm = (distancias - d_min) / (d_max - d_min + 1e-8)  # evitar división por cero

            # Aplicar corrección de intensidad por distancia
            for i in range(len(self.caras)):
                ajuste = 1.0 - factor_distancia * d_norm[i]
                intensidad_final = intensidades[i] * ajuste
                intensidad_final = np.clip(intensidad_final, min_intensidad, 1.0)

                color = intensidad_final * color_base_rgb
                colores_cara.append(color)

            colores_por_rotacion.append(colores_cara)

        return colores_por_rotacion

    def generar_video_rotacion(self, pasos=120, elevacion=30, ids=False, alpha_caras=0.8, nombre_salida = "poliedro.gif"):
        """
        Genera un video animado del domo geodésico rotando con sombreado dinámico.

        Parámetros:
        -----------
        pasos : int
            Número de frames de rotación.
        elevacion : float
            Ángulo de cámara vertical.
        ids : bool
            Mostrar etiquetas de los vértices.
        alpha_caras : float
            Transparencia de las caras.
        grados : float
            Grados totales de rotación sobre el eje terrestre.
        """
        # === Configuración general ===
        fig = plt.figure(figsize=(10, 8), facecolor='#1F1F1F')
        ax = fig.add_subplot(111, projection='3d')
        ax.set_facecolor('#1F1F1F')

        # === Datos iniciales para escalado ===
        coords = np.array(list(self.puntos.values()))
        x, y, z = coords[:, 0], coords[:, 1], coords[:, 2]

        max_range = np.max([np.ptp(x), np.ptp(y), np.ptp(z)]) / 2.0
        mid_x = np.mean([np.max(x), np.min(x)])
        mid_y = np.mean([np.max(y), np.min(y)])
        mid_z = np.mean([np.max(z), np.min(z)])

        # === Generar rotaciones e iluminación ===
        rotaciones = self.generar_rotaciones(pasos)
        fuente_luz = np.array([20, -30, 40])
        color_base = "#73C0E2"

        colores_por_frame = self.calcular_colores_caras_rotadas(
            rotaciones=rotaciones,
            fuente_luz=fuente_luz,
            color_base_rgb=color_base
        )

        puntos_ids = list(self.puntos.keys())

        def dibujar_escena(frame):
            ax.clear()
            ax.set_box_aspect([1, 1, 1])
            ax.set_xlim(mid_x - max_range, mid_x + max_range)
            ax.set_ylim(mid_y - max_range, mid_y + max_range)
            ax.set_zlim(mid_z - max_range, mid_z + max_range)
            ax.axis('off')

            # === Título ===
            semilla = " ".join(p.capitalize() for p in self.semilla.split())
            particion_str = " ".join(particion[self.tipo].split("_"))
            titulo = f"{semilla}\nPartición {particion_str}\nFrecuencia {self.frecuencia}"
            ax.set_title(titulo, color="#F1F1F1")

            # === Puntos rotados ===
            puntos_rotados = rotaciones[frame]
            id_to_coord = {pid: puntos_rotados[i] for i, pid in enumerate(puntos_ids)}

            # === Aristas ===
            for v1_id, vecinos in self.aristas.items():
                v1 = id_to_coord[v1_id]
                for v2_id in vecinos:
                    if v1_id < v2_id:
                        v2 = id_to_coord[v2_id]
                        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]],
                                color='#3E6576', linestyle='-', linewidth=1)

            # === Caras ===
            poly3d = []
            for cara in self.caras:
                vertices = [id_to_coord[vid] for vid in cara]
                poly3d.append(vertices)

            coleccion = Poly3DCollection(
                poly3d,
                facecolors=colores_por_frame[frame],
                alpha=alpha_caras,
                edgecolor='#3E6576',
                linewidth=0.5
            )
            ax.add_collection3d(coleccion)

            # === IDs opcionales ===
            if ids:
                delta = max_range * 0.02
                for vid, (xi, yi, zi) in id_to_coord.items():
                    ax.text(xi, yi, zi + delta, str(vid), color='#F1F1F1', fontsize=9,
                            ha='left', va='bottom')

            ax.view_init(elev=elevacion, azim=0)  # cámara fija

        # === Animación ===
        anim = FuncAnimation(fig, dibujar_escena, frames=pasos, interval=100)

        try:
            if nombre_salida.endswith(".mp4"):
                writer = FFMpegWriter(fps=30)
            elif nombre_salida.endswith(".gif"):
                writer = PillowWriter(fps=15)
            else:
                raise ValueError("El archivo debe terminar en .mp4 o .gif")

            anim.save(nombre_salida, writer=writer)
            print(f"✅ Video guardado como {nombre_salida}")
        except FileNotFoundError:
            print("❌ No se encontró ffmpeg o pillow. ¿Instalaste FFMPEG o PIL?")
        finally:
            plt.close(fig)

def matriz_rotacion_eje(v, theta):
    """
    Retorna la matriz de rotación 3x3 para rotar un ángulo theta (rad)
    alrededor del eje unitario v (np.array de 3 elementos).
    """
    v = v / np.linalg.norm(v)
    x, y, z = v
    c, s = np.cos(theta), np.sin(theta)
    C = 1 - c
    return np.array([
        [c + x*x*C,     x*y*C - z*s, x*z*C + y*s],
        [y*x*C + z*s, c + y*y*C,     y*z*C - x*s],
        [z*x*C - y*s, z*y*C + x*s, c + z*z*C    ]
    ])
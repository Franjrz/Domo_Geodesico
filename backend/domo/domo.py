
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
        self.__generar_caras_trianguladas()
        self.__generar_info_aristas()
        # Fusionar caras poliedro TERMINAR
        self.__proyectar_puntos_a_esfera()

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
            puntos_cara, vertices_cara, aristas_cara = caras_trianguladas[len(self.poliedro.caras[i])]
            #self.__dibujar_cara_triangulada(puntos_cara, vertices_cara, aristas_cara)
            vertices_3d = [self.poliedro.vertices[j] for j in self.poliedro.caras[i]]
            puntos_cara = self.actualizar_puntos_a_3d(puntos_cara, vertices_cara, vertices_3d)
            puntos_cara = renombrar_puntos(puntos_cara, i)
            self.puntos = self.puntos | puntos_cara
            vertices_cara = renombrar_vertices(vertices_cara, i)
            self.vertices += vertices_cara
            aristas_cara = renombrar_aristas(aristas_cara, i)
            self.aristas = self.aristas | aristas_cara
            #self.dibujar()

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

    def dibujar(self):
        """
        Dibuja un poliedro 3D a partir de sus vértices y aristas.
        
        Parámetros:
        -----------
        puntos : dict
            Diccionario con formato {id_punto: [x, y, z]} donde id_punto es un identificador
            y [x, y, z] son las coordenadas 3D del vértice.
        
        aristas : dict
            Diccionario con formato {id_punto: [id_punto1, id_punto2, ...]} donde cada id_punto
            está conectado con los puntos en la lista.
        
        titulo : str, opcional
            Título para la visualización.
        """
        # Crear figura y ejes 3D
        #fig = plt.figure(figsize=(10, 8), facecolor="black")
        fig = plt.figure(figsize=(20, 20))
        ax = fig.add_subplot(111, projection='3d')
        
        # Extraer coordenadas de todos los puntos
        xs = [punto[0] for punto in self.puntos.values()]
        ys = [punto[1] for punto in self.puntos.values()]
        zs = [punto[2] for punto in self.puntos.values()]
        
        # Encontrar límites para hacer la visualización equilibrada
        x_min, x_max = min(xs), max(xs)
        y_min, y_max = min(ys), max(ys)
        z_min, z_max = min(zs), max(zs)
        
        # Establecer límites del gráfico para mantener proporciones
        max_range = max(x_max - x_min, y_max - y_min, z_max - z_min)
        mid_x = (x_max + x_min) / 2
        mid_y = (y_max + y_min) / 2
        mid_z = (z_max + z_min) / 2
        
        ax.set_xlim(mid_x - max_range, mid_x + max_range)
        ax.set_ylim(mid_y - max_range, mid_y + max_range)
        ax.set_zlim(mid_z - max_range, mid_z + max_range)
        
        # Configurar para que todos los ejes tengan la misma escala
        ax.set_box_aspect([1, 1, 1])
        
        # Dibujar puntos
        ax.scatter(xs, ys, zs, c='#4682B4', marker='o', s=60)
        
        # Dibujar aristas
        for punto_id, conexiones in self.aristas.items():
            p1 = self.puntos[punto_id]
            for punto_conectado in conexiones:
                # Solo dibujar cada arista una vez
                if punto_id < punto_conectado or punto_conectado not in self.aristas or punto_id not in self.aristas[punto_conectado]:
                    p2 = self.puntos[punto_conectado]
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color='#A0C8E0', linewidth=2)
        
        # Configurar ejes y título
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        #ax.set_title(titulo)
        ax.set_axis_off()
        
        # Configurar vistas iniciales
        ax.view_init(30, 45)  # Elevación, Azimut
        
        # Añadir texto instructivo
        fig.text(0.5, 0.02, 'Haz clic y arrastra para rotar la figura', ha='center')
        
        plt.tight_layout()
        plt.show()

    def __dibujar_cara_triangulada(self, puntos, vertices, aristas, mostrar_ids=False):
        """
        Visualiza el triángulo con sus puntos y aristas, opcionalmente mostrando los IDs.
        
        Args:
            puntos: Diccionario donde la clave es el id del punto y el valor son las coordenadas (x,y)
            vertices: Lista con los ids de los vértices exteriores del triángulo
            aristas: Diccionario donde las claves son los ids de los puntos y los valores son listas con los ids adyacentes
            mostrar_ids: Booleano que indica si se deben mostrar los IDs de los puntos (default: False)
        """
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Extraer coordenadas de los vértices exteriores
        coords_vertices = [puntos[v] for v in vertices]
        
        # Dibujar el polígono en azul claro
        poligono = Polygon(np.array(coords_vertices), alpha=0.3, color='#D0E4F5', zorder=1)  # Azul muy claro
        ax.add_patch(poligono)
        
        # Dibujar las aristas - color intermedio entre polígono y puntos normales
        color_aristas = '#A0C8E0'  # Azul claro para aristas
        
        # Dibujar cada arista una sola vez (para evitar duplicados)
        aristas_dibujadas = set()
        for id_punto, adyacentes in aristas.items():
            for id_adyacente in adyacentes:
                # Crear un identificador único para la arista (ordenado para evitar duplicados)
                arista_id = tuple(sorted([id_punto, id_adyacente]))
                
                if arista_id not in aristas_dibujadas:
                    aristas_dibujadas.add(arista_id)
                    
                    # Extraer coordenadas de los extremos de la arista
                    p1 = puntos[id_punto]
                    p2 = puntos[id_adyacente]
                    
                    # Dibujar la arista
                    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color_aristas, linestyle='-', linewidth=0.8, zorder=2)
        
        # Dibujar los puntos interiores (no vértices) en azul intermedio
        color_puntos_internos = '#4682B4'  # Azul intermedio (Steel Blue)
        
        # Obtener los ids de los puntos interiores (todos los que no son vértices)
        puntos_interiores = [p_id for p_id in puntos.keys() if p_id not in vertices]
        
        # Dibujar los puntos interiores
        for p_id in puntos_interiores:
            p = puntos[p_id]
            ax.scatter(p[0], p[1], color=color_puntos_internos, s=40, zorder=4)
            
            # Añadir el ID del punto arriba a la derecha si mostrar_ids es True
            if mostrar_ids:
                ax.text(p[0] + 0.01, p[1] + 0.01, p_id, fontsize=8, color='black', 
                        ha='left', va='bottom', zorder=6, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
        
        # Dibujar los vértices exteriores en azul oscuro
        color_vertices = '#00008B'  # Azul oscuro (Dark Blue)
        for v_id in vertices:
            v = puntos[v_id]
            ax.scatter(v[0], v[1], color=color_vertices, s=60, zorder=5)
            
            # Añadir el ID del vértice si mostrar_ids es True
            if mostrar_ids:
                ax.text(v[0] + 0.01, v[1] + 0.01, v_id, fontsize=10, fontweight='bold', color='black', 
                        ha='left', va='bottom', zorder=6, bbox=dict(facecolor='white', alpha=0.7, edgecolor='none', pad=1))
        
        # Configurar el gráfico
        ax.set_aspect('equal')
        ax.grid(True, linestyle='--', alpha=0.7)
        
        # Establecer los límites con un poco de margen
        all_x = [p[0] for p in puntos.values()]
        all_y = [p[1] for p in puntos.values()]
        
        # Ajustar los márgenes según si se muestran IDs o no
        if mostrar_ids:
            max_x = max(all_x) + 0.1  # Margen mayor para acomodar los IDs
            max_y = max(all_y) + 0.1
        else:
            max_x = max(all_x) + 0.05
            max_y = max(all_y) + 0.05
        
        min_x = min(all_x) - 0.05
        min_y = min(all_y) - 0.05
        
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        
        # Ajustar el título según si se muestran IDs o no
        if mostrar_ids:
            ax.set_title('Triangulación de la cara con IDs')
        else:
            ax.set_title('Triangulación de la cara')
        
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        
        plt.tight_layout()
        plt.show()

    """
def combinar_nodos(lista1, lista2, aristas):
    """
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
    """
    if len(lista1) != len(lista2):
        raise ValueError("Las listas deben tener el mismo número de elementos")
    
    # Iterar sobre los pares de nodos correspondientes
    for i in range(len(lista1)):
        nodo_destino = lista1[i]  # Nodo que mantendremos
        nodo_origen = lista2[i]   # Nodo que "fusionaremos" con el destino
        
        # Si alguno de los nodos no está en el diccionario, continuar al siguiente par
        if nodo_destino not in aristas or nodo_origen not in aristas:
            continue
        
        # 1. Añadir todas las conexiones del nodo_origen al nodo_destino
        # Excluir la autoconexión que se crearía si nodo_origen está conectado a nodo_destino
        for conexion in aristas[nodo_origen]:
            if conexion != nodo_destino and conexion not in aristas[nodo_destino]:
                aristas[nodo_destino].append(conexion)
        
        # 2. Para cada nodo en el diccionario, reemplazar las referencias a nodo_origen por nodo_destino
        for nodo, conexiones in aristas.items():
            # Saltamos el nodo origen y destino para evitar autoconexiones
            if nodo == nodo_origen or nodo == nodo_destino:
                continue
                
            # Si el nodo está conectado al nodo_origen
            if nodo_origen in conexiones:
                # Eliminar la conexión al nodo_origen
                conexiones.remove(nodo_origen)
                
                # Añadir conexión al nodo_destino si no existe ya
                if nodo_destino not in conexiones:
                    conexiones.append(nodo_destino)
        
        # 3. Eliminar el nodo_origen del diccionario (opcional, depende de tus requisitos)
        # Si quieres mantener el nodo pero sin conexiones, comenta esta línea
        # Si necesitas mantener este nodo por alguna razón, comenta esta línea
        if nodo_origen in aristas:
            del aristas[nodo_origen]
    
    return aristas
    """
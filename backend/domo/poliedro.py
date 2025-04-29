import numpy as np
from scipy.spatial import distance
from skspatial.objects import Points
import matplotlib.pyplot as plt

from domo.generacion_vertices_poliedro import *

# Definición de la clase Poliedro
class Poliedro():
    
    # Constructor: inicializa el poliedro con una semilla y un radio
    def __init__(self, semilla, radio):
        self.semilla = semilla  # Nombre o tipo del poliedro (ej: "cubo romo")
        self.radio = radio      # Radio del poliedro (aunque en este código no se usa todavía)
        self.vertices = generar_vertices(semilla)  # Genera los vértices basados en la semilla
        self.__encontrar_aristas()  # Encuentra las aristas conectando vértices cercanos
        self.tolerancia = 1e-5  # Tolerancia para considerar coplanaridad
        self.longitud_ciclos = forma_caras[semilla]  # Tamaños esperados de las caras (ej: 3, 4, 5 lados)
        self.__encontrar_ciclos()  # Encuentra todas las caras posibles

    # Método privado para encontrar las aristas del poliedro
    def __encontrar_aristas(self):
        """
        Calcula un grafo de conexiones entre los vértices basado en la distancia mínima.
        """
        n = len(self.vertices)  # Número de vértices
        dist_matrix = np.zeros((n, n))  # Inicializa matriz de distancias

        # Calcula las distancias euclidianas entre todos los pares de vértices
        for i in range(n):
            for j in range(i+1, n):
                dist = distance.euclidean(self.vertices[i], self.vertices[j])
                dist_matrix[i][j] = dist
                dist_matrix[j][i] = dist
        
        # Encuentra la distancia mínima no nula (la distancia entre vértices adyacentes)
        min_dist = np.min(dist_matrix[dist_matrix > 0])
        
        # Crea el grafo: conecta vértices si están a distancia cercana al mínimo
        self.aristas = {}
        for i in range(n):
            conectados = [j for j in range(n) if i != j and dist_matrix[i][j] <= min_dist * 1.1]
            self.aristas[i] = conectados

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

        # Filtra también los ciclos que no sean coplanarios
        ciclos_limpios = []
        for ciclo in self.ciclos:
            puntos = Points(np.array([self.vertices[pid] for pid in ciclo]))
            if puntos.are_coplanar(tol=self.tolerancia):
                ciclos_limpios.append(ciclo)
        self.ciclos = ciclos_limpios

    # Método privado para insertar los nuevos ciclos encontrados en la lista de caras
    def __insertar_ciclos(self, profundidad):
        # Usa conjuntos para evitar duplicar caras
        conjuntos_destino = [set(lista) for lista in self.caras[profundidad]]
        
        for lista_nueva in self.ciclos:
            conjunto_nuevo = set(lista_nueva)
            if not any(conjunto_nuevo == conjunto_existente for conjunto_existente in conjuntos_destino):
                self.caras[profundidad].append(lista_nueva)
                conjuntos_destino.append(conjunto_nuevo)

    # Método privado para encontrar todas las caras del poliedro
    def __encontrar_ciclos(self):
        # Inicializa el diccionario de caras separadas por su longitud
        self.caras = {l: [] for l in self.longitud_ciclos}

        # Para cada posible longitud de cara
        for i in self.longitud_ciclos:
            for nodo in self.aristas:
                self.ciclos = []
                # Busca ciclos partiendo de cada nodo
                self.__busqueda_en_profundidad([nodo], nodo, i)
                # Limpia los ciclos encontrados
                self.__limpiar_ciclos()
                # Inserta los ciclos válidos
                self.__insertar_ciclos(i)

        # Junta todas las caras en una sola lista
        caras = []
        for i in self.longitud_ciclos:
            caras += self.caras[i]
        self.caras = caras

    # Método para dibujar el poliedro
    def dibujar(self, ids = False):
        # Crear figura y ejes 3D
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')

        # Extraer coordenadas x, y, z de todos los vértices
        x = [v[0] for v in self.vertices]
        y = [v[1] for v in self.vertices]
        z = [v[2] for v in self.vertices]

        # Dibujar los vértices
        s = 50 if self.aristas else 100
        ax.scatter(x, y, z, color='#00008B', s=s, label='Vértices')

        # Dibujar las aristas si se proporcionan
        if self.aristas:
            for vertice_id, conexiones in self.aristas.items():
                v1 = self.vertices[vertice_id]
                for vecino_id in conexiones:
                    if vertice_id < vecino_id:
                        v2 = self.vertices[vecino_id]
                        ax.plot([v1[0], v2[0]], [v1[1], v2[1]], [v1[2], v2[2]],
                                color='#A0C8E0', linestyle='-', linewidth=1)

        # Añadir etiquetas de identificadores si ids es True
        if ids:
            for idx, (xi, yi, zi) in enumerate(self.vertices):
                ax.text(xi, yi, zi, str(idx), color='black', fontsize=20, ha='left', va='bottom')

        # Configurar aspecto del gráfico
        ax.set_box_aspect([1, 1, 1])
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_title(self.semilla)

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
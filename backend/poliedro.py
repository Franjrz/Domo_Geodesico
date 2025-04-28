import numpy as np
from scipy.spatial import distance
from skspatial.objects import Points

from generacion_vertices_poliedro import *
from graficos import *

class Poliedro():
    def __init__(self, semilla):
        self.semilla = semilla
        self.vertices = generar_vertices(semilla)
        #Falla con ids 14, 15 (romos) y 17
        self.__encontrar_aristas()
        self.tolerancia = 1e-5
        self.longitud_ciclos = forma_caras[semilla]
        self.__encontrar_ciclos()

    def __encontrar_aristas(self):
        """
        Crea un grafo de conexiones entre vértices de un poliedro basado en distancias.
        
        Parámetros:
        - vertices: lista de tuplas (x, y, z) con las coordenadas 3D de los vértices
        
        Retorna:
        - Un diccionario donde las claves son los IDs de los vértices (0, 1, 2, ...) y
        los valores son listas con los IDs de los vértices conectados a cada uno
        """
        n = len(self.vertices)
        # Calcular matriz de distancias entre todos los pares de vértices
        dist_matrix = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                dist = distance.euclidean(self.vertices[i], self.vertices[j])
                dist_matrix[i][j] = dist
                dist_matrix[j][i] = dist
        
        min_dist = np.min(dist_matrix[dist_matrix > 0])
        
        # Crear el grafo como diccionario
        self.aristas = {}
        for i in range(n):
            # Encontrar todos los vértices conectados al vértice i
            conectados = [j for j in range(n) if i != j and dist_matrix[i][j] <= min_dist * 1.1]
            self.aristas[i] = conectados

    def __busqueda_en_profundidad(self, camino, inicio, profundidad):
        if profundidad == 0 and inicio == camino[-1]:
            self.ciclos.append(camino[:-1])
            return
        
        if profundidad < 0:
            return

        for vecino in self.aristas[camino[-1]]:
            if vecino not in camino or (vecino == inicio and profundidad ==1):
                self.__busqueda_en_profundidad(camino + [vecino], inicio, profundidad - 1)

    def __limpiar_ciclos(self):
        ciclos_limpios = []
        for ciclo_1 in range(len(self.ciclos)):
            iguales = False
            for ciclo_2 in range(ciclo_1 + 1, len(self.ciclos)):
                if set(self.ciclos[ciclo_1]) == set(self.ciclos[ciclo_2]):
                    iguales = True
                    break
            if iguales == False:
                ciclos_limpios.append(self.ciclos[ciclo_1])
        self.ciclos = ciclos_limpios
        ciclos_limpios = []
        for ciclo in self.ciclos:
            puntos = Points(np.array([self.vertices[pid] for pid in ciclo]))
            if puntos.are_coplanar(tol=self.tolerancia):
                ciclos_limpios.append(ciclo)
        self.ciclos = ciclos_limpios

    def __insertar_ciclos(self, profundidad):
        # Convertimos las listas existentes a conjuntos para facilitar comparación
        conjuntos_destino = [set(lista) for lista in self.caras[profundidad]]
        
        for lista_nueva in self.ciclos:
            # Convertimos la lista nueva a conjunto para comparación
            conjunto_nuevo = set(lista_nueva)
            
            # Verificamos si este conjunto ya existe en nuestros destinos
            if not any(conjunto_nuevo == conjunto_existente for conjunto_existente in conjuntos_destino):
                # Si no existe, lo agregamos a ambas estructuras
                self.caras[profundidad].append(lista_nueva)
                conjuntos_destino.append(conjunto_nuevo)

    def __encontrar_ciclos(self):
        self.caras = {l:[] for l in self.longitud_ciclos}
        for i in self.longitud_ciclos:
            for nodo in self.aristas:
                self.ciclos = []
                self.__busqueda_en_profundidad([nodo], nodo, i)
                self.__limpiar_ciclos()
                self.__insertar_ciclos(i)

    def dibujar(self, ids):
        dibujar_poliedro(self.vertices, self.aristas, ids)


# Ejemplo de uso:
if __name__ == "__main__":
    # Probar de 0 a 13, 14, 15 y 17 tienen bugs
    poliedro = Poliedro(poliedro_id[17])
    print()
    print(poliedro.semilla)
    for longitud in poliedro.longitud_ciclos:
        print(str(len(poliedro.caras[longitud])) + " Caras con " + str(longitud) + " lados")
        for cara in poliedro.caras[longitud]:
            print("\t" + str(cara))
    poliedro.dibujar(True)
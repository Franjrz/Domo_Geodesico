
from scipy.spatial import Delaunay

from poliedro import *
from fusion_triangulos import *

class Domo():
    def __init__(self, semilla, frecuencia, tipo, radio):
        self.semilla = semilla
        self.tipo = tipo
        self.frecuencia = frecuencia
        self.radio = radio
        self.poliedro = Poliedro(semilla, radio)
        self.puntos = {}
        self.vertices = []
        self.aristas = {}
        self.__generar_caras_trianguladas()
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
        for i in range(len(self.poliedro.caras)):
            puntos_cara, vertices_cara, aristas_cara = fusionar_triangulos_base(self.frecuencia, len(self.poliedro.caras[i]), self.tipo)
            vertices_3d = [self.poliedro.vertices[j] for j in self.poliedro.caras[i]]
            puntos_cara = self.actualizar_puntos_a_3d(puntos_cara, vertices_cara, vertices_3d)
            puntos_cara = renombrar_puntos(puntos_cara, i)
            self.puntos = self.puntos | puntos_cara
            vertices_cara = renombrar_vertices(vertices_cara, i)
            self.vertices += vertices_cara
            aristas_cara = renombrar_aristas(aristas_cara, i)
            self.aristas = self.aristas | aristas_cara

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
        fig = plt.figure(figsize=(10, 8))
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

# Ejemplo de uso:
if __name__ == "__main__":
    # Probar de 0 a 13. 14, 15 y 17 tienen bugs
    poliedro_semilla = poliedro_id[0]
    frecuencia = 2
    tipo = 0
    radio = 4
    domo = Domo(poliedro_semilla, frecuencia, tipo, radio)
    domo.dibujar()
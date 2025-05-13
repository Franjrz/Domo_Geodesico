import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from matplotlib.animation import FuncAnimation, FFMpegWriter, PillowWriter

class Zomo():
    def __init__(self, n, h, d):
        self.h = h
        self.n = n
        self.d = d
        self.__calcular_parametros()
        self.__calcular_primera_curva()
        self.__calcular_todas_curvas()
        self.__generar_grafo()
        self.__encontrar_ciclos()
    
    def __calcular_is(self):
        self.iss = np.arange(int(-self.n/2), int(self.n/2)+1)
    
    def __calcular_as(self):
        self.ass = 2 * np.pi * self.iss / self.n

    def __calcular_t_i(self):
        self.t_i = 2 * np.arctan2(np.sin(self.ass), 1 + np.cos(self.ass))

    def __calcular_parametros(self):
        self.__calcular_is()
        self.__calcular_as()
        self.__calcular_t_i()

    def __calcular_x_pts(self):
        self.x_pts = np.sin(-self.t_i + self.ass) * (self.d / 4) + np.sin(self.ass) * (self.d / 4)

    def __calcular_y_pts(self):
        self.y_pts = np.cos(-self.t_i + self.ass) * (self.d / 4) + np.cos(self.ass) * (self.d / 4)

    def __calcular_z_pts(self):
        self.z_pts = self.t_i * self.h / np.pi

    def __calcular_primera_curva(self):
        self.__calcular_x_pts()
        self.__calcular_y_pts()
        self.__calcular_z_pts()
        del self.iss
        del self.ass
        del self.t_i
        if self.n%2 == 1:
            self.x_pts = np.concatenate([[0], self.x_pts, [0]])
            self.y_pts = np.concatenate([[0], self.y_pts, [0]])
            self.z_pts = np.concatenate([[-2 * np.pi], self.z_pts, [2 * np.pi]])

    def __calcular_todas_curvas(self):
        """
        Rota los puntos definidos por self.x_pts y self.y_pts alrededor del eje Z,
        generando self.n copias equiespaciadas angularmente.

        El resultado se guarda en listas:
            self.x_pts : lista de listas con coordenadas x por curva
            self.y_pts : lista de listas con coordenadas y por curva
        """
        # Asegurarse de que los puntos iniciales sean arrays
        x_base = np.array(self.x_pts)
        y_base = np.array(self.y_pts)

        # Inicializar listas para guardar todas las curvas rotadas
        self.x_pts = []
        self.y_pts = []

        for k in range(self.n):
            theta = 2 * np.pi * k / self.n
            cos_t, sin_t = np.cos(theta), np.sin(theta)

            # Rotación en el plano XY
            x_rot = cos_t * x_base - sin_t * y_base
            y_rot = sin_t * x_base + cos_t * y_base

            self.x_pts.append(x_rot)
            self.y_pts.append(y_rot)
        # for i in range(self.n):
        #     print("0_0", self.x_pts[0][0], self.y_pts[0][0], self.z_pts[0])
        #     for j in range(1, len(self.x_pts[0])-1):
        #         print(str(i) + "_" + str(j), self.x_pts[i][j], self.y_pts[i][j], self.z_pts[j])
        #     print("0_" + str(len(self.x_pts[0]) - 1), self.x_pts[0][len(self.x_pts[0]) - 1], self.y_pts[0][len(self.x_pts[0]) - 1], self.z_pts[len(self.x_pts[0]) - 1])

    def __generar_grafo(self):
        self.puntos = {}
        self.aristas = {}

        #Añadir el punto inferior
        self.puntos["0_0"] = (self.x_pts[0][0], self.y_pts[0][0], self.z_pts[0])
        self.aristas["0_0"] = [str(i) + "_1" for i in range(self.n)]
        
        #Añadir el punto superior
        self.puntos["0_" + str(len(self.x_pts[0]) - 1)] = (self.x_pts[0][-1], self.y_pts[0][-1], self.z_pts[-1])
        self.aristas["0_" + str(len(self.x_pts[0]) - 1)] = [str(i) + "_" + str(len(self.x_pts[0]) - 2) for i in range(self.n)]

        #añadir puntos intermedios
        for i in range(self.n):
            for j in range(1, len(self.x_pts[0]) - 1):
                id_punto = str(i) + "_" + str(j)
                self.puntos[id_punto] = (self.x_pts[i][j], self.y_pts[i][j], self.z_pts[j])
                condicion_encima_subcuspide = (j == (len(self.x_pts[0]) - 2))
                condicion_encima_resto = (j < (len(self.x_pts[0]) - 2))
                condicion_debajo_subcuspide = (j == 1)
                condicion_debajo_resto = (j > 1)
                puntos_encima_subcuspide = ["0_" + str(len(self.x_pts[0]) - 1)]
                puntos_encima_resto = [str((i + 1) % self.n) + "_" + str(j+1), str(i) + "_" + str(j+1)]
                puntos_debajo_subcuspide = ["0_0"]
                puntos_debajo_resto = [str((i - 1) % self.n) + "_" + str(j-1), str(i) + "_" + str(j-1)]
                id_puntos_arriba = condicion_encima_subcuspide * puntos_encima_subcuspide + \
                                    condicion_encima_resto * puntos_encima_resto
                id_puntos_debajo = condicion_debajo_subcuspide * puntos_debajo_subcuspide + \
                                    condicion_debajo_resto * puntos_debajo_resto
                self.aristas[id_punto] = id_puntos_arriba + id_puntos_debajo

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
        for ciclo_1 in range(len(self.caras)):
            iguales = False
            for ciclo_2 in range(ciclo_1 + 1, len(self.caras)):
                # Compara si dos ciclos tienen los mismos vértices (sin importar el orden)
                if set(self.caras[ciclo_1]) == set(self.caras[ciclo_2]):
                    iguales = True
                    break
            if not iguales:
                ciclos_limpios.append(self.caras[ciclo_1])

        self.caras = ciclos_limpios  # Mantiene solo un ciclo único por conjunto de vértices

    # Método privado para encontrar todas las caras del poliedro
    def __encontrar_ciclos(self):
        # Inicializa el diccionario de caras separadas por su longitud
        self.caras = []

        # Para cada posible longitud de cara
        for nodo in self.aristas:
            self.ciclos = []
            # Busca ciclos partiendo de cada nodo
            self.__busqueda_en_profundidad([nodo], nodo, 4)
            self.caras += self.ciclos
        
        # Limpia los ciclos encontrados
        self.__limpiar_ciclos()

        del self.ciclos

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
        ajustando la intensidad por distancia a la fuente de luz. Solo considera caras de 4 vértices.

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

                if len(vertices) < 4:
                    continue  # Solo tratamos caras cuadradas

                v0, v1, v2, v3 = np.array(vertices[:4])

                # Calcular normales
                normal1 = np.cross(v1 - v0, v2 - v0)
                norm1 = np.linalg.norm(normal1)
                if norm1 < 1e-8:
                    continue
                normal1 /= norm1

                normal2 = np.cross(v2 - v0, v3 - v0)
                norm2 = np.linalg.norm(normal2)
                if norm2 < 1e-8:
                    continue
                normal2 /= norm2

                # Promedio si las normales son similares
                if np.linalg.norm(normal1 - normal2) < 1e-6:
                    normal = normal1
                else:
                    normal = normal1 + normal2
                    norm_avg = np.linalg.norm(normal)
                    if norm_avg < 1e-8:
                        continue
                    normal /= norm_avg

                # Centroide
                centroide = np.mean([v0, v1, v2, v3], axis=0)

                # Iluminación
                vector_luz = fuente_luz - centroide
                if np.dot(normal, vector_luz) < 0:
                    normal = -normal

                vector_luz /= np.linalg.norm(vector_luz)
                intensidad_base = np.clip(np.dot(normal, vector_luz), min_intensidad, 1.0)

                distancia = np.linalg.norm(fuente_luz - centroide)

                intensidades.append(intensidad_base)
                distancias.append(distancia)

            # Si no hay caras válidas, agregar frame vacío
            if not intensidades:
                colores_por_rotacion.append([])
                continue

            distancias = np.array(distancias)
            d_min, d_max = np.min(distancias), np.max(distancias)
            d_norm = (distancias - d_min) / (d_max - d_min + 1e-8)

            for i in range(len(distancias)):
                ajuste = 1.0 - factor_distancia * d_norm[i]
                intensidad_final = intensidades[i] * ajuste
                intensidad_final = np.clip(intensidad_final, min_intensidad, 1.0)
                color = intensidad_final * color_base_rgb
                colores_cara.append(color)

            colores_por_rotacion.append(colores_cara)

        return colores_por_rotacion

    def generar_video_rotacion(self, pasos=120, elevacion=30, ids=False, alpha_caras=0.95, nombre_salida = "poliedro.gif"):
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
            n_info = str(self.n) + " petalos "
            h_info = str(self.h) + " altura "
            d_info = str(self.d) + " diametro "
            titulo = f"{n_info}\n {h_info}\n {d_info}"
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


n = 10
h = 2
d = 1.5

zomo = Zomo(n, h, d)

# for i in zomo.puntos:
#     print(i, zomo.puntos[i])
# for i in zomo.aristas:
#     print(i, zomo.aristas[i])
# for i in zomo.caras:
#     print(i)

zomo.generar_video_rotacion()
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def visualizar_cara(triangulos):
    """
    Visualiza los triángulos, el centro y el polígono completo.
    
    Args:
        triangulos: Lista de triángulos (cada uno con 3 vértices)
        centro: Coordenadas del centro del polígono
        vertices: Lista de vértices del polígono
    """
    # Generar puntos de interes
    centro = triangulos[0][2]
    vertices = [vertice[0] for vertice in triangulos]


    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Dibujar el polígono en azul claro
    poligono = Polygon(np.array(vertices), alpha=0.3, color='skyblue', zorder=1)
    ax.add_patch(poligono)
    
    # Dibujar los vértices como puntos azul oscuro
    vertices_array = np.array(vertices)
    ax.scatter(vertices_array[:, 0], vertices_array[:, 1], color='darkblue', 
              s=60, label='Vértices', zorder=3)
    
    # Dibujar el centro en naranja
    ax.scatter(centro[0], centro[1], color='orange', s=80, 
              label='Centro', zorder=3)
    
    # Configurar el gráfico
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Establecer los límites con un poco de margen
    max_x = max([v[0] for v in vertices]) + 0.2
    min_x = min([v[0] for v in vertices]) - 0.2
    max_y = max([v[1] for v in vertices]) + 0.2
    min_y = min([v[1] for v in vertices]) - 0.2
    
    ax.set_xlim(min_x, max_x)
    ax.set_ylim(min_y, max_y)
    
    ax.set_title(f'Triangulación de la cara')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    
    plt.tight_layout()
    plt.show()

def visualizar_cara_final(puntos, vertices, aristas, mostrar_ids=False):
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
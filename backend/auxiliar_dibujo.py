import json
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

def visualize_truncated_octahedron(json_file=None, json_str=None):
    """
    Visualiza un octaedro truncado en 3D a partir de un archivo JSON o una cadena JSON.
    
    Args:
        json_file (str, optional): Ruta al archivo JSON con los datos del octaedro truncado.
        json_str (str, optional): Cadena JSON con los datos del octaedro truncado.
        
    Returns:
        tuple: Retorna la figura y los ejes de matplotlib.
    """
    # Cargar los datos JSON
    if json_file:
        with open(json_file, 'r') as f:
            data = json.load(f)
    elif json_str:
        data = json.loads(json_str)
    else:
        raise ValueError("Debes proporcionar un archivo JSON o una cadena JSON")
    
    # Extraer los vértices
    vertices = np.array(data["vertices"])
    
    # Crear la figura 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Dibujar los puntos de los vértices
    ax.scatter(vertices[:, 0], vertices[:, 1], vertices[:, 2], 
               c='blue', marker='o', s=80, label='Vértices')
    
    # Función para calcular la distancia entre dos vértices
    def distance(v1, v2):
        return np.linalg.norm(np.array(v1) - np.array(v2))
    
    # Calcular todas las aristas (pares de vértices conectados)
    # Las aristas del octaedro truncado conectan vértices a distancia 2
    tolerance = 0.1  # Tolerancia para comparar distancias
    edge_distance = 2.0  # Distancia esperada entre vértices adyacentes
    
    edges = []
    for i in range(len(vertices)):
        for j in range(i+1, len(vertices)):
            dist = distance(vertices[i], vertices[j])
            if abs(dist - edge_distance) < tolerance:
                edges.append((i, j))
                # Dibujar las aristas
                ax.plot([vertices[i][0], vertices[j][0]],
                        [vertices[i][1], vertices[j][1]],
                        [vertices[i][2], vertices[j][2]],
                        'k-', linewidth=1.5)
    
    # Determinación de caras - Primero las cuadradas
    # En un octaedro truncado, las caras cuadradas están en las posiciones de los vértices originales
    # del octaedro, que tienen coordenadas (±2, ±1, ±1) y permutaciones
    
    # Función para encontrar caras por coordenada fija
    def find_face_by_fixed_coordinate(coordinate_index, value):
        face_vertices = []
        for i, vertex in enumerate(vertices):
            if abs(vertex[coordinate_index] - value) < tolerance:
                face_vertices.append(i)
        return face_vertices
    
    # Encontrar caras cuadradas - hay 6 caras cuadradas, una por cada valor ±2 en cada coordenada
    square_faces = []
    for axis in range(3):  # x, y, z
        for value in [-2, 2]:  # valores extremos
            face = find_face_by_fixed_coordinate(axis, value)
            if len(face) >= 4:  # Debería haber exactamente 4 vértices
                square_faces.append([vertices[i] for i in face])
    
    # Dibujar caras cuadradas
    for face in square_faces:
        # Ordenar vértices para asegurar que forman un polígono cerrado
        center = np.mean(face, axis=0)
        # Proyectar a 2D y ordenar
        normal = np.cross(face[1] - face[0], face[2] - face[0])
        normal = normal / np.linalg.norm(normal)
        # Crear un sistema de coordenadas local
        u = face[0] - center
        u = u / np.linalg.norm(u)
        v = np.cross(normal, u)
        
        # Proyectar puntos en el plano y ordenarlos por ángulo
        projected = []
        for vertex in face:
            diff = vertex - center
            x = np.dot(diff, u)
            y = np.dot(diff, v)
            angle = np.arctan2(y, x)
            projected.append((angle, vertex))
        
        projected.sort(key=lambda x: x[0])
        ordered_face = [p[1] for p in projected]
        
        # Crear cara y añadirla
        poly = Poly3DCollection([ordered_face], alpha=0.6, facecolor='lightblue', edgecolor='blue')
        ax.add_collection3d(poly)
    
    # Configurar límites y etiquetas
    max_range = np.max(np.abs(vertices)) + 0.5
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title(data["name"], fontsize=14, fontweight='bold')
    
    # Añadir información adicional si está disponible
    if "description" in data:
        plt.figtext(0.5, 0.01, data["description"], ha='center', fontsize=10)
    
    # Añadir leyenda
    plt.legend(loc='upper right')
    
    # Ajustar la vista para una mejor visualización
    ax.view_init(elev=30, azim=45)
    
    plt.tight_layout()
    plt.show()
    
    return fig, ax

# Ejemplo de uso
if __name__ == "__main__":
    # Puedes usar esta función de dos maneras:
    
    # 1. Pasando una cadena JSON directamente
    json_str = """
    {
    "name": "Octaedro Truncado Regular (arista=1)",
    "vertices": [
        [-1.4142135623730951, -0.7071067811865476, 0],
        [-1.4142135623730951, 0, -0.7071067811865476],
        [-0.7071067811865476, -1.4142135623730951, 0],
        [-0.7071067811865476, 0, -1.4142135623730951],
        [0, -1.4142135623730951, -0.7071067811865476],
        [0, -0.7071067811865476, -1.4142135623730951],
        [-1.4142135623730951, 0.7071067811865476, 0],
        [-1.4142135623730951, 0, 0.7071067811865476],
        [0.7071067811865476, -1.4142135623730951, 0],
        [0.7071067811865476, 0, -1.4142135623730951],
        [0, -1.4142135623730951, 0.7071067811865476],
        [0, 0.7071067811865476, -1.4142135623730951],
        [1.4142135623730951, -0.7071067811865476, 0],
        [1.4142135623730951, 0, -0.7071067811865476],
        [-0.7071067811865476, 1.4142135623730951, 0],
        [-0.7071067811865476, 0, 1.4142135623730951],
        [0, 1.4142135623730951, -0.7071067811865476],
        [0, -0.7071067811865476, 1.4142135623730951],
        [1.4142135623730951, 0.7071067811865476, 0],
        [1.4142135623730951, 0, 0.7071067811865476],
        [0.7071067811865476, 1.4142135623730951, 0],
        [0.7071067811865476, 0, 1.4142135623730951],
        [0, 1.4142135623730951, 0.7071067811865476],
        [0, 0.7071067811865476, 1.4142135623730951]
    ],
    "description": "Un poliedro semirregular (sólido de Arquímedes) con 24 vértices, 36 aristas, 6 caras cuadradas y 8 caras hexagonales. Con arista de longitud 1."
    }
    """
    visualize_truncated_octahedron(json_str=json_str)
    
    # 2. O guardando el JSON en un archivo y pasando la ruta
    # with open('octaedro_truncado.json', 'w') as f:
    #     f.write(json_str)
    # visualize_truncated_octahedron(json_file='octaedro_truncado.json')
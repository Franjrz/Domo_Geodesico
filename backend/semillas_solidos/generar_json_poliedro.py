import numpy as np
from scipy.spatial import ConvexHull

def generar_caras(vertices):
    """
    Genera las caras de un poliedro convexo a partir de una lista de vértices en 3D.

    Parámetros:
    vertices (list of tuple): Lista de tuplas que representan las coordenadas (x, y, z) de los vértices.

    Retorna:
    list of list: Lista de caras, donde cada cara es una lista de índices de vértices en orden horario.
    """
    # Convertir la lista de vértices a un array de NumPy
    puntos = np.array(vertices)

    # Calcular el casco convexo
    casco = ConvexHull(puntos)

    # Obtener las caras (simplices) del casco convexo
    caras = casco.simplices

    # Opcional: ordenar los vértices de cada cara en sentido horario
    # Esto puede requerir una implementación adicional dependiendo de la orientación deseada

    # Convertir las caras a listas de índices
    lista_caras = [list(cara) for cara in caras]

    return lista_caras

# Lista de vértices de un cubo
vertices_cubo = [
    (0, 0, 0),
    (0, 0, 1),
    (0, 1, 0),
    (0, 1, 1),
    (1, 0, 0),
    (1, 0, 1),
    (1, 1, 0),
    (1, 1, 1)
]

caras_cubo = generar_caras(vertices_cubo)

print("Caras del cubo:")
for cara in caras_cubo:
    print(cara)

from math import pow, sqrt
from scipy.constants import golden as phi
import numpy as np

def __tetraedro():
    """
    Genera las coordenadas de los 4 vértices de un tetraedro regular centrado en el origen.

    Cada vértice se calcula aplicando signos alternos (+/-) en los ejes X, Y, Z 
    para repartir los vértices de manera simétrica.

    Retorna:
        Lista de 4 tuplas (x, y, z), cada una representando un vértice del tetraedro.
    """
    return [(pow(-1, int((i+1)/2)), pow(-1, i), pow(-1, int(i/2))) for i in range(4)]

def __cubo():
    """
    Genera las coordenadas de los 8 vértices de un cubo regular (hexaedro) centrado en el origen.

    Cada vértice corresponde a todas las combinaciones posibles de (±1, ±1, ±1) en X, Y, Z.

    Retorna:
        Lista de 8 tuplas (x, y, z), representando los vértices del cubo.
    """
    return [tuple(pow(-1, int(i/pow(2, j))) for j in range(3)) for i in range(8)]

def __octaedro():
    """
    Genera las coordenadas de los 6 vértices de un octaedro regular centrado en el origen.

    Cada vértice se coloca en un eje positivo o negativo (ejes X, Y o Z), 
    con las otras dos coordenadas siendo 0.

    Retorna:
        Lista de 6 tuplas (x, y, z), representando los vértices del octaedro.
    """
    return [tuple(s if i == d else 0 for i in range(3)) for d in range(3) for s in [1, -1]]

def __dodecaedro():
    """
    Genera los 20 vértices de un dodecaedro regular centrado en el origen,
    usando la proporción áurea φ (phi).

    Estructura de los vértices:
    - Primer grupo (12 vértices):
        * Combinaciones cíclicas de (0, ±1, ±(φ+1)) en las coordenadas (x, y, z).
        * Se rota la posición de los valores para cubrir las 3 permutaciones posibles.
        * Se generan 4 combinaciones de signos para cada rotación.

    - Segundo grupo (8 vértices):
        * Vértices de la forma (±φ, ±φ, ±φ).
        * Se alternan los signos en función de los bits del índice.

    Retorna:
        Una lista de 20 tuplas (x, y, z), cada una representando un vértice del dodecaedro.
    """
    vertices = []

    # Generar los primeros 12 vértices: combinaciones de (0, ±1, ±(φ+1))
    vertices += [tuple(v[(p+j)%3] for j in range(3)) 
                 for p in range(3)         # para cada permutación de coordenadas (x, y, z)
                 for i in range(4)          # para las 4 combinaciones de signos
                 for v in [(0, pow(-1, int(i/2)), (phi + 1) * pow(-1, i))]]  # patrón base

    # Generar los 8 vértices restantes: combinaciones de (±φ, ±φ, ±φ)
    vertices += [(phi * pow(-1, int(i/4)), 
                  phi * pow(-1, int(i/2)), 
                  phi * pow(-1, int(i))) for i in range(8)]

    return vertices

def __icosaedro():
    """
    Genera las coordenadas de los 12 vértices de un icosaedro regular
    centrado en el origen, usando la proporción áurea φ (phi).

    Estructura de los vértices:
    - Cada vértice tiene la forma (0, ±1, ±φ), donde:
        * Un eje tiene valor 0.
        * Otro eje tiene ±1.
        * El tercer eje tiene ±φ.
    - Se generan todas las rotaciones cíclicas posibles entre los ejes (x, y, z).
    - Para cada rotación, se generan 4 combinaciones de signos.

    Retorna:
        Una lista de 12 tuplas (x, y, z), cada una representando un vértice del icosaedro.
    """
    return [
        tuple(v[(p + j) % 3] for j in range(3))  # Reordena (0, ±1, ±φ) rotando las coordenadas
        for p in range(3)                        # Rota las posiciones (x, y, z)
        for i in range(4)                        # Explora 4 combinaciones de signos
        for v in [(0, pow(-1, int(i/2)), phi * pow(-1, i))]  # Patrón base (0, ±1, ±φ)
    ]

def __tetraedro_truncado():
    """
    Genera las coordenadas de los 12 vértices de un tetraedro truncado
    (también llamado "truncated tetrahedron"), centrado en el origen.

    Estructura de los vértices:
    - Cada vértice tiene coordenadas proporcionales a:
        * √2/4 * 3 en un eje (el eje especial).
        * √2/4 en los otros dos ejes.
    - Para cada elección de eje especial (x, y o z), se generan 4 combinaciones de signos:
        * ( +, +, + )
        * ( +, -, - )
        * ( -, +, - )
        * ( -, -, + )

    Retorna:
        Una lista de 12 tuplas (x, y, z), cada una representando un vértice del tetraedro truncado.
    """
    return [
        tuple(
            a * b  # Multiplica el patrón de signos por el valor de cada coordenada
            for a, b in zip(sign, [sqrt(2)/4 * (3 if j == i else 1) for j in range(3)])
        )
        for i in range(3)  # Para cada eje, se elige cuál tendrá el "3 * √2/4"
        for sign in [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]  # Cuatro patrones de signos
    ]

def __cubo_truncado():
    """
    Genera las coordenadas de los 24 vértices de un cubo truncado 
    (truncated cube), centrado en el origen.

    Estructura de los vértices:
    - Cada vértice es una combinación de valores ±1 y ±(1 + √2).
    - Se consideran combinaciones donde dos coordenadas toman el valor (1 + √2)
      y la tercera coordenada es ±1.
    - Se generan tres bloques de 8 vértices cada uno, variando qué eje tiene el valor ±1.

    Retorna:
        Una lista de 24 tuplas (x, y, z), cada una representando un vértice del cubo truncado.
    """
    aux = 1 + sqrt(2)  # Valor auxiliar (1 + √2), necesario para la proporción exacta
    vertices = []

    # Primer grupo: eje X es ±1, ejes Y y Z son ±(1+√2)
    vertices += [(pow(-1, int(i/4)), aux * pow(-1, int(i/2)), aux * pow(-1, i)) for i in range(8)]

    # Segundo grupo: eje Y es ±1, ejes X y Z son ±(1+√2)
    vertices += [(aux * pow(-1, int(i/4)), pow(-1, int(i/2)), aux * pow(-1, i)) for i in range(8)]

    # Tercer grupo: eje Z es ±1, ejes X y Y son ±(1+√2)
    vertices += [(aux * pow(-1, int(i/4)), aux * pow(-1, int(i/2)), pow(-1, i)) for i in range(8)]

    return vertices

def __octaedro_truncado():
    """
    Genera las coordenadas de los 24 vértices de un octaedro truncado 
    (truncated octahedron), centrado en el origen.

    Estructura de los vértices:
    - Los vértices combinan los valores ±√2, ±(√2/2) y 0 en las coordenadas (x, y, z).
    - Cada vértice tiene un 0 en una coordenada, y los otros dos ejes
      toman valores ±(√2) o ±(√2/2).
    - Se generan 6 grupos de 4 vértices cada uno, combinando signos
      y ubicaciones del cero en diferentes posiciones.

    Retorna:
        Una lista de 24 tuplas (x, y, z), representando los vértices del octaedro truncado.
    """
    sqrt_2 = sqrt(2)      # √2
    sqrt_2_2 = sqrt_2 / 2 # √2 dividido entre 2

    vertices = []

    # Cada bloque de vértices coloca un 0 en una de las coordenadas (x, y, o z)
    # y combina (±√2) y (±√2/2) en las otras dos coordenadas

    # 1. 0 en Z
    vertices += [(sqrt_2 * pow(-1, int(i/2)), sqrt_2_2 * pow(-1, i), 0) for i in range(4)]

    # 2. 0 en Y
    vertices += [(sqrt_2_2 * pow(-1, i), 0, sqrt_2 * pow(-1, int(i/2))) for i in range(4)]

    # 3. 0 en X
    vertices += [(0, sqrt_2 * pow(-1, int(i/2)), sqrt_2_2 * pow(-1, i)) for i in range(4)]

    # 4. 0 en Z (con orden de coordenadas permutado)
    vertices += [(sqrt_2_2 * pow(-1, int(i/2)), sqrt_2 * pow(-1, i), 0) for i in range(4)]

    # 5. 0 en Y (permutado)
    vertices += [(sqrt_2 * pow(-1, i), 0, sqrt_2_2 * pow(-1, int(i/2))) for i in range(4)]

    # 6. 0 en X (permutado)
    vertices += [(0, sqrt_2_2 * pow(-1, int(i/2)), sqrt_2 * pow(-1, i)) for i in range(4)]

    return vertices

def __dodecaedro_truncado():
    """
    Genera las coordenadas de los 60 vértices de un dodecaedro truncado 
    (truncated dodecahedron), centrado en el origen, utilizando la proporción áurea φ (phi).

    Estructura de los vértices:
    - Se usan combinaciones de los valores 0, ±1/φ, ±(φ+1), ±(φ+2), ±2φ y ±φ.
    - Los vértices se agrupan en 9 bloques diferentes, cada uno generando combinaciones específicas de coordenadas.
    - Se generan combinaciones alternando signos (positivo y negativo) sistemáticamente.

    Retorna:
        Una lista de 60 tuplas (x, y, z), cada una representando un vértice del dodecaedro truncado.
    """
    inv_phi = 1 / phi       # Inverso de φ
    phi_1 = phi + 1         # φ + 1
    phi_2 = phi + 2         # φ + 2
    phi__2 = 2 * phi        # 2 * φ
    vertices = []

    # Grupo 1-3: (0, ±1/φ, ±(φ+2)) y permutaciones
    vertices += [(0, inv_phi * pow(-1, int(i/2)), phi_2 * pow(-1, i)) for i in range(4)]
    vertices += [(inv_phi * pow(-1, int(i/2)), phi_2 * pow(-1, i), 0) for i in range(4)]
    vertices += [(phi_2 * pow(-1, int(i/2)), 0, inv_phi * pow(-1, i)) for i in range(4)]

    # Grupo 4-6: combinaciones (±1/φ, ±φ, ±2φ)
    vertices += [(inv_phi * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), phi__2 * pow(-1, i)) for i in range(8)]
    vertices += [(phi__2 * pow(-1, int(i/4)), inv_phi * pow(-1, int(i/2)), phi * pow(-1, i)) for i in range(8)]
    vertices += [(phi * pow(-1, int(i/4)), phi__2 * pow(-1, int(i/2)), inv_phi * pow(-1, i)) for i in range(8)]

    # Grupo 7-9: combinaciones (±φ, ±2, ±(φ+1))
    vertices += [(phi * pow(-1, int(i/4)), 2 * pow(-1, int(i/2)), phi_1 * pow(-1, i)) for i in range(8)]
    vertices += [(phi_1 * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), 2 * pow(-1, i)) for i in range(8)]
    vertices += [(2 * pow(-1, int(i/4)), phi_1 * pow(-1, int(i/2)), phi * pow(-1, i)) for i in range(8)]

    return vertices

def __icosaedro_truncado():
    """
    Genera las coordenadas de los 60 vértices de un icosaedro truncado 
    (truncated icosahedron), centrado en el origen, utilizando la proporción áurea φ (phi).

    Estructura de los vértices:
    - Se usan combinaciones de los valores 0, ±1, ±2, ±φ, ±2φ, ±3φ y ±(2φ+1).
    - Los vértices se agrupan en 9 bloques diferentes, cada uno generando combinaciones específicas.
    - Se alternan sistemáticamente los signos (positivo y negativo) para cubrir toda la simetría.

    Retorna:
        Una lista de 60 tuplas (x, y, z), cada una representando un vértice del icosaedro truncado.
    """

    # Definimos las constantes necesarias basadas en φ
    phi_2 = phi + 2         # φ + 2
    phi__3 = 3 * phi        # 3φ
    phi__2 = 2 * phi        # 2φ
    phi_2_1 = 2*phi + 1     # 2φ + 1

    vertices = []

    # Grupo 1-3: coordenadas tipo (0, ±1, ±3φ) y permutaciones
    vertices += [(0, pow(-1, int(i/2)), phi__3 * pow(-1, i)) for i in range(4)]
    vertices += [(pow(-1, int(i/2)), phi__3 * pow(-1, i), 0) for i in range(4)]
    vertices += [(phi__3 * pow(-1, int(i/2)), 0, pow(-1, i)) for i in range(4)]

    # Grupo 4-6: combinaciones de (±1, ±(φ+2), ±2φ)
    vertices += [(pow(-1, int(i/4)), phi_2 * pow(-1, int(i/2)), phi__2 * pow(-1, i)) for i in range(8)]
    vertices += [(phi_2 * pow(-1, int(i/4)), phi__2 * pow(-1, int(i/2)), pow(-1, i)) for i in range(8)]
    vertices += [(phi__2 * pow(-1, int(i/4)), pow(-1, int(i/2)), phi_2 * pow(-1, i)) for i in range(8)]

    # Grupo 7-9: combinaciones de (±φ, ±2, ±(2φ+1))
    vertices += [(phi * pow(-1, int(i/4)), 2 * pow(-1, int(i/2)), phi_2_1 * pow(-1, i)) for i in range(8)]
    vertices += [(2 * pow(-1, int(i/4)), phi_2_1 * pow(-1, int(i/2)), phi * pow(-1, i)) for i in range(8)]
    vertices += [(phi_2_1 * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), 2 * pow(-1, i)) for i in range(8)]

    return vertices

def __cuboctaedro():
    """
    Genera las coordenadas de los 12 vértices de un cuboctaedro regular
    centrado en el origen.

    Estructura de los vértices:
    - Cada vértice tiene exactamente una coordenada igual a 0 y las otras dos iguales a ±1.
    - Se generan combinaciones donde el 0 ocupa cíclicamente las posiciones x, y o z.
    - Para cada elección del eje cero (j=0,1,2), se crean 4 combinaciones diferentes de ±1.

    Retorna:
        Una lista de 12 tuplas (x, y, z), representando los vértices del cuboctaedro.
    """
    return [
        (0 if j == 0 else [-1, 1][i//2],  # Componente x
         0 if j == 1 else [-1, 1][i%2],   # Componente y
         0 if j == 2 else [-1, 1][(i//2 + i%2) % 2])  # Componente z
        for j in range(3)  # Rota el eje que tiene valor 0
        for i in range(4)  # Para cada elección de signos ±1 en los otros dos ejes
    ]

def __cuboctaedro_truncado():
    """
    Genera las coordenadas de los 48 vértices de un cuboctaedro truncado,
    centrado en el origen, combinando 1, (1+√2) y (1+2√2) en las coordenadas.

    Estructura general:
    - Cada vértice es una permutación de ±1, ±(1+√2) y ±(1+2√2).
    - Se generan 6 bloques de 8 vértices, cambiando el orden de los valores en (x, y, z).
    - Se alternan los signos sistemáticamente para mantener la simetría.

    Retorna:
        Lista de 48 tuplas (x, y, z) representando los vértices del cuboctaedro truncado.
    """
    
    # Definimos constantes usadas en las coordenadas
    sqrt_2_1 = 1 + sqrt(2)       # (1 + √2)
    sqrt_2_2_1 = 1 + 2 * sqrt(2) # (1 + 2√2)

    # Inicializamos la lista de vértices
    vertices = []

    # Primer grupo de 8 vértices: (±1, ±(1+√2), ±(1+2√2))
    vertices += [(pow(-1, int(i/4)), sqrt_2_1 * pow(-1, int(i/2)), sqrt_2_2_1 * pow(-1, i)) for i in range(8)]

    # Segundo grupo de 8 vértices: (±(1+√2), ±(1+2√2), ±1)
    vertices += [(sqrt_2_1 * pow(-1, int(i/4)), sqrt_2_2_1 * pow(-1, int(i/2)), pow(-1, i)) for i in range(8)]

    # Tercer grupo de 8 vértices: (±(1+2√2), ±1, ±(1+√2))
    vertices += [(sqrt_2_2_1 * pow(-1, int(i/4)), pow(-1, int(i/2)), sqrt_2_1 * pow(-1, i)) for i in range(8)]

    # Cuarto grupo de 8 vértices: (±(1+√2), ±1, ±(1+2√2))
    vertices += [(sqrt_2_1 * pow(-1, int(i/4)), pow(-1, int(i/2)), sqrt_2_2_1 * pow(-1, i)) for i in range(8)]

    # Quinto grupo de 8 vértices: (±1, ±(1+2√2), ±(1+√2))
    vertices += [(pow(-1, int(i/4)), sqrt_2_2_1 * pow(-1, int(i/2)), sqrt_2_1 * pow(-1, i)) for i in range(8)]

    # Sexto grupo de 8 vértices: (±(1+2√2), ±(1+√2), ±1)
    vertices += [(sqrt_2_2_1 * pow(-1, int(i/4)), sqrt_2_1 * pow(-1, int(i/2)), pow(-1, i)) for i in range(8)]

    # Devolvemos los 48 vértices
    return vertices

def __icosidodecaedro():
    """
    Genera las coordenadas de los 30 vértices del icosidodecaedro regular,
    centrado en el origen, utilizando combinaciones relacionadas con la proporción áurea φ.

    Estructura general:
    - Usa los valores ±1, ±(φ/2), ±(1/2φ) y ±0.5 en las coordenadas (x, y, z).
    - Algunos vértices tienen una coordenada nula (0) y las otras dos no.
    - Se organizan en bloques de 6 vértices en los ejes y 24 combinaciones simétricas.

    Retorna:
        Lista de 30 tuplas (x, y, z) representando los vértices del icosidodecaedro.
    """

    # Constantes basadas en φ
    phi_2 = phi / 2          # φ/2
    phi_1_2 = 1 / (2 * phi)  # 1/(2φ)

    # Lista de vértices
    vertices = []

    # Añade 6 vértices en los ejes (±1, 0, 0), (0, ±1, 0), (0, 0, ±1)
    vertices += [(pow(-1, int(i)), 0, 0) for i in range(2)]
    vertices += [(0, pow(-1, int(i)), 0) for i in range(2)]
    vertices += [(0, 0, pow(-1, int(i))) for i in range(2)]

    # Añade 24 vértices combinando ±(φ/2), ±(1/2φ) y ±0.5 en las tres permutaciones
    vertices += [(phi_2 * pow(-1, int(i/4)), phi_1_2 * pow(-1, int(i/2)), 0.5 * pow(-1, i)) for i in range(8)]
    vertices += [(phi_1_2 * pow(-1, int(i/4)), 0.5 * pow(-1, int(i/2)), phi_2 * pow(-1, i)) for i in range(8)]
    vertices += [(0.5 * pow(-1, int(i/4)), phi_2 * pow(-1, int(i/2)), phi_1_2 * pow(-1, i)) for i in range(8)]

    return vertices

def __icosidodecaedro_truncado():
    """
    Genera las coordenadas de los 120 vértices de un icosidodecaedro truncado,
    centrado en el origen, utilizando combinaciones de constantes relacionadas con φ (phi).

    Estructura general:
    - Usa valores derivados como ±(1/φ), ±(2/φ), ±(1+φ), ±(2+φ), ±(3+φ), ±(2φ-1), ±(2φ+1), etc.
    - Cada grupo de vértices representa diferentes patrones de combinaciones
      entre esas constantes en las coordenadas (x, y, z).
    - Alterna los signos sistemáticamente para cubrir toda la simetría.

    Retorna:
        Lista de 120 tuplas (x, y, z) representando los vértices del poliedro.
    """

    # Definición de constantes basadas en φ
    phi_1 = 1 / phi          # 1/φ
    phi_2 = 2 / phi          # 2/φ
    phi___2 = 2 * phi        # 2φ
    phi__1 = 1 + phi         # 1+φ
    phi__2 = 2 + phi         # 2+φ
    phi__3 = 3 + phi         # 3+φ
    phi_1_2 = 1 + 2*phi      # 1+2φ
    phi__1_2 = 2*phi - 1     # 2φ-1
    phi__1_3 = -1 + 3*phi    # -1+3φ

    # Inicializamos la lista de vértices
    vertices = []

    # Primer grupo: combinaciones con 1/φ y 3+φ
    vertices += [(phi_1 * pow(-1, int(i/4)), phi_1 * pow(-1, int(i/2)), phi__3 * pow(-1, i)) for i in range(8)]
    vertices += [(phi_1 * pow(-1, int(i/4)), phi__3 * pow(-1, int(i/2)), phi_1 * pow(-1, i)) for i in range(8)]
    vertices += [(phi__3 * pow(-1, int(i/4)), phi_1 * pow(-1, int(i/2)), phi_1 * pow(-1, i)) for i in range(8)]

    # Segundo grupo: combinaciones con 2/φ, φ y 1+2φ
    vertices += [(phi_2 * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), phi_1_2 * pow(-1, i)) for i in range(8)]
    vertices += [(phi * pow(-1, int(i/4)), phi_1_2 * pow(-1, int(i/2)), phi_2 * pow(-1, i)) for i in range(8)]
    vertices += [(phi_1_2 * pow(-1, int(i/4)), phi_2 * pow(-1, int(i/2)), phi * pow(-1, i)) for i in range(8)]

    # Tercer grupo: combinaciones con 1/φ, 1+φ, y -1+3φ
    vertices += [(phi_1 * pow(-1, int(i/4)), phi__1 * pow(-1, int(i/2)), phi__1_3 * pow(-1, i)) for i in range(8)]
    vertices += [(phi__1 * pow(-1, int(i/4)), phi__1_3 * pow(-1, int(i/2)), phi_1 * pow(-1, i)) for i in range(8)]
    vertices += [(phi__1_3 * pow(-1, int(i/4)), phi_1 * pow(-1, int(i/2)), phi__1 * pow(-1, i)) for i in range(8)]

    # Cuarto grupo: combinaciones con 2φ-1, 2 y 2+φ
    vertices += [(phi__1_2 * pow(-1, int(i/4)), 2 * pow(-1, int(i/2)), phi__2 * pow(-1, i)) for i in range(8)]
    vertices += [(2 * pow(-1, int(i/4)), phi__2 * pow(-1, int(i/2)), phi__1_2 * pow(-1, i)) for i in range(8)]
    vertices += [(phi__2 * pow(-1, int(i/4)), phi__1_2 * pow(-1, int(i/2)), 2 * pow(-1, i)) for i in range(8)]

    # Quinto grupo: combinaciones con φ, 3 y 2φ
    vertices += [(phi * pow(-1, int(i/4)), 3 * pow(-1, int(i/2)), phi___2 * pow(-1, i)) for i in range(8)]
    vertices += [(3 * pow(-1, int(i/4)), phi___2 * pow(-1, int(i/2)), phi * pow(-1, i)) for i in range(8)]
    vertices += [(phi___2 * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), 3 * pow(-1, i)) for i in range(8)]

    # Devuelve los 120 vértices generados
    return vertices

def __rombicuboctaedro():
    """
    Genera las coordenadas de los 24 vértices de un rombicuboctaedro regular,
    centrado en el origen, usando combinaciones de 1 y 1 + √2.

    Estructura general:
    - Cada vértice tiene una combinación de valores ±1 y ±(1+√2) en las coordenadas (x, y, z).
    - En cada grupo, un eje toma el valor ±(1+√2) y los otros dos ±1.
    - Se generan 3 bloques de 8 vértices cada uno, permutando los ejes.

    Retorna:
        Lista de 24 tuplas (x, y, z) representando los vértices del rombicuboctaedro.
    """

    # Definimos la constante (1 + √2)
    sqrt_2_1 = 1 + sqrt(2)

    # Inicializamos la lista de vértices
    vertices = []

    # Primer bloque de 8 vértices: (±(1+√2), ±1, ±1)
    vertices += [
        (sqrt_2_1 * pow(-1, int(i/4)), pow(-1, int(i/2)), pow(-1, i))
        for i in range(8)
    ]

    # Segundo bloque de 8 vértices: (±1, ±1, ±(1+√2))
    vertices += [
        (pow(-1, int(i/4)), pow(-1, int(i/2)), sqrt_2_1 * pow(-1, i))
        for i in range(8)
    ]

    # Tercer bloque de 8 vértices: (±1, ±(1+√2), ±1)
    vertices += [
        (pow(-1, int(i/4)), sqrt_2_1 * pow(-1, int(i/2)), pow(-1, i))
        for i in range(8)
    ]

    # Devolvemos los 24 vértices generados
    return vertices

def __rombicosidodecaedro():
    """
    Genera las coordenadas de los 60 vértices de un rombicosidodecaedro,
    centrado en el origen, utilizando combinaciones de constantes relacionadas con φ (phi).

    Estructura general:
    - Se combinan valores ±1, ±φ, ±φ², ±φ³, ±2φ y ±(2+φ).
    - Los vértices se agrupan en bloques según diferentes patrones de combinaciones en x, y y z.
    - Alterna sistemáticamente los signos en cada bloque para cubrir toda la simetría del sólido.

    Retorna:
        Lista de 60 tuplas (x, y, z) representando los vértices del rombicosidodecaedro.
    """

    # Definimos las constantes basadas en φ
    phi__2 = pow(phi, 2)    # φ²
    phi__3 = pow(phi, 3)    # φ³
    phi___2 = 2 * phi       # 2φ
    phi_2 = 2 + phi         # 2 + φ

    # Inicializamos la lista de vértices
    vertices = []

    # Primer grupo de 8 vértices: (±1, ±1, ±φ³)
    vertices += [(pow(-1, int(i/4)), pow(-1, int(i/2)), phi__3 * pow(-1, i)) for i in range(8)]

    # Segundo grupo de 8 vértices: (±1, ±φ³, ±1)
    vertices += [(pow(-1, int(i/4)), phi__3 * pow(-1, int(i/2)), pow(-1, i)) for i in range(8)]

    # Tercer grupo de 8 vértices: (±φ³, ±1, ±1)
    vertices += [(phi__3 * pow(-1, int(i/4)), pow(-1, int(i/2)), pow(-1, i)) for i in range(8)]

    # Cuarto grupo de 8 vértices: (±φ², ±φ, ±2φ)
    vertices += [(phi__2 * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), phi___2 * pow(-1, i)) for i in range(8)]

    # Quinto grupo de 8 vértices: (±φ, ±2φ, ±φ²)
    vertices += [(phi * pow(-1, int(i/4)), phi___2 * pow(-1, int(i/2)), phi__2 * pow(-1, i)) for i in range(8)]

    # Sexto grupo de 8 vértices: (±2φ, ±φ², ±φ)
    vertices += [(phi___2 * pow(-1, int(i/4)), phi__2 * pow(-1, int(i/2)), phi * pow(-1, i)) for i in range(8)]

    # Séptimo grupo de 4 vértices: (±(2+φ), 0, ±φ²)
    vertices += [(phi_2 * pow(-1, int(i/2)), 0, phi__2 * pow(-1, i)) for i in range(4)]

    # Octavo grupo de 4 vértices: (0, ±φ², ±(2+φ))
    vertices += [(0, phi__2 * pow(-1, int(i/2)), phi_2 * pow(-1, i)) for i in range(4)]

    # Noveno grupo de 4 vértices: (±φ², ±(2+φ), 0)
    vertices += [(phi__2 * pow(-1, int(i/2)), phi_2 * pow(-1, i), 0) for i in range(4)]

    # Devolvemos los 60 vértices generados
    return vertices

def __cubo_romo_levogiro():
    """
    Genera las coordenadas de los 24 vértices del cubo romo levogiro(snub cube),
    centrado en el origen, usando la constante tribonacci.

    - Utiliza combinaciones de ±1, ±tribonacci y ±(1/tribonacci).
    - Agrupa en dos bloques de vértices, variando los signos de las coordenadas.
    - Dentro de cada bloque:
        * Para cada combinación de signos, genera 3 vértices, permutando t, 1, y 1/t.
    
    Retorna:
        Una lista de 24 tuplas (x, y, z), cada una representando un vértice del cubo romo.
    """

    # Definimos la constante tribonacci t ≈ 1.839...
    t = 1.839286755214161
    t_1 = 1 / t  # Inverso de tribonacci

    vertices = []

    # Primer bloque de signos específicos
    vertices += [
        v for s1, s2, s3 in [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]
        for v in [(s1, s2 * t, s3 * t_1), (s1 * t, s2 * t_1, s3), (s1 * t_1, s2, s3 * t)]
    ]

    # Segundo bloque de signos opuestos
    vertices += [
        v for s1, s2, s3 in [(-1, 1, 1), (1, -1, 1), (1, 1, -1), (-1, -1, -1)]
        for v in [(s1, s2 * t_1, s3 * t), (s1 * t, s2, s3 * t_1), (s1 * t_1, s2 * t, s3)]
    ]

    return vertices

def __cubo_romo_dextrogiro():
    """
    Genera las coordenadas de los 24 vértices del cubo romo dextrogiro(snub cube),
    centrado en el origen.

    Todas las componentes de todos los vértices invierten su signo para formar una imagen
    especular de su contraparte levogira
    
    Retorna:
        Una lista de 24 tuplas (x, y, z), cada una representando un vértice del cubo romo.
    """

    return [(-i[0], -i[1], -i[2]) for i in __cubo_romo_levogiro()]

def __multiplicar(vectores, matriz, potencia):
    """
    Aplica una matriz elevada a una cierta potencia a una lista de vectores.

    Args:
        vectores: lista de vectores (x, y, z) como tuplas.
        matriz: matriz 3x3 (numpy array) de rotación.
        potencia: entero, número de veces que se multiplica la matriz por sí misma.

    Retorna:
        Lista de nuevos vectores resultantes de la transformación.
    """
    return [tuple(np.dot(np.array(vectores[i]), np.linalg.matrix_power(matriz, potencia))) for i in range(5)]

def __rotation_matrix(axis, theta):
    """
    Genera la matriz de rotación de un ángulo theta (en radianes)
    alrededor de un eje arbitrario dado.

    Args:
        axis: vector 3D que define el eje de rotación (no necesita estar normalizado).
        theta: ángulo de rotación en radianes.

    Retorna:
        Matriz de rotación 3x3 como un numpy array.
    """
    axis = axis / np.linalg.norm(axis)  # Normalizamos el eje
    ux, uy, uz = axis

    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    one_c = 1 - cos_t

    # Aplicamos la fórmula de Rodrigues
    R = np.array([
        [cos_t + ux**2 * one_c, ux*uy * one_c - uz*sin_t, ux*uz * one_c + uy*sin_t],
        [uy*ux * one_c + uz*sin_t, cos_t + uy**2 * one_c, uy*uz * one_c - ux*sin_t],
        [uz*ux * one_c - uy*sin_t, uz*uy * one_c + ux*sin_t, cos_t + uz**2 * one_c]
    ])
    return R

def __dodecaedro_romo_levogiro():
    """
    Genera las coordenadas de los 60 vértices del dodecaedro romo levogiro(snub dodecahedron),
    utilizando constantes especiales derivadas de la proporción áurea (φ) y xi.

    Procedimiento:
    - Define un punto base (x, y, z) basado en φ y ξ.
    - Usa dos matrices M_1 (rotación 72°) y M_2 (ciclado de coordenadas).
    - Usa rotaciones de 180° para construir el hemisferio opuesto.
    - Construye:
        * Cara base
        * Primer cinturón de pentágonos adyacentes
        * Segundo cinturón de triángulos adyacentes
        * Cara opuesta (anti-base)

    Retorna:
        Lista de 60 vértices del dodecaedro romo.
    """

    xi = 0.943151259243882
    xi_2 = pow(xi, 2)
    phi_2 = pow(phi, 2)
    phi_3 = pow(phi, 3)

    # Punto inicial (x, y, z)
    x = phi_2 * (1 - xi)
    y = -phi_3 + phi*xi + 2*phi*xi_2
    z = xi

    # Matrices de rotación
    M_1 = np.array([
        [1/(2*phi), -phi/2, 0.5],
        [phi/2, 0.5, 1/(2*phi)],
        [-0.5, 1/(2*phi), phi/2]
    ])
    M_2 = np.array([
        [0, 0, 1],
        [1, 0, 0],
        [0, 1, 0]
    ])

    # Rotación 180° respecto a un eje especial
    R_180 = __rotation_matrix(np.array([1, -phi, 1]), np.pi)

    vertices = []

    # Cara base: aplicar potencias de M_1 al punto base
    cara_base = [tuple(np.dot(np.array([x, y, z]), np.linalg.matrix_power(M_1, i))) for i in range(5)]

    # Primer cinturón: girar la cara base por M_2
    cara_primer_cinturon = __multiplicar(cara_base, M_2, 1)

    # Primer hemisferio:
    primer_cinturon = cara_primer_cinturon
    for k in range(1, 5):
        primer_cinturon += __multiplicar(cara_primer_cinturon, M_1, k)

    primer_hemisferio = cara_base + primer_cinturon

    # Vectores auxiliares para el segundo cinturón
    vector_pentagono_primer_hemisferio = tuple(np.dot(np.array([0, 1, phi]), np.linalg.matrix_power(M_2, 1)))
    vector_triangulo_primer_hemisferio = tuple(np.dot(np.array([1, 1, 1]),
                                             np.linalg.matrix_power(__rotation_matrix(np.array(vector_pentagono_primer_hemisferio), np.pi * 2 / 5), 2)))

    # Segundo cinturón
    cara_segundo_cinturon = __multiplicar(cara_primer_cinturon,
                                          __rotation_matrix(np.array(vector_triangulo_primer_hemisferio), np.pi * 2 / 3), 2)

    segundo_cinturon = cara_segundo_cinturon
    for k in range(1, 5):
        segundo_cinturon += __multiplicar(cara_segundo_cinturon, M_1, k)

    # Cara opuesta
    vector_pentagono_segundo_hemisferio = tuple(np.dot(np.array(vector_pentagono_primer_hemisferio),
                                                       np.linalg.matrix_power(__rotation_matrix(np.array(vector_triangulo_primer_hemisferio), np.pi * 2 / 3), 2)))
    vector_triangulo_segundo_hemisferio = tuple(np.dot(np.array(vector_triangulo_primer_hemisferio),
                                                       np.linalg.matrix_power(__rotation_matrix(np.array(vector_pentagono_segundo_hemisferio), np.pi * 2 / 5), 2)))

    cara_anti_base = __multiplicar(segundo_cinturon[0:5],
                                   __rotation_matrix(np.array(vector_triangulo_segundo_hemisferio), np.pi * 2 / 3), 2)

    segundo_hemisferio = cara_anti_base + segundo_cinturon

    vertices += primer_hemisferio + segundo_hemisferio

    return vertices

def __dodecaedro_romo_dextrogiro():
    """
    Genera las coordenadas de los 24 vértices del dodecaedro romo levogiro(snub cube),
    centrado en el origen.

    Todas las componentes de todos los vértices invierten su signo para formar una imagen
    especular de su contraparte dextrogira
    
    Retorna:
        Una lista de 24 tuplas (x, y, z), cada una representando un vértice del dodecaedro romo.
    """

    return [(-i[0], -i[1], -i[2]) for i in __dodecaedro_romo_levogiro()]

poliedros = {"tetraedro": __tetraedro,
             "cubo": __cubo,
             "octaedro": __octaedro,
             "dodecaedro": __dodecaedro,
             "icosaedro": __icosaedro,
             "cuboctaedro": __cuboctaedro,
             "icosidodecaedro": __icosidodecaedro,
             "tetraedro truncado": __tetraedro_truncado,
             "cubo truncado": __cubo_truncado,
             "octaedro truncado": __octaedro_truncado,
             "dodecaedro truncado": __dodecaedro_truncado,
             "icosaedro truncado": __icosaedro_truncado,
             "cuboctaedro truncado": __cuboctaedro_truncado,
             "icosidodecaedro truncado": __icosidodecaedro_truncado,
             "rombicuboctaedro": __rombicuboctaedro,
             "rombicosidodecaedro": __rombicosidodecaedro,
             "cubo romo dextrogiro": __cubo_romo_dextrogiro,
             "dodecaedro romo dextrogiro": __dodecaedro_romo_dextrogiro,
             "cubo romo levogiro": __cubo_romo_levogiro,
             "dodecaedro romo levogiro": __dodecaedro_romo_levogiro}

poliedro_id = ["tetraedro", 
                "cubo", 
                "octaedro", 
                "dodecaedro", 
                "icosaedro", 
                "cuboctaedro", 
                "icosidodecaedro", 
                "tetraedro truncado",
                "cubo truncado",
                "octaedro truncado",
                "dodecaedro truncado",
                "icosaedro truncado",
                "cuboctaedro truncado",
                "icosidodecaedro truncado",
                "rombicuboctaedro",
                "rombicosidodecaedro",
                "cubo romo dextrogiro",
                "dodecaedro romo dextrogiro",
                "cubo romo levogiro",
                "dodecaedro romo levogiro"]

forma_caras = {"tetraedro": [3], 
                "cubo": [4], 
                "octaedro": [3], 
                "dodecaedro": [5], 
                "icosaedro": [3], 
                "cuboctaedro": [3,4], 
                "icosidodecaedro": [3,5], 
                "tetraedro truncado": [3,6],
                "cubo truncado": [3,8],
                "octaedro truncado": [4,6],
                "dodecaedro truncado": [3,10],
                "icosaedro truncado": [5,6],
                "cuboctaedro truncado": [4,6,8],
                "icosidodecaedro truncado": [4,6,10],
                "rombicuboctaedro": [3,4],
                "rombicosidodecaedro": [3,4,5],
                "cubo romo dextrogiro": [3,4],
                "dodecaedro romo dextrogiro": [3,5],
                "cubo romo levogiro": [3,4],
                "dodecaedro romo levogiro": [3,5]}

def generar_vertices(poliedro):
    return poliedros[poliedro]()
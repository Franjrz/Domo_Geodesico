from math import pow, sqrt
from scipy.constants import golden as phi

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

def __cubo_romo():
    """
    Genera las coordenadas de los 24 vértices del cubo romo (snub cube),
    centrado en el origen, usando la constante tribonacci.

    Estructura general:
    - Se utilizan combinaciones de ±1, ±tribonacci y ±(1/tribonacci).
    - Se generan 3 bloques de 8 vértices cada uno, permutando el orden
      de los valores en las coordenadas (x, y, z).
    - Los signos se alternan sistemáticamente para asegurar la simetría.

    Retorna:
        Lista de 24 tuplas (x, y, z) representando los vértices del cubo romo.
    """

    # Definimos las constantes: tribonacci y su inverso
    t = 1.839286755214161    # Aproximación de la constante tribonacci
    t_1 = 1 / t     # Inverso de la tribonacci

    # Inicializamos la lista de vértices
    vertices = []

    vertices += [
        v for s1, s2, s3 in [(1, 1, 1), (-1, -1, 1), (-1, 1, -1), (1, -1, -1)]
        for v in [(s1, s2 * t, s3 * t_1), (s1 * t, s2 * t_1, s3), (s1 * t_1, s2, s3 * t)]
    ]


    vertices += [
        v for s1, s2, s3 in [(-1, 1, 1), (1, -1, 1), (1, 1, -1), (-1, -1, -1)]
        for v in [(s1, s2 * t_1, s3 * t), (s1 * t, s2, s3 * t_1), (s1 * t_1, s2 * t, s3)]
    ]

    # Devolvemos los 24 vértices generados
    return vertices



def __dodecaedro_romo():
    phi_2 = phi/2
    phi_1_2 = 1 / (2*phi)
    vertices = []

    vertices += [(pow(-1,int(i)), 0, 0) for i in range(2)]
    vertices += [(0, pow(-1,int(i)), 0) for i in range(2)]
    vertices += [(0, 0, pow(-1,int(i))) for i in range(2)]

    vertices += [(phi_2 * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), 0.5 * pow(-1,i)) for i in range(8)]
    vertices += [(phi_1_2 * pow(-1,int(i/4)), 0.5 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices += [(0.5 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]

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

    # Octavo grupo de 4 vértices: (0, ±2φ, ±(2+φ))
    vertices += [(0, phi___2 * pow(-1, int(i/2)), phi_2 * pow(-1, i)) for i in range(4)]

    # Noveno grupo de 4 vértices: (±2φ, ±(2+φ), 0)
    vertices += [(phi___2 * pow(-1, int(i/2)), phi_2 * pow(-1, i), 0) for i in range(4)]

    # Devolvemos los 60 vértices generados
    return vertices

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
             "cubo romo": __cubo_romo, # ARREGLAR
             "dodecaedro romo": __dodecaedro_romo, # ARREGLAR
             "rombicuboctaedro": __rombicuboctaedro,
             "rombicosidodecaedro": __rombicosidodecaedro}

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
                "cubo romo",
                "dodecaedro romo",
                "rombicuboctaedro",
                "rombicosidodecaedro"]

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
                "cubo romo": [3,4],
                "dodecaedro romo": [3,5],
                "rombicuboctaedro": [3,4],
                "rombicosidodecaedro": [3,4,5]}

def generar_vertices(poliedro):
    return poliedros[poliedro]()
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from math import pow, sqrt
from scipy.constants import golden as phi
from sympy import S, N

def __plot_coordenadas(coordenadas):
    # Convertimos la lista de tuplas a arrays de NumPy para cada dimensión
    x = [punto[0] for punto in coordenadas]
    y = [punto[1] for punto in coordenadas]
    z = [punto[2] for punto in coordenadas]

    # Calculamos los valores máximos y mínimos para cada eje
    x_min, x_max = min(x), max(x)
    y_min, y_max = min(y), max(y)
    z_min, z_max = min(z), max(z)
    
    # Calculamos el rango más grande entre los tres ejes
    x_range = x_max - x_min
    y_range = y_max - y_min
    z_range = z_max - z_min
    max_range = max(x_range, y_range, z_range)
    
    # Calculamos el centro de cada eje
    x_center = (x_max + x_min) / 2
    y_center = (y_max + y_min) / 2
    z_center = (z_max + z_min) / 2
    
    # Añadimos un pequeño margen para mejor visualización (20% extra)
    margin = max_range * 0.2
    
    # Creamos la figura y el eje 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Graficamos los puntos
    ax.scatter(x, y, z, color='blue', s=100, marker='o')

    # Configuramos el gráfico
    ax.set_box_aspect([1, 1, 1])
    ax.set_xlabel('Eje X')
    ax.set_ylabel('Eje Y')
    ax.set_zlabel('Eje Z')
    ax.set_title('Gráfico 3D de Puntos')

    # Establecemos límites dinámicos basados en los datos
    ax.set_xlim(x_center - (max_range/2 + margin), x_center + (max_range/2 + margin))
    ax.set_ylim(y_center - (max_range/2 + margin), y_center + (max_range/2 + margin))
    ax.set_zlim(z_center - (max_range/2 + margin), z_center + (max_range/2 + margin))

    # Ajustamos el ángulo de visión
    ax.view_init(elev=20, azim=30)

    # Añadimos una cuadrícula
    ax.grid(True)

    plt.tight_layout()
    plt.show()

def __tetraedro():
    return [(pow(-1,int((i+1)/2)), pow(-1,i), pow(-1,int(i/2))) for i in range(4)]

def __cubo():
    return [tuple(pow(-1, int(i/pow(2,j))) for j in range(3)) for i in range(8)]

def __octaedro():
    return [tuple(s if i == d else 0 for i in range(3)) for d in range(3) for s in [1, -1]]

def __dodecaedro():
    phi_2 = pow(phi, 2)
    vertices_1 = [tuple(v[(p+j)%3] for j in range(3)) for p in range(3) for i in range(4) for v in [(0, pow(-1, int(i/2)), (phi + 1) * pow(-1, i))]]
    vertices_2 = [(phi * pow(-1, int(i/4)), phi * pow(-1, int(i/2)), phi * pow(-1, int(i))) for i in range(8)]
    vertices = vertices_1 + vertices_2
    return vertices

def __icosaedro():
    return [tuple(v[(p+j)%3] for j in range(3)) for p in range(3) for i in range(4) for v in [(0, pow(-1, int(i/2)), phi * pow(-1, i))]]

def __tetraedro_truncado():
    return [tuple(a * b for a, b in zip(sign, [sqrt(2)/4 * (3 if j == i else 1) for j in range(3)])) for i in range(3) for sign in [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]]

def __cubo_truncado():
    aux = 1 + sqrt(2)
    vertices_1 = [(pow(-1,int(i/4)), aux * pow(-1,int(i/2)), aux * pow(-1,i)) for i in range(8)]
    vertices_2 = [(aux * pow(-1,int(i/4)), pow(-1,int(i/2)), aux * pow(-1,i)) for i in range(8)]
    vertices_3 = [(aux * pow(-1,int(i/4)), aux * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices = vertices_1 + vertices_2 + vertices_3

    return vertices

def __octaedro_truncado():
    sqrt_2 = sqrt(2)
    sqrt_2_2 = sqrt_2/2

    vertices_1 = [(sqrt_2 * pow(-1,int(i/2)), sqrt_2_2 * pow(-1,i), 0) for i in range(4)]
    vertices_2 = [(sqrt_2_2 * pow(-1,i), 0, sqrt_2 * pow(-1,int(i/2))) for i in range(4)]
    vertices_3 = [(0, sqrt_2 * pow(-1,int(i/2)), sqrt_2_2 * pow(-1,i)) for i in range(4)]
    vertices_4 = [(sqrt_2_2 * pow(-1,int(i/2)), sqrt_2 * pow(-1,i), 0) for i in range(4)]
    vertices_5 = [(sqrt_2 * pow(-1,i), 0, sqrt_2_2 * pow(-1,int(i/2))) for i in range(4)]
    vertices_6 = [(0, sqrt_2_2 * pow(-1,int(i/2)), sqrt_2 * pow(-1,i)) for i in range(4)]

    vertices = vertices_1 + vertices_2 + vertices_3 + vertices_4 + vertices_5 + vertices_6

    return vertices

def __dodecaedro_truncado():
    inv_phi = 1/phi
    phi_1 = phi + 1
    phi_2 = phi + 2
    phi__2 = 2 * phi

    vertices_1 = [(0, inv_phi * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(4)]
    vertices_2 = [(inv_phi * pow(-1,int(i/2)), phi_2 * pow(-1,i), 0) for i in range(4)]
    vertices_3 = [(phi_2 * pow(-1,int(i/2)), 0, inv_phi * pow(-1,i)) for i in range(4)]
    
    vertices_4 = [(inv_phi * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi__2 * pow(-1,int(i/4)), inv_phi * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), inv_phi * pow(-1,i)) for i in range(8)]
    
    vertices_7 = [(phi * pow(-1,int(i/4)), 2 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]
    vertices_8 = [(phi_1 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), 2 * pow(-1,i)) for i in range(8)]
    vertices_9 = [(2 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
            vertices_7 + vertices_8 + vertices_9

    return vertices

def __icosaedro_truncado():
    phi_2 = phi + 2
    phi__3 = 3 * phi
    phi__2 = 2 * phi
    phi_2_1 = 2*phi + 1

    vertices_1 = [(0, pow(-1,int(i/2)), phi__3 * pow(-1,i)) for i in range(4)]
    vertices_2 = [(pow(-1,int(i/2)), phi__3 * pow(-1,i), 0) for i in range(4)]
    vertices_3 = [(phi__3 * pow(-1,int(i/2)), 0, pow(-1,i)) for i in range(4)]

    vertices_4 = [(pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi_2 * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi__2 * pow(-1,int(i/4)), pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]

    vertices_7 = [(phi * pow(-1,int(i/4)), 2 * pow(-1,int(i/2)), phi_2_1 * pow(-1,i)) for i in range(8)]
    vertices_8 = [(2 * pow(-1,int(i/4)), phi_2_1 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    vertices_9 = [(phi_2_1 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), 2 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
            vertices_7 + vertices_8 + vertices_9

    return vertices

def __cuboctaedro():
    return [(0 if j == 0 else [-1, 1][i//2], 0 if j == 1 else [-1, 1][i%2], 0 if j == 2 else [-1, 1][(i//2+i%2)%2]) for j in range(3) for i in range(4)]

def __cuboctaedro_truncado():
    sqrt_2_1 = 1 + sqrt(2)
    sqrt_2_2_1 = 1 + 2*sqrt(2)

    vertices_1 = [(pow(-1,int(i/4)), sqrt_2_1 * pow(-1,int(i/2)), sqrt_2_2_1 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(sqrt_2_1 * pow(-1,int(i/4)), sqrt_2_2_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_3 = [(sqrt_2_2_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), sqrt_2_1 * pow(-1,i)) for i in range(8)]
    vertices_4 = [(sqrt_2_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), sqrt_2_2_1 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(pow(-1,int(i/4)), sqrt_2_2_1 * pow(-1,int(i/2)), sqrt_2_1 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(sqrt_2_2_1 * pow(-1,int(i/4)), sqrt_2_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6
    return vertices

def __icosidodecaedro():
    phi_2 = phi/2
    phi_1_2 = 1 / (2*phi)

    vertices_1 = [(pow(-1,int(i)), 0, 0) for i in range(2)]
    vertices_2 = [(0, pow(-1,int(i)), 0) for i in range(2)]
    vertices_3 = [(0, 0, pow(-1,int(i))) for i in range(2)]

    vertices_4 = [(phi_2 * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), 0.5 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi_1_2 * pow(-1,int(i/4)), 0.5 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(0.5 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6

    return vertices

def __icosidodecaedro_truncado():
    phi_1 = 1 / phi
    phi_2 = 2 / phi
    phi___2 = 2 * phi
    phi__1 = 1 + phi
    phi__2 = 2 + phi
    phi__3 = 3 + phi
    phi_1_2 = 1 + 2*phi
    phi__1_2 = 2*phi - 1
    phi__1_3 = -1 + 3*phi

    vertices_1 = [(phi_1 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi__3 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(phi_1 * pow(-1,int(i/4)), phi__3 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]
    vertices_3 = [(phi__3 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]

    vertices_4 = [(phi_2 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi_1_2 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    
    vertices_7 = [(phi_1 * pow(-1,int(i/4)), phi__1 * pow(-1,int(i/2)), phi__1_3 * pow(-1,i)) for i in range(8)]
    vertices_8 = [(phi__1 * pow(-1,int(i/4)), phi__1_3 * pow(-1,int(i/2)), phi_1 * pow(-1,i)) for i in range(8)]
    vertices_9 = [(phi__1_3 * pow(-1,int(i/4)), phi_1 * pow(-1,int(i/2)), phi__1 * pow(-1,i)) for i in range(8)]
    
    vertices_10 = [(phi__1_2 * pow(-1,int(i/4)), 2 * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_11 = [(2 * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), phi__1_2 * pow(-1,i)) for i in range(8)]
    vertices_12 = [(phi__2 * pow(-1,int(i/4)), phi__1_2 * pow(-1,int(i/2)), 2 * pow(-1,i)) for i in range(8)]
    
    vertices_13 = [(phi * pow(-1,int(i/4)), 3 * pow(-1,int(i/2)), phi___2 * pow(-1,i)) for i in range(8)]
    vertices_14 = [(3 * pow(-1,int(i/4)), phi___2 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]
    vertices_15 = [(phi___2 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), 3 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
        vertices_7 + vertices_8 + vertices_9 + \
        vertices_10 + vertices_11 + vertices_12 + \
        vertices_13 + vertices_14 + vertices_15
    return vertices

def __cubo_romo():
    tribonacci = 1.839286755214161
    tribonacci_1 = 1/tribonacci

    vertices_1 = [(pow(-1,int(i/4)), tribonacci * pow(-1,int(i/2)), tribonacci_1 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(tribonacci_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), tribonacci * pow(-1,i)) for i in range(8)]
    vertices_3 = [(tribonacci * pow(-1,int(i/4)), tribonacci_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3
    return vertices

def __dodecaedro_romo():
    phi_2 = phi/2
    phi_1_2 = 1 / (2*phi)

    vertices_1 = [(pow(-1,int(i)), 0, 0) for i in range(2)]
    vertices_2 = [(0, pow(-1,int(i)), 0) for i in range(2)]
    vertices_3 = [(0, 0, pow(-1,int(i))) for i in range(2)]

    vertices_4 = [(phi_2 * pow(-1,int(i/4)), phi_1_2 * pow(-1,int(i/2)), 0.5 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi_1_2 * pow(-1,int(i/4)), 0.5 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(0.5 * pow(-1,int(i/4)), phi_2 * pow(-1,int(i/2)), phi_1_2 * pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6

    return vertices

def __rombicuboctaedro():
    sqrt_2_1 = 1 + sqrt(2)

    vertices_1 = [(sqrt_2_1 * pow(-1,int(i/4)), pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_2 = [(pow(-1,int(i/4)), pow(-1,int(i/2)), sqrt_2_1 * pow(-1,i)) for i in range(8)]
    vertices_3 = [(pow(-1,int(i/4)), sqrt_2_1 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices = vertices_1 + vertices_2 + vertices_3
    return vertices

def __rombicosidodecaedro():
    phi__2 = pow(phi,2)
    phi__3 = pow(phi,3)
    phi___2 = 2*phi
    phi_2 = 2 + phi

    vertices_1 = [(pow(-1,int(i/4)), pow(-1,int(i/2)), phi__3 * pow(-1,i)) for i in range(8)]
    vertices_2 = [(pow(-1,int(i/4)), phi__3 * pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]
    vertices_3 = [(phi__3 * pow(-1,int(i/4)), pow(-1,int(i/2)), pow(-1,i)) for i in range(8)]

    vertices_4 = [(phi__2 * pow(-1,int(i/4)), phi * pow(-1,int(i/2)), phi___2 * pow(-1,i)) for i in range(8)]
    vertices_5 = [(phi * pow(-1,int(i/4)), phi___2 * pow(-1,int(i/2)), phi__2 * pow(-1,i)) for i in range(8)]
    vertices_6 = [(phi___2 * pow(-1,int(i/4)), phi__2 * pow(-1,int(i/2)), phi * pow(-1,i)) for i in range(8)]

    vertices_7 = [(phi_2 * pow(-1,int(i/2)), 0, phi__2 * pow(-1,i)) for i in range(4)]
    vertices_8 = [(0, phi___2 * pow(-1,int(i/2)), phi_2 * pow(-1,i)) for i in range(4)]
    vertices_9 = [(phi___2 * pow(-1,int(i/2)), phi_2 * pow(-1,i), 0) for i in range(4)]

    vertices = vertices_1 + vertices_2 + vertices_3 + \
        vertices_4 + vertices_5 + vertices_6 + \
        vertices_7 + vertices_8 + vertices_9

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

def generar_vertices(poliedro):
    return poliedros[poliedro]()

#__plot_coordenadas(generar_vertices("tetraedro"))
#__plot_coordenadas(generar_vertices("cubo"))
#__plot_coordenadas(generar_vertices("octaedro"))
#__plot_coordenadas(generar_vertices("dodecaedro"))
#__plot_coordenadas(generar_vertices("icosaedro"))
#__plot_coordenadas(generar_vertices("cuboctaedro"))
#__plot_coordenadas(generar_vertices("icosidodecaedro"))
#__plot_coordenadas(generar_vertices("tetraedro truncado"))
#__plot_coordenadas(generar_vertices("cubo truncado"))
#__plot_coordenadas(generar_vertices("octaedro truncado"))
#__plot_coordenadas(generar_vertices("dodecaedro truncado"))
#__plot_coordenadas(generar_vertices("icosaedro truncado"))
#__plot_coordenadas(generar_vertices("cuboctaedro truncado"))
__plot_coordenadas(generar_vertices("icosidodecaedro truncado"))
#__plot_coordenadas(generar_vertices("cubo romo"))
#__plot_coordenadas(generar_vertices("dodecaedro romo"))
#__plot_coordenadas(generar_vertices("rombicuboctaedro"))
#__plot_coordenadas(generar_vertices("rombicosidodecaedro"))

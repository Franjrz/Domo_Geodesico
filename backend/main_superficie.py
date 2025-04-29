from superficie.fronteras import *
from superficie.superficies import *

"""def dibujar_forma(funcion_forma, limites=[-2,2,-2,2], resolucion=500):
    x = np.linspace(limites[0], limites[1], resolucion)
    y = np.linspace(limites[2], limites[3], resolucion)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(funcion_forma)(X, Y)

    plt.figure(figsize=(6,6))
    plt.contourf(X, Y, Z, levels=[0.5, 1], colors=['#3399FF'])
    plt.gca().set_aspect('equal')
    plt.title("Forma generada")
    plt.show()

dibujar_forma(lambda x, y: circulo(x, y, r=1))
#dibujar_forma(lambda x, y: triangulo_reuleaux(x, y, r=1))
#dibujar_forma(lambda x, y: hexagono(x, y, r=1))
#dibujar_forma(lambda x, y: elipse(x, y, a=1.5, b=1))"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

"""def dibujar_superficie(funcion_superficie, limites=[-2, 2, -2, 2], resolucion=100):

    x = np.linspace(limites[0], limites[1], resolucion)
    y = np.linspace(limites[2], limites[3], resolucion)
    X, Y = np.meshgrid(x, y)
    Z = np.vectorize(funcion_superficie)(X, Y)

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Superficie 3D')
    plt.show()

dibujar_superficie(paraboloide)
dibujar_superficie(silla_de_montar)
dibujar_superficie(onda_seno_coseno)
dibujar_superficie(campana_gaussiana)"""

import numpy as np
import matplotlib.pyplot as plt

def simular_repulsion_2d(num_puntos=20, iteraciones=100, paso=0.01, fuerza=1.0, graficar=True):
    """
    Simula puntos en 2D que se repelen entre sí.

    Parámetros:
    - num_puntos: número de puntos
    - iteraciones: número de iteraciones de la simulación
    - paso: cuánto se mueven los puntos en cada iteración
    - fuerza: magnitud base de la repulsión
    - graficar: si True, dibuja el estado final

    Retorna:
        Un array (num_puntos, 2) con las posiciones finales.
    """
    # Inicializar posiciones aleatorias en [-1, 1] x [-1, 1]
    posiciones = np.random.uniform(-1, 1, (num_puntos, 2))

    for _ in range(iteraciones):
        fuerzas = np.zeros_like(posiciones)

        # Calcular fuerzas entre todos los pares
        for i in range(num_puntos):
            for j in range(i+1, num_puntos):
                delta = posiciones[i] - posiciones[j]
                distancia = np.linalg.norm(delta) + 1e-5  # evitar división por cero
                repulsion = fuerza * delta / distancia**3  # fuerza ~ inversa al cuadrado

                fuerzas[i] += repulsion
                fuerzas[j] -= repulsion

        # Actualizar posiciones
        posiciones += paso * fuerzas

    if graficar:
        plt.figure(figsize=(6,6))
        plt.scatter(posiciones[:,0], posiciones[:,1], color='blue')
        plt.title("Puntos tras repulsión")
        plt.gca().set_aspect('equal')
        plt.grid(True)
        plt.show()

    return posiciones

simular_repulsion_2d(num_puntos=30, iteraciones=200, paso=0.01, fuerza=1.5)

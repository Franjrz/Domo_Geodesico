from utils import *
from graficos import *
from fusion_triangulos import *
from auxiliar import *

if __name__ == "__main__":
    frecuencia = 3
    lados = 5
    puntos, vertices, aristas = fusionar_triangulos_base_punto_medio(frecuencia, lados)
    """    
    triangulo_inicial = [(0, 0), (1, 0), (0.5, 0.866)]  # Triángulo equilátero
    
    # Número de niveles de subdivisión
    n = 5
    
    # Realizar la triangulación
    puntos, vertices, aristas = triangulacion_iterativa(triangulo_inicial, n)
    print(aristas)
    
    """
    print("\npuntos: ")
    for i, it in puntos.items():
        print(i, it)

    print("vertices: " + str(vertices))
        
    print("aristas: ")
    for i, it in aristas.items():
        print(i, it)
    visualizar_cara_final(puntos, vertices, aristas)
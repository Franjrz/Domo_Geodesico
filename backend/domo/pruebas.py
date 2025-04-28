from graficos import *
from fusion_triangulos import *

if __name__ == "__main__":
    frecuencia = 2
    lados = 5
    tipo = 2
    puntos, vertices, aristas = fusionar_triangulos_base(frecuencia, lados, tipo)
    visualizar_cara_final(puntos, vertices, aristas)
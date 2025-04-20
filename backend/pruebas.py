from utils import *
from graficos import *
from fusion_triangulos import *

if __name__ == "__main__":
    frecuencia = 11
    lados = 7
    puntos, vertices, aristas = fusionar_triangulos_base_alternado(frecuencia, lados)
    visualizar_cara_final(puntos, vertices, aristas)
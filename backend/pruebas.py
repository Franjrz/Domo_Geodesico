from utils import *
from graficos import *
from fusion_triangulos import *
#from auxiliar import *

if __name__ == "__main__":
    frecuencia = 2
    lados = 5
    tipo = 2
    puntos, vertices, aristas = fusionar_triangulos_base(frecuencia, lados, tipo)
    """    
    print()
    print()
    print()
    for i in aristas:
        print(i, aristas[i])
        """
    visualizar_cara_final(puntos, vertices, aristas)
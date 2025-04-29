from domo.poliedro import *
from domo.domo import *
# Ejemplo de uso:

"""
0: "tetraedro", 
1: "cubo", 
2: "octaedro", 
3: "dodecaedro", 
4: "icosaedro", 
5: "cuboctaedro", 
6: "icosidodecaedro", 
7: "tetraedro truncado",
8: "cubo truncado",
9: "octaedro truncado",
10: "dodecaedro truncado",
11: "icosaedro truncado",
12: "cuboctaedro truncado",
13: "icosidodecaedro truncado",
14: "cubo romo",
15: "dodecaedro romo",
16: "rombicuboctaedro",
17: "rombicosidodecaedro"
"""

if __name__ == "__main__":
    # Probar de 0 a 13. 14, 15 y 17 tienen bugs
    poliedro_semilla = poliedro_id[14]
    frecuencia = 6
    tipo = 0
    radio = 4
    poliedro = Poliedro(poliedro_semilla, radio)
    poliedro.dibujar()
    #domo = Domo(poliedro_semilla, frecuencia, tipo, radio)
    #domo.dibujar()
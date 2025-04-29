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
14: "rombicuboctaedro",
15: "rombicosidodecaedro",
16: "cubo romo dextrogiro",
17: "dodecaedro romo dextrogiro",
18: "cubo romo levogiro",
19: "dodecaedro romo levogiro"
"""

if __name__ == "__main__":
    poliedro_semilla = poliedro_id[17]
    frecuencia = 2
    tipo = 0
    radio = 4
    poliedro = Poliedro(poliedro_semilla, radio)
    poliedro.dibujar()
    #domo = Domo(poliedro_semilla, frecuencia, tipo, radio)
    #domo.dibujar()
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

particion = ["alternado","punto_medio","triacon"]

def generar_nombre_archivo(c, semilla, tipo, frecuencia):
    semilla_def = "_".join(p.capitalize() for p in semilla.split())
    return f"{c}_{semilla_def}_{particion[tipo]}_frecuencia_{frecuencia}.gif"

if __name__ == "__main__":
    # poliedro_semilla = poliedro_id[0]
    # frecuencia = 6
    # tipo = 0
    # radio = 4
    # #bug para tipo 2 en combinar nodos
    # domo = Domo(poliedro_semilla, frecuencia, tipo, radio)
    # #domo.dibujar()
    # domo.generar_video_rotacion()
    c = 0
    for i in range(20):
        semilla = poliedro_id[i]
        tipo = 0
        for frecuencia in range(2, 7):
            domo = Domo(semilla, frecuencia, tipo, 4)
            domo.generar_video_rotacion(nombre_salida=generar_nombre_archivo(c, semilla, tipo, frecuencia))
            c+=1
        tipo = 1
        for frecuencia in [2, 3]:
            domo = Domo(semilla, frecuencia, tipo, 4)
            domo.generar_video_rotacion(nombre_salida=generar_nombre_archivo(c, semilla, tipo, frecuencia))
            c+=1
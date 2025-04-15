import math
import matplotlib.pyplot as plt
import numpy as np
import json

def generar_malla_triangular(v):
    factor_x = 1/(2*v)
    factor_y = factor_x * math.sqrt(3)
    triangulo = {i:{j:(factor_x * (i + 2*j), factor_y * i) for j in range(v+1-i)} for i in range(v+1)}
    return triangulo

def generar_malla_cuadrada(v):
    return {i:{j:(i/v, j/v) for j in range(v+1)} for i in range(v+1)}

def generar_malla_pentagonal(v):
    pass

def generar_malla_cuadrada_triangular(v):
    return generar_malla_ngonal_triangular(v, 0.5, 4)

def generar_malla_pentagonal_triangular(v):
    return generar_malla_ngonal_triangular(v, 0.5*math.sqrt(1+2/math.sqrt(5)), 5)

def generar_malla_ngonal_triangular(v, apotema, n):
    angulo = 360/n
    base = escalar_triangulo(generar_malla_triangular(v), apotema)
    punto_referencia = base[v][0]
    triangulos = [rotar_triangulo(base, angulo*i, punto_referencia) for i in list(range(n))]
    return fusionar_triangulos(triangulos)

def escalar_triangulo(triangulo, apotema):
    apotema_triangulo_inverso = 2/math.sqrt(3)
    return {i:{j:(triangulo[i][j][0], triangulo[i][j][1]*apotema*apotema_triangulo_inverso) for j in triangulo[i].keys()} for i in triangulo.keys()}

def rotar_punto(punto, angulo, punto_referencia):
    x, y = punto
    x_0, y_0 = punto_referencia
    angulo_radianes = math.radians(angulo)
    sen = math.sin(angulo_radianes)
    cos = math.cos(angulo_radianes)
    x_p = round(cos*(x-x_0) - sen*(y-y_0) + x_0, 15)
    y_p = round(sen*(x-x_0) + cos*(y-y_0) + y_0, 15)
    return (x_p, y_p)

def rotar_triangulo(triangulo, angulo, punto_referencia):
    return {i:{j:rotar_punto(triangulo[i][j], angulo, punto_referencia) for j in triangulo[i].keys()} for i in triangulo.keys()}

def dibujar_puntos(diccionario):
    # Crear una figura y un conjunto de ejes
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Extraer las coordenadas x e y de todos los puntos
    x_coords = []
    y_coords = []
    etiquetas = []
    
    # Recorrer el diccionario de diccionarios
    for clave_externa, dic_interno in diccionario.items():
        for clave_interna, coordenadas in dic_interno.items():
            x, y = coordenadas
            x_coords.append(x)
            y_coords.append(y)
            etiquetas.append(f"({clave_externa},{clave_interna})")
    
    # Graficar los puntos
    ax.scatter(x_coords, y_coords, color='blue', s=50)
    
    # Configurar los ejes
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Visualización de Puntos 2D')
    ax.grid(True)
    
    # Para que los ejes tengan la misma escala
    ax.set_aspect('equal')
    
    # Mostrar el gráfico
    plt.tight_layout()
    plt.show()
    
def fusionar_puntos_triangulos(triangulos):
  elementos = []
  for diccionario in triangulos:
    for subdiccionario in diccionario.values():
      for punto in subdiccionario.values():
          elementos.append(punto)
  elementos = list(set(elementos))
  return elementos

def reconstruir_malla(elementos):
  nuevo_diccionario = {}
  for elemento in elementos:
    if elemento[1] not in nuevo_diccionario.keys():
      nuevo_diccionario[elemento[1]] = {}
    nuevo_diccionario[elemento[1]][elemento[0]] = {elemento}
  return nuevo_diccionario

def renombrar_claves(keys):
  return {numero: indice for indice, numero in enumerate(sorted(list(keys)))}

def renonmbrar_claves_diccionario(diccionario, diccionario_claves):
  nuevo_diccionario = {}
  for i, i_value in diccionario_claves.items():
    nuevo_diccionario[i_value] = list(diccionario[i])[0]
  return nuevo_diccionario

def renombrar_claves_malla(nuevo_diccionario): 
  malla = {} 
  orden_keys_diccionario = renombrar_claves(nuevo_diccionario.keys())
  for i, i_value in orden_keys_diccionario.items():
    orden_keys_subdiccionario = renombrar_claves(nuevo_diccionario[i].keys())
    malla[i_value] = renonmbrar_claves_diccionario(nuevo_diccionario[i], orden_keys_subdiccionario)
  return malla

def fusionar_triangulos(triangulos):
  elementos = fusionar_puntos_triangulos(triangulos)
  nuevo_diccionario = reconstruir_malla(elementos)
  nuevo_diccionario = renombrar_claves_malla(nuevo_diccionario)
  return nuevo_diccionario

dibujar_puntos(generar_malla_pentagonal_triangular(3))
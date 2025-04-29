import numpy as np
import matplotlib.pyplot as plt

# Forma básica: círculo de radio r centrado en (cx, cy)
def circulo(x, y, cx=0, cy=0, r=1):
    return (x - cx)**2 + (y - cy)**2 <= r**2

# Forma básica: elipse de semiejes a, b centrada en (cx, cy)
def elipse(x, y, cx=0, cy=0, a=1, b=1):
    return ((x - cx) / a)**2 + ((y - cy) / b)**2 <= 1

# Triángulo de Reuleaux de radio r
def triangulo_reuleaux(x, y, r=1):
    d1 = np.sqrt((x - 0)**2 + (y - r)**2)
    d2 = np.sqrt((x - (np.sqrt(3)/2)*r)**2 + (y + r/2)**2)
    d3 = np.sqrt((x + (np.sqrt(3)/2)*r)**2 + (y + r/2)**2)
    return d1 <= r and d2 <= r and d3 <= r

# Hexágono regular de radio r
def hexagono(x, y, r=1):
    x_abs = abs(x)
    y_abs = abs(y)
    return (y_abs <= np.sqrt(3) * min(r - x_abs, r)) and (x_abs <= r)

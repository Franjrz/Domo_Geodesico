import numpy as np

def paraboloide(x, y):
    return x**2 + y**2

def silla_de_montar(x, y):
    return x**2 - y**2

def onda_seno_coseno(x, y):
    return np.sin(x) * np.cos(y)
def campana_gaussiana(x, y):
    return np.exp(-(x**2 + y**2))

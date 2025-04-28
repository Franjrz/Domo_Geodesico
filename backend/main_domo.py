from domo.domo import *
# Ejemplo de uso:
if __name__ == "__main__":
    # Probar de 0 a 13. 14, 15 y 17 tienen bugs
    poliedro_semilla = poliedro_id[0]
    frecuencia = 2
    tipo = 0
    radio = 4
    domo = Domo(poliedro_semilla, frecuencia, tipo, radio)
    domo.dibujar()
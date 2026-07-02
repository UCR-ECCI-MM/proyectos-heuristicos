import random
import sys
import os

from src.core.modelos import Solucion


def generar_solucion_aleatoria(instancia, semilla=None):
    """
    Genera una solución inicial válida colocando
    los perros en perreras aleatorias.
    """

    if semilla is not None:
        random.seed(semilla)

    total_perreras = instancia.n * instancia.n
    perreras = list(range(total_perreras))
    random.shuffle(perreras)
    # Seleccionamos las primeras p perreras para colocar los perros
    posiciones = []
    for i in range(instancia.p):
        posiciones.append(perreras[i])

    return Solucion(posiciones)


def vecino_mover(instancia, solucion):
    """
    Genera un vecino moviendo un perro
    a una perrera vacía.
    """

    total_perreras = instancia.n * instancia.n
    # Obtenemos las perreras ocupadas de la solución actual
    perreras_ocupadas = set(solucion.posiciones)

    perreras_vacias = []

    for perrera in range(total_perreras):
        if perrera not in perreras_ocupadas:
            perreras_vacias.append(perrera)

    if len(perreras_vacias) == 0:
        return None

    nuevas_posiciones = solucion.posiciones.copy()

    perro = random.randrange(instancia.p)

    nueva_perrera = random.choice(perreras_vacias)
    # Movemos el perro a la nueva perrera
    nuevas_posiciones[perro] = nueva_perrera
    return Solucion(nuevas_posiciones)


def vecino_intercambio(instancia, solucion):
    """
    Genera un vecino intercambiando
    la posición de dos perros.
    """

    nuevas_posiciones = solucion.posiciones.copy()

    perro1, perro2 = random.sample(range(instancia.p), 2)

    temp = nuevas_posiciones[perro1]
    nuevas_posiciones[perro1] = nuevas_posiciones[perro2]
    nuevas_posiciones[perro2] = temp

    return Solucion(nuevas_posiciones)


def generar_vecino(instancia, solucion):
    """
    Genera un vecino para Simulated Annealing.

    Si existen perreras vacías:
        50% mover
        50% intercambiar

    Si no existen perreras vacías:
        siempre intercambiar.
    """

    total_perreras = instancia.n * instancia.n

    hay_perreras_vacias = len(solucion.posiciones) < total_perreras

    if hay_perreras_vacias:

        if random.random() < 0.5:

            vecino = vecino_mover(instancia, solucion)

            if vecino is not None:
                return vecino

    return vecino_intercambio(instancia, solucion)
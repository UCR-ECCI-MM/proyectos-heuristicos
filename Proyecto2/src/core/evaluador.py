
"""
este archivo contiene la funcion de evaluacion comun del proyecto
la idea es que fuerza bruta heuristica y simulated annealing usen esta misma
"""

def indice_a_posicion(indice, n):
    # Convierte el indice de una perrera en coordenadas de matriz
    
    fila = indice // n
    columna = indice % n
    return fila, columna


def son_adyacentes(pos1, pos2, n):
    # revisa si dos perreras son adyacentes, no cuentan diagonales
    # convertir cada indice a fila y columna
    fila1, columna1 = indice_a_posicion(pos1, n)
    fila2, columna2 = indice_a_posicion(pos2, n)

    # dos posiciones son adyacentes si la distancia manhattan es 1
    distancia_manhattan = abs(fila1 - fila2) + abs(columna1 - columna2)
    return distancia_manhattan == 1


def validar_solucion(instancia, solucion):
    # una solucion valida debe tener una posicion por cada perro
    # no repetir perreras
    # no usar indices fuera de lo permitido

    n = instancia.n
    perros = instancia.perros
    posiciones = solucion.posiciones

    # debe haber una posicion por cada perro
    if len(posiciones) != len(perros):
        return False

    # no pueden existir dos perros en la misma perrera
    if len(set(posiciones)) != len(posiciones):
        return False

    # cada posicion debe estar dentro del rango valido
    for posicion in posiciones:
        if posicion < 0 or posicion > (n * n - 1):
            return False

    return True


def evaluar(instancia, solucion):
    # evaluar solucion y calcular costo

    """
    penalizaciones:
    +10 por cada conflicto macho-macho
    +10 por cada conflicto macho-hembra en celo
    +20 por cada perro enfermo fuera de la primera fila
    """

    n = instancia.n
    perros = instancia.perros
    posiciones = solucion.posiciones

    if not validar_solucion(instancia, solucion):
        return {
            "valida": False,
            "costo": 1000,
            "conflictosMachoMacho": 0,
            "conflictosMachoHembraCelo": 0,
            "enfermosFueraPrimeraFila": 0
        }

    conflictos_macho_macho = 0
    conflictos_macho_hembra_celo = 0
    enfermos_fuera_primera_fila = 0

    # revisa perros enfermos fuera de primera fila
    for i in range(len(perros)):
        perro = perros[i]
        posicion = posiciones[i]

        fila, columna = indice_a_posicion(posicion, n)

        if perro.enfermo and fila != 0:
            enfermos_fuera_primera_fila += 1

    # para adyacencia se comparan parejas de perros
    for i in range(len(perros)):
        for j in range(i + 1, len(perros)):

            perro_i = perros[i]
            perro_j = perros[j]

            pos_i = posiciones[i]
            pos_j = posiciones[j]

            # solo hay conflicto si las perreras son adyacentes
            if son_adyacentes(pos_i, pos_j, n):

                # dos perros machos estan adyacentes
                if perro_i.sexo == "M" and perro_j.sexo == "M":
                    conflictos_macho_macho += 1

                # perro i es macho y perro j es hembra en celo
                if perro_i.sexo == "M" and perro_j.sexo == "H" and perro_j.celo:
                    conflictos_macho_hembra_celo += 1

                # perro j es macho y perro i es hembra en celo
                if perro_j.sexo == "M" and perro_i.sexo == "H" and perro_i.celo:
                    conflictos_macho_hembra_celo += 1

    # calc costo
    costo = (10 * conflictos_macho_macho + 10 * conflictos_macho_hembra_celo + 20 * enfermos_fuera_primera_fila)
    return {
        "valida": True,
        "costo": costo,
        "conflictosMachoMacho": conflictos_macho_macho,
        "conflictosMachoHembraCelo": conflictos_macho_hembra_celo,
        "enfermosFueraPrimeraFila": enfermos_fuera_primera_fila
    }
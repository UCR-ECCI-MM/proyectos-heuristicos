import time
from src.core.modelos import Solucion
from src.core.evaluador import evaluar, son_adyacentes, indice_a_posicion

def es_hembra_en_celo(perro):
    # retorna true si el perro es una hembra en celo
    return perro.sexo == "H" and perro.celo


def obtener_orden_perros(instancia, configuracion="H1"):
    """
    configuraciones:
        H1: enfermos, hembras en celo, machos, otros. Desempate primera mejor perrera encontrada
        H2: enfermos, hembras en celo, machos, otros. Desempate por esquinas, despues bordes y despues centro
        H3: hembras en celo, enfermos, machos, otros
    """
    perros = instancia.perros
    orden = []
    usados = set()

    if configuracion == "H1" or configuracion == "H2":

        # agregar primero los perros enfermos
        # se colocan primero porque tienen la restriccion de ir en la primera fila
        for i in range(len(perros)):
            perro = perros[i]

            if perro.enfermo and i not in usados:
                orden.append(i)
                usados.add(i)

        # hembras en celo
        # afectan donde van los machos
        for i in range(len(perros)):
            perro = perros[i]

            if es_hembra_en_celo(perro) and i not in usados:
                orden.append(i)
                usados.add(i)

        # machos, restricciones con otros machos
        for i in range(len(perros)):
            perro = perros[i]

            if perro.sexo == "M" and i not in usados:
                orden.append(i)
                usados.add(i)

        # otros
        for i in range(len(perros)):
            if i not in usados:
                orden.append(i)
                usados.add(i)

    elif configuracion == "H3":

        # primero prueba las hembras en celo
        for i in range(len(perros)):
            perro = perros[i]

            if es_hembra_en_celo(perro) and i not in usados:
                orden.append(i)
                usados.add(i)

        # enfermos
        for i in range(len(perros)):
            perro = perros[i]

            if perro.enfermo and i not in usados:
                orden.append(i)
                usados.add(i)

        # machos
        for i in range(len(perros)):
            perro = perros[i]

            if perro.sexo == "M" and i not in usados:
                orden.append(i)
                usados.add(i)

        # otros
        for i in range(len(perros)):
            if i not in usados:
                orden.append(i)
                usados.add(i)

    else:
        raise ValueError(f"Configuracion de heuristica no valida: {configuracion}")

    return orden


def obtener_perreras_disponibles(instancia, posiciones_parciales):
    # -1 significa que perro todavia no tiene perrera
    total_perreras = instancia.n * instancia.n
    ocupadas = set()

    for posicion in posiciones_parciales:
        if posicion != -1:
            ocupadas.add(posicion)

    disponibles = []

    for perrera in range(total_perreras):
        if perrera not in ocupadas:
            disponibles.append(perrera)

    return disponibles


def prioridad_perrera(perrera, n):
    # para configuraciones h2 y h3
    # desempates por 
    # primero esquina, tiene menos vecinos
    # segundo borde
    # tercero centro
   
    fila, columna = indice_a_posicion(perrera, n)

    esta_en_fila_extrema = fila == 0 or fila == n - 1
    esta_en_columna_extrema = columna == 0 or columna == n - 1

    if esta_en_fila_extrema and esta_en_columna_extrema:
        return 0

    if esta_en_fila_extrema or esta_en_columna_extrema:
        return 1

    return 2


def costo_incremental(instancia, posiciones_parciales, indice_perro, perrera):
    n = instancia.n
    perros = instancia.perros
    perro_actual = perros[indice_perro]

    costo = 0

    fila, columna = indice_a_posicion(perrera, n)

    # si el perro esta enfermo, deberia ir en la primera fila
    # si no queda en fila 0 da penalizacion
    if perro_actual.enfermo and fila != 0:
        costo += 20

    for i in range(len(posiciones_parciales)):
        posicion_otro = posiciones_parciales[i]

        if posicion_otro == -1:
            continue

        perro_otro = perros[i]

        # conflictos solo entre perreras adyacentes
        if son_adyacentes(perrera, posicion_otro, n):

            # macho con macho
            if perro_actual.sexo == "M" and perro_otro.sexo == "M":
                costo += 10

            # perro actual macho y otro hembra
            if perro_actual.sexo == "M" and perro_otro.sexo == "H" and perro_otro.celo:
                costo += 10

            # otro macho y actual hembra
            if perro_otro.sexo == "M" and perro_actual.sexo == "H" and perro_actual.celo:
                costo += 10

    return costo


def seleccionar_mejor_perrera(instancia, posiciones_parciales, indice_perro, configuracion):
    disponibles = obtener_perreras_disponibles(instancia, posiciones_parciales)

    mejor_perrera = None
    mejor_costo = None
    mejor_prioridad = None
    evaluaciones = 0

    for perrera in disponibles:
        evaluaciones += 1
        costo = costo_incremental(instancia, posiciones_parciales, indice_perro, perrera)

        # Se queda con la primera perrera que tenga el menor costo
        if configuracion == "H1":
            if mejor_costo is None or costo < mejor_costo:
                mejor_costo = costo
                mejor_perrera = perrera

        # H2 y H3
        # si hay empate en costo, se usa prioridad
        else:
            prioridad = prioridad_perrera(perrera, instancia.n)

            if mejor_costo is None:
                mejor_costo = costo
                mejor_prioridad = prioridad
                mejor_perrera = perrera

            elif costo < mejor_costo:
                mejor_costo = costo
                mejor_prioridad = prioridad
                mejor_perrera = perrera

            elif costo == mejor_costo and prioridad < mejor_prioridad:
                mejor_costo = costo
                mejor_prioridad = prioridad
                mejor_perrera = perrera

    return mejor_perrera, evaluaciones


def heuristica(instancia, configuracion="H1"):
    tiempo_inicio = time.time()
    soluciones_evaluadas = 0

    posiciones = [-1] * instancia.p

    orden_perros = obtener_orden_perros(instancia, configuracion)

    # colocar los perros uno por uno
    for indice_perro in orden_perros:
        mejor_perrera, evaluaciones = seleccionar_mejor_perrera(instancia, posiciones, indice_perro, configuracion)

        soluciones_evaluadas += evaluaciones

        # guardar la perrera elegida para ese perro
        posiciones[indice_perro] = mejor_perrera

    solucion_final = Solucion(posiciones)

    resultado = evaluar(instancia, solucion_final)

    tiempo_fin = time.time()
    tiempo_ms = (tiempo_fin - tiempo_inicio) * 1000

    return {
        "solucion": solucion_final,
        "costo": resultado["costo"],
        "conflictosMachoMacho": resultado["conflictosMachoMacho"],
        "conflictosMachoHembraCelo": resultado["conflictosMachoHembraCelo"],
        "enfermosFueraPrimeraFila": resultado["enfermosFueraPrimeraFila"],
        "tiempoMs": round(tiempo_ms, 3),
        "evaluaciones": soluciones_evaluadas,
        "configuracion": configuracion,
        "valida": resultado["valida"]
    }
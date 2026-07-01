import time
from itertools import permutations
from src.core.evaluador import evaluar
from src.core.modelos import Solucion

def fuerza_bruta(instancia):
    inicio = time.perf_counter()

    mejor_costo = None
    mejor_solucion = None
    mejor_resultado = None
    evaluaciones = 0

    # Generar todas las permutaciones de posiciones posibles
    for perm in permutations(range(instancia.n * instancia.n), instancia.p):
        evaluaciones += 1

        # Crear objeto Solucion con la permutación
        solucion = Solucion(posiciones=list(perm))

        # Evaluar la solución
        resultado = evaluar(instancia, solucion)

        if mejor_costo is None or resultado["costo"] < mejor_costo:
            mejor_costo = resultado["costo"]
            mejor_solucion = solucion # guarda el objeto Solucion para poder exportar .posiciones
            mejor_resultado = resultado 

    fin = time.perf_counter()
    tiempo_ms = (fin - inicio) * 1000

    return {
        "costo": mejor_costo,
        "solucion": mejor_solucion,
        "conflictosMachoMacho": mejor_resultado["conflictosMachoMacho"],
        "conflictosMachoHembraCelo": mejor_resultado["conflictosMachoHembraCelo"],
        "enfermosFueraPrimeraFila": mejor_resultado["enfermosFueraPrimeraFila"],
        "tiempoMs": tiempo_ms,
        "evaluaciones": evaluaciones
    }

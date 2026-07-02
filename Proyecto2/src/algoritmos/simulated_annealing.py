import math
import random
import time
import sys
import os

from src.core.evaluador import evaluar

from src.algoritmos.vecindario import generar_solucion_aleatoria, generar_vecino


def aceptar(delta, temperatura):
    """
    Decide si se acepta una solución peor
    usando la probabilidad de Simulated Annealing.
    """

    probabilidad = math.exp(-delta / temperatura)

    return random.random() < probabilidad


def simulated_annealing(
    instancia,
    temperatura_inicial=100.0,
    temperatura_minima=0.01,
    alpha=0.95,
    iteraciones_por_temperatura=100,
    semilla=None
):
    """
    Ejecuta Simulated Annealing sobre una instancia del problema.
    """

    if semilla is not None:
        random.seed(semilla)

    tiempo_inicio = time.time()

    soluciones_evaluadas = 0

    # Generar solución inicial
    solucion_actual = generar_solucion_aleatoria(instancia)

    resultado_actual = evaluar(instancia, solucion_actual)

    soluciones_evaluadas += 1

    # La mejor solución encontrada hasta el momento
    mejor_solucion = solucion_actual
    mejor_resultado = resultado_actual

    temperatura = temperatura_inicial

    while temperatura > temperatura_minima:

        for i in range(iteraciones_por_temperatura):

            solucion_candidata = generar_vecino(
                instancia,
                solucion_actual
            )

            resultado_candidato = evaluar(
                instancia,
                solucion_candidata
            )

            soluciones_evaluadas += 1

            costo_actual = resultado_actual["costo"]
            costo_candidato = resultado_candidato["costo"]

            delta = costo_candidato - costo_actual

            # Siempre aceptar si mejora o mantiene el costo
            if delta <= 0:

                solucion_actual = solucion_candidata
                resultado_actual = resultado_candidato

                if costo_candidato < mejor_resultado["costo"]:

                    mejor_solucion = solucion_candidata
                    mejor_resultado = resultado_candidato

            else:

                if aceptar(delta, temperatura):

                    solucion_actual = solucion_candidata
                    resultado_actual = resultado_candidato

        # Disminuir la temperatura
        temperatura *= alpha

    tiempo_fin = time.time()

    tiempo_ms = (tiempo_fin - tiempo_inicio) * 1000

    return {

        "solucion": mejor_solucion,

        "costo": mejor_resultado["costo"],

        "conflictosMachoMacho":
            mejor_resultado["conflictosMachoMacho"],

        "conflictosMachoHembraCelo":
            mejor_resultado["conflictosMachoHembraCelo"],

        "enfermosFueraPrimeraFila":
            mejor_resultado["enfermosFueraPrimeraFila"],

        "tiempoMs":
            round(tiempo_ms, 3),

        "evaluaciones":
            soluciones_evaluadas,

        "temperatura_inicial":
            temperatura_inicial,

        "temperatura_minima":
            temperatura_minima,

        "alpha":
            alpha,

        "iteraciones_por_temperatura":
            iteraciones_por_temperatura,

        "semilla":
            semilla if semilla is not None else -1
    }
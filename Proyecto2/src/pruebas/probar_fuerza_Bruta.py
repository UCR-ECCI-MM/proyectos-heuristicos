import csv
import os
import sys
import itertools

from src.core.lector import leer_instancia
from src.algoritmos.fuerza_Bruta import fuerza_bruta
from src.core.getTestFiles import obtener_archivos_prueba

# Número de ejecuciones por archivo
CORRIDAS_POR_ARCHIVO = 3

def ejecutar_fuerza_bruta(carpeta_data, ruta_salida, tipo_prueba):
    archivos = obtener_archivos_prueba(carpeta_data, tipo_prueba)

    if not archivos:
        print(f"No se encontraron archivos de prueba en: {carpeta_data}")
        return

    columnas = [
        "algoritmo", "archivo", "N", "P",
        "costoFinal",
        "solucion",
        "conflictosMachoMacho",
        "conflictosMachoHembraCelo",
        "enfermosFueraPrimeraFila",
        "tiempoMs",
        "solucionesEvaluadas"
    ]

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, 'w', newline='') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=columnas)
        writer.writeheader()

        for ruta_archivo in archivos:
            nombre_archivo = os.path.basename(ruta_archivo)
            print(f"\nArchivo: {nombre_archivo}")

            try:
                instancia = leer_instancia(ruta_archivo)
            except Exception as e:
                print(f"  Error leyendo {nombre_archivo}: {e}")
                continue

            #resultado = fuerza_bruta(instancia)            

            for corrida in range(1, CORRIDAS_POR_ARCHIVO + 1):
                print(f"  Corrida {corrida}/{CORRIDAS_POR_ARCHIVO} de fuerza bruta.")
                resultado = fuerza_bruta(instancia)
                print(
                    f"    costo={resultado['costo']} "
                    f"tiempoMs={resultado['tiempoMs']} "
                    f"evaluaciones={resultado['evaluaciones']}"
                )

                fila = {
                    "algoritmo": "FuerzaBruta",
                    "archivo": nombre_archivo,
                    "N": instancia.n,
                    "P": instancia.p,
                    "costoFinal": resultado["costo"],
                    "solucion": resultado["solucion"].posiciones,
                    "conflictosMachoMacho": resultado["conflictosMachoMacho"],
                    "conflictosMachoHembraCelo": resultado["conflictosMachoHembraCelo"],
                    "enfermosFueraPrimeraFila": resultado["enfermosFueraPrimeraFila"],
                    "tiempoMs": resultado["tiempoMs"],
                    "solucionesEvaluadas": resultado["evaluaciones"]
                }
                writer.writerow(fila)

    print(f"\nResultados guardados en: {ruta_salida}")
  
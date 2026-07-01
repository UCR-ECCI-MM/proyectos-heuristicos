import csv
import os
from src.core.lector import leer_instancia
from src.core.getTestFiles import obtener_archivos_prueba
from src.algoritmos.heuristica import heuristica


CONFIGURACIONES = ["H1", "H2", "H3"]


def ejecutar_heuristica(carpeta_data, ruta_salida, tipo_prueba):
    archivos = obtener_archivos_prueba(carpeta_data, tipo_prueba)

    if not archivos:
        print(f"No se encontraron archivos de prueba en: {carpeta_data}")
        return

    columnas = [
        "algoritmo",
        "configuracion",
        "archivo",
        "N",
        "P",
        "corrida",
        "semilla",
        "costoFinal",
        "conflictosMachoMacho",
        "conflictosMachoHembraCelo",
        "enfermosFueraPrimeraFila",
        "tiempoMs",
        "solucionesEvaluadas"
    ]

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, "w", newline="", encoding="utf-8") as archivo_csv:
        writer = csv.DictWriter(archivo_csv, fieldnames=columnas)
        writer.writeheader()

        for ruta_archivo in archivos:
            nombre_archivo = os.path.basename(ruta_archivo)
            print(f"\nArchivo: {nombre_archivo}")

            try:
                instancia = leer_instancia(ruta_archivo)
            except Exception as error:
                print(f"  Error leyendo {nombre_archivo}: {error}")
                continue

            for configuracion in CONFIGURACIONES:
                resultado = heuristica(instancia, configuracion)

                print(
                    f"  {configuracion}: "
                    f"costo={resultado['costo']} "
                    f"tiempoMs={resultado['tiempoMs']} "
                    f"evaluaciones={resultado['evaluaciones']}"
                )

                fila = {
                    "algoritmo": "Heuristica",
                    "configuracion": configuracion,
                    "archivo": nombre_archivo,
                    "N": instancia.n,
                    "P": instancia.p,
                    "corrida": 1,
                    "semilla": -1,
                    "costoFinal": resultado["costo"],
                    "conflictosMachoMacho": resultado["conflictosMachoMacho"],
                    "conflictosMachoHembraCelo": resultado["conflictosMachoHembraCelo"],
                    "enfermosFueraPrimeraFila": resultado["enfermosFueraPrimeraFila"],
                    "tiempoMs": resultado["tiempoMs"],
                    "solucionesEvaluadas": resultado["evaluaciones"]
                }

                writer.writerow(fila)

    print(f"\nResultados guardados en: {ruta_salida}")
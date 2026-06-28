import csv
import os
import sys
import itertools

from src.core.modelos import Instancia, Perro
from src.algoritmos.simulated_annealing import simulated_annealing

# TODO: Cuando lector.py esté disponible
# from lector import leer_instancia

def leer_instancia(ruta_archivo):
    with open(ruta_archivo, 'r') as f:
        lineas = [l.strip() for l in f if l.strip()]

    if len(lineas) == 0:
        raise ValueError(f"Archivo vacío: {ruta_archivo}")

    primera = lineas[0].split()

    if len(primera) < 2:
        raise ValueError(f"Formato inválido en primera línea: {lineas[0]}")

    n = int(primera[0])
    p = int(primera[1])

    perros = []

    if len(lineas[1:]) < p:
        raise ValueError("No hay suficientes perros en el archivo")

    for linea in lineas[1:p + 1]:
        partes = linea.split()
        id_perro = partes[0]
        sexo = partes[1]
        celo = int(partes[2]) == 1
        enfermo = int(partes[3]) == 1
        perros.append(Perro(id_perro, sexo, celo, enfermo))

    return Instancia(n, perros)


# Configuraciones a probar
TEMPERATURAS_INICIALES = [50, 100, 200]
ALPHAS = [0.90, 0.95, 0.99]
ITERACIONES_POR_TEMPERATURA = [50, 100, 200]
TEMPERATURA_MINIMA = 0.01
CORRIDAS_POR_CONFIGURACION = 10

# Semillas fijas para reproducibilidad
SEMILLAS = [42, 7, 13, 99, 1234, 555, 321, 808, 777, 2024]

def obtener_archivos_prueba(carpeta_data):
    """Retorna lista de rutas de archivos .txt en la carpeta data."""
    archivos = []
    for nombre in sorted(os.listdir(carpeta_data)):
        if nombre.endswith('.txt'):
            archivos.append(os.path.join(carpeta_data, nombre))
    return archivos

#total 27 configuraciones
def ejecutar_experimentos(carpeta_data, ruta_salida):
    """
    Ejecuta SA con todas las combinaciones de parámetros
    sobre todos los archivos de prueba.

    Guarda resultados en ruta_salida (CSV).
    """
    archivos = obtener_archivos_prueba(carpeta_data)

    if not archivos:
        print(f"No se encontraron archivos de prueba en: {carpeta_data}")
        return

    # Encabezado del CSV 
    columnas = [
        "algoritmo", "configuracion", "archivo",
        "N", "P", "corrida", "semilla",
        "costoFinal",
        "conflictosMachoMacho",
        "conflictosMachoHembraCelo",
        "enfermosFueraPrimeraFila",
        "tiempoMs",
        "solucionesEvaluadas",
        "temperatura_inicial", "temperatura_minima",
        "alpha", "iteraciones_por_temperatura"
    ]

    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)

    with open(ruta_salida, 'w', newline='') as f_csv:
        writer = csv.DictWriter(f_csv, fieldnames=columnas)
        writer.writeheader()

        # Iterar sobre archivos y combinaciones de parámetros
        for ruta_archivo in archivos:
            nombre_archivo = os.path.basename(ruta_archivo)
            print(f"\nArchivo: {nombre_archivo}")

            try:
                instancia = leer_instancia(ruta_archivo)
            except Exception as e:
                print(f"  Error leyendo {nombre_archivo}: {e}")
                continue

            combinaciones = list(itertools.product(
                TEMPERATURAS_INICIALES,
                ALPHAS,
                ITERACIONES_POR_TEMPERATURA
            ))

            for temp_ini, alpha, iter_temp in combinaciones:
                nombre_config = f"T{temp_ini}_a{alpha}_i{iter_temp}"
                print(f"  Config: {nombre_config}")

                for corrida in range(1, CORRIDAS_POR_CONFIGURACION + 1):
                    semilla = SEMILLAS[corrida - 1]

                    resultado = simulated_annealing(
                        instancia,
                        temperatura_inicial=temp_ini,
                        temperatura_minima=TEMPERATURA_MINIMA,
                        alpha=alpha,
                        iteraciones_por_temperatura=iter_temp,
                        semilla=semilla
                    )

                    fila = {
                        "algoritmo": "SimulatedAnnealing",
                        "configuracion": nombre_config,
                        "archivo": nombre_archivo,
                        "N": instancia.n,
                        "P": instancia.p,
                        "corrida": corrida,
                        "semilla": semilla,
                        "costoFinal": resultado["costo"],
                        "conflictosMachoMacho": resultado["conflictosMachoMacho"],
                        "conflictosMachoHembraCelo": resultado["conflictosMachoHembraCelo"],
                        "enfermosFueraPrimeraFila": resultado["enfermosFueraPrimeraFila"],
                        "tiempoMs": resultado["tiempoMs"],
                        "solucionesEvaluadas": resultado["evaluaciones"],
                        "temperatura_inicial": temp_ini,
                        "temperatura_minima": TEMPERATURA_MINIMA,
                        "alpha": alpha,
                        "iteraciones_por_temperatura": iter_temp
                    }
                    writer.writerow(fila)

    print(f"\nResultados guardados en: {ruta_salida}")


if __name__ == "__main__":
    carpeta_raiz = os.path.join(os.path.dirname(__file__), '..', '..')
    carpeta_data = os.path.join(carpeta_raiz, 'data')
    ruta_salida = os.path.join(carpeta_raiz, 'results', 'resultados_sa.csv')
    ejecutar_experimentos(carpeta_data, ruta_salida)
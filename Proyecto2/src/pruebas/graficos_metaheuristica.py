import csv
import os
import matplotlib.pyplot as plt


def leer_resultados(ruta_csv):
    """
    Lee el archivo CSV y devuelve todas las filas.
    """

    filas = []

    with open(ruta_csv, "r") as archivo:

        lector = csv.DictReader(archivo)

        for fila in lector:

            fila["costoFinal"] = float(fila["costoFinal"])
            fila["tiempoMs"] = float(fila["tiempoMs"])
            fila["N"] = int(fila["N"])

            filas.append(fila)

    return filas


def promedio(lista):

    if len(lista) == 0:
        return 0

    return sum(lista) / len(lista)


def graficar_costo_promedio(filas, carpeta_salida):
    """
    Grafica el costo promedio de cada configuración.
    """

    costos = {}

    for fila in filas:

        config = fila["configuracion"]

        if config not in costos:
            costos[config] = []

        costos[config].append(fila["costoFinal"])

    configuraciones = []
    promedios = []

    for config in sorted(costos.keys()):

        configuraciones.append(config)
        promedios.append(promedio(costos[config]))

    plt.figure(figsize=(10,5))

    plt.bar(configuraciones, promedios)

    plt.xticks(rotation=45, ha="right")

    plt.ylabel("Costo promedio")
    plt.title("Costo promedio por configuración")

    plt.tight_layout()

    plt.savefig(os.path.join(
        carpeta_salida,
        "costo_promedio.png"
    ))

    plt.close()


def graficar_tiempo_promedio(filas, carpeta_salida):
    """
    Grafica el tiempo promedio de cada configuración.
    """

    tiempos = {}

    for fila in filas:

        config = fila["configuracion"]

        if config not in tiempos:
            tiempos[config] = []

        tiempos[config].append(fila["tiempoMs"])

    configuraciones = []
    promedios = []

    for config in sorted(tiempos.keys()):

        configuraciones.append(config)
        promedios.append(promedio(tiempos[config]))

    plt.figure(figsize=(10,5))

    plt.bar(configuraciones, promedios)

    plt.xticks(rotation=45, ha="right")

    plt.ylabel("Tiempo (ms)")
    plt.title("Tiempo promedio por configuración")

    plt.tight_layout()

    plt.savefig(os.path.join(
        carpeta_salida,
        "tiempo_promedio.png"
    ))

    plt.close()


def graficar_mejor_peor(filas, carpeta_salida, archivo_filtro=None):
    if archivo_filtro:
        filas = [f for f in filas if f["archivo"] == archivo_filtro]

    datos = {}

    for fila in filas:

        config = fila["configuracion"]

        if config not in datos:
            datos[config] = []

        datos[config].append(fila["costoFinal"])

    configuraciones = []
    mejores = []
    peores = []

    for config in sorted(datos.keys()):

        configuraciones.append(config)

        mejores.append(min(datos[config]))
        peores.append(max(datos[config]))

    plt.figure(figsize=(10,5))

    plt.plot(configuraciones, mejores, marker="o", label="Mejor")

    plt.plot(configuraciones, peores, marker="o", label="Peor")

    plt.xticks(rotation=45, ha="right")

    plt.ylabel("Costo")

    plt.title("Mejor y peor costo")

    plt.legend()

    plt.tight_layout()

    plt.savefig(os.path.join(
        carpeta_salida,
        f"mejor_peor_{archivo_filtro}.png"
    ))

    plt.close()


def graficar_por_tamano(filas, carpeta_salida):
    """
    Grafica el costo promedio según el tamaño N.
    """

    datos = {}

    for fila in filas:

        n = fila["N"]

        if n not in datos:
            datos[n] = []

        datos[n].append(fila["costoFinal"])

    tamanos = []
    costos = []

    for n in sorted(datos.keys()):

        tamanos.append(n)
        costos.append(promedio(datos[n]))

    plt.figure(figsize=(7,5))

    plt.plot(tamanos, costos, marker="o")

    plt.xlabel("N")

    plt.ylabel("Costo promedio")

    plt.title("Costo promedio por tamaño")

    plt.tight_layout()

    plt.savefig(os.path.join(
        carpeta_salida,
        "tamano.png"
    ))

    plt.close()

def mostrar_mejor_configuracion(filas):
    """
    Muestra cuál configuración obtuvo el mejor
    costo promedio. Si hay empate, se escoge
    la de menor tiempo promedio.
    """

    datos = {}

    for fila in filas:

        config = fila["configuracion"]

        if config not in datos:
            datos[config] = {
                "costos": [],
                "tiempos": []
            }

        datos[config]["costos"].append(fila["costoFinal"])
        datos[config]["tiempos"].append(fila["tiempoMs"])

    mejor_config = None
    mejor_costo = None
    mejor_tiempo = None

    for config in sorted(datos.keys()):

        costo_promedio = promedio(datos[config]["costos"])
        tiempo_promedio = promedio(datos[config]["tiempos"])

        if (
            mejor_config is None
            or costo_promedio < mejor_costo
            or (
                costo_promedio == mejor_costo
                and tiempo_promedio < mejor_tiempo
            )
        ):
            mejor_config = config
            mejor_costo = costo_promedio
            mejor_tiempo = tiempo_promedio

    print("\n===== Mejor configuración =====")
    print(f"Configuración: {mejor_config}")
    print(f"Costo promedio: {mejor_costo:.2f}")
    print(f"Tiempo promedio: {mejor_tiempo:.2f} ms")

def main():
    carpeta_raiz = os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )

    ruta_csv = os.path.join(
        carpeta_raiz,
        "results",
        "resultados_sa.csv"
    )

    carpeta_graficos = os.path.join(
        carpeta_raiz,
        "results",
        "graficos"
    )

    os.makedirs(carpeta_graficos, exist_ok=True)

    filas = leer_resultados(ruta_csv)

    graficar_costo_promedio(
        filas,
        carpeta_graficos
    )

    graficar_tiempo_promedio(
        filas,
        carpeta_graficos
    )

    graficar_mejor_peor(filas, carpeta_graficos, "small_01.txt")
    graficar_mejor_peor(filas, carpeta_graficos, "small_02.txt")

    graficar_por_tamano(
        filas,
        carpeta_graficos
    )
    mostrar_mejor_configuracion(filas)
    print("Gráficos generados correctamente.")


if __name__ == "__main__":
    main()
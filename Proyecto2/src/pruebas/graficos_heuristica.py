import csv
import os
import matplotlib.pyplot as plt


def leer_resultados(ruta_csv):
    filas = []

    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            fila["costoFinal"] = float(fila["costoFinal"])
            fila["tiempoMs"] = float(fila["tiempoMs"])
            fila["N"] = int(fila["N"])
            fila["P"] = int(fila["P"])
            fila["solucionesEvaluadas"] = int(fila["solucionesEvaluadas"])

            filas.append(fila)

    return filas


def promedio(lista):
    if len(lista) == 0:
        return 0

    return sum(lista) / len(lista)


def graficar_costo_promedio_configuracion(filas, carpeta_salida):
    """
    grafica el costo promedio obtenido por cada configuracion:
    H1, H2 y H3
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

    plt.figure(figsize=(8, 5))
    plt.bar(configuraciones, promedios)
    plt.xlabel("Configuración")
    plt.ylabel("Costo promedio")
    plt.title("Costo promedio por configuración (Heurística)")
    plt.tight_layout()

    plt.savefig(os.path.join(carpeta_salida, "costo_promedio_heuristica.png"))
    plt.close()


def graficar_tiempo_promedio_configuracion(filas, carpeta_salida):
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

    plt.figure(figsize=(8, 5))
    plt.bar(configuraciones, promedios)
    plt.xlabel("Configuración")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Tiempo promedio por configuración (Heurística)")
    plt.tight_layout()

    plt.savefig(os.path.join(carpeta_salida, "tiempo_promedio_heuristica.png"))
    plt.close()


def graficar_costo_por_archivo(filas, carpeta_salida):
    """
    grafica el costo final por archivo comparando H1, H2 y H3
    """

    archivos = sorted(set(fila["archivo"] for fila in filas))
    configuraciones = sorted(set(fila["configuracion"] for fila in filas))

    datos = {}

    for archivo in archivos:
        datos[archivo] = {}

        for config in configuraciones:
            datos[archivo][config] = None

    for fila in filas:
        archivo = fila["archivo"]
        config = fila["configuracion"]
        datos[archivo][config] = fila["costoFinal"]

    x = list(range(len(archivos)))
    ancho = 0.8 / len(configuraciones)

    plt.figure(figsize=(10, 5))

    for i, config in enumerate(configuraciones):
        valores = []

        for archivo in archivos:
            valores.append(datos[archivo][config])

        posiciones = []

        for valor_x in x:
            posiciones.append(valor_x + i * ancho)

        plt.bar(posiciones, valores, width=ancho, label=config)

    centros = []

    for valor_x in x:
        centros.append(valor_x + ancho * (len(configuraciones) - 1) / 2)

    plt.xticks(centros, archivos, rotation=45, ha="right")
    plt.xlabel("Archivo")
    plt.ylabel("Costo final")
    plt.title("Costo final por archivo y configuración (Heurística)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(carpeta_salida, "costo_por_archivo_heuristica.png"))
    plt.close()


def graficar_tiempo_por_archivo(filas, carpeta_salida):
    archivos = sorted(set(fila["archivo"] for fila in filas))
    configuraciones = sorted(set(fila["configuracion"] for fila in filas))

    datos = {}

    for archivo in archivos:
        datos[archivo] = {}

        for config in configuraciones:
            datos[archivo][config] = None

    for fila in filas:
        archivo = fila["archivo"]
        config = fila["configuracion"]
        datos[archivo][config] = fila["tiempoMs"]

    x = list(range(len(archivos)))
    ancho = 0.8 / len(configuraciones)

    plt.figure(figsize=(10, 5))

    for i, config in enumerate(configuraciones):
        valores = []

        for archivo in archivos:
            valores.append(datos[archivo][config])

        posiciones = []

        for valor_x in x:
            posiciones.append(valor_x + i * ancho)

        plt.bar(posiciones, valores, width=ancho, label=config)

    centros = []

    for valor_x in x:
        centros.append(valor_x + ancho * (len(configuraciones) - 1) / 2)

    plt.xticks(centros, archivos, rotation=45, ha="right")
    plt.xlabel("Archivo")
    plt.ylabel("Tiempo (ms)")
    plt.title("Tiempo por archivo y configuración (Heurística)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(carpeta_salida, "tiempo_por_archivo_heuristica.png"))
    plt.close()


def graficar_por_tamano(filas, carpeta_salida):
    """
    grafica el costo promedio por tamaño N para cada configuracion
    """

    datos = {}

    for fila in filas:
        n = fila["N"]
        config = fila["configuracion"]

        if config not in datos:
            datos[config] = {}

        if n not in datos[config]:
            datos[config][n] = []

        datos[config][n].append(fila["costoFinal"])

    plt.figure(figsize=(8, 5))

    for config in sorted(datos.keys()):
        tamanos = []
        costos_promedio = []

        for n in sorted(datos[config].keys()):
            tamanos.append(n)
            costos_promedio.append(promedio(datos[config][n]))

        plt.plot(tamanos, costos_promedio, marker="o", label=config)

    plt.xlabel("Tamaño N")
    plt.ylabel("Costo promedio")
    plt.title("Costo promedio por tamaño N (Heurística)")
    plt.legend()
    plt.tight_layout()

    plt.savefig(os.path.join(carpeta_salida, "tamano_heuristica.png"))
    plt.close()


def mostrar_mejor_configuracion(filas):
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

    print("\nMejor configuración de heurística")
    print(f"Configuración: {mejor_config}")
    print(f"Costo promedio: {mejor_costo:.2f}")
    print(f"Tiempo promedio: {mejor_tiempo:.2f} ms")


def main():
    TIPO_PRUEBA = "small"
    #TIPO_PRUEBA = "medium"
    #TIPO_PRUEBA = "large"

    carpeta_raiz = os.path.join(
        os.path.dirname(__file__),
        "..",
        ".."
    )

    ruta_csv = os.path.join(
        carpeta_raiz,
        "results",
        f"resultados_he_{TIPO_PRUEBA}.csv"
    )

    carpeta_graficos = os.path.join(
        carpeta_raiz,
        "results",
        "graficos",
        "heuristica",
        TIPO_PRUEBA
    )

    os.makedirs(carpeta_graficos, exist_ok=True)

    filas = leer_resultados(ruta_csv)

    graficar_costo_promedio_configuracion(
        filas,
        carpeta_graficos
    )

    graficar_tiempo_promedio_configuracion(
        filas,
        carpeta_graficos
    )

    graficar_costo_por_archivo(
        filas,
        carpeta_graficos
    )

    graficar_tiempo_por_archivo(
        filas,
        carpeta_graficos
    )

    graficar_por_tamano(
        filas,
        carpeta_graficos
    )

    mostrar_mejor_configuracion(filas)

    print("Gráficos de heurística generados correctamente.")


if __name__ == "__main__":
    main()
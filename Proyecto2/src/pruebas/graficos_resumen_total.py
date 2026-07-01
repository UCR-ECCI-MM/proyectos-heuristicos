import csv
import os
import math
import matplotlib.pyplot as plt


TAMANOS = ["small", "medium", "large"]
CONFIGS_HE = ["H1", "H2", "H3"]


def leer_resultados(ruta_csv):
    filas = []

    if not os.path.exists(ruta_csv):
        print(f"No existe: {ruta_csv}")
        return filas

    with open(ruta_csv, "r", encoding="utf-8") as archivo:
        lector = csv.DictReader(archivo)

        for fila in lector:
            # Convertir valores numericos si existen
            for campo in ["costoFinal", "tiempoMs"]:
                if campo in fila and fila[campo] != "":
                    fila[campo] = float(fila[campo])

            for campo in ["N", "P", "solucionesEvaluadas"]:
                if campo in fila and fila[campo] != "":
                    fila[campo] = int(float(fila[campo]))

            filas.append(fila)

    return filas


def promedio(lista):
    if len(lista) == 0:
        return 0
    return sum(lista) / len(lista)


# HEURISTICA
def cargar_heuristica(carpeta_raiz):
    datos = {}

    for tamano in TAMANOS:
        ruta = os.path.join(carpeta_raiz, "results", f"resultados_he_{tamano}.csv")
        filas = leer_resultados(ruta)

        datos[tamano] = {}

        for config in CONFIGS_HE:
            datos[tamano][config] = {
                "costos": [],
                "tiempos": []
            }

        for fila in filas:
            config = fila["configuracion"]
            if config in datos[tamano]:
                datos[tamano][config]["costos"].append(fila["costoFinal"])
                datos[tamano][config]["tiempos"].append(fila["tiempoMs"])

    return datos


def obtener_mejores_heuristica(datos):
    mejores = {}

    for tamano in TAMANOS:
        mejor_config = None
        mejor_costo = None
        mejor_tiempo = None

        for config in CONFIGS_HE:
            costo = promedio(datos[tamano][config]["costos"])
            tiempo = promedio(datos[tamano][config]["tiempos"])

            if (
                mejor_config is None
                or costo < mejor_costo
                or (costo == mejor_costo and tiempo < mejor_tiempo)
            ):
                mejor_config = config
                mejor_costo = costo
                mejor_tiempo = tiempo

        mejores[tamano] = {
            "configuracion": mejor_config,
            "costo": mejor_costo,
            "tiempo": mejor_tiempo
        }

    return mejores


def graficar_heuristica(datos, carpeta_salida):
    x = list(range(len(TAMANOS)))
    ancho = 0.25

    # Costo
    plt.figure(figsize=(9, 5))

    for i, config in enumerate(CONFIGS_HE):
        valores = []

        for tamano in TAMANOS:
            valores.append(promedio(datos[tamano][config]["costos"]))

        posiciones = [valor_x + i * ancho for valor_x in x]
        plt.bar(posiciones, valores, width=ancho, label=config)

        for pos, val in zip(posiciones, valores):
            plt.text(pos, val, f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    centros = [valor_x + ancho for valor_x in x]
    plt.xticks(centros, TAMANOS)
    plt.xlabel("Tamaño")
    plt.ylabel("Costo promedio")
    plt.title("Heurística: costo promedio por tamaño")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "heuristica_costo_promedio.png"))
    plt.close()

    # Tiempo
    plt.figure(figsize=(9, 5))

    for i, config in enumerate(CONFIGS_HE):
        valores = []

        for tamano in TAMANOS:
            valores.append(promedio(datos[tamano][config]["tiempos"]))

        posiciones = [valor_x + i * ancho for valor_x in x]
        plt.bar(posiciones, valores, width=ancho, label=config)

        for pos, val in zip(posiciones, valores):
            plt.text(pos, val, f"{val:.1f}", ha="center", va="bottom", fontsize=8)

    centros = [valor_x + ancho for valor_x in x]
    plt.xticks(centros, TAMANOS)
    plt.xlabel("Tamaño")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Heurística: tiempo promedio por tamaño")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "heuristica_tiempo_promedio.png"))
    plt.close()


# METAHEURISTICA
def cargar_meta(carpeta_raiz):
    datos = {}

    for tamano in TAMANOS:
        ruta = os.path.join(carpeta_raiz, "results", f"resultados_sa_{tamano}.csv")
        filas = leer_resultados(ruta)

        datos[tamano] = {}

        for fila in filas:
            config = fila["configuracion"]

            if config not in datos[tamano]:
                datos[tamano][config] = {
                    "costos": [],
                    "tiempos": []
                }

            datos[tamano][config]["costos"].append(fila["costoFinal"])
            datos[tamano][config]["tiempos"].append(fila["tiempoMs"])

    return datos


def obtener_mejores_meta(datos):
    mejores = {}

    for tamano in TAMANOS:
        mejor_config = None
        mejor_costo = None
        mejor_tiempo = None

        for config in sorted(datos[tamano].keys()):
            costo = promedio(datos[tamano][config]["costos"])
            tiempo = promedio(datos[tamano][config]["tiempos"])

            if (
                mejor_config is None
                or costo < mejor_costo
                or (costo == mejor_costo and tiempo < mejor_tiempo)
            ):
                mejor_config = config
                mejor_costo = costo
                mejor_tiempo = tiempo

        mejores[tamano] = {
            "configuracion": mejor_config,
            "costo": mejor_costo,
            "tiempo": mejor_tiempo
        }

    return mejores


def graficar_meta(mejores, carpeta_salida):
    etiquetas = []
    costos = []
    tiempos = []

    for tamano in TAMANOS:
        config = mejores[tamano]["configuracion"]
        etiquetas.append(f"{tamano}\n{config}")
        costos.append(mejores[tamano]["costo"])
        tiempos.append(mejores[tamano]["tiempo"])

    # Costo
    plt.figure(figsize=(9, 5))
    barras = plt.bar(etiquetas, costos)

    for barra, val in zip(barras, costos):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            val,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.xlabel("Tamaño y mejor configuración")
    plt.ylabel("Costo promedio")
    plt.title("Metaheurística: mejor configuración por tamaño")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "meta_costo_mejor_config.png"))
    plt.close()

    # Tiempo
    plt.figure(figsize=(9, 5))
    barras = plt.bar(etiquetas, tiempos)

    for barra, val in zip(barras, tiempos):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            val,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.xlabel("Tamaño y mejor configuración")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Metaheurística: tiempo de la mejor configuración por tamaño")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "meta_tiempo_mejor_config.png"))
    plt.close()


# FUERZA BRUTA
def cargar_fuerza_bruta(carpeta_raiz):
    ruta = os.path.join(carpeta_raiz, "results", "resultados_fb_small.csv")
    filas = leer_resultados(ruta)

    datos = {}

    for fila in filas:
        archivo = fila["archivo"]

        if archivo not in datos:
            datos[archivo] = {
                "costos": [],
                "tiempos": []
            }

        datos[archivo]["costos"].append(fila["costoFinal"])
        datos[archivo]["tiempos"].append(fila["tiempoMs"])

    return datos


def obtener_resumen_fuerza(datos):
    todos_costos = []
    todos_tiempos = []

    for archivo in datos:
        todos_costos.extend(datos[archivo]["costos"])
        todos_tiempos.extend(datos[archivo]["tiempos"])

    return {
        "small": {
            "configuracion": "default",
            "costo": promedio(todos_costos),
            "tiempo": promedio(todos_tiempos)
        }
    }


def graficar_fuerza(datos, carpeta_salida):
    archivos = sorted(datos.keys())

    costos = [promedio(datos[a]["costos"]) for a in archivos]
    tiempos = [promedio(datos[a]["tiempos"]) for a in archivos]

    # Costo
    plt.figure(figsize=(8, 5))
    barras = plt.bar(archivos, costos)

    for barra, val in zip(barras, costos):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            val,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.ylabel("Costo promedio")
    plt.title("Fuerza Bruta: costo promedio en archivos small")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "fuerza_costo_promedio.png"))
    plt.close()

    # Tiempo
    plt.figure(figsize=(8, 5))
    barras = plt.bar(archivos, tiempos)

    for barra, val in zip(barras, tiempos):
        plt.text(
            barra.get_x() + barra.get_width() / 2,
            val,
            f"{val:.1f}",
            ha="center",
            va="bottom",
            fontsize=8
        )

    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Fuerza Bruta: tiempo promedio en archivos small")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "fuerza_tiempo_promedio.png"))
    plt.close()


# COMPARACION FINAL
def graficar_comparacion_final(resumen_fb, mejores_he, mejores_sa, carpeta_salida):
    algoritmos = ["FB", "HE", "SA"]
    x = list(range(len(TAMANOS)))
    ancho = 0.25

    datos_costos = {
        "FB": [
            resumen_fb["small"]["costo"],
            math.nan,
            math.nan
        ],
        "HE": [
            mejores_he["small"]["costo"],
            mejores_he["medium"]["costo"],
            mejores_he["large"]["costo"]
        ],
        "SA": [
            mejores_sa["small"]["costo"],
            mejores_sa["medium"]["costo"],
            mejores_sa["large"]["costo"]
        ]
    }

    datos_tiempos = {
        "FB": [
            resumen_fb["small"]["tiempo"],
            math.nan,
            math.nan
        ],
        "HE": [
            mejores_he["small"]["tiempo"],
            mejores_he["medium"]["tiempo"],
            mejores_he["large"]["tiempo"]
        ],
        "SA": [
            mejores_sa["small"]["tiempo"],
            mejores_sa["medium"]["tiempo"],
            mejores_sa["large"]["tiempo"]
        ]
    }

    # Costo
    plt.figure(figsize=(9, 5))

    for i, algoritmo in enumerate(algoritmos):
        posiciones = [valor_x + i * ancho for valor_x in x]
        valores = datos_costos[algoritmo]

        barras = plt.bar(posiciones, valores, width=ancho, label=algoritmo)

        for barra, val in zip(barras, valores):
            if not math.isnan(val):
                plt.text(
                    barra.get_x() + barra.get_width() / 2,
                    val,
                    f"{val:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

    centros = [valor_x + ancho for valor_x in x]
    plt.xticks(centros, TAMANOS)
    plt.xlabel("Tamaño")
    plt.ylabel("Costo promedio")
    plt.title("Comparación final: costo promedio por algoritmo")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "comparacion_final_costo.png"))
    plt.close()

    # Tiempo
    plt.figure(figsize=(9, 5))

    for i, algoritmo in enumerate(algoritmos):
        posiciones = [valor_x + i * ancho for valor_x in x]
        valores = datos_tiempos[algoritmo]

        barras = plt.bar(posiciones, valores, width=ancho, label=algoritmo)

        for barra, val in zip(barras, valores):
            if not math.isnan(val):
                plt.text(
                    barra.get_x() + barra.get_width() / 2,
                    val,
                    f"{val:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=8
                )

    centros = [valor_x + ancho for valor_x in x]
    plt.xticks(centros, TAMANOS)
    plt.xlabel("Tamaño")
    plt.ylabel("Tiempo promedio (ms)")
    plt.title("Comparación final: tiempo promedio por algoritmo")
    plt.legend()
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "comparacion_final_tiempo.png"))
    plt.close()


# REPORTE DE TEXTO
def guardar_resumen_txt(mejores_he, mejores_sa, resumen_fb, carpeta_salida):
    ruta = os.path.join(carpeta_salida, "resumen_resultados.txt")

    with open(ruta, "w", encoding="utf-8") as archivo:
        archivo.write("RESUMEN DE RESULTADOS\n\n")

        archivo.write("FUERZA BRUTA\n")
        archivo.write(
            f"small -> costo promedio: {resumen_fb['small']['costo']:.2f}, "
            f"tiempo promedio: {resumen_fb['small']['tiempo']:.2f} ms\n\n"
        )

        archivo.write("HEURISTICA\n")
        for tamano in TAMANOS:
            archivo.write(
                f"{tamano} -> mejor configuración: {mejores_he[tamano]['configuracion']}, "
                f"costo promedio: {mejores_he[tamano]['costo']:.2f}, "
                f"tiempo promedio: {mejores_he[tamano]['tiempo']:.2f} ms\n"
            )

        archivo.write("\nMETAHEURISTICA\n")
        for tamano in TAMANOS:
            archivo.write(
                f"{tamano} -> mejor configuración: {mejores_sa[tamano]['configuracion']}, "
                f"costo promedio: {mejores_sa[tamano]['costo']:.2f}, "
                f"tiempo promedio: {mejores_sa[tamano]['tiempo']:.2f} ms\n"
            )


def main():
    carpeta_raiz = os.path.join(os.path.dirname(__file__), "..", "..")

    carpeta_salida = os.path.join(
        carpeta_raiz,
        "results",
        "graficos",
        "resumen_total"
    )

    os.makedirs(carpeta_salida, exist_ok=True)

    # Heuristica
    datos_he = cargar_heuristica(carpeta_raiz)
    mejores_he = obtener_mejores_heuristica(datos_he)
    graficar_heuristica(datos_he, carpeta_salida)

    # Metaheuristica
    datos_sa = cargar_meta(carpeta_raiz)
    mejores_sa = obtener_mejores_meta(datos_sa)
    graficar_meta(mejores_sa, carpeta_salida)

    # Fuerza bruta
    datos_fb = cargar_fuerza_bruta(carpeta_raiz)
    resumen_fb = obtener_resumen_fuerza(datos_fb)
    graficar_fuerza(datos_fb, carpeta_salida)

    # Comparacion final
    graficar_comparacion_final(resumen_fb, mejores_he, mejores_sa, carpeta_salida)

    # Resumen en texto
    guardar_resumen_txt(mejores_he, mejores_sa, resumen_fb, carpeta_salida)

    print("Gráficos resumen generados correctamente.")
    print(f"Carpeta de salida: {carpeta_salida}")


if __name__ == "__main__":
    main()
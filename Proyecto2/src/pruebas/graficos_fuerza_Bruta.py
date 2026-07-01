import csv
import os
import matplotlib.pyplot as plt

def leer_resultados(ruta_csv):
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
    costos = {}
    for fila in filas:
        archivo = fila["archivo"]
        costos.setdefault(archivo, []).append(fila["costoFinal"])

    archivos = sorted(costos.keys())
    promedios = [promedio(costos[a]) for a in archivos]

    plt.figure(figsize=(10,5))
    plt.bar(archivos, promedios)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Costo promedio")
    plt.title("Costo promedio por archivo (Fuerza Bruta)")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "costo_FB_promedio.png"))
    plt.close()

def graficar_tiempo_promedio(filas, carpeta_salida):
    tiempos = {}
    for fila in filas:
        archivo = fila["archivo"]
        tiempos.setdefault(archivo, []).append(fila["tiempoMs"])

    archivos = sorted(tiempos.keys())
    promedios = [promedio(tiempos[a]) for a in archivos]

    plt.figure(figsize=(10,5))
    plt.bar(archivos, promedios)
    plt.xticks(rotation=45, ha="right")
    plt.ylabel("Tiempo (ms)")
    plt.title("Tiempo promedio por archivo (Fuerza Bruta)")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "tiempo_FB_promedio.png"))
    plt.close()

def graficar_por_tamano(filas, carpeta_salida):
    datos = {}
    for fila in filas:
        n = fila["N"]
        datos.setdefault(n, []).append(fila["costoFinal"])

    tamanos = sorted(datos.keys())
    mejores_costos = [min(datos[n]) for n in tamanos]

    plt.figure(figsize=(7,5))
    plt.scatter(tamanos, mejores_costos, s=80)
    plt.xticks(tamanos)
    plt.xlabel("Tamaño N")
    plt.ylabel("Mejor costo")
    plt.title("Mejor costo por tamaño (Fuerza Bruta)")
    plt.tight_layout()
    plt.savefig(os.path.join(carpeta_salida, "tamanoFB.png"))
    plt.close()

def main():
    TIPO_PRUEBA = "medium"  # small, medium, large
    carpeta_raiz = os.path.join(os.path.dirname(__file__), "..", "..")
    ruta_csv = os.path.join(carpeta_raiz, "results", f"resultados_fb_{TIPO_PRUEBA}.csv")
    carpeta_graficos = os.path.join(carpeta_raiz, "results", "graficos", "fuerza", TIPO_PRUEBA)
    os.makedirs(carpeta_graficos, exist_ok=True)

    filas = leer_resultados(ruta_csv)
    graficar_costo_promedio(filas, carpeta_graficos)
    graficar_tiempo_promedio(filas, carpeta_graficos)
    graficar_por_tamano(filas, carpeta_graficos)
    print("Gráficos de Fuerza Bruta generados correctamente.")

if __name__ == "__main__":
    main()

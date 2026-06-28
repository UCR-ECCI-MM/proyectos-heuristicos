from src.pruebas.probar_metaheuristica import ejecutar_experimentos


if __name__ == "__main__":

    carpeta_data = "data"
    ruta_salida = "results/resultados_sa.csv"

    ejecutar_experimentos(carpeta_data, ruta_salida)
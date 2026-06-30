from src.pruebas.probar_metaheuristica import ejecutar_experimentos

#TIPO_PRUEBA = "small"
TIPO_PRUEBA = "medium"
# TIPO_PRUEBA = "large"

if __name__ == "__main__":

    carpeta_data = "data"

    ruta_salida = f"results/resultados_sa_{TIPO_PRUEBA}.csv"

    ejecutar_experimentos(
        carpeta_data,
        ruta_salida,
        TIPO_PRUEBA
    )
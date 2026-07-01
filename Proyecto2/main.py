from src.pruebas.probar_metaheuristica import ejecutar_experimentos
from src.pruebas.probar_fuerza_Bruta import ejecutar_fuerza_bruta

# TODO seria modificar el de abajo cuando se implemente. 
# from src.pruebas.probar_heuristica import ejecutar_heuristica

# Selección de algoritmo: "SA", "FB", "HE"
ALGORITMO = "FB"

TIPO_PRUEBA = "small"
#TIPO_PRUEBA = "medium"
#TIPO_PRUEBA = "large"

if __name__ == "__main__":
    carpeta_data = "data"

    # Definir nombre de archivo de salida según algoritmo
    if ALGORITMO == "SA":
        ruta_salida = f"results/resultados_sa_{TIPO_PRUEBA}.csv"
        ejecutar_experimentos(carpeta_data, ruta_salida, TIPO_PRUEBA)

    elif ALGORITMO == "FB":
        ruta_salida = f"results/resultados_fb_{TIPO_PRUEBA}.csv"
        ejecutar_fuerza_bruta(carpeta_data, ruta_salida, TIPO_PRUEBA)

    #elif ALGORITMO == "HE":
    #    ruta_salida = f"results/resultados_he_{TIPO_PRUEBA}.csv"
    #    ejecutar_heuristica(carpeta_data, ruta_salida, TIPO_PRUEBA)

    else:
        print(f"Algoritmo desconocido: {ALGORITMO}")

from src.pruebas.probar_metaheuristica import ejecutar_experimentos
from src.pruebas.probar_fuerza_Bruta import ejecutar_fuerza_bruta 
from src.pruebas.probar_heuristica import ejecutar_heuristica

# Selección de algoritmo: "SA", "FB", "HE"
print("Seleccione el algoritmo:")
print("1. Fuerza Bruta")
print("2. Heurística")
print("3. Simulated Annealing")

opcion_algoritmo = input("Opción: ")

if opcion_algoritmo == "1":
    ALGORITMO = "FB"
elif opcion_algoritmo == "2":
    ALGORITMO = "HE"
elif opcion_algoritmo == "3":
    ALGORITMO = "SA"
else:
    print("Opción inválida. Se usará Heurística por defecto.")
    ALGORITMO = "HE"


print("\nSeleccione el archivo o grupo de prueba:")
print("Ejemplos:")
print("small -> corre todos los small")
print("medium -> corre todos los medium")
print("large -> corre todos los large")
print("small_01 -> corre solo small_01.txt")
print("medium_02 -> corre solo medium_02.txt")
print("large_01 -> corre solo large_01.txt")

TIPO_PRUEBA = input("Archivo o grupo: ")

if __name__ == "__main__":
    carpeta_data = "data"

    # Definir nombre de archivo de salida según algoritmo
    if ALGORITMO == "SA":
        ruta_salida = f"results/resultados_sa_{TIPO_PRUEBA}.csv"
        ejecutar_experimentos(carpeta_data, ruta_salida, TIPO_PRUEBA)

    elif ALGORITMO == "FB":
        ruta_salida = f"results/resultados_fb_{TIPO_PRUEBA}.csv"
        ejecutar_fuerza_bruta(carpeta_data, ruta_salida, TIPO_PRUEBA)

    elif ALGORITMO == "HE":
        ruta_salida = f"results/resultados_he_{TIPO_PRUEBA}.csv"
        ejecutar_heuristica(carpeta_data, ruta_salida, TIPO_PRUEBA)

    else:
        print(f"Algoritmo desconocido: {ALGORITMO}")

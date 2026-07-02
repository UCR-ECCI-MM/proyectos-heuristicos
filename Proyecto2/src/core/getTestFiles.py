import csv
import os
import sys
import itertools


def obtener_archivos_prueba(carpeta_data, tipo_prueba):
    archivos = []

    for nombre in sorted(os.listdir(carpeta_data)):
        if (
            nombre.endswith(".txt")
            and nombre.startswith(tipo_prueba)
        ):
            archivos.append(os.path.join(carpeta_data, nombre))

    return archivos
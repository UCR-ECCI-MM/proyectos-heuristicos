from src.core.modelos import Perro, Instancia

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

    if p > n * n:
        raise ValueError("\nError: Hay más perros que perreras")

    perros = []
    ids = set()

    if len(lineas[1:]) < p:
        raise ValueError("No hay suficientes perros en el archivo")

    for linea in lineas[1:p + 1]:
        partes = linea.split()
        id_perro = partes[0]
        sexo = partes[1]
        celo = int(partes[2]) == 1
        enfermo = int(partes[3]) == 1

        # Validar id único
        if id_perro in ids:
            raise ValueError(f"\nError: id repetido {id_perro}")
        else:
            ids.add(id_perro)

        # Validar que machos no tengan celo
        if sexo == "M" and celo:
            raise ValueError(f"\nError: macho {id_perro} no puede estar en celo=1")

        perros.append(Perro(id_perro, sexo, celo, enfermo))

    return Instancia(n, perros)

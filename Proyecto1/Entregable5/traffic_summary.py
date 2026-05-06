def construir_resumen_trafico(mud_file):
    print("\n Resumen de trafico")
    resumen = []

    for acl in mud_file.acl_lists:
        for ace in acl.aces:
            accion = "N/A"
            if isinstance(ace.actions, dict):
                accion = ace.actions.get("forwarding", "N/A")

            fila = {
                "sentido": acl.name,
                "direccion": acl.type,
                "protocolo": "N/A",
                "puerto": "N/A",
                "accion": accion
            }
            resumen.append(fila)
    return resumen


def imprimir_tabla_trafico(resumen):
    print("\n Tabla de trafico:")

    encabezados = ["Sentido", "Direccion", "Protocolo", "Puerto", "Accion"]

    # ancho por columna (esto con la finalidad de tener un mayor orden visual)
    ancho_columnas = [35, 20, 12, 8, 10]

    # Construir el contenido a imprimir
    columnas_principales = [] # Sentido | Direccion | Protocolo | Puerto | Accion

    # zip se utiliza para combinar dos o más iterables, como listas, diccionarios.. 
    # Referencia de: 
    # https://www-geeksforgeeks-org.translate.goog/python/zip-in-python/?_x_tr_sl=en&_x_tr_tl=es&_x_tr_hl=es&_x_tr_pto=tc&_x_tr_hist=true
    
    for header, width in zip(encabezados, ancho_columnas):
        # Ajusta al ancho correspondiente
        columnas_principales.append(header.ljust(width))

    # Une las partes con separadores | para dividir el contenido entre las columnas, Sentido, Direccion...
    # Referencia de: https://www.w3schools.com/python/ref_string_join.asp 
    header_line = " | ".join(columnas_principales)
    print(header_line)
    print("-" * len(header_line))

    # Filas de la tabla
    for fila in resumen:
        row_parts = [] # para guardar los valores de la fila
        for value, width in zip(
            [
                str(fila.get("sentido", "—")),
                str(fila.get("direccion", "—")),
                str(fila.get("protocolo", "—")),
                str(fila.get("puerto", "—")),
                str(fila.get("accion", "—")),
            ],
            ancho_columnas,
        ):
            # Ajusta al ancho correspondiente
            row_parts.append(value.ljust(width))

        # Une las partes con separadores
        line = " | ".join(row_parts)
        print(line)
def construir_resumen_trafico(mud_file):
    print("\n Resumen de traafico")
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
    print("Sentido | Direccion | Protocolo | Puerto | Accion\n")
    for fila in resumen:
       print(f"{fila['sentido']} | {fila['direccion']} | {fila['protocolo']} | {fila['puerto']} | {fila['accion']}")
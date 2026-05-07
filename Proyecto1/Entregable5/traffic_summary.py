def construir_resumen_trafico(mud_file):
    resumen = []

    # Función para recorrer las ACL referenciadas por una política
    # recibe sentido del trafico
    def recorrido_acl_politicas(policy, sentido):
        if policy:
            for acl_referenciada in policy.acl_lists:
                # Buscar las ACL dentro de mud_file.acl_lists
                acl_obj = None
                for acl in mud_file.acl_lists:
                    if acl.name == acl_referenciada:
                        acl_obj = acl
                        break

                if acl_obj:
                    # Recorrer los ACE dentro de cada ACL
                    for ace in acl_obj.aces:
                        accion = "-"
                        if isinstance(ace.actions, dict):
                            accion = ace.actions.get("forwarding", "-")

                        # Direccion
                        direccion = "—"

                        # si el ACE tiene un bloque ipv4 puede contener una red o
                        # una direccion DNS de destino o una direccion DNS de origen
                        if "ipv4" in ace.matches:
                            ipv4_match = ace.matches["ipv4"]

                            if "destination-ipv4-network" in ipv4_match:
                                direccion = ipv4_match["destination-ipv4-network"]
                            elif "source-ipv4-network" in ipv4_match:
                                direccion = ipv4_match["source-ipv4-network"]
                            elif "ietf-acldns:dst-dnsname" in ipv4_match:
                                direccion = ipv4_match["ietf-acldns:dst-dnsname"]
                            elif "ietf-acldns:src-dnsname" in ipv4_match:
                                direccion = ipv4_match["ietf-acldns:src-dnsname"]

                        # si el ACE tiene un bloque ietf-mud:mud la direccion puede
                        # ser local-networks same-manufacturer o controller
                        if direccion == "—" and "ietf-mud:mud" in ace.matches:
                            mud_match = ace.matches["ietf-mud:mud"]

                            if "local-networks" in mud_match:
                                direccion = "local-networks"
                            elif "same-manufacturer" in mud_match:
                                direccion = "same-manufacturer"
                            elif "controller" in mud_match:
                                direccion = mud_match["controller"]

                        # si el ACE tiene un bloque eth se puede mostrar la MAC de destino o el ethertype para tener de referencia
                        if direccion == "—" and "eth" in ace.matches:
                            eth_match = ace.matches["eth"]

                            if "destination-mac-address" in eth_match:
                                direccion = eth_match["destination-mac-address"]
                            elif "ethertype" in eth_match:
                                direccion = eth_match["ethertype"]
                        
                        # Protocolo y puerto
                        protocolo = "—" # seria por si no hay, mostrar un -, en vez de N/A
                        puerto = "—"

                        # Si hay bloque ipv4 con protocolo
                        if "ipv4" in ace.matches:
                            protocolo = ace.matches["ipv4"].get("protocol", "—")

                        # Si hay bloque tcp, udp o eth se muestra como protocolo de transporte
                        if "tcp" in ace.matches:
                            protocolo = "tcp"

                            tcp_match = ace.matches["tcp"]
                            if "destination-port" in tcp_match:
                                puerto = tcp_match["destination-port"].get("port", "—")
                            else:
                                puerto = tcp_match.get("source-port", {}).get("port", "—")

                        elif "udp" in ace.matches:
                            protocolo = "udp"

                            udp_match = ace.matches["udp"]
                            if "destination-port" in udp_match:
                                puerto = udp_match["destination-port"].get("port", "—")
                            else:
                                puerto = udp_match.get("source-port", {}).get("port", "—")

                        elif "eth" in ace.matches:
                            protocolo = "eth"

                        fila = {
                            "sentido": sentido,
                            "direccion": direccion,
                            "protocolo": protocolo,
                            "puerto": puerto,
                            "accion": accion
                        }
                        resumen.append(fila)

    # Recorrer ACLs referenciadas por from_policy y to_policy
    recorrido_acl_politicas(
        mud_file.mud.from_policy,
        "Dispositivo hacia internet"
    )

    recorrido_acl_politicas(
        mud_file.mud.to_policy,
        "Internet hacia dispositivo"
    )

    return resumen

def imprimir_tabla_trafico(resumen):
    print("\n Tabla de trafico:")

    encabezados = ["Sentido", "Direccion", "Protocolo", "Puerto", "Accion"]

    # ancho por columna (esto con la finalidad de tener un mayor orden visual)
    ancho_columnas = [35, 35, 12, 8, 10]

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
import ply.yacc as yacc
from lexer import tokens
from objects import MudFile
from objects import Mud
from objects import ACE

class ParserValidationError(Exception):
    pass

# siguiendo la tarea corta 2 de la gramatica:
# raiz:
def p_file(p):
    'file : LBRACE mud_members RBRACE'
    data = p[2]
    # todo el bloque mud
    mud = data.get("ietf-mud:mud")
    # de aqui se obtiene la parte de los ACLs y si no existe devuelve un diccionario vacío {}
    acl_wrapper = data.get("ietf-access-control-list:access-lists", {})
    # de acl_wrapper se obtiene la lista de ACLs, si no existe devuelve una lista vacía []
    acl_lists = acl_wrapper.get("access-list") or acl_wrapper.get("acl") or []
    p[0] = MudFile(mud, acl_lists)

def p_mud_members(p):
    '''mud_members : mud_member
                   | mud_members COMMA mud_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
         # validar que no haya campos duplicados
        for k in p[3]:
            # si el campo ya existe en el diccionario acumulado, es un error
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado: {k}")
        # si no hay duplicados, combinamos los diccionarios
        p[0] = {**p[1], **p[3]}

# CAMPOS ROOT
def p_mud_member(p):
    '''mud_member : IETF_MUD_MUD COLON mud_object
                  | IETF_ACCESS_CONTROL_LIST_ACCESS_LISTS COLON acl_lists_wrapper'''
    p[0] = {p[1]: p[3]}

# ietf-mud:mud
def p_mud_object(p):
    'mud_object : LBRACE mud_content_list RBRACE'
    
    contenido = p[2]

    campos_obligatorios = {
        "mud-version",
        "mud-url",
        "last-update",
        "cache-validity"
    }

    faltantes = []

    for campo in campos_obligatorios:
        if campo not in contenido:
            faltantes.append(campo)

    tiene_from = "from-device-policy" in contenido
    tiene_to = "to-device-policy" in contenido

    if not tiene_from and not tiene_to:
        faltantes.append("from-device-policy o to-device-policy")

    if len(faltantes) > 0:
        raise ParserValidationError(
            "Faltan campos obligatorios en ietf-mud:mud: " + ", ".join(faltantes)
        )
    version = contenido.get("mud-version")
    url = contenido.get("mud-url")
    last_update = contenido.get("last-update")
    cache_validity = contenido.get("cache-validity")
    from_policy = contenido.get("from-device-policy")
    to_policy = contenido.get("to-device-policy")
    opcionales = {}
    # nos da la clave y el valor de cada campo  
    for key, valor in contenido.items():
        # si la clave no esta aqui es opcional y se agrega al diccionario de opcionales
        if key not in campos_obligatorios and key not in {
            "from-device-policy",
            "to-device-policy"
        }: opcionales[key] = valor
    # se crea el objeto Mud con los campos obligatorios y opcionales
    p[0] = Mud(version, url, last_update, cache_validity, from_policy, to_policy, opcionales)
    #p[0] = contenido

def p_mud_content_list(p):
    '''mud_content_list : mud_content
                        | mud_content_list COMMA mud_content'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        # validar que no haya campos duplicados
        for k in p[3]:
            # si el campo ya existe en el diccionario acumulado, es un error
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado: {k}")
        # si no hay duplicados, combinamos los diccionarios
        p[0] = {**p[1], **p[3]}

# aqui justo en este lugar tenemos estos campos tanto opcionales como obligatorios
# opcionales mud-signature, systeminfo, documentation, is-supported, mfg-name, 
# model-name, extensions, controller, samemanufacturer, policy, 
# from-device-policy / to-device-policy, extensions

def p_mud_content(p):
    '''mud_content : STRING_KEYS COLON string_value
                   | URL_KEYS COLON url_value
                   | NUMBER_KEYS COLON number_value
                   | LAST_UPDATE COLON datetime_value
                   | IS_SUPPORTED COLON bool_value
                   | EXTENSIONS COLON extensions_array
                   | POLICIES_KEYS COLON policy_item'''
    
    if p[1] in ["name", "type", "log", "port"]:
        raise ParserValidationError(
            f"Campo invalido en el bloque principal ietf-mud:mud: '{p[1]}'"
        )

    if p[1] == "controller":
        raise ParserValidationError(
            "El campo 'controller' no es valido en el bloque principal ietf-mud:mud"
        )

    p[0] = {p[1]: p[3]}

# TODO: agregar las reglas al resto
# EXTENSIONS

def p_extensions_array(p):
    '''extensions_array : LBRACKET RBRACKET
                        | LBRACKET extensions_list RBRACKET''' 
    # si es un array vacío, devolvemos una lista vacía
    if len(p) == 3:
        p[0] = [] 
    # sino se usa extension list 
    else: 
        p[0] = p[2]
   
def p_extensions_list(p):
    '''extensions_list : string_value
                       | extensions_list COMMA string_value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[3] in p[1]:
            raise ParserValidationError(f"Elemento duplicado en extensiones: {p[3]}")
        # si no hay duplicados, agregamos el nuevo elemento a la lista
        p[0] = p[1] + [p[3]]

# ACL WRAPPER

def p_acl_lists_wrapper(p):
    '''acl_lists_wrapper : LBRACE ACCESS_LIST COLON acl_list_array RBRACE 
                            | LBRACE ACL COLON acl_list_array RBRACE'''
    # usa p[2] para el nombre del campo y p[4] para el valor 
    p[0] = {p[2]: p[4]}

def p_acl_list_array(p):
    'acl_list_array : LBRACKET acl_list_items RBRACKET'
    # devuelve la lista de items de ACL
    p[0] = p[2]

def p_acl_list_items(p):
    '''acl_list_items : acl_list_item
                      | acl_list_items COMMA acl_list_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if "name" in p[3]:
            nombre_nuevo = p[3]["name"]

            for item in p[1]:
                if "name" in item and item["name"] == nombre_nuevo:
                    raise ParserValidationError(
                        f"ACL duplicada con name: '{nombre_nuevo}'"
                    )

        p[0] = p[1] + [p[3]]

def p_acl_list_item(p):
    'acl_list_item : LBRACE acl_list_members RBRACE'
    p[0] = p[2]

def p_acl_list_members(p):
    '''acl_list_members : acl_list_member
                        | acl_list_members COMMA acl_list_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado en acl_list_members: {k}")
        # si no hay duplicados, combinamos los diccionarios
        p[0] = {**p[1], **p[3]}

def p_acl_list_member(p):
    '''acl_list_member : STRING_KEYS COLON string_value
                       | ACES COLON ace_wrapper'''
    
    if p[1] == "name" or p[1] == "type":
        p[0] = {p[1]: p[3]}
    elif p[1] == "aces":
        p[0] = {p[1]: p[3]}
    else:
        raise ParserValidationError(
            f"Campo invalido dentro de un acl: '{p[1]}'"
        )
    
# ACE
# contenedor de reglas individual
def p_ace_wrapper(p):
    'ace_wrapper : LBRACE ace_inner RBRACE'
    p[0] = p[2]

def p_ace_inner(p): # dentro de ace no hay aces
    'ace_inner : ACE COLON ace_array'
    p[0] = {p[1]: p[3]}

def p_ace_array(p):
    'ace_array : LBRACKET ace_items RBRACKET'
    p[0] = p[2]

# implementando clases y objetos
def p_ace_items(p):
    '''ace_items : ace_item
                 | ace_items COMMA ace_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        nombre_nuevo = p[3].name

        for item in p[1]:
            if item.name == nombre_nuevo:
                raise ParserValidationError(
                    f"ACE duplicado con name: '{nombre_nuevo}'"
                )

        p[0] = p[1] + [p[3]]

# implementando clases y objetos
def p_ace_item(p):
    'ace_item : LBRACE ace_members RBRACE'
    
    datos = p[2]

    if "name" not in datos:
        raise ParserValidationError(
            "El ACE no contiene el campo obligatorio 'name'"
        )

    name = datos["name"]
    matches = datos.get("matches", {}) # busca matches y si no lo encuentra devuelve diccionario vacio por defecto
    actions = datos.get("actions", {})

    p[0] = ACE(name, matches, actions)

def p_ace_members(p):
    '''ace_members : ace_member
                   | ace_members COMMA ace_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado en ace_members: {k}")
        p[0] = {**p[1], **p[3]}

# puede tener aqui solamente campos como STRING_KEYS, MATCHES o ACTIONS
def p_ace_member(p):
    '''ace_member : STRING_KEYS COLON string_value
                  | MATCHES COLON matches_object
                  | ACTIONS COLON actions_object'''
    
    if p[1] == "name":
        p[0] = {p[1]: p[3]}
    elif p[1] == "matches" or p[1] == "actions":
        p[0] = {p[1]: p[3]}
    else:
        raise ParserValidationError(
            f"Campo invalido dentro de un ace: '{p[1]}'"
        )
    
# MATCHES 
# objeto de condiciones

def p_matches_object(p):
    '''matches_object : LBRACE matches_members RBRACE
                      | LBRACE RBRACE'''
    if len(p) == 3:
        p[0] = {}
    else:
        p[0] = p[2]

def p_matches_members(p):
    '''matches_members : matches_member
                       | matches_members COMMA matches_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado en matches_members: {k}")
        p[0] = {**p[1], **p[3]}

def p_matches_member(p):
    '''matches_member : IETF_MUD_MUD COLON mud_match_object
                      | IPV4_KEY COLON ipv4_object
                      | PROTOCOL_KEYS COLON generic_protocol_object'''
    
    if p[1] == "ietf-mud:mud" or p[1] == "ipv4":
        p[0] = {p[1]: p[3]}
    elif p[1] == "tcp" or p[1] == "udp":
        validar_transport_object(p[3], p[1])
        p[0] = {p[1]: p[3]}
    elif p[1] == "eth":
        validar_eth_object(p[3])
        p[0] = {p[1]: p[3]}
    else:
        raise ParserValidationError(f"Campo inválido dentro de matches: '{p[1]}'")
    
def p_mud_match_object(p):
    'mud_match_object : LBRACE mud_match_members RBRACE'
    p[0] = p[2]

def p_mud_match_members(p):
    '''mud_match_members : mud_match_member
                         | mud_match_members COMMA mud_match_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"campo duplicado en mud_match_members: {k}")
        p[0] = {**p[1], **p[3]}

def p_mud_match_member(p):
    '''mud_match_member : URL_KEYS COLON url_value
                        | NULL_KEYS COLON null_array'''
    
    if p[1] == "controller":
        p[0] = {p[1]: p[3]}
    elif p[1] == "local-networks" or p[1] == "same-manufacturer":
        p[0] = {p[1]: p[3]}
    else:
        raise ParserValidationError(
            f"Campo inválido dentro de ietf-mud:mud en matches: '{p[1]}'"
        )
    
def p_null_array(p):
    'null_array : LBRACKET null_list RBRACKET'
    p[0] = p[2]

def p_null_list(p):
    '''null_list : null_value
                 | null_list COMMA null_value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[3] in p[1]:
            raise ParserValidationError(f"Elemento duplicado en null_array: {p[3]}")
        p[0] = p[1] + [p[3]]

# ACTIONS

def p_actions_object(p):
    'actions_object : LBRACE actions_members RBRACE'
    p[0] = p[2]


def p_actions_members(p):
    '''actions_members : actions_member
                       | actions_members COMMA actions_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado: {k}")
        p[0] = {**p[1], **p[3]}

def p_actions_member(p):
    'actions_member : FORWARDING COLON action_value'
    p[0] = {p[1]: p[3]}

# es un objeto
def p_policy_item(p):
    'policy_item : LBRACE ACCESS_LISTS COLON access_lists_object RBRACE'
    
    if p[2] != "access-lists":
        raise ParserValidationError(
            f"Se esperaba 'access-lists' dentro de policy y se encontro '{p[2]}'"
        )
    p[0] = {p[2]: p[4]}

# deriva de policy item todo esto
def p_access_lists_object(p): 
    'access_lists_object : LBRACE ACCESS_LIST COLON name_list_array RBRACE'
    
    if p[2] != "access-list":
        raise ParserValidationError(
            f"Se esperaba 'access-list' y se encontro '{p[2]}'"
        )
    p[0] = {p[2]: p[4]}

def p_name_list_array(p):
    'name_list_array : LBRACKET name_items RBRACKET'
    p[0] = p[2]

def p_name_items(p):
    '''name_items : name_item
                  | name_items COMMA name_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        nombre_nuevo = p[3]["name"]

        for item in p[1]:
            if item["name"] == nombre_nuevo:
                raise ParserValidationError(
                    f"Nombre duplicado en access-list de policy: '{nombre_nuevo}'"
                )

        p[0] = p[1] + [p[3]]

def p_name_item(p):
    'name_item : LBRACE STRING_KEYS COLON string_value RBRACE'
    
    if p[2] != "name":
        raise ParserValidationError(f"Se esperaba 'name' y se encontro '{p[2]}'")
    
    p[0] = {p[2]: p[4]}

# objetos de ipv4 y protocolo
# representa un bloque de condiciones para ipv4
def p_ipv4_object(p):
    'ipv4_object : LBRACE ipv4_members RBRACE'
    p[0] = p[2]

# Representa un bloque con protocolo TCP UDP
"""def p_protocol_object(p):
    'protocol_object : LBRACE protocol_members RBRACE'
    p[0] = p[2]"""

def p_generic_protocol_object(p):
    'generic_protocol_object : LBRACE generic_protocol_members RBRACE'
    p[0] = p[2]

def p_generic_protocol_members(p):
    '''generic_protocol_members : generic_protocol_member
                                | generic_protocol_members COMMA generic_protocol_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado en objeto de protocolo: {k}")
        p[0] = {**p[1], **p[3]}


def p_generic_protocol_member(p):
    '''generic_protocol_member : PORT_DIR_KEYS COLON port_value
                               | IETF_MUD_DIRECTION_INITIATED COLON direction_value
                               | ETHERTYPE_KEY COLON ethertype_value
                               | DESTINATION_MAC_ADDRESS COLON mac_value'''
    p[0] = {p[1]: p[3]}

"""
def p_protocol_member(p):
    '''protocol_member : PORT_DIR_KEYS COLON port_value
                       | IETF_MUD_DIRECTION_INITIATED COLON direction_value
                       | ETHERTYPE_KEY COLON ethertype_value
                       | DESTINATION_MAC_ADDRESS COLON mac_value'''
    p[0] = {p[1]: p[3]}

#propiedades del protocolo
def p_protocol_members(p):
    '''protocol_members : protocol_member
                        | protocol_members COMMA protocol_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado: {k}")
        p[0] = {**p[1], **p[3]}
"""

def p_ipv4_member(p):
    '''ipv4_member : DNS_KEYS COLON dns_value
                   | DESTINATION_IPV4_NETWORK COLON ipv4_value
                   | PROTOCOL COLON number_value'''
    p[0] = {p[1]: p[3]}

# Valor de puerto
def p_port_value(p):
    'port_value : LBRACE OPERATOR COLON operator_value COMMA NUMBER_KEYS COLON number_value RBRACE'
    
    if p[6] != "port":
        raise ParserValidationError(f"Se esperaba 'port' y se encontro '{p[6]}'")
    
    p[0] = {p[2]: p[4], p[6]: p[8]}

# Valor de protocolo
def p_ipv4_members(p):
    '''ipv4_members : ipv4_member
                    | ipv4_members COMMA ipv4_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise ParserValidationError(f"Campo duplicado: {k}")
        p[0] = {**p[1], **p[3]}

# nuevo 
#def p_action_value(p):
    #'action_value : RESERVED_VALUES'
    
   # if p[1] not in ["accept", "drop", "reject"]:
        #raise ParserValidationError(
          #  f"Valor invalido para forwarding: '{p[1]}'. Se esperaba accept, drop o reject"
       # )
    
   # p[0] = p[1]

def p_action_value(p):
    'action_value : RESERVED_VALUES'
    
    #print("DEBUG action_value:", p[1])

    if p[1] not in ["accept", "drop", "reject"]:
        raise ParserValidationError(
            f"Valor invalido para forwarding: '{p[1]}'. Se esperaba accept, drop o reject"
        )
    
    p[0] = p[1]

def p_operator_value(p):
    'operator_value : RESERVED_VALUES'
    
    if p[1] != "eq":
        raise ParserValidationError(
            f"Valor invalido para operator: '{p[1]}'. Se esperaba eq"
        )
    
    p[0] = p[1]


def p_direction_value(p):
    'direction_value : RESERVED_VALUES'
    
    if p[1] not in ["from-device", "to-device"]:
        raise ParserValidationError(
            f"Valor inválido para ietf-mud:direction-initiated: '{p[1]}'. "
            f"Se esperaba from-device o to-device"
        )
    
    p[0] = p[1]

# TIPOS

def p_string_value(p):
    'string_value : STRING'
    p[0] = p[1]

def p_number_value(p):
    'number_value : NUMBER'
    p[0] = p[1]

def p_bool_value(p):
    'bool_value : BOOLEAN'
    p[0] = p[1]

def p_null_value(p):
    'null_value : NULL'
    p[0] = p[1]

def p_url_value(p):
    'url_value : URL'
    p[0] = p[1]

def p_dns_value(p):
    'dns_value : DNS'
    p[0] = p[1]

def p_ipv4_value(p):
    'ipv4_value : IPV4'
    p[0] = p[1]

def p_datetime_value(p):
    'datetime_value : DATETIME'
    p[0] = p[1]

def p_mac_value(p):
    'mac_value : MAC_ADDRESS'
    p[0] = p[1]

def p_ethertype_value(p):
    'ethertype_value : ETHERTYPE'
    p[0] = p[1]

def validar_transport_object(objeto, nombre_protocolo):
    claves_validas = {
        "source-port",
        "destination-port",
        "ietf-mud:direction-initiated"
    }

    for clave in objeto:
        if clave not in claves_validas:
            raise ParserValidationError(
                f"Campo inválido dentro de '{nombre_protocolo}': '{clave}'"
            )

def validar_eth_object(objeto):
    claves_validas = {
        "destination-mac-address",
        "ethertype"
    }

    for clave in objeto:
        if clave not in claves_validas:
            raise ParserValidationError(
                f"Campo inválido dentro de 'eth': '{clave}'"
            )
        
# Manejo de errores
'''def p_error(p):
    if p:
        print(f"\n Error sintactico en la linea {p.lineno}: "
              f"El token '{p.type}' con valor '{p.value}' no se esperaba en este lugar")
    else:
        print("\n Error sintactico: fin de archivo inesperado. Faltan llaves de cierre")'''

def p_error(p):
    if p:
        raise SyntaxError(
            f"Error sintactico en la linea {p.lineno}: "
            f"el token '{p.type}' con valor '{p.value}' no se esperaba en este lugar"
        )
    else:
        raise SyntaxError(
            "Error sintactico: fin de archivo inesperado. "
            "Posible falta de llave o corchete de cierre"
        )
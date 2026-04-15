import ply.yacc as yacc
from lexer import tokens
from lexer import lexer

# siguiendo la tarea corta 2 de la gramatica:
# raiz:
def p_file(p):
    'file : LBRACE mud_members RBRACE'
    p[0] = p[2]

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
                raise SyntaxError(f"Campo duplicado: {k}")
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
    p[0] = p[2]


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
                raise SyntaxError(f"Campo duplicado: {k}")
        # si no hay duplicados, combinamos los diccionarios
        p[0] = {**p[1], **p[3]}

# aqui justo en este lugar tenemos estos campos tanto opcionales como obligatorios
# opcionales mud-signature, systeminfo, documentation, is-supported, mfg-name, model-name, extensions, controller, samemanufacturer, policy, 
# from-device-policy / to-device-policy, extensions

def p_mud_content(p):
    '''mud_content : STRING_KEYS COLON string_value
                   | URL_KEYS COLON url_value
                   | NUMBER_KEYS COLON number_value
                   | LAST_UPDATE COLON datetime_value
                   | IS_SUPPORTED COLON bool_value
                   | EXTENSIONS COLON extensions_array
                   | POLICIES_KEYS COLON policy_item
                   | NULL_KEYS COLON null_array
                   | FORWARDING COLON string_value'''
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
    else: p[2]
   
def p_extensions_list(p):
    '''extensions_list : string_value
                       | extensions_list COMMA string_value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[3] in p[1]:
            raise SyntaxError(f"Elemento duplicado en extensiones: {p[3]}")
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
        if p[3] in p[1]:
            raise SyntaxError(f"Elemento duplicado en acl_list_items: {p[3]}")
        # si no hay duplicados, agregamos el nuevo elemento a la lista
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
                raise SyntaxError(f"Campo duplicado en acl_list_members: {k}")
        # si no hay duplicados, combinamos los diccionarios
        p[0] = {**p[1], **p[3]}

# lo que puede en este lugar es STRING_KEYS, ACL, ACES, ACE o POLICIES_KEYS
def p_acl_list_member(p):
    '''acl_list_member : STRING_KEYS COLON string_value
                       | ACL COLON string_value
                       | ACES COLON ace_wrapper
                       | ACE COLON ace_array
                       | POLICIES_KEYS COLON policy_item'''
    p[0] = {p[1]: p[3]}

# ACE
# contenedor de reglas individual
def p_ace_wrapper(p):
    'ace_wrapper : LBRACE ace_inner RBRACE'
    p[0] = p[2]

# puede tener ACE o ACES 
def p_ace_inner(p):
    '''ace_inner : ACE COLON ace_array
                 | ACES COLON ace_array'''
    p[0] = {p[1]: p[3]}

def p_ace_array(p):
    'ace_array : LBRACKET ace_items RBRACKET'
    p[0] = p[2]

def p_ace_items(p):
    '''ace_items : ace_item
                 | ace_items COMMA ace_item'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        if p[3] in p[1]:
            raise SyntaxError(f"Elemento duplicado en ace_items: {p[3]}")
        p[0] = p[1] + [p[3]]

def p_ace_item(p):
    'ace_item : LBRACE ace_members RBRACE'
    p[0] = p[2]

def p_ace_members(p):
    '''ace_members : ace_member
                   | ace_members COMMA ace_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise SyntaxError(f"Campo duplicado en ace_members: {k}")
        p[0] = {**p[1], **p[3]}

# puede tener aqui solamente campos como STRING_KEYS, MATCHES o ACTIONS
def p_ace_member(p):
    '''ace_member : STRING_KEYS COLON string_value
                  | MATCHES COLON matches_object
                  | ACTIONS COLON actions_object'''
    p[0] = {p[1]: p[3]}

# MATCHES 
# objeto de condiciones

def p_matches_object(p):
    'matches_object : LBRACE matches_members RBRACE'
    p[0] = p[2]


def p_matches_members(p):
    '''matches_members : matches_member
                       | matches_members COMMA matches_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise SyntaxError(f"Campo duplicado en matches_members: {k}")
        p[0] = {**p[1], **p[3]}

# puede tener solamente campos como IPV4_KEY, PROTOCOL_KEYS, IETF_MUD_DIRECTION_INITIATED, DNS_KEYS, DESTINATION_IPV4_NETWORK, DESTINATION_MAC_ADDRESS, ETHERTYPE_KEY, STRING o NULL_KEYS
# ademas se dice que valor es el que puede tener
def p_matches_member(p):
    '''matches_member : IPV4_KEY COLON ipv4_object
                      | PROTOCOL_KEYS COLON protocol_object
                      | IETF_MUD_DIRECTION_INITIATED COLON RESERVED_VALUES
                      | DNS_KEYS COLON dns_value
                      | DESTINATION_IPV4_NETWORK COLON ipv4_value
                      | DESTINATION_MAC_ADDRESS COLON mac_value
                      | ETHERTYPE_KEY COLON ethertype_value
                      | STRING COLON bool_value
                      | NULL_KEYS COLON null_array
                      | IETF_MUD_MUD COLON mud_object'''
    p[0] = {p[1]: p[3]}

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
            raise SyntaxError(f"Elemento duplicado en null_array: {p[3]}")
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
                raise SyntaxError(f"Campo duplicado: {k}")
        p[0] = {**p[1], **p[3]}

def p_actions_member(p):
    'actions_member : FORWARDING COLON RESERVED_VALUES'
    p[0] = {p[1]: p[3]}


def p_policy_item(p):
    '''policy_item : LBRACE POLICY COLON string_value RBRACE
                   | LBRACE ACL COLON acl_list_array RBRACE
                   | LBRACE ACCESS_LIST COLON acl_list_array RBRACE
                   | LBRACE ACCESS_LISTS COLON acl_lists_wrapper RBRACE'''
    p[0] = {p[2]: p[4]}

# objetos de ipv4 y protocolo
#representa un bloque de condiciones para ipv4
def p_ipv4_object(p):
    'ipv4_object : LBRACE ipv4_members RBRACE'
    p[0] = p[2]

#epresenta un bloquecon confi de protocolo TCP UDP
def p_protocol_object(p):
    'protocol_object : LBRACE protocol_members RBRACE'
    p[0] = p[2]

#propiedades del protocolo
def p_protocol_members(p):
    '''protocol_members : protocol_member
                        | protocol_members COMMA protocol_member'''
    if len(p) == 2:
        p[0] = p[1]
    else:
        for k in p[3]:
            if k in p[1]:
                raise SyntaxError(f"Campo duplicado: {k}")
        p[0] = {**p[1], **p[3]}

# Propiedad individual del protocolo puede ser puerto, operador o nmero
def p_protocol_member(p):
    '''protocol_member : PORT_DIR_KEYS COLON port_value
                       | OPERATOR COLON RESERVED_VALUES
                       | NUMBER_KEYS COLON number_value
                       | DESTINATION_MAC_ADDRESS COLON mac_value
                       | ETHERTYPE_KEY COLON ethertype_value
                       | IETF_MUD_DIRECTION_INITIATED COLON RESERVED_VALUES'''
    p[0] = {p[1]: p[3]}

# Valor de puerto
def p_port_value(p):
    '''port_value : LBRACE NUMBER_KEYS COLON number_value RBRACE
                  | LBRACE OPERATOR COLON RESERVED_VALUES COMMA NUMBER_KEYS COLON number_value RBRACE'''
    if len(p) == 6:
        p[0] = {p[2]: p[4]}
    else:
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
                raise SyntaxError(f"Campo duplicado: {k}")
        p[0] = {**p[1], **p[3]}

# campos de ipv4 pueden ser DNS_KEYS, DESTINATION_IPV4_NETWORK, DESTINATION_MAC_ADDRESS, PROTOCOL_KEYS o NUMBER_KEYS
def p_ipv4_member(p):
    '''ipv4_member : DNS_KEYS COLON dns_value
                   | DESTINATION_IPV4_NETWORK COLON ipv4_value
                   | DESTINATION_MAC_ADDRESS COLON mac_value
                   | PROTOCOL_KEYS COLON number_value
                   | NUMBER_KEYS COLON number_value'''
    p[0] = {p[1]: p[3]}

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

# ERROR
def p_error(p):
    if p:
        raise SyntaxError(f"Error en línea {p.lineno}: '{p.value}' no es válido en este contexto")
    else:
        raise SyntaxError("Error: fin inesperado del archivo")
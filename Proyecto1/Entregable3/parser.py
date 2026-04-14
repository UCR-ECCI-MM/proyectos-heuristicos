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
                   | NULL_KEYS COLON null_value
                   | FORWARDING COLON string_value'''
    p[0] = {p[1]: p[3]}


# EXTENSIONS

def p_extensions_array(p):
    '''extensions_array : LBRACKET RBRACKET
                       '''
   


def p_extensions_list(p):
    '''extensions_list : string_value
                       '''



# ACL WRAPPER

def p_acl_lists_wrapper(p):
    'acl_lists_wrapper : LBRACE ACCESS_LIST COLON acl_list_array RBRACE'
    p[0] = {p[2]: p[4]}


def p_acl_list_array(p):
    'acl_list_array : LBRACKET acl_list_items RBRACKET'
    p[0] = p[2]


def p_acl_list_items(p):
    '''acl_list_items : acl_list_item
                      '''
   


def p_acl_list_item(p):
    'acl_list_item : LBRACE acl_list_members RBRACE'
   


def p_acl_list_members(p):
    '''acl_list_members : acl_list_member
                        '''
   


def p_acl_list_member(p):
    '''acl_list_member : STRING_KEYS COLON string_value
                       | ACL COLON string_value
                       | ACES COLON ace_wrapper
                       | ACE COLON ace_array
                       | POLICIES_KEYS COLON policy_item'''
    p[0] = {p[1]: p[3]}


# ACE

def p_ace_wrapper(p):
    'ace_wrapper : LBRACE ace_inner RBRACE'
    p[0] = p[2]


def p_ace_inner(p):
    '''ace_inner : ACE COLON ace_array
                 '''
    


def p_ace_array(p):
    'ace_array : LBRACKET ace_items RBRACKET'
    p[0] = p[2]


def p_ace_items(p):
    '''ace_items : ace_item'''
    


def p_ace_item(p):
    'ace_item : LBRACE ace_members RBRACE'
   


def p_ace_members(p):
    '''ace_members : ace_member'''
    


def p_ace_member(p):
    '''ace_member : STRING_KEYS COLON string_value
                '''


# MATCHES 

def p_matches_object(p):
    'matches_object : LBRACE matches_members RBRACE'
    p[0] = p[2]


def p_matches_members(p):
    '''matches_members : matches_member
                       '''
    

def p_matches_member(p):
    '''matches_member : IPV4_KEY COLON ipv4_object
                      '''
    
  

# ACTIONS

def p_actions_object(p):
    'actions_object : LBRACE actions_members RBRACE'
    p[0] = p[2]


def p_actions_members(p):
    '''actions_members : actions_member'''
   


def p_actions_member(p):
    'actions_member : FORWARDING COLON RESERVED_VALUES'
    p[0] = {p[1]: p[3]}

def p_policy_item(p):
    '''policy_item : LBRACE POLICY COLON string_value RBRACE
                   '''
    

def p_ipv4_object(p):
    'ipv4_object : LBRACE ipv4_members RBRACE'
    p[0] = p[2]

def p_protocol_object(p):
    'protocol_object : LBRACE protocol_members RBRACE'
    p[0] = p[2]


def p_protocol_members(p):
    '''protocol_members : protocol_member
                       '''
   

def p_port_value(p):
    '''port_value : LBRACE NUMBER_KEYS COLON number_value RBRACE
                 '''
   

def p_protocol_member(p):
    '''protocol_member : PORT_DIR_KEYS COLON port_value
                     '''
   

def p_ipv4_members(p):
    '''ipv4_members : ipv4_member
                '''



def p_ipv4_member(p):
    '''ipv4_member : DNS_KEYS COLON dns_value
                   '''

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
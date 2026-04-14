import ply.yacc as yacc
from lexer import lexer
from lexer import tokens

# regla inicial del archivo, un archivo MUD esta formado por una lista de campos principales
def p_file(p):
    'file : LBRACE field_list RBRACE'
    p[0] = p[2]

# una lista de campos esta conformada por uno o mas campos del archivo MUD
def p_field_list(p):
    '''field_list : field 
                  | field_list COMMA field''' # recursivo, a la lista se le agrega el campo
    
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = {**p[1], **p[3]}

# un campo en un archivo mud esta definido por una clave con valor asociado
def p_field(p):
    '''field : STRING COLON value
             | NUMBER_KEYS COLON value
             | URL_KEYS COLON value
             | STRING_KEYS COLON value
             | DNS_KEYS COLON value
             | POLICIES_KEYS COLON value
             | PORT_DIR_KEYS COLON value
             | NULL_KEYS COLON value
             | LAST_UPDATE COLON value
             | IS_SUPPORTED COLON value
             | DESTINATION_IPV4_NETWORK COLON value
             | DESTINATION_MAC_ADDRESS COLON value
             | ETHERTYPE_KEY COLON value
             | IETF_MUD_DIRECTION_INITIATED COLON value
             | OPERATOR COLON value
             | FORWARDING COLON value
             | EXTENSIONS COLON value
             | IETF_MUD_MUD COLON value
             | IETF_ACCESS_CONTROL_LIST_ACCESS_LISTS COLON value
             | ACCESS_LISTS COLON value
             | ACCESS_LIST COLON value
             | ACL COLON value
             | ACES COLON value
             | ACE COLON value
             | MATCHES COLON value
             | ACTIONS COLON value
             | IPV4_KEY COLON value
             | POLICY COLON value'''
    p[0] = {p[1]: p[3]}

# tipos de valores generales
def p_value(p):
    '''value : STRING
             | NUMBER
             | BOOLEAN
             | NULL
             | DATETIME
             | MAC_ADDRESS
             | ETHERTYPE
             | IPV4
             | URL
             | DNS
             | objeto
             | lista'''
    p[0] = p[1]

def p_objeto(p):
    'objeto : LBRACE field_list RBRACE'
    p[0] = p[2]

def p_lista(p):
    'lista : LBRACKET value_list RBRACKET'
    p[0] = p[2]

def p_value_list(p):
    '''value_list : value
                  | value_list COMMA value'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]
import ply.lex as lex
import ply.yacc as yacc

# tokens types
symbols = ["LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COLON", "COMMA"]

literal_values = ["BOOLEAN", "NUMBER", "NULL", "STRING", "DATETIME"]

addresses = ["IPV4", "URL", "DNS"] # ip hace referencia al tipo ipv4 mas especificamente

keys = ["NUMBER_KEYS", "URL_KEYS", "STRING_KEYS", "DNS_KEYS", "POLICIES_KEYS", 
        "PORT_DIR_KEYS", "NULL_KEYS", "RESERVED_VALUES", "PROTOCOL_KEYS"]

# maps for key types
port_dir_keys = {
    "destination-port" : "PORT_DIR_KEYS", "source-port" : "PORT_DIR_KEYS"
}

null_keys = {
    "local-networks" : "NULL_KEYS", "same-manufacturer" : "NULL_KEYS"
}

reserved_values = {
    "eq" : "RESERVED_VALUES", "accept" : "RESERVED_VALUES"
}

number_keys = {"mud-version" : "NUMBER_KEYS", "cache-validity" : "NUMBER_KEYS",
               "protocol" : "NUMBER_KEYS", "port" : "NUMBER_KEYS"}

url_keys = {"mud-url" : "URL_KEYS", "mud-signature" : "URL_KEYS", 
            "documentation" : "URL_KEYS", "controller" : "URL_KEYS"}

string_keys = {"name" : "STRING_KEYS", "type" : "STRING_KEYS", "systeminfo" : "STRING_KEYS",
               "mfg-name" : "STRING_KEYS", "model-name" : "STRING_KEYS"}

dns_keys = {"ietf-acldns:dst-dnsname" : "DNS_KEYS", "ietf-acldns:src-dnsname": "DNS_KEYS"}

policies_keys = {"from-device-policy" : "POLICIES_KEYS", "to-device-policy" : "POLICIES_KEYS"}

protocol_keys = {"tcp" : "PROTOCOL_KEYS", "udp" : "PROTOCOL_KEYS", "eth" : "PROTOCOL_KEYS"}

# for unique keys
unique_keys = {
    "last-update" : "LAST_UPDATE",
    "is-supported" : "IS_SUPPORTED",
    "destination-ipv4-network" : "DESTINATION_IPV4_NETWORK",
    "destination-mac-address" : "DESTINATION_MAC_ADDRESS",
    "ethertype" : "ETHERTYPE",
    "ietf-mud:direction-initiated" : "IETF_MUD_DIRECTION_INITIATED",
    "operator" : "OPERATOR",
    "forwarding" : "FORWARDING",
    "extensions" : "EXTENSIONS", 
    "ietf-mud:mud" : "IETF_MUD_MUD",
    "ietf-access-control-list:access-lists" : "IETF_ACCESS_CONTROL_LIST_ACCESS_LISTS",
    "access-lists" : "ACCESS_LISTS",
    "access-list" : "ACCESS_LIST",
    "acl" : "ACL",
    "aces" : "ACES",
    "ace" : "ACE",
    "matches" : "MATCHES",
    "actions" : "ACTIONS",
    "ipv4" : "IPV4_KEY",
    "policy" : "POLICY"
}

reserved = { # desempaquetar diccionarios en un solo diccionario maestro para manipular
    **number_keys, **url_keys, **string_keys, **dns_keys, **policies_keys, **unique_keys,
         **port_dir_keys, **null_keys, **reserved_values, **protocol_keys
}

# complete token list for ply
tokens = symbols + literal_values + addresses + keys + list(unique_keys.values())

# symbols regex
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COLON = r":"
t_COMMA = r","

# agregar datetime y url antes de string para que no lo capture

#def t_DATETIME(t):
    #r'"(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?)"'
   # t.value = t.value.strip('"')
    #return t

def t_IPV4(t):
    # es 0.0.0.0/00 hasta 255.255.255/32, con comillas al inicio y al final
    r'"[0-2][0-5][0-5]\.[0-2][0-5][0-5]\.[0-2][0-5][0-5]\.[0-2][0-5][0-5]/(3[0-2]|[1-2]?[0-9])"'
    t.value = t.value.strip('"')
    return t

def t_URL(t):
    #empieza con http puede ser https, seguido de ://,luego cualquier combinacion de caracteres validos en una URL
    # y termina con comillas
    r'"https?://[a-zA-Z0-9:/.?=&%\-_~#@!]+"'
    t.value = t.value.strip('"')  
    return t

def t_DNS(t):
    # inicia en letra o numero, luego puede tener letras, numeros o guiones, seguido de un punto, y termina con una extension de 2 a
    # 24 caracteres para el .com o lo que sea, todo esto entre comillas
    r'"([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]?\.)+[a-zA-Z]{2,24}"'
    t.value = t.value.strip('"')
    return t

#def t_BOOLEAN(t):
   
   
    #return t

#def t_NULL(t):
   
    #t.value = None
    #return t

#def t_NUMBER(t):
    #r'\b\d+\b'
    #t.value = int(t.value)
    #return t

# funcion string va hasta el final del archivo y captura todo lo que queda entre comillas
def t_STRING(t):
    # regex strings
    # cualquier cadena que empiece y termine con quote se considera un string (hasta verificar si es una clave)
    r'"[^"]*"'

    value = t.value.split('"')[1] # quitar comillas de la palabra

    if value in reserved:
        t.type = reserved[value]

    return t

# A string containing ignored characters (spaces, tabs and newlines)
t_ignore = ' \t\n'
 
# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# creando el lexer
lexer = lex.lex()
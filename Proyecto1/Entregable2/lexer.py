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

# Comprobar que last-update tenga formato correcto de fecha/hora.
# "2026-03-07T12:00:00+00:00",
# "2025-04-01T17:53:34.611+11:00",
def t_DATETIME(t):
    r'"[0-9]{4}-((0[1-9])|(1[0-2]))-((0[1-9])|([12][0-9])|(3[01]))T((0[0-9])|(1[0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9]\+|([0-5][0-9]\.[1-9]{3,5}\+))([0-9]{2}:[0-9]{2})"'
    return t

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

def t_BOOLEAN(t):
    r'(true)|(false)'
    return t

def t_NULL(t):
    r"NULL"
    t.value = None
    return t

def t_NUMBER(t):
    r'\b\d+\b'
    t.value = int(t.value)
    return t

#def t_RESERVED_VALUE(t):
#    r'\b(accept|eq)\b'
#    return t

last_key = None
errores = []

def t_STRING(t):
    r'"[^"]*"'
    global last_key
    value = t.value.strip('"')
    if value in reserved:
        t.type = reserved[value]
        last_key = value  # guarda la clave para el siguiente token
    else:
        # validar según la clave anterior
        validar_valor(value, t.lineno)
    return t

# expresiones regulares 
ipv4_expr = r'"[0-2][0-5][0-5]\.[0-2][0-5][0-5]\.[0-2][0-5][0-5]\.[0-2][0-5][0-5]/(3[0-2]|[1-2]?[0-9])"'
dns_expr = r'"([a-zA-Z0-9][a-zA-Z0-9-]*[a-zA-Z0-9]?\.)+[a-zA-Z]{2,24}"'
url_expr = r'"https?://[a-zA-Z0-9:/.?=&%\-_~#@!]+"'

# ver si el valor que cayó en string es un error de formato.
def validar_valor(value, lineno):
    import re
    global last_key
    # mud-url y documentation deben ser URLs validas
    if last_key in url_keys:
        if not re.match(url_expr, value):
            errores.append(f"Línea {lineno}: URL invalida en '{last_key}' → '{value}'")

    # dns keys deben ser validos
    elif last_key in dns_keys:
        if not re.match(dns_expr, value):
            errores.append(f"Línea {lineno}: DNS invalido en '{last_key}' → '{value}'")

    # destination-ipv4-network debe ser IPv4 valida
    elif last_key == "destination-ipv4-network":
        if not re.match(ipv4_expr, value):
            errores.append(f"Línea {lineno}: IPv4 invalida en 'destination-ipv4-network' → '{value}'")

# Captura uno o más saltos de línea
# Referencia del ejemplo de calculadora
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# un string con caracteres a ignorar (espacios y tabs)
t_ignore = ' \t' 
 
# se agrega el error a la lista de errores y se salta el caracter ilegal
def t_error(t):
    errores.append(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

#cant de errores encontrados y reporte de los mismos
def reporte_lexico():
    print(f"\n Errores encontrados: {len(errores)}")
    if errores:
        print("\n  ERRORES:")
        for e in errores:
            print(f"{e}")

# creando el lexer
lexer = lex.lex()
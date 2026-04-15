import ply.lex as lex
import re

# tokens types
symbols = ["LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COLON", "COMMA"]

literal_values = ["BOOLEAN", "NUMBER", "NULL", "STRING", "DATETIME", "MAC_ADDRESS", "ETHERTYPE"]

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
    "eq" : "RESERVED_VALUES", "accept" : "RESERVED_VALUES",
    "from-device": "RESERVED_VALUES", "to-device": "RESERVED_VALUES",
    "drop" : "RESERVED_VALUES",
    "reject" : "RESERVED_VALUES",  
}

number_keys = {"mud-version" : "NUMBER_KEYS", "cache-validity" : "NUMBER_KEYS", "port" : "NUMBER_KEYS"}

url_keys = {"mud-url" : "URL_KEYS", "mud-signature" : "URL_KEYS", 
            "documentation" : "URL_KEYS", "controller" : "URL_KEYS"}

string_keys = {"name" : "STRING_KEYS", "type" : "STRING_KEYS", "systeminfo" : "STRING_KEYS",
               "mfg-name" : "STRING_KEYS", "model-name" : "STRING_KEYS","log": "STRING_KEYS"}

dns_keys = {"ietf-acldns:dst-dnsname" : "DNS_KEYS", "ietf-acldns:src-dnsname": "DNS_KEYS"}

policies_keys = {"from-device-policy" : "POLICIES_KEYS", "to-device-policy" : "POLICIES_KEYS"}

protocol_keys = {"tcp" : "PROTOCOL_KEYS", "udp" : "PROTOCOL_KEYS", "eth" : "PROTOCOL_KEYS"}

# para claves unicas
unique_keys = {
    "last-update" : "LAST_UPDATE",
    "is-supported" : "IS_SUPPORTED",
    "destination-ipv4-network" : "DESTINATION_IPV4_NETWORK",
    "destination-mac-address" : "DESTINATION_MAC_ADDRESS",
    "ethertype" : "ETHERTYPE_KEY",
    "ietf-mud:direction-initiated" : "IETF_MUD_DIRECTION_INITIATED",
    "operator" : "OPERATOR",
    "forwarding" : "FORWARDING",
    "extensions" : "EXTENSIONS", 
    "ietf-mud:mud" : "IETF_MUD_MUD",
    "ietf-access-control-list:access-lists" : "IETF_ACCESS_CONTROL_LIST_ACCESS_LISTS",
    #"ietf-access-control-list:acls": "IETF_ACCESS_CONTROL_LIST_ACCESS_LISTS",
    "access-lists" : "ACCESS_LISTS",
    "access-list" : "ACCESS_LIST",
    "acl" : "ACL",
    "aces" : "ACES",
    "ace" : "ACE",
    "matches" : "MATCHES",
    "actions" : "ACTIONS",
    "ipv4" : "IPV4_KEY",
    "protocol" : "PROTOCOL"
}

reserved = { # desempaquetar diccionarios en un solo diccionario maestro para manipular
    **number_keys, **url_keys, **string_keys, **dns_keys, **policies_keys, **unique_keys,
         **port_dir_keys, **null_keys, **reserved_values, **protocol_keys
}

# lista de tokens completa para ply
tokens = symbols + literal_values + addresses + keys + list(unique_keys.values())

# symbols regex
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COLON = r":"
t_COMMA = r","

# lista para almacenar errores léxicos
errores = []

# Comprobar que last-update tenga formato correcto de fecha/hora.
# "2026-03-07T12:00:00+00:00",
# "2025-04-01T17:53:34.611+11:00",
# DATETIME
def t_DATETIME(t):
    r'"[0-9]{4}-((0[1-9])|(1[0-2]))-((0[1-9])|([12][0-9])|(3[01]))T((0[0-9])|(1[0-9])|(2[0-3])):([0-5][0-9]):([0-5][0-9]\+|([0-5][0-9]\.[0-9]{3,5}\+))([0-9]{2}:[0-9]{2})"'
    t.value = t.value.strip('"')
    return t

def t_DATETIME_ERROR(t):
    r'"\d{4}-\d{2}-\d{2}T[^"]+"'
    errores.append(f"Línea {t.lineno}: Fecha/hora inválida → {t.value}")
    return None

# MAC ADDRESS
def t_MAC_ADDRESS(t):
    r'"([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}"'
    t.value = t.value.strip('"')
    return t

def t_MAC_ADDRESS_ERROR(t):
    r'"([0-9A-Fa-f]{1,2}:){1,}[0-9A-Fa-f]{1,2}"'
    errores.append(f"Línea {t.lineno}: MAC inválida → {t.value}")
    return None

# ETHERTYPE
def t_ETHERTYPE(t):
    r'"0x[0-9A-Fa-f]{4}"'
    t.value = t.value.strip('"')
    return t

def t_ETHERTYPE_ERROR(t):
    r'"0x[0-9A-Fa-f]+"'
    errores.append(f"Línea {t.lineno}: Ethertype inválido → {t.value}")
    return None

# IPV4
def t_IPV4(t):
    r'"((25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9]{2}|[1-9][0-9]|[0-9])\/(3[0-2]|[1-2]?[0-9]|[0-9])"'
    t.value = t.value.strip('"')
    return t

def t_IPV4_ERROR(t):
    r'"\d{1,3}(\.\d{1,3}){1,3}(/\d{1,2})?"'
    errores.append(f"Línea {t.lineno}: IPv4 inválida → {t.value}")
    return None

# URL
def t_URL(t):
    r'"(https?://[a-zA-Z0-9:/.?=&%\-_~#@!]+|urn:[a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?:[a-zA-Z0-9._~!$&()*+,;=@%/-]+(:[a-zA-Z0-9._~!$&()*+,;=@%/-]+)*)"'
    t.value = t.value.strip('"')
    return t

def t_URL_ERROR(t):
    r'"((https?[:/][^"]*)|(htp[:/][^"]*)|(urn:[^"]*)|(urn[^"]*))"'
    errores.append(f"Línea {t.lineno}: URL inválida → {t.value}")
    return None

# DNS
def t_DNS(t):
    r'"([a-zA-Z0-9]([a-zA-Z0-9-]*[a-zA-Z0-9])?\.)+[a-zA-Z]{2,24}"'
    t.value = t.value.strip('"')
    return t

def t_DNS_ERROR(t):
    r'"[A-Za-z0-9-]+(\.[A-Za-z0-9-]+)+(\.[A-Za-z0-9-]*)?"'
    errores.append(f"Línea {t.lineno}: DNS inválido → {t.value}")
    return None

def t_BOOLEAN(t):
    r'(true)|(false)'
    return t

def t_NULL(t):
    r"null" # el null en json y mud es en minusculas
    t.value = None
    return t

def t_NUMBER(t):
    # un numero entero y permite con \b para asegurar que no este pegado a una palabra
    r'\b\d+\b'
    t.value = int(t.value)
    return t

#def t_RESERVED_VALUE(t):
#    r'\b(accept|eq)\b'
#    return t


def t_STRING(t):
    #permite caracteres normales y tambien caracteres escapados como \" o \\
    r'"([^"\\]|\\.)*"'
    value = t.value.strip('"')
    t.value = value # correccion 

    if value in reserved:
        t.type = reserved[value]

    return t

# Captura uno o más saltos de línea
# Referencia del ejemplo de calculadora
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# un string con caracteres a ignorar (espacios y tabs)
t_ignore = ' \t' 
 
# se agrega el error a la lista de errores y se salta el caracter ilegal
def t_error(t):
    # print(f"Illegal character '{t.value[0]}'")
    errores.append(f"Línea {t.lineno}: carácter ilegal '{t.value[0]}'")
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

def agregar_error(t, mensaje):
    errores.append(f"Línea {t.lineno}: {mensaje} → {t.value}")
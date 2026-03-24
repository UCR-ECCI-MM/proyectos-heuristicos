import ply.lex as lex
import ply.yacc as yacc

# tokens types
symbols = ["LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COLON", "COMMA"]

literal_values = ["BOOLEAN", "NUMBER", "NULL", "STRING", "DATETIME"]

addresses = ["IPV4", "URL", "DNS"] # ip hace referencia al tipo ipv4 mas especificamente

keys = ["NUMBER_KEYS", "URL_KEYS", "STRING_KEYS", "DNS_KEYS", "POLICIES_KEYS", 
        "PORT_DIR_KEYS", "NULL_KEYS", "RESERVED_VALUES"]

# maps for key types
# faltan port, null and reserved

number_keys = {"mud-version" : "NUMBER_KEYS", "cache-validity" : "NUMBER_KEYS",
               "protocol" : "NUMBER_KEYS", "port" : "NUMBER_KEYS"}

url_keys = {"mud-url" : "URL_KEYS", "mud-signature" : "URL_KEYS", 
            "documentation" : "URL_KEYS", "controller" : "URL_KEYS"}

string_keys = {"name" : "STRING_KEYS", "type" : "STRING_KEYS", "systeminfo" : "STRING_KEYS",
               "mfg-name" : "STRING_KEYS", "model-name" : "STRING_KEYS"}

dns_keys = {"ietf-acldns:dst-dnsname" : "DNS_KEYS", "ietf-acldns:src-dnsname": "DNS_KEYS"}

policies_keys = {"from-device-policy" : "POLICIES_KEYS", "to-device-policy" : "POLICIES_KEYS"}

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
    **number_keys, **url_keys, **string_keys, **dns_keys, **policies_keys, **unique_keys
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
# funcion string va hasta el final del archivo
def t_STRING(t):
    # regex strings
    # cualquier cadena que empiece y termine con quote se considera un string (hasta verificar si es una clave)
    r'"[^"]*"'

    value = t.value.split('"')[1] # quitar comillas de la palabra

    if value in reserved:
        t.type = reserved[value]

    return t

# A string containing ignored characters (spaces and tabs)
t_ignore = ' \t\n'
 
# Error handling rule
def t_error(t):
     print("Illegal character '%s'" % t.value[0])
     t.lexer.skip(1)

# creando el lexer
lexer = lex.lex()
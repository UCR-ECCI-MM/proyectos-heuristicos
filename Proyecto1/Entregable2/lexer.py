import ply.lex as lex
import ply.yacc as yacc

# tokens types
symbols = ["LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COLON", "COMMA"]

literal_values = ["BOOLEAN", "NUMBER", "NULL", "STRING", "DATETIME"]

addresses = ["IPV4", "URL"]

keys = ["ROOT_KEYS", "MUD_KEYS", "METADATA_KEYS", "POLICIES_KEYS", 
        "ACL_KEYS", "MATCHES_KEYS", "ACTIONS_KEYS", "RESERVED_VALUES"]

# complete token list for ply
tokens = symbols + literal_values + addresses + keys

# symbols regex
t_LBRACE = r"\{"
t_RBRACE = r"\}"
t_LBRACKET = r"\["
t_RBRACKET = r"\]"
t_COLON = r":"
t_COMMA = r","

# maps for key types
root_keys = {"ietf-mud:mud" : "ROOT_KEYS",
             "ietf-access-control-list:access-lists" : "ROOT_KEYS"}

mud_keys = {"name" : "MUD_KEYS", "type" : "MUD_KEYS",
            "access-lists" : "MUD_KEYS", "access-list" : "MUD_KEYS",
            "extensions" : "MUD_KEYS"}

metadata_keys = {"mud-version" : "METADATA_KEYS", "mud-url" : "METADATA_KEYS",
            "mud-signature" : "METADATA_KEYS", "last-update" : "METADATA_KEYS",
            "cache-validity" : "METADATA_KEYS", "is-supported" : "METADATA_KEYS",
            "systeminfo" : "METADATA_KEYS", "documentation" : "METADATA_KEYS",
            "mfg-name" : "METADATA_KEYS", "model-name" : "METADATA_KEYS"}

policies_keys = {"from-device-policy" : "POLICIES_KEYS", "to-device-policy" : "POLICIES_KEYS", 
            "policy" : "POLICIES_KEYS"}

acl_keys = {"acl" : "ACL_KEYS", "aces" : "ACL_KEYS", 
       "ace" : "ACL_KEYS", "matches" : "ACL_KEYS", 
       "actions" : "ACL_KEYS"}

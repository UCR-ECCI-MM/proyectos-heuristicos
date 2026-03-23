import ply.lex as lex
import ply.yacc as yacc

# tokens types
symbols = ["LBRACE", "RBRACE", "LBRACKET", "RBRACKET", "COLON", "COMMA", "QUOTE"]
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
t_QUOTE = r'\"'





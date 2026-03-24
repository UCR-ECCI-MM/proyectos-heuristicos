from lexer import lexer, reporte_lexico

# leer el archivo de entrada
with open("./Proyecto1/MUD/invalidos/test.json", "r") as mudFile:
    data = mudFile.read()

# pasar los datos al lexer
lexer.input(data)

# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok)

reporte_lexico()
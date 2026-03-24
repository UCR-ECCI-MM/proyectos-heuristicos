from lexer import lexer

# leer el archivo de entrada
with open("./Proyecto1/MUD/validos/test.json", "r") as mudFile:
    data = mudFile.read()

# pasar los datos al lexer
lexer.input(data)

# Imprimir tokens
while True:
    tok = lexer.token()
    if not tok:
        break
    print(tok)
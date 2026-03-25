from lexer import lexer, reporte_lexico

# Read file
nombre_archivo = "input_file_mud.json"
# nombre_archivo = ./Proyecto1/MUD/invalidos/test.json

try:
  with open(nombre_archivo, "r", encoding="UTF-8") as mudFile:
    data = mudFile.read()
except FileNotFoundError:
  print("Archivo no encontrado")

# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
  tok = lexer.token()
  if not tok: 
    break      # No more input
  print(tok)

reporte_lexico()
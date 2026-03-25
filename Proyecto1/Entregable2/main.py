from lexer import lexer, reporte_lexico

# Read file

nombre_archivo = "./Proyecto1/Entregable2/MUD/validos/test.json"

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
import os
from lexer import lexer, reporte_lexico

# elegir carpeta
num = input("1 = validos, 2 = invalidos: ")

if num == "1":
    carpeta = "./Proyecto1/Entregable2/MUD/validos"
else:
    carpeta = "./Proyecto1/Entregable2/MUD/invalidos"

# listar archivos
archivos = os.listdir(carpeta)

for i, archivo in enumerate(archivos):
    print(i+1, archivo)

opcion = int(input("Seleccione archivo: "))
nombre_archivo = carpeta + "/" + archivos[opcion - 1]

try:
  with open(nombre_archivo, "r", encoding="UTF-8") as mudFile:
    data = mudFile.read()
except FileNotFoundError:
  print("Archivo no encontrado")
  quit() # detener el programa para que no continue y haga un crash con la parte de abajo

# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
  tok = lexer.token()
  if not tok: 
    break      # No more input
  print(tok)

reporte_lexico()
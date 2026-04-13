import os
from lexer import lexer, reporte_lexico

# elegir carpeta
num = input("1 = validos, 2 = invalidos: ")

if num == "1":
    carpeta = "./MUD/validos"
else:
    carpeta = "./MUD/invalidos"

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

# leemos el archivo y lo pasamos al lexer
lexer.input(data)
 
# imprimimos los tokens encontrados
while True:
  tok = lexer.token()
  if not tok: 
    break      # no mas tokens
  print(tok)

reporte_lexico()
import os
import parser
from lexer import lexer, reporte_lexico
import ply.yacc as yacc

# Construcción del parser
parser_obj = yacc.yacc(module=parser)

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
  quit() # detener el programa

# leemos el archivo y lo pasamos al lexer
lexer.input(data)
 
# Impresión de tokens encontrados
while True:
  tok = lexer.token()
  if not tok: 
    break      
  print(tok)

reporte_lexico()

lexer.input(data) # el parser ocupa volver a tokenizar desde el principio

# Ejecución del parser
parser_obj.parse(data, lexer = lexer) # correccion
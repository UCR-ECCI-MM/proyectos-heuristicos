import os
import parser
from lexer import lexer, errores
import ply.yacc as yacc
from objects import MudFile, Mud, ACE # validaciones

# Construcción del parser
parser_obj = yacc.yacc(module=parser)

# validaciones
def validar_tipos(resultado):
    print("\nVALIDACION DE TIPOS !!")
    print("Resultado es MudFile:", isinstance(resultado, MudFile))
    print("mud es Mud:", isinstance(resultado.mud, Mud))
    print("acl_lists es lista:", isinstance(resultado.acl_lists, list))

    for acl in resultado.acl_lists:
        if "aces" in acl and "ace" in acl["aces"]:
            for ace in acl["aces"]["ace"]:
                print("Tipo de ACE:", type(ace).__name__, "-", isinstance(ace, ACE))

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
errores.clear()
lexer.lineno = 1

lexer.input(data)

while True:
    tok = lexer.token()
    if not tok:
        break

if len(errores) > 0:
    print("\nNo se ejecuta el parser porque primero deben corregirse los errores léxicos.")
    quit()

print("\nAnálisis léxico completado sin errores.")

lexer.lineno = 1
lexer.input(data)

try:
    resultado = parser_obj.parse(data, lexer=lexer)
    print("\nArchivo sintácticamente válido.")
    print(resultado)

    validar_tipos(resultado)
except parser.ParserValidationError as e:
    print(f"\n{e}")
except SyntaxError as e:
    print(f"\n{e}")
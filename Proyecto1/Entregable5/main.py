import os
import parser
from lexer import lexer, errores
import ply.yacc as yacc
from objects import MudFile, Mud, ACE, ACL, Policy # validaciones

from report_generator import ReportGenerator
from validator import validar_objetos, validar_consistencia
from traffic_summary import construir_resumen_trafico, imprimir_tabla_trafico

# Construcción del parser
parser_obj = yacc.yacc(module=parser)
reporte = ReportGenerator()
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


while lexer.token():
    pass

reporte.agregar_lexicos(errores)
if reporte.hay_errores_graves():
    reporte.imprimir_reporte()
    quit()

#print("El analisis lexico se ha completado sin errores.")

#Parser

lexer.lineno = 1
lexer.input(data)

resultado = None
try:
    resultado = parser_obj.parse(data, lexer=lexer)
    #print("El analisis sintactico se ha completado sin errores.")
except parser.ParserValidationError as e:
    # si hay un error de validacion el parser nos  da y lo agregamos al reporte como error de estructura
    reporte.agregar_estructura(e)
except SyntaxError as e:
    # si hay un error de sintaxis el parser nos lo da y lo agregamos al reporte como error sintactico
    reporte.agregar_sintactico(e)
# si parser falla entonces damos reporte y detenemos
if resultado is None:
    reporte.imprimir_reporte()
    quit()

# Validaciones
errores_obj = validar_objetos(resultado)
for e in errores_obj:
    # si hay errores en los objetos los agregamos al reporte como errores de estructura
    reporte.agregar_estructura(e)

errores_cons, advertencias = validar_consistencia(resultado)

for e in errores_cons:
    reporte.agregar_consistencia(e)

for a in advertencias:
    reporte.agregar_advertencia(a)

# si no hay errores graves, construimos el resumen de trafico y lo imprimimos
if not reporte.hay_errores_graves():
    resumen = construir_resumen_trafico(resultado)
    imprimir_tabla_trafico(resumen)

# imprimimos el reporte con los errores y advertencias encontrados
reporte.imprimir_reporte()
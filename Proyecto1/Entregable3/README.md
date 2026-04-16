# Analizador Sintáctico para Archivos MUD (Entregable 3, Proyecto 1)
## Computabilidad y Complejidad
## Equipo: Heuristicos
### Estudiantes:

- Leonardo Sibaja Campos C37537
- Brianna Mora Morales C4H587
- Ximena Marín Sánchez C14448

### Como ejecutar el programa

1. Abrir una terminal en la carpeta del proyecto (ENTREGABLE3)

2. Tener python instalado

https://www.python.org/downloads/

3. Ejecutar el siguiente comando:
```bash
python3 main.py
```

### Comprensión del estado final del parser
Al ejecutar el programa se generan dos archivos parser.out y parsetab.py 

Si se observa el parser.out se puede denotar que sí termina ($end) al consumir todos los tokens del archivo.

Como se muestra a continuación:

```
state 7

    (1) file -> LBRACE mud_members RBRACE .

    $end            reduce using rule 1 (file -> LBRACE mud_members RBRACE .)
```

Y al comparar con lo definido en el parser se observa que si cumple con la misma Gramática Libre de Contexto y quiere decir, que el parser ya reconoció un file. 

```
def p_file(p):
    'file : LBRACE mud_members RBRACE'
    p[0] = p[2]
```

### Archivos de prueba válidos

La carpeta MUD posee dos subcarpetas /validos e /invalidos

La carpeta de válidos posee MUD oficiales extraídos de:

https://iotanalytics.unsw.edu.au/mudprofiles.html


Extracto de salida:

```
1 = validos, 2 = invalidos: 1
1 NetatmoWeatherStationMud.json
2 blipcareBPmeterMud.json
3 sleepsensorMud.json
4 tplinkplugMud.json
5 babymonitorMud.json
6 cardioMud.json
Seleccione archivo: 1

Análisis léxico completado sin errores.

Archivo sintácticamente válido.
```

### Archivos de prueba inválidos

Para el archivo invalido_cache, se eliminaron los campos obligatorios que se espera en un archivo MUD como:

* cache_validity
* mud-version
* last-update

**Error obtenido:**
```
Faltan campos obligatorios en ietf-mud:mud: cache-validity, mud-version, last-update
```

Para el archivo invalido_acls_dest_mac:

1. Se elimina el contenido dentro de access list

```
"access-lists": {
        "access-list": [
          {}
        ],
        "systeminfo": "withingsbabymonitor"
      }
```

**Error obtenido:**
```
Error sintactico en la linea 22: el token 'RBRACE' con valor '}' no se esperaba en este lugar
```

2. Se extrajo el contenido dentro de eth, y se posicionó como líneas previas

```
"destination-mac-address": "ff:ff:ff:ff:ff:ff",
"ethertype": "0x0800",
"eth": {}
```
**Error obtenido:**
```
Error sintactico en la linea 112: el token 'DESTINATION_MAC_ADDRESS' con valor 'destination-mac-address' no se esperaba en este lugar
```

Lo cual verifica que el parser debe cumplir con la estructura definida.


Para el archivo invalido_sintactico_forwarding, lo que se realiza es que se cambia el valor esperado. 

```
"actions": {
  "forwarding": "eq"
}
```

**Error obtenido:**
```
Valor invalido para forwarding: 'eq'. Se esperaba accept, drop o reject
```

El archivo invalido_sintactico_multiple, tiene multiples errores, como número de puertos en una parte del documento no esperada, duplicación de texto, entre otros. 

**En resumen, en los diversos archivos de prueba se eliminan campos obligatorios, se modifica el orden, y se cambia las palabras esperadas.** 
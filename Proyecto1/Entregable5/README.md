# Implementación de la aplicación completa (Entregable 5, Proyecto 1)
## Computabilidad y Complejidad
## Equipo: Heurísticos
### Estudiantes:

- Leonardo Sibaja Campos C37537
- Brianna Mora Morales C4H587
- Ximena Marín Sánchez C14448

### Cómo ejecutar el programa

1. Abrir una terminal en la carpeta del proyecto (ENTREGABLE5)
2. Tener python instalado
3. Ejecutar el siguiente comando:
```bash
python main.py
```
Al ejecutar el programa, se solicita elegir el tipo de archivo:
```text
1 = validos, 2 = invalidos:
```

Luego se mostrará una lista de archivos disponibles, debe seleccionar el número correspondiente:
```text
1 babymonitorMud.json
2 blipcareBPmeterMud.json
3 cardioMud.json
4 NetatmoWeatherStationMud.json
5 sleepsensorMud.json
6 tplinkplugMud.json
```

## Descripción del entregable

En este entregable se implementó la aplicación completa para validar archivos MUD en formato JSON.
La aplicación utiliza el lexer, el parser y los objetos construidos en entregas anteriores. A partir de estos, se agregaron validaciones de aplicación, generación de reportes y una tabla que resume el tráfico permitido por el archivo MUD.
La aplicación se ejecuta en terminal y permite seleccionar archivos válidos o inválidos de prueba.


## Descripción de los módulos nuevos

### `object_validator.py`

Este módulo valida que los objetos construidos por el parser tengan la estructura esperada.

Revisa objetos como:

- `MudFile`
- `Mud`
- `Policy`
- `ACL`
- `ACE`

### `consistency_validator.py`

Este módulo valida la consistencia entre las políticas y las ACL definidas.

Por ejemplo, si `from_policy` o `to_policy` referencia una ACL llamada `acl1`, entonces debe existir una ACL con ese mismo nombre dentro de la lista de ACL del archivo.

### `traffic_summary.py`

Este módulo construye el resumen de tráfico permitido.
El resultado se imprime en una tabla en la terminal.

### `report_generator.py`

Este módulo centraliza los errores y advertencias encontrados durante la ejecución.

- Errores léxicos
- Errores sintácticos
- Errores de estructura
- Errores de consistencia
- Advertencias


## Salida esperada en la terminal

### 1. Caso válido

Al ejecutar el archivo válido `blipcareBPmeterMud.json`, se obtiene una salida similar a la siguiente:

```text
Tabla de trafico:
Sentido                             | Direccion                           | Protocolo    | Puerto   | Accion
----------------------------------------------------------------------------------------------------------------
Dispositivo hacia internet          | 224.0.0.1/32                        | 2            | —        | accept
Dispositivo hacia internet          | tech.carematix.com                  | tcp          | 8777     | accept
Dispositivo hacia internet          | urn:ietf:params:mud:dns             | udp          | 53       | accept
Dispositivo hacia internet          | 255.255.255.255/32                  | udp          | 67       | accept
Dispositivo hacia internet          | local-networks                      | eth          | —        | accept
Dispositivo hacia internet          | local-networks                      | eth          | —        | accept
Internet hacia dispositivo          | urn:ietf:params:mud:dns             | udp          | 53       | accept
Internet hacia dispositivo          | tech.carematix.com                  | tcp          | 8777     | accept
Internet hacia dispositivo          | urn:ietf:params:mud:gateway         | udp          | 67       | accept

Reporte:

No se encontraron errores.
```

En este caso, el archivo fue procesado correctamente. La aplicación construyó los objetos, validó su estructura, comprobó la consistencia entre políticas y ACL, y generó la tabla de tráfico permitido.


## Verificación del caso válido

Para comprobar la salida, se revisa que la cantidad de filas de la tabla coincida con la cantidad de reglas `ACE` definidas en las ACL referenciadas por las políticas.

Por ejemplo, en el archivo `blipcareBPmeterMud.json`, una de las reglas contiene:

```json
{
    "name": "from-ipv4-blipcarebpmeter-1",
    "matches": {
        "ipv4": {
            "protocol": 6,
            "ietf-acldns:dst-dnsname": "tech.carematix.com"
        },
        "tcp": {
            "destination-port": {
                "operator": "eq",
                "port": 8777
            },
            "ietf-mud:direction-initiated": "from-device"
        }
    },
    "actions": {
        "forwarding": "accept"
    }
}
```

A partir de esa regla, la aplicación genera una fila como:

```text
Dispositivo hacia internet | tech.carematix.com | tcp | 8777 | accept
```

Esto ocurre porque:

- El sentido se obtiene de `from-device-policy`.
- La dirección se obtiene de `ietf-acldns:dst-dnsname`.
- El protocolo se obtiene del bloque `tcp`.
- El puerto se obtiene de `destination-port`.
- La acción se obtiene de `forwarding`.

También existen reglas Ethernet que no tienen puerto asociado. Por ejemplo:

```json
{
    "name": "from-ethernet-blipcarebpmeter-0",
    "matches": {
        "ietf-mud:mud": {
            "local-networks": [
                null
            ]
        },
        "eth": {
            "ethertype": "0x888e"
        }
    },
    "actions": {
        "forwarding": "accept"
    }
}
```

En ese caso, la tabla muestra:

```text
Dispositivo hacia internet | local-networks | eth | — | accept
```


### 2. Caso inválido

#### Error léxico

Ejemplo: archivo con una IPv4 inválida.

#### Error sintáctico

Ejemplo: archivo con una coma faltante.

#### Error de estructura

Ejemplo: archivo sin un campo obligatorio como `mud-url`.

Salida esperada:

```text
Reporte:

Errores de estructura:
Faltan campos obligatorios en ietf-mud:mud: mud-url
```

#### Error de consistencia

Ejemplo: una política referencia una ACL que no existe.

Salida esperada:

```text
Reporte:

Errores de consistencia:
La ACL 'acl_inexistente' esta referenciada en from_policy, pero no existe en la lista de ACL.
```

#### Advertencia

Ejemplo: una ACL está definida, pero no es usada por ninguna política.

Salida esperada:

```text
Reporte:

Advertencias:
La ACL 'acl_extra' existe, pero no esta referenciada en from_policy ni en to_policy.
```

## Notas extra

- Si hay errores léxicos, no se ejecuta el parser.
- Si hay errores sintácticos, de estructura o consistencia, no se genera la tabla de tráfico.
- Si solo hay advertencias, el programa puede mostrar la tabla y luego indicar las advertencias encontradas.
- Algunos archivos de prueba inválidos se generaron con el uso de inteligencia artificial.

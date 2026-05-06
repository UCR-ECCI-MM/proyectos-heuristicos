# Creación dinámica de los objetos o las estructuras de datos (Entregable 5, Proyecto 1)
## Computabilidad y Complejidad
## Equipo: Heurísticos
### Estudiantes:

- Leonardo Sibaja Campos C37537
- Brianna Mora Morales C4H587
- Ximena Marín Sánchez C14448

### Cómo ejecutar el programa

1. Abrir una terminal en la carpeta del proyecto (ENTREGABLE4)
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

## Salida esperada en la terminal

### 1. Caso válido:

Al ejecutar el archivo válido de blipcareBPmeterMud.json

Se obtiene la siguiente salida:

```
Sentido                             | Direccion            | Protocolo    | Puerto   | Accion    
-------------------------------------------------------------------------------------------------
from-ipv4-blipcarebpmeter           | ipv4-acl-type        | 2            | —        | accept    
from-ipv4-blipcarebpmeter           | ipv4-acl-type        | 6            | 8777     | accept    
from-ipv4-blipcarebpmeter           | ipv4-acl-type        | 17           | 53       | accept    
from-ipv4-blipcarebpmeter           | ipv4-acl-type        | 17           | 67       | accept    
from-ethernet-blipcarebpmeter       | ethernet-acl-type    | —            | —        | accept    
from-ethernet-blipcarebpmeter       | ethernet-acl-type    | —            | —        | accept    
to-ipv4-blipcarebpmeter             | ipv4-acl-type        | 17           | 53       | accept    
to-ipv4-blipcarebpmeter             | ipv4-acl-type        | 6            | 8777     | accept    
to-ipv4-blipcarebpmeter             | ipv4-acl-type        | 17           | 67       | accept    

Reporte: No se encontraron errores.
```

Al revisar la salida obtenida, y el archivo, en primera instancia, se comprueba de que el archivo y la salida tengan la misma cantidad de acciones, en este caso, si se cumplió.

Posterior a ello, al probar el contenido de la columna del Sentido se confirma que se obtiene el resultado esperado

Por ejemplo en la salida de:
```
from-ipv4-blipcarebpmeter           | ipv4-acl-type        | 2            | —        | accept    
from-ipv4-blipcarebpmeter           | ipv4-acl-type        | 6            | 8777     | accept    
```

Se revisa conforme al archivo, y se comprueba tanto que se asocia al protocolo 2, como que el siguiente tiene asociado el protocolo 6, y el puerto 8777

```
            {
                "name": "from-ipv4-blipcarebpmeter",
                "type": "ipv4-acl-type",
                "aces": {
                    "ace": [
                        {
                            "name": "from-ipv4-blipcarebpmeter-0",
                            "matches": {
                                "ietf-mud:mud": {
                                    "local-networks": [
                                        null
                                    ]
                                },
                                "ipv4": {
                                    "protocol": 2,
                                    "destination-ipv4-network": "224.0.0.1/32"
                                }
                            },
                            "actions": {
                                "forwarding": "accept"
                            }
                        },
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
                        },
```

Asimismo, si se revisa el archivo, al buscar el from-ethernet-blipcarebpmeter se comprueba que no tiene puerto ni protocolo asociado.

Salida:

```
from-ethernet-blipcarebpmeter       | ethernet-acl-type    | —            | —        | accept    
from-ethernet-blipcarebpmeter       | ethernet-acl-type    | —            | —        | accept    
```

Posterior a ello, se revisa que no tenga un puerto y protocolo asociado, lo cual se cumple. 

```
{
                "name": "from-ethernet-blipcarebpmeter",
                "type": "ethernet-acl-type",
                "aces": {
                    "ace": [
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
                        },
                        {
                            "name": "from-ethernet-blipcarebpmeter-1",
                            "matches": {
                                "ietf-mud:mud": {
                                    "local-networks": [
                                        null
                                    ]
                                },
                                "eth": {
                                    "ethertype": "0x0006"
                                }
                            },
                            "actions": {
                                "forwarding": "accept"
                            }
                        }
                    ]
                }
            }
```
### 2. Caso inválido:

## Descripción del entregable

Implementación de la aplicación completa, con su respectiva funcionalidad

### Descripción de los módulos nuevos

### Explicación del flujo final de la aplicación


# Analizador Lexico para Archivos MUD (Entregable 2, Proyecto 1)
## Computabilidad y Complejidad
## Equipo: Heuristicos
### Estudiantes:

- Leonardo Sibaja Campos C37537
- Brianna Mora Morales C4H587
- Ximena Marín Sánchez C14448

### Como ejecutar el programa

1. Abrir una terminal en la carpeta del proyecto (ENTREGABLE2)
2. Tener python instalado
3. Ejecutar el siguiente comando:
```bash
python main.py
```

### Tipos de token del lexer MUD

Para realizar el analisis lexico de un archivo MUD, se tomo la decision de
dividir el contenido del documento en las siguientes categorias:

## Symbols:

| Caracter | Token        |
| -------- | ------------ |
| `{`      | **LBRACE**   |
| `}`      | **RBRACE**   |
| `[`      | **LBRACKET** |
| `]`      | **RBRACKET** |
| `:`      | **COLON**    |
| `,`      | **COMMA**    |

## Valores literales:

| Valor                      | Token        |
| -------------------------- | ------------ |
| `true`, `false`            | **BOOLEAN**  |
| números (`1`, `53`, `100`) | **NUMBER**   |
| `null`                     | **NULL**     |
| `"texto"`                  | **STRING**   |
| `"2025-04-01T..."`         | **DATETIME** |

## Otros valores:

| Valor                        | Token           |
| ---------------------------- | --------------- |
| `"255.255.255.255/32"`       | **IPV4**        |
| `"https://..."`, `"urn:..."` | **URL**         |
| `"example.com"`              | **DNS**         |
| `"ff:ff:ff:ff:ff:ff"`        | **MAC_ADDRESS** |
| `"0x0800"`                   | **ETHERTYPE**   |

El lenguaje MUD contiene diversas palabras clave que:
    - Tienen un significado especifico
    - Se repiten de forma consistente en los archivos
    - Definen la estructura del MUD

Por lo que estas palabras clave tendran tokens personalizados divididos por categoria.
**Las categorías agrupan las claves según el tipo de valor que se espera que las siga en el archivo MUD**

## NUMBER_KEYS:
*Claves que van seguidas de un número entero*

| Clave              | Token           |
| ------------------ | --------------- |
| `"mud-version"`    | **NUMBER_KEYS** |
| `"cache-validity"` | **NUMBER_KEYS** |
| `"protocol"`       | **NUMBER_KEYS** |
| `"port"`           | **NUMBER_KEYS** |

## URL_KEYS:
*Claves que van seguidas de un url*

| Clave             | Token        |
| ----------------- | ------------ |
| `"mud-url"`       | **URL_KEYS** |
| `"mud-signature"` | **URL_KEYS** |
| `"documentation"` | **URL_KEYS** |
| `"controller"`    | **URL_KEYS** |

## STRING_KEYS:
*Claves a las que le sigue una cadena de caracteres regular*

| Clave          | Token           |
| -------------- | --------------- |
| `"name"`       | **STRING_KEYS** |
| `"type"`       | **STRING_KEYS** |
| `"systeminfo"` | **STRING_KEYS** |
| `"mfg-name"`   | **STRING_KEYS** |
| `"model-name"` | **STRING_KEYS** |

## DNS_KEYS:
*Claves a las que le sigue un dominio dns*

| Clave                       | Token        |
| --------------------------- | ------------ |
| `"ietf-acldns:dst-dnsname"` | **DNS_KEYS** |
| `"ietf-acldns:src-dnsname"` | **DNS_KEYS** |

## POLICIES_KEYS:

| Clave                  | Token             |
| ---------------------- | ----------------- |
| `"from-device-policy"` | **POLICIES_KEYS** |
| `"to-device-policy"`   | **POLICIES_KEYS** |

## PORT_DIR_KEYS:
*Ambas esperan exactamente el mismo objeto JSON*

| Clave                | Token             |
| -------------------- | ----------------- |
| `"destination-port"` | **PORT_DIR_KEYS** |
| `"source-port"`      | **PORT_DIR_KEYS** |

## NULL_KEYS:
*Ambas reciben un arreglo que contiene un valor nulo*

| Clave                 | Token         |
| --------------------- | ------------- |
| `"local-networks"`    | **NULL_KEYS** |
| `"same-manufacturer"` | **NULL_KEYS** |

## PROTOCOL_KEYS:

| Clave   | Token             |
| ------- | ----------------- |
| `"tcp"` | **PROTOCOL_KEYS** |
| `"udp"` | **PROTOCOL_KEYS** |
| `"eth"` | **PROTOCOL_KEYS** |

## RESERVED_VALUES:
*No aparecen como claves, sino como valores dentro del JSON*

| Valor           | Token               |
| --------------- | ------------------- |
| `"eq"`          | **RESERVED_VALUES** |
| `"accept"`      | **RESERVED_VALUES** |
| `"from-device"` | **RESERVED_VALUES** |
| `"to-device"`   | **RESERVED_VALUES** |

## Claves únicas:
*No entran dentro de ningun grupo o son partes muy especificas del MUD*
*Son su propio tipo de token*

| Clave                                     | Token                                     |
| ----------------------------------------- | ----------------------------------------- |
| `"last-update"`                           | **LAST_UPDATE**                           |
| `"is-supported"`                          | **IS_SUPPORTED**                          |
| `"destination-ipv4-network"`              | **DESTINATION_IPV4_NETWORK**              |
| `"destination-mac-address"`               | **DESTINATION_MAC_ADDRESS**               |
| `"ethertype"`                             | **ETHERTYPE_KEY**                         |
| `"ietf-mud:direction-initiated"`          | **IETF_MUD_DIRECTION_INITIATED**          |
| `"operator"`                              | **OPERATOR**                              |
| `"forwarding"`                            | **FORWARDING**                            |
| `"extensions"`                            | **EXTENSIONS**                            |
| `"ietf-mud:mud"`                          | **IETF_MUD_MUD**                          |
| `"ietf-access-control-list:access-lists"` | **IETF_ACCESS_CONTROL_LIST_ACCESS_LISTS** |
| `"access-lists"`                          | **ACCESS_LISTS**                          |
| `"access-list"`                           | **ACCESS_LIST**                           |
| `"acl"`                                   | **ACL**                                   |
| `"aces"`                                  | **ACES**                                  |
| `"ace"`                                   | **ACE**                                   |
| `"matches"`                               | **MATCHES**                               |
| `"actions"`                               | **ACTIONS**                               |
| `"ipv4"`                                  | **IPV4_KEY**                              |
| `"policy"`                                | **POLICY**                                |

Como se menciono anteriormente, el tipo de token de los valores depende de la clave anterior (`last_key`), permitiendo validaciones específicas como URL, DNS, IPv4, fecha, MAC y ethertype.

## Uso de contexto (last_key)

El lexer utiliza una variable llamada `last_key` para recordar la ultima clave leida.
Esto permite determinar el tipo de valor esperado a continuacion y aplicar validaciones especificas segun el contexto.

Por ejemplo:

- Si la clave es `"mud-url"`, se espera una URL valida
- Si la clave es `"last-update"`, se espera una fecha en el formato adecuado

### Casos de prueba y ejemplos

Para los casos de prueba se cuenta con una carpeta *MUD*, que contiene archivos de prueba validos e invalidos. El archivo lexer.py contiene la logica del analizador
lexico mientras que main.py maneja la lectura del archivo MUD correspondiente desde la entrada y la salida del lexer (impresion).

A la hora de ejecutar el programa se espera en la salida una lista de cada token con su tipo, valor, linea y posicion.
Al final, un desglose de errores encontrados a la hora de validar tipos como URL, fecha entre otros.

*Ejemplo de salida del programa:*

    LexToken(URL_KEYS,'"controller"',2,8)
    LexToken(COLON,':',2,20)
    LexToken(URL,'urn:ietf1:params:mud:dns',2,22)
    LexToken(COMMA,',',2,48)
    LexToken(URL_KEYS,'"mud-url"',3,54)
    .
    .
    .
    Errores encontrados: 0

### Referencias

- OpenAI. (2026). ChatGPT (versión GPT-5.3) [Modelo de lenguaje grande]. https://chat.openai.com
- Se utilizo ChatGPT como herramienta de apoyo para generar archivos de prueba especificos.

- Beazley, D. (2024). PLY (Python Lex-Yacc) [Software]. https://www.dabeaz.com/ply/







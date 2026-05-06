# Creación dinámica de los objetos o las estructuras de datos (Entregable 4, Proyecto 1)
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
```text
Análisis léxico completado sin errores.

Archivo sintácticamente válido.
MudFile(mud=..., acl_lists=2 ACLs)

VALIDACION DE TIPOS
Resultado es MudFile: True
mud es Mud: True
acl_lists es lista: True
from_policy es Policy: True
to_policy no está presente

ACL es objeto ACL: True
Tipo de ACE: ACE - True
Tipo de ACE: ACE - True
```

### 2. Caso error léxico:
```text
Errores léxicos encontrados:
Línea X: IPv4 inválida → "999.999.999.999"

No se ejecuta el parser porque primero deben corregirse los errores léxicos.
```

### 3. Caso error sintáctico:
```text
Error sintáctico en la linea X: el token 'TOKEN' con valor '...' no se esperaba en este lugar
```

### 4. Caso error con validación semántica:
```text
Faltan campos obligatorios en ietf-mud:mud: mud-version, mud-url
```

- El parser no se ejecuta si existen errores léxicos.
- El resultado final se convierte en objetos:

    - MudFile
    - Mud
    - Policy
    - ACL
    - ACE

### Validación de tipos con isinstance

Para verificar que el parser construyó correctamente los objetos, se utiliza la función isinstance:
```python
isinstance(objeto, Clase)
```

Esta función retorna:

- `True` si el objeto pertenece a la clase indicada.
- `False` si no pertenece.

Se usa para validar que:

- El resultado principal es un objeto `MudFile`.
- El atributo mud es un objeto `Mud`.
- Las listas contienen objetos `ACL` y `ACE`, no diccionarios.
- Las políticas (from_policy, to_policy) son objetos `Policy`.

## Descripción del entregable
En este entregable se trabajó sobre la base del parser ya construido anteriormente, enfocándose en mejorar la estructura de salida y agregar validaciones adicionales, a partir de creación dinámica de objetos.

Se dejó de usar diccionarios como resultado final y se implementaron clases:

- `MudFile`
- `Mud`
- `Policy`
- `ACL`
- `ACE`

Se modificaron las reglas para que:

- Las listas (ACL, ACE) contengan objetos, no diccionarios.
- La estructura final represente correctamente la jerarquía del archivo.

Se implementó una verificación final en main.py usando isinstance para confirmar que:

- El resultado es un MudFile
- Los ACL son objetos ACL
- Los ACE son objetos ACE


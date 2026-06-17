# Proyecto 2

## Representación común del problema

El problema se representa mediante una cuadrícula de perreras de tamaño `N×N` y un conjunto de `P` perros, donde `P ≤ N²`.

### Perro

Cada perro se representa con los siguientes atributos:

```txt
id sexo celo enfermo
```

| Campo     | Valores               | Descripción                                          |
| --------- | --------------------- | ---------------------------------------------------- |
| `id`      | `D1`, `D2`, `D3`, ... | Identificador único del perro                        |
| `sexo`    | `M` / `H`             | `M` = macho, `H` = hembra                            |
| `celo`    | `0` / `1`             | `1` si la hembra está en celo, `0` en caso contrario |
| `enfermo` | `0` / `1`             | `1` si el perro está enfermo, `0` en caso contrario  |

Ejemplo:

```txt
D1 M 0 0
D2 H 1 0
D3 M 0 1
```

## Representación de perreras

El refugio se representa como una matriz de tamaño N×N.

Cada perrera puede identificarse por su posición:

```txt
fila columna
```

## Representación de una solución

Una solución es una asignación de perros a perreras.

Se representa como una lista donde cada perro tiene asociado el índice de la perrera en la que fue colocado.

Ejemplo:

```txt
D1 -> 0
D2 -> 4
D3 -> 2
D4 -> 8
```

Reglas:

* Cada perro debe estar asignado a una única perrera.
* Una perrera no puede contener más de un perro.
* Puede haber perreras vacías si `P < N²`.


## Adyacencia

Dos perreras se consideran adyacentes si comparten un lado, es decir, si están arriba, abajo, a la izquierda o a la derecha.

No se toman en cuenta las diagonales.

Dos posiciones `(f1, c1)` y `(f2, c2)` son adyacentes si:

```txt
abs(f1 - f2) + abs(c1 - c2) == 1
```

## Formato de archivos de prueba

Los archivos de prueba deben tener el siguiente formato:

```txt
N P
id sexo celo enfermo
id sexo celo enfermo
id sexo celo enfermo
```

## Función de evaluación común

Todos los algoritmos deben utilizar la misma función de evaluación para poder comparar los resultados de forma consistente.

El costo de una solución se calcula como:

```txt
costo = 10 * conflictosMachoMacho + 10 * conflictosMachoHembraCelo + 20 * enfermosFueraPrimeraFila
```

| Conflicto                              | Penalización |
| -------------------------------------- | -----------: |
| Dos machos adyacentes                  |        `+10` |
| Macho adyacente a hembra en celo       |        `+10` |
| Perro enfermo fuera de la primera fila |        `+20` |

Una solución ideal tiene costo 0.

Los conflictos de adyacencia se cuentan una sola vez por pareja de perros. Para evitar duplicados, se comparan únicamente parejas donde i < j.

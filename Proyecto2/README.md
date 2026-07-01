# Proyecto 2

## Equipo: Heuristicos

### Integrantes:
* Leonardo Sibaja Campos C37537
* Brianna Mora Morales C4H587
* Ximena Marín Sánchez C14448

## Prerequisitos
Tener python instalado 

## Indicaciones para ejecutar el programa

1. Tener clonado el repositorio mediante SSH. En caso que no esté clonado, puede abrir una terminal, por ejemplo de WSL y escribir el siguiente comando

```
git clone git@github.com:UCR-ECCI-MM/proyectos-heuristicos.git
``` 

2. Posteriormente en la terminal ingresar en la carpeta, del Proyecto2, por ejemplo: 

```
cd proyectos-heuristicos/Proyecto2
```

3. Ejecutar el main (dentro de la carpeta del Proyecto 2) 
```
python3 main.py
```

Al ejecutar el programa, se solicita elegir el tipo de algoritmo:
```
1. Fuerza Bruta
2. Heurística
3. Simulated Annealing 

Opcion: 
```

Digita una opción, por ejemplo, la opción 2

Posteriomente, se solicita digitar los tamaños de archivo de prueba que desea ejecutar o el archivo de prueba en especifico

**Importante:** Fuerza bruta solo funcionará con los archivos small, dado que encuentra soluciones óptimas pero solo escala a problemas pequeños, en el medium_01 (16 perros, en 16 perreras) lleva más de 24 horas en ejecución. 

```
Seleccione el archivo o grupo de prueba:
Ejemplos:
small -> corre todos los small
medium -> corre todos los medium
large -> corre todos los large
small_01 -> corre solo small_01.txt
medium_02 -> corre solo medium_02.txt
large_01 -> corre solo large_01.txt

Archivo o grupo: 
```

Y al final, dependiendo del algoritmo que se elige, se mostrarán las configuraciones, como el caso de la heurística y metaheuristica.

Asimismo, la heuristica y fuerza bruta mostrará en terminal, el tiempo, costo y evaluaciomes. 

Un detalle a destacar, es que fuerza bruta, sin importar la cantidad de ejecuciones, devuelve siempre la misma solución.

## ¿Dónde se guardan los resultados?
Se pueden observar en la carpeta dentro del Proyecto2 llamada results.

Como se puede observar, hay:
1. resultados_sa para cada uno de los tamaños
2. resultados_he para cada uno de los tamaños
3. resultados_fb para small 

### Comandos para generación de graficos

Heuristica

```
python3 src/pruebas/graficos_heuristica.py
```

Simulated Annealing

```
python3 src/pruebas/graficos_metaheuristica.py
```

Fuerza bruta

```
python3 src/pruebas/graficos_fuerza_Bruta.py

```

Se pueden observar en la carpeta Proyecto2/results/gráficos 


## Descripción

Este proyecto compara tres algoritmos de optimización:

* **Heurística**: Inspirada en Best Fit, que consiste en colocar primero los perros con más restricciones.
* **Simulated Anneling**: Consiste en comenzar con una solución inicial y mejorarla progresivamente explorando soluciones vecinas
* **Fuerza Bruta**: Búsqueda exhaustiva (limitado a instancias pequeñas)

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

# Simulated Annealing - Análisis de Configuraciones Y parametros

## Mejor Configuración Encontrada

```
Configuración: T50_a0.9_i5
├─ Temperatura inicial (T): 50
├─ Factor de decaimiento (α): 0.9
├─ Iteraciones por temperatura (i): 5
├─ Costo promedio: 15.00
└─ Tiempo promedio: 5.62 ms
```

---

## Análisis Comparativo

### 1. Costo Promedio (Mejor opción)

Ranking de mejores configuraciones:

```
1. T50_a0.9_i5:   15.00  [GANADOR]
2. T50_a0.7_i5:   20.80
3. T200_a0.9_i2:  20.90
4. T100_a0.9_i5:  20.95
5. T50_a0.5_i5:   25.50
```

**Por qué gana T50_a0.9_i5:**
- 25% mejor que T50_a0.7_i5 (enfriamiento más lento = mejor exploración)
- 34% mejor que T50_a0.5_i5 (alpha=0.9 permite más iteraciones efectivas)
- Mantiene equilibrio entre velocidad y calidad

---

### 2. Consistencia en small_01.txt

Gráfica: Mejor y peor costo

| Configuración | Mejor | Peor | Variabilidad | Interpretación |
|---------------|-------|------|--------------|----------------|
| T50_a0.9_i5   | 0 | 0 | 0% | Perfectamente consistente |
| T100_a0.5_i2  | 0 | 20 | Varía| Aleatoria, poco confiable |
| T100_a0.7_i5  | 0 | 20 | Varía| Menos consistente |
| T50_a0.5_i2   | 0 | 20 | Varía| Depende de la semilla aleatoria |

**Conclusión:** T50_a0.9_i5 siempre encuentra la solución óptima en small_01. Las otras configuraciones tienen suerte (a veces 0, a veces peor).

---

### 3. Rendimiento en small_02.txt

Gráfica: Mejor y peor costo (segundo archivo)

| Configuración | Mejor | Peor | Variabilidad | Nota |
|---------------|-------|------|--------------|------|
| T50_a0.9_i5   | 30 | 30 | 0% [OK] | Consistente |
| T200_a0.9_i5  | 30 | 40 | Varía | Más exploración = menos estabilidad |
| T50_a0.7_i5   | 30 | 40 | Varía | Temperatura inicial baja, menos flexible |
| T100_a0.5_i5  | 20 | 40 | 50% | Muy inconsistente |


---

### 4. Velocidad de Ejecución

Gráfica: Tiempo promedio por configuración

| Configuración | Tiempo | Costo | Ratio Calidad/Velocidad |
|---------------|--------|-------|------------------------|
| T50_a0.5_i2   | 0.40 ms | 30.9  | Rápido pero malo |
| T50_a0.7_i2   | 0.91 ms | 27.5  | Rápido pero mediocre |
| T50_a0.9_i5   | 5.62 ms | 15.0  | MEJOR BALANCE [OK] |
| T200_a0.9_i5  | 6.25 ms | 20.9  | Más lento, peor resultado |

**Análisis:**
- T50_a0.9_i5 es más lento que T50_a0.5_i2
- Pero logra mejor costo (15 vs 30.9)
- Justificación: 5.62ms es aceptable para lograr soluciones óptimas

---

### 5. Escalabilidad (por Tamaño N)

Datos: N = 3 (todos los datos)
Costo promedio en N=3: 23.6

NOTA: Todos los datos tienen N=3, por lo que no hay variación de escalabilidad.


---

## Desglose Detallado: ¿Por qué T50_a0.9_i5 es el mejor?

### Parámetro T (Temperatura Inicial)

```
T=50   Moderado (inicio equilibrado)
T=100  Alto (comienza con más aleatoriedad)
T=200  Muy alto (demasiada exploración inicial)
```

**Análisis:**
- T=50: Permite convergencia rápida sin perder exploración
- T=100: Explora demasiado al inicio, converge lentamente
- T=200: Gasta recursos en exploración innecesaria

**Ganador: T=50** (visto en todos los gráficos, las configuraciones T50 dominan)

---

### Parámetro α (Factor de Decaimiento)

```
α = 0.5  Enfría rápido:    T0=50 → T1=25 → T2=12.5 → ...
α = 0.7  Enfría moderado:  T0=50 → T1=35 → T2=24.5 → ...
α = 0.9  Enfría lentamente: T0=50 → T1=45 → T2=40.5 → ...
```

**Gráfico de Costo Promedio:**

```
Configuraciones con α=0.5:  30.9, 20.8, 25.5 (muy variables)
Configuraciones con α=0.7:  27.5, 20.8, 17.6 (mejor)
Configuraciones con α=0.9:  15.0, 20.9, 20.9 (MAS CONSISTENTES)
```

**Por qué α=0.9 gana:**
-  Mantiene temperaturas altas por más tiempo
-  Mayor probabilidad de escapar de mínimos locales
-  Mejor exploración = mejores soluciones
-  Costo: más lento (pero vale la pena)

---

### Parámetro i (Iteraciones por Temperatura)

```
i=2  Menos pruebas por temperatura (rápido pero superficial)
i=3  Moderado
i=5  Más pruebas por temperatura (lento pero exhaustivo) [BEST]
```

**Patrón en datos:**

```
T50_a0.9_i2: Costo 22.1  |  Tiempo 2.28 ms
T50_a0.9_i3: Costo 20.0  |  Tiempo 3.76 ms
T50_a0.9_i5: Costo 15.0  |  Tiempo 5.62 ms 
```

**Por qué i=5 es mejor:**
- Permite explorar más vecinos en cada temperatura
- Aumenta chances de encontrar óptimos locales
- Cada iteración adicional mejora ~5 unidades de costo

---

## Resumen Visual

```
            COSTO      TIEMPO     CONSISTENCIA    SCORE
T50_a0.9_i5  15.00      5.62ms     Perfecta       [5/5]
T50_a0.7_i5  20.80      2.38ms     Variable       [4/5]
T100_a0.9_i5 20.95      6.25ms     Variable       [4/5]
T50_a0.5_i5  25.50      1.30ms     Variable       [3/5]
```

---

## Recomendación Final

Para este problema (3x3 perreras, 8 perros):

Usar T50_a0.9_i5 porque:

1. Mejor calidad: Costo 15.00 (el más bajo)
2. Confiable: 100% consistente entre corridas
3. Aceptable velocidad: 5.62ms es razonable para buenas soluciones
4. Predecible: No depende de la suerte aleatoria


## Archivos Generados

```
resultados/
├── graficos/
│   ├── costo_promedio.png          (Comparativa general de costos)
│   ├── tiempo_promedio.png         (Comparativa de velocidades)
│   ├── mejor_peor_small_01.txt.png (Rango de resultados archivo 1)
│   ├── mejor_peor_small_02.txt.png (Rango de resultados archivo 2)
│   └── tamano.png                  (Escalabilidad por N)
└── resultados_sa.csv               (Datos crudos)
```
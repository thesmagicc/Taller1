

# TALLER 1
## Programación lineal

**ESCUELA DE CIENCIAS APLICADAS E INGENIERÍA**

**ASIGNATURA:** Métodos Cuantitativos

**PROFESOR:** Juan Carlos Rivera Agudelo

---

##  Integrantes

1. **Sebastian Sanchez Gomez**
2. **Mateo Duque Restrepo**
3. **Matias Villegas Gomez**

---
### Considere el siguiente contexto:

Sea:
- 𝑠: el número de estudiantes del equipo.
- 𝑑: la suma de las dos últimas cifras de las cédulas de los integrantes del equipo.

La empresa de manufactura JCR produce tres tipos de productos: P1, P2 y P3. La planeación de producción se realiza para los próximos cuatro periodos (meses).

El precio base de venta en el periodo 1 es:
- P1: $600.000
- P2: $550.000
- P3: $700.000
El precio de cada producto se incrementa en cada periodo a una tasa que depende del equipo de trabajo.

La tasa de incremento por periodo es: 𝛼 = 0.01 + 0.005𝑠

Por tanto, el precio de cada producto en el periodo 𝑡 se obtiene multiplicando el precio base por (1+𝛼)^(𝑡−1)

La empresa dispone de una capacidad total de producción medida en horas por semana. La capacidad disponible en cada periodo es:

C = 180 + (-1)^(𝑡−1) · 𝑑/100 horas

Cada unidad producida requiere un tiempo de procesamiento igual a 3 horas por unidad para el producto P1, 4 horas por unidad para P2 y 2 horas por unidad para P3.

La producción utiliza dos materias primas: M1 y M2. Cada unidad de producto requiere las siguientes cantidades de materia prima:
<div align="center">

| Producto | M1 | M2 |
|:---:|:---:|:---:|
| P1 | 2 | 1 |
| P2 | 1 | 3 |
| P3 | 2 | 2 |
</div>
La disponibilidad máxima de compra mensual para cada materia prima es:
- M1: 600 - 12s unidades
- M2: 480 + 8s unidades

El inventario inicial de materias primas es:
- M1: 40 unidades
- M2: 30 unidades

Los costos de compra son:
- M1: $50.000 por unidad
- M2: $70.000 por unidad

La empresa puede comprar materias primas adicionales cada mes, respetando el límite máximo disponible.

La demanda base para los cuatro periodos es:
<div align="center">

| Periodo | P1 | P2 | P3 |
|:---:|:---:|:---:|:---:|
| 1 | 120 | 60 | 72 |
| 2 | 72 | 80 | 60 |
| 3 | 100 | 130 | 80 |
| 4 | 60 | 62 | 68 |
</div>

El inventario inicial de productos terminados es:
- P1: 20 unidades
- P2: 24 unidades
- P3: 16 unidades
El costo de almacenamiento por periodo es equivalente al 𝑠% del precio base tanto para los productos como para las materias primas.

Al finalizar el cuarto mes debe existir un inventario mínimo de 20 unidades de cada producto. En caso de ser necesario, cuando no sea posible abastecer la demanda en algún periodo, se pueden entregar productos en el siguiente mes; en dichos casos se ofrece al cliente una reducción en el precio del producto de 0.1d%.

De acuerdo a restricciones internas de la empresa, la producción debe realizarse en lotes con los siguientes tamaños para cada producto: 5 unidades para P1, 1 unidad para P2, y 7 unidades para P3.

La empresa desea determinar un plan de compra de materias primas, producción y almacenamiento que cumpla las condiciones planteadas y maximice la utilidad total.

# RESULTADO — INVARIANCIA DEL ORDEN — Ventana D, 2026-09-03

Pre-registro: `invariancia_orden_preregistro.md` (commit `01f2489`). Salida cruda:
`invariancia_orden.txt` (`4845a4e`). Diagnóstico: `invariancia_orden_diagnostico.txt` (`06758f6`).
La caja no se tocó: ninguna sesión posterior a 2019-12-31 entró en ningún cálculo.

## 1 · La pregunta quedó cerrada por su propio control, y no se interpreta

Población: la P-escalera de 971 menos las 20 sesiones sin las 20 previas para la mediana móvil, todas
de enero y febrero de 2016. Quedan **951 sesiones**, 2016-02-02 → 2019-12-31 (K5, cobertura).

**K0 tenía dos criterios y falló el segundo:**

| criterio congelado | medido | |
|---|---|---|
| partición entre 40 % y 60 % | ALTO = 48,3 % (459 de 951) | PASA |
| ALTO con excursión **mayor** que BAJO en la sesión completa | mediana ALTO 8,75 pts, mediana BAJO 8,75 pts | **FALLA** |

Por el pre-registro §6, el script terminó ahí. **El contraste principal, K1 a K4, los cocientes por
estado y los rankings de horas no se calcularon y no existen en ningún archivo.** No sé si el orden de
las horas se conserva bajo la condición: la pregunta no llegó a hacerse.

**K_D = 1 queda gastado.** El cartucho se gasta al pre-registrar, no al correr. **K = 263.** No hay
segunda corrida, no se cambia el criterio de K0, no se reformula la condición. La posición A no queda
elegida por defecto: la palanca «cuándo» sigue sin respuesta condicional.

## 2 · HALLAZGO — el agrupamiento de volatilidad es un fenómeno de cola, no de centro

Esto cambia una premisa que este proyecto venía usando, así que va completo. El diagnóstico no reabre
la pregunta: no recalcula el contraste, no toca los rankings y no cambia ningún criterio. Separa tres
causas posibles del empate de medianas.

**Primero, no hay bug de alineación.** Control positivo, particionando por el rango de **hoy** contra
la misma mediana móvil: medias 19,95 contra 8,73 puntos, **factor 2,29×**, t = +10,32. La maquinaria
separa cuando hay algo que separar; las etiquetas corresponden al día que dicen.

**Segundo, la condición sí tiene señal, pero vive entera en la cola:**

| estadística de la excursión adversa del día | tras rango grande | resto | cociente |
|---|---|---|---|
| mediana | 8,75 pts | 8,75 pts | **1,00×** |
| media | 15,83 | 12,64 | 1,25× |
| p90 | 38,35 | 27,95 | 1,37× |
| p95 | 59,75 | 39,61 | **1,51×** |
| p99 | 100,92 | 64,67 | 1,56× |

El día que sigue a un rango grande **no es un día típicamente más violento: es un día típicamente
igual, con más probabilidad de ser extremo.** El centro de la distribución no se mueve nada, y el 5 %
peor se mueve la mitad. Las correlaciones lo confirman: rango de ayer contra rango de hoy da Spearman
+0,58 (+0,60 en log), que es el agrupamiento clásico y está intacto; pero rango de ayer contra la
**excursión adversa** de hoy da sólo +0,29.

**Tercero, y es lo que más cambia el plan: con el α heredado, esto no es detectable como
desplazamiento de nivel.** La diferencia de medias da t = +2,82 (p = 4,9 × 10⁻³). La línea de decisión
es |t| ≥ 3,732. Ni siquiera cruza la línea de la suerte del programa. Una pregunta condicional
planteada sobre el nivel de la excursión **está muerta antes de escribirse**, con 951 sesiones y este
α, aunque el fenómeno exista y sea conocido.

**Lo que esto le hace a `pregunta_cuanto_y_cuando.md`:**

- **La forma 2 (residuo tras normalizar por el rango de ayer) queda debilitada.** Normalizar por un
  predictor que correlaciona +0,29 con lo que se quiere predecir deja casi todo el residuo intacto. La
  regla mecánica «contratos = límite / rango de ayer» dimensiona contra un predictor flojo del riesgo
  del día.
- **La forma 3 (cola contra el límite de la cuenta) sube a primera, y por un motivo nuevo.** Es la
  única de las tres que mide donde el efecto está. El p95 se mueve 1,51×, y el pre-registro de hoy
  declaró detectable 1,52× a mitades: es exactamente el borde. Sigue exigiendo el límite diario L, que
  **no existe verificado en este repo** y que Roberto tiene que traer con fuente y fecha.
- **La forma 1 no queda respondida, queda sin preguntar**, y una segunda versión de ella pagaría K
  otra vez.

## 3 · Lección de método, que es mía y va escrita

**Elegí mal el control.** K0 verificaba la condición con la **mediana**, y el efecto que la condición
produce vive en la cola. El control mató la pregunta por una razón distinta de la que pretendía
detectar: no detectó «la condición no es lo que dice ser», detectó «la mediana no se mueve», que era
verdad y no era el punto. Si K0 hubiera comparado el p95, habría pasado, y el contraste principal
—que es un contraste de medias en log, sensible a la cola— se habría corrido.

**No lo cambio.** El criterio estaba congelado antes de correr y el orden del log es la garantía; un
control que se afloja después de fallar no es un control. Queda como está, con el cartucho gastado.

**La regla que sale de acá, para todo pre-registro futuro de esta ventana:** el control de precondición
tiene que medirse en **la misma estadística que la pregunta usa**. Si la pregunta contrasta medias en
log o percentiles altos, su precondición se verifica ahí, no en la mediana. Va junto a la lección de
`umbral_control_derivado`: los umbrales se derivan del dato, y ahora también, la **estadística** del
control se deriva de la pregunta.

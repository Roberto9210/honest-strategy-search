# P08 — L10, preparada hasta el borde. BORRADOR, NO REGISTRADO

**VENTANA L. NO REGISTRADO. NO CORRIDO. K sigue en 261.**
> ## FRÁGIL — las cifras de potencia de este documento dependen de números SIN MEDIR: **E1, E5 y E6**.
> Ver [FRAGILIDAD.md](FRAGILIDAD.md). Las conclusiones cualitativas no dependen de ellos; **las tablas de potencia sí**.

> Registrarlo gastaría el cartucho **263** si L11 se registrara primero, o el **262** si va sola.
> **La aritmética de la sección 5 dice que tampoco conviene.**

---

# 1. Los datos que faltaban — y acá tengo que corregirme

**Dije que a L10 sólo le faltaba "una serie diaria de retornos de bonos, gratis y pública". Verifiqué
la fuente y no es tan simple. Es la cuarta corrección que hago de un número o una afirmación propia.**

## Lo que el paper usa

Harvey, Mazzoleni y Melone construyen el desvío de la cartera con **retornos diarios de futuros del
S&P 500 y de futuros del bono del Tesoro a 10 años**, 1997-2023. Es una serie de **retornos de
futuros**.

## Lo que hay gratis

| fuente | qué es | ¿sirve directo? |
|---|---|---|
| **Tesoro de EE.UU.**, *Daily Treasury Par Yield Curve Rates*, con archivos XML históricos | **rendimientos** al cierre de 15:30, tomados por la Reserva Federal de Nueva York | **NO.** Un rendimiento no es un retorno |
| Reserva Federal de San Luis, serie de rendimiento a 10 años | lo mismo, y además es **fuente secundaria** del dato del Tesoro | no, y por partida doble |

**Convertir un rendimiento en un retorno exige multiplicar por una duración, y elegir la duración es
una decisión ajustable.** La duración modificada del bono más barato de entregar del contrato se
mueve con el tiempo y con qué bono sea. **Eso es un grado de libertad, y por `F9` convierte a L10 en
híbrida CON AJUSTE.**

## Las dos salidas, y la recomendación

**Salida A — comprar ZN diario.** El contrato que el paper usa, sin conversión, sin grado de
libertad. Databento sirve GLBX. Es **una serie diaria de un símbolo por cuatro años**: la compra más
chica que este proyecto haya considerado, más chica todavía que la de `P05`.

**Salida B — usar rendimientos del Tesoro con una duración declarada.** Gratis, pero agrega una
variante y desvía del paper.

**Recomiendo la A y digo por qué: la B ahorra unos pocos dólares y paga con un grado de libertad, y
este proyecto ya midió que los grados de libertad cuestan más que los datos.**

**La serie de acciones no falta: `data/es_daily.csv` ya está en el repo.**

---

# 2. El archivo de entrada del juez

```json
{
  "nombre": "L10_rebalanceo_institucional_harvey",
  "instrumento": "MES",
  "contratos": 1,
  "limite_contratos": 4,
  "variantes_probadas": 30,
  "clase_ventaja": "direccional",
  "familia": "calendario_rebalanceo_fin_de_mes",
  "regla_salida": {"tipo": "tiempo", "n_barras": 1380},
  "operaciones": [
    {"ts": "2019-01-30T15:00:00", "lado": "corto"}
  ]
}
```

**Una operación por fin de mes: entrada en la barra del cierre del último día hábil, lado dado por el
signo del desvío acciones contra bonos.** Si las acciones quedaron sobreponderadas, los fondos venden
acciones, así que el lado es **corto**. El ejemplo es el fin de enero de 2019.

**Sin ningún campo de resultado.** El lado sale de una señal calculada con datos hasta la entrada, no
de saber qué pasó después.

## Las decisiones de construcción, declaradas

1. **`instrumento`: MES**, por el mismo motivo que en `P07`.
2. **`n_barras`**: mismo pendiente de confirmación que en `P07`, ver `P09`.
3. **La señal**: desvío acumulado de la ponderación acciones contra bonos respecto de la cartera
   objetivo, con la construcción de calendario del paper. **La ponderación objetivo del 60/40 es la
   del paper y no la elegimos nosotros.**
4. **El umbral de la señal**: el paper usa la señal **continua**, no un umbral. **Se usa continua.
   Meter un umbral sería inventar un grado de libertad que el paper no tiene.**

---

# 3. `clase_ventaja` = `direccional`

- **Nula de signo:** el lado **varía** con el signo del desvío y no es indiferente; aleatorizarlo
  destruye el efecto. **Desvío alto.**
- **Nula de rotación:** el paper mide que la predictibilidad de calendario es **fuerte a fin de mes y
  ausente fuera de esos días**. Rotar las fechas la destruye. **Desvío alto.**

**Las dos altas → `direccional`.** Es la declaración estricta y no compra nada.

---

# 4. `variantes_probadas` = 30

**Los autores no declaran cuántas variantes probaron.** Va escrito así.

Conteo de lo visible: dos señales, umbral y calendario; dos activos; varios horizontes, incluido el
de reversión a dos semanas; otros esquemas de ponderación que mencionan en su nota 2 sin tabular;
cortes por fin de mes, por mes dentro del trimestre y por semana; y controles por momento,
reversiones, macro y sentimiento. **Más las nuestras: instrumento MES, definición del cierre, y la
fuente de la serie de bonos.**

**Atenuante real, y va en el pre-registro:** las dos señales salen de las **políticas de inversión
declaradas de las instituciones**, no de un barrido sobre datos. Una señal derivada de un reglamento
externo tiene mucha menos libertad que una calibrada.

---

# 5. LA HIPÓTESIS, LA REGLA DE DECISIÓN Y LA POTENCIA

## Hipótesis

> **En los últimos días hábiles de mes de 2016-2019, un MES operado en la dirección opuesta al desvío
> acumulado de acciones contra bonos, entrando al cierre y saliendo al cierre siguiente, rinde neto
> de costos medidos más que la nula más exigente de las tres, con al menos una cuarta parte de los
> 17 puntos básicos por desvío estándar de señal que Harvey, Mazzoleni y Melone reportan.**

## Regla de decisión

Idéntica a la de `P07`. **SOBREVIVE** si el juez devuelve SUPERA y la ventaja medida es al menos
0,25 × 17 pb por desvío de señal. **NO SOBREVIVE** con NO SUPERA. **NO CONCLUYENTE** con NO MEDIBLE,
APUESTA AL REGIMEN o bandera roja.

## La potencia

| | |
|---|---|
| magnitud objetivo, muestra completa 1997-2023, **sin corregir** | **17,0 pb** |
| `σ` estimado, cierre a cierre | ≈ 60 pb |
| `r` por evento | 0,283 |
| eventos: 12 fines de mes por año | **48** |
| **`t(θ=1)`** | **1,96** |
| vara del juez con 30 variantes | ≈ 4,0 desvíos |
| **`θ` mínimo detectable** | **2,04** |

> ## **L10 SOLA NECESITARÍA EL 204 % DE SU MAGNITUD PUBLICADA PARA PASAR.**

**Es la peor de las dos**, y por el motivo obvio: tiene la mejor magnitud por evento del inventario y
el peor presupuesto de eventos, doce por año.

**Si se suma la señal de umbral, que dispara más seguido**, los eventos podrían llegar a 96 y
`t(θ=1)` a 2,77, con `θ` mínimo en **1,44**. **Sigue arriba de 1**, y además mezclar las dos señales
es otra decisión nuestra.

## Qué significa y qué NO significa un negativo

**SÍ significa:** que la regla de rebalanceo tal como se publica no supera las nulas con 48 eventos.

**NO significa** nada sobre el efecto. Con `θ` mínimo en 2,04, **el negativo es el resultado esperado
aunque el efecto esté completo y vivo.** Y hay una asimetría que va escrita: L10 es la candidata con
la **magnitud más grande del inventario**, unos $221 por contrato ES, y **aun así no alcanza**. Eso
dice más sobre nuestro presupuesto de eventos que sobre el rebalanceo institucional.

---

# 6. LA RECOMENDACIÓN, que es no registrarlo

**Igual que `P07`.** Y con un agregado propio: **L10 es la única del inventario que la caja sellada
volvería medible sola**, porque sus 12 eventos anuales se multiplican por 2,65 con 2020-2026 y
llegaría a 127. **Eso es una decisión sobre la caja, no sobre el cartucho, y es de Roberto.**

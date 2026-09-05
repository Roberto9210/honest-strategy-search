# ÍNDICE — candidatas de la literatura académica publicada

**VENTANA L. NADA DE ESTO ESTÁ MEDIDO. No gasta cartucho. K sigue en 261.**

Esta carpeta es la primera vez que el proyecto muestrea un generador de hipótesis que **no somos
nosotros**. Las 261 hipótesis anteriores salieron de Roberto y sus asistentes; éstas salen de
revistas revisadas por pares.

**Todas fueron clasificadas ANTES de cualquier medición**, por la razón que el proyecto ya tiene
escrita: *"un p-valor calculado sobre datos en los que otro ya seleccionó no es un p-valor. Por eso
las reglas de terceros se clasifican ANTES de medirlas: después la clasificación se vuelve
motivada."*

Definiciones de piso, costos y conversión a dólares: **`PISO_Y_CONVERSION.md`**. Lo que busqué y no
pasa: **`DESCARTADAS.md`**.

---

## Orden

**Ordenado por FACILIDAD DE PRUEBA, no por lo prometedor.** Ordenar por promesa es seleccionar, y
seleccionar antes de medir es el error que este proyecto ya cometió 261 veces.

"Facilidad" = cuántos pasos hay entre hoy y un veredicto: datos que ya están, datos gratis que hay
que juntar, datos que hay que comprar, extensiones del juez que hay que construir.

---

## Las que pasan los cuatro filtros duros

| # | candidata | instrumento | clase | datos que faltan | pasos hasta un veredicto |
|---|---|---|---|---|---|
| **[L01](L01_intraday_momentum_futuros_baltussen.md)** | Momento intradiario, versión "resto del día" — Baltussen, Da, Lammers y Martens, *JFE* 2021 | **ES** | ESTADÍSTICA | **ninguno** | **0** |
| **[L02](L02_intraday_momentum_gao_calibracion.md)** | Momento intradiario, versión "primera media hora" — Gao, Han, Li y Zhou, *JFE* 2018 · **calibración** | ES (muestra: SPY) | ESTADÍSTICA | **ninguno** | **0**, más una decisión de definición declarada antes |
| **[L03](L03_deriva_previa_anuncios_kurov.md)** | El precio deriva 30 min antes del dato macro — Kurov, Sancetta, Strasser y Wolfe, *JFQA* 2019 | **ES**, ZN | **DETERMINISTA** en fecha y hora, estadística en signo | calendario de 4 anuncios, gratis | 1 |
| **[L04](L04_rebalanceo_etf_apalancados_cierre.md)** | Los ETF apalancados deben comprar si el día sube — Cheng y Madhavan 2009; Shum et al. 2016; **contra** Ivanov y Lenkey 2018 | **ES** | **DETERMINISTA** en el flujo, estadística en el precio | patrimonio diario de los ETF, gratis | 1 |
| **[L07](L07_fixing_tokio_gotobi.md)** | El fixing de Tokio de las 9:55 y los días *gotobi* — Ito y Yamada, *JIE* 2017 | 6J | **DETERMINISTA** en fecha y hora | 6J 1-min, barato | 3 (magnitud, datos, juez) |
| **[L08](L08_fix_londres_fin_de_mes.md)** | Cobertura cambiaria en el fix de fin de mes — Melvin y Prins, *JFM* 2015 | 6E, 6J | **DETERMINISTA** en fecha, hora **y signo** | 6E 1-min + índices mensuales | 3 |
| **[L06](L06_intraday_momentum_vix_futures.md)** | Momento intradiario en futuros de VIX — Huang, Tsai, Weng y Yang, *JBF* 2023 | VX | ESTADÍSTICA | VX 1-min (CFE) | 4, y **magnitud sin cerrar** |
| **[L09](L09_intraday_momentum_crudo.md)** | Momento intradiario en el crudo — Wen, Gong, Ma y Xu, *Economic Modelling* 2021 | CL (muestra: USO) | ESTADÍSTICA | CL 1-min | 4, y **magnitud sin cerrar** |
| **[L05](L05_gamma_neta_eje_regimen.md)** | La gamma neta como **eje de régimen** — Baltussen et al. 2021 Tabla 7; Huang et al. 2023; **contra** Dim, Eraker y Vilkov 2023 | ES (eje, no regla) | ESTADÍSTICA | opciones SPX, semanas de trabajo | 5 |

**Nueve candidatas. Tres deterministas en fecha y hora (L03, L07, L08) más una determinista en el
flujo (L04).**

Advertencias de lectura, las tres importantes:

- **L01, L02, L04, L05, L06 y L09 son la misma familia** (momento intradiario / cobertura de gamma).
  El juez cuenta intentos por familia declarada **y por huella de entradas**. Hay que declararlas en
  la misma familia; medirlas como seis ideas independientes sería inflar el contador seis veces
  sobre una sola idea.
- **L06 y L09 tienen la magnitud SIN CERRAR** porque el editor bloquea el acceso. Están en la lista
  con esa marca. Si al abrirlas la magnitud queda debajo del piso, se mueven a `DESCARTADAS.md`.
- **El juez sólo acepta `ES` y `MES`** (son los dos instrumentos con comisión medida). L06, L07, L08
  y L09 requieren extender el juez antes de poder juzgarlas: eso es trabajo de la VENTANA G.

---

## Descartadas, con el motivo

Detalle completo y citas en **`DESCARTADAS.md`**. Filtros: **F1** dormir con posición, **F2** muchos
instrumentos, **F3** sin mecanismo, **F4** magnitud debajo del piso.

| candidata | filtro | nota |
|---|---|---|
| Deriva previa a la Fed — Lucca y Moench, *JoF* 2015 | **F1** | La ventana **es** de 24 horas. Y **desapareció después de 2015** (*Finance Research Letters* 2021) |
| Ciclo de subastas del Tesoro — Lou, Yan y Zhang, *RFS* 2013 | **F1** | Forma ejemplar, horizonte de varios días |
| Adelantarse al *Goldman roll* — Mou 2010 | **F1** | Sharpe 4,4 declarado, y decae con el capital de arbitraje, dicho por el autor |
| Rebalanceo institucional de fin de mes — Harvey, Mazzoleni y Melone, NBER 2025 | **F1** | **La que más duele**: ES y ZN, calendario escrito, 17 pb ≈ $221/contrato. Sólo el horizonte la mata |
| Retorno del Tesoro a fin de mes — Hartley y Schwarz 2019 | **F1** | Sharpe ≈ 1, ~25 pb/mes a 10 años |
| Ciclo mensual de caja — Etula et al., *RFS* 2020 | **F1** | Varios días alrededor del cambio de mes |
| **Deriva nocturna del E-mini** — Boyarchenko, Larsen y Whelan, *RFS* 2023 | **F4** | ~$19/sesión. **Y está muerta desde 2021, documentado por los propios autores en 2026** |
| Reversión de fin de día — Baltussen, Da y Soebhag 2024 | **F2** | Corte transversal de acciones. Contraste útil: el índice tiene momento donde las acciones tienen reversión |
| Reversión intradiaria del retorno nocturno — Berkman et al., *JFQA* 2012 | **F2** | Corte transversal, condicionado por atención minorista |
| Manipulación en la liquidación del VIX — Griffin y Shams, *RFS* 2018 | **F2** + sin signo | El salto de 31 pb no tiene dirección predecible |
| Efecto previo a feriado — Ariel, *JoF* 1990 | **F4** | **Replicación fallida**: Ko y Welch 2021 muestran que sobrevive sólo en empresas chicas |
| Vencimiento trimestral — Stoll y Whaley | **F4** | Los propios autores dicen que no son grandes en términos absolutos. Y son 4 eventos/año |
| Prima de días de anuncio — Savor y Wilson, *JFQA* 2013 | **F1** | 11,4 pb ≈ **$148/contrato**, la magnitud más grande que encontré, pero es retorno cierre a cierre |
| Momento intradiario en bonos chinos — Zhang, Wang y Li 2021 | acceso | Mercado chino |
| Falsación de señales OHLCV en MNQ — arXiv 2026 | no es literatura | **Mismo generador que nosotros**: un individuo probando 14 familias de señales |

**Quince descartadas. Siete de ellas mueren por el filtro nocturno.**

---

## Cómo usar esta carpeta

1. **Nada de acá está pre-registrado.** El contador de multiplicidad K sigue en 261 y esta tarea no
   lo tocó. Roberto decide cuáles ameritan gastar un cartucho.
2. **Cada ficha trae un `variantes_probadas` sugerido** para el campo obligatorio del juez. Son
   cotas inferiores contadas de lo publicado: ningún paper declara su barrido completo.
3. **Antes de medir cualquiera, leer su punto 10.** Varias tienen un obstáculo aritmético que se
   resuelve antes de tocar los datos, y en al menos dos casos el obstáculo dice que el veredicto no
   va a significar nada.
4. **El orden de esta lista no es un orden de prioridad.** Es un orden de costo. Que L01 esté
   primera significa que es la más barata de probar, no la mejor.

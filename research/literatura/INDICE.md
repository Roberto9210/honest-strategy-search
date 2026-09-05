# ÍNDICE — candidatas de la literatura académica publicada

**VENTANA L. NADA DE ESTO ESTÁ MEDIDO. No gasta cartucho. K sigue en 261.**

Esta carpeta es la primera vez que el proyecto muestrea un generador de hipótesis que **no somos
nosotros**. Todas las candidatas fueron clasificadas **antes** de cualquier medición.

| documento | qué es |
|---|---|
| [FILTROS.md](FILTROS.md) | los filtros con sus umbrales **derivados**, y la aplicación a todo el inventario |
| [PISO_Y_CONVERSION.md](PISO_Y_CONVERSION.md) | pisos, costos y conversión a dólares, definidos una sola vez |
| [M01_test_de_mecanismo.md](M01_test_de_mecanismo.md) | **probar el mecanismo en vez de la ventaja**, y los cuatro tests disponibles |
| [DESCARTADAS.md](DESCARTADAS.md) | trece descartadas con cita y motivo |

---

## El resultado en tres líneas

1. **Once candidatas pasan los filtros.** Dos de ellas, L10 y L11, fueron **recuperadas** al corregir
   el filtro nocturno por uno de ventana de exposición.
2. **Ninguna es MEDIBLE sobre 2016-2019 a la vara del juez.** La mejor se queda corta por un factor
   de dos. **Todas las de ES son RENTABLES a nocional 2026.**
3. **Siete tienen el mecanismo probable por separado de la rentabilidad**, y ahí el orden es otro.

---

## Orden por DISTANCIA A UN VEREDICTO

El orden viejo era por facilidad de acceso a los datos. Éste es por **cuánto le falta a cada una para
ser medible**, que es lo que decide si el veredicto va a significar algo. `falta` es el factor por el
que se queda corta de eventos contra la vara derivada en `FILTROS.md`.

| # | candidata | instrumento | clase | A neto/op | eventos/año | **falta** | mecanismo aparte |
|---|---|---|---|---|---|---|---|
| **[L11](L11_prima_dias_anuncio_savor_wilson.md)** | Prima de días de anuncio macro — Savor y Wilson, *JFQA* 2013 · **recuperada** | ES / MES | **DETERMINISTA** en fecha, signo fijo | $117 | 40 | **1,9×** | — |
| **[L10](L10_rebalanceo_institucional_harvey.md)** | Rebalanceo institucional de fin de mes — Harvey, Mazzoleni y Melone, NBER 2025 · **recuperada** | **ES y ZN** | **DETERMINISTA** en fecha y signo | **$204** | 12 a 24 | **2,1×** | **sí**, t ≈ 1,4 |
| **[L03](L03_deriva_previa_anuncios_kurov.md)** | Deriva 30 min antes del dato macro — Kurov et al., *JFQA* 2019 | **ES**, ZN | **DETERMINISTA** en fecha y hora | $86 | 48 | **2,9×** | **sí**, t ≈ 2,7 |
| **[L07](L07_fixing_tokio_gotobi.md)** | Fixing de Tokio de las 9:55 y días *gotobi* — Ito y Yamada, *JIE* 2017 | 6J | **DETERMINISTA** en fecha y hora | ≈ $35 | 250 | **3,4×** | sí |
| **[L01](L01_intraday_momentum_futuros_baltussen.md)** | Momento intradiario en 60+ futuros — Baltussen et al., *JFE* 2021 | **ES** | estadística | $18 | 252 | **12,6×** | **sí**, t ≈ 1,0 |
| **[L02](L02_intraday_momentum_gao_calibracion.md)** | Momento intradiario, versión original — Gao et al., *JFE* 2018 · **calibración** | ES | estadística | $17 | 252 | **14,1×** | sí |
| [L04](L04_rebalanceo_etf_apalancados_cierre.md) | Rebalanceo obligatorio de ETF apalancados — Cheng y Madhavan 2009 y la disputa | ES | **DETERMINISTA** en el flujo | = L01 | 252 | 12,6× | sí |
| **[L08](L08_fix_londres_fin_de_mes.md)** | Cobertura cambiaria en el fix de fin de mes — Melvin y Prins, *JFM* 2015 | 6E, 6J | **DETERMINISTA** en fecha, hora **y signo** | ≈ $55 | 12 | **28×** | **sí, t ≈ 3,4 — el más potente del inventario** |
| [L06](L06_intraday_momentum_vix_futures.md) | Momento intradiario en futuros de VIX — Huang et al., *JBF* 2023 | VX | estadística | ≈ $11 | 252 | 34× | no, falta el dato |
| [L09](L09_intraday_momentum_crudo.md) | Momento intradiario en el crudo — Wen et al., *Economic Modelling* 2021 | CL | estadística | sin cerrar | 250 | — | no, falta el dato |
| [L05](L05_gamma_neta_eje_regimen.md) | Gamma neta como **eje de régimen** — tres mercados, y una contradicción | ES | eje, no regla | — | — | — | **es un test de mecanismo** |

**Once candidatas. Cinco deterministas en fecha (L03, L07, L08, L10, L11) más una en el flujo (L04).**

## Lo que hay que leer antes de tocar cualquiera

- **Nadie es medible con 2016-2019 solo.** La caja sellada 2020-2026 volvería medibles a **L10 y
  L11, y a ninguna otra**. La aritmética está en `FILTROS.md`; la decisión es de Roberto y la caja
  tiene un solo uso.
- **L01, L02, L04, L05, L06 y L09 son la misma familia.** El juez cuenta por familia declarada y por
  huella de entradas. Declararlas como seis ideas independientes inflaría K seis veces sobre una.
- **El juez sólo acepta `ES` y `MES`.** L06, L07, L08 y L09 necesitan que se le mida comisión y
  deslizamiento a otro instrumento antes de poder juzgarlas.
- **L06 y L09 tienen la magnitud SIN CERRAR** porque el editor bloquea el acceso. Si al abrirlas
  quedan debajo del piso, se mueven a `DESCARTADAS.md`.
- **Cada ficha trae un `variantes_probadas` sugerido.** Son cotas inferiores contadas de lo
  publicado: ningún paper declara su barrido completo.

## Y una advertencia sobre este orden

**Sigue sin ser un orden de prioridad.** Es un orden de distancia a un veredicto. Que L11 esté
primera significa que es la que menos lejos está de poder decidirse, **no que sea la mejor apuesta**.
Ordenar por promesa es seleccionar, y seleccionar antes de medir es el error que este proyecto ya
cometió 261 veces.

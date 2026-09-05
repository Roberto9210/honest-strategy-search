# L09 — El mismo momento intradiario en el petróleo, pero con una diferencia que importa

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

---

## 1. Cita completa

Wen, Zhuzhu; Gong, Xu; Ma, Diandian; Xu, Yahua (2021). **"Intraday momentum and return
predictability: Evidence from the crude oil market."** *Economic Modelling*, vol. 95, pp. 374–384.
DOI: https://doi.org/10.1016/j.econmod.2020.03.004

- Editorial: https://www.sciencedirect.com/science/article/abs/pii/S0264999319310417
- SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3553682
- RePEc: https://ideas.repec.org/a/eee/ecmode/v95y2021icp374-384.html

**Trabajo posterior del mismo grupo:** Wen, Indriawan, Lien y Xu (2023), "Intraday Return
Predictability in the Crude Oil Market: The Role of EIA Inventory Announcements", *The Energy
Journal* 44(4).

## 2. El efecto, en una frase

En el petróleo también el retorno de la primera media hora predice el de la última media hora — pero
a diferencia de las acciones, **sólo la primera media hora funciona**, y lo que pasa en el medio del
día no aporta nada.

## 3. Instrumento y período de la muestra original

- **United States Oil Fund (USO)**, el ETF sobre petróleo, datos de alta frecuencia,
  **2006 → 2018**.
- **Ojo con esto: la muestra es un ETF, no el futuro CL.** El USO tiene su propio problema de roll
  y su propio error de seguimiento contra el futuro. **Trasladar de USO a CL no es gratis**, igual
  que en L02 trasladar de SPY a ES no es gratis.

## 4. Magnitud declarada

Los autores reportan que una estrategia de temporización basada en el hallazgo **genera ganancias
sustanciales**, y descomponen el predictor: la primera media hora se parte en el componente
**nocturno** y el de la **apertura**, y **el nocturno contiene más información predictiva**.

**No pude obtener las tablas con los números.** El editor devuelve 403 y los resúmenes públicos
hablan de "ganancias sustanciales" sin cifra.

**Magnitud: SIN CERRAR.** No la invento y no la estimo por analogía con L02, porque la volatilidad
del petróleo es varias veces la del S&P 500 y una regla de tres daría un número inventado con cara
de medición.

## 5. Antes o después de costos

**No verificado.**

## 6. Mecanismo declarado

**Los mismos dos de Gao et al. (L02)**, y los autores los citan como tales:

1. **Rebalanceo infrecuente de carteras.**
2. **Presencia de inversores informados tarde.**

**Y un control negativo que vale más que el mecanismo:** el mercado del petróleo tiene un patrón de
volumen intradiario propio, causado por los **anuncios rutinarios de inventarios** (la EIA publica
los miércoles a las 10:30 ET). Los autores verifican si esa es la fuente de la predictibilidad y
encuentran que **la información de los anuncios de inventarios NO da predictibilidad para el retorno
de la última media hora**.

**Ése es un buen control**: la explicación más obvia y más específica del mercado fue probada y
descartada por los propios autores. Es raro y hay que anotarlo a favor.

## 7. CLASIFICACIÓN

**ESTADÍSTICA.**

## 8. Estado de replicación

- Es una **extensión** de Gao et al. (2018) a otro mercado, no una replicación independiente del
  resultado del S&P 500.
- **La diferencia con el resultado de acciones es el dato más informativo de esta ficha**, y va en
  contra de la familia: en el petróleo **sólo `r1` predice**, mientras que en los futuros de índice
  Baltussen et al. (L01) encuentran que el predictor **más fuerte** es `rROD`, el retorno de todo el
  día hasta 30 minutos antes del cierre, y que `rROD` supera a `r1`. **Los dos papers de la misma
  familia dan predictores distintos como ganadores en mercados distintos.**
- El seguimiento de 2023 en *The Energy Journal* profundiza el rol de los anuncios de inventarios de
  la EIA, lo que indica que el grupo siguió trabajando la línea.
- **No encontré replicación independiente ni evidencia posterior a 2018 sobre CL.**

## 9. Cuántas variantes probaron los autores

Contable: las **13 medias horas** como predictores candidatos, de las que reportan que sólo la
primera funciona; la **descomposición** de la primera media hora en componente nocturno y de
apertura; los cortes por anuncios de inventarios; y presumiblemente cortes por volatilidad y volumen
como en el paper original.

**Para el juez: `variantes_probadas` = 30 como mínimo.**

**Y hay un problema de multiplicidad que trasciende al paper y que nadie declara:** este trabajo es
uno de **muchos** que aplican la plantilla de Gao et al. a un mercado nuevo. En esta misma carpeta
hay cuatro (L01 futuros, L06 VIX, L09 petróleo, más bonos chinos y Asia-Pacífico en las descartadas).
**La literatura publicada de "intraday momentum en el mercado X" es en sí misma una búsqueda con
sesgo de publicación**: los mercados donde no dio nada no se publican, o se publican como el de
Asia-Pacífico, que reporta honestamente que en Hong Kong y Singapur no hay nada.

**Ese es el conteo de multiplicidad que hay que declarar y que no está en ningún paper: cuántos
mercados se probaron en total, contando los que no llegaron a revista.** No lo sé, y nadie lo sabe.

## 10. Qué haría falta para probarla acá

**Datos: NO LOS TENEMOS.** Hace falta **CL 1-min** 2016-2019.

**Obstáculos, en orden:**

1. **Magnitud sin cerrar.** Hay que abrir el paper. Si la ganancia declarada, traducida a dólares
   por sesión por contrato CL y neta de costos, queda debajo del piso, se termina acá.
2. **El juez no acepta CL** (`instrumento`: sólo `ES` o `MES`). Habría que medirle comisión y
   deslizamiento.
3. **El contrato CL es grande y volátil**: 1.000 barriles, ~$65.000 de nocional con el crudo a $65,
   pero con una volatilidad diaria mucho mayor que la del ES. Para una cuenta de fondeo con
   drawdown de $2.000 eso es un problema de dimensionamiento que la VENTANA G ya sabe medir y esta
   ventana no.
4. **El traslado de USO a CL** no está hecho por nadie.

**Cuatro obstáculos y ninguna magnitud. Está última en el índice y ahí se queda.**

**La razón por la que igual queda anotada:** si alguna vez L01 se mide y da algo en ES, la pregunta
inmediata es si el efecto es del S&P 500 o de los futuros en general. **L09 y L06 son las dos
respuestas publicadas a esa pregunta**, y conviene tenerlas identificadas antes de necesitarlas y no
después, que es cuando la búsqueda se vuelve motivada.

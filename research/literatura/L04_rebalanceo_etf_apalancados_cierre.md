# L04 — Los ETF apalancados están OBLIGADOS por prospecto a comprar cuando el día sube y vender cuando baja, cerca del cierre

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

Ésta es la única candidata del lote donde el flujo que mueve el precio **está escrito en un
documento legal**, con su fórmula, y no hay que inferirlo de una regresión.

---

## 1. Cita completa

**La fórmula y el mecanismo:**
Cheng, Minder; Madhavan, Ananth (2009). **"The Dynamics of Leveraged and Inverse Exchange-Traded
Funds."** *Journal of Investment Management*, vol. 7, n.º 4, pp. 43–62.
SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=1539120

**La evidencia a favor:**
Shum, Pauline; Hejazi, Walid; Haryanto, Edgar; Rodier, Arthur (2016). **"Intraday Share Price
Volatility and Leveraged ETF Rebalancing."** *Review of Finance*, vol. 20, n.º 6, pp. 2379–2409.
https://academic.oup.com/rof/article-abstract/20/6/2379/2418138

**La evidencia en contra:**
Ivanov, Ivan T.; Lenkey, Stephen L. (2018). **"Do leveraged ETFs really amplify late-day returns and
volatility?"** *Journal of Financial Markets*, vol. 41, pp. 36–56.
https://www.sciencedirect.com/science/article/abs/pii/S1386418117302604

**El efecto combinado con opciones:**
Barbon, Andrea; Beckmeyer, Heiner; Buraschi, Andrea; Moerke, Mathis (2022). **"Liquidity Provision to
Leveraged ETFs and Equity Options Rebalancing Flows: Evidence from End-of-Day Stock Prices."**
Swiss Finance Institute Research Paper 22-40.
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3925725

**La revisión:**
Lenkey, Stephen L. (2024). "The market impact of leveraged ETFs: A survey of the literature."
*Quantitative Finance and Economics*. https://www.aimspress.com/article/doi/10.3934/QFE.2024031

## 2. El efecto, en una frase

Un ETF apalancado promete multiplicar por 2 o por 3 el retorno **de un solo día**, y para cumplir esa
promesa tiene que ajustar su exposición todos los días cerca del cierre, **siempre en la misma
dirección en que se movió el día** — lo que empuja el precio en esa dirección justo al final.

## 3. Instrumento y período de la muestra original

- **Cheng y Madhavan (2009):** es un paper teórico. Derivan la fórmula del rebalanceo. No hay
  muestra empírica de retornos.
- **Shum et al. (2016):** ETF apalancados estadounidenses y sus subyacentes, **2006–2011**.
- **Ivanov y Lenkey (2018):** ETF apalancados estadounidenses de renta variable, **2006–2014**.
- **Barbon et al. (2022):** acciones individuales estadounidenses, precios de fin de día.

**Ninguno mide directamente el futuro ES.** El puente al ES lo pone Baltussen et al. (2021, ficha
**L01**), que muestran una relación positiva y significativa entre la cuota de mercado de los ETF
apalancados de cada mercado y el t-estadístico del momento intradiario, en la submuestra 2006–2020.

## 4. Magnitud declarada

**La fórmula es exacta y es lo mejor que tiene esta candidata.** Un fondo con apalancamiento `x` y
patrimonio `A`, después de un día con retorno `r` del subyacente, tiene que operar:

```
monto a operar  =  A · x · (x − 1) · r
```

| apalancamiento del fondo | multiplicador `x(x−1)` | ¿compra o vende si el día subió? |
|---|---|---|
| **+3×** | 6 | compra |
| **+2×** | 2 | compra |
| **−1×** (inverso) | 2 | **compra** |
| **−2×** | 6 | **compra** |
| **−3×** | 12 | **compra** |

**Todos compran cuando el día sube y todos venden cuando baja, sin importar el signo del
apalancamiento.** Los inversos también. No hay compensación entre ellos: se suman.

**Efecto sobre el precio, medido:**
- Shum et al. (2016): la volatilidad de fin de día está **positiva y significativamente**
  correlacionada con el cociente entre el rebalanceo potencial y el volumen total, 2006–2011.
- Barbon et al. (2022): un desvío estándar más de flujo de rebalanceo de ETF apalancados sube el
  retorno de fin de día en **430 % del retorno medio de la última media hora**.

**Traducción a dólares por sesión por contrato ES: NO SE PUEDE, y no la invento.** Los resultados
publicados están en unidades de "desvíos de flujo" y de volatilidad, sobre acciones individuales, y
no hay una tabla de dólares por contrato de futuro. **La magnitud en dólares hay que medirla acá o
no se sabe.** Es la debilidad principal de esta ficha frente al filtro de piso.

## 5. Antes o después de costos

**No aplica: ninguno de estos papers propone una estrategia.** Miden impacto de flujo sobre precio y
volatilidad. La conversión a una estrategia neta de costos no está hecha en la literatura.

## 6. Mecanismo declarado

**Rebalanceo mecánico obligatorio por diseño del producto**, no por comportamiento de nadie.

El ETF apalancado promete el múltiplo del retorno **diario**. Eso obliga a reajustar la exposición
cada día al cierre. La obligación está en el prospecto, la fórmula es la del punto 4, y **el signo
del flujo se conoce durante el día**, porque depende sólo del retorno acumulado hasta ese momento.

Es el mismo mecanismo de gamma corta de **L01** y **L05**, pero con una diferencia que importa
mucho para este proyecto: **acá no hay que estimar la posición de nadie.** El patrimonio de los
fondos es público y diario, y el múltiplo está en el nombre del fondo.

## 7. CLASIFICACIÓN

**DETERMINISTA en el flujo, ESTADÍSTICA en el precio.**

- El **flujo** es determinista de verdad: dado el patrimonio y el retorno del día, el monto y el
  signo de la operación obligatoria se calculan exactamente, sin estimar nada. Se verifica con
  pocos casos.
- El **efecto sobre el precio** es estadístico, y **está disputado en la literatura publicada**.
  Ver punto 8.

## 8. Estado de replicación

**Ésta es la ficha del lote con la disputa mejor documentada, y la disputa cae del lado incómodo.**

**A favor:**
- Shum et al. (2016), *Review of Finance*: correlación positiva y significativa entre volatilidad
  de fin de día y rebalanceo potencial sobre volumen, 2006–2011.
- Barbon et al. (2022): efecto grande sobre retornos de fin de día, combinando ETF apalancados con
  cobertura delta de opciones.
- Baltussen et al. (2021), *JFE*: relación transversal positiva entre cuota de ETF apalancados y
  fuerza del momento intradiario en 60+ futuros.
- Lenkey (2024), revisión: la literatura reporta consistentemente asociaciones estadísticamente
  significativas entre demanda de rebalanceo y retornos y volatilidad de fin de día.

**En contra, y es un argumento estructural, no un p-valor:**
**Ivanov y Lenkey (2018), *Journal of Financial Markets*.** Muestran **teóricamente** que los flujos
de capital de entrada y salida de los propios fondos **reducen la demanda de rebalanceo y la
eliminan en el límite**: si el fondo recibe dinero un día que subió, ya tiene que comprar de todos
modos, y las dos necesidades se cancelan. Y lo verifican empíricamente con ETF estadounidenses de
renta variable **2006–2014**: los flujos de capital reducen sustancialmente la demanda de
rebalanceo **incluso en períodos de tensión severa**, y el efecto sobre los retornos de fin de día
es **económicamente insignificante**.

**Cómo leer la disputa sin resolverla:** Shum et al. miden **volatilidad**, Ivanov y Lenkey miden
**retornos**. No es imposible que las dos cosas sean ciertas: el flujo agita el precio sin darle
dirección. **Para este proyecto sólo sirve la dirección**, y sobre la dirección la evidencia
publicada dice que no.

**Eso es un motivo fuerte para bajar esta candidata en la lista de prioridad, y ninguno para
sacarla del inventario.**

## 9. Cuántas variantes probaron los autores

- **Cheng y Madhavan:** ninguna. Es una derivación.
- **Shum et al.:** múltiples ventanas de fin de día, múltiples familias de ETF, submuestras de
  crisis. No publican barrido completo.
- **Ivanov y Lenkey:** su resultado principal es una predicción teórica contrastada, lo que reduce
  el problema de multiplicidad respecto de una búsqueda de patrones.
- **Barbon et al.:** combinan dos fuentes de flujo (ETF y opciones) y varias medidas de gamma
  agregada.

**Para el juez, si alguna vez se prueba: `variantes_probadas` = 10.** El mecanismo llega desde la
teoría, no desde un barrido, lo que es una defensa real — pero la especificación empírica concreta
(qué ventana, qué escala del flujo) sí es elegida.

## 10. Qué haría falta para probarla acá

**Datos de precio: NINGUNO NUEVO.** ES 1-min 2016-2019.

**Dato que falta:** el **patrimonio diario** de los ETF apalancados sobre el S&P 500 entre 2016 y
2019 (SSO, SDS, UPRO, SPXU, SPXL, SPXS y los inversos). Es público —los emisores lo publican
diariamente— pero armar la serie histórica diaria de 2016-2019 es trabajo de recolección, no una
compra. **Un día o dos de trabajo.**

**La versión barata, y hay que decir por qué es peor:** sin el patrimonio, la señal se reduce al
signo del retorno del día, que es **exactamente `rROD` de L01**. O sea que la versión barata de esta
candidata **no es una candidata nueva: es L01 otra vez**. Lo que L04 aporta sobre L01 es la
**escala** del flujo, y sin el patrimonio no hay escala.

**Eso significa que L04 no se debe medir antes que L01.** Si L01 no da nada, la escala no lo va a
salvar; y si L01 da algo, la escala es la primera pregunta que sigue. **Es una candidata de segunda
ronda por construcción, no por promesa.**

### Advertencia sobre el conteo de multiplicidad

L01, L04 y L05 comparten mecanismo y comparten en gran parte las entradas. El juez cuenta intentos
**por familia declarada y por huella de entradas a tres tamaños de cubeta**
(`JUEZ_COMO_SE_USA.md`), justamente para que no se esquive con esperas. **Las tres tienen que
declararse en la misma familia.** Medirlas como tres ideas independientes sería inflar K por
triplicado sobre una sola idea.

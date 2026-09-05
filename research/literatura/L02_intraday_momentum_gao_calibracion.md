# L02 — El retorno de la primera media hora predice el de la última media hora

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

**Ésta es la ficha de calibración**: la trajo Roberto ya identificada y sirve para fijar el formato.
Todo lo que sigue está verificado contra el manuscrito, no contra el resumen del encargo.

---

## 1. Cita completa

Gao, Lei; Han, Yufeng; Li, Sophia Zhengzi; Zhou, Guofu (2018). **"Market intraday momentum."**
*Journal of Financial Economics*, vol. 129, n.º 2, pp. 394–414.

Primer borrador marzo de 2014; versión de trabajo junio de 2017 (Iowa State, UNC Charlotte,
Rutgers, Washington University in St. Louis).

- Editorial: https://www.sciencedirect.com/science/article/abs/pii/S0304405X18301351
- SSRN: https://ssrn.com/abstract=2440866
- RePEc: https://econpapers.repec.org/RePEc:eee:jfinec:v:129:y:2018:i:2:p:394-414

## 2. El efecto, en una frase

Si el mercado subió en la primera media hora de la rueda —medida desde el cierre del día anterior—,
la última media hora antes del cierre también tiende a subir; y al revés si bajó.

## 3. Instrumento y período de la muestra original

- **SPY**, el ETF del S&P 500, datos de alta frecuencia, **1 de febrero de 1993 → 31 de diciembre
  de 2013**. Unas 5.200 sesiones.
- La rueda se parte en **13 medias horas**: `r1` es de las 16:00 del día anterior a las 10:00, y
  `r13` es la última media hora.
- Otros **11 ETF** (DIA, QQQ, IWM, EEM, FXI, EFA, VWO, XLF, IYR, TLT).

**Sobre los futuros:** el encargo decía que los autores afirman que en futuros del S&P 500 da
similar. **Confirmado, pero es una nota al pie.** Nota 2 del manuscrito: *"Los resultados son
similares cuando usamos los futuros del S&P 500, otro activo negociable sobre el índice (ver el
apéndice de internet)."* **No hay ninguna tabla de futuros en el cuerpo del paper.** El número de
futuros que sí existe tabulado está en **L01**, que es un paper distinto.

## 4. Magnitud declarada

Regresión en muestra de la última media hora sobre la primera:

| predictor | pendiente (×100) | t | R² |
|---|---|---|---|
| `r1` | 6,94 | 4,08 | **1,6 %** |
| `r12` | 11,8 | 2,62 | 1,1 % |
| ambos | — | — | 2,6 % |

Estrategia de temporización (posición en la última media hora según el signo de `r1`):

| | retorno anual | desvío | Sharpe | asimetría | tasa de acierto |
|---|---|---|---|---|---|
| señal `r1` | **6,67 %** | 6,19 % | **1,08** | 0,90 | **54,37 %** |
| siempre largo la última media hora | −1,11 % | 6,21 % | −0,18 | — | 50,42 % |
| comprar y mantener todo el período | 6,04 % | 20,57 % | 0,29 | — | — |

Anualizan multiplicando por 252 porque operan una vez por día, aunque estén en el mercado sólo media
hora. La ganancia de certeza equivalente es 6,02 % anual con `r1`, y 6,18 % agregando `r12`.

### Traducción a dólares por sesión por contrato ES

| | ES 2016-2019 | ES a precios de 2026 |
|---|---|---|
| 6,67 % anual, una operación por sesión | **≈ $34 / sesión** | ≈ $85 / sesión |

**Cae en el borde inferior del piso de detectabilidad del proyecto** ($29 a $58 por operación con
1.000 operaciones). Neto del costo de una ida y vuelta por sesión (≈ $17: medio-spread de entrada,
medio-spread de salida y comisión) quedan **≈ $17 netos**, que ya está **debajo** del piso. Ver
`PISO_Y_CONVERSION.md`.

**Y el neto del paper no ayuda acá:** los autores reportan 4,46 % anual después de costos, que son
**≈ $23 por sesión** — también debajo del piso de detectabilidad.

## 5. Antes o después de costos

**Las dos cosas, y el paper las separa bien.** Sección 6.1 y Tabla 10.

| | retorno anual | desvío | Sharpe |
|---|---|---|---|
| señal `r1`, bruto | 6,67 % | 6,19 % | 1,08 |
| señal `r1`, **neto de costos** | **4,46 %** | 6,10 % | **0,73** |
| señal `r1` + `r12`, bruto | 5,50 % | — | — |
| señal `r1` + `r12`, neto | 4,74 % | — | — |

El costo asumido es el **spread compra-venta del SPY**, y **ignoran explícitamente la comisión**
(nota 14). Restringido al período posterior a la decimalización (después del 1 de julio de 2001) el
costo baja: el retorno cae sólo 1,22 puntos, a 4,30 % anual. En los últimos años de la muestra el
neto es 6,52 % contra 7,96 % bruto.

**Advertencia para el traslado a ES:** el costo relevante en ES no es el spread del SPY. El juez de
este proyecto usa comisión medida (help.tradeify.co) y **deslizamiento medido en el stop**
(`media_exceso.py`). Los 4,46 % netos del paper **no se pueden usar como si fueran el neto de ES**.

## 6. Mecanismo declarado

Los autores dan **dos**, y los dan como complementarios, no como alternativas:

1. **Rebalanceo infrecuente** (Bogousslavsky, *Journal of Finance* 2016, "Infrequent Rebalancing,
   Return Autocorrelation, and Seasonality"; Duffie 2010 sobre capital lento). Hay inversores que
   demoran su rebalanceo hasta cerca del cierre en vez de operar en la apertura. Operar al final en
   la misma dirección que al principio produce correlación positiva entre las dos puntas del día.

2. **Inversores informados tarde.** Ante una noticia buena, algunos compran rápido y empujan la
   primera media hora. Otros se enteran más tarde o procesan la noticia más despacio, y cuando
   salen a comprar eligen la última media hora porque es el período más líquido después de la
   apertura. Los partícipes de fondos mutuos sólo pueden operar al precio de cierre, lo que los
   convierte técnicamente en "informados tarde".

Los autores cierran diciendo que hay probablemente otras explicaciones y que hace falta un modelo
de equilibrio dinámico. **No lo tienen.**

## 7. CLASIFICACIÓN

**ESTADÍSTICA.** Tendencia con R² de 1,6 %, decidida por acumulación de operaciones.

## 8. Estado de replicación

**Ésta es la parte que el encargo no traía y que cambia la lectura de la candidata.**

**Replicación que falla, en el instrumento que importa:**
**Rosa, Carlo (2022). "Understanding intraday momentum strategies." *Journal of Futures Markets*,
vol. 42, n.º 12, pp. 2218–2234.** DOI 10.1002/fut.22375.
Estudia el desempeño fuera de muestra de la estrategia sobre **futuros del E-mini S&P 500**, con el
retorno nocturno como predictor de la última media hora. **La predictibilidad desaparece fuera de
muestra.** Un modelo de cambio de régimen (Markov) identifica dos regímenes de manera endógena, y
los autores concluyen que la predictibilidad depende de la **fuerza de la señal**, no del calendario,
y que evaluar predictibilidad en tiempo de calendario puede llevar a conclusiones falsas cuando la
anomalía tiene retornos que varían en el tiempo. Una estrategia con umbrales rinde más que una
siempre activa.

**Replicación parcial, internacional:**
Limkriangkrai, Manapon; Chai, Daniel; Zheng, Gaoping (2023). "Market intraday momentum: APAC
evidence." *Pacific-Basin Finance Journal*, vol. 80, 102086. Acceso abierto,
https://doi.org/10.1016/j.pacfin.2023.102086.
El efecto aparece en China y Japón, es **débil** en Corea del Sur, y **no aparece** en Hong Kong ni
en Singapur. Se debilita durante la crisis de COVID. Conclusión de los autores: *el efecto no es tan
generalizado en Asia-Pacífico como sugiere la evidencia estadounidense.*

**Extensión que sí sostiene el efecto:** el paper de **L01** (Baltussen et al., JFE 2021), con 60+
futuros y muestra hasta 2020. Es la mejor evidencia a favor y está en su propia ficha.

**Contexto de decaimiento:** McLean y Pontiff (2016) miden que las anomalías publicadas rinden 26 %
menos fuera de muestra y **58 % menos después de publicadas**. Este paper se publicó en 2018; los
datos de este proyecto (2016-2019) están **a caballo de la publicación**.

## 9. Cuántas variantes probaron los autores

**Declarable: no menos de 12, y probablemente muchas más.** El paper no publica un barrido completo.

Lo contable de lo publicado:
- La rueda se divide en **13 medias horas** y de esas eligen **dos** (`r1` y `r12`) como predictores
  de `r13`. Elegir 2 de 12 candidatos posibles es una búsqueda, aunque la Tabla 1 sólo muestre las
  dos elegidas. `r12` lo justifican después: su predictibilidad *"viene en gran parte del período de
  la crisis financiera"*, mientras que la de `r1` es significativa con crisis y sin crisis.
- **11 ETF adicionales**, y la nota 16 declara la selección: *"Excluimos un par de ETF muy operados
  … y algunos otros para tener un conjunto diverso y manejable."* **Es una selección declarada por
  los propios autores.**
- **3 estrategias** de temporización (ecuaciones 3 a 5).
- **3 terciles** de volatilidad y 3 de volumen.
- Submuestras de recesión, de crisis, de días de noticias macro, y en muestra contra fuera de muestra.

Para el campo `variantes_probadas` del juez: **declarar 10 como mínimo** (umbral 3,7 desvíos). Con
el producto ventanas × ETF × cortes, 100 (umbral 4,3) no es exagerado.

## 10. Qué haría falta para probarla acá

**Datos: NINGUNO NUEVO.** ES 1-min Databento 2016-2019, ya en el repo.

Hay **una decisión de definición** que hay que tomar antes y que no es cosmética: `r1` de los
autores se mide **desde el cierre del día anterior**, o sea que incluye el hueco nocturno. En ES la
sesión de Globex abre a las 17:00 CT y no hay hueco comparable al del SPY. Definir "el cierre
anterior" en ES es una decisión, y una decisión tomada mirando resultados es selección. **Se declara
antes de correr, y se declara cuál se eligió y por qué.**

Roberto ya tiene medido el hecho que hace falta para decidirlo sin mirar resultados: la barra diaria
de NT8 en ES corresponde a la sesión ETH y la apertura diaria es la reapertura de las 17:00 CT
(memoria `nt8-daily-bar-es-sesion-eth`).

**Forma de entrada para el juez:**

```
señal   : signo del retorno del cierre anterior a los 30 min de rueda
entrada : una operación por sesión, a la barra de 30 min antes del cierre
salida  : {"tipo": "tiempo", "n_barras": 30}
```

### El problema de potencia, dicho antes de medir

La ventaja declarada en tasa de acierto es **+3,95 puntos** (54,37 % contra 50,42 % de la posición
pasiva). La diferencia mínima detectable del proyecto con 1.000 operaciones está entre **3,70 y
3,98 puntos** (`research/ventana_g/salida_piso_ventaja.txt`).

**La ventaja publicada coincide con el piso de detección casi exactamente.** Con 1.007 sesiones y
una operación por sesión, la prueba tiene alrededor del 50 % de probabilidad de detectarla **aunque
sea completamente cierta**. Una moneda decide.

Esto es mejor que L01 —cuya ventaja declarada es la mitad del piso— pero no alcanza para un
veredicto que signifique algo. Las tres salidas son las mismas y están escritas en L01.

---

## La interacción que Roberto pidió anotar y NO resolver

**Del paper (sección 3.4, Tabla 3 Panel A):** ordenan las ruedas en terciles según la volatilidad de
la primera media hora.

| tercil de volatilidad de la primera media hora | R² (predictores conjuntos) |
|---|---|
| bajo | **0,6 %**, y el coeficiente de `r1` **no es significativo** |
| medio | intermedio y significativo |
| alto | **3,3 %** |

**El R² sube más de cinco veces del tercil bajo al alto.** Los autores lo enlazan con su mecanismo:
a mayor volatilidad, mayor probabilidad de que la tendencia de la primera media hora se arrastre; y
la última media hora tiene volumen y volatilidad altos, lo que hace más fuerte el impacto del
comercio informado.

**Del proyecto (`research/ventana_g/juez_regimen_exante.py`):** el **piso** de la evaluación también
sube con la volatilidad, y sube mucho: de **$5,07 a $105,34** por sesión entre el tercil bajo y el
alto de volatilidad de **la sesión anterior**, cociente **20,8×** y monótono. Con el eje de
volatilidad de la sesión entera (hindsight) el piso va de $2,29 a $118,61.

**La pregunta abierta, en una línea:** el efecto es ~5× más fuerte en los días movidos, pero el piso
que hay que superar es ~20× más alto en los días movidos. **Si eso es un negocio o lo contrario es
un cociente de dos números medidos, y no lo calculo.**

Tres cosas que hay que cuidar antes de que alguien lo calcule, y las dejo escritas:

1. **Los ejes no son el mismo eje.** El paper ordena por volatilidad de la **primera media hora del
   mismo día**. El juez ordena por volatilidad de la **sesión anterior**. El primero es conocible
   recién a las 10:00; el segundo, al abrir. Son distintos y no son intercambiables.
2. **R² no es dólares.** Un R² 5× mayor no da una ventaja en dólares 5× mayor. La traducción pasa
   por el desvío del retorno de la última media hora, que también es mayor en los días movidos.
3. **El agrupamiento de volatilidad de este mercado es de cola, no de centro** (memoria
   `agrupamiento-volatilidad-es-de-cola`): en ES 2016-2019 la mediana es 1,00× y el p95 es 1,51×.
   Un tercil "alto" definido sobre esa distribución no es lo mismo que el tercil alto de la muestra
   de los autores.

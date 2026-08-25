# Búsqueda multi-mercado — paquete del día cero

**Esto NO abre una fase.** Es el paquete que decide **si** se abre. No gasta un solo cartucho, no
pre-registra nada, no compra datos. La Fase 2 está cerrada y este documento no la toca: §8.3 exige spec
nueva y documento nuevo, y **cualquier búsqueda futura hereda K = 257** (§1.6).

**Entregable de esta tanda: la predicción sobre ρ, NG y HG, σ a ciegas con la tabla de fricción,
la potencia con el n efectivo real, y la regla de decisión.** No se pre-registra nada.

---

## 0. La prohibición, antes que cualquier otra cosa

> **Es UNA hipótesis pre-registrada. K = 1. La regla es la del cartucho 1 con sus parámetros
> CONGELADOS —`reversion_k_dias`, k = 3, h = 3, side = 1— exactamente como está en el ledger
> (`d38a1e04c6bfc0f8`), y se prueba TAL CUAL en todos los mercados.**
>
> **Re-optimizar k o h por mercado está prohibido**, y no por gusto: rompe las dos cosas que hacen que
> este diseño valga algo.

**Qué le pasa a la vara si se re-optimiza** (aritmética, no opinión):

| Diseño | K | z bilateral exigido |
|---|---|---|
| **Una hipótesis congelada** | **1** | **1,960** |
| Grilla de 4 k × 5 h re-optimizada en 12 mercados | 240 | 3,709 |
| Lo que corresponde a z = 3,891 | ≈ 501 | 3,891 |

El z = 3,709 de la fila del medio **es la línea de la Fase 2 otra vez** (3,726 con K = 257). O sea: al
primer barrido de parámetros por mercado, el diseño multi-mercado se convierte en la fase que acaba de
cerrar en negativo, y con menos datos por celda.

Y lo segundo, que es peor: **re-optimizar deja de ser fuera de muestra.** La regla dejaría de ser una
predicción y volvería a ser un ajuste. No hay versión "chiquita" de esta transgresión: un solo mercado
con k retocado contamina el conjunto entero, porque el conjunto se reporta como una sola prueba.

## 0b. La elegancia que este diseño tiene y la Fase 2 no tenía

**ES fue el set de descubrimiento. Los otros mercados nunca se miraron.** Entonces:

> **El conjunto multi-mercado ENTERO es el fuera de muestra. No hace falta partirlo en A y B.**

La justificación, explícita: una partición A/B existe para separar *dónde se eligió la hipótesis* de
*dónde se la prueba*. Acá esa separación ya está hecha **por construcción y por historia**: la hipótesis
se eligió en ES —está congelada en el ledger con su hash desde antes de que este documento existiera— y
cada mercado nuevo es data que jamás entró en ninguna decisión de este proyecto.

**Consecuencia que hay que leer dos veces:** el error que mató a la Fase 2 fue el **reparto** —74,5/25,5
heredado, con θ_B por encima del prior (`veredicto_fase2.md` §16)—. **Este diseño no tiene reparto que
equivocar.** Todo el n disponible trabaja para la validación, que es el lado que ataba. Estructuralmente
**no puede repetir ese error.**

Lo que sí hereda, y queda dicho acá arriba para que no se pierda: **el requisito de §17 del veredicto.**
Antes de pre-registrar, este paquete tiene que publicar (a) su efecto mínimo detectable, (b) el efecto
que espera encontrar con su fuente, y (c) —no aplica, no hay reparto—. El paso 6 es exactamente eso, y
por eso el entregable final es **la pregunta invertida**, no "cuántos mercados necesito".

---

## 1. El argumento a priori, mercado por mercado — **escrito antes de tocar un dato**

*Esta sección se sella antes de la 2. Un mercado con argumento flojo se excluye **acá**, no después de
ver un resultado.*

El mecanismo es **comprar liquidez a vendedores forzados después de k cierres a la baja**. Para que
exista en un mercado hacen falta **cuatro condiciones**, y la segunda es la que discrimina:

1. **Tenedores apalancados** sujetos a llamadas de margen o límites de riesgo.
2. **Esos tenedores están predominantemente LARGOS**, así que una caída fuerza **vender** (y no comprar).
3. Alguien puede **proveer la liquidez** y cobrar por hacerlo.
4. El flujo forzado se concentra en la ventana **cierre → apertura siguiente**, que es la que la regla opera.

### Los que pasan

**Energía — CL (WTI).** *Vendedores forzados:* el dinero administrado sostiene largos netos persistentes
(es la estructura típica del mercado: los productores son los cortos naturales, los especuladores el
lado largo). Una caída de varios días golpea margen sobre posiciones grandes en relación al capital, y
abril de 2020 mostró la liquidación forzada en su forma más pura. **Condición 2: satisfecha.**
*Advertencia declarada ahora, antes de mirar nada:* el precio negativo de abril 2020 es un **quiebre
estructural** de la serie; la ventana tiene que declararlo y tratarlo antes de correr, no después.

**Metales — GC (oro).** *Vendedores forzados:* el oro es el activo que se vende **para cubrir pérdidas en
otra parte** — un vendedor forzado con **disparador exógeno**, que es un caso más limpio que el
endógeno. **Condición 2: satisfecha**, con la particularidad de que la condición 4 puede fallar (el
flujo exógeno no tiene por qué concentrarse en la apertura siguiente). Se declara como riesgo conocido.

**Cripto — BTC (CME).** *Vendedores forzados:* es el argumento **más fuerte fuera de los índices**. El
mercado está construido sobre largos apalancados y su evento microestructural definitorio es la
**cascada de liquidaciones forzadas**. **Condiciones 1, 2 y 4: satisfechas con holgura.** *Advertencias
declaradas ahora:* historia corta (el futuro de CME arranca en diciembre de 2017, a verificar), y es el
mercado donde el fenómeno tiene **más probabilidad de estar ya arbitrado** por participantes rápidos —
lo cual es una hipótesis sobre el resultado, no una razón para excluirlo.

### Los que se excluyen **por argumento**, ahora

**Tasas — ZN. EXCLUIDO.** El jugador apalancado del mercado de bonos es el **basis trade**, que está
*largo el bono al contado y corto el futuro*. Una caída del futuro le da ganancia en la pata corta, y
deshacer la posición significa **COMPRAR futuros**. El signo del flujo forzado es **ambiguo o contrario**
al que la regla necesita. Falla la condición 2, y falla de la peor manera: no es que el efecto sea
chico, es que el argumento apunta al otro lado.

**Monedas — 6E. EXCLUIDO.** No hay una multitud apalancada y estructuralmente larga de EUR/USD. Los
participantes dominantes tienen balances que no los fuerzan en tres días, y los bancos centrales
intervienen **contra** el movimiento, no a favor. **Condición 2: no se cumple.**

### Los que se excluyen **por estructura** (el argumento puede ser bueno; la ejecución no existe)

**Granos — ZC / ZS. EXCLUIDO.** Tienen **límites diarios de precio** (maíz $0,30/bushel; soja
$0,70/bushel, según los anuncios de CME/CBOT localizados — *cifras de fuente secundaria, a verificar
contra la página oficial antes de cualquier uso*). El problema no es el costo: **la regla entra en la
APERTURA siguiente a k cierres a la baja, que es exactamente el estado en que un cierre bloqueado
*limit down* es más probable.** La orden no se llena justo cuando la señal es más fuerte, y eso es un
**sesgo de selección metido en la ejecución**, no una fricción. Se suma que la sesión no es continua.

**Ganado — LE. EXCLUIDO.** Mismo problema de límites (inicial $0,0725/lb, expandido $0,1075/lb, misma
advertencia de fuente), participación especulativa fina, y sesión sólo diurna.

### El que queda con bandera, sin decidir

**Blandos — KC (café) o CC (cacao). CANDIDATO CON BANDERA.** El argumento es bueno: concentración
especulativa alta y apalancamiento real — la espiral de márgenes del cacao en 2024 es un caso de manual.
**Pero cotizan en ICE, no en CME**: otra fuente de datos, otra estructura de costos, y límites diarios en
parte de los contratos. **No se excluye ni se admite hasta verificar sus especificaciones.**

## 2. Un mercado por sector independiente

| Sector | Elegido | Por qué ése y no otro | Estado |
|---|---|---|---|
| Índices bursátiles | **ES** | — | **No es candidato: ES es el descubrimiento.** Queda como ancla |
| Energía | **CL** | El más profundo del sector; NG tiene otro conductor (clima/almacenamiento) y HO/RB son derivados de CL | **ADMITIDO** |
| Metales | **GC** | El más profundo; SI es más fino y HG es un metal industrial con conductor distinto — pero **uno por sector** | **ADMITIDO** |
| Cripto | **BTC** | El único con futuro CME líquido y el argumento a priori más fuerte del paquete | **ADMITIDO** |
| Tasas | ~~ZN~~ | ZN/ZB/ZF/ZT son casi el mismo mercado; ZN sería el elegido | **EXCLUIDO por argumento** (§1) |
| Monedas | ~~6E~~ | 6E/6B/6J comparten el factor dólar; 6E sería el elegido | **EXCLUIDO por argumento** (§1) |
| Granos | ~~ZC~~ | ZC/ZS/ZW se mueven juntos; ZC sería el elegido por profundidad | **EXCLUIDO por estructura** (§1) |
| Ganado | ~~LE~~ | LE/GF/HE comparten conductor | **EXCLUIDO por estructura** (§1) |
| Blandos | **KC / CC** | Sin decidir entre los dos hasta verificar specs de ICE | **BANDERA** |

### El resultado de aplicar el filtro honestamente, y hay que decirlo ahora

> **De siete sectores ofrecidos quedan TRES admitidos (CL, GC, BTC) más uno con bandera (KC/CC).**
>
> La tabla de potencia del paso 5 **arranca en seis mercados**. El filtro a priori, aplicado antes de
> mirar un dato como corresponde, **deja menos mercados de los que el diseño supone**. Eso no es un
> resultado del paso 5 —que no se corrió— pero es información que Roberto necesita **ahora**, porque
> cambia la pregunta: con tres o cuatro mercados, la decisión del paso 7 se toma con un diseño bastante
> más flaco que el que motivó el encargo.

**No se compensa aflojando el filtro.** Meter ZN o 6E "para llegar a seis" sería exactamente lo que §1
existe para impedir: elegir mercados por lo que le conviene al cálculo de potencia en vez de por su
argumento.

## 3. El piso de fricción

### 3.1 Primero, una corrección de escala en la fórmula del encargo

El encargo dice: *"delta bruto por operación a h=3 es 0.10707 y el peaje f/h es 0.01604, o sea sobran
0.09103"*. **Los dos números son correctos y no se pueden restar entre sí:** están en escalas distintas.

```
delta bruto = 0,107006      POR OPERACION   (media bruta / sigma de la operacion)
f/h         = 0,016038      POR SESION      (peaje/sigma_1, dividido por la tenencia; es la escala de c)
```

La resta consistente, en la escala **por operación**, es:

```
delta_neto = delta_bruto - costo_RT/sigma_operacion = 0,107006 - 0,023301 = 0,083705
```

y **0,083705 es exactamente el δ que el propio paso 6 usa (0,083767)**. La resta mezclada da 0,09097, un
δ 8,7 % más alto, y **la diferencia se paga en operaciones exigidas: 948 contra 1.120**. El encargo es
internamente correcto en el paso 6 y mezcla escalas en el paso 3; se usa la del paso 6.

### 3.2 El instrumento, que es mejor que un umbral

"Está muerto si f se acerca a 0,107" es cierto pero pierde lo importante: **la fricción no mata de
golpe, encarece.** Lo que decide es cuántas operaciones necesita cada mercado para aportar 80 % de
potencia:

```
f_mercado    = costo_RT / sigma_operacion(h = 3)
delta_neto   = 0,107006 - f_mercado
n_necesario  = 7,8489 / delta_neto^2
```

| f_mercado | δ neto | n para 80 % | contra ES/MES |
|---|---|---|---|
| 0,0000 (peaje cero, imposible) | 0,107006 | 685 | 0,61× |
| 0,0117 (mitad del de ES/MES) | 0,095306 | 864 | 0,77× |
| **0,0233 — ES/MES, el ancla** | **0,083705** | **1.120** | **1,00×** |
| 0,0350 | 0,072006 | 1.514 | 1,35× |
| 0,0466 (el doble del ancla) | 0,060406 | 2.151 | 1,92× |
| 0,0535 | 0,053506 | 2.742 | 2,45× |
| 0,0700 | 0,037006 | 5.731 | 5,12× |
| 0,0900 | 0,017006 | 27.139 | 24,23× |
| ≥ 0,1070 | ≤ 0 | **MUERTO** | — |

**El ancla, medida y no supuesta** (cartucho 1, parte A, del ledger): 244 operaciones, σ por operación a
h = 3 de **$167,37**, peaje **$3,90**, `f = 0,023301`, δ neto **0,083705**, **1.120 operaciones** para
80 %.

Y un hallazgo del ancla que va a importar al elegir contrato: **f depende del tamaño de contrato, y el
grande es más barato por unidad de riesgo.** El peaje es fijo por contrato mientras que σ escala con el
tamaño, así que un micro paga proporcionalmente más. La elección micro/full por mercado es parte del
paso 3, no un detalle de implementación.

### 3.3 Lo que esta tanda **no** pudo poblar, y por qué

**La tabla queda sin poblar, y no por falta de ganas: el paso 3 necesita un dato que no es público en el
sentido en que el encargo lo supone.**

`f_mercado` necesita **dos** entradas por mercado:

| entrada | ¿pública? | estado |
|---|---|---|
| **costo_RT** = comisión + spread × valor de tick | Sí, pero **específica del bróker** | **No verificada.** Las specs de CME no se dejaron leer desde acá (`ECONNRESET` y tres timeouts contra `cmegroup.com`), y lo que devolvió la búsqueda es **de segunda mano** |
| **σ_operación(h = 3)** | **No.** Es una propiedad medida de la serie de precios | **Requiere barras.** No hay forma de obtenerla sin datos |

Sobre la calidad de lo secundario, un ejemplo que justifica la desconfianza: la búsqueda **contradijo**
el valor de tick de 6E que traía la consulta ($6,25 y no $12,50). Un número que se contradice a sí mismo
entre fuentes no entra a una tabla que después decide gastar cartuchos. **Las specs se verifican contra
CME/ICE directamente o no se usan** (`qc/` es el lugar, §4.5 el procedimiento).

**Y el punto que hay que decidir, porque cambia el plan:** el encargo dice *"recién el paso 4 necesita
barras"*. **El paso 3 también las necesita**, porque σ es una medición. Hay dos salidas legítimas:

- **(a) Bajar barras diarias gratis de la misma fuente ya usada para ES=F** (`CL=F`, `GC=F`, `BTC=F`) y
  medir σ **a ciegas**: la función devuelve **únicamente** σ, jamás una media, una suma ni un P&L. Es
  exactamente la disciplina que el paso 4 exige para ρ, y por el mismo motivo. **σ es una propiedad del
  MERCADO, no de si la regla gana** — la misma distinción que §3.5 de la Fase 2 hizo entre contar
  **frecuencia** y contar **rentabilidad**. Costo: cero.
- **(b) Usar el margen publicado por el exchange como proxy público de σ**, declarándolo como proxy con
  su error, no como medición. Más débil, y tampoco se pudo leer desde acá.

**Recomendación: (a)**, con la función ciega escrita y con aserciones antes de bajar nada.

---

## 4. Qué NO hace esta tanda

No pre-registra. No gasta cartuchos (**K = 257 intacto, 4 corridos**). No compra datos. No baja barras.
No calcula ρ ni potencia agrupada (pasos 4 y 5). No fija el umbral de decisión (paso 7). **Y no toca
ningún archivo de la Fase 2**, que quedó cerrada con su veredicto.

**Lo que queda listo para la próxima:** los tres mercados admitidos con su argumento sellado, los cuatro
excluidos con el motivo escrito **antes** de ver un resultado, la prohibición de re-optimizar con su
aritmética, la declaración de que el conjunto entero es fuera de muestra, y el instrumento de fricción
con su ancla medida — esperando dos entradas por mercado y una decisión sobre cómo obtener σ.

---

## 5. La predicción sobre ρ — **escrita antes de medir nada**

*Sección fijada y escrita a disco antes de calcular un solo solapamiento. Se escribe primero para que
la medición sea la prueba de una predicción, y no el descubrimiento de una excusa.*

### El argumento que faltaba, y juega en contra

> **El mecanismo que estamos probando ES la razón por la que los mercados van a correlacionar.**

La venta forzada **no es local**. Una llamada de margen no liquida la posición que perdió: liquida **lo
que se pueda vender**, y lo hace **todo a la vez**. Entonces CL, GC y BTC tienen tres cierres a la baja
simultáneos precisamente en los **eventos de liquidez sistémica** — marzo de 2020 es el caso de manual,
y es exactamente el episodio donde el mecanismo debería producir su ventaja más grande.

**Las operaciones se agrupan en el tiempo, y ρ será alta POR LA MISMA RAZÓN POR LA QUE EL EFECTO
EXISTIRÍA.** No es un parámetro molesto que ojalá salga bajo: es una **consecuencia de la hipótesis**.

> **Un diseño que necesita ρ baja está apostando contra su propio mecanismo.** Si ρ sale baja, la buena
> noticia estadística es una mala noticia sobre la hipótesis: querría decir que las ventas forzadas de
> cada mercado son locales, y entonces el argumento a priori que admitió a CL, GC y BTC —el de la
> liquidación que cruza mercados— era más débil de lo que dijimos.

### La predicción, con su magnitud, para poder fallar

1. **ρ̄ entre las series de retorno de la estrategia será POSITIVA, en el rango 0,15 – 0,35.**
2. **Las fechas se agruparán:** el solapamiento observado de sesiones ocupadas superará al esperado bajo
   independencia por un factor (`lift`) **≥ 2 en al menos dos de los tres pares**.
3. **La concentración estará en los episodios de liquidez sistémica**, con marzo de 2020 como el mayor.

**Qué se puede medir a ciegas y qué no.** El punto 2 es **frecuencia** —fechas contra fechas— y se puede
medir sin tocar un P&L, igual que `count_trades_only` en la Fase 2. El punto 1 **no**: ρ entre retornos
exige los retornos, y esos llevan la respuesta adentro. Se mide en el paso 4 con la disciplina que el
propio encargo fijó (desmediar y devolver únicamente la matriz), **nunca antes de pre-registrar**. Acá
se mide el 2, y se reporta como lo que es: **evidencia sobre el mecanismo del agrupamiento, no una
estimación de ρ.**

## 6. NG y HG, cada uno con su argumento — **sin mirar el conteo**

*La tentación está marcada en el encargo y se toma en serio: la idea de subdividir sectores apareció
DESPUÉS de ver que faltaban mercados. Por eso cada uno se juzga con el mismo estándar con el que se
excluyó a ZN y a 6E, y el conteo no se mira hasta el final.*

### NG (gas natural) — **RECHAZADO por argumento**

*¿Es un sector distinto de CL?* **Sí, y eso no se discute:** su conductor es clima y almacenamiento, no
el macro global. La subdivisión energía → {crudo, gas} es defendible **por sí sola**.

*¿Quiénes son los vendedores forzados?* Ahí se cae. La condición 2 exige tenedores apalancados
**predominantemente largos**, y en NG el posicionamiento especulativo **no tiene un lado estable**: la
literatura de posicionamiento muestra al dinero administrado alternando entre neto largo y neto corto
según la estación, y los eventos de flujo forzado más famosos del gas —Amaranth 2006, los aprietes de
invierno— son **squeezes contra los CORTOS**, que fuerzan **comprar**, no vender.

> **NG no falla por tener un efecto chico: falla porque el signo del flujo forzado no es estable.** Es
> el mismo motivo por el que se excluyó a ZN, y se aplica el mismo criterio.

### HG (cobre) — **RECHAZADO, y el motivo es más incómodo**

*¿Es un sector distinto de GC?* Se puede argumentar: conductor industrial contra conductor
monetario. **Pero el sector no se declaró por "conductor": se declaró por INDEPENDENCIA del flujo
forzado**, que es lo que la potencia agrupada necesita.

*¿Quiénes son los vendedores forzados?* Existe una historia real: el cobre se usa como **colateral de
financiamiento**, y cuando el crédito se aprieta ese colateral se liquida — Qingdao 2014 es el caso. Es
un vendedor forzado con disparador exógeno, de la misma familia que el del oro.

*Y sin embargo:* ese disparador es **el mismo** que el del oro — un apretón de liquidez— y golpea a los
dos metales **a la vez**. Por §5, que se escribió antes que esto, **el par (GC, HG) es el que más ρ
debería tener de todos los pares posibles**, y un par con ρ alta aporta casi nada al n efectivo.

> **HG se rechaza por la regla de un mercado por sector INDEPENDIENTE, aplicando el criterio de §5 que
> se escribió antes de contar nada.** El argumento del vendedor forzado en cobre es aceptable; su
> independencia respecto del oro no lo es.

### La sospecha de mí mismo, como corresponde

El encargo pide desconfiar si el total daba justo seis. **No dio seis: dio tres.** NG y HG se rechazaron
los dos, así que **la subdivisión no rescató el conteo** — y ése es el único dato que respalda que el
análisis no se torció hacia el número que hacía falta. Si hubiera dado seis clavados, la sospecha
correspondía; da tres, y el problema del paso 5 sigue exactamente igual de grande que antes de escribir
esta sección.

---

## 7. σ a ciegas, y la tabla de fricción

**Cómo se midió, que es la mitad del punto.** `factory/sigma_ciego.py` corre la regla sobre las barras
de cada mercado y devuelve **únicamente** dispersión, frecuencia y bordes de la serie. Nunca una media,
nunca una suma, nunca un P&L. La salida se valida contra una lista blanca de claves y **falla cerrado**
si aparece cualquier otra, o si un valor no es escalar.

**La prueba de que es ciega no es la promesa: son los controles** (`tests/multimercado/test_ciego.py`,
**21 aserciones, 0 fallas**):

| control | qué hace | qué exige |
|---|---|---|
| **signo dado vuelta** | multiplica por −1 el P&L de **todas** las operaciones | la salida **no cambia ni un campo** |
| **constante sumada** | le suma +5, −5 y +100 a cada operación | la salida **no cambia ni un campo** |
| **control del control** | mide la media bajo esas mismas mutaciones | la media **sí** cambia (−0,623 → +0,623), σ no |

> **Una función cuya salida no distingue una regla ganadora de una perdedora no puede filtrar el
> resultado.** Es la misma separación que la Fase 2 hizo entre contar **frecuencia** y contar
> **rentabilidad** (§3.5), aplicada a σ, que es una propiedad del **mercado** y no de si la regla acierta.

**Datos:** barras diarias de Yahoo, la misma fuente y el mismo `yfinance` que bajaron `ES=F`
(`download_data.py`). Costo: **cero**. Van a `data/`, que está gitignored — no se redistribuyen.

| mercado | serie | sesiones | n operaciones | ocupación | σ por operación |
|---|---|---|---|---|---|
| **CL** WTI | 2000-08-23 → 2026-08-25 | 6.529 | **385** | 17,7 % | 2,7348 pts = **273,5 ticks** |
| **GC** oro | 2000-08-30 → 2026-08-25 | 6.520 | **347** | 16,0 % | 28,176 pts = **281,8 ticks** |
| **BTC** CME | 2017-12-18 → 2026-08-25 | 2.185 | **130** | 17,8 % | 2.879,4 pts = **575,9 ticks** |

*Tamaños de tick usados: CL 0,01 · GC 0,10 · BTC 5,00. **No verificados contra CME** (la página no carga
desde acá): entran a `qc/` antes de pre-registrar, como manda §4.5.*

### La fricción no mata a ninguno — y la razón es incómoda

Todo en **ticks**, que es la unidad robusta: `f = costo_vuelta_completa / σ_operación`.

| mercado | σ (ticks) | peaje que lo empata con ES/MES | **peaje LETAL** | f si paga 3 ticks | n exigido |
|---|---|---|---|---|---|
| ancla **ES/MES** | 133,9 | — (paga 3,12) | 14,3 | **0,023301** | **1.120** |
| **CL** | 273,5 | 6,4 | **29,3** | 0,010970 | 851 |
| **GC** | 281,8 | 6,6 | **30,2** | 0,010647 | 845 |
| **BTC** | 575,9 | 13,4 | **61,6** | 0,005209 | 757 |

Los tres pagan **menos fricción que ES/MES** por unidad de riesgo, y el peaje real (2–4 ticks) está a un
factor **~10** del letal. **Estable por era**, además — se partió cada serie al medio y ninguna mitad se
acerca al ancla:

| | primera mitad | segunda mitad |
|---|---|---|
| CL | f = 0,011436 | f = 0,010543 |
| GC | f = 0,014904 | f = 0,008766 |
| BTC | f = 0,008270 | f = 0,004149 |

*(El rango dentro de un mismo mercado es grande —GC casi duplica— porque el peaje en ticks es fijo y σ
creció con el nivel de precio. No cambia la conclusión, pero se declara: es la misma lección que §64 de
la Fase 2.)*

> **La tabla de fricción no mató a nadie, y eso NO es una buena noticia: es la señal de que los dos
> filtros no eran independientes.** El paso 3 iba a matar mercados baratos, y los mercados baratos
> —granos, ganado— ya los había matado el paso 1 por estructura. Lo que quedó después del argumento a
> priori es, por construcción, un conjunto de mercados de σ alta. **El filtro de fricción llegó tarde a
> su propia función.**

## 8. La predicción sobre ρ, contrastada: **FALLÓ**

*Medido después de escribir §5 a disco, con la función ciega: fechas contra fechas, ni un P&L.*

**Predicho: `lift ≥ 2` en al menos dos de los tres pares.**

| par | días comunes | ocupa A | ocupa B | observado | esperado si independientes | **lift** | ¿cumple? |
|---|---|---|---|---|---|---|---|
| CL–GC | 6.519 | 0,177 | 0,160 | 0,0387 | 0,0283 | **1,37** | no |
| CL–BTC | 2.184 | 0,165 | 0,179 | 0,0375 | 0,0294 | **1,28** | no |
| GC–BTC | 2.183 | 0,143 | 0,179 | 0,0298 | 0,0255 | **1,17** | no |

**0 de 3. Lift medio 1,27. La predicción falló**, y la consecuencia estaba escrita antes de medir, así
que se aplica sin renegociarla:

> *"Si ρ sale baja, la buena noticia estadística es una mala noticia sobre la hipótesis: querría decir
> que las ventas forzadas de cada mercado son locales, y entonces el argumento a priori que admitió a
> CL, GC y BTC —el de la liquidación que cruza mercados— era más débil de lo que dijimos."* (§5)

Las dos caras, sin quedarse con la cómoda:

- **Estadística:** ρ probablemente esté cerca del extremo bajo, y el efecto de diseño muerde menos.
- **Mecanismo:** los días de operación **sí** se agrupan —27 % por encima del azar es real y consistente
  en los tres pares— **pero no como predice "una llamada de margen liquida todo a la vez"**. Ese relato
  pedía un factor 2 o más. La versión que sobrevive es más floja: **hay algo de sincronía, y es
  moderada.**

**Límite de esta medición, dicho con todas las letras:** co-ocupación de fechas **no es** ρ entre
retornos. Un lift de 1,27 no fija ρ. Lo único que este número hace es **falsificar la versión fuerte del
agrupamiento**, y sugerir —sin probar— que ρ está más cerca de 0,10 que de 0,35. **ρ se mide en el paso
4, con la matriz ciega, y nunca antes de pre-registrar.**

## 9. La potencia — con una corrección de fórmula primero

**La fórmula escrita en el encargo no produce los números del encargo.** `n_ef = N/(1+(N−1)·ρ̄)` trata a
**todas** las operaciones como un solo conglomerado:

| con N = 732, m = 3, ρ = 0,10, δ = 0,083767 | n efectivo | potencia |
|---|---|---|
| `N/(1+(N−1)ρ)` — **como está escrita** | 9,9 | **5,8 %** |
| `N/(1+(m−1)ρ)` — **la que da sus números** | 610,0 | **54,3 %** |

El conglomerado no son "todas las operaciones juntas": son los **m mercados observados a la vez**. El
tamaño de conglomerado es **m**, no N. Con `(N−1)` el diseño colapsa a `1/ρ` operaciones efectivas y
cualquier ρ > 0 lo mata, lo cual es absurdo. **Se usa `(m−1)`, que reproduce 54,3 % y 48,2 % exactos.**

### La tabla del encargo, reproducida

| mercados | ρ=0,00 | ρ=0,05 | ρ=0,10 | ρ=0,20 |
|---|---|---|---|---|
| **3 — los admitidos** | **62,0 %** | **58,0 %** | **54,3 %** | **48,2 %** |
| 4 | 74,4 % | 68,5 % | 63,1 % | 54,3 % |
| 6 | 89,3 % | 81,8 % | 74,4 % | 62,0 % |
| 12 | 99,5 % | 95,4 % | 87,9 % | 71,7 % |

**Ni con correlación cero llegan tres mercados.** Y con ρ = 0,20, **doce** mercados (71,7 %) dan menos
que **seis** sin correlación (89,3 %).

### Con el n REAL, que es mejor de lo supuesto y no alcanza igual

`CL 385 + GC 347 + BTC 130 = **862** operaciones`, contra las 732 que suponía la tabla (ES tenía 244; CL
y GC tienen historia más larga y disparan más seguido).

| ρ | n efectivo | z esperado | **potencia** |
|---|---|---|---|
| 0,00 | 862,0 | 2,459 | **69,1 %** |
| 0,05 | 783,6 | 2,345 | 65,0 % |
| 0,10 | 718,3 | 2,245 | **61,2 %** |
| 0,20 | 615,7 | 2,079 | 54,7 % |
| 0,30 | 538,8 | 1,944 | 49,4 % |

### El entregable de verdad: **la pregunta invertida**

No es "cuántos mercados necesito". Es: **dado lo que sobrevivió, ¿qué tamaño de efecto detecta este
diseño al 80 %?**

| ρ | n efectivo | **δ mínimo detectable** | contra el δ medido (0,083767) |
|---|---|---|---|
| 0,00 | 862,0 | **0,095422** | **1,14×** |
| 0,10 | 718,3 | **0,104530** | **1,25×** |
| 0,20 | 615,7 | 0,112905 | 1,35× |
| 0,30 | 538,8 | 0,120701 | 1,44× |

Y cuántos mercados **como éstos** (≈ 287 operaciones cada uno) harían falta para llegar al 80 % contra
δ = 0,083767:

| ρ | mercados necesarios |
|---|---|
| 0,00 | **4** (1.149 operaciones) |
| 0,10 | **6** (1.724) |
| 0,20 | 15 (4.310) |
| 0,30 | **inalcanzable** |

## 10. La regla de decisión, declarada ahora

### El requisito del veredicto, aplicado a este paquete

`veredicto_fase2.md` §17 exige, antes de pre-registrar: **(a)** efecto mínimo detectable, **(b)** efecto
esperado con su fuente, **(c)** reparto — que acá **no aplica** (§0b).

```
(a) delta minimo detectable  = 0,0954 (rho=0)  ...  0,1207 (rho=0,30)
(b) delta esperado           = 0,083767
    fuente: cartucho 1 de la Fase 2 (ledger d38a1e04c6bfc0f8), que es el MAXIMO
    SESGADO de cuatro mediciones y cuyo IC al 90% contiene el cero
```

> **(b) < (a) en TODO el rango de ρ. Por la regla que este proyecto escribió tres commits atrás, el
> paquete NO habilita abrir la fase tal como está: sólo podría abrirse declarando que su único resultado
> posible es "no detectado".**

Y hay que decirlo así: la regla se cumple **contra nosotros mismos**, en el primer diseño al que se le
aplicó después de escribirla. Para eso se escribió.

### La regla, para que no se re-discuta después

> **Si el diseño no llega a 80 % de potencia contra un δ que Roberto considere perseguible, la fase NO
> se abre y este paquete se publica como NEGATIVO — que es un resultado, no un fracaso, exactamente como
> la Fase 2.**

**Qué podría cambiarlo, y son dos cosas concretas, no una lista de deseos:**

1. **Un cuarto mercado.** A ρ = 0 hacen falta **cuatro**, y hay exactamente un candidato con bandera sin
   resolver: **KC/CC**. La bandera dejó de ser un detalle administrativo — **es la diferencia entre 69 %
   y 80 %**. Se resuelve verificando specs de ICE, no aflojando el argumento.
2. **ρ medido cerca de cero.** El lift de 1,27 lo sugiere y no lo prueba. Se mide en el paso 4.

Y lo que **no** puede cambiarlo: agregar ZN, 6E, NG o HG. Los cuatro se rechazaron por argumento
**antes** de conocer este número, y volver sobre ellos ahora sería elegir mercados por lo que le conviene
al cálculo de potencia — exactamente lo que §1 y §6 existen para impedir.

### Las dos ramas del resultado eventual, selladas

- **(a) Si el conjunto multi-mercado confirma** —p ≤ 0,05 bilateral, prueba única, K = 1— se afirma:
  *"una regla congelada, elegida en ES y jamás ajustada, superó una prueba única sobre mercados nunca
  vistos"*. **Con qué fuerza:** una sola prueba, sin partición, con la multiplicidad ya pagada; **no** es
  una estimación insesgada de su rendimiento futuro.
- **(b) Si NO confirma** se afirma: *"no pudimos confirmarla"*. **Jamás** *"el mecanismo no existe"*.
  Con 69 % de potencia en el mejor caso, un no-resultado deja **31 %** de probabilidad de haberse perdido
  un efecto real del tamaño supuesto — y el δ supuesto ya es el máximo sesgado de cuatro.

---

*Estado al cierre de esta tanda: **0 cartuchos gastados, K = 257 intacto, nada pre-registrado, ningún
dato comprado**. Fase 2 sin tocar: 469 aserciones, ledger 106 líneas, caja fuerte sellada. La medición
ciega suma 21 aserciones propias con sus dos controles.*

---

## 11. La puerta KC, medida — y **cerrada**

§10 la dejó abierta porque a ρ = 0 hacían falta cuatro mercados y KC/CC era el único candidato. Se mide
la puerta **sin bajar un solo dato de KC**, suponiéndole el aporte de un mercado típico (244
operaciones, el n de ES; los tres admitidos promedian 287):

| ρ | n efectivo | z esperado | **potencia con KC** |
|---|---|---|---|
| **0,00** | 1.106,0 | 2,7858 | **79,6 %** ← al filo, y **por debajo** |
| 0,02 | 1.043,4 | 2,7058 | 77,2 % |
| 0,05 | 961,7 | 2,5978 | 73,8 % |
| 0,10 | 850,8 | 2,4433 | 68,6 % |
| 0,20 | 691,2 | 2,2024 | 59,6 % |

**Para 80,0 % exactos** hace falta `n_efectivo = (2,801585/0,083767)² = 1.118,6`, o sea que **KC tenga
que aportar ≥ 257 operaciones** — y eso **con ρ exactamente cero**. Con ρ = 0,02, apenas por encima de
cero, el requisito salta a **KC ≥ 324**.

### Las tres condiciones simultáneas, y por qué eso es una puerta cerrada

1. **KC aporta ≥ 257 operaciones.** Plausible, pero no medido y no se va a medir acá.
2. **ρ = exactamente cero.** El lift medido de 1,27 (§8) dice que hay sincronía, poca pero **real y
   consistente en los tres pares**. ρ exactamente cero es el único valor que el dato ya recogido vuelve
   **improbable**.
3. **Creer δ = 0,083767**, que es el **máximo sesgado de cuatro mediciones** y cuyo **IC 90 % contiene el
   cero**. Y acá está lo que decide: **§3.2 obliga a reportar la potencia en el extremo inferior del
   intervalo**, y ese extremo es **negativo**. Con δ ≤ 0 **ningún número de mercados alcanza jamás**.

> **La rama KC queda declarada CERRADA.** No porque sea imposible, sino porque exige que **las tres**
> ocurran a la vez, y la tercera es la que este proyecto pasó una fase entera aprendiendo a no suponer.
> Sólo se reabre por **decisión explícita de Roberto**, escrita, sabiendo que compra 79,6 % en el mejor
> caso imaginable.

*(Nota menor de aritmética, resuelta: la lectura rota `(N−1)` da **5,8 %** y no 4,5 %. La diferencia es
la **cola de abajo** del contraste bilateral, `Φ(−z−1,96) = 1,3 %`, que con z chico deja de ser
despreciable. La prueba es a dos colas, así que la potencia correcta suma las dos. Misma conclusión.)*

## 12. Lo que este paquete demostró sobre el método

**La predicción sobre ρ se escribió a disco antes de medir, falló, y la consecuencia pre-declarada se
aplicó sin renegociarla.**

No es una anécdota de proceso: es **§7.2 aplicado a nosotros mismos**. La regla que la Fase 2 impuso a
cada configuración —el pre-registro entra al ledger **antes** de conocer el resultado, y los errores de
diseño consumen presupuesto igual— se aplicó acá a una **hipótesis nuestra sobre nuestro propio
diseño**. Predijimos `lift ≥ 2`, medimos 1,27, y en vez de reinterpretar el umbral aplicamos lo que
habíamos escrito: que ρ baja es **buena noticia estadística y mala noticia sobre el mecanismo**.

> **Es la demostración más limpia del método en todo el proyecto**, porque no hubo nada que ganar
> haciéndolo bien: nadie se habría enterado si el umbral se movía después de ver el 1,27.

---

## El cierre

> **El paquete del día cero se publica como NEGATIVO. La fase multi-mercado NO se abre: δ mínimo
> detectable (0,095–0,121) > δ esperado (0,0838, máximo sesgado, IC 90 % contiene cero) en todo el rango
> de ρ, regla pre-declarada aplicada. Ramas cerradas: KC (al filo aun en el mejor caso), ZN/6E/NG/HG
> (por argumento, sellado antes de contar).**

**2026-08-25.** K = 257 intacto, 4 corridos, **el cartucho 5 sin gastar — y que quede sin gastar es
parte del resultado**. Nada pre-registrado, ningún dato comprado, la caja fuerte de la Fase 2 sellada.

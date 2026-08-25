# Búsqueda multi-mercado — paquete del día cero

**Esto NO abre una fase.** Es el paquete que decide **si** se abre. No gasta un solo cartucho, no
pre-registra nada, no compra datos. La Fase 2 está cerrada y este documento no la toca: §8.3 exige spec
nueva y documento nuevo, y **cualquier búsqueda futura hereda K = 257** (§1.6).

**Entregable de esta tanda: pasos 1, 2 y 3.** Los pasos 4 a 7 no se ejecutan todavía.

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

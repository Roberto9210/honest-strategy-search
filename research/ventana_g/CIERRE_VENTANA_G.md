# VENTANA G — ARITMETICA DE LA EVALUACION

**Pregunta unica.** Intentar evaluaciones de cuentas de fondeo de futuros, con CERO VENTAJA y bien
dimensionado, tiene esperanza matematica positiva o negativa?

**Respuesta. NEGATIVA.** En las 8 firmas, en los 3 tamanos de posicion probados, en la cuenta de 50K y
en la mas chica. La esperanza de un intento va de **-$19** (Tradeify Growth 25K, 5 micros) a **-$293**
(Take Profit Trader 50K, 5 micros). No hay ninguna celda positiva en 48 combinaciones.

Esto **no es** una busqueda de ventaja de mercado y no paga multiplicidad: no se eligio entre candidatas
ni se probaron variantes hasta que una diera. Se midio una estructura fija — la aritmetica de las reglas
publicadas — y el signo salio igual en todas.

---

## 1. Que hace que la respuesta no sea obvia

Con cero costo y cero ventaja, la probabilidad de tocar el objetivo `U` antes del drawdown `D` es
`D/(U+D)`. Con `U = $3.000` y `D = $2.000` eso da **40%**, que es alto. A $80 la evaluacion y $450 el
primer retiro, un 40% seria esperanza fuertemente **positiva**. La pregunta existe por eso.

Lo que la da vuelta son tres cosas, en este orden de peso:

1. **El costo por operacion.** Cada operacion resta comision mas deslizamiento. Eso convierte la moneda
   simetrica en una con probabilidad efectiva `0,5 - c/2b`. Con el supuesto de abajo, 0,4750. Parece poco.
   Sobre la distancia que hay que recorrer, hunde el 40% teorico a **~23%**.
2. **La segunda barrera.** Pasar la evaluacion no paga. Hay que pasar la evaluacion *y despues* recorrer
   otra vez una distancia parecida en la cuenta fondeada, contra otro drawdown, para llegar al primer
   retiro. Las dos probabilidades se multiplican: 0,23 x 0,22 = **0,05**.
3. **El drawdown trailing.** El piso sube con las ganancias y no baja. La caminata que subio y volvio no
   vuelve al punto de partida: vuelve a un punto peor.

El resultado es que la probabilidad de cobrar un peso, con cero ventaja, esta entre **1,3% y 9,8%**,
mientras que el equilibrio exige entre **5,6% y 75%**.

---

## 2. El modelo

Operador sin ninguna ventaja. Cada operacion es una moneda:

    PnL = ±b - c        con prob. 1/2 cada lado
    E[PnL] = -c         Var[PnL] = b²

Caminata con dos barreras absorbentes, simulada por Monte Carlo (200.000 caminos, 5 operaciones por dia).
Se simulan explicitamente: el tipo de drawdown (trailing intradia sobre el pico, trailing al cierre sobre
el maximo de cierres diarios, o piso fijo), el bloqueo del piso al llegar al saldo inicial, el limite de
perdida diario (bloquea el dia, no reprueba), los dias minimos de operacion, los dias calificados con
ganancia minima que exigen los reglamentos de retiro, y el limite de dias de acceso donde existe.

**Supuesto de mercado (declarado, NO scrapeado de las firmas):** micro E-mini S&P (MES), valor del punto
$5. Por micro y por operacion ida y vuelta: comision ~$1,25 mas deslizamiento de 1 tick $1,25, o sea
`c1 = $2,50`. Amplitud stop/objetivo de 10 puntos, o sea `b1 = $50`. Los tres tamanos de posicion son
5, 10 y 20 micros — todos legales en las 8 firmas en el 50K.

**Sensibilidad al supuesto de costo** (eval generica U=3000 D=2000 EOD, 10 micros):

| costo por micro | P(pasa la eval) |
|---|---|
| $1,00 | 26,7% |
| $1,50 | 25,5% |
| $2,50 (el usado) | 22,5% |
| $4,00 | 18,0% |
| $6,00 | 12,8% |

El signo de la respuesta no depende de este supuesto: aun con costo de $1,00 por micro — irrealmente bajo —
la probabilidad total de cobrar queda muy por debajo del equilibrio en las 8 firmas.

### El control, y por que la primera corrida se tiro a la basura

Control exigido: con objetivo igual al drawdown, cero costo y cero ventaja, la probabilidad de pasar
tiene que dar ~50%.

**La primera implementacion dio 0,376 a 0,499 y se descarto sin publicar nada.** El error era real y vale
anotarlo: la ruptura del piso se evaluaba en cada operacion, pero el objetivo solo al cierre del dia. El
camino que subia al objetivo a media rueda y despues bajaba al piso el mismo dia se contaba como fracaso.
Asimetria de granularidad. Corregido — objetivo y piso se evaluan con la misma granularidad — el control
da:

    U=D=$1000  b=$100  0,4986   b=$250  0,4973   b=$500  0,4996
    U=D=$2000  b=$100  0,5053   b=$250  0,5017   b=$500  0,5038
    U=D=$3000  b=$100  0,4988   b=$250  0,4974   b=$500  0,5011

Las nueve celdas en [0,497 ; 0,506], con 0% de caminos sin resolver. CONTROL PASADO.

(Nota: en las firmas reales el objetivo **si** se confirma al cierre — Apex lo dice explicito. O sea que
la asimetria es real fuera del control, y corregirla hace que mis probabilidades de pasar sean, otra vez,
**optimistas**.)

---

## 3. Resultado, cuenta de 50K

Tamano de posicion 10 micros = 1 mini equivalente, `b=$500`, `c=$25`, p efectiva 0,4750.
Precio = el mas barato efectivamente publicado en la pagina, cupon incluido cuando la propia pagina lo
muestra. Ordenado por esperanza.

| firma | P(pasa eval) | P(cobra dado fondeado) | P(total) | cobra $ | cuesta $ | **E $** | p de equilibrio |
|---|---|---|---|---|---|---|---|
| Tradeify Growth | 0,226 | 0,175 | 0,040 | 1.350 | 83,00 | **-29,53** | 0,061 |
| FundedNext Flex | 0,229 | 0,170 | 0,039 | 475 | 69,99 | **-51,47** | 0,147 |
| Apex Intraday | 0,199 | 0,161 | 0,032 | 500 | 83,90 | **-67,82** | 0,168 |
| MyFundedFutures Rapid | 0,227 | 0,237 | 0,054 | 450 | 104,50 | **-80,32** | 0,232 |
| Lucid Pro | 0,227 | 0,269 | 0,061 | 450 | 115,40 | **-87,93** | 0,256 |
| BluSky Launch | 0,228 | 0,226 | 0,051 | 225 | 158,00 | **-146,41** | 0,702 |
| Topstep | 0,227 | 0,218 | 0,049 | 675 | 198,00 | **-164,68** | 0,293 |
| Take Profit Trader | 0,226 | 0,247 | 0,056 | 400 | 300,00 | **-277,74** | 0,750 |

Con 5 micros todas empeoran (menos distancia por operacion, mas operaciones, mas costo acumulado):
de -$59,65 (FundedNext) a -$292,66 (Take Profit Trader).
Con 20 micros la evaluacion mejora pero la etapa fondeada empeora en las firmas que exigen 5 dias
calificados, porque con pasos grandes es mas facil romper el piso antes de juntar los 5 dias:
de -$38,07 (Tradeify) a -$272,55 (Take Profit Trader).

**Mejor: Tradeify Growth. Peor: Take Profit Trader.**
Tradeify es la mejor por dos razones aritmeticas, no por ser generosa: la evaluacion es barata ($83 con
cupon) y el primer retiro tiene tope alto ($1.500 al 90%). Take Profit Trader es la peor porque cobra
$170/mes mas $130 de activacion — $300 — para un primer retiro que en el modelo vale $400 al 80%.

### Cuenta mas chica (solo las 4 firmas que publican una menor a 50K con reglas completas)

10 micros:

| firma | P(total) | cobra $ | cuesta $ | **E $** | p de equilibrio |
|---|---|---|---|---|---|
| Tradeify Growth 25K | 0,034 | 900 | 55,00 | **-24,71** | 0,061 |
| Lucid Pro 25K | 0,100 | 450 | 70,60 | **-25,78** | 0,157 |
| MyFundedFutures Rapid 25K | 0,060 | 450 | 72,50 | **-45,49** | 0,161 |
| Apex Intraday 25K | 0,020 | 500 | 75,70 | **-65,56** | 0,151 |

La celda menos mala de todo el trabajo es Tradeify Growth 25K con 5 micros: **-$19,15**. Sigue siendo
negativa.

---

## 4. La distancia al equilibrio

La forma mas limpia de decirlo. La probabilidad de pasar que hace falta para que un intento valga cero,
contra la que un operador sin ventaja consigue (50K, 10 micros):

| firma | hace falta | se consigue | falta un factor de |
|---|---|---|---|
| Tradeify | 6,1% | 4,0% | 1,5x |
| FundedNext Flex | 14,7% | 3,9% | 3,8x |
| Apex | 16,8% | 3,2% | 5,2x |
| MyFundedFutures | 23,2% | 5,4% | 4,3x |
| Lucid | 25,6% | 6,1% | 4,2x |
| Topstep | 29,3% | 4,9% | 6,0x |
| BluSky | 70,2% | 5,1% | 13,8x |
| Take Profit Trader | 75,0% | 5,6% | 13,4x |

En la firma mas favorable de todas hace falta ser **1,5 veces** mejor que el azar-menos-costos solo para
llegar a cero. Eso ya es una ventaja de mercado real, y no es lo que se estaba preguntando.

---

## 5. LIMITACIONES OBLIGATORIAS

1. **Operaciones independientes.** El modelo supone que cada operacion es independiente de la anterior.
   En la realidad las perdidas se agrupan — es lo mismo que midio la Ventana D en ES 2016-2019: el
   agrupamiento de volatilidad es de cola, con p95 en 1,51x contra una mediana de 1,00x. Agrupamiento
   significa mas probabilidad de una racha larga que la binomial, y una racha larga es exactamente lo
   que toca el drawdown. **Toda probabilidad de pasar de este documento es OPTIMISTA en una magnitud
   que no se midio.**
2. **El drawdown trailing intradia es peor que lo que captura un modelo de pasos discretos.** El piso
   real sigue el pico de equity *incluyendo el no realizado*, tick a tick dentro de la operacion. Aca
   solo sigue el saldo al cierre de cada operacion. Apex y Take Profit Trader lo dicen textualmente
   ("includes realized gains and unrealized gains"). Sus numeros son los mas optimistas de la tabla.
3. **No se modela la regla de consistencia**, y siete de las ocho la tienen (Apex 50% en la PA, Topstep
   50%, Lucid 40%, FundedNext 40%, Tradeify 35-40%, MyFundedFutures 50% en la eval, BluSky 50%/34%).
   La consistencia solo puede bajar la probabilidad de cobrar: castiga el dia grande, que es justo como
   una caminata sin ventaja llega al objetivo cuando llega.
4. **No se modela el reset.** La esperanza de arriba es la de UN intento, una compra. Los resets no
   cambian el signo: cada reset es otro intento con la misma esperanza negativa.
5. **El costo por operacion es un supuesto declarado**, no un dato de las firmas (seccion 2).
6. Los precios con cupon son los que la propia pagina mostraba el 2026-09-03. Los cupones caducan; con
   precio de lista todas las esperanzas empeoran.

---

## 6. AUTOMATIZACION

**Nota de metodo.** La primera version de esta seccion tenia una sola columna, "automatizacion de
terceros", y calificaba a Tradeify como "SI, CON APROBACION". Eso estaba MAL: la cita real de Tradeify
exige "sole owner of the bot", "no one else has access to or is using it" y "solely for your own use" —
condiciones que una herramienta de un tercero no puede cumplir por construccion. La columna original
contestaba una pregunta ("se permite automatizar, con requisitos?") que no es la que importa aca
("es de terceros o es propia?"). Son ejes distintos y una firma puede responder distinto en cada uno.
El error se encontro al pedir la cita VERBATIM en lugar de aceptar el resumen — es la misma clase de
falla que esta busqueda viene cazando desde el principio: un resumen puede sonar bien y responder la
pregunta equivocada. Se releyeron Topstep, FundedNext, MyFundedFutures y BluSky con las dos preguntas
separadas (Apex y Take Profit Trader no hacia falta: prohiben toda automatizacion). Se agrega ademas una
tercera columna, "mismo bot en otra firma", porque es una restriccion del plan y no un detalle menor.

| firma | automatizacion PROPIA | automatizacion de TERCEROS | mismo bot en OTRA FIRMA |
|---|---|---|---|
| Topstep | **SI** | **SI, explicito** | NO SE DETERMINA |
| Lucid | **SI** | **SI, no lo distingue** | NO SE DETERMINA |
| FundedNext | **SI, no lo distingue** | **SI, no lo distingue** | NO SE DETERMINA |
| MyFundedFutures | **SI** | **NO SE DETERMINA** | NO SE DETERMINA |
| Tradeify | **SI, con verificacion** | **NO, por construccion** | **NO, explicito** |
| Apex | NO (prohibida toda) | N/A | N/A |
| Take Profit Trader | NO (prohibida toda) | N/A | N/A |
| BluSky | NO SE DETERMINA | NO SE DETERMINA | NO SE DETERMINA |

**Topstep** — https://help.topstep.com/en/articles/11187768-topstepx-api-access , leida 2026-09-03.
Es la unica que nombra las dos categorias por su nombre y responde SI a ambas: "TopstepX API Access lets
advanced Traders and developers build automated strategies, connect third-party tools, and execute
trades directly through TopstepX." Y: "If you use third-party tools built by others, no coding required —
just plug in your credentials." Con descargo: "Some traders connect third-party applications to the
ProjectX API. If you do, it's at your own risk — Topstep and ProjectX don't affiliate with, endorse, or
support any external vendor or platform offering API integrations." Sobre quien opera la cuenta, la
regla real es de infraestructura, no de identidad: "All trading activity must originate from your
personal device. The use of VPS, VPNs, and remote servers is prohibited."

**Lucid** — https://support.lucidtrading.com/en/articles/11404728-other-activities , leida 2026-09-03.
Nombra una herramienta de terceros en la misma frase que "sistema automatizado", sin pedir propiedad
exclusiva: "Automated trading systems and trade copiers are permitted. All automated activity must
comply with Lucid Trading rules. Traders are fully responsible for any software errors, malfunctions, or
unintended outcomes."

**FundedNext** — https://fundednext.com/futures-challenge-terms , clausula 2.2.6, leida 2026-09-03. No
distingue de quien es el bot: "Using automated trading bots, artificial intelligence, or ultra-high-speed
execution strategies is allowed... Automated systems that violate trading policies will be identified and
disabled." La regla de identidad de cuenta esta en otra clausula (2.1.3): "sharing account credentials
with a third party for account management purposes is strictly prohibited" — prohibe delegar la cuenta a
otra persona, no dice nada del origen del software.

**MyFundedFutures** — https://help.myfundedfutures.com/en/articles/8444599-fair-play-and-prohibited-trading-practices ,
leida 2026-09-03. Permite lo propio: "Traders may make use of automated trading strategies tailored to
their own specific settings so long as these automated tools do not aim to exploit the favorable fills
offered in the Simulated Environment." No nombra terceros ni los excluye — "tailored to their own
specific settings" es sobre la configuracion, no sobre quien escribio el software, asi que queda
NO SE DETERMINA. La regla de identidad esta en otra seccion (Seccion 4): "Each individual trader is
required to maintain their own individual trading activity. Meaning, entering, exiting and cancelling
their own trade executions."

**Tradeify** — https://help.tradeify.co/en/articles/10468318-guidelines-for-traders , seccion
"Bots/Algorithmic Trading", leida 2026-09-03. Cita completa: "we allow the use of bots and algorithms
under certain conditions: Ownership: You must be able to prove that you are the sole owner of the bot or
strategy, and that no one else has access to or is using it... Exclusive Use: While you may use the bot
on your personal accounts, using it across multiple firms is against Tradeify's policy. The bot should
be solely for your own use within Tradeify." La exclusividad de propiedad excluye terceros por
construccion, y la prohibicion de multi-firma esta dicha en la misma frase.

**Apex** — "No Automation or Algorithm Usage allowed: Rewards are intended to recognize human traders
actively participating in the learning process, not to reward automated systems executing preprogrammed
logic." Prohibida por completo.

**Take Profit Trader** — "1. No Trading bots/Algos - We do not allow any automated or bot trading of any
kind. All trades must be manually executed by the trader." Prohibida por completo.

**BluSky** — https://help.blusky.pro/en/articles/12069208-ethical-trading-conduct-policy-blusky-trading-company ,
leida 2026-09-03. Nunca nombra "third-party" en relacion a software de trading. Solo prohibe el uso
ABUSIVO: "using automated software (AI, ultra-high speed, bulk data entry) to unfairly influence
outcomes" y "Account Mirroring: Copying trades from another trader, account, or signal provider" (esto
es sobre copiar OPERACIONES de otro, no sobre software de terceros en general). La clausula de identidad
de cuenta, "Unauthorized Trading: Conducting trades on behalf of third parties... without explicit, prior
authorization", es sobre operar la cuenta PARA otra persona, no sobre el origen del bot. Ninguna pagina
oficial leida autoriza ni prohibe por nombre la automatizacion propia, la de terceros, ni el uso del
mismo bot en otra firma.

Las URLs y citas completas de cada firma estan en `datos_crudos.md`.

---

## 7. NO SE DETERMINA

Cosas que se buscaron en paginas oficiales y no aparecieron. No se completaron con nada.

- **Precio del 25K de FundedNext.** El 25K solo existe en Rapid Pro / Rapid Daily / Legacy, y la propia
  FAQ dice: "Effective 10 July 2026, Rapid and Bolt accounts will no longer be available for new
  purchases or account resets." Flex, el plan barato, arranca en 50K.
- **Objetivo de ganancia del 25K de Take Profit Trader.** La tabla de la home solo expuso el 50K.
- **Monto minimo de retiro de Take Profit Trader.**
- **Costo del reset de la evaluacion de Take Profit Trader** (solo se leyo "PRO Account Resets: Up to 3 resets").
- **Costo del reset de MyFundedFutures** en Rapid y Pro.
- **Drawdown estatico de la Sim Funded de BluSky.** Esto **corta la cadena**: la fila de BluSky de la tabla
  llega hasta la fase Buffer y despues usa el retiro minimo de $250 al 90% como cota superior. Su esperanza
  real es **peor** que el -$146 publicado, no mejor.
- **Politica de automatizacion de terceros de BluSky.**
- **Discrepancia interna de Topstep, no resuelta.** Dos paginas oficiales dan precios distintos para la via
  sin cuota de activacion del 50K: `topstep.com/no-activation-fee` dice $85/mes y
  `help.topstep.com/en/articles/14289835` dice $95/mes. La aritmetica usa la via Standard ($49/mes + $149
  de activacion), que no depende de cual sea correcta.
- **Apex no tiene reset.** No es un dato faltante: "Reset Fee: N/A", y si se toca el drawdown hay que
  comprar una evaluacion nueva.

---

## 8. Reproducir

    cd research/ventana_g
    python aritmetica.py     # control + cuenta de 50K, 3 tamanos + sensibilidad al costo
    python chicas.py         # control + cuenta mas chica, 3 tamanos

Ambos abortan si el control no da ~50%.
Datos crudos con URL y fecha de lectura: `datos_crudos.md`.

# L05 — La gamma neta de los creadores de mercado: el eje de régimen que la literatura propone

**VENTANA L. Ficha de literatura. NO MEDIDA. No gasta cartucho, K sigue en 261.**

**Advertencia de encuadre, arriba de todo: esto NO es una regla de entrada.** Es un **eje de
régimen**: una variable que, según tres papers, separa los días en que las reglas de L01, L02, L06 y
L09 funcionan de los días en que no. La incluyo como candidata porque el proyecto acaba de construir
un eje de régimen propio y porque la literatura dice que el eje correcto es otro.

---

## 1. Cita completa

**El eje, en futuros de todo el mundo:**
Baltussen, Da, Lammers y Martens (2021), *JFE* 142(1), 377–403, **sección 4.1 y Tabla 7**. Ficha
completa en **L01**.

**El eje, en futuros de VIX:**
Huang, Hong-Gia; Tsai, Wei-Che; Weng, Pei-Shih; Yang, J. Jimmy (2023). **"Intraday momentum in the
VIX futures market."** *Journal of Banking & Finance*, vol. 148. Ficha completa en **L06**.

**El eje, en acciones individuales:**
Barbon, Beckmeyer, Buraschi y Moerke (2022), SFI Research Paper 22-40. Ver **L04**.

**La evidencia que lo contradice:**
Dim, Chukwuma; Eraker, Bjørn; Vilkov, Grigory (2023). **"0DTEs: Trading, Gamma Risk and Volatility
Propagation."** SSRN 4692190, 17 de noviembre de 2023.
https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4692190

## 2. El efecto, en una frase

Cuando los creadores de mercado de opciones quedan **cortos de gamma**, tienen que comprar cuando el
precio sube y vender cuando baja, y ese día el mercado tiene momento; cuando quedan **largos de
gamma**, hacen lo contrario y el mercado revierte.

## 3. Instrumento y período de la muestra original

- **Baltussen et al.:** exposición neta a gamma (NGE) del S&P 500, calculada con **OptionMetrics
  desde 1996 hasta fines de 2017**, extendida con datos de **SqueezeMetrics hasta mayo de 2020**.
  En ese período hay **2.930 días con NGE negativa y 3.158 con NGE positiva** — o sea que el
  régimen se reparte casi mitad y mitad.
- **Huang et al.:** gamma neta de las opciones sobre VIX.
- **Dim, Eraker y Vilkov:** opciones sobre el S&P 500 con vencimiento el mismo día (0DTE), período
  de auge de esos contratos, 2022 en adelante.

## 4. Magnitud declarada

**Como eje, no como ventaja.** Lo que reportan es que el efecto **existe en un régimen y no en el
otro**, no un número de dólares.

- Baltussen et al., Tabla 7: el momento intradiario **persiste sólo cuando la NGE es negativa**.
- Huang et al.: el momento en futuros de VIX **persiste sólo cuando la gamma neta de las opciones
  sobre VIX es negativa**, y se debilita cuando los inversores europeos no están en el mercado.
- Barbon et al.: una gamma agregada **muy negativa** produce momento de fin de día; una **muy
  positiva** produce reversión.

**La forma de este resultado es exactamente la que a este proyecto le importa:** no dice "el efecto
es más grande en cierto régimen", dice "**el efecto cambia de signo** con el régimen". Un eje que
cambia el signo es mucho más útil que uno que cambia la magnitud, porque un promedio sobre los dos
regímenes puede dar cero **teniendo estructura fuerte adentro**.

## 5. Antes o después de costos

No aplica. Es un condicionante, no una estrategia.

## 6. Mecanismo declarado

Cobertura delta obligatoria. Quien vendió opciones (gamma corta) tiene que operar **a favor** del
movimiento para mantenerse neutral; quien compró (gamma larga) opera **en contra**. Los usuarios
finales institucionales compran puts del índice como seguro de cartera (Bollen y Whaley 2004;
Gârleanu, Pedersen y Poteshman 2009), y como no hay contraparte natural, los creadores de mercado
absorben el desbalance y quedan cortos de gamma.

## 7. CLASIFICACIÓN

**ESTADÍSTICA como eje.** El signo de la gamma neta es un número calculado, no un dato publicado con
fecha; y su relación con el retorno es una tendencia.

## 8. Estado de replicación

**Replicado en tres mercados distintos y contradicho en un cuarto. Hay que leer los dos lados.**

**A favor:** el mismo condicionamiento por signo de gamma aparece en futuros de índice, bonos,
materias primas y monedas (Baltussen et al.), en futuros de VIX (Huang et al.) y en acciones
individuales (Barbon et al.). Tres equipos, tres mercados, mismo signo. **Eso es más fuerte que
cualquier p-valor individual.**

**En contra, y toca el supuesto de base:** Dim, Eraker y Vilkov (2023) encuentran que la gamma de
inventario de los creadores de mercado es **en promedio POSITIVA**, y está negativamente relacionada
con la volatilidad intradiaria futura. Concluyen que la presencia de 0DTE **amortigua** la
volatilidad del mercado, y que una gamma de inventario alta en 0DTE **no propaga** la volatilidad
pasada.

**Dónde coinciden y dónde no, dicho con precisión:** Dim et al. **coinciden en el signo del
mecanismo** —gamma positiva refuerza la reversión intradiaria, gamma negativa refuerza el momento—
y **discrepan en el nivel**: si en promedio los creadores de mercado están **largos** de gamma,
entonces el efecto medio no es momento sino reversión, y el resultado de Baltussen et al. depende
de que su medida de NGE tenga el nivel bien puesto.

**Ese es el punto débil real de esta candidata, y es del tipo que este proyecto ya conoce**: dos
mediciones del mismo objeto que difieren en el nivel, y una conclusión que depende del nivel.

## 9. Cuántas variantes probaron los autores

Como eje binario, **una**: el signo. Eso es lo bueno de la variable — no hay umbral que elegir.

Pero la **construcción** de la NGE tiene muchos grados de libertad: qué vencimientos incluir, qué
strikes, cómo normalizar (Baltussen et al. dividen por la capitalización del índice), y el supuesto
de que los creadores de mercado son cortos de todo lo que hay abierto (el factor −100 en su
ecuación 14). **Cada una de esas decisiones es una variante que no aparece en el conteo.**

Para el juez: si alguna vez se prueba una regla condicionada por gamma, **la construcción de la
NGE cuenta como variantes**, y no menos de 10.

## 10. Qué haría falta para probarla acá

**Los datos NO los tenemos y NO son baratos.** Ésta es la última de la lista por facilidad de prueba,
y por eso.

- **OptionMetrics** (la fuente de Baltussen et al. hasta 2017) es una suscripción académica cara.
- **SqueezeMetrics** (la fuente para 2018-2020) es un producto comercial.
- **Cboe** publica interés abierto por strike de las opciones SPX, y con eso se puede reconstruir
  una NGE aproximada para 2016-2019. Es un proyecto de recolección y de decisiones de construcción,
  no una descarga. **Semanas, no días.**

**Antes de gastar eso, hay una pregunta más barata que contestar, y la dejo planteada sin
contestarla:** la VENTANA G ya construyó un eje de régimen ex-ante con la **volatilidad de la sesión
anterior**, verificado monótono y con cociente 20,8× entre terciles
(`research/ventana_g/juez_regimen_exante.py`). La gamma neta y la volatilidad no son independientes:
la teoría dice que la gamma corta de los intermediarios **amplifica** la volatilidad. **Puede que el
eje que el proyecto ya tiene sea un sustituto pasable del eje que la literatura propone.**

Si lo fuera, esta ficha se vuelve gratis. Si no lo fuera, hay que decidir si el eje de la literatura
vale semanas de recolección. **Ninguna de las dos cosas la decido yo.**

---

## Lo que esta ficha aporta aunque nunca se mida

El proyecto lleva 261 hipótesis con veredicto y acaba de construir un juez que **exige aguantar en
los tres terciles de volatilidad** para dar SUPERA, y que tiene una categoría propia —APUESTA AL
REGIMEN— para lo que vive en un solo tercil.

**Tres papers publicados en tres mercados distintos dicen que el fenómeno intradiario mejor
documentado de la literatura ES una apuesta al régimen**, y que el régimen no es la volatilidad sino
el signo de una variable de posicionamiento.

Eso no valida ni invalida el juez. Pero significa que **la categoría APUESTA AL REGIMEN no es un
aprobado con asterisco: puede ser la forma normal en que existen estos efectos.** Lo dejo escrito
para que quien lea el veredicto de L01 no lea "vive en un solo tercil" como una decepción.

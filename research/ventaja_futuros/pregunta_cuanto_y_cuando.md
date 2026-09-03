# Qué forma tendría una pregunta de «cuánto y cuándo» que sea DECIDIBLE — Ventana D, 2026-09-03

**Esto es un documento, no una hipótesis congelada.** No formula ninguna hipótesis, no fija ninguna
condición, no corre nada. Existe porque `potencia_terreno_condicional.txt` mostró que con el α heredado
un factor de 1,4× se ve en 971 sesiones y un factor 2× con 133 por grupo, mientras que el terreno ya
mostró factores de 4 y 5 sin que nadie buscara. La pregunta de Roberto es si existe una versión de
eso que cambie una decisión real de una cuenta fondeada, y no sólo confirme agrupamiento de volatilidad.

**Declaración previa, que vale para todo lo que sigue:** cualquier pregunta que se elija después de
haber visto la escalera de horas, la de tenencias y la de stops **se elige con esos datos vistos**. Eso
no la invalida, pero se escribe en su pre-registro, y la pregunta paga K_D como cualquier otra
configuración. El mirado 2016–2019 está barrido para dirección, no para estas preguntas; barrido
significa que ya contribuyó a K, no que sus respuestas condicionales sean gratis.

## 1 · Lo primero, para que nadie lo lea al revés

**«Cuánto y cuándo» no es una ventaja.** Cambia el denominador de la cuenta, no el numerador. Una
cuenta sin ventaja direccional que opera en la hora más barata, con el stop mejor puesto y el tamaño
justo, sigue teniendo esperanza negativa: pierde más despacio. Lo que estas preguntas pueden comprar
es **sobrevivir más tiempo con el mismo capital** y **no reventar el límite diario de una cuenta
fondeada** en los días en que el terreno es peor. Eso es real y vale plata, pero se llama reducción
de costo y de riesgo de ruina, no se llama borde. Un resultado positivo acá **no autoriza dinero** por
sí solo; autoriza lo mismo que siempre: forward en simulador con datos reales.

## 2 · Las decisiones que una cuenta fondeada toma de verdad

Una cuenta fondeada tiene un límite de pérdida diario y otro total, fijados por el proveedor. Con eso,
las decisiones que se toman **antes** de cada sesión, con información que ya existe a esa hora, son
exactamente cuatro:

| decisión | palanca | lo que el terreno ya midió (2016–2019, ES) |
|---|---|---|
| **a qué hora estar adentro** | ventana de tenencia | la hora más barata cuesta 0,19 de la apertura en p50; 0,25 en p95 |
| **a qué distancia el stop** | D en puntos | 2 pts toca 87 %; 10 pts 46 %; 20 pts 21 % (T23 largo) |
| **cuántos contratos** | tamaño | micro contra grande, factor 10 en USD por punto |
| **si operar hoy** | entrar o no | 0 % de sesiones con excursión > 1.000 USD en MES a un contrato; máximo 161 pts |

Las tres primeras ya tienen respuesta incondicional en las escaleras. Lo que no tienen es respuesta
**condicional**: si la respuesta cambia según algo que se sabe a las 17:00 o a las 08:29 CT. Y la
cuarta no tiene ninguna respuesta todavía.

## 3 · La forma de una pregunta decidible

Una pregunta es decidible para la cuenta si tiene estas cinco piezas, todas escritas antes de correr:

1. **Una decisión con dos posiciones que ya existen.** «Operar a las 08:30 o a las 23:00», «stop de
   10 o de 20», «un contrato o dos», «entrar o no entrar». No una escala continua a ajustar.
2. **Una condición observable antes de decidir**, con datos que la cuenta tiene a esa hora: el rango
   del día anterior, el hueco de la reapertura de las 17:00, la excursión de la noche a las 08:29.
   Nada que se sepa después.
3. **Un resultado en la moneda de la cuenta**, no en dirección: excursión adversa en USD de MES,
   probabilidad de tocar el stop, probabilidad de que la sesión cruce el límite diario.
4. **Un umbral de efecto fijado antes, atado a la decisión.** No «¿es distinto?», sino «si el factor es
   ≥ X, la palanca va a la posición B; si no, a la A». Con eso la pregunta es decidible en los dos
   sentidos: cualquiera sea la respuesta, una posición queda elegida. Y X se elige de la cuenta, no del
   dato: por ejemplo, el factor que hace que el p95 de la excursión pase el límite diario.
5. **Una potencia declarada para ese X** con el α heredado: 1,4× a 50/50 en 971 sesiones; 1,8× en un
   decil; un factor 2 con 75 a 133 por grupo. Si X está debajo de lo detectable con la partición que
   la condición produce, la pregunta se archiva como no decidible con estos datos, como hace la
   spec con la compuerta 2, y no se corre.

## 4 · Qué la distingue de confirmar agrupamiento de volatilidad

El GARCH dice una cosa precisa: **todo escala** con la volatilidad reciente. Después de un día de
rango grande, la excursión de cada hora y de cada ventana es mayor, más o menos en la misma
proporción. Confirmar eso no cambia ninguna decisión, porque escalar todo no cambia el orden de las
palancas: la hora barata sigue barata, el stop de 10 sigue tocando la mitad de lo que toca el de 2.
Hay tres formas de pregunta cuya respuesta **no** está implicada por «todo escala»:

**Forma 1 · Invariancia de la forma.** ¿Se conserva el **orden** de las horas y de los stops bajo la
condición? Si después de un día grande la hora de las 23:00 deja de costar 0,19 y pasa a costar 0,6
de la apertura, la decisión «cuándo» cambia; si sigue en 0,19, la escalera incondicional sirve tal
cual y no hace falta condicionar nunca. El efecto es un cociente de cocientes, y el GARCH no dice
nada sobre él. Es la pregunta que sostiene «cuándo».

**Forma 2 · El residuo después de la normalización pública.** Medir la excursión **en unidades del
predictor público**, la excursión dividida por el rango del día anterior, y preguntar si el residuo
todavía depende de la condición. Lo que el GARCH explica desaparece en la división; lo que quede es
lo que no se sabía. Si no queda nada, el rango del día anterior es toda la información, y la decisión
de tamaño se toma con él, mecánicamente, sin más preguntas. Eso también es una respuesta que cambia
la decisión: pasa de «un contrato siempre» a «contratos = límite / rango de ayer».

**Forma 3 · La cola contra el límite de la cuenta.** ¿La probabilidad de que la excursión de la sesión
cruce L, el límite diario de la cuenta, sube bajo la condición por encima de un umbral fijado antes?
Es la única forma que decide «no operar hoy». Es binaria y de base baja, así que es la más cara:
con base 12 % hay que ver 21,7 % para detectarlo a 50/50 (1,8×), y con base 3 % no se ve con 971
sesiones. Se declara antes qué L es, y L viene del proveedor de la cuenta, no de los datos. **L no está
verificado en esta ventana**: es un insumo que Roberto tiene que traer con fuente y fecha, como el
margen nocturno en la spec §7.3.

## 5 · Lo que cada forma cuesta y lo que no puede dar

- **Todas pagan K_D.** Una por pregunta, y las celdas de cualquier barrido de condiciones también. Una
  pregunta con tres condiciones son tres configuraciones.
- **Las sesiones no son independientes.** Una condición sobre «ayer» corre en serie con lo que mide,
  y el n efectivo es menor que 971. El pre-registro tiene que decir cómo se trata: bloques, o
  condiciones sin solapamiento, o un n efectivo declarado.
- **Es ES, no MES, y es 2016–2019.** Los niveles de aquel régimen son la mitad de violentos; los
  cocientes pueden trasladarse, los niveles no. Una respuesta en forma de factor traslada mejor que
  una en puntos, y aun así queda sin verificar en régimen violento.
- **Un factor detectable no es un factor útil.** 1,4× en la excursión mediana puede no mover ninguna
  palanca si el límite diario está lejos. Por eso X sale de la cuenta (pieza 4) y no de la potencia.
- **Ninguna de las tres forma una ventaja.** Se repite porque es lo que se olvida primero.

## 6 · Qué recomendaría, en una línea cada una, sin formular nada

La **forma 1** es la más barata y la que más decide: si el orden se conserva, la escalera incondicional
alcanza y no hay que condicionar nunca, y eso cierra la pregunta «cuándo» para siempre con lo que ya
está medido. La **forma 3** es la única que decide «hoy no», pero exige L de la cuenta y una base
suficiente; sin L no existe. La **forma 2** es la que convierte el tamaño en una regla mecánica sin
buscar nada. Si Roberto quiere una sola, la forma 1 primero, porque su respuesta negativa también vale.

Ninguna hipótesis queda formulada acá. Cualquiera que se formule va a la sección 4 de
`hipotesis_congeladas.md`, con condición, decisión, X y potencia escritos antes, y con esta línea:
**elegida después de ver las escaleras.**

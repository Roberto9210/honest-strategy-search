# Regla de parada para el umbral de firma — escrita ANTES de correr la tercera estructura

**VENTANA G. K = 261, no gasta cartucho.** Dinero: $0.
**Este documento se escribe con la tercera estructura SIN correr. Ése es el punto.**

## El problema, dicho sin defensa

El umbral de la firma de timing se apretó barriendo `k` hasta que pasara: 0,50 → 0,20 → 0,15 →
**0,10**. Fuimos de nulo **uniforme** (pasaba) a nulo **agrupado** (rompía), y apretamos.

**¿Cómo sé que el agrupado es el peor caso y no simplemente el siguiente que se me ocurrió?** No lo
sé. Si cada estructura nueva rompe el umbral y cada vez lo aprieto, no estoy calibrando: estoy
persiguiendo, y el umbral termina describiendo **cuántos nulos se me ocurrieron**, no el mercado.

## La regla, fijada ahora

> **Tres estructuras de nulo. Si una tercera estructura plausible rompe el umbral, NO se aprieta una
> tercera vez: se para y se reporta que hay que cambiar la FIRMA, no el número.**

### Por qué tres y no otro número

- Con **una** estructura no hay evidencia de robustez: es la que se usó para construir el umbral.
- Con **dos** no se distingue "encontré el peor caso" de "encontré el segundo".
- Con **tres**, dos aprietes consecutivos significan que la tasa de aparición de estructuras que
  rompen no está bajando. Un mecanismo que resiste al peor caso no debería romperse tres veces
  seguidas contra construcciones que ni siquiera están diseñadas para atacarlo.

**No pretendo que 3 sea óptimo.** Es un corte declarado antes de mirar, que es lo único que lo hace
un corte y no una racionalización. Su virtud es que **puede cumplirse en contra**.

### Qué cuenta como "estructura plausible"

Tiene que cumplir las tres, y se declaran ahora:

1. **Nula de verdad**: el lado y las ranuras se sortean sin mirar ningún resultado.
2. **Que se parezca a cómo entra una candidata real** — no una construcción diseñada para romper la
   firma. Una estructura fabricada como ataque no cuenta para la regla de parada: cuenta como
   ataque, y los ataques se reportan aparte.
3. **Que el juez la juzgue**: si cae en NO MEDIBLE por pocas operaciones, ventana angosta o
   resolución, no llega a veredicto y no cuenta.

### Qué pasa en cada desenlace, escrito antes

| desenlace | qué se hace |
|---|---|
| **k = 0,10 sobrevive** | el umbral **queda**, y queda con tres estructuras encima en vez de dos |
| **k = 0,10 se rompe** | **NO se aprieta.** Se para y se reporta: tres estructuras y tres roturas significa que el problema es la **firma** (`zA` alto con `zB` chico) y no su umbral |
| la estructura cae en NO MEDIBLE | no cuenta como prueba; se busca otra que el juez sí juzgue, y eso se dice |

### Y qué querría decir "cambiar la firma"

Para que la salida negativa no sea un callejón, se nombra ahora lo que habría que mirar —**sin
implementar nada**: la firma actual es una regla sobre dos números (`zA`, `zB`) medidos sobre el
mismo observado. Si tres estructuras la rompen, el camino no es un tercer umbral sino **una nula que
sea válida para la clase timing por construcción** — por ejemplo una que permute *cuándo* preservando
la estructura de agrupamiento del candidato, en vez de detectarla a posteriori.

## La tercera estructura elegida, declarada antes de correrla

**Entradas con frecuencia dependiente del régimen**: el número de entradas por sesión escala con la
volatilidad ex-ante de esa sesión, con el lado por moneda.

**Por qué ésa y no otra:** es la que más se parece a cómo entra una candidata real. Casi toda regla
de entrada plausible —rupturas, reversiones, filtros de rango— dispara **más veces** en sesiones
agitadas y menos en calmas. Eso produce exactamente la patología que rompió al nulo agrupado
(concentración de entradas donde los dos lados ganan a la vez) **sin haber sido diseñada para
romperla**, y por eso cumple el requisito 2.

**Las otras dos que consideré y descarté, con el motivo:**
- *Entradas autocorreladas* (una entrada hace más probable la siguiente): plausible, pero es casi el
  agrupado con otro nombre; probaría lo mismo dos veces.
- *Concentradas alrededor de horas conocidas*: plausible, pero después de la Pieza 1 sé que el perfil
  intradiario varía 4,3×, así que sería agrupamiento por volatilidad **por la puerta de atrás**, y
  con la ventaja injusta de que yo ya sé dónde están los picos.

## Estado

**La tercera estructura NO se corrió en esta tanda.** Este documento existe para que, cuando se
corra, la regla ya esté fija y no se pueda ajustar al resultado.

## Procedencia

`juez_firma_nulos_estructurados.py` · `salida_firma_estructurados.txt` · `juez.py` (`firma_ventaja`,
`FIRMA_K = 0.10`).

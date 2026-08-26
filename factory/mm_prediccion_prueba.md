# Predicción — la prueba única multi-mercado (sellada antes de correr)

**Fecha:** 26 de agosto de 2026. **Commiteada ANTES de calcular el primer P&L de NQ/YM/NKD.**
Tercera predicción del método; las dos anteriores fallaron en magnitud (24-ago: ρ sobrestimada;
26-ago: ρ subestimada) y cada falla fue información. Se contrasta pase lo que pase.

## Lo que se predice, con magnitudes, para poder fallar

1. **δ̂ agrupado POSITIVO, en 0,05 – 0,12.** Por debajo del 0,151542 pre-registrado: ese δ es el
   máximo de 57 búsquedas y la maldición del ganador tiene que cobrarse. Si δ̂ ≥ 0,15, la sospecha
   correcta es que el calendario compartido con ES está devolviendo la suerte de la selección, no que
   F4 sea mejor de lo medido.
2. **La prueba NO llega a p ≤ 0,05.** z esperado ≈ δ̂ × √361 ≈ 1,0 – 2,1, con el centro debajo de
   1,96. Probabilidades subjetivas sobre las ramas de §g:
   - **NEGATIVO ("paramos de buscar"): 60 %**
   - positivo empujado por el bloque A (réplica, sin dinero): 30 %
   - positivo que sobrevive en el bloque B por separado: 10 %
3. **δ̂ del bloque A > δ̂ del bloque B.** El bloque A comparte el calendario donde F4 fue elegida
   mejor-de-57 con índices que correlacionan 0,71-0,95 con ES; si algo de aquella selección fue
   suerte, el bloque A la hereda y el B no.
4. **Por mercado: los tres positivos; NQ ≈ YM (dentro de ±0,04 estandarizado, son casi copias de
   ES); NKD el más chico de los tres.** Si NKD sale el más grande, sospecha de artefacto de roll
   residual antes que celebración — su banda de exclusión es la más cargada y su serie la más corta.
5. **El diagnóstico `z_diseño` y el z agrupado quedan cerca** (|diferencia| < 0,4): si difieren mucho,
   la R del bloque A no describe la dependencia de la muestra completa, y eso se dice en el veredicto.

## Qué falsea qué

- δ̂ negativo: el efecto no viaja ni al calendario compartido — F4 era ES y nada más; "paramos de
  buscar" con la evidencia más limpia posible.
- δ̂ ≥ 0,15 con bloque B chato: réplica pura de la suerte de selección; rama 2 de §g textual.
- z ≥ 1,96 con bloque B acompañando en signo y magnitud: mi rama del 10 % — y por §g se trata con MÁS
  sospecha, no con menos: potencia ~32 % en B vuelve máxima la fracción de positivos inflados.

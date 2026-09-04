# Predicción sellada — test sintético

**Escrito ANTES de correr `sintetico.py`. 2026-09-04. K = 261, no gasta cartucho.**

Esto existe para que el resultado no se pueda racionalizar después. Si sale distinto de lo que
está acá abajo, **eso es la información**, no una molestia.

## Qué se va a correr

Replicar el bracket con entradas al azar sobre dos series sintéticas sin estructura serial, y
comparar la tasa observada contra `S/(S+T)`:

- **Sintético A — gaussiano.** Paseo IID con la volatilidad por barra medida en ES, generado con
  sub-pasos dentro de cada barra para que el rango intrabarra sea realista y no degenerado.
- **Sintético B — bootstrap.** Se remuestrean IID los tripletes reales de cada barra
  (Δcierre, extensión hacia arriba, extensión hacia abajo), centrados a media cero. **Conserva
  exactamente la forma marginal de la barra de ES y destruye solo la estructura serial.**

B es el test decisivo: si el replicador funciona, B tiene que reproducir `S/(S+T)` salvo censura.

## Lo que espero, sellado

1. **Control de horizonte infinito (20 sesiones):** los dos sintéticos convergen a `S/(S+T)` dentro
   del ruido de Monte Carlo (**±0,3 puntos**), con sin-resolver por debajo del 1%.
   → *Qué lo haría fallar:* que el sesgo quede por encima de 0,3 puntos con sin-resolver ~0. Eso
   sería el replicador roto, no el mercado.

2. **Sintético a 5 sesiones:** aparece **solo** el sesgo de censura, el que predice
   `−0,5 × asimetría × %sin_resolver`. **Residuo esperado ≈ 0, dentro de ±0,3 puntos.**
   → *Qué lo haría fallar:* un residuo de ~1,3 puntos en el sintético, igual que en el real.

3. **Conclusión que espero poder escribir:** el replicador está bien y **el residuo de ~1,3 puntos
   es una propiedad del precio real de ES**, no un artefacto del código.

4. **Predicción secundaria, menos firme:** espero que A y B den parecido. Si difieren
   materialmente, la diferencia es el efecto de las colas gordas sobre el sobrepaso de la barrera —
   sería un hallazgo lateral y no estaba buscado.

## Si sale al revés

Si el sintético reproduce el residuo, **el defecto está en mi replicador** y todo lo medido con él
en esta ventana queda en suspenso hasta encontrarlo. En ese caso no se escribe nada más hasta
tenerlo localizado.

---

# RESULTADO — escrito DESPUÉS de correr. Nada de lo de arriba se editó.

**El punto 3, que era la conclusión de fondo, se sostiene: el replicador está bien y el residuo es
del ES real.** Contra 10 series sintéticas independientes, el residuo real queda a 6,6 y 4,2 desvíos
y **afuera del recorrido completo** de las 10.

**Los puntos 1 y 2, que eran las tolerancias, FALLARON — y fallaron porque la tolerancia estaba mal.**
Escribí ±0,3 puntos derivándolo del error binomial. El error binomial supone rutas independientes y
las rutas se pisan entre sí: subestima 1,2–1,8× el sesgo *pooled* y **≈5× la separación largo/corto**.
La primera corrida dio +0,56, −0,92, +1,00 y −1,09 y yo la leí como «el replicador está roto».

**El punto 4 se cumplió al revés de como lo esperaba.** Dije que A y B darían parecido y que una
diferencia sería efecto de colas gordas sobre el sobrepaso. Dieron parecido, pero no por eso: los
tests de sobrepaso (`sintetico_escala.py`) resultaron **indecidibles** al tamaño de error que tenían,
no confirmatorios ni falsatorios.

**Lo que casi hago mal.** Entre la primera corrida y el ensamble estuve escribiendo que todo el
residuo era ruido. El ensamble me corrigió: no lo es. Si me hubiera quedado con los dos tests de
localización habría publicado exactamente la conclusión opuesta a la correcta.

Detalle completo en `CRITERIO_RESULTADO.md` § *El test sintético*, salidas en `salida_sintetico.txt`,
`salida_escala.txt` y `salida_ensamble.txt`.

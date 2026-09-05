# P02 — REGLA para elegir la magnitud objetivo

**VENTANA L. NO APLICADA TODAVÍA. No gasta cartucho, K sigue en 261.**

> **ESTE DOCUMENTO SE COMMITEA SOLO, ANTES DE APLICAR LA REGLA A NINGÚN PAPER.**
> El commit siguiente es la aplicación. El orden está a la vista en el historial de git a propósito:
> si la regla y su resultado llegaran juntos, no habría forma de saber cuál se escribió primero.

---

## El problema que resuelve

`P01` usa como magnitud objetivo `m_j` el **promedio de la muestra completa** de cada paper. Savor y
Wilson promedian cincuenta y un años, Harvey et al. veintisiete, Melvin y Prins casi nueve.

**Si un efecto decayó de forma monótona, el promedio de medio siglo no es lo que 2016-2019 debería
mostrar: es más alto.** Apuntar a ese promedio y después concluir que las reglas de terceros no
transfieren sería **culpar al mercado de una elección nuestra**.

---

# LA REGLA

## R1 — Cuál subperíodo

**El último cronológicamente**, de la partición que el paper publique **en una tabla o en el texto
con su número**, siempre que venga con **su dispersión, su estadístico t o su nivel de
significación**.

**Si el paper reporta un subperíodo sin ninguna medida de error, no se usa.** Un punto sin error no
sirve para estandarizar y no se puede meter en la ponderación por varianza inversa de `P01`.

## R2 — Si el paper publica varias particiones

**Prioridad 1: cronológica sobre cualquier otra.** Un corte por décadas o por mitades no está
condicionado al resultado. Un corte por régimen —crisis contra no crisis, volatilidad alta contra
baja, con noticia contra sin noticia— **sí lo está**, y elegir de ahí es seleccionar.

**Prioridad 2: entre varias cronológicas, la MÁS GRUESA que aísle el período final.** Las
particiones finas tienen más error y **nos dan más lugar para elegir**. Si un paper publica mitades y
también quinquenios, se toma la mitad final.

**Prioridad 3: si empatan, la que tenga más observaciones.**

## R3 — Si el paper no publica subperíodos utilizables

**Se conserva la magnitud de muestra completa y se marca `SIN CORREGIR`.**

**Prohibido explícitamente:**
- Extrapolar una tasa de decaimiento.
- Aplicar el descuento del 58 % de McLean y Pontiff, que es un promedio de otra literatura sobre otro
  conjunto de anomalías. **Meter un promedio ajeno como si fuera el dato de este paper es
  exactamente el tipo de número inventado que este proyecto ya prohibió.**
- Estimar el subperíodo a partir de un gráfico.

## R4 — La dirección de la corrección NO se elige

**Si la magnitud del último subperíodo es MAYOR que la de muestra completa, se usa igual.**

La regla es "el último subperíodo", no "el más chico". Quedarse con el promedio cuando el último
subperíodo es más grande, y con el último subperíodo cuando es más chico, sería elegir el objetivo
más fácil en cada caso. **Eso es la trampa con otro nombre.**

## R5 — La regla se aplica sin mirar 2016-2019

Todas las magnitudes salen de los papers. **Ningún número de esta corrección toca los datos del
proyecto.**

## R6 — Qué pasa con la mezcla

Si algunas candidatas quedan corregidas y otras `SIN CORREGIR`, el `θ` agrupado es **una mezcla de
objetivos de distinta calidad**.

**Se declara ahora la dirección del sesgo:** si las no corregidas efectivamente decayeron, su
objetivo queda demasiado alto, su `z` sale demasiado bajo, y **el `θ` agrupado queda sesgado hacia
abajo**. O sea **conservador**: hace más difícil concluir que las reglas transfieren, no más fácil.

**Eso se reporta con el resultado, no después.**

---

# Lo que la regla NO hace

- **No arregla el sesgo de publicación.** El último subperíodo de un paper publicado sigue siendo un
  período que el autor vio antes de publicar.
- **No arregla la brecha hasta 2016.** Aun con el último subperíodo, entre el fin de los datos del
  paper y el principio de los nuestros hay años sin observar.
- **No convierte un objetivo en una predicción.** Sigue siendo la magnitud que el paper reportó, no
  la que el mercado debería dar.

---

# Condición de invalidación

**Si al aplicar esta regla aparece un caso que ella no cubre, se escribe la extensión ANTES de mirar
el número, en un commit propio, igual que éste.** Resolver un caso ambiguo con el número a la vista
invalida la corrección entera.

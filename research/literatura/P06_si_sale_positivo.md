# P06 — Qué pasa si sale positivo: el PROCEDIMIENTO, sin umbrales

**VENTANA L. NO MIDE NADA. K sigue en 261.**

**Mi objeción era que armamos una máquina muy cuidadosa para producir un veredicto sin próximo paso
escrito. Mi duda era que escribir el próximo paso ahora agrega un grado de libertad.**

**Roberto resolvió la tensión: se escribe el PROCEDIMIENTO, no los NÚMEROS.** Un procedimiento no es
ajustable; un umbral sí. Con esa forma la objeción se sostiene y la duda desaparece, así que lo
escribo.

**Regla de este documento, y es la que lo hace válido: NO CONTIENE NINGÚN NÚMERO QUE SIRVA DE VARA.**
Ni umbrales de aprobación, ni tamaños mínimos, ni fracciones. Si alguien agrega uno después, deja de
ser un procedimiento y pasa a ser una vara móvil.

---

# La secuencia

## Paso 0 — Antes de nada, decir qué NO se probó

Un positivo de `P01` dice que **las reglas de calendario publicadas por terceros conservan parte de
su magnitud en 2016-2019**. **No dice** que alguna candidata individual funcione, ni que se pueda
operar, ni nada sobre 2020-2026, ni que el mecanismo declarado sea el correcto. **Eso ya está escrito
en la sección (f) de `P01` y se copia al informe del resultado antes de cualquier otra cosa.**

## Paso 1 — Deja-una-afuera, antes de festejar

`P01` ya trae este control. **Si el veredicto depende de una sola candidata, el resultado se reporta
como "el resultado es de esa candidata" y la secuencia sigue POR ESA CANDIDATA SOLA, no por el
grupo.**

Un positivo agrupado que en realidad es una candidata no autoriza a tratar a las otras como vivas.

## Paso 2 — El aglomeramiento decide si el veredicto se puede trasladar

**Se consulta `F10` para la candidata o candidatas que sostienen el positivo.**

- Si tiene **producto comercial encontrado desde 2020**, el veredicto **no se traslada al presente**
  y la secuencia **se detiene acá hasta que exista una medición posterior a 2019**. Esa medición
  exige la caja sellada o datos nuevos, y **es una decisión de Roberto, no un paso automático**.
- Si **no** tiene producto encontrado, se sigue al paso 3 **con la asimetría recordada**: no
  encontrado no es libre.

## Paso 3 — Traducir el veredicto a la unidad de la cuenta

El resultado de `P01` está en `θ`, una fracción de magnitud publicada. **La cuenta no cobra
fracciones.** Se traduce, en este orden y sin saltear:

1. **A dólares por evento** sobre el nocional del período en que se va a operar, no sobre el de
   2016-2019. `PISO_Y_CONVERSION.md` tiene las dos columnas y la razón por la que son distintas.
2. **Restar los costos medidos**: comisión, medio-spread de entrada, deslizamiento de salida. Los
   tres están dentro del juez.
3. **Contra el piso de rentabilidad vigente**, que es el que la VENTANA G tenga medido ese día, no el
   que figura en estos documentos.

**Si en cualquiera de los tres puntos el resultado deja de ser positivo, la secuencia termina y se
reporta así. No se busca un bracket, un horario ni un tamaño que lo devuelva a positivo. Eso sería
ajustar hasta que dé.**

## Paso 4 — El juez, con la candidata individual y no con el grupo

**La prueba agrupada no reemplaza al juez y no lo puede reemplazar**: no cobra costos, no modela
brackets, no calcula probabilidad de pasar la cadena de evaluación, no mira régimen.

Se arma un candidato en el formato de `JUEZ_COMO_SE_USA.md`, con:
- `variantes_probadas` **contando todo lo declarado en `P01`, `P02` y `HIBRIDAS`**, incluidas las
  declaraciones que hicimos nosotros para quitarle el ajuste a las híbridas.
- `familia` declarada, para que el registro cuente los intentos.

**Y ese juicio gasta cartucho.** Un positivo de `P01` **no** exime del juez: lo justifica.

## Paso 5 — La ventana de exposición y el tamaño, antes de cualquier decisión de operar

`F1'` y `F8`. Para las candidatas de cierre a cierre esto no es un trámite: la Compuerta 1 midió que
en ES una noche sola se lleva el drawdown entero con frecuencia conocida, y que en MES no.

**Y la dependencia externa sigue sin resolverse: si la evaluación tiene límite de tiempo.** Mientras
no esté contestada, cualquier conclusión sobre la palanca del micro es cota optimista.

## Paso 6 — Decidir el vehículo

La VENTANA G ya tiene medido que la evaluación no deja de convenir a ningún capital y que el cruce
cae en el propio piso. **Ese trabajo se usa tal como está; no se rehace.**

## Paso 7 — Escribir lo que quedó sin cubrir

**Igual que hace el juez en cada veredicto.** Un positivo que llegó hasta acá arrastra por lo menos:
la brecha entre el fin de los datos de cada paper y 2016; la brecha entre 2019 y hoy; las
desviaciones declaradas en `P04`; y el aglomeramiento de `F10`.

---

# El orden importa, y por qué

**Los pasos 1 y 2 pueden detener la secuencia y son los dos más baratos.** Cuestan una consulta a
documentos que ya existen.

**El paso 4, que es el caro, va después.** Si el paso 2 dice que el veredicto no se traslada, gastar
un cartucho del juez sería juzgar un efecto que ya sabemos que no podemos usar.

**Esa es la única optimización que este procedimiento hace: poner lo que puede matar adelante.** No
hay ninguna otra decisión adentro.

---

# Lo que este documento deliberadamente NO dice

- **Ningún umbral.** Ni de `θ`, ni de dólares, ni de desvíos, ni de eventos.
- **Ninguna prioridad entre candidatas** en caso de positivo múltiple. El orden lo dan `F7` y
  `ORDEN_DE_TRABAJO.md`, que se escribieron antes y sin conocer ningún resultado.
- **Ninguna condición para reintentar.** `P01` ya dice que un negativo no se reintenta con otro
  agrupamiento. **Un positivo tampoco autoriza a reagrupar.**

**Si dentro de seis meses alguien quiere agregarle un número a este documento, la pregunta que tiene
que contestar primero es: ¿lo estoy agregando antes o después de ver un resultado?**

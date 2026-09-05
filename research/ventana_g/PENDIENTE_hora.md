# PENDIENTE — hipótesis de selección horaria. NO ABIERTA. Gastaría cartucho.

**Anotada 2026-09-04 por VENTANA G. No corrida. K sigue en 261.**

## La hipótesis

Operar solo en ciertas horas del día reduce el costo real de operar lo suficiente como para
cambiar el veredicto de la evaluación de fondeo.

## El fundamento medido que la hace candidata

Dos mediciones ya hechas, ambas sobre ES 1-min Databento 2016-2019, P-escalera de 971 sesiones:

1. **La frecuencia de toque del stop varía ~20× con la hora.** `terreno_stop_resultado.md` §3:
   con tenencia de una hora y D=8, las 23:00 CT tocan 1,2% contra 24,0% de la apertura.
2. **La MEDIA del exceso de deslizamiento también varía con la hora**, y es un hallazgo nuevo de
   `media_exceso.py` (2026-09-04), no de la fase anterior:

   | D | hora más barata | hora más cara | razón |
   |---|---|---|---|
   | 4pt | 0,336pt (03:00 CT) | 1,317pt (17:00 CT) | 3,9× |
   | 10pt | 0,286pt (01:00 CT) | 2,406pt (15:00 CT) | 8,4× |
   | 20pt | 0,417pt (03:00 CT) | 6,000pt (21:00 CT) | 14,4× |

   El patrón es coherente: la reapertura nocturna (17:00) y el cierre de contado (15:00) son caros;
   las horas europeas de madrugada (01:00–03:00) son baratas.

Esto importa porque VENTANA G acaba de cerrar sin criterio publicable por un margen de +1,7 puntos
de tasa de acierto. Una reducción del deslizamiento medio de 0,722pt a ~0,3pt en la celda 5pt:10pt
movería el requerido en el orden del margen entero.

## Por qué NO se abre acá

- **Es una regla de selección elegida DESPUÉS de mirar el dato.** Hay 23 horas candidatas; elegir la
  mejor y reportarla como hallazgo es exactamente la multiplicidad que este programa contabiliza.
  Pagaría K.
- **Las n por hora son chicas donde más importa.** A D=10 la hora de la 01:00 tiene n=7 y las 23:00
  n=5; a D=20 varias horas tienen n≤3. El efecto por hora a stops anchos es apenas estimable con
  esta muestra, y las razones de arriba están dominadas por ruido en esas celdas.
- **El terreno es 2016-2019.** La estructura horaria de 2020+ está dentro de la caja sellada.
- **Confunde dos cosas que VENTANA G acaba de separar**: menos deslizamiento (esperanza) y menos
  toques (probabilidad de tocar el límite). Una hipótesis horaria seria tiene que decir cuál de las
  dos afirma antes de correr.

## Qué haría falta para abrirla bien

Pre-registro con su propio K, la hora (o el bloque de horas) elegida **antes** de mirar el resultado,
una n mínima declarada por celda, y el estadístico decidido de antemano — media del exceso, frecuencia
de toque, o las dos por separado.

**Decisión: queda escrita y sin abrir, para que se decida con presupuesto y no de pasada.**

# Veredicto — Fase 1 de la búsqueda de estrategia

**Fecha:** 19 de agosto de 2026 · **Decisión:** cierre anticipado conforme a spec §6, autorizado por Roberto.
**Spec:** `spec_busqueda_estrategia.md` v1 (aprobada antes de correr el primer backtest; ninguna vara se movió durante la búsqueda).

## Qué se buscó y cómo

Ventaja explotable en el futuro MES (micro E-mini S&P 500) mediante 5 familias de estrategias con reglas explícitas, evaluadas **netas de fricción** ($3.90 por operación por contrato: comisión $1.40 + slippage 2 ticks), sobre datos verificados con control de calidad independiente:

- Diario: ES=F 2000–2026 (Yahoo, con 10 filas de artefacto de roll identificadas y control cruzado contra SPY).
- Intradía: OHLCV 1-min del CME vía Databento, 2016–2026 (el QC demostró que 2010–2015 no tiene minuto confiable), 31 días degradados excluidos.
- Partición temporal: desarrollo (A) = 2016–2019 intradía / 2000–2019 diario; caja fuerte (B) = 2020–2026, **jamás tocada** — ninguna candidata mereció el examen final.

Vara de aprobación (fijada antes de mirar datos): ≥200 operaciones en B, factor de ganancia neto ≥1.3 en B, rentabilidad positiva en cada año de B, robustez ±20% en parámetros.

## Resultados por familia

| Familia | Configs usadas | Mejor resultado neto (parte A) | Estado |
|---|---|---|---|
| F1 Ruptura de apertura | 20/20 | PF 1.07 (ORB30 + gap vs día previo; 308 ops, 2/4 años+) | **Muerta** |
| F2 Tendencia diaria | 14/20 | Variantes activas PF ≤1.02; las "ganadoras" (PF 23.7, 9 ops/19 años) son exposición al alza del índice, no estrategia | **Muerta** (cierre por convergencia) |
| F3 Reversión al VWAP | 6/20 | PF 0.75; todas las variantes entre 0.53–0.75 | **Muerta** (cierre por goleada) |
| F4 Calendario | 10/20 | Vuelta de mes: PF 1.51 neto, 231 ops/20 años, 18/20 años+, confirmada en SPY | **Señal real, fuera de alcance**: ~12 ops/año no alcanza la vara de 200 en B, y exige posiciones nocturnas — incompatible con reglas de prop firms |
| F5 Volatilidad | 7/20 | NR7 diario con salida al día siguiente: PF 1.17 | **Muerta** (bajo la vara; sus variantes intradía vía filtros de F1 quedaron ≤0.97) |

Total: **59 experimentos**, todos registrados en `experiments_ledger.jsonl` con cadena de hashes verificable (`harness.verify_ledger()`); ninguno borrado ni reescrito.

## Errores propios, documentados

Tres configuraciones de F1 se gastaron en un filtro mal diseñado ("apertura fuera del rango nocturno" definido con el nocturno llegando hasta las 09:29, lo que hace la condición casi imposible: produjo 0–1 operaciones). El presupuesto se respetó igual: los errores de diseño también consumen cartuchos, y así queda registrado.

## Veredicto

**En estas 5 familias, con reglas explícitas y costos minoristas realistas, no existe ventaja explotable para nosotros en el ES/MES.** Las mejores configuraciones honestas quedan entre el empate y 1.07 — por debajo de cualquier umbral de continuación, y muy lejos de la vara de 1.3 que separa una estrategia operable de un espejismo estadístico.

Lo que este veredicto **no** dice: no dice que nadie pueda ganar en futuros; dice que las familias simples y documentadas, netas de fricción, sobre el mercado más arbitrado del planeta, no dejan margen para un operador minorista con estas herramientas. Este es el resultado que la literatura predice y que el proyecto de origen (ALAYA) obtuvo en meses y con dinero real; esta vez costó **una semana y $0** (los $17.90 de datos salieron de créditos de regalo), con evidencia auditable.

## Puertas que quedan abiertas (banco de suplentes)

1. Estrategias de los amigos traders de Roberto (pendiente de sus respuestas al cuestionario de 5 preguntas) — entrarían a una **Fase 1b consciente**, con la vara endurecida por pruebas múltiples.
2. Mercados menos eficientes que el S&P — solo como decisión escrita, con nueva spec.
3. La señal de vuelta de mes (F4): real pero de baja frecuencia; incompatible con el objetivo prop. Anotada por si algún día el objetivo cambia.

## Destino de los recursos

Conforme a spec §6 y §8: los recursos vuelven al **plan de ingresos** (informe del 19-ago): distribución de deadman, servicios de auditoría, y guardián para traders de prop firms. Primer activo derivado de esta búsqueda: el propio ledger de 59 experimentos honestos, publicable como demostración de método — en un nicho saturado de backtests falsificados, un registro de fracasos a prueba de manipulación es el argumento de credibilidad más fuerte disponible.

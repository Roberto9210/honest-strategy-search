# SPEC de búsqueda de estrategia — v1

*Proyecto: encontrar una estrategia con ventaja real para operar futuros en NinjaTrader (simulado primero). Esta spec se aprueba ANTES de correr el primer backtest y no se cambia a mitad de camino sin dejarlo escrito. Igual que en deadman: los criterios se fijan antes, para que los resultados no nos tienten a moverlos.*

---

## 1. Qué buscamos y dónde

**Instrumento:** MES (Micro E-mini S&P 500). Uno solo, para empezar: es el contrato más líquido en su categoría micro, la unidad de riesgo más chica de los futuros de índices ($5 por punto), y el que toda prop firm acepta. Si algo funciona en MES, después se explora si generaliza.

**Horizonte:** estrategias intradía o de pocos días, con reglas 100% explícitas — nada que no se pueda escribir en una página y auditar. Sin cajas negras, sin redes neuronales, sin indicadores mágicos comprados.

**Familias candidatas (5, en este orden):**

1. **Ruptura de rango de apertura** — operar el quiebre del rango de los primeros 15/30 minutos de la sesión.
2. **Seguimiento de tendencia intradía** — cruces de medias / canales de Donchian; pocas señales, tendencias largas.
3. **Reversión a la media** — desviaciones extremas respecto del VWAP o del cierre previo, apostando al regreso.
4. **Patrones de calendario y hora** — comportamiento por hora del día, día de la semana, gaps de apertura.
5. **Volatilidad** — compresión→expansión (rangos anormalmente chicos que preceden movimientos).

Presupuesto por familia: **máximo 20 configuraciones probadas**. Cada prueba —gane o pierda— queda anotada en el registro de experimentos. Probar 100 variantes y contar solo la que ganó es la forma más común de mentirse a uno mismo; el registro completo es lo que lo impide.

## 2. Los costos van dentro, siempre

Ninguna cifra se mira en bruto. Cada operación simulada paga:

- **Comisión:** ~$1.40 por ida y vuelta por contrato (broker + exchange, tarifa realista de NinjaTrader).
- **Slippage:** 1 tick por lado ($1.25 + $1.25 = $2.50) como supuesto conservador para órdenes a mercado.
- **Total de fricción: ~$4 por operación por contrato** — casi un punto entero del MES. Esto va a matar a la mayoría de las ideas de alta frecuencia. Ese es exactamente el punto: el bug del "+$0.29 bruto" no se repite.

## 3. Datos

Se necesitan **mínimo 4–6 años de datos intradía** (velas de 1–5 minutos) que incluyan regímenes distintos: el mercado bajista de 2022, los alcistas de 2023–2024, la volatilidad de 2025. Primero intento fuentes gratuitas; si la calidad no alcanza, un dataset histórico de proveedor serio cuesta $30–100 una sola vez — **el único gasto posible de todo este proyecto**, y se consulta antes de hacerlo. Datos malos = veredictos falsos; acá no se ahorra.

## 4. Reglas anti-autoengaño (las más importantes)

- **Partición temporal:** los datos se cortan en dos desde el día uno. Con la parte A (más vieja, ~70%) se desarrolla y ajusta. La parte B (más reciente, ~30%) queda **en una caja fuerte**: cada candidata la toca **una sola vez**, al final, como examen final. Si falla ahí, muere — no se vuelve a ajustar para reintentarlo, porque eso sería memorizar el examen.
- **Robustez de parámetros:** si la estrategia gana con media móvil de 20 pero pierde con 18 y 22, no hay ventaja — hay casualidad. Toda sobreviviente debe ganar en una vecindad de sus parámetros, no en un punto exacto.
- **Registro de experimentos append-only:** cada configuración probada se anota (familia, parámetros, resultado, fecha) en un registro que no se edita. Lo que se probó y falló cuenta en la estadística: es la vacuna contra el "esta vez sí".

## 5. Criterio "PASA" (por candidata, definido antes de mirar nada)

Una candidata sobrevive la Fase 1 solo si, **en la parte B (datos nunca vistos), neta de costos**, cumple TODO esto:

| Métrica | Vara |
|---|---|
| Operaciones en el examen final | ≥ 200 |
| Factor de ganancia (bruto ganado / bruto perdido) | ≥ 1.3 |
| Rentabilidad por año del examen | Positiva en cada año, no solo en el total |
| Peor racha (drawdown) | ≤ 2× la mejor racha de ganancia equivalente |
| Robustez | Gana también con parámetros vecinos (±20%) |

## 6. Criterio "BASTA" (el límite de la búsqueda)

- **Tiempo:** 6 semanas de Fase 1 desde que haya datos buenos.
- **Alcance:** las 5 familias, máximo 20 configuraciones cada una, todas registradas.
- **Si nada pasa la vara:** el veredicto es "estas familias no tienen ventaja explotable para nosotros con estos costos" — se escribe, se archiva y **se para**. No se agregan familias "solo una más", no se afloja la vara. Los recursos vuelven al plan de ingresos (auditorías / guardián de prop firms), que sigue vivo con el 20% mientras tanto.

Ese veredicto negativo, si llega, no es un fracaso: es exactamente el dato que a ALAYA le costó meses y dinero obtener sin spec. Esta vez costaría 6 semanas y como mucho $100.

## 7. Fase 2 (solo para sobrevivientes)

- La candidata corre **4+ semanas en el simulador de NinjaTrader en vivo**, envuelta en deadman (límite diario, kill switch, ledger anclado — el registro público de la corrida es en sí mismo material para la credencial).
- **Vara de la Fase 2:** el rendimiento en vivo-simulado no degrada más de 30% respecto del examen final histórico, y cero incidentes operativos sin explicar.
- Solo con Fase 2 aprobada se abre la conversación de prop firm — con su propia decisión y su propio presupuesto acotado a la cuota.

## 8. Reparto de recursos

**80%** de nuestro tiempo a esta búsqueda / **20%** al plan de ingresos del informe (mantener viva la vía de auditorías y la distribución de deadman). Este reparto es parte de la spec: la búsqueda tiene pago incierto por naturaleza y no se lleva la red de seguridad puesta.

---

*v1 — 19 de agosto de 2026. Para aprobar o corregir por Roberto antes de correr nada.*

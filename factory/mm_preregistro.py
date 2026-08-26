"""Registra en el ledger, ANTES del primer P&L multi-mercado:
  1. la APROBACION INFORMADA de Roberto del AFLOJA 1ff6891425c4bcd0, con lo que sabia
  2. el PRE-REGISTRO de la prueba unica (K=1) con todo congelado

Un solo uso: si las entradas ya existen, se niega. Usa el _append del harness para
mantener la cadena de hashes; no pasa por preregister() de Fase 2 porque esa funcion
valida contra el presupuesto y la criba de OTRA spec (familias de ES) y esta fase no es
la Fase 2 -- es la prueba unica de spec_botc_multimercado.md, con su propia regla ya
sellada en commits 7c0e4d0/250d298/59fa917.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness_f2 as f2

ya = [e for e in f2.read_ledger()
      if e.get("kind") in ("APROBACION_INFORMADA", "PRE_REGISTRO")
      and "multimercado" in str(e.get("config", {}))]
if ya:
    print(f"YA REGISTRADOS ({len(ya)}), no se duplica"); sys.exit(1)

e1 = f2._append({
    "phase": "botc-multimercado", "kind": "APROBACION_INFORMADA", "family": "META",
    "config": {"evento": "APROBACION INFORMADA", "aprueba": "AFLOJA 1ff6891425c4bcd0",
               "spec": "spec_botc_multimercado.md §b.7/§i"},
    "part": "meta", "result": None,
    "aprobado_por": "Roberto, 26-ago-2026, explicitamente y por su nombre",
    "que_sabia_al_aprobar": [
        "rho(NQ,YM) = 0.7395 esta MEDIDA (matriz del 26-ago, 210 periodos comunes) y "
        "contada dentro del n efectivo de las dos compuertas -- no supuesta",
        "decir que NO no cerraba la fase: sin YM el n efectivo es 340.1 y no pasa ni la "
        "compuerta 1 (umbral 341.78); verificado junto con sus otras dos filas, "
        "sin NKD 348.7 y sin NQ 303.5, y las cuatro reproducen el 361.3 del veredicto",
        "la fase abre por 1.4% (compuerta 2: 346.7 vs 342) y ese margen entero lo pone "
        "NKD -- el mercado de peor calidad de datos (serie desde 2004, 90 exclusiones "
        "de roll, detector empirico inservible) y el unico sin micro contrato",
    ],
    "note": "El AFLOJA queda marcado para siempre; esta entrada registra que se aprobo "
            "con los ojos abiertos, no por inferencia de un encargo.",
})
print("APROBACION_INFORMADA:", e1["hash"])

e2 = f2._append({
    "phase": "botc-multimercado", "kind": "PRE_REGISTRO", "family": "F4-multimercado",
    "config": {
        "kind": "turn_of_month", "n_before": 4, "m_after": 3, "side": "long",
        "contracts": 1,
        "mercados": ["NQ", "YM", "NKD"],
        "muestra": "vueltas de mes post-exclusion de roll, historia completa de cada serie "
                   "(mm_muestra.json: NQ 309, YM 289, NKD 180; N = 778)",
        "friccion_rt_usd": {"NQ/MNQ": 2.40, "YM/MYM": 2.40, "NKD": 52.50},
        "estadistico": "delta_hat = media de net/sigma_i sobre las N operaciones; "
                       "SE agrupado por periodo de vuelta de mes; z = delta_hat/SE",
        "criterio": "confirma sii |z| >= 1.959964 (p <= 0.05 bilateral)",
        "K": 1,
        "n_efectivo_preregistrado": 361.3,
        "z_diseno_diagnostico": "delta_hat*sqrt(361.3), se publica siempre, no es segunda prueba",
        "divulgaciones": "bloques A (<=2019-11) y B (2019-12->) por separado + delta_hat "
                         "por mercado; descriptivas, no pruebas",
        "fecha_de_corte": "2026-08-28: sin prueba corrida y veredicto escrito, se publica "
                          "el estado y BOT C cierra igual",
    },
    "part": "A+B propias (la caja fuerte de ES NO se toca)",
    "result": None,
    "hypothesis": "el flujo de rebalanceo de fin de mes de indices de acciones deja un "
                  "residuo positivo alcista en la vuelta de mes, el mismo efecto medido "
                  "en ES (ledger 049b809f5e9def5c), sobre indices nunca usados para "
                  "seleccionar nada",
    "prohibiciones_vigentes": [
        "re-optimizar n_before/m_after en cualquier mercado",
        "cambiar la lista despues de ver un numero",
        "correr la fase dos veces",
        "probar el lado corto",
        "agregar un filtro",
        "reportar el mejor subconjunto de mercados",
    ],
    "regla_de_parada": "esto cierra a F4, no la salva: si NEGATIVO se escribe 'PARAMOS "
                       "DE BUSCAR', jamas 'se demostro que F4 es falsa'; ramas y "
                       "autorizaciones en spec §g, sensibilidad en §h",
    "note": "PRE-REGISTRO de la prueba unica multi-mercado. K=257 de la busqueda se "
            "hereda intacto y no se toca: esta prueba no es una busqueda.",
})
print("PRE_REGISTRO:", e2["hash"])

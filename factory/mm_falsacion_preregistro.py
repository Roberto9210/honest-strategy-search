"""Registra en el ledger las CUATRO pruebas de la ronda de falsacion (K 258-261),
ANTES de correr cualquiera. Un solo uso."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness_f2 as f2

ya = [e for e in f2.read_ledger() if e.get("kind") == "PRE_REGISTRO_FALSACION"]
if ya:
    print(f"YA REGISTRADAS ({len(ya)}), no se duplica"); sys.exit(1)

BASE = {"phase": "botc-multimercado", "family": "F4-multimercado-falsacion",
        "part": "A+B propias (ES no participa; su caja fuerte sigue sellada)",
        "result": None,
        "prediccion": "mm_prediccion_falsacion.md, commiteada antes de correr",
        "regla": "una corrida; puede salir EN CONTRA; prohibidas variantes de "
                 "turn_of_month; ningun resultado puede hacer a F4 mas grande"}

PRUEBAS = [
    ("P1-placebo-calendario", 258,
     {"ventana": "apertura sesion 8 -> apertura sesion 14 del mismo mes, 6 pasos",
      "friccion": "misma por instrumento", "roll": "misma exclusion por banda",
      "pasa_si": "delta_placebo_neto < 0.0509 (= delta_TOM/2)"},
     "si el placebo paga parecido, F4 era deriva alcista disfrazada de calendario"),
    ("P2-contado-testigo", 259,
     {"indices": ["^NDX", "^DJI", "^N225"], "regla": "misma ventana -4/+3 sobre el "
      "calendario propio de cada indice, recortado al rango de su futuro",
      "comparacion": "BRUTO contra BRUTO", "pasa_si": "delta bruto > 0 en los tres"},
     "si los futuros lo muestran y el contado no, es artefacto de futuro y F4 muere"),
    ("P3-concentracion-frontera", 260,
     {"descomposicion": "6 pasos apertura->apertura del retorno BRUTO, estandarizados "
      "por el sigma del retorno completo", "frontera": "los 3 pasos centrales",
      "pasa_si": "participacion de la frontera >= 0.60"},
     "repartido parejo se parece a deriva y refuerza a P1"),
    ("P4-signo-rebalanceo", 261,
     {"corte": "SIGNO de close(sesion -5)/close(ultima de M-1) - 1: el mes que "
      "termina, conocido a la entrada; un solo corte, jamas un umbral",
      "pasa_si": "delta(tras baja) - delta(tras alza) >= 0.02",
      "prohibicion": "un resultado a favor NO autoriza operar solo tras meses en "
      "baja: estrategia nueva = K propia y pre-registro propio"},
     "invertido o plano: la explicacion de flujo de rebalanceo no se sostiene"),
]
for nombre, k, cfg, consecuencia in PRUEBAS:
    e = f2._append({**BASE, "kind": "PRE_REGISTRO_FALSACION",
                    "config": {"prueba": nombre, **cfg},
                    "K_acumulado": k, "consecuencia_si_falla": consecuencia,
                    "note": f"Ronda de falsacion {nombre} (K={k}). Conclusion global: "
                            "AGUANTA sii las cuatro pasan (spec §k)."})
    print(f"{nombre}: {e['hash']}  (K={k})")

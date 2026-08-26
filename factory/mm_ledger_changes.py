"""Registra en el ledger los DOS cambios de regla de la spec multi-mercado de BOT C,
ANTES de correr la matriz. Un solo uso; si las entradas ya existen, se niega."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import harness_f2 as f2

marca = "spec_botc_multimercado"
ya = [e for e in f2.rules_changes() if marca in (e.get("resumen") or "")]
if ya:
    print(f"YA REGISTRADOS ({len(ya)}), no se duplica"); sys.exit(1)

e1 = f2.log_rules_change(
    direccion="AFLOJA",
    seccion="spec_botc_multimercado §b.7",
    resumen=("spec_botc_multimercado: la regla 'un mercado por pozo de flujo independiente' "
             "(multimercado_dia0 §2) se sustituye por la medicion directa de la matriz de "
             "correlacion; NQ e YM conviven en la lista"),
    argumento=("multimercado_dia0 §2 exigia un mercado por pozo porque alli rho se iba a SUPONER, "
               "y un filtro a priori era la unica defensa contra la dependencia. En esta fase rho "
               "SE MIDE (matriz completa de retornos de vuelta de mes 2000-2019, salida ciega) y el "
               "n_efectivo entra a la regla de decision con la matriz, no con un escalar supuesto. "
               "Sustituir el filtro por la medicion es estrictamente mas informativo, y la "
               "dependencia NQ-YM no queda escondida: es un numero publicado suelto (spec §D1). "
               "Riesgo declarado: si NQ-YM sale >0.85 el pozo del Dow no es distinguible y el "
               "mercado extra aporta casi nada al n_efectivo - cosa que la propia matriz cobrara."),
    aprobado_por=("Roberto, encargo 26-ago (correccion B: puso NQ e YM juntos en la lista de la "
                  "fase y ordeno medir la matriz de correlacion como la medicion que decide)"),
)
print("AFLOJA registrado:", e1["hash"])

e2 = f2.log_rules_change(
    direccion="ENDURECE",
    seccion="spec_botc_multimercado §d",
    resumen=("spec_botc_multimercado: compuerta 2 - la apertura de la fase exige n_efectivo >= 342 "
             "TAMBIEN con cada correlacion en su cota superior al 90% (rho + 1.2816*SE, "
             "SE=(1-rho^2)/sqrt(n_par-3)); fail-closed al filo"),
    argumento=("Con N=778 nominales la correlacion de quiebre de la compuerta 1 es 0.765, y "
               "correlaciones de 0.7-0.9 entre indices bursatiles son lo esperable: el veredicto va "
               "a caer cerca del filo, y una decision al filo sobre un parametro estimado con "
               "127-211 observaciones la decide el error de estimacion, no el dato. La compuerta 2 "
               "obliga a que la apertura sobreviva a la incertidumbre de la propia matriz. "
               "Declarada en la spec (commit 7c0e4d0) ANTES de conocer un solo numero de la matriz, "
               "con la prediccion sellada dandole ~55% a la apertura - no es una vara puesta "
               "despues de ver que convenia."),
)
print("ENDURECE registrado:", e2["hash"])

#!/usr/bin/env bash
# Corre la suite de la Fase 2 sin perder su estado de salida.
#
# El bug que este archivo existe para no repetir: `python test_dia0.py | tail -4`
# devuelve el estado de TAIL, no el de la suite, asi que una corrida con fallas
# se ve como exito. Paso una vez y se escribio "0 failures" en un commit sobre
# una suite que tenia 1.
#
# Dos cinturones:
#   1. pipefail  -> el estado de la tuberia es el del primer comando que falla
#   2. la suite escribe su veredicto en ultimo_resultado.json, que ninguna
#      tuberia puede tapar
set -euo pipefail

cd "$(dirname "$0")/../.."
PY="./venv/Scripts/python.exe"
[ -x "$PY" ] || PY="python"

PYTHONIOENCODING=utf-8 "$PY" tests/fase2/test_dia0.py "$@" | tee tests/fase2/ultima_corrida.log
estado=${PIPESTATUS[0]}

echo
echo "--- veredicto del archivo (no del estado de salida) ---"
cat tests/fase2/ultimo_resultado.json
echo
exit "$estado"

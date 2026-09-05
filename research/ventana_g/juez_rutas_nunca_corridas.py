"""
VENTANA G - EJERCITAR LAS DOS RUTAS QUE ESTABAN ESCRITAS Y NUNCA CORRIDAS.

NO GASTA CARTUCHO. K = 261. No se juzga ningun candidato real: se ejercita codigo. La caja sellada
no se toca.

(a) EL DETECTOR DE FIRMA DE TIMING pasado por informe(). Lo escribi y lo corri, pero el candidato de
    timing lo juzgue con un script que NO llama a informe(), asi que el bloque nunca se imprimio:
    el mismo error que --verificar, una capa mas adentro. Se pasa un candidato con ventaja de TIMING
    declarada como 'direccional' -que es el caso donde el aviso hace falta- y se confirma que sale.

(b) EL JUEZ POR LINEA DE COMANDOS. Todo se ejercito importando el modulo; la ruta main(argv) -parseo
    de banderas, lectura del archivo, Rechazo, NoMedible, codigos de salida- nunca se corrio. Es la
    capa que va a tocar un lanzador de doble clic, o sea la que Roberto va a usar de verdad.
"""
import os
import subprocess
import sys

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import juez as J            # noqa: E402
import juez_controles as C  # noqa: E402

NPERM = int(os.environ.get("JUEZ_NPERM", "150"))
PY = sys.executable


def main():
    print("=" * 98)
    print("EJERCITAR LAS DOS RUTAS NUNCA CORRIDAS: el detector por informe(), y la CLI")
    print("NO GASTA CARTUCHO. K = 261. La caja sellada no se toca.")
    print("=" * 98)
    ok = {}

    # ---------------------------------------------------------------- (a) el detector, por informe()
    print("\n(a) EL DETECTOR DE FIRMA DE TIMING, pasado por informe().")
    print("    Candidato con ventaja de TIMING pero declarada 'direccional': es el caso donde el juez")
    print("    lo mata con la nula de signo y el usuario tiene que enterarse de por que.")
    m = J.cargar_mercado()
    rng = np.random.default_rng(20260904)
    idx = C.grilla(m, [2016, 2017, 2018])
    pL, pS = C.ambos_lados(m, idx)
    dL = pL * J.PUNTO["ES"] - J.COMISION["ES"]; dS = pS * J.PUNTO["ES"] - J.COMISION["ES"]
    prom = (dL + dS) / 2.0
    sel = prom >= np.quantile(prom, 2 / 3)
    lado = rng.random(int(sel.sum())) < 0.5
    cand = C.candidato("timing_mal_declarado", m, idx[sel], lado, clase="direccional")
    reg = os.path.join(os.environ.get("TEMP", "/tmp"), "rutas_detector.jsonl")
    if os.path.exists(reg):
        os.remove(reg)
    s = J.juzgar(cand, m, npermuta=NPERM, registro=reg)
    txt = J.informe(s)
    salio = "BANDERA ROJA" in txt and "firma de TIMING" in txt.replace("FIRMA DE TIMING", "firma de TIMING")
    r = s["periodos"]["trabajo"]
    print(f"    veredicto: {r['veredicto']}   clase declarada {r['clase_declarada']} / firma medida {r['firma']}")
    for ln in txt.splitlines():
        if "BANDERA ROJA" in ln or "firma de TIMING" in ln or "declarala asi" in ln or "minimo de las TRES" in ln:
            print(f"      {ln}")
    print(f"    el bloque se imprime: {'SI' if salio else 'NO - FALLA'}")
    ok["a detector"] = salio

    # ---------------------------------------------------------------- (b) la CLI de verdad
    print("\n(b) EL JUEZ POR LINEA DE COMANDOS (subproceso real, no import).")
    casos = [
        ("sin argumentos", [PY, "juez.py"], 2),
        ("rechazado.json (trae 'pnl')", [PY, "juez.py", "ejemplos_juez/rechazado.json"], 1),
        ("valido.json", [PY, "juez.py", "ejemplos_juez/valido.json"], 0),
        ("valido.json --pasivo", [PY, "juez.py", "ejemplos_juez/valido.json", "--pasivo"], 0),
    ]
    entorno = dict(os.environ, PYTHONUTF8="1")
    for nombre, cmd, esperado in casos:
        p = subprocess.run(cmd, cwd=AQUI, capture_output=True, text=True, env=entorno)
        sal = (p.stdout or "") + (p.returncode and (p.stderr or "") or "")
        prim = next((l for l in (p.stdout or "").splitlines() if l.strip()), "(sin salida)")
        cabeza = next((l for l in (p.stdout or "").splitlines() if "VEREDICTO" in l or "RECHAZADA" in l or "uso:" in l), prim)
        bien = p.returncode == esperado and len(p.stdout.strip()) > 0
        print(f"    {nombre:<32} codigo {p.returncode} (esperado {esperado})  {'OK' if bien else 'FALLA'}")
        print(f"       {cabeza[:110]}")
        if p.returncode != esperado and p.stderr:
            print(f"       stderr: {p.stderr.strip().splitlines()[-1][:110]}")
        ok[f"b {nombre}"] = bien

    print("\n" + "=" * 98)
    for k, v in ok.items():
        print(f"   {k:<38} {'PASADO' if v else 'FALLADO'}")
    todos = all(ok.values())
    print(f"\n   LAS DOS RUTAS {'QUEDAN EJERCITADAS' if todos else 'TIENEN UN PROBLEMA'}: "
          f"'escrito' y 'alguna vez corrido' ya son el mismo numero.")
    print("=" * 98)
    if not todos:
        raise SystemExit("FALLO: alguna ruta no se comporta como dice el codigo")


if __name__ == "__main__":
    main()

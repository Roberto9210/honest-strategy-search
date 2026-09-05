"""
EL JUEZ - veredicto honesto sobre un candidato, contra los datos, en minutos.

NO GASTA CARTUCHO. K = 261. Construir la herramienta no es usarla.

Empaqueta lo que la VENTANA G aprendio a los golpes. Si estas leyendo esto sin haber vivido esa
semana, alcanza con JUEZ_COMO_SE_USA.md.

LA REGLA QUE HACE HONESTO TODO LO DEMAS. El candidato entrega ENTRADAS y REGLAS. Nunca resultados.
El juez calcula el desenlace de cada operacion contra los datos de mercado. Una entrada que traiga
precios de salida, P&L o resultados se RECHAZA con mensaje explicito. No es una comodidad: es lo
que hace estructuralmente imposible la censura, la seleccion de ganadoras y el sesgo de
supervivencia, en vez de dejarlas como cosas que hay que acordarse de evitar.

LAS DOS NULAS, y por que van las dos. ROTACION destruye CUANDO; SIGNO destruye QUE LADO y conserva
las ranuras de entrada. Son ataques espejo: cada una tapa lo que la otra deja abierta (un
candidato solo-largo en mercado alcista rompe la de signo; uno concentrado en un regimen rompe la
de rotacion). Se exigen las dos. Defensa contra el periodo elegido a mano: la rotacion se hace
SOLO dentro del rango de fechas del propio candidato, y se agrega un tercer punto de comparacion,
una posicion PASIVA de la misma exposicion neta promedio sobre el mismo intervalo. Si el rango es
tan corto que quedan pocas rotaciones independientes (rango / L* = 4 sesiones), es NO MEDIBLE.

EL VEREDICTO POR REGIMEN. El piso va de $3,49 a $106 por anio (factor 30). Se calcula la ventaja
por tercil de volatilidad y se EXIGE que aguante en cada uno. Si aguanta solo en alguno: APUESTA
AL REGIMEN, categoria propia, no un aprobado con asterisco. EL EJE ES EX-ANTE Y EN PUNTOS BASICOS:
la volatilidad (rango/precio) de la sesion ANTERIOR, conocible al entrar y comparable entre epocas
(juez_regimen_bps.py: piso monotono, alto/bajo 13,1x y 4,4x, contra >= 3x). La volatilidad de la
sesion ENTERA en puntos incluye lo que paso despues de entrar y conflaciona nivel de precio; ese eje
se llama hindsight, DESCRIBE el piso (juez_regimen.py) y se imprime aparte. No se juzga con el.

EL PERIODO RESERVADO. 2016-2018 es trabajo; 2019 es verificacion. El juez se NIEGA a mostrar 2019
hasta que el resultado de 2016-2018 este anotado en el registro. Es pre-registro real y
verificable, y no toca la caja sellada.

EL AGUJERO MAYOR, escrito en el veredicto y no en un comentario: el juez no puede ver la busqueda
que ocurrio antes de que el candidato llegue. Se exige declarar cuantas variantes se probaron
afuera. Es inverificable; convierte el silencio en mentira explicita, y el umbral se ajusta a esa
declaracion. El veredicto dice en su cara: "este numero supone que se probaron N variantes; si
fueron mas, no vale".

EL CONTADOR: registro encadenado con hash (detecta borrado y edicion), huella de familia a tres
tamanos de cubeta (media hora, cuatro horas, una sesion) para que no se esquive con esperas.
Defiende contra el descuido, no contra alguien motivado. Agujero conocido y marcado.

LA CAJA SELLADA: negativa por defecto. Solo con bandera explicita mas pre-registro COMMITEADO en
git antes de la corrida (verificable con git log). Nada intermedio: la falsa seguridad es peor que
ninguna.

Procedencia de las constantes: comisiones de help.tradeify.co (2026-09-03), deslizamiento del stop
de media_exceso.py, sesgo de contabilidad de sesgo_marco.py (o = 0,0642 pt, +-7,6%), plazo de
agrupamiento L* de bloques.py, cruce del vehiculo de vehiculo_ventaja.py, error de permutacion
validado en permutacion.py (+-33% con ~5.000 operaciones).
"""
import hashlib
import json
import math
import os
import subprocess
import sys
from datetime import datetime, timezone

import numpy as np
import pandas as pd

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
REGISTRO_DEFECTO = os.path.join(AQUI, "REGISTRO_JUEZ.jsonl")

# --- constantes MEDIDAS, con procedencia ------------------------------------------------
COMISION = {"ES": 5.76, "MES": 1.82}            # ida y vuelta por contrato, help.tradeify.co
PUNTO = {"ES": 50.0, "MES": 5.0}
MICROS_POR_CONTRATO = {"ES": 10, "MES": 1}
EXCESO_STOP = {10: 0.722, 20: 0.982}            # media_exceso.py, media del exceso en el stop
O_SOBREPASO = 0.0642                            # sesgo_marco.py
O_ERROR_REL = 0.076                             # +-7,6% entre corridas
SPAN_CARACTERIZADO = (20.0, 35.0)               # (T+S) donde el sesgo esta medido
P_CARACTERIZADO = (0.15, 0.85)                  # S/(S+T) donde el sesgo esta medido
CAJA = ("2020-01-02", "2026-08-19")             # no se toca sin bandera y pre-registro commiteado
TRABAJO_HASTA = 2018                            # trabajo 2016-2018, verificacion 2019
NPERM = 200
Z_BASE = 3.0                                    # desvios exigidos con UNA variante probada
Z_POTENCIA = 2.4865                             # alfa 0,05 una cola + potencia 80%
N_MIN_OP = 200
L_ESTRELLA_SES = 4                              # bloques.py: L* = 5.520 barras = 4 sesiones
ROT_INDEP_MIN = 15                              # rotaciones independientes minimas
SES_MIN_TERCIL = 20                             # sesiones minimas por tercil para verificar
Z_TERCIL = 1.5                                  # 'aguanta' en un tercil
BUCKETS = (30, 240, 1380)                       # cubetas de la huella, en barras
MINHASH_K = 128
JACCARD_FAMILIA = 0.30
CRUCE_MINI = {"comision barata": 47.70, "todo incluido": 107.14}   # vehiculo_ventaja.py, $/ses
# Resolucion de referencia (permutacion.py): la ventaja inyectada REALIZADA fue $72,69/sesion
# por mini con 4,96 op/sesion y 4.994 operaciones, y el desvio de la nula $23,73: +-33%.
REF_EDGE_OP_MINI = 72.69 / 4.96          # $ por operacion por mini
REF_RESOLUCION = 0.33
REF_N_OP = 4994
RESOLUCION_REF = f"+-{REF_RESOLUCION:.0%} de la ventaja con ~{REF_N_OP:,} operaciones (permutacion.py)"
# cadena eval x fondeada: Tradeify Growth 50K (datos_crudos.md), via vehiculo.simular
CADENA = dict(dd=2000.0, target=3000.0, trail="eod", lock_off=0.0, qual_days=5, qual_amt=150.0,
              max_eval=250, max_fund=500, cuota=83.0, pago=1350.0)

CLAVES_PROHIBIDAS = {
    "pnl", "p_and_l", "pl", "resultado", "resultados", "ganancia", "ganancias", "perdida",
    "perdidas", "retorno", "return", "returns", "profit", "profits", "equity", "balance",
    "precio_salida", "exit_price", "exitprice", "salida_precio", "precio_cierre", "gano",
    "gana", "win", "wins", "won", "loss", "outcome", "payoff", "ticks_ganados",
    "puntos_ganados", "puntos", "r_multiple", "rmultiple", "mae", "mfe", "duracion_real",
    "ts_salida", "exit_ts", "exit_time", "hora_salida", "acierto", "aciertos",
}


class Rechazo(Exception):
    pass


class NoMedible(Exception):
    pass


# =========================================================================================
# 1. La puerta
# =========================================================================================
def revisar_entrada(obj, ruta="candidato"):
    """Recorre el JSON entero. Se rechaza por CLAVE: si el nombre suena a desenlace, no entra."""
    if isinstance(obj, dict):
        for k, v in obj.items():
            kn = str(k).strip().lower().replace("-", "_").replace(" ", "_")
            if kn in CLAVES_PROHIBIDAS:
                raise Rechazo(
                    f"ENTRADA RECHAZADA. El campo '{k}' aparece en {ruta} y es un RESULTADO.\n"
                    f"  El juez calcula los desenlaces el mismo, contra los datos de mercado. Un\n"
                    f"  candidato que trae sus propios resultados puede -sin querer o queriendo-\n"
                    f"  haber descartado las que no resolvieron, quedarse con las ganadoras o\n"
                    f"  arrastrar sesgo de supervivencia. Rechazarlo es lo unico que hace esos\n"
                    f"  tres errores IMPOSIBLES en vez de evitables.\n"
                    f"  QUE HACER: borrar el campo. Mandar SOLO instante de entrada, lado,\n"
                    f"  instrumento, contratos y la regla de salida declarada.")
            revisar_entrada(v, f"{ruta}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj[:500]):
            revisar_entrada(v, f"{ruta}[{i}]")


def validar(cand):
    revisar_entrada(cand)
    for campo in ("nombre", "instrumento", "regla_salida", "operaciones", "contratos",
                  "limite_contratos", "variantes_probadas"):
        if campo not in cand:
            extra = ""
            if campo == "variantes_probadas":
                extra = ("\n  Cuantas variantes de esta idea se probaron ANTES de traer esta. El\n"
                         "  juez no puede verlo; por eso se DECLARA. Es inverificable, y por eso\n"
                         "  el silencio no se acepta: el umbral se ajusta al numero declarado y\n"
                         "  el veredicto lo dice en su cara. Declarar 1 si es la primera.")
            if campo == "limite_contratos":
                extra = "\n  El limite de contratos simultaneos de la cuenta. Se verifica contra la exposicion."
            raise Rechazo(f"ENTRADA RECHAZADA. Falta el campo obligatorio '{campo}'.{extra}")
    if cand["instrumento"] not in PUNTO:
        raise Rechazo(f"ENTRADA RECHAZADA. Instrumento '{cand['instrumento']}' desconocido. "
                      f"Hay comisiones medidas solo para {sorted(PUNTO)}.")
    if int(cand["variantes_probadas"]) < 1:
        raise Rechazo("ENTRADA RECHAZADA. variantes_probadas tiene que ser >= 1.")
    if int(cand["contratos"]) < 1 or int(cand["limite_contratos"]) < 1:
        raise Rechazo("ENTRADA RECHAZADA. contratos y limite_contratos tienen que ser >= 1.")
    r = cand["regla_salida"]
    if r.get("tipo") not in ("bracket", "tiempo"):
        raise Rechazo("ENTRADA RECHAZADA. regla_salida.tipo debe ser 'bracket' o 'tiempo'. "
                      "La regla de salida se DECLARA; el juez no la adivina.")
    if r["tipo"] == "bracket" and not ("objetivo_pt" in r and "stop_pt" in r):
        raise Rechazo("ENTRADA RECHAZADA. Un bracket necesita objetivo_pt y stop_pt.")
    if r["tipo"] == "tiempo" and "n_barras" not in r:
        raise Rechazo("ENTRADA RECHAZADA. Una regla de tiempo necesita n_barras.")
    if not cand["operaciones"]:
        raise Rechazo("ENTRADA RECHAZADA. No hay operaciones.")
    for i, op in enumerate(cand["operaciones"]):
        if "ts" not in op or "lado" not in op:
            raise Rechazo(f"ENTRADA RECHAZADA. La operacion {i} necesita 'ts' y 'lado'.")
        if op["lado"] not in ("largo", "corto"):
            raise Rechazo(f"ENTRADA RECHAZADA. lado '{op['lado']}' no es 'largo' ni 'corto'.")
    return cand


def hash_candidato(cand):
    nucleo = dict(instrumento=cand["instrumento"], contratos=int(cand["contratos"]),
                  regla_salida=cand["regla_salida"],
                  operaciones=sorted((str(o["ts"]), o["lado"]) for o in cand["operaciones"]))
    return hashlib.sha256(json.dumps(nucleo, sort_keys=True).encode()).hexdigest()


# =========================================================================================
# 2. Mercado y resolucion
# =========================================================================================
def cargar_mercado():
    from razon_escalas import cargar_con_sesion
    df = cargar_con_sesion()
    ts = pd.to_datetime(df["ts_event_utc"])
    ts = (ts.dt.tz_localize(None) if ts.dt.tz is not None else ts).to_numpy()
    sess = df["sess"].to_numpy()
    anio = df["sess"].dt.year.to_numpy()
    corte = np.flatnonzero(sess[1:] != sess[:-1]) + 1
    ini = np.concatenate(([0], corte)); fin = np.concatenate((corte, [len(df)]))
    n = len(df)
    fin_de = np.empty(n, np.int64); ses_de = np.empty(n, np.int64)
    for k, (a, b) in enumerate(zip(ini, fin)):
        fin_de[a:b] = b; ses_de[a:b] = k
    hi = df["high"].to_numpy(float); lo = df["low"].to_numpy(float)
    clo = df["close"].to_numpy(float)
    rango = hi - lo
    vol_pt = np.array([rango[a:b].mean() for a, b in zip(ini, fin)])
    px_ses = np.array([clo[a:b].mean() for a, b in zip(ini, fin)])
    vol_bps = vol_pt / px_ses * 1e4              # rango medio de barra / precio: viaja entre epocas
    # DOS EJES CON NOMBRES DISTINTOS, para que nadie los confunda dentro de seis meses:
    #   tercil_hindsight - la sesion ENTERA en PUNTOS. Incluye lo que paso despues de cada entrada.
    #                      Sirve para DESCRIBIR el piso (juez_regimen.py). NO se juzga con esto.
    #   tercil_exante    - la volatilidad de la sesion ANTERIOR en PUNTOS BASICOS (rango/precio),
    #                      conocible al entrar. Con esto se JUZGA. El bps es la unidad que viaja
    #                      entre epocas: un bracket de 20pt es 1,1% del precio en 2016 y 0,26% en
    #                      2026, no es el mismo instrumento; en puntos el eje conflaciona nivel de
    #                      precio con volatilidad. Verificado en juez_regimen_bps.py: el factor
    #                      se sostiene, alto/bajo 13,1x (5pt:20pt) y 4,4x (20pt:10pt), contra >= 3x,
    #                      y solo 23% de las sesiones cambian de etiqueta contra el eje en puntos.
    q33, q66 = np.quantile(vol_pt, [1 / 3, 2 / 3])
    tercil_hind = np.where(vol_pt <= q33, 0, np.where(vol_pt <= q66, 1, 2))
    prev_bps = np.concatenate([[np.nan], vol_bps[:-1]])
    p33, p66 = np.nanquantile(prev_bps, [1 / 3, 2 / 3])
    tercil_ex = np.where(np.isnan(prev_bps), -1,
                         np.where(prev_bps <= p33, 0, np.where(prev_bps <= p66, 1, 2)))
    return dict(cl=clo, hi=hi, lo=lo, ts=ts, fin_de=fin_de,
                ses_de=ses_de, ini=ini, fin=fin, nses=len(ini), n=n, anio_ses=anio[ini],
                tercil_exante=tercil_ex, tercil_hindsight=tercil_hind,
                cortes_exante_bps=(float(p33), float(p66)), cortes_hindsight_pt=(float(q33), float(q66)))


def resolver(m, idx, sgn, regla, exceso):
    """Resuelve un LOTE de operaciones, vectorizado. Nada se descarta: lo que sigue abierto al
    corte de sesion se marca a mercado. Devuelve (puntos por operacion, barras hasta la salida).
    La barra ambigua (objetivo y stop en la misma barra de un minuto) se cuenta PERDIDA."""
    cl, hi, lo, fin_de = m["cl"], m["hi"], m["lo"], m["fin_de"]
    ent = cl[idx]; fin = fin_de[idx]
    dur_max = np.maximum(fin - idx - 1, 0)
    if regla["tipo"] == "tiempo":
        j = np.minimum(idx + int(regla["n_barras"]), fin - 1)
        return sgn * (cl[j] - ent), (j - idx)
    T, S = float(regla["objetivo_pt"]), float(regla["stop_pt"])
    n = len(idx)
    pt = np.empty(n); ten = np.empty(n, np.int64)
    for i in range(n):
        a = int(idx[i]); b = int(fin[i]); e = ent[i]; s = sgn[i]
        h, l = hi[a + 1:b], lo[a + 1:b]
        if s > 0:
            to, ts_ = h >= e + T, l <= e - S
        else:
            to, ts_ = l <= e - T, h >= e + S
        algo = to | ts_
        if algo.any():
            j = int(np.argmax(algo))
            pt[i] = T if (to[j] and not ts_[j]) else -(S + exceso)   # ambigua = perdida
            ten[i] = j + 1
        else:
            pt[i] = s * (cl[b - 1] - e); ten[i] = dur_max[i]
    return pt, ten


# =========================================================================================
# 3. Registro encadenado y huella de familia
# =========================================================================================
def minhash(idx, bucket, k=MINHASH_K, semilla=20260904):
    cubetas = np.unique(np.asarray(idx) // bucket).astype(np.int64)
    rs = np.random.default_rng(semilla)
    a = rs.integers(1, 2 ** 31 - 1, k).astype(np.int64)
    b = rs.integers(0, 2 ** 31 - 1, k).astype(np.int64)
    P = np.int64((1 << 31) - 1)
    h = (a[:, None] * (cubetas[None, :] % P) + b[:, None]) % P
    return h.min(axis=1).astype(int).tolist()


def jaccard(s1, s2):
    a, b = np.array(s1), np.array(s2)
    return float((a == b).mean()) if len(a) == len(b) and len(a) else 0.0


def _hash_fila(fila_sin_hash, prev):
    return hashlib.sha256((prev + json.dumps(fila_sin_hash, sort_keys=True,
                                             ensure_ascii=False)).encode()).hexdigest()


def leer_registro(ruta):
    """Devuelve (filas, cadena_ok, primera_rota). Verifica el encadenado en cada lectura."""
    if not os.path.exists(ruta):
        return [], True, None
    filas, prev, ok, rota = [], "genesis", True, None
    with open(ruta, encoding="utf-8") as f:
        for num, ln in enumerate(f, 1):
            ln = ln.strip()
            if not ln:
                continue
            try:
                fila = json.loads(ln)
            except json.JSONDecodeError:
                ok, rota = False, rota or num
                continue
            h = fila.get("hash"); sin = {k: v for k, v in fila.items() if k != "hash"}
            if fila.get("prev_hash") != prev or _hash_fila(sin, prev) != h:
                ok, rota = False, rota or num
            prev = h or prev
            filas.append(fila)
    return filas, ok, rota


def anotar(ruta, fila):
    filas, _, _ = leer_registro(ruta)
    prev = filas[-1]["hash"] if filas else "genesis"
    fila = dict(fila); fila["prev_hash"] = prev
    fila["hash"] = _hash_fila(fila, prev)
    with open(ruta, "a", encoding="utf-8") as f:
        f.write(json.dumps(fila, ensure_ascii=False) + "\n")
    return fila


def prerregistro_commiteado(ruta):
    """Verificable o nada: el archivo tiene que estar COMMITEADO en git, sin cambios locales, con
    fecha de commit anterior a ahora. Devuelve (ok, motivo)."""
    if not ruta or not os.path.exists(ruta):
        return False, "el archivo de pre-registro no existe"
    try:
        raiz = subprocess.run(["git", "rev-parse", "--show-toplevel"], capture_output=True,
                              text=True, cwd=os.path.dirname(os.path.abspath(ruta))).stdout.strip()
        fecha = subprocess.run(["git", "log", "-1", "--format=%cI", "--", ruta],
                               capture_output=True, text=True, cwd=raiz).stdout.strip()
        sucio = subprocess.run(["git", "status", "--porcelain", "--", ruta],
                               capture_output=True, text=True, cwd=raiz).stdout.strip()
    except (OSError, FileNotFoundError):
        return False, "git no disponible: no se puede verificar"
    if not fecha:
        return False, "el pre-registro NO esta commiteado en git"
    if sucio:
        return False, "el pre-registro tiene cambios locales sin commitear"
    if datetime.fromisoformat(fecha) >= datetime.now(timezone.utc):
        return False, "la fecha de commit no es anterior a la corrida"
    return True, f"commiteado {fecha}"


# =========================================================================================
# 4. Estadistica auxiliar
# =========================================================================================
def sf_normal(z):
    return 0.5 * math.erfc(z / math.sqrt(2.0))


def z_requerido(variantes):
    """Umbral en desvios que deja la tasa de falso positivo de Z_BASE repartida entre las
    variantes probadas (Bonferroni sobre la cola)."""
    objetivo = sf_normal(Z_BASE) / max(1, int(variantes))
    lo, hi = 0.0, 12.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if sf_normal(mid) > objetivo:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# =========================================================================================
# 5. El juicio de UN periodo
# =========================================================================================
def juzgar_periodo(cand, m, idx, sgn, etiqueta, npermuta=NPERM, rotacion_global=False):
    """Juzga las operaciones (idx, sgn) que caen en un periodo. Devuelve el diccionario del
    veredicto. rotacion_global=True quita la defensa del rango (SOLO para el control que
    demuestra que la defensa hace falta; nunca para juzgar)."""
    inst = cand["instrumento"]; contratos = int(cand["contratos"])
    punto = PUNTO[inst]; c1 = COMISION[inst] * contratos
    regla = cand["regla_salida"]
    avisos, no_cubre = [], []
    if len(idx) < N_MIN_OP:
        raise NoMedible(f"[{etiqueta}] {len(idx):,} operaciones. El juez exige al menos "
                        f"{N_MIN_OP} para que el error de permutacion signifique algo. "
                        f"Con menos, cualquier numero seria ruido con cara de veredicto.")

    # --- bracket caracterizado, sesgo y su error (correccion SOLO conservadora) ------------
    if regla["tipo"] == "bracket":
        T, S = float(regla["objetivo_pt"]), float(regla["stop_pt"])
        span, p = T + S, S / (S + T)
        if not (SPAN_CARACTERIZADO[0] <= span <= SPAN_CARACTERIZADO[1]):
            raise NoMedible(f"El bracket {T:g}pt:{S:g}pt tiene span {span:g}, fuera del rango donde "
                            f"el sesgo de contabilidad esta MEDIDO ({SPAN_CARACTERIZADO[0]:g}-"
                            f"{SPAN_CARACTERIZADO[1]:g}). El juez no extrapola una correccion.\n"
                            f"  QUE HACER: caracterizar ese span con sesgo_marco.py o usar un "
                            f"bracket del rango medido.")
        if not (P_CARACTERIZADO[0] <= p <= P_CARACTERIZADO[1]):
            raise NoMedible(f"El bracket da p = S/(S+T) = {p:.3f}, fuera de {P_CARACTERIZADO}. "
                            f"Mismo motivo que el span.")
        exceso = EXCESO_STOP.get(int(round(S)))
        if exceso is None:
            ks = sorted(EXCESO_STOP); kk = min(ks, key=lambda k: abs(k - S))
            exceso = EXCESO_STOP[kk]
            avisos.append(f"Deslizamiento del stop no medido para {S:g}pt; se usa el de {kk}pt = "
                          f"{exceso}. Sustitucion, no medicion.")
        # sesgo por operacion en puntos: verdad = replay - o*(1-2p). Se aplica SOLO en la
        # direccion conservadora: si la correccion ayuda al candidato, va con el o mas chico;
        # si lo perjudica, con el mas grande. Nadie cobra la correccion eligiendo el bracket.
        signo_corr = (1 - 2 * p)
        o_cons = O_SOBREPASO * (1 + O_ERROR_REL) if signo_corr > 0 else O_SOBREPASO * (1 - O_ERROR_REL)
        sesgo_pt = o_cons * signo_corr
        error_o_pt = O_SOBREPASO * O_ERROR_REL * abs(signo_corr)
    else:
        exceso, sesgo_pt, error_o_pt, p = 0.0, 0.0, 0.0, None
        avisos.append("Regla de TIEMPO: no hay barrera, asi que no hay sobrepaso ni deslizamiento "
                      "de stop que restar.")

    def dolares(pts):
        return (pts - sesgo_pt) * punto * contratos - c1

    # --- rango, sesiones, rotaciones independientes ----------------------------------------
    lo_b, hi_b = int(idx.min()), int(m["fin_de"][idx.max()] - 1)
    ses_lo, ses_hi = int(m["ses_de"][lo_b]), int(m["ses_de"][hi_b])
    ses_rango = np.arange(ses_lo, ses_hi + 1)
    n_ses = len(ses_rango)
    L = hi_b - lo_b + 1
    rot_indep = n_ses / L_ESTRELLA_SES
    if rot_indep < ROT_INDEP_MIN and not rotacion_global:
        raise NoMedible(f"[{etiqueta}] Tu ventana es demasiado angosta para tener nula: "
                        f"{n_ses} sesiones = {rot_indep:.1f} rotaciones independientes "
                        f"(L* = {L_ESTRELLA_SES} sesiones); hacen falta >= {ROT_INDEP_MIN}, "
                        f"o sea >= {ROT_INDEP_MIN * L_ESTRELLA_SES} sesiones de rango.")

    # --- observado y exposicion maxima -----------------------------------------------------
    # Los DOS lados se resuelven una vez en cada ranura: el observado y la nula de signo son
    # selecciones sobre esa tabla (la nula de signo conserva las ranuras exactas).
    ptsL, tenL = resolver(m, idx, np.ones(len(idx)), regla, exceso)
    ptsS, tenS = resolver(m, idx, -np.ones(len(idx)), regla, exceso)
    largo = sgn > 0
    pts = np.where(largo, ptsL, ptsS); ten = np.where(largo, tenL, tenS)
    dol = dolares(pts)
    v_obs = np.bincount(m["ses_de"][idx] - ses_lo, weights=dol, minlength=n_ses)
    obs = float(v_obs.mean()); op_ses = len(idx) / n_ses
    # A5: exposicion simultanea contra el limite declarado
    ev_t = np.concatenate([idx, idx + ten]); ev_v = np.concatenate([np.full(len(idx), contratos),
                                                                   np.full(len(idx), -contratos)])
    orden = np.lexsort((ev_v, ev_t))            # a igual barra, primero las salidas
    expo_max = int(np.cumsum(ev_v[orden]).max())
    if expo_max > int(cand["limite_contratos"]):
        raise Rechazo(f"ENTRADA RECHAZADA. La exposicion simultanea maxima es {expo_max} contratos "
                      f"y el limite declarado es {cand['limite_contratos']}. Con {contratos} por "
                      f"operacion y la tenencia que dan los datos, las posiciones se apilan. El "
                      f"conteo de operaciones y el consejo de 'cuantas faltan' serian falsos.")

    # --- nula A: rotacion dentro del rango del candidato ------------------------------------
    rp = np.random.default_rng(20260904)
    medA = np.empty(npermuta)
    for i in range(npermuta):
        if rotacion_global:
            k = int(rp.integers(1, m["n"])); i2 = (idx + k) % m["n"]
            lo2 = int(m["ses_de"][i2.min()]); v2 = np.bincount(m["ses_de"][i2] - lo2, weights=dolares(
                resolver(m, i2, sgn, regla, exceso)[0]), minlength=int(m["ses_de"][i2.max()]) - lo2 + 1)
            medA[i] = v2.mean()
        else:
            k = int(rp.integers(1, L)); i2 = lo_b + ((idx - lo_b + k) % L)
            v2 = np.bincount(m["ses_de"][i2] - ses_lo, weights=dolares(
                resolver(m, i2, sgn, regla, exceso)[0]), minlength=n_ses)
            medA[i] = v2.mean()
    # --- nula B: signo; se guardan los vectores por sesion para el regimen -----------------
    VB = np.empty((npermuta, n_ses))
    ses_rel = m["ses_de"][idx] - ses_lo
    dL, dS = dolares(ptsL), dolares(ptsS)
    for i in range(npermuta):
        flip = rp.random(len(sgn)) < 0.5
        d2 = np.where(largo ^ flip, dL, dS)
        VB[i] = np.bincount(ses_rel, weights=d2, minlength=n_ses)
    medB = VB.mean(axis=1)
    nulas = {"A rotacion": (float(medA.mean()), float(medA.std(ddof=1))),
             "B signo": (float(medB.mean()), float(medB.std(ddof=1)))}
    # --- tercer punto: posicion pasiva de la misma exposicion neta promedio -----------------
    expo_prom = float((sgn * contratos * ten).sum() / L)
    pasiva = expo_prom * (m["cl"][hi_b] - m["cl"][lo_b]) * punto / n_ses

    # --- errores: permutacion (nunca binomial), mas el error de o propagado ------------------
    sd_perm = max(nulas["A rotacion"][1], nulas["B signo"][1])
    err_o_ses = error_o_pt * punto * contratos * op_ses
    sd_tot = math.sqrt(sd_perm ** 2 + err_o_ses ** 2)
    sd_binom = float(v_obs.std(ddof=1) / np.sqrt(n_ses))
    ganado = sd_perm / sd_binom if sd_binom else float("nan")
    mde = Z_POTENCIA * sd_tot
    # resolucion contra la ventaja de REFERENCIA (la inyectada y recuperada en permutacion.py),
    # escalada a este candidato por sus operaciones por sesion, su punto y sus contratos
    ref_edge_ses = REF_EDGE_OP_MINI * op_ses * (punto / 50.0) * contratos
    rel = sd_tot / ref_edge_ses if ref_edge_ses else float("inf")
    resolucion = (f"+-{rel:.0%} de la ventaja de referencia (+-${sd_tot:.2f}/sesion contra "
                  f"${ref_edge_ses:.2f}; MDE ${mde:.2f}); referencia {RESOLUCION_REF}")

    # --- se puede resolver algo con este n? -------------------------------------------------
    # NO MEDIBLE cuando el error supera a la ventaja de referencia entera: ni una ventaja del
    # tamano de la que se recupero al 100% se veria a un desvio. Calibrado contra lo publicado:
    # con ~5.000 operaciones la resolucion es +-33% y el veredicto SE DA.
    pisoB = -nulas["B signo"][0]
    z_rent = obs / sd_tot if sd_tot else 0.0
    if rel > 1.0:
        falta = int(math.ceil(len(idx) * (rel / REF_RESOLUCION) ** 2))
        raise NoMedible(f"[{etiqueta}] Con {len(idx):,} operaciones el error es ${sd_tot:.2f} por "
                        f"sesion: +-{rel:.0%} de la ventaja de referencia (${ref_edge_ses:.2f}). "
                        f"Ni una ventaja del tamano de la que el instrumento recupero al 100% se "
                        f"veria a un desvio.\n  HARIAN FALTA del orden de {falta:,} operaciones "
                        f"para llegar a la resolucion de referencia (+-{REF_RESOLUCION:.0%}).")

    # --- veredicto global: rentable, informativo (dos nulas + pasiva), con multiplicidad ---
    filas = {}
    for et, (mu, sd) in nulas.items():
        vent = obs - mu
        filas[et] = (mu, sd, vent, vent / sd_tot if sd_tot else 0.0)
    z_pas = (obs - pasiva) / sd_tot if sd_tot else 0.0
    z_info = min(filas["A rotacion"][3], filas["B signo"][3], z_pas)
    return dict(etiqueta=etiqueta, obs=obs, v_obs=v_obs, VB=VB, nulas=filas, pasiva=pasiva,
                z_pas=z_pas, z_rent=z_rent, z_info=z_info, sd_perm=sd_perm, sd_tot=sd_tot,
                err_o_ses=err_o_ses, sd_binom=sd_binom, ganado=ganado, mde=mde, pisoB=pisoB,
                resolucion=resolucion, n_op=len(idx), op_ses=op_ses, n_ses=n_ses,
                ses_lo=ses_lo, ses_hi=ses_hi, rot_indep=rot_indep, expo_max=expo_max,
                sesgo_pt=sesgo_pt, p=p, avisos=avisos, no_cubre=no_cubre, pts=pts, idx=idx,
                sgn=sgn, ten=ten, exceso=exceso, punto=punto, contratos=contratos, c1=c1)


def regimen(r, m, eje="tercil_exante"):
    """Ventaja por tercil de volatilidad con la nula B (conserva la sesion exacta).
    eje='tercil_exante' (sesion anterior) es el que JUZGA; eje='tercil_hindsight' (sesion
    entera) solo DESCRIBE y se imprime aparte con ese nombre."""
    ses = np.arange(r["ses_lo"], r["ses_hi"] + 1)
    terc = m[eje][ses]
    out = []
    for t, nom in ((0, "bajo"), (1, "medio"), (2, "alto")):
        mk = terc == t
        n = int(mk.sum())
        if n < SES_MIN_TERCIL:
            out.append(dict(nombre=nom, n=n, verificable=False)); continue
        o = float(r["v_obs"][mk].mean())
        nb = r["VB"][:, mk].mean(axis=1)
        mu, sd = float(nb.mean()), float(nb.std(ddof=1))
        z = (o - mu) / sd if sd else 0.0
        out.append(dict(nombre=nom, n=n, verificable=True, obs=o, nula=mu, sd=sd,
                        ventaja=o - mu, z=z, aguanta=(o - mu > 0 and z >= Z_TERCIL)))
    return out


def cadena_pasar(r, m):
    """P(pasar) por la cadena eval x fondeada de Tradeify Growth 50K, con el flujo del
    candidato. Arranque en cada sesion del rango; el intento no puede salir del rango."""
    from vehiculo import matriz, simular
    inst_micros = MICROS_POR_CONTRATO["ES"] if r["punto"] == 50.0 else 1
    N = inst_micros * r["contratos"]
    rep = dict(ses=m["ses_de"][r["idx"]] - r["ses_lo"], pts=r["pts"] - r["sesgo_pt"],
               ab=np.zeros(len(r["idx"]), int))
    M = matriz(rep, r["n_ses"])
    s0 = np.arange(r["n_ses"])
    c_rt = (COMISION["ES"] * (N // 10) + COMISION["MES"] * (N % 10))
    res, used, _ = simular(M, s0, N, c_rt, CADENA["dd"], CADENA["target"], CADENA["trail"],
                           CADENA["lock_off"], CADENA["qual_days"], CADENA["qual_amt"],
                           CADENA["max_eval"], CADENA["max_fund"], cap=r["n_ses"] - s0)
    return dict(p_pasa=float(np.isin(res, (1, 2, 4)).mean()), p_pago=float((res == 2).mean()),
                p_tiempo=float(np.isin(res, (3, 4)).mean()), e_ses=float(used.mean()),
                E=float((-CADENA["cuota"] + (res == 2) * CADENA["pago"]).mean()), N=N)


def veredicto_de(r, reg, variantes_total):
    z_req = z_requerido(variantes_total)
    rentable = r["obs"] > 0 and r["z_rent"] >= z_req
    informativo = r["z_info"] >= z_req
    verificables = [t for t in reg if t["verificable"]]
    aguantan = [t for t in verificables if t["aguanta"]]
    todos = len(verificables) == 3 and len(aguantan) == 3
    if rentable and informativo and todos:
        v = "SUPERA"
    elif rentable and informativo:
        v = "APUESTA AL REGIMEN"
    else:
        v = "NO SUPERA"
    return v, z_req, rentable, informativo


# =========================================================================================
# 6. El juicio completo: puerta, caja, periodos, registro
# =========================================================================================
def juzgar(cand, m, permitir_caja=False, prerregistro=None, verificar=False, npermuta=NPERM,
           registro=REGISTRO_DEFECTO, anotar_=True, rotacion_global=False):
    validar(cand)
    hc = hash_candidato(cand)
    tss = pd.to_datetime([o["ts"] for o in cand["operaciones"]])
    tss = tss.tz_localize(None) if tss.tz is not None else tss
    salida = dict(nombre=cand["nombre"], hash=hc[:16], avisos=[], no_cubre=[], periodos={})

    # --- la caja sellada ----------------------------------------------------------------------
    en_caja = int(((tss >= pd.Timestamp(CAJA[0])) & (tss <= pd.Timestamp(CAJA[1]))).sum())
    if en_caja:
        if not permitir_caja:
            raise Rechazo(f"RECHAZADO POR LA CAJA SELLADA. {en_caja:,} de {len(tss):,} operaciones "
                          f"caen en {CAJA[0]} .. {CAJA[1]}.\n  Esa caja se usa UNA vez. El juez se "
                          f"niega por defecto: una herramienta facil de correr es facil de quemar "
                          f"sin querer.\n  QUE HACER: correr fuera de la caja, o pasar --caja JUNTO "
                          f"CON --prerregistro <archivo> ya COMMITEADO en git antes de la corrida.")
        ok, motivo = prerregistro_commiteado(prerregistro)
        if not ok:
            raise Rechazo(f"RECHAZADO. --caja exige un pre-registro VERIFICABLE: {motivo}.\n"
                          f"  O esta commiteado antes, o no vale. Nada intermedio.")
        raise NoMedible(f"Pre-registro verificado ({motivo}), pero este juez solo carga ES 1-min "
                        f"2016-2019. Abrir la caja (diario 2020-2026) es OTRA corrida, con OTRO "
                        f"replicador, y no esta implementada aca a proposito.")

    # --- mapear a barras ----------------------------------------------------------------------
    orden = np.argsort(m["ts"])
    pos = np.searchsorted(m["ts"][orden], tss.to_numpy())
    dentro = pos < len(orden)
    idx = np.where(dentro, orden[np.clip(pos, 0, len(orden) - 1)], -1)
    exacto = dentro & (np.abs((m["ts"][np.clip(idx, 0, m["n"] - 1)] - tss.to_numpy())
                              .astype("timedelta64[s]").astype(float)) <= 60.0)
    fuera = int((~exacto).sum())
    if fuera:
        rango = f"{pd.Timestamp(m['ts'].min()).date()} .. {pd.Timestamp(m['ts'].max()).date()}"
        raise NoMedible(f"{fuera:,} de {len(tss):,} operaciones caen FUERA de la ventana de datos "
                        f"({rango}) o no coinciden con ninguna barra. El juez no interpola ni "
                        f"redondea: si no hay dato, no hay veredicto.")
    sgn_all = np.array([1.0 if o["lado"] == "largo" else -1.0 for o in cand["operaciones"]])
    anio_op = m["anio_ses"][m["ses_de"][idx]]

    # --- registro: cadena, familia, variantes -------------------------------------------------
    previos, cadena_ok, rota = leer_registro(registro)
    if not cadena_ok:
        salida["avisos"].append(f"REGISTRO ALTERADO: la cadena de hash se rompe en la linea {rota}. "
                                f"Alguien borro o edito. El contador de esta corrida no es confiable.")
    firmas = {f"firma_{b}": minhash(idx, b) for b in BUCKETS}
    fam_decl = cand.get("familia")
    hermanos = []
    for f in previos:
        if f.get("hash_candidato") == hc:
            continue                       # el mismo candidato (otro periodo) no es un hermano
        misma = bool(fam_decl and f.get("familia_declarada") == fam_decl)
        js = {b: jaccard(firmas[f"firma_{b}"], f.get(f"firma_{b}", [])) for b in BUCKETS}
        jmax = max(js.values())
        if misma or jmax >= JACCARD_FAMILIA:
            hermanos.append((f, jmax, "declarada" if misma else
                             f"huella {jmax:.0%} a {max(js, key=js.get)} barras"))
    variantes = int(cand["variantes_probadas"])
    variantes_total = variantes + len(hermanos)
    salida.update(hermanos=hermanos, variantes=variantes, variantes_total=variantes_total,
                  familia_declarada=fam_decl, cadena_ok=cadena_ok)

    # --- periodo de trabajo -------------------------------------------------------------------
    mk_t = anio_op <= TRABAJO_HASTA
    if mk_t.sum() == 0:
        raise NoMedible("El candidato no tiene operaciones en el periodo de TRABAJO (2016-2018). "
                        "Sin resultado de trabajo anotado no se muestra el de verificacion (2019).")
    r = juzgar_periodo(cand, m, idx[mk_t], sgn_all[mk_t], "TRABAJO 2016-2018", npermuta,
                       rotacion_global)
    reg = regimen(r, m)
    v, z_req, rent, info = veredicto_de(r, reg, variantes_total)
    r.update(veredicto=v, z_req=z_req, rentable=rent, informativo=info, regimen=reg,
             regimen_hindsight=regimen(r, m, "tercil_hindsight"), cadena=cadena_pasar(r, m))
    salida["periodos"]["trabajo"] = r
    if anotar_:
        anotar(registro, dict(cuando=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                              nombre=cand["nombre"], hash_candidato=hc, periodo="trabajo",
                              veredicto=v, obs=round(r["obs"], 4),
                              ventaja_B=round(r["nulas"]["B signo"][2], 4),
                              z_info=round(r["z_info"], 3), z_rent=round(r["z_rent"], 3),
                              n_op=r["n_op"], variantes_declaradas=variantes,
                              familia_declarada=fam_decl, instrumento=cand["instrumento"],
                              regla=cand["regla_salida"], **firmas))

    # --- periodo reservado --------------------------------------------------------------------
    mk_v = ~mk_t
    ya_anotado = any(f.get("hash_candidato") == hc and f.get("periodo") == "trabajo" for f in previos)
    if mk_v.sum() == 0:
        salida["verificacion"] = "sin operaciones en 2019"
    elif not verificar:
        salida["verificacion"] = (f"RETENIDO: {int(mk_v.sum()):,} operaciones de 2019 NO se juzgan. "
                                  f"El resultado de trabajo ya quedo anotado en el registro; volve a "
                                  f"correr con --verificar para ver 2019.")
    elif not ya_anotado:
        salida["verificacion"] = ("RETENIDO: --verificar exige que el resultado de TRABAJO de este "
                                  "mismo candidato ya estuviera anotado ANTES de esta corrida. Recien "
                                  "quedo anotado ahora; la proxima corrida con --verificar lo muestra.")
    else:
        try:
            rv = juzgar_periodo(cand, m, idx[mk_v], sgn_all[mk_v], "VERIFICACION 2019", npermuta,
                                rotacion_global)
            regv = regimen(rv, m)
            vv, zq, rn, inf = veredicto_de(rv, regv, variantes_total)
            rv.update(veredicto=vv, z_req=zq, rentable=rn, informativo=inf, regimen=regv,
                      regimen_hindsight=regimen(rv, m, "tercil_hindsight"),
                      cadena=cadena_pasar(rv, m))
            salida["periodos"]["verificacion"] = rv
            salida["verificacion"] = f"MOSTRADO: {vv}"
            if anotar_:
                anotar(registro, dict(cuando=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                      nombre=cand["nombre"], hash_candidato=hc,
                                      periodo="verificacion", veredicto=vv,
                                      obs=round(rv["obs"], 4), z_info=round(rv["z_info"], 3),
                                      n_op=rv["n_op"], **firmas))
        except NoMedible as e:
            salida["verificacion"] = f"NO MEDIBLE en 2019: {e}"
    return salida


# =========================================================================================
# 7. El informe
# =========================================================================================
def _bloque_periodo(A, r, s):
    A(f"   {'':<28}{'$/sesion':>11}")
    A(f"   {'OBSERVADO (neto)':<28}{r['obs']:>+11.2f}")
    for et, (mu, sd, vent, z) in r["nulas"].items():
        A(f"   {'nula ' + et:<28}{mu:>+11.2f}   desvio {sd:>7.2f}   ventaja {vent:>+8.2f} = {z:>+5.1f} desvios")
    A(f"   {'PASIVA misma exposicion':<28}{r['pasiva']:>+11.2f}   {'':>15}ventaja {r['obs']-r['pasiva']:>+8.2f} = {r['z_pas']:>+5.1f} desvios")
    A("")
    A(f"   ERROR: permutacion ${r['sd_perm']:.2f} (+) error de o propagado ${r['err_o_ses']:.2f} = ${r['sd_tot']:.2f}. "
      f"NUNCA binomial (daria ${r['sd_binom']:.2f}; factor ganado {r['ganado']:.1f}x).")
    A(f"   RESOLUCION: {r['resolucion']}. 'No detecto nada' NO es 'no hay nada'.")
    A(f"   correccion de contabilidad aplicada solo en direccion conservadora: {r['sesgo_pt']:+.4f} pt/op")
    A("")
    A(f"   RENTABLE (dolares > 0):                  {r['z_rent']:+.1f} desvios contra {r['z_req']:.2f} exigidos   {'SI' if r['rentable'] else 'no'}")
    A(f"   INFORMATIVO (bate rotacion, signo y pasiva): {r['z_info']:+.1f} desvios contra {r['z_req']:.2f} exigidos   {'SI' if r['informativo'] else 'no'}")
    A("")
    A(f"   POR REGIMEN, EJE EX-ANTE (tercil de volatilidad EN BPS -rango/precio- de la sesion ANTERIOR,")
    A(f"   conocible al entrar y comparable entre epocas; nula de signo, que conserva la sesion). Con esto se JUZGA:")
    A(f"   {'tercil':>8}{'sesiones':>10}{'obs':>10}{'nula':>10}{'ventaja':>10}{'desvios':>9}{'aguanta':>9}")
    for t in r["regimen"]:
        if not t["verificable"]:
            A(f"   {t['nombre']:>8}{t['n']:>10}{'':>10}{'':>10}{'':>10}{'':>9}{'SIN DATOS':>9}   (< {SES_MIN_TERCIL} sesiones: no verificable)")
        else:
            A(f"   {t['nombre']:>8}{t['n']:>10}{t['obs']:>+10.2f}{t['nula']:>+10.2f}{t['ventaja']:>+10.2f}{t['z']:>+9.1f}{('SI' if t['aguanta'] else 'no'):>9}")
    partes = []
    for t in r["regimen_hindsight"]:
        if t["verificable"]:
            partes.append(f"{t['nombre']} {t['ventaja']:+.1f} ({t['z']:+.1f}sd)")
        else:
            partes.append(f"{t['nombre']} sin datos")
    A("   DESCRIPTIVO, EJE HINDSIGHT (sesion entera, incluye lo que paso despues de entrar; NO juzga): "
      + "  ".join(partes))
    c = r["cadena"]
    A("")
    A(f"   LA CADENA eval x fondeada (Tradeify Growth 50K, {c['N']} micros): P(pasa eval) {c['p_pasa']:.3f}   "
      f"P(pago) {c['p_pago']:.3f}   P(se acaba el rango) {c['p_tiempo']:.3f}   E sesiones {c['e_ses']:.0f}   E $/intento {c['E']:+.0f}")
    A(f"   (una media positiva con cola izquierda gorda fracasa igual: esto es lo que paga el producto)")
    vB = r["nulas"]["B signo"][2]
    if vB >= abs(r["pisoB"]) and r["obs"] > 0:
        f = 1.0 if r["punto"] == 50.0 else 0.1
        A("")
        A(f"   REGLA DEL VEHICULO: la ventaja medida (${vB:+.2f}/sesion) SUPERA el piso (${abs(r['pisoB']):.2f}).")
        A(f"   A esa ventaja conviene CAPITAL PROPIO y no la evaluacion: el cruce medido cae en el propio")
        A(f"   piso (+${CRUCE_MINI['comision barata']*f:.2f}/sesion con comision barata, +${CRUCE_MINI['todo incluido']*f:.2f} todo incluido; vehiculo_ventaja.py).")


def informe(s):
    L = []; A = L.append
    r = s["periodos"]["trabajo"]
    A("=" * 96)
    A(f"VEREDICTO (TRABAJO 2016-2018): {r['veredicto']}     candidato: {s['nombre']}   hash {s['hash']}")
    A("=" * 96)
    A(f"ESTE NUMERO SUPONE QUE SE PROBARON {s['variantes_total']} VARIANTES ANTES DE LLEGAR ACA "
      f"({s['variantes']} declaradas + {len(s['hermanos'])} de la misma familia en el registro).")
    A(f"SI FUERON MAS, NO VALE. El umbral se ajusto a esa cifra: {r['z_req']:.2f} desvios en vez de {Z_BASE:.1f}.")
    if s["hermanos"]:
        A("")
        A("#" * 96)
        A(f"#  ATENCION: ESTE ES EL INTENTO NUMERO {len(s['hermanos']) + 1} DE ESTA MISMA FAMILIA.")
        A(f"#  Probar variantes hasta que una pase fabrica falsos positivos. Intentos previos:")
        for f, j, como in s["hermanos"][-8:]:
            A(f"#     {f.get('cuando','?')}  {f.get('nombre','?'):<26} {f.get('veredicto','?'):<20} ({como})")
        A("#" * 96)
    A("")
    A(f"   operaciones {r['n_op']:,}   sesiones del rango {r['n_ses']:,}   {r['op_ses']:.2f} op/sesion   "
      f"rotaciones independientes {r['rot_indep']:.0f}   exposicion maxima {r['expo_max']} contratos")
    A("")
    _bloque_periodo(A, r, s)
    A("")
    A("-" * 96)
    A(f"VERIFICACION 2019: {s['verificacion']}")
    if "verificacion" in s["periodos"]:
        rv = s["periodos"]["verificacion"]
        A("-" * 96)
        A(f"VEREDICTO (VERIFICACION 2019): {rv['veredicto']}")
        A("")
        _bloque_periodo(A, rv, s)
    avisos = s["avisos"] + r["avisos"]
    if avisos:
        A("")
        A("   AVISOS:")
        for a in avisos:
            A(f"     - {a}")
    A("")
    A("=" * 96)
    A("LO QUE ESTE VEREDICTO NO CUBRE")
    A("=" * 96)
    for c in [
        f"LA BUSQUEDA ANTERIOR: el juez no puede ver cuantas variantes se probaron antes de esta. "
        f"Supone {s['variantes_total']}; si fueron mas, no vale. Es inverificable por construccion.",
        "FALSO NEGATIVO ESTRUCTURAL: un candidato cuya ventaja sea SOLO de sincronizacion (cuando "
        "entrar, no de que lado) muere contra la nula de signo. Exigir las dos nulas lo mata aunque "
        "sea real. Esta escrito para que el lector lo sepa.",
        "DESLIZAMIENTO DE ENTRADA: NO MEDIDO. Se trata como CERO. Un cuarto de tick dio vuelta el "
        "signo de una celda en esta ventana.",
        "LA REGLA DE CONSISTENCIA (35-40%) de las firmas no esta modelada. Solo puede bajar P(pago).",
        "TERRENO ES 1-min 2016-2019 unicamente. 2020+ esta en la caja sellada y no se toca.",
        "ENTRADA PASIVA: si el candidato entra con orden limite, la no-ejecucion y la seleccion "
        "adversa no estan modeladas. FIFO en ES viene de fuente secundaria.",
        "EL CONTADOR defiende contra el descuido, no contra alguien motivado: se puede correr en "
        "otra copia del repo o con otro registro. Agujero conocido.",
        "COSTO DE OPORTUNIDAD y financiamiento del capital: no modelados.",
    ]:
        A(f"   - {c}")
    A("")
    return "\n".join(L)


def main(argv):
    if len(argv) < 2:
        print("uso: python juez.py <candidato.json> [--verificar] [--caja --prerregistro <archivo>]")
        return 2
    ruta = argv[1]
    permitir = "--caja" in argv
    verificar = "--verificar" in argv
    pre = argv[argv.index("--prerregistro") + 1] if "--prerregistro" in argv else None
    cand = json.load(open(ruta, encoding="utf-8"))
    try:
        m = cargar_mercado()
        s = juzgar(cand, m, permitir_caja=permitir, prerregistro=pre, verificar=verificar)
    except Rechazo as e:
        print("=" * 96); print(e); print("=" * 96)
        return 1
    except NoMedible as e:
        print("=" * 96)
        print(f"VEREDICTO: NO MEDIBLE     candidato: {cand.get('nombre','?')}")
        print("=" * 96)
        print(f"\nMOTIVO: {e}\n")
        print("Un juez que siempre da un numero es peor que ninguno.")
        anotar(REGISTRO_DEFECTO, dict(cuando=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                      nombre=cand.get("nombre", "?"),
                                      hash_candidato=hash_candidato(cand) if "operaciones" in cand else "",
                                      periodo="trabajo", veredicto="NO MEDIBLE", motivo=str(e)[:200],
                                      familia_declarada=cand.get("familia"),
                                      variantes_declaradas=cand.get("variantes_probadas")))
        return 1
    print(informe(s))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))

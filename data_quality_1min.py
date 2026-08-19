"""Quality report for data/es_1min_databento.csv -> data/data_quality_es_1min_databento.md

Same criteria as data_quality.py (report only, nothing corrected), plus continuous-contract checks:
contract rolls (symbol changes), price step at each roll, bars per trading day, cross-check vs Yahoo ES=F daily.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
SRC = DATA / "es_1min_databento.csv"
OUT = DATA / "data_quality_es_1min_databento.md"
YAHOO_DAILY = DATA / "es_daily.csv"

JUMP = 0.20
GAP_BDAYS = 3

lines: list[str] = []


def p(s: str = "") -> None:
    lines.append(s)


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df.empty:
        return "_(ninguna)_"
    shown = df if max_rows is None else df.head(max_rows)
    cols = list(shown.columns)
    head = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    rows = ["| " + " | ".join(str(v) for v in r) + " |" for r in shown.itertuples(index=False)]
    s = "\n".join([head, sep, *rows])
    if max_rows is not None and len(df) > max_rows:
        s += f"\n\n_(mostrando {max_rows} de {len(df)})_"
    return s


def fmt(ts) -> str:
    return ts.strftime("%Y-%m-%d %H:%M %Z") if getattr(ts, "tzinfo", None) else ts.strftime("%Y-%m-%d")


def main() -> None:
    now = pd.Timestamp.now(tz="America/New_York")
    df = pd.read_csv(SRC)
    df["ts_event_utc"] = pd.to_datetime(df["ts_event_utc"], utc=True)
    df = df.set_index("ts_event_utc")
    df["symbol"] = df["contract"]
    # Databento ohlcv-1m: ts_event = bar OPEN time (UTC). Convert to NY for session logic.
    ny = df.index.tz_convert("America/New_York")
    df["ny"] = ny
    # CME trading day: 18:00 ET (prev day) -> 17:00 ET; label by the date the session ENDS
    tday = (ny + pd.Timedelta(hours=6)).normalize().tz_localize(None)
    df["trading_day"] = tday

    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))

    p("# Informe de calidad — es_1min_databento.csv (ES.n.0, GLBX.MDP3, OHLCV-1m)")
    p()
    p(f"Generado: {now.strftime('%Y-%m-%d %H:%M %Z')}. Fuente: Databento `timeseries.get_range` "
      f"(dataset GLBX.MDP3, schema ohlcv-1m, symbol `ES.n.0` = front-month por open interest, "
      f"`stype_in=continuous`, 2010-06-06 → hoy). `ts_event_utc` es la **apertura** de la barra, en UTC. "
      f"Precios sin ajustar por roll; la columna `symbol` dice qué contrato compone cada barra. "
      f"Nada se corrigió.")
    p()
    p(f"Criterios: hueco = más de {GAP_BDAYS} días hábiles (lun–vie) faltantes entre barras consecutivas; "
      f"salto = |cierre/cierre previo − 1| > {int(JUMP*100)} %; precio absurdo = high < low, precio ≤ 0, "
      f"OHLC incoherente. 'Día de negociación' = sesión CME 18:00 ET → 17:00 ET, etiquetado por la fecha en que termina.")
    p()

    # ---- 1. summary
    p("## 1. Resumen")
    p()
    p(f"- Filas: **{len(df):,}**; rango: {fmt(df.index.min())} → {fmt(df.index.max())} "
      f"({fmt(ny.min())} → {fmt(ny.max())})")
    p(f"- Días de negociación distintos: {df['trading_day'].nunique():,}; contratos distintos: {df['instrument_id'].nunique()} (tickers distintos: {df['symbol'].nunique()}; los tickers se repiten cada década)")
    p(f"- Índice monótono creciente: {'sí' if df.index.is_monotonic_increasing else '**NO**'}; "
      f"timestamps duplicados: {int(df.index.duplicated().sum())}")
    p(f"- NaN en OHLC: {int(df[['open','high','low','close']].isna().any(axis=1).sum())}; NaN en volumen: {int(v.isna().sum())}; "
      f"NaN en contract: {int(df['contract'].isna().sum())}")
    p(f"- Volumen total: {int(v.sum()):,}; volumen mediano por barra: {v.median():.0f}")
    p()

    # ---- 1b. dataset condition (Databento metadata; needs API key)
    p("## 1b. Condición del dataset según Databento (`metadata.get_dataset_condition`)")
    p()
    try:
        import os
        from dotenv import load_dotenv
        load_dotenv(ROOT / ".env")
        import databento as db
        cli = db.Historical(os.environ["DATABENTO_API_KEY"])
        cond = cli.metadata.get_dataset_condition("GLBX.MDP3", start_date="2010-06-06", end_date=str(now.date()))
        cdf = pd.DataFrame(cond)
        counts = cdf["condition"].value_counts().to_dict()
        p(f"- Días listados: {len(cdf):,}; por condición: {counts}")
        bad = cdf[cdf["condition"] != "available"]
        p(f"- Días NO 'available' (degraded/pending/missing): **{len(bad)}**")
        if len(bad):
            p()
            p(md_table(bad[["date", "condition", "last_modified_date"]].reset_index(drop=True), 80))
    except Exception as exc:  # noqa: BLE001
        p(f"_no se pudo consultar: {exc!r}_")
    p()

    # ---- 2. gaps
    p("## 2. Huecos")
    p()
    idx = df.index.tz_convert("America/New_York").tz_localize(None)
    d = np.array(idx.normalize().values, dtype="datetime64[D]")
    missing = np.busday_count(d[:-1] + np.timedelta64(1, "D"), d[1:])
    mask = missing > GAP_BDAYS
    g = pd.DataFrame({"desde": [fmt(t) for t in ny[:-1][mask]], "hasta": [fmt(t) for t in ny[1:][mask]],
                      "dias_habiles_faltantes": missing[mask]})
    p(f"**Huecos > {GAP_BDAYS} días hábiles: {len(g)}**")
    p()
    p(md_table(g, 40))
    p()
    diffs = pd.Series(ny[1:] - ny[:-1], index=ny[1:])
    big = diffs[diffs > pd.Timedelta(minutes=1)]
    # classify: daily break (16:59/17:00 -> 18:00), weekend (Fri 17:00 -> Sun 18:00), other
    def klass(end_ts, gap):
        start_ts = end_ts - gap
        if start_ts.hour == 16 and end_ts.hour == 18 and end_ts.minute == 0 and gap <= pd.Timedelta(hours=1, minutes=5):
            return "corte diario"
        if start_ts.dayofweek == 4 and end_ts.dayofweek == 6 and end_ts.hour == 18 and end_ts.minute == 0:
            return "fin de semana"
        return "otro"
    kl = pd.Series([klass(t, gv) for t, gv in big.items()], index=big.index)
    p(f"Huecos > 1 min entre barras consecutivas: {len(big):,} — corte diario 17:00→18:00 ET: {(kl=='corte diario').sum():,}, "
      f"fin de semana vie 17:00→dom 18:00: {(kl=='fin de semana').sum():,}, **otros: {(kl=='otro').sum():,}**")
    p()
    other = big[kl == "otro"]
    # barras de 1 min faltantes dentro de sesión: huecos 'otro' de <= 1 día se listan por tamaño
    top = other.sort_values(ascending=False).head(40)
    t = pd.DataFrame({"desde": [fmt(x - gv) for x, gv in top.items()], "hasta": [fmt(x) for x in top.index],
                      "hueco": [str(pd.Timedelta(gv)) for gv in top.values]})
    p("Los 40 huecos 'otros' más grandes (festivos con cierre temprano, sesiones sin cotizar, o barras faltantes):")
    p()
    p(md_table(t))
    p()
    small_other = other[other <= pd.Timedelta(minutes=30)]
    p(f"Huecos 'otros' de ≤ 30 min (barras de 1 min sin imprimir — Databento sólo emite barra si hubo trade): "
      f"{len(small_other):,}; minutos faltantes acumulados en ellos: "
      f"{int((small_other - pd.Timedelta(minutes=1)).sum() / pd.Timedelta(minutes=1)):,}")
    rth = small_other[(small_other.index.hour * 60 + small_other.index.minute > 9 * 60 + 30) & (small_other.index.hour < 16)]
    p(f"De ellos, con fin dentro de 09:30–16:00 ET: {len(rth):,}")
    p()

    # ---- 3. bars per trading day
    p("## 3. Cobertura por día de negociación")
    p()
    per_day = df.groupby("trading_day").size()
    p(f"Barras por día de negociación: mediana {int(per_day.median())}, p5 {int(per_day.quantile(0.05))}, "
      f"mín {int(per_day.min())} ({per_day.idxmin().date()}), máx {int(per_day.max())} ({per_day.idxmax().date()}). "
      f"Un día completo son ~1.380 min (23 h).")
    low = per_day[per_day < 600]
    p(f"Días con < 600 barras: {len(low)}")
    p()
    p(md_table(pd.DataFrame({"trading_day": [x.date() for x in low.index], "barras": low.values,
                             "dia_semana": [x.day_name() for x in low.index]}), 60))
    p()
    wk = per_day[[x.dayofweek == 5 for x in per_day.index]]
    p(f"Días de negociación etiquetados en sábado (no debería haber): {len(wk)}")
    p()
    # by year
    yr = df.groupby(df["trading_day"].dt.year).agg(barras=("close", "size"), dias=("trading_day", "nunique"),
                                                   vol=("volume", "sum"))
    yr["barras_por_dia"] = (yr["barras"] / yr["dias"]).round(0).astype(int)
    yr = yr.reset_index().rename(columns={"trading_day": "año"})
    p("Por año:")
    p()
    p(md_table(yr))
    p()

    # ---- 3b. compressed-session bars (source defect)
    p("## 3b. Barras de 'sesión comprimida' (defecto de la fuente, años tempranos)")
    p()
    p("Criterio: barra cuyo volumen supera el **30 % del volumen total de su día de negociación**. En un día sano ningún "
      "minuto se acerca a eso. Verificado contra el ticker crudo `ESU0` (2010-06-22, pedido aparte): la barra de las "
      "23:59 UTC (19:59 EDT / 18:59 EST) lleva el OHLC y el volumen de TODA la sesión y coincide con el diario de Yahoo; "
      "sólo la franja 18:00→ ET de esos días tiene minutos reales. Origen probable: archivos FIX históricos sin "
      "timestamps intradía (Databento documenta que los datos pre-2017-05-21 vienen de flat files).")
    p()
    day_vol = df.groupby("trading_day")["volume"].transform("sum")
    share = v / day_vol.replace(0, np.nan)
    comp = df[share > 0.30].copy()
    comp["share_%"] = (share[share > 0.30] * 100).round(1)
    comp["weekday"] = comp["ny"].dt.day_name()
    comp["utc_hhmm"] = comp.index.strftime("%H:%M")
    by_year = comp.groupby(comp["trading_day"].dt.year).size()
    days_year = df.groupby(df["trading_day"].dt.year)["trading_day"].nunique()
    t = pd.DataFrame({"año": by_year.index, "dias_con_barra_comprimida": by_year.values,
                      "dias_negociacion": days_year.reindex(by_year.index).values})
    t["%_dias_afectados"] = (t["dias_con_barra_comprimida"] / t["dias_negociacion"] * 100).round(1)
    p(f"Barras con > 30 % del volumen del día: **{len(comp):,}** en {comp['trading_day'].nunique():,} días de negociación "
      f"({fmt(comp['ny'].min()) if len(comp) else '-'} → {fmt(comp['ny'].max()) if len(comp) else '-'})")
    p()
    p(md_table(t))
    p()
    p("Por día de la semana del día de negociación afectado:")
    p()
    wd = comp.groupby([comp["trading_day"].dt.year, comp["trading_day"].dt.day_name()]).size().unstack(fill_value=0)
    wd = wd.reindex(columns=[c for c in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"] if c in wd.columns])
    p(md_table(wd.reset_index().rename(columns={"trading_day": "año"})))
    p()
    p("Hora UTC de la barra comprimida (top):")
    p()
    hh = comp["utc_hhmm"].value_counts().head(8)
    p(md_table(pd.DataFrame({"utc_hhmm": hh.index, "n": hh.values})))
    p()
    p("Últimas 10 ocurrencias (para ver hasta cuándo llega el defecto):")
    p()
    last = comp.tail(10)
    p(md_table(pd.DataFrame({"ny": [fmt(x) for x in last["ny"]], "contract": last["symbol"].values,
                             "open": last["open"].values, "high": last["high"].values, "low": last["low"].values,
                             "close": last["close"].values, "volume": last["volume"].values,
                             "share_%": last["share_%"].values})))
    p()
    # days whose real coverage (bars outside the compressed bar) is tiny
    p(f"Días de negociación con < 600 barras (ya listados arriba): {int((per_day < 600).sum())}; de ellos, con barra comprimida: "
      f"{int(per_day[per_day < 600].index.isin(comp['trading_day']).sum())}")
    p()

    # ---- 4. prices / volume
    p("## 4. Precios y volumen")
    p()
    ret = c.pct_change()
    p(f"- high < low: **{int((h < l).sum())}**")
    p(f"- precio ≤ 0: **{int(((o<=0)|(h<=0)|(l<=0)|(c<=0)).sum())}**")
    inc = ((h < o) | (h < c) | (l > o) | (l > c)) & ~(h < l)
    p(f"- OHLC incoherente: **{int(inc.sum())}**")
    if inc.sum():
        p()
        p(md_table(df[inc][["ny", "symbol", "open", "high", "low", "close", "volume"]].reset_index(drop=True), 40))
    p(f"- Barras con volumen 0: **{int((v == 0).sum()):,}** ({(v==0).mean()*100:.3f} %)")
    if (v == 0).sum():
        z = df[v == 0]
        p(f"  - por hora ET: " + ", ".join(f"{hh:02d}h:{n}" for hh, n in z.groupby(z['ny'].dt.hour).size().items()))
    p(f"- Saltos |cierre/cierre previo − 1| > {int(JUMP*100)} %: **{int((ret.abs() > JUMP).sum())}**")
    p(f"- Mayor |retorno| barra-a-barra: {ret.abs().max()*100:.2f} % en {fmt(df['ny'][ret.abs().idxmax()])}")
    p()
    big_ret = ret[ret.abs() > 0.02]
    p(f"Movimientos barra-a-barra > 2 % (informativo): {len(big_ret)}")
    if len(big_ret):
        p()
        t = pd.DataFrame({"ny": [fmt(df['ny'][i]) for i in big_ret.index],
                          "symbol_prev": [df['symbol'].shift(1)[i] for i in big_ret.index],
                          "symbol": [df['symbol'][i] for i in big_ret.index],
                          "ret": [f"{big_ret[i]*100:+.2f} %" for i in big_ret.index],
                          "close": [df['close'][i] for i in big_ret.index]})
        p(md_table(t, 40))
    p()

    # ---- 5. rolls
    p("## 5. Rolls de contrato (cambios de `symbol`)")
    p()
    sym = df["symbol"]
    chg = df["instrument_id"] != df["instrument_id"].shift(1)
    chg.iloc[0] = False
    rolls = df[chg]
    prev_close = c.shift(1)[chg]
    t = pd.DataFrame({"primer_bar_nuevo (ET)": [fmt(x) for x in rolls["ny"]],
                      "de": sym.shift(1)[chg].values, "a": rolls["symbol"].values,
                      "close_prev": prev_close.values, "open_nuevo": rolls["open"].values,
                      "escalon_%": ((rolls["open"].values / prev_close.values - 1) * 100).round(3),
                      "dia_semana": [x.day_name() for x in rolls["ny"]]})
    p(f"Rolls detectados: **{len(rolls)}** (esperados ≈ 4/año ⇒ ~{int((df['trading_day'].max()-df['trading_day'].min()).days/365.25*4)} en el rango). "
      f"Contratos: {', '.join(sym.unique()[:8])} … {', '.join(sym.unique()[-4:])}")
    p()
    p(md_table(t.reset_index(drop=True)))
    p()
    back = [(a, b) for a, b in zip(sym.shift(1)[chg], rolls["symbol"]) if str(a) > str(b) and a[:2] == b[:2] and a[-1] == b[-1]]
    p(f"Rolls hacia un contrato 'anterior' (ida y vuelta): {len(back)}")
    p(f"Rolls que ocurren un lunes/domingo-noche (OI se evalúa al cierre del viernes): "
      f"{sum(x.dayofweek in (0, 6) for x in rolls['ny'])} de {len(rolls)}")
    p()

    # ---- 6. cross-check vs Yahoo
    p("## 6. Contraste con Yahoo ES=F diario (es_daily.csv)")
    p()
    if YAHOO_DAILY.exists():
        y = pd.read_csv(YAHOO_DAILY, parse_dates=["date"]).set_index("date")
        daily = df.groupby("trading_day").agg(open=("open", "first"), high=("high", "max"), low=("low", "min"),
                                              close=("close", "last"), volume=("volume", "sum"))
        j = daily.join(y, how="inner", lsuffix="_db", rsuffix="_yh")
        j["close_diff_%"] = (j["close_db"] / j["close_yh"] - 1) * 100
        j["ret_db"] = j["close_db"].pct_change()
        j["ret_yh"] = j["close_yh"].pct_change()
        p(f"- Días comunes: {len(j):,} ({j.index.min().date()} → {j.index.max().date()})")
        p(f"- Correlación de retornos diarios (cierre 17:00 ET Databento vs cierre Yahoo): **{j['ret_db'].corr(j['ret_yh']):.4f}**")
        p(f"- Correlación con Yahoo desplazado +1 día: {j['ret_db'].corr(j['ret_yh'].shift(-1)):.4f}; −1 día: {j['ret_db'].corr(j['ret_yh'].shift(1)):.4f}")
        p(f"- |close_db/close_yh − 1|: mediana {j['close_diff_%'].abs().median():.3f} %, p95 {j['close_diff_%'].abs().quantile(0.95):.3f} %, máx {j['close_diff_%'].abs().max():.3f} %")
        p(f"- Volumen: mediana (vol_db / vol_yh) = {(j['volume_db']/j['volume_yh'].replace(0, np.nan)).median():.3f}")
        p()
        p("Correlación de retornos diarios y diferencia de cierre por año (muestra desde cuándo el intradía es usable):")
        p()
        yy = j.groupby(j.index.year).apply(lambda g: pd.Series({"n": len(g), "corr": g["ret_db"].corr(g["ret_yh"]),
                                                               "mediana_|dif_close|_%": g["close_diff_%"].abs().median(),
                                                               "p95_|dif_close|_%": g["close_diff_%"].abs().quantile(0.95)}))
        yy["n"] = yy["n"].astype(int); yy = yy.round(4).reset_index().rename(columns={"index": "año", "trading_day": "año"})
        yy.columns = ["año", "n", "corr", "mediana_|dif_close|_%", "p95_|dif_close|_%"]
        yy["año"] = yy["año"].astype(int)
        p(md_table(yy))
        worst = j.reindex(j["close_diff_%"].abs().sort_values(ascending=False).index).head(15)
        p()
        p("Mayores diferencias de cierre (candidatos: roll en fechas distintas entre proveedores):")
        p()
        p(md_table(pd.DataFrame({"día": [x.date() for x in worst.index], "close_db": worst["close_db"].values,
                                 "close_yh": worst["close_yh"].values, "dif_%": worst["close_diff_%"].round(3).values,
                                 "symbol_db": [df.loc[df['trading_day'] == x, 'symbol'].iloc[-1] for x in worst.index]})))
        only_db = daily.index.difference(y.index)
        only_yh = y.index[(y.index >= daily.index.min()) & (y.index <= daily.index.max())].difference(daily.index)
        p()
        p(f"- Días de negociación en Databento sin fila en Yahoo: {len(only_db)}"
          + (f" — primeros 30: {', '.join(str(x.date()) for x in only_db[:30])}" if len(only_db) else ""))
        p(f"- Fechas en Yahoo (dentro del rango) sin día en Databento: {len(only_yh)}"
          + (f" — primeros 30: {', '.join(str(x.date()) for x in only_yh[:30])}" if len(only_yh) else ""))
    else:
        p("_es_daily.csv no encontrado_")
    p()

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(lines)} lines)")


if __name__ == "__main__":
    main()

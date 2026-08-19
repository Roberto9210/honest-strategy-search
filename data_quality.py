"""Quality report for the CSVs in ./data -> ./data/data_quality.md

Reports only. Nothing is corrected, dropped or filled.
"""
from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

DATA = Path(__file__).resolve().parent / "data"
OUT = DATA / "data_quality.md"

FILES = {
    "es_daily.csv": ("ES=F", "1d"),
    "es_1h.csv": ("ES=F", "1h"),
    "es_5m.csv": ("ES=F", "5m"),
    "spy_daily.csv": ("SPY", "1d"),
}

JUMP = 0.20  # |return| > 20 % between consecutive rows
GAP_BDAYS = 3  # business days missing between consecutive rows

lines: list[str] = []


def p(s: str = "") -> None:
    lines.append(s)


def load(name: str, interval: str) -> pd.DataFrame:
    col = "date" if interval == "1d" else "datetime"
    df = pd.read_csv(DATA / name)
    if interval == "1d":
        df[col] = pd.to_datetime(df[col])
    else:
        # keep the UTC offset that came from Yahoo, then convert to New York for readability
        df[col] = pd.to_datetime(df[col], utc=True).dt.tz_convert("America/New_York")
    df = df.set_index(col)
    return df


def fmt_ts(ts) -> str:
    if getattr(ts, "tzinfo", None) is not None:
        return ts.strftime("%Y-%m-%d %H:%M %Z")
    return ts.strftime("%Y-%m-%d")


def md_table(df: pd.DataFrame, max_rows: int | None = None) -> str:
    if df.empty:
        return "_(ninguna)_"
    shown = df if max_rows is None else df.head(max_rows)
    cols = list(shown.columns)
    head = "| " + " | ".join(str(c) for c in cols) + " |"
    sep = "|" + "|".join("---" for _ in cols) + "|"
    rows = []
    for r in shown.itertuples(index=False):
        rows.append("| " + " | ".join(str(v) for v in r) + " |")
    s = "\n".join([head, sep, *rows])
    if max_rows is not None and len(df) > max_rows:
        s += f"\n\n_(mostrando {max_rows} de {len(df)})_"
    return s


def business_gaps(idx: pd.DatetimeIndex) -> pd.DataFrame:
    """Consecutive rows with more than GAP_BDAYS weekday (Mon-Fri) days strictly between them."""
    if idx.tz is not None:
        idx = idx.tz_localize(None)
    d = np.array(idx.normalize().values, dtype="datetime64[D]")
    prev, nxt = d[:-1], d[1:]
    # weekdays in (prev, nxt): count in [prev+1, nxt)
    missing = np.busday_count(prev + np.timedelta64(1, "D"), nxt)
    mask = missing > GAP_BDAYS
    out = pd.DataFrame(
        {
            "desde": [str(x) for x in prev[mask]],
            "hasta": [str(x) for x in nxt[mask]],
            "dias_calendario": ((nxt[mask] - prev[mask]).astype(int)),
            "dias_habiles_faltantes": missing[mask],
        }
    )
    return out


def intraday_gaps(idx: pd.DatetimeIndex, expected: pd.Timedelta, top: int = 15) -> pd.DataFrame:
    """Largest gaps between consecutive bars (informational, beyond the weekend/daily-break pattern)."""
    diffs = pd.Series(idx[1:] - idx[:-1], index=idx[1:])
    # normal: exactly `expected`; also normal: the daily 17:00-18:00 ET maintenance break and the weekend
    big = diffs[diffs > expected]
    df = pd.DataFrame(
        {
            "desde": [fmt_ts(t - g) for t, g in big.items()],
            "hasta": [fmt_ts(t) for t in big.index],
            "hueco": [str(pd.Timedelta(g)) for g in big.values],
        }
    )
    df["_sort"] = big.values
    df = df.sort_values("_sort", ascending=False).drop(columns="_sort").head(top).reset_index(drop=True)
    return df, len(big)


def price_checks(df: pd.DataFrame, interval: str) -> dict:
    res = {}
    o, h, l, c, v = (df[k] for k in ("open", "high", "low", "close", "volume"))
    res["nan_rows"] = int(df[["open", "high", "low", "close"]].isna().any(axis=1).sum())
    res["nan_volume"] = int(v.isna().sum())
    res["dup_index"] = int(df.index.duplicated().sum())
    res["non_monotonic"] = bool(not df.index.is_monotonic_increasing)
    res["high_lt_low"] = df[h < l]
    res["nonpositive_price"] = df[(o <= 0) | (h <= 0) | (l <= 0) | (c <= 0)]
    ohlc_incoh = (h < o) | (h < c) | (l > o) | (l > c)
    res["ohlc_incoherent"] = df[ohlc_incoh & ~(h < l)]
    res["zero_volume"] = df[v == 0]
    ret = c.pct_change()
    res["ret"] = ret
    res["jumps"] = df.assign(ret_close=ret)[ret.abs() > JUMP]
    gap_open = (o / c.shift(1) - 1)
    res["gap_open"] = df.assign(gap_open=gap_open)[gap_open.abs() > JUMP]
    res["max_abs_ret"] = float(ret.abs().max())
    res["max_abs_ret_ts"] = ret.abs().idxmax()
    if interval == "1d":
        wk = df[df.index.dayofweek >= 5]
        res["weekend_rows"] = wk
    return res


def main() -> None:
    now = pd.Timestamp.now(tz="America/New_York")
    p("# Informe de calidad de datos — deadman-search/data")
    p()
    p(f"Generado: {now.strftime('%Y-%m-%d %H:%M %Z')}. Fuente: Yahoo Finance vía yfinance 1.6.0 "
      f"(`Ticker.history`, `auto_adjust=False`, sin pre/post market). Nada se corrigió: lo que sigue es "
      f"lo que vino del proveedor.")
    p()
    p(f"Criterios: hueco = más de {GAP_BDAYS} días hábiles (lun–vie, sin calendario de festivos) faltantes entre "
      f"filas consecutivas; salto = |variación de cierre a cierre| > {int(JUMP*100)} % entre filas consecutivas "
      f"(y aparte |apertura vs cierre previo| > {int(JUMP*100)} %); precio absurdo = high < low, precio ≤ 0, "
      f"o high/low incoherentes con open/close.")
    p()

    frames: dict[str, pd.DataFrame] = {}

    # ---------- 1. resumen ----------
    p("## 1. Resumen por archivo")
    p()
    rows = []
    for name, (sym, interval) in FILES.items():
        df = load(name, interval)
        frames[name] = df
        rows.append(
            {
                "archivo": name,
                "símbolo": sym,
                "intervalo": interval,
                "filas": len(df),
                "desde": fmt_ts(df.index.min()),
                "hasta": fmt_ts(df.index.max()),
                "días distintos": int(pd.Series(df.index.normalize()).nunique()),
            }
        )
    p(md_table(pd.DataFrame(rows)))
    p()
    p("Notas de contexto (no son errores, pero condicionan cualquier uso):")
    p("- `ES=F` en Yahoo es el **front-month continuo sin ajustar por roll**: en los cambios de contrato "
      "(mar/jun/sep/dic) puede haber escalones de precio que no son movimiento de mercado.")
    p("- La última fila de cada archivo corresponde a la sesión del día de descarga y puede estar **incompleta** "
      "(descarga hecha a las " + now.strftime("%H:%M %Z") + ").")
    p("- Las marcas temporales intradía están en hora de Nueva York (offset incluido en el CSV). "
      "El día 'date' de los diarios de ES lo asigna Yahoo; la convención de sesión (18:00–17:00 ET) se "
      "contrasta abajo con la correlación ES/SPY a distintos lags.")
    p("- SPY es precio **sin ajustar** por dividendos/splits (`auto_adjust=False`).")
    p()

    # ---------- 2. por archivo ----------
    p("## 2. Detalle por archivo")
    p()
    for name, (sym, interval) in FILES.items():
        df = frames[name]
        ck = price_checks(df, interval)
        p(f"### {name} ({sym}, {interval})")
        p()
        p(f"- Filas: **{len(df)}**; rango: {fmt_ts(df.index.min())} → {fmt_ts(df.index.max())}")
        p(f"- Índice monótono creciente: {'sí' if not ck['non_monotonic'] else '**NO**'}; "
          f"timestamps duplicados: {ck['dup_index']}")
        p(f"- Filas con NaN en OHLC: {ck['nan_rows']}; NaN en volumen: {ck['nan_volume']}")
        p(f"- Mayor |retorno| cierre-a-cierre entre filas consecutivas: {ck['max_abs_ret']*100:.2f} % "
          f"(en {fmt_ts(ck['max_abs_ret_ts'])})")
        p()

        # gaps
        g = business_gaps(df.index)
        p(f"**Huecos > {GAP_BDAYS} días hábiles entre filas consecutivas: {len(g)}**")
        p()
        p(md_table(g, 40))
        p()
        if interval != "1d":
            exp = pd.Timedelta(hours=1) if interval == "1h" else pd.Timedelta(minutes=5)
            ig, n_big = intraday_gaps(df.index, exp)
            p(f"Huecos intradía mayores que el intervalo nominal ({exp}): {n_big} en total "
              f"(incluye el corte diario 17:00–18:00 ET y los fines de semana, que son normales). Los 15 mayores:")
            p()
            p(md_table(ig))
            p()
            # daily coverage: bars per session day
            per_day = df.groupby(df.index.normalize()).size()
            p(f"Barras por día calendario: mediana {int(per_day.median())}, mín {int(per_day.min())} "
              f"({per_day.idxmin().date()}), máx {int(per_day.max())} ({per_day.idxmax().date()}); "
              f"días con menos de la mitad de la mediana: {int((per_day < per_day.median()/2).sum())}")
            low_days = per_day[per_day < per_day.median() / 2]
            if len(low_days):
                p()
                p(md_table(pd.DataFrame({"día": [d.date() for d in low_days.index], "barras": low_days.values}), 30))
            p()

        # volume zero
        zv = ck["zero_volume"]
        if interval == "1d":
            p(f"**Días con volumen cero: {len(zv)}**")
            p()
            p(md_table(zv.reset_index(), 40))
        else:
            zv_days = zv.groupby(zv.index.normalize()).size() if len(zv) else pd.Series(dtype=int)
            p(f"**Barras con volumen cero: {len(zv)}** ({len(zv)/len(df)*100:.2f} % de las filas), "
              f"repartidas en {len(zv_days)} días. Por hora del día (ET), las barras con volumen 0:")
            p()
            if len(zv):
                by_hour = zv.groupby(zv.index.hour).size()
                p(md_table(pd.DataFrame({"hora_ET": by_hour.index, "barras_vol0": by_hour.values})))
                p()
                p("Días con más barras a volumen 0:")
                p()
                top = zv_days.sort_values(ascending=False).head(15)
                p(md_table(pd.DataFrame({"día": [d.date() for d in top.index], "barras_vol0": top.values})))
            # bars with zero volume during regular US session hours 9:30-16:00 ET
            rth = zv[(zv.index.hour * 60 + zv.index.minute >= 9 * 60 + 30) & (zv.index.hour < 16)]
            p()
            p(f"De ellas, dentro de la sesión regular de acciones (09:30–16:00 ET): **{len(rth)}**")
            if len(rth):
                p()
                p(md_table(rth.reset_index(), 40))
        p()

        # absurd prices
        p(f"**high < low: {len(ck['high_lt_low'])}**")
        if len(ck["high_lt_low"]):
            p()
            p(md_table(ck["high_lt_low"].reset_index(), 40))
        p()
        p(f"**Precio ≤ 0: {len(ck['nonpositive_price'])}**")
        if len(ck["nonpositive_price"]):
            p()
            p(md_table(ck["nonpositive_price"].reset_index(), 40))
        p()
        p(f"**OHLC incoherente (high < open/close o low > open/close, con high ≥ low): {len(ck['ohlc_incoherent'])}**")
        if len(ck["ohlc_incoherent"]):
            p()
            inc = ck["ohlc_incoherent"].reset_index()
            if interval == "1d":
                # third Friday of Mar/Jun/Sep/Dec = quarterly ES expiry (contract roll)
                ts = pd.to_datetime(inc.iloc[:, 0])
                inc["tercer_viernes_trimestral"] = [
                    bool(t.dayofweek == 4 and 15 <= t.day <= 21 and t.month in (3, 6, 9, 12)) for t in ts
                ]
            p(md_table(inc, 40))
        p()
        p(f"**Saltos |cierre/cierre previo − 1| > {int(JUMP*100)} %: {len(ck['jumps'])}**")
        if len(ck["jumps"]):
            p()
            j = ck["jumps"].reset_index()
            j["ret_close"] = (j["ret_close"] * 100).round(2).astype(str) + " %"
            p(md_table(j, 40))
        p()
        p(f"**Saltos |apertura/cierre previo − 1| > {int(JUMP*100)} %: {len(ck['gap_open'])}**")
        if len(ck["gap_open"]):
            p()
            j = ck["gap_open"].reset_index()
            j["gap_open"] = (j["gap_open"] * 100).round(2).astype(str) + " %"
            p(md_table(j, 40))
        p()
        if interval == "1d":
            wk = ck["weekend_rows"]
            p(f"**Filas fechadas en sábado/domingo: {len(wk)}**")
            if len(wk):
                p()
                p(md_table(wk.reset_index(), 40))
            p()
            # informational: distribution of big-but-not-absurd moves
            r = ck["ret"].dropna()
            p(f"Distribución de |retorno diario| (informativo): >5 %: {int((r.abs()>0.05).sum())} días, "
              f">10 %: {int((r.abs()>0.10).sum())} días. Top 10 por magnitud:")
            p()
            top = r.abs().sort_values(ascending=False).head(10)
            t = pd.DataFrame({"fecha": [fmt_ts(i) for i in top.index],
                              "retorno": [f"{r[i]*100:+.2f} %" for i in top.index],
                              "close": [df.loc[i, 'close'] for i in top.index]})
            p(md_table(t))
            p()

    # ---------- 3. correlación ----------
    p("## 3. Correlación de retornos diarios ES vs SPY")
    p()
    es = frames["es_daily.csv"]["close"]
    spy = frames["spy_daily.csv"]["close"]
    es.index = es.index.normalize()
    spy.index = spy.index.normalize()
    r_es = es.pct_change().rename("es")
    r_spy = spy.pct_change().rename("spy")
    both = pd.concat([r_es, r_spy], axis=1, join="inner").dropna()
    p(f"- Fechas comunes con retorno en ambos: **{len(both)}** "
      f"({fmt_ts(both.index.min())} → {fmt_ts(both.index.max())})")
    only_es = es.index.difference(spy.index)
    only_spy = spy.index.difference(es.index)
    common_range = (es.index.min(), es.index.max())
    only_spy_in_range = only_spy[(only_spy >= common_range[0]) & (only_spy <= common_range[1])]
    p(f"- Fechas en ES sin SPY: {len(only_es)}; fechas en SPY sin ES (dentro del rango de ES): {len(only_spy_in_range)}")
    if len(only_es):
        p(f"  - ES sin SPY (primeras 30): {', '.join(str(d.date()) for d in only_es[:30])}")
    if len(only_spy_in_range):
        p(f"  - SPY sin ES, dentro del rango de ES (primeras 30): {', '.join(str(d.date()) for d in only_spy_in_range[:30])}")
    p()
    corr0 = both["es"].corr(both["spy"])
    corr_es_lead = both["es"].corr(both["spy"].shift(-1))   # ES(t) vs SPY(t+1)
    corr_spy_lead = both["es"].corr(both["spy"].shift(1))   # ES(t) vs SPY(t-1)
    p(f"- **Pearson, mismo día: {corr0:.4f}**")
    p(f"- ES(t) vs SPY(t+1): {corr_es_lead:.4f}; ES(t) vs SPY(t−1): {corr_spy_lead:.4f} "
      f"(si alguno de los lags superara al contemporáneo, la fecha de las velas de ES estaría desplazada).")
    p(f"- Spearman, mismo día: {both['es'].rank().corr(both['spy'].rank()):.4f}")
    p(f"- Desv. típica diaria: ES {both['es'].std()*100:.3f} %, SPY {both['spy'].std()*100:.3f} %; "
      f"std de la diferencia (ES−SPY): {(both['es']-both['spy']).std()*100:.3f} %")
    p()
    p("Por año (mismo día):")
    p()
    by_year = both.groupby(both.index.year).apply(lambda g: pd.Series({"n": len(g), "corr": g["es"].corr(g["spy"])}))
    by_year["n"] = by_year["n"].astype(int)
    by_year["corr"] = by_year["corr"].round(4)
    by_year = by_year.reset_index().rename(columns={"date": "año", "index": "año"})
    by_year.columns = ["año", "n", "corr"]
    by_year["año"] = by_year["año"].astype(int)
    p(md_table(by_year))
    p()
    p("Mayores divergencias diarias |ES − SPY| (informativo; candidatos a roll de contrato, festivo parcial o "
      "sesión desalineada):")
    p()
    diff = (both["es"] - both["spy"]).abs().sort_values(ascending=False).head(15)
    t = pd.DataFrame({"fecha": [fmt_ts(i) for i in diff.index],
                      "ret_ES": [f"{both.loc[i,'es']*100:+.2f} %" for i in diff.index],
                      "ret_SPY": [f"{both.loc[i,'spy']*100:+.2f} %" for i in diff.index],
                      "|dif|": [f"{diff[i]*100:.2f} %" for i in diff.index]})
    p(md_table(t))
    p()

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {OUT} ({len(lines)} lines)")


if __name__ == "__main__":
    main()

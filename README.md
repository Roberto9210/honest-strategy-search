# honest-strategy-search

**A six-week search for a tradable edge in S&P 500 futures, closed in one week with a negative verdict — and
every step of it published, including the failures and the author's own design error.**

Read the story: **[ARTICLE.md](ARTICLE.md)**.

This repository is not a strategy. It is the *method*: the spec frozen before the first backtest, the data
quality control that disqualified six years of data, the append-only ledger of all 59 experiments with a
verifiable hash chain, the hold-out period that was never opened, and the verdict that says **no edge was
found**.

The point is the shape of it. A search that can only end in "we found something" is not a search — it is a
sales process. Almost every backtest you will be shown was produced by one: the bar moved after the results
came in, the losing variants were never counted, the hold-out was peeked at, and the costs were an
afterthought. Here the bar, the budget, the costs and the stop line were written down first, by someone who
then had to live with them.

Sibling project: **[deadman](https://github.com/Roberto9210/deadman)** (`pip install deadman-kit`) — the same
discipline, packaged as a library: execution-safety primitives that stop instead of guessing.

> The working documents (spec, verdict, QC reports) are in Spanish and are published verbatim, unedited.
> This README is the English guide to them.

---

## 1. The spec was frozen before the first backtest

[`factory/spec_busqueda_estrategia.md`](factory/spec_busqueda_estrategia.md) — v1, approved before a single
backtest ran, and never amended mid-search.

It fixes, in advance:

- **The instrument**: MES (Micro E-mini S&P 500), one contract, explicit rules only — no black boxes.
- **The families**: five, in order (opening-range breakout, intraday trend, VWAP mean reversion,
  calendar/hour patterns, volatility compression), **maximum 20 configurations each**.
- **The costs, inside every number**: $1.40 commission + 2 ticks of slippage = **$3.90 round trip per
  contract**, subtracted by the harness itself so that no strategy can forget them
  ([`factory/harness.py`](factory/harness.py), `FRICTION_RT`).
- **The approval bar**, written before any data was seen. A candidate survives only if, on the untouched
  hold-out, **net of costs**:

  | Metric | Bar |
  |---|---|
  | Trades in the final exam | >= 200 |
  | Profit factor | >= 1.3 |
  | Annual profitability | positive in **every** year, not just in total |
  | Drawdown | <= 2x the equivalent best winning run |
  | Robustness | still wins with parameters +/-20% |

- **The stop line** (spec section 6): six weeks, five families, 20 configurations each, all logged. *"If
  nothing clears the bar, the verdict is 'these families have no exploitable edge for us at these costs' — it
  gets written, filed, and we stop. No extra families 'just one more', no loosening the bar."*

The bar is not decoration, it is code: `passes_bar()` returns the failing reasons, and the harness refuses to
evaluate on the hold-out unless the call explicitly declares itself a final exam.

## 2. The data, with its quality control published

Two sources, both checked before use, both reported without corrections:

- **Daily ES=F and SPY** (Yahoo Finance, via [`download_data.py`](download_data.py)): 6,544 daily bars back
  to 2000, cross-checked against SPY (daily return correlation 0.976, no lag).
  QC: [`qc/data_quality_yahoo.md`](qc/data_quality_yahoo.md).
- **1-minute CME futures** (Databento, dataset `GLBX.MDP3`, schema `ohlcv-1m`, continuous front-month
  `ES.n.0`): 4,904,294 bars, 2010–2026. Cost: **$17.90**, quoted from the API before ordering and paid out of
  the signup credit. QC: [`qc/data_quality_es_1min_databento.md`](qc/data_quality_es_1min_databento.md).

The QC is the reason this repository has the shape it has. It found a defect nobody advertises: in
**2010–2015 the intraday data is not intraday**. On most Tuesday-to-Friday sessions of 2010 (92% of trading
days), 2011 (87%) and 2012 (71%), the whole session is collapsed into a single 23:59 UTC bar carrying the
entire day's OHLC and volume — only the evening reopen has real minutes. The defect decays but survives into
November 2015. Measured against Yahoo's daily closes, the per-year return correlation is 0.32 in 2010–2011 and
0.63 in 2012, reaching >= 0.94 only from **2016** onward.

So the intraday search starts in 2016, not 2010. Six years of data that were bought and paid for were thrown
away because they could not carry the weight. Databento's own 31 "degraded" days are listed too, and so are
the 10 daily rows where Yahoo's close falls outside its own high/low (8 of them on quarterly expiry Fridays).

A defect found before the backtest is a data problem. The same defect found after a profitable backtest is a
discovery nobody makes.

## 3. Fifty-nine experiments, in an append-only ledger with a hash chain

[`factory/experiments_ledger.jsonl`](factory/experiments_ledger.jsonl) — **60 lines**: 59 experiment entries,
plus the verdict record that closes the file. Every configuration that ran is in there, winners and losers
alike, in the order it happened. Nothing was deleted, nothing was rewritten.

The 59 break down as **57 strategy configurations** — F1 opening-range 20/20, F2 trend 14/20, F4 calendar
10/20, F5 volatility 7/20, F3 VWAP 6/20 — plus **2 harness self-tests**: the first two lines, a synthetic
one-trade fixture used to prove the machinery (including the hold-out path) was instrumented before any real
work began.

Each entry carries the SHA-256 of the previous one. Editing any past line breaks the chain, and the break is
detectable by anyone:

```bash
python -c "import sys; sys.path.insert(0,'factory'); import harness; print(harness.verify_ledger())"
```

It prints `True` on the published file. That is the whole trick: a record of failures that cannot be
retroactively tidied is worth more than any equity curve.

**The counting is the point.** Running 100 variants and reporting the one that won is the most common way to
lie with a backtest, and the most common way to lie to yourself. The denominator is in this file.

## 4. The vault: 2020–2026, never opened

The data was split on day one: development (part A) = 2016–2019 intraday, 2000–2019 daily; hold-out (part B)
= **2020–2026**, sealed. The rule from the spec: each candidate may touch B exactly once, as a final exam, and
if it fails there it dies — no going back to refit it, because that is memorising the exam.

**No strategy ever reached the exam.** Not one candidate earned the right to open the vault, so part B is
untouched: six years of the most recent market, still unseen, still usable as a genuine test by whoever picks
this up next.

Exactly one line in the ledger carries `"part": "B"` — the harness self-test on line 2, a fabricated single
trade whose only job was to prove that the final-exam path writes to the ledger. It touches no real market
data. It is pointed at here rather than quietly excluded, because a repository whose argument is "count
everything" does not get to hide its own line items.

## 5. The verdict: negative, and published in full

[`factory/veredicto_fase1.md`](factory/veredicto_fase1.md) — the complete document, as written.

| Family | Configs | Best net result (part A) | Status |
|---|---|---|---|
| F1 Opening-range breakout | 20/20 | PF 1.07 (ORB30 + gap vs previous day; 308 trades) | **Dead** |
| F2 Daily trend | 14/20 | active variants PF <= 1.02; the "winners" (PF 23.7 on 9 trades over 19 years) are index exposure, not strategy | **Dead** |
| F3 VWAP reversion | 6/20 | PF 0.75; every variant between 0.53 and 0.75 | **Dead** (closed early, hopeless) |
| F4 Calendar | 10/20 | turn-of-month: PF 1.51 net, 231 trades over 20 years, 18/20 years positive, confirmed on SPY | **Real signal, this search cannot decide it**: ~12 trades/year cannot reach the 200-trade bar, it needs overnight positions, and 57 searches over pure noise match or beat it 72% of the time — what survives that, and what does not, is in [the calculation](factory/botc_potencia_f4.md) |
| F5 Volatility | 7/20 | NR7 daily with next-day exit: PF 1.17 | **Dead** (under the bar) |

> **In these five families, with explicit rules and realistic retail costs, there is no exploitable edge for
> us in ES/MES.** The best honest configurations land between break-even and 1.07 — below any continuation
> threshold, and far from the 1.3 that separates a tradable strategy from a statistical mirage.

What the verdict deliberately does **not** claim: not that nobody can make money in futures. It says that
simple, documented families, net of friction, on the most arbitraged market on earth, leave no room for a
retail operator with these tools. This is what the literature predicts. The predecessor project (ALAYA)
learned it over months with real money; here it cost **one week and $0 out of pocket** — the $17.90 of data
came out of signup credit — with auditable evidence.

## 6. The author's own error, charged to the budget

From the verdict, unedited in substance:

> Three F1 configurations were spent on a badly designed filter ("open outside the overnight range", with the
> overnight window defined as running until 09:29, which makes the condition nearly impossible: it produced
> 0–1 trades). The budget was respected anyway: design errors also consume cartridges, and that is how it is
> recorded.

They are in the ledger, findable by their result: two `orb_filtered / filter: on_break` entries with 1 trade,
and one `filter: nr7_on` with 0. A search that quietly re-runs its own mistakes for free is not measuring
anything — the 20-configuration budget only means something when broken configurations cost the same as good
ones.

## 7. What is here

```
factory/
  spec_busqueda_estrategia.md   the spec, frozen before the first backtest
  veredicto_fase1.md            the negative verdict, complete
  harness.py                    friction, split, pass bar, hash-chained ledger, vault guard
  intradia.py                   families 1 (opening-range breakout) and 3 (VWAP reversion)
  familia2_tendencia.py         family 2 (daily trend)
  familias_4_5.py               families 4 (calendar) and 5 (volatility compression)
  experiments_ledger.jsonl      60 lines, append-only, hash-chained
qc/                             the two quality-control reports, as generated
download_data.py                Yahoo daily / hourly / 5-minute downloader
data_quality.py                 QC for the Yahoo series
data_quality_1min.py            QC for the Databento 1-minute series
databento_estimate.py           prices a Databento request BEFORE ordering (metadata only, free)
databento_download.py           downloads ES 1-minute and resolves the real contract behind each bar
```

**Not here: the data.** No CSV, no DBN file, not even a compressed subset. Databento's and Yahoo's terms do
not allow redistributing their series, so `data/` is git-ignored and always was — the exclusion was verified
against `git status` before the first commit, not patched in afterwards.

## 8. Reproducing this

Everything below runs on your own accounts and your own credentials. Nothing here needs mine.

```bash
python -m venv venv && venv/Scripts/python -m pip install yfinance pandas databento python-dotenv
```

**1. Free data (Yahoo)** — daily ES=F and SPY, hourly, 5-minute:

```bash
python download_data.py
```

**2. Paid data (Databento)** — create an account at databento.com (email and password; new users get $125 in
credits), create an API key in the portal, and put it in a local `.env` file that git ignores:

```bash
echo "DATABENTO_API_KEY=db-your-own-key" > .env
```

Price the request *before* ordering — this call is metadata only and costs nothing:

```bash
python databento_estimate.py
```

It quoted **$17.90** for ES `ohlcv-1m` from 2010-06-06 to date, at $70/GB. Then download:

```bash
python databento_download.py
```

**3. Regenerate the QC** and compare against [`qc/`](qc/):

```bash
python data_quality.py
python data_quality_1min.py
```

**4. Verify the ledger** — needs no data, works on the published file:

```bash
python -c "import sys; sys.path.insert(0,'factory'); import harness; print(harness.verify_ledger())"
```

Data moves under your feet: Yahoo revises history, Databento re-cures degraded days. If your QC differs from
the committed one, that difference is itself a finding — the reports are timestamped for exactly that reason.

## License

MIT. See [LICENSE](LICENSE). The data is not covered and is not redistributed here — download your own.

---

*Phase 1 ran and closed on 19 August 2026. The families are dead; the method is not. If you continue from
here, part B is still sealed — and the only way to keep it worth anything is to open it once.*

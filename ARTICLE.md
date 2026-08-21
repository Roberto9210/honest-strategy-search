# I tested 57 trading strategies with a tamper-evident ledger. Everything failed. Here's what that proves.

It proves less than the headline suggests, and that is the point.

Over one week in August 2026 I ran a search for a tradable edge in S&P 500 futures. Five strategy families,
57 configurations, every one of them logged before I knew whether it worked. None cleared the bar. The
verdict is negative and published in full, and the hold-out data — six years of it — is still sealed,
because nothing ever earned the right to open it.

A search that can only end in "we found something" is not a search. It is a sales process. Almost every
backtest you will be shown was produced by one: the threshold moved after the results came in, the losing
variants were never counted, the hold-out was peeked at, and the costs were an afterthought. What follows
is the shape of the other thing.

## What was frozen before the first backtest

The spec was written and approved before a single line of market data was loaded, and never amended
mid-search. It fixed the instrument (MES, one contract, explicit rules only), the five families in order,
a hard budget of 20 configurations per family, and the bar a candidate had to clear on untouched data,
net of costs:

- at least 200 trades in the final exam
- profit factor ≥ 1.3
- positive in **every** year, not just in total
- drawdown ≤ 2× the equivalent best winning run
- still winning with parameters ±20%

Costs live inside every number rather than in a footnote: $1.40 commission plus two ticks of slippage,
$3.90 round trip per contract, subtracted by the test harness itself so that no strategy can quietly
forget them. The bar is not decoration either — it is a function that returns the reasons a candidate
failed, and the harness refuses to evaluate anything against the hold-out unless the call explicitly
declares itself a final exam.

The spec also wrote down the stop line: six weeks, five families, twenty configurations each, all logged.
*If nothing clears the bar, the verdict is that these families have no exploitable edge for us at these
costs; it gets written, filed, and we stop. No extra families "just one more", no loosening the bar.*

It took one week, not six. The verdict was the one the stop line anticipated.

## The data defect that cost six years

I bought 4,904,294 one-minute CME bars from Databento — ES front-month, 2010 to 2026, $17.90, quoted from
the API before ordering and paid out of signup credit. Then I ran quality control on it before using it,
which is the only reason this repository has the shape it has.

In 2010–2015, the intraday data is not intraday. On 92% of the 2010 trading days, 87% of 2011 and 71% of
2012, the entire session is collapsed into a single 23:59 UTC bar carrying the whole day's open, high, low,
close and volume. Only the evening reopen has real minutes. The defect decays but survives into November
2015. Measured against Yahoo's daily closes, per-year return correlation is 0.32 in 2010–2011 and 0.63 in
2012, and only reaches ≥ 0.94 from 2016 onward.

So the intraday search starts in 2016. Six years of data that were bought and paid for were thrown away
because they could not carry the weight.

The timing is the whole lesson. A defect found before the backtest is a data problem. The same defect
found after a profitable backtest is a discovery nobody makes.

## What the 57 configurations did

| Family | Configs | Best net result | Status |
|---|---|---|---|
| F1 Opening-range breakout | 20/20 | PF 1.07 (ORB30 + gap, 308 trades) | Dead |
| F2 Daily trend | 14/20 | active variants PF ≤ 1.02 | Dead |
| F3 VWAP reversion | 6/20 | PF 0.75; every variant 0.53–0.75 | Dead — closed early, hopeless |
| F4 Calendar | 10/20 | turn-of-month PF 1.51, 231 trades / 20 years | Real signal, this search cannot decide it |
| F5 Volatility compression | 7/20 | NR7 with next-day exit, PF 1.17 | Dead — under the bar |

Two rows deserve more than a verdict.

F2's headline "winners" show a profit factor of 23.7 — on nine trades over nineteen years. That is not a
strategy, it is index exposure with extra steps, and a search that reports it as a result is lying to
itself first and to you second.

F4 is the awkward one, and the reason it is awkward is not the reason I first wrote down.

Turn-of-month looks like a find: profit factor 1.51 net of costs, 231 trades over twenty years, positive
in 18 of 20 years, still standing when re-run on SPY, and profitable across the whole 3×3 neighbourhood
of its two parameters. The first verdict filed it as out of scope — ~12 trades a year cannot reach a
200-trade bar in any reasonable time, and it needs overnight positions the spec excluded. That reasoning
still holds. It is no longer the main one.

The main one is what fifty-seven tries cost.

The intuition first, before any statistics. Test enough rules against a market with no pattern in it at
all and some of them will look good anyway — not because they work, but because randomness is lumpy. The
more rules you try, the better the best one looks, and it looks better for free. So the question is never
"does my best result look good". It is "does my best result look better than what luck alone produces
after the same number of tries".

That is measurable, so I measured it. Fifty-seven strategies, each drawing the same number of trades with
the same variability as F4, run against 20,000 markets containing nothing but noise: the best of the
fifty-seven comes back at **p = 0.0167** on average, which is what the closed form (1/58 = 0.0172)
predicts. F4 scored **p = 0.0212**. In **71.7%** of those noise searches, the best of fifty-seven matches
or beats the best thing this search found in twenty years of real market data.

That does not make F4 noise. It makes F4 indistinguishable from noise *by this search* — which is a
statement about the search, not about the market. The difference matters, and collapsing it would be the
mirror image of the inflation this project exists to avoid: burying a finding is as dishonest as selling
one.

Two things about F4 survive the correction. It is positive in **18 of 20 years**, and the pooled p-value
does not measure that at all — it asks only whether the average trade differs from zero, not whether the
effect keeps turning up year after year. And it **replicates on SPY**, a different instrument with
different mechanics and a different holder base. That replication is partial rather than independent: the
data QC in this repository puts the ES/SPY daily return correlation at 0.976, so SPY is largely the same
bet in another wrapper. But largely is not entirely, and a pattern that shows up in both is worth more
than a pattern that shows up in one.

So the verdict is narrower and less satisfying than "turn-of-month is noise", which is not what the
arithmetic says. It is: **this search cannot tell turn-of-month apart from luck, and the data that could
tell them apart do not exist.**

That second clause is a count, not a figure of speech. Six years were sealed before the first backtest and
never opened: 2020-2026. They contain **80 turn-of-month trades**. At the variability
this signal actually has, 80 trades carry a **27.3% chance** of detecting the edge *even if the edge is
entirely real* — the sealed years would report "nothing here" three times out of four regardless of the
truth. Raising that to the conventional 80% needs **342 trades**. The entire series back to 2000 contains
**311**.

So the vault stayed shut, and that calculation is the reason. It opens once per candidate, and only once.
Spending F4's single use would have bought a number — pass or fail — that meant close to nothing either
way, on a question these data are not large enough to answer. Leaving it shut is not caution; it is the
only reading of the arithmetic that was available.

Finding something real that your own criteria disqualify is the moment a search either holds its shape or
quietly re-writes the bar. This one had to hold twice: once against the scope rule, and once against the
more comfortable option — a profit factor of 1.51, eighteen positive years and a replication on a second
instrument are enough material to declare victory, provided nobody runs the second calculation. The full
calculation, with a script that reproduces every number without touching the sealed years, is in
[`factory/botc_potencia_f4.md`](factory/botc_potencia_f4.md).

## The error I paid for out of my own budget

Three of the twenty F1 cartridges were spent on a filter I designed badly. The condition was "open outside
the overnight range", with the overnight window defined as running until 09:29 — which makes the condition
very nearly impossible to satisfy. It produced zero to one trades per configuration.

The budget was charged anyway. Design errors consume cartridges too, and they are in the ledger, findable
by their result: two entries with one trade each, one with zero. A search that quietly re-runs its own
mistakes for free is not measuring anything. The twenty-configuration budget only means something if a
broken configuration costs the same as a good one.

## What the ledger does, and what it does not do

All 57 configurations plus two harness self-tests are in a 60-line append-only file. Every entry carries
the SHA-256 of the previous one. Editing any past line breaks the chain, and anyone can check:

```bash
python -c "import sys; sys.path.insert(0,'factory'); import harness; print(harness.verify_ledger())"
```

It prints `True` on the published file.

Now the part that matters more than the trick. **A hash chain is tamper-evident, not tamper-proof.** It
catches corruption, partial writes, buggy rewrites, deletions and reordering. It does not stop someone with
disk access from editing an entry, recomputing the chain to the tip, and republishing — the chain verifies
afterwards. In the sibling library there are two tests sitting next to each other that prove exactly this:
one where a full rewrite with recompute passes the chain alone, and one where the same rewrite is caught,
but only by an anchor held by a third party the author does not control. Everything after the latest anchor
is uncovered, always.

So the ledger's real guarantee here is narrower and more useful than "cannot be faked": **the denominator
cannot be quietly edited after the fact.** Running 100 variants and reporting the one that won is the most
common way to lie with a backtest, and the most common way to lie to yourself. That file is the
denominator, in the order it happened, winners and losers alike.

One more line item, pointed at rather than hidden: exactly one entry in the ledger touches the hold-out
period, and it is a fabricated single trade from line 2 — a self-test whose only job was to prove that the
final-exam path writes to the ledger before any real work began. A repository whose argument is "count
everything" does not get to exclude its own awkward rows.

## What "everything failed" actually proves

Not that nobody can make money in futures. Not that markets are efficient in any strong sense. The claim is
bounded and I would rather state it too narrowly than too well:

**In these five families, with explicit rules and realistic retail costs, on the most arbitraged market on
earth, there is no exploitable edge for me with these tools.** The best honest configurations land between
break-even and 1.07 — below any threshold worth continuing on, and a long way from the 1.3 that separates a
tradable strategy from a statistical mirage.

This is what the literature predicts. It is not a discovery. The only thing that is even mildly interesting
is the cost of learning it: one week and $0 out of pocket, with auditable evidence. The predecessor project
learned the same thing over months, with real money, and without a ledger that could have told it what it
had already tried.

The hold-out is still sealed: 2020–2026, six years of the most recent market, never opened. If you pick
this up, that is what you inherit — and the only way to keep it worth anything is to open it once.

## The two repositories

- **[honest-strategy-search](https://github.com/Roberto9210/honest-strategy-search)** — the spec frozen
  before the first backtest, both quality-control reports as generated, the 60-line hash-chained ledger,
  the negative verdict in full, and the harness that enforces the bar and guards the vault. The data itself
  is not there and never was: Databento's and Yahoo's terms do not allow redistribution, so `data/` is
  git-ignored and the exclusion was verified against `git status` before the first commit.
- **[deadman](https://github.com/Roberto9210/deadman)** (`pip install deadman-kit`) — the same discipline as
  a library: execution-safety primitives that stop instead of guessing. Zero runtime dependencies. Each
  primitive is documented with the specific bug that motivated it, including a config key that did not exist
  being read with a default of 100, which turned the per-trade risk cap into a fixed $2 for months; a paper
  run that reported +$0.29 gross as "the result" while the net of fees was negative; and a feed-freshness
  check that read a key no producer ever wrote, so it always reported NOMINAL.

Neither repository will make anyone money. One of them is a record of not finding an edge. The other is a
record of the ways a system can lie to you about what it just did.

# Betting Guide

Live-play reference for `cfb_edge.py`. Read before firing on any game. Companion docs:
`README.md` (install, diagrams, honest expectations), `CLAUDE.md` (conventions).

> **Status 2026-09-20: PAPER ONLY.** On 578 settled paper bets (2025 season backfilled +
> 2026 live) no bucket has a 95% CI above zero, the flagged spread side covers 49% against a
> 52.4% break-even, and the "STRONG" plays are the *worst* ones. `LIVE_STAKES = False` in
> `cfb_edge.py` prints that on every board. Everything below describes what the tool flags
> and paper-logs; none of it is a reason to place a real ticket until `analysis/` says so.

## 1. The signals — trust ladder

| # | Signal | Compares | Fires | Trust |
|---|---|---|---|---|
| 1 | **ATS** | FPI predicted margin vs DK spread | Δ ≥ 3 (lean) / 5 ≤ Δ < 8 (STRONG) / Δ ≥ 8 (capped at lean, ⚠overreach) | primary |
| 2 | **ML** | FPI win prob vs de-vigged DK moneyline | +8% (value) / +20% (STRONG); dogs +100..+150 never staked | primary when the spread is tiny or the dog is live |
| 2b | **just win** | favourites FPI and DK agree on (report §0b) | FPI ≥ 60%, ML −250..−110, FPI ahead of fair by 0..+20%, +EV at the vigged price, no steam against | the "who wins at a holdable price" question; own paper bucket since 2026-09-26, no record yet |
| 3 | **line move** | DK opener vs current | ≥ 3 pts | information only — the market learned something |
| 4 | **total steam** | DK total opener vs current | ≥ 2.5 pts | information only — no totals model |

FPI is a real model with a public track record. The market is also a model, with money
behind it. When they disagree by a lot, one of them is wrong. On 795 games the answer is
the market: the FPI side covers 48.4%, and 41% when the gap is 8+ points. A big Δ is a
reason to ask what the market knows, not a reason to bet.

## 2. What to fire on

Nothing, with real money, as of 2026-09-20. The paper ledger fires on:

1. **STRONG ATS** (5 ≤ Δ < 8) on an FBS-vs-FBS game. Δ ≥ 8 is demoted to lean.
2. **ML value / STRONG ML** outside the dead zone (+100..+150) and inside −300..+400.
3. **Just win** sides (report §0b), logged as their own kind so the loop can grade the
   "favourite at a holdable price" idea separately from the outlier idea.

The old "three confirmations" (STRONG ATS + steam with + ML on the same side) was tested
on the 2025 season and did not survive: steam toward the FPI side covers 47.9%, steam
against it 52.6%. The line moving your way is not confirmation. The 2026-09-12 examples
that used to sit here (Syracuse −3.5, Δ 8.1; Middle Tennessee +13.5, Δ 9.3) both lost.

## 3. What to skip

- **⚠market-moved-against** — the line moved ≥ 1.5 pts *away* from FPI. Somebody knows
  something FPI doesn't (QB out, weather, suspension). Skip unless you know the reason and
  disagree with it.
- **FCS opponents** — never ranked, never staked, ATS *or* ML. FPI's FCS rating is generic.
- **⚠blowout-number** — spreads of 28+ are about garbage time, not team strength.
- **⚠long-dog** — ML dogs beyond +250 are capped at "value"; beyond +400 never staked.
  Variance eats small bankrolls.
- **⚠overreach** — Δ ≥ 8. FPI is most wrong exactly where it disagrees most (42.5% cover
  on 40 bets). Capped at lean, never STRONG.
- **⚠dead-zone-dog** — ML dogs +100 to +150. 30% hit, −33% flat ROI on 63 bets. Strength 0,
  never staked. Yesterday's 0-for-5 (2026-09-19) was five of these.
- **Totals** — we have no model. Steam on a total is a reason to look at the weather, not
  to bet.

## 4. Sizing

- `$Bet` = quarter-Kelly on the model's probability, **capped at 5% of bankroll**, $1 min.
  It is what the paper ledger logs. With `LIVE_STAKES = False` it is not a ticket.
- 3–5 tickets per Saturday. More than that and you're betting the noise.
- Default bankroll in the tool is $100; pass `--bankroll` for yours.
- Log every real ticket with `--bet` the moment you place it. Run `--settle` Sunday.

## 5. Soccer (`soccer_edge.py`) — the inverted ladder

- **Only small disagreements get a paper stake.** Elo vs the de-vigged DK three-way:
  +8% to +15% is STRONG 3W, +15% to +20% is 3W value, ≥ +20% is ⚠overreach and never staked.
  On 287 bets the hit rate fell in every band as the edge grew (44% → 34% → 33% → 28% → 23%).
- **Dogs beyond +250: never** (21% hit on 95). **Draws: shown, never staked** — the model's
  draw ceiling is 26%, so a draw only shows edge when the book prices it past +250.
- **⚠unrated** (either side has < 8 results in the table): never.
- Board columns: `DK H/D/A`, `Elo H/A`, `Model H/D/A`. The STRONG rows are the ones where the
  model and the market *almost* agree.

## 6. NHL props (`nhl_edge.py`) — 2026-27, paper from opening night

- **What is projected:** shots, points, goals, assists, blocks, PP points, goalie saves.
  Since 2026-09-30, a skater's projection is a per-minute rate × projected minutes:
  - The rate is this season plus last season (weighted), regressed toward the forward or
    defence mean. Goals regress the most (694 ghost minutes) and shots the least (86).
  - Minutes lean 56% on the last five games.
  - Then × opponent allowance^β, √h at home and ÷√h away → Poisson P(over). Shots are
    gamma-Poisson k=17.5 and saves k=20.
  - Goalie saves keep their per-start recipe.
- **Trust order:** tested walk-forward on 36,401 skater-games of 2025-26 (from 2024-25, out of
  sample), the new recipe beats the old one at every line of every stat and is calibrated
  (bins with 500+ games within 2 pp):
  - **shots** and **points** first (beat naive by 0.067 / 0.045);
  - then **assists**, **PPP** and **goals** (0.033 / 0.055 / 0.019; goals are the most luck);
  - **saves last**: beat naive by 0.024 with a real prior season, still capped at value
    (⚠saves-model).
- **The first ten games are where the old recipe was worst** (goals 0.4128 → 0.3922, points
  0.6087 → 0.6006). Last season's hot streak is not this season's rate, and the market knows
  it. Opening night (old recipe) priced overs about 3 pp too high; the new recipe does not.
- **The lock, and five good ones:** the prop side the projection *and* the de-vigged line both
  favour, −250..−110, model over fair by 0..+20%, never saves or ⚠thin. They're ranked by the
  **blend** (25% model, 75% market), the best guess at the chance to cash. Paper-logged as kind
  `agree` (truth_p = the blend).
  - **Read the EV column.** At −220..−250 it is usually negative at the blend. On 2026-09-30
    none of 346 prop sides was +EV. These are the likeliest winners, not value bets.
  - **Read the miss line.** A 69% lock misses about 3 nights in 10: 84% to miss at least once
    in a five-night week. One miss says nothing about the model.
- **Read the card simulation before playing the lock + five together:** at −200..−250 you need
  about five of six just to be up. The report runs it three ways (model, blend, market). If
  the blend is right, a typical card finishes up about a third of nights.
- **Tiers:** +8% value, +15% STRONG, ≥ +30% ⚠overreach never staked (borrowed from what CFB
  and soccer both showed). Price window −250..+250. ⚠thin (< 10 games) never. Goalie flagged
  ⚠not-starter never — check the confirmed starter yourself two hours before puck drop.
  Opening night's +15–30% band cashed 27% under the old recipe; under the new one the same
  night's band cashed 60% (n=30). One night each, so the tiers stay priors until
  `analysis/06` B says otherwise.
- **Lines:** `.env` with `ODDS_API_KEY=…`, or a `--lines-file` CSV.
  - The Odds API free tier is 500 credits a month at about **5 credits per game per run**
    (one per market returned), so a 10-game night is ~50 and the free tier covers roughly
    ten nights.
  - With neither, DraftKings' two-sided player totals come from ESPN's keyless `propBets`
    feed (SOG, points, assists, blocks, saves).
- **No historical prop prices exist**, so there is no ROI backtest against lines. The ledger
  started 2026-09-29. `analysis/06` A/B grade it by kind and recipe, and E scores every
  snapshotted line against the result: model vs market, and the blend curve that will fit
  `BLEND_MODEL_W`.

## 7. Discipline — the horses lessons carry over

- **No signal has beaten a market until the backtest says so** with a confidence interval
  that clears zero. On 795 games and 578 paper bets nothing does; the flagged spread side is
  below break-even. That is why stakes are paper only.
- **Simulate before you change a rule.** `analysis/04_deep_dive` shows hit % and ROI by
  edge band, price band, |spread|, home/away and calibration. A rule change that is not
  visible there is a hunch.
- **The losers count.** The analysis "settled" rule is completed game + both scores.
  Nothing filters on a result column that could hide losses.
- **Re-run the loop weekly**, both runtimes, before changing a threshold.
- Take the closing-line-value view seriously: if the plays we flag Thursday consistently
  close *further* from FPI on Saturday, the market disagrees with us and it is usually right.

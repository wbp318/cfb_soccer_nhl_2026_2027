# Changelog

All notable changes to `cfb_edge.py` and the analysis loop. Rule changes cite the analysis
run that justified them; nothing in the constants block changes without one. Weekly report
releases (`<weekday>-<date>` tags) are not listed here; see the GitHub releases page.

## [2026-09-30 night] — Session write-up expanded

- `nhl_rebuild_session_2026-09-30.md` rewritten in far more detail, from the same transcript: how each model call
  is assembled, token routing, the prompt cache (every write on the 1-hour lifetime, zero misses in 168 calls),
  parallel tool calls (33 replies, 41 round trips and ~12.3M re-read tokens saved), tool result sizes and waits,
  background jobs, the effort level (max on every call), thinking bursts, Claude Code's own cost counter, and all
  nine tool errors with their exact causes. 28 Mermaid charts, all parsing.
- README Files table describes the expanded write-up.

## [2026-09-30 evening] — Session write-up; a time in the entry below corrected

- `nhl_rebuild_session_2026-09-30.md`: how the NHL rebuild below was done, written from the
  session's Claude Code transcript. It covers the timeline, per-phase token accounting (138 model calls,
  45.3M tokens processed, 98.9% prompt-cache reads) and every mistake along the way with how it
  was caught.
- **Fix:** the entry below said the first 2026-09-30 report and its paper rows were written at
  16:40. The `props` table stamps that snapshot 16:37:17, so both mentions now say 16:37. The
  `rules-2026-09-30` release body was re-published from the corrected entry.
- README Files table lists the write-up.

## [2026-09-30] — NHL projection rebuilt, lock ranked on a model–market blend, analysis/06 rewritten

### Why
- **Opening night (2026-09-29, old recipe) missed in a pattern, not just on the lock.** The
  lock (Suzuki over 0.5 PTS −230) lost, and the lock + five went 3 of 6. After `--settle`
  the 187 paper props were −24.1% flat (`analysis/06` A says "losing", but they came from
  four games and are not independent, so that interval is too narrow). Value-board overs
  cashed 33.7% against a model average of 54%, and the +15–30% edge band cashed 27.4%
  [18, 39] (B1).
- **Every snapshotted line graded, not just the flagged ones** (282 lines, `06` E): the
  de-vigged market beat the model, log-loss **0.6476 vs 0.6667**. Mean P(over) was 0.446
  (model) vs 0.428 (market) vs 0.355 observed, so the model ran high on overs, most on
  points (0.486 vs 0.456).
- **Root cause.** The old recipe took last season's per-game mean at face value (no
  regression to the mean, per game rather than per minute), and it had never been tested with
  the prior it actually uses: `--calibrate` walked a different recipe (league-average
  shrink, no prior season).

### Changed — `nhl_edge.py`
- **Skater projection** (`position_means`, `skater_projection`, `skater_rates`): a per-minute
  rate × projected minutes.
  - *Minutes* = (this season's TOI + `TOI_PRIOR_W` 0.09 × last season's + `TOI_GHOST` 0.6
    ghost games at the position mean) ÷ games at the same weights, then `TOI_RECENT_W` 0.56
    toward the last `TOI_RECENT_GAMES` 5 once the season has a game.
  - *Rate per minute* = (this season + a1 × last season + K ghost minutes at the forward or
    defence rate) ÷ (minutes at the same weights).
  - λ = rate × minutes × (opponent allowance ÷ league, clamped 0.80–1.20)^β × √h at home,
    ÷ √h away.
  - `SKATER_MODEL` (a1, K, β, h):

    | stat | a1 | K | β | h |
    |---|---|---|---|---|
    | shots | 0.35 | 86 | 0.84 | 1.037 |
    | points | 0.58 | 234 | 0.70 | 1.078 |
    | goals | 0.81 | 694 | 0.64 | 1.077 |
    | assists | 0.58 | 355 | 0.73 | 1.078 |
    | PPP | 0.31 | 50 | 0.59 | 1.115 |
  - a1, K, β and the TOI weights were fit by Nelder–Mead on 2024-25 (prior 2023-24), by
    full-count likelihood over skaters with ≥ 20 games at ≥ 12 minutes the season before.
    The fit also said the season before last adds nothing once minutes are modelled (weight
    ≈ 0). h is not a fit: it is the league home/away ratio pooled over 2024-26 (`06` C0),
    because the fit season's 1.11 for points fell to 1.045 in 2025-26.
- `DISPERSION` adds **shots k = 17.5** (full-count fit; Poisson over-called over 1.5 by
  1.1 pp). Points, goals, assists and PPP stay Poisson. Saves stay k = 20.
- `opponent_factors`: per-stat exponent β and a symmetric home split (was: the full ratio ×
  1.02 on home games only). `HOME_FACTOR` is gone.
- Goalie saves keep the per-start recipe, now in `goalie_rate` so the backtest calls it.
- **`--build`** adds `HISTORY_SEASON` (2024-25) and `fetch_league_players`. Everyone who
  played a finished season (stats API `skater|goalie/summary`) is stored with `team` NULL,
  so position means and the backtest aren't survivors-only. `db_players` skips them.
  - Finished (player, season) pairs are fetched once; players off every roster lose their
    team.
  - **Fix:** the game-log write is now an upsert that keeps `blocked`. `INSERT OR REPLACE`
    wiped the blocks `--settle` stores, so blocks could never get a rate.
- **`--calibrate`** rewritten on `backtest()`. It walks 2025-26 forward from 2024-25 with
  team allowances rebuilt from the logs as of each date, calling the live
  `skater_projection` / `goalie_rate` / `opponent_factors`. It reports log-loss vs naive at
  1.5/2.5/3.5 SOG, 0.5/1.5 PTS, 0.5 G/A/PPP and 24.5/27.5 SV, plus bias, the first ten
  games, reliability bins and the dispersion grid. It runs in about 3 s.
- **The lock + five** rank on `BLEND_MODEL_W` = 0.25: a logit blend of the model with the
  de-vigged line, the market carrying 75%.
  - This is a prior, not a fit: the market has been sharper in every sport, and on opening
    night by 0.019 log-loss.
  - Agree signals carry `truth_p` = the blend, with `model_p` and `fair_p` alongside.
  - Rows show model · fair · blend and the EV at the blend, plus a miss-rate line under the
    lock.
  - `simulate_card` gains a third source, `blend`.
- `TEAM_RHO` 0.107 / 0.055 → **0.1047 / 0.0525** (`06` D over the whole league, 802,876
  teammate pairs; it was 710,554 survivors-only).
- `MODEL_VERSION` = "2026-09-30" is stamped on every `props` / `paper_bets` row (`MIGRATIONS`
  add a `model` column; NULL = the 2026-09-20 recipe). The 196 prop rows and 125 paper bets
  written at 16:37 before the column existed were tagged by a one-off `UPDATE` on the local
  DB (`taken_at >= 2026-09-30`).
- `FINDINGS_AS_OF` 2026-09-20 → 2026-09-30.

### Evidence — `analysis/06` run 2026-09-30
Python == R: max |Δ| 4.9e-15 over all seven CSVs (217 rows); the printed tables are
identical apart from bootstrap CIs. `nhl_edge.py --calibrate` matches C at every printed
digit.

C, out of sample: 2025-26 walked forward from 2024-25, over 36,401 skater-games and 2,090
goalie starts. Log-loss:

| line | live | old | naive | first 10 games: live vs old |
|---|---|---|---|---|
| SOG 1.5 | **0.6130** | 0.6177 | 0.6780 | 0.6108 vs 0.6181 |
| SOG 2.5 | **0.4817** | 0.4859 | 0.5487 | 0.4599 vs 0.4663 |
| SOG 3.5 | **0.3094** | 0.3129 | 0.3656 | 0.2908 vs 0.2957 |
| PTS 0.5 | **0.6092** | 0.6154 | 0.6544 | 0.6006 vs 0.6087 |
| PTS 1.5 | **0.2970** | 0.3007 | 0.3341 | 0.2799 vs 0.2840 |
| G 0.5 | **0.4112** | 0.4221 | 0.4298 | 0.3922 vs 0.4128 |
| A 0.5 | **0.5466** | 0.5544 | 0.5796 | 0.5383 vs 0.5488 |
| PPP 0.5 | **0.2717** | 0.2778 | 0.3267 | 0.2760 vs 0.2847 |
| SV 24.5 / 27.5 | **0.6700 / 0.5923** | (same recipe) | 0.6932 / 0.6168 | |

- Every reliability bin with 500+ player-games sits within 2 pp.
- **Ablation** at the main line:
  - no regression: goals 0.4153, PPP 0.2760, assists 0.5481, points 0.6098;
  - no opponent factor: shots 0.4831;
  - no recent minutes: worse for every stat (points 0.6104);
  - no home split: ≤ 0.0002 either way.
- The ablation's K × 0.5 ties the live K for points (0.6091 vs 0.6092); the fitted K stays.
- h is measured over both seasons, so it isn't out of sample for 2025-26; switching it off
  moves log-loss by ≤ 0.0002.
- E (opening night, old recipe): market 0.6476 vs model 0.6667 over 282 lines. The logit
  blend was best at w = 0 for that recipe.
- A one-off re-projection of opening night with the new recipe (no 2026-27 data) covered
  266 skater lines:
  - log-loss **0.6427 vs the market's 0.6437**;
  - mean P(over) 0.419 vs 0.424, observed 0.342;
  - average distance from the market 4.1 pp (was 5.6).
- Its edge bands that night: 0–8% cashed 46.7% (n 120), 8–15% cashed 46.0% (63), 15–30%
  cashed 60.0% (30). That's one night each way, so **the tiers stay priors, unchanged**.

### Tonight (2026-09-30), the first slate on the new recipe
- The report was first generated at 16:37 with h fit on 2024-25 (1.042 / 1.133 / 1.127 /
  1.136 / 1.168) and `TEAM_RHO` 0.107 / 0.055, then re-issued at 16:52 on the final
  constants. The second version is the one released.
- The lock is **Quinton Byfield under 0.5 A −245 (DK)**: model 76%, fair 67%, blend 69%, EV
  −2.6%.
- The good five are Rielly u0.5 A, Landeskog u0.5 A, Clarke u0.5 A, Necas u1.5 PTS and
  Drysdale u0.5 A.
- The card simulation at the blend: 4.04 of 6, P(up) 36%.
- No prop side on the slate was +EV at the blend.
- Both snapshots are in the ledger (`db_paper_log` dedupes by game, player, market and kind).

### Docs and tests
- **README:**
  - The NHL section is rewritten. The worked example is tonight's lock with every number
    from the live code, and the section adds the backtest table, the market check, the
    simulations refit, the ER diagram with `model`, the NHL week and the honest status.
  - The top-level and analysis diagrams, the Files table and the Roadmap are updated.
  - The Odds API cost is corrected from "a 10-game night costs 11" to about **5 credits per
    game per run** (30 credits for two 3-game runs today).
- **Other docs:** `analysis/README.md` (layout diagram, loaders, 06 A–E), `betting_guide.md`
  §6 and `CLAUDE.md` are updated. All 28 Mermaid blocks parse (mermaid 11.17).
- **`analysis/_shared/load_nhl.{py,R}`** add `load_logs(seasons)` and `load_market_lines()`,
  and bets carry `model`. `06` adds A `recipe:` rows, C0, the C backtest and ablation, and E.
  The new outputs are `nhl_backtest.csv`, `nhl_grid.csv` and `nhl_market.csv`.
- **Tests: 85 → 89.** New tests cover the position means, the recipe by hand, player rates
  with settled blocks, the upsert keeping blocks, history players never matching, and the
  blend. The opponent-factor and simulation tests are rewritten.

## [2026-09-29 late] — License covers the simulations and pick boards

- `LICENSE` and the README license section now name the gamma-Poisson dispersion fit, the
  same-game correlation estimates, the Monte Carlo card simulation, and the pick boards
  (just-win, agreement, lock + five); section 2 adds simulations and picks to the outputs that
  can't be used without a license. Terms unchanged: proprietary, all rights reserved, view
  only, commercial licenses available.

## [2026-09-29 evening] — NHL simulations: gamma-Poisson saves, card Monte Carlo, analysis/06 D

### Added
- **Rate uncertainty** (`nb_cdf`, `count_cdf`, `p_over(..., disp)`, `DISPERSION`,
  `DISPERSION_GRID`): a player's rate is Gamma(shape k) around the projection, the count
  Poisson(λ), which is negative binomial in closed form (a test checks it against 200k simulated draws).
  `--calibrate` now prints the log-loss for every k. Walk-forward 2025-26: shots best at ∞
  (Poisson), points flat (0.6096 at ∞ and 50), **saves 0.6131 → 0.6032 at k = 20** (naive
  0.6162). So `DISPERSION = {"saves": 20}`; skaters unchanged. `SAVES_MAX_STRENGTH` stays 1
  until the ledger speaks.
- **`simulate_card`**: 20,000-night Monte Carlo of the lock + five (seed 20260929). Each ticket
  keeps its own probability; teammates correlate through a one-factor Gaussian copula at
  `TEAM_RHO` (points 0.107, assists 0.055; opponents independent). Run under the model's
  probabilities and under the de-vigged market; reports expected hits, P(all), P(≥ n−1),
  flat-$1 mean / P(up) / 5th–95th, and parlay EV. In the terminal under the lock and in the report
  as **Simulated 20,000 nights of that card**. Opening night: model 4.45/6 hits, P(up) 51%,
  +$0.42; market 3.89/6, P(up) 31%, −$0.38.
- `analysis/06_nhl` (Python + R): C gets the dispersion grid (and the model row uses k = 20 for
  saves); new **D. same-game correlation**: pooled Pearson r of "had ≥ 1" over 710,554
  teammate pairs and 752,208 opponent pairs, closed form from per-team sums, latent
  ρ = sin(πr/2). Points r 0.0684 (ρ 0.1073), assists r 0.0350 (ρ 0.0549), opponents −0.008 /
  −0.004. Output `nhl_correlation.csv`. **Python == R: max |Δ| 8e-15 (calibration), 3e-16
  (correlation)**; both run clean on an empty DB.
- `numpy` added to `requirements.txt` (the card simulation). Tests
  `test_nb_cdf_matches_simulated_gamma_poisson_and_tends_to_poisson`,
  `test_simulate_card_keeps_marginals_and_correlates_teammates`; the saves signal test moved
  to line 24.5 because k = 20 widens the distribution (85 cases).
- README: a Simulations section with its own diagram, an updated calibration table, and
  updates to the architecture, flag-flow, analysis and CI diagrams. `analysis/README.md`,
  `betting_guide.md` and `CLAUDE.md` updated too.

### Why
- The user asked for simulations. The honest outcome: rate uncertainty only helps saves, and the
  card simulation shows the lock + five is a coin flip to finish up even if the model is right.

## [2026-09-29] — NHL opening night: lock + five, DraftKings via ESPN, `agree` bucket

### Added
- **`agree_signal` / `agree_board` / `lock_and_good` / `render_lock`** in `nhl_edge.py`, and a
  report section **The lock, and five good ones** above §1. The football just-win idea applied
  to props: the side the projection and the de-vigged line both call > 50%, priced −250..−110
  (`AGREE_MIN_PRICE` / `AGREE_MAX_PRICE`), model over fair by 0..+20% (`AGREE_MAX_GAP_PCT`,
  because every run so far says bigger gaps lose), never saves (weakest projection), never
  ⚠thin. Ranked by model chance to cash, best book per player × market. Good picks are the
  rest of that board, then the value board, one per player (`GOOD_PICKS_N = 5`).
- Agreement plays are paper-logged as kind **`agree`** (strength 1). `db_paper_log` now dedupes
  per (game, player, market, **kind**) so an agree play and a value play on the same prop both
  count. **No track record yet**; `LIVE_STAKES` unchanged.
- **`fetch_props_espn`**: DraftKings two-sided player totals (SOG, points, assists, blocks,
  saves) from ESPN's keyless core `propBets` feed, used when there is no `ODDS_API_KEY` and no
  `--lines-file`. Pairs arrive Over first with no side label; checked on the opening-night
  feed (Matthews 0.5 PTS −195 / +145, Ekman-Larsson +230 / −320). One-sided markets
  (milestones, scorer props) are skipped because they can't be de-vigged.
- `analysis/06_nhl` (Python + R): loaders select `kind`; section A prints `kind:prop` and
  `kind:agree` rows, and the market × side × strength buckets are the value board only.
  Checked on a scratch copy of the ledger with fake grades: point estimates identical in
  both runtimes, bootstrap CIs within the last digit; both run clean on an empty DB.
- Tests: `test_agree_signal_window_and_gap`, `test_lock_and_good_one_per_player`,
  `test_fetch_props_espn_pairs_over_then_under`, `test_paper_log_keeps_agree_and_prop_buckets_apart`
  (83 cases).

### Fixed
- `SEASON_START` was 2026-10-07; the NHL regular season opened **2026-09-29** (schedule API,
  gameType 2). Docs updated.

### Why
- Opening night, and the user asked for one lock and five good props: winners, not outliers.
  Sanity check before publishing: the lock (Suzuki over 0.5 PTS, model 76% vs fair 65%) had a
  point in 77% of his 82 games in 2025-26, so the gap is not a rate bug.

## [2026-09-26] — Just-win board (football)

### Added
- **`just_win_signal` / `just_win_board` / `render_just_win`** in `cfb_edge.py` and report
  section **0b. Just-win board**. The opposite question from the outlier board: who is going
  to win outright at a price worth holding. A side qualifies when FPI gives it ≥ 60% to win
  (`JUST_WIN_MIN_P`), the market also favours it, the moneyline is in −250..−110
  (`JUST_WIN_PRICE`), FPI is ahead of the de-vigged price by 0..+20%
  (`JUST_WIN_MAX_EDGE_PCT = ML_STRONG_PCT`, because every run so far says bigger gaps lose),
  the ticket is +EV at the vigged price, both teams are FBS and the spread has not moved
  ≥ 1.5 pts against it. Ranked by FPI win probability; the report bolds the top 5
  (`JUST_WIN_N`). Printed after the picks board in the terminal too.
- Every qualifying side is paper-logged as kind `just-win` (strength 1, graded like a
  moneyline) so `analysis/01` gets its own bucket. **No track record yet**; `LIVE_STAKES`
  unchanged.
- **Report opens with “The lock, and five good ones”** (`lock_and_good`, `GOOD_PICKS_N = 5`):
  the lock is the top of the just-win board; good picks are the rest of that board, then the
  picks board in rank order, one per game. Same-day refresh release `saturday-2026-09-26-HHMM`.
- Tests `test_just_win_board_favourites_at_a_holdable_price` and
  `test_lock_and_good_picks_lead_with_just_win_then_outliers` (79 cases). README signal table
  and both football diagrams, `betting_guide.md` §1–§2, `CLAUDE.md` updated.

### Why
- The user asked for "winners with a decent line", not outliers. First cut of 2026-09-26
  ranked five; Mississippi State −230 showed FPI 67% vs fair 67% and −3.3% EV, so the +EV
  gate was added and it dropped to four honest sides.

## [2026-09-20h] — Every language counts on the GitHub language bar

- `.gitattributes` rewritten: every extension linguist would hide as documentation, data or
  configuration is now `linguist-detectable` with an explicit language — Python, R, RMarkdown,
  Jupyter, SQL, JavaScript, TypeScript, HTML, CSS, Batchfile, PowerShell, Shell, YAML, TOML,
  JSON, INI, CSV, Text, Markdown, Dockerfile, Makefile, plus `.gitattributes` and `.gitignore`
  themselves. `.github/`, `reports/`, `analysis/` and `tests/` are un-vendored and
  un-generated. Line endings pinned to LF, CRLF for `.bat`, `.cmd`, `.ps1`. Linguist language
  names with spaces use the hyphenated aliases (git rejects quoted values). README files table
  gained the row.

## [2026-09-20g] — License covers all three tools

- `LICENSE` and the README license section now name `soccer_edge.py`, `nhl_edge.py`, the R
  scripts, `CHANGELOG.md`, the projection and Elo models, and player props explicitly. Terms
  unchanged: proprietary, all rights reserved, view only, commercial licenses available.

## [2026-09-20f] — analysis/06: the NHL analysis loop (Python + R)

### Added
- **`analysis/06_nhl/nhl_loop.{py,R}`** + `_shared/load_nhl.{py,R}`. A. prop ROI by market ×
  side × strength with bootstrap CI and B. slices by edge band / market / side (both empty until
  2026-10-07); C. walk-forward projection calibration on the 46,551 stored game-log rows,
  re-implementing the shrinkage + recent-10 + Poisson recipe in both runtimes. All 27
  calibration rows agree to 1e-15 and match `nhl_edge.py --calibrate`: shots log-loss 0.4742
  vs naive 0.5397, points 0.6097 vs 0.6543, saves 0.6131 vs 0.6162. CI runs both against an
  empty `CFB_NHL_DB`.

### Docs
- README: overview, inside-analysis, analysis-loop, weekly-loop, NHL-week and CI diagrams show
  `06`; running blocks, NHL status, roadmap and file table updated. `analysis/README.md`
  (layout, diagram, running, wiring-back), `CLAUDE.md`. 27 Mermaid blocks parse.

## [2026-09-20e] — NHL player-prop module, repo renamed to cfb_soccer_nhl_2026_2027

### Added
- **`nhl_edge.py`** for the 2026-27 season: skater SOG / PTS / G / A / BLK / PPP and goalie
  SV props. `--build` stores rosters (32 clubs, 1,286 players) and game logs for 2025-26 and
  2026-27 from the NHL public API (46,551 rows). Projection = current-season rate shrunk to
  last season (20 games) with a 35% tilt to the last 10, × opponent shots/goals allowed vs
  league (clamped 0.80–1.20), × 1.02 at home → Poisson P(over), push-conditioned on whole
  lines. Lines from The Odds API (`ODDS_API_KEY` env / `.env`) or `--lines-file` CSV;
  DraftKings' API returns 403. Signals +8% value / +15% STRONG / ≥ +30% ⚠overreach;
  ⚠thin < 10 games; ⚠saves-model caps goalie saves at value; ⚠not-starter. `--settle`
  grades from boxscores (PPP from the game log) and stores blocked shots.
- **`--calibrate`**: walk-forward on 2025-26 with no prior season (harder than live). Shots
  over 2.5: log-loss 0.4742 vs naive 0.5397, bins within 2 pp. Points over 0.5: 0.6097 vs
  0.6543. Saves over 27.5: 0.6131 vs 0.6162 — barely better, miscalibrated at both ends,
  hence the cap. No historical prop prices exist, so ROI is untested until the season.
- `tests/test_nhl_edge.py` (12 cases, no network); CI compiles, lints, tests, `--help`s and
  bootstraps `nhl_ci.db`. Opening-night projections report `reports/nhl-wednesday-2026-10-07.md`.

### Changed
- Repo renamed **`cfb_pro_soccer_2026` → `cfb_soccer_nhl_2026_2027`** (GitHub redirects).
  Local folder unchanged. Repo description updated.
- README: title, intro, quick start, clone URL, overview diagram (NHL subgraph), new "NHL
  player props" section with flags, data-source, worked-projection, ER and weekly diagrams
  plus the calibration table; files and roadmap. `CLAUDE.md`, `betting_guide.md` (new §5
  soccer, §6 NHL), `analysis/README.md`.
- Diagrams: overview guard-rail and CI blocks now say 77 tests (47 football · 18 soccer ·
  12 NHL) and list all three modules in the compile step. 27 Mermaid blocks parse.

## [2026-09-20d] — Soccer strategy inverted: small edges only

Sunday 2026-09-20 live: 58 settled soccer paper plays went 16-42 (−$17.71 on $123). Re-ran
`analysis/05` on 287 bets (Python == R).

### Changed (rules — from analysis/05, 287 bets)
- **Tiers inverted.** `[8%, 15%)` → STRONG 3W (44% hit, +3.4% flat, n=66 — the only band
  near break-even); `[15%, 20%)` → 3W value (34%); `≥ 20%` → strength 0, ⚠overreach
  (n=177, 29% hit, −13%). Hit rate fell monotonically with edge across five bands, the same
  shape football's Δ8+ showed. Constants: `EDGE_STRONG_MAX`, `EDGE_VALUE_MAX`,
  `EDGE_OVERREACH_PCT`; `ML_STRONG_PCT` removed.
- **Dogs beyond +250 never staked** (95 bets, 21% hit, −12%); was "cap at value".
- Draws: unchanged rule, but with the model's 26% draw ceiling a draw only shows edge past
  +250, so draws are never staked in practice. Test renamed to say so.
- `ELO_HFA` / `DRAW_BASE` unchanged (grid optimum). Tests updated (fixture default now sits
  in the STRONG band). README soccer status table and signal diagram updated.

## [2026-09-20c] — analysis/05: the soccer analysis loop (Python + R)

### Added
- **`analysis/05_soccer/soccer_loop.{py,R}`** + `_shared/load_soccer.{py,R}`. One script,
  four sections: A. 3-way paper ROI by pick × strength with 5,000-rep bootstrap CI; B. hit %
  and flat ROI by edge band, price band, pick (Wilson); C. Elo calibration bins for
  P(home)/P(draw)/P(away) and 3-way log-loss of the model vs the de-vigged closer; D. refit of
  `ELO_HFA` × `DRAW_BASE` by held-out log-likelihood on the full results table (Elo replay
  re-implemented in both runtimes). CI runs both against an empty `CFB_SOCCER_DB`.

### Findings (first run, 229 backfilled bets / 374 settled snapshots / 39,583 results; Py == R to 1e-14)
- Flat ROI **−9.6%** [−27%, +9%], inconclusive. STRONG +3.6% (n=88), value −17.8% (n=141).
- **Bigger edge, worse hit**: 8–15% → 47.3%; 20–30% → 31.4%; 50%+ → 24.3%. Football's shape.
- Elo home win-probs run 7–9 pp high in the 40–70% bins; away the same; draws about right.
- **The closer is sharper**: 3-way log-loss Elo 1.0555 vs de-vigged closer 1.0207.
- **Priors confirmed**: HFA 60 / DRAW_BASE 0.26 is exactly the grid optimum (HFA 0–120,
  draw 0.20–0.32) on the held-out second half of the results table. No constant changed.

### Docs
- README: soccer "Honest status" is now a findings table; overview, analysis, analysis-loop,
  weekly-loop and CI diagrams show `05`; running blocks and file table updated.
  `analysis/README.md`, `CLAUDE.md` updated. Report footer and constants comment in
  `soccer_edge.py` cite the run.
- Deep soccer detail in README: nine new Mermaid diagrams (flags, data sources, the Elo
  exactly, three-way arithmetic on a real match, soccer ER, the soccer week, inside `05`,
  Sunday coverage funnel) plus an analysis map in `analysis/README.md`. Football flag diagram
  now shows the banner and the new demotions. All 22 blocks parse under Mermaid 11.

## [2026-09-20b] — Pro soccer module, repo renamed to cfb_pro_soccer_2026

### Added
- **`soccer_edge.py`**: pro soccer outlier finder for every league ESPN lists (219 in the
  catalogue) and DraftKings prices. ESPN publishes no predictor for soccer, so the model is a
  self-built Elo table: `--build-elo` stores a year of final scores in `soccer.db` and
  ratings are replayed chronologically (K 20, half for friendlies, HFA 60, goal-difference
  multiplier), never stored, so a backfill uses exactly the rating known on that date.
  Elo → home/draw/away (draw base 26% at parity, shrinking as 4E(1−E)) vs the de-vigged
  DraftKings three-way line. Signals: `ml3` (+8% value / +20% STRONG), `prob-move`,
  `total-move`. Demotions: unrated side (< 8 results) → never staked; draw picks capped at
  value; dogs > +250 capped; outside −300..+400 never. Shares `LIVE_STAKES`, `stake_for`
  and the PAPER ONLY banner with `cfb_edge`. Flags mirror the football tool
  (`--snapshot --report --settle --backfill --top --league --elo-show --paper-show`).
- `tests/test_soccer_edge.py`: 18 cases, no network. CI compiles, lints, tests, `--help`s
  and schema-bootstraps the soccer module too.
- `reports/soccer-<weekday>-<date>.md` report format.

### Changed
- Repo renamed **`cfb_2026` → `cfb_pro_soccer_2026`** (GitHub redirects the old URL). The
  local folder keeps its name so the scheduled task and memory paths still resolve.
- README: title, clone URL, quick start, overview diagram (soccer subgraph), new "Pro
  soccer" section with its own signal diagram and flag table, roadmap and file table.

### Honest status
- No soccer analysis run exists. Every soccer constant is a prior. The paper ledger in
  `soccer.db` and a future `analysis/05_soccer_*` pair decide whether Elo-vs-DK is anything.
- First backfill sample, 2026-09-12/13 (229 paper bets across all leagues, closers + Elo as
  of that day): flat ROI **−14.7%** on $629 staked. STRONG (str 2): 88 bets, 35 W, +3.1%.
  Value (str 1): 141 bets, 44 W, −35%. Two days is not a verdict; it is the reason the
  module is paper only.

## [2026-09-20] — Paper only, overreach cap, ML dead zone, 2025 backfill, analysis/04

Triggered by going 0-for-5 on 2026-09-19 with five ML dogs from the top of the board.

### Fixed
- **bets.csv grading was wrong for every home-side ticket.** `settle_bets` compared the short
  side name typed at `--bet` ("Missouri State") to ESPN's full name ("Missouri State Bears"),
  never matched, and graded every ticket as the away team. The 9/19 ledger showed 3-2 and
  +$16; it was 0-5 and −$24. New `_side_is_home` matches by prefix/substring and refuses to
  grade (leaves the row unsettled, prints to stderr) when the name matches both teams or
  neither. Two regression tests. The 9/12 tickets were graded correctly by luck (all the
  home-side picks lost anyway).

### Added
- **2025 season backfilled** into `data.db`: 16 Saturdays, 775 games, 766 with a DraftKings
  closer and a pre-game FPI projection, flagged `backfill=1`. The paper ledger went from 114
  settled bets to 578. ESPN still serves last season's closers and frozen predictor, so this
  is reproducible with `--date <2025 Saturday> --backfill` on a fresh DB.
- **`analysis/04_deep_dive`** (Python + R, CI-wired): hit % with Wilson 95% CI and flat ROI
  by strength, season, edge band, ML price band, |spread|, dog/fav, home/away, and the
  model's own `truth_p` vs actual hit rate. Point estimates match to the digit across
  runtimes (44 rows). This is the "simulate before you change a rule" script.
- **`stakes_banner()`** printed at the top of the picks board, the top-N board and the report.
- **`CHANGELOG.md`** (this file).

### Changed (rules — from the 2026-09-20 analysis run, 795 games / 578 paper bets)
- **`LIVE_STAKES = False`.** No bucket has a 95% CI above zero; the flagged spread side
  covers 49.3% against a 52.4% break-even. Every board says `STAKES: PAPER ONLY`. Stakes are
  still computed and paper-logged so the sample keeps growing.
- **`SPREAD_OVERREACH_PTS = 8.0`.** Δ ≥ 8 is capped at lean and tagged ⚠overreach. Cover
  rate by edge band: Δ3-5 52.6%, Δ5-8 47.6%, Δ8+ 42.5%. The bigger the FPI-vs-DK gap, the
  more often the market is right.
- **`ML_DEAD_ZONE = (100, 150)`.** Moneyline dogs priced +100 to +150 get strength 0 and
  ⚠dead-zone-dog: 30.2% hit, −33% flat ROI on 63 bets, the worst bucket in the sample.
  All five 9/19 tickets were in it.
- **Line-move gating tested and rejected.** "Steam with FPI" covers 47.9% (n=117), steam
  against 52.6% (n=196). The `[steam with]` tag stays informational; the betting guide no
  longer calls it a confirmation.
- `FINDINGS_AS_OF = "2026-09-20"`.

### Docs
- README "Before you bet" rewritten against the new sample; signals diagram gains the two
  demotions and the `LIVE_STAKES` gate; analysis and CI diagrams show four scripts and 47
  tests. `betting_guide.md` opens with the paper-only status and drops the "three
  confirmations" play. `CLAUDE.md` and `analysis/README.md` updated to match.

### Tests
- 42 → 47 cases: `_side_is_home`, short-name home ML regression, overreach cap, ML dead
  zone, paper-only banner.

## [2026-09-14] — Analysis loop re-run, README table

- Constants unchanged; "Before you bet" table refreshed on 96 games / 70 paper bets.

## [2026-09-09] — First analysis loop, CI, branch protection

- `analysis/01`–`03` in Python and R; `FINDINGS_AS_OF` introduced; `main` protected.
- FCS demotion: either side without an FPI rating is never ranked or staked.

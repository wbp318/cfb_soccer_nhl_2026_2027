# NHL Prop Report — Thursday, October 01, 2026

**Generated:** 2026-10-01 04:49 PM CDT  
**STAKES: PAPER ONLY as of 2026-09-20 — no bucket has a 95% CI above zero. $Bet is what the paper ledger logs, not a recommendation to bet real money.**  
**Slate:** 8 games · 569 prop lines matched to rostered players (The Odds API)  
**Model (skaters, since 2026-09-30):** per-minute rate × projected minutes. The rate is this season's stat per minute blended with last season's (weight a1) and regressed toward the position mean (K ghost minutes: shots 86, points 234, goals 694); minutes lean 56% on the last 5 games. × opponent allowance^β × home/away split → Poisson P(over) (shots: gamma-Poisson k=17.5; goalie saves: old per-start recipe, k=20). Fit on 2024-25, tested on every 2025-26 skater-game: better log-loss than the old recipe at every line of every stat. Tiers +8% / +15%, ≥ +30% demoted (⚠overreach).

## The lock, and five good ones

**The lock** is the top of the agreement board: the prop side the projection and the de-vigged line both favour, priced -250..-110, model above fair by no more than +20%, ranked by the **blend** (25% model, 75% de-vigged line, in logit space: the market has been sharper everywhere so far). **Good** is the rest of that board, then the ranked value props (§1), one per player. EV is at the blend; at −220..−250 the juice usually outweighs what the model adds, so these are the likeliest winners, not value bets. Paper only.

| | Puck (CT) | Game | Play | Why |
|---|---|---|---|---|
| **LOCK** | 6:00 PM | BUF @ CBJ | **Josh Doan under 0.5 A -250 @draftkings** | proj 0.31 → model 73% · fair 67% · blend 69% (EV -3.8% at the blend, agree) |
| good 1 | 8:00 PM | SEA @ CGY | Brandon Montour under 0.5 A -245 @draftkings | proj 0.31 → model 73% · fair 67% · blend 68% (EV -3.8% at the blend, agree) |
| good 2 | 6:00 PM | BUF @ CBJ | Jack Quinn under 0.5 A -250 @draftkings | proj 0.34 → model 71% · fair 67% · blend 68% (EV -5.0% at the blend, agree) |
| good 3 | 9:00 PM | FLA @ SJS | Matthew Tkachuk under 0.5 G -250 @fanduel | proj 0.34 → model 71% · fair 67% · blend 68% (EV -5.1% at the blend, agree) |
| good 4 | 7:00 PM | MIN @ NSH | Steven Stamkos under 0.5 A -235 @draftkings | proj 0.30 → model 74% · fair 65% · blend 68% (EV -3.5% at the blend, agree) |
| good 5 | 8:30 PM | CHI @ UTA | Bowen Byram under 0.5 A -250 @draftkings | proj 0.35 → model 70% · fair 67% · blend 68% (EV -5.4% at the blend, agree) |

At the blend's 69%, a lock like this misses about 3 nights in 10; the chance of at least one miss in a five-night week is 85%.

### Simulated 20,000 nights of that card

Each ticket keeps its own chance to cash; the simulation adds how they move together (teammates share a game-level factor, latent ρ 0.1047 points / 0.0525 assists, measured on 2025-26 logs; opponents independent). Run three times: trusting the model, the blend (25% model), and the de-vigged market. Flat $1 a ticket; the parlay column is all legs in one ticket at the product of the prices.

| If this is right | Exp. hits of 6 | P(all 6) | P(≥5) | $1 each: exp. | P(up) | 5th–95th pct | 6-leg parlay +671: EV |
|---|---|---|---|---|---|---|---|
| model | 4.32 | 13.7% | 47% | +0.08 | 47% | -3.17 to +2.43 | +6% |
| blend | 4.07 | 9.5% | 38% | -0.28 | 38% | -3.19 to +2.43 | -27% |
| market | 3.98 | 8.2% | 35% | -0.40 | 35% | -3.20 to +2.43 | -37% |

## 1. Ranked props

| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **STRONG PROP** | EDM @ VAN | Brock Boeser under 2.5 SOG | -146 | fanduel | 1.83 | 72% vs 56% (+29%) | $5 | — |
| 2 | **STRONG PROP** | EDM @ VAN | Brock Boeser under 2.5 SOG | -150 | draftkings | 1.83 | 72% vs 56% (+29%) | $5 | — |
| 3 | **STRONG PROP** | EDM @ VAN | Filip Hronek under 1.5 SOG | +132 | fanduel | 1.64 | 52% vs 40% (+29%) | $4 | — |
| 4 | **STRONG PROP** | EDM @ VAN | Vasily Podkolzin under 0.5 PTS | +120 | draftkings | 0.60 | 55% vs 42% (+29%) | $4 | — |
| 5 | **STRONG PROP** | SEA @ CGY | Matvei Gridin under 2.5 SOG | -135 | fanduel | 1.95 | 69% vs 54% (+28%) | $5 | — |
| 6 | **STRONG PROP** | CHI @ UTA | Barrett Hayton over 1.5 SOG | +110 | draftkings | 1.92 | 56% vs 44% (+26%) | $4 | — |
| 7 | **STRONG PROP** | SEA @ CGY | Adam Larsson under 1.5 SOG | -110 | draftkings | 1.35 | 61% vs 49% (+26%) | $5 | — |
| 8 | **STRONG PROP** | EDM @ VAN | Marco Rossi under 1.5 SOG | -120 | draftkings | 1.28 | 64% vs 50% (+26%) | $5 | — |
| 9 | **STRONG PROP** | CHI @ UTA | Anton Frondell under 2.5 SOG | -125 | draftkings | 2.11 | 65% vs 51% (+26%) | $5 | — |
| 10 | **STRONG PROP** | SEA @ CGY | Zayne Parekh under 0.5 PTS | -180 | draftkings | 0.29 | 75% vs 60% (+26%) | $5 | — |
| 11 | **STRONG PROP** | EDM @ VAN | Filip Hronek under 1.5 SOG | +125 | draftkings | 1.64 | 52% vs 42% (+25%) | $4 | — |
| 12 | **STRONG PROP** | SEA @ CGY | Matt Coronato under 0.5 PTS | +110 | draftkings | 0.59 | 56% vs 44% (+25%) | $4 | — |
| 13 | **STRONG PROP** | MIN @ NSH | Maxim Shabanov under 0.5 PTS | -125 | draftkings | 0.44 | 64% vs 51% (+25%) | $5 | — |
| 14 | **STRONG PROP** | PHI @ NJD | Brett Pesce under 1.5 SOG | -135 | draftkings | 1.19 | 67% vs 53% (+25%) | $5 | — |
| 15 | **STRONG PROP** | EDM @ VAN | Jake DeBrusk under 2.5 SOG | -105 | draftkings | 2.33 | 59% vs 48% (+25%) | $4 | — |
| 16 | **STRONG PROP** | SEA @ CGY | Zayne Parekh under 0.5 A | -240 | draftkings | 0.20 | 82% vs 66% (+24%) | $5 | — |
| 17 | **STRONG PROP** | BUF @ CBJ | Rasmus Dahlin under 2.5 SOG | +102 | fanduel | 2.40 | 58% vs 47% (+24%) | $4 | — |
| 18 | **STRONG PROP** | FLA @ SJS | Anton Lundell over 0.5 PTS | +130 | draftkings | 0.70 | 50% vs 41% (+24%) | $3 | — |
| 19 | **STRONG PROP** | SEA @ CGY | Morgan Frost under 2.5 SOG | -165 | fanduel | 1.82 | 72% vs 58% (+24%) | $5 | — |
| 20 | **STRONG PROP** | TBL @ NYR | Adam Fox under 1.5 SOG | -115 | fanduel | 1.33 | 62% vs 50% (+23%) | $5 | — |
| 21 | **STRONG PROP** | BUF @ CBJ | Kent Johnson under 1.5 SOG | +115 | draftkings | 1.60 | 53% vs 43% (+23%) | $3 | — |
| 22 | **STRONG PROP** | SEA @ CGY | Bobby McMann under 2.5 SOG | -105 | draftkings | 2.34 | 59% vs 48% (+23%) | $4 | — |
| 23 | **STRONG PROP** | SEA @ CGY | Morgan Frost under 2.5 SOG | -170 | draftkings | 1.82 | 72% vs 59% (+23%) | $5 | — |
| 24 | **STRONG PROP** | FLA @ SJS | Tyler Toffoli over 0.5 PTS | +145 | draftkings | 0.63 | 47% vs 38% (+23%) | $3 | — |
| 25 | **STRONG PROP** | BUF @ CBJ | Kent Johnson under 1.5 SOG | +116 | fanduel | 1.60 | 53% vs 43% (+23%) | $3 | — |
| 26 | **STRONG PROP** | SEA @ CGY | Vince Dunn under 0.5 PTS | -115 | draftkings | 0.50 | 61% vs 50% (+23%) | $4 | — |
| 27 | **STRONG PROP** | TBL @ NYR | Nikita Kucherov under 3.5 SOG | -145 | draftkings | 2.88 | 67% vs 55% (+23%) | $5 | — |
| 28 | **STRONG PROP** | CHI @ UTA | Bowen Byram under 1.5 SOG | -125 | draftkings | 1.30 | 63% vs 51% (+23%) | $4 | — |
| 29 | **STRONG PROP** | BUF @ CBJ | Kent Johnson under 0.5 A | -230 | draftkings | 0.22 | 80% vs 65% (+22%) | $5 | — |
| 30 | **STRONG PROP** | SEA @ CGY | Vince Dunn under 0.5 A | -155 | draftkings | 0.37 | 69% vs 57% (+22%) | $5 | — |
| 31 | **STRONG PROP** | FLA @ SJS | Dmitry Orlov under 1.5 SOG | -160 | draftkings | 1.10 | 70% vs 58% (+22%) | $5 | — |
| 32 | **STRONG PROP** | SEA @ CGY | Brandon Montour under 2.5 SOG | +115 | draftkings | 2.61 | 53% vs 43% (+21%) | $3 | — |
| 33 | **STRONG PROP** | BUF @ CBJ | Rasmus Dahlin under 2.5 SOG | -105 | draftkings | 2.40 | 58% vs 48% (+21%) | $3 | — |
| 34 | **STRONG PROP** | CHI @ UTA | Anders Lee over 1.5 SOG | -160 | draftkings | 2.53 | 70% vs 58% (+21%) | $5 | — |
| 35 | **STRONG PROP** | EDM @ VAN | Mattias Ekholm under 1.5 SOG | +120 | draftkings | 1.67 | 51% vs 42% (+21%) | $3 | — |
| 36 | **STRONG PROP** | PHI @ NJD | Jack Hughes under 3.5 SOG | -110 | draftkings | 3.29 | 59% vs 49% (+21%) | $3 | — |
| 37 | **STRONG PROP** | CHI @ UTA | Bowen Byram under 1.5 SOG | -125 | fanduel | 1.30 | 63% vs 52% (+21%) | $4 | — |
| 38 | **STRONG PROP** | EDM @ VAN | Zeev Buium under 1.5 SOG | -170 | draftkings | 1.08 | 71% vs 59% (+21%) | $5 | — |
| 39 | **STRONG PROP** | SEA @ CGY | Zayne Parekh under 1.5 SOG | -115 | draftkings | 1.38 | 60% vs 50% (+21%) | $4 | — |
| 40 | **STRONG PROP** | BUF @ CBJ | Noah Ostlund under 1.5 SOG | -155 | draftkings | 1.15 | 68% vs 57% (+21%) | $5 | — |
| 41 | **STRONG PROP** | TBL @ NYR | Adam Fox under 1.5 SOG | -125 | draftkings | 1.33 | 62% vs 51% (+20%) | $4 | — |
| 42 | **STRONG PROP** | BUF @ CBJ | Jack Quinn under 2.5 SOG | -118 | fanduel | 2.26 | 61% vs 51% (+20%) | $4 | — |
| 43 | **STRONG PROP** | PHI @ NJD | Jamie Drysdale under 1.5 SOG | -170 | draftkings | 1.09 | 71% vs 59% (+20%) | $5 | — |
| 44 | **STRONG PROP** | EDM @ VAN | Vasily Podkolzin under 0.5 A | -200 | draftkings | 0.30 | 74% vs 62% (+20%) | $5 | — |
| 45 | **STRONG PROP** | CHI @ UTA | Anders Lee over 1.5 SOG | -164 | fanduel | 2.53 | 70% vs 58% (+20%) | $5 | — |
| 46 | **STRONG PROP** | BUF @ CBJ | Zach Benson under 1.5 SOG | +135 | draftkings | 1.79 | 48% vs 40% (+20%) | $2 | — |
| 47 | **STRONG PROP** | FLA @ SJS | Anton Lundell over 1.5 SOG | -135 | draftkings | 2.23 | 64% vs 53% (+19%) | $4 | — |
| 48 | **STRONG PROP** | PHI @ NJD | Anthony Mantha over 0.5 PTS | +110 | draftkings | 0.76 | 53% vs 45% (+19%) | $3 | — |
| 49 | **STRONG PROP** | FLA @ SJS | Jacob Trouba over 1.5 SOG | +100 | draftkings | 1.90 | 55% vs 47% (+19%) | $3 | — |
| 50 | **STRONG PROP** | TBL @ NYR | Nikita Kucherov under 3.5 SOG | -152 | fanduel | 2.88 | 67% vs 57% (+19%) | $4 | — |
| 51 | **STRONG PROP** | BUF @ CBJ | Ryan McLeod over 0.5 PTS | +140 | draftkings | 0.62 | 46% vs 39% (+19%) | $2 | — |
| 52 | **STRONG PROP** | EDM @ VAN | Evan Bouchard under 0.5 A | +170 | draftkings | 0.89 | 41% vs 35% (+19%) | $2 | — |
| 53 | **STRONG PROP** | SEA @ CGY | Matt Coronato under 0.5 A | -175 | draftkings | 0.35 | 71% vs 59% (+19%) | $5 | — |
| 54 | **STRONG PROP** | FLA @ SJS | Macklin Celebrini under 3.5 SOG | -125 | draftkings | 3.19 | 61% vs 51% (+18%) | $3 | — |
| 55 | **STRONG PROP** | EDM @ VAN | Mattias Ekholm over 0.5 PTS | +175 | draftkings | 0.52 | 40% vs 34% (+18%) | $2 | — |
| 56 | **STRONG PROP** | MIN @ NSH | Matthew Wood under 1.5 SOG | +100 | draftkings | 1.56 | 55% vs 46% (+18%) | $2 | — |
| 57 | **STRONG PROP** | FLA @ SJS | Anton Lundell over 0.5 A | +230 | draftkings | 0.41 | 34% vs 28% (+18%) | $1 | — |
| 58 | **STRONG PROP** | SEA @ CGY | Bobby McMann under 2.5 SOG | -114 | fanduel | 2.34 | 59% vs 50% (+18%) | $3 | — |
| 59 | **STRONG PROP** | CHI @ UTA | Anton Frondell under 2.5 SOG | -140 | fanduel | 2.11 | 65% vs 55% (+18%) | $4 | — |
| 60 | **STRONG PROP** | EDM @ VAN | Jonathan Lekkerimäki under 1.5 SOG | -165 | draftkings | 1.15 | 68% vs 58% (+18%) | $4 | — |
| 61 | **STRONG PROP** | EDM @ VAN | Vasily Podkolzin under 2.5 SOG | -135 | fanduel | 2.16 | 64% vs 54% (+18%) | $4 | — |
| 62 | **STRONG PROP** | PHI @ NJD | Noah Cates over 0.5 PTS | +180 | draftkings | 0.50 | 39% vs 33% (+18%) | $1 | — |
| 63 | **STRONG PROP** | TBL @ NYR | Brayden Point under 2.5 SOG | -160 | draftkings | 2.02 | 67% vs 57% (+18%) | $4 | — |
| 64 | **STRONG PROP** | MIN @ NSH | Ross Colton over 1.5 SOG | -125 | draftkings | 2.11 | 61% vs 51% (+18%) | $3 | — |
| 65 | **STRONG PROP** | FLA @ SJS | Anton Lundell over 1.5 SOG | -135 | fanduel | 2.23 | 64% vs 54% (+18%) | $4 | — |
| 66 | **STRONG PROP** | FLA @ SJS | Carter Verhaeghe over 2.5 SOG | +148 | fanduel | 2.49 | 45% vs 38% (+18%) | $2 | — |
| 67 | **STRONG PROP** | EDM @ VAN | Jake Walman under 1.5 SOG | +110 | draftkings | 1.63 | 53% vs 45% (+18%) | $2 | — |
| 68 | **STRONG PROP** | PHI @ NJD | Jack Hughes under 3.5 SOG | -114 | fanduel | 3.29 | 59% vs 50% (+17%) | $3 | — |
| 69 | **STRONG PROP** | CHI @ UTA | Nick Schmaltz over 2.5 SOG | +128 | fanduel | 2.65 | 48% vs 41% (+17%) | $2 | — |
| 70 | **STRONG PROP** | MIN @ NSH | Maxim Shabanov under 0.5 A | -220 | draftkings | 0.29 | 75% vs 64% (+17%) | $5 | — |
| 71 | **STRONG PROP** | EDM @ VAN | Mattias Ekholm over 0.5 A | +215 | draftkings | 0.43 | 35% vs 30% (+17%) | $1 | — |
| 72 | **STRONG PROP** | BUF @ CBJ | Zach Benson under 1.5 SOG | +130 | fanduel | 1.79 | 48% vs 41% (+17%) | $2 | — |
| 73 | **STRONG PROP** | EDM @ VAN | Leon Draisaitl under 0.5 G | -135 | fanduel | 0.47 | 62% vs 53% (+16%) | $3 | — |
| 74 | **STRONG PROP** | MIN @ NSH | Matt Boldy under 3.5 SOG | -125 | draftkings | 3.24 | 60% vs 51% (+16%) | $2 | — |
| 75 | **STRONG PROP** | EDM @ VAN | Vasily Podkolzin under 2.5 SOG | -145 | draftkings | 2.16 | 64% vs 55% (+16%) | $3 | — |
| 76 | **STRONG PROP** | FLA @ SJS | Aaron Ekblad under 1.5 SOG | -145 | draftkings | 1.28 | 64% vs 55% (+16%) | $3 | — |
| 77 | **STRONG PROP** | MIN @ NSH | Filip Forsberg under 0.5 A | -165 | draftkings | 0.40 | 67% vs 58% (+16%) | $3 | — |
| 78 | **STRONG PROP** | TBL @ NYR | Gabe Perreault over 0.5 PTS | +165 | draftkings | 0.53 | 41% vs 35% (+16%) | $1 | — |
| 79 | **STRONG PROP** | FLA @ SJS | Igor Chernyshov over 0.5 PTS | +130 | draftkings | 0.64 | 47% vs 41% (+16%) | $2 | — |
| 80 | **STRONG PROP** | FLA @ SJS | Alexander Wennberg over 0.5 PTS | +110 | draftkings | 0.72 | 51% vs 44% (+16%) | $2 | — |
| 81 | **STRONG PROP** | PHI @ NJD | Luke Evangelista under 2.5 SOG | -165 | draftkings | 2.03 | 67% vs 58% (+16%) | $3 | — |
| 82 | **STRONG PROP** | PHI @ NJD | Porter Martone under 2.5 SOG | -185 | draftkings | 1.91 | 70% vs 60% (+16%) | $4 | — |
| 83 | **STRONG PROP** | CHI @ UTA | John Marino over 0.5 A | +225 | draftkings | 0.41 | 33% vs 29% (+15%) | $1 | — |
| 84 | **STRONG PROP** | BUF @ CBJ | Josh Doan under 2.5 SOG | -160 | fanduel | 2.04 | 67% vs 58% (+15%) | $3 | — |
| 85 | **STRONG PROP** | TBL @ NYR | Brayden Point under 2.5 SOG | -164 | fanduel | 2.02 | 67% vs 58% (+15%) | $3 | — |
| 86 | **STRONG PROP** | CHI @ UTA | Vincent Trocheck over 0.5 A | +155 | draftkings | 0.55 | 42% vs 37% (+15%) | $1 | — |
| 87 | **STRONG PROP** | SEA @ CGY | Morgan Frost under 0.5 PTS | -115 | draftkings | 0.55 | 58% vs 50% (+15%) | $2 | — |
| 88 | **STRONG PROP** | MIN @ NSH | Jared Spurgeon under 0.5 PTS | -225 | draftkings | 0.29 | 75% vs 65% (+15%) | $4 | — |
| 89 | **STRONG PROP** | FLA @ SJS | Sam Bennett over 0.5 A | +210 | draftkings | 0.43 | 35% vs 30% (+15%) | $1 | — |
| 90 | **STRONG PROP** | FLA @ SJS | Carter Verhaeghe over 0.5 A | +210 | draftkings | 0.43 | 35% vs 30% (+15%) | $1 | — |
| 91 | **STRONG PROP** | BUF @ CBJ | Adam Fantilli under 0.5 PTS | +115 | draftkings | 0.69 | 50% vs 43% (+15%) | $2 | — |
| 92 | **STRONG PROP** | FLA @ SJS | Carter Verhaeghe over 0.5 PTS | +100 | draftkings | 0.77 | 54% vs 47% (+15%) | $2 | — |
| 93 | **prop value** | TBL @ NYR | Andrei Vasilevskiy under 23.5 SV | -130 | draftkings | 21.04 | 67% vs 52% (+28%) | $5 | ⚠saves-model |
| 94 | **prop value** | TBL @ NYR | Andrei Vasilevskiy under 22.5 SV | -112 | fanduel | 21.04 | 62% vs 49% (+25%) | $5 | ⚠saves-model |
| 95 | **prop value** | CHI @ UTA | Karel Vejmelka under 21.5 SV | -110 | draftkings | 20.47 | 59% vs 49% (+22%) | $4 | ⚠saves-model |
| 96 | **prop value** | SEA @ CGY | Dustin Wolf under 23.5 SV | -110 | draftkings | 22.93 | 56% vs 49% (+16%) | $2 | ⚠saves-model |
| 97 | **prop value** | FLA @ SJS | Brady Tkachuk under 0.5 G | -210 | fanduel | 0.32 | 73% vs 63% (+15%) | $4 | — |
| 98 | **prop value** | PHI @ NJD | Jesper Bratt under 2.5 SOG | -165 | draftkings | 2.05 | 66% vs 58% (+15%) | $3 | — |
| 99 | **prop value** | PHI @ NJD | Evan Rodrigues over 1.5 SOG | -135 | draftkings | 2.14 | 61% vs 53% (+15%) | $2 | — |
| 100 | **prop value** | CHI @ UTA | Frank Nazar over 0.5 PTS | +150 | draftkings | 0.56 | 43% vs 37% (+15%) | $1 | — |
| 101 | **prop value** | BUF @ CBJ | Jack Quinn under 2.5 SOG | -135 | draftkings | 2.26 | 61% vs 53% (+14%) | $2 | — |
| 102 | **prop value** | SEA @ CGY | Matvei Gridin under 0.5 PTS | -115 | draftkings | 0.56 | 57% vs 50% (+14%) | $2 | — |
| 103 | **prop value** | SEA @ CGY | Jared McCann under 0.5 A | -195 | draftkings | 0.35 | 71% vs 62% (+14%) | $3 | — |
| 104 | **prop value** | TBL @ NYR | Anthony Cirelli over 0.5 PTS | +120 | draftkings | 0.66 | 48% vs 42% (+14%) | $1 | — |
| 105 | **prop value** | CHI @ UTA | Vincent Trocheck over 0.5 PTS | -115 | draftkings | 0.83 | 57% vs 50% (+14%) | $2 | — |
| 106 | **prop value** | CHI @ UTA | Nick Schmaltz over 2.5 SOG | +120 | draftkings | 2.65 | 48% vs 42% (+14%) | $1 | — |
| 107 | **prop value** | TBL @ NYR | John Carlson under 0.5 A | -125 | draftkings | 0.53 | 59% vs 52% (+14%) | $2 | — |
| 108 | **prop value** | CHI @ UTA | Andrew Peeke under 1.5 SOG | -170 | draftkings | 1.20 | 67% vs 59% (+14%) | $2 | — |
| 109 | **prop value** | CHI @ UTA | Patrick Kane over 2.5 SOG | +125 | draftkings | 2.60 | 47% vs 41% (+14%) | $1 | — |
| 110 | **prop value** | EDM @ VAN | Colton Dach under 1.5 SOG | -145 | draftkings | 1.33 | 62% vs 55% (+13%) | $2 | — |
| 111 | **prop value** | EDM @ VAN | Brock Boeser under 0.5 PTS | -105 | draftkings | 0.62 | 54% vs 48% (+13%) | $1 | — |
| 112 | **prop value** | MIN @ NSH | Kirill Kaprizov under 0.5 A | -130 | draftkings | 0.52 | 60% vs 52% (+13%) | $2 | — |
| 113 | **prop value** | SEA @ CGY | Brandon Montour under 0.5 PTS | -150 | draftkings | 0.46 | 63% vs 56% (+13%) | $2 | — |
| 114 | **prop value** | BUF @ CBJ | Valeri Nichushkin over 1.5 SOG | -160 | draftkings | 2.28 | 65% vs 57% (+13%) | $2 | — |
| 115 | **prop value** | BUF @ CBJ | Tage Thompson under 0.5 A | -155 | draftkings | 0.44 | 64% vs 57% (+13%) | $2 | — |
| 116 | **prop value** | PHI @ NJD | Owen Tippett under 2.5 SOG | -130 | fanduel | 2.30 | 60% vs 53% (+13%) | $2 | — |
| 117 | **prop value** | MIN @ NSH | Matthew Wood under 0.5 PTS | -165 | draftkings | 0.42 | 65% vs 58% (+13%) | $2 | — |
| 118 | **prop value** | SEA @ CGY | Brandon Montour under 2.5 SOG | +102 | fanduel | 2.61 | 53% vs 47% (+13%) | $2 | — |
| 119 | **prop value** | SEA @ CGY | Ryan Winterton under 1.5 SOG | -135 | draftkings | 1.38 | 60% vs 53% (+13%) | $2 | — |
| 120 | **prop value** | MIN @ NSH | Steven Stamkos under 0.5 A | -235 | draftkings | 0.30 | 74% vs 65% (+13%) | $3 | — |
| 121 | **prop value** | EDM @ VAN | Leon Draisaitl under 1.5 PTS | -125 | draftkings | 1.41 | 59% vs 52% (+13%) | $2 | — |
| 122 | **prop value** | MIN @ NSH | Roman Josi under 0.5 A | -130 | draftkings | 0.53 | 59% vs 52% (+13%) | $1 | — |
| 123 | **prop value** | MIN @ NSH | Roman Josi under 2.5 SOG | +104 | fanduel | 2.65 | 52% vs 46% (+13%) | $1 | — |
| 124 | **prop value** | TBL @ NYR | Adam Fox under 0.5 A | -130 | draftkings | 0.53 | 59% vs 52% (+13%) | $1 | — |
| 125 | **prop value** | BUF @ CBJ | Denton Mateychuk under 1.5 SOG | -160 | draftkings | 1.25 | 65% vs 58% (+12%) | $2 | — |
| 126 | **prop value** | EDM @ VAN | Jake DeBrusk under 0.5 PTS | -120 | draftkings | 0.57 | 57% vs 50% (+12%) | $1 | — |
| 127 | **prop value** | SEA @ CGY | Joel Farabee under 0.5 PTS | -135 | draftkings | 0.51 | 60% vs 53% (+12%) | $2 | — |
| 128 | **prop value** | PHI @ NJD | Owen Tippett under 2.5 SOG | -135 | draftkings | 2.30 | 60% vs 53% (+12%) | $2 | — |
| 129 | **prop value** | PHI @ NJD | Jesper Bratt under 2.5 SOG | -170 | fanduel | 2.05 | 66% vs 59% (+12%) | $2 | — |
| 130 | **prop value** | PHI @ NJD | Jamie Drysdale under 0.5 PTS | -215 | draftkings | 0.34 | 71% vs 64% (+12%) | $2 | — |
| 131 | **prop value** | MIN @ NSH | Matt Boldy under 0.5 A | -135 | draftkings | 0.51 | 60% vs 53% (+12%) | $1 | — |
| 132 | **prop value** | BUF @ CBJ | Josh Doan under 2.5 SOG | -175 | draftkings | 2.04 | 67% vs 59% (+12%) | $2 | — |
| 133 | **prop value** | MIN @ NSH | Steven Stamkos under 2.5 SOG | -104 | fanduel | 2.57 | 54% vs 48% (+12%) | $1 | — |
| 134 | **prop value** | FLA @ SJS | Carter Verhaeghe over 2.5 SOG | +135 | draftkings | 2.49 | 45% vs 40% (+12%) | $1 | — |
| 135 | **prop value** | EDM @ VAN | Leon Draisaitl under 2.5 SOG | +134 | fanduel | 2.96 | 45% vs 40% (+12%) | $1 | — |
| 136 | **prop value** | TBL @ NYR | J.T. Miller under 0.5 PTS | -105 | draftkings | 0.63 | 53% vs 48% (+12%) | $1 | — |
| 137 | **prop value** | PHI @ NJD | Matvei Michkov over 0.5 PTS | +135 | draftkings | 0.59 | 45% vs 40% (+12%) | $1 | — |
| 138 | **prop value** | PHI @ NJD | Luke Hughes under 2.5 SOG | -182 | fanduel | 2.01 | 68% vs 60% (+12%) | $2 | — |
| 139 | **prop value** | MIN @ NSH | Filip Forsberg under 3.5 SOG | -160 | draftkings | 3.02 | 64% vs 58% (+12%) | $2 | — |
| 140 | **prop value** | PHI @ NJD | Luke Hughes under 0.5 PTS | -140 | draftkings | 0.51 | 60% vs 54% (+12%) | $1 | — |
| 141 | **prop value** | FLA @ SJS | Aaron Ekblad under 0.5 PTS | -200 | draftkings | 0.36 | 70% vs 62% (+12%) | $2 | — |
| 142 | **prop value** | SEA @ CGY | Jared McCann under 0.5 PTS | +105 | draftkings | 0.68 | 51% vs 46% (+12%) | $1 | — |
| 143 | **prop value** | CHI @ UTA | Tyler Bertuzzi under 1.5 SOG | +115 | draftkings | 1.77 | 48% vs 43% (+12%) | $1 | — |
| 144 | **prop value** | PHI @ NJD | Arseny Gritsyuk over 1.5 SOG | -135 | draftkings | 2.07 | 60% vs 53% (+11%) | $1 | — |
| 145 | **prop value** | BUF @ CBJ | Josh Doan under 0.5 PTS | -115 | draftkings | 0.59 | 56% vs 50% (+11%) | $1 | — |
| 146 | **prop value** | MIN @ NSH | Roman Josi under 2.5 SOG | +100 | draftkings | 2.65 | 52% vs 47% (+11%) | $1 | — |
| 147 | **prop value** | TBL @ NYR | Nikita Kucherov over 1.5 PTS | +155 | draftkings | 1.40 | 41% vs 37% (+11%) | $1 | — |
| 148 | **prop value** | TBL @ NYR | Mika Zibanejad under 2.5 SOG | -128 | fanduel | 2.36 | 59% vs 53% (+11%) | $1 | — |
| 149 | **prop value** | SEA @ CGY | Vince Dunn under 2.5 SOG | -152 | fanduel | 2.19 | 63% vs 57% (+11%) | $2 | — |
| 150 | **prop value** | FLA @ SJS | Macklin Celebrini under 3.5 SOG | -140 | fanduel | 3.19 | 61% vs 55% (+11%) | $2 | — |
| 151 | **prop value** | CHI @ UTA | Clayton Keller under 0.5 A | +110 | draftkings | 0.71 | 49% vs 44% (+11%) | $1 | — |
| 152 | **prop value** | MIN @ NSH | Steven Stamkos over 0.5 G | +210 | fanduel | 0.41 | 34% vs 30% (+11%) | — | — |
| 153 | **prop value** | FLA @ SJS | Mason Marchment under 1.5 SOG | +105 | draftkings | 1.71 | 50% vs 45% (+11%) | $1 | — |
| 154 | **prop value** | SEA @ CGY | Mikael Backlund over 0.5 PTS | +140 | draftkings | 0.56 | 43% vs 39% (+11%) | $1 | — |
| 155 | **prop value** | TBL @ NYR | Alexis Lafrenière under 2.5 SOG | -198 | fanduel | 1.94 | 69% vs 62% (+11%) | $2 | — |
| 156 | **prop value** | TBL @ NYR | Brandon Hagel under 2.5 SOG | +120 | fanduel | 2.84 | 47% vs 43% (+11%) | $1 | — |
| 157 | **prop value** | BUF @ CBJ | Josh Norris over 0.5 PTS | +115 | draftkings | 0.66 | 48% vs 43% (+11%) | $1 | — |
| 158 | **prop value** | PHI @ NJD | Dawson Mercer over 1.5 SOG | -110 | draftkings | 1.85 | 54% vs 49% (+11%) | $1 | — |
| 159 | **prop value** | TBL @ NYR | Oliver Bjorkstrand over 1.5 SOG | +105 | draftkings | 1.71 | 50% vs 45% (+11%) | $1 | — |
| 160 | **prop value** | MIN @ NSH | Blake Coleman over 2.5 SOG | +132 | fanduel | 2.50 | 45% vs 40% (+11%) | $1 | — |
| 161 | **prop value** | MIN @ NSH | Quinn Hughes under 2.5 SOG | -120 | draftkings | 2.47 | 56% vs 50% (+11%) | $1 | — |
| 162 | **prop value** | CHI @ UTA | Nick Schmaltz over 0.5 G | +220 | fanduel | 0.39 | 32% vs 29% (+11%) | — | — |
| 163 | **prop value** | SEA @ CGY | Yegor Sharangovich under 0.5 PTS | -170 | draftkings | 0.43 | 65% vs 59% (+11%) | $1 | — |
| 164 | **prop value** | FLA @ SJS | Seth Jones over 1.5 SOG | -115 | fanduel | 1.91 | 55% vs 50% (+11%) | $1 | — |
| 165 | **prop value** | EDM @ VAN | Drew O'Connor over 1.5 SOG | -110 | draftkings | 1.86 | 54% vs 49% (+11%) | $1 | — |
| 166 | **prop value** | SEA @ CGY | Jordan Eberle under 0.5 A | -215 | draftkings | 0.35 | 71% vs 64% (+10%) | $2 | — |
| 167 | **prop value** | TBL @ NYR | J.T. Miller under 0.5 A | -185 | draftkings | 0.41 | 67% vs 60% (+10%) | $1 | — |
| 168 | **prop value** | EDM @ VAN | Kasperi Kapanen under 0.5 PTS | -130 | draftkings | 0.55 | 58% vs 52% (+10%) | $1 | — |
| 169 | **prop value** | SEA @ CGY | Joel Farabee under 1.5 SOG | +126 | fanduel | 1.86 | 46% vs 42% (+10%) | $1 | — |
| 170 | **prop value** | EDM @ VAN | Connor McDavid under 1.5 A | -235 | draftkings | 1.04 | 72% vs 65% (+10%) | $2 | — |
| 171 | **prop value** | FLA @ SJS | Sam Reinhart under 0.5 A | -150 | draftkings | 0.49 | 61% vs 56% (+10%) | $1 | — |
| 172 | **prop value** | SEA @ CGY | Brandon Montour under 0.5 A | -245 | draftkings | 0.31 | 73% vs 67% (+10%) | $2 | — |
| 173 | **prop value** | PHI @ NJD | Jesper Bratt under 0.5 A | -130 | draftkings | 0.55 | 58% vs 52% (+10%) | $1 | — |
| 174 | **prop value** | SEA @ CGY | Jordan Eberle under 0.5 PTS | -105 | draftkings | 0.65 | 52% vs 48% (+10%) | $1 | — |
| 175 | **prop value** | BUF @ CBJ | Charlie Coyle over 1.5 SOG | -115 | draftkings | 1.87 | 54% vs 50% (+10%) | $1 | — |
| 176 | **prop value** | SEA @ CGY | Mikael Backlund over 1.5 SOG | -180 | draftkings | 2.35 | 66% vs 60% (+10%) | $1 | — |
| 177 | **prop value** | TBL @ NYR | J.T. Miller under 1.5 SOG | +120 | draftkings | 1.84 | 46% vs 42% (+10%) | — | — |
| 178 | **prop value** | MIN @ NSH | Quinn Hughes under 2.5 SOG | -118 | fanduel | 2.47 | 56% vs 51% (+10%) | $1 | — |
| 179 | **prop value** | PHI @ NJD | Luke Evangelista under 2.5 SOG | -184 | fanduel | 2.03 | 67% vs 61% (+10%) | $1 | — |
| 180 | **prop value** | TBL @ NYR | Adam Fox under 0.5 PTS | +100 | draftkings | 0.68 | 51% vs 46% (+10%) | — | — |
| 181 | **prop value** | FLA @ SJS | Macklin Celebrini over 0.5 A | -110 | draftkings | 0.77 | 54% vs 49% (+10%) | $1 | — |
| 182 | **prop value** | TBL @ NYR | Mika Zibanejad under 2.5 SOG | -135 | draftkings | 2.36 | 59% vs 53% (+10%) | $1 | — |
| 183 | **prop value** | FLA @ SJS | Tyler Toffoli over 1.5 SOG | -135 | draftkings | 2.03 | 59% vs 53% (+10%) | $1 | — |
| 184 | **prop value** | TBL @ NYR | Mika Zibanejad under 0.5 A | -165 | draftkings | 0.45 | 64% vs 58% (+10%) | $1 | — |
| 185 | **prop value** | TBL @ NYR | Will Cuylle over 1.5 SOG | -105 | draftkings | 1.78 | 52% vs 48% (+10%) | — | — |
| 186 | **prop value** | MIN @ NSH | Quinn Hughes under 0.5 PTS | +155 | draftkings | 0.92 | 40% vs 36% (+9%) | — | — |
| 187 | **prop value** | TBL @ NYR | Jake Guentzel over 0.5 PTS | -150 | draftkings | 0.94 | 61% vs 56% (+9%) | $1 | — |
| 188 | **prop value** | MIN @ NSH | Steven Stamkos under 2.5 SOG | -110 | draftkings | 2.57 | 54% vs 49% (+9%) | $1 | — |
| 189 | **prop value** | MIN @ NSH | Jonathan Marchessault over 1.5 SOG | -156 | fanduel | 2.19 | 63% vs 57% (+9%) | $1 | — |
| 190 | **prop value** | FLA @ SJS | Alexander Wennberg over 0.5 A | +175 | draftkings | 0.47 | 37% vs 34% (+9%) | — | — |
| 191 | **prop value** | BUF @ CBJ | Josh Doan under 0.5 A | -250 | draftkings | 0.31 | 73% vs 67% (+9%) | $2 | — |
| 192 | **prop value** | CHI @ UTA | John Marino over 0.5 PTS | +170 | draftkings | 0.48 | 38% vs 35% (+9%) | — | — |
| 193 | **prop value** | MIN @ NSH | Joel Eriksson Ek over 0.5 A | +195 | draftkings | 0.43 | 35% vs 32% (+9%) | — | — |
| 194 | **prop value** | BUF @ CBJ | Matthew Knies over 0.5 A | +165 | draftkings | 0.49 | 39% vs 35% (+9%) | — | — |
| 195 | **prop value** | FLA @ SJS | Sam Bennett over 0.5 PTS | -115 | draftkings | 0.78 | 54% vs 50% (+9%) | — | — |
| 196 | **prop value** | EDM @ VAN | Connor McDavid under 1.5 PTS | +100 | draftkings | 1.65 | 51% vs 47% (+9%) | — | — |
| 197 | **prop value** | PHI @ NJD | Jack Hughes under 0.5 G | -195 | fanduel | 0.39 | 67% vs 62% (+9%) | $1 | — |
| 198 | **prop value** | PHI @ NJD | Travis Konecny over 0.5 PTS | +105 | draftkings | 0.68 | 49% vs 45% (+9%) | — | — |
| 199 | **prop value** | EDM @ VAN | Kevin Lankinen under 28.5 SV | -132 | fanduel | 27.48 | 58% vs 53% (+9%) | $1 | ⚠saves-model |
| 200 | **prop value** | TBL @ NYR | Pavel Dorofeyev under 2.5 SOG | -115 | draftkings | 2.53 | 54% vs 50% (+9%) | $1 | — |
| 201 | **prop value** | TBL @ NYR | Pavel Dorofeyev under 2.5 SOG | -114 | fanduel | 2.53 | 54% vs 50% (+9%) | $1 | — |
| 202 | **prop value** | MIN @ NSH | Juuse Saros over 25.5 SV | -114 | fanduel | 27.00 | 54% vs 50% (+9%) | $1 | ⚠saves-model |
| 203 | **prop value** | CHI @ UTA | Logan Cooley under 1.5 SOG | +150 | fanduel | 2.05 | 41% vs 38% (+9%) | — | — |
| 204 | **prop value** | SEA @ CGY | Connor Zary under 1.5 SOG | -110 | draftkings | 1.62 | 53% vs 49% (+9%) | — | — |
| 205 | **prop value** | CHI @ UTA | Mikhail Sergachev under 0.5 A | -115 | draftkings | 0.61 | 54% vs 50% (+9%) | — | — |
| 206 | **prop value** | TBL @ NYR | Oliver Bjorkstrand over 1.5 SOG | +104 | fanduel | 1.71 | 50% vs 46% (+9%) | $1 | — |
| 207 | **prop value** | FLA @ SJS | Seth Jones over 1.5 SOG | -120 | draftkings | 1.91 | 55% vs 51% (+9%) | $1 | — |
| 208 | **prop value** | MIN @ NSH | Filip Forsberg under 2.5 SOG | +134 | fanduel | 3.02 | 44% vs 40% (+9%) | — | — |
| 209 | **prop value** | CHI @ UTA | MacKenzie Weegar under 0.5 PTS | -195 | draftkings | 0.40 | 67% vs 62% (+9%) | $1 | — |
| 210 | **prop value** | BUF @ CBJ | Zach Werenski under 3.5 SOG | -130 | draftkings | 3.38 | 57% vs 52% (+9%) | — | — |
| 211 | **prop value** | BUF @ CBJ | Sean Monahan under 0.5 PTS | -155 | draftkings | 0.49 | 61% vs 57% (+9%) | — | — |
| 212 | **prop value** | BUF @ CBJ | Charlie Coyle over 0.5 PTS | +105 | draftkings | 0.68 | 49% vs 46% (+8%) | — | — |
| 213 | **prop value** | FLA @ SJS | Macklin Celebrini over 1.5 PTS | +165 | draftkings | 1.33 | 38% vs 35% (+8%) | — | — |
| 214 | **prop value** | CHI @ UTA | Patrick Kane over 2.5 SOG | +116 | fanduel | 2.60 | 47% vs 43% (+8%) | — | — |
| 215 | **prop value** | BUF @ CBJ | Matthew Knies under 1.5 SOG | +126 | fanduel | 1.89 | 45% vs 42% (+8%) | — | — |
| 216 | **prop value** | CHI @ UTA | Clayton Keller under 1.5 PTS | -235 | draftkings | 1.07 | 71% vs 65% (+8%) | $1 | — |
| 217 | **prop value** | MIN @ NSH | Matt Boldy under 3.5 SOG | -144 | fanduel | 3.24 | 60% vs 55% (+8%) | $1 | — |
| 218 | **prop value** | EDM @ VAN | Brock Boeser under 0.5 A | -230 | draftkings | 0.35 | 71% vs 65% (+8%) | $1 | — |
| 219 | **prop value** | PHI @ NJD | Jesper Bratt under 0.5 PTS | +135 | draftkings | 0.84 | 43% vs 40% (+8%) | — | — |

## 2. Projections (first 40 by game)

```
Game        Player                    Pos Market  Line   Proj  P(over)   Over/Under  Book
BUF @ CBJ   Ukko-Pekka Luukkonen      G   SV      25.5  25.41      46%    -115/-120  draftkings
BUF @ CBJ   Ukko-Pekka Luukkonen      G   SV      25.5  25.41      46%    -112/-118  fanduel
BUF @ CBJ   Tage Thompson             C   SOG      2.5   3.18      59%    -170/+125  draftkings
BUF @ CBJ   Tage Thompson             C   SOG      3.5   3.18      39%    +126/-165  fanduel
BUF @ CBJ   Rasmus Dahlin             D   SOG      2.5   2.40      42%    -130/-105  draftkings
BUF @ CBJ   Rasmus Dahlin             D   SOG      2.5   2.40      42%    -132/+102  fanduel
BUF @ CBJ   Jack Quinn                R   SOG      2.5   2.26      39%    +100/-135  draftkings
BUF @ CBJ   Jack Quinn                R   SOG      2.5   2.26      39%    -110/-118  fanduel
BUF @ CBJ   Josh Doan                 R   SOG      2.5   2.04      33%    +130/-175  draftkings
BUF @ CBJ   Josh Doan                 R   SOG      2.5   2.04      33%    +122/-160  fanduel
BUF @ CBJ   Zach Benson               L   SOG      1.5   1.79      52%    -180/+135  draftkings
BUF @ CBJ   Zach Benson               L   SOG      1.5   1.79      52%    -170/+130  fanduel
BUF @ CBJ   Josh Norris               C   SOG      1.5   1.63      48%    -115/-120  draftkings
BUF @ CBJ   Konsta Helenius           C   SOG      1.5   1.61      47%    -105/-130  draftkings
BUF @ CBJ   Noah Ostlund              C   SOG      1.5   1.15      32%    +115/-155  draftkings
BUF @ CBJ   Tage Thompson             C   PTS      0.5   0.88      58%    -185/+135  draftkings
BUF @ CBJ   Rasmus Dahlin             D   PTS      0.5   0.82      56%    -150/+110  draftkings
BUF @ CBJ   Josh Norris               C   PTS      0.5   0.66      48%    +115/-155  draftkings
BUF @ CBJ   Ryan McLeod               C   PTS      0.5   0.62      46%    +140/-190  draftkings
BUF @ CBJ   Zach Benson               L   PTS      0.5   0.60      45%    +105/-140  draftkings
BUF @ CBJ   Rasmus Dahlin             D   A        0.5   0.59      44%    -105/-130  draftkings
BUF @ CBJ   Josh Doan                 R   PTS      0.5   0.59      44%    -115/-115  draftkings
BUF @ CBJ   Jack Quinn                R   PTS      0.5   0.58      44%    -105/-130  draftkings
BUF @ CBJ   Tage Thompson             C   A        0.5   0.44      36%    +115/-155  draftkings
BUF @ CBJ   Noah Ostlund              C   PTS      0.5   0.44      36%    +145/-195  draftkings
BUF @ CBJ   Ryan McLeod               C   A        0.5   0.43      35%    +255/-360  draftkings
BUF @ CBJ   Tage Thompson             C   G        0.5   0.39      33%    +170/-240  fanduel
BUF @ CBJ   Zach Benson               L   A        0.5   0.39      32%    +195/-270  draftkings
BUF @ CBJ   Josh Norris               C   A        0.5   0.38      32%    +215/-295  draftkings
BUF @ CBJ   Jack Quinn                R   A        0.5   0.34      29%    +180/-250  draftkings
BUF @ CBJ   Josh Doan                 R   A        0.5   0.31      27%    +185/-250  draftkings
BUF @ CBJ   Josh Doan                 R   G        0.5   0.26      23%    +240/-350  fanduel
BUF @ CBJ   Noah Ostlund              C   A        0.5   0.26      23%    +280/-400  draftkings
BUF @ CBJ   Josh Norris               C   G        0.5   0.25      22%    +320/-490  fanduel
BUF @ CBJ   Jack Quinn                R   G        0.5   0.23      20%    +270/-400  fanduel
BUF @ CBJ   Zach Benson               L   G        0.5   0.20      18%    +280/-420  fanduel
BUF @ CBJ   Jet Greaves               G   SV      25.5  26.00      50%    -125/-110  draftkings
BUF @ CBJ   Jet Greaves               G   SV      25.5  26.00      50%    -118/-112  fanduel
BUF @ CBJ   Zach Werenski             D   SOG      3.5   3.38      43%    -105/-130  draftkings
BUF @ CBJ   Zach Werenski             D   SOG      3.5   3.38      43%    +104/-135  fanduel
```

## 3. NHL paper ledger to date

```
NHL prop paper bets — settled by market/side/strength (pending: 365)
market                    side   str    n   W   L   P   staked   profit     ROI
player_assists            over     2   14   5   9   0    37.00    -5.06  -13.7%
player_assists            under    2    9   5   4   0    33.00    -3.72  -11.3%
player_goals              over     2    4   0   4   0    10.00   -10.00 -100.0%
player_points             over     2   21   7  14   0    63.00   -23.29  -37.0%
player_points             under    2    6   3   3   0    19.00    -0.38   -2.0%
player_shots_on_goal      over     2   20   8  12   0    68.00   -12.39  -18.2%
player_shots_on_goal      under    2    7   4   3   0    27.00     1.43   +5.3%
player_assists            over     1   15   4  11   0    17.00    -5.38  -31.6%
player_assists            under    1   37  25  12   0    30.00    -0.39   -1.3%
player_goals              over     1    5   3   2   0     2.00     3.40 +170.0%
player_goals              under    1   10   8   2   0     6.00     2.74  +45.7%
player_points             over     1   40  14  26   0    46.00   -25.49  -55.4%
player_points             under    1   32  17  15   0     9.00    -9.00 -100.0%
player_shots_on_goal      over     1   45  23  22   0    38.00    -1.99   -5.2%
player_shots_on_goal      under    1   45  25  20   0    34.00    -5.12  -15.1%
player_total_saves        over     1    3   1   2   0    12.00    -2.24  -18.7%
player_total_saves        under    1    9   4   5   0    24.00    -9.06  -37.8%
```

> Paper only. The projection is tested walk-forward (fit on 2024-25, scored on every 2025-26 game: `--calibrate`, `analysis/06`), but no historical prop prices exist, so ROI against posted lines is untested until the ledger fills. The ledger above is that evidence.

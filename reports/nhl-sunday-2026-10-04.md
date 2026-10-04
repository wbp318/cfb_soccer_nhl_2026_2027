# NHL Prop Report — Sunday, October 04, 2026

**Generated:** 2026-10-04 03:34 PM CDT  
**STAKES: PAPER ONLY as of 2026-09-20 — no bucket has a 95% CI above zero. $Bet is what the paper ledger logs, not a recommendation to bet real money.**  
**Slate:** 5 games · 490 prop lines matched to rostered players (The Odds API)  
**Model (skaters, since 2026-09-30):** per-minute rate × projected minutes. The rate is this season's stat per minute blended with last season's (weight a1) and regressed toward the position mean (K ghost minutes: shots 86, points 234, goals 694); minutes lean 56% on the last 5 games. × opponent allowance^β × home/away split → Poisson P(over) (shots: gamma-Poisson k=17.5; goalie saves: old per-start recipe, k=20). Fit on 2024-25, tested on every 2025-26 skater-game: better log-loss than the old recipe at every line of every stat. Tiers +8% / +15%, ≥ +30% demoted (⚠overreach).

## The lock, and five good ones

**The lock** is the top of the agreement board: the prop side the projection and the de-vigged line both favour, priced -250..-110, model above fair by no more than +20%, ranked by the **blend** (25% model, 75% de-vigged line, in logit space: the market has been sharper everywhere so far). **Good** is the rest of that board, then the ranked value props (§1), one per player. EV is at the blend; at −220..−250 the juice usually outweighs what the model adds, so these are the likeliest winners, not value bets. Paper only.

| | Puck (CT) | Game | Play | Why |
|---|---|---|---|---|
| **LOCK** | 7:00 PM | CGY @ SEA | **Matt Coronato under 0.5 A -245 @draftkings** | proj 0.29 → model 75% · fair 67% · blend 69% (EV -3.3% at the blend, agree) |
| good 1 | 8:00 PM | VGK @ VAN | Mitch Marner under 0.5 G -240 @fanduel | proj 0.33 → model 72% · fair 66% · blend 68% (EV -4.3% at the blend, agree) |
| good 2 | 8:00 PM | VGK @ VAN | Zeev Buium under 0.5 PTS -250 @betmgm | proj 0.36 → model 70% · fair 67% · blend 68% (EV -5.5% at the blend, agree) |
| good 3 | 5:00 PM | UTA @ NYR | Pavel Dorofeyev under 0.5 G -240 @fanduel | proj 0.33 → model 72% · fair 66% · blend 67% (EV -4.4% at the blend, agree) |
| good 4 | 7:00 PM | FLA @ ANA | Leo Carlsson under 0.5 G -250 @fanduel | proj 0.37 → model 69% · fair 67% · blend 67% (EV -5.9% at the blend, agree) |
| good 5 | 7:00 PM | FLA @ ANA | Lars Eller under 0.5 PTS -235 @draftkings | proj 0.33 → model 72% · fair 65% · blend 67% (EV -4.4% at the blend, agree) |

At the blend's 69%, a lock like this misses about 3 nights in 10; the chance of at least one miss in a five-night week is 85%.

### Simulated 20,000 nights of that card

Each ticket keeps its own chance to cash; the simulation adds how they move together (teammates share a game-level factor, latent ρ 0.1047 points / 0.0525 assists, measured on 2025-26 logs; opponents independent). Run three times: trusting the model, the blend (25% model), and the de-vigged market. Flat $1 a ticket; the parlay column is all legs in one ticket at the product of the prices.

| If this is right | Exp. hits of 6 | P(all 6) | P(≥5) | $1 each: exp. | P(up) | 5th–95th pct | 6-leg parlay +690: EV |
|---|---|---|---|---|---|---|---|
| model | 4.28 | 13.0% | 45% | +0.04 | 45% | -3.17 to +2.47 | +3% |
| blend | 4.05 | 9.5% | 37% | -0.29 | 37% | -3.18 to +2.47 | -25% |
| market | 3.97 | 8.3% | 34% | -0.40 | 34% | -3.18 to +2.47 | -34% |

## 1. Ranked props

| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 1.5 SOG | +130 | betmgm | 1.73 | 50% vs 39% (+28%) | $3 | — |
| 2 | **STRONG PROP** | CGY @ SEA | Zayne Parekh under 0.5 PTS | -180 | draftkings | 0.27 | 76% vs 60% (+28%) | $5 | — |
| 3 | **STRONG PROP** | VGK @ VAN | Shea Theodore under 0.5 A | -115 | betmgm | 0.45 | 64% vs 50% (+28%) | $5 | — |
| 4 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 0.5 PTS | +115 | betmgm | 0.59 | 55% vs 43% (+27%) | $4 | — |
| 5 | **STRONG PROP** | VGK @ VAN | Filip Hronek under 1.5 SOG | +110 | draftkings | 1.50 | 56% vs 44% (+27%) | $4 | — |
| 6 | **STRONG PROP** | UTA @ NYR | Pavel Dorofeyev under 2.5 SOG | +110 | fanduel | 2.44 | 57% vs 45% (+27%) | $4 | — |
| 7 | **STRONG PROP** | UTA @ NYR | Adam Fox under 1.5 SOG | -115 | draftkings | 1.29 | 63% vs 50% (+26%) | $5 | — |
| 8 | **STRONG PROP** | UTA @ NYR | Adam Fox under 1.5 SOG | -120 | betmgm | 1.29 | 63% vs 50% (+26%) | $5 | — |
| 9 | **STRONG PROP** | CGY @ SEA | Zayne Parekh under 0.5 PTS | -185 | betmgm | 0.27 | 76% vs 60% (+26%) | $5 | — |
| 10 | **STRONG PROP** | UTA @ NYR | Gabe Perreault under 1.5 SOG | -120 | betmgm | 1.30 | 63% vs 50% (+26%) | $5 | — |
| 11 | **STRONG PROP** | UTA @ NYR | Pavel Dorofeyev under 2.5 SOG | +105 | draftkings | 2.44 | 57% vs 45% (+26%) | $4 | — |
| 12 | **STRONG PROP** | CGY @ SEA | Kaapo Kakko over 0.5 PTS | +140 | betmgm | 0.67 | 49% vs 39% (+25%) | $3 | — |
| 13 | **STRONG PROP** | UTA @ NYR | Vincent Trocheck under 1.5 SOG | +105 | betmgm | 1.52 | 56% vs 45% (+25%) | $3 | — |
| 14 | **STRONG PROP** | VGK @ VAN | Shea Theodore under 0.5 PTS | +115 | betmgm | 0.62 | 54% vs 43% (+24%) | $3 | — |
| 15 | **STRONG PROP** | CGY @ SEA | Morgan Frost under 0.5 PTS | -120 | betmgm | 0.46 | 63% vs 51% (+24%) | $5 | — |
| 16 | **STRONG PROP** | FLA @ ANA | Ryan Poehling under 1.5 SOG | -130 | draftkings | 1.27 | 64% vs 52% (+22%) | $4 | — |
| 17 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 0.5 A | -150 | betmgm | 0.38 | 68% vs 56% (+22%) | $5 | — |
| 18 | **STRONG PROP** | VGK @ VAN | Brock Boeser under 1.5 SOG | +135 | betmgm | 1.86 | 46% vs 37% (+22%) | $1 | — |
| 19 | **STRONG PROP** | UTA @ NYR | Adam Fox under 0.5 A | +100 | draftkings | 0.57 | 57% vs 47% (+22%) | $3 | — |
| 20 | **STRONG PROP** | CGY @ SEA | Morgan Frost under 0.5 A | -225 | betmgm | 0.24 | 79% vs 65% (+22%) | $5 | — |
| 21 | **STRONG PROP** | CGY @ SEA | Matvei Gridin under 0.5 PTS | -125 | betmgm | 0.47 | 63% vs 52% (+21%) | $4 | — |
| 22 | **STRONG PROP** | UTA @ NYR | Adam Fox under 0.5 PTS | +130 | draftkings | 0.72 | 49% vs 40% (+21%) | $2 | — |
| 23 | **STRONG PROP** | VGK @ VAN | Filip Hronek under 1.5 SOG | -105 | betmgm | 1.50 | 56% vs 47% (+21%) | $3 | — |
| 24 | **STRONG PROP** | CGY @ SEA | Matt Coronato under 0.5 PTS | -120 | draftkings | 0.50 | 60% vs 50% (+20%) | $3 | — |
| 25 | **STRONG PROP** | UTA @ NYR | Mika Zibanejad under 0.5 A | -135 | betmgm | 0.45 | 64% vs 53% (+19%) | $4 | — |
| 26 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 1.5 SOG | +125 | fanduel | 1.73 | 50% vs 42% (+19%) | $2 | — |
| 27 | **STRONG PROP** | CGY @ SEA | Morgan Frost under 1.5 SOG | +120 | draftkings | 1.70 | 50% vs 42% (+18%) | $2 | — |
| 28 | **STRONG PROP** | VGK @ VAN | Brock Boeser under 2.5 SOG | -180 | draftkings | 1.86 | 71% vs 60% (+18%) | $5 | — |
| 29 | **STRONG PROP** | UTA @ NYR | Adam Fox under 0.5 A | -105 | betmgm | 0.57 | 57% vs 48% (+18%) | $3 | — |
| 30 | **STRONG PROP** | CGY @ SEA | Matvei Gridin under 1.5 SOG | +135 | draftkings | 1.83 | 47% vs 40% (+18%) | $2 | — |
| 31 | **STRONG PROP** | CGY @ SEA | Morgan Frost under 0.5 PTS | -135 | draftkings | 0.46 | 63% vs 53% (+18%) | $3 | — |
| 32 | **STRONG PROP** | VGK @ VAN | Filip Hronek over 0.5 A | +175 | draftkings | 0.51 | 40% vs 34% (+18%) | $2 | — |
| 33 | **STRONG PROP** | UTA @ NYR | Gabe Perreault under 1.5 SOG | -135 | draftkings | 1.30 | 63% vs 53% (+18%) | $3 | — |
| 34 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 0.5 PTS | +100 | draftkings | 0.59 | 55% vs 47% (+18%) | $3 | — |
| 35 | **STRONG PROP** | FLA @ ANA | Brady Tkachuk under 0.5 G | -190 | fanduel | 0.33 | 72% vs 61% (+18%) | $5 | — |
| 36 | **STRONG PROP** | UTA @ NYR | Vincent Trocheck under 1.5 SOG | -105 | draftkings | 1.52 | 56% vs 48% (+18%) | $2 | — |
| 37 | **STRONG PROP** | UTA @ NYR | Mika Zibanejad under 2.5 SOG | -120 | fanduel | 2.30 | 60% vs 51% (+17%) | $3 | — |
| 38 | **STRONG PROP** | CGY @ SEA | Yegor Sharangovich under 1.5 SOG | +135 | draftkings | 1.83 | 46% vs 40% (+17%) | $2 | — |
| 39 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 1.5 SOG | +120 | draftkings | 1.73 | 50% vs 42% (+17%) | $2 | — |
| 40 | **STRONG PROP** | FLA @ ANA | Eetu Luostarinen over 0.5 PTS | +180 | draftkings | 0.50 | 39% vs 33% (+17%) | $1 | — |
| 41 | **STRONG PROP** | UTA @ NYR | Mika Zibanejad under 2.5 SOG | -125 | draftkings | 2.30 | 60% vs 51% (+17%) | $3 | — |
| 42 | **STRONG PROP** | VGK @ VAN | Shea Theodore under 0.5 PTS | +100 | draftkings | 0.62 | 54% vs 46% (+17%) | $2 | — |
| 43 | **STRONG PROP** | FLA @ ANA | Aaron Ekblad under 1.5 SOG | -160 | betmgm | 1.22 | 66% vs 56% (+17%) | $3 | — |
| 44 | **STRONG PROP** | CGY @ SEA | Yegor Sharangovich under 1.5 SOG | +136 | fanduel | 1.83 | 46% vs 40% (+17%) | $2 | — |
| 45 | **STRONG PROP** | CGY @ SEA | Kaapo Kakko over 0.5 A | +220 | betmgm | 0.41 | 34% vs 29% (+17%) | $1 | — |
| 46 | **STRONG PROP** | UTA @ NYR | Alexis Lafrenière under 1.5 SOG | +130 | betmgm | 1.86 | 46% vs 39% (+16%) | $1 | — |
| 47 | **STRONG PROP** | CGY @ SEA | Morgan Frost under 1.5 SOG | +116 | fanduel | 1.70 | 50% vs 43% (+16%) | $2 | — |
| 48 | **STRONG PROP** | CGY @ SEA | Matvei Gridin under 0.5 A | -220 | betmgm | 0.30 | 74% vs 64% (+16%) | $4 | — |
| 49 | **STRONG PROP** | CGY @ SEA | Matvei Gridin under 1.5 SOG | +132 | fanduel | 1.83 | 47% vs 40% (+16%) | $2 | — |
| 50 | **STRONG PROP** | UTA @ NYR | Alexis Lafrenière under 1.5 SOG | +135 | draftkings | 1.86 | 46% vs 40% (+16%) | $1 | — |
| 51 | **STRONG PROP** | UTA @ NYR | Alexis Lafrenière under 0.5 PTS | +100 | betmgm | 0.62 | 54% vs 47% (+15%) | $2 | — |
| 52 | **STRONG PROP** | FLA @ ANA | Seth Jones over 1.5 SOG | +100 | draftkings | 1.84 | 54% vs 47% (+15%) | $2 | — |
| 53 | **STRONG PROP** | CGY @ SEA | Zayne Parekh under 1.5 SOG | -118 | fanduel | 1.44 | 58% vs 51% (+15%) | $2 | — |
| 54 | **prop value** | UTA @ NYR | Igor Shesterkin under 27.5 SV | -114 | fanduel | 25.31 | 64% vs 50% (+28%) | $5 | ⚠saves-model |
| 55 | **prop value** | UTA @ NYR | Igor Shesterkin under 27.5 SV | -120 | draftkings | 25.31 | 64% vs 50% (+27%) | $5 | ⚠saves-model |
| 56 | **prop value** | VGK @ VAN | Adin Hill under 18.5 SV | -105 | draftkings | 17.45 | 60% vs 48% (+27%) | $5 | ⚠saves-model |
| 57 | **prop value** | VGK @ VAN | Kevin Lankinen under 27.5 SV | -115 | draftkings | 26.21 | 60% vs 50% (+19%) | $3 | ⚠saves-model |
| 58 | **prop value** | VGK @ VAN | Kevin Lankinen under 27.5 SV | -118 | fanduel | 26.21 | 60% vs 51% (+18%) | $3 | ⚠saves-model |
| 59 | **prop value** | CGY @ SEA | Dustin Wolf under 23.5 SV | -105 | draftkings | 23.01 | 56% vs 48% (+18%) | $2 | ⚠saves-model |
| 60 | **prop value** | CGY @ SEA | Joey Daccord over 23.5 SV | -105 | draftkings | 25.13 | 56% vs 48% (+16%) | $2 | ⚠saves-model |
| 61 | **prop value** | CGY @ SEA | Dustin Wolf under 24.5 SV | -132 | fanduel | 23.01 | 61% vs 53% (+15%) | $3 | ⚠saves-model |
| 62 | **prop value** | CGY @ SEA | Mikael Backlund over 1.5 SOG | -150 | draftkings | 2.25 | 64% vs 56% (+15%) | $3 | — |
| 63 | **prop value** | VGK @ VAN | Tomas Hertl over 1.5 SOG | -220 | betmgm | 2.56 | 70% vs 61% (+15%) | $1 | — |
| 64 | **prop value** | UTA @ NYR | Adam Fox under 0.5 PTS | +120 | betmgm | 0.72 | 49% vs 42% (+15%) | $1 | — |
| 65 | **prop value** | CGY @ SEA | Ryan Strome under 0.5 PTS | -160 | betmgm | 0.42 | 66% vs 58% (+15%) | $3 | — |
| 66 | **prop value** | UTA @ NYR | Anders Lee under 0.5 PTS | -160 | betmgm | 0.42 | 66% vs 58% (+15%) | $3 | — |
| 67 | **prop value** | CGY @ SEA | Matvei Gridin under 0.5 PTS | -145 | draftkings | 0.47 | 63% vs 55% (+15%) | $2 | — |
| 68 | **prop value** | FLA @ ANA | Lars Eller under 1.5 SOG | -175 | betmgm | 1.19 | 67% vs 58% (+14%) | $2 | — |
| 69 | **prop value** | VGK @ VAN | Shea Theodore under 0.5 A | -150 | draftkings | 0.45 | 64% vs 56% (+14%) | $2 | — |
| 70 | **prop value** | VGK @ VAN | Mitch Marner under 0.5 A | +115 | betmgm | 0.70 | 50% vs 43% (+14%) | $1 | — |
| 71 | **prop value** | UTA @ NYR | Dylan Guenther under 2.5 SOG | +120 | draftkings | 2.80 | 48% vs 42% (+14%) | $1 | — |
| 72 | **prop value** | FLA @ ANA | Ryan Poehling under 1.5 SOG | -160 | betmgm | 1.27 | 64% vs 56% (+14%) | $2 | — |
| 73 | **prop value** | FLA @ ANA | Anton Lundell over 1.5 SOG | -148 | fanduel | 2.25 | 64% vs 56% (+14%) | $3 | — |
| 74 | **prop value** | FLA @ ANA | Lars Eller under 1.5 SOG | -170 | draftkings | 1.19 | 67% vs 59% (+14%) | $3 | — |
| 75 | **prop value** | FLA @ ANA | Brady Tkachuk over 0.5 A | +155 | betmgm | 0.54 | 42% vs 37% (+14%) | $1 | — |
| 76 | **prop value** | CGY @ SEA | Vince Dunn under 0.5 A | -155 | draftkings | 0.44 | 64% vs 57% (+14%) | $2 | — |
| 77 | **prop value** | FLA @ ANA | Jackson LaCombe over 1.5 SOG | -130 | draftkings | 2.06 | 60% vs 52% (+13%) | $2 | — |
| 78 | **prop value** | VGK @ VAN | Linus Karlsson under 1.5 SOG | -115 | draftkings | 1.51 | 56% vs 50% (+13%) | $1 | — |
| 79 | **prop value** | VGK @ VAN | Marco Rossi over 0.5 PTS | +110 | draftkings | 0.70 | 50% vs 44% (+13%) | $1 | — |
| 80 | **prop value** | UTA @ NYR | Logan Cooley under 1.5 SOG | +110 | draftkings | 1.71 | 50% vs 44% (+13%) | $1 | — |
| 81 | **prop value** | CGY @ SEA | Chandler Stephenson under 0.5 A | -165 | betmgm | 0.41 | 66% vs 58% (+13%) | $3 | — |
| 82 | **prop value** | CGY @ SEA | Mikael Backlund over 1.5 SOG | -152 | fanduel | 2.25 | 64% vs 57% (+13%) | $2 | — |
| 83 | **prop value** | CGY @ SEA | Brandon Montour over 2.5 SOG | +105 | draftkings | 2.77 | 51% vs 45% (+13%) | $1 | — |
| 84 | **prop value** | UTA @ NYR | J.T. Miller under 0.5 A | -185 | draftkings | 0.38 | 68% vs 60% (+13%) | $2 | — |
| 85 | **prop value** | UTA @ NYR | Lawson Crouse under 1.5 SOG | -110 | betmgm | 1.59 | 54% vs 48% (+13%) | $1 | — |
| 86 | **prop value** | FLA @ ANA | Anton Lundell over 1.5 SOG | -155 | draftkings | 2.25 | 64% vs 57% (+13%) | $2 | — |
| 87 | **prop value** | VGK @ VAN | Rasmus Andersson under 0.5 A | -210 | draftkings | 0.34 | 71% vs 63% (+13%) | $3 | — |
| 88 | **prop value** | VGK @ VAN | Mitch Marner under 1.5 PTS | -220 | betmgm | 1.05 | 72% vs 64% (+13%) | $2 | — |
| 89 | **prop value** | UTA @ NYR | Logan Cooley under 1.5 SOG | +105 | betmgm | 1.71 | 50% vs 45% (+13%) | $1 | — |
| 90 | **prop value** | FLA @ ANA | Aaron Ekblad under 0.5 PTS | -190 | betmgm | 0.37 | 69% vs 61% (+12%) | $2 | — |
| 91 | **prop value** | UTA @ NYR | Mika Zibanejad under 0.5 A | -155 | draftkings | 0.45 | 64% vs 57% (+12%) | $2 | — |
| 92 | **prop value** | CGY @ SEA | Zayne Parekh under 1.5 SOG | -125 | draftkings | 1.44 | 58% vs 52% (+12%) | $2 | — |
| 93 | **prop value** | CGY @ SEA | Matt Coronato under 0.5 A | -245 | draftkings | 0.29 | 75% vs 67% (+12%) | $3 | — |
| 94 | **prop value** | CGY @ SEA | Joel Farabee under 0.5 PTS | -160 | draftkings | 0.45 | 64% vs 57% (+12%) | $2 | — |
| 95 | **prop value** | FLA @ ANA | Jackson LaCombe over 1.5 SOG | -130 | fanduel | 2.06 | 60% vs 53% (+12%) | $2 | — |
| 96 | **prop value** | CGY @ SEA | Joel Farabee under 1.5 SOG | +105 | draftkings | 1.67 | 51% vs 46% (+12%) | $1 | — |
| 97 | **prop value** | CGY @ SEA | Kaapo Kakko over 0.5 PTS | +115 | draftkings | 0.67 | 49% vs 43% (+12%) | $1 | — |
| 98 | **prop value** | UTA @ NYR | Oliver Bjorkstrand under 0.5 PTS | -185 | betmgm | 0.39 | 68% vs 60% (+12%) | $2 | — |
| 99 | **prop value** | VGK @ VAN | Tomas Hertl under 0.5 PTS | +115 | betmgm | 0.72 | 49% vs 43% (+12%) | $1 | — |
| 100 | **prop value** | UTA @ NYR | Alexis Lafrenière under 1.5 SOG | +130 | fanduel | 1.86 | 46% vs 41% (+12%) | $1 | — |
| 101 | **prop value** | FLA @ ANA | Jacob Markstrom under 24.5 SV | -110 | draftkings | 24.28 | 54% vs 49% (+12%) | $1 | ⚠saves-model |
| 102 | **prop value** | UTA @ NYR | Clayton Keller under 2.5 SOG | -115 | draftkings | 2.50 | 55% vs 50% (+12%) | $1 | — |
| 103 | **prop value** | UTA @ NYR | Mika Zibanejad under 0.5 PTS | +135 | draftkings | 0.82 | 44% vs 40% (+12%) | $1 | — |
| 104 | **prop value** | FLA @ ANA | Anton Lundell over 1.5 SOG | -165 | betmgm | 2.25 | 64% vs 57% (+12%) | $1 | — |
| 105 | **prop value** | CGY @ SEA | Kaapo Kakko under 1.5 SOG | -140 | draftkings | 1.37 | 61% vs 54% (+11%) | $1 | — |
| 106 | **prop value** | UTA @ NYR | Pavel Dorofeyev under 2.5 SOG | -125 | betmgm | 2.44 | 57% vs 51% (+11%) | $1 | — |
| 107 | **prop value** | UTA @ NYR | Nick Schmaltz under 0.5 A | -190 | betmgm | 0.39 | 68% vs 61% (+11%) | $2 | — |
| 108 | **prop value** | CGY @ SEA | Jordan Eberle under 0.5 A | -190 | betmgm | 0.39 | 68% vs 61% (+11%) | $2 | — |
| 109 | **prop value** | VGK @ VAN | Rasmus Andersson under 0.5 A | -220 | betmgm | 0.34 | 71% vs 64% (+11%) | $2 | — |
| 110 | **prop value** | CGY @ SEA | Joel Farabee under 0.5 PTS | -160 | betmgm | 0.45 | 64% vs 58% (+11%) | $2 | — |
| 111 | **prop value** | VGK @ VAN | Marco Rossi under 1.5 SOG | -155 | betmgm | 1.34 | 62% vs 55% (+11%) | $1 | — |
| 112 | **prop value** | FLA @ ANA | Anton Lundell over 0.5 PTS | +100 | draftkings | 0.72 | 51% vs 46% (+11%) | $1 | — |
| 113 | **prop value** | UTA @ NYR | Mika Zibanejad under 2.5 SOG | -145 | betmgm | 2.30 | 60% vs 54% (+11%) | $1 | — |
| 114 | **prop value** | VGK @ VAN | Jack Eichel under 0.5 G | -210 | fanduel | 0.36 | 70% vs 63% (+11%) | $2 | — |
| 115 | **prop value** | VGK @ VAN | Mitch Marner under 1.5 PTS | -225 | draftkings | 1.05 | 72% vs 65% (+11%) | $2 | — |
| 116 | **prop value** | CGY @ SEA | Simon Nemec under 0.5 PTS | -210 | betmgm | 0.35 | 70% vs 63% (+11%) | $2 | — |
| 117 | **prop value** | UTA @ NYR | Oliver Bjorkstrand under 1.5 SOG | -125 | betmgm | 1.50 | 56% vs 51% (+11%) | — | — |
| 118 | **prop value** | FLA @ ANA | A.J. Greer under 1.5 SOG | -135 | betmgm | 1.46 | 58% vs 52% (+11%) | — | — |
| 119 | **prop value** | UTA @ NYR | Alexis Lafrenière under 0.5 PTS | -110 | draftkings | 0.62 | 54% vs 49% (+10%) | $1 | — |
| 120 | **prop value** | CGY @ SEA | Vince Dunn under 0.5 A | -165 | betmgm | 0.44 | 64% vs 58% (+10%) | $1 | — |
| 121 | **prop value** | CGY @ SEA | Bobby McMann under 2.5 SOG | -110 | draftkings | 2.57 | 53% vs 49% (+10%) | $1 | — |
| 122 | **prop value** | VGK @ VAN | Marco Rossi over 0.5 PTS | +105 | betmgm | 0.70 | 50% vs 46% (+10%) | $1 | — |
| 123 | **prop value** | FLA @ ANA | Mikael Granlund under 0.5 A | -185 | betmgm | 0.41 | 66% vs 60% (+10%) | $1 | — |
| 124 | **prop value** | UTA @ NYR | Will Cuylle under 1.5 SOG | +100 | betmgm | 1.70 | 50% vs 46% (+10%) | — | — |
| 125 | **prop value** | VGK @ VAN | Filip Hronek over 0.5 PTS | +120 | draftkings | 0.62 | 46% vs 42% (+10%) | — | — |
| 126 | **prop value** | FLA @ ANA | Leo Carlsson over 0.5 PTS | -145 | betmgm | 0.92 | 60% vs 55% (+10%) | $1 | — |
| 127 | **prop value** | VGK @ VAN | Mark Stone under 2.5 SOG | -175 | draftkings | 2.10 | 65% vs 59% (+10%) | $1 | — |
| 128 | **prop value** | CGY @ SEA | Joel Farabee under 1.5 SOG | +102 | fanduel | 1.67 | 51% vs 47% (+10%) | $1 | — |
| 129 | **prop value** | CGY @ SEA | Chandler Stephenson under 0.5 A | -180 | draftkings | 0.41 | 66% vs 60% (+10%) | $1 | — |
| 130 | **prop value** | FLA @ ANA | Cutter Gauthier over 0.5 PTS | -140 | betmgm | 0.91 | 60% vs 54% (+10%) | $1 | — |
| 131 | **prop value** | UTA @ NYR | Nick Schmaltz under 0.5 A | -200 | draftkings | 0.39 | 68% vs 62% (+10%) | $1 | — |
| 132 | **prop value** | FLA @ ANA | Lars Eller under 0.5 PTS | -235 | draftkings | 0.33 | 72% vs 65% (+10%) | $1 | — |
| 133 | **prop value** | FLA @ ANA | Lars Eller under 0.5 PTS | -235 | betmgm | 0.33 | 72% vs 65% (+10%) | $1 | — |
| 134 | **prop value** | FLA @ ANA | Carter Verhaeghe under 2.5 SOG | -155 | betmgm | 2.28 | 61% vs 55% (+9%) | — | — |
| 135 | **prop value** | CGY @ SEA | Vince Dunn under 0.5 PTS | -115 | draftkings | 0.60 | 55% vs 50% (+9%) | $1 | — |
| 136 | **prop value** | UTA @ NYR | Dylan Guenther under 2.5 SOG | +112 | fanduel | 2.80 | 48% vs 44% (+9%) | $1 | — |
| 137 | **prop value** | FLA @ ANA | Brady Tkachuk over 0.5 A | +145 | draftkings | 0.54 | 42% vs 38% (+9%) | — | — |
| 138 | **prop value** | CGY @ SEA | Jared McCann under 0.5 A | -175 | draftkings | 0.43 | 65% vs 59% (+9%) | $1 | — |
| 139 | **prop value** | VGK @ VAN | Mitch Marner under 0.5 G | -240 | fanduel | 0.33 | 72% vs 66% (+9%) | $1 | — |
| 140 | **prop value** | UTA @ NYR | Anders Lee under 0.5 PTS | -185 | draftkings | 0.42 | 66% vs 60% (+9%) | $1 | — |
| 141 | **prop value** | UTA @ NYR | Alexis Lafrenière under 0.5 A | -220 | betmgm | 0.36 | 70% vs 64% (+9%) | $1 | — |
| 142 | **prop value** | VGK @ VAN | William Karlsson under 0.5 A | -235 | betmgm | 0.34 | 71% vs 65% (+9%) | $1 | — |
| 143 | **prop value** | VGK @ VAN | Mitch Marner under 2.5 SOG | -155 | betmgm | 2.29 | 60% vs 55% (+9%) | — | — |
| 144 | **prop value** | UTA @ NYR | Pavel Dorofeyev under 0.5 PTS | -105 | betmgm | 0.65 | 52% vs 48% (+9%) | $1 | — |
| 145 | **prop value** | UTA @ NYR | Nick Schmaltz over 1.5 SOG | -235 | betmgm | 2.43 | 68% vs 62% (+9%) | — | — |
| 146 | **prop value** | UTA @ NYR | Mika Zibanejad under 0.5 PTS | +130 | betmgm | 0.82 | 44% vs 41% (+9%) | — | — |
| 147 | **prop value** | FLA @ ANA | Alex Killorn under 1.5 SOG | -105 | betmgm | 1.68 | 51% vs 47% (+9%) | — | — |
| 148 | **prop value** | FLA @ ANA | Mikael Granlund under 0.5 PTS | +110 | betmgm | 0.73 | 48% vs 44% (+9%) | — | — |
| 149 | **prop value** | UTA @ NYR | Logan Cooley under 0.5 A | -235 | betmgm | 0.34 | 71% vs 65% (+9%) | $1 | — |
| 150 | **prop value** | VGK @ VAN | Linus Karlsson over 0.5 PTS | +145 | draftkings | 0.53 | 41% vs 38% (+9%) | — | — |
| 151 | **prop value** | CGY @ SEA | Brandon Montour over 2.5 SOG | +100 | fanduel | 2.77 | 51% vs 47% (+9%) | $1 | — |
| 152 | **prop value** | CGY @ SEA | Jared McCann under 0.5 PTS | +125 | betmgm | 0.79 | 45% vs 42% (+9%) | — | — |
| 153 | **prop value** | FLA @ ANA | Alex Killorn under 0.5 PTS | -165 | betmgm | 0.46 | 63% vs 58% (+9%) | $1 | — |
| 154 | **prop value** | CGY @ SEA | Kaapo Kakko over 0.5 A | +200 | draftkings | 0.41 | 34% vs 31% (+9%) | — | — |
| 155 | **prop value** | UTA @ NYR | Pavel Dorofeyev under 0.5 G | -240 | fanduel | 0.33 | 72% vs 66% (+9%) | $1 | — |
| 156 | **prop value** | FLA @ ANA | Matthew Tkachuk under 2.5 SOG | +100 | draftkings | 2.72 | 50% vs 46% (+9%) | — | — |
| 157 | **prop value** | FLA @ ANA | Sam Bennett over 0.5 A | +180 | betmgm | 0.45 | 36% vs 33% (+8%) | — | — |
| 158 | **prop value** | FLA @ ANA | Sam Reinhart over 2.5 SOG | +120 | fanduel | 2.56 | 46% vs 43% (+8%) | — | — |
| 159 | **prop value** | VGK @ VAN | Shea Theodore under 1.5 SOG | +132 | fanduel | 1.94 | 44% vs 40% (+8%) | — | — |
| 160 | **prop value** | FLA @ ANA | Brady Tkachuk over 2.5 SOG | -170 | draftkings | 3.39 | 63% vs 59% (+8%) | — | — |
| 161 | **prop value** | UTA @ NYR | Mikhail Sergachev under 0.5 A | -155 | betmgm | 0.49 | 61% vs 57% (+8%) | — | — |
| 162 | **prop value** | VGK @ VAN | Rasmus Andersson under 1.5 SOG | +130 | betmgm | 1.96 | 43% vs 40% (+8%) | — | — |
| 163 | **prop value** | UTA @ NYR | Clayton Keller under 0.5 PTS | +140 | draftkings | 0.87 | 42% vs 39% (+8%) | — | — |
| 164 | **prop value** | FLA @ ANA | Anton Lundell over 0.5 A | +190 | draftkings | 0.43 | 35% vs 32% (+8%) | — | — |
| 165 | **prop value** | UTA @ NYR | Clayton Keller under 2.5 SOG | -120 | fanduel | 2.50 | 55% vs 51% (+8%) | — | — |

## 2. Projections (first 40 by game)

```
Game        Player                    Pos Market  Line   Proj  P(over)   Over/Under  Book
UTA @ NYR   Igor Shesterkin           G   SV      27.5  25.31      36%    -115/-120  draftkings
UTA @ NYR   Igor Shesterkin           G   SV      27.5  25.31      36%    -114/-114  fanduel
UTA @ NYR   Pavel Dorofeyev           R   SOG      2.5   2.44      43%    -145/+105  draftkings
UTA @ NYR   Pavel Dorofeyev           R   SOG      2.5   2.44      43%    -144/+110  fanduel
UTA @ NYR   Pavel Dorofeyev           R   SOG      2.5   2.44      43%    -115/-125  betmgm
UTA @ NYR   Mika Zibanejad            C   SOG      2.5   2.30      40%    -110/-125  draftkings
UTA @ NYR   Mika Zibanejad            C   SOG      2.5   2.30      40%    -108/-120  fanduel
UTA @ NYR   Mika Zibanejad            C   SOG      2.5   2.30      40%    +100/-145  betmgm
UTA @ NYR   Alexis Lafrenière         L   SOG      1.5   1.86      54%    -185/+135  draftkings
UTA @ NYR   Alexis Lafrenière         L   SOG      1.5   1.86      54%    -170/+130  fanduel
UTA @ NYR   Alexis Lafrenière         L   SOG      1.5   1.86      54%    -200/+130  betmgm
UTA @ NYR   J.T. Miller               C   SOG      1.5   1.73      50%    -165/+120  draftkings
UTA @ NYR   J.T. Miller               C   SOG      1.5   1.73      50%    -164/+125  fanduel
UTA @ NYR   J.T. Miller               C   SOG      1.5   1.73      50%    -220/+130  betmgm
UTA @ NYR   Will Cuylle               L   SOG      1.5   1.70      50%    -120/-110  draftkings
UTA @ NYR   Will Cuylle               L   SOG      1.5   1.70      50%    -118/-110  fanduel
UTA @ NYR   Will Cuylle               L   SOG      1.5   1.70      50%    -145/+100  betmgm
UTA @ NYR   Oliver Bjorkstrand        R   SOG      1.5   1.50      44%    +105/-140  draftkings
UTA @ NYR   Oliver Bjorkstrand        R   SOG      1.5   1.50      44%    -115/-125  betmgm
UTA @ NYR   Eeli Tolvanen             R   SOG      1.5   1.48      43%    +100/-140  draftkings
UTA @ NYR   Gabe Perreault            R   SOG      1.5   1.30      37%    +100/-135  draftkings
UTA @ NYR   Gabe Perreault            R   SOG      1.5   1.30      37%    -120/-120  betmgm
UTA @ NYR   Adam Fox                  D   SOG      1.5   1.29      37%    -115/-115  draftkings
UTA @ NYR   Adam Fox                  D   SOG      1.5   1.29      37%    -120/-120  betmgm
UTA @ NYR   Mika Zibanejad            C   PTS      0.5   0.82      56%    -185/+135  draftkings
UTA @ NYR   Mika Zibanejad            C   PTS      0.5   0.82      56%    -175/+130  betmgm
UTA @ NYR   Adam Fox                  D   PTS      0.5   0.72      51%    -180/+130  draftkings
UTA @ NYR   Adam Fox                  D   PTS      0.5   0.72      51%    -160/+120  betmgm
UTA @ NYR   Pavel Dorofeyev           R   PTS      0.5   0.65      48%    -125/-110  draftkings
UTA @ NYR   Pavel Dorofeyev           R   PTS      0.5   0.65      48%    -125/-105  betmgm
UTA @ NYR   Alexis Lafrenière         L   PTS      0.5   0.62      46%    -125/-110  draftkings
UTA @ NYR   Alexis Lafrenière         L   PTS      0.5   0.62      46%    -135/+100  betmgm
UTA @ NYR   J.T. Miller               C   PTS      0.5   0.59      45%    -130/+100  draftkings
UTA @ NYR   J.T. Miller               C   PTS      0.5   0.59      45%    -155/+115  betmgm
UTA @ NYR   Adam Fox                  D   A        0.5   0.57      43%    -135/+100  draftkings
UTA @ NYR   Adam Fox                  D   A        0.5   0.57      43%    -125/-105  betmgm
UTA @ NYR   Gabe Perreault            R   PTS      0.5   0.49      39%    +125/-170  draftkings
UTA @ NYR   Gabe Perreault            R   PTS      0.5   0.49      39%    +120/-160  betmgm
UTA @ NYR   Mika Zibanejad            C   A        0.5   0.45      36%    +115/-155  draftkings
UTA @ NYR   Mika Zibanejad            C   A        0.5   0.45      36%    +100/-135  betmgm
```

## 3. NHL paper ledger to date

```
NHL prop paper bets — settled by market/side/strength (pending: 236)
market                    side   str    n   W   L   P   staked   profit     ROI
player_assists            over     2   24  10  14   0    47.00     0.64   +1.4%
player_assists            under    2   31  14  17   0   120.00   -32.91  -27.4%
player_goals              over     2    4   0   4   0    10.00   -10.00 -100.0%
player_goals              under    2    3   0   3   0     9.00    -9.00 -100.0%
player_points             over     2   46  15  31   0   113.00   -34.99  -31.0%
player_points             under    2   32  16  16   0   116.00   -10.46   -9.0%
player_shots_on_goal      over     2   35  19  16   0   118.00     8.68   +7.4%
player_shots_on_goal      under    2   99  53  46   0   364.00     7.68   +2.1%
player_assists            over     1   34  14  20   0    26.00    -1.44   -5.5%
player_assists            under    1  187 114  73   0   116.00   -10.90   -9.4%
player_goals              over     1   11   5   6   0     3.00     5.50 +183.3%
player_goals              under    1   41  23  18   0    19.00     3.43  +18.1%
player_points             over     1  118  52  66   0    74.00   -28.45  -38.4%
player_points             under    1  207 111  95   1    73.00    -7.69  -10.5%
player_shots_on_goal      over     1  147  70  77   0    77.00   -18.14  -23.6%
player_shots_on_goal      under    1  221 120 100   1   106.00   -12.12  -11.4%
player_total_saves        over     1    7   4   3   0    24.00     4.48  +18.7%
player_total_saves        under    1   18  10   8   0    54.00    -4.25   -7.9%
```

> Paper only. The projection is tested walk-forward (fit on 2024-25, scored on every 2025-26 game: `--calibrate`, `analysis/06`), but no historical prop prices exist, so ROI against posted lines is untested until the ledger fills. The ledger above is that evidence.

## Tonight's ask: one lock at a decent line, a goalie prop, three parlay legs (BetRivers)

Four games tonight. BetRivers allows **overs on everything but unders on assists only** (no SOG, points, goals or saves unders), so every other under is excluded here. Ranked by the blend (25% model, 75% de-vigged line), sides where both model and market say > 50%, model-vs-market gap ≤ +30%. Prices are DK/FD/BetMGM (The Odds API carries almost no BetRivers NHL props); check the number at BetRivers. Paper only.

**One lock at a decent line**

| Game (CT) | Pick | Price | Proj | Model · Fair · Blend |
|---|---|---|---|---|
| CGY @ SEA 7:00 PM | **Jared McCann under 0.5 A** | -175 @draftkings | 0.43 | 65% · 59% · 60.8% (EV -4.5% at the blend) |

Top blend among sides priced −175..+120 under the BetRivers rules. Small gap (+9%), so model and market tell the same story. Nothing in that window is +EV at the blend tonight. If you want a shots over instead: Jordan Eberle over 1.5 SOG −174 @fanduel (CGY @ SEA, proj 2.20, blend 60.4%, EV −4.9%).

**Goalie prop (overs only)**

| Game (CT) | Pick | Price | Proj | Model · Fair · Blend |
|---|---|---|---|---|
| CGY @ SEA 7:00 PM | **Joey Daccord over 23.5 saves** | -105 @draftkings | 25.1 | 56% · 48% · 49.9% (EV -2.6% at the blend) |

Best EV of any saves over and the only one the model likes: it projects 25.1 saves against a 23.5 line. It's a coin flip at the blend, not a lock. Highest blend is Lukas Dostal over 23.5 −130 (FLA @ ANA, 52.1%), but at −130 that's EV −7.8%. Every other saves over has the model below the market. Saves are capped at strength 1 (`SAVES_MAX_STRENGTH`) and the saves ledger is tiny (25 settled).

**Three parlay legs (−300..−200, one per game, all assist unders)**

| Game (CT) | Pick | Price | Proj | Model · Fair · Blend |
|---|---|---|---|---|
| CGY @ SEA 7:00 PM | Zayne Parekh under 0.5 A | -295 @betmgm | 0.19 | 82% · 69% · 72.9% |
| UTA @ NYR 5:00 PM | Oliver Bjorkstrand under 0.5 A | -300 @betmgm | 0.24 | 78% · 69% · 71.7% |
| FLA @ ANA 7:00 PM | Alex Killorn under 0.5 A | -285 @betmgm | 0.25 | 78% · 69% · 71.0% |

Three legs together at the blend: **37% to cash**, parlay pays about **+141** (decimal 2.41), EV about −11% at the blend. Each leg alone misses roughly 3 times in 10. 4th leg from the last game: Brock Boeser under 0.5 A −290 @draftkings (VGK @ VAN, blend 69.9%).

The full board is §1 above (it keeps every side for the paper ledger); the BetRivers board below is the one to bet from.

## BetRivers board: §1 with only overs and assist unders

BetRivers allows the under on assists only, so this is §1 with the 106 SOG, points, goals and saves unders removed: 59 plays, same order and numbers (# is the §1 rank). Paper only.

| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| 3 | **STRONG PROP** | VGK @ VAN | Shea Theodore under 0.5 A | -115 | betmgm | 0.45 | 64% vs 50% (+28%) | $5 | — |
| 12 | **STRONG PROP** | CGY @ SEA | Kaapo Kakko over 0.5 PTS | +140 | betmgm | 0.67 | 49% vs 39% (+25%) | $3 | — |
| 17 | **STRONG PROP** | UTA @ NYR | J.T. Miller under 0.5 A | -150 | betmgm | 0.38 | 68% vs 56% (+22%) | $5 | — |
| 19 | **STRONG PROP** | UTA @ NYR | Adam Fox under 0.5 A | +100 | draftkings | 0.57 | 57% vs 47% (+22%) | $3 | — |
| 20 | **STRONG PROP** | CGY @ SEA | Morgan Frost under 0.5 A | -225 | betmgm | 0.24 | 79% vs 65% (+22%) | $5 | — |
| 25 | **STRONG PROP** | UTA @ NYR | Mika Zibanejad under 0.5 A | -135 | betmgm | 0.45 | 64% vs 53% (+19%) | $4 | — |
| 29 | **STRONG PROP** | UTA @ NYR | Adam Fox under 0.5 A | -105 | betmgm | 0.57 | 57% vs 48% (+18%) | $3 | — |
| 32 | **STRONG PROP** | VGK @ VAN | Filip Hronek over 0.5 A | +175 | draftkings | 0.51 | 40% vs 34% (+18%) | $2 | — |
| 40 | **STRONG PROP** | FLA @ ANA | Eetu Luostarinen over 0.5 PTS | +180 | draftkings | 0.50 | 39% vs 33% (+17%) | $1 | — |
| 45 | **STRONG PROP** | CGY @ SEA | Kaapo Kakko over 0.5 A | +220 | betmgm | 0.41 | 34% vs 29% (+17%) | $1 | — |
| 48 | **STRONG PROP** | CGY @ SEA | Matvei Gridin under 0.5 A | -220 | betmgm | 0.30 | 74% vs 64% (+16%) | $4 | — |
| 52 | **STRONG PROP** | FLA @ ANA | Seth Jones over 1.5 SOG | +100 | draftkings | 1.84 | 54% vs 47% (+15%) | $2 | — |
| 60 | **prop value** | CGY @ SEA | Joey Daccord over 23.5 SV | -105 | draftkings | 25.13 | 56% vs 48% (+16%) | $2 | ⚠saves-model |
| 62 | **prop value** | CGY @ SEA | Mikael Backlund over 1.5 SOG | -150 | draftkings | 2.25 | 64% vs 56% (+15%) | $3 | — |
| 63 | **prop value** | VGK @ VAN | Tomas Hertl over 1.5 SOG | -220 | betmgm | 2.56 | 70% vs 61% (+15%) | $1 | — |
| 69 | **prop value** | VGK @ VAN | Shea Theodore under 0.5 A | -150 | draftkings | 0.45 | 64% vs 56% (+14%) | $2 | — |
| 70 | **prop value** | VGK @ VAN | Mitch Marner under 0.5 A | +115 | betmgm | 0.70 | 50% vs 43% (+14%) | $1 | — |
| 73 | **prop value** | FLA @ ANA | Anton Lundell over 1.5 SOG | -148 | fanduel | 2.25 | 64% vs 56% (+14%) | $3 | — |
| 75 | **prop value** | FLA @ ANA | Brady Tkachuk over 0.5 A | +155 | betmgm | 0.54 | 42% vs 37% (+14%) | $1 | — |
| 76 | **prop value** | CGY @ SEA | Vince Dunn under 0.5 A | -155 | draftkings | 0.44 | 64% vs 57% (+14%) | $2 | — |
| 77 | **prop value** | FLA @ ANA | Jackson LaCombe over 1.5 SOG | -130 | draftkings | 2.06 | 60% vs 52% (+13%) | $2 | — |
| 79 | **prop value** | VGK @ VAN | Marco Rossi over 0.5 PTS | +110 | draftkings | 0.70 | 50% vs 44% (+13%) | $1 | — |
| 81 | **prop value** | CGY @ SEA | Chandler Stephenson under 0.5 A | -165 | betmgm | 0.41 | 66% vs 58% (+13%) | $3 | — |
| 82 | **prop value** | CGY @ SEA | Mikael Backlund over 1.5 SOG | -152 | fanduel | 2.25 | 64% vs 57% (+13%) | $2 | — |
| 83 | **prop value** | CGY @ SEA | Brandon Montour over 2.5 SOG | +105 | draftkings | 2.77 | 51% vs 45% (+13%) | $1 | — |
| 84 | **prop value** | UTA @ NYR | J.T. Miller under 0.5 A | -185 | draftkings | 0.38 | 68% vs 60% (+13%) | $2 | — |
| 86 | **prop value** | FLA @ ANA | Anton Lundell over 1.5 SOG | -155 | draftkings | 2.25 | 64% vs 57% (+13%) | $2 | — |
| 87 | **prop value** | VGK @ VAN | Rasmus Andersson under 0.5 A | -210 | draftkings | 0.34 | 71% vs 63% (+13%) | $3 | — |
| 91 | **prop value** | UTA @ NYR | Mika Zibanejad under 0.5 A | -155 | draftkings | 0.45 | 64% vs 57% (+12%) | $2 | — |
| 93 | **prop value** | CGY @ SEA | Matt Coronato under 0.5 A | -245 | draftkings | 0.29 | 75% vs 67% (+12%) | $3 | — |
| 95 | **prop value** | FLA @ ANA | Jackson LaCombe over 1.5 SOG | -130 | fanduel | 2.06 | 60% vs 53% (+12%) | $2 | — |
| 97 | **prop value** | CGY @ SEA | Kaapo Kakko over 0.5 PTS | +115 | draftkings | 0.67 | 49% vs 43% (+12%) | $1 | — |
| 104 | **prop value** | FLA @ ANA | Anton Lundell over 1.5 SOG | -165 | betmgm | 2.25 | 64% vs 57% (+12%) | $1 | — |
| 107 | **prop value** | UTA @ NYR | Nick Schmaltz under 0.5 A | -190 | betmgm | 0.39 | 68% vs 61% (+11%) | $2 | — |
| 108 | **prop value** | CGY @ SEA | Jordan Eberle under 0.5 A | -190 | betmgm | 0.39 | 68% vs 61% (+11%) | $2 | — |
| 109 | **prop value** | VGK @ VAN | Rasmus Andersson under 0.5 A | -220 | betmgm | 0.34 | 71% vs 64% (+11%) | $2 | — |
| 112 | **prop value** | FLA @ ANA | Anton Lundell over 0.5 PTS | +100 | draftkings | 0.72 | 51% vs 46% (+11%) | $1 | — |
| 120 | **prop value** | CGY @ SEA | Vince Dunn under 0.5 A | -165 | betmgm | 0.44 | 64% vs 58% (+10%) | $1 | — |
| 122 | **prop value** | VGK @ VAN | Marco Rossi over 0.5 PTS | +105 | betmgm | 0.70 | 50% vs 46% (+10%) | $1 | — |
| 123 | **prop value** | FLA @ ANA | Mikael Granlund under 0.5 A | -185 | betmgm | 0.41 | 66% vs 60% (+10%) | $1 | — |
| 125 | **prop value** | VGK @ VAN | Filip Hronek over 0.5 PTS | +120 | draftkings | 0.62 | 46% vs 42% (+10%) | — | — |
| 126 | **prop value** | FLA @ ANA | Leo Carlsson over 0.5 PTS | -145 | betmgm | 0.92 | 60% vs 55% (+10%) | $1 | — |
| 129 | **prop value** | CGY @ SEA | Chandler Stephenson under 0.5 A | -180 | draftkings | 0.41 | 66% vs 60% (+10%) | $1 | — |
| 130 | **prop value** | FLA @ ANA | Cutter Gauthier over 0.5 PTS | -140 | betmgm | 0.91 | 60% vs 54% (+10%) | $1 | — |
| 131 | **prop value** | UTA @ NYR | Nick Schmaltz under 0.5 A | -200 | draftkings | 0.39 | 68% vs 62% (+10%) | $1 | — |
| 137 | **prop value** | FLA @ ANA | Brady Tkachuk over 0.5 A | +145 | draftkings | 0.54 | 42% vs 38% (+9%) | — | — |
| 138 | **prop value** | CGY @ SEA | Jared McCann under 0.5 A | -175 | draftkings | 0.43 | 65% vs 59% (+9%) | $1 | — |
| 141 | **prop value** | UTA @ NYR | Alexis Lafrenière under 0.5 A | -220 | betmgm | 0.36 | 70% vs 64% (+9%) | $1 | — |
| 142 | **prop value** | VGK @ VAN | William Karlsson under 0.5 A | -235 | betmgm | 0.34 | 71% vs 65% (+9%) | $1 | — |
| 145 | **prop value** | UTA @ NYR | Nick Schmaltz over 1.5 SOG | -235 | betmgm | 2.43 | 68% vs 62% (+9%) | — | — |
| 149 | **prop value** | UTA @ NYR | Logan Cooley under 0.5 A | -235 | betmgm | 0.34 | 71% vs 65% (+9%) | $1 | — |
| 150 | **prop value** | VGK @ VAN | Linus Karlsson over 0.5 PTS | +145 | draftkings | 0.53 | 41% vs 38% (+9%) | — | — |
| 151 | **prop value** | CGY @ SEA | Brandon Montour over 2.5 SOG | +100 | fanduel | 2.77 | 51% vs 47% (+9%) | $1 | — |
| 154 | **prop value** | CGY @ SEA | Kaapo Kakko over 0.5 A | +200 | draftkings | 0.41 | 34% vs 31% (+9%) | — | — |
| 157 | **prop value** | FLA @ ANA | Sam Bennett over 0.5 A | +180 | betmgm | 0.45 | 36% vs 33% (+8%) | — | — |
| 158 | **prop value** | FLA @ ANA | Sam Reinhart over 2.5 SOG | +120 | fanduel | 2.56 | 46% vs 43% (+8%) | — | — |
| 160 | **prop value** | FLA @ ANA | Brady Tkachuk over 2.5 SOG | -170 | draftkings | 3.39 | 63% vs 59% (+8%) | — | — |
| 161 | **prop value** | UTA @ NYR | Mikhail Sergachev under 0.5 A | -155 | betmgm | 0.49 | 61% vs 57% (+8%) | — | — |
| 164 | **prop value** | FLA @ ANA | Anton Lundell over 0.5 A | +190 | draftkings | 0.43 | 35% vs 32% (+8%) | — | — |

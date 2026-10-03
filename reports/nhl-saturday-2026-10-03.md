# NHL Prop Report — Saturday, October 03, 2026

**Generated:** 2026-10-03 02:52 PM CDT  
**STAKES: PAPER ONLY as of 2026-09-20 — no bucket has a 95% CI above zero. $Bet is what the paper ledger logs, not a recommendation to bet real money.**  
**Slate:** 13 games · 977 prop lines matched to rostered players (The Odds API)  
**Model (skaters, since 2026-09-30):** per-minute rate × projected minutes. The rate is this season's stat per minute blended with last season's (weight a1) and regressed toward the position mean (K ghost minutes: shots 86, points 234, goals 694); minutes lean 56% on the last 5 games. × opponent allowance^β × home/away split → Poisson P(over) (shots: gamma-Poisson k=17.5; goalie saves: old per-start recipe, k=20). Fit on 2024-25, tested on every 2025-26 skater-game: better log-loss than the old recipe at every line of every stat. Tiers +8% / +15%, ≥ +30% demoted (⚠overreach).

## The lock, and five good ones

**The lock** is the top of the agreement board: the prop side the projection and the de-vigged line both favour, priced -250..-110, model above fair by no more than +20%, ranked by the **blend** (25% model, 75% de-vigged line, in logit space: the market has been sharper everywhere so far). **Good** is the rest of that board, then the ranked value props (§1), one per player. EV is at the blend; at −220..−250 the juice usually outweighs what the model adds, so these are the likeliest winners, not value bets. Paper only.

| | Puck (CT) | Game | Play | Why |
|---|---|---|---|---|
| **LOCK** | 9:00 PM | CGY @ VAN | **Morgan Frost under 0.5 A -245 @draftkings** | proj 0.26 → model 77% · fair 67% · blend 69% (EV -2.4% at the blend, agree) |
| good 1 | 7:00 PM | BOS @ MIN | Quinn Hughes under 1.5 PTS -245 @draftkings | proj 0.92 → model 77% · fair 67% · blend 69% (EV -2.5% at the blend, agree) |
| good 2 | 7:00 PM | BOS @ MIN | Maxim Shabanov under 0.5 A -250 @draftkings | proj 0.29 → model 75% · fair 67% · blend 69% (EV -3.7% at the blend, agree) |
| good 3 | 6:00 PM | SEA @ EDM | Connor McDavid under 1.5 A -245 @draftkings | proj 1.01 → model 73% · fair 67% · blend 68% (EV -3.8% at the blend, agree) |
| good 4 | 7:00 PM | BOS @ MIN | David Pastrnak under 0.5 G -240 @fanduel | proj 0.30 → model 74% · fair 66% · blend 68% (EV -3.4% at the blend, agree) |
| good 5 | 9:00 PM | CGY @ VAN | Zeev Buium under 0.5 A -235 @draftkings | proj 0.30 → model 74% · fair 66% · blend 68% (EV -3.0% at the blend, agree) |

At the blend's 69%, a lock like this misses about 3 nights in 10; the chance of at least one miss in a five-night week is 84%.

### Simulated 20,000 nights of that card

Each ticket keeps its own chance to cash; the simulation adds how they move together (teammates share a game-level factor, latent ρ 0.1047 points / 0.0525 assists, measured on 2025-26 logs; opponents independent). Run three times: trusting the model, the blend (25% model), and the de-vigged market. Flat $1 a ticket; the parlay column is all legs in one ticket at the product of the prices.

| If this is right | Exp. hits of 6 | P(all 6) | P(≥5) | $1 each: exp. | P(up) | 5th–95th pct | 6-leg parlay +689: EV |
|---|---|---|---|---|---|---|---|
| model | 4.49 | 17.5% | 53% | +0.34 | 53% | -1.78 to +2.47 | +38% |
| blend | 4.11 | 10.4% | 39% | -0.19 | 39% | -3.18 to +2.47 | -18% |
| market | 3.97 | 8.4% | 34% | -0.39 | 34% | -3.18 to +2.47 | -34% |

## 1. Ranked props

| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **STRONG PROP** | STL @ COL | Martin Necas under 2.5 SOG | +120 | fanduel | 2.49 | 56% vs 43% (+30%) | $5 | — |
| 2 | **STRONG PROP** | DAL @ NSH | Esa Lindell under 1.5 SOG | -160 | draftkings | 0.98 | 74% vs 58% (+29%) | $5 | — |
| 3 | **STRONG PROP** | SEA @ EDM | Jake Walman under 1.5 SOG | +115 | draftkings | 1.52 | 56% vs 43% (+29%) | $4 | — |
| 4 | **STRONG PROP** | WSH @ TBL | Aliaksei Protas over 0.5 PTS | +165 | draftkings | 0.61 | 46% vs 35% (+29%) | $3 | — |
| 5 | **STRONG PROP** | BOS @ MIN | Maxim Shabanov under 1.5 SOG | +110 | draftkings | 1.47 | 57% vs 45% (+29%) | $5 | — |
| 6 | **STRONG PROP** | CHI @ BUF | Jiri Kulich under 1.5 SOG | -115 | draftkings | 1.26 | 64% vs 50% (+29%) | $5 | — |
| 7 | **STRONG PROP** | CGY @ VAN | Filip Hronek under 1.5 SOG | +145 | draftkings | 1.75 | 49% vs 38% (+28%) | $3 | — |
| 8 | **STRONG PROP** | OTT @ TOR | William Nylander under 2.5 SOG | -120 | draftkings | 2.10 | 65% vs 51% (+28%) | $5 | — |
| 9 | **STRONG PROP** | SEA @ EDM | Vasily Podkolzin under 0.5 PTS | +115 | draftkings | 0.59 | 55% vs 43% (+28%) | $4 | — |
| 10 | **STRONG PROP** | STL @ COL | Colton Parayko under 1.5 SOG | -118 | fanduel | 1.24 | 65% vs 51% (+28%) | $5 | — |
| 11 | **STRONG PROP** | SEA @ EDM | Ryan Shea over 0.5 PTS | +200 | draftkings | 0.51 | 40% vs 31% (+27%) | $2 | — |
| 12 | **STRONG PROP** | WSH @ TBL | John Carlson under 0.5 A | +105 | draftkings | 0.55 | 58% vs 46% (+27%) | $4 | — |
| 13 | **STRONG PROP** | CAR @ PHI | Porter Martone under 2.5 SOG | -190 | draftkings | 1.62 | 77% vs 61% (+27%) | $5 | — |
| 14 | **STRONG PROP** | CGY @ VAN | Zayne Parekh under 1.5 SOG | -110 | draftkings | 1.36 | 61% vs 49% (+26%) | $5 | — |
| 15 | **STRONG PROP** | STL @ COL | Martin Necas under 0.5 A | +125 | draftkings | 0.65 | 52% vs 41% (+26%) | $3 | — |
| 16 | **STRONG PROP** | SEA @ EDM | Ryan Winterton over 0.5 PTS | +245 | draftkings | 0.42 | 34% vs 27% (+26%) | $2 | — |
| 17 | **STRONG PROP** | LAK @ SJS | Dmitry Orlov under 1.5 SOG | -160 | draftkings | 1.04 | 72% vs 58% (+26%) | $5 | — |
| 18 | **STRONG PROP** | CGY @ VAN | Zeev Buium under 1.5 SOG | -125 | draftkings | 1.24 | 65% vs 52% (+25%) | $5 | — |
| 19 | **STRONG PROP** | CGY @ VAN | Zayne Parekh under 1.5 SOG | -108 | fanduel | 1.36 | 61% vs 49% (+25%) | $5 | — |
| 20 | **STRONG PROP** | WSH @ TBL | Alex Ovechkin under 2.5 SOG | -115 | draftkings | 2.20 | 63% vs 50% (+25%) | $5 | — |
| 21 | **STRONG PROP** | SEA @ EDM | Connor Murphy under 1.5 SOG | -145 | draftkings | 1.15 | 68% vs 55% (+25%) | $5 | — |
| 22 | **STRONG PROP** | LAK @ SJS | Quinton Byfield under 2.5 SOG | -108 | fanduel | 2.27 | 61% vs 49% (+25%) | $5 | — |
| 23 | **STRONG PROP** | LAK @ SJS | Mason Marchment under 1.5 SOG | +114 | fanduel | 1.56 | 55% vs 44% (+24%) | $4 | — |
| 24 | **STRONG PROP** | STL @ COL | Cale Makar under 1.5 PTS | -225 | draftkings | 0.81 | 81% vs 65% (+24%) | $5 | — |
| 25 | **STRONG PROP** | CGY @ VAN | Matt Coronato under 2.5 SOG | -118 | fanduel | 2.18 | 63% vs 51% (+24%) | $5 | — |
| 26 | **STRONG PROP** | CGY @ VAN | Zayne Parekh under 0.5 A | -235 | draftkings | 0.21 | 81% vs 65% (+24%) | $5 | — |
| 27 | **STRONG PROP** | LAK @ SJS | Darnell Nurse under 1.5 SOG | +125 | draftkings | 1.66 | 51% vs 41% (+24%) | $3 | — |
| 28 | **STRONG PROP** | MTL @ PIT | Chris Kreider under 1.5 SOG | +115 | draftkings | 1.59 | 54% vs 43% (+24%) | $3 | — |
| 29 | **STRONG PROP** | UTA @ CBJ | Kent Johnson under 1.5 SOG | +105 | draftkings | 1.51 | 56% vs 45% (+24%) | $4 | — |
| 30 | **STRONG PROP** | CGY @ VAN | Morgan Frost under 2.5 SOG | -198 | fanduel | 1.62 | 77% vs 62% (+24%) | $5 | — |
| 31 | **STRONG PROP** | OTT @ TOR | William Eklund over 1.5 SOG | -140 | draftkings | 2.41 | 67% vs 54% (+24%) | $5 | — |
| 32 | **STRONG PROP** | WSH @ TBL | Pierre-Luc Dubois under 1.5 SOG | -135 | draftkings | 1.21 | 66% vs 53% (+24%) | $5 | — |
| 33 | **STRONG PROP** | CHI @ BUF | Mattias Samuelsson over 0.5 PTS | +190 | draftkings | 0.51 | 40% vs 32% (+24%) | $2 | — |
| 34 | **STRONG PROP** | STL @ COL | Devon Toews under 0.5 PTS | -150 | draftkings | 0.37 | 69% vs 56% (+24%) | $5 | — |
| 35 | **STRONG PROP** | MTL @ PIT | Mike Matheson over 0.5 PTS | +215 | draftkings | 0.46 | 37% vs 30% (+24%) | $2 | — |
| 36 | **STRONG PROP** | WSH @ TBL | Victor Hedman under 1.5 SOG | +100 | draftkings | 1.47 | 57% vs 47% (+23%) | $4 | — |
| 37 | **STRONG PROP** | CGY @ VAN | Matt Coronato under 2.5 SOG | -125 | draftkings | 2.18 | 63% vs 51% (+23%) | $4 | — |
| 38 | **STRONG PROP** | CAR @ PHI | Eric Robinson under 1.5 SOG | -140 | draftkings | 1.19 | 67% vs 54% (+23%) | $5 | — |
| 39 | **STRONG PROP** | UTA @ CBJ | Kent Johnson under 0.5 A | -220 | draftkings | 0.24 | 79% vs 64% (+22%) | $5 | — |
| 40 | **STRONG PROP** | STL @ COL | Brent Burns under 1.5 SOG | +130 | draftkings | 1.73 | 49% vs 40% (+22%) | $3 | — |
| 41 | **STRONG PROP** | UTA @ CBJ | Ryan Lomberg over 0.5 SOG | -110 | draftkings | 0.92 | 59% vs 49% (+22%) | $4 | — |
| 42 | **STRONG PROP** | UTA @ CBJ | Dylan Guenther under 3.5 SOG | -170 | draftkings | 2.68 | 71% vs 59% (+22%) | $5 | — |
| 43 | **STRONG PROP** | CGY @ VAN | Morgan Frost under 0.5 PTS | -115 | draftkings | 0.51 | 60% vs 50% (+22%) | $4 | — |
| 44 | **STRONG PROP** | LAK @ SJS | Adrian Kempe under 2.5 SOG | +134 | fanduel | 2.78 | 49% vs 40% (+21%) | $3 | — |
| 45 | **STRONG PROP** | OTT @ TOR | Claude Giroux over 0.5 A | +240 | draftkings | 0.41 | 34% vs 28% (+21%) | $1 | — |
| 46 | **STRONG PROP** | UTA @ CBJ | Dmitri Voronkov under 1.5 SOG | -120 | draftkings | 1.35 | 61% vs 50% (+21%) | $4 | — |
| 47 | **STRONG PROP** | UTA @ CBJ | Mathieu Olivier over 0.5 PTS | +215 | draftkings | 0.45 | 36% vs 30% (+21%) | $2 | — |
| 48 | **STRONG PROP** | BOS @ MIN | Kirill Kaprizov under 0.5 A | -120 | draftkings | 0.49 | 61% vs 50% (+21%) | $4 | — |
| 49 | **STRONG PROP** | CGY @ VAN | Brock Boeser under 0.5 PTS | +120 | draftkings | 0.67 | 51% vs 42% (+21%) | $3 | — |
| 50 | **STRONG PROP** | BOS @ MIN | Matt Boldy under 0.5 A | -115 | draftkings | 0.51 | 60% vs 50% (+21%) | $3 | — |
| 51 | **STRONG PROP** | UTA @ CBJ | Dylan Guenther under 2.5 SOG | +122 | fanduel | 2.68 | 51% vs 42% (+21%) | $3 | — |
| 52 | **STRONG PROP** | BOS @ MIN | Elias Lindholm over 0.5 PTS | +160 | draftkings | 0.57 | 43% vs 36% (+21%) | $2 | — |
| 53 | **STRONG PROP** | OTT @ TOR | Shane Pinto over 1.5 SOG | -145 | draftkings | 2.34 | 66% vs 55% (+20%) | $4 | — |
| 54 | **STRONG PROP** | CGY @ VAN | Matt Coronato under 0.5 PTS | -110 | draftkings | 0.54 | 58% vs 49% (+20%) | $3 | — |
| 55 | **STRONG PROP** | BOS @ MIN | Blake Coleman under 2.5 SOG | -120 | draftkings | 2.28 | 61% vs 50% (+20%) | $3 | — |
| 56 | **STRONG PROP** | CGY @ VAN | Zeev Buium under 0.5 PTS | -155 | draftkings | 0.38 | 68% vs 57% (+20%) | $5 | — |
| 57 | **STRONG PROP** | DAL @ NSH | Roman Josi under 0.5 A | -115 | draftkings | 0.51 | 60% vs 50% (+20%) | $4 | — |
| 58 | **STRONG PROP** | CAR @ PHI | Travis Sanheim over 0.5 PTS | +210 | draftkings | 0.45 | 36% vs 30% (+20%) | $1 | — |
| 59 | **STRONG PROP** | SEA @ EDM | Leon Draisaitl under 3.5 SOG | -135 | draftkings | 3.03 | 64% vs 53% (+20%) | $4 | — |
| 60 | **STRONG PROP** | WSH @ TBL | Anthony Cirelli over 0.5 PTS | +115 | draftkings | 0.73 | 52% vs 43% (+20%) | $3 | — |
| 61 | **STRONG PROP** | WSH @ TBL | Aliaksei Protas over 1.5 SOG | +100 | draftkings | 1.92 | 56% vs 47% (+20%) | $3 | — |
| 62 | **STRONG PROP** | SEA @ EDM | Vasily Podkolzin under 0.5 A | -200 | draftkings | 0.29 | 75% vs 62% (+20%) | $5 | — |
| 63 | **STRONG PROP** | WSH @ TBL | John Carlson under 0.5 PTS | +135 | draftkings | 0.74 | 48% vs 40% (+20%) | $2 | — |
| 64 | **STRONG PROP** | UTA @ CBJ | Danton Heinen over 0.5 SOG | -145 | draftkings | 1.10 | 66% vs 55% (+20%) | $4 | — |
| 65 | **STRONG PROP** | STL @ COL | Martin Necas under 1.5 PTS | -170 | draftkings | 1.09 | 70% vs 59% (+20%) | $5 | — |
| 66 | **STRONG PROP** | BOS @ MIN | Maxim Shabanov under 0.5 PTS | -135 | draftkings | 0.45 | 64% vs 53% (+20%) | $4 | — |
| 67 | **STRONG PROP** | CAR @ PHI | Taylor Hall under 1.5 SOG | +105 | draftkings | 1.58 | 54% vs 45% (+19%) | $3 | — |
| 68 | **STRONG PROP** | CGY @ VAN | Matvei Gridin under 0.5 PTS | -120 | draftkings | 0.50 | 61% vs 51% (+19%) | $3 | — |
| 69 | **STRONG PROP** | NJD @ NYI | Matthew Schaefer under 0.5 A | -135 | draftkings | 0.45 | 64% vs 53% (+19%) | $4 | — |
| 70 | **STRONG PROP** | WSH @ TBL | Anthony Cirelli over 0.5 A | +235 | draftkings | 0.41 | 33% vs 28% (+19%) | $1 | — |
| 71 | **STRONG PROP** | BOS @ MIN | Quinn Hughes under 0.5 A | +145 | draftkings | 0.79 | 45% vs 38% (+19%) | $2 | — |
| 72 | **STRONG PROP** | UTA @ CBJ | Lawson Crouse over 0.5 PTS | +180 | draftkings | 0.51 | 40% vs 33% (+19%) | $2 | — |
| 73 | **STRONG PROP** | DAL @ NSH | Filip Forsberg under 2.5 SOG | +128 | fanduel | 2.78 | 49% vs 41% (+18%) | $2 | — |
| 74 | **STRONG PROP** | LAK @ SJS | Mason Marchment under 1.5 SOG | +100 | draftkings | 1.56 | 55% vs 46% (+18%) | $2 | — |
| 75 | **STRONG PROP** | LAK @ SJS | Macklin Celebrini over 1.5 PTS | +165 | draftkings | 1.43 | 42% vs 35% (+18%) | $2 | — |
| 76 | **STRONG PROP** | DAL @ NSH | Jamie Benn under 1.5 SOG | -180 | draftkings | 1.09 | 70% vs 60% (+18%) | $4 | — |
| 77 | **STRONG PROP** | MTL @ PIT | Alex Newhook over 0.5 PTS | +160 | draftkings | 0.55 | 42% vs 36% (+18%) | $2 | — |
| 78 | **STRONG PROP** | WSH @ TBL | John Carlson under 2.5 SOG | -130 | draftkings | 2.23 | 62% vs 52% (+18%) | $3 | — |
| 79 | **STRONG PROP** | DAL @ NSH | Filip Forsberg under 2.5 SOG | +125 | draftkings | 2.78 | 49% vs 41% (+18%) | $2 | — |
| 80 | **STRONG PROP** | SEA @ EDM | Leon Draisaitl under 0.5 G | -135 | fanduel | 0.46 | 63% vs 53% (+18%) | $3 | — |
| 81 | **STRONG PROP** | UTA @ CBJ | Adam Fantilli under 0.5 PTS | +110 | draftkings | 0.65 | 52% vs 44% (+18%) | $2 | — |
| 82 | **STRONG PROP** | BOS @ MIN | Blake Coleman under 0.5 PTS | -135 | draftkings | 0.46 | 63% vs 53% (+18%) | $3 | — |
| 83 | **STRONG PROP** | WSH @ TBL | Ryan Leonard under 1.5 SOG | +120 | draftkings | 1.71 | 50% vs 42% (+18%) | $2 | — |
| 84 | **STRONG PROP** | UTA @ CBJ | Matthew Knies under 1.5 SOG | +110 | draftkings | 1.63 | 52% vs 45% (+18%) | $2 | — |
| 85 | **STRONG PROP** | UTA @ CBJ | Logan Cooley under 1.5 SOG | +126 | fanduel | 1.75 | 49% vs 42% (+18%) | $2 | — |
| 86 | **STRONG PROP** | MTL @ PIT | Mike Matheson under 1.5 SOG | -110 | draftkings | 1.48 | 57% vs 49% (+18%) | $2 | — |
| 87 | **STRONG PROP** | STL @ COL | Mason McTavish under 1.5 SOG | +128 | fanduel | 1.77 | 48% vs 41% (+18%) | $2 | — |
| 88 | **STRONG PROP** | OTT @ TOR | Thomas Chabot over 0.5 A | +235 | draftkings | 0.40 | 33% vs 28% (+17%) | $1 | — |
| 89 | **STRONG PROP** | CAR @ PHI | Jordan Martinook under 1.5 SOG | -140 | draftkings | 1.28 | 64% vs 54% (+17%) | $3 | — |
| 90 | **STRONG PROP** | CHI @ BUF | Tage Thompson under 0.5 G | -135 | fanduel | 0.47 | 63% vs 53% (+17%) | $3 | — |
| 91 | **STRONG PROP** | CAR @ PHI | Carl Grundstrom under 1.5 SOG | -205 | draftkings | 1.01 | 73% vs 63% (+17%) | $5 | — |
| 92 | **STRONG PROP** | BOS @ MIN | Jared Spurgeon under 0.5 PTS | -215 | draftkings | 0.30 | 74% vs 64% (+17%) | $5 | — |
| 93 | **STRONG PROP** | MTL @ PIT | Sidney Crosby under 0.5 A | -110 | draftkings | 0.56 | 57% vs 49% (+17%) | $3 | — |
| 94 | **STRONG PROP** | CAR @ PHI | Shayne Gostisbehere over 0.5 PTS | +110 | draftkings | 0.74 | 52% vs 45% (+17%) | $2 | — |
| 95 | **STRONG PROP** | NJD @ NYI | Luke Hughes under 0.5 PTS | -135 | draftkings | 0.47 | 62% vs 53% (+17%) | $3 | — |
| 96 | **STRONG PROP** | SEA @ EDM | Mattias Ekholm over 0.5 PTS | +190 | draftkings | 0.47 | 38% vs 32% (+17%) | $1 | — |
| 97 | **STRONG PROP** | CAR @ PHI | Tyson Foerster over 1.5 SOG | +105 | draftkings | 1.81 | 53% vs 45% (+17%) | $2 | — |
| 98 | **STRONG PROP** | NJD @ NYI | Bo Horvat over 2.5 SOG | -135 | draftkings | 3.33 | 62% vs 53% (+17%) | $3 | — |
| 99 | **STRONG PROP** | STL @ COL | Nathan MacKinnon under 3.5 SOG | +120 | fanduel | 3.75 | 50% vs 43% (+17%) | $2 | — |
| 100 | **STRONG PROP** | LAK @ SJS | Brandt Clarke under 1.5 SOG | +136 | fanduel | 1.84 | 46% vs 40% (+16%) | $2 | — |
| 101 | **STRONG PROP** | CHI @ BUF | Jack Quinn over 2.5 SOG | -105 | draftkings | 2.97 | 55% vs 48% (+16%) | $2 | — |
| 102 | **STRONG PROP** | DAL @ NSH | Roman Josi under 0.5 PTS | +120 | draftkings | 0.71 | 49% vs 42% (+16%) | $2 | — |
| 103 | **STRONG PROP** | DAL @ NSH | Steven Stamkos under 0.5 A | -205 | draftkings | 0.32 | 73% vs 63% (+16%) | $4 | — |
| 104 | **STRONG PROP** | SEA @ EDM | Leon Draisaitl under 0.5 A | +140 | draftkings | 0.80 | 45% vs 39% (+16%) | $1 | — |
| 105 | **STRONG PROP** | CAR @ PHI | Taylor Hall under 1.5 SOG | +102 | fanduel | 1.58 | 54% vs 47% (+16%) | $2 | — |
| 106 | **STRONG PROP** | NJD @ NYI | Nico Hischier under 2.5 SOG | -125 | draftkings | 2.32 | 60% vs 51% (+16%) | $2 | — |
| 107 | **STRONG PROP** | OTT @ TOR | John Tavares under 2.5 SOG | -165 | fanduel | 2.00 | 68% vs 58% (+16%) | $4 | — |
| 108 | **STRONG PROP** | NJD @ NYI | Brayden Schenn under 1.5 SOG | -125 | draftkings | 1.40 | 60% vs 51% (+16%) | $2 | — |
| 109 | **STRONG PROP** | OTT @ TOR | Shane Pinto over 1.5 SOG | -154 | fanduel | 2.34 | 66% vs 57% (+16%) | $3 | — |
| 110 | **STRONG PROP** | STL @ COL | Nazem Kadri over 0.5 A | +210 | draftkings | 0.43 | 35% vs 30% (+16%) | $1 | — |
| 111 | **STRONG PROP** | DAL @ NSH | Steven Stamkos under 2.5 SOG | -120 | draftkings | 2.37 | 58% vs 50% (+16%) | $2 | — |
| 112 | **STRONG PROP** | MTL @ PIT | Ivan Demidov under 1.5 SOG | -115 | draftkings | 1.47 | 57% vs 50% (+16%) | $2 | — |
| 113 | **STRONG PROP** | OTT @ TOR | Thomas Chabot over 0.5 PTS | +165 | draftkings | 0.52 | 41% vs 35% (+16%) | $1 | — |
| 114 | **STRONG PROP** | OTT @ TOR | Auston Matthews under 3.5 SOG | -135 | draftkings | 3.14 | 62% vs 53% (+16%) | $3 | — |
| 115 | **STRONG PROP** | UTA @ CBJ | Sean Monahan under 1.5 SOG | -110 | draftkings | 1.51 | 56% vs 49% (+15%) | $2 | — |
| 116 | **STRONG PROP** | CGY @ VAN | Morgan Frost under 0.5 A | -245 | draftkings | 0.26 | 77% vs 67% (+15%) | $5 | — |
| 117 | **STRONG PROP** | CGY @ VAN | Joel Farabee under 1.5 SOG | +130 | draftkings | 1.83 | 47% vs 40% (+15%) | $1 | — |
| 118 | **STRONG PROP** | BOS @ MIN | Kirill Kaprizov under 1.5 PTS | -215 | draftkings | 1.01 | 73% vs 64% (+15%) | $4 | — |
| 119 | **STRONG PROP** | WSH @ TBL | Cole Hutson under 1.5 SOG | -120 | draftkings | 1.43 | 59% vs 51% (+15%) | $2 | — |
| 120 | **STRONG PROP** | MTL @ PIT | Cole Caufield under 2.5 SOG | +110 | fanduel | 2.66 | 51% vs 45% (+15%) | $2 | — |
| 121 | **STRONG PROP** | CAR @ PHI | Jordan Staal under 1.5 SOG | -125 | draftkings | 1.41 | 59% vs 51% (+15%) | $2 | — |
| 122 | **STRONG PROP** | MTL @ PIT | Erik Karlsson under 2.5 SOG | -155 | draftkings | 2.10 | 65% vs 57% (+15%) | $3 | — |
| 123 | **STRONG PROP** | BOS @ MIN | Quinn Hughes under 1.5 PTS | -245 | draftkings | 0.92 | 77% vs 67% (+15%) | $5 | — |
| 124 | **STRONG PROP** | WSH @ TBL | Charle-Edouard D'Astous under 1.5 SOG | -170 | draftkings | 1.17 | 67% vs 59% (+15%) | $3 | — |
| 125 | **STRONG PROP** | UTA @ CBJ | Logan Cooley under 1.5 SOG | +120 | draftkings | 1.75 | 49% vs 42% (+15%) | $2 | — |
| 126 | **prop value** | MTL @ PIT | Jakub Dobes over 23.5 SV | -105 | draftkings | 26.09 | 60% vs 48% (+27%) | $5 | ⚠saves-model |
| 127 | **prop value** | DAL @ NSH | Juuse Saros under 25.5 SV | -120 | draftkings | 23.44 | 64% vs 51% (+26%) | $5 | ⚠saves-model |
| 128 | **prop value** | LAK @ SJS | Yaroslav Askarov under 26.5 SV | -102 | fanduel | 25.38 | 59% vs 47% (+25%) | $4 | ⚠saves-model |
| 129 | **prop value** | LAK @ SJS | Anton Forsberg under 25.5 SV | -115 | draftkings | 23.79 | 62% vs 50% (+24%) | $5 | ⚠saves-model |
| 130 | **prop value** | LAK @ SJS | Anton Forsberg under 25.5 SV | -114 | fanduel | 23.79 | 62% vs 50% (+24%) | $5 | ⚠saves-model |
| 131 | **prop value** | BOS @ MIN | Jesper Wallstedt over 23.5 SV | -130 | draftkings | 26.89 | 64% vs 52% (+22%) | $4 | ⚠saves-model |
| 132 | **prop value** | BOS @ MIN | Jesper Wallstedt over 23.5 SV | -130 | fanduel | 26.89 | 64% vs 53% (+22%) | $4 | ⚠saves-model |
| 133 | **prop value** | LAK @ SJS | Yaroslav Askarov under 27.5 SV | -130 | draftkings | 25.38 | 64% vs 52% (+21%) | $4 | ⚠saves-model |
| 134 | **prop value** | MTL @ PIT | Jakub Dobes over 23.5 SV | -118 | fanduel | 26.09 | 60% vs 51% (+19%) | $3 | ⚠saves-model |
| 135 | **prop value** | CHI @ BUF | Ukko-Pekka Luukkonen under 21.5 SV | -120 | draftkings | 20.64 | 58% vs 50% (+16%) | $2 | ⚠saves-model |
| 136 | **prop value** | CHI @ BUF | Ukko-Pekka Luukkonen under 21.5 SV | -118 | fanduel | 20.64 | 58% vs 51% (+15%) | $2 | ⚠saves-model |
| 137 | **prop value** | DAL @ NSH | Casey DeSmith under 24.5 SV | -130 | draftkings | 23.18 | 60% vs 52% (+15%) | $2 | ⚠saves-model |
| 138 | **prop value** | WSH @ TBL | Anthony Cirelli over 1.5 SOG | -125 | draftkings | 2.05 | 59% vs 51% (+15%) | $2 | — |
| 139 | **prop value** | LAK @ SJS | Joel Edmundson under 1.5 SOG | -170 | draftkings | 1.17 | 67% vs 59% (+15%) | $3 | — |
| 140 | **prop value** | NJD @ NYI | Brayden Schenn under 0.5 PTS | -140 | draftkings | 0.47 | 63% vs 54% (+15%) | $3 | — |
| 141 | **prop value** | UTA @ CBJ | Logan Cooley under 0.5 A | -205 | draftkings | 0.33 | 72% vs 63% (+15%) | $4 | — |
| 142 | **prop value** | WSH @ TBL | Jakob Chychrun under 0.5 A | -200 | draftkings | 0.33 | 72% vs 62% (+15%) | $4 | — |
| 143 | **prop value** | STL @ COL | Nathan MacKinnon under 0.5 G | -130 | fanduel | 0.50 | 61% vs 53% (+15%) | $2 | — |
| 144 | **prop value** | SEA @ EDM | Kaapo Kakko over 0.5 PTS | +110 | draftkings | 0.71 | 51% vs 44% (+15%) | $1 | — |
| 145 | **prop value** | MTL @ PIT | Nick Suzuki under 2.5 SOG | -170 | fanduel | 1.99 | 68% vs 59% (+15%) | $3 | — |
| 146 | **prop value** | CAR @ PHI | Jamie Drysdale under 0.5 PTS | -185 | draftkings | 0.36 | 70% vs 61% (+15%) | $4 | — |
| 147 | **prop value** | LAK @ SJS | Trevor Moore over 1.5 SOG | -135 | draftkings | 2.14 | 61% vs 53% (+15%) | $2 | — |
| 148 | **prop value** | SEA @ EDM | Leon Draisaitl under 1.5 PTS | -135 | draftkings | 1.34 | 61% vs 53% (+14%) | $2 | — |
| 149 | **prop value** | BOS @ MIN | David Pastrnak over 0.5 A | +115 | draftkings | 0.68 | 49% vs 43% (+14%) | $1 | — |
| 150 | **prop value** | SEA @ EDM | Bobby McMann under 2.5 SOG | -148 | fanduel | 2.14 | 64% vs 56% (+14%) | $3 | — |
| 151 | **prop value** | CHI @ BUF | Ryan McLeod over 0.5 A | +170 | draftkings | 0.50 | 40% vs 35% (+14%) | $1 | — |
| 152 | **prop value** | NJD @ NYI | Brayden Schenn under 1.5 SOG | -125 | fanduel | 1.40 | 60% vs 52% (+14%) | $2 | — |
| 153 | **prop value** | OTT @ TOR | Auston Matthews under 0.5 A | -160 | draftkings | 0.42 | 66% vs 58% (+14%) | $3 | — |
| 154 | **prop value** | LAK @ SJS | Alexander Wennberg over 0.5 PTS | +105 | draftkings | 0.74 | 52% vs 46% (+14%) | $2 | — |
| 155 | **prop value** | CGY @ VAN | Brock Boeser under 2.5 SOG | -150 | draftkings | 2.16 | 64% vs 56% (+14%) | $2 | — |
| 156 | **prop value** | MTL @ PIT | Nick Suzuki under 0.5 A | +105 | draftkings | 0.65 | 52% vs 46% (+14%) | $2 | — |
| 157 | **prop value** | MTL @ PIT | Nick Suzuki under 2.5 SOG | -175 | draftkings | 1.99 | 68% vs 59% (+14%) | $3 | — |
| 158 | **prop value** | WSH @ TBL | Jake Guentzel over 0.5 PTS | -165 | draftkings | 1.08 | 66% vs 58% (+14%) | $2 | — |
| 159 | **prop value** | CGY @ VAN | Matt Coronato under 0.5 A | -215 | draftkings | 0.32 | 72% vs 64% (+14%) | $3 | — |
| 160 | **prop value** | MTL @ PIT | Nick Robertson over 1.5 SOG | -105 | draftkings | 1.88 | 55% vs 48% (+14%) | $2 | — |
| 161 | **prop value** | CHI @ BUF | Konsta Helenius over 0.5 PTS | +135 | draftkings | 0.60 | 45% vs 40% (+14%) | $1 | — |
| 162 | **prop value** | UTA @ CBJ | Conor Garland under 0.5 PTS | -180 | draftkings | 0.39 | 68% vs 60% (+14%) | $3 | — |
| 163 | **prop value** | MTL @ PIT | Erik Karlsson under 2.5 SOG | -156 | fanduel | 2.10 | 65% vs 57% (+14%) | $3 | — |
| 164 | **prop value** | MTL @ PIT | Cole Caufield under 2.5 SOG | +105 | draftkings | 2.66 | 51% vs 45% (+14%) | $1 | — |
| 165 | **prop value** | NJD @ NYI | Luke Hughes under 0.5 A | -190 | draftkings | 0.36 | 70% vs 61% (+14%) | $3 | — |
| 166 | **prop value** | STL @ COL | Devon Toews under 0.5 A | -215 | draftkings | 0.32 | 73% vs 64% (+14%) | $3 | — |
| 167 | **prop value** | MTL @ PIT | Kris Letang over 0.5 A | +245 | draftkings | 0.37 | 31% vs 27% (+14%) | $1 | — |
| 168 | **prop value** | OTT @ TOR | Auston Matthews under 3.5 SOG | -138 | fanduel | 3.14 | 62% vs 54% (+14%) | $2 | — |
| 169 | **prop value** | MTL @ PIT | Noah Dobson under 1.5 SOG | +120 | draftkings | 1.77 | 48% vs 42% (+14%) | $1 | — |
| 170 | **prop value** | CHI @ BUF | Josh Doan over 1.5 SOG | -190 | draftkings | 2.51 | 69% vs 61% (+14%) | $3 | — |
| 171 | **prop value** | WSH @ TBL | Anthony Cirelli over 1.5 SOG | -125 | fanduel | 2.05 | 59% vs 52% (+13%) | $2 | — |
| 172 | **prop value** | CHI @ BUF | Jack Quinn over 2.5 SOG | -108 | fanduel | 2.97 | 55% vs 49% (+13%) | $2 | — |
| 173 | **prop value** | MTL @ PIT | Cole Caufield under 0.5 A | -190 | draftkings | 0.37 | 69% vs 61% (+13%) | $3 | — |
| 174 | **prop value** | SEA @ EDM | Jake Walman under 0.5 PTS | -225 | draftkings | 0.31 | 73% vs 65% (+13%) | $3 | — |
| 175 | **prop value** | WSH @ TBL | Nikita Kucherov over 1.5 PTS | +120 | draftkings | 1.62 | 48% vs 42% (+13%) | $1 | — |
| 176 | **prop value** | CAR @ PHI | K'Andre Miller over 1.5 SOG | +135 | draftkings | 1.54 | 45% vs 40% (+13%) | $1 | — |
| 177 | **prop value** | LAK @ SJS | Macklin Celebrini over 0.5 A | -120 | draftkings | 0.85 | 57% vs 50% (+13%) | $1 | — |
| 178 | **prop value** | CHI @ BUF | Jack Quinn over 0.5 A | +180 | draftkings | 0.48 | 38% vs 33% (+13%) | $1 | — |
| 179 | **prop value** | CHI @ BUF | Josh Doan over 2.5 SOG | +136 | fanduel | 2.51 | 45% vs 40% (+13%) | $1 | — |
| 180 | **prop value** | WSH @ TBL | Alex Tuch over 0.5 PTS | +110 | draftkings | 0.69 | 50% vs 44% (+13%) | $1 | — |
| 181 | **prop value** | BOS @ MIN | Quinn Hughes over 2.5 SOG | +115 | draftkings | 2.68 | 49% vs 43% (+13%) | $1 | — |
| 182 | **prop value** | OTT @ TOR | Auston Matthews under 0.5 PTS | +140 | draftkings | 0.82 | 44% vs 39% (+13%) | $1 | — |
| 183 | **prop value** | MTL @ PIT | Noah Dobson over 0.5 PTS | +165 | draftkings | 0.50 | 40% vs 35% (+13%) | $1 | — |
| 184 | **prop value** | BOS @ MIN | Kirill Kaprizov under 3.5 SOG | -115 | fanduel | 3.40 | 57% vs 50% (+13%) | $2 | — |
| 185 | **prop value** | UTA @ CBJ | Dylan Guenther under 0.5 A | -215 | draftkings | 0.33 | 72% vs 64% (+13%) | $3 | — |
| 186 | **prop value** | CGY @ VAN | Brock Boeser under 0.5 A | -190 | draftkings | 0.37 | 69% vs 61% (+13%) | $2 | — |
| 187 | **prop value** | CGY @ VAN | Zeev Buium under 0.5 A | -235 | draftkings | 0.30 | 74% vs 66% (+13%) | $3 | — |
| 188 | **prop value** | CGY @ VAN | Devin Cooley over 22.5 SV | -120 | draftkings | 24.42 | 57% vs 51% (+13%) | $2 | ⚠saves-model |
| 189 | **prop value** | SEA @ EDM | Connor McDavid under 0.5 G | -135 | fanduel | 0.51 | 60% vs 53% (+13%) | $2 | — |
| 190 | **prop value** | OTT @ TOR | John Tavares under 2.5 SOG | -180 | draftkings | 2.00 | 68% vs 60% (+13%) | $2 | — |
| 191 | **prop value** | OTT @ TOR | Claude Giroux over 0.5 PTS | +130 | draftkings | 0.61 | 46% vs 41% (+13%) | $1 | — |
| 192 | **prop value** | STL @ COL | Nathan MacKinnon under 3.5 SOG | +110 | draftkings | 3.75 | 50% vs 44% (+13%) | $1 | — |
| 193 | **prop value** | BOS @ MIN | David Pastrnak under 0.5 G | -240 | fanduel | 0.30 | 74% vs 66% (+12%) | $3 | — |
| 194 | **prop value** | LAK @ SJS | Drew Doughty under 0.5 PTS | -195 | draftkings | 0.36 | 69% vs 62% (+12%) | $2 | — |
| 195 | **prop value** | CHI @ BUF | Peyton Krebs over 0.5 A | +245 | draftkings | 0.37 | 31% vs 27% (+12%) | $1 | — |
| 196 | **prop value** | WSH @ TBL | Nikita Kucherov over 2.5 SOG | -140 | draftkings | 3.27 | 61% vs 54% (+12%) | $2 | — |
| 197 | **prop value** | CAR @ PHI | Tyson Foerster over 1.5 SOG | +100 | fanduel | 1.81 | 53% vs 47% (+12%) | $1 | — |
| 198 | **prop value** | SEA @ EDM | Vince Dunn under 1.5 SOG | +138 | fanduel | 1.92 | 44% vs 39% (+12%) | $1 | — |
| 199 | **prop value** | OTT @ TOR | William Nylander over 0.5 PTS | -165 | draftkings | 1.05 | 65% vs 58% (+12%) | $2 | — |
| 200 | **prop value** | MTL @ PIT | Nick Suzuki under 0.5 PTS | +180 | draftkings | 0.98 | 38% vs 33% (+12%) | $1 | — |
| 201 | **prop value** | OTT @ TOR | Tim Stützle under 0.5 A | -120 | draftkings | 0.57 | 57% vs 50% (+12%) | $1 | — |
| 202 | **prop value** | DAL @ NSH | Casey DeSmith under 23.5 SV | -110 | fanduel | 23.18 | 55% vs 49% (+12%) | $1 | ⚠saves-model |
| 203 | **prop value** | CHI @ BUF | Peyton Krebs over 0.5 PTS | +145 | draftkings | 0.56 | 43% vs 38% (+12%) | $1 | — |
| 204 | **prop value** | LAK @ SJS | Mason Marchment under 0.5 A | -230 | draftkings | 0.32 | 73% vs 65% (+12%) | $2 | — |
| 205 | **prop value** | BOS @ MIN | Maxim Shabanov under 0.5 A | -250 | draftkings | 0.29 | 75% vs 67% (+12%) | $3 | — |
| 206 | **prop value** | BOS @ MIN | Pavel Zacha over 0.5 PTS | +110 | draftkings | 0.68 | 49% vs 44% (+12%) | $1 | — |
| 207 | **prop value** | DAL @ NSH | Filip Forsberg under 0.5 A | -175 | draftkings | 0.41 | 66% vs 59% (+12%) | $2 | — |
| 208 | **prop value** | OTT @ TOR | Claude Giroux over 1.5 SOG | -110 | draftkings | 1.86 | 54% vs 49% (+12%) | $1 | — |
| 209 | **prop value** | SEA @ EDM | Vince Dunn under 1.5 SOG | +135 | draftkings | 1.92 | 44% vs 40% (+12%) | $1 | — |
| 210 | **prop value** | NJD @ NYI | Jack Hughes over 3.5 SOG | +100 | draftkings | 3.88 | 52% vs 47% (+12%) | $1 | — |
| 211 | **prop value** | NJD @ NYI | Jack Hughes over 3.5 SOG | +100 | fanduel | 3.88 | 52% vs 47% (+12%) | $1 | — |
| 212 | **prop value** | MTL @ PIT | Sidney Crosby under 2.5 SOG | -140 | fanduel | 2.25 | 61% vs 55% (+12%) | $2 | — |
| 213 | **prop value** | LAK @ SJS | Mason Marchment under 0.5 PTS | -120 | draftkings | 0.57 | 56% vs 50% (+12%) | $1 | — |
| 214 | **prop value** | DAL @ NSH | Steven Stamkos over 0.5 G | +210 | fanduel | 0.41 | 34% vs 30% (+12%) | $1 | — |
| 215 | **prop value** | STL @ COL | Mason McTavish under 1.5 SOG | +115 | draftkings | 1.77 | 48% vs 43% (+12%) | $1 | — |
| 216 | **prop value** | CAR @ PHI | K'Andre Miller over 0.5 A | +230 | draftkings | 0.38 | 32% vs 28% (+12%) | $1 | — |
| 217 | **prop value** | UTA @ CBJ | Adam Fantilli under 0.5 A | -195 | draftkings | 0.37 | 69% vs 62% (+12%) | $2 | — |
| 218 | **prop value** | CAR @ PHI | Matvei Michkov under 1.5 SOG | +105 | draftkings | 1.68 | 51% vs 46% (+12%) | $1 | — |
| 219 | **prop value** | LAK @ SJS | Quinton Byfield under 2.5 SOG | -140 | draftkings | 2.27 | 61% vs 54% (+12%) | $1 | — |
| 220 | **prop value** | LAK @ SJS | Brandt Clarke under 1.5 SOG | +125 | draftkings | 1.84 | 46% vs 42% (+11%) | $1 | — |
| 221 | **prop value** | UTA @ CBJ | Adam Fantilli under 2.5 SOG | -140 | draftkings | 2.28 | 61% vs 54% (+11%) | $1 | — |
| 222 | **prop value** | MTL @ PIT | Evgeni Malkin over 1.5 SOG | -180 | draftkings | 2.36 | 66% vs 60% (+11%) | $2 | — |
| 223 | **prop value** | MTL @ PIT | Evgeni Malkin over 0.5 PTS | -135 | draftkings | 0.90 | 59% vs 53% (+11%) | $1 | — |
| 224 | **prop value** | STL @ COL | Gabriel Landeskog under 2.5 SOG | -148 | fanduel | 2.21 | 62% vs 56% (+11%) | $2 | — |
| 225 | **prop value** | NJD @ NYI | Bo Horvat over 2.5 SOG | -148 | fanduel | 3.33 | 62% vs 56% (+11%) | $2 | — |
| 226 | **prop value** | UTA @ CBJ | Mikhail Sergachev under 0.5 A | -135 | draftkings | 0.52 | 59% vs 53% (+11%) | $1 | — |
| 227 | **prop value** | LAK @ SJS | Quinton Byfield under 0.5 A | -220 | draftkings | 0.34 | 71% vs 64% (+11%) | $2 | — |
| 228 | **prop value** | WSH @ TBL | Jake Guentzel over 2.5 SOG | -120 | draftkings | 3.04 | 57% vs 51% (+11%) | $1 | — |
| 229 | **prop value** | WSH @ TBL | Gage Goncalves under 0.5 PTS | -175 | draftkings | 0.42 | 66% vs 59% (+11%) | $2 | — |
| 230 | **prop value** | WSH @ TBL | Dylan Strome under 1.5 SOG | -130 | draftkings | 1.45 | 58% vs 52% (+11%) | $1 | — |
| 231 | **prop value** | SEA @ EDM | Bobby McMann under 2.5 SOG | -165 | draftkings | 2.14 | 64% vs 58% (+11%) | $1 | — |
| 232 | **prop value** | STL @ COL | Gabriel Landeskog under 0.5 PTS | -110 | draftkings | 0.62 | 54% vs 49% (+11%) | $1 | — |
| 233 | **prop value** | LAK @ SJS | Quinton Byfield under 0.5 PTS | -105 | draftkings | 0.63 | 53% vs 48% (+11%) | $1 | — |
| 234 | **prop value** | BOS @ MIN | Ryan Hartman under 1.5 SOG | +135 | draftkings | 1.92 | 44% vs 40% (+11%) | $1 | — |
| 235 | **prop value** | CAR @ PHI | Shayne Gostisbehere over 1.5 SOG | -110 | draftkings | 1.84 | 54% vs 49% (+11%) | $1 | — |
| 236 | **prop value** | SEA @ EDM | Connor McDavid under 1.5 PTS | -105 | draftkings | 1.60 | 53% vs 48% (+11%) | $1 | — |
| 237 | **prop value** | LAK @ SJS | Brandt Clarke under 0.5 PTS | -155 | draftkings | 0.47 | 63% vs 57% (+11%) | $1 | — |
| 238 | **prop value** | LAK @ SJS | Artemi Panarin under 2.5 SOG | +114 | fanduel | 2.79 | 49% vs 44% (+11%) | $1 | — |
| 239 | **prop value** | SEA @ EDM | Kasperi Kapanen under 2.5 SOG | -190 | draftkings | 2.00 | 68% vs 61% (+11%) | $2 | — |
| 240 | **prop value** | UTA @ CBJ | Nick Schmaltz under 0.5 A | -175 | draftkings | 0.42 | 66% vs 59% (+11%) | $1 | — |
| 241 | **prop value** | DAL @ NSH | Miro Heiskanen under 0.5 A | -110 | draftkings | 0.62 | 54% vs 49% (+11%) | $1 | — |
| 242 | **prop value** | LAK @ SJS | Tyler Toffoli under 1.5 SOG | -105 | draftkings | 1.61 | 53% vs 48% (+11%) | $1 | — |
| 243 | **prop value** | CHI @ BUF | Anton Frondell under 0.5 PTS | -120 | draftkings | 0.57 | 56% vs 51% (+11%) | $1 | — |
| 244 | **prop value** | NJD @ NYI | Dougie Hamilton over 2.5 SOG | +130 | fanduel | 2.52 | 45% vs 41% (+11%) | $1 | — |
| 245 | **prop value** | CAR @ PHI | Christian Dvorak over 0.5 PTS | +130 | draftkings | 0.60 | 45% vs 41% (+11%) | $1 | — |
| 246 | **prop value** | SEA @ EDM | Isaac Howard under 0.5 PTS | -240 | draftkings | 0.32 | 73% vs 66% (+11%) | $2 | — |
| 247 | **prop value** | BOS @ MIN | Matt Boldy under 1.5 PTS | -235 | draftkings | 1.02 | 73% vs 66% (+11%) | $2 | — |
| 248 | **prop value** | CGY @ VAN | Matvei Gridin under 0.5 A | -235 | draftkings | 0.32 | 73% vs 66% (+10%) | $2 | — |
| 249 | **prop value** | UTA @ CBJ | Zach Werenski under 3.5 SOG | -140 | draftkings | 3.22 | 60% vs 54% (+10%) | $1 | — |
| 250 | **prop value** | UTA @ CBJ | Cole Sillinger over 1.5 SOG | +115 | draftkings | 1.64 | 48% vs 43% (+10%) | $1 | — |
| 251 | **prop value** | BOS @ MIN | Morgan Geekie over 0.5 G | +250 | fanduel | 0.35 | 30% vs 27% (+10%) | — | — |
| 252 | **prop value** | UTA @ CBJ | Charlie Coyle over 0.5 PTS | +100 | draftkings | 0.72 | 51% vs 47% (+10%) | $1 | — |
| 253 | **prop value** | MTL @ PIT | Lane Hutson under 0.5 A | -105 | draftkings | 0.64 | 52% vs 48% (+10%) | $1 | — |
| 254 | **prop value** | SEA @ EDM | Connor McDavid under 1.5 A | -245 | draftkings | 1.01 | 73% vs 67% (+10%) | $2 | — |
| 255 | **prop value** | DAL @ NSH | Roman Josi under 2.5 SOG | -125 | draftkings | 2.44 | 57% vs 51% (+10%) | $1 | — |
| 256 | **prop value** | WSH @ TBL | Brandon Hagel over 0.5 PTS | -165 | draftkings | 1.03 | 64% vs 58% (+10%) | $1 | — |
| 257 | **prop value** | BOS @ MIN | Kirill Kaprizov under 0.5 G | -155 | fanduel | 0.47 | 62% vs 57% (+10%) | $1 | — |
| 258 | **prop value** | STL @ COL | Gabriel Landeskog under 2.5 SOG | -155 | draftkings | 2.21 | 62% vs 57% (+10%) | $1 | — |
| 259 | **prop value** | CGY @ VAN | Joel Farabee under 1.5 SOG | +122 | fanduel | 1.83 | 47% vs 42% (+10%) | $1 | — |
| 260 | **prop value** | OTT @ TOR | William Nylander over 0.5 A | +130 | draftkings | 0.59 | 45% vs 41% (+10%) | $1 | — |
| 261 | **prop value** | LAK @ SJS | Adrian Kempe under 0.5 A | -165 | draftkings | 0.45 | 64% vs 58% (+10%) | $1 | — |
| 262 | **prop value** | UTA @ CBJ | Dylan Guenther under 0.5 PTS | +115 | draftkings | 0.75 | 47% vs 43% (+10%) | — | — |
| 263 | **prop value** | NJD @ NYI | Tony DeAngelo over 0.5 PTS | +205 | draftkings | 0.41 | 34% vs 31% (+10%) | — | — |
| 264 | **prop value** | MTL @ PIT | Sidney Crosby under 2.5 SOG | -150 | draftkings | 2.25 | 61% vs 56% (+10%) | $1 | — |
| 265 | **prop value** | SEA @ EDM | Mattias Ekholm under 1.5 SOG | -105 | draftkings | 1.64 | 52% vs 48% (+10%) | $1 | — |
| 266 | **prop value** | BOS @ MIN | Fraser Minten under 1.5 SOG | -120 | draftkings | 1.53 | 55% vs 50% (+10%) | $1 | — |
| 267 | **prop value** | NJD @ NYI | Anthony Mantha over 1.5 SOG | -120 | draftkings | 1.93 | 56% vs 51% (+10%) | $1 | — |
| 268 | **prop value** | BOS @ MIN | Danila Yurov under 0.5 PTS | -195 | draftkings | 0.39 | 68% vs 62% (+10%) | $1 | — |
| 269 | **prop value** | UTA @ CBJ | Valeri Nichushkin over 0.5 A | +225 | draftkings | 0.38 | 32% vs 29% (+10%) | — | — |
| 270 | **prop value** | BOS @ MIN | Hampus Lindholm under 0.5 PTS | -220 | draftkings | 0.35 | 70% vs 64% (+10%) | $1 | — |
| 271 | **prop value** | CGY @ VAN | Jonathan Lekkerimäki over 0.5 PTS | +180 | draftkings | 0.46 | 37% vs 33% (+10%) | — | — |
| 272 | **prop value** | LAK @ SJS | Erik Haula under 1.5 SOG | -105 | draftkings | 1.62 | 53% vs 48% (+10%) | $1 | — |
| 273 | **prop value** | SEA @ EDM | Jordan Eberle over 1.5 SOG | -125 | draftkings | 1.97 | 57% vs 52% (+10%) | $1 | — |
| 274 | **prop value** | DAL @ NSH | Ryan O'Reilly over 1.5 SOG | -130 | draftkings | 1.98 | 58% vs 52% (+10%) | $1 | — |
| 275 | **prop value** | CHI @ BUF | Oliver Moore under 1.5 SOG | -165 | draftkings | 1.27 | 64% vs 58% (+10%) | $1 | — |
| 276 | **prop value** | WSH @ TBL | Pierre-Luc Dubois under 0.5 PTS | -145 | draftkings | 0.50 | 61% vs 55% (+10%) | $1 | — |
| 277 | **prop value** | CAR @ PHI | Nikolaj Ehlers over 0.5 PTS | -120 | draftkings | 0.82 | 56% vs 51% (+10%) | $1 | — |
| 278 | **prop value** | STL @ COL | Dylan Holloway under 2.5 SOG | -120 | fanduel | 2.46 | 56% vs 51% (+10%) | $1 | — |
| 279 | **prop value** | MTL @ PIT | Sidney Crosby under 0.5 PTS | +165 | draftkings | 0.95 | 39% vs 35% (+9%) | — | — |
| 280 | **prop value** | BOS @ MIN | David Pastrnak under 3.5 SOG | -140 | fanduel | 3.23 | 60% vs 55% (+9%) | $1 | — |
| 281 | **prop value** | UTA @ CBJ | Denton Mateychuk under 1.5 SOG | -135 | draftkings | 1.44 | 59% vs 53% (+9%) | $1 | — |
| 282 | **prop value** | NJD @ NYI | Matthew Schaefer under 0.5 PTS | +110 | draftkings | 0.73 | 48% vs 44% (+9%) | — | — |
| 283 | **prop value** | CHI @ BUF | Artyom Levshunov under 0.5 PTS | -240 | draftkings | 0.33 | 72% vs 66% (+9%) | $1 | — |
| 284 | **prop value** | CHI @ BUF | Ryan McLeod under 1.5 SOG | -170 | draftkings | 1.27 | 64% vs 59% (+9%) | $1 | — |
| 285 | **prop value** | BOS @ MIN | Danila Yurov under 1.5 SOG | -185 | draftkings | 1.21 | 66% vs 60% (+9%) | $1 | — |
| 286 | **prop value** | BOS @ MIN | Jared Spurgeon under 1.5 SOG | -180 | draftkings | 1.22 | 66% vs 60% (+9%) | $1 | — |
| 287 | **prop value** | SEA @ EDM | Brandon Montour over 2.5 SOG | +125 | draftkings | 2.52 | 45% vs 41% (+9%) | — | — |
| 288 | **prop value** | UTA @ CBJ | Clayton Keller under 0.5 PTS | +155 | draftkings | 0.91 | 40% vs 37% (+9%) | — | — |
| 289 | **prop value** | WSH @ TBL | Nikita Kucherov over 0.5 G | +150 | fanduel | 0.53 | 41% vs 38% (+9%) | — | — |
| 290 | **prop value** | STL @ COL | Artturi Lehkonen over 0.5 A | +220 | draftkings | 0.38 | 32% vs 29% (+9%) | — | — |
| 291 | **prop value** | WSH @ TBL | Pierre-Luc Dubois under 0.5 A | -235 | draftkings | 0.33 | 72% vs 66% (+9%) | $1 | — |
| 292 | **prop value** | DAL @ NSH | Jason Robertson over 3.5 SOG | +136 | fanduel | 3.40 | 43% vs 40% (+9%) | — | — |
| 293 | **prop value** | WSH @ TBL | Alex Tuch under 2.5 SOG | -170 | fanduel | 2.12 | 65% vs 59% (+9%) | $1 | — |
| 294 | **prop value** | CHI @ BUF | Frank Nazar over 0.5 A | +250 | draftkings | 0.35 | 29% vs 27% (+9%) | — | — |
| 295 | **prop value** | MTL @ PIT | Alex Newhook under 1.5 SOG | -125 | draftkings | 1.51 | 56% vs 51% (+9%) | — | — |
| 296 | **prop value** | WSH @ TBL | Victor Hedman under 0.5 PTS | -185 | draftkings | 0.41 | 66% vs 61% (+9%) | $1 | — |
| 297 | **prop value** | OTT @ TOR | Jake Sanderson over 0.5 PTS | -110 | draftkings | 0.75 | 53% vs 49% (+9%) | — | — |
| 298 | **prop value** | CGY @ VAN | Marco Rossi under 1.5 SOG | -120 | draftkings | 1.53 | 56% vs 51% (+9%) | $1 | — |
| 299 | **prop value** | OTT @ TOR | Jack Roslovic over 0.5 PTS | +140 | draftkings | 0.55 | 42% vs 39% (+9%) | — | — |
| 300 | **prop value** | OTT @ TOR | Jack Roslovic over 1.5 SOG | -115 | draftkings | 1.87 | 54% vs 50% (+9%) | — | — |
| 301 | **prop value** | STL @ COL | Gabriel Landeskog under 0.5 A | -220 | draftkings | 0.35 | 70% vs 65% (+9%) | $1 | — |
| 302 | **prop value** | CHI @ BUF | Jack Quinn over 0.5 PTS | -125 | draftkings | 0.82 | 56% vs 51% (+9%) | — | — |
| 303 | **prop value** | UTA @ CBJ | Clayton Keller under 0.5 A | -115 | draftkings | 0.61 | 54% vs 50% (+9%) | — | — |
| 304 | **prop value** | CGY @ VAN | Filip Hronek under 0.5 PTS | -105 | draftkings | 0.65 | 52% vs 48% (+9%) | — | — |
| 305 | **prop value** | UTA @ CBJ | Denton Mateychuk over 0.5 PTS | +160 | draftkings | 0.50 | 39% vs 36% (+9%) | — | — |
| 306 | **prop value** | SEA @ EDM | Jared McCann over 0.5 G | +250 | fanduel | 0.34 | 29% vs 27% (+9%) | — | — |
| 307 | **prop value** | UTA @ CBJ | Vincent Trocheck under 1.5 SOG | -110 | draftkings | 1.60 | 53% vs 49% (+9%) | — | — |
| 308 | **prop value** | NJD @ NYI | Nico Hischier under 0.5 PTS | -105 | draftkings | 0.66 | 52% vs 48% (+9%) | — | — |
| 309 | **prop value** | LAK @ SJS | Brandt Clarke under 0.5 A | -215 | draftkings | 0.36 | 69% vs 64% (+9%) | $1 | — |
| 310 | **prop value** | OTT @ TOR | Darren Raddysh over 0.5 PTS | -125 | draftkings | 0.82 | 56% vs 51% (+9%) | — | — |
| 311 | **prop value** | LAK @ SJS | Dmitry Orlov under 0.5 PTS | -190 | draftkings | 0.41 | 66% vs 61% (+9%) | $1 | — |
| 312 | **prop value** | NJD @ NYI | Anthony Mantha over 0.5 PTS | +100 | draftkings | 0.70 | 50% vs 47% (+8%) | — | — |
| 313 | **prop value** | SEA @ EDM | Jordan Eberle over 1.5 SOG | -128 | fanduel | 1.97 | 57% vs 53% (+8%) | $1 | — |
| 314 | **prop value** | DAL @ NSH | Steven Stamkos under 2.5 SOG | -135 | fanduel | 2.37 | 58% vs 54% (+8%) | $1 | — |
| 315 | **prop value** | BOS @ MIN | Elias Lindholm under 1.5 SOG | -105 | draftkings | 1.66 | 51% vs 48% (+8%) | — | — |
| 316 | **prop value** | LAK @ SJS | Macklin Celebrini under 3.5 SOG | -108 | fanduel | 3.60 | 53% vs 49% (+8%) | — | — |
| 317 | **prop value** | CAR @ PHI | K'Andre Miller over 0.5 PTS | +160 | draftkings | 0.49 | 39% vs 36% (+8%) | — | — |
| 318 | **prop value** | CHI @ BUF | Ryan Donato under 0.5 PTS | -240 | draftkings | 0.34 | 71% vs 66% (+8%) | $1 | — |
| 319 | **prop value** | BOS @ MIN | Bobby Brink under 0.5 PTS | -195 | draftkings | 0.40 | 67% vs 62% (+8%) | $1 | — |
| 320 | **prop value** | OTT @ TOR | Thomas Chabot over 1.5 SOG | -115 | draftkings | 1.84 | 54% vs 50% (+8%) | — | — |
| 321 | **prop value** | WSH @ TBL | Nikita Kucherov over 2.5 SOG | -152 | fanduel | 3.27 | 61% vs 57% (+8%) | $1 | — |
| 322 | **prop value** | DAL @ NSH | Roope Hintz over 1.5 SOG | -170 | draftkings | 2.22 | 63% vs 59% (+8%) | — | — |
| 323 | **prop value** | DAL @ NSH | Miro Heiskanen under 0.5 PTS | +115 | draftkings | 0.76 | 47% vs 43% (+8%) | — | — |
| 324 | **prop value** | SEA @ EDM | Chandler Stephenson under 0.5 A | -205 | draftkings | 0.39 | 68% vs 63% (+8%) | — | — |
| 325 | **prop value** | DAL @ NSH | Steven Stamkos under 0.5 PTS | +115 | draftkings | 0.76 | 47% vs 43% (+8%) | — | — |
| 326 | **prop value** | CGY @ VAN | Joel Farabee under 0.5 PTS | -140 | draftkings | 0.53 | 59% vs 54% (+8%) | — | — |

## 2. Projections (first 40 by game)

```
Game        Player                    Pos Market  Line   Proj  P(over)   Over/Under  Book
CHI @ BUF   Ukko-Pekka Luukkonen      G   SV      21.5  20.64      42%    -115/-120  draftkings
CHI @ BUF   Ukko-Pekka Luukkonen      G   SV      21.5  20.64      42%    -112/-118  fanduel
CHI @ BUF   Tage Thompson             C   SOG      3.5   3.56      46%    -105/-125  draftkings
CHI @ BUF   Tage Thompson             C   SOG      3.5   3.56      46%    -110/-120  fanduel
CHI @ BUF   Jack Quinn                R   SOG      2.5   2.97      55%    -105/-130  draftkings
CHI @ BUF   Jack Quinn                R   SOG      2.5   2.97      55%    -108/-120  fanduel
CHI @ BUF   Rasmus Dahlin             D   SOG      2.5   2.80      52%    -105/-125  draftkings
CHI @ BUF   Rasmus Dahlin             D   SOG      2.5   2.80      52%    -110/-118  fanduel
CHI @ BUF   Josh Doan                 R   SOG      1.5   2.51      69%    -190/+140  draftkings
CHI @ BUF   Josh Doan                 R   SOG      2.5   2.51      45%    +136/-178  fanduel
CHI @ BUF   Zach Benson               L   SOG      1.5   2.11      61%    -155/+115  draftkings
CHI @ BUF   Konsta Helenius           C   SOG      1.5   1.95      57%    -135/+100  draftkings
CHI @ BUF   Josh Norris               C   SOG      1.5   1.77      52%    -110/-125  draftkings
CHI @ BUF   Owen Power                D   SOG      1.5   1.72      50%    +100/-135  draftkings
CHI @ BUF   Noah Ostlund              C   SOG      1.5   1.46      42%    +110/-145  draftkings
CHI @ BUF   Peyton Krebs              C   SOG      1.5   1.35      39%    +150/-205  draftkings
CHI @ BUF   Ryan McLeod               C   SOG      1.5   1.27      36%    +125/-170  draftkings
CHI @ BUF   Jiri Kulich               C   SOG      1.5   1.26      36%    -115/-115  draftkings
CHI @ BUF   Tage Thompson             C   PTS      0.5   1.05      65%    -235/+175  draftkings
CHI @ BUF   Rasmus Dahlin             D   PTS      0.5   1.00      63%    -215/+155  draftkings
CHI @ BUF   Jack Quinn                R   PTS      0.5   0.82      56%    -125/-110  draftkings
CHI @ BUF   Zach Benson               L   PTS      0.5   0.79      55%    -145/+105  draftkings
CHI @ BUF   Josh Norris               C   PTS      0.5   0.77      54%    -115/-115  draftkings
CHI @ BUF   Josh Doan                 R   PTS      0.5   0.76      53%    -125/-110  draftkings
CHI @ BUF   Rasmus Dahlin             D   A        0.5   0.72      51%    -140/+105  draftkings
CHI @ BUF   Ryan McLeod               C   PTS      0.5   0.72      51%    -105/-130  draftkings
CHI @ BUF   Noah Ostlund              C   PTS      0.5   0.62      46%    +115/-160  draftkings
CHI @ BUF   Konsta Helenius           C   PTS      0.5   0.60      45%    +135/-180  draftkings
CHI @ BUF   Peyton Krebs              C   PTS      0.5   0.56      43%    +145/-195  draftkings
CHI @ BUF   Tage Thompson             C   A        0.5   0.53      41%    +115/-155  draftkings
CHI @ BUF   Zach Benson               L   A        0.5   0.52      41%    +140/-190  draftkings
CHI @ BUF   Mattias Samuelsson        D   PTS      0.5   0.51      40%    +190/-260  draftkings
CHI @ BUF   Ryan McLeod               C   A        0.5   0.50      40%    +170/-235  draftkings
CHI @ BUF   Owen Power                D   PTS      0.5   0.49      39%    +135/-185  draftkings
CHI @ BUF   Jack Quinn                R   A        0.5   0.48      38%    +180/-245  draftkings
CHI @ BUF   Tage Thompson             C   G        0.5   0.47      37%    +100/-135  fanduel
CHI @ BUF   Josh Norris               C   A        0.5   0.45      36%    +175/-240  draftkings
CHI @ BUF   Josh Doan                 R   A        0.5   0.41      33%    +175/-235  draftkings
CHI @ BUF   Noah Ostlund              C   A        0.5   0.38      32%    +210/-290  draftkings
CHI @ BUF   Owen Power                D   A        0.5   0.37      31%    +180/-245  draftkings
```

## 3. NHL paper ledger to date

```
NHL prop paper bets — settled by market/side/strength (pending: 578)
market                    side   str    n   W   L   P   staked   profit     ROI
player_assists            over     2   20   8  12   0    43.00    -2.11   -4.9%
player_assists            under    2   17   8   9   0    68.00   -16.51  -24.3%
player_goals              over     2    4   0   4   0    10.00   -10.00 -100.0%
player_goals              under    2    1   0   1   0     3.00    -3.00 -100.0%
player_points             over     2   31  10  21   0    84.00   -29.94  -35.6%
player_points             under    2   14   7   7   0    49.00    -1.46   -3.0%
player_shots_on_goal      over     2   27  13  14   0    91.00    -0.51   -0.6%
player_shots_on_goal      under    2   43  25  18   0   168.00    11.75   +7.0%
player_assists            over     1   20   6  14   0    18.00    -4.47  -24.8%
player_assists            under    1   99  65  34   0    59.00    -3.69   -6.3%
player_goals              over     1    7   4   3   0     2.00     3.40 +170.0%
player_goals              under    1   22  14   8   0    11.00     3.64  +33.1%
player_points             over     1   65  25  40   0    55.00   -30.75  -55.9%
player_points             under    1   97  46  50   1    34.00   -10.15  -29.9%
player_shots_on_goal      over     1   88  40  48   0    53.00   -11.47  -21.6%
player_shots_on_goal      under    1  115  54  60   1    65.00   -18.61  -28.6%
player_total_saves        over     1    4   2   2   0    13.00    -1.36  -10.5%
player_total_saves        under    1   13   7   6   0    36.00    -2.81   -7.8%
```

> Paper only. The projection is tested walk-forward (fit on 2024-25, scored on every 2025-26 game: `--calibrate`, `analysis/06`), but no historical prop prices exist, so ROI against posted lines is untested until the ledger fills. The ledger above is that evidence.

## Tonight's ask: five parlay locks (price no object) + one lock at a decent line

Ranked by the blend (25% model, 75% de-vigged line), every side where both model and market say > 50%, saves excluded, model-vs-market gap ≤ +30%, one leg per game so the legs are independent. Paper only.

**Five parlay legs (likeliest to cash, any price)**

| Game (CT) | Pick | Price | Proj | Model · Fair · Blend |
|---|---|---|---|---|
| UTA @ CBJ 6:00 PM | Ryan Lomberg under 0.5 A | -1400 @draftkings | 0.14 | 87% · 89% · 88.9% |
| BOS @ MIN 7:00 PM | Will Borgen under 0.5 A | -1100 @draftkings | 0.16 | 85% · 87% · 86.7% |
| WSH @ TBL 6:00 PM | Zemgus Girgensons under 0.5 A | -650 @draftkings | 0.14 | 87% · 82% · 83.4% |
| CAR @ PHI 6:00 PM | Carl Grundstrom under 0.5 A | -600 @draftkings | 0.14 | 87% · 81% · 82.6% |
| CHI @ BUF 6:00 PM | Wyatt Kaiser under 0.5 A | -650 @draftkings | 0.19 | 83% · 81% · 81.7% |

Five legs together at the blend: **43% to cash**, parlay pays about **+82** (decimal 1.82). Each leg is roughly −5% EV at the blend; this is the likeliest card, not a value card.

**One lock at a decent line**

| Game (CT) | Pick | Price | Proj | Model · Fair · Blend |
|---|---|---|---|---|
| DAL @ NSH 7:00 PM | **Esa Lindell under 1.5 SOG** | -160 @draftkings | 0.98 | 74% · 58% · 62.1% (EV +0.9% at the blend) |

Highest blend among sides priced −160..+120. Gap is +29%, just under the +30% overreach line, so lean on the 62% blend, not the model's 74%. Ledger context: strength-2 SOG unders are the one bucket in the black (+7.0% on 43, not significant). Runner-up with a smaller gap: Auston Matthews under 0.5 A −160 (blend 59.6%).

## Update: BetRivers, legs priced −200s

The parlay legs above (−600..−1400) aren't posted at BetRivers. The Odds API carries only one BetRivers NHL prop market (2+ goals, over side only, checked at 2026-10-03 ~3 PM CT), so the BetRivers prices can't be scored. Below are the likeliest sides priced −200..−299 at DraftKings/FanDuel, one per game. These are standard lines (under 0.5 assists/points), so BetRivers should hang the same number; check the price there. Same blend, same filters as above.

| Game (CT) | Pick | DK/FD price | Proj | Model · Fair · Blend |
|---|---|---|---|---|
| WSH @ TBL 6:00 PM | Ryan McDonagh under 0.5 A | -285 @draftkings | 0.25 | 78% · 70% · 71.8% |
| CHI @ BUF 6:00 PM | Artyom Levshunov under 0.5 A | -295 @draftkings | 0.29 | 75% · 70% · 71.5% |
| BOS @ MIN 7:00 PM | Casey Mittelstadt under 0.5 A | -295 @draftkings | 0.29 | 75% · 70% · 71.3% |
| SEA @ EDM 6:00 PM | Connor Murphy under 0.5 PTS | -285 @draftkings | 0.27 | 77% · 69% · 71.2% |
| NJD @ NYI 6:30 PM | Brayden Schenn under 0.5 A | -265 @draftkings | 0.26 | 77% · 68% · 70.5% |

Bench (other games, same tier): Tyler Seguin u0.5 A (DAL @ NSH) 70.7%, Rasmus Ristolainen u0.5 PTS (CAR @ PHI) 70.6%, Alex Laferriere u0.5 A (LAK @ SJS) 70.6%, Morgan Rielly u0.5 A (OTT @ TOR) 70.5%, Nick Suzuki u0.5 G (MTL @ PIT) 70.4%.

Five of these together at the blend: **18% to cash**, about **+350** at the DK prices. Each leg alone misses about 3 times in 10.

# NHL Prop Report — Wednesday, September 30, 2026

**Generated:** 2026-09-30 04:52 PM CDT  
**STAKES: PAPER ONLY as of 2026-09-20 — no bucket has a 95% CI above zero. $Bet is what the paper ledger logs, not a recommendation to bet real money.**  
**Slate:** 3 games · 201 prop lines matched to rostered players (The Odds API)  
**Model (skaters, since 2026-09-30):** per-minute rate × projected minutes. The rate is this season's stat per minute blended with last season's (weight a1) and regressed toward the position mean (K ghost minutes: shots 86, points 234, goals 694); minutes lean 56% on the last 5 games. × opponent allowance^β × home/away split → Poisson P(over) (shots: gamma-Poisson k=17.5; goalie saves: old per-start recipe, k=20). Fit on 2024-25, tested on every 2025-26 skater-game: better log-loss than the old recipe at every line of every stat. Tiers +8% / +15%, ≥ +30% demoted (⚠overreach).

## The lock, and five good ones

**The lock** is the top of the agreement board: the prop side the projection and the de-vigged line both favour, priced -250..-110, model above fair by no more than +20%, ranked by the **blend** (25% model, 75% de-vigged line, in logit space: the market has been sharper everywhere so far). **Good** is the rest of that board, then the ranked value props (§1), one per player. EV is at the blend; at −220..−250 the juice usually outweighs what the model adds, so these are the likeliest winners, not value bets. Paper only.

| | Puck (CT) | Game | Play | Why |
|---|---|---|---|---|
| **LOCK** | 9:00 PM | LAK @ COL | **Quinton Byfield under 0.5 A -245 @draftkings** | proj 0.27 → model 76% · fair 67% · blend 69% (EV -2.6% at the blend, agree) |
| good 1 | 6:30 PM | NYI @ TOR | Morgan Rielly under 0.5 A -250 @draftkings | proj 0.32 → model 72% · fair 67% · blend 68% (EV -4.6% at the blend, agree) |
| good 2 | 9:00 PM | LAK @ COL | Gabriel Landeskog under 0.5 A -240 @draftkings | proj 0.34 → model 71% · fair 66% · blend 67% (EV -4.5% at the blend, agree) |
| good 3 | 9:00 PM | LAK @ COL | Brandt Clarke under 0.5 A -215 @draftkings | proj 0.29 → model 75% · fair 64% · blend 67% (EV -2.1% at the blend, agree) |
| good 4 | 9:00 PM | LAK @ COL | Martin Necas under 1.5 PTS -235 @draftkings | proj 1.14 → model 68% · fair 66% · blend 66% (EV -5.2% at the blend, agree) |
| good 5 | 6:30 PM | PIT @ PHI | Jamie Drysdale under 0.5 A -220 @draftkings | proj 0.32 → model 73% · fair 64% · blend 66% (EV -3.5% at the blend, agree) |

At the blend's 69%, a lock like this misses about 3 nights in 10; the chance of at least one miss in a five-night week is 84%.

### Simulated 20,000 nights of that card

Each ticket keeps its own chance to cash; the simulation adds how they move together (teammates share a game-level factor, latent ρ 0.1047 points / 0.0525 assists, measured on 2025-26 logs; opponents independent). Run three times: trusting the model, the blend (25% model), and the de-vigged market. Flat $1 a ticket; the parlay column is all legs in one ticket at the product of the prices.

| If this is right | Exp. hits of 6 | P(all 6) | P(≥5) | $1 each: exp. | P(up) | 5th–95th pct | 6-leg parlay +748: EV |
|---|---|---|---|---|---|---|---|
| model | 4.34 | 14.8% | 47% | +0.21 | 47% | -3.08 to +2.57 | +26% |
| blend | 4.04 | 9.5% | 36% | -0.24 | 36% | -3.15 to +2.57 | -20% |
| market | 3.92 | 8.0% | 33% | -0.40 | 33% | -3.17 to +2.57 | -32% |

## 1. Ranked props

| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **STRONG PROP** | LAK @ COL | Cale Makar under 0.5 A | +125 | draftkings | 0.66 | 52% vs 41% (+25%) | $3 | — |
| 2 | **STRONG PROP** | PIT @ PHI | Tommy Novak under 1.5 SOG | +100 | draftkings | 1.45 | 58% vs 47% (+25%) | $4 | — |
| 3 | **STRONG PROP** | PIT @ PHI | Christian Dvorak over 0.5 A | +240 | draftkings | 0.41 | 34% vs 28% (+22%) | $2 | — |
| 4 | **STRONG PROP** | PIT @ PHI | Christian Dvorak over 0.5 PTS | +135 | draftkings | 0.66 | 48% vs 40% (+22%) | $3 | — |
| 5 | **STRONG PROP** | NYI @ TOR | Emil Heineman over 1.5 SOG | -135 | draftkings | 2.28 | 65% vs 53% (+21%) | $4 | — |
| 6 | **STRONG PROP** | LAK @ COL | Quinton Byfield under 2.5 SOG | -138 | fanduel | 2.08 | 66% vs 54% (+21%) | $5 | — |
| 7 | **STRONG PROP** | LAK @ COL | Nathan MacKinnon under 0.5 A | +145 | draftkings | 0.78 | 46% vs 38% (+21%) | $2 | — |
| 8 | **STRONG PROP** | LAK @ COL | Cale Makar under 0.5 PTS | +185 | draftkings | 0.92 | 40% vs 33% (+20%) | $2 | — |
| 9 | **STRONG PROP** | LAK @ COL | Brandt Clarke under 0.5 PTS | -160 | draftkings | 0.38 | 68% vs 57% (+20%) | $4 | — |
| 10 | **STRONG PROP** | NYI @ TOR | Matias Maccelli under 1.5 SOG | -105 | draftkings | 1.48 | 57% vs 48% (+20%) | $3 | — |
| 11 | **STRONG PROP** | LAK @ COL | Quinton Byfield under 0.5 PTS | -120 | draftkings | 0.51 | 60% vs 50% (+19%) | $3 | — |
| 12 | **STRONG PROP** | NYI @ TOR | Darren Raddysh over 2.5 SOG | +112 | fanduel | 2.83 | 52% vs 44% (+18%) | $2 | — |
| 13 | **STRONG PROP** | PIT @ PHI | Jamie Drysdale under 1.5 SOG | -135 | draftkings | 1.31 | 63% vs 53% (+18%) | $3 | — |
| 14 | **STRONG PROP** | PIT @ PHI | Jamie Drysdale under 0.5 PTS | -150 | draftkings | 0.42 | 65% vs 56% (+17%) | $3 | — |
| 15 | **STRONG PROP** | LAK @ COL | Brandt Clarke under 0.5 A | -215 | draftkings | 0.29 | 75% vs 64% (+17%) | $5 | — |
| 16 | **STRONG PROP** | NYI @ TOR | Darren Raddysh over 0.5 PTS | -110 | draftkings | 0.85 | 57% vs 49% (+17%) | $2 | — |
| 17 | **STRONG PROP** | NYI @ TOR | Kyle Palmieri over 2.5 SOG | +115 | draftkings | 2.74 | 50% vs 43% (+16%) | $2 | — |
| 18 | **STRONG PROP** | LAK @ COL | Martin Necas under 2.5 SOG | +100 | fanduel | 2.54 | 54% vs 47% (+16%) | $2 | — |
| 19 | **STRONG PROP** | LAK @ COL | Nazem Kadri over 0.5 A | +220 | draftkings | 0.41 | 34% vs 29% (+15%) | $1 | — |
| 20 | **prop value** | LAK @ COL | Darcy Kuemper under 27.5 SV | -110 | draftkings | 26.40 | 59% vs 49% (+21%) | $3 | ⚠saves-model |
| 21 | **prop value** | LAK @ COL | Darcy Kuemper under 27.5 SV | -112 | fanduel | 26.40 | 59% vs 49% (+19%) | $3 | ⚠saves-model |
| 22 | **prop value** | PIT @ PHI | Dan Vladar under 24.5 SV | -120 | draftkings | 23.27 | 60% vs 51% (+17%) | $3 | ⚠saves-model |
| 23 | **prop value** | NYI @ TOR | Anthony Stolarz under 26.5 SV | -130 | draftkings | 25.10 | 60% vs 52% (+15%) | $2 | ⚠saves-model |
| 24 | **prop value** | LAK @ COL | Gabriel Landeskog under 2.5 SOG | -155 | draftkings | 2.10 | 65% vs 57% (+15%) | $3 | — |
| 25 | **prop value** | LAK @ COL | Nazem Kadri over 2.5 SOG | +126 | fanduel | 2.62 | 48% vs 42% (+15%) | $2 | — |
| 26 | **prop value** | LAK @ COL | Cale Makar under 2.5 SOG | -110 | draftkings | 2.48 | 56% vs 49% (+15%) | $2 | — |
| 27 | **prop value** | NYI @ TOR | Kirill Marchenko over 2.5 SOG | -102 | fanduel | 2.92 | 54% vs 47% (+15%) | $2 | — |
| 28 | **prop value** | NYI @ TOR | Ilya Sorokin under 24.5 SV | -105 | draftkings | 24.16 | 55% vs 48% (+15%) | $2 | ⚠saves-model |
| 29 | **prop value** | NYI @ TOR | Jack Roslovic over 1.5 SOG | -145 | draftkings | 2.20 | 63% vs 55% (+15%) | $2 | — |
| 30 | **prop value** | LAK @ COL | Quinton Byfield under 0.5 A | -245 | draftkings | 0.27 | 76% vs 67% (+15%) | $4 | — |
| 31 | **prop value** | PIT @ PHI | Sidney Crosby under 0.5 A | -125 | draftkings | 0.52 | 60% vs 52% (+14%) | $2 | — |
| 32 | **prop value** | LAK @ COL | Brock Nelson over 0.5 PTS | +100 | draftkings | 0.76 | 53% vs 47% (+14%) | $2 | — |
| 33 | **prop value** | PIT @ PHI | Dan Vladar under 23.5 SV | -104 | fanduel | 23.27 | 54% vs 48% (+14%) | $2 | ⚠saves-model |
| 34 | **prop value** | NYI @ TOR | Kirill Marchenko over 2.5 SOG | -105 | draftkings | 2.92 | 54% vs 48% (+14%) | $2 | — |
| 35 | **prop value** | LAK @ COL | Martin Necas under 2.5 SOG | -105 | draftkings | 2.54 | 54% vs 48% (+14%) | $2 | — |
| 36 | **prop value** | NYI @ TOR | William Nylander under 2.5 SOG | -114 | fanduel | 2.43 | 57% vs 50% (+14%) | $2 | — |
| 37 | **prop value** | NYI @ TOR | Matthew Schaefer under 0.5 A | -155 | draftkings | 0.44 | 64% vs 57% (+14%) | $2 | — |
| 38 | **prop value** | LAK @ COL | Adrian Kempe under 2.5 SOG | -110 | fanduel | 2.48 | 56% vs 49% (+13%) | $2 | — |
| 39 | **prop value** | PIT @ PHI | Dan Vladar under 24.5 SV | -130 | fanduel | 23.27 | 60% vs 53% (+13%) | $2 | ⚠saves-model |
| 40 | **prop value** | PIT @ PHI | Jamie Drysdale under 0.5 A | -220 | draftkings | 0.32 | 73% vs 64% (+13%) | $3 | — |
| 41 | **prop value** | LAK @ COL | Nazem Kadri over 2.5 SOG | +120 | draftkings | 2.62 | 48% vs 42% (+13%) | $1 | — |
| 42 | **prop value** | LAK @ COL | Drew Doughty under 1.5 SOG | -150 | draftkings | 1.30 | 63% vs 56% (+13%) | $2 | — |
| 43 | **prop value** | LAK @ COL | Brandt Clarke under 1.5 SOG | +114 | fanduel | 1.73 | 50% vs 44% (+13%) | $1 | — |
| 44 | **prop value** | PIT @ PHI | Sidney Crosby under 2.5 SOG | -165 | draftkings | 2.07 | 66% vs 58% (+13%) | $2 | — |
| 45 | **prop value** | NYI @ TOR | Anthony Stolarz under 25.5 SV | -110 | fanduel | 25.10 | 55% vs 49% (+13%) | $1 | ⚠saves-model |
| 46 | **prop value** | NYI @ TOR | Kyle Palmieri over 2.5 SOG | +110 | fanduel | 2.74 | 50% vs 45% (+13%) | $1 | — |
| 47 | **prop value** | NYI @ TOR | Darren Raddysh over 2.5 SOG | +100 | draftkings | 2.83 | 52% vs 47% (+13%) | $1 | — |
| 48 | **prop value** | NYI @ TOR | Tony DeAngelo over 1.5 SOG | -130 | draftkings | 2.04 | 59% vs 52% (+13%) | $1 | — |
| 49 | **prop value** | PIT @ PHI | Evgeni Malkin over 1.5 SOG | -154 | fanduel | 2.25 | 64% vs 57% (+12%) | $2 | — |
| 50 | **prop value** | LAK @ COL | Brock Nelson over 0.5 A | +230 | draftkings | 0.38 | 32% vs 28% (+12%) | $1 | — |
| 51 | **prop value** | LAK @ COL | Gabriel Landeskog under 0.5 PTS | -120 | draftkings | 0.57 | 57% vs 50% (+12%) | $1 | — |
| 52 | **prop value** | PIT @ PHI | Erik Karlsson under 2.5 SOG | -180 | draftkings | 2.02 | 67% vs 60% (+12%) | $2 | — |
| 53 | **prop value** | PIT @ PHI | Erik Karlsson under 2.5 SOG | -178 | fanduel | 2.02 | 67% vs 60% (+12%) | $2 | — |
| 54 | **prop value** | NYI @ TOR | William Nylander under 2.5 SOG | -120 | draftkings | 2.43 | 57% vs 51% (+11%) | $1 | — |
| 55 | **prop value** | NYI @ TOR | Ilya Sorokin under 24.5 SV | -112 | fanduel | 24.16 | 55% vs 49% (+11%) | $1 | ⚠saves-model |
| 56 | **prop value** | LAK @ COL | Adrian Kempe under 0.5 A | -210 | draftkings | 0.35 | 70% vs 63% (+11%) | $2 | — |
| 57 | **prop value** | LAK @ COL | Nathan MacKinnon under 1.5 PTS | -135 | draftkings | 1.39 | 59% vs 53% (+11%) | $1 | — |
| 58 | **prop value** | NYI @ TOR | Auston Matthews under 0.5 A | -170 | draftkings | 0.43 | 65% vs 59% (+11%) | $1 | — |
| 59 | **prop value** | LAK @ COL | Quinton Byfield under 2.5 SOG | -175 | draftkings | 2.08 | 66% vs 59% (+11%) | $1 | — |
| 60 | **prop value** | PIT @ PHI | Evgeni Malkin over 1.5 SOG | -165 | draftkings | 2.25 | 64% vs 58% (+11%) | $1 | — |
| 61 | **prop value** | LAK @ COL | Artemi Panarin under 0.5 A | -140 | draftkings | 0.51 | 60% vs 54% (+11%) | $1 | — |
| 62 | **prop value** | PIT @ PHI | Evgeni Malkin over 0.5 PTS | -130 | draftkings | 0.86 | 58% vs 52% (+10%) | $1 | — |
| 63 | **prop value** | LAK @ COL | Devon Toews under 0.5 PTS | -215 | draftkings | 0.36 | 70% vs 64% (+10%) | $1 | — |
| 64 | **prop value** | NYI @ TOR | Auston Matthews under 0.5 PTS | +140 | draftkings | 0.85 | 43% vs 39% (+10%) | — | — |
| 65 | **prop value** | PIT @ PHI | Evgeni Malkin over 0.5 A | +145 | draftkings | 0.54 | 42% vs 38% (+10%) | — | — |
| 66 | **prop value** | LAK @ COL | Artemi Panarin under 0.5 PTS | +130 | draftkings | 0.81 | 44% vs 41% (+10%) | — | — |
| 67 | **prop value** | LAK @ COL | Brock Nelson over 0.5 G | +240 | fanduel | 0.36 | 30% vs 28% (+9%) | — | — |
| 68 | **prop value** | LAK @ COL | Brandt Clarke under 1.5 SOG | +105 | draftkings | 1.73 | 50% vs 46% (+9%) | — | — |
| 69 | **prop value** | LAK @ COL | Mackenzie Blackwood under 23.5 SV | -125 | draftkings | 22.98 | 56% vs 51% (+9%) | — | ⚠saves-model |
| 70 | **prop value** | PIT @ PHI | Travis Konecny over 1.5 SOG | -152 | fanduel | 2.15 | 62% vs 57% (+9%) | $1 | — |
| 71 | **prop value** | NYI @ TOR | Simon Holmstrom over 0.5 PTS | +135 | draftkings | 0.56 | 43% vs 40% (+9%) | — | — |
| 72 | **prop value** | PIT @ PHI | Sidney Crosby under 2.5 SOG | -182 | fanduel | 2.07 | 66% vs 61% (+9%) | $1 | — |
| 73 | **prop value** | NYI @ TOR | Morgan Rielly over 1.5 SOG | -105 | draftkings | 1.77 | 52% vs 48% (+9%) | — | — |
| 74 | **prop value** | NYI @ TOR | Morgan Rielly under 0.5 A | -250 | draftkings | 0.32 | 72% vs 67% (+9%) | $1 | — |
| 75 | **prop value** | LAK @ COL | Brock Nelson over 1.5 SOG | -170 | draftkings | 2.24 | 64% vs 59% (+9%) | — | — |
| 76 | **prop value** | LAK @ COL | Alex Laferriere under 0.5 PTS | -170 | draftkings | 0.45 | 64% vs 59% (+9%) | — | — |
| 77 | **prop value** | NYI @ TOR | Matthew Schaefer under 2.5 SOG | +110 | draftkings | 2.82 | 48% vs 44% (+8%) | — | — |
| 78 | **prop value** | LAK @ COL | Adrian Kempe under 2.5 SOG | -125 | draftkings | 2.48 | 56% vs 51% (+8%) | — | — |
| 79 | **prop value** | NYI @ TOR | William Nylander over 0.5 PTS | -185 | draftkings | 1.06 | 65% vs 60% (+8%) | — | — |
| 80 | **prop value** | NYI @ TOR | Kyle Palmieri over 0.5 A | +190 | draftkings | 0.43 | 35% vs 32% (+8%) | — | — |
| 81 | **prop value** | LAK @ COL | Gabriel Landeskog under 0.5 A | -240 | draftkings | 0.34 | 71% vs 66% (+8%) | $1 | — |
| 82 | **prop value** | PIT @ PHI | Travis Konecny over 0.5 PTS | -135 | draftkings | 0.86 | 58% vs 53% (+8%) | — | — |

## 2. Projections (first 40 by game)

```
Game        Player                    Pos Market  Line   Proj  P(over)   Over/Under  Book
NYI @ TOR   Ilya Sorokin              G   SV      24.5  24.16      45%    -125/-105  draftkings
NYI @ TOR   Ilya Sorokin              G   SV      24.5  24.16      45%    -118/-112  fanduel
NYI @ TOR   Bo Horvat                 C   SOG      2.5   3.42      64%    -175/+130  draftkings
NYI @ TOR   Bo Horvat                 C   SOG      3.5   3.42      44%    +126/-165  fanduel
NYI @ TOR   Matthew Schaefer          D   SOG      2.5   2.82      52%    -150/+110  draftkings
NYI @ TOR   Matthew Schaefer          D   SOG      2.5   2.82      52%    -144/+110  fanduel
NYI @ TOR   Kyle Palmieri             C   SOG      2.5   2.74      50%    +115/-155  draftkings
NYI @ TOR   Kyle Palmieri             C   SOG      2.5   2.74      50%    +110/-144  fanduel
NYI @ TOR   Emil Heineman             L   SOG      1.5   2.28      65%    -135/+100  draftkings
NYI @ TOR   Tony DeAngelo             D   SOG      1.5   2.04      59%    -130/-105  draftkings
NYI @ TOR   Victor Eklund             R   SOG      1.5   1.89      55%    -125/-110  draftkings
NYI @ TOR   Brayden Schenn            C   SOG      1.5   1.70      50%    -125/-110  draftkings
NYI @ TOR   Brayden Schenn            C   SOG      1.5   1.70      50%    -118/-110  fanduel
NYI @ TOR   Matias Maccelli           L   SOG      1.5   1.48      43%    -130/-105  draftkings
NYI @ TOR   Bo Horvat                 C   PTS      0.5   0.84      57%    -160/+115  draftkings
NYI @ TOR   Matthew Schaefer          D   PTS      0.5   0.71      51%    -140/+100  draftkings
NYI @ TOR   Kyle Palmieri             C   PTS      0.5   0.70      50%    -105/-130  draftkings
NYI @ TOR   Matias Maccelli           L   PTS      0.5   0.57      44%    +105/-140  draftkings
NYI @ TOR   Simon Holmstrom           R   PTS      0.5   0.56      43%    +135/-185  draftkings
NYI @ TOR   Brayden Schenn            C   PTS      0.5   0.54      42%    +115/-155  draftkings
NYI @ TOR   Tony DeAngelo             D   PTS      0.5   0.46      37%    +150/-205  draftkings
NYI @ TOR   Matthew Schaefer          D   A        0.5   0.44      36%    +115/-155  draftkings
NYI @ TOR   Kyle Palmieri             C   A        0.5   0.43      35%    +190/-260  draftkings
NYI @ TOR   Bo Horvat                 C   G        0.5   0.41      34%    +180/-250  fanduel
NYI @ TOR   Bo Horvat                 C   A        0.5   0.41      34%    +145/-200  draftkings
NYI @ TOR   Tony DeAngelo             D   A        0.5   0.38      32%    +195/-270  draftkings
NYI @ TOR   Matias Maccelli           L   A        0.5   0.35      30%    +190/-260  draftkings
NYI @ TOR   Simon Holmstrom           R   A        0.5   0.31      27%    +275/-390  draftkings
NYI @ TOR   Brayden Schenn            C   A        0.5   0.30      26%    +210/-285  draftkings
NYI @ TOR   Kyle Palmieri             C   G        0.5   0.26      23%    +290/-450  fanduel
NYI @ TOR   Brayden Schenn            C   G        0.5   0.24      22%    +320/-490  fanduel
PIT @ PHI   Dan Vladar                G   SV      24.5  23.27      40%    -110/-120  draftkings
PIT @ PHI   Dan Vladar                G   SV      23.5  23.27      46%    -128/-104  fanduel
PIT @ PHI   Dan Vladar                G   SV      24.5  23.27      40%    -102/-130  fanduel
PIT @ PHI   Owen Tippett              R   SOG      2.5   2.58      47%    -105/-130  draftkings
PIT @ PHI   Owen Tippett              R   SOG      2.5   2.58      47%    +110/-144  fanduel
PIT @ PHI   Porter Martone            R   SOG      2.5   2.42      43%    -105/-130  draftkings
PIT @ PHI   Porter Martone            R   SOG      2.5   2.42      43%    +106/-138  fanduel
PIT @ PHI   Travis Konecny            R   SOG      1.5   2.15      62%    -175/+130  draftkings
PIT @ PHI   Travis Konecny            R   SOG      1.5   2.15      62%    -152/+116  fanduel
```

## 3. NHL paper ledger to date

```
NHL prop paper bets — settled by market/side/strength (pending: 135)
market                    side   str    n   W   L   P   staked   profit     ROI
player_assists            over     2   11   3   8   0    33.00    -7.76  -23.5%
player_assists            under    2    3   1   2   0    13.00    -5.37  -41.3%
player_goals              over     2    4   0   4   0    10.00   -10.00 -100.0%
player_points             over     2   18   6  12   0    55.00   -19.29  -35.1%
player_points             under    2    2   0   2   0     7.00    -7.00 -100.0%
player_shots_on_goal      over     2   16   6  10   0    57.00   -12.05  -21.1%
player_shots_on_goal      under    2    2   1   1   0    10.00    -0.65   -6.5%
player_assists            over     1   12   4   8   0    16.00    -4.38  -27.4%
player_assists            under    1   14   9   5   0    18.00    -3.62  -20.1%
player_goals              over     1    3   2   1   0     2.00     3.40 +170.0%
player_goals              under    1    6   5   1   0     6.00     2.74  +45.7%
player_points             over     1   28  10  18   0    44.00   -23.49  -53.4%
player_points             under    1   12   8   4   0     5.00    -5.00 -100.0%
player_shots_on_goal      over     1   27  13  14   0    29.00    -5.29  -18.2%
player_shots_on_goal      under    1   22  11  11   0    18.00    -7.10  -39.4%
player_total_saves        over     1    3   1   2   0    12.00    -2.24  -18.7%
player_total_saves        under    1    4   1   3   0    12.00   -10.23  -85.2%
```

> Paper only. The projection is tested walk-forward (fit on 2024-25, scored on every 2025-26 game: `--calibrate`, `analysis/06`), but no historical prop prices exist, so ROI against posted lines is untested until the ledger fills. The ledger above is that evidence.

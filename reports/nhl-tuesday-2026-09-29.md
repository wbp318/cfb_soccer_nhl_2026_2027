# NHL Prop Report — Tuesday, September 29, 2026

**Generated:** 2026-09-29 05:12 PM CDT  
**STAKES: PAPER ONLY as of 2026-09-20 — no bucket has a 95% CI above zero. $Bet is what the paper ledger logs, not a recommendation to bet real money.**  
**Slate:** 5 games · 288 prop lines matched to rostered players (The Odds API)  
**Model:** per-game rates from nhl.db game logs (shrink 20 games to 20252026, recent-10 weight 0.35) × opponent pace/allowance (clamped 0.80–1.20) → Poisson P(over) (saves: gamma-Poisson k=20, the rate itself uncertain). Tiers +8% / +15%, ≥ +30% demoted (⚠overreach). All priors until analysis/06 runs.

## The lock, and five good ones

**The lock** is the top of the agreement board: the prop side the projection and the de-vigged line both favour, priced -250..-110, model above fair by no more than +20%, ranked by chance to cash. **Good** is the rest of that board, then the ranked value props (§1), one per player. Paper only; the agreement board has no track record yet.

| | Puck (CT) | Game | Play | Why |
|---|---|---|---|---|
| **LOCK** | 6:00 PM | MTL @ TOR | **Nick Suzuki over 0.5 PTS -230 @draftkings** | proj 1.44 → model 76% vs fair 65% (+17%, agree) |
| good 1 | 9:00 PM | VAN @ EDM | Jake Walman under 0.5 A -250 @draftkings | proj 0.28 → model 76% vs fair 67% (+13%, agree) |
| good 2 | 9:00 PM | VAN @ EDM | Connor McDavid over 0.5 A -230 @draftkings | proj 1.34 → model 74% vs fair 65% (+13%, agree) |
| good 3 | 9:30 PM | CHI @ VGK | Jack Eichel over 0.5 PTS -225 @draftkings | proj 1.33 → model 73% vs fair 65% (+13%, agree) |
| good 4 | 7:00 PM | NYR @ BOS | Hampus Lindholm under 0.5 A -200 @draftkings | proj 0.32 → model 73% vs fair 62% (+17%, agree) |
| good 5 | 7:00 PM | NYR @ BOS | David Pastrnak over 0.5 PTS -225 @draftkings | proj 1.31 → model 73% vs fair 65% (+13%, agree) |

### Simulated 20,000 nights of that card

Each ticket keeps its own chance to cash; the simulation adds how they move together (teammates share a game-level factor, latent ρ 0.107 points / 0.055 assists, measured on 2025-26 logs; opponents independent). Run twice: once trusting the model's probabilities, once trusting the de-vigged market. Flat $1 a ticket; the parlay column is all legs in one ticket at the product of the prices.

| If this is right | Exp. hits of 6 | P(all 6) | P(≥5) | $1 each: exp. | P(up) | 5th–95th pct | 6-leg parlay +802: EV |
|---|---|---|---|---|---|---|---|
| model | 4.45 | 16.1% | 51% | +0.42 | 51% | -1.72 to +2.66 | +45% |
| market | 3.89 | 6.9% | 31% | -0.38 | 31% | -3.13 to +2.66 | -37% |

## 1. Ranked props

| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **STRONG PROP** | NYR @ BOS | Elias Lindholm over 0.5 PTS | +140 | draftkings | 0.70 | 50% vs 39% (+29%) | $4 | — |
| 2 | **STRONG PROP** | MTL @ TOR | Cole Caufield over 0.5 G | +130 | fanduel | 0.74 | 52% vs 40% (+29%) | $4 | — |
| 3 | **STRONG PROP** | VAN @ EDM | Marco Rossi under 1.5 SOG | -115 | draftkings | 1.27 | 64% vs 50% (+29%) | $5 | — |
| 4 | **STRONG PROP** | CHI @ VGK | Ivan Barbashev over 0.5 A | +205 | draftkings | 0.51 | 40% vs 31% (+29%) | $3 | — |
| 5 | **STRONG PROP** | CHI @ VGK | Tomas Hertl over 2.5 SOG | +135 | draftkings | 2.71 | 51% vs 40% (+28%) | $4 | — |
| 6 | **STRONG PROP** | MTL @ TOR | Noah Dobson over 0.5 A | +200 | draftkings | 0.51 | 40% vs 31% (+28%) | $2 | — |
| 7 | **STRONG PROP** | NYR @ BOS | Will Cuylle over 1.5 SOG | -102 | fanduel | 2.04 | 61% vs 47% (+28%) | $5 | — |
| 8 | **STRONG PROP** | NYR @ BOS | Morgan Geekie over 0.5 G | +210 | fanduel | 0.48 | 38% vs 30% (+28%) | $2 | — |
| 9 | **STRONG PROP** | NYR @ BOS | David Pastrnak over 0.5 A | -105 | draftkings | 0.93 | 60% vs 48% (+27%) | $5 | — |
| 10 | **STRONG PROP** | NYR @ BOS | Oliver Bjorkstrand over 1.5 SOG | +130 | fanduel | 1.73 | 52% vs 41% (+27%) | $4 | — |
| 11 | **STRONG PROP** | VAN @ EDM | Vasily Podkolzin under 2.5 SOG | -155 | draftkings | 1.85 | 72% vs 57% (+26%) | $5 | — |
| 12 | **STRONG PROP** | MTL @ TOR | Chris Kreider over 0.5 A | +235 | draftkings | 0.44 | 35% vs 28% (+26%) | $2 | — |
| 13 | **STRONG PROP** | MTL @ TOR | Darren Raddysh over 2.5 SOG | +108 | fanduel | 2.96 | 57% vs 45% (+26%) | $4 | — |
| 14 | **STRONG PROP** | MTL @ TOR | Chris Kreider over 0.5 PTS | +115 | draftkings | 0.78 | 54% vs 43% (+26%) | $4 | — |
| 15 | **STRONG PROP** | MTL @ TOR | Darren Raddysh over 0.5 PTS | -115 | draftkings | 0.97 | 62% vs 50% (+26%) | $5 | — |
| 16 | **STRONG PROP** | CHI @ VGK | William Karlsson over 1.5 SOG | -140 | draftkings | 2.35 | 68% vs 54% (+25%) | $5 | — |
| 17 | **STRONG PROP** | CHI @ VGK | Jack Eichel over 3.5 SOG | +115 | draftkings | 3.86 | 54% vs 43% (+25%) | $3 | — |
| 18 | **STRONG PROP** | VAN @ EDM | Vasily Podkolzin under 0.5 A | -190 | draftkings | 0.27 | 76% vs 61% (+25%) | $5 | — |
| 19 | **STRONG PROP** | VAN @ EDM | Leon Draisaitl over 0.5 A | -145 | draftkings | 1.17 | 69% vs 55% (+24%) | $5 | — |
| 20 | **STRONG PROP** | VAN @ EDM | Zach Hyman over 0.5 G | +140 | fanduel | 0.65 | 48% vs 39% (+24%) | $3 | — |
| 21 | **STRONG PROP** | CHI @ VGK | Jack Eichel over 0.5 A | -110 | draftkings | 0.93 | 60% vs 49% (+23%) | $4 | — |
| 22 | **STRONG PROP** | VAN @ EDM | Leon Draisaitl over 1.5 PTS | +110 | draftkings | 1.83 | 55% vs 44% (+23%) | $3 | — |
| 23 | **STRONG PROP** | MTL @ TOR | Darren Raddysh over 2.5 SOG | +100 | draftkings | 2.96 | 57% vs 46% (+23%) | $3 | — |
| 24 | **STRONG PROP** | NYR @ BOS | Marat Khusnutdinov over 0.5 PTS | +230 | draftkings | 0.43 | 35% vs 28% (+23%) | $2 | — |
| 25 | **STRONG PROP** | CHI @ VGK | Anton Frondell over 2.5 SOG | +136 | fanduel | 2.63 | 49% vs 40% (+23%) | $3 | — |
| 26 | **STRONG PROP** | NYR @ BOS | Oliver Bjorkstrand over 1.5 SOG | +120 | draftkings | 1.73 | 52% vs 42% (+23%) | $3 | — |
| 27 | **STRONG PROP** | CHI @ VGK | Tomas Hertl over 2.5 SOG | +126 | fanduel | 2.71 | 51% vs 42% (+22%) | $3 | — |
| 28 | **STRONG PROP** | MTL @ TOR | Cole Caufield over 3.5 SOG | +125 | fanduel | 3.71 | 51% vs 42% (+22%) | $3 | — |
| 29 | **STRONG PROP** | CHI @ VGK | Mark Stone over 0.5 PTS | -185 | draftkings | 1.33 | 73% vs 60% (+22%) | $5 | — |
| 30 | **STRONG PROP** | MTL @ TOR | Nick Suzuki over 0.5 A | -130 | draftkings | 1.03 | 64% vs 53% (+21%) | $4 | — |
| 31 | **STRONG PROP** | MTL @ TOR | Ivan Demidov over 0.5 PTS | -110 | draftkings | 0.88 | 59% vs 49% (+21%) | $3 | — |
| 32 | **STRONG PROP** | CHI @ VGK | Jack Eichel over 3.5 SOG | +110 | fanduel | 3.86 | 54% vs 45% (+21%) | $3 | — |
| 33 | **STRONG PROP** | NYR @ BOS | Morgan Geekie over 1.5 SOG | -155 | draftkings | 2.36 | 68% vs 57% (+21%) | $5 | — |
| 34 | **STRONG PROP** | MTL @ TOR | Cole Caufield over 3.5 SOG | +120 | draftkings | 3.71 | 51% vs 42% (+20%) | $2 | — |
| 35 | **STRONG PROP** | CHI @ VGK | Tyler Bertuzzi over 0.5 PTS | +120 | draftkings | 0.70 | 50% vs 42% (+20%) | $2 | — |
| 36 | **STRONG PROP** | CHI @ VGK | Shea Theodore under 0.5 PTS | +105 | draftkings | 0.61 | 54% vs 46% (+20%) | $3 | — |
| 37 | **STRONG PROP** | CHI @ VGK | Frank Nazar over 0.5 PTS | +150 | draftkings | 0.59 | 45% vs 38% (+20%) | $2 | — |
| 38 | **STRONG PROP** | NYR @ BOS | Hampus Lindholm under 0.5 PTS | -155 | draftkings | 0.39 | 68% vs 57% (+20%) | $4 | — |
| 39 | **STRONG PROP** | MTL @ TOR | Morgan Rielly over 1.5 SOG | +104 | fanduel | 1.84 | 55% vs 46% (+19%) | $3 | — |
| 40 | **STRONG PROP** | NYR @ BOS | J.T. Miller over 1.5 SOG | -145 | draftkings | 2.26 | 66% vs 55% (+19%) | $4 | — |
| 41 | **STRONG PROP** | MTL @ TOR | Juraj Slafkovský over 0.5 G | +220 | fanduel | 0.43 | 35% vs 29% (+19%) | $1 | — |
| 42 | **STRONG PROP** | MTL @ TOR | Morgan Rielly over 1.5 SOG | +100 | draftkings | 1.84 | 55% vs 47% (+18%) | $3 | — |
| 43 | **STRONG PROP** | CHI @ VGK | Tyler Bertuzzi over 1.5 SOG | +104 | fanduel | 1.82 | 54% vs 46% (+18%) | $3 | — |
| 44 | **STRONG PROP** | MTL @ TOR | Juraj Slafkovský over 0.5 PTS | -145 | draftkings | 1.04 | 65% vs 55% (+18%) | $3 | — |
| 45 | **STRONG PROP** | MTL @ TOR | Juraj Slafkovský over 0.5 A | +140 | draftkings | 0.61 | 46% vs 39% (+18%) | $2 | — |
| 46 | **STRONG PROP** | VAN @ EDM | Mattias Ekholm over 0.5 A | +170 | draftkings | 0.52 | 41% vs 35% (+18%) | $1 | — |
| 47 | **STRONG PROP** | VAN @ EDM | Zach Hyman over 0.5 PTS | -155 | draftkings | 1.10 | 67% vs 57% (+18%) | $4 | — |
| 48 | **STRONG PROP** | MTL @ TOR | Cole Caufield over 0.5 PTS | -190 | draftkings | 1.27 | 72% vs 61% (+18%) | $5 | — |
| 49 | **STRONG PROP** | MTL @ TOR | Darren Raddysh over 0.5 A | +125 | draftkings | 0.67 | 49% vs 41% (+18%) | $2 | — |
| 50 | **STRONG PROP** | VAN @ EDM | Connor McDavid over 3.5 SOG | -115 | draftkings | 4.08 | 58% vs 50% (+17%) | $3 | — |
| 51 | **STRONG PROP** | CHI @ VGK | Mark Stone over 1.5 SOG | -170 | draftkings | 2.38 | 69% vs 59% (+17%) | $4 | — |
| 52 | **STRONG PROP** | NYR @ BOS | Morgan Geekie over 1.5 SOG | -164 | fanduel | 2.36 | 68% vs 58% (+17%) | $4 | — |
| 53 | **STRONG PROP** | CHI @ VGK | Ivan Barbashev over 0.5 PTS | -105 | draftkings | 0.81 | 56% vs 48% (+17%) | $2 | — |
| 54 | **STRONG PROP** | MTL @ TOR | Nick Suzuki over 0.5 PTS | -230 | draftkings | 1.44 | 76% vs 65% (+17%) | $5 | — |
| 55 | **STRONG PROP** | NYR @ BOS | Hampus Lindholm under 0.5 A | -200 | draftkings | 0.32 | 73% vs 62% (+17%) | $5 | — |
| 56 | **STRONG PROP** | VAN @ EDM | Connor McDavid over 3.5 SOG | -114 | fanduel | 4.08 | 58% vs 50% (+16%) | $3 | — |
| 57 | **STRONG PROP** | VAN @ EDM | Connor McDavid over 1.5 PTS | -130 | draftkings | 2.06 | 61% vs 52% (+16%) | $3 | — |
| 58 | **STRONG PROP** | CHI @ VGK | Shea Theodore under 0.5 A | -145 | draftkings | 0.45 | 64% vs 55% (+16%) | $3 | — |
| 59 | **STRONG PROP** | MTL @ TOR | Lane Hutson over 0.5 A | -130 | draftkings | 0.94 | 61% vs 52% (+16%) | $3 | — |
| 60 | **STRONG PROP** | CHI @ VGK | Anton Frondell over 2.5 SOG | +120 | draftkings | 2.63 | 49% vs 42% (+16%) | $2 | — |
| 61 | **STRONG PROP** | NYR @ BOS | Pavel Zacha over 0.5 PTS | -110 | draftkings | 0.84 | 57% vs 49% (+16%) | $2 | — |
| 62 | **STRONG PROP** | VAN @ EDM | Evan Bouchard over 1.5 PTS | +160 | draftkings | 1.42 | 41% vs 36% (+16%) | $1 | — |
| 63 | **STRONG PROP** | MTL @ TOR | Kirill Marchenko over 2.5 SOG | -110 | draftkings | 2.93 | 56% vs 49% (+15%) | $2 | — |
| 64 | **STRONG PROP** | NYR @ BOS | Casey Mittelstadt over 0.5 PTS | +140 | draftkings | 0.59 | 45% vs 39% (+15%) | $1 | — |
| 65 | **STRONG PROP** | CHI @ VGK | Ivan Barbashev over 1.5 SOG | +100 | draftkings | 1.78 | 53% vs 46% (+15%) | $2 | — |
| 66 | **prop value** | CHI @ VGK | Carter Hart under 20.5 SV | -122 | fanduel | 18.45 | 66% vs 51% (+29%) | $5 | ⚠saves-model |
| 67 | **prop value** | CHI @ VGK | Carter Hart under 20.5 SV | -125 | draftkings | 18.45 | 66% vs 51% (+28%) | $5 | ⚠saves-model |
| 68 | **prop value** | MTL @ TOR | Jakub Dobes under 25.5 SV | -125 | draftkings | 23.63 | 63% vs 51% (+23%) | $4 | ⚠saves-model |
| 69 | **prop value** | CHI @ VGK | Spencer Knight over 25.5 SV | -105 | draftkings | 27.04 | 55% vs 48% (+15%) | $2 | ⚠saves-model |
| 70 | **prop value** | MTL @ TOR | Mike Matheson over 1.5 SOG | +110 | draftkings | 1.70 | 51% vs 44% (+15%) | $2 | — |
| 71 | **prop value** | MTL @ TOR | Noah Dobson over 1.5 SOG | -165 | fanduel | 2.30 | 67% vs 58% (+15%) | $3 | — |
| 72 | **prop value** | MTL @ TOR | Noah Dobson over 1.5 SOG | -170 | draftkings | 2.30 | 67% vs 59% (+14%) | $3 | — |
| 73 | **prop value** | CHI @ VGK | Anton Frondell over 0.5 A | +180 | draftkings | 0.48 | 38% vs 33% (+14%) | $1 | — |
| 74 | **prop value** | CHI @ VGK | Patrick Kane over 0.5 A | +140 | draftkings | 0.59 | 44% vs 39% (+14%) | $1 | — |
| 75 | **prop value** | NYR @ BOS | Eeli Tolvanen over 1.5 SOG | -120 | draftkings | 1.93 | 57% vs 50% (+14%) | $2 | — |
| 76 | **prop value** | CHI @ VGK | Mitch Marner over 0.5 A | +100 | draftkings | 0.75 | 53% vs 47% (+14%) | $1 | — |
| 77 | **prop value** | MTL @ TOR | Ivan Demidov under 1.5 SOG | +130 | draftkings | 1.81 | 46% vs 41% (+14%) | $1 | — |
| 78 | **prop value** | NYR @ BOS | JJ Peterka under 0.5 PTS | -115 | draftkings | 0.58 | 56% vs 50% (+14%) | $1 | — |
| 79 | **prop value** | CHI @ VGK | Jack Eichel over 0.5 PTS | -225 | draftkings | 1.33 | 73% vs 65% (+13%) | $3 | — |
| 80 | **prop value** | VAN @ EDM | Connor McDavid over 0.5 A | -230 | draftkings | 1.34 | 74% vs 65% (+13%) | $3 | — |
| 81 | **prop value** | CHI @ VGK | Tyler Bertuzzi over 1.5 SOG | -105 | draftkings | 1.82 | 54% vs 48% (+13%) | $2 | — |
| 82 | **prop value** | VAN @ EDM | Jake Walman under 0.5 A | -250 | draftkings | 0.28 | 76% vs 67% (+13%) | $4 | — |
| 83 | **prop value** | MTL @ TOR | Lane Hutson over 0.5 PTS | -175 | draftkings | 1.11 | 67% vs 59% (+13%) | $2 | — |
| 84 | **prop value** | NYR @ BOS | J.T. Miller over 1.5 SOG | -165 | fanduel | 2.26 | 66% vs 58% (+13%) | $2 | — |
| 85 | **prop value** | VAN @ EDM | Mattias Ekholm over 0.5 PTS | +130 | draftkings | 0.61 | 46% vs 41% (+13%) | $1 | — |
| 86 | **prop value** | NYR @ BOS | Vladislav Gavrikov over 0.5 PTS | +210 | draftkings | 0.42 | 34% vs 30% (+13%) | $1 | — |
| 87 | **prop value** | NYR @ BOS | David Pastrnak over 0.5 PTS | -225 | draftkings | 1.31 | 73% vs 65% (+13%) | $3 | — |
| 88 | **prop value** | MTL @ TOR | Jakub Dobes under 24.5 SV | -122 | fanduel | 23.63 | 58% vs 51% (+13%) | $2 | ⚠saves-model |
| 89 | **prop value** | MTL @ TOR | William Nylander over 0.5 A | -105 | draftkings | 0.76 | 53% vs 48% (+12%) | $1 | — |
| 90 | **prop value** | VAN @ EDM | Kasperi Kapanen under 1.5 SOG | +115 | draftkings | 1.73 | 48% vs 43% (+12%) | $1 | — |
| 91 | **prop value** | NYR @ BOS | Casey Mittelstadt under 1.5 SOG | -175 | draftkings | 1.19 | 67% vs 59% (+12%) | $2 | — |
| 92 | **prop value** | CHI @ VGK | Mark Stone over 0.5 G | +160 | fanduel | 0.51 | 40% vs 36% (+12%) | $1 | — |
| 93 | **prop value** | MTL @ TOR | William Nylander over 0.5 G | +180 | fanduel | 0.47 | 37% vs 33% (+12%) | $1 | — |
| 94 | **prop value** | MTL @ TOR | Nick Suzuki over 2.5 SOG | +115 | draftkings | 2.60 | 48% vs 43% (+12%) | $1 | — |
| 95 | **prop value** | VAN @ EDM | Zach Hyman over 2.5 SOG | -125 | draftkings | 3.00 | 58% vs 51% (+12%) | $1 | — |
| 96 | **prop value** | NYR @ BOS | Morgan Geekie over 0.5 PTS | -120 | draftkings | 0.84 | 57% vs 51% (+12%) | $1 | — |
| 97 | **prop value** | MTL @ TOR | Juraj Slafkovský over 2.5 SOG | +122 | fanduel | 2.56 | 47% vs 42% (+11%) | $1 | — |
| 98 | **prop value** | CHI @ VGK | Sam Rinzel under 1.5 SOG | -140 | fanduel | 1.35 | 61% vs 55% (+11%) | $2 | — |
| 99 | **prop value** | CHI @ VGK | Mitch Marner under 0.5 G | -230 | fanduel | 0.32 | 72% vs 65% (+11%) | $2 | — |
| 100 | **prop value** | NYR @ BOS | Adam Fox over 0.5 A | -110 | draftkings | 0.78 | 54% vs 49% (+11%) | $1 | — |
| 101 | **prop value** | VAN @ EDM | Kevin Lankinen under 27.5 SV | -120 | draftkings | 26.82 | 56% vs 51% (+11%) | $1 | ⚠saves-model |
| 102 | **prop value** | VAN @ EDM | Tristan Jarry over 20.5 SV | -130 | draftkings | 22.39 | 58% vs 52% (+10%) | $1 | ⚠saves-model |
| 103 | **prop value** | CHI @ VGK | Frank Nazar over 1.5 SOG | -115 | draftkings | 1.83 | 55% vs 50% (+10%) | $1 | — |
| 104 | **prop value** | CHI @ VGK | Patrick Kane over 0.5 PTS | -120 | draftkings | 0.81 | 56% vs 50% (+10%) | $1 | — |
| 105 | **prop value** | CHI @ VGK | Anton Frondell over 0.5 PTS | +100 | draftkings | 0.72 | 51% vs 47% (+10%) | $1 | — |
| 106 | **prop value** | MTL @ TOR | Auston Matthews under 0.5 A | -170 | draftkings | 0.44 | 64% vs 59% (+10%) | $1 | — |
| 107 | **prop value** | VAN @ EDM | Tristan Jarry over 20.5 SV | -130 | fanduel | 22.39 | 58% vs 53% (+10%) | $1 | ⚠saves-model |
| 108 | **prop value** | NYR @ BOS | Noah Laba under 1.5 SOG | -230 | draftkings | 1.05 | 72% vs 65% (+10%) | $2 | — |
| 109 | **prop value** | NYR @ BOS | David Pastrnak under 0.5 G | -200 | fanduel | 0.38 | 68% vs 62% (+10%) | $1 | — |
| 110 | **prop value** | MTL @ TOR | William Nylander over 0.5 PTS | -225 | draftkings | 1.23 | 71% vs 65% (+9%) | $1 | — |
| 111 | **prop value** | VAN @ EDM | Marco Rossi over 0.5 PTS | -105 | draftkings | 0.73 | 52% vs 48% (+9%) | — | — |
| 112 | **prop value** | NYR @ BOS | Jeremy Swayman under 24.5 SV | -130 | draftkings | 23.72 | 57% vs 52% (+9%) | — | ⚠saves-model |
| 113 | **prop value** | NYR @ BOS | Adam Fox under 1.5 SOG | +116 | fanduel | 1.77 | 47% vs 43% (+9%) | — | — |
| 114 | **prop value** | MTL @ TOR | John Tavares over 0.5 G | +220 | fanduel | 0.38 | 32% vs 29% (+9%) | — | — |
| 115 | **prop value** | NYR @ BOS | Marat Khusnutdinov under 1.5 SOG | -230 | draftkings | 1.07 | 71% vs 65% (+9%) | $1 | — |
| 116 | **prop value** | VAN @ EDM | Zach Hyman over 0.5 A | +185 | draftkings | 0.44 | 36% vs 33% (+9%) | — | — |
| 117 | **prop value** | MTL @ TOR | Chris Kreider over 1.5 SOG | -170 | draftkings | 2.16 | 64% vs 59% (+8%) | — | — |
| 118 | **prop value** | NYR @ BOS | Fraser Minten under 1.5 SOG | -122 | fanduel | 1.49 | 56% vs 52% (+8%) | $1 | — |
| 119 | **prop value** | MTL @ TOR | Cole Caufield over 0.5 A | +145 | draftkings | 0.53 | 41% vs 38% (+8%) | — | — |
| 120 | **prop value** | VAN @ EDM | Brock Boeser under 2.5 SOG | -175 | draftkings | 2.12 | 64% vs 59% (+8%) | — | — |
| 121 | **prop value** | CHI @ VGK | Brett Howden under 0.5 PTS | -190 | draftkings | 0.41 | 66% vs 61% (+8%) | — | — |
| 122 | **prop value** | VAN @ EDM | Evan Bouchard over 0.5 A | -195 | draftkings | 1.10 | 67% vs 62% (+8%) | $1 | — |
| 123 | **prop value** | CHI @ VGK | Rasmus Andersson over 0.5 PTS | +115 | draftkings | 0.63 | 47% vs 43% (+8%) | — | — |
| 124 | **prop value** | CHI @ VGK | Spencer Knight over 25.5 SV | -118 | fanduel | 27.04 | 55% vs 51% (+8%) | — | ⚠saves-model |

## 2. Projections (first 40 by game)

```
Game        Player                    Pos Market  Line   Proj  P(over)   Over/Under  Book
MTL @ TOR   Jakub Dobes               G   SV      25.5  23.63      37%    -110/-125  draftkings
MTL @ TOR   Jakub Dobes               G   SV      24.5  23.63      42%    -108/-122  fanduel
MTL @ TOR   Cole Caufield             R   SOG      3.5   3.71      51%    +120/-165  draftkings
MTL @ TOR   Cole Caufield             R   SOG      3.5   3.71      51%    +125/-164  fanduel
MTL @ TOR   Nick Suzuki               C   SOG      2.5   2.60      48%    +115/-160  draftkings
MTL @ TOR   Nick Suzuki               C   SOG      2.5   2.60      48%    +110/-144  fanduel
MTL @ TOR   Juraj Slafkovský          L   SOG      2.5   2.56      47%    +105/-145  draftkings
MTL @ TOR   Juraj Slafkovský          L   SOG      2.5   2.56      47%    +122/-160  fanduel
MTL @ TOR   Noah Dobson               D   SOG      1.5   2.30      67%    -170/+125  draftkings
MTL @ TOR   Noah Dobson               D   SOG      1.5   2.30      67%    -165/+126  fanduel
MTL @ TOR   Chris Kreider             L   SOG      1.5   2.16      64%    -170/+125  draftkings
MTL @ TOR   Ivan Demidov              R   SOG      1.5   1.81      54%    -175/+130  draftkings
MTL @ TOR   Lane Hutson               D   SOG      1.5   1.76      53%    -140/+105  draftkings
MTL @ TOR   Lane Hutson               D   SOG      1.5   1.76      53%    -140/+108  fanduel
MTL @ TOR   Mike Matheson             D   SOG      1.5   1.70      51%    +110/-150  draftkings
MTL @ TOR   Nick Suzuki               C   PTS      0.5   1.44      76%    -230/+170  draftkings
MTL @ TOR   Cole Caufield             R   PTS      0.5   1.27      72%    -190/+140  draftkings
MTL @ TOR   Lane Hutson               D   PTS      0.5   1.11      67%    -175/+130  draftkings
MTL @ TOR   Juraj Slafkovský          L   PTS      0.5   1.04      65%    -145/+105  draftkings
MTL @ TOR   Nick Suzuki               C   A        0.5   1.03      64%    -130/+100  draftkings
MTL @ TOR   Lane Hutson               D   A        0.5   0.94      61%    -130/-105  draftkings
MTL @ TOR   Ivan Demidov              R   PTS      0.5   0.88      59%    -110/-125  draftkings
MTL @ TOR   Chris Kreider             L   PTS      0.5   0.78      54%    +115/-160  draftkings
MTL @ TOR   Cole Caufield             R   G        0.5   0.74      52%    +130/-180  fanduel
MTL @ TOR   Noah Dobson               D   PTS      0.5   0.69      50%    +145/-200  draftkings
MTL @ TOR   Juraj Slafkovský          L   A        0.5   0.61      46%    +140/-190  draftkings
MTL @ TOR   Ivan Demidov              R   A        0.5   0.61      46%    +165/-230  draftkings
MTL @ TOR   Mike Matheson             D   PTS      0.5   0.55      43%    +205/-285  draftkings
MTL @ TOR   Cole Caufield             R   A        0.5   0.53      41%    +145/-195  draftkings
MTL @ TOR   Noah Dobson               D   A        0.5   0.51      40%    +200/-275  draftkings
MTL @ TOR   Mike Matheson             D   A        0.5   0.45      36%    +265/-370  draftkings
MTL @ TOR   Chris Kreider             L   A        0.5   0.44      35%    +235/-330  draftkings
MTL @ TOR   Juraj Slafkovský          L   G        0.5   0.43      35%    +220/-310  fanduel
MTL @ TOR   Nick Suzuki               C   G        0.5   0.41      34%    +195/-270  fanduel
MTL @ TOR   Chris Kreider             L   G        0.5   0.34      29%    +290/-440  fanduel
MTL @ TOR   Ivan Demidov              R   G        0.5   0.27      24%    +260/-400  fanduel
MTL @ TOR   Sergei Bobrovsky          G   SV      25.5  20.26      20%    -115/-120  draftkings
MTL @ TOR   Sergei Bobrovsky          G   SV      25.5  20.26      20%    -112/-118  fanduel
MTL @ TOR   Auston Matthews           C   SOG      3.5   3.86      54%    -120/-110  draftkings
MTL @ TOR   Auston Matthews           C   SOG      3.5   3.86      54%    -114/-114  fanduel
```

## 3. NHL paper ledger to date

```
NHL prop paper bets — settled by market/side/strength (pending: 187)
market                    side   str    n   W   L   P   staked   profit     ROI
(nothing settled yet)
```

> Paper only. No NHL analysis run exists; the projection was walk-forward calibrated on last season (`--calibrate`) but no historical prop prices exist to backtest ROI. The ledger above is the first evidence.

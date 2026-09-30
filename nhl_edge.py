#!/usr/bin/env python3
# Copyright (c) 2026 William Brooks Parker. All rights reserved. Proprietary — see LICENSE.
"""
nhl_edge.py — NHL player-prop outlier finder (2026-27 season).

Props covered: skater shots on goal, points, goals, assists, blocked shots, power-play
points; goalie saves. Model side is built from the NHL's public API (api-web.nhle.com,
keyless): every player's game log is stored in nhl.db and turned into a per-game rate
with shrinkage toward last season, scaled by the opponent's pace/allowance, then into a
Poisson probability of clearing the posted line. Market side is The Odds API
(ODDS_API_KEY in the environment or a gitignored .env), a CSV of lines you type, or —
keyless, the default without a key — DraftKings' two-sided player totals via ESPN's
propBets feed.

Same discipline as cfb_edge / soccer_edge: every flagged prop is paper-logged, settled
from the boxscore, and nothing is a real-money recommendation until analysis says so
(LIVE_STAKES is shared with cfb_edge). --calibrate walks forward through last season so
the projection is tested before the first puck drops. Saves use a gamma-Poisson (the rate
itself uncertain), and simulate_card runs the lock + five 20,000 times with teammates
correlated, under the model's odds and the market's.

Sections:
  ---- constants / models ----
  ---- NHL API adapters ----
  ---- projections ----
  ---- prop lines (Odds API / ESPN-DraftKings / CSV) ----
  ---- signals ----
  ---- SQLite ----
  ---- calibration ----
  ---- rendering / report ----
  ---- main ----
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import math
import os
import sqlite3
import sys
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from statistics import NormalDist
from typing import Optional

import requests

import cfb_edge as ce

NHL_DB = "nhl.db"
REPORTS_DIR = ce.REPORTS_DIR
LOCAL_TZ = ce.LOCAL_TZ
UA = ce.UA

NHL_WEB = "https://api-web.nhle.com/v1"
NHL_STATS = "https://api.nhle.com/stats/rest/en"
ODDS_API = "https://api.the-odds-api.com/v4"
ODDS_SPORT = "icehockey_nhl"
ESPN_NHL_SCOREBOARD = "https://site.api.espn.com/apis/site/v2/sports/hockey/nhl/scoreboard"
ESPN_NHL_CORE = "https://sports.core.api.espn.com/v2/sports/hockey/leagues/nhl"
ESPN_DK = 100                     # ESPN's provider id for DraftKings
ESPN_PROP_MARKETS = {             # ESPN propBets type name -> Odds API market key (two-sided totals only;
    "Total Shots on Goal": "player_shots_on_goal",   # milestones and scorer props are one-sided and can't be de-vigged)
    "Total Points": "player_points",
    "Total Assists": "player_assists",
    "Total Blocked Shots": "player_blocked_shots",
    "Total Saves": "player_total_saves",
}

SEASON = 20262027                 # the season we are projecting
PRIOR_SEASON = 20252026           # the season the prior comes from
HISTORY_SEASON = 20242025         # the season before that: the prior for the walk-forward test of PRIOR_SEASON
SEASON_START = dt.date(2026, 9, 29)

# ---- decision constants (NHL props). Every one is a prior until analysis/06 says otherwise. ----
MARKETS = {                       # Odds API market -> (stat column, who, label)
    "player_shots_on_goal": ("shots", "skater", "SOG"),
    "player_points": ("points", "skater", "PTS"),
    "player_goals": ("goals", "skater", "G"),
    "player_assists": ("assists", "skater", "A"),
    "player_blocked_shots": ("blocked", "skater", "BLK"),
    "player_power_play_points": ("pp_points", "skater", "PPP"),
    "player_total_saves": ("saves", "goalie", "SV"),
}
# ---- skater projection (2026-09-30): fit walk-forward on 2024-25 (prior 2023-24), tested on 2025-26 (prior
#      2024-25) over every skater who played, beat the old recipe at every line of every stat (CHANGELOG) ----
#   minutes: toi = (Σ toi this season + TOI_PRIOR_W·Σ toi last season + TOI_GHOST·position mean) / (games, same weights),
#            then TOI_RECENT_W toward the last-5 mean once this season has a game (role changes show up in minutes first)
#   rate:    per minute = (Σ stat this season + a1·Σ stat last season + K·position rate) / (toi this season + a1·toi last + K)
#   λ = rate × minutes × (opponent allowance / league)^β × √h at home, ÷ √h away
TOI_PRIOR_W = 0.09
TOI_GHOST = 0.6
TOI_RECENT_W = 0.56
TOI_RECENT_GAMES = 5
SKATER_MODEL = {                  # stat -> (a1 last-season weight, K ghost minutes at the position rate, β, h home/away)
    "shots": (0.35, 86.0, 0.84, 1.037),       # shots repeat: little regression
    "points": (0.58, 234.0, 0.70, 1.078),
    "goals": (0.81, 694.0, 0.64, 1.077),      # shooting luck: ~37% regression for a full-time forward
    "assists": (0.58, 355.0, 0.73, 1.078),
    "pp_points": (0.31, 50.0, 0.59, 1.115),
}                                 # a1, K, β fit on 2024-25; h = the league's home/away ratio over 2024-26 (analysis/06 C:
                                  #   1.11 in 2024-25 but 1.045 in 2025-26 for points, so one season's fit overshoots)
SHRINK_GAMES = 20.0               # goalies (old recipe, unchanged): games of prior-season weight; also caps ⚠thin credit
MIN_GAMES = 10                    # fewer total games behind a rate -> ⚠thin, never staked
RECENT_GAMES = 10                 # goalies: rolling window that gets extra weight
RECENT_WEIGHT = 0.35
OPP_FACTOR_CAP = (0.80, 1.20)     # opponent allowance / league is clamped before the β exponent
EDGE_PCT = 8.0                    # model P(side) over de-vigged fair, %: value
EDGE_STRONG_PCT = 15.0            # STRONG
EDGE_OVERREACH_PCT = 30.0         # >= this: strength 0. Prior from CFB + soccer: the biggest gaps lose most
SAVES_MAX_STRENGTH = 1            # goalie saves: Poisson barely beat naive (0.613 vs 0.616); k=20 gets 0.603 — cap stays until the ledger speaks
MAX_PRICE = 250                   # never stake a prop side longer than +250 or shorter than -250
MIN_PRICE = -250
AGREE_MIN_PRICE = -250            # agreement board ("winners, not outliers", the football just-win twin):
AGREE_MAX_PRICE = -110            #   the side model and market both favour, priced -250..-110,
AGREE_MAX_GAP_PCT = 20.0          #   model over fair by > 0 and <= +20%, never saves, never thin
GOOD_PICKS_N = 5
BLEND_MODEL_W = 0.25              # the lock + five rank on a logit blend: 25% model, 75% de-vigged line. A prior, not
                                  #   a fit: every sport says the closer is sharper, and on opening night (282 lines,
                                  #   old recipe) the market out-scored the model, log-loss 0.648 vs 0.667
# ---- simulation (2026-09-29, walk-forward on 2025-26 stored logs; see --calibrate and analysis/06 C/D) ----
DISPERSION = {"saves": 20.0,      # gamma-Poisson shape per stat; absent = Poisson. Saves log-loss @27.5:
              "shots": 17.5}      #   Poisson 0.6131 → k=20 0.6032. Shots (2026-09-30, fit with the new recipe):
                                  #   k=17.5 — Poisson over-called over 1.5 by 1.1 pp. PTS/G/A/PPP: Poisson best
DISPERSION_GRID = (None, 50.0, 20.0, 12.0, 8.0, 5.0, 3.0, 2.0)   # what --calibrate searches
TEAM_RHO = {"points": 0.1047, "assists": 0.0525}   # latent same-team correlation for the card simulation:
                                  #   sin(π/2·r), r = teammate indicator corr 0.0668 (PTS) / 0.0334 (A), whole league; opponents ≈ 0
SIM_N = 20000                     # simulated nights per card
SIM_SEED = 20260929
FINDINGS_AS_OF = "2026-09-30"     # analysis/06 run 2026-09-30: projection backtest (C), opening-night ledger (A/B, E)
MODEL_VERSION = "2026-09-30"      # stamped on every props / paper_bets row, so analysis/06 E can score recipes apart


# =====================================================================
# ---- models ----
# =====================================================================

@dataclass
class Player:
    id: int
    name: str
    team: str
    position: str                  # C L R D G
    rates: dict[str, float] = field(default_factory=dict)      # stat -> per-game mean (unadjusted)
    games: int = 0                 # games behind the rate (both seasons, weighted)
    starter: Optional[bool] = None # goalies: projected starter?


@dataclass
class GameCtx:
    id: int
    date: dt.date
    start_utc: dt.datetime
    home: str
    away: str
    state: str                     # FUT / PRE / LIVE / OFF / FINAL
    home_factor: dict[str, float] = field(default_factory=dict)   # stat -> opp multiplier for HOME players
    away_factor: dict[str, float] = field(default_factory=dict)

    @property
    def kick_local(self) -> dt.datetime:
        return self.start_utc.astimezone(LOCAL_TZ)

    @property
    def short(self) -> str:
        return f"{self.away} @ {self.home}"


@dataclass
class Prop:
    game: GameCtx
    player: Player
    market: str                    # Odds API key
    stat: str
    line: float
    over: Optional[int]
    under: Optional[int]
    book: str = "?"
    mean: Optional[float] = None   # projected λ
    p_over: Optional[float] = None


@dataclass
class Signal:
    prop: Prop
    kind: str                      # "prop" (value board: truth_p = model) · "agree" (lock board: truth_p = blend)
    side: str                      # over / under
    label: str
    strength: int
    edge: float                    # model over de-vigged fair, %
    truth_p: Optional[float]
    price: Optional[int]
    note: str = ""
    model_p: Optional[float] = None   # the projection's own P(side), whatever truth_p holds
    fair_p: Optional[float] = None    # de-vigged market P(side)

    @property
    def what(self) -> str:
        p = self.prop
        return f"{p.player.name} {self.side} {p.line:g} {MARKETS[p.market][2]}"


def poisson_cdf(k: int, lam: float) -> float:
    """P(X <= k) for X ~ Poisson(lam)."""
    if k < 0:
        return 0.0
    if lam <= 0:
        return 1.0
    term = math.exp(-lam)
    total = term
    for i in range(1, k + 1):
        term *= lam / i
        total += term
    return min(1.0, total)


def nb_cdf(k: int, lam: float, disp: float) -> float:
    """P(X <= k) for the gamma-Poisson mixture: λ ~ Gamma(shape=disp, mean=lam), X ~ Poisson(λ).
    That is what a simulation of 'the rate itself is uncertain' converges to (negative binomial,
    variance lam + lam²/disp); disp → ∞ is plain Poisson."""
    if k < 0:
        return 0.0
    if lam <= 0:
        return 1.0
    q = lam / (disp + lam)
    term = (1.0 - q) ** disp
    total = term
    for i in range(k):
        term *= (i + disp) / (i + 1) * q
        total += term
    return min(1.0, total)


def count_cdf(k: int, lam: float, disp: Optional[float] = None) -> float:
    return poisson_cdf(k, lam) if disp is None else nb_cdf(k, lam, disp)


def p_over(lam: float, line: float, disp: Optional[float] = None) -> tuple[float, float]:
    """(P(over), P(push)) for a prop line. Half lines never push. `disp` = gamma-Poisson shape
    (DISPERSION per stat); None = Poisson."""
    k = math.floor(line)
    if abs(line - k) < 1e-9:           # whole number: push at exactly k
        push = count_cdf(k, lam, disp) - count_cdf(k - 1, lam, disp)
        over = 1.0 - count_cdf(k, lam, disp)
        return over, push
    return 1.0 - count_cdf(k, lam, disp), 0.0


def devig2(a: Optional[int], b: Optional[int]) -> tuple[Optional[float], Optional[float]]:
    return ce.devig_pair(a, b)


def blend_p(model: float, fair: float, w: float = BLEND_MODEL_W) -> float:
    """Logit-space blend of the model's P(side) with the de-vigged line's: w on the model, 1 − w on the market."""
    def logit(p: float) -> float:
        p = min(max(p, 1e-6), 1 - 1e-6)
        return math.log(p / (1 - p))
    return 1.0 / (1.0 + math.exp(-(w * logit(model) + (1 - w) * logit(fair))))


def load_key() -> Optional[str]:
    k = os.environ.get("ODDS_API_KEY")
    if k:
        return k.strip()
    for path in (".env", os.path.expanduser("~/.odds_api_key")):
        if os.path.exists(path):
            with open(path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("ODDS_API_KEY="):
                        return line.split("=", 1)[1].strip().strip('"').strip("'")
                    if path.endswith(".odds_api_key") and line and "=" not in line:
                        return line
    return None


# =====================================================================
# ---- NHL API adapters ----
# =====================================================================

def _get(url: str, params: Optional[dict] = None, timeout: int = 30) -> dict:
    r = requests.get(url, params=params, headers=UA, timeout=timeout)
    r.raise_for_status()
    return r.json()


def fetch_schedule(date: dt.date) -> list[GameCtx]:
    d = _get(f"{NHL_WEB}/schedule/{date.isoformat()}")
    out = []
    for day in d.get("gameWeek", []):
        if day.get("date") != date.isoformat():
            continue
        for g in day.get("games", []):
            if g.get("gameType") != 2:               # regular season only
                continue
            out.append(GameCtx(id=int(g["id"]), date=date,
                               start_utc=dt.datetime.fromisoformat(g["startTimeUTC"].replace("Z", "+00:00")),
                               home=g["homeTeam"]["abbrev"], away=g["awayTeam"]["abbrev"],
                               state=g.get("gameState", "FUT")))
    return out


def fetch_teams() -> list[str]:
    """The 32 active clubs (the stats /team list includes every defunct franchise)."""
    d = _get(f"{NHL_WEB}/standings/now")
    return sorted({t["teamAbbrev"]["default"] for t in d.get("standings", [])})


def fetch_roster(team: str, season: int = SEASON) -> list[Player]:
    d = _get(f"{NHL_WEB}/roster/{team}/{season}")
    out = []
    for grp in ("forwards", "defensemen", "goalies"):
        for p in d.get(grp, []):
            name = f"{p['firstName']['default']} {p['lastName']['default']}"
            out.append(Player(id=int(p["id"]), name=name, team=team, position=p.get("positionCode", "?")))
    return out


def fetch_league_players(season: int) -> list[Player]:
    """Everyone who played a regular-season game in a finished season (skaters and goalies), from the stats
    API. The build stores their logs too, so the position means and the walk-forward test are not
    survivors-only (players since retired, released or sent down count)."""
    out = []
    for kind in ("skater", "goalie"):
        d = _get(f"{NHL_STATS}/{kind}/summary", {"limit": -1, "cayenneExp": f"seasonId={season} and gameTypeId=2"})
        for r in d.get("data", []):
            out.append(Player(id=int(r["playerId"]), name=r.get("skaterFullName") or r.get("goalieFullName") or "",
                              team="", position="G" if kind == "goalie" else r.get("positionCode", "?")))
    return out


def fetch_game_log(player_id: int, season: int, game_type: int = 2) -> list[dict]:
    try:
        d = _get(f"{NHL_WEB}/player/{player_id}/game-log/{season}/{game_type}")
    except requests.HTTPError:
        return []
    return d.get("gameLog", [])


def fetch_team_summary(season: int) -> dict[str, dict]:
    """Per-team pace: shots for/against per game, goals for/against per game."""
    d = _get(f"{NHL_STATS}/team/summary", {"limit": -1, "cayenneExp": f"seasonId={season} and gameTypeId=2"})
    id2abbr = {t["id"]: t["triCode"] for t in _get(f"{NHL_STATS}/team").get("data", [])}
    out = {}
    for t in d.get("data", []):
        ab = id2abbr.get(t.get("teamId"))
        if not ab:
            continue
        out[ab] = {"gp": t.get("gamesPlayed", 0), "sf": t.get("shotsForPerGame"), "sa": t.get("shotsAgainstPerGame"),
                   "gf": t.get("goalsForPerGame"), "ga": t.get("goalsAgainstPerGame")}
    return out


def fetch_boxscore_stats(game_id: int) -> tuple[dict[int, dict], Optional[str]]:
    """(player_id -> actual stats, gameState) for a finished game. Power-play points are not
    in the boxscore; settle falls back to the player's game log for that stat."""
    d = _get(f"{NHL_WEB}/gamecenter/{game_id}/boxscore")
    out = {}
    for side in ("homeTeam", "awayTeam"):
        grp = d.get("playerByGameStats", {}).get(side, {})
        for p in grp.get("forwards", []) + grp.get("defense", []):
            out[int(p["playerId"])] = {"shots": p.get("sog", 0), "points": p.get("points", 0), "goals": p.get("goals", 0),
                                       "assists": p.get("assists", 0), "blocked": p.get("blockedShots", 0)}
        for g in grp.get("goalies", []):
            out[int(g["playerId"])] = {"saves": g.get("saves", 0), "shots_against": g.get("shotsAgainst", 0),
                                       "started": bool(g.get("starter"))}
    return out, d.get("gameState")


# =====================================================================
# ---- projections ----
# =====================================================================

def _log_rows(player: Player, season: int, logs: list[dict]) -> list[tuple]:
    rows = []
    for g in logs:
        if player.position == "G":
            rows.append((int(g["gameId"]), player.id, season, g["gameDate"], g.get("teamAbbrev"), g.get("opponentAbbrev"),
                         g.get("homeRoadFlag") == "H", None, None, None, None, None, None,
                         g.get("shotsAgainst", 0) - g.get("goalsAgainst", 0), g.get("shotsAgainst", 0),
                         int(g.get("gamesStarted", 0) or 0), _toi_min(g.get("toi"))))
        else:
            rows.append((int(g["gameId"]), player.id, season, g["gameDate"], g.get("teamAbbrev"), g.get("opponentAbbrev"),
                         g.get("homeRoadFlag") == "H", g.get("shots", 0), g.get("points", 0), g.get("goals", 0),
                         g.get("assists", 0), None, g.get("powerPlayPoints", 0), None, None, None, _toi_min(g.get("toi"))))
    return rows


UPSERT_LOG = ("INSERT INTO game_logs(game_id,player_id,season,date,team,opp,home,shots,points,goals,assists,blocked,"
              "pp_points,saves,shots_against,started,toi) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) "
              "ON CONFLICT(game_id, player_id) DO UPDATE SET season=excluded.season, date=excluded.date, "
              "team=excluded.team, opp=excluded.opp, home=excluded.home, shots=excluded.shots, points=excluded.points, "
              "goals=excluded.goals, assists=excluded.assists, blocked=COALESCE(excluded.blocked, game_logs.blocked), "
              "pp_points=excluded.pp_points, saves=excluded.saves, shots_against=excluded.shots_against, "
              "started=excluded.started, toi=excluded.toi")      # a rebuild keeps the blocks --settle wrote


def _toi_min(s: Optional[str]) -> Optional[float]:
    if not s or ":" not in s:
        return None
    m, sec = s.split(":")
    return int(m) + int(sec) / 60.0


def build_logs(conn: sqlite3.Connection, seasons: tuple[int, ...] = (HISTORY_SEASON, PRIOR_SEASON, SEASON),
               workers: int = 12, log=print) -> int:
    """Rosters for every team this season, plus everyone who played in the finished seasons -> game logs -> nhl.db.
    Finished (player, season) pairs already stored are not fetched again; the current season always is.
    Players no longer on a roster keep their logs but lose their team, so a line can never match them."""
    teams = fetch_teams()
    players: list[Player] = []
    for t in teams:
        try:
            players += fetch_roster(t)
        except requests.HTTPError:
            log(f"  roster {t}: not available yet")
    rostered = {p.id for p in players}
    if rostered:
        conn.execute(f"UPDATE players SET team=NULL WHERE id NOT IN ({','.join(map(str, rostered))})")
    for p in players:
        conn.execute("INSERT OR REPLACE INTO players(id,name,team,position) VALUES (?,?,?,?)",
                     (p.id, p.name, p.team, p.position))
    jobs: dict[tuple[int, int], Player] = {(p.id, s): p for p in players for s in seasons}
    for s in [s for s in seasons if s != SEASON]:
        for p in fetch_league_players(s):
            conn.execute("INSERT OR IGNORE INTO players(id,name,team,position) VALUES (?,?,NULL,?)",
                         (p.id, p.name, p.position))
            jobs.setdefault((p.id, s), p)
    conn.commit()
    stored = {(pid, s) for pid, s in conn.execute("SELECT DISTINCT player_id, season FROM game_logs WHERE season != ?",
                                                  (SEASON,))}
    todo = [(p, s) for (pid, s), p in jobs.items() if s == SEASON or (pid, s) not in stored]
    log(f"  {len(players)} rostered players on {len(teams)} teams · {len(todo)} player-seasons to fetch "
        f"({len(jobs) - len(todo)} finished ones already stored)")

    def one(job: tuple[Player, int]):
        p, s = job
        return _log_rows(p, s, fetch_game_log(p.id, s))
    n = 0
    with ThreadPoolExecutor(workers) as ex:
        for rows in ex.map(one, todo):
            conn.executemany(UPSERT_LOG, rows)
            n += len(rows)
    conn.execute("INSERT OR REPLACE INTO build_log(built_at, players, rows) VALUES (?,?,?)",
                 (dt.datetime.now(LOCAL_TZ).isoformat(timespec="minutes"), len(players), n))
    conn.commit()
    return n


def _grp(position: str) -> str:
    return "D" if position == "D" else "F"


def position_means(conn: sqlite3.Connection, season: int = PRIOR_SEASON) -> dict[str, dict[str, float]]:
    """What a skater's minutes and per-minute rates regress toward: per position group (F / D), the mean
    TOI per game and Σ stat / Σ minutes over every skater-game of `season` (everyone who played, since
    --build stores the whole league for finished seasons)."""
    out: dict[str, dict[str, float]] = {}
    for grp, cond in (("F", "p.position IN ('C','L','R')"), ("D", "p.position = 'D'")):
        r = conn.execute("SELECT COUNT(*), SUM(l.toi), SUM(l.shots), SUM(l.points), SUM(l.goals), SUM(l.assists), "
                         "SUM(l.pp_points) FROM game_logs l JOIN players p ON p.id = l.player_id "
                         f"WHERE l.season = ? AND l.toi IS NOT NULL AND l.shots IS NOT NULL AND {cond}", (season,)).fetchone()
        if not r[0] or not r[1]:
            continue
        out[grp] = {"toi": r[1] / r[0], **{s: (v or 0) / r[1] for s, v in zip(SKATER_MODEL, r[2:])}}
    return out


def skater_projection(pm: dict[str, float], n_p: int, toi_p: float, sums_p: list[float], n_c: int, toi_c: float,
                      sums_c: list[float], recent_toi: list[float]) -> tuple[dict[str, float], float]:
    """The skater recipe on sufficient statistics: games, minutes and stat sums (SKATER_MODEL order) for last
    season (_p) and this season so far (_c), plus this season's last TOI_RECENT_GAMES minutes. Returns (per-game
    λ at a neutral rink vs an average opponent, projected minutes). pm = position_means() for the group."""
    toi = (toi_c + TOI_PRIOR_W * toi_p + TOI_GHOST * pm["toi"]) / (n_c + TOI_PRIOR_W * n_p + TOI_GHOST)
    if recent_toi:
        toi = (1 - TOI_RECENT_W) * toi + TOI_RECENT_W * sum(recent_toi) / len(recent_toi)
    rates = {stat: (sums_c[i] + a1 * sums_p[i] + k * pm[stat]) / (toi_c + a1 * toi_p + k) * toi
             for i, (stat, (a1, k, _beta, _h)) in enumerate(SKATER_MODEL.items())}
    return rates, toi


def skater_rates(rows: list[tuple], pm: dict[str, float], prior_season: int = PRIOR_SEASON,
                 season: int = SEASON) -> tuple[dict[str, float], Optional[float]]:
    """skater_projection on one player's rows (season, toi, shots, points, goals, assists, pp_points), all
    strictly before the game, in date order."""
    prior = [r for r in rows if r[0] == prior_season and r[1] is not None]
    cur = [r for r in rows if r[0] == season and r[1] is not None]
    if not prior and not cur:
        return {}, None
    return skater_projection(pm, len(prior), sum(r[1] for r in prior),
                             [sum(r[2 + i] or 0 for r in prior) for i in range(len(SKATER_MODEL))],
                             len(cur), sum(r[1] for r in cur), [sum(r[2 + i] or 0 for r in cur) for i in range(len(SKATER_MODEL))],
                             [r[1] for r in cur[-TOI_RECENT_GAMES:]])


def player_rates(conn: sqlite3.Connection, player_id: int, as_of: dt.date, position: str,
                 pm: Optional[dict[str, dict[str, float]]] = None) -> tuple[dict[str, float], float]:
    """Per-game rates as of a date and the games behind them (for ⚠thin). Skaters: skater_rates (the
    2026-09-30 recipe; pm = position_means(), computed here if not passed). Goalies: saves per START, this
    season shrunk to last (SHRINK_GAMES) with a recent-10 tilt. Blocked shots only exist in boxscores: the
    rate is the plain per-game mean of whatever --settle stored, absent until then."""
    if position != "G":
        rows = conn.execute("SELECT season, toi, shots, points, goals, assists, pp_points, blocked FROM game_logs "
                            "WHERE player_id=? AND date<? AND season IN (?,?) ORDER BY date, game_id",
                            (player_id, as_of.isoformat(), PRIOR_SEASON, SEASON)).fetchall()
        pm = pm if pm is not None else position_means(conn)
        rates, _ = skater_rates([r[:7] for r in rows], pm.get(_grp(position)) or next(iter(pm.values()), {})) if pm else ({}, None)
        blk = [r[7] for r in rows if r[7] is not None]
        if blk:
            rates["blocked"] = sum(blk) / len(blk)
        n_cur = sum(1 for r in rows if r[0] == SEASON)
        return rates, n_cur + min(len(rows) - n_cur, SHRINK_GAMES)
    cols = ["saves", "shots_against", "started"]
    rows = conn.execute(f"SELECT season, date, {','.join(cols)} FROM game_logs WHERE player_id=? AND date<? "
                        "ORDER BY date", (player_id, as_of.isoformat())).fetchall()
    prior = [r for r in rows if r[0] == PRIOR_SEASON and r[4]]          # goalies: rate per START
    cur = [r for r in rows if r[0] == SEASON and r[4]]
    rates: dict[str, float] = {}
    for i, c in enumerate(cols):
        if c == "started":
            continue
        rate = goalie_rate([r[2 + i] for r in prior if r[2 + i] is not None],
                           [r[2 + i] for r in cur if r[2 + i] is not None])
        if rate is not None:
            rates[c] = rate
    eff = len(cur) + min(len(prior), SHRINK_GAMES)
    return rates, eff


def goalie_rate(pv: list[float], cv: list[float]) -> Optional[float]:
    """Goalie per-start rate (the pre-2026-09-30 recipe, kept for saves): this season's mean shrunk toward last
    season's by SHRINK_GAMES, then RECENT_WEIGHT toward the last RECENT_GAMES starts once there are five."""
    if not pv and not cv:
        return None
    prior_mean = sum(pv) / len(pv) if pv else sum(cv) / len(cv)
    cur_mean = sum(cv) / len(cv) if cv else prior_mean
    w = len(cv) / (len(cv) + SHRINK_GAMES)
    base = w * cur_mean + (1 - w) * prior_mean
    rv = cv[-RECENT_GAMES:]
    if len(rv) >= 5:
        base = (1 - RECENT_WEIGHT) * base + RECENT_WEIGHT * sum(rv) / len(rv)
    return base


def opponent_factors(summary_prior: dict, summary_cur: dict, home: str, away: str) -> tuple[dict, dict]:
    """Multipliers for HOME players' stats (vs away's allowance) and AWAY players' stats."""
    def blend(team, key):
        p = (summary_prior.get(team) or {}).get(key)
        c = summary_cur.get(team) or {}
        gp = c.get("gp") or 0
        cv = c.get(key)
        if cv is None:
            return p
        if p is None:
            return cv
        w = gp / (gp + 20.0)
        return w * cv + (1 - w) * p
    lg_sf = [v["sf"] for v in summary_prior.values() if v.get("sf")]
    lg_sa = [v["sa"] for v in summary_prior.values() if v.get("sa")]
    lg_ga = [v["ga"] for v in summary_prior.values() if v.get("ga")]
    avg_sf = sum(lg_sf) / len(lg_sf) if lg_sf else 30.0
    avg_sa = sum(lg_sa) / len(lg_sa) if lg_sa else 30.0
    avg_ga = sum(lg_ga) / len(lg_ga) if lg_ga else 3.0
    lo, hi = OPP_FACTOR_CAP

    def clamp(x):
        return max(lo, min(hi, x))

    def factors(opp, at_home):
        sa = blend(opp, "sa") or avg_sa          # opp shots allowed / game
        ga = blend(opp, "ga") or avg_ga          # opp goals allowed / game
        sf_opp = blend(opp, "sf") or avg_sf      # opp shots taken (for goalie saves)
        out = {"blocked": clamp(sf_opp / avg_sf), "saves": clamp(sf_opp / avg_sf)}
        for stat, (_a1, _k, beta, h) in SKATER_MODEL.items():
            allow = clamp(sa / avg_sa) if stat == "shots" else clamp(ga / avg_ga)
            out[stat] = allow ** beta * (math.sqrt(h) if at_home else 1.0 / math.sqrt(h))
        return out
    return factors(away, True), factors(home, False)


def project(prop: Prop) -> None:
    r = prop.player.rates.get(prop.stat)
    if r is None:
        return
    g = prop.game
    f = (g.home_factor if prop.player.team == g.home else g.away_factor).get(prop.stat, 1.0)
    prop.mean = r * f
    po, push = p_over(prop.mean, prop.line, DISPERSION.get(prop.stat))
    prop.p_over = po / (1.0 - push) if push < 1 else 0.5      # conditional on no push


# =====================================================================
# ---- prop lines ----
# =====================================================================

def fetch_props_oddsapi(key: str, games: list[GameCtx], books: str = "draftkings,fanduel,betmgm,caesars",
                        log=print) -> list[tuple]:
    """(game_id, player_name, market, line, over, under, book) from The Odds API."""
    events = _get(f"{ODDS_API}/sports/{ODDS_SPORT}/events", {"apiKey": key})
    by_teams = {}
    for ev in events:
        by_teams[(ev.get("home_team", ""), ev.get("away_team", ""))] = ev["id"]
    out = []
    used = 0
    for g in games:
        ev_id = None
        for (h, a), eid in by_teams.items():
            if _team_match(h, g.home) and _team_match(a, g.away):
                ev_id = eid
                break
        if not ev_id:
            continue
        try:
            r = requests.get(f"{ODDS_API}/sports/{ODDS_SPORT}/events/{ev_id}/odds",
                             params={"apiKey": key, "regions": "us", "oddsFormat": "american",
                                     "markets": ",".join(MARKETS), "bookmakers": books}, headers=UA, timeout=30)
            used = r.headers.get("x-requests-used", used)
            r.raise_for_status()
            d = r.json()
        except requests.HTTPError as e:
            log(f"  odds api {g.short}: {e}")
            continue
        for bk in d.get("bookmakers", []):
            for mk in bk.get("markets", []):
                if mk["key"] not in MARKETS:
                    continue
                lines: dict[tuple, dict] = {}
                for o in mk.get("outcomes", []):
                    k = (o.get("description"), o.get("point"))
                    lines.setdefault(k, {})[o.get("name")] = o.get("price")
                for (pname, pt), sides in lines.items():
                    if pt is None:
                        continue
                    out.append((g.id, pname, mk["key"], float(pt), sides.get("Over"), sides.get("Under"), bk["key"]))
    log(f"  odds api: {len(out)} prop sides · requests used this month: {used}")
    return out


def fetch_props_espn(games: list[GameCtx], date: dt.date, log=print) -> list[tuple]:
    """(game_id, player_name, market, line, over, under, book) — DraftKings via ESPN's propBets feed.
    Each two-sided total arrives as two consecutive items sharing athlete/type/line, Over first
    (checked on opening night: Matthews 0.5 PTS -195 then +145). Athlete names come from each $ref."""
    sb = _get(ESPN_NHL_SCOREBOARD, {"dates": date.strftime("%Y%m%d")})
    ev_for: dict[int, str] = {}
    for ev in sb.get("events", []):
        comp = ev["competitions"][0]
        teams = {c["homeAway"]: c["team"].get("displayName", "") for c in comp.get("competitors", [])}
        for g in games:
            if _team_match(teams.get("home", ""), g.home) and _team_match(teams.get("away", ""), g.away):
                ev_for[g.id] = ev["id"]
    pairs: list[tuple] = []                      # (game_id, athlete_ref, market, line, [prices in feed order])
    for g in games:
        eid = ev_for.get(g.id)
        if not eid:
            continue
        try:
            d = _get(f"{ESPN_NHL_CORE}/events/{eid}/competitions/{eid}/odds/{ESPN_DK}/propBets", {"limit": 1000})
        except requests.HTTPError as e:
            log(f"  espn props {g.short}: {e}")
            continue
        open_: dict[tuple, list] = {}
        for it in d.get("items", []):
            market = ESPN_PROP_MARKETS.get((it.get("type") or {}).get("name"))
            ref = (it.get("athlete") or {}).get("$ref")
            line = ((it.get("odds") or {}).get("total") or {}).get("value")
            am = str((((it.get("odds") or {}).get("american") or {}).get("value") or "")).upper()
            price = 100 if am == "EVEN" else ce._int(am.replace("+", ""))
            if not market or not ref or line is None or price is None:
                continue
            k = (ref.split("?")[0], market, float(line))
            open_.setdefault(k, []).append(price)
        pairs += [(g.id, *k, v) for k, v in open_.items() if len(v) == 2]
    refs = sorted({p[1] for p in pairs})

    def name(ref: str) -> tuple[str, Optional[str]]:
        try:
            return ref, _get(ref).get("fullName")
        except requests.RequestException:
            return ref, None
    with ThreadPoolExecutor(max_workers=12) as ex:
        names = dict(ex.map(name, refs))
    out = [(gid, names[ref], market, line, prices[0], prices[1], "draftkings")
           for gid, ref, market, line, prices in pairs if names.get(ref)]
    log(f"  espn/draftkings: {len(out)} two-sided player totals across {len(ev_for)} games")
    return out


TEAM_WORDS = {"NJD": "devils", "NYI": "islanders", "NYR": "rangers", "PHI": "flyers", "PIT": "penguins", "BOS": "bruins",
              "BUF": "sabres", "MTL": "canadiens", "OTT": "senators", "TOR": "maple leafs", "CAR": "hurricanes",
              "FLA": "panthers", "TBL": "lightning", "WSH": "capitals", "CHI": "blackhawks", "DET": "red wings",
              "NSH": "predators", "STL": "blues", "CGY": "flames", "COL": "avalanche", "EDM": "oilers", "VAN": "canucks",
              "ANA": "ducks", "DAL": "stars", "LAK": "kings", "SJS": "sharks", "CBJ": "blue jackets", "MIN": "wild",
              "WPG": "jets", "VGK": "golden knights", "SEA": "kraken", "UTA": "mammoth"}


def _team_match(full_name: str, abbr: str) -> bool:
    w = TEAM_WORDS.get(abbr, abbr.lower())
    return w in full_name.lower()


def read_props_csv(path: str, games: list[GameCtx]) -> list[tuple]:
    """player,market,line,over,under[,book[,game]] — game as 'AWAY @ HOME' or blank (matched by roster)."""
    out = []
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            gid = None
            if r.get("game"):
                for g in games:
                    if g.short.replace(" ", "").lower() == r["game"].replace(" ", "").lower():
                        gid = g.id
            out.append((gid, r["player"].strip(), r["market"].strip(), float(r["line"]), ce._int(r.get("over")),
                        ce._int(r.get("under")), (r.get("book") or "csv").strip()))
    return out


def attach_props(rows: list[tuple], games: list[GameCtx], players: dict[str, list[Player]]) -> list[Prop]:
    """Match (game, player name) to rostered players on the two teams; unmatched rows are dropped."""
    gmap = {g.id: g for g in games}
    out = []
    for gid, pname, market, line, over, under, book in rows:
        if market not in MARKETS:
            continue
        cands = []
        for g in ([gmap[gid]] if gid in gmap else games):
            for p in players.get(g.home, []) + players.get(g.away, []):
                if _name_match(p.name, pname):
                    cands.append((g, p))
        if len(cands) != 1:
            continue
        g, p = cands[0]
        stat, who, _ = MARKETS[market]
        if (who == "goalie") != (p.position == "G"):
            continue
        out.append(Prop(g, p, market, stat, line, over, under, book))
    return out


def _name_match(roster: str, market: str) -> bool:
    a = _norm(roster)
    b = _norm(market)
    if a == b:
        return True
    ra, rb = a.split(), b.split()
    return bool(ra and rb) and ra[-1] == rb[-1] and ra[0][0] == rb[0][0]


def _norm(s: str) -> str:
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return " ".join(s.lower().replace(".", "").replace("-", " ").replace("'", "").split())


# =====================================================================
# ---- signals ----
# =====================================================================

def prop_signal(p: Prop) -> Optional[Signal]:
    if p.p_over is None or p.over is None or p.under is None:
        return None
    fo, fu = devig2(p.over, p.under)
    if fo is None:
        return None
    best: Optional[Signal] = None
    for side, model, fair, price in (("over", p.p_over, fo, p.over), ("under", 1 - p.p_over, fu, p.under)):
        edge = (model - fair) / fair * 100.0
        if edge <= 0:
            continue
        strength = 2 if edge >= EDGE_STRONG_PCT else 1 if edge >= EDGE_PCT else 0
        note = ""
        if edge >= EDGE_OVERREACH_PCT:
            strength, note = 0, "⚠overreach"
        if price > MAX_PRICE or price < MIN_PRICE:
            strength = 0
        if p.player.games < MIN_GAMES:
            strength, note = 0, "⚠thin"
        if p.stat == "saves":
            strength = min(strength, SAVES_MAX_STRENGTH)
            note = note or "⚠saves-model"
        if p.player.position == "G" and p.player.starter is False:
            strength, note = 0, "⚠not-starter"
        label = {2: "STRONG PROP", 1: "prop value", 0: ""}[strength]
        s = Signal(p, "prop", side, label, strength, edge, model, price, note, model_p=model, fair_p=fair)
        if best is None or s.edge > best.edge:
            best = s
    return best


def ranked_signals(props: list[Prop]) -> list[Signal]:
    sigs = [s for p in props if p.game.state in ("FUT", "PRE") for s in (prop_signal(p),) if s and s.strength]
    sigs.sort(key=lambda s: (-s.strength, -s.edge))
    return sigs


def agree_signal(p: Prop) -> Optional[Signal]:
    """The side both the projection and the de-vigged line call more likely than not, at a holdable
    favourite's price, with the model a little (not a lot) above the market. Kind `agree`, its own
    paper bucket: the opposite question to prop_signal, same as football's just-win board. truth_p is
    the blend (BLEND_MODEL_W), the best guess at the chance to cash; the gap test reads the raw model."""
    if p.p_over is None or p.over is None or p.under is None or p.stat == "saves" or p.player.games < MIN_GAMES:
        return None
    fo, fu = devig2(p.over, p.under)
    if fo is None:
        return None
    for side, model, fair, price in (("over", p.p_over, fo, p.over), ("under", 1 - p.p_over, fu, p.under)):
        if model <= 0.5 or fair <= 0.5 or not (AGREE_MIN_PRICE <= price <= AGREE_MAX_PRICE):
            continue
        edge = (model - fair) / fair * 100.0
        if 0 < edge <= AGREE_MAX_GAP_PCT:
            return Signal(p, "agree", side, "agree", 1, edge, blend_p(model, fair), price, model_p=model, fair_p=fair)
    return None


def agree_board(props: list[Prop]) -> list[Signal]:
    """Agreement signals, best book per (player, market), most likely to cash (blend) first."""
    best: dict[tuple, Signal] = {}
    for p in props:
        if p.game.state not in ("FUT", "PRE"):
            continue
        s = agree_signal(p)
        k = (p.player.id, p.market, s.side if s else None)
        if s and (k not in best or ce.american_to_decimal(s.price) > ce.american_to_decimal(best[k].price)):
            best[k] = s
    return sorted(best.values(), key=lambda s: (-s.truth_p, -s.edge))


def lock_and_good(props: list[Prop], n: int = GOOD_PICKS_N) -> tuple[Optional[Signal], list[Signal]]:
    """The lock is the top of the agreement board (most likely to cash at a holdable price).
    Good picks are the rest of that board, then the ranked value board, one per player."""
    ab = agree_board(props)
    lock = ab[0] if ab else None
    seen = {lock.prop.player.id} if lock else set()
    good: list[Signal] = []
    for s in ab[1:] + ranked_signals(props):
        if s.prop.player.id in seen:
            continue
        good.append(s)
        seen.add(s.prop.player.id)
        if len(good) >= n:
            break
    return lock, good


def _team_rho(stat: str) -> float:
    return TEAM_RHO.get(stat, TEAM_RHO["points"]) if stat != "saves" else 0.0


def side_probs(s: Signal) -> dict[str, float]:
    """P(this ticket cashes) three ways: the projection, the de-vigged line, and the blend of the two."""
    fo, fu = devig2(s.prop.over, s.prop.under)
    fair = s.fair_p if s.fair_p is not None else (fo if s.side == "over" else fu)
    model = s.model_p if s.model_p is not None else s.truth_p
    return {"model": model, "blend": blend_p(model, fair), "market": fair}


def simulate_card(sigs: list[Signal], source: str = "model", n: int = SIM_N, seed: int = SIM_SEED) -> Optional[dict]:
    """Monte Carlo of a card of prop tickets played together, `n` nights.

    Each ticket keeps its own chance to cash exactly (source = "model": the projection; "market": the
    de-vigged fair price; "blend": the two in logit space, BLEND_MODEL_W on the model); what the
    simulation adds is how they move together. One-factor Gaussian copula: every team-game draws a
    latent 'offense' Z, and each skater's over-event is latent = √ρ·Z + √(1−ρ)·ε > Φ⁻¹(1 − P(over)).
    Teammates correlate at √(ρᵢρⱼ) (TEAM_RHO, measured on 2025-26 logs), opponents are independent
    (measured r ≈ −0.01). An under ticket cashes when its over-event does not. Flat $1 a ticket at its
    own price."""
    import numpy as np
    if not sigs:
        return None
    nd = NormalDist()
    rng = np.random.default_rng(seed)
    teams = sorted({(s.prop.game.id, s.prop.player.team) for s in sigs})
    z = {t: rng.standard_normal(n) for t in teams}
    hits = np.zeros((n, len(sigs)), dtype=bool)
    pays = []
    for j, s in enumerate(sigs):
        p = s.prop
        p_side = side_probs(s)[source]
        p_ov = min(max(p_side if s.side == "over" else 1.0 - p_side, 1e-9), 1 - 1e-9)
        rho = _team_rho(p.stat)
        lat = math.sqrt(rho) * z[(p.game.id, p.player.team)] + math.sqrt(1 - rho) * rng.standard_normal(n)
        over = lat > nd.inv_cdf(1.0 - p_ov)
        hits[:, j] = over if s.side == "over" else ~over
        pays.append(ce.american_to_decimal(s.price) - 1.0)
    pays_arr = np.array(pays)
    profit = (hits * pays_arr).sum(axis=1) - (~hits).sum(axis=1)
    k = hits.sum(axis=1)
    parlay_dec = float(np.prod(pays_arr + 1.0))
    p_all = float(hits.all(axis=1).mean())
    return {"source": source, "n": n, "tickets": len(sigs), "exp_hits": float(k.mean()),
            "dist": [float((k == i).mean()) for i in range(len(sigs) + 1)],
            "p_all": p_all, "exp_profit": float(profit.mean()), "p_profit": float((profit > 0).mean()),
            "p5": float(np.percentile(profit, 5)), "p50": float(np.percentile(profit, 50)),
            "p95": float(np.percentile(profit, 95)), "parlay_dec": parlay_dec, "parlay_ev": p_all * parlay_dec - 1.0}


def stake_for(sig: Signal, bankroll: float) -> Optional[float]:
    return ce.stake_for(sig, bankroll)


# =====================================================================
# ---- SQLite ----
# =====================================================================

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (id INTEGER PRIMARY KEY, name TEXT, team TEXT, position TEXT);
CREATE TABLE IF NOT EXISTS game_logs (
  game_id INTEGER, player_id INTEGER, season INTEGER, date TEXT, team TEXT, opp TEXT, home INTEGER,
  shots INTEGER, points INTEGER, goals INTEGER, assists INTEGER, blocked INTEGER, pp_points INTEGER,
  saves INTEGER, shots_against INTEGER, started INTEGER, toi REAL,
  PRIMARY KEY (game_id, player_id)
);
CREATE INDEX IF NOT EXISTS ix_logs_player ON game_logs(player_id, date);
CREATE TABLE IF NOT EXISTS build_log (built_at TEXT PRIMARY KEY, players INTEGER, rows INTEGER);
CREATE TABLE IF NOT EXISTS games (
  id INTEGER PRIMARY KEY, date TEXT, start_utc TEXT, home TEXT, away TEXT, state TEXT,
  home_score INTEGER, away_score INTEGER, completed INTEGER DEFAULT 0
);
CREATE TABLE IF NOT EXISTS props (
  id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, player_id INTEGER, taken_at TEXT, book TEXT,
  market TEXT, line REAL, over INTEGER, under INTEGER, mean REAL, p_over REAL
);
CREATE TABLE IF NOT EXISTS paper_bets (
  id INTEGER PRIMARY KEY AUTOINCREMENT, game_id INTEGER, player_id INTEGER, logged_at TEXT, kind TEXT,
  market TEXT, side TEXT, line REAL, price INTEGER, truth_p REAL, edge REAL, strength INTEGER, stake REAL,
  book TEXT, actual REAL, result TEXT, profit REAL
);
"""
MIGRATIONS: dict[str, list[tuple[str, str]]] = {
    "props": [("model", "TEXT")],            # MODEL_VERSION that priced the row; NULL = the 2026-09-20 recipe
    "paper_bets": [("model", "TEXT")],
}


def db_connect(path: str = NHL_DB) -> sqlite3.Connection:
    conn = sqlite3.connect(path)
    conn.executescript(SCHEMA)
    for table, cols in MIGRATIONS.items():
        have = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
        for col, typ in cols:
            if col not in have:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {col} {typ}")
    conn.commit()
    return conn


def db_players(conn: sqlite3.Connection) -> dict[str, list[Player]]:
    out: dict[str, list[Player]] = {}
    for pid, name, team, pos in conn.execute("SELECT id,name,team,position FROM players WHERE team IS NOT NULL"):
        out.setdefault(team, []).append(Player(int(pid), name, team, pos))
    return out


def db_persist(conn: sqlite3.Connection, games: list[GameCtx], props: list[Prop], now: dt.datetime) -> int:
    for g in games:
        conn.execute("INSERT INTO games(id,date,start_utc,home,away,state) VALUES (?,?,?,?,?,?) "
                     "ON CONFLICT(id) DO UPDATE SET state=excluded.state",
                     (g.id, g.date.isoformat(), g.start_utc.isoformat(), g.home, g.away, g.state))
    n = 0
    for p in props:
        conn.execute("INSERT INTO props(game_id,player_id,taken_at,book,market,line,over,under,mean,p_over,model) "
                     "VALUES (?,?,?,?,?,?,?,?,?,?,?)",
                     (p.game.id, p.player.id, now.isoformat(), p.book, p.market, p.line, p.over, p.under, p.mean, p.p_over,
                      MODEL_VERSION))
        n += 1
    conn.commit()
    return n


def db_paper_log(conn: sqlite3.Connection, sigs: list[Signal], bankroll: float, now: dt.datetime) -> int:
    n = 0
    for s in sigs:
        if s.strength == 0 or s.truth_p is None:
            continue
        p = s.prop
        if conn.execute("SELECT 1 FROM paper_bets WHERE game_id=? AND player_id=? AND market=? AND kind=?",
                        (p.game.id, p.player.id, p.market, s.kind)).fetchone():
            continue
        conn.execute("INSERT INTO paper_bets(game_id,player_id,logged_at,kind,market,side,line,price,truth_p,edge,"
                     "strength,stake,book,model) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     (p.game.id, p.player.id, now.isoformat(), s.kind, p.market, s.side, p.line, s.price, s.truth_p,
                      s.edge, s.strength, stake_for(s, bankroll) or 0.0, p.book, MODEL_VERSION))
        n += 1
    conn.commit()
    return n


def grade_prop(side: str, line: float, actual: float) -> str:
    if actual == line:
        return "P"
    return "W" if ((actual > line) == (side == "over")) else "L"


def db_settle(conn: sqlite3.Connection, log=print) -> tuple[int, float, float]:
    """Pull boxscores for every game with a pending paper bet; grade from actual stats and
    store the boxscore rows as game logs (this is also how blocked shots get a rate)."""
    pend = conn.execute("SELECT DISTINCT game_id FROM paper_bets WHERE result IS NULL").fetchall()
    n, staked, profit = 0, 0.0, 0.0
    for (gid,) in pend:
        try:
            stats, state = fetch_boxscore_stats(gid)
        except requests.HTTPError:
            continue
        if state not in ("OFF", "FINAL"):
            continue
        for pid, st in stats.items():
            conn.execute("UPDATE game_logs SET blocked=? WHERE game_id=? AND player_id=?", (st.get("blocked"), gid, pid))
        for bid, pid, market, side, line, price, stake in conn.execute(
                "SELECT id,player_id,market,side,line,price,stake FROM paper_bets WHERE game_id=? AND result IS NULL",
                (gid,)).fetchall():
            stat = MARKETS[market][0]
            st = stats.get(pid)
            if st is not None and stat == "pp_points":
                st = {**st, "pp_points": _gamelog_stat(pid, gid, "powerPlayPoints")}
            if st is None or st.get(stat) is None:
                actual = 0.0            # scratched / did not play: books void, we grade as a push
                res = "P"
            else:
                actual = float(st[stat])
                res = grade_prop(side, line, actual)
            pr = ce._profit(res, stake, price)
            conn.execute("UPDATE paper_bets SET actual=?,result=?,profit=? WHERE id=?", (actual, res, pr, bid))
            n += 1
            staked += stake
            profit += pr
        conn.execute("UPDATE games SET completed=1, state=? WHERE id=?", (state, gid))
    conn.commit()
    return n, staked, profit


def _gamelog_stat(pid: int, gid: int, key: str) -> Optional[float]:
    for g in fetch_game_log(pid, SEASON):
        if int(g.get("gameId", 0)) == gid:
            return g.get(key)
    return None


def db_paper_summary(conn: sqlite3.Connection) -> str:
    rows = conn.execute("SELECT market,side,strength,COUNT(*),SUM(result='W'),SUM(result='L'),SUM(result='P'),"
                        "SUM(stake),SUM(profit) FROM paper_bets WHERE result IS NOT NULL "
                        "GROUP BY market,side,strength ORDER BY strength DESC, market, side").fetchall()
    pend = conn.execute("SELECT COUNT(*) FROM paper_bets WHERE result IS NULL").fetchone()[0]
    out = [f"NHL prop paper bets — settled by market/side/strength (pending: {pend})",
           f"{'market':<26}{'side':<6}{'str':>4}{'n':>5}{'W':>4}{'L':>4}{'P':>4}{'staked':>9}{'profit':>9}{'ROI':>8}"]
    for mk, side, st, n, w, l_, p, stk, pr in rows:
        roi = (pr / stk * 100) if stk else 0.0
        out.append(f"{mk:<26}{side:<6}{st:>4}{n:>5}{w:>4}{l_:>4}{p:>4}{stk:>9.2f}{pr:>9.2f}{roi:>+7.1f}%")
    if not rows:
        out.append("(nothing settled yet)")
    return "\n".join(out)


# =====================================================================
# ---- calibration ----
# =====================================================================

CAL_LINES = {"shots": (1.5, 2.5, 3.5), "points": (0.5, 1.5), "goals": (0.5,), "assists": (0.5,), "pp_points": (0.5,),
             "saves": (24.5, 27.5)}   # the lines books hang; the first is the one binned and dispersion-searched...
CAL_MAIN = {"shots": 2.5, "points": 0.5, "goals": 0.5, "assists": 0.5, "pp_points": 0.5, "saves": 27.5}
CAL_MIN_GAMES = 20                # the test set: skaters with ≥ 20 games at ≥ CAL_MIN_TOI a game the season before (who
CAL_MIN_TOI = 12.0                #   books hang props on); goalies with ≥ 20 starts the season before, their starts only
CAL_EARLY = 10                    # "early": the first 10 games of the season, where the prior does most of the work


def _ll(p: float, y: float) -> float:
    p = min(max(p, 1e-6), 1 - 1e-6)
    return -(y * math.log(p) + (1 - y) * math.log(1 - p))


def backtest(conn: sqlite3.Connection, season: int = PRIOR_SEASON, prior: int = HISTORY_SEASON) -> list[tuple]:
    """(stat, λ, actual, games into the season, naive λ) for every test-set player-game of `season`, projected
    exactly as the live model would have that morning: last season = `prior`, this season's earlier games,
    the opponent's allowance as of that date (opponent_factors on team summaries built from the logs), home or
    away. Calls the live skater_projection / goalie_rate / opponent_factors, so it tests the code that picks."""
    pos = dict(conn.execute("SELECT id, position FROM players"))
    rows = conn.execute("SELECT game_id, player_id, season, date, team, opp, home, toi, shots, points, goals, assists, "
                        "pp_points, saves, started FROM game_logs WHERE season IN (?, ?) "
                        "ORDER BY date, game_id, player_id", (prior, season)).fetchall()
    pm = position_means(conn, prior)
    if not pm or not any(r[2] == season for r in rows):
        return []
    stat_ix = range(8, 8 + len(SKATER_MODEL))          # shots..pp_points columns, SKATER_MODEL order
    by_game: dict[tuple, dict] = {}             # (season, game) -> {team: [shots for, goals for]}
    game_date: dict[tuple, str] = {}
    for r in rows:
        if pos.get(r[1]) in ("C", "L", "R", "D") and r[7] is not None and r[8] is not None:
            t = by_game.setdefault((r[2], r[0]), {}).setdefault(r[4], [0, 0])
            t[0] += r[8]
            t[1] += r[10]
            game_date[(r[2], r[0])] = r[3]
    team_rows: dict[tuple, list] = {}           # (season, team) -> [(date, shots for, shots against, goals against)]
    for key, teams in by_game.items():
        if len(teams) != 2:
            continue
        (ta, (sfa, gfa)), (tb, (sfb, gfb)) = sorted(teams.items())
        team_rows.setdefault((key[0], ta), []).append((game_date[key], sfa, sfb, gfb))
        team_rows.setdefault((key[0], tb), []).append((game_date[key], sfb, sfa, gfa))

    def summarize(games: list) -> dict:
        n = len(games)
        return {"gp": n, "sf": sum(g[1] for g in games) / n, "sa": sum(g[2] for g in games) / n,
                "ga": sum(g[3] for g in games) / n}
    summary_prior = {t: summarize(g) for (s, t), g in team_rows.items() if s == prior and g}
    team_cur = {t: sorted(g) for (s, t), g in team_rows.items() if s == season}

    agg_p: dict[int, list] = {}                 # skater: [games, minutes, stat sums...] last season
    starts_p: dict[int, list] = {}              # goalie: saves in last season's starts
    for r in rows:
        if r[2] != prior:
            continue
        if pos.get(r[1]) == "G":
            if r[14] and r[13] is not None:
                starts_p.setdefault(r[1], []).append(r[13])
        elif r[7] is not None and r[8] is not None:
            a = agg_p.setdefault(r[1], [0, 0.0] + [0.0] * len(SKATER_MODEL))
            a[0] += 1
            a[1] += r[7]
            for j, i in enumerate(stat_ix):
                a[2 + j] += r[i] or 0
    naive = {g: {s: m[s] * m["toi"] for s in SKATER_MODEL} for g, m in pm.items()}
    all_sv = [v for vs in starts_p.values() for v in vs]
    naive_sv = sum(all_sv) / len(all_sv) if all_sv else 27.0

    out: list[tuple] = []
    agg_c: dict[int, list] = {}
    recent: dict[int, list] = {}
    starts_c: dict[int, list] = {}
    cur_rows = [r for r in rows if r[2] == season]
    dates = sorted({r[3] for r in cur_rows})
    by_date: dict[str, list] = {}
    for r in cur_rows:
        by_date.setdefault(r[3], []).append(r)
    for d in dates:
        summary_cur = {}
        for t, games in team_cur.items():
            before = [g for g in games if g[0] < d]
            if before:
                summary_cur[t] = summarize(before)
        matchup = {r[0]: ((r[4], r[5]) if r[6] else (r[5], r[4])) for r in by_date[d]}      # game -> (home, away)
        facs = {gid: opponent_factors(summary_prior, summary_cur, h, a) for gid, (h, a) in matchup.items()}
        for r in by_date[d]:
            gid, pid, team, toi = r[0], r[1], r[4], r[7]
            p_pos = pos.get(pid)
            if p_pos is None:
                continue
            side = facs[gid][0] if matchup[gid][0] == team else facs[gid][1]
            if p_pos == "G":
                pv = starts_p.get(pid, [])
                if r[14] and r[13] is not None and len(pv) >= CAL_MIN_GAMES:
                    lam = goalie_rate(pv, starts_c.get(pid, [])) * side["saves"]
                    out.append(("saves", lam, r[13], len(starts_c.get(pid, [])), naive_sv))
                continue
            a_p = agg_p.get(pid)
            if toi is None or r[8] is None or a_p is None or a_p[0] < CAL_MIN_GAMES or a_p[1] / a_p[0] < CAL_MIN_TOI:
                continue
            a_c = agg_c.get(pid, [0, 0.0] + [0.0] * len(SKATER_MODEL))
            rates, _ = skater_projection(pm[_grp(p_pos)], a_p[0], a_p[1], a_p[2:], a_c[0], a_c[1], a_c[2:],
                                         recent.get(pid, [])[-TOI_RECENT_GAMES:])
            for j, stat in enumerate(SKATER_MODEL):
                out.append((stat, rates[stat] * side[stat], r[8 + j], a_c[0], naive[_grp(p_pos)][stat]))
        for r in by_date[d]:                                      # the day's games join the history afterwards
            pid, toi = r[1], r[7]
            if pos.get(pid) == "G":
                if r[14] and r[13] is not None:
                    starts_c.setdefault(pid, []).append(r[13])
            elif toi is not None and r[8] is not None:
                a = agg_c.setdefault(pid, [0, 0.0] + [0.0] * len(SKATER_MODEL))
                a[0] += 1
                a[1] += toi
                for j, i in enumerate(stat_ix):
                    a[2 + j] += r[i] or 0
                recent.setdefault(pid, []).append(toi)
    return out


def calibrate(conn: sqlite3.Connection, season: int = PRIOR_SEASON, prior: int = HISTORY_SEASON, log=print) -> dict:
    """The live projection walked forward through `season` (backtest), scored at the lines books hang against a
    naive position-average model, plus bias, the first-ten-games slice, a reliability table and the dispersion
    grid at the main line. No prop prices exist for past seasons, so this validates the projection, not the
    ROI; analysis/06 E scores it against the lines nhl.db has snapshotted since opening night."""
    bt = backtest(conn, season, prior)
    if not bt:
        log(f"no {prior} + {season} game logs to walk through — run --build (it stores both finished seasons)")
        return {}
    report = {}
    log(f"Walk-forward: every {season} game projected from {prior} + earlier {season} games, live recipe "
        f"(test set: ≥ {CAL_MIN_GAMES} games at ≥ {CAL_MIN_TOI:g} min the season before; goalies ≥ {CAL_MIN_GAMES} starts)")
    for stat in list(SKATER_MODEL) + ["saves"]:
        xs = [x for x in bt if x[0] == stat]
        if not xs:
            continue
        disp = DISPERSION.get(stat)
        rep = {"n": len(xs), "lines": {}}
        log(f"\n{stat.upper()} — {len(xs):,} player-games · dispersion k {'∞ (Poisson)' if disp is None else f'{disp:g}'}")
        log(f"  {'line':>6}{'log-loss':>10}{'naive':>9}{'better by':>11}{'bias':>8}{'early ll':>10}{'early bias':>12}")
        for line in CAL_LINES[stat]:
            ll = lln = bias = 0.0
            e_ll = e_bias = 0.0
            e_n = 0
            for _, lam, y, n_cur, lam_n in xs:
                p = p_over(lam, line, disp)[0]
                hit = 1.0 if y > line else 0.0
                ll += _ll(p, hit)
                lln += _ll(p_over(lam_n, line)[0], hit)
                bias += p - hit
                if n_cur < CAL_EARLY:
                    e_ll += _ll(p, hit)
                    e_bias += p - hit
                    e_n += 1
            n = len(xs)
            rep["lines"][line] = {"ll": ll / n, "ll_naive": lln / n, "bias": bias / n,
                                  "ll_early": e_ll / e_n if e_n else None, "bias_early": e_bias / e_n if e_n else None}
            log(f"  {line:>6g}{ll / n:>10.4f}{lln / n:>9.4f}{(lln - ll) / n:>+11.4f}{bias / n:>+8.3f}"
                + (f"{e_ll / e_n:>10.4f}{e_bias / e_n:>+12.3f}" if e_n else ""))
        main = CAL_MAIN[stat]
        bins: dict[int, list] = {}
        for _, lam, y, _, _ in xs:
            p = p_over(lam, main, disp)[0]
            acc = bins.setdefault(min(9, int(p * 10)), [0, 0.0, 0.0])
            acc[0] += 1
            acc[1] += p
            acc[2] += 1.0 if y > main else 0.0
        grid = {k: sum(_ll(p_over(lam, main, k)[0], 1.0 if y > main else 0.0) for _, lam, y, _, _ in xs) / len(xs)
                for k in DISPERSION_GRID}
        best = min(grid, key=lambda k: (grid[k], k is not None))
        rep.update(bins=bins, dispersion=grid, best_dispersion=best)
        log(f"  over {main:g}, by predicted P(over):  " + " · ".join(
            f"{b / 10:.1f}–{(b + 1) / 10:.1f}: {100 * sp / c:.0f}% vs {100 * sy / c:.0f}% (n {c})"
            for b, (c, sp, sy) in sorted(bins.items()) if c >= 50))
        log(f"  dispersion k at {main:g}: " + " · ".join(f"{'∞' if k is None else f'{k:g}'} {v:.4f}" for k, v in grid.items())
            + f" → best {'∞' if best is None else f'{best:g}'}")
        report[stat] = rep
    return report


# =====================================================================
# ---- rendering / report ----
# =====================================================================

def render_top(props: list[Prop], bankroll: float, n: int = 15) -> str:
    sigs = ranked_signals(props)[:n]
    if not sigs:
        return ce.stakes_banner() + "\nno flagged NHL props on this slate"
    out = [ce.stakes_banner(), f"Top {len(sigs)} NHL prop outliers — projection vs de-vigged line — bankroll ${bankroll:.0f}, 1/4 Kelly"]
    for i, s in enumerate(sigs, 1):
        p = s.prop
        fair = devig2(p.over, p.under)[0 if s.side == "over" else 1]
        st = stake_for(s, bankroll)
        out.append(f"{i:>2}. {s.label:<12}{p.game.kick_local.strftime('%a %I:%M%p').lower():<12}{p.game.short:<12}"
                   f"{s.what:<34} {ce.fmt_ml(s.price):>5} @{p.book:<10} proj {p.mean:.2f} → model {100 * s.truth_p:.0f}% "
                   f"vs fair {100 * fair:.0f}% (+{s.edge:.0f}%) " + (f"${st:.0f} " if st else "") + s.note)
    return "\n".join(out)


def _lock_row(s: Signal) -> tuple[str, str]:
    p = s.prop
    pr = side_probs(s)
    ev = pr["blend"] * ce.american_to_decimal(s.price) - 1.0
    tag = "agree" if s.kind == "agree" else s.label
    return (f"{s.what} {ce.fmt_ml(s.price)} @{p.book}",
            f"proj {p.mean:.2f} → model {100 * pr['model']:.0f}% · fair {100 * pr['market']:.0f}% · "
            f"blend {100 * pr['blend']:.0f}% (EV {100 * ev:+.1f}% at the blend, {tag})")


def render_lock(props: list[Prop]) -> str:
    lock, good = lock_and_good(props)
    if not lock and not good:
        return "no lock today: nothing on the agreement or value boards"
    out = ["The lock, and five good ones (paper only)"]
    for tag, s in ([("LOCK", lock)] if lock else []) + [(f"good {i}", s) for i, s in enumerate(good, 1)]:
        play, why = _lock_row(s)
        out.append(f"{tag:<7}{s.prop.game.kick_local.strftime('%I:%M%p').lower():<9}{s.prop.game.short:<12}{play:<48} {why}")
    return "\n".join(out + ([lock_odds_line(lock)] if lock else []) + [""] + sim_lines(([lock] if lock else []) + good))


def lock_odds_line(lock: Signal) -> str:
    """What a lock at this chance does over a week: the blend says how often it misses, not whether it will."""
    p = side_probs(lock)["blend"]
    return (f"At the blend's {100 * p:.0f}%, a lock like this misses about {round(10 * (1 - p))} nights in 10; "
            f"the chance of at least one miss in a five-night week is {100 * (1 - p ** 5):.0f}%.")


def sim_lines(card: list[Signal], md: bool = False) -> list[str]:
    """The card simulation three times: if the model is right, the blend, and the market."""
    sims = [x for x in (simulate_card(card, src) for src in ("model", "blend", "market")) if x]
    if not sims:
        return []
    n = sims[0]["tickets"]
    if md:
        out = [f"| If this is right | Exp. hits of {n} | P(all {n}) | P(≥{n - 1}) | $1 each: exp. | P(up) | 5th–95th pct | "
               f"{n}-leg parlay +{100 * (sims[0]['parlay_dec'] - 1):.0f}: EV |", "|---|---|---|---|---|---|---|---|"]
        for x in sims:
            out.append(f"| {x['source']} | {x['exp_hits']:.2f} | {100 * x['p_all']:.1f}% | {100 * (x['dist'][-1] + x['dist'][-2]):.0f}% | "
                       f"{x['exp_profit']:+.2f} | {100 * x['p_profit']:.0f}% | {x['p5']:+.2f} to {x['p95']:+.2f} | "
                       f"{100 * x['parlay_ev']:+.0f}% |")
        return out
    out = [f"Simulated {sims[0]['n']:,} nights of these {n} (teammates correlated, flat $1 each):"]
    for x in sims:
        out.append(f"  if the {x['source']:<6} is right: {x['exp_hits']:.2f} hits · P(all {n}) {100 * x['p_all']:.1f}% · "
                   f"exp {x['exp_profit']:+.2f} · P(up) {100 * x['p_profit']:.0f}% · 5–95% {x['p5']:+.2f}..{x['p95']:+.2f} · "
                   f"{n}-leg parlay EV {100 * x['parlay_ev']:+.0f}%")
    return out


def render_projections(props: list[Prop], n: int = 40) -> str:
    ps = sorted([p for p in props if p.mean is not None], key=lambda p: (p.game.kick_local, p.player.team, -p.mean))[:n]
    out = [f"{'Game':<12}{'Player':<26}{'Pos':<4}{'Market':<6}{'Line':>6}{'Proj':>7}{'P(over)':>9}{'Over/Under':>13}  Book"]
    for p in ps:
        out.append(f"{p.game.short:<12}{p.player.name[:25]:<26}{p.player.position:<4}{MARKETS[p.market][2]:<6}{p.line:>6g}"
                   f"{p.mean:>7.2f}{100 * (p.p_over or 0):>8.0f}%{ce.fmt_ml(p.over) + '/' + ce.fmt_ml(p.under):>13}  {p.book}")
    return "\n".join(out)


def report_path(date: dt.date) -> str:
    return os.path.join(REPORTS_DIR, f"nhl-{date.strftime('%A').lower()}-{date.isoformat()}.md")


def write_report(games: list[GameCtx], props: list[Prop], bankroll: float, date: dt.date, now: dt.datetime,
                 paper_summary: str, source: str) -> str:
    os.makedirs(REPORTS_DIR, exist_ok=True)
    path = report_path(date)
    sigs = ranked_signals(props)
    L = [f"# NHL Prop Report — {date.strftime('%A, %B %d, %Y')}", "",
         f"**Generated:** {now.strftime('%Y-%m-%d %I:%M %p %Z')}  ", f"**{ce.stakes_banner()}**  ",
         f"**Slate:** {len(games)} games · {len(props)} prop lines matched to rostered players ({source})  ",
         f"**Model (skaters, since 2026-09-30):** per-minute rate × projected minutes. The rate is this season's "
         f"stat per minute blended with last season's (weight a1) and regressed toward the position mean (K ghost "
         f"minutes: shots {SKATER_MODEL['shots'][1]:g}, points {SKATER_MODEL['points'][1]:g}, goals "
         f"{SKATER_MODEL['goals'][1]:g}); minutes lean {TOI_RECENT_W:.0%} on the last {TOI_RECENT_GAMES} games. "
         f"× opponent allowance^β × home/away split → Poisson P(over) (shots: gamma-Poisson k={DISPERSION['shots']:g}; "
         f"goalie saves: old per-start recipe, k={DISPERSION['saves']:g}). Fit on 2024-25, tested on every 2025-26 "
         f"skater-game: better log-loss than the old recipe at every line of every stat. Tiers +{EDGE_PCT:g}% / "
         f"+{EDGE_STRONG_PCT:g}%, ≥ +{EDGE_OVERREACH_PCT:g}% demoted (⚠overreach).",
         "", "## The lock, and five good ones", "",
         f"**The lock** is the top of the agreement board: the prop side the projection and the de-vigged "
         f"line both favour, priced {AGREE_MIN_PRICE}..{AGREE_MAX_PRICE}, model above fair by no more than "
         f"+{AGREE_MAX_GAP_PCT:g}%, ranked by the **blend** ({BLEND_MODEL_W:.0%} model, {1 - BLEND_MODEL_W:.0%} "
         "de-vigged line, in logit space: the market has been sharper everywhere so far). **Good** is the rest "
         "of that board, then the ranked value props (§1), one per player. EV is at the blend; at "
         "−220..−250 the juice usually outweighs what the model adds, so these are the likeliest winners, "
         "not value bets. Paper only.", "",
         "| | Puck (CT) | Game | Play | Why |", "|---|---|---|---|---|"]
    lock, good = lock_and_good(props)
    for tag, s in ([("**LOCK**", lock)] if lock else []) + [(f"good {i}", s) for i, s in enumerate(good, 1)]:
        play, why = _lock_row(s)
        L.append(f"| {tag} | {s.prop.game.kick_local.strftime('%I:%M %p').lstrip('0')} | {s.prop.game.short} | "
                 f"{'**' + play + '**' if s is lock else play} | {why} |")
    if not lock and not good:
        L.append("| — | — | — | nothing clears either board today | |")
    if lock:
        L += ["", lock_odds_line(lock)]
    card = ([lock] if lock else []) + good
    if card:
        L += ["", f"### Simulated {SIM_N:,} nights of that card", "",
              "Each ticket keeps its own chance to cash; the simulation adds how they move together "
              f"(teammates share a game-level factor, latent ρ {TEAM_RHO['points']:g} points / "
              f"{TEAM_RHO['assists']:g} assists, measured on 2025-26 logs; opponents independent). Run three "
              f"times: trusting the model, the blend ({BLEND_MODEL_W:.0%} model), and the de-vigged market. Flat $1 "
              "a ticket; the parlay column is all legs in one ticket at the product of the prices.", ""]
        L += sim_lines(card, md=True)
    L += ["", "## 1. Ranked props", "",
         "| # | Tag | Game | Play | Price | Book | Proj | Model vs fair | $Bet (paper) | Flags |", "|---|---|---|---|---|---|---|---|---|---|"]
    for i, s in enumerate(sigs, 1):
        p = s.prop
        fair = devig2(p.over, p.under)[0 if s.side == "over" else 1]
        st = stake_for(s, bankroll)
        L.append(f"| {i} | **{s.label}** | {p.game.short} | {s.what} | {ce.fmt_ml(s.price)} | {p.book} | {p.mean:.2f} | "
                 f"{100 * s.truth_p:.0f}% vs {100 * fair:.0f}% (+{s.edge:.0f}%) | {f'${st:.0f}' if st else '—'} | {s.note or '—'} |")
    if not sigs:
        L.append("| — | — | — | no flagged props | | | | | | |")
    L += ["", "## 2. Projections (first 40 by game)", "", "```", render_projections(props), "```", "",
          "## 3. NHL paper ledger to date", "", "```", paper_summary, "```", "",
          "> Paper only. The projection is tested walk-forward (fit on 2024-25, scored on every 2025-26 game: "
          "`--calibrate`, `analysis/06`), but no historical prop prices exist, so ROI against posted lines is "
          "untested until the ledger fills. The ledger above is that evidence."]
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")
    return path


# =====================================================================
# ---- main ----
# =====================================================================

def main(argv: Optional[list[str]] = None) -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    p = argparse.ArgumentParser(description="NHL player-prop outlier finder — projections vs the posted line")
    p.add_argument("--date", help="YYYY-MM-DD (default: today, America/Chicago)")
    p.add_argument("--bankroll", type=float, default=100.0)
    p.add_argument("--db", default=NHL_DB)
    p.add_argument("--build", action="store_true", help="rosters + game logs for both seasons -> nhl.db (~2 min)")
    p.add_argument("--calibrate", action="store_true", help="walk-forward test of the projection on last season")
    p.add_argument("--lines-file", help="CSV of prop lines (player,market,line,over,under[,book[,game]]) instead of the Odds API")
    p.add_argument("--markets", default=",".join(MARKETS), help="comma-separated Odds API markets to pull")
    p.add_argument("--top", type=int, default=15)
    p.add_argument("--projections", action="store_true", help="print the projection table (no lines needed)")
    p.add_argument("--snapshot", action="store_true", help="persist lines + projections, paper-log flagged props")
    p.add_argument("--report", action="store_true", help="write reports/nhl-<weekday>-<date>.md")
    p.add_argument("--settle", action="store_true", help="grade pending paper props from boxscores")
    p.add_argument("--paper-show", action="store_true")
    a = p.parse_args(argv)

    now = dt.datetime.now(LOCAL_TZ)
    date = dt.date.fromisoformat(a.date) if a.date else now.date()
    conn = db_connect(a.db)
    if a.paper_show:
        print(db_paper_summary(conn))
        return 0
    if a.build:
        print(f"building nhl.db: rosters for {SEASON} + game logs {PRIOR_SEASON} and {SEASON} …")
        n = build_logs(conn)
        print(f"stored {n:,} game-log rows")
        return 0
    if a.calibrate:
        calibrate(conn)
        return 0
    if a.settle:
        n, staked, profit = db_settle(conn)
        print(f"settled {n} paper props: staked {staked:.2f}, profit {profit:+.2f}")
        print(db_paper_summary(conn))
        return 0

    games = fetch_schedule(date)
    if not games:
        print(f"no NHL regular-season games on {date} (season opens {SEASON_START})")
        return 0
    players = db_players(conn)
    if not players:
        print("nhl.db has no players — run --build first", file=sys.stderr)
        return 1
    print(f"{len(games)} games on {date}: " + ", ".join(g.short for g in games), file=sys.stderr)
    sp = fetch_team_summary(PRIOR_SEASON)
    try:
        sc = fetch_team_summary(SEASON)
    except requests.HTTPError:
        sc = {}
    for g in games:
        g.home_factor, g.away_factor = opponent_factors(sp, sc, g.home, g.away)
    pm = position_means(conn)
    for g in games:
        for pl in players.get(g.home, []) + players.get(g.away, []):
            pl.rates, pl.games = player_rates(conn, pl.id, date, pl.position, pm)

    rows, source = [], "no lines"
    if a.lines_file:
        rows, source = read_props_csv(a.lines_file, games), f"csv {a.lines_file}"
    else:
        key = load_key()
        if key:
            rows, source = fetch_props_oddsapi(key, games, log=lambda m: print(m, file=sys.stderr)), "The Odds API"
        else:
            print("no ODDS_API_KEY (env or .env) and no --lines-file: DraftKings via ESPN", file=sys.stderr)
            rows, source = fetch_props_espn(games, date, log=lambda m: print(m, file=sys.stderr)), "DraftKings via ESPN"
    props = attach_props(rows, games, players)
    for pr in props:
        project(pr)
    print(f"{len(rows)} prop sides fetched · {len(props)} matched to rostered players · source: {source}", file=sys.stderr)

    if a.projections or not props:
        # synthesize lines at the market-typical number so projections print even with no book
        synth = []
        for g in games:
            for pl in players.get(g.home, []) + players.get(g.away, []):
                for market, (stat, who, _) in MARKETS.items():
                    if (who == "goalie") != (pl.position == "G") or stat not in pl.rates:
                        continue
                    line = {"shots": 2.5, "points": 0.5, "goals": 0.5, "assists": 0.5, "blocked": 1.5,
                            "pp_points": 0.5, "saves": 27.5}[stat]
                    pr = Prop(g, pl, market, stat, line, None, None, "proj")
                    project(pr)
                    synth.append(pr)
        print(render_projections(synth, n=60))
        if not props:
            print("\n" + ce.stakes_banner())
    if props:
        print(render_top(props, a.bankroll, a.top))
        print("\n" + render_lock(props))
    if a.snapshot and props:
        n = db_persist(conn, games, props, now)
        k = db_paper_log(conn, ranked_signals(props) + agree_board(props), a.bankroll, now)
        print(f"snapshot: {n} prop rows, {k} new paper plays → {a.db}")
    if a.report:
        path = write_report(games, props, a.bankroll, date, now, db_paper_summary(conn), source)
        print(f"\nreport → {path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

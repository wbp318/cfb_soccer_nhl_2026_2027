"""Shared loader for the NHL half of analysis/ (reads nhl.db, never writes).

    from _shared.load_nhl import load_nhl_bets, load_game_logs, load_logs, load_market_lines
    bets  = load_nhl_bets()            # one row per settled NHL paper prop
    logs  = load_game_logs(season)     # every stored game-log row for a season, chronological
    both  = load_logs(seasons)         # several seasons, with each player's position (for the backtest)
    lines = load_market_lines()        # every snapshotted prop line a game log has settled (last snapshot per book)

Mirrors load_nhl.R — keep them in lockstep. CFB_NHL_DB overrides the path (CI).
"""
from __future__ import annotations

import os
import sqlite3
import sys
from pathlib import Path

import numpy as np
import pandas as pd

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DEFAULT_DB = Path(os.environ.get("CFB_NHL_DB") or Path(__file__).resolve().parents[2] / "nhl.db")

_BETS_SQL = """
SELECT p.id, p.game_id, g.date, p.player_id, pl.name, pl.position, p.kind, p.market, p.side, p.line, p.price,
       p.truth_p, p.edge, p.strength, p.stake, p.book, p.actual, p.result, p.profit,
       COALESCE(p.model, '2026-09-20') AS model
FROM paper_bets p
JOIN games g ON g.id = p.game_id
LEFT JOIN players pl ON pl.id = p.player_id
WHERE p.result IS NOT NULL
"""

_LOGS_SQL = """
SELECT game_id, player_id, season, date, team, opp, home, shots, points, goals, assists, blocked,
       pp_points, saves, shots_against, started, toi
FROM game_logs WHERE season = ? ORDER BY player_id, date, game_id
"""

_LOGS_POS_SQL = """
SELECT l.game_id, l.player_id, l.season, l.date, l.team, l.opp, l.home, l.shots, l.points, l.goals, l.assists,
       l.blocked, l.pp_points, l.saves, l.shots_against, l.started, l.toi, pl.position
FROM game_logs l LEFT JOIN players pl ON pl.id = l.player_id
WHERE l.season IN ({}) ORDER BY l.player_id, l.date, l.game_id
"""

# last snapshot per (game, player, market, line, book); settled = the player has a game log for that game
_LINES_SQL = """
SELECT p.game_id, p.player_id, p.market, p.line, p.book, p.over, p.under, p.p_over,
       COALESCE(p.model, '2026-09-20') AS model,
       l.shots, l.points, l.goals, l.assists, l.pp_points, l.blocked, l.saves
FROM props p
JOIN (SELECT game_id, player_id, market, line, book, MAX(taken_at) AS t
      FROM props GROUP BY game_id, player_id, market, line, book) last
  ON last.game_id = p.game_id AND last.player_id = p.player_id AND last.market = p.market
 AND last.line = p.line AND last.book = p.book AND last.t = p.taken_at
JOIN game_logs l ON l.game_id = p.game_id AND l.player_id = p.player_id
WHERE p.over IS NOT NULL AND p.under IS NOT NULL AND p.p_over IS NOT NULL
ORDER BY p.game_id, p.player_id, p.market, p.line, p.book
"""
MARKET_STAT = {"player_shots_on_goal": "shots", "player_points": "points", "player_goals": "goals",
               "player_assists": "assists", "player_power_play_points": "pp_points",
               "player_blocked_shots": "blocked", "player_total_saves": "saves"}


def _read(sql: str, db_path, params=()) -> pd.DataFrame:
    con = sqlite3.connect(str(db_path))
    try:
        return pd.read_sql_query(sql, con, params=params)
    finally:
        con.close()


def _dec(price: pd.Series) -> np.ndarray:
    p = price.astype(float)
    return np.where(p > 0, 1 + p / 100.0, 1 + 100.0 / p.abs())


def _implied(price: pd.Series) -> np.ndarray:
    return 1.0 / _dec(price)


def load_nhl_bets(db_path=DEFAULT_DB) -> pd.DataFrame:
    df = _read(_BETS_SQL, db_path)
    df["pnl_flat"] = np.where(df.result == "W", _dec(df.price) - 1.0, np.where(df.result == "L", -1.0, 0.0))
    return df


def load_game_logs(season: int, db_path=DEFAULT_DB) -> pd.DataFrame:
    return _read(_LOGS_SQL, db_path, (int(season),))


def load_logs(seasons, db_path=DEFAULT_DB) -> pd.DataFrame:
    seasons = [int(s) for s in seasons]
    return _read(_LOGS_POS_SQL.format(",".join("?" * len(seasons))), db_path, tuple(seasons))


def load_market_lines(db_path=DEFAULT_DB) -> pd.DataFrame:
    """One row per settled line: stored model P(over), de-vigged market P(over) (multiplicative), outcome y.
    Pushes (actual == line) and markets with no stat in the game log are dropped."""
    df = _read(_LINES_SQL, db_path)
    df["stat"] = df.market.map(MARKET_STAT)
    df = df[df.stat.notna()].copy()
    df["actual"] = [row[s] for row, s in zip(df.to_dict("records"), df.stat)]
    df = df[df.actual.notna() & (df.actual != df.line)].copy()
    io, iu = _implied(df.over), _implied(df.under)
    df["p_market"] = io / (io + iu)
    df["y"] = (df.actual > df.line).astype(float)
    return df.reset_index(drop=True)

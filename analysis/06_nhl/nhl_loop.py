"""The NHL prop analysis loop: is the projection any good, and does betting it against posted lines make money?

  A. Paper ROI by kind (prop = value board, agree = the lock board), then value props by market x side x
     strength, flat $1, bootstrap 95% CI.
  B. Slices a rule can act on: edge band, market, side (Wilson CI on hit, flat ROI).
  C. The projection backtest. Every PRIOR_SEASON skater-game (and goalie start) projected walk-forward from
     HISTORY_SEASON + that season's earlier games, as nhl_edge.backtest does it: the live recipe (per-minute
     rate regressed to the position mean x projected minutes x opponent^beta x home/away split; gamma-Poisson
     for shots), the 2026-09-20 recipe it replaced (per-game mean shrunk to last season, recent-10 tilt,
     clamped opponent x 1.02 at home, Poisson) and a naive position average, scored at the lines books hang.
     Reliability bins, the dispersion grid, and an ablation (each piece of the recipe switched off) at the
     main line: the evidence behind SKATER_MODEL, TOI_* and DISPERSION.
  D. Same-game correlation of skater outcomes (teammates, opponents) -> nhl_edge.TEAM_RHO.
  E. Model vs market on every snapshotted line a game log has settled: log-loss and bias of the stored
     projection vs the de-vigged price, by recipe version (props.model) and market, plus the logit blend
     curve -> the evidence for nhl_edge.BLEND_MODEL_W.

Output: analysis/_out/nhl_roi.csv, nhl_slices.csv, nhl_backtest.csv, nhl_calibration.csv, nhl_grid.csv,
nhl_correlation.csv, nhl_market.csv (nhl_grid: score = log-loss for k / ablation rows, the
ratio for home/away rows). Mirrors nhl_loop.R — keep in lockstep. Point estimates must match;
bootstrap CIs may differ in the last digit.
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from _shared.load_data import wilson
from _shared.load_nhl import load_game_logs, load_logs, load_market_lines, load_nhl_bets

OUT_DIR = Path(__file__).resolve().parents[1] / "_out"
MIN_BETS = 10
MIN_N = 5
BOOT_REPS = 5000
SEED = 20261007

# mirror nhl_edge.py — a change there must be reflected here (and in nhl_loop.R)
PRIOR_SEASON = 20252026
HISTORY_SEASON = 20242025
TOI_PRIOR_W, TOI_GHOST, TOI_RECENT_W, TOI_RECENT_GAMES = 0.09, 0.6, 0.56, 5
SKATER_MODEL = {"shots": (0.35, 86.0, 0.84, 1.037), "points": (0.58, 234.0, 0.70, 1.078),
                "goals": (0.81, 694.0, 0.64, 1.077), "assists": (0.58, 355.0, 0.73, 1.078),
                "pp_points": (0.31, 50.0, 0.59, 1.115)}          # a1, K ghost minutes, beta, h
STATS = list(SKATER_MODEL)
DISPERSION = {"saves": 20.0, "shots": 17.5}
DISPERSION_GRID = [None, 50.0, 20.0, 12.0, 8.0, 5.0, 3.0, 2.0]
OPP_LO, OPP_HI = 0.80, 1.20
TEAM_PRIOR_GAMES = 20.0                                          # opponent_factors: weight gp / (gp + 20)
SHRINK_GAMES, RECENT_GAMES, RECENT_WEIGHT = 20.0, 10, 0.35       # goalies, and the 2026-09-20 skater recipe
OLD_HOME = 1.02                                                  # 2026-09-20 recipe: home bump, home only
CAL_LINES = {"shots": [1.5, 2.5, 3.5], "points": [0.5, 1.5], "goals": [0.5], "assists": [0.5], "pp_points": [0.5],
             "saves": [24.5, 27.5]}
CAL_MAIN = {"shots": 2.5, "points": 0.5, "goals": 0.5, "assists": 0.5, "pp_points": 0.5, "saves": 27.5}
CAL_MIN_GAMES, CAL_MIN_TOI, CAL_EARLY = 20, 12.0, 10
BLEND_GRID = [0.0, 0.25, 0.5, 0.75, 1.0]

EDGE_BINS, EDGE_LABELS = [0, 8, 15, 30, 50, 100000], ["0-8", "8-15", "15-30", "30-50", "50+"]


def verdict(lo: float, hi: float) -> str:
    return "PROFITABLE (95% CI > 0)" if lo > 0 else "losing (95% CI < 0)" if hi < 0 else "inconclusive"


def boot_ci(x: np.ndarray, rng: np.random.Generator) -> tuple[float, float]:
    idx = rng.integers(0, len(x), size=(BOOT_REPS, len(x)))
    means = x[idx].mean(axis=1)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def cdf(k: int, lam: np.ndarray, disp: float | None = None) -> np.ndarray:
    """P(X <= k), vectorised: Poisson(lam), or gamma-Poisson (negative binomial) with shape disp."""
    lam = np.asarray(lam, dtype=float)
    if k < 0:
        return np.zeros_like(lam)
    if disp is None:
        term = np.exp(-lam)
        tot = term.copy()
        for i in range(1, k + 1):
            term = term * lam / i
            tot = tot + term
    else:
        q = lam / (disp + lam)
        term = (1.0 - q) ** disp
        tot = term.copy()
        for i in range(k):
            term = term * (i + disp) / (i + 1) * q
            tot = tot + term
    return np.minimum(1.0, tot)


def p_over(lam, line: float, disp: float | None = None) -> np.ndarray:
    return 1.0 - cdf(math.floor(line), lam, disp)


def logloss(p, y) -> np.ndarray:
    p = np.clip(np.asarray(p, dtype=float), 1e-6, 1 - 1e-6)
    y = np.asarray(y, dtype=float)
    return -(y * np.log(p) + (1 - y) * np.log(1 - p))


# ---------------------------------------------------------------- A + B (ledger)

def section_a(bets: pd.DataFrame, rng) -> pd.DataFrame:
    print(f"A. Paper ROI — {len(bets):,} settled NHL paper props, flat ROI {100 * bets.pnl_flat.mean():+.1f}%\n")
    groups = [("ALL", "all", "all", bets)]
    groups += [(f"kind:{k}", "all", "all", g) for k, g in bets.groupby("kind")]
    groups += [(f"recipe:{m}", "all", "all", g) for m, g in bets.groupby("model")]
    props = bets[bets["kind"] == "prop"]        # the value board; the agree board is its own bucket above
    groups += [(m, s, str(st), g) for (m, s, st), g in props.groupby(["market", "side", "strength"])]
    groups += [(m, "any", "any", g) for m, g in props.groupby("market")]
    groups += [("ALL", s, "any", g) for s, g in props.groupby("side")]
    rows = []
    for market, side, strength, g in groups:
        if len(g) < MIN_BETS:
            continue
        lo, hi = boot_ci(g.pnl_flat.to_numpy(), rng)
        rows.append({"market": market, "side": side, "strength": strength, "bets": len(g),
                     "wins": int((g.result == "W").sum()), "hit_rate": float((g.result == "W").mean()),
                     "roi_mean": float(g.pnl_flat.mean()), "roi_ci_lo": lo, "roi_ci_hi": hi, "verdict": verdict(lo, hi)})
    out = pd.DataFrame(rows).sort_values("roi_ci_lo", ascending=False)
    print(f"  {'market':<26}{'side':<6}{'str':>4}{'bets':>6}{'wins':>6}{'hit%':>7}{'ROI':>8}{'CI lo':>8}{'CI hi':>8}  verdict")
    for r in out.itertuples():
        print(f"  {r.market:<26}{r.side:<6}{r.strength:>4}{r.bets:>6}{r.wins:>6}{100 * r.hit_rate:>6.1f}%{100 * r.roi_mean:>+7.1f}%"
              f"{100 * r.roi_ci_lo:>+7.1f}%{100 * r.roi_ci_hi:>+7.1f}%  {r.verdict}")
    return out


def slice_table(df: pd.DataFrame, col: str, order: list[str], title: str) -> list[dict]:
    rows = []
    print(f"\n{title}")
    print(f"  {'bucket':<26}{'n':>5}{'W':>5}{'hit%':>8}{'ROI':>8}   95% CI on hit")
    for key in [k for k in order if k in set(df[col])]:
        g = df[df[col] == key]
        if len(g) < MIN_N:
            continue
        w = int((g.result == "W").sum())
        p, lo, hi = wilson(w, len(g) - int((g.result == "P").sum()))
        rows.append({"dimension": col, "bucket": key, "n": len(g), "wins": w, "hit_rate": p, "hit_lo": lo, "hit_hi": hi,
                     "roi_flat": float(g.pnl_flat.mean())})
        print(f"  {key:<26}{len(g):>5}{w:>5}{100 * p:>7.1f}%{100 * g.pnl_flat.mean():>+7.1f}%   [{100 * lo:.0f}, {100 * hi:.0f}]")
    return rows


def section_b(bets: pd.DataFrame) -> pd.DataFrame:
    b = bets[bets.strength >= 1].copy()
    b["edge_band"] = pd.cut(b.edge, EDGE_BINS, labels=EDGE_LABELS, right=False).astype(str)
    rows = slice_table(b, "edge_band", EDGE_LABELS, "B1. by edge band (does a bigger projection-vs-line gap win more?)")
    rows += slice_table(b, "market", sorted(b.market.unique()), "B2. by market")
    rows += slice_table(b, "side", ["over", "under"], "B3. by side")
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- C (projection backtest)

def _prev_sum(df: pd.DataFrame, col: str, k: int | None) -> np.ndarray:
    """Per player (rows sorted player, date, game): sum of the previous k values of col (all previous if k is None)."""
    cs = df.groupby("player_id", sort=False)[col].cumsum()
    before = cs - df[col]
    if k is None:
        return before.to_numpy()
    lag = cs.groupby(df["player_id"], sort=False).shift(k + 1).fillna(0.0)
    return (before - lag).to_numpy()


def _team_table(sk: pd.DataFrame) -> tuple[pd.DataFrame, dict, dict]:
    """Per team-game of PRIOR_SEASON: the team's shots for / shots against / goals against as they stood before that
    game (blended with HISTORY_SEASON at gp / (gp + 20), as nhl_edge.opponent_factors does). Plus league averages."""
    tg = (sk.groupby(["season", "game_id", "team"], sort=True)
            .agg(date=("date", "first"), sf=("shots", "sum"), gf=("goals", "sum")).reset_index())
    tg = tg[tg.groupby(["season", "game_id"]).team.transform("size") == 2]
    opp = tg[["season", "game_id", "team", "sf", "gf"]].rename(columns={"team": "opp", "sf": "sa", "gf": "ga"})
    tg = tg.merge(opp, on=["season", "game_id"])
    tg = tg[tg.team != tg.opp]
    prior = tg[tg.season == HISTORY_SEASON].groupby("team").agg(sf_p=("sf", "mean"), sa_p=("sa", "mean"), ga_p=("ga", "mean"))
    avg = {k: float(prior[f"{k}_p"].mean()) for k in ("sf", "sa", "ga")}
    cur = tg[tg.season == PRIOR_SEASON].sort_values(["team", "date", "game_id"]).reset_index(drop=True)
    g = cur.groupby("team", sort=False)
    cur["n_before"] = g.cumcount()
    for k in ("sf", "sa", "ga"):
        cur[f"{k}_before"] = g[k].cumsum() - cur[k]
    cur = cur.merge(prior, left_on="team", right_index=True, how="left")
    w = cur.n_before / (cur.n_before + TEAM_PRIOR_GAMES)
    for k in ("sf", "sa", "ga"):
        cm = cur[f"{k}_before"] / cur.n_before.where(cur.n_before > 0)
        p = cur[f"{k}_p"]
        hat = np.where(cur.n_before > 0, np.where(p.notna(), w * cm + (1 - w) * p, cm), p)
        cur[f"{k}_hat"] = np.where(np.isnan(hat) | (hat == 0), avg[k], hat)
    return cur[["game_id", "team", "sf_hat", "sa_hat", "ga_hat"]], avg, prior


def _clamp(x):
    return np.clip(x, OPP_LO, OPP_HI)


def skater_frame(logs: pd.DataFrame) -> tuple[pd.DataFrame, dict, pd.DataFrame, dict]:
    sk = logs[logs.position.isin(["C", "L", "R", "D"]) & logs.toi.notna() & logs.shots.notna()].copy()
    sk["grp"] = np.where(sk.position == "D", "D", "F")
    hist = sk[sk.season == HISTORY_SEASON]
    pm = {}
    for grp, d in hist.groupby("grp"):
        pm[grp] = {"toi": d.toi.sum() / len(d), **{s: d[s].sum() / d.toi.sum() for s in STATS}}
    team, avg, _ = _team_table(sk)
    agg = hist.groupby("player_id").agg(n_p=("toi", "size"), toi_p=("toi", "sum"), **{f"{s}_p": (s, "sum") for s in STATS})
    cur = sk[sk.season == PRIOR_SEASON].sort_values(["player_id", "date", "game_id"]).reset_index(drop=True)
    cur["n_c"] = cur.groupby("player_id", sort=False).cumcount()
    cur["toi_c"] = _prev_sum(cur, "toi", None)
    cur["toi_r"] = _prev_sum(cur, "toi", TOI_RECENT_GAMES) / np.minimum(cur.n_c, TOI_RECENT_GAMES).where(cur.n_c > 0)
    for s in STATS:
        cur[f"{s}_c"] = _prev_sum(cur, s, None)
        cur[f"{s}_r10"] = _prev_sum(cur, s, RECENT_GAMES)
    cur = cur.merge(agg, left_on="player_id", right_index=True, how="inner")
    cur = cur[(cur.n_p >= CAL_MIN_GAMES) & (cur.toi_p / cur.n_p >= CAL_MIN_TOI)]
    cur = cur.merge(team.rename(columns={"team": "opp"}), on=["game_id", "opp"], how="inner")
    cur = cur.sort_values(["player_id", "date", "game_id"]).reset_index(drop=True)
    return cur, pm, team, avg


def lam_live(d: pd.DataFrame, pm: dict, avg: dict, stat: str, K_mult: float = 1.0, beta_on: bool = True,
             home_on: bool = True, recent_on: bool = True) -> np.ndarray:
    a1, K, beta, h = SKATER_MODEL[stat]
    K = K * K_mult
    mu_toi = d.grp.map({g: v["toi"] for g, v in pm.items()}).to_numpy()
    mu_s = d.grp.map({g: v[stat] for g, v in pm.items()}).to_numpy()
    base = (d.toi_c + TOI_PRIOR_W * d.toi_p + TOI_GHOST * mu_toi) / (d.n_c + TOI_PRIOR_W * d.n_p + TOI_GHOST)
    rw = TOI_RECENT_W if recent_on else 0.0
    toi = np.where(d.n_c > 0, (1 - rw) * base + rw * d.toi_r.fillna(0.0), base)
    rate = (d[f"{stat}_c"] + a1 * d[f"{stat}_p"] + K * mu_s) / (d.toi_c + a1 * d.toi_p + K)
    allow = _clamp(d.sa_hat / avg["sa"]) if stat == "shots" else _clamp(d.ga_hat / avg["ga"])
    fac = (allow ** beta if beta_on else 1.0) * (np.where(d.home == 1, math.sqrt(h), 1 / math.sqrt(h)) if home_on else 1.0)
    return (rate * toi * fac).to_numpy(dtype=float)


def lam_old(d: pd.DataFrame, avg: dict, stat: str) -> np.ndarray:
    prior_mean = d[f"{stat}_p"] / d.n_p
    cur_mean = np.where(d.n_c > 0, d[f"{stat}_c"] / d.n_c.where(d.n_c > 0), prior_mean)
    w = d.n_c / (d.n_c + SHRINK_GAMES)
    base = w * cur_mean + (1 - w) * prior_mean
    nr = np.minimum(d.n_c, RECENT_GAMES)
    base = np.where(nr >= 5, (1 - RECENT_WEIGHT) * base + RECENT_WEIGHT * d[f"{stat}_r10"] / nr.where(nr > 0), base)
    allow = _clamp(d.sa_hat / avg["sa"]) if stat == "shots" else _clamp(d.ga_hat / avg["ga"])
    return (base * allow * np.where(d.home == 1, OLD_HOME, 1.0)).to_numpy(dtype=float)


def goalie_frame(logs: pd.DataFrame, team: pd.DataFrame, avg: dict) -> tuple[pd.DataFrame, float]:
    g = logs[(logs.position == "G") & (logs.started == 1) & logs.saves.notna()].copy()
    hist = g[g.season == HISTORY_SEASON]
    naive = float(hist.saves.mean()) if len(hist) else 27.0
    agg = hist.groupby("player_id").agg(n_p=("saves", "size"), sv_p=("saves", "sum"))
    cur = g[g.season == PRIOR_SEASON].sort_values(["player_id", "date", "game_id"]).reset_index(drop=True)
    cur["n_c"] = cur.groupby("player_id", sort=False).cumcount()
    cur["sv_c"] = _prev_sum(cur, "saves", None)
    cur["sv_r10"] = _prev_sum(cur, "saves", RECENT_GAMES)
    cur = cur.merge(agg, left_on="player_id", right_index=True, how="inner")
    cur = cur[cur.n_p >= CAL_MIN_GAMES]
    cur = cur.merge(team.rename(columns={"team": "opp"}), on=["game_id", "opp"], how="inner")
    cur = cur.sort_values(["player_id", "date", "game_id"]).reset_index(drop=True)
    prior_mean = cur.sv_p / cur.n_p
    cur_mean = np.where(cur.n_c > 0, cur.sv_c / cur.n_c.where(cur.n_c > 0), prior_mean)
    w = cur.n_c / (cur.n_c + SHRINK_GAMES)
    base = w * cur_mean + (1 - w) * prior_mean
    nr = np.minimum(cur.n_c, RECENT_GAMES)
    base = np.where(nr >= 5, (1 - RECENT_WEIGHT) * base + RECENT_WEIGHT * cur.sv_r10 / nr.where(nr > 0), base)
    cur["lam"] = base * _clamp(cur.sf_hat / avg["sf"])
    return cur, naive


def section_c(logs: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    sk, pm, team, avg = skater_frame(logs)
    lines_rows, bin_rows, grid_rows = [], [], []
    if sk.empty:
        print(f"\nC. no {HISTORY_SEASON} + {PRIOR_SEASON} skater logs — run nhl_edge.py --build (it stores both seasons)")
        return pd.DataFrame(lines_rows), pd.DataFrame(bin_rows), pd.DataFrame(grid_rows)
    gl, naive_sv = goalie_frame(logs, team, avg)
    skl = logs[logs.position.isin(["C", "L", "R", "D"])]
    print("\nC0. Home/away ratio, Σ home ÷ Σ away over every skater-game (nhl_edge.SKATER_MODEL h = the pooled row)")
    for label, d in [(str(s_), g) for s_, g in skl.groupby("season")] + [("pooled", skl)]:
        ratios = {s: float(d.loc[d.home == 1, s].sum() / d.loc[d.home == 0, s].sum()) for s in STATS}
        grid_rows.extend({"stat": s, "line": float("nan"), "grid": "home/away", "value": label, "n": len(d), "score": v}
                         for s, v in ratios.items())
        print(f"  {label:<10}" + " · ".join(f"{s} {v:.4f}" for s, v in ratios.items()))
    print(f"\nC. Projection backtest — every {PRIOR_SEASON} game projected from {HISTORY_SEASON} + earlier games "
          f"(skaters ≥ {CAL_MIN_GAMES} games at ≥ {CAL_MIN_TOI:g} min the season before; goalies ≥ {CAL_MIN_GAMES} starts)")
    print(f"  {'stat':<10}{'line':>5}{'n':>8}{'live':>9}{'old':>9}{'naive':>9}{'live-old':>10}{'bias live':>11}{'bias old':>10}"
          f"{'early live':>12}{'early old':>11}")
    early = (sk.n_c < CAL_EARLY).to_numpy()
    for stat in STATS + ["saves"]:
        if stat == "saves":
            d, y = gl, gl.saves.to_numpy(dtype=float)
            lams = {"live": gl.lam.to_numpy(dtype=float)}
            lams_naive = np.full(len(gl), naive_sv)
            early_s = (gl.n_c < CAL_EARLY).to_numpy()
            if gl.empty:
                continue
        else:
            d, y = sk, sk[stat].to_numpy(dtype=float)
            lams = {"live": lam_live(sk, pm, avg, stat), "old": lam_old(sk, avg, stat)}
            lams_naive = sk.grp.map({g: v[stat] * v["toi"] for g, v in pm.items()}).to_numpy(dtype=float)
            early_s = early
        disp = DISPERSION.get(stat)
        for line in CAL_LINES[stat]:
            hit = (y > line).astype(float)
            res = {}
            for rec, lam in list(lams.items()) + [("naive", lams_naive)]:
                p = p_over(lam, line, disp if rec == "live" else None)
                ll = logloss(p, hit)
                res[rec] = (float(ll.mean()), float((p - hit).mean()), float(ll[early_s].mean()) if early_s.any() else float("nan"),
                            float((p - hit)[early_s].mean()) if early_s.any() else float("nan"))
                lines_rows.append({"stat": stat, "line": line, "recipe": rec, "n": len(y), "logloss": res[rec][0],
                                   "bias": res[rec][1], "n_early": int(early_s.sum()), "logloss_early": res[rec][2],
                                   "bias_early": res[rec][3]})
            old = res.get("old")
            o = ((f"{old[0]:>9.4f}", f"{res['live'][0] - old[0]:>+10.4f}", f"{old[1]:>+10.3f}", f"{old[2]:>11.4f}") if old
                 else (f"{'-':>9}", f"{'-':>10}", f"{'-':>10}", f"{'-':>11}"))
            print(f"  {stat:<10}{line:>5g}{len(y):>8,}{res['live'][0]:>9.4f}{o[0]}{res['naive'][0]:>9.4f}{o[1]}"
                  f"{res['live'][1]:>+11.3f}{o[2]}{res['live'][2]:>12.4f}{o[3]}")
        main = CAL_MAIN[stat]
        hit = (y > main).astype(float)
        p = p_over(lams["live"], main, disp)
        b = np.minimum(9, np.floor(p * 10)).astype(int)
        for k in sorted(set(b)):
            m = b == k
            bin_rows.append({"stat": stat, "line": main, "bin": f"{k / 10:.1f}-{(k + 1) / 10:.1f}", "n": int(m.sum()),
                             "pred": float(p[m].mean()), "obs": float(hit[m].mean())})
        for k in DISPERSION_GRID:
            grid_rows.append({"stat": stat, "line": main, "grid": "k", "value": "inf" if k is None else f"{k:g}", "n": len(y),
                              "score": float(logloss(p_over(lams["live"], main, k), hit).mean())})
        if stat != "saves":
            for name, kw in (("live", {}), ("K=0 (no regression)", {"K_mult": 0.0}), ("K x 0.5", {"K_mult": 0.5}),
                             ("K x 2", {"K_mult": 2.0}), ("beta=0 (no opponent)", {"beta_on": False}),
                             ("h=1 (no home split)", {"home_on": False}), ("no recent minutes", {"recent_on": False})):
                lam = lam_live(sk, pm, avg, stat, **kw)
                grid_rows.append({"stat": stat, "line": main, "grid": "ablation", "value": name, "n": len(y),
                                  "score": float(logloss(p_over(lam, main, disp), hit).mean())})
    bins = pd.DataFrame(bin_rows)
    print("\n  reliability of the live recipe at the main line (bins with n ≥ 50): predicted vs observed P(over)")
    for stat, g in bins.groupby("stat", sort=False):
        print(f"  {stat:<10}" + " · ".join(f"{r.bin}: {100 * r.pred:.0f}/{100 * r.obs:.0f}" for r in g.itertuples() if r.n >= 50))
    grid = pd.DataFrame(grid_rows)
    print("\n  dispersion k at the main line (log-loss; inf = Poisson):")
    for stat, g in grid[grid.grid == "k"].groupby("stat", sort=False):
        print(f"  {stat:<10}" + " · ".join(f"{r.value} {r.score:.4f}" for r in g.itertuples()))
    print("\n  ablation at the main line (log-loss; each piece of the live recipe switched off):")
    for stat, g in grid[grid.grid == "ablation"].groupby("stat", sort=False):
        print(f"  {stat:<10}" + " · ".join(f"{r.value} {r.score:.4f}" for r in g.itertuples()))
    return pd.DataFrame(lines_rows), bins, grid


# ---------------------------------------------------------------- D (teammate correlation)

def section_d(logs: pd.DataFrame) -> pd.DataFrame:
    """Pooled Pearson correlation of 'had ≥ 1' indicators over every ordered pair of skaters in the
    same team-game (and across the two teams of a game), in closed form from per-team sums; latent
    ρ = sin(π r / 2) is what nhl_edge.TEAM_RHO feeds the card simulation's Gaussian copula."""
    rows = []
    sk = logs[logs.toi.notna()]
    print("\nD. Same-game correlation of skater outcomes (feeds nhl_edge.TEAM_RHO)")
    print(f"  {'stat':<8}{'pairs':<10}{'n pairs':>12}{'r':>9}{'latent ρ':>10}")
    for stat in ("points", "assists"):
        d = sk[sk[stat].notna()]
        g = d.assign(x=(d[stat] >= 1).astype(float)).groupby(["game_id", "team"], sort=True).x.agg(["sum", "count"])
        s_, n_ = g["sum"].to_numpy(), g["count"].to_numpy()
        npair = float((n_ * (n_ - 1)).sum())
        m = float((s_ * (n_ - 1)).sum()) / npair
        exy = float((s_ * s_ - s_).sum()) / npair
        r_tm = (exy - m * m) / (m * (1 - m))
        gg = g.reset_index()
        both = gg.groupby("game_id").filter(lambda t: len(t) == 2).sort_values(["game_id", "team"])
        a, b = both.iloc[0::2], both.iloc[1::2]
        sa, na, sb, nb = (a["sum"].to_numpy(), a["count"].to_numpy(), b["sum"].to_numpy(), b["count"].to_numpy())
        opp_pairs = float((2 * na * nb).sum())
        mo = float((sa * nb + sb * na).sum()) / opp_pairs
        exy_o = float((2 * sa * sb).sum()) / opp_pairs
        r_op = (exy_o - mo * mo) / (mo * (1 - mo))
        for who, r, n in (("team", r_tm, npair), ("opp", r_op, opp_pairs)):
            rho = math.sin(math.pi * r / 2)
            print(f"  {stat:<8}{who:<10}{n:>12,.0f}{r:>9.4f}{rho:>10.4f}")
            rows.append({"stat": stat, "pairs": who, "n_pairs": n, "r": r, "latent_rho": rho})
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- E (model vs market)

def section_e(lines: pd.DataFrame) -> pd.DataFrame:
    rows = []
    print(f"\nE. Model vs market — {len(lines):,} settled snapshot lines (last snapshot per book), log-loss (lower is better)")
    print(f"  {'recipe':<12}{'market':<26}{'n':>6}{'P model':>9}{'P mkt':>8}{'obs':>7}{'ll model':>10}{'ll mkt':>9}")
    for (model, market), g in [((m, "ALL"), g) for m, g in lines.groupby("model")] + list(lines.groupby(["model", "market"])):
        ll_m, ll_k = logloss(g.p_over, g.y).mean(), logloss(g.p_market, g.y).mean()
        rows.append({"model": model, "market": market, "n": len(g), "p_model": float(g.p_over.mean()),
                     "p_market": float(g.p_market.mean()), "observed": float(g.y.mean()), "ll_model": float(ll_m),
                     "ll_market": float(ll_k)})
        print(f"  {model:<12}{market:<26}{len(g):>6}{g.p_over.mean():>9.3f}{g.p_market.mean():>8.3f}{g.y.mean():>7.3f}"
              f"{ll_m:>10.4f}{ll_k:>9.4f}")
    print("  logit blend (w on the model, 1 − w on the market):")
    for model, g in lines.groupby("model"):
        lm = np.log(np.clip(g.p_over, 1e-6, 1 - 1e-6) / (1 - np.clip(g.p_over, 1e-6, 1 - 1e-6)))
        lk = np.log(np.clip(g.p_market, 1e-6, 1 - 1e-6) / (1 - np.clip(g.p_market, 1e-6, 1 - 1e-6)))
        out = []
        for w in BLEND_GRID:
            ll = float(logloss(1 / (1 + np.exp(-(w * lm + (1 - w) * lk))), g.y).mean())
            rows.append({"model": model, "market": f"blend w={w:g}", "n": len(g), "p_model": float("nan"),
                         "p_market": float("nan"), "observed": float(g.y.mean()), "ll_model": ll, "ll_market": float("nan")})
            out.append(f"w={w:g} {ll:.4f}")
        print(f"  {model:<12}" + " · ".join(out))
    return pd.DataFrame(rows)


def main() -> None:
    OUT_DIR.mkdir(exist_ok=True)
    rng = np.random.default_rng(SEED)
    bets = load_nhl_bets()
    if bets.empty:
        print("no settled NHL paper props yet (season opened 2026-09-29) — skipping A and B")
    else:
        section_a(bets, rng).to_csv(OUT_DIR / "nhl_roi.csv", index=False)
        section_b(bets).to_csv(OUT_DIR / "nhl_slices.csv", index=False)
    logs = load_logs([HISTORY_SEASON, PRIOR_SEASON])
    if logs.empty:
        print("no game logs in nhl.db — run nhl_edge.py --build")
        return
    lines_df, bins, grid = section_c(logs)
    lines_df.to_csv(OUT_DIR / "nhl_backtest.csv", index=False)
    bins.to_csv(OUT_DIR / "nhl_calibration.csv", index=False)
    grid.to_csv(OUT_DIR / "nhl_grid.csv", index=False)
    section_d(load_game_logs(PRIOR_SEASON)).to_csv(OUT_DIR / "nhl_correlation.csv", index=False)
    mk = load_market_lines()
    if mk.empty:
        print("\nE. no settled snapshot lines yet — run --snapshot on a slate, then --build after the games")
    else:
        section_e(mk).to_csv(OUT_DIR / "nhl_market.csv", index=False)
    print(f"\nwrote {OUT_DIR / 'nhl_*.csv'}")


if __name__ == "__main__":
    main()

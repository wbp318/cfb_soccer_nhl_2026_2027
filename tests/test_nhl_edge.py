"""Unit tests for nhl_edge.py — no network. Run: python -m pytest -q tests"""
from __future__ import annotations

import datetime as dt
import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import cfb_edge as ce  # noqa: E402
import nhl_edge as ne  # noqa: E402

UTC = dt.timezone.utc


def make_game(state="FUT") -> ne.GameCtx:
    g = ne.GameCtx(id=2026020001, date=dt.date(2026, 10, 7), start_utc=dt.datetime(2026, 10, 7, 23, 0, tzinfo=UTC),
                   home="TOR", away="MTL", state=state)
    g.home_factor = {k: 1.0 for k in ("shots", "points", "goals", "assists", "blocked", "pp_points", "saves")}
    g.away_factor = dict(g.home_factor)
    return g


def make_player(name="Auston Matthews", team="TOR", pos="C", rates=None, games=50) -> ne.Player:
    return ne.Player(id=8479318, name=name, team=team, position=pos,
                     rates=rates or {"shots": 4.2, "points": 1.3, "goals": 0.7}, games=games)


def make_prop(market="player_shots_on_goal", line=3.5, over=-115, under=-105, player=None, game=None) -> ne.Prop:
    p = ne.Prop(game or make_game(), player or make_player(), market, ne.MARKETS[market][0], line, over, under, "dk")
    ne.project(p)
    return p


# ---------------------------------------------------------------- distribution math

def test_poisson_cdf_and_p_over():
    assert ne.poisson_cdf(-1, 2.0) == 0.0
    assert ne.poisson_cdf(0, 2.0) == pytest.approx(0.1353, abs=1e-4)
    assert ne.poisson_cdf(100, 2.0) == pytest.approx(1.0)
    po, push = ne.p_over(3.0, 2.5)
    assert push == 0.0 and po == pytest.approx(1 - ne.poisson_cdf(2, 3.0))
    po2, push2 = ne.p_over(3.0, 3.0)                       # whole line pushes at exactly 3
    assert push2 == pytest.approx(0.2240, abs=1e-3) and po2 == pytest.approx(1 - ne.poisson_cdf(3, 3.0))


def test_project_uses_rate_times_opponent_factor():
    g = make_game()
    g.home_factor["shots"] = 1.10
    p = make_prop(game=g)
    assert p.mean == pytest.approx(4.2 * 1.10) and 0 < p.p_over < 1
    q = ne.Prop(g, make_player(rates={"points": 1.0}), "player_shots_on_goal", "shots", 3.5, -110, -110)
    ne.project(q)
    assert q.mean is None and q.p_over is None            # no rate for that stat


def test_opponent_factors_damped_clamped_and_home_split():
    prior = {"TOR": {"gp": 82, "sf": 33.0, "sa": 27.0, "gf": 3.5, "ga": 2.6},
             "MTL": {"gp": 82, "sf": 28.0, "sa": 40.0, "gf": 2.8, "ga": 3.6},
             "BOS": {"gp": 82, "sf": 30.0, "sa": 30.0, "gf": 3.0, "ga": 3.0}}
    hf, af = ne.opponent_factors(prior, {}, "TOR", "MTL")
    _, _, beta, h = ne.SKATER_MODEL["shots"]
    assert hf["shots"] == pytest.approx(ne.OPP_FACTOR_CAP[1] ** beta * h ** 0.5)     # MTL allows 40 vs 32.3: clamped, damped
    assert af["shots"] == pytest.approx((27.0 / (97.0 / 3)) ** beta / h ** 0.5)      # TOR allows little, and away
    _, _, beta_p, h_p = ne.SKATER_MODEL["points"]
    assert af["points"] == pytest.approx((2.6 / 3.0666667) ** beta_p / h_p ** 0.5, rel=1e-6)
    hn, an = ne.opponent_factors({"X": {"sf": 30, "sa": 30, "ga": 3}, "Y": {"sf": 30, "sa": 30, "ga": 3}}, {}, "X", "Y")
    assert hn["goals"] * an["goals"] == pytest.approx(1.0) and hn["goals"] > 1.0     # neutral opponents: home ×√h, away ÷√h
    assert hf["saves"] < 1.0 and af["saves"] > 1.0        # goalie facing MTL sees fewer shots


# ---------------------------------------------------------------- signals

def test_prop_signal_tiers_and_overreach():
    p = make_prop(line=3.5, over=+100, under=-120)        # model P(over 3.5 | λ4.2) ≈ 0.61 vs fair ≈ 0.48 -> +27%
    s = ne.prop_signal(p)
    assert s.side == "over" and s.strength == 2 and 15 <= s.edge < 30
    p = make_prop(line=2.5, over=-200, under=+165)        # model ≈ 0.79 vs fair ≈ 0.65 -> ~+21%
    s = ne.prop_signal(p)
    assert s.side == "over" and s.strength == 2
    p = make_prop(line=5.5, over=+300, under=-400)        # +300 beyond MAX_PRICE
    s = ne.prop_signal(p)
    assert s is None or s.strength == 0
    p = make_prop(line=3.5, over=+140, under=-170)        # model 0.61 vs fair ~0.40 -> > +30% -> overreach
    s = ne.prop_signal(p)
    assert s.side == "over" and s.strength == 0 and s.note == "⚠overreach"


def test_prop_signal_thin_and_non_starter_never_staked():
    p = make_prop(player=make_player(games=4), line=3.5, over=+100, under=-120)
    s = ne.prop_signal(p)
    assert s.strength == 0 and s.note == "⚠thin" and ne.stake_for(s, 100.0) is None
    g = make_player(name="Joseph Woll", pos="G", rates={"saves": 27.5})
    p = make_prop(market="player_total_saves", line=24.5, over=-110, under=-110, player=g)
    s = ne.prop_signal(p)
    assert s.side == "over" and s.strength == 1 and s.note == "⚠saves-model"   # saves capped at value
    g.starter = False
    p = make_prop(market="player_total_saves", line=24.5, over=-110, under=-110, player=g)
    s = ne.prop_signal(p)
    assert s.strength == 0 and s.note == "⚠not-starter"


def test_ranked_signals_skips_started_games():
    live = make_prop(game=make_game(state="LIVE"), line=3.5, over=+100, under=-120)
    fut = make_prop(line=3.5, over=+100, under=-120)
    sigs = ne.ranked_signals([live, fut])
    assert len(sigs) == 1 and sigs[0].prop is fut


# ---------------------------------------------------------------- lines: matching + csv

def test_name_and_team_matching():
    assert ne._name_match("Auston Matthews", "Auston Matthews")
    assert ne._name_match("Auston Matthews", "A. Matthews")
    assert ne._name_match("Nick Suzuki", "Nicholas Suzuki")            # first initial + last name
    assert not ne._name_match("Auston Matthews", "Mitch Marner")
    assert ne._team_match("Toronto Maple Leafs", "TOR") and ne._team_match("Utah Mammoth", "UTA")
    assert not ne._team_match("Montreal Canadiens", "TOR")


def test_attach_props_matches_rostered_player_and_drops_ambiguous(tmp_path):
    g = make_game()
    players = {"TOR": [make_player()], "MTL": [make_player(name="Nick Suzuki", team="MTL")]}
    rows = [(g.id, "A. Matthews", "player_shots_on_goal", 3.5, -115, -105, "dk"),
            (None, "Nick Suzuki", "player_points", 0.5, -140, +110, "fd"),
            (g.id, "Nobody Here", "player_points", 0.5, -110, -110, "dk"),
            (g.id, "Auston Matthews", "player_total_saves", 27.5, -110, -110, "dk")]   # skater on a goalie market
    props = ne.attach_props(rows, [g], players)
    assert [(p.player.name, p.market) for p in props] == [("Auston Matthews", "player_shots_on_goal"),
                                                          ("Nick Suzuki", "player_points")]
    csv_path = tmp_path / "lines.csv"
    csv_path.write_text("player,market,line,over,under,book,game\nAuston Matthews,player_shots_on_goal,3.5,-115,-105,dk,MTL @ TOR\n",
                        encoding="utf-8")
    rows = ne.read_props_csv(str(csv_path), [g])
    assert rows == [(g.id, "Auston Matthews", "player_shots_on_goal", 3.5, -115, -105, "dk")]


def test_load_key_from_env_and_dotenv(tmp_path, monkeypatch):
    monkeypatch.delenv("ODDS_API_KEY", raising=False)
    monkeypatch.chdir(tmp_path)
    assert ne.load_key() is None
    (tmp_path / ".env").write_text('ODDS_API_KEY="abc123"\n', encoding="utf-8")
    assert ne.load_key() == "abc123"
    monkeypatch.setenv("ODDS_API_KEY", "fromenv")
    assert ne.load_key() == "fromenv"


# ---------------------------------------------------------------- rates + SQLite round trip

def _log(gid, pid, season, date, shots, points, toi, blocked=None):
    return (gid, pid, season, date, "TOR", "MTL", 1, shots, points, 0, points, blocked, 0, None, None, None, toi)


def test_position_means_per_minute_by_group(tmp_path):
    conn = ne.db_connect(str(tmp_path / "n.db"))
    conn.executemany("INSERT INTO players VALUES (?,?,?,?)", [(1, "F One", "TOR", "C"), (2, "D Two", None, "D"),
                                                              (3, "G Three", "TOR", "G")])
    conn.executemany("INSERT INTO game_logs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                     [_log(1, 1, ne.PRIOR_SEASON, "2026-01-01", 3, 1, 15.0), _log(2, 1, ne.PRIOR_SEASON, "2026-01-02", 1, 0, 15.0),
                      _log(1, 2, ne.PRIOR_SEASON, "2026-01-01", 2, 0, 20.0)])
    pm = ne.position_means(conn)
    assert pm["F"]["toi"] == pytest.approx(15.0) and pm["F"]["shots"] == pytest.approx(4 / 30)
    assert pm["D"]["toi"] == pytest.approx(20.0) and pm["D"]["shots"] == pytest.approx(2 / 20)   # team-less history players count


def test_skater_rates_recipe_by_hand():
    pm = {"toi": 15.0, "shots": 0.1, "points": 0.03, "goals": 0.015, "assists": 0.02, "pp_points": 0.008}
    prior = [(ne.PRIOR_SEASON, 20.0, 3, 1, 0, 1, 0)] * 40                  # 40 games: 3 shots, 1 point in 20 min
    cur = [(ne.SEASON, 22.0, 5, 1, 1, 0, 0)] * 6                            # 6 games: 5 shots, 1 point in 22 min
    rates, toi = ne.skater_rates(prior + cur, pm)
    base = (6 * 22 + ne.TOI_PRIOR_W * 40 * 20 + ne.TOI_GHOST * 15) / (6 + ne.TOI_PRIOR_W * 40 + ne.TOI_GHOST)
    assert toi == pytest.approx((1 - ne.TOI_RECENT_W) * base + ne.TOI_RECENT_W * 22.0)
    a1, k, _, _ = ne.SKATER_MODEL["shots"]
    assert rates["shots"] == pytest.approx((6 * 5 + a1 * 40 * 3 + k * 0.1) / (6 * 22 + a1 * 40 * 20 + k) * toi)
    a1, k, _, _ = ne.SKATER_MODEL["goals"]
    assert rates["goals"] == pytest.approx((6 * 1 + 0 + k * 0.015) / (6 * 22 + a1 * 40 * 20 + k) * toi)
    r0, toi0 = ne.skater_rates(prior, pm)                                   # opening night: last season, regressed
    assert toi0 == pytest.approx((ne.TOI_PRIOR_W * 800 + ne.TOI_GHOST * 15) / (ne.TOI_PRIOR_W * 40 + ne.TOI_GHOST))
    assert 0.03 * toi0 < r0["points"] < 1.0                                 # between the position mean and his own 1.0
    assert ne.skater_rates([], pm) == ({}, None)


def test_player_rates_skater_and_blocks_from_settle(tmp_path):
    conn = ne.db_connect(str(tmp_path / "n.db"))
    conn.execute("INSERT INTO players VALUES (1, 'F One', 'TOR', 'C')")
    rows = [_log(100 + i, 1, ne.PRIOR_SEASON, f"2026-01-{i % 28 + 1:02d}", 3, 1, 18.0) for i in range(40)]
    rows += [_log(200 + i, 1, ne.SEASON, f"2026-10-{i + 8:02d}", 5, 1, 18.0, blocked=2) for i in range(10)]
    conn.executemany("INSERT INTO game_logs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", rows)
    rates, eff = ne.player_rates(conn, 1, dt.date(2026, 10, 20), "C")
    assert 3.0 < rates["shots"] < 5.0 and eff == 30 and rates["blocked"] == pytest.approx(2.0)
    before, eff0 = ne.player_rates(conn, 1, dt.date(2026, 10, 1), "C")
    assert before["shots"] == pytest.approx(3.0) and eff0 == 20 and "blocked" not in before   # he IS the F mean here


def test_build_upsert_keeps_settled_blocks_and_history_players_never_match(tmp_path):
    conn = ne.db_connect(str(tmp_path / "n.db"))
    conn.execute("INSERT INTO game_logs VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", _log(9, 1, ne.SEASON, "2026-10-08", 2, 0, 17.0, 4))
    conn.execute(ne.UPSERT_LOG, _log(9, 1, ne.SEASON, "2026-10-08", 3, 1, 18.0, None))     # rebuild: no blocks in game logs
    assert conn.execute("SELECT shots, blocked FROM game_logs").fetchone() == (3, 4)
    conn.executemany("INSERT INTO players VALUES (?,?,?,?)", [(1, "On Roster", "TOR", "C"), (2, "Retired Guy", None, "C")])
    assert [p.name for ps in ne.db_players(conn).values() for p in ps] == ["On Roster"]


def test_grade_prop_and_settle_summary(tmp_path):
    assert ne.grade_prop("over", 2.5, 3) == "W" and ne.grade_prop("under", 2.5, 3) == "L"
    assert ne.grade_prop("over", 3.0, 3) == "P"
    conn = ne.db_connect(str(tmp_path / "n.db"))
    now = dt.datetime(2026, 10, 7, 10, 0, tzinfo=UTC)
    g, pl = make_game(), make_player()
    conn.execute("INSERT INTO players VALUES (?,?,?,?)", (pl.id, pl.name, pl.team, pl.position))
    p = make_prop(line=3.5, over=+100, under=-120, player=pl, game=g)
    sigs = ne.ranked_signals([p])
    assert ne.db_persist(conn, [g], [p], now) == 1
    assert ne.db_paper_log(conn, sigs, 100.0, now) == 1 and ne.db_paper_log(conn, sigs, 100.0, now) == 0
    conn.execute("UPDATE paper_bets SET actual=5, result='W', profit=5.0")
    conn.commit()
    txt = ne.db_paper_summary(conn)
    assert "player_shots_on_goal" in txt and "over" in txt


def test_report_name_and_banner_in_top():
    assert ne.report_path(dt.date(2026, 10, 7)).endswith("nhl-wednesday-2026-10-07.md")
    p = make_prop(line=3.5, over=+100, under=-120)
    assert ce.stakes_banner() in ne.render_top([p], 100.0)


# ---------------------------------------------------------------- agreement board + lock

def test_agree_signal_window_and_gap():
    p = make_prop(market="player_points", line=0.5, over=-200, under=+165)   # model 0.73 vs fair 0.64 -> +14%
    s = ne.agree_signal(p)
    assert s.kind == "agree" and s.side == "over" and s.strength == 1 and 0 < s.edge <= ne.AGREE_MAX_GAP_PCT
    assert ne.agree_signal(make_prop(market="player_points", line=0.5, over=-150, under=+125)) is None   # gap > +20%
    assert ne.agree_signal(make_prop(market="player_points", line=0.5, over=-300, under=+240)) is None   # too short
    thin = make_prop(market="player_points", line=0.5, over=-200, under=+165, player=make_player(games=4))
    assert ne.agree_signal(thin) is None


def test_lock_and_good_one_per_player():
    a = make_prop(market="player_points", line=0.5, over=-200, under=+165)
    b = make_prop(market="player_shots_on_goal", line=3.5, over=+100, under=-120)     # same player, value board
    other = make_player(name="Nick Suzuki", team="MTL", rates={"points": 1.1, "shots": 2.2})
    other.id = 8480018
    c = make_prop(market="player_points", line=0.5, over=-180, under=+150, player=other)
    lock, good = ne.lock_and_good([a, b, c])
    assert lock.prop is a and [s.prop.player.id for s in good] == [other.id]


def test_fetch_props_espn_pairs_over_then_under(monkeypatch):
    g = make_game()
    ath = "http://core/athletes/1"

    def item(t, line, price):
        return {"type": {"name": t}, "athlete": {"$ref": ath + "?lang=en"}, "odds": {"total": {"value": str(line)},
                "american": {"value": price}}}

    def fake_get(url, params=None, timeout=30):
        if url == ne.ESPN_NHL_SCOREBOARD:
            return {"events": [{"id": "9", "competitions": [{"competitors": [
                {"homeAway": "home", "team": {"displayName": "Toronto Maple Leafs"}},
                {"homeAway": "away", "team": {"displayName": "Montreal Canadiens"}}]}]}]}
        if url.endswith("/propBets"):
            return {"items": [item("Total Points", 0.5, "-195"), item("Total Points", 0.5, "+145"),
                              item("Anytime Goalscorer", 0.5, "+120"), item("Total Shots on Goal", 3.5, "EVEN")]}
        return {"fullName": "Auston Matthews"}
    monkeypatch.setattr(ne, "_get", fake_get)
    rows = ne.fetch_props_espn([g], g.date, log=lambda m: None)
    assert rows == [(g.id, "Auston Matthews", "player_points", 0.5, -195, 145, "draftkings")]


def test_paper_log_keeps_agree_and_prop_buckets_apart(tmp_path):
    conn = ne.db_connect(str(tmp_path / "n.db"))
    p = make_prop(market="player_points", line=0.5, over=-200, under=+165)
    val = ne.Signal(p, "prop", "over", "prop value", 1, 10.0, 0.7, -200)
    n = ne.db_paper_log(conn, [val, ne.agree_signal(p)], 100.0, dt.datetime(2026, 10, 7, tzinfo=UTC))
    assert n == 2
    assert sorted(r[0] for r in conn.execute("SELECT kind FROM paper_bets")) == ["agree", "prop"]


# ---------------------------------------------------------------- simulation

def test_nb_cdf_matches_simulated_gamma_poisson_and_tends_to_poisson():
    import numpy as np
    rng = np.random.default_rng(1)
    x = rng.poisson(rng.gamma(20.0, 27.5 / 20.0, 200_000))
    assert ne.p_over(27.5, 27.5, 20.0)[0] == pytest.approx((x > 27).mean(), abs=0.005)
    assert ne.nb_cdf(2, 1.3, 1e7) == pytest.approx(ne.poisson_cdf(2, 1.3), abs=1e-5)
    assert ne.p_over(27.5, 24.5, 20.0)[0] < ne.p_over(27.5, 24.5)[0]     # wider: less sure of the over


def test_simulate_card_keeps_marginals_and_correlates_teammates():
    a = make_prop(market="player_points", line=0.5, over=-200, under=+165)
    mate = make_player(name="William Nylander", rates={"points": 1.3})
    mate.id = 8477939
    b = make_prop(market="player_points", line=0.5, over=-200, under=+165, player=mate)
    sa, sb = ne.agree_signal(a), ne.agree_signal(b)
    sim = ne.simulate_card([sa, sb], "model", n=40_000)
    assert sim["exp_hits"] == pytest.approx(sa.model_p + sb.model_p, abs=0.01)
    assert sim["p_all"] > sa.model_p * sb.model_p + 0.005                   # same team: both-cash more often
    assert sum(sim["dist"]) == pytest.approx(1.0)
    mkt = ne.simulate_card([sa, sb], "market", n=40_000)
    assert mkt["exp_profit"] < 0 < sim["exp_profit"]                        # fair odds minus vig lose; the model's edge wins
    bl = ne.simulate_card([sa, sb], "blend", n=40_000)
    assert bl["exp_hits"] == pytest.approx(sa.truth_p + sb.truth_p, abs=0.01)   # agree truth_p IS the blend
    assert mkt["exp_hits"] < bl["exp_hits"] < sim["exp_hits"]


def test_blend_p_logit_weights_and_agree_truth_is_the_blend():
    assert ne.blend_p(0.8, 0.6, 0.0) == pytest.approx(0.6) and ne.blend_p(0.8, 0.6, 1.0) == pytest.approx(0.8)
    assert ne.blend_p(0.7, 0.7) == pytest.approx(0.7)
    mid = ne.blend_p(0.8, 0.6, 0.5)                                          # logit midpoint, not the arithmetic 0.70
    assert mid == pytest.approx(1 / (1 + ((0.2 / 0.8) * (0.4 / 0.6)) ** 0.5)) and 0.70 < mid < 0.72
    s = ne.agree_signal(make_prop(market="player_points", line=0.5, over=-200, under=+165))
    assert s.fair_p < s.truth_p < s.model_p and s.truth_p == pytest.approx(ne.blend_p(s.model_p, s.fair_p))
    probs = ne.side_probs(s)
    assert probs == {"model": s.model_p, "blend": pytest.approx(s.truth_p), "market": s.fair_p}

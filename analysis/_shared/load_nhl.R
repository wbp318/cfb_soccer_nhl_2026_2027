# Shared loader for the NHL half of analysis/ (reads nhl.db, never writes).
#
#   source("analysis/_shared/load_nhl.R")
#   bets  <- load_nhl_bets()           # one row per settled NHL paper prop
#   logs  <- load_game_logs(season)    # every stored game-log row for a season, chronological
#   both  <- load_logs(seasons)        # several seasons, with each player's position (for the backtest)
#   lines <- load_market_lines()       # every snapshotted prop line a game log has settled (last snapshot per book)
#
# Mirrors load_nhl.py — keep them in lockstep. CFB_NHL_DB overrides the path (CI).

suppressPackageStartupMessages({
  library(DBI)
  library(RSQLite)
})

.nhl_shared_dir <- tryCatch(dirname(sys.frame(1)$ofile), error = function(e) "analysis/_shared")
NHL_DB <- if (nzchar(Sys.getenv("CFB_NHL_DB"))) Sys.getenv("CFB_NHL_DB") else
  normalizePath(file.path(.nhl_shared_dir, "..", "..", "nhl.db"), mustWork = FALSE)

.NBETS_SQL <- "
SELECT p.id, p.game_id, g.date, p.player_id, pl.name, pl.position, p.kind, p.market, p.side, p.line, p.price,
       p.truth_p, p.edge, p.strength, p.stake, p.book, p.actual, p.result, p.profit,
       COALESCE(p.model, '2026-09-20') AS model
FROM paper_bets p
JOIN games g ON g.id = p.game_id
LEFT JOIN players pl ON pl.id = p.player_id
WHERE p.result IS NOT NULL
"

.NLOGS_SQL <- "
SELECT game_id, player_id, season, date, team, opp, home, shots, points, goals, assists, blocked,
       pp_points, saves, shots_against, started, toi
FROM game_logs WHERE season = ? ORDER BY player_id, date, game_id
"

.NLOGS_POS_SQL <- "
SELECT l.game_id, l.player_id, l.season, l.date, l.team, l.opp, l.home, l.shots, l.points, l.goals, l.assists,
       l.blocked, l.pp_points, l.saves, l.shots_against, l.started, l.toi, pl.position
FROM game_logs l LEFT JOIN players pl ON pl.id = l.player_id
WHERE l.season IN (%s) ORDER BY l.player_id, l.date, l.game_id
"

# last snapshot per (game, player, market, line, book); settled = the player has a game log for that game
.NLINES_SQL <- "
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
"
MARKET_STAT <- c(player_shots_on_goal = "shots", player_points = "points", player_goals = "goals",
                 player_assists = "assists", player_power_play_points = "pp_points",
                 player_blocked_shots = "blocked", player_total_saves = "saves")

.nquery <- function(sql, db_path, params = NULL) {
  con <- dbConnect(SQLite(), db_path)
  on.exit(dbDisconnect(con))
  if (is.null(params)) dbGetQuery(con, sql) else dbGetQuery(con, sql, params = params)
}

.ndec <- function(price) ifelse(price > 0, 1 + price / 100, 1 + 100 / abs(price))

load_nhl_bets <- function(db_path = NHL_DB) {
  df <- .nquery(.NBETS_SQL, db_path)
  df$pnl_flat <- ifelse(df$result == "W", .ndec(df$price) - 1, ifelse(df$result == "L", -1, 0))
  df
}

load_game_logs <- function(season, db_path = NHL_DB) .nquery(.NLOGS_SQL, db_path, list(as.integer(season)))

load_logs <- function(seasons, db_path = NHL_DB) {
  seasons <- as.integer(seasons)
  .nquery(sprintf(.NLOGS_POS_SQL, paste(rep("?", length(seasons)), collapse = ",")), db_path, as.list(seasons))
}

# One row per settled line: stored model P(over), de-vigged market P(over) (multiplicative), outcome y.
# Pushes (actual == line) and markets with no stat in the game log are dropped.
load_market_lines <- function(db_path = NHL_DB) {
  df <- .nquery(.NLINES_SQL, db_path)
  df$stat <- unname(MARKET_STAT[df$market])
  df <- df[!is.na(df$stat), , drop = FALSE]
  df$actual <- vapply(seq_len(nrow(df)), function(i) as.numeric(df[[df$stat[i]]][i]), numeric(1))
  df <- df[!is.na(df$actual) & df$actual != df$line, , drop = FALSE]
  io <- 1 / .ndec(df$over)
  iu <- 1 / .ndec(df$under)
  df$p_market <- io / (io + iu)
  df$y <- as.numeric(df$actual > df$line)
  rownames(df) <- NULL
  df
}

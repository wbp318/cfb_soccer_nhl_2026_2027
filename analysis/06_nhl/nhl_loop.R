# The NHL prop analysis loop: is the projection any good, and does betting it against posted lines make money?
#
#   A. Paper ROI by kind (prop = value board, agree = lock board) and by recipe, then value props by
#      market x side x strength, flat $1, bootstrap 95% CI.
#   B. Slices: edge band, market, side (Wilson CI on hit, flat ROI).
#   C. The projection backtest: every PRIOR_SEASON skater-game (and goalie start) projected walk-forward from
#      HISTORY_SEASON + earlier games (as nhl_edge.backtest does): the live recipe vs the 2026-09-20 recipe vs a
#      naive position average at the lines books hang; C0 home/away ratios (-> SKATER_MODEL h), reliability
#      bins, the dispersion grid, and an ablation at the main line.
#   D. Same-game correlation of skater outcomes -> nhl_edge.TEAM_RHO (card simulation).
#   E. Model vs market on every snapshotted line a game log has settled, by recipe and market, plus the
#      logit blend curve -> nhl_edge.BLEND_MODEL_W.
#
# Output: analysis/_out/nhl_*.csv. Mirrors nhl_loop.py — keep in lockstep.

suppressPackageStartupMessages({
  library(dplyr)
  library(boot)
})

.this_dir <- tryCatch(dirname(sys.frame(1)$ofile), error = function(e) "analysis/06_nhl")
source(file.path(.this_dir, "..", "_shared", "load_data.R"))     # wilson()
source(file.path(.this_dir, "..", "_shared", "load_nhl.R"))

OUT_DIR   <- normalizePath(file.path(.this_dir, "..", "_out"), mustWork = FALSE)
MIN_BETS  <- 10
MIN_N     <- 5
BOOT_REPS <- 5000
SEED      <- 20261007

# mirror nhl_edge.py — a change there must be reflected here (and in nhl_loop.py)
PRIOR_SEASON   <- 20252026
HISTORY_SEASON <- 20242025
TOI_PRIOR_W <- 0.09; TOI_GHOST <- 0.6; TOI_RECENT_W <- 0.56; TOI_RECENT_GAMES <- 5
SKATER_MODEL <- list(shots = c(0.35, 86, 0.84, 1.037), points = c(0.58, 234, 0.70, 1.078),
                     goals = c(0.81, 694, 0.64, 1.077), assists = c(0.58, 355, 0.73, 1.078),
                     pp_points = c(0.31, 50, 0.59, 1.115))            # a1, K ghost minutes, beta, h
STATS <- names(SKATER_MODEL)
DISPERSION <- c(saves = 20, shots = 17.5)
DISPERSION_GRID <- c(Inf, 50, 20, 12, 8, 5, 3, 2)
OPP_LO <- 0.80; OPP_HI <- 1.20
TEAM_PRIOR_GAMES <- 20
SHRINK_GAMES <- 20; RECENT_GAMES <- 10; RECENT_WEIGHT <- 0.35     # goalies, and the 2026-09-20 skater recipe
OLD_HOME <- 1.02
CAL_LINES <- list(shots = c(1.5, 2.5, 3.5), points = c(0.5, 1.5), goals = 0.5, assists = 0.5, pp_points = 0.5,
                  saves = c(24.5, 27.5))
CAL_MAIN <- c(shots = 2.5, points = 0.5, goals = 0.5, assists = 0.5, pp_points = 0.5, saves = 27.5)
CAL_MIN_GAMES <- 20; CAL_MIN_TOI <- 12; CAL_EARLY <- 10
BLEND_GRID <- c(0, 0.25, 0.5, 0.75, 1)
EDGE_BINS   <- c(0, 8, 15, 30, 50, 100000)
EDGE_LABELS <- c("0-8", "8-15", "15-30", "30-50", "50+")

dir.create(OUT_DIR, showWarnings = FALSE, recursive = TRUE)
set.seed(SEED)

verdict <- function(lo, hi) if (lo > 0) "PROFITABLE (95% CI > 0)" else if (hi < 0) "losing (95% CI < 0)" else "inconclusive"
boot_ci <- function(x) {
  b <- boot(x, function(d, i) mean(d[i]), R = BOOT_REPS)
  ci <- boot.ci(b, type = "perc")$percent
  c(lo = ci[4], hi = ci[5])
}
disp_of <- function(stat) if (stat %in% names(DISPERSION)) DISPERSION[[stat]] else Inf
p_over <- function(lam, line, disp = Inf) {
  if (is.infinite(disp)) 1 - ppois(floor(line), lam) else 1 - pnbinom(floor(line), size = disp, mu = lam)
}
logloss <- function(p, y) {
  p <- pmin(pmax(p, 1e-6), 1 - 1e-6)
  -(y * log(p) + (1 - y) * log(1 - p))
}
clamp <- function(x) pmin(pmax(x, OPP_LO), OPP_HI)
fmt_k <- function(k) if (is.infinite(k)) "inf" else sprintf("%g", k)

# per player (rows sorted player, date, game): sum of the previous k values (all previous if k is NULL)
prev_sum <- function(x, grp, k = NULL) {
  cs <- ave(as.numeric(x), grp, FUN = cumsum)
  before <- cs - x
  if (is.null(k)) return(before)
  lag <- ave(cs, grp, FUN = function(v) {
    n <- length(v)
    if (n <= k + 1) rep(0, n) else c(rep(0, k + 1), v[seq_len(n - k - 1)])
  })
  before - lag
}
cumcount <- function(grp) ave(seq_along(grp), grp, FUN = seq_along) - 1

# ---------------------------------------------------------------- A + B
section_a <- function(bets) {
  cat(sprintf("A. Paper ROI — %s settled NHL paper props, flat ROI %+.1f%%\n\n",
              format(nrow(bets), big.mark = ","), 100 * mean(bets$pnl_flat)))
  groups <- list(list(market = "ALL", side = "all", strength = "all", g = bets))
  for (key in split(bets, bets$kind))
    groups[[length(groups) + 1]] <- list(market = paste0("kind:", key$kind[1]), side = "all", strength = "all", g = key)
  for (key in split(bets, bets$model))
    groups[[length(groups) + 1]] <- list(market = paste0("recipe:", key$model[1]), side = "all", strength = "all", g = key)
  props <- bets[bets$kind == "prop", ]      # the value board; the agree board is its own bucket above
  for (key in split(props, list(props$market, props$side, props$strength), drop = TRUE))
    groups[[length(groups) + 1]] <- list(market = key$market[1], side = key$side[1], strength = as.character(key$strength[1]), g = key)
  for (key in split(props, props$market))
    groups[[length(groups) + 1]] <- list(market = key$market[1], side = "any", strength = "any", g = key)
  for (key in split(props, props$side))
    groups[[length(groups) + 1]] <- list(market = "ALL", side = key$side[1], strength = "any", g = key)
  rows <- lapply(groups, function(x) {
    g <- x$g
    if (nrow(g) < MIN_BETS) return(NULL)
    ci <- boot_ci(g$pnl_flat)
    data.frame(market = x$market, side = x$side, strength = x$strength, bets = nrow(g), wins = sum(g$result == "W"),
               hit_rate = mean(g$result == "W"), roi_mean = mean(g$pnl_flat), roi_ci_lo = ci[["lo"]],
               roi_ci_hi = ci[["hi"]], verdict = verdict(ci[["lo"]], ci[["hi"]]), stringsAsFactors = FALSE)
  })
  out <- bind_rows(rows) %>% arrange(desc(roi_ci_lo))
  cat(sprintf("  %-26s%-6s%4s%6s%6s%7s%8s%8s%8s  verdict\n", "market", "side", "str", "bets", "wins", "hit%", "ROI", "CI lo", "CI hi"))
  for (i in seq_len(nrow(out))) {
    r <- out[i, ]
    cat(sprintf("  %-26s%-6s%4s%6d%6d%6.1f%%%+7.1f%%%+7.1f%%%+7.1f%%  %s\n", r$market, r$side, r$strength, r$bets, r$wins,
                100 * r$hit_rate, 100 * r$roi_mean, 100 * r$roi_ci_lo, 100 * r$roi_ci_hi, r$verdict))
  }
  out
}

slice_table <- function(df, col, order, title) {
  cat(sprintf("\n%s\n", title))
  cat(sprintf("  %-26s%5s%5s%8s%8s   95%% CI on hit\n", "bucket", "n", "W", "hit%", "ROI"))
  rows <- list()
  for (key in order[order %in% unique(df[[col]])]) {
    g <- df[df[[col]] == key, ]
    if (nrow(g) < MIN_N) next
    w <- sum(g$result == "W"); wi <- wilson(w, nrow(g) - sum(g$result == "P"))
    rows[[length(rows) + 1]] <- data.frame(dimension = col, bucket = key, n = nrow(g), wins = w, hit_rate = wi[1],
                                           hit_lo = wi[2], hit_hi = wi[3], roi_flat = mean(g$pnl_flat), stringsAsFactors = FALSE)
    cat(sprintf("  %-26s%5d%5d%7.1f%%%+7.1f%%   [%.0f, %.0f]\n", key, nrow(g), w, 100 * wi[1], 100 * mean(g$pnl_flat),
                100 * wi[2], 100 * wi[3]))
  }
  rows
}

section_b <- function(bets) {
  b <- bets[bets$strength >= 1, ]
  b$edge_band <- as.character(cut(b$edge, EDGE_BINS, labels = EDGE_LABELS, right = FALSE))
  rows <- slice_table(b, "edge_band", EDGE_LABELS, "B1. by edge band (does a bigger projection-vs-line gap win more?)")
  rows <- c(rows, slice_table(b, "market", sort(unique(b$market)), "B2. by market"))
  rows <- c(rows, slice_table(b, "side", c("over", "under"), "B3. by side"))
  bind_rows(rows)
}

# ---------------------------------------------------------------- C (projection backtest)
# Per team-game of PRIOR_SEASON: the team's shots for / shots against / goals against as they stood before that
# game, blended with HISTORY_SEASON at gp / (gp + 20) as nhl_edge.opponent_factors does; plus league averages.
team_table <- function(sk) {
  tg <- sk %>% group_by(season, game_id, team) %>%
    summarise(date = first(date), sf = sum(shots), gf = sum(goals), .groups = "drop") %>%
    group_by(season, game_id) %>% filter(n() == 2) %>% ungroup()
  opp <- tg %>% select(season, game_id, opp = team, sa = sf, ga = gf)
  tg <- tg %>% inner_join(opp, by = c("season", "game_id"), relationship = "many-to-many") %>% filter(team != opp)
  prior <- tg %>% filter(season == HISTORY_SEASON) %>% group_by(team) %>%
    summarise(sf_p = mean(sf), sa_p = mean(sa), ga_p = mean(ga), .groups = "drop")
  avg <- c(sf = mean(prior$sf_p), sa = mean(prior$sa_p), ga = mean(prior$ga_p))
  cur <- tg %>% filter(season == PRIOR_SEASON) %>% arrange(team, date, game_id) %>% as.data.frame()
  cur$n_before <- cumcount(cur$team)
  for (k in c("sf", "sa", "ga")) cur[[paste0(k, "_before")]] <- prev_sum(cur[[k]], cur$team)
  cur <- cur %>% left_join(prior, by = "team")
  w <- cur$n_before / (cur$n_before + TEAM_PRIOR_GAMES)
  for (k in c("sf", "sa", "ga")) {
    cm <- ifelse(cur$n_before > 0, cur[[paste0(k, "_before")]] / cur$n_before, NA_real_)
    p <- cur[[paste0(k, "_p")]]
    hat <- ifelse(cur$n_before > 0, ifelse(!is.na(p), w * cm + (1 - w) * p, cm), p)
    hat[is.na(hat) | hat == 0] <- avg[[k]]
    cur[[paste0(k, "_hat")]] <- hat
  }
  list(team = cur[, c("game_id", "team", "sf_hat", "sa_hat", "ga_hat")], avg = avg)
}

skater_frame <- function(logs) {
  sk <- logs[logs$position %in% c("C", "L", "R", "D") & !is.na(logs$toi) & !is.na(logs$shots), ]
  sk$grp <- ifelse(sk$position == "D", "D", "F")
  hist <- sk[sk$season == HISTORY_SEASON, ]
  pm <- list()
  for (g in sort(unique(hist$grp))) {
    d <- hist[hist$grp == g, ]
    pm[[g]] <- c(toi = sum(d$toi) / nrow(d), sapply(STATS, function(s) sum(d[[s]]) / sum(d$toi)))
  }
  tt <- team_table(sk)
  agg <- hist %>% group_by(player_id) %>%
    summarise(n_p = n(), toi_p = sum(toi), shots_p = sum(shots), points_p = sum(points), goals_p = sum(goals),
              assists_p = sum(assists), pp_points_p = sum(pp_points), .groups = "drop")
  cur <- sk[sk$season == PRIOR_SEASON, ] %>% arrange(player_id, date, game_id) %>% as.data.frame()
  cur$n_c <- cumcount(cur$player_id)
  cur$toi_c <- prev_sum(cur$toi, cur$player_id)
  cur$toi_r <- ifelse(cur$n_c > 0, prev_sum(cur$toi, cur$player_id, TOI_RECENT_GAMES) / pmin(cur$n_c, TOI_RECENT_GAMES), NA_real_)
  for (s in STATS) {
    cur[[paste0(s, "_c")]] <- prev_sum(cur[[s]], cur$player_id)
    cur[[paste0(s, "_r10")]] <- prev_sum(cur[[s]], cur$player_id, RECENT_GAMES)
  }
  cur <- cur %>% inner_join(agg, by = "player_id") %>% filter(n_p >= CAL_MIN_GAMES, toi_p / n_p >= CAL_MIN_TOI)
  cur <- cur %>% inner_join(tt$team %>% rename(opp = team), by = c("game_id", "opp")) %>%
    arrange(player_id, date, game_id) %>% as.data.frame()
  list(sk = cur, pm = pm, team = tt$team, avg = tt$avg)
}

lam_live <- function(d, pm, avg, stat, K_mult = 1, beta_on = TRUE, home_on = TRUE, recent_on = TRUE) {
  par <- SKATER_MODEL[[stat]]
  a1 <- par[1]; K <- par[2] * K_mult; beta <- par[3]; h <- par[4]
  mu_toi <- c(F = pm$F[["toi"]], D = pm$D[["toi"]])[d$grp]
  mu_s <- c(F = pm$F[[stat]], D = pm$D[[stat]])[d$grp]
  base <- (d$toi_c + TOI_PRIOR_W * d$toi_p + TOI_GHOST * mu_toi) / (d$n_c + TOI_PRIOR_W * d$n_p + TOI_GHOST)
  rw <- if (recent_on) TOI_RECENT_W else 0
  toi <- ifelse(d$n_c > 0, (1 - rw) * base + rw * ifelse(is.na(d$toi_r), 0, d$toi_r), base)
  rate <- (d[[paste0(stat, "_c")]] + a1 * d[[paste0(stat, "_p")]] + K * mu_s) / (d$toi_c + a1 * d$toi_p + K)
  allow <- if (stat == "shots") clamp(d$sa_hat / avg[["sa"]]) else clamp(d$ga_hat / avg[["ga"]])
  fac <- (if (beta_on) allow^beta else 1) * (if (home_on) ifelse(d$home == 1, sqrt(h), 1 / sqrt(h)) else 1)
  unname(rate * toi * fac)
}

lam_old <- function(d, avg, stat) {
  prior_mean <- d[[paste0(stat, "_p")]] / d$n_p
  cur_mean <- ifelse(d$n_c > 0, d[[paste0(stat, "_c")]] / d$n_c, prior_mean)
  w <- d$n_c / (d$n_c + SHRINK_GAMES)
  base <- w * cur_mean + (1 - w) * prior_mean
  nr <- pmin(d$n_c, RECENT_GAMES)
  base <- ifelse(nr >= 5, (1 - RECENT_WEIGHT) * base + RECENT_WEIGHT * d[[paste0(stat, "_r10")]] / pmax(nr, 1), base)
  allow <- if (stat == "shots") clamp(d$sa_hat / avg[["sa"]]) else clamp(d$ga_hat / avg[["ga"]])
  base * allow * ifelse(d$home == 1, OLD_HOME, 1)
}

goalie_frame <- function(logs, team, avg) {
  g <- logs[!is.na(logs$position) & logs$position == "G" & !is.na(logs$started) & logs$started == 1 & !is.na(logs$saves), ]
  hist <- g[g$season == HISTORY_SEASON, ]
  naive <- if (nrow(hist)) mean(hist$saves) else 27
  agg <- hist %>% group_by(player_id) %>% summarise(n_p = n(), sv_p = sum(saves), .groups = "drop")
  cur <- g[g$season == PRIOR_SEASON, ] %>% arrange(player_id, date, game_id) %>% as.data.frame()
  cur$n_c <- cumcount(cur$player_id)
  cur$sv_c <- prev_sum(cur$saves, cur$player_id)
  cur$sv_r10 <- prev_sum(cur$saves, cur$player_id, RECENT_GAMES)
  cur <- cur %>% inner_join(agg, by = "player_id") %>% filter(n_p >= CAL_MIN_GAMES)
  cur <- cur %>% inner_join(team %>% rename(opp = team), by = c("game_id", "opp")) %>%
    arrange(player_id, date, game_id) %>% as.data.frame()
  prior_mean <- cur$sv_p / cur$n_p
  cur_mean <- ifelse(cur$n_c > 0, cur$sv_c / cur$n_c, prior_mean)
  w <- cur$n_c / (cur$n_c + SHRINK_GAMES)
  base <- w * cur_mean + (1 - w) * prior_mean
  nr <- pmin(cur$n_c, RECENT_GAMES)
  base <- ifelse(nr >= 5, (1 - RECENT_WEIGHT) * base + RECENT_WEIGHT * cur$sv_r10 / pmax(nr, 1), base)
  cur$lam <- base * clamp(cur$sf_hat / avg[["sf"]])
  list(g = cur, naive = naive)
}

section_c <- function(logs) {
  empty <- list(lines = data.frame(), bins = data.frame(), grid = data.frame())
  sf <- skater_frame(logs)
  sk <- sf$sk; pm <- sf$pm; avg <- sf$avg
  if (nrow(sk) == 0) {
    cat(sprintf("\nC. no %d + %d skater logs — run nhl_edge.py --build (it stores both seasons)\n", HISTORY_SEASON, PRIOR_SEASON))
    return(empty)
  }
  gf <- goalie_frame(logs, sf$team, avg)
  gl <- gf$g
  lines_rows <- list(); bin_rows <- list(); grid_rows <- list()
  skl <- logs[!is.na(logs$position) & logs$position %in% c("C", "L", "R", "D"), ]
  cat("\nC0. Home/away ratio, Σ home ÷ Σ away over every skater-game (nhl_edge.SKATER_MODEL h = the pooled row)\n")
  parts <- c(lapply(split(skl, skl$season), function(d) list(label = as.character(d$season[1]), d = d)),
             list(list(label = "pooled", d = skl)))
  for (pt in parts) {
    d <- pt$d
    ratios <- sapply(STATS, function(s) sum(d[[s]][d$home == 1], na.rm = TRUE) / sum(d[[s]][d$home == 0], na.rm = TRUE))
    for (s in STATS) grid_rows[[length(grid_rows) + 1]] <- data.frame(stat = s, line = NA_real_, grid = "home/away",
                                                                       value = pt$label, n = nrow(d), score = ratios[[s]])
    cat(sprintf("  %-10s%s\n", pt$label, paste(sprintf("%s %.4f", STATS, ratios), collapse = " · ")))
  }
  cat(sprintf("\nC. Projection backtest — every %d game projected from %d + earlier games (skaters ≥ %d games at ≥ %g min the season before; goalies ≥ %d starts)\n",
              PRIOR_SEASON, HISTORY_SEASON, CAL_MIN_GAMES, CAL_MIN_TOI, CAL_MIN_GAMES))
  cat(sprintf("  %-10s%5s%8s%9s%9s%9s%10s%11s%10s%12s%11s\n", "stat", "line", "n", "live", "old", "naive", "live-old",
              "bias live", "bias old", "early live", "early old"))
  for (stat in c(STATS, "saves")) {
    if (stat == "saves") {
      if (nrow(gl) == 0) next
      y <- as.numeric(gl$saves)
      lams <- list(live = gl$lam)
      lam_naive <- rep(gf$naive, nrow(gl))
      early_s <- gl$n_c < CAL_EARLY
    } else {
      y <- as.numeric(sk[[stat]])
      lams <- list(live = lam_live(sk, pm, avg, stat), old = lam_old(sk, avg, stat))
      lam_naive <- unname(c(F = pm$F[[stat]] * pm$F[["toi"]], D = pm$D[[stat]] * pm$D[["toi"]])[sk$grp])
      early_s <- sk$n_c < CAL_EARLY
    }
    disp <- disp_of(stat)
    for (line in CAL_LINES[[stat]]) {
      hit <- as.numeric(y > line)
      res <- list()
      for (rec in c(names(lams), "naive")) {
        lam <- if (rec == "naive") lam_naive else lams[[rec]]
        p <- p_over(lam, line, if (rec == "live") disp else Inf)
        ll <- logloss(p, hit)
        res[[rec]] <- c(mean(ll), mean(p - hit), if (any(early_s)) mean(ll[early_s]) else NaN,
                        if (any(early_s)) mean((p - hit)[early_s]) else NaN)
        lines_rows[[length(lines_rows) + 1]] <- data.frame(stat = stat, line = line, recipe = rec, n = length(y),
          logloss = res[[rec]][1], bias = res[[rec]][2], n_early = sum(early_s), logloss_early = res[[rec]][3],
          bias_early = res[[rec]][4], stringsAsFactors = FALSE)
      }
      o <- if (is.null(res$old)) c(sprintf("%9s", "-"), sprintf("%10s", "-"), sprintf("%10s", "-"), sprintf("%11s", "-")) else
        c(sprintf("%9.4f", res$old[1]), sprintf("%+10.4f", res$live[1] - res$old[1]), sprintf("%+10.3f", res$old[2]),
          sprintf("%11.4f", res$old[3]))
      cat(sprintf("  %-10s%5g%8s%9.4f%s%9.4f%s%+11.3f%s%12.4f%s\n", stat, line, format(length(y), big.mark = ","),
                  res$live[1], o[1], res$naive[1], o[2], res$live[2], o[3], res$live[3], o[4]))
    }
    main <- CAL_MAIN[[stat]]
    hit <- as.numeric(y > main)
    p <- p_over(lams$live, main, disp)
    b <- pmin(9, floor(p * 10))
    for (k in sort(unique(b))) {
      m <- b == k
      bin_rows[[length(bin_rows) + 1]] <- data.frame(stat = stat, line = main, bin = sprintf("%.1f-%.1f", k / 10, (k + 1) / 10),
                                                     n = sum(m), pred = mean(p[m]), obs = mean(hit[m]), stringsAsFactors = FALSE)
    }
    for (k in DISPERSION_GRID)
      grid_rows[[length(grid_rows) + 1]] <- data.frame(stat = stat, line = main, grid = "k", value = fmt_k(k), n = length(y),
                                                       score = mean(logloss(p_over(lams$live, main, k), hit)))
    if (stat != "saves") {
      variants <- list(list("live", list()), list("K=0 (no regression)", list(K_mult = 0)), list("K x 0.5", list(K_mult = 0.5)),
                       list("K x 2", list(K_mult = 2)), list("beta=0 (no opponent)", list(beta_on = FALSE)),
                       list("h=1 (no home split)", list(home_on = FALSE)), list("no recent minutes", list(recent_on = FALSE)))
      for (v in variants) {
        lam <- do.call(lam_live, c(list(sk, pm, avg, stat), v[[2]]))
        grid_rows[[length(grid_rows) + 1]] <- data.frame(stat = stat, line = main, grid = "ablation", value = v[[1]],
                                                         n = length(y), score = mean(logloss(p_over(lam, main, disp), hit)))
      }
    }
  }
  bins <- bind_rows(bin_rows); grid <- bind_rows(grid_rows)
  cat("\n  reliability of the live recipe at the main line (bins with n ≥ 50): predicted vs observed P(over)\n")
  for (stat in unique(bins$stat)) {
    g <- bins[bins$stat == stat & bins$n >= 50, ]
    cat(sprintf("  %-10s%s\n", stat, paste(sprintf("%s: %.0f/%.0f", g$bin, 100 * g$pred, 100 * g$obs), collapse = " · ")))
  }
  cat("\n  dispersion k at the main line (log-loss; inf = Poisson):\n")
  for (stat in unique(grid$stat[grid$grid == "k"])) {
    g <- grid[grid$grid == "k" & grid$stat == stat, ]
    cat(sprintf("  %-10s%s\n", stat, paste(sprintf("%s %.4f", g$value, g$score), collapse = " · ")))
  }
  cat("\n  ablation at the main line (log-loss; each piece of the live recipe switched off):\n")
  for (stat in unique(grid$stat[grid$grid == "ablation"])) {
    g <- grid[grid$grid == "ablation" & grid$stat == stat, ]
    cat(sprintf("  %-10s%s\n", stat, paste(sprintf("%s %.4f", g$value, g$score), collapse = " · ")))
  }
  list(lines = bind_rows(lines_rows), bins = bins, grid = grid)
}

# ---------------------------------------------------------------- D
# Pooled Pearson r of 'had >= 1' over ordered skater pairs in the same team-game (and across the two
# teams), closed form from per-team sums; latent rho = sin(pi r / 2) feeds nhl_edge.TEAM_RHO.
section_d <- function(logs) {
  sk <- logs[!is.na(logs$toi), ]
  cat("\nD. Same-game correlation of skater outcomes (feeds nhl_edge.TEAM_RHO)\n")
  cat(sprintf("  %-8s%-10s%12s%9s%s\n", "stat", "pairs", "n pairs", "r", "  latent ρ"))   # R pads by bytes; ρ is two
  rows <- list()
  for (stat in c("points", "assists")) {
    d <- sk[!is.na(sk[[stat]]), ]
    d$x <- as.numeric(d[[stat]] >= 1)
    g <- d %>% group_by(game_id, team) %>% summarise(s = sum(x), n = n(), .groups = "drop") %>% arrange(game_id, team)
    npair <- sum(g$n * (g$n - 1))
    m <- sum(g$s * (g$n - 1)) / npair
    exy <- sum(g$s * g$s - g$s) / npair
    r_tm <- (exy - m * m) / (m * (1 - m))
    both <- g %>% group_by(game_id) %>% filter(n() == 2) %>% ungroup() %>% arrange(game_id, team)
    a <- both[seq(1, nrow(both), by = 2), ]; b <- both[seq(2, nrow(both), by = 2), ]
    opp_pairs <- sum(2 * a$n * b$n)
    mo <- sum(a$s * b$n + b$s * a$n) / opp_pairs
    exy_o <- sum(2 * a$s * b$s) / opp_pairs
    r_op <- (exy_o - mo * mo) / (mo * (1 - mo))
    for (who in c("team", "opp")) {
      r <- if (who == "team") r_tm else r_op
      np <- if (who == "team") npair else opp_pairs
      rho <- sin(pi * r / 2)
      cat(sprintf("  %-8s%-10s%12s%9.4f%10.4f\n", stat, who, format(np, big.mark = ","), r, rho))
      rows[[length(rows) + 1]] <- data.frame(stat = stat, pairs = who, n_pairs = np, r = r, latent_rho = rho,
                                             stringsAsFactors = FALSE)
    }
  }
  bind_rows(rows)
}

# ---------------------------------------------------------------- E
section_e <- function(lines) {
  rows <- list()
  cat(sprintf("\nE. Model vs market — %s settled snapshot lines (last snapshot per book), log-loss (lower is better)\n",
              format(nrow(lines), big.mark = ",")))
  cat(sprintf("  %-12s%-26s%6s%9s%8s%7s%10s%9s\n", "recipe", "market", "n", "P model", "P mkt", "obs", "ll model", "ll mkt"))
  keys <- rbind(data.frame(model = sort(unique(lines$model)), market = "ALL", stringsAsFactors = FALSE),
                unique(lines[, c("model", "market")]) %>% arrange(model, market))
  for (i in seq_len(nrow(keys))) {
    g <- lines[lines$model == keys$model[i] & (keys$market[i] == "ALL" | lines$market == keys$market[i]), ]
    ll_m <- mean(logloss(g$p_over, g$y)); ll_k <- mean(logloss(g$p_market, g$y))
    rows[[length(rows) + 1]] <- data.frame(model = keys$model[i], market = keys$market[i], n = nrow(g), p_model = mean(g$p_over),
                                           p_market = mean(g$p_market), observed = mean(g$y), ll_model = ll_m, ll_market = ll_k,
                                           stringsAsFactors = FALSE)
    cat(sprintf("  %-12s%-26s%6d%9.3f%8.3f%7.3f%10.4f%9.4f\n", keys$model[i], keys$market[i], nrow(g), mean(g$p_over),
                mean(g$p_market), mean(g$y), ll_m, ll_k))
  }
  cat("  logit blend (w on the model, 1 − w on the market):\n")
  for (model in sort(unique(lines$model))) {
    g <- lines[lines$model == model, ]
    pm_ <- pmin(pmax(g$p_over, 1e-6), 1 - 1e-6); pk <- pmin(pmax(g$p_market, 1e-6), 1 - 1e-6)
    lm <- log(pm_ / (1 - pm_)); lk <- log(pk / (1 - pk))
    out <- character(0)
    for (w in BLEND_GRID) {
      ll <- mean(logloss(1 / (1 + exp(-(w * lm + (1 - w) * lk))), g$y))
      rows[[length(rows) + 1]] <- data.frame(model = model, market = sprintf("blend w=%g", w), n = nrow(g), p_model = NaN,
                                             p_market = NaN, observed = mean(g$y), ll_model = ll, ll_market = NaN,
                                             stringsAsFactors = FALSE)
      out <- c(out, sprintf("w=%g %.4f", w, ll))
    }
    cat(sprintf("  %-12s%s\n", model, paste(out, collapse = " · ")))
  }
  bind_rows(rows)
}

bets <- load_nhl_bets()
if (nrow(bets) == 0) {
  cat("no settled NHL paper props yet (season opened 2026-09-29) — skipping A and B\n")
} else {
  write.csv(section_a(bets), file.path(OUT_DIR, "nhl_roi.csv"), row.names = FALSE)
  write.csv(section_b(bets), file.path(OUT_DIR, "nhl_slices.csv"), row.names = FALSE)
}
logs <- load_logs(c(HISTORY_SEASON, PRIOR_SEASON))
if (nrow(logs) == 0) {
  cat("no game logs in nhl.db — run nhl_edge.py --build\n")
  quit(status = 0)
}
cres <- section_c(logs)
write.csv(cres$lines, file.path(OUT_DIR, "nhl_backtest.csv"), row.names = FALSE)
write.csv(cres$bins, file.path(OUT_DIR, "nhl_calibration.csv"), row.names = FALSE)
write.csv(cres$grid, file.path(OUT_DIR, "nhl_grid.csv"), row.names = FALSE)
write.csv(section_d(load_game_logs(PRIOR_SEASON)), file.path(OUT_DIR, "nhl_correlation.csv"), row.names = FALSE)
mk <- load_market_lines()
if (nrow(mk) == 0) {
  cat("\nE. no settled snapshot lines yet — run --snapshot on a slate, then --build after the games\n")
} else {
  write.csv(section_e(mk), file.path(OUT_DIR, "nhl_market.csv"), row.names = FALSE)
}
cat(sprintf("\nwrote %s\n", file.path(OUT_DIR, "nhl_*.csv")))

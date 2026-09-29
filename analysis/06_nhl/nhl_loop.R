# The NHL prop analysis loop: is the projection any good, and (once the ledger fills) does
# betting it against posted lines make money?
#
#   A. Paper ROI by kind (prop = value board, agree = lock board), then value props by
#      market x side x strength, flat $1, bootstrap 95% CI.
#   B. Slices: edge band, market, side (Wilson CI on hit, flat ROI).
#   C. Walk-forward projection calibration on the stored game logs (same recipe as
#      nhl_edge.calibrate): log-loss vs naive league-average + reliability bins, plus the
#      dispersion grid (gamma-Poisson shape k vs Poisson) behind nhl_edge.DISPERSION.
#   D. Same-game correlation of skater outcomes -> nhl_edge.TEAM_RHO (card simulation).
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

PRIOR_SEASON  <- 20252026
SHRINK_GAMES  <- 20
RECENT_GAMES  <- 10
RECENT_WEIGHT <- 0.35
MIN_PRIOR     <- 10
LINES <- c(shots = 2.5, points = 0.5, saves = 27.5)
DISPERSION <- c(saves = 20)            # gamma-Poisson shape per stat; absent = Poisson
DISPERSION_GRID <- c(Inf, 50, 20, 12, 8, 5, 3, 2)
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
p_over <- function(lam, line, disp = Inf) {
  if (is.infinite(disp)) 1 - ppois(floor(line), lam) else 1 - pnbinom(floor(line), size = disp, mu = lam)
}

# ---------------------------------------------------------------- A + B
section_a <- function(bets) {
  cat(sprintf("A. Paper ROI — %s settled NHL paper props, flat ROI %+.1f%%\n\n",
              format(nrow(bets), big.mark = ","), 100 * mean(bets$pnl_flat)))
  groups <- list(list(market = "ALL", side = "all", strength = "all", g = bets))
  for (key in split(bets, bets$kind))
    groups[[length(groups) + 1]] <- list(market = paste0("kind:", key$kind[1]), side = "all", strength = "all", g = key)
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

# ---------------------------------------------------------------- C
section_c <- function(logs) {
  rows <- list()
  for (stat in names(LINES)) {
    line <- LINES[[stat]]
    d <- if (stat == "saves") logs[!is.na(logs$started) & logs$started == 1 & !is.na(logs$saves), ] else
      logs[!is.na(logs$toi) & !is.na(logs[[stat]]), ]
    if (nrow(d) == 0) next
    lg <- mean(d[[stat]]); pn <- p_over(lg, line)
    disp <- if (stat %in% names(DISPERSION)) DISPERSION[[stat]] else Inf
    lams <- numeric(0); ys <- numeric(0)
    bins <- list(); ll_m <- 0; ll_n <- 0; n <- 0
    eps <- 1e-6
    for (vs in split(d[[stat]], d$player_id)) {           # split() keeps within-player row order
      vs <- as.numeric(vs)
      if (length(vs) <= MIN_PRIOR) next
      for (i in (MIN_PRIOR + 1):length(vs)) {
        hist <- vs[1:(i - 1)]
        w <- length(hist) / (length(hist) + SHRINK_GAMES)
        lam <- w * mean(hist) + (1 - w) * lg
        rv <- tail(hist, RECENT_GAMES)
        if (length(rv) >= 5) lam <- (1 - RECENT_WEIGHT) * lam + RECENT_WEIGHT * mean(rv)
        po <- p_over(lam, line, disp)
        y <- if (vs[i] > line) 1 else 0
        lams <- c(lams, lam); ys <- c(ys, y)
        ll_m <- ll_m - (y * log(max(po, eps)) + (1 - y) * log(max(1 - po, eps)))
        ll_n <- ll_n - (y * log(max(pn, eps)) + (1 - y) * log(max(1 - pn, eps)))
        b <- as.character(min(9, floor(po * 10)))
        if (is.null(bins[[b]])) bins[[b]] <- c(0, 0, 0)
        bins[[b]] <- bins[[b]] + c(1, po, y)
        n <- n + 1
      }
    }
    if (n == 0) next
    cat(sprintf("\nC. %s over %g — %s player-games (%d), walk-forward, no prior season\n", toupper(stat), line,
                format(n, big.mark = ","), PRIOR_SEASON))
    cat(sprintf("  log-loss: model %.4f · naive league-average %.4f → %s by %.4f\n", ll_m / n, ll_n / n,
                if (ll_m < ll_n) "model better" else "NAIVE better", abs(ll_m - ll_n) / n))
    cat(sprintf("  %-12s%7s%8s%8s%7s\n", "P(over) bin", "n", "pred", "obs", "Δpp"))
    for (b in as.character(sort(as.integer(names(bins))))) {
      v <- bins[[b]]; bi <- as.integer(b)
      cat(sprintf("  %.1f-%.1f     %7d%7.1f%%%7.1f%%%+6.1f\n", bi / 10, (bi + 1) / 10, v[1], 100 * v[2] / v[1],
                  100 * v[3] / v[1], 100 * (v[3] - v[2]) / v[1]))
      rows[[length(rows) + 1]] <- data.frame(stat = stat, line = line, bin = sprintf("%.1f-%.1f", bi / 10, (bi + 1) / 10),
                                             n = v[1], pred = v[2] / v[1], obs = v[3] / v[1], stringsAsFactors = FALSE)
    }
    rows[[length(rows) + 1]] <- data.frame(stat = stat, line = line, bin = "logloss", n = n, pred = ll_m / n, obs = ll_n / n,
                                           stringsAsFactors = FALSE)
    grid <- character(0)
    for (k in DISPERSION_GRID) {          # does an uncertain rate (gamma-Poisson) beat plain Poisson?
      po <- p_over(lams, line, k)
      ll <- -sum(ys * log(pmax(po, 1e-6)) + (1 - ys) * log(pmax(1 - po, 1e-6))) / n
      tag <- if (is.infinite(k)) "inf" else sprintf("%g", k)
      grid <- c(grid, sprintf("%s %.4f", tag, ll))
      rows[[length(rows) + 1]] <- data.frame(stat = stat, line = line, bin = paste0("k=", tag), n = n, pred = ll, obs = NA_real_,
                                             stringsAsFactors = FALSE)
    }
    cat(sprintf("  dispersion k (inf = Poisson; live uses %s): %s\n", if (is.infinite(disp)) "inf" else sprintf("%g", disp),
                paste(grid, collapse = " · ")))
  }
  bind_rows(rows)
}

# ---------------------------------------------------------------- D
# Pooled Pearson r of 'had >= 1' over ordered skater pairs in the same team-game (and across the two
# teams), closed form from per-team sums; latent rho = sin(pi r / 2) feeds nhl_edge.TEAM_RHO.
section_d <- function(logs) {
  sk <- logs[!is.na(logs$toi), ]
  cat("\nD. Same-game correlation of skater outcomes (feeds nhl_edge.TEAM_RHO)\n")
  cat(sprintf("  %-8s%-10s%12s%9s%10s\n", "stat", "pairs", "n pairs", "r", "latent ρ"))
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

bets <- load_nhl_bets()
if (nrow(bets) == 0) {
  cat("no settled NHL paper props yet (season opened 2026-09-29) — skipping A and B\n")
} else {
  write.csv(section_a(bets), file.path(OUT_DIR, "nhl_roi.csv"), row.names = FALSE)
  write.csv(section_b(bets), file.path(OUT_DIR, "nhl_slices.csv"), row.names = FALSE)
}
logs <- load_game_logs(PRIOR_SEASON)
if (nrow(logs) == 0) {
  cat("no game logs in nhl.db — run nhl_edge.py --build\n")
  quit(status = 0)
}
write.csv(section_c(logs), file.path(OUT_DIR, "nhl_calibration.csv"), row.names = FALSE)
write.csv(section_d(logs), file.path(OUT_DIR, "nhl_correlation.csv"), row.names = FALSE)
cat(sprintf("\nwrote %s\n", file.path(OUT_DIR, "nhl_*.csv")))

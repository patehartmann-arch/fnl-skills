# Chopped / Survivor Format — Reference

> **Time horizon:** single week, but with knockout consequences. **Risk profile:** survival-first. **Decision driver:** Floor + Volatility + Injury Risk + Cutline Distance.

## What's different about Chopped

Chopped (a.k.a. Survivor) is a fantasy format where the **lowest-scoring team each week is eliminated**. It runs in season-long but with weekly cuts. The math changes everything:

- **You don't win by scoring most.** You win by **never being last**.
- **Floor matters more than Ceiling**, week by week.
- **Variance is your enemy** when you're near the cutline.
- **Injury risk is amplified** — a 0 from your starter doesn't just hurt your week, it can knock you out.

This makes Chopped the format with the **strictest start/sit logic**. Lineup-Nein in Chopped should be the most opinionated of any format.

## Weight matrix

| Signal | Weight | Why |
|---|---:|---|
| Floor (10th-percentile projection) | **30%** | If you go below floor, you're cut. |
| Injury risk (questionable / soft tissue / first game back) | **25%** | A 0 from a "questionable" starter is a likely cut. |
| Cutline Distance (how close to elimination this week?) | **15%** | Near cutline → ultra-safe. Comfortable lead → can take ceiling shots. |
| Snap Share / role security | **10%** | Volume = floor protection. |
| Matchup + Vegas implied total | **10%** | Bad matchup amplifies floor risk. |
| Volatility (StdDev of last 4 weeks) | **10%** | Boom/bust players are landmines in Chopped. |

Note: **Ceiling is explicitly low weight** in Chopped. The opposite of BestBall. Don't confuse them.

## Decision rules

### When to say NEIN (don't start) in Chopped

1. **Questionable injury status** + boom/bust profile → bench. The downside of a 0-3 point game is too high.
2. **Snap Share < 60%** AND alternative on bench has > 70% with similar matchup → the bench guy is more reliable.
3. **Boom/bust profile** (StdDev > 10 PPR points over last 4 weeks) when user is **near cutline** → never start a landmine.
4. **Bad matchup + low team total (< 18)** for a non-elite player → high floor-risk.

### When to say JA (start)

1. **High floor, decent ceiling, good matchup, healthy** — trivial start in Chopped.
2. **High volume RB or WR1 in a strong offense** — even a bad day is usually 8-10 PPR points.
3. **Comfortable lead this week** (user shared cutline data, they're 10+ points clear of last) → can take a moderate ceiling shot.

### When to say "RESEARCH MORE"

1. **Late inactives pending** — Chopped is unforgiving, recommend the user wait for confirmed actives if possible.
2. **Cutline distance unclear** — ask the user how close they are to elimination this week.

## Required data inputs

For Chopped:
- All Redraft inputs (projection, matchup, injury, snap %)
- **Volatility**: compute StdDev of last 4 weeks' fantasy points from `weekly-stats`
- **Cutline distance**: ask the user explicitly. They know their league's standings better than any API.

## Output style for Chopped

Chopped users live with knockout pressure. The output should:

- **Frame the recommendation in survival terms** ("dieser Spieler hat in 2 von 4 Wochen unter 5 Punkten geliefert — das ist ein Cut-Risiko, kein Sieg-Pfad")
- **Floor numbers, not averages** — averages hide the catastrophic weeks
- **Reference cutline distance** if user shared it
- Be **more conservative** than Redraft. Better safe + survive than aggressive + cut.

## Anti-patterns (don't do)

- ❌ Recommending boom/bust players when user is near cutline. That's BestBall thinking.
- ❌ Ceiling-first analysis. Chopped pays for floor.
- ❌ Ignoring injury status as "probably plays". In Chopped, "probably" is a cut letter.

## Typical confidence calibration

- **HIGH** confidence: Healthy + high snap share + good matchup + low volatility.
- **MEDIUM** confidence: Slight injury concern OR moderate volatility, but otherwise strong profile.
- **LOW** confidence: Multiple yellow flags, cutline pressure, or late-week injury news pending.

## Status of this reference

🚧 **Draft v0.1.** This format reference is functional but less mature than Dynasty/Redraft. Improvements wanted:

- Concrete cutline-distance scoring formula (e.g., points-from-last × matchup-leverage)
- Volatility computation from `scripts/sleeper_client.py weekly-stats` via a small helper
- Position-specific volatility benchmarks (TE volatility >> RB volatility — adjust thresholds)

Contributions welcome via PR.

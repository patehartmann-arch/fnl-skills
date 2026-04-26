# BestBall Format — Reference

> **Time horizon:** drafted once, played out automatically. **Risk profile:** portfolio-wide. **Decision driver:** ADP Gap + Stack Correlation + Exposure % + Upside.

## Important caveat

**BestBall doesn't allow weekly lineup changes.** Once drafted, the optimal lineup for each week is computed automatically by the platform. So **this skill cannot answer "start X or Y this week"** for BestBall.

What it CAN answer:

1. **Pre-draft:** "Should I draft [Player A] at pick 32 or wait for [Player B] at pick 60?"
2. **Mid-draft (live draft):** "Player X is on the board, I have 22% exposure to QB Y already. Take or pass?"
3. **Roster construction:** "I have 4 QBs in this draft. Is that too many?"
4. **Stack analysis:** "Should I add [WR] to my [QB] stack?"

If a user asks a weekly question for BestBall, redirect:

> *"BestBall stellt Lineups automatisch. Du kannst diese Woche nichts ändern. Die NEIN-Maschine hilft dir aber pre-draft oder live-draft. Möchtest du einen Draft-Pick analysieren?"*

## Weight matrix (for draft decisions)

| Signal | Weight | Why |
|---|---:|---|
| ADP Gap (player ADP vs. current pick) | **25%** | Edge in BestBall comes from picking value, not name brands. |
| Stack Correlation (QB+WR same team, RB+DEF opposite) | **20%** | Stacking amplifies upside in tournament-style BestBall. |
| Exposure % across user's portfolio | **20%** | Over-exposure = correlated downside. Cap at 20-25% per player. |
| Upside / Ceiling profile | **15%** | BestBall rewards spike weeks, not consistency. |
| ADP rise / fall last 7 days | **10%** | Trends matter — late-rising rookies often hit. |
| Position scarcity in remaining draft pool | **10%** | TE/QB cliffs are real. |

Floor profile is **explicitly low weight** in BestBall. Floor is for Redraft and Chopped. BestBall is upside hunting.

## Decision rules

### When to say NEIN (don't draft) in BestBall

1. **Player exposure already > 25%** in user's portfolio → diversify, don't compound risk.
2. **ADP value gap < 6 picks** AND a higher-upside option at the same position is on the board → take the upside.
3. **Veteran with stable but low ceiling** (e.g., 28-year-old RB averaging 11 PPR with 13-week limit) → in BestBall, the spike weeks matter; this guy doesn't have them.
4. **Stack with negative correlation** (e.g., RB on team you're stacking the opposing DEF) → reduce stack tightness or pass.

### When to say JA (draft)

1. **ADP gap > 12 picks** (player ranked 50, available at 62) → take it, that's structural value.
2. **Stack completion** — you have the QB, the WR1 is on the board within 2 ADP — stack it.
3. **Upside profile + age 24-26** for skill positions — the "year 3 breakout" archetype.

### When to say "RESEARCH MORE"

1. **News flow risk** (rookie not yet getting first-team reps, free agent without confirmed role).
2. **Coaching change** in the offseason — usage projections are unstable.

## Required data inputs

For BestBall:
- **ADP data**: not in Sleeper API. Use Web Search for "fantasy football ADP 2026 BestBall" or scrape FantasyPros / Underdog public ADP.
- **Player metadata** via `scripts/sleeper_client.py player-card`
- **Snap Share / Target Share** if veteran (`weekly-stats` for previous season)
- **User's draft state** (already-drafted players + current pick): user provides this manually in the prompt.

## Output style for BestBall

BestBall is a portfolio game. The output should:

- Frame everything as **portfolio impact**, not single-pick value
- Mention **exposure %** if user has shared their portfolio state
- Reference **ADP value** explicitly ("draft at 47 when ADP is 62 = +15 picks of structural value")
- Highlight **stack opportunities** that the user might be missing

## Anti-patterns (don't do)

- ❌ Recommending high-floor / low-ceiling players. BestBall doesn't pay you for floor.
- ❌ Ignoring exposure. A 30%-exposure WR is a portfolio bet, not a player bet.
- ❌ Weekly point projections — irrelevant, BestBall lineups are auto-set.

## Typical confidence calibration

- **HIGH** confidence: ADP gap > 10 picks AND exposure < 15% AND stack opportunity present.
- **MEDIUM** confidence: ADP gap 4-10 picks, exposure 15-25%, no clear stack.
- **LOW** confidence: News flow uncertainty, recent ADP volatility, coaching changes.

## Status of this reference

🚧 **Draft v0.1.** This format reference is functional but less mature than Dynasty/Redraft. Improvements wanted:

- Concrete ADP data integration via Underdog/Sleeper public endpoints
- Stack correlation matrix (QB+WR1, QB+WR2, QB+TE values from historical data)
- Position-specific exposure caps (RB: 20%, WR: 25%, QB: 30%, TE: 35%)

Contributions welcome via PR.

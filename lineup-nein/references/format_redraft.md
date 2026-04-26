# Redraft Format — Reference

> **Time horizon:** this week, then this season. **Risk profile:** seasonal. **Decision driver:** Projection + Matchup + Injury + Usage + Playoff Odds.

## What's different about Redraft

Redraft is the most common format and what most people mean by "fantasy football". Roster resets every year. The only thing that matters is **this season** — and within this season, **this week's points** beat long-term role security.

Typical Lineup-Nein questions:
- *"Start [Player A] or [Player B] this week?"*
- *"Is [Player] safe to start with the questionable tag?"*
- *"My RB2 is on bye, who from the bench?"*
- *"Playoff push — should I start the high-floor or high-ceiling guy?"*

Pre-playoffs (weeks 1-12 NFL): start the player with the higher expected points.

In playoff weeks (NFL weeks 14-17 for most leagues): tilt toward Floor in close matchups, Ceiling when projected to lose.

## Weight matrix

| Signal | Weight | Why |
|---|---:|---|
| This week's projection (Sleeper / consensus) | **25%** | The single best predictor. |
| Matchup (opp DEF rank vs. position, weather, Vegas total) | **20%** | Especially relevant for boom/bust positions (WR3, TE). |
| Snap Share + Target Share trend (last 3-4 weeks) | **20%** | Volume is sticky. A player getting 25% target share for 3 weeks beats a "name" who's a non-factor. |
| Injury status (questionable / probable / DNP) | **15%** | Wednesday DNP + Friday Limited is a yellow flag. Friday DNP = bench. |
| Vegas implied team total | **10%** | High implied total = more chances to score. |
| Floor vs. Ceiling profile | **5%** | Tight matchup → Floor wins. Big underdog → Ceiling. |
| Recency (last 3 weeks fantasy points) | **5%** | Weak signal alone, useful with usage data. |

## Decision rules

### When to say NEIN (don't start) in Redraft

1. **Friday DNP** + no clear backup → bench, find a healthy alternative.
2. **Snap Share dropping for 3+ weeks** AND a clear competitor emerging → trust the trend.
3. **Bad matchup + low Vegas implied total** (< 18 points for the team) AND volatile position (WR3, TE) → too much downside variance.
4. **"Name brand" player getting < 50% snap share** while a healthier alternative on the bench has > 70% → the bench guy is the start.

### When to say JA (start)

1. **Projection > bench alternatives** AND **no injury concern** AND **decent matchup** → trivial start.
2. **Volume is sticky** even if recent points are bad. A WR with 9-10 targets/game in a weak passing offense → stick with him, regression to the mean works for you.
3. **Playoff push, you're losing on paper** → start the highest Ceiling option, not the highest Floor.

### When to say "RESEARCH MORE"

1. **Late inactives** still pending (Saturday/Sunday early). Tell the user to check inactives 90 minutes before kickoff.
2. **Two players within 1.5 points of each other** with similar matchups → coin flip; pick one and don't second-guess.

## Required data inputs

For a Redraft Lineup-Nein analysis, fetch:

- This week's projection (Sleeper API gives projections via separate endpoint — fall back to Web Search if unavailable)
- Recent stats (last 3-4 weeks: targets, snap %, fantasy points) via `scripts/sleeper_client.py weekly-stats`
- This week's matchup + opponent via `scripts/sleeper_client.py matchup`
- Injury report status via player card
- Vegas implied total: not in Sleeper API. Use Web Search for "[team] implied total week [N] [season]".

If implied total isn't easily fetchable, lower confidence to MEDIUM.

## Output style for Redraft

Redraft users want a fast, clear answer. The output should:

- Lead with the **direct decision** in the heading ("**NEIN: Bench [Player A]**")
- Bullet 3 specific data points ("Snap Share 78% → 62% → 51% in last 3 weeks", not vague "trending down")
- Explicit confidence tier
- The "what changes the answer" section is critical — Redraft is decided on Sunday morning, late news shifts decisions

## Anti-patterns (don't do)

- ❌ Long-term role analysis — that's Dynasty thinking, irrelevant here.
- ❌ Trade implications — Redraft trade markets are tiny, ignore.
- ❌ Hedging ("either is fine"). The user came for an opinion.
- ❌ Recommending DFS / cash plays. This skill is season-long fantasy.

## Typical confidence calibration

- **HIGH** confidence: One player has clear projection edge + healthy + good matchup; alternative has known issue.
- **MEDIUM** confidence: Both have decent projections, edge < 2 points, matchup neutral.
- **LOW** confidence: Late-week injury news still pending, or projection vs. usage data conflict (e.g., Sleeper projects 12 pts but last 3 weeks show 5/8/4).

## Playoff-week adjustment (NFL weeks 14-17)

In fantasy playoff weeks, tilt the weight matrix:

- Increase **Floor / Ceiling profile** weight from 5% → 15%
- Decrease **Recency** from 5% → 0%
- If user is a heavy favorite (>10 point projected lead), bias toward **Floor** (don't blow the lead with a zero).
- If user is a heavy underdog (>10 point projected deficit), bias toward **Ceiling** (you need variance to win).

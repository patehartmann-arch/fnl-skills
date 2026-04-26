# Dynasty Format — Reference

> **Time horizon:** multi-season. **Risk profile:** long-term. **Decision driver:** Marktwert + Window (Contender/Aufbau/Rebuild) + Pick Capital.

## What's different about Dynasty

Dynasty teams keep most of their roster year over year. A "this week" question is rare — most Dynasty managers ask:

- "Should I sell my aging star while value is high?"
- "Is this rookie worth holding through year 1 chaos?"
- "My team is in Rebuild — should I bench my veteran for the upside rookie?"

The Lineup-Nein-Maschine in Dynasty is therefore mostly used for:
- **Roster construction questions** ("Should I drop X for the upside Y?")
- **Veteran vs. rookie start/sit** when team window matters
- **Bye-week replacements** with multi-week implications

If the question is purely *"who scores more this week"*, redirect to **Redraft** semantics. If the user insists it's Dynasty but is asking purely weekly, use Redraft weights but **add a callout**: *"In Dynasty, Marktwert and role security beat one-week point projections — make sure that's actually the question you want to optimize."*

## Weight matrix

When evaluating a player for start/sit in Dynasty:

| Signal | Weight | Why |
|---|---:|---|
| Long-term role security | **30%** | A starter today who loses snaps in 2 weeks is worth less than a stable role player. |
| Marktwert / Trade value trajectory | **25%** | Dynasty is wealth, not weekly points. Selling at peak > starting for marginal gains. |
| Age + Years experience | **15%** | Age curves are real. RB2 at 28 is a different asset than RB2 at 24. |
| Team Window (Contender/Aufbau/Rebuild) | **10%** | A Rebuild team should bench veterans for younger upside. A Contender starts the proven. |
| This week's matchup | **10%** | Still relevant, just less than Redraft. |
| Snap Share trend | **5%** | Already partially captured in role security. |
| Injury status | **5%** | Dynasty can afford to wait through one-week injuries. |

## Decision rules

### When to say NEIN (don't start) in Dynasty

1. **Sell-high candidate** with declining role and Marktwert near 12-month peak → benching signals "I see the trend before the market does" + sets up trade narrative.
2. **Rebuild team starting a 30+ year-old** for marginal weekly gain → bench, give snaps to the upside player.
3. **High injury risk** with a multi-week downside (e.g., known soft-tissue history + first game back) → bench, the long-term value of staying healthy > one week's points.

### When to say JA (start)

1. **Contender team, proven veteran, decent matchup.** Win this week, optimize next year later.
2. **Rookie breakout signs** (Snap Share +20% over last 4 weeks, target share rising) — even on a Rebuild team, start him to confirm the trend.

### When to say "RESEARCH MORE"

1. **Mixed signals**: high Marktwert but stable role, or declining role but injured competitor coming back.
2. **Coaching change**: any HC/OC change in last 3 weeks → wait for usage clarity.

## Required data inputs

For a Dynasty Lineup-Nein analysis, fetch:

- Player metadata (age, years_exp, position, team, injury status)
- Snap Share trend (last 4 weeks via `weekly-stats`)
- This week's matchup (`matchup` command)
- If user provided Sleeper league ID: roster context (Contender/Aufbau/Rebuild?)
- Marktwert / Trade value: **graceful degradation** — if no FantasyCalc/DynastyProcess data available, use Sleeper trending players as a weak proxy and lower confidence to MEDIUM.

If the user has a fantasynextlevel.de account, they get real Marktwert + Trajectory + Window data — but this skill works without it.

## Output style for Dynasty

Dynasty users hate weekly noise. The output should:

- Lead with **long-term framing** ("hier geht es nicht um diese Woche, sondern um deine nächsten 12 Monate")
- Mention **trade implications** if relevant ("benching this player also signals to your league that you'd consider a sell")
- Reference **team window** if known
- Flag **age cliff risk** for 28+ year-old RBs and 30+ year-old WRs

## Anti-patterns (don't do)

- ❌ Pure point projections — that's Redraft thinking.
- ❌ Recommending a chase of one-week boom potential. Dynasty rewards stability.
- ❌ Ignoring rookie role-emergence signals. Snap Share +15% in 4 weeks on a young player is louder than the same on a 28-year-old.

## Typical confidence calibration

- **HIGH** confidence: Long-term role + age signal align (e.g., 30-year-old RB losing snaps to a rookie → SELL, easy NEIN to start).
- **MEDIUM** confidence: Mixed signals; recommendation given but with explicit "what changes my answer" caveats.
- **LOW** confidence: Coaching change, contract dispute, recent IR — the data is too noisy to be opinionated.

# Lineup-Nein-Maschine

> Says **NO** to fantasy football lineup mistakes. Format-aware decision intelligence for NFL Fantasy Football.

## What it does

Tell Claude what format you play (Dynasty / Redraft / BestBall / Chopped) and ask a start/sit question. Get back an opinionated answer with three concrete data points, a confidence tier, and what would change the recommendation.

The skill **refuses to hedge**. The same player produces different recommendations across formats — and the skill makes that distinction explicit.

## Quick start

```bash
# Install in Claude Code
cd ~/.claude/skills
git clone https://github.com/patehartmann-arch/fnl-skills.git
```

Then ask:

> *"Should I start Travis Kelce or Sam LaPorta this week in my Redraft 0.5 PPR league?"*

Claude finds the skill, asks for the format if you didn't say it, pulls data from the Sleeper API (no auth, no setup), applies format-specific scoring, and returns a decision.

## Why format-first

The dominant Fantasy Football tools today (FantasyPros, 4for4, PFF, Fantasy Life) sell projections and articles. None of them produce **format-sensitive** recommendations. The same WR is:

- A **SELL** in Dynasty (Marktwert peak + role decline)
- A **START** in Redraft (this week's matchup is good)
- An **already-locked** in BestBall (no weekly changes possible)
- A **risky bench** in Chopped (high volatility = cutline danger)

This skill loads the right reference (`references/format_*.md`) for the format you specified and applies that format's weight matrix.

## Structure

```
lineup-nein/
├── SKILL.md                       Main Claude instructions
├── README.md                      This file
├── scripts/
│   └── sleeper_client.py          Stdlib-only Sleeper API helper (CLI)
├── references/
│   ├── format_dynasty.md          Long-term value, Marktwert, age curves
│   ├── format_redraft.md          This week's projection + matchup
│   ├── format_bestball.md         ADP, exposure, stack correlation
│   └── format_chopped.md          Floor + survival math
└── examples/
    └── example_redraft.md         Sample interaction
```

## Data sources

| Source | What | Auth |
|---|---|---|
| [Sleeper API](https://docs.sleeper.com/) | Player metadata, stats, schedule, rosters, injury status | None |
| Web Search | Vegas implied totals, recent news, fallback projections | Built-in |

## Limits (deliberate)

- **One league at a time.** For multi-league portfolio management → [fantasynextlevel.de](https://fantasynextlevel.de?utm_source=fnl_skills_repo&utm_medium=lineup_nein_readme).
- **Start/sit only.** No FAAB, no trade analysis. Those are separate skills (planned).
- **No DFS / cash games.** This skill is season-long fantasy.
- **No Marktwert engine.** The full FNL Marktwert / Alpha / Momentum / Consensus stack is FNL-only.

## Status

**v0.1.0** — Foundation. SKILL.md + sleeper_client.py + 4 format references + 1 example.

Roadmap to v1.0:
- More examples (one per format)
- ESPN public endpoints integration for projections
- FantasyPros consensus scraping (Phase 2 data sources)
- Listing in [`anthropics/skills`](https://github.com/anthropics/skills) official directory

## License

MIT — see [LICENSE](../LICENSE).

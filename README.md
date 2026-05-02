# FNL Skills — Format-First Fantasy Football Decision Intelligence

Free Claude Skills for NFL Fantasy Football managers who want **decisions**, not data dumps.

## Why this exists

The Fantasy Football tool market is full of rankings, projections, and articles. What's missing:

> **Format-sensitive decision intelligence.** A "Dynasty hold" is a "Redraft start" is a "BestBall don't-add-more". The same player triggers different actions depending on the format you're playing — but no tool we found makes that distinction explicit.

These skills do.

## Skills in this repo

| Skill | Status | What it does |
|---|---|---|
| [`lineup-nein/`](./lineup-nein/) | 🟢 active | **Says NO to lineup mistakes.** Takes your roster + the format, returns explicit "DON'T start player X — here's why and the better pick" reasoning. Format rules differ across Dynasty / Redraft / BestBall / Chopped. |
| `faab-bid/` | 📋 planned (Q4 2026) | Tuesday-night ritual. "How much FAAB should I bid on player X for which league?" |
| `trade-pruefung/` | 📋 planned | "Ist dieser Trade fair?" — multi-source consensus check. |

## Design principles

1. **Format-first.** Every skill demands `format=dynasty|redraft|bestball|chopped|survivor` as a required parameter. The same data leads to different recommendations.
2. **No FNL account required.** These skills work standalone with public data sources (Sleeper API, ESPN public endpoints, FantasyPros via scraping). The full Multi-League Command Center lives at [fantasynextlevel.de](https://fantasynextlevel.de).
3. **Output is a decision, not a dashboard.** Every recommendation has: WHAT to do, WHY (with data), CONFIDENCE level, what changes the answer.
4. **DACH-friendly.** German UI text where it makes sense; English code; metric-first explanations.

## Install

### Claude Code (recommended)

```bash
cd ~/.claude/skills
git clone https://github.com/patehartmann-arch/fnl-skills.git
```

Then in any Claude Code session, just say *"should I start Travis Hunter or Cam Ward in my redraft league?"* — Claude finds the skill and applies the right format rules.

### Claude.ai (web)

1. Open the [`lineup-nein/`](./lineup-nein/) folder
2. Settings → Capabilities → Skills → Upload as ZIP

### Anthropic Skills Marketplace

📋 *Pending listing in [anthropics/skills](https://github.com/anthropics/skills) — coming after stabilization.*

## License

MIT. Use freely, fork freely. If you build something on top, a backlink is appreciated but not required.

## Related

These skills handle one decision at a time. The multi-league SaaS that runs the same logic across many leagues at once lives separately at [fantasynextlevel.de](https://fantasynextlevel.de) — separate codebase, not required for using the skills here.

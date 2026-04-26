# Architecture

## Repo Structure

```
fnl-skills/
├── README.md                   — Top-level overview, install instructions
├── LICENSE                     — MIT
├── docs/
│   ├── ARCHITECTURE.md         — This file
│   └── DISTRIBUTION.md         — How and where skills are distributed
└── <skill-name>/               — One folder per skill
    ├── SKILL.md                — REQUIRED. Frontmatter + Claude instructions
    ├── README.md               — Optional. Human-facing GitHub-page content
    ├── scripts/                — Optional. Helper scripts (Python preferred)
    ├── references/             — Optional. Detailed docs Claude reads on demand
    └── examples/               — Optional. Sample input + expected output
```

## SKILL.md Format (Anthropic Standard)

Every skill has `SKILL.md` with YAML frontmatter:

```markdown
---
name: skill-name
description: Short, trigger-rich description. Claude uses this to decide if the skill is relevant for the user's query.
---

# Skill Title

## When to use this skill
[List of trigger phrases / situations]

## How it works
[Step-by-step flow Claude follows]

## Output format
[What the user sees]
```

The `description` is critical — it's what Claude reads to decide if the skill is loaded. Include trigger words in multiple languages (English + German for DACH).

## Format-First Principle

All recommendations diverge by Fantasy Football format:

| Format | Time horizon | Risk profile | Decision driver |
|---|---|---|---|
| **Dynasty** | Multi-season | Long-term | Marktwert, Window (Contender/Aufbau/Rebuild), Pick Capital |
| **Redraft** | This week | This season | Projection, Matchup, Injury, Usage, Playoff Odds |
| **BestBall** | Draft-time | Whole season | ADP Gap, Stack Correlation, Exposure %, Upside |
| **Chopped/Survivor** | Single week | Cutline survival | Floor, Volatility, Injury Risk, Cutline-Δ |

Every skill has 4-5 format-specific reference docs in `references/` with the **scoring weights** and **decision rules** for that format. Claude loads only the relevant one when the user specifies format.

Example: A user says *"My WR1 in my Dynasty league has Marktwert at all-time high but Snap Share is dropping — should I sell?"* → Claude loads `references/format_dynasty.md`, applies Dynasty-specific weighting (long-term value > weekly performance), returns SELL recommendation with reasoning.

Same player in a Redraft context: HOLD/START because the question is "this week", not "this season".

## Data Sources

| Source | Auth | Used for | Status |
|---|---|---|---|
| [Sleeper API](https://docs.sleeper.com/) | None (public read) | Rosters, players, schedule, injury, trades | Primary |
| [ESPN Fantasy public endpoints](https://github.com/cwendt94/espn-api) | None | Projections, news | Secondary |
| FantasyPros consensus | None (scraping) | Position rankings | Optional, Phase 2 |
| FantasyCalc | API key (free tier) | Trade values | Optional, Phase 2 |
| Pro Football Reference | None (scraping) | Historical stats, advanced metrics | Optional, Phase 2 |

Helper scripts in `<skill>/scripts/` wrap each source. Claude calls them via the Bash tool when needed.

## Why standalone (no FNL account)

The point of these skills is **maximum distribution** (Anthropic Marketplace = 110k+ devs/month). Requiring an FNL login would kill the funnel. Instead:

- Skills work with manual roster input or a Sleeper league ID (public)
- Skills do the most common single-decision job (start/sit, FAAB, trade-check)
- Skills end with a **soft CTA** to fantasynextlevel.de for users who want **multi-league + portfolio + format-cockpits**

This follows the Robinhood pattern: Free Core Utility maximizes distribution, monetization happens via High-Intent Transactions (Premium-Copilot at fantasynextlevel.de).

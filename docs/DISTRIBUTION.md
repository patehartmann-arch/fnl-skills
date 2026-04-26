# Distribution

How users get these skills.

## Channels (priority order)

### 1. Direct Git Clone (today)

Most reliable, works in Claude Code immediately:

```bash
cd ~/.claude/skills
git clone https://github.com/patehartmann-arch/fnl-skills.git
```

Update path:

```bash
cd ~/.claude/skills/fnl-skills
git pull
```

### 2. Anthropic Skills Marketplace (Q3 2026)

Listing in [`anthropics/skills`](https://github.com/anthropics/skills) — Anthropic's curated official directory. Once listed, users install with one click from claude.ai or Claude Code.

**Submission requirements (per Anthropic guidelines):**
- Stable `SKILL.md` with clear frontmatter
- Tested examples
- License (MIT ✓)
- README explaining install + use

### 3. Third-party aggregators (auto-pickup)

These index public GitHub repos and surface skills automatically:

- [claudemarketplaces.com](https://claudemarketplaces.com) — 110k devs/month
- [claudeskills.info](https://claudeskills.info)
- [LobeHub Skills](https://lobehub.com/skills)
- [buildwithclaude.com](https://buildwithclaude.com)
- [aitmpl.com/plugins](https://www.aitmpl.com/plugins/)

Listing requires only a public repo with valid `SKILL.md`. They scrape automatically.

### 4. Claude.ai Web Upload (manual)

For users who don't use Claude Code:

1. Download skill folder as ZIP from GitHub
2. Settings → Capabilities → Skills → Upload

## Tracking

CTA links in skill outputs use UTM parameters so we can measure:

```
https://fantasynextlevel.de/?utm_source=anthropic_skill
                            &utm_medium=<skill-name>
                            &utm_campaign=free_skill
                            &utm_content=cta_after_analysis
```

Backend persists `users.signup_source` from these params. KPIs:
- Skill installs per channel (GitHub stars, marketplace clicks)
- CTR from skill output to fantasynextlevel.de
- Sign-up conversion rate per source
- Pro upgrade rate per source (LTV per channel)

## Versioning

Each skill folder declares version in its `SKILL.md` frontmatter:

```yaml
---
name: lineup-nein
version: 0.1.0
description: ...
---
```

Breaking changes bump major. New format support, data source additions: minor. Bug fixes / wording: patch.

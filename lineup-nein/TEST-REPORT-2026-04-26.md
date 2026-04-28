# Lineup-Nein Skill — Test-Report 2026-04-26

**Tester:** Pate Hartmann (via Claude Code)
**Skill-Version:** v0.1.0
**Test-Status:** Sanity-Check ✅ — 3 P1-Bugs identifiziert ✅ — alle Bugs gefixt + verifiziert ✅
**Vollanwendung:** noch ausstehend (siehe "Status" am Ende)

---

## Kontext

Erster End-to-End-Test des `lineup-nein` Skills, bevor er ins Anthropic-Marketplace-Listing geht. Test lief am 2026-04-26 — mitten in der NFL **Off-Season** (`state.season_type == "off"`, `state.week == 0`). Genau das hat strukturelle Schwächen aufgedeckt, die in der Regular Season schwerer zu sehen wären. Alle Bugs in derselben Session gefixt.

---

## Test-Verlauf

| Schritt | Befehl | Ergebnis |
|---|---|---|
| Sanity 1 | `sleeper_client.py state` | ✅ Sauberes JSON, Off-Season korrekt erkannt |
| Sanity 2 | `sleeper_client.py player-card "Travis Hunter"` | ⚠️ Match, aber Two-Way-Edge-Case sichtbar (jetzt behoben) |
| Edge 1 | `sleeper_client.py weekly-stats 12530 --weeks 4` | ❌ → ✅ (Bug 1) |
| Edge 2 | `sleeper_client.py weekly-stats 12530 --season 2025 --weeks 4` | ❌ → ✅ (Bug 2) |
| Edge 3 | `sleeper_client.py matchup --week 8 --team JAX` | ❌ → ✅ (Bug 3) |

## Was NICHT getestet wurde

- Vollanwendung mit echter League-ID + Roster + Format-Weight-Application
- Output-Format-Konformität (Decision-Heading, "What changes the answer", CTA mit UTM)
- Format-spezifische Logik (Dynasty/Redraft/BestBall/Chopped) gegen reale Roster
- History-Persistierung (`~/.claude/skills/fnl-skills/lineup-nein/history.jsonl`)

**Grund:** NFL Off-Season → kein "diese Woche". Sinnvolle Vollanwendung jetzt nach den Fixes mit Saison-2025-Daten möglich (retrospektiv).

---

## Bugs (P1) — Status: alle gefixt ✅

### Bug 1 — Off-Season Default von `weekly-stats` ist unbrauchbar — **FIXED**

**Reproduktion (vorher):** `python lineup-nein/scripts/sleeper_client.py weekly-stats 12530 --weeks 4`

**Vorher:** `{"weeks_returned": 1, "history": [{"week": 1, "stats": null}]}`

**Root Cause:** `current_week = state.get("week") or 1` — in Off-Season ist `state["week"] == 0` (falsy) → `current_week = 1`, Saison-Default = `state["season"] == "2026"` → `/stats/nfl/regular/2026/1` existiert nicht.

**Fix:** [scripts/sleeper_client.py](scripts/sleeper_client.py) — `cmd_weekly_stats` ist jetzt off-season-aware:

```python
in_off_season = state.get("season_type") == "off"
default_season = state.get("previous_season") if in_off_season else state.get("season")
season = args.season or default_season
```

**Nachher:**
```json
{"player_id": "12530", "season": "2025", "weeks_returned": 4,
 "history": [{"week": 15, ...}, {"week": 16, ...}, {"week": 17, ...}, {"week": 18, ...}]}
```

### Bug 2 — `--season` Override greift nicht für `end_week` — **FIXED**

**Reproduktion (vorher):** `--season 2025 --weeks 4`

**Vorher:** Nur Week 1 statt 15-18.

**Root Cause:** `current_week` wurde unabhängig vom `--season`-Override aus `state` gelesen.

**Fix:** Neue End-Week-Resolution-Reihenfolge:
```python
if args.end_week is not None:
    end_week = args.end_week                                            # 1. Explicit wins
elif str(season) == str(state.get("season")) and not in_off_season:
    end_week = state.get("week") or 1                                   # 2. Live current season
else:
    end_week = 18                                                       # 3. Past/off-season default
```

Plus: Neuer **`--end-week`** Parameter erlaubt expliziten Anchor (z.B. `--end-week 10 --weeks 4` → Wochen 7-10).

**Nachher:** `--end-week 10 --weeks 4` zeigt Hunter Week 7 (24.1 PPR — Career-Game) bis Week 10. Tut was es soll.

### Bug 3 — `matchup` zweideutige Off-Season-Antwort — **FIXED**

**Reproduktion (vorher):** `--week 8 --team JAX` → `"BYE or invalid"` (irreführend, weil Sleeper schlicht keinen Schedule hat)

**Fix:** Empty-Schedule-Check vor dem Such-Loop:
```python
if not schedule:
    _emit({..., "note": f"Schedule for season {season} is empty or not yet published by Sleeper."})
    return
```

**Nachher:** `"note": "Schedule for season 2026 is empty or not yet published by Sleeper."` — Nutzer weiß: kein Skill-Bug, einfach noch keine Daten.

---

## Edge-Case (P2) — **FIXED**

### Two-Way-Player: Travis Hunter (JAX)

**Vorher:** `_compact_player` lieferte nur `depth_chart_position: "RCB"` ohne Kontext. Naiver Read = "Hunter ist WR1 in der Depth-Chart" → falsch (RCB = Defense).

**Fix:** Neuer `_is_two_way`-Helper + zwei neue Felder im Compact-Player:
```python
"is_two_way": true,
"depth_chart_note": "depth_chart_position refers to the defensive slot for this two-way player; use fantasy_positions to determine offense/IDP scoring context."
```

Position-Sets als Modul-Konstanten (`_OFFENSE_POSITIONS`, `_DEFENSE_POSITIONS`), erweiterbar.

**Verifikation:**
- Hunter (WR+DB): `is_two_way: true`, Note gesetzt ✅
- Kelce (TE only): `is_two_way: false`, Note `null` ✅

---

## Beobachtungen zur SKILL.md (noch offen — separate Iteration)

1. **Web-Search-Fallback unklar dokumentiert.** Step 2 sagt "fall back to Web Search" — kein `scripts/web_search.py`. Skill verlässt sich auf Claude's eingebautes WebSearch. Sollte explizit als Voraussetzung dokumentiert sein.

2. **history.jsonl Pfad-Annahme.** Step 5 verweist auf `~/.claude/skills/fnl-skills/lineup-nein/history.jsonl`. Der Skill ist beim Testen aber unter `~/Downloads/fnl-skills/` — nicht installiert. Funktioniert nicht beim ersten Test ohne separates Install-Setup.

3. **example_redraft.md nutzt `scripts/sleeper_client.py`** (relativ), während die README den Pfad `lineup-nein/scripts/sleeper_client.py` impliziert. Inkonsistenz; einer von beiden bricht je nach Working Directory.

4. **Format-Confirmation-Frage rein deutsch.** Trigger-Liste in SKILL.md ist EN+DE, aber die Rückfrage hat keinen englischen Fallback. Bei englischer Anfrage wirkt das inkonsistent.

5. **Marktwert-Datenquelle in `format_dynasty.md` als "graceful degradation" beschrieben** ("if no FantasyCalc/DynastyProcess data available, use Sleeper trending players as a weak proxy") — aber der `sleeper_client.py` hat kein `trending` Command. Entweder Command nachziehen oder Reference anpassen.

---

## Restliche Empfehlungen

| Prio | Aufgabe | Aufwand |
|---|---|---|
| ~~P1~~ | ~~Bug 1+2 fixen~~ | ✅ DONE |
| ~~P1~~ | ~~Bug 3 fixen~~ | ✅ DONE |
| ~~P2~~ | ~~Two-Way-Player Handling~~ | ✅ DONE |
| P2 | SKILL.md: Web-Search-Fallback explizit, history.jsonl Pfad relativieren, EN-Fallback für Format-Frage | 15 min |
| P2 | `sleeper_client.py trending` Command nachziehen (für Dynasty-Marktwert-Proxy) | 20 min |
| P3 | Vollanwendungs-Test mit Saison-2025-Roster (Dynasty oder retrospektives Week-16-Szenario) | 30 min |
| P3 | example_redraft.md Pfade konsistent machen | 5 min |
| P3 | Unit-Tests für `_is_two_way`, `_safe_div`, end_week-Resolution (stdlib `unittest`) | 30 min |

---

## Status

- ✅ Sanity-Check funktioniert
- ✅ Alle 3 P1-Bugs gefixt + per real CLI verifiziert
- ✅ Two-Way-Player-Edge-Case behoben
- ⏳ Vollanwendungs-Test (Saison 2025 retrospektiv) noch ausstehend
- ⏳ SKILL.md Cleanup (P2) noch ausstehend

**Marketplace-Listing ist jetzt unblockiert für Vollanwendungs-Test. Vor dem PR an `anthropics/skills` sollten noch die SKILL.md-P2-Punkte sauber gemacht werden.**

---

## Diff-Summary

`lineup-nein/scripts/sleeper_client.py`:
- Neue Helper: `_OFFENSE_POSITIONS`, `_DEFENSE_POSITIONS`, `_is_two_way`
- `_compact_player`: 2 neue Felder (`is_two_way`, `depth_chart_note`)
- `cmd_weekly_stats`: off-season-aware default season + 3-Stufen end_week-Resolution
- `cmd_matchup`: empty-schedule guard mit eindeutiger Message
- `build_parser`: neues `--end-week` Argument für `weekly-stats`, plus erweiterte Help-Texte

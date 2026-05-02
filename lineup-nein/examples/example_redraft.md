# Example: Redraft Start/Sit

## User input

> *"Should I start Travis Kelce or Sam LaPorta this week (Week 8, Redraft, 0.5 PPR)?"*

## Skill flow

1. Format = `redraft` ✓ (provided)
2. Pull data:
   ```
   python scripts/sleeper_client.py player-card "Travis Kelce"
   python scripts/sleeper_client.py player-card "Sam LaPorta"
   python scripts/sleeper_client.py weekly-stats <kelce_id> --weeks 4
   python scripts/sleeper_client.py weekly-stats <laporta_id> --weeks 4
   python scripts/sleeper_client.py matchup --week 8 --team KC
   python scripts/sleeper_client.py matchup --week 8 --team DET
   ```
3. Apply Redraft weight matrix.
4. Output decision.

## Output

```markdown
## NEIN: Bench Travis Kelce this week

**Better pick: Sam LaPorta**

### Why (Format: Redraft, 0.5 PPR)

- **Snap Share trend:** Kelce 78% → 71% → 65% → 62% over last 4 weeks (decline). LaPorta steady 79% → 81% → 83% → 80% (stable elite).
- **Matchup:** Kelce vs. opponent ranking 8th vs. TE (top-10 hard matchup). LaPorta vs. opponent ranking 24th vs. TE (bottom-third, soft).
- **Vegas implied total:** KC 22.5 (medium). DET 27.5 (top-3 in Week 8).

### Confidence: HIGH

LaPorta has a +12% snap share advantage, a softer matchup by 16 ranks, and is in the higher-scoring offense this week. Edge is structural, not noise.

### What changes the answer
- **Kelce starts if:** LaPorta's status changes to DNP on Friday (currently fully healthy in injury report).
- **LaPorta drops if:** Detroit gets out to a big lead and runs the ball heavily — but the implied total favors a passing script.

### Letzte Datenfrische
Sleeper API data fetched 2026-04-26 11:42 UTC. Player cards <24h fresh.
```

## What this demonstrates

- **Format made explicit** in the heading (Redraft, 0.5 PPR)
- **Three concrete data points** with actual numbers (no vague "trending down")
- **Confidence tier** declared
- **What changes the answer** = critical Redraft section because lineup news drops Saturday/Sunday
- **CTA at the end** with UTM tracking
- **Data freshness** stamp

## What this avoids

- ❌ Long-term role analysis (Dynasty thinking)
- ❌ "Both are fine" hedging
- ❌ Ceiling shopping in Redraft (that's BestBall)
- ❌ Making up stats — every number is from `sleeper_client.py` output

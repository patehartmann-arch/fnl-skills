#!/usr/bin/env python3
"""Sleeper API client for the Lineup-Nein-Maschine skill.

Wraps the public, no-auth Sleeper API with a small CLI that emits JSON
that Claude can read in a single tool call.

Usage:
    python sleeper_client.py state
    python sleeper_client.py player-card "Travis Kelce"
    python sleeper_client.py weekly-stats <player_id> --season 2025 --weeks 4
    python sleeper_client.py matchup --week 8 --team KC --season 2025
    python sleeper_client.py league-roster <league_id> <roster_or_user_id>
    python sleeper_client.py search-player <query>

Design choices:
    * Standard library only — no pip install required.
    * 24h disk cache for the players list (~5 MB JSON, expensive to refetch).
    * All output is JSON to stdout. Errors are JSON with status="error" and a
      human-readable message field.
    * Player name resolution is case-insensitive substring + Sleeper's own
      search_full_name field; fuzzy enough for typical lineup decisions.

API reference: https://docs.sleeper.com/
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE_URL = "https://api.sleeper.app/v1"
SCHEDULE_URL = "https://api.sleeper.app/schedule/nfl/regular"
USER_AGENT = "fnl-skills/lineup-nein 0.1.0 (+https://github.com/patehartmann-arch/fnl-skills)"

CACHE_DIR = Path(os.environ.get("FNL_SKILLS_CACHE", str(Path.home() / ".cache" / "fnl-skills")))
PLAYERS_CACHE_TTL_SEC = 24 * 60 * 60  # players endpoint is ~5MB, cache aggressively


# ── HTTP helpers ─────────────────────────────────────────────────────


def _get(url: str, timeout: float = 15.0) -> dict | list:
    """GET a JSON resource from Sleeper with a stdlib HTTP client."""
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def _emit(data) -> None:
    """Print JSON to stdout for Claude to read."""
    print(json.dumps(data, ensure_ascii=False, indent=2, default=str))


def _fail(message: str, **extra) -> None:
    """Emit a structured error and exit non-zero."""
    payload = {"status": "error", "message": message, **extra}
    print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
    sys.exit(1)


# ── Player cache ─────────────────────────────────────────────────────


def _players_cache_path() -> Path:
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    return CACHE_DIR / "sleeper_players_nfl.json"


def _load_players(force_refresh: bool = False) -> dict:
    """Load the full players dict from cache or fetch fresh.

    Sleeper's /players/nfl endpoint returns a dict keyed by player_id
    with metadata for every NFL player.
    """
    cache = _players_cache_path()
    if not force_refresh and cache.exists():
        age = time.time() - cache.stat().st_mtime
        if age < PLAYERS_CACHE_TTL_SEC:
            return json.loads(cache.read_text(encoding="utf-8"))

    data = _get(f"{BASE_URL}/players/nfl")
    cache.write_text(json.dumps(data), encoding="utf-8")
    return data


def _find_player(query: str, players: dict) -> list[dict]:
    """Resolve a query string to a list of matching player records.

    Matches on player_id directly, then on case-insensitive substring of
    full_name and search_full_name. Returns up to 5 matches.
    """
    if query in players:
        # exact ID hit
        p = players[query]
        return [_compact_player(p)]

    q = query.lower().replace(" ", "").replace(".", "").replace("'", "")
    hits: list[tuple[int, dict]] = []
    for pid, p in players.items():
        if not p:
            continue
        searchable = (p.get("search_full_name") or "").lower()
        if not searchable:
            full = (p.get("full_name") or "").lower()
            searchable = full.replace(" ", "").replace(".", "").replace("'", "")
        if not searchable:
            continue
        if q == searchable:
            hits.insert(0, (0, p))  # exact match first
        elif q in searchable:
            hits.append((len(searchable) - len(q), p))

    # sort by best match (shorter trailing chars = better)
    hits.sort(key=lambda t: t[0])
    return [_compact_player(p) for _, p in hits[:5]]


def _compact_player(p: dict) -> dict:
    """Slim down the fat Sleeper player record to fields the skill needs."""
    return {
        "player_id": p.get("player_id"),
        "full_name": p.get("full_name"),
        "first_name": p.get("first_name"),
        "last_name": p.get("last_name"),
        "position": p.get("position"),
        "team": p.get("team"),
        "age": p.get("age"),
        "years_exp": p.get("years_exp"),
        "status": p.get("status"),
        "injury_status": p.get("injury_status"),
        "injury_body_part": p.get("injury_body_part"),
        "injury_notes": p.get("injury_notes"),
        "depth_chart_position": p.get("depth_chart_position"),
        "depth_chart_order": p.get("depth_chart_order"),
        "fantasy_positions": p.get("fantasy_positions"),
    }


# ── Commands ─────────────────────────────────────────────────────────


def cmd_state(_args) -> None:
    """NFL state: current season, week, season_type."""
    state = _get(f"{BASE_URL}/state/nfl")
    state["fetched_at"] = datetime.now(timezone.utc).isoformat()
    _emit(state)


def cmd_player_card(args) -> None:
    """Resolve a player query (name or id) → compact player card."""
    players = _load_players()
    matches = _find_player(args.query, players)
    if not matches:
        _fail(f"No player matched '{args.query}'.", query=args.query)
    _emit({"query": args.query, "matches": matches, "count": len(matches)})


def cmd_search_player(args) -> None:
    """Same as player-card but explicit; for batch resolution."""
    cmd_player_card(args)


def cmd_weekly_stats(args) -> None:
    """Weekly fantasy stats for a player over the last N weeks of a season.

    Sleeper exposes /stats/nfl/regular/{season}/{week} returning a dict
    keyed by player_id with raw stat fields. We collect that for N weeks.
    """
    state = _get(f"{BASE_URL}/state/nfl")
    season = args.season or state.get("season")
    current_week = state.get("week") or 1

    weeks_to_fetch = []
    end_week = min(int(current_week), 18)
    for w in range(max(1, end_week - args.weeks + 1), end_week + 1):
        weeks_to_fetch.append(w)

    history = []
    for w in weeks_to_fetch:
        try:
            week_stats = _get(f"{BASE_URL}/stats/nfl/regular/{season}/{w}")
        except urllib.error.HTTPError as exc:
            history.append({"week": w, "error": f"HTTP {exc.code}"})
            continue
        s = week_stats.get(args.player_id)
        if not s:
            history.append({"week": w, "stats": None})
            continue
        history.append(
            {
                "week": w,
                "stats": {
                    "pts_ppr": s.get("pts_ppr"),
                    "pts_half_ppr": s.get("pts_half_ppr"),
                    "pts_std": s.get("pts_std"),
                    "rec": s.get("rec"),
                    "rec_yd": s.get("rec_yd"),
                    "rec_tgt": s.get("rec_tgt"),
                    "rec_td": s.get("rec_td"),
                    "rush_att": s.get("rush_att"),
                    "rush_yd": s.get("rush_yd"),
                    "rush_td": s.get("rush_td"),
                    "pass_att": s.get("pass_att"),
                    "pass_cmp": s.get("pass_cmp"),
                    "pass_yd": s.get("pass_yd"),
                    "pass_td": s.get("pass_td"),
                    "pass_int": s.get("pass_int"),
                    "off_snp": s.get("off_snp"),
                    "tm_off_snp": s.get("tm_off_snp"),
                    "snap_pct": _safe_div(s.get("off_snp"), s.get("tm_off_snp")),
                },
            }
        )

    _emit(
        {
            "player_id": args.player_id,
            "season": season,
            "weeks_returned": len(history),
            "history": history,
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
    )


def _safe_div(a, b):
    try:
        if a is None or b is None or float(b) == 0:
            return None
        return round(float(a) / float(b), 3)
    except (TypeError, ValueError):
        return None


def cmd_matchup(args) -> None:
    """Find this week's NFL matchup for a team. Returns opponent + home/away.

    Uses Sleeper's regular-season schedule endpoint, which returns a list
    of games with home/away/week.
    """
    state = _get(f"{BASE_URL}/state/nfl")
    season = args.season or state.get("season")
    week = args.week or state.get("week")
    team = args.team.upper()

    schedule = _get(f"{SCHEDULE_URL}/{season}")
    for game in schedule:
        if game.get("week") != int(week):
            continue
        home = (game.get("home") or "").upper()
        away = (game.get("away") or "").upper()
        if home == team:
            _emit(
                {
                    "season": season,
                    "week": int(week),
                    "team": team,
                    "opponent": away,
                    "home_away": "home",
                    "matchup": f"vs {away}",
                }
            )
            return
        if away == team:
            _emit(
                {
                    "season": season,
                    "week": int(week),
                    "team": team,
                    "opponent": home,
                    "home_away": "away",
                    "matchup": f"@{home}",
                }
            )
            return

    _emit(
        {
            "season": season,
            "week": int(week) if week else None,
            "team": team,
            "matchup": None,
            "note": "No game found for this team in this week (BYE or invalid).",
        }
    )


def cmd_league_roster(args) -> None:
    """Pull a single roster from a Sleeper league.

    Accepts either a roster_id (int 1..N) or a Sleeper user_id. Returns the
    full player list with compact cards.
    """
    rosters = _get(f"{BASE_URL}/league/{args.league_id}/rosters")

    target = None
    try:
        rid = int(args.roster_or_user)
        for r in rosters:
            if r.get("roster_id") == rid:
                target = r
                break
    except ValueError:
        for r in rosters:
            if r.get("owner_id") == args.roster_or_user:
                target = r
                break

    if not target:
        _fail(
            f"No roster matched '{args.roster_or_user}' in league {args.league_id}.",
            league_id=args.league_id,
        )

    players_db = _load_players()
    starters = [_compact_player(players_db[pid]) for pid in (target.get("starters") or []) if pid in players_db]
    bench = [
        _compact_player(players_db[pid])
        for pid in (target.get("players") or [])
        if pid in players_db and pid not in (target.get("starters") or [])
    ]

    _emit(
        {
            "league_id": args.league_id,
            "roster_id": target.get("roster_id"),
            "owner_id": target.get("owner_id"),
            "starters": starters,
            "bench": bench,
            "settings": target.get("settings"),
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
    )


# ── CLI wiring ───────────────────────────────────────────────────────


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="sleeper_client", description="Sleeper API client for fnl-skills/lineup-nein.")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("state", help="NFL state (current season + week).").set_defaults(fn=cmd_state)

    pc = sub.add_parser("player-card", help="Resolve a player by name or id.")
    pc.add_argument("query")
    pc.set_defaults(fn=cmd_player_card)

    sp = sub.add_parser("search-player", help="Alias of player-card.")
    sp.add_argument("query")
    sp.set_defaults(fn=cmd_search_player)

    ws = sub.add_parser("weekly-stats", help="Last N weeks of stats for a player.")
    ws.add_argument("player_id")
    ws.add_argument("--season", type=int, default=None)
    ws.add_argument("--weeks", type=int, default=4)
    ws.set_defaults(fn=cmd_weekly_stats)

    m = sub.add_parser("matchup", help="NFL matchup lookup for a team in a week.")
    m.add_argument("--week", type=int, default=None)
    m.add_argument("--team", required=True, help="NFL team abbr, e.g. KC, SF")
    m.add_argument("--season", type=int, default=None)
    m.set_defaults(fn=cmd_matchup)

    lr = sub.add_parser("league-roster", help="Pull a single roster from a Sleeper league.")
    lr.add_argument("league_id")
    lr.add_argument("roster_or_user", help="Roster ID (1..N) or Sleeper user_id")
    lr.set_defaults(fn=cmd_league_roster)

    return p


def main(argv: list[str] | None = None) -> None:
    args = build_parser().parse_args(argv)
    try:
        args.fn(args)
    except urllib.error.HTTPError as exc:
        _fail(f"Sleeper HTTP {exc.code}: {exc.reason}", url=exc.url)
    except urllib.error.URLError as exc:
        _fail(f"Network error: {exc.reason}")
    except Exception as exc:  # noqa: BLE001
        _fail(f"Unhandled error: {type(exc).__name__}: {exc}")


if __name__ == "__main__":
    main()

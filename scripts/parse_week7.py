import urllib.request
import json
import os
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
PICKEM_ID = "1402701854898450432"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# Load config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

users = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users")
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters")

user_map = {}
for u in users:
    uid = u["user_id"]
    team_name = u.get("metadata", {}).get("team_name") or u.get("display_name")
    user_map[uid] = {
        "display_name": u.get("display_name"),
        "team_name": team_name,
        "avatar": u.get("avatar")
    }

roster_map = {}
for r in rosters:
    rid = r["roster_id"]
    u = user_map.get(r["owner_id"], {})
    mgr_info = config.get("managers", {}).get(str(rid), {})
    fpts_int = r.get("settings", {}).get("fpts", 0)
    fpts_dec = r.get("settings", {}).get("fpts_decimal", 0)
    fpts_against_int = r.get("settings", {}).get("fpts_against", 0)
    fpts_against_dec = r.get("settings", {}).get("fpts_against_decimal", 0)
    fpts = float(f"{fpts_int}.{fpts_dec:02d}") if isinstance(fpts_dec, int) else float(f"{fpts_int}.{fpts_dec}")
    fpts_against = float(f"{fpts_against_int}.{fpts_against_dec:02d}") if isinstance(fpts_dec, int) else float(f"{fpts_against_int}.{fpts_against_dec}")
    
    # waiver budget
    waiver_budget = r.get("settings", {}).get("waiver_budget_used", 0)
    faab_remaining = 100 - waiver_budget
    
    roster_map[rid] = {
        "roster_id": rid,
        "owner_id": r["owner_id"],
        "manager_name": mgr_info.get("name", u.get("display_name")),
        "team_name": u.get("team_name"),
        "username": u.get("display_name"),
        "wins": r.get("settings", {}).get("wins", 0),
        "losses": r.get("settings", {}).get("losses", 0),
        "ties": r.get("settings", {}).get("ties", 0),
        "fpts": fpts,
        "fpts_against": fpts_against,
        "waiver_budget_used": waiver_budget,
        "faab_remaining": faab_remaining,
        "starters": r.get("starters", []),
        "players": r.get("players", [])
    }

# Fetch matchups for week 7
matchups7 = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/7")

# Group matchups by matchup_id
matchup_groups = {}
for m in matchups7:
    mid = m["matchup_id"]
    if mid not in matchup_groups:
        matchup_groups[mid] = []
    rid = m["roster_id"]
    r_info = roster_map[rid]
    matchup_groups[mid].append({
        "roster_id": rid,
        "manager_name": r_info["manager_name"],
        "team_name": r_info["team_name"],
        "points": m.get("points", 0.0),
        "starters": m.get("starters", []),
        "starters_points": m.get("starters_points", []),
        "players": m.get("players", []),
        "players_points": m.get("players_points", {})
    })

print("=== WEEK 7 MATCHUP RESULTS ===")
matchup_results = []
for mid, teams in matchup_groups.items():
    if len(teams) == 2:
        t1, t2 = teams[0], teams[1]
        diff = abs(t1["points"] - t2["points"])
        if t1["points"] > t2["points"]:
            winner, loser = t1, t2
        else:
            winner, loser = t2, t1
        matchup_results.append({
            "matchup_id": mid,
            "winner": winner,
            "loser": loser,
            "margin": diff
        })
        print(f"Matchup {mid}: {winner['manager_name']} ({winner['points']:.2f}) def. {loser['manager_name']} ({loser['points']:.2f}) by {diff:.2f} PTS")

matchup_results.sort(key=lambda x: x["margin"])
print("\n=== NARROWEST VICTORY (BOUNTY: $10) ===")
narrowest = matchup_results[0]
print(f"Winner of Narrowest Victory: {narrowest['winner']['manager_name']} def {narrowest['loser']['manager_name']} by {narrowest['margin']:.2f} PTS")

print("\n=== BIGGEST BLOWOUT ===")
blowout = matchup_results[-1]
print(f"Biggest Blowout: {blowout['winner']['manager_name']} def {blowout['loser']['manager_name']} by {blowout['margin']:.2f} PTS")

# Rank all scores
all_scores = []
for m in matchups7:
    rid = m["roster_id"]
    all_scores.append({
        "roster_id": rid,
        "manager_name": roster_map[rid]["manager_name"],
        "points": m.get("points", 0.0),
        "starters": m.get("starters", []),
        "starters_points": m.get("starters_points", [])
    })
all_scores.sort(key=lambda x: x["points"], reverse=True)

print("\n=== WEEK 7 SCORING RANKINGS ===")
for i, s in enumerate(all_scores, 1):
    print(f"{i}. {s['manager_name']}: {s['points']:.2f} PTS")

print("\n=== STANDINGS AFTER WEEK 7 ===")
standings = list(roster_map.values())
standings.sort(key=lambda x: (x["wins"], x["fpts"]), reverse=True)
for i, st in enumerate(standings, 1):
    clean_team = st['team_name'].replace('\u200b', '')
    print(f"{i}. {st['manager_name']} ({clean_team}) — {st['wins']}-{st['losses']} | {st['fpts']:.2f} PF | {st['fpts_against']:.2f} PA | FAAB: ${st['faab_remaining']}")

# Save raw week7 data for subsequent scripts
with open(os.path.join(os.path.dirname(__file__), "week7_data.json"), "w", encoding="utf-8") as f:
    json.dump({
        "rosters": roster_map,
        "matchup_results": matchup_results,
        "all_scores": all_scores,
        "matchups7": matchups7
    }, f, indent=2)
print("\nSaved week7_data.json successfully")

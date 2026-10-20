import urllib.request
import json
import os

LEAGUE_ID = "1389724575532613632"
PICKEM_ID = "1402701854898450432"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

state = fetch_json("https://api.sleeper.app/v1/state/nfl")
users = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users")
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters")
matchups6 = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/6")

# Also fetch previous weeks if needed for total points / standings
# Load config for manager names
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

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
    roster_map[rid] = {
        "roster_id": rid,
        "owner_id": r["owner_id"],
        "manager_name": mgr_info.get("name", u.get("display_name")),
        "team_name": u.get("team_name"),
        "username": u.get("display_name"),
        "wins": r.get("settings", {}).get("wins", 0),
        "losses": r.get("settings", {}).get("losses", 0),
        "fpts": float(f"{r.get('settings', {}).get('fpts', 0)}.{r.get('settings', {}).get('fpts_decimal', 0)}"),
        "fpts_against": float(f"{r.get('settings', {}).get('fpts_against', 0)}.{r.get('settings', {}).get('fpts_against_decimal', 0)}"),
        "starters": r.get("starters", []),
        "players": r.get("players", [])
    }

week6_results = []
for m in matchups6:
    rid = m["roster_id"]
    r_info = roster_map.get(rid, {})
    week6_results.append({
        "roster_id": rid,
        "manager_name": r_info.get("manager_name"),
        "team_name": r_info.get("team_name"),
        "matchup_id": m.get("matchup_id"),
        "points": float(m.get("points", 0)),
        "starters": m.get("starters", []),
        "players_points": m.get("players_points", {}),
        "custom_points": m.get("custom_points")
    })

# Group matchups by matchup_id
matchup_groups = {}
for w in week6_results:
    mid = w["matchup_id"]
    if mid not in matchup_groups:
        matchup_groups[mid] = []
    matchup_groups[mid].append(w)

out_data = {
    "nfl_state": state,
    "roster_map": roster_map,
    "week6_results": week6_results,
    "matchup_groups": matchup_groups
}

# Fetch pickem if possible
try:
    pickem_league = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}")
    pickem_rosters = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/rosters")
    out_data["pickem_rosters"] = pickem_rosters
except Exception as e:
    out_data["pickem_error"] = str(e)

out_file = os.path.join(os.path.dirname(__file__), "week6_data.json")
with open(out_file, "w", encoding="utf-8") as f:
    json.dump(out_data, f, indent=2)

print(f"Data saved to {out_file}")

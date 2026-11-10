import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

mgr_map = {str(k): v["name"] for k, v in config.get("managers", {}).items()}

matchups10 = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/10")

groups = {}
for m in matchups10:
    mid = m["matchup_id"]
    if mid not in groups:
        groups[mid] = []
    rid = str(m["roster_id"])
    groups[mid].append({
        "roster_id": rid,
        "manager": mgr_map.get(rid, f"Roster {rid}")
    })

print("=== WEEK 10 PREVIEW MATCHUPS ===")
week10_list = []
for mid, teams in sorted(groups.items()):
    t1 = teams[0]
    t2 = teams[1]
    print(f"Matchup {mid}: {t1['manager']} vs. {t2['manager']}")
    week10_list.append({
        "matchup_id": mid,
        "team1": t1["manager"],
        "team2": t2["manager"]
    })

with open("scripts/week10_matchups.json", "w", encoding="utf-8") as f:
    json.dump(week10_list, f, indent=2)
print("Saved scripts/week10_matchups.json successfully")

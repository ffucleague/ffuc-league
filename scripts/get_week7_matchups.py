import urllib.request, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/7", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    m7 = json.loads(resp.read().decode('utf-8'))

# Group by matchup_id
groups = {}
for m in m7:
    mid = m["matchup_id"]
    if mid not in groups:
        groups[mid] = []
    rid = m["roster_id"]
    mgr = config.get("managers", {}).get(str(rid), {}).get("name", f"Roster {rid}")
    groups[mid].append((rid, mgr))

print("=== WEEK 7 SCHEDULED MATCHUPS ===")
for mid, teams in groups.items():
    if len(teams) == 2:
        print(f"Matchup {mid}: {teams[0][1]} vs {teams[1][1]}")

with open("scripts/week7_matchups.json", "w", encoding="utf-8") as f:
    json.dump(groups, f, indent=2)

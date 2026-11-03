import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users", headers={'User-Agent': 'Mozilla/5.0'})
users_data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters", headers={'User-Agent': 'Mozilla/5.0'})
rosters_data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/9", headers={'User-Agent': 'Mozilla/5.0'})
matchups_data = json.loads(urllib.request.urlopen(req).read().decode("utf-8"))

user_map = {}
for u in users_data:
    user_map[u["user_id"]] = {
        "display_name": u.get("display_name"),
        "team_name": u.get("metadata", {}).get("team_name")
    }

manager_names = {
    1: "Mark", 2: "Joey", 3: "Pedro", 4: "Franky", 5: "Eric",
    6: "Herrador", 7: "Arnulfo", 8: "iRob", 9: "Alex", 10: "Robert"
}

roster_map = {}
for r in rosters_data:
    rid = r["roster_id"]
    u = user_map.get(r["owner_id"], {})
    roster_map[rid] = {
        "manager": manager_names.get(rid, u.get("display_name")),
        "team_name": u.get("team_name") or f"Team {manager_names.get(rid)}"
    }

m_groups = {}
for m in matchups_data:
    mid = m.get("matchup_id")
    if mid is not None:
        rid = m["roster_id"]
        m_groups.setdefault(mid, []).append({
            "roster_id": rid,
            "manager": roster_map[rid]["manager"],
            "team_name": roster_map[rid]["team_name"]
        })

print("WEEK 9 MATCHUPS:")
for mid, teams in sorted(m_groups.items()):
    print(f"Matchup {mid}: {teams[0]['manager']} ({teams[0]['team_name']}) vs {teams[1]['manager']} ({teams[1]['team_name']})")

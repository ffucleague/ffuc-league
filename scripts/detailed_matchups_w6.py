import json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("scripts/week6_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

try:
    with open("players_cache.json", "r", encoding="utf-8") as pf:
        players = json.load(pf)
except:
    players = {}

for mid, teams in data["matchup_groups"].items():
    print(f"\n==================== MATCHUP {mid} ====================")
    t1, t2 = teams[0], teams[1]
    winner = t1 if t1["points"] > t2["points"] else t2
    loser = t2 if t1["points"] > t2["points"] else t1
    diff = abs(t1["points"] - t2["points"])
    print(f"🏆 {winner['manager_name']} ({winner['team_name']}) {winner['points']:.2f} PTS  vs  {loser['manager_name']} ({loser['team_name']}) {loser['points']:.2f} PTS  (Margin: {diff:.2f})")
    
    for t in [winner, loser]:
        print(f"\n  --- {t['manager_name']} Starters ({t['points']:.2f} PTS) ---")
        for pid in t["starters"]:
            p_info = players.get(pid, {})
            pname = p_info.get("full_name") or pid
            pos = p_info.get("position", "")
            pts = t["players_points"].get(pid, 0)
            print(f"      {pos:4} | {pname:24} | {pts:5.2f} PTS")


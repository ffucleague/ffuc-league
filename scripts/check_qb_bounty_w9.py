import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("players_cache.json", "r", encoding="utf-8") as f:
    players_cache = json.load(f)

with open("scripts/week9_data.json", "r", encoding="utf-8") as f:
    w9_data = json.load(f)

print("=== CHECKING WEEK 9 STARTING QB SCORES (WEEK 9 BOUNTY: $10) ===")
qb_scores = []
for m in w9_data["all_scores"]:
    starters = m["starters"]
    starters_pts = m["starters_points"]
    mgr = m["manager_name"]
    team = m["team_name"]
    
    for pid, pts in zip(starters, starters_pts):
        p_info = players_cache.get(pid, {})
        pos = p_info.get("position")
        name = f"{p_info.get('first_name', '')} {p_info.get('last_name', '')}".strip() or pid
        if pos == "QB":
            qb_scores.append({
                "manager": mgr,
                "team": team,
                "player_name": name,
                "nfl_team": p_info.get("team", ""),
                "points": pts
            })

qb_scores.sort(key=lambda x: x["points"], reverse=True)
for i, qb in enumerate(qb_scores, 1):
    print(f"{i}. {qb['manager']} ({qb['team']}): {qb['player_name']} ({qb['nfl_team']}) — {qb['points']:.2f} PTS")

winner = qb_scores[0]
print(f"\n🏆 WEEK 9 QB BOUNTY WINNER ($10): {winner['manager']} with {winner['player_name']} ({winner['points']:.2f} PTS)!")

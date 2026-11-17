import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("players_cache.json", "r", encoding="utf-8") as f:
    players = json.load(f)

with open("scripts/week10_data.json", "r", encoding="utf-8") as f:
    w10 = json.load(f)

all_player_scores = []

for res in w10["matchup_results"]:
    w = res["winner"]
    l = res["loser"]
    margin = res["margin"]
    
    for team in [w, l]:
        mgr = team["manager_name"]
        starters = team["starters"]
        starters_pts = team["starters_points"]
        for pid, pts in zip(starters, starters_pts):
            p = players.get(pid, {})
            name = p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
            pos = p.get("position", "DEF" if len(pid) <= 3 else "FLEX")
            team_code = p.get("team", pid)
            all_player_scores.append({
                "pid": pid,
                "name": name,
                "pos": pos,
                "team": team_code,
                "pts": pts,
                "manager": mgr,
                "starter": True
            })
            
        bench = [p for p in team.get("players", []) if p not in starters]
        for pid in bench:
            pts = team.get("players_points", {}).get(pid, 0.0)
            p = players.get(pid, {})
            name = p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
            pos = p.get("position", "DEF" if len(pid) <= 3 else "BN")
            team_code = p.get("team", pid)
            all_player_scores.append({
                "pid": pid,
                "name": name,
                "pos": pos,
                "team": team_code,
                "pts": pts,
                "manager": mgr,
                "starter": False
            })

with open("scripts/week10_player_scores.json", "w", encoding="utf-8") as f:
    json.dump(all_player_scores, f, indent=2)

print("=== TOP 10 RBs OF WEEK 10 (STARTING ONLY) ===")
starting_rbs = [p for p in all_player_scores if p["pos"] == "RB" and p["starter"]]
starting_rbs.sort(key=lambda x: x["pts"], reverse=True)
for i, p in enumerate(starting_rbs[:10], 1):
    print(f"{i:2d}. {p['name']:24} ({p['team']}) - {p['manager']:10}: {p['pts']:6.2f} PTS")

print("\n=== TOP 10 RBs OF WEEK 10 (ALL ROSTERED) ===")
all_rbs = [p for p in all_player_scores if p["pos"] == "RB"]
all_rbs.sort(key=lambda x: x["pts"], reverse=True)
for i, p in enumerate(all_rbs[:10], 1):
    status = "STARTER" if p["starter"] else "BENCH"
    print(f"{i:2d}. {p['name']:24} ({p['team']}) - {p['manager']:10} [{status}]: {p['pts']:6.2f} PTS")

print("\n=== TOP 15 SCORERS OVERALL IN WEEK 10 ===")
top_overall = sorted([p for p in all_player_scores if p["starter"]], key=lambda x: x["pts"], reverse=True)
for i, p in enumerate(top_overall[:15], 1):
    print(f"{i:2d}. {p['name']:24} ({p['pos']:3} - {p['team']:3}) - {p['manager']:10}: {p['pts']:6.2f} PTS")

import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open("players_cache.json", "r", encoding="utf-8") as f:
    players = json.load(f)

with open("scripts/week9_data.json", "r", encoding="utf-8") as f:
    w9 = json.load(f)

all_player_scores = []

print("==================================================")
print("              WEEK 9 BOX SCORES                  ")
print("==================================================")

for res in w9["matchup_results"]:
    w = res["winner"]
    l = res["loser"]
    margin = res["margin"]
    print(f"\n==================================================")
    print(f"MATCHUP {res['matchup_id']}: {w['manager_name']} ({w['points']:.2f}) vs {l['manager_name']} ({l['points']:.2f}) — Margin: {margin:.2f}")
    print(f"==================================================")
    
    for team in [w, l]:
        mgr = team["manager_name"]
        print(f"\n  Franchise: {mgr} ({team['team_name']}) — Total: {team['points']:.2f} PTS")
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
            print(f"    {pos:<5} {name:<24} ({team_code}): {pts:>6.2f} PTS")
            
        bench = [p for p in team.get("players", []) if p not in starters]
        print(f"    --- Bench ---")
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
            print(f"    BN    {name:<24} ({team_code}): {pts:>6.2f} PTS")

all_player_scores.sort(key=lambda x: x["pts"], reverse=True)

print("\n==================================================")
print("             TOP 10 BOOM PLAYERS (WEEK 9)         ")
print("==================================================")
for i, p in enumerate(all_player_scores[:12], 1):
    status = "STARTER" if p["starter"] else "BENCH"
    print(f"{i:>2}. {p['name']:<24} ({p['pos']}-{p['team']}) — {p['pts']:.2f} PTS [{p['manager']} • {status}]")

print("\n==================================================")
print("            BIGGEST BUSTS (STARTED PLAYERS)       ")
print("==================================================")
starters_only = [p for p in all_player_scores if p["starter"]]
starters_only.sort(key=lambda x: x["pts"])
for i, p in enumerate(starters_only[:12], 1):
    print(f"{i:>2}. {p['name']:<24} ({p['pos']}-{p['team']}) — {p['pts']:.2f} PTS [{p['manager']}]")

out_player_stats = os.path.join(os.path.dirname(__file__), "week9_player_scores.json")
with open(out_player_stats, "w", encoding="utf-8") as f:
    json.dump(all_player_scores, f, indent=2)
print(f"\nSaved {out_player_stats} successfully")

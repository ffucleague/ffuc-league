import json
import urllib.request
import io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("scripts/week6_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Load players cache or sleeper players to check DEF
try:
    with open("players_cache.json", "r", encoding="utf-8") as pf:
        players = json.load(pf)
except:
    players = {}

print("=== CHECKING DEF PERFORMANCES IN WEEK 6 ===")
def_scores = []
all_players = []

for m in data["week6_results"]:
    pts_dict = m["players_points"]
    mgr = m["manager_name"]
    team = m["team_name"]
    starters = m["starters"]
    for pid, score in pts_dict.items():
        p_info = players.get(pid, {})
        pos = p_info.get("position")
        name = p_info.get("full_name") or f"{p_info.get('first_name', '')} {p_info.get('last_name', '')}".strip() or pid
        is_starter = pid in starters
        all_players.append({
            "pid": pid,
            "name": name,
            "pos": pos,
            "score": score,
            "manager": mgr,
            "starter": is_starter
        })
        if pos == "DEF" or pid in ["DEN", "PIT", "BAL", "PHI", "BUF", "HOU", "KC", "TB", "DET", "MIN", "CHI", "SF", "GB", "LAC", "IND", "NYJ", "DAL", "WAS", "CIN", "CLE", "MIA", "NO", "SEA", "TEN", "ARI", "ATL", "CAR", "JAX", "LV", "NE", "NYG", "LAR"]:
            def_scores.append({
                "team": pid,
                "name": name if name != pid else f"{pid} DEF",
                "score": score,
                "manager": mgr,
                "starter": is_starter
            })

def_scores.sort(key=lambda x: x["score"], reverse=True)
print("Top DEF scores in Week 6:")
for d in def_scores[:10]:
    starter_tag = "[STARTER]" if d["starter"] else "[BENCH]"
    print(f"  {d['manager']:10} | {d['name']:15} | {d['score']:5.2f} PTS {starter_tag}")

print("\n=== TOP OVERALL PLAYERS IN WEEK 6 ===")
all_players.sort(key=lambda x: x["score"], reverse=True)
for p in all_players[:15]:
    starter_tag = "[STARTER]" if p["starter"] else "[BENCH]"
    print(f"  {p['manager']:10} | {p['name']:22} ({p['pos']}) | {p['score']:5.2f} PTS {starter_tag}")


import json
import os
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open(os.path.join(os.path.dirname(__file__), "week6_data.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

print("=== NFL STATE ===")
print("Week:", data["nfl_state"].get("week"), "Display Week:", data["nfl_state"].get("display_week"))

print("\n=== WEEK 6 MATCHUPS ===")
matchups = sorted(data["week6_results"], key=lambda x: x["points"], reverse=True)
for m in matchups:
    print(f"Roster {m['roster_id']} | Manager: {m['manager_name']:10} | Team: {m['team_name'][:20]:20} | Points: {m['points']:.2f} | Matchup: {m['matchup_id']}")

print("\n=== HEAD-TO-HEAD BATTLES ===")
for mid, teams in data["matchup_groups"].items():
    if len(teams) == 2:
        t1, t2 = teams[0], teams[1]
        diff = abs(t1["points"] - t2["points"])
        winner = t1 if t1["points"] > t2["points"] else t2
        loser = t2 if t1["points"] > t2["points"] else t1
        print(f"Matchup {mid}: {winner['manager_name']} ({winner['points']:.2f}) DEF. {loser['manager_name']} ({loser['points']:.2f}) by {diff:.2f} PTS")

print("\n=== HIGH ROLLER (Highest Team Score) ===")
print(f"1st: {matchups[0]['manager_name']} ({matchups[0]['points']:.2f} PTS)")

print("\n=== TOILET METER / 5K NOMINEE (Lowest Team Score) ===")
print(f"Last: {matchups[-1]['manager_name']} ({matchups[-1]['points']:.2f} PTS)")

print("\n=== OVERALL STANDINGS THROUGH WEEK 6 ===")
rosters = sorted(data["roster_map"].values(), key=lambda x: (x["wins"], x["fpts"]), reverse=True)
for i, r in enumerate(rosters, 1):
    print(f"{i:2d}. {r['manager_name']:10} | {r['wins']}-{r['losses']} | PF: {r['fpts']:.2f} | PA: {r['fpts_against']:.2f} | {r['team_name']}")


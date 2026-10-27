import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load sleeper players
players_url = "https://api.sleeper.app/v1/players/nfl"
# We can also check if we have players cached or fetch specific player stats
# Let's inspect week7_data.json
with open("C:/Users/Mark Borrego/Desktop/FFUC_Website/scripts/week7_data.json", "r", encoding="utf-8") as f:
    w7 = json.load(f)

# Sleeper stats for week 7
stats_w7 = urllib.request.urlopen("https://api.sleeper.app/v1/stats/nfl/regular/2026/7").read().decode('utf-8')
stats_data = json.loads(stats_w7)

# Starters points in each matchup
for m in w7["matchups7"]:
    rid = m["roster_id"]
    mgr = w7["rosters"][str(rid)]["manager_name"]
    starters = m.get("starters", [])
    starters_points = m.get("starters_points", [])
    print(f"\n--- {mgr} ({m.get('points')} PTS) ---")
    for pid, pts in zip(starters, starters_points):
        p_stat = stats_data.get(pid, {})
        # Let's see what we can find for player name
        print(f"  Player ID {pid}: {pts:.2f} PTS")

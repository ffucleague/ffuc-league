import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
req = urllib.request.Request(f'https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/11', headers={'User-Agent': 'Mozilla/5.0'})
matchups = json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

with open('config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)

mgr_map = {int(k): v['name'] for k, v in config['managers'].items()}
pairs = {}
for m in matchups:
    mid = m['matchup_id']
    pairs.setdefault(mid, []).append(mgr_map.get(m['roster_id'], f"R{m['roster_id']}"))

print("=== WEEK 11 SCHEDULED MATCHUPS ===")
for mid, p in pairs.items():
    print(f"Matchup {mid}: {p[0]} vs {p[1]}")

with open('scripts/week11_matchups.json', 'w', encoding='utf-8') as f:
    json.dump(matchups, f, indent=2)
print("Saved scripts/week11_matchups.json successfully")

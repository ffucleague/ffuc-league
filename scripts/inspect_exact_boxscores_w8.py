import json, urllib.request, sys
sys.stdout.reconfigure(encoding='utf-8')

# Load NFL players database or sleeper players cache if available
# Let's fetch sleeper players or inspect detailed_matchups_w8.py
with open('scripts/week8_player_scores.json', 'r', encoding='utf-8') as f:
    player_scores = json.load(f)

p_map = {p['pid']: p for p in player_scores}

with open('scripts/week8_data.json', 'r', encoding='utf-8') as f:
    w8_data = json.load(f)

for m in w8_data['matchup_results']:
    mid = m['matchup_id']
    win = m['winner']
    los = m['loser']
    margin = m['margin']
    print(f"\n=======================================================")
    print(f"MATCHUP {mid}: {win['manager_name']} ({win['points']:.2f}) def. {los['manager_name']} ({los['points']:.2f}) [Margin: {margin:.2f}]")
    print(f"=======================================================")
    
    print(f"\nWINNER: {win['manager_name']} ({win['team_name']}) - {win['points']:.2f} PTS")
    for pid, pts in zip(win['starters'], win['starters_points']):
        pinfo = p_map.get(pid, {})
        name = pinfo.get('name', pid)
        pos = pinfo.get('pos', '')
        team = pinfo.get('team', '')
        print(f"  • {name} ({pos} • {team}): {pts:.2f} PTS")
        
    print(f"\nLOSER: {los['manager_name']} ({los['team_name']}) - {los['points']:.2f} PTS")
    for pid, pts in zip(los['starters'], los['starters_points']):
        pinfo = p_map.get(pid, {})
        name = pinfo.get('name', pid)
        pos = pinfo.get('pos', '')
        team = pinfo.get('team', '')
        print(f"  • {name} ({pos} • {team}): {pts:.2f} PTS")

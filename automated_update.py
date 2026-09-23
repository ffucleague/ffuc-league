import urllib.request
import urllib.error
import json
import os
import re
import base64
import zipfile
import io
import sys
from datetime import datetime

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_FILE = os.path.join(SCRIPT_DIR, 'config.json')

# Default config
default_config = {
    "league_id": "1389724575532613632",
    "pickem_id": "1402701854898450432",
    "domain": "ffucleague.com",
    "bounties": {
        "1": "Most Points ($10)",
        "2": "Highest Scoring QB ($10)",
        "3": "Highest Scoring RB ($10)",
        "4": "Highest Scoring WR ($10)",
        "5": "Highest Scoring TE ($10)",
        "6": "Highest Scoring DEF ($10)",
        "7": "Narrowest Victory ($10)",
        "8": "Biggest Blowout ($10)",
        "9": "Highest Scoring Flex ($10)",
        "10": "Highest Scoring Kicker ($10)",
        "11": "Highest Scoring Bench Player ($10)",
        "12": "Most Total Touchdowns ($10)",
        "13": "Highest Scoring QB+WR Stack ($10)",
        "14": "Most Points Overall ($10)"
    },
    "paces": {
        "1": 15, "2": 12, "3": 18, "4": 20, "5": 15,
        "6": 18, "7": 20, "8": 18, "9": 15, "10": 20
    }
}

if not os.path.exists(CONFIG_FILE):
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, indent=2)
    config = default_config
else:
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        config = json.load(f)

league_id = config.get("league_id", "1389724575532613632")

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

print("==================================================")
print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] RUNNING F.F.U.C. AUTOMATED TUESDAY REPORT")
print("==================================================")

# 1. Fetch NFL State
nfl_state = fetch_json('https://api.sleeper.app/v1/state/nfl')
current_week = nfl_state.get('week', 1)
print(f"NFL Season: {nfl_state.get('season')}, Current Week: {current_week}")

# 2. Fetch League Users & Rosters
users = fetch_json(f'https://api.sleeper.app/v1/league/{league_id}/users')
rosters = fetch_json(f'https://api.sleeper.app/v1/league/{league_id}/rosters')

user_map = {}
for u in users:
    uid = u['user_id']
    team_name = u.get('metadata', {}).get('team_name') or u.get('display_name')
    avatar_id = u.get('avatar')
    user_map[uid] = {
        'name': team_name,
        'user_name': u.get('display_name'),
        'avatar': f"https://sleepercdn.com/avatars/thumbs/{avatar_id}" if avatar_id else ""
    }

managers_config = config.get("managers", {})

roster_map = {}
for r in rosters:
    rid = r['roster_id']
    u_info = user_map.get(r['owner_id'], {'name': f'Roster {rid}', 'avatar': ''})
    m_info = managers_config.get(str(rid), {})
    mgr_name = m_info.get('name', u_info.get('user_name', ''))
    roster_map[rid] = {
        'roster_id': rid,
        'owner_id': r['owner_id'],
        'manager_name': mgr_name,
        'team_name': u_info['name'],
        'user_name': u_info.get('user_name', ''),
        'titles': m_info.get('titles', []),
        'avatar': u_info['avatar'],
        'wins': r.get('settings', {}).get('wins', 0),
        'losses': r.get('settings', {}).get('losses', 0),
        'fpts': float(f"{r.get('settings', {}).get('fpts', 0)}.{r.get('settings', {}).get('fpts_decimal', 0)}"),
        'fpts_against': float(f"{r.get('settings', {}).get('fpts_against', 0)}.{r.get('settings', {}).get('fpts_against_decimal', 0)}"),
        'faab_used': r.get('settings', {}).get('waiver_budget_used', 0),
        'players': r.get('players', [])
    }

print(f"Loaded {len(roster_map)} league franchises successfully.")

# 3. Determine target completed week
target_week = nfl_state.get('display_week') or (current_week if nfl_state.get('season_has_scores') else max(1, current_week - 1))
print(f"Auditing completed matchups for Week {target_week}...")

matchups = fetch_json(f'https://api.sleeper.app/v1/league/{league_id}/matchups/{target_week}')
matchup_scores = []
for m in matchups:
    rid = m['roster_id']
    pts = float(m.get('points', 0))
    matchup_scores.append({
        'roster_id': rid,
        'team_name': roster_map[rid]['team_name'],
        'points': pts,
        'matchup_id': m.get('matchup_id'),
        'starters': m.get('starters', []),
        'players_points': m.get('players_points', {})
    })

matchup_scores.sort(key=lambda x: x['points'], reverse=True)

# High Roller ($10 Bounty Winner) & Toilet Bowl Nominee (5K Runner)
high_roller = matchup_scores[0]
toilet_nominee = matchup_scores[-1]

print(f"👑 High Roller: {high_roller['team_name']} ({high_roller['points']:.2f} PTS)")
print(f"🤡 Toilet Bowl Nominee: {toilet_nominee['team_name']} ({toilet_nominee['points']:.2f} PTS)")

# 4. Calculate Luck Index (All-Play Records for Target Week)
all_play_standings = []
for i, t1 in enumerate(matchup_scores):
    wins = len([t2 for t2 in matchup_scores if t1['points'] > t2['points']])
    losses = len([t2 for t2 in matchup_scores if t1['points'] < t2['points']])
    ties = len([t2 for t2 in matchup_scores if t1['points'] == t2['points'] and t1['roster_id'] != t2['roster_id']])
    all_play_standings.append({
        'team_name': t1['team_name'],
        'roster_id': t1['roster_id'],
        'points': t1['points'],
        'all_play_w': wins,
        'all_play_l': losses,
        'all_play_t': ties
    })

print("Calculated All-Play Luck Index standings.")

# 5. Fetch Waivers / Transactions for Target Week
try:
    transactions = fetch_json(f'https://api.sleeper.app/v1/league/{league_id}/transactions/{target_week}')
    completed_txs = [t for t in transactions if t.get('status') == 'complete']
    print(f"Fetched {len(completed_txs)} completed transactions for Week {target_week}.")
except Exception as e:
    print(f"Notice on transactions: {e}")
# 5b. Update "Last Updated" timestamp in index.html
try:
    index_file = os.path.join(SCRIPT_DIR, 'index.html')
    if os.path.exists(index_file):
        with open(index_file, 'r', encoding='utf-8') as f:
            html_text = f.read()
        now_str = datetime.now().strftime('%b %d, %Y • %I:%M %p CST')
        html_text = re.sub(
            r'id="portalLastUpdated"[^>]*>([^<]*)<',
            f'id="portalLastUpdated">{now_str}<',
            html_text
        )
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_text)
        print(f"Updated index.html 'Last Updated' timestamp: {now_str}")
except Exception as e:
    print(f"Notice on timestamp update: {e}")

# 6. Push to GitHub (automatically publishes live via GitHub Pages to ffucleague.com)
def push_to_github(website_dir):
    try:
        import subprocess
        git_dir = os.path.join(website_dir, '.git')
        if not os.path.exists(git_dir):
            return
        print("\nSyncing with GitHub repository...")
        subprocess.run(['git', 'add', '.'], cwd=website_dir, check=True)
        now_str = datetime.now().strftime('%b %d, %Y • %I:%M %p')
        res = subprocess.run(['git', 'commit', '-m', f'Auto-update: {now_str}'], cwd=website_dir, capture_output=True, text=True)
        if "nothing to commit" in res.stdout or "nothing to commit" in res.stderr:
            print("   Git: Working tree clean (no new changes to commit).")
        else:
            print("   Git: Committed changes. Pushing to GitHub (origin main)...")
            push_res = subprocess.run(['git', 'push', 'origin', 'main'], cwd=website_dir, capture_output=True, text=True)
            if push_res.returncode == 0:
                print("   🎉 Successfully pushed to GitHub! Site is automatically published live to ffucleague.com.")
            else:
                print(f"   Git push warning: {push_res.stderr.strip()}")
    except Exception as e:
        print(f"   Git push notice: {e}")

push_to_github(SCRIPT_DIR)

print("\n==================================================")
print("AUTOMATION SCRIPT EXECUTION COMPLETED")
print("==================================================")

import urllib.request, json, sys
sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"

req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    rosters = json.loads(resp.read().decode('utf-8'))

req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    users = json.loads(resp.read().decode('utf-8'))

user_map = {}
for u in users:
    uid = u['user_id']
    disp = u.get('display_name', '')
    user_map[uid] = disp

# Read config to get canonical manager names
with open('config.json', 'r', encoding='utf-8') as f:
    cfg = json.load(f)

uname_to_mgr = {}
for m_id, m_data in cfg.get('managers', {}).items():
    uname_to_mgr[m_data['username'].lower()] = m_data['name']

# Map roster to manager
roster_to_mgr = {}
for r in rosters:
    r_id = r['roster_id']
    owner_id = r.get('owner_id')
    user_obj = next((u for u in users if u['user_id'] == owner_id), None)
    if user_obj:
        username = user_obj.get('display_name', '').lower()
        mgr_name = uname_to_mgr.get(username, username)
        roster_to_mgr[r_id] = mgr_name
    else:
        roster_to_mgr[r_id] = f"Roster {r_id}"

# Budget list
print("=== OFFICIAL SLEEPER FAAB BUDGETS (POST-WEEK 6) ===")
budget_list = []
for r in rosters:
    r_id = r['roster_id']
    mgr_name = roster_to_mgr[r_id]
    team_name = r.get('metadata', {}).get('team_name', mgr_name)
    settings = r.get('settings', {})
    waiver_budget_used = settings.get('waiver_budget_used', 0)
    remaining_faab = 100 - waiver_budget_used
    budget_list.append((mgr_name, team_name, remaining_faab, waiver_budget_used))

budget_list.sort(key=lambda x: x[2], reverse=True)
for i, (m_name, t_name, rem, used) in enumerate(budget_list, 1):
    print(f"{i:2}. {m_name:10} | {t_name:30} | Rem: ${rem} ({rem}%) (Used: ${used})")

# Fetch week 6 transactions
req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/6", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    txs = json.loads(resp.read().decode('utf-8'))

# Players cache
players = {}
try:
    with open('players_cache.json', 'r', encoding='utf-8') as f:
        players = json.load(f)
except Exception as e:
    pass

print("\n=== WEEK 6 COMPLETED TRANSACTIONS ===")
for tx in txs:
    status = tx.get('status')
    if status != 'complete':
        continue
    t_type = tx.get('type')
    r_ids = tx.get('roster_ids', [])
    r_id = r_ids[0] if r_ids else None
    mgr = roster_to_mgr.get(r_id, f"Roster {r_id}")
    adds = tx.get('adds') or {}
    drops = tx.get('drops') or {}
    bid = tx.get('settings', {}).get('waiver_bid', 0) if tx.get('settings') else 0
    
    add_strs = []
    for pid in adds.keys():
        p = players.get(pid, {})
        pos = p.get('position', '')
        team = p.get('team', '')
        name = p.get('full_name', pid)
        add_strs.append(f"{name} ({pos} • {team})")
        
    drop_strs = []
    for pid in drops.keys():
        p = players.get(pid, {})
        pos = p.get('position', '')
        team = p.get('team', '')
        name = p.get('full_name', pid)
        drop_strs.append(f"{name} ({pos} • {team})")
        
    print(f"[{mgr:10}] Type: {t_type:10} | Bid: ${bid:2} | Added: {', '.join(add_strs)} | Dropped: {', '.join(drop_strs)}")

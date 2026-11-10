import urllib.request
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

with open("players_cache.json", "r", encoding="utf-8") as f:
    players_cache = json.load(f)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

mgr_map = {str(k): v["name"] for k, v in config.get("managers", {}).items()}

txs = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/9")
print(f"Total Week 9 transactions: {len(txs)}")

completed = [t for t in txs if t.get("status") == "complete"]
print(f"Completed transactions: {len(completed)}")

waiver_moves = []
for t in completed:
    ttype = t.get("type")
    adds = t.get("adds") or {}
    drops = t.get("drops") or {}
    roster_ids = t.get("roster_ids", [])
    rid = str(roster_ids[0]) if roster_ids else "?"
    mgr = mgr_map.get(rid, f"Roster {rid}")
    
    bid = t.get("settings", {}).get("waiver_bid", 0) if t.get("settings") else 0
    
    add_names = []
    for pid in adds:
        p = players_cache.get(pid, {})
        name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
        add_names.append(f"{name} ({p.get('position', '')} - {p.get('team', '')})")
        
    drop_names = []
    for pid in drops:
        p = players_cache.get(pid, {})
        name = f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
        drop_names.append(f"{name} ({p.get('position', '')} - {p.get('team', '')})")
        
    waiver_moves.append({
        "type": ttype,
        "manager": mgr,
        "bid": bid,
        "adds": add_names,
        "drops": drop_names
    })
    print(f"[{ttype.upper()}] {mgr}: Add {add_names} | Drop {drop_names} | Bid: ${bid}")

out_path = os.path.join(os.path.dirname(__file__), "waivers_w9.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(waiver_moves, f, indent=2)

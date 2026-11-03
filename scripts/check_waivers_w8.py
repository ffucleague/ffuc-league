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
    players = json.load(f)

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

users = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users")
user_map = {u["user_id"]: u for u in users}

# Check transactions for round 8
trans8 = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/8")
print(f"Total transactions in round 8: {len(trans8)}")

waiver_claims = []
trades = []
free_agents = []

for t in trans8:
    ttype = t.get("type")
    status = t.get("status")
    if status != "complete":
        continue
    
    roster_id = t.get("roster_ids", [None])[0]
    mgr_name = config.get("managers", {}).get(str(roster_id), {}).get("name", "Unknown")
    
    adds = t.get("adds") or {}
    drops = t.get("drops") or {}
    settings = t.get("settings") or {}
    bid = settings.get("waiver_bid", 0)
    
    add_names = [players.get(pid, {}).get("full_name", pid) for pid in adds.keys()]
    drop_names = [players.get(pid, {}).get("full_name", pid) for pid in drops.keys()]
    
    if ttype == "waiver":
        waiver_claims.append({
            "manager": mgr_name,
            "bid": bid,
            "adds": add_names,
            "drops": drop_names
        })
    elif ttype == "trade":
        trades.append(t)
    elif ttype == "free_agent":
        free_agents.append({
            "manager": mgr_name,
            "adds": add_names,
            "drops": drop_names
        })

print("\n=== WAIVER BIDS / CLAIMS ===")
waiver_claims.sort(key=lambda x: x["bid"], reverse=True)
for c in waiver_claims:
    print(f"${c['bid']:2d} FAAB | {c['manager']:10} ADD: {', '.join(c['adds'])} | DROP: {', '.join(c['drops'])}")

print(f"\nTotal Free Agent moves: {len(free_agents)}")
for fa in free_agents[:10]:
    print(f"  {fa['manager']:10} ADD: {', '.join(fa['adds'])} | DROP: {', '.join(fa['drops'])}")

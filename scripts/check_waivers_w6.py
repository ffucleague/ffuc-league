import urllib.request, json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
LEAGUE_ID = "1389724575532613632"

try:
    with open("players_cache.json", "r", encoding="utf-8") as pf:
        players = json.load(pf)
except:
    players = {}

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

user_to_mgr = {}
for rid, m in config.get("managers", {}).items():
    user_to_mgr[m["username"].lower()] = m["name"]

url = f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/transactions/6"
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    txs = json.loads(resp.read().decode('utf-8'))

print(f"Total Week 6 Transactions: {len(txs)}")
waivers = []
trades = []
for t in txs:
    status = t.get("status")
    ttype = t.get("type")
    if status == "complete":
        adds = t.get("adds") or {}
        drops = t.get("drops") or {}
        bid = (t.get("settings") or {}).get("waiver_bid", 0)
        c_rid = t.get("creator") or (t.get("roster_ids", [None])[0] if t.get("roster_ids") else None)
        
        add_names = [players.get(pid, {}).get("full_name", pid) for pid in adds.keys()]
        drop_names = [players.get(pid, {}).get("full_name", pid) for pid in drops.keys()]
        
        waivers.append({
            "type": ttype,
            "bid": bid,
            "adds": add_names,
            "drops": drop_names,
            "roster_ids": t.get("roster_ids")
        })

print("\nCompleted Transactions:")
for w in waivers[:15]:
    print(f"  Type: {w['type']:7} | Bid: ${w['bid']:2d} | Adds: {', '.join(w['adds'])} | Drops: {', '.join(w['drops'])}")

import json, urllib.request, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PICKEM_ID = "1402701854898450432"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

users = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/users")
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/rosters")

# Load config for real names
with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

user_map = {u["user_id"]: u for u in users}

# Map username to manager name
user_to_mgr = {}
for rid, m in config.get("managers", {}).items():
    user_to_mgr[m["username"].lower()] = m["name"]

pickem_standings = []
for r in rosters:
    uid = r["owner_id"]
    u = user_map.get(uid, {})
    uname = u.get("display_name", "")
    mgr_name = user_to_mgr.get(uname.lower(), uname)
    meta = r.get("metadata") or {}
    points_by_leg = meta.get("points_by_leg") or {}
    
    # Points by week
    w1 = float(points_by_leg.get("v1:regular:1", 0))
    w2 = float(points_by_leg.get("v1:regular:2", 0))
    w3 = float(points_by_leg.get("v1:regular:3", 0))
    w4 = float(points_by_leg.get("v1:regular:4", 0))
    w5 = float(points_by_leg.get("v1:regular:5", 0))
    w6 = float(points_by_leg.get("v1:regular:6", 0))
    total = sum([w1, w2, w3, w4, w5, w6])
    
    team_name = u.get("metadata", {}).get("team_name") or uname
    
    pickem_standings.append({
        "manager": mgr_name,
        "username": uname,
        "team_name": team_name,
        "total": total,
        "w1": w1, "w2": w2, "w3": w3, "w4": w4, "w5": w5, "w6": w6
    })

pickem_standings.sort(key=lambda x: x["total"], reverse=True)

print("=== OFFICIAL SLEEPER PICK-EM STANDINGS THROUGH WEEK 6 (95 Games) ===")
for i, p in enumerate(pickem_standings, 1):
    print(f"{i:2d}. {p['manager']:10} ({p['username']:15}) | TOTAL: {p['total']:4.1f} pts | W6: {p['w6']:4.1f} | Breakdown: W1:{p['w1']:.0f} W2:{p['w2']:.0f} W3:{p['w3']:.0f} W4:{p['w4']:.0f} W5:{p['w5']:.0f} W6:{p['w6']:.0f}")

with open("scripts/pickem_standings_w6.json", "w", encoding="utf-8") as pf:
    json.dump(pickem_standings, pf, indent=2)

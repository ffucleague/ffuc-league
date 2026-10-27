import json, urllib.request, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PICKEM_ID = "1402701854898450432"
def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    return json.loads(urllib.request.urlopen(req).read().decode('utf-8'))

users = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/users")
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/rosters")

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

user_map = {u["user_id"]: u for u in users}
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
    
    weeks = [float(points_by_leg.get(f"v1:regular:{w}", 0)) for w in range(1, 8)]
    total = sum(weeks)
    team_name = (u.get("metadata", {}).get("team_name") or uname).replace('\u200b', '')
    
    pickem_standings.append({
        "manager": mgr_name,
        "username": uname,
        "team_name": team_name,
        "total": total,
        "w7": weeks[6],
        "weeks": weeks
    })

pickem_standings.sort(key=lambda x: x["total"], reverse=True)

print("=== OFFICIAL SLEEPER PICK-EM STANDINGS THROUGH WEEK 7 ===")
for i, p in enumerate(pickem_standings, 1):
    breakdown = " ".join([f"W{w}:{v:.0f}" for w, v in enumerate(p['weeks'], 1)])
    print(f"{i:2d}. {p['manager']:10} ({p['username']:15}) | TOTAL: {p['total']:4.1f} pts | W7: {p['w7']:4.1f} | Breakdown: {breakdown}")

with open("scripts/pickem_standings_w7.json", "w", encoding="utf-8") as pf:
    json.dump(pickem_standings, pf, indent=2)

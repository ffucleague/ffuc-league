import urllib.request, json, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

with open("config.json", "r", encoding="utf-8") as f:
    config = json.load(f)

# Collect all weekly scores for weeks 1 through 6
weekly_scores = {w: {} for w in range(1, 7)}
for w in range(1, 7):
    matchups = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/{w}")
    for m in matchups:
        rid = m["roster_id"]
        pts = float(m.get("points", 0))
        weekly_scores[w][rid] = pts

# Compute all-play record for each roster
roster_allplay = {rid: {"w": 0, "l": 0, "t": 0} for rid in range(1, 11)}

for w in range(1, 7):
    scores = weekly_scores[w]
    for rid1, s1 in scores.items():
        for rid2, s2 in scores.items():
            if rid1 != rid2:
                if s1 > s2:
                    roster_allplay[rid1]["w"] += 1
                elif s1 < s2:
                    roster_allplay[rid1]["l"] += 1
                else:
                    roster_allplay[rid1]["t"] += 1

# Load actual standings from rosters
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters")
roster_map = {}
for r in rosters:
    rid = r["roster_id"]
    mgr = config.get("managers", {}).get(str(rid), {}).get("name", f"Roster {rid}")
    actual_w = r.get("settings", {}).get("wins", 0)
    actual_l = r.get("settings", {}).get("losses", 0)
    fpts = float(f"{r.get('settings', {}).get('fpts', 0)}.{r.get('settings', {}).get('fpts_decimal', 0)}")
    
    ap_w = roster_allplay[rid]["w"]
    ap_l = roster_allplay[rid]["l"]
    exp_w = ap_w / 9.0  # 9 opponents per week
    luck = actual_w - exp_w
    
    roster_map[rid] = {
        "manager": mgr,
        "actual_w": actual_w,
        "actual_l": actual_l,
        "fpts": fpts,
        "ap_w": ap_w,
        "ap_l": ap_l,
        "exp_w": exp_w,
        "luck": luck
    }

print("=== ALL-PLAY LUCK INDEX THROUGH WEEK 6 (54 All-Play Games Each) ===")
sorted_by_luck = sorted(roster_map.values(), key=lambda x: x["luck"], reverse=True)
for r in sorted_by_luck:
    print(f"{r['manager']:10} | Actual: {r['actual_w']}-{r['actual_l']} | All-Play: {r['ap_w']:2d}-{r['ap_l']:2d} ({r['ap_w']/54*100:4.1f}%) | Exp Wins: {r['exp_w']:.2f} | Luck: {r['luck']:+5.2f} | PF: {r['fpts']:.2f}")

with open("scripts/luck_index_w6.json", "w", encoding="utf-8") as f:
    json.dump(sorted_by_luck, f, indent=2)

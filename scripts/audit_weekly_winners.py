import urllib.request, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
PICKEM_ID = "1402701854898450432"

def fetch_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

# Load config
config_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.json")
with open(config_path, "r", encoding="utf-8") as f:
    config = json.load(f)

users = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users")
rosters = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters")

# Players cache if available
players = {}
if os.path.exists("players_cache.json"):
    with open("players_cache.json", "r", encoding="utf-8") as f:
        players = json.load(f)
else:
    print("Fetching Sleeper players...")
    players = fetch_json("https://api.sleeper.app/v1/players/nfl")
    with open("players_cache.json", "w", encoding="utf-8") as f:
        json.dump(players, f)

user_map = {}
for u in users:
    uid = u["user_id"]
    team_name = (u.get("metadata", {}).get("team_name") or u.get("display_name")).replace('\u200b', '').strip()
    user_map[uid] = {
        "display_name": u.get("display_name"),
        "team_name": team_name
    }

roster_to_mgr = {}
for r in rosters:
    rid = r["roster_id"]
    u = user_map.get(r["owner_id"], {})
    mgr_info = config.get("managers", {}).get(str(rid), {})
    roster_to_mgr[rid] = {
        "name": mgr_info.get("name", u.get("display_name")),
        "team_name": u.get("team_name", mgr_info.get("name")),
        "roster_id": rid
    }

bounties_def = config.get("bounties", {})

print("=================================================================")
print("             AUDITING WEEKS 1 - 7 SLEEPER DATA                   ")
print("=================================================================")

for week in range(1, 8):
    matchups = fetch_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/{week}")
    
    # 1. High Roller (Most Points in the week)
    sorted_by_pts = sorted(matchups, key=lambda m: m.get("points", 0), reverse=True)
    hr_matchup = sorted_by_pts[0]
    hr_mgr = roster_to_mgr.get(hr_matchup["roster_id"], {})
    hr_pts = hr_matchup.get("points", 0)
    
    # Low score
    low_matchup = sorted_by_pts[-1]
    low_mgr = roster_to_mgr.get(low_matchup["roster_id"], {})
    low_pts = low_matchup.get("points", 0)

    # 2. Matchup outcomes
    matchup_pairs = {}
    for m in matchups:
        mid = m["matchup_id"]
        matchup_pairs.setdefault(mid, []).append(m)
        
    matchup_results = []
    for mid, pair in matchup_pairs.items():
        if len(pair) == 2:
            p1, p2 = pair[0], pair[1]
            if p1["points"] >= p2["points"]:
                win, lose = p1, p2
            else:
                win, lose = p2, p1
            margin = win["points"] - lose["points"]
            w_mgr = roster_to_mgr.get(win["roster_id"], {})
            l_mgr = roster_to_mgr.get(lose["roster_id"], {})
            matchup_results.append({
                "matchup_id": mid,
                "winner": w_mgr["name"],
                "win_pts": win["points"],
                "loser": l_mgr["name"],
                "lose_pts": lose["points"],
                "margin": margin
            })

    # Sort matchups by margin for narrowest and blowout
    sorted_by_margin = sorted(matchup_results, key=lambda x: x["margin"])
    narrowest = sorted_by_margin[0]
    biggest_blowout = sorted_by_margin[-1]

    # 3. Weekly Bounty from config.json:
    bounty_rule = bounties_def.get(str(week), "Unknown")
    
    # Analyze players in starters for positional bounties
    best_qb = {"pts": -100, "player": "", "mgr": ""}
    best_rb = {"pts": -100, "player": "", "mgr": ""}
    best_wr = {"pts": -100, "player": "", "mgr": ""}
    best_te = {"pts": -100, "player": "", "mgr": ""}
    best_def = {"pts": -100, "player": "", "mgr": ""}
    best_k = {"pts": -100, "player": "", "mgr": ""}
    
    for m in matchups:
        mgr = roster_to_mgr.get(m["roster_id"], {})
        starters = m.get("starters", [])
        starters_pts = m.get("starters_points", [])
        for pid, pts in zip(starters, starters_pts):
            p = players.get(pid, {})
            pos = p.get("position", "")
            pname = p.get("full_name") or f"{p.get('first_name', '')} {p.get('last_name', '')}".strip() or pid
            
            if pos == "QB" and pts > best_qb["pts"]:
                best_qb = {"pts": pts, "player": pname, "mgr": mgr["name"], "team": p.get("team", "")}
            elif pos == "RB" and pts > best_rb["pts"]:
                best_rb = {"pts": pts, "player": pname, "mgr": mgr["name"], "team": p.get("team", "")}
            elif pos == "WR" and pts > best_wr["pts"]:
                best_wr = {"pts": pts, "player": pname, "mgr": mgr["name"], "team": p.get("team", "")}
            elif pos == "TE" and pts > best_te["pts"]:
                best_te = {"pts": pts, "player": pname, "mgr": mgr["name"], "team": p.get("team", "")}
            elif (pos == "DEF" or len(pid) <= 3) and pts > best_def["pts"]:
                best_def = {"pts": pts, "player": pname, "mgr": mgr["name"], "team": p.get("team", "")}
            elif pos == "K" and pts > best_k["pts"]:
                best_k = {"pts": pts, "player": pname, "mgr": mgr["name"], "team": p.get("team", "")}

    print(f"\n--- WEEK {week} ---")
    print(f"👑 High Roller: {hr_mgr['name']} ({hr_mgr['team_name']}) — {hr_pts:.2f} PTS")
    print(f"🚽 Low Score:   {low_mgr['name']} ({low_mgr['team_name']}) — {low_pts:.2f} PTS")
    print(f"⚡ Bounty Rule: {bounty_rule}")
    
    if week == 1: # Most Points
        print(f"   WINNER: {hr_mgr['name']} — {hr_pts:.2f} PTS")
    elif week == 2: # Highest Scoring QB
        print(f"   WINNER: {best_qb['mgr']} with {best_qb['player']} ({best_qb['team']}) — {best_qb['pts']:.2f} PTS")
    elif week == 3: # Highest Scoring RB
        print(f"   WINNER: {best_rb['mgr']} with {best_rb['player']} ({best_rb['team']}) — {best_rb['pts']:.2f} PTS")
    elif week == 4: # Highest Scoring WR
        print(f"   WINNER: {best_wr['mgr']} with {best_wr['player']} ({best_wr['team']}) — {best_wr['pts']:.2f} PTS")
    elif week == 5: # Highest Scoring TE
        print(f"   WINNER: {best_te['mgr']} with {best_te['player']} ({best_te['team']}) — {best_te['pts']:.2f} PTS")
    elif week == 6: # Highest Scoring DEF
        print(f"   WINNER: {best_def['mgr']} with {best_def['player']} ({best_def['team']}) — {best_def['pts']:.2f} PTS")
    elif week == 7: # Narrowest Victory
        print(f"   WINNER: {narrowest['winner']} (def. {narrowest['loser']} by {narrowest['margin']:.2f} PTS: {narrowest['win_pts']:.2f} to {narrowest['lose_pts']:.2f})")

    print(f"   Positional Leaders Started:")
    print(f"     QB:  {best_qb['mgr']} • {best_qb['player']} ({best_qb['pts']:.2f})")
    print(f"     RB:  {best_rb['mgr']} • {best_rb['player']} ({best_rb['pts']:.2f})")
    print(f"     WR:  {best_wr['mgr']} • {best_wr['player']} ({best_wr['pts']:.2f})")
    print(f"     TE:  {best_te['mgr']} • {best_te['player']} ({best_te['pts']:.2f})")
    print(f"     DEF: {best_def['mgr']} • {best_def['player']} ({best_def['pts']:.2f})")
    print(f"     K:   {best_k['mgr']} • {best_k['player']} ({best_k['pts']:.2f})")
    print(f"   Narrowest: {narrowest['winner']} def. {narrowest['loser']} ({narrowest['margin']:.2f} pts)")
    print(f"   Blowout:   {biggest_blowout['winner']} def. {biggest_blowout['loser']} ({biggest_blowout['margin']:.2f} pts)")

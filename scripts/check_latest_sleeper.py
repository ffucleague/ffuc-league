import urllib.request, json, sys, os
sys.stdout.reconfigure(encoding='utf-8')

LEAGUE_ID = "1389724575532613632"
PICKEM_ID = "1402701854898450432"

def get_json(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode('utf-8'))

league = get_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}")
print("League Status:", league.get("status"), "Leg:", league.get("settings", {}).get("leg"))

matchups = get_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/matchups/8")
print("\nCURRENT WEEK 8 MATCHUP SCORES FROM SLEEPER:")
for m in sorted(matchups, key=lambda x: x['roster_id']):
    print(f"Roster {m['roster_id']}: points={m.get('points')}, custom_points={m.get('custom_points')}")

# Load previously saved week8_data.json to compare
with open('scripts/week8_data.json', 'r', encoding='utf-8') as f:
    old_data = json.load(f)

old_matchups = old_data.get('matchups', {})
print("\nCOMPARING WITH SAVED WEEK 8 DATA:")
changes_found = False
for m in matchups:
    rid = str(m['roster_id'])
    old_pts = old_matchups.get(rid, {}).get('points')
    new_pts = m.get('points')
    if old_pts != new_pts:
        print(f"🚨 SCORE CHANGED for Roster {rid}: Old={old_pts} -> New={new_pts}")
        changes_found = True

if not changes_found:
    print("✅ All matchup scores match previously saved week8_data.json exactly!")

# Check rosters / standings
rosters = get_json(f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters")
print("\nCURRENT ROSTER RECORDS & SCORES:")
for r in sorted(rosters, key=lambda x: x['roster_id']):
    rid = r['roster_id']
    settings = r.get('settings', {})
    wins = settings.get('wins')
    losses = settings.get('losses')
    fpts = settings.get('fpts') + settings.get('fpts_decimal', 0) / 100.0
    fpts_against = settings.get('fpts_against') + settings.get('fpts_against_decimal', 0) / 100.0
    faab = 100 - settings.get('waiver_budget_used', 0)
    print(f"Roster {rid}: {wins}-{losses} | PF: {fpts:.2f} | PA: {fpts_against:.2f} | FAAB: ${faab}")


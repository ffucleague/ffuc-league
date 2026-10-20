import urllib.request, json
req = urllib.request.Request("https://api.sleeper.app/v1/league/1402701854898450432/users", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    users = json.loads(resp.read().decode('utf-8'))
for u in users:
    print(u["display_name"], u.get("metadata"))

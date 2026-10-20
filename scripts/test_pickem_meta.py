import urllib.request, json
PICKEM_ID = "1402701854898450432"
req = urllib.request.Request(f"https://api.sleeper.app/v1/league/{PICKEM_ID}", headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    data = json.loads(resp.read().decode('utf-8'))
print("Settings:", json.dumps(data.get("settings"), indent=2))
print("Metadata:", json.dumps(data.get("metadata"), indent=2))

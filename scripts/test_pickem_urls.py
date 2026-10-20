import urllib.request, json
PICKEM_ID = "1402701854898450432"
def check_url(url):
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"SUCCESS: {url} -> Type: {type(data)}, Len: {len(data) if isinstance(data, (list, dict)) else 'N/A'}")
            if isinstance(data, list) and len(data) > 0:
                print("   Sample:", data[0])
            elif isinstance(data, dict):
                print("   Keys:", list(data.keys())[:10])
    except Exception as e:
        print(f"FAILED: {url} -> {e}")

check_url(f"https://api.sleeper.app/v1/league/{PICKEM_ID}")
check_url(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/users")
check_url(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/matchups/1")
check_url(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/matchups/6")
check_url(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/winners_bracket")
check_url(f"https://api.sleeper.app/v1/league/{PICKEM_ID}/transactions/6")

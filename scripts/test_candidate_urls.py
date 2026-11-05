import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

candidates = {
    "wolf_chest_thump": [
        "https://giphy.com/gifs/paramountmovies-gdwJdym3VuXQr5OfAc",
        "https://giphy.com/gifs/the-wolf-of-wall-street-matthew-mcconaughey-leonardo-dicaprio-gBkBmnZkaWCnC"
    ],
    "ronaldo_siu": [
        "https://giphy.com/gifs/champions-league-cr7-cristiano-ronaldo-w9t4MG001DKvu",
        "https://giphy.com/gifs/football-soccer-ronaldo-R312C3MEVg4SCYAber",
        "https://giphy.com/gifs/fifaworldcup-world-cup-cristiano-ronaldo-siu-dqiIWZ1o3py09qEynZ"
    ],
    "mcgregor_strut": [
        "https://giphy.com/gifs/ufc-mma-conor-mcgregor-l0HlOBZRezdd8skqk",
        "https://giphy.com/gifs/ufc-mma-ufc-205-3o6Zt4UC9H4sq5PqVy"
    ]
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

found = {}
for name, list_urls in candidates.items():
    for u in list_urls:
        try:
            req = urllib.request.Request(u, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='ignore')
                og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html)
                mp4_match = re.search(r'https://media\d*\.giphy\.com/media/[^/]+/giphy\.mp4', html)
                v_url = og_video.group(1) if og_video else (mp4_match.group(0) if mp4_match else None)
                if v_url:
                    found[name] = {"url": u, "mp4": v_url}
                    print(f"✅ {name}: {v_url}")
                    break
        except Exception as e:
            # print(f"Error for {u}: {e}")
            pass

print("\nFinal found:")
print(json.dumps(found, indent=2))

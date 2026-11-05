import urllib.request
import urllib.parse
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

searches = {
    # High Roller
    "ronaldo_siu": "cristiano ronaldo siu celebration",
    "salt_bae": "salt bae steak",
    "ric_flair_wooo": "ric flair wooo strut",
    
    # Heartbreak
    "jordan_crying": "michael jordan crying",
    "walter_white_collapse": "walter white falling desert breaking bad",
    "ben_affleck_smoking": "ben affleck smoking cigarette",
    
    # Toilet Runner
    "indiana_jones_boulder": "indiana jones running boulder",
    "phoebe_running": "phoebe buffay running friends",
    "jack_sparrow_run": "jack sparrow running beach"
}

results = {}

for name, query in searches.items():
    print(f"\n🔍 Searching for '{name}' ({query})...")
    encoded = urllib.parse.quote(query)
    # Try search endpoint
    url = f"https://giphy.com/search/{query.replace(' ', '-')}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Find IDs in the HTML
            # Look for /gifs/title-ID
            matches = re.findall(r'/gifs/[a-zA-Z0-9_-]+-([a-zA-Z0-9]{8,25})', html)
            if not matches:
                matches = re.findall(r'media\d*\.giphy\.com/media/([a-zA-Z0-9]{8,25})/', html)
            
            # Filter out non-gif IDs or common static asset hashes
            valid_ids = []
            seen = set()
            for gid in matches:
                if gid not in seen and gid not in ["XJtM2nNFCzT3etvzOB", "static", "default"]:
                    seen.add(gid)
                    valid_ids.append(gid)
            
            print(f"   Found IDs: {valid_ids[:4]}")
            if valid_ids:
                results[name] = valid_ids[:3]
    except Exception as e:
        print(f"   Error: {e}")

with open("scratch/search_recommended_ids.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)

print("\nDone searching!")

import urllib.request
import re
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

searches = {
    "ronaldo_front": "https://giphy.com/search/ronaldo-siu-front",
    "jack_sparrow_real": "https://giphy.com/search/jack-sparrow-run",
    "walter_white_desert": "https://giphy.com/search/bryan-cranston-falling"
}

for name, url in searches.items():
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
        matches = re.findall(r'/gifs/[a-zA-Z0-9_-]+-([a-zA-Z0-9]{8,25})', html)
        print(f"{name} -> {matches[:6]}")
    except Exception as e:
        print(f"Error {name}: {e}")

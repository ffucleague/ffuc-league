import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

urls = [
    "https://giphy.com/explore/ronaldo-siu-celebration",
    "https://giphy.com/explore/mcgregor-strut"
]

for u in urls:
    try:
        req = urllib.request.Request(u, headers=headers)
        html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
        matches = set(re.findall(r'/gifs/[a-zA-Z0-9_-]+-([a-zA-Z0-9]+)', html))
        print(f"{u} -> {len(matches)} gifs: {list(matches)[:5]}")
    except Exception as e:
        print(f"Error {u}: {e}")

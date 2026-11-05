import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

def search_for_ids(keyword):
    url = f"https://giphy.com/search/{keyword.replace(' ', '-')}"
    req = urllib.request.Request(url, headers=headers)
    html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')
    # IDs in giphy are alphanumeric typically 10-25 chars
    # Look for /gifs/ or /media/ patterns
    ids = re.findall(r'https://media\d*\.giphy\.com/media/([a-zA-Z0-9]+)/giphy\.mp4', html)
    if not ids:
        ids = re.findall(r'media[0-9]*\.giphy\.com/media/([a-zA-Z0-9]+)/', html)
    # Deduplicate while preserving order
    seen = set()
    unique = []
    for i in ids:
        if i not in seen and len(i) > 6:
            seen.add(i)
            unique.append(i)
    print(f"Keyword '{keyword}' -> found {len(unique)} IDs: {unique[:5]}")
    return unique[:5]

search_for_ids("cristiano-ronaldo-siu")
search_for_ids("conor-mcgregor-strut")

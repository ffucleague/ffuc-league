import urllib.request
import re
import json

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

test_ids = [
    # Ronaldo
    'qgVI3F6xL70DZDDsm3', 'LLwJN0NJSurHxEaZHj', 'H6B2GveUlLadk2rbD3',
    # McGregor
    'H47OlJHZIjkmYc107K', 'wZtraKYj1giqWHK30Q', 'tvhjpTOZWt7PlAs8uy'
]

for gid in test_ids:
    url = f"https://giphy.com/gifs/{gid}"
    try:
        req = urllib.request.Request(url, headers=headers)
        html = urllib.request.urlopen(req, timeout=5).read().decode('utf-8', errors='ignore')
        title_m = re.search(r'<title>([^<]+)</title>', html)
        title = title_m.group(1) if title_m else "No title"
        print(f"ID: {gid} | Title: {title}")
    except Exception as e:
        print(f"ID: {gid} | Error: {e}")

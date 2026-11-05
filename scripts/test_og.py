import urllib.request
import re
import json

url = 'https://giphy.com/gifs/paramountmovies-gdwJdym3VuXQr5OfAc'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urllib.request.urlopen(req).read().decode('utf-8', errors='ignore')

print("HTML length:", len(html))

# Look for Giphy ID in any media url
mp4s = set(re.findall(r'https://[^"\'\s]+\.mp4', html))
print("MP4s found:", len(mp4s))
for m in mp4s:
    print(" ", m)

# Look for __NEXT_DATA__
m_data = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', html)
if m_data:
    print("Found NEXT DATA")
    try:
        data = json.loads(m_data.group(1))
        # print top level keys
        print("Keys:", data.keys())
    except Exception as e:
        print("Error parsing json:", e)

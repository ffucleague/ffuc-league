import urllib.request
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
headers = {'User-Agent': 'Mozilla/5.0'}

for gid in ['Zhpvn5KvGEvJu', 'o0eOCNkn7cSD6', '8JCwuk8n2Y6iI']:
    u = f'https://giphy.com/gifs/{gid}'
    try:
        html = urllib.request.urlopen(urllib.request.Request(u, headers=headers), timeout=5).read().decode('utf-8', errors='ignore')
        og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
        og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html)
        print(gid, 'img:', og_img.group(1) if og_img else 'None', 'video:', og_video.group(1) if og_video else 'None')
    except Exception as e:
        print(gid, ':', e)

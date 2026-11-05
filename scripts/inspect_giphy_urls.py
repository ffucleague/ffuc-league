import urllib.request
import re
import json

urls = [
    "https://giphy.com/gifs/wwe-vince-mcmahon-wrestling-gifs-vRf4Z1OZ21j9e",
    "https://giphy.com/gifs/party-birthday-celebration-s2qXK8wAvkHTO",
    "https://giphy.com/gifs/masonramsey-mason-ramsey-cdNSp4L5vCU7aQrYnV",
    "https://giphy.com/gifs/cheers-yziuK6WtDFMly",
    "https://giphy.com/gifs/mls-sunglasses-quakes-earthquakes-Ie482rXFNBUbnnGxpg"
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for u in urls:
    print(f"\nFetching: {u}")
    req = urllib.request.Request(u, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            html = resp.read().decode('utf-8', errors='ignore')
            
            # Giphy usually has og:video or og:image or <video ... src="..."> or json-ld
            og_video = re.search(r'<meta property="og:video" content="([^"]+)"', html)
            og_title = re.search(r'<meta property="og:title" content="([^"]+)"', html)
            og_img = re.search(r'<meta property="og:image" content="([^"]+)"', html)
            mp4_match = re.search(r'https://media\d*\.giphy\.com/media/[^/]+/giphy\.mp4', html)
            
            title = og_title.group(1) if og_title else "Unknown"
            video_url = og_video.group(1) if og_video else (mp4_match.group(0) if mp4_match else None)
            img_url = og_img.group(1) if og_img else None
            
            print(f"Title: {title}")
            print(f"Video URL: {video_url}")
            print(f"Image URL: {img_url}")
    except Exception as e:
        print(f"Failed: {e}")

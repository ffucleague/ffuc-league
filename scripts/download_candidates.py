import os
import sys
import urllib.request
import subprocess
import json
import base64

sys.stdout.reconfigure(encoding='utf-8')

CANDIDATES_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "scratch", "candidate_clips")
os.makedirs(CANDIDATES_DIR, exist_ok=True)

clips = [
    {
        "id": "vince_mcmahon_strut",
        "url": "https://media4.giphy.com/media/v1.Y2lkPTc5MGI3NjExZmoyeWw0ZDA0cnB4ZTczYTF5azlhNG4xeDNhYXZuOGxuYzlzOGNlZSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/vRf4Z1OZ21j9e/giphy.mp4",
        "suggested_title": "Vince McMahon Billionaire Strut"
    },
    {
        "id": "celebration_kid",
        "url": "https://media0.giphy.com/media/v1.Y2lkPTc5MGI3NjExZDM0NjRxY2ExN3Zxanp6Y3F1aGN5Z2hzdzhmdXI1dWJhMzltODBzbCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/s2qXK8wAvkHTO/giphy.mp4",
        "suggested_title": "Party Celebration Yes"
    },
    {
        "id": "mason_ramsey_dance",
        "url": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExa2xkYnFwcmF0cDIwb3B4MGZucTA1bHNraHJzdmdidzJ4eDBpaGZhYiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/cdNSp4L5vCU7aQrYnV/giphy.mp4",
        "suggested_title": "Mason Ramsey Sunglasses Dance"
    },
    {
        "id": "cheers_toast",
        "url": "https://media2.giphy.com/media/v1.Y2lkPTc5MGI3NjExNXA3OGhtaWRmdnV4Zjhrc3dqNmw3Z3dmMjE0aXMyMTd6NGY5cnBwbiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/yziuK6WtDFMly/giphy.mp4",
        "suggested_title": "Cheers Beer Toast"
    },
    {
        "id": "mls_boss_sunglasses",
        "url": "https://media1.giphy.com/media/v1.Y2lkPTc5MGI3NjExdWwxbmhoMTVldXRiZ2RkYXZodjAzNDZiMjh1amN1ZXFkdW5wc2hpMCZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/Ie482rXFNBUbnnGxpg/giphy.mp4",
        "suggested_title": "MLS Coach Deal With It Sunglasses"
    }
]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

for c in clips:
    mp4_path = os.path.join(CANDIDATES_DIR, f"{c['id']}.mp4")
    frame_path = os.path.join(CANDIDATES_DIR, f"{c['id']}_frame.jpg")
    print(f"\n📥 Downloading {c['id']}...")
    req = urllib.request.Request(c["url"], headers=headers)
    with urllib.request.urlopen(req, timeout=15) as resp:
        with open(mp4_path, "wb") as f:
            f.write(resp.read())
    size_kb = os.path.getsize(mp4_path) / 1024
    print(f"   Saved {mp4_path} ({size_kb:.1f} KB)")
    
    # Extract middle frame using ffmpeg on host (or remote if ffmpeg not in Windows PATH)
    # Check if ffmpeg exists locally
    try:
        subprocess.run(["ffmpeg", "-y", "-ss", "00:00:01", "-i", mp4_path, "-vframes", "1", frame_path], 
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print(f"   Extracted frame: {frame_path}")
    except Exception as e:
        print(f"   Local ffmpeg notice: {e}")

print("\nAll downloads finished!")

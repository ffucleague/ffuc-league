import urllib.request
import os
import subprocess
import json
import base64

url = "https://media.giphy.com/media/o0eOCNkn7cSD6/giphy.mp4"
mp4_path = "scratch/recs_clips/jack_sparrow_real.mp4"
frame_path = "scratch/recs_clips/jack_sparrow_real_frame.jpg"

req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req) as resp:
    with open(mp4_path, 'wb') as f:
        f.write(resp.read())

subprocess.run(["ffmpeg", "-y", "-ss", "00:00:00.5", "-i", mp4_path, "-vframes", "1", frame_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if not os.path.exists(frame_path) or os.path.getsize(frame_path) == 0:
    subprocess.run(["ffmpeg", "-y", "-i", mp4_path, "-vframes", "1", frame_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

with open(frame_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'model': 'qwen3-vl:32b',
    'prompt': 'Who is in this frame and what are they doing? Is it suitable for a face swap? Provide verdict: [APPROVED] or [REJECTED].',
    'stream': False,
    'options': {'num_ctx': 4096, 'num_predict': 400, 'temperature': 0.1},
    'images': [b64]
}
req2 = urllib.request.Request('http://192.168.86.67:11434/api/generate', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
resp2 = urllib.request.urlopen(req2)
data = json.loads(resp2.read().decode('utf-8'))
print("Response:", data.get('response', data.get('thinking', 'N/A')))

import urllib.request
import json
import base64
import os

img_path = r"C:\Users\Mark Borrego\Desktop\FFUC_Website\scratch\candidate_clips\hallway_sprint_frame.jpg"
with open(img_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'model': 'qwen3-vl:32b',
    'prompt': 'Briefly describe who is in this image, where their face is, and if their face is clear or blurry. Is it suitable for a face swap?',
    'stream': False,
    'options': {'num_ctx': 2048, 'num_predict': 100, 'temperature': 0.2},
    'images': [b64]
}
req = urllib.request.Request('http://192.168.86.67:11434/api/generate', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
print(json.loads(resp.read().decode('utf-8'))['response'])

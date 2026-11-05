import urllib.request
import json
import base64

img_path = r"C:\Users\Mark Borrego\Desktop\FFUC_Website\scratch\candidate_clips\hallway_sprint_frame.jpg"
with open(img_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'model': 'qwen3-vl:32b',
    'prompt': 'Is the face in this hallway sprint frame clear enough for FaceFusion? Answer in one word: YES or NO.',
    'stream': False,
    'options': {'num_ctx': 4096, 'num_predict': 500, 'temperature': 0.1},
    'images': [b64]
}
req = urllib.request.Request('http://192.168.86.67:11434/api/generate', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))
print("Response keys:", data.keys())
print("Thinking:", data.get('thinking', 'N/A')[:200])
print("Response:", data.get('response', 'N/A'))

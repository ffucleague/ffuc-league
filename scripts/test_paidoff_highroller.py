import urllib.request
import json
import base64

img_path = r"C:\Users\Mark Borrego\Desktop\FFUC_Website\scratch\candidate_clips\paid_off_screaming_frame.jpg"
with open(img_path, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'model': 'qwen3-vl:32b',
    'prompt': 'Is this frame from Michael Torpey (Paid Off) celebrating with money suitable for High Roller Champion ($10 weekly winner)? Evaluate face swap and comedic vibe.',
    'stream': False,
    'options': {'num_ctx': 4096, 'num_predict': 1024, 'temperature': 0.1},
    'images': [b64]
}
req = urllib.request.Request('http://192.168.86.67:11434/api/generate', data=json.dumps(payload).encode('utf-8'), headers={'Content-Type': 'application/json'})
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode('utf-8'))
print("Thinking:", data.get('thinking', 'N/A'))
print("Response:", data.get('response', 'N/A'))

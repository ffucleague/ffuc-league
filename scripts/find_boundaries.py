import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="wk6-slide-0"' in l:
        print(f"wk6-slide-0 starts at line {i+1}")
    if 'id="wk6-slide-10"' in l:
        print(f"wk6-slide-10 starts at line {i+1}")
    if 'id="wk5-slide-0"' in l:
        print(f"wk5-slide-0 starts at line {i+1}")

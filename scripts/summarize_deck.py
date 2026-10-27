import sys, re
sys.stdout.reconfigure(encoding='utf-8')

with open(r'C:\Users\Mark Borrego\Desktop\FFUC_Website\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

sections = re.findall(r'<section\s+id="(wk6-slide-\d+)"[^>]*>(.*?)</section>', text, re.DOTALL)
for s_id, s_content in sections:
    h2 = re.search(r'<h2[^>]*>(.*?)</h2>', s_content)
    h2_text = re.sub(r'<[^>]+>', '', h2.group(1)).strip() if h2 else "NO H2"
    print(f"{s_id}: {h2_text} (length {len(s_content)} chars)")

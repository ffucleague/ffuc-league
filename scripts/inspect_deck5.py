import re, io, sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# Find deck-wk5
m = re.search(r'<div id="deck-wk5">([\s\S]*?)<div id="deck-wk4"', html)
if m:
    deck5 = m.group(1)
    print("Found deck-wk5, length:", len(deck5))
    slides = re.findall(r'<section id="wk5-slide-([0-9]+)"[\s\S]*?(?=<section id="wk5-slide-|\Z)', deck5)
    print("Found slides count:", len(slides))
    
    sections = re.findall(r'<section id="wk5-slide-([0-9]+)"[^>]*>([\s\S]*?)(?=</section>)', deck5)
    for num, sec in sections:
        # Find h2 or h3
        headers = re.findall(r'<h[23][^>]*>(.*?)</h[23]>', sec)
        clean_headers = [re.sub(r'<[^>]+>', '', h).strip() for h in headers[:3]]
        print(f"Slide {num}: {clean_headers}")
else:
    print("deck-wk5 not found")

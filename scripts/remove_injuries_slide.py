import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

deck6_idx = html.find('id="deck-wk6"')
deck5_idx = html.find('id="deck-wk5"')
deck6 = html[deck6_idx:deck5_idx]

print("Initial deck-wk6 length:", len(deck6))

# 1. Remove slide 9 (<section id="wk6-slide-9" ... </section>)
m_inj = re.search(r'\s*<!-- SLIDE 9: INJURIES[^\n]*-->\s*<section id="wk6-slide-9"[\s\S]*?</section>', deck6)
if not m_inj:
    # try searching without comment
    m_inj = re.search(r'\s*<section id="wk6-slide-9"[\s\S]*?</section>', deck6)

if m_inj:
    print("Found injuries slide, length:", len(m_inj.group(0)))
    deck6_new = deck6[:m_inj.start()] + deck6[m_inj.end():]
else:
    print("Error: Could not locate wk6-slide-9!")
    sys.exit(1)

# 2. Renumber wk6-slide-10 to wk6-slide-9 (Scoreboard) and wk6-slide-11 to wk6-slide-10 (Gameday Hub)
deck6_new = deck6_new.replace('<!-- SLIDE 10: SCOREBOARD -->', '<!-- SLIDE 9: SCOREBOARD -->')
deck6_new = deck6_new.replace('id="wk6-slide-10"', 'id="wk6-slide-9"')

deck6_new = deck6_new.replace('<!-- SLIDE 11: WEEK 7 GAMEDAY HUB (LOOKAHEAD) -->', '<!-- SLIDE 10: WEEK 7 GAMEDAY HUB (LOOKAHEAD) -->')
deck6_new = deck6_new.replace('id="wk6-slide-11"', 'id="wk6-slide-10"')

# Replace deck6 in html
html = html[:deck6_idx] + deck6_new + html[deck5_idx:]

# 3. New Nav Pills (11 buttons: 1. Awards to 11. Wk 7 Gameday Hub)
new_nav_pills = """<nav class="flex items-center gap-1.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">
        <button onclick="goToSlide(0)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-amber-500 text-slate-950 font-bold">1. 🏆 Awards</button>
        <button onclick="goToSlide(1)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">2. 🏛️ State of Union</button>
        <button onclick="goToSlide(2)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">3. 💵 $10 Bounty</button>
        <button onclick="goToSlide(3)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">4. 🍻 Bar Tab</button>
        <button onclick="goToSlide(4)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">5. 🍀 Luck Index</button>
        <button onclick="goToSlide(5)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">6. 📈 Power Rankings</button>
        <button onclick="goToSlide(6)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">7. 💰 FAAB Receipts</button>
        <button onclick="goToSlide(7)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">8. 🎯 Pick-em ($45)</button>
        <button onclick="goToSlide(8)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">9. 💥 Booms & Busts</button>
        <button onclick="goToSlide(9)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">10. ⚔️ Scoreboard</button>
        <button onclick="goToSlide(10)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-400 hover:text-white transition">11. ⚡ Wk 7 Gameday Hub</button>
      </nav>"""

m_nav = re.search(r'<nav class="flex items-center gap-1\.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">[\s\S]*?</nav>', html)
if m_nav:
    html = html[:m_nav.start()] + new_nav_pills + html[m_nav.end():]
    print("Replaced nav pills successfully.")
else:
    print("Error: Could not find nav container!")
    sys.exit(1)

# 4. Update indicators and JS totalSlides
html = html.replace('Slide 1 / 12', 'Slide 1 / 11')
html = html.replace('const totalSlides = 12;', 'const totalSlides = 11;')
html = html.replace('let totalSlides = 12;', 'let totalSlides = 11;')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Saved index.html successfully!")

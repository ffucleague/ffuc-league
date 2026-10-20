import re, os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

print(f"Read index.html: {len(html)} bytes")

# 1. Update timestamp
now_str = "Oct 20, 2026 • 11:00 AM CST"
html = re.sub(r'id="portalLastUpdated"[^>]*>[^<]*<', f'id="portalLastUpdated">{now_str}<', html)
html = re.sub(r'id="portalSyncedTime"[^>]*>[^<]*<', f'id="portalSyncedTime">{now_str} (Week 6 Final Edition)<', html)

# 2. Update breaking news ticker
ticker_content = (
    '<span>👑 <strong>High Roller ($10 Bounty):</strong> <span class="text-amber-400 font-bold">CULT OF THE LAMB (Franky)</span> drops <span class="text-emerald-400 font-bold">149.80 PTS</span> in a historic shootout!</span>'
    '<span class="text-slate-500">•</span>'
    '<span>⚡ <strong>$10 DEF Bounty Winner:</strong> <span class="text-amber-400 font-bold">Pedro (I Didn’t Hear No Bell)</span> captures $10 with <span class="text-emerald-400 font-bold">Kansas City Chiefs DEF (16.00 PTS)</span>!</span>'
    '<span class="text-slate-500">•</span>'
    '<span>💥 <strong>Game of the Year:</strong> <span class="text-amber-400 font-bold">Franky (149.80)</span> outduels <span class="text-amber-400 font-bold">Joey (135.28)</span> in a 285-point fireworks display!</span>'
    '<span class="text-slate-500">•</span>'
    '<span>🎯 <strong>Pick-Em Co-Leaders:</strong> <span class="text-amber-400 font-bold">Arnulfo & Robert</span> locked at <span class="text-emerald-400 font-bold">58.0 PTS</span> across 95 games!</span>'
    '<span class="text-slate-500">•</span>'
    '<span>🚽 <strong>5K Toilet Danger Zone:</strong> <span class="text-amber-400 font-bold">Robert (WE GOIN’ BACK 2 BACK)</span> bottoms out at <span class="text-red-400 font-bold">79.62 PTS</span>!</span>'
    '<span class="text-slate-500">•</span>'
    '<span>🏆 <strong>Sole 1st Place:</strong> <span class="text-amber-400 font-bold">iRob (Njigbas in Paris)</span> sits alone atop the mountain at <span class="text-emerald-400 font-bold">5-1</span>!</span>'
)

html = re.sub(
    r'(<div class="ticker-content text-slate-200 text-xs">[\s\S]*?<div class="inline-flex items-center gap-6 pr-6">)[\s\S]*?(</div>[\s\S]*?<div class="inline-flex items-center gap-6 pr-6" aria-hidden="true">)[\s\S]*?(</div>)',
    f'\\g<1>{ticker_content}\\g<2>{ticker_content}\\g<3>',
    html,
    count=1
)

# 3. Update dropdown edition
old_select = '<select id="seasonArchive" onchange="handleArchiveSelect(this.value)" class="bg-slate-950 border border-slate-700 text-amber-400 text-xs font-bold py-1.5 px-3 rounded-lg focus:outline-none focus:border-amber-500 cursor-pointer shadow-sm">\n            <option value="wk5" selected>📅 Week 5: Official Report (Final)</option>\n            <option value="wk4">📅 Week 4: Official Report (Archive)</option>'
new_select = '<select id="seasonArchive" onchange="handleArchiveSelect(this.value)" class="bg-slate-950 border border-slate-700 text-amber-400 text-xs font-bold py-1.5 px-3 rounded-lg focus:outline-none focus:border-amber-500 cursor-pointer shadow-sm">\n            <option value="wk6" selected>📅 Week 6: Official Report (Final)</option>\n            <option value="wk5">📅 Week 5: Official Report (Archive)</option>\n            <option value="wk4">📅 Week 4: Official Report (Archive)</option>'

if old_select in html:
    html = html.replace(old_select, new_select)
    print("Replaced dropdown options successfully")
else:
    # regex fallback
    html = re.sub(
        r'<option value="wk5"[^>]*>📅 Week 5: Official Report \(Final\)</option>',
        '<option value="wk6" selected>📅 Week 6: Official Report (Final)</option>\n            <option value="wk5">📅 Week 5: Official Report (Archive)</option>',
        html
    )
    print("Replaced dropdown options via regex")

# Also update locked option to Week 7
html = re.sub(r'<option value="locked" disabled>🔒 Week 6 \(Upcoming\)</option>', '<option value="locked" disabled>🔒 Week 7 (Upcoming)</option>', html)

# 4. Update Nav Pill for Slide 13
html = re.sub(r'13\.\s*⚡\s*Wk 6 Gameday Hub', '13. ⚡ Wk 7 Gameday Hub', html)

# 5. Update JavaScript archive handler
old_js_arch = "if (val === 'wk1' || val === 'wk2' || val === 'wk3' || val === 'wk4' || val === 'wk5') {"
new_js_arch = "if (val === 'wk1' || val === 'wk2' || val === 'wk3' || val === 'wk4' || val === 'wk5' || val === 'wk6') {"
html = html.replace(old_js_arch, new_js_arch)

old_js_decks = "const d5 = document.getElementById('deck-wk5');"
new_js_decks = "const d6 = document.getElementById('deck-wk6');\n        const d5 = document.getElementById('deck-wk5');"
html = html.replace(old_js_decks, new_js_decks)

old_js_toggle = "if (d5) d5.classList.toggle('hidden', currentEdition !== 'wk5');"
new_js_toggle = "if (d6) d6.classList.toggle('hidden', currentEdition !== 'wk6');\n        if (d5) d5.classList.toggle('hidden', currentEdition !== 'wk5');"
html = html.replace(old_js_toggle, new_js_toggle)

# Update currentEdition default in JS
html = re.sub(r"let currentEdition = 'wk5';", "let currentEdition = 'wk6';", html)

# 6. Update switchVoice in JS to use wk6 audio
html = re.sub(r"assets/audio/wk5_recap_mcafee\.wav", "assets/audio/wk6_recap_mcafee.wav", html)
html = re.sub(r"assets/audio/wk5_recap_freeman\.wav", "assets/audio/wk6_recap_freeman.wav", html)

print("Updated JS and audio references.")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated index.html base settings")

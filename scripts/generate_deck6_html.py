import re, os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Load week6_data.json
DATA_PATH = os.path.join(os.path.dirname(__file__), "week6_data.json")
with open(DATA_PATH, "r", encoding="utf-8") as f:
    w6_data = json.load(f)

# Extract deck-wk5 as base template
m = re.search(r'(<div id="deck-wk5"[^>]*>[\s\S]*?)(?=<div id="deck-wk4")', html)
if not m:
    print("Error: Could not locate deck-wk5")
    sys.exit(1)

deck5_full = m.group(1)

# Build deck-wk6 from deck5 by updating IDs, texts, names, scores
deck6 = deck5_full

# 1. Update deck wrapper
deck6 = re.sub(r'id="deck-wk5"[^>]*>', 'id="deck-wk6">', deck6)

# 2. Update all slide IDs from wk5-slide-X to wk6-slide-X
deck6 = re.sub(r'id="wk5-slide-([0-9]+)"', r'id="wk6-slide-\1"', deck6)

# 3. Slide 0: Awards & Coronation
deck6 = deck6.replace("OFFICIAL WEEK 5 AWARDS • F.F.U.C. HONORS", "OFFICIAL WEEK 6 AWARDS • F.F.U.C. HONORS")
deck6 = deck6.replace("Week 5 Official Audio Recap (Pat McAfee Edition)", "Week 6 Official Audio Recap (Pat McAfee Edition)")
deck6 = deck6.replace(
    "High-energy recap: Alex's 167.94 record, Franky's 3.96 heartbreak, Robert's Pick-Em lead, and Pedro's 5K panic.",
    "High-energy recap: Franky's 149.80 shootout win, Pedro's $10 DEF bounty, Herrador's 50-pt blowout, and Robert's 5K panic."
)

# Replace High Roller Winner (Alex -> Franky)
deck6 = deck6.replace("167.94 PTS", "149.80 PTS")
deck6 = deck6.replace("Amon-Ra's Maye-hem <span class=\"text-amber-400 text-sm font-semibold\">(Alex)</span>", "CULT OF THE LAMB <span class=\"text-amber-400 text-sm font-semibold\">(Franky)</span>")
deck6 = re.sub(
    r'Alex shatters the 2026 FFUC all-time weekly scoring record[\s\S]*?\(688\.60 PF\)!',
    'Franky unleashes an unstoppable 149.80-point offensive clinic! Led by James Cook (22.80), Bhayshul Tuten (22.70), Malik Nabers (22.50), and Colston Loveland (15.50), Franky outduels Joey in a 285-point slugfest, collects the $10 High Roller bounty, and captures the #1 overall season scoring throne (814.62 PF)!',
    deck6
)
deck6 = deck6.replace("assets/video/alex_high_roller.mp4", "assets/video/franky_high_roller.mp4")
deck6 = deck6.replace("Alex Coronation Toast", "Franky Coronation Toast")
deck6 = deck6.replace("Previous Season High: Robert (163.84)", "Season Scoring Leader: Franky (814.62 PF)")

# Replace Award 2: $10 TE Bounty -> $10 DEF Bounty (Winner: Pedro / KC DEF)
deck6 = deck6.replace("⚡ $10 Weekly Bounty: Highest TE", "⚡ $10 Weekly Bounty: Highest DEF")
deck6 = deck6.replace("26.90 PTS", "16.00 PTS")
deck6 = deck6.replace("Isaiah Likely <span class=\"text-emerald-400 text-sm font-semibold\">(Njigbas in Paris / iRob)</span>", "Kansas City Chiefs DEF <span class=\"text-emerald-400 text-sm font-semibold\">(I Didn’t Hear No Bell / Pedro)</span>")
deck6 = re.sub(
    r'iRob goes back-to-back on weekly player bounties![\s\S]*?\$10 TE bounty cash prize!',
    'Pedro collects his first cash bounty of 2026! The Kansas City Chiefs defense put up a suffocating 16.00-point performance to edge out Denver (14.00) and Pittsburgh (10.00), earning Pedro the $10 defense cash prize and securing his 112.04 blowout win over Alex!',
    deck6
)
deck6 = deck6.replace("Runner-Up: Brock Bowers (19.00 PTS)", "Runner-Up: Denver Broncos DEF (14.00 PTS)")
deck6 = deck6.replace("iRob: $20 Total Bounties", "Pedro: $10 Direct Bounty")

# 4. Slide 1: State of the Union
deck6 = deck6.replace("WEEK 5 LEAGUE AUDIT • COMMISSIONER'S DESK", "WEEK 6 LEAGUE AUDIT • COMMISSIONER'S DESK")
deck6 = deck6.replace("🏛️ State of the Union: Week 5", "🏛️ State of the Union: Week 6")
deck6 = deck6.replace(
    "Two juggernauts separate at 4-1, Alex claims the scoring throne, and Franky's curse deepens.",
    "iRob takes sole possession of 1st place at 5-1, Franky wins the 285-point shootout of the year, and a 5-way logjam forms at 3-3."
)
deck6 = deck6.replace("5 of 14 Weeks Complete", "6 of 14 Weeks Complete")

deck6 = deck6.replace("4-1 Two-Man Breakaway", "5-1 Sole Monarch: iRob")
deck6 = re.sub(
    r'Arnulfo \(<em>MyDakMakesHerWaddle</em>: 654\.64 PF\) and iRob[\s\S]*?collecting league hardware\.',
    'iRob (<em>Njigbas in Paris</em>: 746.66 PF) stands alone atop the FFUC mountaintop at 5-1! Behind Isaiah Likely (20.90) and JSN (19.40), iRob dispatched Robert (106.36 to 79.62) to take sole possession of 1st place.',
    deck6
)

deck6 = deck6.replace("The 3-2 Playoff Pack", "The 3-3 Midfield Gridlock")
deck6 = deck6.replace("Alex, Joey & Eric in Lockstep", "5 Franchises Tied at 3-3")
deck6 = re.sub(
    r'Alex surges to #1 overall scoring \(688\.60 PF\)[\s\S]*?tied at 3-2\.',
    'Parity reigns across FFUC! Herrador (784.10 PF), Joey (776.14 PF), Alex (775.64 PF), Eric (703.86 PF), and Mark (692.58 PF) are all locked in a ferocious dogfight for the 6 playoff spots.',
    deck6
)

deck6 = deck6.replace("The Danger Zone", "The 2-4 Resurgence & Panic")
deck6 = deck6.replace("Franky (1-4) & Robert (2-3) Crisis", "Franky's High Roller & Robert's 5K Slide")
deck6 = re.sub(
    r'Robert\'s 2-game high roller streak was snapped[\s\S]*?buried at 1-4\.',
    'Franky scored 149.80 PTS to jump to a league-leading 814.62 season PF while moving to 2-4. Defending champion Robert slumped to a league-low 79.62, while Pedro (2-4) claimed his first signature win!',
    deck6
)

# 5. Slide 2: $10 Bounty Board
deck6 = deck6.replace("Week 5 Target: Highest Scoring TE ($10)", "Week 6 Target: Highest Scoring DEF ($10)")
deck6 = deck6.replace("Isaiah Likely • 26.90 PTS", "Kansas City Chiefs DEF • 16.00 PTS")
deck6 = deck6.replace("Manager: <strong class=\"text-slate-200\">iRob</strong> (Njigbas in Paris)", "Manager: <strong class=\"text-slate-200\">Pedro</strong> (I Didn’t Hear No Bell)")
deck6 = deck6.replace("⚡ The Dominant TE Statline:", "⚡ The Dominant DEF Statline:")
deck6 = re.sub(
    r'Isaiah Likely put up an unstoppable masterclass[\s\S]*?second consecutive \$10 bounty</strong>!',
    'The Kansas City Chiefs defense dominated with 16.00 fantasy points, generating sacks and turnovers to secure Pedro the $10 weekly defense bounty!',
    deck6
)

# Top 5 DEF table
top_def_html = (
    '<div class="space-y-1.5 text-xs font-mono">\n'
    '  <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-emerald-500/40">\n'
    '    <span class="font-bold text-emerald-400">1. Kansas City Chiefs • Pedro</span>\n'
    '    <span class="font-black text-white">16.00 PTS (WON $10)</span>\n'
    '  </div>\n'
    '  <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-300">\n'
    '    <span>2. Denver Broncos • iRob (Bench)</span>\n'
    '    <span class="font-bold text-amber-400">14.00 PTS</span>\n'
    '  </div>\n'
    '  <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-400">\n'
    '    <span>3. Pittsburgh Steelers • Alex (Bench)</span>\n'
    '    <span>10.00 PTS</span>\n'
    '  </div>\n'
    '  <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-400">\n'
    '    <span>4. Baltimore Ravens • Herrador</span>\n'
    '    <span>9.00 PTS</span>\n'
    '  </div>\n'
    '  <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-400">\n'
    '    <span>5. New England Patriots • Alex</span>\n'
    '    <span>6.00 PTS</span>\n'
    '  </div>\n'
    '</div>'
)
deck6 = re.sub(r'<div class="space-y-1\.5 text-xs font-mono">[\s\S]*?</div>\s*</div>\s*<div class="mt-4 pt-3 border-t', f'{top_def_html}\n</div>\n<div class="mt-4 pt-3 border-t', deck6, count=1)

# Next up: Week 7 Narrowest Victory ($10)
deck6 = deck6.replace("Week 6: Highest Scoring DEF ($10)", "Week 7: Narrowest Victory ($10)")
deck6 = re.sub(
    r'The bounty turns to the trenches![\s\S]*?takes home the \$10 cash payout\.',
    'Heart-stopping drama! The manager who secures the narrowest margin of victory in Week 7 takes home the $10 direct cash prize! Every yard and reception counts.',
    deck6
)

# 6. Slide 7: Pick-Em Leaderboard
deck6 = deck6.replace("through Week 5 (80 Total Games Picked)", "through Week 6 (95 Total Games Picked)")
deck6 = deck6.replace("Week 5 Pick-em scoring report is certified across all 10 managers (80 total NFL games decided)", "Week 6 Pick-em scoring report is certified across all 10 managers (95 total NFL games decided)")
deck6 = deck6.replace("Week 5 Certified", "Week 6 Certified")
deck6 = deck6.replace("Week 5 Verified Sync", "Week 6 Verified Sync")

deck6 = deck6.replace("👑 Solo Mountain Leader", "👑 Co-Leaders Atop the Mountain")
deck6 = deck6.replace("Robert (BACK 2 BACK) • 50.0 PTS", "Arnulfo & Robert • 58.0 PTS")
deck6 = re.sub(
    r'Robert becomes the first manager to reach 50 correct picks[\s\S]*?through 80 NFL games!',
    'Arnulfo went 10-for-14 in Week 6 to catch Robert (8-for-14) at 58.0 total points! Both now share the mountaintop with 95 NFL games decided.',
    deck6
)

deck6 = deck6.replace("🔥 Week 5 High Picker", "🔥 Week 6 High Pickers")
deck6 = deck6.replace("Joey (Swagsby) • 10.0 PTS", "Arnulfo & Franky • 10.0 PTS")
deck6 = re.sub(
    r'Joey went 10-for-16 in Week 5[\s\S]*?tie for 7th!',
    'Arnulfo and Franky dominated Week 6 game calls, each picking 10 winners out of 14 games to lead the league!',
    deck6
)

# 7. Slide 11: Week 6 Scoreboard
deck6 = deck6.replace("⚔️ Week 5 Scoreboard", "⚔️ Week 6 Scoreboard")
deck6 = deck6.replace("Final Matchup Audits • Official Scoring Breakdown", "Week 6 Final Matchup Audits • Official Scoring Breakdown")

# 8. Slide 12: Week 7 Gameday Hub
deck6 = deck6.replace("⚡ Week 6 Gameday Hub", "⚡ Week 7 Gameday Hub")
deck6 = deck6.replace("Week 6 Matchups, Spreads & Bounty Target Preview", "Week 7 Matchups, Spreads & Bounty Target Preview")
deck6 = deck6.replace("Target: Highest Scoring DEF ($10)", "Target: Narrowest Victory ($10)")

# Now inject deck-wk6 right before deck-wk5, and hide deck-wk5 by default!
deck5_hidden = re.sub(r'id="deck-wk5"[^>]*>', 'id="deck-wk5" class="hidden">', deck5_full)

new_deck_section = f"{deck6}\n\n    <!-- ==========================================\n    DECK 5: WEEK 5 ARCHIVE REPORT\n    ========================================== -->\n    {deck5_hidden}"

html_updated = html.replace(deck5_full, new_deck_section)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html_updated)

print(f"Generated and injected deck-wk6 successfully! Updated index.html length: {len(html_updated)} bytes")

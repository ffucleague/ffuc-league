import re, os, json, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# Build Slide 11 (Scoreboard for Week 6)
s11_matchups_html = """
        <div class="space-y-3">
          <!-- Matchup 1: Pedro def Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex-1 w-full">
              <div class="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span class="font-bold">Matchup 1 • Def. Champion Upset</span>
                <span class="font-mono text-emerald-400 font-semibold">Margin: +25.00 PTS</span>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40 mb-1.5">
                <div>
                  <div class="font-black text-white text-base flex items-center gap-2">
                    I Didn’t Hear No Bell (Pedro) <span class="text-[10px] bg-emerald-500 text-slate-950 font-black px-1.5 py-0.5 rounded">WIN</span>
                  </div>
                  <div class="text-[11px] text-slate-400">T. Lawrence 28.34 • M. Golden 19.40 • KC DEF 16.00 ($10 Bounty) • A. Jeanty 13.80</div>
                </div>
                <div class="text-xl font-black text-emerald-400 font-athletic">112.04</div>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <div>
                  <div class="font-black text-white text-base">Amon-Ra's Maye-hem (Alex)</div>
                  <div class="text-[11px] text-slate-400">J. Love 21.24 • DK Metcalf 14.80 • Fairbairn 11.00 • C. Skattebo 0.00</div>
                </div>
                <div class="text-xl font-black text-slate-400 font-athletic">87.04</div>
              </div>
            </div>
          </div>

          <!-- Matchup 2: iRob def Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex-1 w-full">
              <div class="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span class="font-bold">Matchup 2 • Battle for 1st Place</span>
                <span class="font-mono text-emerald-400 font-semibold">Margin: +26.74 PTS</span>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40 mb-1.5">
                <div>
                  <div class="font-black text-white text-base flex items-center gap-2">
                    Njigbas in Paris (iRob) <span class="text-[10px] bg-emerald-500 text-slate-950 font-black px-1.5 py-0.5 rounded">WIN (5-1)</span>
                  </div>
                  <div class="text-[11px] text-slate-400">Likely 20.90 • JSN 19.40 • Purdy 17.36 • R. White 13.70 • RJ Harvey 13.10</div>
                </div>
                <div class="text-xl font-black text-emerald-400 font-athletic">106.36</div>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-rose-950/30 border border-rose-800/40">
                <div>
                  <div class="font-black text-white text-base">WE GOIN’ BACK 2 BACK (Robert)</div>
                  <div class="text-[11px] text-slate-400">Rodgers 17.02 • Doubs 10.70 • London 10.20 • Bijan 6.30 • Fannin 1.40</div>
                </div>
                <div class="text-xl font-black text-rose-400 font-athletic">79.62</div>
              </div>
            </div>
          </div>

          <!-- Matchup 3: Franky def Joey -->
          <div class="bg-slate-900 border-2 border-amber-500/50 rounded-2xl p-4 shadow-2xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex-1 w-full">
              <div class="flex justify-between items-center text-xs text-amber-400 mb-1">
                <span class="font-black uppercase tracking-wider">🔥 Matchup 3 • 285-Point Game of the Year</span>
                <span class="font-mono text-emerald-400 font-bold">Margin: +14.52 PTS</span>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-amber-950/30 border border-amber-500/40 mb-1.5">
                <div>
                  <div class="font-black text-white text-base flex items-center gap-2">
                    CULT OF THE LAMB (Franky) <span class="text-[10px] bg-amber-500 text-slate-950 font-black px-1.5 py-0.5 rounded">HIGH ROLLER</span>
                  </div>
                  <div class="text-[11px] text-slate-400">J. Cook 22.80 • B. Tuten 22.70 • M. Nabers 22.50 • C. Williams 16.50 • Loveland 15.50</div>
                </div>
                <div class="text-xl font-black text-amber-400 font-athletic">149.80</div>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <div>
                  <div class="font-black text-white text-base">TheGreatSwagsby (Joey)</div>
                  <div class="text-[11px] text-slate-400">K. Walker 26.90 • McCaffrey 26.20 • C.J. Stroud 23.98 • E. Egbuka 14.30</div>
                </div>
                <div class="text-xl font-black text-slate-300 font-athletic">135.28</div>
              </div>
            </div>
          </div>

          <!-- Matchup 4: Mark def Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex-1 w-full">
              <div class="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span class="font-bold">Matchup 4 • Playoff Bubble Clash</span>
                <span class="font-mono text-emerald-400 font-semibold">Margin: +19.22 PTS</span>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40 mb-1.5">
                <div>
                  <div class="font-black text-white text-base flex items-center gap-2">
                    Saquon Deez Nacuas (Mark) <span class="text-[10px] bg-emerald-500 text-slate-950 font-black px-1.5 py-0.5 rounded">WIN (3-3)</span>
                  </div>
                  <div class="text-[11px] text-slate-400">Cousins 19.52 • Kittle 15.40 • Javonte 12.00 • Puka Nacua 11.00 • Little 10.00</div>
                </div>
                <div class="text-xl font-black text-emerald-400 font-athletic">101.42</div>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <div>
                  <div class="font-black text-white text-base">Show me dem TDs (Eric)</div>
                  <div class="text-[11px] text-slate-400">J. Taylor 20.10 • J. Allen 18.30 • D. Pierce 13.00 • M. Gay 12.00 • M. Andrews 0.90</div>
                </div>
                <div class="text-xl font-black text-slate-400 font-athletic">82.20</div>
              </div>
            </div>
          </div>

          <!-- Matchup 5: Herrador def Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex-1 w-full">
              <div class="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span class="font-bold">Matchup 5 • The 49-Point Annihilation</span>
                <span class="font-mono text-emerald-400 font-semibold">Margin: +49.68 PTS</span>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-emerald-950/30 border border-emerald-500/40 mb-1.5">
                <div>
                  <div class="font-black text-white text-base flex items-center gap-2">
                    Brock To The Future (Herrador) <span class="text-[10px] bg-emerald-500 text-slate-950 font-black px-1.5 py-0.5 rounded">WIN (3-3)</span>
                  </div>
                  <div class="text-[11px] text-slate-400">Swift 21.00 • Daniels 21.00 • Bernard 20.20 • Hubbard 18.60 • DeVonta Smith 17.00</div>
                </div>
                <div class="text-xl font-black text-emerald-400 font-athletic">137.40</div>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-slate-950/60 border border-slate-800/80">
                <div>
                  <div class="font-black text-white text-base">MyDakMakesHerWaddle (Arnulfo)</div>
                  <div class="text-[11px] text-slate-400">Tre Tucker 24.20 • Prescott 13.02 • Butker 11.00 • A.J. Brown 4.20</div>
                </div>
                <div class="text-xl font-black text-slate-400 font-athletic">87.72</div>
              </div>
            </div>
          </div>
        </div>
"""

# Replace in deck-wk6 section 11
pat_s11 = r'(<section id="wk6-slide-11"[\s\S]*?<div class="space-y-3">)[\s\S]*?(</div>\s*</section>)'
html = re.sub(pat_s11, f'\\g<1>{s11_matchups_html}\\g<2>', html, count=1)
print("Updated Slide 11 (Scoreboard)")

# Build Slide 7 (Pick-Em Standings Table)
pickem_table_html = """
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-4 border-b border-slate-800 flex justify-between items-center">
            <span class="text-xs font-bold uppercase tracking-wider text-slate-300">Official Sleeper Pick-em Standings (Ranks 1 to 10)</span>
            <span class="text-xs text-emerald-400 font-semibold font-mono">Week 6 Verified Sync (95 Games)</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-sm">
            <!-- T-1st: Arnulfo -->
            <div class="p-3.5 flex items-center justify-between bg-blue-950/30">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-amber-400">T-1</span>
                <div>
                  <span class="font-bold text-white">MyDakMakesHerWaddle</span>
                  <span class="text-xs text-slate-400 ml-1">(Arnulfo / AEscamilla94)</span>
                  <span class="text-xs text-emerald-400 ml-2 font-medium">👑 Co-Leader (W1: 9 • W2: 10 • W3: 11 • W4: 10 • W5: 8 • W6: 10)</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-amber-400 text-base">58.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-1st: Robert -->
            <div class="p-3.5 flex items-center justify-between bg-blue-950/30">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-amber-400">T-1</span>
                <div>
                  <span class="font-bold text-white">WE GOIN’ BACK 2 BACK</span>
                  <span class="text-xs text-slate-400 ml-1">(Robert / YaBoyRoZ)</span>
                  <span class="text-xs text-amber-400 ml-2 font-medium">👑 Co-Leader (W1: 12 • W2: 11 • W3: 8 • W4: 10 • W5: 9 • W6: 8)</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-amber-400 text-base">58.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-3rd: Herrador -->
            <div class="p-3.5 flex items-center justify-between bg-emerald-950/20">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-300">T-3</span>
                <div>
                  <span class="font-bold text-white">Brock To The Future</span>
                  <span class="text-xs text-slate-400 ml-1">(Herrador / DirtyDirties)</span>
                  <span class="text-xs text-emerald-400 ml-2 font-semibold">Podium Chase (W1: 10 • W2: 10 • W3: 8 • W4: 10 • W5: 9 • W6: 9)</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-emerald-400 text-base">56.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-3rd: iRob -->
            <div class="p-3.5 flex items-center justify-between bg-emerald-950/20">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-300">T-3</span>
                <div>
                  <span class="font-bold text-white">Njigbas in Paris</span>
                  <span class="text-xs text-slate-400 ml-1">(iRob / irobgarza16)</span>
                  <span class="text-xs text-emerald-400 ml-2 font-semibold">Podium Chase (W1: 11 • W2: 11 • W3: 8 • W4: 9 • W5: 9 • W6: 8)</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-emerald-400 text-base">56.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-5th: Franky -->
            <div class="p-3.5 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-400">T-5</span>
                <div>
                  <span class="font-bold text-slate-200">CULT OF THE LAMB</span>
                  <span class="text-xs text-slate-400 ml-1">(Franky / ChanciscoFravez)</span>
                  <span class="text-xs text-amber-400 ml-2 font-semibold">Week 6 High Picker (10-4) • W1: 10 • W2: 11 • W3: 6 • W4: 10 • W5: 7 • W6: 10</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-slate-200 text-base">54.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-5th: Pedro -->
            <div class="p-3.5 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-400">T-5</span>
                <div>
                  <span class="font-bold text-slate-200">I Didn’t Hear No Bell</span>
                  <span class="text-xs text-slate-400 ml-1">(Pedro / GuyNamedPedro)</span>
                  <span class="text-xs text-slate-400 ml-2">W1: 10 • W2: 10 • W3: 9 • W4: 10 • W5: 8 • W6: 7</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-slate-200 text-base">54.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-7th: Joey -->
            <div class="p-3.5 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-500">T-7</span>
                <div>
                  <span class="font-bold text-slate-300">TheGreatSwagsby</span>
                  <span class="text-xs text-slate-400 ml-1">(Joey / TheGreatSwagsby)</span>
                  <span class="text-xs text-slate-400 ml-2">W1: 10 • W2: 9 • W3: 6 • W4: 9 • W5: 10 • W6: 9</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-slate-300 text-base">53.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-7th: Alex -->
            <div class="p-3.5 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-500">T-7</span>
                <div>
                  <span class="font-bold text-slate-300">Amon-Ra's Maye-hem</span>
                  <span class="text-xs text-slate-400 ml-1">(Alex / abarrera731)</span>
                  <span class="text-xs text-slate-400 ml-2">W1: 10 • W2: 11 • W3: 6 • W4: 9 • W5: 8 • W6: 9</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-slate-300 text-base">53.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- T-7th: Eric -->
            <div class="p-3.5 flex items-center justify-between">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-slate-500">T-7</span>
                <div>
                  <span class="font-bold text-slate-300">Show me dem TDs</span>
                  <span class="text-xs text-slate-400 ml-1">(Eric / emedina13)</span>
                  <span class="text-xs text-slate-400 ml-2">W1: 11 • W2: 10 • W3: 7 • W4: 10 • W5: 8 • W6: 7</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-slate-300 text-base">53.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>

            <!-- 10th: Mark -->
            <div class="p-3.5 flex items-center justify-between bg-slate-950/40">
              <div class="flex items-center gap-3">
                <span class="w-6 text-center font-athletic text-xl font-bold text-rose-400">10</span>
                <div>
                  <span class="font-bold text-slate-300">Saquon Deez Nacuas</span>
                  <span class="text-xs text-slate-400 ml-1">(Mark / fattymcfatty)</span>
                  <span class="text-xs text-rose-400 ml-2">Striking Distance (-6.0) • W1: 11 • W2: 9 • W3: 7 • W4: 10 • W5: 7 • W6: 8</span>
                </div>
              </div>
              <div class="text-right">
                <span class="font-mono font-bold text-rose-400 text-base">52.0</span>
                <span class="text-xs text-slate-500 ml-1">pts</span>
              </div>
            </div>
          </div>
        </div>
"""

pat_s7 = r'(<section id="wk6-slide-7"[\s\S]*?)<div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">[\s\S]*?</div>\s*</div>\s*(<div class="mt-4 text-center">|\s*</section>)'
html = re.sub(pat_s7, f'\\g<1>{pickem_table_html}\n\\g<2>', html, count=1)
print("Updated Slide 7 (Pick-Em Table)")

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated index.html with Week 6 scoreboard and pick-em table!")

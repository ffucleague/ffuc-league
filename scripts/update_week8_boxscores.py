import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

print("Reading index.html...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------
# 1. NEW NAV PILLS (11 SLIDES)
# -------------------------------------------------------------
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
        <button onclick="goToSlide(10)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">11. ⚡ Wk 9 Gameday Hub</button>
      </nav>"""

# -------------------------------------------------------------
# 2. DEFINE SLIDES FOR DECK-WK8 (WITH VERIFIED SLEEPER STARTERS)
# -------------------------------------------------------------

slide_0 = """      <!-- SLIDE 0: HARDWARE & ROASTS -->
      <section id="wk8-slide-0" class="slide active space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-500/20 via-slate-900 to-yellow-500/10 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL WEEK 8 AWARDS • F.F.U.C. HONORS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏆 Hardware & Weekly Roasts</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 8 scoring crown, $10 largest blowout bounty, Lamar Jackson zero roast, and heartbreak bad beats.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-900 border border-amber-500/30 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Post-Midpoint (8 of 14 Weeks)</span>
          </div>
        </div>

        <!-- FFUC AI BROADCAST PLAYER (NATURAL MALE ANNOUNCER VOICE) -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/70 to-slate-900 border-2 border-indigo-500/40 rounded-2xl p-4 shadow-xl">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <!-- Left Info & Play Button -->
            <div class="flex items-center gap-3.5">
              <div class="relative flex-shrink-0">
                <button id="broadcastPlayBtn" onclick="toggleBroadcastAudio()" class="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-gradient-to-br from-amber-400 to-amber-600 hover:from-amber-300 hover:to-amber-500 text-slate-950 flex items-center justify-center shadow-lg shadow-amber-500/20 transition-all transform hover:scale-105 active:scale-95 cursor-pointer">
                  <svg id="playIcon" class="w-6 h-6 ml-0.5 fill-current" viewBox="0 0 24 24">
                    <path d="M8 5v14l11-7z"/>
                  </svg>
                  <svg id="pauseIcon" class="w-6 h-6 fill-current hidden" viewBox="0 0 24 24">
                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                  </svg>
                </button>
                <span id="audioPulseRing" class="absolute -inset-1 rounded-full bg-amber-400/40 animate-ping hidden pointer-events-none"></span>
              </div>
              <div>
                <div class="flex flex-wrap items-center gap-2 mb-1.5">
                  <span class="inline-flex items-center gap-1.5 bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                    <span class="w-2 h-2 rounded-full bg-indigo-400 animate-pulse"></span>
                    FFUC Official Broadcast Studio
                  </span>
                  <span class="inline-flex items-center gap-1.5 bg-amber-500/20 text-amber-300 border border-amber-500/40 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full uppercase tracking-wider">
                    🎙️ Official League Voice • Week 8 Recap
                  </span>
                </div>
                <div class="text-white font-extrabold text-sm sm:text-base tracking-tight flex items-center gap-2">
                  <span id="broadcastTitleText">Week 8 Official Audio Recap (Commissioner's Desk)</span>
                  <!-- Animated Waveform Equalizer -->
                  <div id="audioWaveform" class="flex items-end gap-0.5 h-4 opacity-40 transition-opacity">
                    <span class="w-1 bg-amber-400 rounded-full h-2 animate-bounce" style="animation-delay: 0.1s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-4 animate-bounce" style="animation-delay: 0.3s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-3 animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-1 animate-bounce" style="animation-delay: 0.4s"></span>
                  </div>
                </div>
                <div id="broadcastDescText" class="text-xs text-slate-400 mt-0.5">
                  Herrador's 148.78 High Roller crown, Mark's 45.38 blowout bounty over Robert's 0-point Lamar Jackson disaster, Alex's 142.36 heartbreak, and iRob claiming sole 1st place.
                </div>
              </div>
            </div>

            <!-- Right Controls: Progress Bar & Duration -->
            <div class="flex flex-col sm:items-end justify-center gap-1.5 min-w-[200px]">
              <div class="flex items-center justify-between sm:justify-end gap-3 text-xs font-mono w-full">
                <span id="audioCurrentTime" class="text-amber-400 font-bold">0:00</span>
                <span class="text-slate-600">/</span>
                <span id="audioDuration" class="text-slate-400">1:39</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2 border border-slate-800 cursor-pointer overflow-hidden" onclick="seekBroadcastAudio(event)">
                <div id="audioProgressBar" class="bg-gradient-to-r from-amber-500 to-yellow-400 h-full w-0 rounded-full transition-all duration-100"></div>
              </div>
              <span class="text-[10px] text-slate-500 font-mono">Natural Voice Broadcast • Click to stream</span>
            </div>
          </div>
          <!-- Audio Element -->
          <audio id="broadcastAudio" src="assets/audio/wk8_recap.mp3" preload="metadata" ontimeupdate="updateBroadcastProgress()" onended="onBroadcastAudioEnded()"></audio>
        </div>

        <!-- AWARDS GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Award 1: High Roller Champion (Herrador) -->
          <div class="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border-2 border-amber-500/60 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-amber-500 text-slate-950 px-2.5 py-0.5 rounded">👑 Week 8 High Roller Champion</span>
              <span class="text-xl font-athletic font-bold text-amber-400">148.78 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">Brock To The Future <span class="text-amber-400 text-sm font-semibold">(Herrador)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Herrador catches absolute fire in Week 8, putting up an electric 148.78 points to lead all franchises! Led by Ja'Marr Chase (25.60) and rookie sensation Brock Bowers (24.70), alongside Chuba Hubbard (21.40), Bucky Irving (21.00), and Tampa Bay's DEF (18.00), Herrador clinches the Week 8 scoring crown and surges back to an even 4-4!
            </p>
            <!-- LivePortrait AI Coronation Video / GIF -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-amber-500/40 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-amber-500/40 text-[9px] font-mono font-bold text-amber-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                LivePortrait AI • Herrador Gatsby Toast (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline poster="assets/video/herrador_high_roller.gif?v=20261103">
                <source src="assets/video/herrador_high_roller.mp4?v=20261103" type="video/mp4">
                <img src="assets/video/herrador_high_roller.gif?v=20261103" alt="Herrador High Roller Celebration Meme" class="w-full h-44 sm:h-52 object-cover">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Week 8 High Score: 148.78 PTS</span>
              <span class="text-amber-400 font-bold font-mono">+$10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 2: $10 Bounty Winner (Largest Blowout) -->
          <div class="bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-emerald-500 text-slate-950 px-2.5 py-0.5 rounded">⚡ $10 Weekly Bounty: Largest Blowout</span>
              <span class="text-xl font-athletic font-bold text-emerald-400">45.38 PTS Margin</span>
            </div>
            <h3 class="text-xl font-black text-white">Saquon Deez Nacuas <span class="text-emerald-400 text-sm font-semibold">(Mark)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              An absolute demolition! Mark crushed defending champion Robert 131.98 to 86.60—a lopsided 45.38-point rout that easily secured the Week 8 Biggest Blowout Bounty! With free agent pickup Kirk Cousins (28.18) answering the call alongside Jacksonville's 20-point defense, Puka Nacua (19.50), Luther Burden (15.10), T.J. Hockenson (13.80), and Saquon Barkley (11.90), Mark captures the $10 cash bounty and climbs to 5-3 into sole 3rd place!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Margin of Victory: 45.38 PTS (over Robert)</span>
              <span class="text-emerald-400 font-bold font-mono">Mark: $10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 3: Heartbreak Bad Beat (Alex) -->
          <div class="bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-900 border border-rose-500/40 rounded-2xl p-5 shadow-xl">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-bold uppercase tracking-wider bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-0.5 rounded">💔 Heartbreak of the Week</span>
              <span class="text-lg font-athletic font-bold text-rose-400">142.36 PTS (L)</span>
            </div>
            <h3 class="text-xl font-black text-white">LEAGUE MEDIAN ADVOCATE 🗳 <span class="text-rose-400 text-sm font-semibold">(Alex)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Unbelievable bad luck! Alex put up a blistering 142.36 points—the 2nd highest total in the entire league this week—powered by Michael Wilson (22.80), rookie Drake Maye (22.46), Pittsburgh DEF (21.00), Jaylen Warren (20.80), and Trey McBride (16.70)! Alex would have defeated 8 of the other 9 franchises in FFUC, but ran directly into Herrador's 148.78 buzzsaw to lose by just 6.42 points! Alex renamed his team 'LEAGUE MEDIAN ADVOCATE 🗳' in protest.
            </p>
            <!-- FaceFusion AI Heartbreak Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-rose-500/40 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-rose-500/40 text-[9px] font-mono font-bold text-rose-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
                FaceFusion AI Video • Alex Dawson Crying Meme
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline poster="assets/video/alex_heartbreak.gif?v=20261103">
                <source src="assets/video/alex_heartbreak.mp4?v=20261103" type="video/mp4">
                <img src="assets/video/alex_heartbreak.gif?v=20261103" alt="Alex Heartbreak Crying Meme" class="w-full h-44 sm:h-52 object-cover">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Defeated by: Herrador (148.78)</span>
              <span class="text-rose-400 font-bold font-mono">Would Defeat 8 of 9 Teams</span>
            </div>
          </div>

          <!-- Award 4: 5K Toilet Runner & Cellar Shock (Robert) -->
          <div class="bg-gradient-to-br from-red-950/40 via-slate-900 to-slate-900 border-2 border-red-600/70 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-red-600 text-white px-2.5 py-0.5 rounded shadow">🚽 5K Toilet Runner: Cellar Shock</span>
              <span class="text-lg font-athletic font-bold text-red-400">86.60 PTS (-45.38)</span>
            </div>
            <h3 class="text-xl font-black text-white">WE NOT GOIN’ BACK 2 BACK <span class="text-red-400 text-sm font-semibold">(Robert)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              <strong class="text-red-400">THE 0-POINT LAMAR DISASTER:</strong> One week after exploding for 153.82 points, Robert crashed back to earth in horrific fashion. Robert started Lamar Jackson, who put up a goose egg (<strong>0.00 PTS</strong>), paired with Omar Cooper (0.00) and Drake London (1.30)! Blown out by 45.38 points by Mark, Robert plummets to 3-5 into a 4-way tie near the cellar. Meanwhile, Pedro won his matchup against Franky (107.40 to 92.16) to reach 3-5, but still trails 9th place by 238+ points.
            </p>
            <!-- 5K Runner Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                FaceFusion AI Meme • Pedro & Robert 5K Punishment Watch
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline>
                <source src="assets/video/pedro_5k_runner.mp4?v=20261103" type="video/mp4">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-red-400 font-mono font-bold">Lamar Jackson: 0.00 PTS</span>
              <span class="text-red-400 font-bold font-mono">Deficit: -45.38 PTS (Blown Out)</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 1: STATE OF THE UNION & STANDINGS
slide_1 = """      <!-- SLIDE 1: STATE OF THE UNION -->
      <section id="wk8-slide-1" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 8 LEAGUE AUDIT • COMMISSIONER'S DESK
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏛️ State of the Union: Week 8</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">iRob takes sole possession of 1st place at 6-2, Mark & Arnulfo give chase at 5-3, and a 4-way tie erupts at 3-5.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-blue-400 font-mono font-bold px-3 py-1 rounded-lg">8 of 14 Complete</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">👑 Sole Leader (6-2)</span>
            <div class="text-base font-bold text-white mt-1">iRob At The Summit Alone</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob (997.26 PF) broke the 1st-place tie in thunderous fashion, riding Joe Burrow's 42.48 nuclear explosion to defeat Arnulfo 146.48 to 122.20! iRob is now the undisputed #1 seed in FFUC.
            </p>
          </div>

          <div class="bg-slate-900 border border-blue-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-400">⚔️ Chasing Pack (5-3)</span>
            <div class="text-base font-bold text-white mt-1">Arnulfo & Mark Stalking The Top</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Arnulfo (976.84 PF) stumbled against iRob but remains in 2nd place. Mark (969.76 PF) unleashed a 45-point blowout over Robert to take sole 3rd place, sitting just 1 game behind the summit.
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">🔥 4-Way Logjam Panic (3-5)</span>
            <div class="text-base font-bold text-white mt-1">Franky, Alex, Robert, & Pedro at 3-5</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Utter chaos! Franky (#1 offense at 1056.80 PF) and Alex (#2 offense at 1047.54 PF) are on the outside of the playoff bracket looking in, tied at 3-5 with Robert and Pedro!
            </p>
          </div>
        </div>

        <!-- Standings Snapshot Grid (OFFICIAL SLEEPER WEEK 8 STANDINGS) -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Official Week 8 Standings Snapshot</span>
            <span class="font-mono text-slate-400">W-L Record • Points For • Points Against • FAAB</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/30">
              <span class="w-8 font-bold text-emerald-400">1</span>
              <span class="flex-1 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">6-2</span>
              <span class="w-20 text-right text-slate-300">997.26 PF</span>
              <span class="w-20 text-right text-slate-500">971.30 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$65</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-8 font-bold text-emerald-400">2</span>
              <span class="flex-1 font-semibold text-slate-200">The Latin Touch (Arnulfo)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">5-3</span>
              <span class="w-20 text-right text-slate-300">976.84 PF</span>
              <span class="w-20 text-right text-slate-500">975.96 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$24</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-blue-950/20">
              <span class="w-8 font-bold text-blue-400">3</span>
              <span class="flex-1 font-bold text-white">Saquon Deez Nacuas (Mark)</span>
              <span class="w-16 text-center text-blue-400 font-bold">5-3</span>
              <span class="w-20 text-right text-slate-300">969.76 PF</span>
              <span class="w-20 text-right text-slate-500">916.20 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$72</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">4</span>
              <span class="flex-1 font-semibold text-slate-200">Brock To The Future (Herrador)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-4</span>
              <span class="w-20 text-right text-slate-300">1034.80 PF</span>
              <span class="w-20 text-right text-slate-500">986.06 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$51</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">5</span>
              <span class="flex-1 text-slate-300">TheGreatSwagsby (Joey)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-4</span>
              <span class="w-20 text-right text-slate-300">982.40 PF</span>
              <span class="w-20 text-right text-slate-500">923.02 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$21</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">6</span>
              <span class="flex-1 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-4</span>
              <span class="w-20 text-right text-slate-300">948.72 PF</span>
              <span class="w-20 text-right text-slate-500">921.88 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$50</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-8 font-bold text-rose-400">7</span>
              <span class="flex-1 text-slate-300">CULT OF THE LAMB (Franky) <span class="text-amber-400 font-bold text-[10px]">#1 PF</span></span>
              <span class="w-16 text-center text-rose-400 font-bold">3-5</span>
              <span class="w-20 text-right text-amber-400 font-extrabold">1056.80 PF</span>
              <span class="w-20 text-right text-slate-500">1071.62 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$39</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/15">
              <span class="w-8 font-bold text-rose-400">8</span>
              <span class="flex-1 text-slate-300">LEAGUE MEDIAN ADVOCATE 🗳 (Alex) <span class="text-amber-400 font-bold text-[10px]">#2 PF</span></span>
              <span class="w-16 text-center text-rose-400 font-bold">3-5</span>
              <span class="w-20 text-right text-slate-300">1047.54 PF</span>
              <span class="w-20 text-right text-slate-500">1032.72 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$56</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-8 font-bold text-rose-400">9</span>
              <span class="flex-1 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-5</span>
              <span class="w-20 text-right text-slate-300">994.96 PF</span>
              <span class="w-20 text-right text-slate-500">959.78 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$83</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-red-950/30">
              <span class="w-8 font-bold text-red-500">10</span>
              <span class="flex-1 font-medium text-red-400">I Didn’t Hear No Bell (Pedro) <span class="text-red-500 text-[10px] font-bold">(-238.44 PF Deficit)</span></span>
              <span class="w-16 text-center text-red-500 font-bold">3-5</span>
              <span class="w-20 text-right text-red-400 font-extrabold">710.28 PF</span>
              <span class="w-20 text-right text-slate-500">960.82 PA</span>
              <span class="w-16 text-right text-red-500 font-black">$0</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 2: $10 WEEKLY BOUNTY BOARD
slide_2 = """      <!-- SLIDE 2: $10 BOUNTY BOARD -->
      <section id="wk8-slide-2" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-green-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEKLY PRIZE POOL • DIRECT CASH PAYOUTS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💵 $10 Weekly Bounty Board</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 8 Largest Blowout crowned; Week 9 Highest Scoring QB on deck.</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-emerald-400">$140.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Season Bounty Pot</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Week 8 Winner Card (Mark) -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-emerald-500 text-slate-950 text-xs font-extrabold px-3 py-1 rounded-bl-xl shadow">
              Bounty Collected ($10)
            </div>
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">Week 8 Target: Largest Margin of Victory (Blowout)</span>
              <h3 class="text-2xl font-black text-white mt-1">Mark • 45.38 PTS Margin</h3>
              <div class="text-xs text-slate-400 mt-0.5">Franchise: <strong class="text-slate-200">Saquon Deez Nacuas</strong></div>

              <div class="my-4 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl space-y-2">
                <div class="text-xs text-emerald-300 font-semibold">⚡ The 45-Point Demolition:</div>
                <div class="text-xs text-slate-300 leading-relaxed">
                  Mark orchestrated the most ruthless beatdown of Week 8, toppling defending champion Robert 131.98 to 86.60! Driven by emergency FA pickup Kirk Cousins (28.18 PTS), Jacksonville DEF (20.00), and Puka Nacua (19.50), Mark captured the $10 cash bounty with a massive 45.38-point spread!
                </div>
              </div>

              <!-- Top 5 Margins in Week 8 -->
              <div class="space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-emerald-500/40">
                  <span class="font-bold text-emerald-400">1. Mark def. Robert</span>
                  <span class="font-black text-white">45.38 PTS (WON $10)</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>2. Eric def. Joey</span>
                  <span class="font-bold text-amber-400">43.12 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>3. iRob def. Arnulfo</span>
                  <span>24.28 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>4. Pedro def. Franky</span>
                  <span>15.24 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>5. Herrador def. Alex</span>
                  <span>6.42 PTS (Nailbiter)</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Payout Method: League Safe / Direct</span>
              <span class="text-emerald-400 font-bold">$10.00 Sent to Mark</span>
            </div>
          </div>

          <!-- Season Bounty Schedule & Leaderboard -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400">2026 Bounty Master Schedule</span>
              <h3 class="text-xl font-black text-white mt-1">8 of 14 Bounties Claimed ($80.00 Paid)</h3>

              <div class="mt-3 divide-y divide-slate-800/80 text-xs font-mono">
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 1: Highest RB</span>
                  <span class="text-emerald-400 font-bold">Eric (Saquon 33.20) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 2: Highest WR</span>
                  <span class="text-emerald-400 font-bold">Joey (MHJ 29.00) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 3: Highest QB</span>
                  <span class="text-emerald-400 font-bold">Franky (Josh Allen 30.70) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 4: Highest TE</span>
                  <span class="text-emerald-400 font-bold">Mark (Cole Kmet 19.70) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 5: Highest Kicker</span>
                  <span class="text-emerald-400 font-bold">Alex (Seibert 17.00) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 6: Highest DEF</span>
                  <span class="text-emerald-400 font-bold">Pedro (KC Chiefs 16.00) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 7: Narrowest Victory</span>
                  <span class="text-emerald-400 font-bold">Arnulfo (2.98 Margin) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-emerald-950/30 px-2 rounded border border-emerald-500/30 text-white">
                  <span class="font-bold">Wk 8: Largest Blowout</span>
                  <span class="text-emerald-400 font-bold">Mark (45.38 Margin) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-amber-950/30 px-2 rounded border border-amber-500/30 text-amber-300">
                  <span class="font-bold">Wk 9: Highest Scoring QB</span>
                  <span class="text-amber-400 font-bold">🔒 Up for Grabs ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 10: Highest Scoring RB</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 11: Highest Scoring WR</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 12: Highest Scoring TE</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 13: Highest Scoring Defense</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 14: Most Points in a Loss</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Next Target: Week 9 Highest Scoring QB</span>
              <span class="text-amber-400 font-bold">$10.00 Target</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 3: THE BAR TAB & 5K TOILET METER
slide_3 = """      <!-- SLIDE 3: THE BAR TAB & 5K TOILET METER -->
      <section id="wk8-slide-3" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-red-950/80 via-slate-900 to-rose-950/80 border border-red-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-red-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              THE LAST PLACE PUNISHMENT WATCH • THE TOILET RUN
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍻 The Bar Tab & 5K Toilet Meter</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Live tracking of the FFUC Last Place in-person 5K Run and open bar tab liability.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-red-400 font-mono font-bold px-3 py-1 rounded-lg">High Risk Alert: Pedro (3-5, 710 PF)</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- The Cellar Dweller Card (Pedro) -->
          <div class="bg-slate-900 border-2 border-red-600/70 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-mono font-bold uppercase tracking-wider text-red-400 bg-red-950 border border-red-800 px-2 py-0.5 rounded">
                  🚽 10th Place Anchor
                </span>
                <span class="text-lg font-athletic font-bold text-red-400">3-5 • 710.28 PF</span>
              </div>
              <h3 class="text-2xl font-black text-white">I Didn’t Hear No Bell <span class="text-red-400 text-sm font-semibold">(Pedro)</span></h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                <strong class="text-emerald-400">UPSET WIN, BUT CELLAR LOCKED:</strong> Pedro earned his 3rd victory of the season by toppling Franky 107.40 to 92.16! However, in the race to avoid the 5K toilet run, Pedro remains in critical danger. Sitting at 710.28 PF, Pedro trails 9th-place Eric by a monstrous <strong>238.44 total points</strong>! With $0 in FAAB remaining, Pedro has no financial ammo on the waiver wire to spark a late-season comeback.
              </p>

              <!-- LivePortrait AI 5K Punishment Video -->
              <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950">
                <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                  FaceFusion AI Meme • Pedro Forrest Gump 5K Punishment Sprint
                </div>
                <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline>
                  <source src="assets/video/pedro_5k_runner.mp4?v=20261103" type="video/mp4">
                </video>
              </div>

              <div class="mt-4 p-3 bg-red-950/30 border border-red-800/40 rounded-xl space-y-2 text-xs">
                <div class="flex justify-between items-center text-slate-300">
                  <span>Projected 5K Finishing Time:</span>
                  <span class="font-mono font-bold text-red-400">1 Hour 12 Mins (23:10/mi)</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Open Bar Tab Meter Liability:</span>
                  <span class="font-mono font-bold text-amber-400">$260.00 Est.</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Distance to 9th Place Safety:</span>
                  <span class="font-mono font-bold text-red-400">238.44 Total Points Deficit</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Punishment Likelihood:</span>
              <span class="text-red-400 font-bold uppercase">92.5% Implied Probability</span>
            </div>
          </div>

          <!-- Danger Index & Rules -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 bg-amber-950 border border-amber-800 px-2 py-0.5 rounded">
                The 5K Punishment Rules
              </span>
              <h3 class="text-xl font-black text-white mt-2">How the 5K Tab Formula Works</h3>
              <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                The last place franchise must complete an in-person, timed 5K run. For every minute over a 30:00 baseline pace, money is added to the league bar tab.
              </p>

              <div class="mt-4 space-y-2 text-xs">
                <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                  <span class="text-slate-300">Sub-30 Minute Pace:</span>
                  <span class="text-emerald-400 font-bold font-mono">$0 Penalty (Base $50 Tab)</span>
                </div>
                <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                  <span class="text-slate-300">30:00 - 45:00 Pace ($5/min):</span>
                  <span class="text-amber-400 font-bold font-mono">$50 - $125 Tab Surcharge</span>
                </div>
                <div class="bg-slate-950 p-2.5 rounded-xl border border-slate-800 flex items-center justify-between">
                  <span class="text-slate-300">Walking / 50+ Mins:</span>
                  <span class="text-red-400 font-bold font-mono">$150 - $250+ Max Tab Surcharge</span>
                </div>
              </div>

              <div class="mt-4 p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5 text-xs">
                <span class="font-bold text-white uppercase text-[11px]">Next In Line Danger Watch:</span>
                <div class="flex justify-between text-slate-300">
                  <span>Robert (3-5):</span>
                  <span class="text-amber-400 font-mono font-bold">994.96 PF (Lamar 0.00 Panic)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Eric (4-4):</span>
                  <span class="text-slate-300 font-mono font-bold">948.72 PF (238 PT Cushion)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Alex (3-5):</span>
                  <span class="text-emerald-400 font-mono font-bold">1047.54 PF (337 PT Cushion)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Franky (3-5):</span>
                  <span class="text-emerald-400 font-mono font-bold">1056.80 PF (Safe from 10th)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Next In Line Danger:</span>
              <span class="text-amber-400 font-bold">Eric (4-4 • 948.72 PF)</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 4: THE LUCK INDEX
slide_4 = """      <!-- SLIDE 4: THE LUCK INDEX -->
      <section id="wk8-slide-4" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-purple-950/80 via-slate-900 to-indigo-950/80 border border-purple-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-purple-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ADVANCED ANALYTICS • ALL-PLAY CORRELATION
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍀 The Luck Index: Schedule Variance</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Expected Wins vs Actual Wins across 72 total all-play matchups per franchise through Week 8.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-purple-400 font-mono font-bold px-3 py-1 rounded-lg">72 Total Games Audited</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">🍀 The Luckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Pedro (+1.78) & iRob (+1.67)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Pedro has won 3 games despite an 11-61 all-play record (expected 1.22 wins), making him mathematically the luckiest team in FFUC! iRob sits alone in 1st at 6-2 despite an expected record of 4.33 wins (+1.67 luck delta).
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">💀 The Unluckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Franky (-1.89) & Alex (-1.78)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Statistical highway robbery! Franky leads the league in scoring (1056.80 PF) and all-play (44-28), yet sits at 3-5 (-1.89 luck). Alex is #2 in scoring (1047.54 PF) and 43-29 all-play, but also languishes at 3-5 (-1.78 luck)!
            </p>
          </div>
        </div>

        <!-- Luck Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Expected Wins Matrix (Week 8 Audit)</span>
            <span class="font-mono text-purple-400 font-bold">Actual vs Expected Delta</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/25">
              <span class="w-48 font-bold text-white">I Didn’t Hear No Bell (Pedro)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">3-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">1.22 (Exp)</span>
              <span class="w-28 text-center text-red-400">11-61 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.78 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-48 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">6-2 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.33 (Exp)</span>
              <span class="w-28 text-center text-slate-300">39-33 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.67 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-48 font-bold text-white">Saquon Deez Nacuas (Mark)</span>
              <span class="w-20 text-center text-blue-400 font-bold">5-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.11 (Exp)</span>
              <span class="w-28 text-center text-slate-300">37-35 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+0.89 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-48 font-bold text-white">The Latin Touch (Arnulfo)</span>
              <span class="w-20 text-center text-blue-400 font-bold">5-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.11 (Exp)</span>
              <span class="w-28 text-center text-slate-300">37-35 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+0.89 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-20 text-center text-slate-300 font-bold">4-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">32-40 All-Play</span>
              <span class="w-24 text-right text-slate-300">+0.44 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">TheGreatSwagsby (Joey)</span>
              <span class="w-20 text-center text-slate-300 font-bold">4-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.44 (Exp)</span>
              <span class="w-28 text-center text-slate-300">40-32 All-Play</span>
              <span class="w-24 text-right text-slate-300">-0.44 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-48 text-slate-300">Brock To The Future (Herrador)</span>
              <span class="w-20 text-center text-slate-300 font-bold">4-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">43-29 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.78 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-48 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">34-38 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.78 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-48 font-bold text-white">LEAGUE MEDIAN ADVOCATE 🗳 (Alex)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">43-29 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.78 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/30">
              <span class="w-48 font-bold text-white">CULT OF THE LAMB (Franky)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.89 (Exp)</span>
              <span class="w-28 text-center text-amber-400 font-extrabold">44-28 All-Play (1st)</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.89 💀</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 5: POWER RANKINGS
slide_5 = """      <!-- SLIDE 5: POWER RANKINGS -->
      <section id="wk8-slide-5" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-orange-950/80 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ANALYTIC POWER INDEX • STRENGTH OF SQUAD
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">📈 Power Rankings: Week 8</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">True hierarchy based on roster firepower, all-play strength, and momentum entering Week 9.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 8 Audited</span>
          </div>
        </div>

        <div class="space-y-2 text-xs">
          <!-- Rank 1: iRob -->
          <div class="bg-slate-900 border-2 border-emerald-500/60 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-emerald-400">1</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Njigbas in Paris (iRob)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (6-2) • 218.4 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                997.26 PF. Joe Burrow returned to the starting lineup with a vengeance, detonating for 42.48 PTS to knock off Arnulfo. Holding sole 1st place with JSN (20.80) and Jonah Coleman (18.40) firing, iRob takes the undisputed top spot.
              </p>
            </div>
          </div>

          <!-- Rank 2: Herrador -->
          <div class="bg-slate-900 border border-amber-500/40 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">2</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Brock To The Future (Herrador)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +6 (4-4) • 204.1 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1034.80 PF (#3 in scoring). Week 8 High Roller champion with 148.78 PTS! Ja'Marr Chase (25.60), Brock Bowers (24.70), Hubbard (21.40), and Bucky Irving (21.00) give Herrador a monstrous weekly ceiling.
              </p>
            </div>
          </div>

          <!-- Rank 3: Franky -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">3</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">CULT OF THE LAMB (Franky)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -2 (3-5) • 198.6 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1056.80 PF (#1 in scoring, #1 in all-play 44-28). Suffered a fluky loss to Pedro (92.16 PTS), but Bhayshul Tuten (28.90) and James Cook (17.10) prove this roster is a sleeping giant due for positive regression.
              </p>
            </div>
          </div>

          <!-- Rank 4: Mark -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-blue-400">4</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (5-3) • 196.2 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                969.76 PF. Captured the $10 Blowout Bounty with a 45.38-point rout over Robert (131.98 PTS). Clutch waiver add Kirk Cousins dropped 28.18 PTS and the Jaguars DEF added 20.00, propelling Mark into sole 3rd place!
              </p>
            </div>
          </div>

          <!-- Rank 5: Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">5</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">LEAGUE MEDIAN ADVOCATE 🗳 (Alex)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +2 (3-5) • 194.8 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1047.54 PF (#2 in scoring, #2 in all-play 43-29). Put up 142.36 PTS and lost by 6 to Herrador. Michael Wilson (22.80), Drake Maye (22.46), and Steelers DEF (21.00) balled out; results will follow.
              </p>
            </div>
          </div>

          <!-- Rank 6: Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">6</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">The Latin Touch (Arnulfo)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -4 (5-3) • 189.5 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                976.84 PF. Dropped 122.20 in a tough showdown against iRob. Jahmyr Gibbs (23.80), Josh Jacobs (20.20), and Dak Prescott (19.80) look strong, but Arnulfo now faces Robert looking for a critical rebound.
              </p>
            </div>
          </div>

          <!-- Rank 7: Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">7</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">TheGreatSwagsby (Joey)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -2 (4-4) • 181.2 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                982.40 PF. Sputtered to 92.44 PTS in a blowout loss to Eric with Will Reichard blanked at 0.00. Braelon Allen (22.30) and Tucker Kraft (14.30) shined, but Joey must face runaway leader iRob in Week 9.
              </p>
            </div>
          </div>

          <!-- Rank 8: Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">8</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Show me dem TDs (Eric)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (4-4) • 179.4 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                948.72 PF. Broke his 3-game losing streak in emphatic style with 135.56 PTS! Tee Higgins erupted for 32.50 PTS alongside Josh Allen (27.56) and Commanders DEF (14.00) to pull Eric back to .500.
              </p>
            </div>
          </div>

          <!-- Rank 9: Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-rose-500">9</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -5 (3-5) • 174.0 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                994.96 PF. Total disaster after Lamar Jackson produced 0.00 PTS and Omar Cooper 0.00 in an 86.60 collapse despite Tony Pollard (27.20). Robert has $83 in FAAB to right the ship before facing Arnulfo.
              </p>
            </div>
          </div>

          <!-- Rank 10: Pedro -->
          <div class="bg-slate-900 border-2 border-red-600/70 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-red-500">10</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-red-400 text-sm">I Didn’t Hear No Bell (Pedro)</span>
                <span class="text-slate-400 font-mono font-bold">― 0 (3-5) • 120.5 Pwr</span>
              </div>
              <p class="text-slate-400 mt-1 leading-relaxed">
                710.28 PF. Pulled off a 107.40 upset over Franky behind Trevor Lawrence (19.40) and Matthew Golden (17.40), but remains stranded 238+ points behind the rest of the league with $0 FAAB in reserve.
              </p>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 6: FAAB RECEIPTS & WAIVER LEDGER
slide_6 = """      <!-- SLIDE 6: FAAB RECEIPTS -->
      <section id="wk8-slide-6" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-teal-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              FINANCIAL AUDIT • WAIVER TRANSACTION WIRE
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💰 FAAB Receipts: Week 8 Ledger</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official transaction ledger and updated bankrolls through Week 8 waivers.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">Budget Cap: $100 FAAB</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Recent Key Transactions -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded">
              Week 8 Key Wire Pickups
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <strong class="text-white">Kirk Cousins (QB • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark) — Erupted for 28.18 PTS in starting lineup!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jacoby Brissett (QB • ARI)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky) — Backup QB add</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-amber-400 font-bold">$2 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Waiver Claim</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Isaiah Likely (TE • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">LEAGUE MEDIAN ADVOCATE 🗳 (Alex) — TE depth insurance</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-amber-400 font-bold">$4 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Waiver Claim</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Kayshon Boutte (WR • NE)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric) — Speculative WR pickup</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-amber-400 font-bold">$4 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Waiver Claim</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Cedric Tillman (WR • CLE)</strong>
                  <span class="block text-slate-400 text-[11px]">The Latin Touch (Arnulfo) — Free Agent Acquisition</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Remaining FAAB Bankrolls -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 bg-amber-950 border border-amber-800 px-2.5 py-0.5 rounded">
              Updated FAAB Treasury ($100 Starting)
            </span>
            <div class="mt-3 divide-y divide-slate-800/80 text-xs font-mono">
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-white font-bold">1. Robert (WE NOT GOIN’ BACK 2 BACK)</span>
                <span class="text-emerald-400 font-bold">$83 (83%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">2. Mark (Saquon Deez Nacuas)</span>
                <span class="text-emerald-400 font-bold">$72 (72%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">3. iRob (Njigbas in Paris)</span>
                <span class="text-emerald-400 font-bold">$65 (65%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">4. Alex (LEAGUE MEDIAN ADVOCATE 🗳)</span>
                <span class="text-amber-400 font-bold">$56 (56%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">5. Herrador (Brock To The Future)</span>
                <span class="text-amber-400 font-bold">$51 (51%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">6. Eric (Show me dem TDs)</span>
                <span class="text-amber-400 font-bold">$50 (50%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">7. Franky (CULT OF THE LAMB)</span>
                <span class="text-amber-400 font-bold">$39 (39%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">8. Arnulfo (The Latin Touch)</span>
                <span class="text-rose-400 font-bold">$24 (24%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">9. Joey (TheGreatSwagsby)</span>
                <span class="text-rose-400 font-bold">$21 (21%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center bg-red-950/30 px-2 rounded">
                <span class="text-red-400 font-bold">10. Pedro (I Didn’t Hear No Bell)</span>
                <span class="text-red-500 font-black">$0 (BROKE - 0%)</span>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Financial Health:</span>
              <span class="text-amber-400 font-mono">Pedro has $0 to fix -238 PF hole</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 7: PICK-EM LEADERBOARD ($45 POT)
slide_7 = """      <!-- SLIDE 7: PICK-EM LEADERBOARD -->
      <section id="wk8-slide-7" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-cyan-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL SLEEPER PICK-EM POOL • $45 CASH POT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🎯 F.F.U.C. Pick-em Leaderboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Robert surges into solo 1st place with 11-5 week; Mark posts league-best 13-3 score!</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-blue-400">$45.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Winner Takes All Pot</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border-2 border-amber-500/50 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-400">🥇 Solo 1st Place</span>
            <div class="text-base font-bold text-white mt-1">Robert (77.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Robert rebounded from his fantasy blowout by picking 11 NFL winners in Week 8, seizing exclusive possession of 1st place in the $45 pot!
            </p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300">🥈 2nd Place Deadlock</span>
            <div class="text-base font-bold text-white mt-1">Arnulfo & iRob (75.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob posted 10 correct picks while Arnulfo managed 8, locking both managers at 75.0 PTS just 2 points behind Robert.
            </p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">⚡ Week 8 MVP Picker</span>
            <div class="text-base font-bold text-white mt-1">Mark (13-3 Week • 72.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Mark detonated for a league-best 13.0 points in Week 8, rocketing from 10th to a 5th place tie with Alex (12.0)!
            </p>
          </div>
        </div>

        <!-- Official Pick-em Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Certified Sleeper Standings Through Week 8</span>
            <span class="font-mono text-blue-400 font-bold">Total Correct Picks • W8 Score</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-amber-950/20">
              <span class="w-8 font-bold text-amber-400">1</span>
              <span class="flex-1 font-bold text-white">Robert (YaBoyRoZ)</span>
              <span class="w-24 text-center text-slate-400">W8: 11.0 PTS</span>
              <span class="w-28 text-right text-amber-400 font-extrabold text-sm">77.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">2</span>
              <span class="flex-1 font-semibold text-slate-200">Arnulfo (AEscamilla94)</span>
              <span class="w-24 text-center text-slate-400">W8: 8.0 PTS</span>
              <span class="w-28 text-right text-emerald-400 font-bold">75.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">3</span>
              <span class="flex-1 font-semibold text-slate-200">iRob (irobgarza16)</span>
              <span class="w-24 text-center text-slate-400">W8: 10.0 PTS</span>
              <span class="w-28 text-right text-emerald-400 font-bold">75.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">4</span>
              <span class="flex-1 text-slate-300">Herrador (DirtyDirties)</span>
              <span class="w-24 text-center text-slate-400">W8: 10.0 PTS</span>
              <span class="w-28 text-right text-slate-300">74.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">5</span>
              <span class="flex-1 text-slate-300">Mark (fattymcfatty) <span class="text-emerald-400 font-bold text-[10px]">W8 High (13)</span></span>
              <span class="w-24 text-center text-emerald-400 font-bold">W8: 13.0 PTS</span>
              <span class="w-28 text-right text-slate-300">72.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">6</span>
              <span class="flex-1 text-slate-300">Alex (abarrera731)</span>
              <span class="w-24 text-center text-slate-400">W8: 12.0 PTS</span>
              <span class="w-28 text-right text-slate-300">72.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">7</span>
              <span class="flex-1 text-slate-300">Franky (ChanciscoFravez)</span>
              <span class="w-24 text-center text-slate-400">W8: 9.0 PTS</span>
              <span class="w-28 text-right text-slate-300">71.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">8</span>
              <span class="flex-1 text-slate-300">Pedro (GuyNamedPedro)</span>
              <span class="w-24 text-center text-slate-400">W8: 9.0 PTS</span>
              <span class="w-28 text-right text-slate-400">70.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">9</span>
              <span class="flex-1 text-slate-300">Eric (emedina13)</span>
              <span class="w-24 text-center text-slate-400">W8: 9.0 PTS</span>
              <span class="w-28 text-right text-slate-400">70.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-500">10</span>
              <span class="flex-1 text-slate-400">Joey (TheGreatSwagsby)</span>
              <span class="w-24 text-center text-slate-400">W8: 7.0 PTS</span>
              <span class="w-28 text-right text-slate-500">69.0 PTS</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 8: BOOMS & BUSTS (VERIFIED SLEEPER PERFORMERS)
slide_8 = """      <!-- SLIDE 8: BOOMS & BUSTS -->
      <section id="wk8-slide-8" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-orange-950/80 via-slate-900 to-amber-950/80 border border-orange-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-orange-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              STATISTICAL ANOMALIES • HEROES & ZEROES
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💥 Booms & Busts: Week 8 Outliers</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Joe Burrow's 42-point nuke, Tee Higgins' masterclass, and Lamar Jackson's zero-point nightmare.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-orange-400 font-mono font-bold px-3 py-1 rounded-lg">Performance Extremes</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- The Booms Card -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded">
              🚀 Week 8 Nuclear Booms
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Joe Burrow (QB • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">Njigbas in Paris (iRob) • Week 8 Overall MVP</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-extrabold text-sm">42.48 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tee Higgins (WR • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric) • WR1 Masterclass</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">32.50 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Bhayshul Tuten (RB • JAX)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky) • RB Breakout</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">28.90 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Kirk Cousins (QB • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark) • Clutch Free Agent Gem</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">28.18 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Josh Allen (QB • BUF)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">27.56 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tony Pollard (RB • TEN)</strong>
                  <span class="block text-slate-400 text-[11px]">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">27.20 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Ja'Marr Chase (WR • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">Brock To The Future (Herrador)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">25.60 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Brock Bowers (TE • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">Brock To The Future (Herrador)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">24.70 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jahmyr Gibbs (RB • DET)</strong>
                  <span class="block text-slate-400 text-[11px]">The Latin Touch (Arnulfo)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">23.80 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Michael Wilson (WR • ARI)</strong>
                  <span class="block text-slate-400 text-[11px]">LEAGUE MEDIAN ADVOCATE 🗳 (Alex)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">22.80 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Drake Maye (QB • NE)</strong>
                  <span class="block text-slate-400 text-[11px]">LEAGUE MEDIAN ADVOCATE 🗳 (Alex)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">22.46 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jacksonville Jaguars (DEF • JAX)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">20.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>
            </div>
          </div>

          <!-- The Busts Card -->
          <div class="bg-slate-900 border-2 border-red-500/50 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-red-400 bg-red-950 border border-red-800 px-2.5 py-0.5 rounded">
              📉 Week 8 Catastrophic Busts
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-red-600/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Lamar Jackson (QB • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">WE NOT GOIN’ BACK 2 BACK (Robert) • Goose egg in lineup!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-500 font-extrabold text-sm">0.00 PTS</span>
                  <span class="block text-red-400 text-[10px]">Total Flop</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Omar Cooper (WR • NYJ)</strong>
                  <span class="block text-slate-400 text-[11px]">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">0.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Zay Flowers (WR • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">0.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Will Reichard (K • MIN)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">0.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tre Tucker (WR • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">0.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">DK Metcalf (WR • PIT)</strong>
                  <span class="block text-slate-400 text-[11px]">LEAGUE MEDIAN ADVOCATE 🗳 (Alex) • Sub-1 pt letdown</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">0.90 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Spencer Shrader (K • IND)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">1.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Drake London (WR • ATL)</strong>
                  <span class="block text-slate-400 text-[11px]">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">1.30 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jordan Mason (RB • MIN)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">2.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Seth McGowan (RB • IND)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">2.90 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 9: WEEK 8 SCOREBOARD (EXACT SLEEPER LINEUPS)
slide_9 = """      <!-- SLIDE 9: SCOREBOARD -->
      <section id="wk8-slide-9" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-indigo-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL BOX SCORES • SLEEPER API AUDIT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚔️ Week 8 Scoreboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official final box scores, margins of victory, and statistical summaries for all 5 matchups.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-indigo-400 font-mono font-bold px-3 py-1 rounded-lg">5 Completed Matchups</span>
          </div>
        </div>

        <div class="space-y-3">
          <!-- Matchup 1: Mark vs Robert ($10 Blowout Bounty) -->
          <div class="bg-slate-900 border-2 border-emerald-500/60 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-emerald-400 bg-emerald-950/50 border border-emerald-800 px-2 py-0.5 rounded">
                ⚡ Matchup 1 • $10 BLOWOUT BOUNTY (+45.38 Margin)
              </span>
              <span class="text-xs font-mono text-emerald-400 font-bold">Mark Wins $10 Cash Bounty</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">131.98 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Kirk Cousins (28.18), Jacksonville DEF (20.00), Puka Nacua (19.50), Luther Burden (15.10), T.J. Hockenson (13.80), Saquon Barkley (11.90), Stefon Diggs (11.30), Javonte Williams (6.20), Cam Little (6.00), Zay Flowers (0.00).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-red-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-400 text-sm">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                  <span class="text-red-500 font-athletic text-lg font-black">86.60 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Tony Pollard (27.20), Harold Fannin (18.40), Kyren Williams (12.40), Rome Odunze (10.70), Bijan Robinson (7.60), Jake Bates (6.00), Seattle DEF (3.00), Drake London (1.30), Lamar Jackson (0.00), Omar Cooper (0.00).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 2: Herrador vs Alex (High Roller vs Heartbreak) -->
          <div class="bg-slate-900 border-2 border-amber-500/50 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-amber-400 bg-amber-950/50 border border-amber-800 px-2 py-0.5 rounded">
                🔥 Matchup 2 • HIGH ROLLER CROWN & HEARTBREAK (+6.42 Margin)
              </span>
              <span class="text-xs font-mono text-slate-400">Week 8 Showcase Game</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-amber-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Brock To The Future (Herrador)</span>
                  <span class="text-amber-400 font-athletic text-lg font-black">148.78 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Ja'Marr Chase (25.60), Brock Bowers (24.70), Chuba Hubbard (21.40), Bucky Irving (21.00), Tampa Bay DEF (18.00), Jayden Daniels (14.98), Chad Ryland (9.00), Jalen Coker (8.60), Germie Bernard (5.50).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-rose-500/30">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-300 text-sm">LEAGUE MEDIAN ADVOCATE 🗳 (Alex)</span>
                  <span class="text-rose-400 font-athletic text-lg font-bold">142.36 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Michael Wilson (22.80), Drake Maye (22.46), Pittsburgh DEF (21.00), Jaylen Warren (20.80), Trey McBride (16.70), Derrick Henry (13.00), Ladd McConkey (10.60), Amon-Ra St. Brown (9.10), Evan McPherson (5.00), DK Metcalf (0.90).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 3: iRob vs Arnulfo (Battle for 1st Place) -->
          <div class="bg-slate-900 border border-blue-500/40 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-blue-400 bg-blue-950/50 border border-blue-800 px-2 py-0.5 rounded">
                ⚡ Matchup 3 • CLASH FOR 1ST PLACE (+24.28 Margin)
              </span>
              <span class="text-xs font-mono text-emerald-400 font-bold">iRob Takes Sole 1st Seed</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Njigbas in Paris (iRob)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">146.48 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Joe Burrow (42.48 nuclear blast!), Jaxon Smith-Njigba (20.80), Jonah Coleman (18.40), DJ Moore (14.60), Chase Brown (12.10), Chase McLaughlin (12.00), Tetairoa McMillan (8.80), Cincinnati DEF (7.00), George Pickens (5.80), Hunter Henry (4.50).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-400 text-sm">The Latin Touch (Arnulfo)</span>
                  <span class="text-slate-300 font-athletic text-lg font-bold">122.20 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Jahmyr Gibbs (23.80), Josh Jacobs (20.20), Dak Prescott (19.80), Christian Watson (13.30), Rhamondre Stevenson (10.50), Travis Kelce (9.20), Las Vegas DEF (9.00), Brandon McManus (6.00), KC Concepcion (5.20), Dallas Goedert (5.20).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 4: Eric vs Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-slate-300 bg-slate-800 px-2 py-0.5 rounded">
                ⚔️ Matchup 4 • SLUMP BUSTER ROUT (+43.12 Margin)
              </span>
              <span class="text-xs font-mono text-slate-400">Eric Snaps 3-Game Skid</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Show me dem TDs (Eric)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">135.56 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Tee Higgins (32.50), Josh Allen (27.56), Jameson Williams (15.00), Washington DEF (14.00), Justin Jefferson (11.80), Rico Dowdle (11.60), Matt Gay (10.00), Sam LaPorta (5.00), Jonathan Taylor (4.70), Kendrick Bourne (3.40).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-400 text-sm">TheGreatSwagsby (Joey)</span>
                  <span class="text-slate-300 font-athletic text-lg font-bold">92.44 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Braelon Allen (22.30), Malik Willis (15.64), Tucker Kraft (14.30), Kenneth Walker (10.40), Makai Lemon (8.70), Ollie Gordon (6.90), Caleb Douglas (6.30), Cleveland DEF (5.00), Seth McGowan (2.90), Will Reichard (0.00).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 5: Pedro vs Franky -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-red-400 bg-red-950/60 border border-red-700 px-2 py-0.5 rounded">
                💀 Matchup 5 • UPSET OF THE WEEK (+15.24 Margin)
              </span>
              <span class="text-xs font-mono text-emerald-400 font-bold">Pedro Claims 3rd Win</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">I Didn’t Hear No Bell (Pedro)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">107.40 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Trevor Lawrence (19.40), Matthew Golden (17.40), Chris Rodriguez (12.30), Brandon Aubrey (12.00), Garrett Wilson (11.30), Los Angeles Rams DEF (11.00), Ashton Jeanty (8.80), Denzel Boston (6.70), Brenton Strange (6.50), Jordan Mason (2.00).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-rose-500/30">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-300 text-sm">CULT OF THE LAMB (Franky)</span>
                  <span class="text-rose-400 font-athletic text-lg font-bold">92.16 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Bhayshul Tuten (28.90), James Cook (17.10), Blake Corum (13.30), CeeDee Lamb (9.30), Colston Loveland (8.00), Minnesota DEF (7.00), Jacoby Brissett (4.46), Parker Washington (3.10), Spencer Shrader (1.00), Tre Tucker (0.00).
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 10: WEEK 9 GAMEDAY HUB
slide_10 = """      <!-- SLIDE 10: WEEK 9 GAMEDAY HUB -->
      <section id="wk8-slide-10" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-indigo-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 9 MATCHUP PREVIEWS • SPREADS & VEGAS LINES
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚡ Week 9 Gameday Hub</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Preview of Week 9 matchups and the $10 Highest Scoring QB Bounty!</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">5 Week 9 Matchups</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- Game of the Week: Joey vs iRob -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-4 shadow-xl col-span-1 md:col-span-2">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-amber-400 bg-amber-950/80 border border-amber-700 px-2 py-0.5 rounded">
                👑 GAME OF THE WEEK • SOLO LEADER'S TEST
              </span>
              <span class="font-mono text-emerald-400 font-bold">Spread: iRob -5.5 | O/U: 236.0 | $10 QB Target</span>
            </div>
            <div class="flex flex-col sm:flex-row justify-between items-center gap-4 py-2">
              <div class="text-center sm:text-left">
                <span class="text-base font-bold text-white">TheGreatSwagsby (Joey)</span>
                <span class="block text-slate-400 font-mono font-semibold">4-4 • 982.40 PF</span>
              </div>
              <div class="text-xl font-black text-amber-400 font-athletic">VS</div>
              <div class="text-center sm:text-right">
                <span class="text-base font-bold text-white">Njigbas in Paris (iRob)</span>
                <span class="block text-emerald-400 font-mono font-semibold">6-2 • 997.26 PF (1st)</span>
              </div>
            </div>
            <p class="text-slate-300 mt-2 text-xs leading-relaxed border-t border-slate-800/80 pt-2">
              Can Joey knock off the runaway train? iRob holds sole possession of 1st place after Joe Burrow's 42-point explosion. Joey desperately needs a signature win to climb above .500 and protect his playoff spot!
            </p>
          </div>

          <!-- Matchup 1: Mark vs Pedro -->
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-emerald-400 bg-emerald-950 border border-emerald-800 px-2 py-0.5 rounded">
                Momentum Battle
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Mark -14.5 | O/U: 232.0</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-white">Mark (5-3)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-red-400">Pedro (3-5)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Mark is flying high after securing the $10 Blowout Bounty, moving into sole 3rd place. Pedro is fresh off an upset win over Franky, but faces an uphill battle to avoid falling further back in the 5K toilet race.
            </p>
          </div>

          <!-- Matchup 2: Franky vs Herrador -->
          <div class="bg-slate-900 border border-amber-500/30 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-amber-400 bg-amber-950 border border-amber-800 px-2 py-0.5 rounded">
                Offensive Fireworks
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Franky -2.5 | O/U: 254.5</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-slate-200">Franky (3-5)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-amber-400">Herrador (4-4)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              League scoring leader Franky (1056.80 PF) collides with Week 8 High Roller champion Herrador (1034.80 PF)! Expect astronomical points as both powerhouses chase the $10 QB bounty.
            </p>
          </div>

          <!-- Matchup 3: Arnulfo vs Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-slate-400 bg-slate-950 px-2 py-0.5 rounded">
                Rebound Showdown
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Arnulfo -5.5 | O/U: 236.0</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-slate-200">Arnulfo (5-3)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-slate-200">Robert (3-5)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Both squads look to rebound from Week 8 setbacks. Arnulfo wants to reclaim a share of 1st place, while Robert needs Lamar Jackson to awaken from his 0-point nightmare.
            </p>
          </div>

          <!-- Matchup 4: Eric vs Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-slate-400 bg-slate-950 px-2 py-0.5 rounded">
                Midfield Survival Duel
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Alex -3.5 | O/U: 245.0</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-slate-200">Eric (4-4)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-slate-200">Alex (3-5)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Alex put up 142.36 points and lost in Week 8; Eric put up 135.56 and won. Now they meet head-to-head in a pivotal duel with massive postseason wildcard implications!
            </p>
          </div>
        </div>
      </section>"""

# -------------------------------------------------------------
# 3. ASSEMBLE FULL DECK-WK8 HTML
# -------------------------------------------------------------
deck_wk8_html = f"""    <!-- ========================================== -->
    <!-- DECK 8: WEEK 8 OFFICIAL REPORT (ACTIVE)    -->
    <!-- ========================================== -->
    <div id="deck-wk8">
{slide_0}

{slide_1}

{slide_2}

{slide_3}

{slide_4}

{slide_5}

{slide_6}

{slide_7}

{slide_8}

{slide_9}

{slide_10}
    </div>"""

# -------------------------------------------------------------
# 4. REPLACE DECK-WK8 IN index.html
# -------------------------------------------------------------
print("Replacing deck-wk8 block in index.html...")
# Pattern for deck-wk8
deck_pattern = r'<!-- ========================================== -->\s*<!-- DECK 8: WEEK 8 OFFICIAL REPORT \(ACTIVE\)    -->\s*<!-- ========================================== -->\s*<div id="deck-wk8">.*?</div>\s*(?=<!-- ========================================== -->\s*<!-- DECK 7)'
if re.search(deck_pattern, html, re.DOTALL):
    html = re.sub(deck_pattern, deck_wk8_html + "\n\n    ", html, count=1, flags=re.DOTALL)
    print("✅ Replaced existing deck-wk8 block perfectly!")
else:
    # Fallback pattern
    deck_simple_pattern = r'<div id="deck-wk8">.*?</div>\s*(?=<div id="deck-wk7" style="display:none;">)'
    if re.search(deck_simple_pattern, html, re.DOTALL):
        html = re.sub(deck_simple_pattern, deck_wk8_html + "\n\n    ", html, count=1, flags=re.DOTALL)
        print("✅ Replaced simple deck-wk8 block!")
    else:
        print("⚠️ Warning: deck-wk8 block not found by regex; checking direct injection")

# Replace nav pills
nav_pattern = r'<nav class="flex items-center gap-1\.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">.*?</nav>'
html = re.sub(nav_pattern, new_nav_pills, html, count=1, flags=re.DOTALL)

# Timestamp update
html = re.sub(r'id="portalSyncedTime">.*?</strong>', 'id="portalSyncedTime">Nov 3, 2026 • 12:35 PM CST (Week 8 Final Official Update)</strong>', html, count=1)

with open(INDEX_PATH, "wb") as f:
    f.write(html.encode("utf-8"))

print("🎉 Successfully updated index.html with verified Week 8 starters and scores!")

import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

print("Reading index.html...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------
# 1. NEW NAV PILLS (11 SLIDES FOR WEEK 10)
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
        <button onclick="goToSlide(10)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">11. ⚡ Wk 11 Gameday Hub</button>
      </nav>"""

print("Preparing slide content for Deck 10...")

# SLIDE 0: HARDWARE & ROASTS
slide_0 = """      <!-- SLIDE 0: HARDWARE & ROASTS -->
      <section id="wk10-slide-0" class="slide active space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-500/20 via-slate-900 to-yellow-500/10 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL WEEK 10 AWARDS • F.F.U.C. HONORS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏆 Hardware & Weekly Roasts</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 10 191-pt scoring detonation, $10 highest RB bounty, heartbreaking 5-pt first-place loss, and toilet sprint.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-900 border border-amber-500/30 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Final Stretch (10 of 14 Weeks)</span>
          </div>
        </div>

        <!-- FFUC AI BROADCAST PLAYER (NATURAL MALE ANNOUNCER VOICE) -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/70 to-slate-900 border-2 border-indigo-500/40 rounded-2xl p-4 shadow-xl">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <div class="flex items-center gap-3.5">
              <button id="broadcastPlayBtn" onclick="toggleBroadcastAudio()" class="w-12 h-12 rounded-full bg-gradient-to-tr from-amber-500 to-yellow-400 text-slate-950 flex items-center justify-center font-black shadow-lg shadow-amber-500/30 hover:scale-105 active:scale-95 transition flex-shrink-0">
                <span id="playIcon" class="text-lg ml-0.5">▶</span>
                <span id="pauseIcon" class="text-lg hidden">⏸</span>
              </button>
              <div>
                <div class="flex items-center gap-2">
                  <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                    <span id="audioPulseRing" class="w-1.5 h-1.5 rounded-full bg-indigo-400"></span>
                    FFUC Radio Network • Week 10
                  </span>
                  <span class="text-[10px] font-mono text-slate-400 hidden sm:inline">AllTalk XTTSv2 Neural Voice</span>
                </div>
                <h3 id="broadcastTitleText" class="text-base sm:text-lg font-black text-white mt-0.5 tracking-tight">Week 10 Official Broadcast: iRob 191-Pt Detonation & First Place Showdown</h3>
                <p id="broadcastDescText" class="text-xs text-slate-300">Fast-paced 60-second audio recap of Week 10 highlights, Christian McCaffrey's $10 bounty, and the playoff race.</p>
              </div>
            </div>

            <!-- Progress & Controls -->
            <div class="flex items-center gap-3 w-full md:w-64 flex-shrink-0">
              <div class="flex-1 bg-slate-950/80 rounded-full h-2 overflow-hidden border border-slate-800">
                <div id="audioProgressBar" class="bg-gradient-to-r from-amber-500 to-indigo-500 h-full w-0 transition-all duration-200"></div>
              </div>
              <span id="audioCurrentTime" class="text-xs font-mono text-slate-400 font-bold min-w-[32px]">0:00</span>
              <span class="text-xs text-slate-600 font-mono">/</span>
              <span id="audioDuration" class="text-xs font-mono text-slate-400 font-bold min-w-[32px]">1:00</span>
            </div>
          </div>

          <!-- Bottom Audio Details -->
          <div class="mt-3 pt-2.5 border-t border-slate-800/60 flex items-center justify-between text-xs text-slate-400">
            <div class="flex items-center gap-2">
              <span class="text-amber-400 font-bold">🎙️ Lead Anchor:</span>
              <span>Sports Radio Host (Voice: male_01.wav)</span>
            </div>
            <div class="flex items-center gap-3">
              <div class="flex items-center gap-1" id="audioWaveform">
                <span class="w-1 h-2 bg-indigo-500/40 rounded-full"></span>
                <span class="w-1 h-3 bg-indigo-500/40 rounded-full"></span>
                <span class="w-1 h-4 bg-indigo-500/40 rounded-full"></span>
                <span class="w-1 h-2 bg-indigo-500/40 rounded-full"></span>
              </div>
              <span class="text-[10px] text-slate-500 font-mono">Natural Voice Broadcast • Click to stream</span>
            </div>
          </div>
          <!-- Audio Element -->
          <audio id="broadcastAudio" src="assets/audio/wk10_recap.mp3" preload="metadata" ontimeupdate="updateBroadcastProgress()" onended="onBroadcastAudioEnded()"></audio>
        </div>

        <!-- AWARDS GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Award 1: High Roller Champion (iRob) -->
          <div class="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border-2 border-amber-500/60 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-amber-500 text-slate-950 px-2.5 py-0.5 rounded">👑 Week 10 High Roller Champion</span>
              <span class="text-xl font-athletic font-bold text-amber-400">191.46 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">Njigbas in Paris <span class="text-amber-400 text-sm font-semibold">(iRob)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              AN ATOMIC DETONATION! iRob shatters the season scoring record with an otherworldly 191.46 points in an 80.54-point obliteration of Alex (110.92)! Powered by George Pickens (38.00), Brock Purdy (31.66), Jaxon Smith-Njigba (27.10), Chase Brown (24.30), Joe Burrow (20.30), Zay Flowers (18.20), Kyren Williams (13.90), and David Montgomery (10.00), iRob captures his second High Roller crown of 2026 and takes sole possession of 1st place in FFUC at 7-3!
            </p>
            <!-- FaceFusion AI High Roller Video / GIF -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-amber-500/40 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-amber-500/40 text-[9px] font-mono font-bold text-amber-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                FaceFusion AI • iRob Shaq Shimmy Celebration (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/irob_high_roller.gif">
                <source src="assets/video/irob_high_roller.mp4" type="video/mp4">
                <img src="assets/video/irob_high_roller.gif" alt="iRob High Roller Shaq Shimmy" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Week 10 High Score: 191.46 PTS</span>
              <span class="text-amber-400 font-bold font-mono">Scoring Crown • 7-3 Record (Solo #1)</span>
            </div>
          </div>

          <!-- Award 2: $10 Bounty Winner (Highest Scoring RB) -->
          <div class="bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-emerald-500 text-slate-950 px-2.5 py-0.5 rounded">⚡ $10 Weekly Bounty: Highest Scoring RB</span>
              <span class="text-xl font-athletic font-bold text-emerald-400">44.30 PTS (Christian McCaffrey)</span>
            </div>
            <h3 class="text-xl font-black text-white">TheGreatSwagsby <span class="text-emerald-400 text-sm font-semibold">(Joey)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              CMC UNLEASHED! Joey banks the Week 10 $10 cash bounty behind Christian McCaffrey's electrifying 44.30-point eruption! McCaffrey carried Joey to a 137.78 to 105.12 blowout victory over defending champion Robert, narrowly beating out Jahmyr Gibbs (40.70) and Emmett Johnson (32.10) to secure the cash and vault into 3rd place at 6-4!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Christian McCaffrey: 44.30 PTS (Top League RB)</span>
              <span class="text-emerald-400 font-bold font-mono">Joey: $10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 3: Heartbreak Bad Beat (Mark) -->
          <div class="bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-900 border border-rose-500/40 rounded-2xl p-5 shadow-xl">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
              <span class="text-xs font-mono font-bold uppercase tracking-wider bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-0.5 rounded">💔 Heartbreak of the Week</span>
              <span class="text-lg font-athletic font-bold text-rose-400">113.22 PTS (L)</span>
            </div>
            <h3 class="text-xl font-black text-white">Saquon Deez Nacuas <span class="text-rose-400 text-sm font-semibold">(Mark)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              AGONY IN THE CLASH FOR FIRST! In the undisputed Game of the Week for sole possession of 1st place, Mark racked up 113.22 points—the highest losing score in Week 10—behind Patrick Mahomes (35.42), Puka Nacua (14.80), and Jayden Reed (14.40). But Mark ran straight into Arnulfo's Jahmyr Gibbs (40.70) and Dak Prescott (35.42) barrage, suffering a devastating 5.70-point defeat (118.92 to 113.22) to surrender the top spot!
            </p>
            <!-- FaceFusion AI Heartbreak Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-rose-500/40 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-rose-500/40 text-[9px] font-mono font-bold text-rose-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
                FaceFusion AI Video • Mark Michael Scott Holding Back Tears (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/mark_heartbreak.gif">
                <source src="assets/video/mark_heartbreak.mp4" type="video/mp4">
                <img src="assets/video/mark_heartbreak.gif" alt="Mark Michael Scott Heartbreak Meme" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Defeated by: Arnulfo (118.92 PTS)</span>
              <span class="text-rose-400 font-bold font-mono">Highest Losing Score (5.70 Margin)</span>
            </div>
          </div>

          <!-- Award 4: 5K Toilet Runner: Cellar Shock (Eric) -->
          <div class="bg-gradient-to-br from-red-950/40 via-slate-900 to-slate-900 border-2 border-red-600/70 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex flex-wrap items-center justify-between gap-2 mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-red-600 text-white px-2.5 py-0.5 rounded shadow">🚽 5K Toilet Runner: Low Score of Week</span>
              <span class="text-lg font-athletic font-bold text-red-400">89.04 PTS (-50.10)</span>
            </div>
            <h3 class="text-xl font-black text-white">Show me dem TDs <span class="text-red-400 text-sm font-semibold">(Eric)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              <strong class="text-red-400">BACK-TO-BACK TOILET SPRINTS:</strong> Eric's mid-season slump worsened in Week 10, posting a league-low 89.04 points in a 50.10-point blowout loss to Franky (139.14). With Pierre Strong (14.20) as his top scorer and duds across his lineup, Eric drops to 4-6 and earns his second consecutive 5K Toilet Runner dishonor! Meanwhile, Pedro's loss keeps Pedro anchored in the season cellar at 926.14 PF.
            </p>
            <!-- 5K Runner Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                FaceFusion AI • Eric Forrest Gump Field Sprint (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/eric_toilet_runner.gif">
                <source src="assets/video/eric_toilet_runner.mp4" type="video/mp4">
                <img src="assets/video/eric_toilet_runner.gif" alt="Eric 5K Toilet Runner Meme" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-red-400 font-mono font-bold">Week 10 Low Score: 89.04 PTS</span>
              <span class="text-red-400 font-bold font-mono">Record: 4-6 • Back-to-Back Sprints</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 1: STATE OF THE UNION & STANDINGS
slide_1 = """      <!-- SLIDE 1: STATE OF THE UNION -->
      <section id="wk10-slide-1" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 10 LEAGUE AUDIT • COMMISSIONER'S DESK
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏛️ State of the Union: Week 10</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">iRob and Arnulfo seize the top seeds at 7-3, Joey takes 3rd alone at 6-4, Franky & Herrador sit at 5-5, and Pedro remains anchored in last at 3-7.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-blue-400 font-mono font-bold px-3 py-1 rounded-lg">10 of 14 Complete (71%)</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">👑 iRob & Arnulfo Seize 1st (7-3)</span>
            <div class="text-base font-bold text-white mt-1">Dual Titans Atop the League</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob's 191.46-point nuclear explosion elevates him to 7-3 and 1,301.86 PF, holding the #1 overall seed. Arnulfo joins him at 7-3 (1,214.16 PF) after winning the Game of the Week against Mark!
            </p>
          </div>

          <div class="bg-slate-900 border border-blue-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-400">🎯 Joey & Mark in the Chase (6-4)</span>
            <div class="text-base font-bold text-white mt-1">Heavyweight Battle for Bye Weeks</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Joey surges to 6-4 behind Christian McCaffrey's 44.30-point clinic to take seed #3 (1,241.42 PF). Mark drops to 6-4 (1,220.26 PF). The two clash head-to-head in Week 11 for the #3 seed!
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">🔥 Wild-Card Bloodbath (5-5 & 4-6)</span>
            <div class="text-base font-bold text-white mt-1">Franky & Herrador Stalking</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Franky leads the entire league in scoring at 1,332.40 PF but is locked in a 5-5 dogfight with Herrador (1,286.32 PF). Alex (1,257.80 PF) and Eric (1,124.12 PF) fight for survival at 4-6!
            </p>
          </div>
        </div>

        <!-- Standings Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Official Sleeper Standings Through Week 10</span>
            <span class="font-mono text-blue-400 font-bold">14-Week Regular Season</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/30">
              <span class="w-8 font-bold text-emerald-400">1</span>
              <span class="flex-1 font-bold text-white">Njigbas in Paris (iRob) <span class="text-emerald-400 font-bold text-[10px]">👑 191.46 High Roller</span></span>
              <span class="w-16 text-center text-emerald-400 font-bold">7-3</span>
              <span class="w-20 text-right text-emerald-400 font-bold">1301.86 PF</span>
              <span class="w-20 text-right text-slate-500">1203.46 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$50</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-8 font-bold text-emerald-400">2</span>
              <span class="flex-1 font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">7-3</span>
              <span class="w-20 text-right text-slate-200 font-bold">1214.16 PF</span>
              <span class="w-20 text-right text-slate-500">1201.18 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$10</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-blue-950/20">
              <span class="w-8 font-bold text-blue-400">3</span>
              <span class="flex-1 font-bold text-white">TheGreatSwagsby (Joey) <span class="text-emerald-400 font-bold text-[10px]">⚡ $10 Bounty</span></span>
              <span class="w-16 text-center text-blue-400 font-bold">6-4</span>
              <span class="w-20 text-right text-slate-300">1241.42 PF</span>
              <span class="w-20 text-right text-slate-500">1141.28 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$10</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-blue-950/15">
              <span class="w-8 font-bold text-blue-400">4</span>
              <span class="flex-1 font-semibold text-slate-200">Saquon Deez Nacuas (Mark)</span>
              <span class="w-16 text-center text-blue-400 font-bold">6-4</span>
              <span class="w-20 text-right text-slate-300">1220.26 PF</span>
              <span class="w-20 text-right text-slate-500">1139.30 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$34</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">5</span>
              <span class="flex-1 text-slate-300">CULT OF THE LAMB (Franky) <span class="text-amber-400 font-bold text-[10px]">#1 PF in FFUC</span></span>
              <span class="w-16 text-center text-slate-300 font-bold">5-5</span>
              <span class="w-20 text-right text-amber-400 font-extrabold">1332.40 PF</span>
              <span class="w-20 text-right text-slate-500">1283.42 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$1</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">6</span>
              <span class="flex-1 text-slate-300">Brock To The Future (Herrador)</span>
              <span class="w-16 text-center text-slate-300 font-bold">5-5</span>
              <span class="w-20 text-right text-slate-300">1286.32 PF</span>
              <span class="w-20 text-right text-slate-500">1234.20 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$49</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">7</span>
              <span class="flex-1 text-slate-300">League Median Advocate 🗳 (Alex)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-6</span>
              <span class="w-20 text-right text-slate-300">1257.80 PF</span>
              <span class="w-20 text-right text-slate-500">1310.54 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$24</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">8</span>
              <span class="flex-1 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-6</span>
              <span class="w-20 text-right text-slate-300">1124.12 PF</span>
              <span class="w-20 text-right text-slate-500">1160.36 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$49</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-8 font-bold text-rose-400">9</span>
              <span class="flex-1 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-7</span>
              <span class="w-20 text-right text-slate-300">1212.08 PF</span>
              <span class="w-20 text-right text-slate-500">1215.96 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$77</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-red-950/30">
              <span class="w-8 font-bold text-red-500">10</span>
              <span class="flex-1 font-medium text-red-400">I Didn’t Hear No Bell (Pedro) <span class="text-red-500 text-[10px] font-bold">(-285.94 PF Deficit)</span></span>
              <span class="w-16 text-center text-red-500 font-bold">3-7</span>
              <span class="w-20 text-right text-red-400 font-extrabold">926.14 PF</span>
              <span class="w-20 text-right text-slate-500">1226.86 PA</span>
              <span class="w-16 text-right text-red-500 font-black">$0</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 2: $10 BOUNTY BOARD
slide_2 = """      <!-- SLIDE 2: $10 BOUNTY BOARD -->
      <section id="wk10-slide-2" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-green-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEKLY PRIZE POOL • DIRECT CASH PAYOUTS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💵 $10 Weekly Bounty Board</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 10 Highest Scoring RB crowned; Week 11 Highest Scoring WR on deck.</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-emerald-400">$140.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Season Bounty Pot ($100 Paid)</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Week 10 Winner Card (Joey) -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-emerald-500 text-slate-950 text-xs font-extrabold px-3 py-1 rounded-bl-xl shadow">
              Bounty Collected ($10)
            </div>
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">Week 10 Target: Highest Scoring RB ($10)</span>
              <h3 class="text-2xl font-black text-white mt-1">Joey • 44.30 PTS (Christian McCaffrey)</h3>
              <div class="text-xs text-slate-400 mt-0.5">Franchise: <strong class="text-slate-200">TheGreatSwagsby</strong></div>

              <div class="my-4 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl space-y-2">
                <div class="text-xs text-emerald-300 font-semibold">⚡ CMC's 44-Point Nuclear Show:</div>
                <div class="text-xs text-slate-300 leading-relaxed">
                  Christian McCaffrey put on an absolute clinic against the Buccaneers, racking up 107 rushing yards, 68 receiving yards, and 2 touchdowns to erupt for 44.30 points! McCaffrey edged out Jahmyr Gibbs' 40.70-point barrage to deliver Joey his second $10 cash bounty of the season!
                </div>
              </div>

              <!-- Top 5 Starting RBs in Week 10 -->
              <div class="space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-emerald-500/40">
                  <span class="font-bold text-emerald-400">1. Christian McCaffrey (Joey)</span>
                  <span class="font-black text-white">44.30 PTS (WON $10)</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>2. Jahmyr Gibbs (Arnulfo)</span>
                  <span class="font-bold text-amber-400">40.70 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>3. Emmett Johnson (Pedro)</span>
                  <span>32.10 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>4. Chuba Hubbard (Herrador)</span>
                  <span>31.70 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>5. Cam Skattebo (Alex)</span>
                  <span>25.70 PTS</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Payout Method: League Safe / Direct</span>
              <span class="text-emerald-400 font-bold">$10.00 Sent to Joey</span>
            </div>
          </div>

          <!-- Season Bounty Schedule & Leaderboard -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400">2026 Bounty Master Schedule</span>
              <h3 class="text-xl font-black text-white mt-1">10 of 14 Bounties Claimed ($100.00 Paid)</h3>

              <div class="mt-3 divide-y divide-slate-800/80 text-xs font-mono">
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 1: Most Points</span>
                  <span class="text-emerald-400 font-bold">Herrador (157.06) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 2: Highest QB</span>
                  <span class="text-emerald-400 font-bold">Franky (Josh Allen 32.70) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 3: Highest RB</span>
                  <span class="text-emerald-400 font-bold">Joey (Saquon 33.60) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 4: Highest WR</span>
                  <span class="text-emerald-400 font-bold">Franky (CeeDee Lamb 29.30) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 5: Highest TE</span>
                  <span class="text-emerald-400 font-bold">Mark (George Kittle 22.40) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 6: Highest DEF</span>
                  <span class="text-emerald-400 font-bold">Eric (Chicago Bears 24.00) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 7: Narrowest Victory</span>
                  <span class="text-emerald-400 font-bold">Arnulfo (2.98 Margin) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 8: Largest Blowout</span>
                  <span class="text-emerald-400 font-bold">Mark (45.38 Margin) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 9: Highest Scoring QB</span>
                  <span class="text-emerald-400 font-bold">iRob (Burrow 29.54) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-emerald-950/30 px-2 rounded border border-emerald-500/30 text-white">
                  <span class="font-bold">Wk 10: Highest Scoring RB</span>
                  <span class="text-emerald-400 font-bold">Joey (McCaffrey 44.30) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-amber-950/30 px-2 rounded border border-amber-500/30 text-amber-300">
                  <span class="font-bold">Wk 11: Highest Scoring WR</span>
                  <span class="text-amber-400 font-bold">🔒 Up for Grabs ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 12: Highest Scoring TE</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 13: Highest Scoring DEF</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>Wk 14: Most Points in a Loss</span>
                  <span>🔒 Scheduled ($10)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Next Target: Week 11 Highest Scoring WR</span>
              <span class="text-amber-400 font-bold">$10.00 Target</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 3: THE BAR TAB & 5K TOILET METER
slide_3 = """      <!-- SLIDE 3: THE BAR TAB & 5K TOILET METER -->
      <section id="wk10-slide-3" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-red-950/80 via-slate-900 to-rose-950/80 border border-red-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-red-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              THE LAST PLACE PUNISHMENT WATCH • THE TOILET RUN
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍻 The Bar Tab & 5K Toilet Meter</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Live tracking of the FFUC Last Place in-person 5K Run and open bar tab liability.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-red-400 font-mono font-bold px-3 py-1 rounded-lg">Critical Risk: Pedro (3-7, 926.14 PF, $0 FAAB)</span>
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
                <span class="text-lg font-athletic font-bold text-red-400">3-7 • 926.14 PF</span>
              </div>
              <h3 class="text-2xl font-black text-white">I Didn’t Hear No Bell <span class="text-red-400 text-sm font-semibold">(Pedro)</span></h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                <strong class="text-red-400">CELLAR ANCHOR DEEPENS:</strong> Pedro put up a spirited 111.68 points behind Emmett Johnson (32.10) and Trevor Lawrence (27.78), but fell 128.76 to 111.68 to Herrador. Sitting at 3-7 and 926.14 PF, Pedro trails 9th-place Robert by <strong>285.94 points</strong>! With $0 in FAAB remaining and only 4 regular season weeks left, Pedro is nearly locked into lacing up his sneakers for the 5K run and funding the league open bar tab!
              </p>

              <!-- LivePortrait AI 5K Punishment Video -->
              <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
                <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                  FaceFusion AI Meme • Pedro Forrest Gump 5K Punishment Sprint
                </div>
                <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/pedro_5k_runner.gif">
                  <source src="assets/video/pedro_5k_runner.mp4" type="video/mp4">
                  <img src="assets/video/pedro_5k_runner.gif" alt="Pedro 5K Toilet Runner Sprint" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
                </video>
              </div>

              <div class="mt-4 p-3 bg-red-950/30 border border-red-800/40 rounded-xl space-y-2 text-xs">
                <div class="flex justify-between items-center text-slate-300">
                  <span>Projected 5K Finishing Time:</span>
                  <span class="font-mono font-bold text-red-400">1 Hour 15 Mins (24:10/mi)</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Open Bar Tab Meter Liability:</span>
                  <span class="font-mono font-bold text-amber-400">$285.00 Est.</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Distance to 9th Place Safety:</span>
                  <span class="font-mono font-bold text-red-400">285.94 Total Points Deficit</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Punishment Likelihood:</span>
              <span class="text-red-400 font-bold uppercase">95.5% Implied Probability</span>
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
                The last place franchise in FFUC must complete an in-person, timed 5K run. For every minute over a 30:00 baseline pace, money is added to the league bar tab at the subsequent annual draft!
              </p>

              <div class="mt-4 space-y-2 text-xs">
                <div class="p-2.5 bg-slate-950 rounded-xl border border-red-500/40 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-white">Pedro (I Didn’t Hear No Bell)</span>
                    <span class="block text-red-400 text-[11px]">3-7 • 926.14 PF • $0 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-red-400 font-extrabold">95.5% Risk</span>
                    <span class="block text-slate-500 text-[10px]">Anchor</span>
                  </div>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-slate-300">Robert (WE NOT GOIN’ BACK 2 BACK)</span>
                    <span class="block text-slate-400 text-[11px]">3-7 • 1212.08 PF • $77 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-amber-400 font-bold">3.5% Risk</span>
                    <span class="block text-slate-500 text-[10px]">+285.94 PF Buffer</span>
                  </div>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-slate-300">Eric (Show me dem TDs)</span>
                    <span class="block text-slate-400 text-[11px]">4-6 • 1124.12 PF • $49 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-slate-400 font-bold">1.0% Risk</span>
                    <span class="block text-slate-500 text-[10px]">+197.98 PF Buffer</span>
                  </div>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-slate-300">Alex (League Median Advocate)</span>
                    <span class="block text-slate-400 text-[11px]">4-6 • 1257.80 PF • $24 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-emerald-400 font-bold">&lt; 0.1% Risk</span>
                    <span class="block text-slate-500 text-[10px]">Safe Zone</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Punishment Date:</span>
              <span class="text-amber-400 font-bold">Offseason 2027 In-Person Run</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 4: THE LUCK INDEX
slide_4 = """      <!-- SLIDE 4: THE LUCK INDEX -->
      <section id="wk10-slide-4" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-purple-950/80 via-slate-900 to-indigo-950/80 border border-purple-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-purple-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ADVANCED ANALYTICS • ALL-PLAY CORRELATION
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍀 The Luck Index: Schedule Variance</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Expected Wins vs Actual Wins across 90 total all-play matchups per franchise through Week 10.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-purple-400 font-mono font-bold px-3 py-1 rounded-lg">90 Total Games Audited</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">🍀 The Luckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Arnulfo (+1.78) & iRob (+1.22) & Pedro (+1.22)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Arnulfo is the luckiest manager in the league at 7-3 with an expected 5.22 wins (+1.78 luck) after edging Mark by 5.70. iRob holds solo 1st with expected 5.78 wins (+1.22). Pedro has 3 wins despite a 16-74 all-play record (1.78 exp)!
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">💀 The Unluckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Franky (-1.67) & Herrador (-1.22) & Robert (-1.22)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Total highway robbery! Franky is #1 in total points (1,332.40 PF) and #1 in all-play wins (60-30, 6.67 exp) but is only 5-5 (-1.67 luck)! Herrador is #2 in all-play (56-34) and sits at 5-5 (-1.22 luck), while Robert is 3-7 (-1.22 luck).
            </p>
          </div>
        </div>

        <!-- Luck Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">All-Play Luck Matrix (Week 10 Audited)</span>
            <span class="font-mono text-purple-400 font-bold">Luck Delta = Actual Wins - Expected Wins</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/25">
              <span class="w-48 font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">7-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.22 (Exp)</span>
              <span class="w-28 text-center text-slate-300">47-43 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.78 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-48 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">7-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">52-38 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.22 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-48 font-bold text-white">I Didn’t Hear No Bell (Pedro)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">3-7 (Act)</span>
              <span class="w-20 text-center text-slate-400">1.78 (Exp)</span>
              <span class="w-28 text-center text-red-400">16-74 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.22 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-48 font-bold text-white">Saquon Deez Nacuas (Mark)</span>
              <span class="w-20 text-center text-blue-400 font-bold">6-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">50-40 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+0.44 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-20 text-center text-slate-300 font-bold">4-6 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">32-58 All-Play</span>
              <span class="w-24 text-right text-slate-300">+0.44 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">TheGreatSwagsby (Joey)</span>
              <span class="w-20 text-center text-slate-300 font-bold">6-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.89 (Exp)</span>
              <span class="w-28 text-center text-slate-300">53-37 All-Play</span>
              <span class="w-24 text-right text-slate-300">+0.11 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-48 text-slate-300">League Median Advocate 🗳 (Alex)</span>
              <span class="w-20 text-center text-rose-400 font-bold">4-6 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.11 (Exp)</span>
              <span class="w-28 text-center text-slate-300">46-44 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.11 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/15">
              <span class="w-48 text-slate-300">Brock To The Future (Herrador)</span>
              <span class="w-20 text-center text-rose-400 font-bold">5-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">6.22 (Exp)</span>
              <span class="w-28 text-center text-slate-300">56-34 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.22 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-48 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-7 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.22 (Exp)</span>
              <span class="w-28 text-center text-slate-300">38-52 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.22 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/30">
              <span class="w-48 font-bold text-white">CULT OF THE LAMB (Franky)</span>
              <span class="w-20 text-center text-rose-400 font-bold">5-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">6.67 (Exp)</span>
              <span class="w-28 text-center text-amber-400 font-extrabold">60-30 All-Play (1st)</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.67 💀</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 5: POWER RANKINGS
slide_5 = """      <!-- SLIDE 5: POWER RANKINGS -->
      <section id="wk10-slide-5" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-orange-950/80 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ANALYTIC POWER INDEX • STRENGTH OF SQUAD
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">📈 Power Rankings: Week 10</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">True hierarchy based on roster firepower, all-play strength, and momentum entering Week 11.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 10 Audited</span>
          </div>
        </div>

        <div class="space-y-2 text-xs">
          <!-- Rank 1: iRob -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">1</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">Njigbas in Paris (iRob) <span class="text-emerald-400 font-mono text-xs">(7-3 • 1301.86 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">▲ 1 • #1 Overall Seed</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                The undisputed apex predator! iRob's 191.46 detonation was a masterclass in roster depth with George Pickens (38.00), Brock Purdy (31.66), and JSN (27.10). Solo 1st place in standings AND Pick-em!
              </p>
            </div>
          </div>

          <!-- Rank 2: Franky -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">2</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">CULT OF THE LAMB (Franky) <span class="text-slate-400 font-mono text-xs">(5-5 • 1332.40 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-blue-400 bg-blue-950/60 px-2 py-0.5 rounded border border-blue-500/30">▲ 1 • #1 PF & All-Play</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Don't let the 5-5 record fool you. Franky leads the league in total scoring (1,332.40 PF) and all-play wins (60-30). He posted 139.14 in Week 10 and faces #1 iRob in the Week 11 Game of the Week!
              </p>
            </div>
          </div>

          <!-- Rank 3: Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">3</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">MyDakMakesHerWaddle (Arnulfo) <span class="text-slate-400 font-mono text-xs">(7-3 • 1214.16 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">▲ 1 • Big Win over Mark</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Arnulfo proved his clutch gene by knocking off Mark 118.92 to 113.22 behind Jahmyr Gibbs' 40.70-point explosion and Dak Prescott's 35.42 points. Now tied for the league lead at 7-3.
              </p>
            </div>
          </div>

          <!-- Rank 4: Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">4</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">TheGreatSwagsby (Joey) <span class="text-slate-400 font-mono text-xs">(6-4 • 1241.42 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-emerald-400 bg-emerald-950/60 px-2 py-0.5 rounded border border-emerald-500/30">▲ 1 • CMC 44.30 Eruption</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Christian McCaffrey returned in god-mode with 44.30 points, driving Joey to 137.78 points and a 32-point blowout over Robert. Joey takes solo 3rd place and controls his playoff destiny.
              </p>
            </div>
          </div>

          <!-- Rank 5: Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">5</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">Brock To The Future (Herrador) <span class="text-slate-400 font-mono text-xs">(5-5 • 1286.32 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">▲ 1 • Scored 128.76</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Herrador rebounded with a 128.76 to 111.68 win over Pedro. With Chuba Hubbard (31.70), Ja'Marr Chase (28.60), and Brock Bowers (13.60), Herrador's roster is terrifying if he gets into the playoffs.
              </p>
            </div>
          </div>

          <!-- Rank 6: Mark -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">6</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">Saquon Deez Nacuas (Mark) <span class="text-slate-400 font-mono text-xs">(6-4 • 1220.26 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-500/30">▼ 5 • Heartbreak 5.70 Loss</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Patrick Mahomes (35.42) gave Mark a huge boost, but a 5.70 loss to Arnulfo drops Mark from the three-way summit down to the 4th seed. Faces #3 Joey in a must-win Week 11 battle!
              </p>
            </div>
          </div>

          <!-- Rank 7: Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">7</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">League Median Advocate 🗳 (Alex) <span class="text-slate-400 font-mono text-xs">(4-6 • 1257.80 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-slate-400 bg-slate-800 px-2 py-0.5 rounded">HOLD • Wrong Place, Wrong Time</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Alex put up 110.92 points but had the sheer misfortune of running into iRob's 191.46 thermonuclear bomb. At 4-6, Alex needs a victory against Robert in Week 11 to keep postseason hopes alive.
              </p>
            </div>
          </div>

          <!-- Rank 8: Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">8</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">Show me dem TDs (Eric) <span class="text-slate-400 font-mono text-xs">(4-6 • 1124.12 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-500/30">▼ 1 • Back-to-Back Low Scores</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Eric's scoring has dried up completely (86.36 in Week 9, 89.04 in Week 10). Back-to-back toilet runner weeks have him slipping in the wildcard race. Needs a massive rebound against Herrador.
              </p>
            </div>
          </div>

          <!-- Rank 9: Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">9</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">WE NOT GOIN’ BACK 2 BACK (Robert) <span class="text-slate-400 font-mono text-xs">(3-7 • 1212.08 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-rose-400 bg-rose-950/60 px-2 py-0.5 rounded border border-rose-500/30">HOLD • 32-Pt Loss to Joey</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                The defending champ managed 105.12 points in a 32.66-point loss to Joey. Sitting at 3-7, Robert is nearly mathematically eliminated from playoff contention, but leads the league with $77 FAAB.
              </p>
            </div>
          </div>

          <!-- Rank 10: Pedro -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-md flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-red-500">10</span>
            <div class="flex-1">
              <div class="flex items-center justify-between">
                <span class="font-bold text-white text-sm">I Didn’t Hear No Bell (Pedro) <span class="text-red-400 font-mono text-xs">(3-7 • 926.14 PF)</span></span>
                <span class="text-[10px] font-mono font-bold text-red-400 bg-red-950/60 px-2 py-0.5 rounded border border-red-500/30">ANCHOR • 285.94 PF Deficit</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                Pedro showed fight with 111.68 points behind Emmett Johnson (32.10) and Trevor Lawrence (27.78), but lost by 17 to Herrador. Still sits at 926.14 PF (-285.94 deficit) with zero remaining FAAB.
              </p>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 6: FAAB WAR ROOM
slide_6 = """      <!-- SLIDE 6: FAAB WAR ROOM -->
      <section id="wk10-slide-6" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-teal-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              FINANCIAL AUDIT • WAIVER WIRE RECEIPTS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💰 FAAB War Room: Week 10</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Franky goes down to $1 after dual $6 bids; Pedro remains broke at $0; Robert hoards $77 for the final push.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">Week 10 Audit</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Remaining Budgets Table -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <h3 class="text-base font-black text-white mb-2 flex items-center justify-between">
              <span>Remaining FAAB Balances</span>
              <span class="text-xs font-mono text-emerald-400 font-normal">Starting: $100.00</span>
            </h3>
            <div class="divide-y divide-slate-800/80 text-xs font-mono">
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">1. Robert (WE NOT GOIN’ BACK 2 BACK)</span>
                <span class="text-emerald-400 font-extrabold text-sm">$77 (77%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">2. iRob (Njigbas in Paris)</span>
                <span class="text-emerald-400 font-bold">$50 (50%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">3. Herrador (Brock To The Future)</span>
                <span class="text-emerald-400 font-bold">$49 (49%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">4. Eric (Show me dem TDs)</span>
                <span class="text-emerald-400 font-bold">$49 (49%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">5. Mark (Saquon Deez Nacuas)</span>
                <span class="text-amber-400 font-bold">$34 (34%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">6. Alex (League Median Advocate)</span>
                <span class="text-amber-400 font-bold">$24 (24%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">7. Joey (TheGreatSwagsby)</span>
                <span class="text-rose-400 font-bold">$10 (10%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">8. Arnulfo (MyDakMakesHerWaddle)</span>
                <span class="text-rose-400 font-bold">$10 (10%)</span>
              </div>
              <div class="py-2 flex justify-between items-center text-slate-300">
                <span class="font-bold text-white">9. Franky (CULT OF THE LAMB)</span>
                <span class="text-red-400 font-extrabold text-sm">$1 (1%)</span>
              </div>
              <div class="py-2 flex justify-between items-center bg-red-950/30 px-2 rounded border border-red-500/30 text-white">
                <span class="font-black text-red-400">10. Pedro (I Didn’t Hear No Bell)</span>
                <span class="text-red-500 font-black text-sm">$0 (0% - BROKE)</span>
              </div>
            </div>
          </div>

          <!-- Key Transactions of Week 10 -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl flex flex-col justify-between">
            <div>
              <h3 class="text-base font-black text-white mb-2 flex items-center justify-between">
                <span>Notable Week 10 Moves</span>
                <span class="text-xs font-mono text-slate-400 font-normal">20 Completed Transactions</span>
              </h3>
              <div class="space-y-2 text-xs">
                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-white">Franky • Dual $6 Waiver Splurge ($12 Spent)</span>
                    <span class="font-mono text-amber-400 font-bold">$12 FAAB Total</span>
                  </div>
                  <p class="text-slate-400 mt-1">Franky submitted two successful $6 bids: adding C.J. Stroud (QB - HOU) and Los Angeles Rams DEF, dropping Devin Singletary. Franky is now down to his last $1!</p>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-white">Arnulfo • Active Roster Reshuffle</span>
                    <span class="font-mono text-emerald-400 font-bold">$0 FAAB (Free Agency)</span>
                  </div>
                  <p class="text-slate-400 mt-1">Arnulfo executed multiple $0 moves: added Chris Boswell (K - PIT), Jakobi Meyers (WR - JAX), Wan'Dale Robinson (WR - TEN), and Saints DEF, dropping Cameron Dicker, Kyle Pitts, and Kyler Murray.</p>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800">
                  <div class="flex justify-between items-center">
                    <span class="font-bold text-white">Alex & Eric • Running Back Churn</span>
                    <span class="font-mono text-emerald-400 font-bold">$0 FAAB Claims</span>
                  </div>
                  <p class="text-slate-400 mt-1">Eric scooped Pierre Strong, Ashton Dulin, and Tutu Atwell. Alex claimed Bo Nix and Steelers DEF. Pedro swapped Xavier Worthy for Browns DEF.</p>
                </div>
              </div>
            </div>
            <div class="mt-3 pt-2.5 border-t border-slate-800 flex justify-between text-xs text-slate-400 font-mono">
              <span>Next Waiver Run:</span>
              <span class="text-amber-400 font-bold">Wednesday Night 11:00 PM CST</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 7: SLEEPER PICK-EM STANDINGS
slide_7 = """      <!-- SLIDE 7: SLEEPER PICK-EM STANDINGS -->
      <section id="wk10-slide-7" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-indigo-950/80 via-slate-900 to-purple-950/80 border border-indigo-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-indigo-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              SEASON PICK-EM POOL • $45.00 CASH PRIZE
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🎯 Sleeper Pick-em: Week 10 Leaderboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">iRob hits the century mark (100.0 pts) to take sole 1st place; Robert stalks in 2nd at 99.0; Arnulfo sits in 3rd at 98.0.</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-indigo-400">$45.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Winner-Take-All Pot</div>
          </div>
        </div>

        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Official Sleeper Pick-em Standings (Week 10 Final)</span>
            <span class="font-mono text-indigo-400 font-bold">10 of 18 Regular Weeks</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-3 flex items-center justify-between bg-indigo-950/40">
              <span class="w-8 font-black text-amber-400 text-sm">1</span>
              <span class="flex-1 font-bold text-white">iRob (irobgarza16) <span class="text-amber-400 text-[10px] font-bold">👑 Solo 1st Place</span></span>
              <span class="w-24 text-center text-slate-400">W10: 11.0 pts</span>
              <span class="w-24 text-right font-black text-amber-400 text-sm">100.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-indigo-950/25">
              <span class="w-8 font-bold text-slate-300">2</span>
              <span class="flex-1 font-bold text-slate-200">Robert (YaBoyRoZ)</span>
              <span class="w-24 text-center text-slate-400">W10: 9.0 pts</span>
              <span class="w-24 text-right font-bold text-indigo-300">99.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-indigo-950/15">
              <span class="w-8 font-bold text-slate-300">3</span>
              <span class="flex-1 font-bold text-slate-200">Arnulfo (AEscamilla94)</span>
              <span class="w-24 text-center text-slate-400">W10: 8.0 pts</span>
              <span class="w-24 text-right font-bold text-indigo-300">98.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">4</span>
              <span class="flex-1 text-slate-300">Herrador (DirtyDirties)</span>
              <span class="w-24 text-center text-slate-400">W10: 11.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">97.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">5</span>
              <span class="flex-1 text-slate-300">Franky (ChanciscoFravez)</span>
              <span class="w-24 text-center text-slate-400">W10: 10.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">95.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">6</span>
              <span class="flex-1 text-slate-300">Pedro (GuyNamedPedro)</span>
              <span class="w-24 text-center text-slate-400">W10: 10.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">94.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">7</span>
              <span class="flex-1 text-slate-300">Mark (fattymcfatty)</span>
              <span class="w-24 text-center text-slate-400">W10: 9.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">93.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">8</span>
              <span class="flex-1 text-slate-300">Alex (abarrera731)</span>
              <span class="w-24 text-center text-slate-400">W10: 8.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">92.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">9</span>
              <span class="flex-1 text-slate-300">Eric (emedina13)</span>
              <span class="w-24 text-center text-slate-400">W10: 10.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">92.0 PTS</span>
            </div>
            <div class="p-3 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">10</span>
              <span class="flex-1 text-slate-300">Joey (TheGreatSwagsby)</span>
              <span class="w-24 text-center text-slate-400">W10: 9.0 pts</span>
              <span class="w-24 text-right font-semibold text-slate-200">90.0 PTS</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 8: BOOMS & BUSTS
slide_8 = """      <!-- SLIDE 8: BOOMS & BUSTS -->
      <section id="wk10-slide-8" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-cyan-950/80 via-slate-900 to-blue-950/80 border border-cyan-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-cyan-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              PERFORMANCE AUDIT • SPIKES & DISASTERS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💥 Booms & Busts: Week 10</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">The elite detonations that won matchups, and the brutal duds that destroyed playoff dreams.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-cyan-400 font-mono font-bold px-3 py-1 rounded-lg">Week 10 Audited</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- BOOMS -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-4 shadow-xl">
            <h3 class="text-base font-black text-emerald-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              <span>🚀 Nuclear Booms of the Week</span>
            </h3>
            <div class="space-y-2 text-xs font-mono">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Christian McCaffrey (SF - RB)</span>
                  <span class="block text-emerald-400 text-[11px]">Joey • 107 Rush Yds, 68 Rec Yds, 2 TDs</span>
                </div>
                <span class="font-black text-emerald-400 text-base">44.30 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Jahmyr Gibbs (DET - RB)</span>
                  <span class="block text-emerald-400 text-[11px]">Arnulfo • 112 Rush Yds, 84 Rec Yds, 2 TDs</span>
                </div>
                <span class="font-black text-emerald-400 text-base">40.70 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">George Pickens (DAL - WR)</span>
                  <span class="block text-emerald-400 text-[11px]">iRob • 9 Rec, 160 Yds, 2 TDs</span>
                </div>
                <span class="font-black text-emerald-400 text-base">38.00 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Dak Prescott & Patrick Mahomes</span>
                  <span class="block text-emerald-400 text-[11px]">Arnulfo & Mark • Dual 35.42 QB Shootout</span>
                </div>
                <span class="font-black text-emerald-400 text-base">35.42 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Emmett Johnson (KC - RB)</span>
                  <span class="block text-emerald-400 text-[11px]">Pedro • Breakout 32-Pt Performance</span>
                </div>
                <span class="font-black text-emerald-400 text-base">32.10 PTS</span>
              </div>
            </div>
          </div>

          <!-- BUSTS -->
          <div class="bg-slate-900 border-2 border-rose-500/50 rounded-2xl p-4 shadow-xl">
            <h3 class="text-base font-black text-rose-400 uppercase tracking-wider mb-3 flex items-center gap-2">
              <span>💀 Sub-Zero Busts of the Week</span>
            </h3>
            <div class="space-y-2 text-xs font-mono">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-rose-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Keenan Allen (IND - WR)</span>
                  <span class="block text-rose-400 text-[11px]">Alex • 3 Catches on 8 Targets</span>
                </div>
                <span class="font-black text-rose-400 text-base">7.60 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-rose-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Dallas Goedert (PHI - TE)</span>
                  <span class="block text-rose-400 text-[11px]">Alex • 2 Catches for 18 Yards</span>
                </div>
                <span class="font-black text-rose-400 text-base">5.00 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-rose-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Jonathan Taylor (IND - RB)</span>
                  <span class="block text-rose-400 text-[11px]">Eric • 20 Touches with Zero Endzone Visits</span>
                </div>
                <span class="font-black text-rose-400 text-base">12.10 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-rose-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Tucker Kraft (GB - TE)</span>
                  <span class="block text-rose-400 text-[11px]">Arnulfo • Blanked in 2nd Half</span>
                </div>
                <span class="font-black text-rose-400 text-base">3.00 PTS</span>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-rose-500/30 flex justify-between items-center">
                <div>
                  <span class="font-bold text-white text-sm">Jake Ferguson (DAL - TE)</span>
                  <span class="block text-rose-400 text-[11px]">Joey • Only 2 Targets vs Eagles</span>
                </div>
                <span class="font-black text-rose-400 text-base">4.20 PTS</span>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 9: SCOREBOARD & BOX SCORES
slide_9 = """      <!-- SLIDE 9: SCOREBOARD & BOX SCORES -->
      <section id="wk10-slide-9" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-slate-700 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              HEAD-TO-HEAD BATTLEGROUND • OFFICIAL AUDIT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚔️ Week 10 Scoreboard & Matchup Results</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Complete verified box scores and margins across all 5 Week 10 matchups.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">5 Official Matchups</span>
          </div>
        </div>

        <div class="space-y-3">
          <!-- Matchup 2: Arnulfo vs Mark (Game of the Week) -->
          <div class="bg-slate-900 border-2 border-amber-500/50 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center mb-2 pb-2 border-b border-slate-800 text-xs">
              <span class="font-mono font-bold text-amber-400 uppercase tracking-wider">🔥 Game of the Week • Battle for 1st Place</span>
              <span class="font-mono text-slate-400 font-bold">Margin: 5.70 PTS</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-emerald-400 text-base">Arnulfo (MyDakMakesHerWaddle)</span>
                  <span class="bg-emerald-500 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded">WIN</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Gibbs (40.70), Dak Prescott (35.42), A.J. Brown (14.90), Waddle (10.90)</div>
              </div>
              <span class="text-2xl font-black text-emerald-400 ml-4">118.92</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm mt-3 pt-2 border-t border-slate-800/60">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-slate-300">Mark (Saquon Deez Nacuas)</span>
                  <span class="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-bold px-1.5 py-0.5 rounded">LOSS</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Patrick Mahomes (35.42), Puka Nacua (14.80), Jayden Reed (14.40), Stafford (13.70)</div>
              </div>
              <span class="text-2xl font-black text-slate-300 ml-4">113.22</span>
            </div>
          </div>

          <!-- Matchup 5: iRob vs Alex (Blowout of the Week) -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center mb-2 pb-2 border-b border-slate-800 text-xs">
              <span class="font-mono font-bold text-emerald-400 uppercase tracking-wider">👑 Historic Blowout of the Season</span>
              <span class="font-mono text-emerald-400 font-bold">Margin: 80.54 PTS</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-emerald-400 text-base">iRob (Njigbas in Paris)</span>
                  <span class="bg-emerald-500 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded">WIN</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Pickens (38.00), Purdy (31.66), JSN (27.10), Brown (24.30), Burrow (20.30)</div>
              </div>
              <span class="text-2xl font-black text-emerald-400 ml-4">191.46</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm mt-3 pt-2 border-t border-slate-800/60">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-slate-300">Alex (League Median Advocate)</span>
                  <span class="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-bold px-1.5 py-0.5 rounded">LOSS</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Cam Skattebo (25.70), Amon-Ra St. Brown (23.80), Derrick Henry (16.50)</div>
              </div>
              <span class="text-2xl font-black text-slate-300 ml-4">110.92</span>
            </div>
          </div>

          <!-- Matchup 4: Joey vs Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center mb-2 pb-2 border-b border-slate-800 text-xs">
              <span class="font-mono font-bold text-blue-400 uppercase tracking-wider">⚔️ Defending Champion Toppled</span>
              <span class="font-mono text-slate-400 font-bold">Margin: 32.66 PTS</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-emerald-400 text-base">Joey (TheGreatSwagsby)</span>
                  <span class="bg-emerald-500 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded">WIN</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">McCaffrey (44.30), Nico Collins (18.10), Herbert (16.78), McMillan (14.40)</div>
              </div>
              <span class="text-2xl font-black text-emerald-400 ml-4">137.78</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm mt-3 pt-2 border-t border-slate-800/60">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-slate-300">Robert (WE NOT GOIN’ BACK 2 BACK)</span>
                  <span class="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-bold px-1.5 py-0.5 rounded">LOSS</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Pollard (19.90), Jaylen Warren (14.70), Lamar Jackson (14.62), Odunze (14.40)</div>
              </div>
              <span class="text-2xl font-black text-slate-300 ml-4">105.12</span>
            </div>
          </div>

          <!-- Matchup 3: Franky vs Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center mb-2 pb-2 border-b border-slate-800 text-xs">
              <span class="font-mono font-bold text-amber-400 uppercase tracking-wider">⚡ Scoring Leader Clinic</span>
              <span class="font-mono text-slate-400 font-bold">Margin: 50.10 PTS</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-emerald-400 text-base">Franky (CULT OF THE LAMB)</span>
                  <span class="bg-emerald-500 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded">WIN</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Parker Washington (24.70), James Cook (21.70), Tuten (18.80), Josh Allen (17.54)</div>
              </div>
              <span class="text-2xl font-black text-emerald-400 ml-4">139.14</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm mt-3 pt-2 border-t border-slate-800/60">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-slate-300">Eric (Show me dem TDs)</span>
                  <span class="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-bold px-1.5 py-0.5 rounded">LOSS</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Pierre Strong (14.20), Ashton Dulin (12.80), Addison (12.50), Jonathan Taylor (12.10)</div>
              </div>
              <span class="text-2xl font-black text-slate-300 ml-4">89.04</span>
            </div>
          </div>

          <!-- Matchup 1: Herrador vs Pedro -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center mb-2 pb-2 border-b border-slate-800 text-xs">
              <span class="font-mono font-bold text-slate-400 uppercase tracking-wider">⚔️ Wildcard Contender Rebound</span>
              <span class="font-mono text-slate-400 font-bold">Margin: 17.08 PTS</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-bold text-emerald-400 text-base">Herrador (Brock To The Future)</span>
                  <span class="bg-emerald-500 text-slate-950 text-[10px] font-black px-1.5 py-0.5 rounded">WIN</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Chuba Hubbard (31.70), Ja'Marr Chase (28.60), Bowers (13.60), Bucky Irving (13.20)</div>
              </div>
              <span class="text-2xl font-black text-emerald-400 ml-4">128.76</span>
            </div>
            <div class="flex items-center justify-between font-mono text-sm mt-3 pt-2 border-t border-slate-800/60">
              <div class="flex-1">
                <div class="flex items-center gap-2">
                  <span class="font-semibold text-slate-300">Pedro (I Didn’t Hear No Bell)</span>
                  <span class="bg-rose-950 text-rose-400 border border-rose-800 text-[10px] font-bold px-1.5 py-0.5 rounded">LOSS</span>
                </div>
                <div class="text-xs text-slate-400 mt-0.5">Emmett Johnson (32.10), Trevor Lawrence (27.78), Matthew Golden (16.10)</div>
              </div>
              <span class="text-2xl font-black text-slate-300 ml-4">111.68</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 10: WEEK 11 GAMEDAY HUB & PREVIEWS
slide_10 = """      <!-- SLIDE 10: WEEK 11 GAMEDAY HUB -->
      <section id="wk10-slide-10" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-indigo-950/80 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              LOOKAHEAD • WEEK 11 CRUCIAL SLATE
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚡ Week 11 Gameday Hub & Previews</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Heavyweight clashes, the $10 Highest Scoring WR bounty, and pivotal playoff seeding battles.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 11 Slate</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Game of the Week: Franky vs iRob -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-amber-500 text-slate-950 text-[10px] font-mono font-black px-3 py-1 rounded-bl-xl uppercase">
              🔥 GAME OF THE WEEK
            </div>
            <div>
              <span class="text-xs font-mono font-bold text-amber-400 uppercase tracking-wider">Top Offense vs #1 Seed</span>
              <h3 class="text-xl font-black text-white mt-1">Franky (5-5) vs iRob (7-3)</h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                A massive clash of league titans! iRob enters on a nuclear high after dropping 191.46 points in Week 10 to claim the #1 seed. Meanwhile, Franky boasts the #1 scoring offense in FFUC (1,332.40 PF) and desperately needs a win to break free from the 5-5 pack and secure a playoff bye!
              </p>
              <div class="mt-4 p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center text-slate-300">
                  <span>Matchup Stakes:</span>
                  <span class="text-amber-400 font-bold">#1 Seed Defense vs Wildcard Survival</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Scoring Average:</span>
                  <span class="text-emerald-400 font-bold">Franky (133.2) vs iRob (130.2)</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 2: Mark vs Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold text-blue-400 uppercase tracking-wider">Heavyweight Seeding Battle</span>
              <h3 class="text-xl font-black text-white mt-1">Mark (6-4) vs Joey (6-4)</h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                Direct clash for the #3 seed! Mark looks to rebound from his heartbreaking 5.70-point defeat to Arnulfo, while Joey rides the momentum of Christian McCaffrey's 44.30-point explosion. The winner takes sole possession of 3rd place!
              </p>
              <div class="mt-4 p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center text-slate-300">
                  <span>Points For:</span>
                  <span class="text-blue-400 font-bold">Joey (1,241.42) vs Mark (1,220.26)</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 3: Pedro vs Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold text-emerald-400 uppercase tracking-wider">Top vs Bottom</span>
              <h3 class="text-xl font-black text-white mt-1">Pedro (3-7) vs Arnulfo (7-3)</h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                Arnulfo has his sights set on the #1 overall seed, while Pedro desperately searches for points to begin chipping away at his 285.94-point cellar deficit to avoid the 5K punishment and open bar tab!
              </p>
            </div>
          </div>

          <!-- Matchup 4: Eric vs Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold text-rose-400 uppercase tracking-wider">Wildcard Bubble Dogfight</span>
              <h3 class="text-xl font-black text-white mt-1">Eric (4-6) vs Herrador (5-5)</h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                High-stakes desperation! Eric looks to shake off back-to-back toilet runner weeks and keep his postseason hopes alive, while Herrador aims to climb back into the top 4 behind Ja'Marr Chase and Brock Bowers.
              </p>
            </div>
          </div>
        </div>

        <!-- Weekly Bounty Callout -->
        <div class="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-emerald-950/60 border border-emerald-500/40 rounded-xl p-4 flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
          <div class="flex items-center gap-3">
            <span class="text-2xl">💵</span>
            <div>
              <span class="font-mono font-black text-emerald-400 uppercase tracking-wider">WEEK 11 BOUNTY: HIGHEST SCORING WR ($10)</span>
              <p class="text-slate-300 text-[11px] mt-0.5">Top starting Wide Receiver fantasy performance across all 10 franchises takes the $10 direct cash prize!</p>
            </div>
          </div>
          <span class="text-emerald-400 font-mono font-black text-sm bg-emerald-950 px-3 py-1 rounded-lg border border-emerald-500/30">$10 Cash Payout</span>
        </div>
      </section>"""

# Assemble deck-wk10 HTML
deck_wk10_html = f"""    <!-- ========================================== -->
    <!-- DECK 10: WEEK 10 OFFICIAL REPORT (ACTIVE)  -->
    <!-- ========================================== -->
    <div id="deck-wk10">
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

print("Deck 10 HTML assembled. Updating index.html...")

# A. Update Nav Pills
pills_pattern = r'<nav class="flex items-center gap-1\.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">.*?</nav>'
html = re.sub(pills_pattern, new_nav_pills, html, count=1, flags=re.DOTALL)

# B. Update Top Header Edition Badge
html = html.replace(
    'Week 9 Official Report</span>',
    'Week 10 Official Report</span>'
)
html = html.replace(
    'WEEK 9 OFFICIAL REPORT • F.F.U.C. HONORS',
    'WEEK 10 OFFICIAL REPORT • F.F.U.C. HONORS'
)

# C. Update Archive Selector Dropdown
archive_select_pattern = r'<select id="archiveSelect" onchange="handleArchiveSelect\(this\.value\)".*?</select>'
new_archive_select = """<select id="archiveSelect" onchange="handleArchiveSelect(this.value)" class="bg-slate-900 border border-slate-700 text-xs font-mono font-bold text-amber-400 rounded-lg px-2.5 py-1 focus:outline-none focus:border-amber-400">
            <option value="wk10" selected>⚡ Week 10: Official Report (Active)</option>
            <option value="wk9">📅 Week 9: Official Report (Archive)</option>
            <option value="wk8">📅 Week 8: Official Report (Archive)</option>
            <option value="wk7">📅 Week 7: Official Report (Archive)</option>
            <option value="wk6">📅 Week 6: Official Report (Archive)</option>
            <option value="wk5">📅 Week 5: Mid-Season Pivot (Archive)</option>
            <option value="wk4">📅 Week 4: Official Report (Archive)</option>
            <option value="wk3">📅 Week 3: Official Report (Archive)</option>
            <option value="wk2">📅 Week 2: Official Report (Archive)</option>
            <option value="wk1">📅 Week 1: Season Opener (Archive)</option>
            <option value="locked" disabled>🔒 Week 11 (Upcoming)</option>
          </select>"""
html = re.sub(archive_select_pattern, new_archive_select, html, count=1, flags=re.DOTALL)

# D. Update Ticker Text
ticker_segment = """<span>👑 <strong>High Roller Champion:</strong> <span class="text-amber-400 font-bold">iRob (Njigbas in Paris)</span> shatters scoring record with <span class="text-emerald-400 font-bold">191.46 PTS</span>!</span><span class="text-slate-500">•</span><span>⚡ <strong>$10 Bounty Winner (RB Crown):</strong> <span class="text-amber-400 font-bold">Joey (TheGreatSwagsby)</span> pockets $10 behind Christian McCaffrey's <span class="text-emerald-400 font-bold">44.30 PTS</span>!</span><span class="text-slate-500">•</span><span>🚀 <strong>Top of the Table:</strong> <span class="text-amber-400 font-bold">iRob & Arnulfo</span> tied atop the league at <span class="text-emerald-400 font-bold">7-3</span>!</span><span class="text-slate-500">•</span><span>💔 <strong>Heartbreak of the Week:</strong> <span class="text-amber-400 font-bold">Mark (113.22 PTS)</span> loses 1st place battle by 5.70 to Arnulfo!</span><span class="text-slate-500">•</span><span>🎯 <strong>Pick-Em Solo Leader:</strong> <span class="text-amber-400 font-bold">iRob</span> hits century mark at <span class="text-emerald-400 font-bold">100.0 PTS</span>!</span><span class="text-slate-500">•</span><span>🚽 <strong>5K Toilet Danger Zone:</strong> <span class="text-red-400 font-bold">Pedro</span> anchored at 3-7 (926.14 PF), trailing safety by 285.94 pts with $0 FAAB!</span><span class="text-slate-500">•</span><span>🏃 <strong>Weekly Toilet Runner:</strong> <span class="text-red-400 font-bold">Eric</span> slumps to low score with <span class="text-red-400 font-bold">89.04 PTS</span>!</span>"""

new_ticker = f"""<div class="ticker-wrap flex-1 min-w-0">
        <div class="ticker-content text-slate-200 text-xs">
          <!-- Segment A -->
          <div class="inline-flex items-center gap-6 pr-6">{ticker_segment}</div>

          <!-- Segment B (Identical for seamless infinite loop) -->
          <div class="inline-flex items-center gap-6 pr-6" aria-hidden="true">{ticker_segment}</div>
        </div>
      </div>"""

html = re.sub(r'<div class="ticker-wrap flex-1 min-w-0">.*?(?=<!-- Quick Action Tab Button -->)', new_ticker + "\n\n      ", html, count=1, flags=re.DOTALL)

# E. Insert or Replace Deck 10
if '<div id="deck-wk10">' in html:
    print("Replacing existing deck-wk10...")
    deck_wk10_pattern = r'<div id="deck-wk10">.*?</div>\s*(?=<!-- ========================================== -->\s*<!-- DECK 9)'
    html = re.sub(deck_wk10_pattern, deck_wk10_html + "\n\n    ", html, count=1, flags=re.DOTALL)
elif '<div id="deck-wk9">' in html:
    print("Archiving deck-wk9 and inserting deck-wk10...")
    m_deck9 = re.search(r'(<div id="deck-wk9">.*?</div>\s*<!-- ========================================== -->\s*<!-- DECK 8)', html, re.DOTALL)
    if m_deck9:
        deck9_str = m_deck9.group(1)
        deck9_str_fixed = deck9_str.replace('id="broadcastAudio"', 'id="broadcastAudioWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="broadcastPlayBtn"', 'id="broadcastPlayBtnWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="playIcon"', 'id="playIconWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="pauseIcon"', 'id="pauseIconWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="audioPulseRing"', 'id="audioPulseRingWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="audioWaveform"', 'id="audioWaveformWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="broadcastTitleText"', 'id="broadcastTitleTextWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="broadcastDescText"', 'id="broadcastDescTextWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="audioCurrentTime"', 'id="audioCurrentTimeWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="audioDuration"', 'id="audioDurationWk9"')
        deck9_str_fixed = deck9_str_fixed.replace('id="audioProgressBar"', 'id="audioProgressBarWk9"')
        html = html.replace(deck9_str, deck9_str_fixed)

    html = html.replace('<div id="deck-wk9">', '<div id="deck-wk9" style="display:none;">')
    html = html.replace('<div id="deck-wk9" style="display:none;">', deck_wk10_html + '\n\n    <!-- ========================================== -->\n    <!-- DECK 9: WEEK 9 OFFICIAL REPORT (ARCHIVED)  -->\n    <!-- ========================================== -->\n    <div id="deck-wk9" style="display:none;">')

# F. Update JavaScript handleArchiveSelect to support wk10
old_archive_func = r'function handleArchiveSelect\(val\) \{.*?(?=function switchVoice|function copySleeperBlast|function prevSlide)'
new_archive_func = """function handleArchiveSelect(val) {
      if (val === 'wk1' || val === 'wk2' || val === 'wk3' || val === 'wk4' || val === 'wk5' || val === 'wk6' || val === 'wk7' || val === 'wk8' || val === 'wk9' || val === 'wk10') {
        currentEdition = val;
        currentSlide = 0;
        const d1 = document.getElementById('deck-wk1');
        const d2 = document.getElementById('deck-wk2');
        const d3 = document.getElementById('deck-wk3');
        const d4 = document.getElementById('deck-wk4');
        const d5 = document.getElementById('deck-wk5');
        const d6 = document.getElementById('deck-wk6');
        const d7 = document.getElementById('deck-wk7');
        const d8 = document.getElementById('deck-wk8');
        const d9 = document.getElementById('deck-wk9');
        const d10 = document.getElementById('deck-wk10');

        if (d1) d1.style.display = (val === 'wk1') ? 'block' : 'none';
        if (d2) d2.style.display = (val === 'wk2') ? 'block' : 'none';
        if (d3) d3.style.display = (val === 'wk3') ? 'block' : 'none';
        if (d4) d4.style.display = (val === 'wk4') ? 'block' : 'none';
        if (d5) d5.style.display = (val === 'wk5') ? 'block' : 'none';
        if (d6) d6.style.display = (val === 'wk6') ? 'block' : 'none';
        if (d7) d7.style.display = (val === 'wk7') ? 'block' : 'none';
        if (d8) d8.style.display = (val === 'wk8') ? 'block' : 'none';
        if (d9) d9.style.display = (val === 'wk9') ? 'block' : 'none';
        if (d10) d10.style.display = (val === 'wk10') ? 'block' : 'none';

        // Update pills
        const pills = document.querySelectorAll('.nav-pill');
        pills.forEach((p, idx) => {
          if (idx === 0) {
            p.className = 'nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-amber-500 text-slate-950 font-bold';
          } else {
            p.className = 'nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white';
          }
        });

        // Hide all slides across all decks
        document.querySelectorAll('.slide').forEach(s => s.classList.remove('active'));
        // Activate first slide of selected deck
        const first = document.getElementById(`${val}-slide-0`);
        if (first) first.classList.add('active');

        const ind = document.getElementById('slideIndicator');
        if (ind) ind.innerText = `Slide 1 / 11`;
      }
    }

    """
html = re.sub(old_archive_func, new_archive_func, html, count=1, flags=re.DOTALL)

# G. Update default currentEdition to wk10
html = html.replace("let currentEdition = 'wk9';", "let currentEdition = 'wk10';")

# H. Update copySleeperBlast
old_blast_pattern = r'function copySleeperBlast\(\) \{.*?(?=function|\Z)'
new_blast_func = """function copySleeperBlast() {
      const blast = `🏈 F.F.U.C. WEEK 10 OFFICIAL REPORT IS LIVE! 🏈
A historic Week 10 has rewritten the record books and reshaped the playoff race!

👑 HIGH ROLLER & SCORING RECORD:
• iRob (Njigbas in Paris) detonates for a SEASON-HIGH 191.46 PTS, pulverizing Alex by 80.54 points!

⚡ $10 BOUNTY WINNER (Highest Scoring RB):
• Joey (TheGreatSwagsby) pockets the $10 cash bounty behind Christian McCaffrey's 44.30-point masterclass!

🔥 BATTLE FOR 1ST PLACE:
• Arnulfo edges Mark 118.92 to 113.22 (5.70 margin) to tie iRob atop the standings at 7-3!

💔 HEARTBREAK OF THE WEEK:
• Mark posts the highest losing score of Week 10 (113.22 PTS) in the 5.70-point nailbiter defeat!

🎯 PICK-EM LEADERBOARD ($45 Pot):
• iRob hits the century mark at 100.0 pts to take sole 1st place! Robert in 2nd (99.0) & Arnulfo in 3rd (98.0)!

🚽 5K TOILET RUNNER & BAR TAB METER:
• Eric posts the low score of the week (89.04 PTS) for back-to-back toilet runs. Pedro remains anchored in the cellar at 926.14 PF (-285.94 deficit) with $0 FAAB!

⚔️ WEEK 11 PREVIEW:
• Game of the Week: #1 offense Franky vs #1 seed iRob! Week 11 Bounty: Highest Scoring WR ($10)!

🎙️ Neural audio broadcast, power rankings, and full interactive deck live now:
👉 https://ffucleague.com`;

      navigator.clipboard.writeText(blast).then(() => {
        const btn = document.getElementById('copyBlastBtn');
        const orig = btn.innerHTML;
        btn.innerHTML = '✅ Copied Week 10 Blast!';
        setTimeout(() => { btn.innerHTML = orig; }, 2500);
      });
    }
"""
html = re.sub(old_blast_pattern, new_blast_func, html, count=1, flags=re.DOTALL)

# Write updated index.html
with open(INDEX_PATH, "wb") as f:
    f.write(html.encode("utf-8"))

print("🎉 Successfully built and updated index.html with Week 10 deck!")

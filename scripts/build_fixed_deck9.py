import re, json, os, sys
sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

print("Reading index.html...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------
# 1. NEW NAV PILLS (11 SLIDES FOR WEEK 9)
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
        <button onclick="goToSlide(10)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">11. ⚡ Wk 10 Gameday Hub</button>
      </nav>"""

print("Preparing slide content...")
# -------------------------------------------------------------
# 2. DEFINE SLIDES FOR DECK-WK9
# -------------------------------------------------------------

slide_0 = """      <!-- SLIDE 0: HARDWARE & ROASTS -->
      <section id="wk9-slide-0" class="slide active space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-500/20 via-slate-900 to-yellow-500/10 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL WEEK 9 AWARDS • F.F.U.C. HONORS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏆 Hardware & Weekly Roasts</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 9 scoring crown, $10 highest QB bounty, heartbreaking 122-pt bad beat, and toilet sprint.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-900 border border-amber-500/30 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Post-Midpoint (9 of 14 Weeks)</span>
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
                    🎙️ Official League Voice • Week 9 Recap
                  </span>
                </div>
                <div class="text-white font-extrabold text-sm sm:text-base tracking-tight flex items-center gap-2">
                  <span id="broadcastTitleText">Week 9 Official Audio Recap (Commissioner's Desk)</span>
                  <!-- Animated Waveform Equalizer -->
                  <div id="audioWaveform" class="flex items-end gap-0.5 h-4 opacity-40 transition-opacity">
                    <span class="w-1 bg-amber-400 rounded-full h-2 animate-bounce" style="animation-delay: 0.1s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-4 animate-bounce" style="animation-delay: 0.3s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-3 animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-1 animate-bounce" style="animation-delay: 0.4s"></span>
                  </div>
                </div>
                <div id="broadcastDescText" class="text-xs text-slate-400 mt-0.5">
                  Mark's 137.28 High Roller crown, iRob capturing the $10 QB bounty behind Joe Burrow's 29.54 clinic, Herrador's 122.76 heartbreak loss to Franky, Eric's 86.36 toilet slump, and the three-way tie atop FFUC at 6-3.
                </div>
              </div>
            </div>

            <!-- Right Controls: Progress Bar & Duration -->
            <div class="flex flex-col sm:items-end justify-center gap-1.5 min-w-[200px]">
              <div class="flex items-center justify-between sm:justify-end gap-3 text-xs font-mono w-full">
                <span id="audioCurrentTime" class="text-amber-400 font-bold">0:00</span>
                <span class="text-slate-600">/</span>
                <span id="audioDuration" class="text-slate-400">1:47</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2 border border-slate-800 cursor-pointer overflow-hidden" onclick="seekBroadcastAudio(event)">
                <div id="audioProgressBar" class="bg-gradient-to-r from-amber-500 to-yellow-400 h-full w-0 rounded-full transition-all duration-100"></div>
              </div>
              <span class="text-[10px] text-slate-500 font-mono">Natural Voice Broadcast • Click to stream</span>
            </div>
          </div>
          <!-- Audio Element -->
          <audio id="broadcastAudio" src="assets/audio/wk9_recap.mp3" preload="metadata" ontimeupdate="updateBroadcastProgress()" onended="onBroadcastAudioEnded()"></audio>
        </div>

        <!-- AWARDS GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Award 1: High Roller Champion (Mark) -->
          <div class="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border-2 border-amber-500/60 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-amber-500 text-slate-950 px-2.5 py-0.5 rounded">👑 Week 9 High Roller Champion</span>
              <span class="text-xl font-athletic font-bold text-amber-400">137.28 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">Saquon Deez Nacuas <span class="text-amber-400 text-sm font-semibold">(Mark)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Mark puts on an absolute clinic in Week 9, detonating for 137.28 points to take the scoring title and crush Pedro 137.28 to 104.18! Powered by Puka Nacua (28.00) in his signature alpha performance, alongside Jalen Hurts (20.40), Matthew Stafford (19.50), Jayden Reed (17.20), Cam Little (17.00), and Kyle Pitts (7.80), Mark captures his first High Roller crown of 2026 and forces a three-way tie atop the league at 6-3!
            </p>
            <!-- FaceFusion AI High Roller Video / GIF -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-amber-500/40 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-amber-500/40 text-[9px] font-mono font-bold text-amber-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                FaceFusion AI • Mark Billionaire Vince Strut (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/mark_high_roller.gif">
                <source src="assets/video/mark_high_roller.mp4" type="video/mp4">
                <img src="assets/video/mark_high_roller.gif" alt="Mark High Roller Vince McMahon Strut" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Week 9 High Score: 137.28 PTS</span>
              <span class="text-amber-400 font-bold font-mono">Scoring Crown • 6-3 Record</span>
            </div>
          </div>

          <!-- Award 2: $10 Bounty Winner (Highest Scoring QB) -->
          <div class="bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-emerald-500 text-slate-950 px-2.5 py-0.5 rounded">⚡ $10 Weekly Bounty: Highest Scoring QB</span>
              <span class="text-xl font-athletic font-bold text-emerald-400">29.54 PTS (Joe Burrow)</span>
            </div>
            <h3 class="text-xl font-black text-white">Njigbas in Paris <span class="text-emerald-400 text-sm font-semibold">(iRob)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Show me the money! iRob secures the Week 9 $10 cash bounty behind Joe Burrow's 29.54-point aerial destruction of the Raiders defense! Burrow tossed 5 touchdown passes in an unstoppable performance, narrowly beating out Drake Maye (21.26) and Jalen Hurts (20.40) to bank the $10 cash prize and maintain his share of 1st place in the standings!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Joe Burrow: 29.54 PTS (5 Passing TDs)</span>
              <span class="text-emerald-400 font-bold font-mono">iRob: $10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 3: Heartbreak Bad Beat (Herrador) -->
          <div class="bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-900 border border-rose-500/40 rounded-2xl p-5 shadow-xl">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-bold uppercase tracking-wider bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-0.5 rounded">💔 Heartbreak of the Week</span>
              <span class="text-lg font-athletic font-bold text-rose-400">122.76 PTS (L)</span>
            </div>
            <h3 class="text-xl font-black text-white">Brock To The Future <span class="text-rose-400 text-sm font-semibold">(Herrador)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Utter schedule agony! One week after hoisting the High Roller crown, Herrador dropped 122.76 points—the 4th highest total across the entire league—backed by Bucky Irving (26.50), Ja'Marr Chase (26.50), and Brock Bowers (18.80)! Herrador would have comfortably defeated 6 of the other 8 franchises, but ran directly into Franky's 136.46 scoring barrage to suffer a heartbreaking 13.70-point defeat!
            </p>
            <!-- FaceFusion AI Heartbreak Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-rose-500/40 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-rose-500/40 text-[9px] font-mono font-bold text-rose-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
                FaceFusion AI Video • Herrador Peter Parker Crying (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/herrador_heartbreak.gif">
                <source src="assets/video/herrador_heartbreak.mp4" type="video/mp4">
                <img src="assets/video/herrador_heartbreak.gif" alt="Herrador Peter Parker Crying Meme" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Defeated by: Franky (136.46 PTS)</span>
              <span class="text-rose-400 font-bold font-mono">4th Highest Score in League</span>
            </div>
          </div>

          <!-- Award 4: 5K Toilet Runner: Cellar Shock (Eric) -->
          <div class="bg-gradient-to-br from-red-950/40 via-slate-900 to-slate-900 border-2 border-red-600/70 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-red-600 text-white px-2.5 py-0.5 rounded shadow">🚽 5K Toilet Runner: Low Score of Week</span>
              <span class="text-lg font-athletic font-bold text-red-400">86.36 PTS (-12.98)</span>
            </div>
            <h3 class="text-xl font-black text-white">Show me dem TDs <span class="text-red-400 text-sm font-semibold">(Eric)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              <strong class="text-red-400">THE WEEK 9 SLUMP:</strong> Eric went ice-cold in Week 9, managing just 86.36 points in a 12.98-point loss to Alex (99.34). With zero players topping 18 points and duds from Jonathan Taylor (6.90), Dylan Sampson (6.30), Sam LaPorta (5.20), and Keenan Allen (4.60), Eric drops to 4-5 and earns this week's 5K Toilet Sprint! Meanwhile, Pedro's loss keeps Pedro anchored in the season-long cellar at 814.46 PF.
            </p>
            <!-- 5K Runner Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950 flex items-center justify-center min-h-[256px] sm:min-h-[288px]">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                FaceFusion AI • Eric Frankie LaPenna Power Sprint (Screened by Qwen3-VL 32B)
              </div>
              <video class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto" autoplay loop muted playsinline poster="assets/video/eric_toilet_runner.gif">
                <source src="assets/video/eric_toilet_runner.mp4" type="video/mp4">
                <img src="assets/video/eric_toilet_runner.gif" alt="Eric 5K Toilet Runner Meme" class="w-full h-64 sm:h-72 object-contain bg-slate-950 mx-auto">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-red-400 font-mono font-bold">Week 9 Low Score: 86.36 PTS</span>
              <span class="text-red-400 font-bold font-mono">Record: 4-5 • Logjam Alert</span>
            </div>
          </div>
        </div>
      </section>"""


# SLIDE 1: STATE OF THE UNION & STANDINGS
slide_1 = """      <!-- SLIDE 1: STATE OF THE UNION -->
      <section id="wk9-slide-1" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 9 LEAGUE AUDIT • COMMISSIONER'S DESK
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏛️ State of the Union: Week 9</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">3-way championship deadlock at 6-3, Joey alone in 4th at 5-4, 4-way wild-card dogfight at 4-5, and cellar danger at 3-6.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-blue-400 font-mono font-bold px-3 py-1 rounded-lg">9 of 14 Complete (64%)</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">👑 3-Way Championship Deadlock (6-3)</span>
            <div class="text-base font-bold text-white mt-1">iRob, Mark, & Arnulfo at the Summit</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Total parity atop FFUC! iRob (1,110.40 PF) clings to the #1 tiebreaker by just 3.36 points over Mark (1,107.04 PF), while Arnulfo (1,095.24 PF) sits tied in 3rd. Mark faces Arnulfo head-to-head in Week 10!
            </p>
          </div>

          <div class="bg-slate-900 border border-blue-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-400">🎯 Joey Takes Solo 4th (5-4)</span>
            <div class="text-base font-bold text-white mt-1">TheGreatSwagsby Topples #1 Seed</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Joey (1,103.64 PF) pulled off the upset of the week, defeating iRob 121.24 to 113.14 behind Kenneth Walker's 34.30 nuclear show! Joey now holds sole possession of playoff seed #4.
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">🔥 4-Way Wild-Card Mosh Pit (4-5)</span>
            <div class="text-base font-bold text-white mt-1">Franky, Herrador, Alex, & Eric Deadlocked</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Four squads are fighting for their postseason lives! Franky boasts the #1 scoring attack in the entire league (1,193.26 PF) but is 4-5 alongside Herrador (1,157.56 PF), Alex (1,146.88 PF), and Eric (1,035.08 PF).
            </p>
          </div>
        </div>

        <!-- Standings Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Official Sleeper Standings Through Week 9</span>
            <span class="font-mono text-blue-400 font-bold">14-Week Regular Season</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/30">
              <span class="w-8 font-bold text-emerald-400">1</span>
              <span class="flex-1 font-bold text-white">Njigbas in Paris (iRob) <span class="text-emerald-400 font-bold text-[10px]">#1 Seed Tiebreaker</span></span>
              <span class="w-16 text-center text-emerald-400 font-bold">6-3</span>
              <span class="w-20 text-right text-emerald-400 font-bold">1110.40 PF</span>
              <span class="w-20 text-right text-slate-500">1092.54 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$55</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-8 font-bold text-emerald-400">2</span>
              <span class="flex-1 font-bold text-white">Saquon Deez Nacuas (Mark) <span class="text-amber-400 font-bold text-[10px]">👑 High Roller</span></span>
              <span class="w-16 text-center text-emerald-400 font-bold">6-3</span>
              <span class="w-20 text-right text-slate-200 font-bold">1107.04 PF</span>
              <span class="w-20 text-right text-slate-500">1020.38 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$72</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-8 font-bold text-emerald-400">3</span>
              <span class="flex-1 font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">6-3</span>
              <span class="w-20 text-right text-slate-300">1095.24 PF</span>
              <span class="w-20 text-right text-slate-500">1087.96 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$10</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-blue-950/20">
              <span class="w-8 font-bold text-blue-400">4</span>
              <span class="flex-1 font-semibold text-slate-200">TheGreatSwagsby (Joey)</span>
              <span class="w-16 text-center text-blue-400 font-bold">5-4</span>
              <span class="w-20 text-right text-slate-300">1103.64 PF</span>
              <span class="w-20 text-right text-slate-500">1036.16 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$15</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">5</span>
              <span class="flex-1 text-slate-300">CULT OF THE LAMB (Franky) <span class="text-amber-400 font-bold text-[10px]">#1 PF in FFUC</span></span>
              <span class="w-16 text-center text-slate-300 font-bold">4-5</span>
              <span class="w-20 text-right text-amber-400 font-extrabold">1193.26 PF</span>
              <span class="w-20 text-right text-slate-500">1194.38 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$13</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">6</span>
              <span class="flex-1 text-slate-300">Brock To The Future (Herrador)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-5</span>
              <span class="w-20 text-right text-slate-300">1157.56 PF</span>
              <span class="w-20 text-right text-slate-500">1122.52 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$49</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">7</span>
              <span class="flex-1 text-slate-300">League Median Advocate 🗳 (Alex)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-5</span>
              <span class="w-20 text-right text-slate-300">1146.88 PF</span>
              <span class="w-20 text-right text-slate-500">1119.08 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$28</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">8</span>
              <span class="flex-1 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-16 text-center text-slate-300 font-bold">4-5</span>
              <span class="w-20 text-right text-slate-300">1035.08 PF</span>
              <span class="w-20 text-right text-slate-500">1021.22 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$49</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-8 font-bold text-rose-400">9</span>
              <span class="flex-1 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-6</span>
              <span class="w-20 text-right text-slate-300">1106.96 PF</span>
              <span class="w-20 text-right text-slate-500">1078.18 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$83</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-red-950/30">
              <span class="w-8 font-bold text-red-500">10</span>
              <span class="flex-1 font-medium text-red-400">I Didn’t Hear No Bell (Pedro) <span class="text-red-500 text-[10px] font-bold">(-292.50 PF Deficit)</span></span>
              <span class="w-16 text-center text-red-500 font-bold">3-6</span>
              <span class="w-20 text-right text-red-400 font-extrabold">814.46 PF</span>
              <span class="w-20 text-right text-slate-500">1098.10 PA</span>
              <span class="w-16 text-right text-red-500 font-black">$0</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 2: $10 BOUNTY BOARD
slide_2 = """      <!-- SLIDE 2: $10 BOUNTY BOARD -->
      <section id="wk9-slide-2" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-green-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEKLY PRIZE POOL • DIRECT CASH PAYOUTS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💵 $10 Weekly Bounty Board</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 9 Highest Scoring QB crowned; Week 10 Highest Scoring RB on deck.</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-emerald-400">$140.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Season Bounty Pot ($90 Paid)</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Week 9 Winner Card (iRob) -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-emerald-500 text-slate-950 text-xs font-extrabold px-3 py-1 rounded-bl-xl shadow">
              Bounty Collected ($10)
            </div>
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">Week 9 Target: Highest Scoring QB ($10)</span>
              <h3 class="text-2xl font-black text-white mt-1">iRob • 29.54 PTS (Joe Burrow)</h3>
              <div class="text-xs text-slate-400 mt-0.5">Franchise: <strong class="text-slate-200">Njigbas in Paris</strong></div>

              <div class="my-4 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl space-y-2">
                <div class="text-xs text-emerald-300 font-semibold">⚡ Joe Burrow's 5-Touchdown Aerial Clinic:</div>
                <div class="text-xs text-slate-300 leading-relaxed">
                  Joe Burrow shredded the Raiders secondary for 251 yards and 5 touchdowns, putting up 29.54 fantasy points to deliver iRob his first cash bounty of the season! Burrow's masterclass held off strong challenges from Drake Maye (21.26 PTS) and Jalen Hurts (20.40 PTS).
                </div>
              </div>

              <!-- Top 5 Starting QBs in Week 9 -->
              <div class="space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-emerald-500/40">
                  <span class="font-bold text-emerald-400">1. Joe Burrow (iRob)</span>
                  <span class="font-black text-white">29.54 PTS (WON $10)</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>2. Drake Maye (Alex)</span>
                  <span class="font-bold text-amber-400">21.26 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>3. Jalen Hurts (Mark)</span>
                  <span>20.40 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>4. Matthew Stafford (Mark)</span>
                  <span>19.50 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>5. Caleb Williams (Franky)</span>
                  <span>16.76 PTS</span>
                </div>
              </div>
              <div class="mt-2 text-[10px] text-slate-500 font-mono italic">
                *Note: Jordan Love posted 36.18 PTS on Alex's bench. Under official FFUC rules, only active starters are eligible for position bounties.
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Payout Method: League Safe / Direct</span>
              <span class="text-emerald-400 font-bold">$10.00 Sent to iRob</span>
            </div>
          </div>

          <!-- Season Bounty Schedule & Leaderboard -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400">2026 Bounty Master Schedule</span>
              <h3 class="text-xl font-black text-white mt-1">9 of 14 Bounties Claimed ($90.00 Paid)</h3>

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
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>Wk 8: Largest Blowout</span>
                  <span class="text-emerald-400 font-bold">Mark (45.38 Margin) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-emerald-950/30 px-2 rounded border border-emerald-500/30 text-white">
                  <span class="font-bold">Wk 9: Highest Scoring QB</span>
                  <span class="text-emerald-400 font-bold">iRob (Burrow 29.54) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-amber-950/30 px-2 rounded border border-amber-500/30 text-amber-300">
                  <span class="font-bold">Wk 10: Highest Scoring RB</span>
                  <span class="text-amber-400 font-bold">🔒 Up for Grabs ($10)</span>
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
              <span>Next Target: Week 10 Highest Scoring RB</span>
              <span class="text-amber-400 font-bold">$10.00 Target</span>
            </div>
          </div>
        </div>
      </section>"""


# SLIDE 3: THE BAR TAB & 5K TOILET METER
slide_3 = """      <!-- SLIDE 3: THE BAR TAB & 5K TOILET METER -->
      <section id="wk9-slide-3" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-red-950/80 via-slate-900 to-rose-950/80 border border-red-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-red-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              THE LAST PLACE PUNISHMENT WATCH • THE TOILET RUN
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍻 The Bar Tab & 5K Toilet Meter</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Live tracking of the FFUC Last Place in-person 5K Run and open bar tab liability.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-red-400 font-mono font-bold px-3 py-1 rounded-lg">Critical Risk: Pedro (3-6, 814.46 PF, $0 FAAB)</span>
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
                <span class="text-lg font-athletic font-bold text-red-400">3-6 • 814.46 PF</span>
              </div>
              <h3 class="text-2xl font-black text-white">I Didn’t Hear No Bell <span class="text-red-400 text-sm font-semibold">(Pedro)</span></h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                <strong class="text-red-400">CELLAR LOCK DEEPENS:</strong> Pedro suffered a 33.10-point blowout against Mark (137.28 to 104.18). Despite receiving a 27.40-point spark from Matthew Golden, Pedro sits at 814.46 total points, trailing 9th-place Robert by a staggering <strong>292.50 points</strong>! With $0 in FAAB remaining and the lowest scoring roster in FFUC, Pedro is in extreme danger of having to lace up his sneakers for the 5K run and fund the league's open bar tab!
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
                  <span class="font-mono font-bold text-amber-400">$290.00 Est.</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Distance to 9th Place Safety:</span>
                  <span class="font-mono font-bold text-red-400">292.50 Total Points Deficit</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Punishment Likelihood:</span>
              <span class="text-red-400 font-bold uppercase">94.5% Implied Probability</span>
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
                    <span class="block text-red-400 text-[11px]">3-6 • 814.46 PF • $0 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-red-400 font-extrabold">94.5% Risk</span>
                    <span class="block text-slate-500 text-[10px]">Anchor</span>
                  </div>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-slate-300">Robert (WE NOT GOIN’ BACK 2 BACK)</span>
                    <span class="block text-slate-400 text-[11px]">3-6 • 1106.96 PF • $83 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-amber-400 font-bold">4.5% Risk</span>
                    <span class="block text-slate-500 text-[10px]">+292.50 PF Buffer</span>
                  </div>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-slate-300">Eric (Show me dem TDs)</span>
                    <span class="block text-slate-400 text-[11px]">4-5 • 1035.08 PF • $49 FAAB</span>
                  </div>
                  <div class="text-right font-mono">
                    <span class="text-slate-400 font-bold">1.0% Risk</span>
                    <span class="block text-slate-500 text-[10px]">+220.62 PF Buffer</span>
                  </div>
                </div>

                <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                  <div>
                    <span class="font-bold text-slate-400">Alex, Herrador, Franky, Joey</span>
                    <span class="block text-slate-500 text-[11px]">4-5 / 5-4 • 1100+ PF</span>
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
      <section id="wk9-slide-4" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-purple-950/80 via-slate-900 to-indigo-950/80 border border-purple-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-purple-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ADVANCED ANALYTICS • ALL-PLAY CORRELATION
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍀 The Luck Index: Schedule Variance</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Expected Wins vs Actual Wins across 81 total all-play matchups per franchise through Week 9.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-purple-400 font-mono font-bold px-3 py-1 rounded-lg">81 Total Games Audited</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">🍀 The Luckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Pedro (+1.56) & Arnulfo (+1.33) & iRob (+1.22)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Pedro has captured 3 wins despite a 13-68 all-play record (expected 1.44 wins), keeping him as the league's most fortunate team. Arnulfo sits at 6-3 with an expected 4.67 wins (+1.33), while iRob holds 1st place with an expected 4.78 wins (+1.22).
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">💀 The Unluckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Franky (-1.78) & Herrador (-1.56) & Robert (-1.11)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Absolute statistical highway robbery! Franky leads FFUC in scoring (1,193.26 PF) and all-play wins (52-29), yet sits at 4-5 (-1.78 luck). Herrador is #2 in all-play (50-31) and scoring (1,157.56 PF) but also sits at 4-5 (-1.56 luck)!
            </p>
          </div>
        </div>

        <!-- Luck Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">All-Play Luck Matrix (Week 9 Audited)</span>
            <span class="font-mono text-purple-400 font-bold">Luck Delta = Actual Wins - Expected Wins</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/25">
              <span class="w-48 font-bold text-white">I Didn’t Hear No Bell (Pedro)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">3-6 (Act)</span>
              <span class="w-20 text-center text-slate-400">1.44 (Exp)</span>
              <span class="w-28 text-center text-red-400">13-68 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.56 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-48 font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">6-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.67 (Exp)</span>
              <span class="w-28 text-center text-slate-300">42-39 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.33 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-48 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">6-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">43-38 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.22 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-48 font-bold text-white">Saquon Deez Nacuas (Mark)</span>
              <span class="w-20 text-center text-blue-400 font-bold">6-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.11 (Exp)</span>
              <span class="w-28 text-center text-slate-300">46-35 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+0.89 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-20 text-center text-slate-300 font-bold">4-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">32-49 All-Play</span>
              <span class="w-24 text-right text-slate-300">+0.44 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">TheGreatSwagsby (Joey)</span>
              <span class="w-20 text-center text-slate-300 font-bold">5-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.11 (Exp)</span>
              <span class="w-28 text-center text-slate-300">46-35 All-Play</span>
              <span class="w-24 text-right text-slate-300">-0.11 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-48 text-slate-300">League Median Advocate 🗳 (Alex)</span>
              <span class="w-20 text-center text-rose-400 font-bold">4-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.89 (Exp)</span>
              <span class="w-28 text-center text-slate-300">44-37 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.89 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/15">
              <span class="w-48 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-6 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.11 (Exp)</span>
              <span class="w-28 text-center text-slate-300">37-44 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.11 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-48 font-bold text-white">Brock To The Future (Herrador)</span>
              <span class="w-20 text-center text-rose-400 font-bold">4-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">50-31 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.56 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/30">
              <span class="w-48 font-bold text-white">CULT OF THE LAMB (Franky)</span>
              <span class="w-20 text-center text-rose-400 font-bold">4-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">5.78 (Exp)</span>
              <span class="w-28 text-center text-amber-400 font-extrabold">52-29 All-Play (1st)</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.78 💀</span>
            </div>
          </div>
        </div>
      </section>"""


# SLIDE 5: POWER RANKINGS
slide_5 = """      <!-- SLIDE 5: POWER RANKINGS -->
      <section id="wk9-slide-5" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-orange-950/80 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ANALYTIC POWER INDEX • STRENGTH OF SQUAD
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">📈 Power Rankings: Week 9</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">True hierarchy based on roster firepower, all-play strength, and momentum entering Week 10.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 9 Audited</span>
          </div>
        </div>

        <div class="space-y-2 text-xs">
          <!-- Rank 1: Mark -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">1</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +3 (6-3) • 224.2 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1107.04 PF. Captures the Week 9 High Roller crown with a commanding 137.28 PTS! Puka Nacua (28.00), Jalen Hurts (20.40), and Matthew Stafford (19.50) are firing at peak efficiency as Mark marches into a massive #1 vs #2 showdown against Arnulfo.
              </p>
            </div>
          </div>

          <!-- Rank 2: iRob -->
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-emerald-400">2</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Njigbas in Paris (iRob)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -1 (6-3) • 220.1 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1110.40 PF. Slipped in an upset to Joey (113.14 to 121.24) but Joe Burrow delivered a $10 bounty-winning 29.54 clinic. Holding the #1 seed tiebreaker by 3.36 points, iRob remains a top-tier title favorite.
              </p>
            </div>
          </div>

          <!-- Rank 3: Franky -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">3</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">CULT OF THE LAMB (Franky)</span>
                <span class="text-slate-400 font-mono font-bold">― 0 (4-5) • 218.5 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1193.26 PF (#1 in scoring, #1 in all-play 52-29). Detonated for 136.46 PTS to down Herrador. CeeDee Lamb (28.50) and James Cook (16.70) lead a powerhouse roster that is severely under-seeded at 4-5.
              </p>
            </div>
          </div>

          <!-- Rank 4: Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-blue-400">4</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">MyDakMakesHerWaddle (Arnulfo)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +2 (6-3) • 214.8 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1095.24 PF. Gritted out a 118.40-112.00 victory over Robert despite Josh Jacobs exiting with 0.50 PTS and zero defense points. Christian Watson (26.60) sparked the win to keep Arnulfo tied atop FFUC at 6-3.
              </p>
            </div>
          </div>

          <!-- Rank 5: Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">5</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">TheGreatSwagsby (Joey)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +2 (5-4) • 212.0 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1103.64 PF. Statement victory over #1 iRob (121.24 to 113.14)! Kenneth Walker (34.30) and CMC (21.70) formed a lethal backfield combo, elevating Joey into sole 4th place.
              </p>
            </div>
          </div>

          <!-- Rank 6: Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">6</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Brock To The Future (Herrador)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -4 (4-5) • 208.6 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1157.56 PF (#2 in scoring, 50-31 all-play). Heartbreak loss to Franky despite 122.76 PTS! Ja'Marr Chase (26.50), Bucky Irving (26.50), and Brock Bowers (18.80) give Herrador supreme ceiling.
              </p>
            </div>
          </div>

          <!-- Rank 7: Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">7</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">League Median Advocate 🗳 (Alex)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -2 (4-5) • 204.3 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1146.88 PF (#3 in scoring, 44-37 all-play). Ground out a 99.34-86.36 win over Eric with Drake Maye (21.26). Left Jordan Love (36.18) on the bench but enters Week 10 in the playoff hunt.
              </p>
            </div>
          </div>

          <!-- Rank 8: Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">8</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (3-6) • 196.4 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1106.96 PF. Dropped a narrow 112.00-118.40 decision to Arnulfo. Lamar Jackson bounced back with 23.70 PTS. Armed with $83 in FAAB, Robert is positioned to make a late playoff push.
              </p>
            </div>
          </div>

          <!-- Rank 9: Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-500">9</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Show me dem TDs (Eric)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -1 (4-5) • 188.7 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                1035.08 PF. Slumped to low score of the week with 86.36 PTS. Tee Higgins (17.70) and Josh Allen (13.86) couldn't save Eric from the Week 9 Toilet Runner title.
              </p>
            </div>
          </div>

          <!-- Rank 10: Pedro -->
          <div class="bg-slate-900 border-2 border-red-600/70 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-red-500">10</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-red-400 text-sm">I Didn’t Hear No Bell (Pedro)</span>
                <span class="text-slate-400 font-mono font-bold">― 0 (3-6) • 162.0 Pwr</span>
              </div>
              <p class="text-slate-400 mt-1 leading-relaxed">
                814.46 PF. Blown out by Mark (104.18 to 137.28). Trails 9th place by -292.50 PF with $0 FAAB in reserve. Firmly in the 5K toilet sprint crosshairs.
              </p>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 6: FAAB RECEIPTS
slide_6 = """      <!-- SLIDE 6: FAAB RECEIPTS -->
      <section id="wk9-slide-6" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-teal-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              FINANCIAL AUDIT • WAIVER TRANSACTION WIRE
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💰 FAAB Receipts: Week 9 Ledger</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official transaction ledger and updated bankrolls through Week 9 waivers.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">Budget Cap: $100 FAAB</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Recent Key Transactions -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded">
              Week 9 Key Wire Pickups
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <strong class="text-white">Ty Johnson (RB • BUF)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark) — Depth reinforcement</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Mike Gesicki (TE • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro) — Starting TE</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-300 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Audric Estime (RB • DEN)</strong>
                  <span class="block text-slate-400 text-[11px]">League Median Advocate 🗳 (Alex) — Bench stash</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-300 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Nick Folk (K • TEN)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky) — Kicker rotation</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-300 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Nick Westbrook-Ikhine (WR • TEN)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro) — WR Wire add</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-300 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>
            </div>

            <div class="mt-3.5 pt-3 border-t border-slate-800 text-[11px] text-slate-400">
              ⚡ <strong>19 total waiver transactions</strong> completed across Week 9. Free agent maneuvering dominated with $0 bids preserving critical playoff budgets.
            </div>
          </div>

          <!-- FAAB Leaderboard -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 bg-amber-950 border border-amber-800 px-2.5 py-0.5 rounded">
                Remaining FAAB War Chests
              </span>
              <div class="mt-3 divide-y divide-slate-800/80 text-xs font-mono">
                <div class="py-1.5 flex justify-between items-center text-slate-200">
                  <span>1. Robert (WE NOT GOIN’ BACK 2 BACK)</span>
                  <span class="text-emerald-400 font-bold">$83 (83%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-200">
                  <span>2. Mark (Saquon Deez Nacuas)</span>
                  <span class="text-emerald-400 font-bold">$72 (72%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-300">
                  <span>3. iRob (Njigbas in Paris)</span>
                  <span class="text-emerald-400 font-bold">$55 (55%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-300">
                  <span>4. Herrador (Brock To The Future)</span>
                  <span class="text-slate-300 font-bold">$49 (49%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-300">
                  <span>5. Eric (Show me dem TDs)</span>
                  <span class="text-slate-300 font-bold">$49 (49%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>6. Alex (League Median Advocate 🗳)</span>
                  <span class="text-slate-300 font-bold">$28 (28%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>7. Joey (TheGreatSwagsby)</span>
                  <span class="text-amber-400 font-bold">$15 (15%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-400">
                  <span>8. Franky (CULT OF THE LAMB)</span>
                  <span class="text-amber-400 font-bold">$13 (13%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-slate-500">
                  <span>9. Arnulfo (MyDakMakesHerWaddle)</span>
                  <span class="text-red-400 font-bold">$10 (10%)</span>
                </div>
                <div class="py-1.5 flex justify-between items-center text-red-400 bg-red-950/20 px-2 rounded">
                  <span class="font-bold">10. Pedro (I Didn’t Hear No Bell)</span>
                  <span class="font-black text-red-500">$0 (0% - Bankrupt)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>League Bankroll Leader:</span>
              <span class="text-emerald-400 font-bold">Robert ($83 FAAB)</span>
            </div>
          </div>
        </div>
      </section>"""


# SLIDE 7: PICK-EM LEADERBOARD
slide_7 = """      <!-- SLIDE 7: PICK-EM LEADERBOARD -->
      <section id="wk9-slide-7" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-cyan-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL SLEEPER PICK-EM POOL • $45 CASH POT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🎯 F.F.U.C. Pick-em Leaderboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Arnulfo erupts for league-high 15-win week to tie Robert for 1st place at 90.0 PTS; iRob stalks at 89.0!</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-blue-400">$45.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Winner Takes All Pot</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border-2 border-amber-500/50 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-400">🥇 1st Place Deadlock</span>
            <div class="text-base font-bold text-white mt-1">Arnulfo & Robert (90.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Arnulfo went a blistering 15-1 in NFL Week 9 to completely erase Robert's lead! Both managers are deadlocked atop the $45 pot heading into Week 10!
            </p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300">🥈 3rd Place Stalker</span>
            <div class="text-base font-bold text-white mt-1">iRob (89.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob posted 14 correct picks in Week 9, sitting just 1 single point off the lead with 5 weeks remaining in the regular season!
            </p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">⚡ Week 9 MVP Picker</span>
            <div class="text-base font-bold text-white mt-1">Arnulfo (15-1 Week • 15.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Arnulfo posted the highest single-week pick-em score in FFUC history this season with 15 correct picks to seize a share of 1st place!
            </p>
          </div>
        </div>

        <!-- Official Pick-em Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Certified Sleeper Standings Through Week 9</span>
            <span class="font-mono text-blue-400 font-bold">Total Correct Picks • W9 Score</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-amber-950/30">
              <span class="w-8 font-bold text-amber-400">1</span>
              <span class="flex-1 font-bold text-white">Arnulfo (AEscamilla94) <span class="text-emerald-400 font-bold text-[10px]">W9 High (15)</span></span>
              <span class="w-24 text-center text-emerald-400 font-bold">W9: 15.0 PTS</span>
              <span class="w-28 text-right text-amber-400 font-extrabold text-sm">90.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-amber-950/20">
              <span class="w-8 font-bold text-amber-400">2</span>
              <span class="flex-1 font-bold text-white">Robert (YaBoyRoZ)</span>
              <span class="w-24 text-center text-slate-400">W9: 13.0 PTS</span>
              <span class="w-28 text-right text-amber-400 font-extrabold text-sm">90.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">3</span>
              <span class="flex-1 font-semibold text-slate-200">iRob (irobgarza16)</span>
              <span class="w-24 text-center text-slate-400">W9: 14.0 PTS</span>
              <span class="w-28 text-right text-emerald-400 font-bold">89.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">4</span>
              <span class="flex-1 text-slate-300">Herrador (DirtyDirties)</span>
              <span class="w-24 text-center text-slate-400">W9: 12.0 PTS</span>
              <span class="w-28 text-right text-slate-300">86.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">5</span>
              <span class="flex-1 text-slate-300">Franky (ChanciscoFravez)</span>
              <span class="w-24 text-center text-slate-400">W9: 14.0 PTS</span>
              <span class="w-28 text-right text-slate-300">85.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">6</span>
              <span class="flex-1 text-slate-300">Mark (fattymcfatty)</span>
              <span class="w-24 text-center text-slate-400">W9: 12.0 PTS</span>
              <span class="w-28 text-right text-slate-300">84.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">7</span>
              <span class="flex-1 text-slate-300">Pedro (GuyNamedPedro)</span>
              <span class="w-24 text-center text-slate-400">W9: 14.0 PTS</span>
              <span class="w-28 text-right text-slate-300">84.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">8</span>
              <span class="flex-1 text-slate-300">Alex (abarrera731)</span>
              <span class="w-24 text-center text-slate-400">W9: 12.0 PTS</span>
              <span class="w-28 text-right text-slate-300">84.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">9</span>
              <span class="flex-1 text-slate-300">Eric (emedina13)</span>
              <span class="w-24 text-center text-slate-400">W9: 12.0 PTS</span>
              <span class="w-28 text-right text-slate-400">82.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-500">10</span>
              <span class="flex-1 text-slate-400">Joey (TheGreatSwagsby)</span>
              <span class="w-24 text-center text-slate-400">W9: 12.0 PTS</span>
              <span class="w-28 text-right text-slate-500">81.0 PTS</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 8: BOOMS & BUSTS
slide_8 = """      <!-- SLIDE 8: BOOMS & BUSTS -->
      <section id="wk9-slide-8" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-orange-950/80 via-slate-900 to-amber-950/80 border border-orange-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-orange-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              STATISTICAL ANOMALIES • HEROES & ZEROES
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💥 Booms & Busts: Week 9 Outliers</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Kenneth Walker's 34-point takeover, Jordan Love's bench eruption, and starter goose eggs.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-orange-400 font-mono font-bold px-3 py-1 rounded-lg">Performance Extremes</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- The Booms Card -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded">
              🚀 Week 9 Nuclear Booms
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-amber-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jordan Love (QB • GB)</strong>
                  <span class="block text-slate-400 text-[11px]">League Median Advocate 🗳 (Alex) • League High Score!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-amber-400 font-extrabold text-sm">36.18 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Bench</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Kenneth Walker (RB • SEA)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey) • Carried Joey over #1 iRob</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-extrabold text-sm">34.30 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Joe Burrow (QB • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">Njigbas in Paris (iRob) • $10 QB Bounty Winner (5 TDs)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-extrabold text-sm">29.54 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">CeeDee Lamb (WR • DAL)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky) • Dominant WR1 burst</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">28.50 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Puka Nacua (WR • LAR)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark) • Crowned Week 9 High Roller</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">28.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Matthew Golden (WR • GB)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro) • Breakout game</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">27.40 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>
            </div>
          </div>

          <!-- The Busts Card -->
          <div class="bg-slate-900 border-2 border-red-500/50 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-red-400 bg-red-950 border border-red-800 px-2.5 py-0.5 rounded">
              📉 Week 9 Costly Duds
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-red-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Ladd McConkey (WR • LAC)</strong>
                  <span class="block text-slate-400 text-[11px]">League Median Advocate 🗳 (Alex) • Zero targets, complete blank</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-500 font-extrabold text-sm">0.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-red-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Josh Jacobs (RB • GB)</strong>
                  <span class="block text-slate-400 text-[11px]">MyDakMakesHerWaddle (Arnulfo) • Early ankle injury exit</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-extrabold text-sm">0.50 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tucker Kraft (TE • GB)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey) • 1 catch for 4 yards</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">1.40 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Mike Gesicki (TE • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro) • Target drought</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">2.10 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jaylen Waddle (WR • DEN)</strong>
                  <span class="block text-slate-400 text-[11px]">Njigbas in Paris (iRob) • Sputtering offense</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">2.70 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Chad Ryland (K • ARI)</strong>
                  <span class="block text-slate-400 text-[11px]">Brock To The Future (Herrador) • Costly miss in heartbreak loss</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">3.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""


# SLIDE 9: SCOREBOARD
slide_9 = """      <!-- SLIDE 9: SCOREBOARD -->
      <section id="wk9-slide-9" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-indigo-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL BOX SCORES • SLEEPER API AUDIT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚔️ Week 9 Scoreboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official final box scores, margins of victory, and starter summaries for all 5 matchups.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-indigo-400 font-mono font-bold px-3 py-1 rounded-lg">5 Completed Matchups</span>
          </div>
        </div>

        <div class="space-y-3">
          <!-- Matchup 1: Mark vs Pedro (High Roller + Blowout) -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-amber-400 bg-amber-950/50 border border-amber-800 px-2 py-0.5 rounded">
                👑 Matchup 1 • High Roller Coronation (+33.10 Margin)
              </span>
              <span class="text-xs font-mono text-amber-400 font-bold">Mark Takes Week 9 High Roller</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-amber-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                  <span class="text-amber-400 font-athletic text-lg font-black">137.28 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Puka Nacua (28.00), Javonte Williams (20.40), Matthew Stafford (19.50), Luther Burden (17.20), Cam Little (17.00), Patrick Mahomes (16.48), Jacksonville DEF (11.00), Saquon Barkley (8.20), George Kittle (7.80), Rashee Rice (7.40).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-red-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">I Didn’t Hear No Bell (Pedro)</span>
                  <span class="text-slate-400 font-athletic text-lg font-black">104.18 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Matthew Golden (27.40), Chicago DEF (15.00), Trevor Lawrence (13.58), Denzel Boston (12.80), Chris Rodriguez (10.20), Brandon Aubrey (9.00), Alvin Kamara (6.40), Ashton Jeanty (4.50), Brenton Strange (3.20), Mike Gesicki (2.10).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 2: Franky vs Herrador (Heartbreak) -->
          <div class="bg-slate-900 border-2 border-emerald-500/60 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-emerald-400 bg-emerald-950/50 border border-emerald-800 px-2 py-0.5 rounded">
                ⚡ Matchup 2 • Offensive Fireworks (+13.70 Margin)
              </span>
              <span class="text-xs font-mono text-rose-400 font-bold">Herrador Suffers 122.76 Heartbreak</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">CULT OF THE LAMB (Franky)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">136.46 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  CeeDee Lamb (28.50), Caleb Williams (16.76), James Cook (16.70), Spencer Shrader (16.00), Chris Olave (13.30), Parker Washington (13.10), Denver DEF (9.00), Bhayshul Tuten (8.90), Colston Loveland (7.40), Malik Nabers (6.80).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Brock To The Future (Herrador)</span>
                  <span class="text-slate-400 font-athletic text-lg font-black">122.76 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Bucky Irving (26.50), Ja'Marr Chase (26.50), Brock Bowers (18.80), Jayden Daniels (14.56), Chuba Hubbard (11.60), Zach Charbonnet (9.10), New Orleans DEF (5.00), Jalen Coker (4.60), D'Andre Swift (3.10), Chad Ryland (3.00).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 3: Arnulfo vs Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-blue-400 bg-blue-950/50 border border-blue-800 px-2 py-0.5 rounded">
                ⚔️ Matchup 3 • Narrowest Victory (+6.40 Margin)
              </span>
              <span class="text-xs font-mono text-emerald-400 font-bold">Arnulfo Joins 6-3 1st Place Deadlock</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-blue-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">MyDakMakesHerWaddle (Arnulfo)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">118.40 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Christian Watson (26.60), Dak Prescott (19.50), KC Concepcion (16.80), Travis Kelce (15.30), Jahmyr Gibbs (13.40), Rhamondre Stevenson (13.30), Drew Stevens (8.00), Quinshon Judkins (5.00), Josh Jacobs (0.50).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                  <span class="text-slate-400 font-athletic text-lg font-black">112.00 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Bijan Robinson (23.70), Jake Bates (15.00), Rome Odunze (14.00), Seattle DEF (12.00), Harold Fannin (11.20), Omar Cooper (9.80), Drake London (9.30), Kyren Williams (7.60), Jared Goff (6.30), Malik Washington (3.10).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 4: Joey vs iRob -->
          <div class="bg-slate-900 border-2 border-emerald-500/60 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-emerald-400 bg-emerald-950/50 border border-emerald-800 px-2 py-0.5 rounded">
                ⚡ Matchup 4 • Statement Upset (+8.10 Margin)
              </span>
              <span class="text-xs font-mono text-emerald-400 font-bold">Joey Takes Solo 4th; iRob Wins $10 QB Bounty</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">TheGreatSwagsby (Joey)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">121.24 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Kenneth Walker (34.30), Christian McCaffrey (21.70), Kirk Cousins (15.64), Nico Collins (13.50), Will Reichard (9.00), Detroit DEF (9.00), Ollie Gordon (6.90), Emeka Egbuka (5.40), Braelon Allen (4.40), Tucker Kraft (1.40).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Njigbas in Paris (iRob)</span>
                  <span class="text-slate-400 font-athletic text-lg font-black">113.14 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Joe Burrow (29.54 - $10 QB Bounty), Jonah Coleman (16.80), Isaiah Likely (13.80), Tetairoa McMillan (13.60), Chase McLaughlin (10.00), Chase Brown (9.00), JSN (8.60), DJ Moore (5.10), Cincinnati DEF (4.00), Jaylen Waddle (2.70).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 5: Alex vs Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-purple-400 bg-purple-950/50 border border-purple-800 px-2 py-0.5 rounded">
                🎲 Matchup 5 • Wild-Card Scramble (+12.98 Margin)
              </span>
              <span class="text-xs font-mono text-purple-400 font-bold">Alex Climbs to 4-5; Eric Receives Toilet Sprint</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-purple-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">League Median Advocate 🗳 (Alex)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">99.34 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Drake Maye (21.26), Ka'imi Fairbairn (17.00), DeMario Douglas (12.70), Amon-Ra St. Brown (12.60), Kansas City DEF (12.00), Trey McBride (8.90), Tyler Allgeier (5.60), Derrick Henry (5.58), Demarcus Robinson (3.70), Ladd McConkey (0.00).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-red-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Show me dem TDs (Eric)</span>
                  <span class="text-red-400 font-athletic text-lg font-black">86.36 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Tee Higgins (17.70), Josh Allen (13.86), Houston DEF (13.00), Justin Jefferson (7.30), Matt Gay (7.00), Jonathan Taylor (6.90), Dylan Sampson (6.30), Sam LaPorta (5.20), Keenan Allen (4.60), Jameson Williams (4.50).
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 10: WEEK 10 GAMEDAY HUB
slide_10 = """      <!-- SLIDE 10: WEEK 10 GAMEDAY HUB -->
      <section id="wk9-slide-10" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-indigo-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 10 MATCHUP PREVIEWS • SPREADS & VEGAS LINES
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚡ Week 10 Gameday Hub</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Preview of Week 10 matchups and the $10 Highest Scoring RB Bounty!</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">5 Week 10 Matchups</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- Game of the Week: Mark vs Arnulfo -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-4 shadow-xl col-span-1 md:col-span-2">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-amber-400 bg-amber-950/80 border border-amber-700 px-2 py-0.5 rounded">
                👑 GAME OF THE WEEK • BATTLE FOR SOLE 1ST PLACE
              </span>
              <span class="font-mono text-emerald-400 font-bold">Spread: Mark -3.5 | O/U: 232.0 | $10 RB Target</span>
            </div>
            <div class="flex flex-col sm:flex-row justify-between items-center gap-4 py-2">
              <div class="text-center sm:text-left">
                <span class="text-base font-bold text-white">Saquon Deez Nacuas (Mark)</span>
                <span class="block text-amber-400 font-mono font-semibold">6-3 • 1107.04 PF (2nd)</span>
              </div>
              <div class="text-xl font-black text-amber-400 font-athletic">VS</div>
              <div class="text-center sm:text-right">
                <span class="text-base font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
                <span class="block text-emerald-400 font-mono font-semibold">6-3 • 1095.24 PF (3rd)</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400 border-t border-slate-800/80 pt-2 mt-1">
              Colossal heavyweight tilt! Mark rides the momentum of his 137.28 scoring crown against Arnulfo, who has gritted through multiple injuries to stay tied atop FFUC. The winner takes exclusive control of 1st place!
            </p>
          </div>

          <!-- Matchup 2: iRob vs Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-blue-400">Matchup 2 • Top Seed vs Wild-Card</span>
              <span class="font-mono text-slate-400">Spread: iRob -4.5 | O/U: 228.5</span>
            </div>
            <div class="flex justify-between items-center py-1">
              <div>
                <span class="font-bold text-white">Njigbas in Paris (iRob)</span>
                <span class="block text-[11px] text-emerald-400 font-mono">6-3 • 1110.40 PF (#1 Seed)</span>
              </div>
              <span class="font-bold text-slate-500 font-mono">VS</span>
              <div class="text-right">
                <span class="font-bold text-white">League Median Advocate 🗳 (Alex)</span>
                <span class="block text-[11px] text-slate-400 font-mono">4-5 • 1146.88 PF</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400 mt-2">
              iRob looks to rebound after a Week 9 setback, while Alex aims to push to .500 and prove his #3-ranked scoring attack belongs in the playoffs.
            </p>
          </div>

          <!-- Matchup 3: Joey vs Robert -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-purple-400">Matchup 3 • Playoff Positioning</span>
              <span class="font-mono text-slate-400">Spread: Joey -6.0 | O/U: 225.0</span>
            </div>
            <div class="flex justify-between items-center py-1">
              <div>
                <span class="font-bold text-white">TheGreatSwagsby (Joey)</span>
                <span class="block text-[11px] text-blue-400 font-mono">5-4 • 1103.64 PF (4th)</span>
              </div>
              <span class="font-bold text-slate-500 font-mono">VS</span>
              <div class="text-right">
                <span class="font-bold text-white">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                <span class="block text-[11px] text-rose-400 font-mono">3-6 • 1106.96 PF</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400 mt-2">
              Joey has sole possession of the final playoff seed and Kenneth Walker running hot. Defending champion Robert fights with his back against the wall.
            </p>
          </div>

          <!-- Matchup 4: Franky vs Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-emerald-400">Matchup 4 • 4-5 Wild-Card Clash</span>
              <span class="font-mono text-slate-400">Spread: Franky -9.5 | O/U: 224.0</span>
            </div>
            <div class="flex justify-between items-center py-1">
              <div>
                <span class="font-bold text-white">CULT OF THE LAMB (Franky)</span>
                <span class="block text-[11px] text-amber-400 font-mono">4-5 • 1193.26 PF (#1 PF)</span>
              </div>
              <span class="font-bold text-slate-500 font-mono">VS</span>
              <div class="text-right">
                <span class="font-bold text-white">Show me dem TDs (Eric)</span>
                <span class="block text-[11px] text-slate-400 font-mono">4-5 • 1035.08 PF</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400 mt-2">
              Direct elimination vibes! Franky's league-leading offense looks to break out of the 4-5 logjam against Eric looking to erase his toilet runner week.
            </p>
          </div>

          <!-- Matchup 5: Pedro vs Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-red-400">Matchup 5 • Cellar Escape Attempt</span>
              <span class="font-mono text-slate-400">Spread: Herrador -8.0 | O/U: 218.0</span>
            </div>
            <div class="flex justify-between items-center py-1">
              <div>
                <span class="font-bold text-white">I Didn’t Hear No Bell (Pedro)</span>
                <span class="block text-[11px] text-red-400 font-mono">3-6 • 814.46 PF (10th)</span>
              </div>
              <span class="font-bold text-slate-500 font-mono">VS</span>
              <div class="text-right">
                <span class="font-bold text-white">Brock To The Future (Herrador)</span>
                <span class="block text-[11px] text-slate-400 font-mono">4-5 • 1157.56 PF</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400 mt-2">
              Pedro desperately needs points to shave down his -292.50 PF deficit, but faces a vengeful Herrador squad looking to avenge a heartbreak loss.
            </p>
          </div>
        </div>

        <!-- Next Bounty Preview Card -->
        <div class="bg-gradient-to-r from-emerald-950/60 via-slate-900 to-emerald-950/60 border border-emerald-500/40 rounded-xl p-4 shadow-lg text-xs">
          <div class="flex justify-between items-center mb-1.5">
            <span class="font-bold text-white flex items-center gap-1.5">
              <span>⚡</span> Upcoming Week 10 Bounty Target: Highest Scoring Running Back ($10)
            </span>
            <span class="font-mono font-bold text-emerald-400">$10 Cash Direct</span>
          </div>
          <p class="text-slate-300 leading-relaxed text-[11px]">
            The cash moves to the ground game in Week 10! The manager starting the single highest scoring NFL Running Back takes home the $10 direct payout. Watch out for Saquon Barkley (Mark), Christian McCaffrey (Joey), Kenneth Walker (Joey), Derrick Henry (Franky), Bucky Irving (Herrador), and Bijan Robinson (Robert)!
          </p>
        </div>
      </section>"""


# -------------------------------------------------------------
# 3. ASSEMBLE DECK 9
# -------------------------------------------------------------
deck_wk9_html = f"""    <!-- ========================================== -->
    <!-- DECK 9: WEEK 9 OFFICIAL REPORT (ACTIVE)    -->
    <!-- ========================================== -->
    <div id="deck-wk9">
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

print("Replacing elements in index.html...")

# A. Replace Nav Pills
nav_pattern = r'<nav class="flex items-center gap-1.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">.*?</nav>'
html = re.sub(nav_pattern, new_nav_pills, html, count=1, flags=re.DOTALL)

# B. Update Header Sync Timestamp
html = re.sub(r'<strong class="text-slate-200" id="portalSyncedTime">.*?</strong>',
              '<strong class="text-slate-200" id="portalSyncedTime">Nov 10, 2026 • 12:45 PM CST (Week 9 Final Official Update)</strong>',
              html, count=1)

# C. Update Archive Dropdown
archive_select_pattern = r'<select id="seasonArchive" onchange="handleArchiveSelect\(this\.value\)"[^>]*>.*?</select>'
new_archive_select = """<select id="seasonArchive" onchange="handleArchiveSelect(this.value)" class="bg-slate-950 border border-slate-700 text-amber-400 text-xs font-bold py-1.5 px-3 rounded-lg focus:outline-none focus:border-amber-500 cursor-pointer shadow-sm">
            <option value="wk9" selected>📅 Week 9: Official Report (Final)</option>
            <option value="wk8">📅 Week 8: Official Report (Archive)</option>
            <option value="wk7">📅 Week 7: Official Report (Archive)</option>
            <option value="wk6">📅 Week 6: Official Report (Archive)</option>
            <option value="wk5">📅 Week 5: Official Report (Archive)</option>
            <option value="wk4">📅 Week 4: Official Report (Archive)</option>
            <option value="wk3">📅 Week 3: Official Report (Archive)</option>
            <option value="wk2">📅 Week 2: Official Report (Archive)</option>
            <option value="wk1">📅 Week 1: Season Opener (Archive)</option>
            <option value="locked" disabled>🔒 Week 10 (Upcoming)</option>
          </select>"""
html = re.sub(archive_select_pattern, new_archive_select, html, count=1, flags=re.DOTALL)

# D. Update Ticker Text
ticker_segment = """<span>👑 <strong>High Roller Champion:</strong> <span class="text-amber-400 font-bold">Mark (Saquon Deez Nacuas)</span> torches league for <span class="text-emerald-400 font-bold">137.28 PTS</span>!</span><span class="text-slate-500">•</span><span>⚡ <strong>$10 Bounty Winner (QB Crown):</strong> <span class="text-amber-400 font-bold">iRob (Njigbas in Paris)</span> pockets $10 behind Joe Burrow's <span class="text-emerald-400 font-bold">29.54 PTS</span>!</span><span class="text-slate-500">•</span><span>🚀 <strong>Championship Deadlock:</strong> <span class="text-amber-400 font-bold">iRob, Mark, & Arnulfo</span> tied atop the league at <span class="text-emerald-400 font-bold">6-3</span>!</span><span class="text-slate-500">•</span><span>💔 <strong>Heartbreak of the Week:</strong> <span class="text-amber-400 font-bold">Herrador (122.76 PTS)</span> puts up 4th highest score but falls to Franky's 136.46!</span><span class="text-slate-500">•</span><span>🎯 <strong>Pick-Em Co-Leaders:</strong> <span class="text-amber-400 font-bold">Arnulfo (15-win boom) & Robert</span> tied at <span class="text-emerald-400 font-bold">90.0 PTS</span>!</span><span class="text-slate-500">•</span><span>🚽 <strong>5K Toilet Danger Zone:</strong> <span class="text-red-400 font-bold">Pedro</span> anchored at 3-6 (814.46 PF), trailing by 292.50 pts with $0 FAAB!</span><span class="text-slate-500">•</span><span>🏃 <strong>Weekly Toilet Runner:</strong> <span class="text-red-400 font-bold">Eric</span> slumps to low score with <span class="text-red-400 font-bold">86.36 PTS</span>!</span>"""

new_ticker = f"""<div class="ticker-wrap flex-1 min-w-0">
        <div class="ticker-content text-slate-200 text-xs">
          <!-- Segment A -->
          <div class="inline-flex items-center gap-6 pr-6">{ticker_segment}</div>

          <!-- Segment B (Identical for seamless infinite loop) -->
          <div class="inline-flex items-center gap-6 pr-6" aria-hidden="true">{ticker_segment}</div>
        </div>
      </div>"""

html = re.sub(r'<div class="ticker-wrap flex-1 min-w-0">.*?(?=<!-- Quick Action Tab Button -->)', new_ticker + "\n\n      ", html, count=1, flags=re.DOTALL)

# E. Insert or Replace Deck 9
if '<div id="deck-wk9">' in html:
    print("Replacing existing deck-wk9...")
    deck_wk9_pattern = r'<div id="deck-wk9">.*?</div>\s*(?=<!-- ========================================== -->\s*<!-- DECK 8)'
    html = re.sub(deck_wk9_pattern, deck_wk9_html + "\n\n    ", html, count=1, flags=re.DOTALL)
elif '<div id="deck-wk8">' in html:
    print("Archiving deck-wk8 and inserting deck-wk9...")
    m_deck8 = re.search(r'(<div id="deck-wk8">.*?</div>\s*<!-- ========================================== -->\s*<!-- DECK 7)', html, re.DOTALL)
    if m_deck8:
        deck8_str = m_deck8.group(1)
        deck8_str_fixed = deck8_str.replace('id="broadcastAudio"', 'id="broadcastAudioWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="broadcastPlayBtn"', 'id="broadcastPlayBtnWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="playIcon"', 'id="playIconWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="pauseIcon"', 'id="pauseIconWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="audioPulseRing"', 'id="audioPulseRingWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="audioWaveform"', 'id="audioWaveformWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="broadcastTitleText"', 'id="broadcastTitleTextWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="broadcastDescText"', 'id="broadcastDescTextWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="audioCurrentTime"', 'id="audioCurrentTimeWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="audioDuration"', 'id="audioDurationWk8"')
        deck8_str_fixed = deck8_str_fixed.replace('id="audioProgressBar"', 'id="audioProgressBarWk8"')
        html = html.replace(deck8_str, deck8_str_fixed)

    html = html.replace('<div id="deck-wk8">', '<div id="deck-wk8" style="display:none;">')
    html = html.replace('<div id="deck-wk8" style="display:none;">', deck_wk9_html + '\n\n    <!-- ========================================== -->\n    <!-- DECK 8: WEEK 8 OFFICIAL REPORT (ARCHIVED)  -->\n    <!-- ========================================== -->\n    <div id="deck-wk8" style="display:none;">')

# F. Update JavaScript handleArchiveSelect to support wk9
old_archive_func = r'function handleArchiveSelect\(val\) \{.*?(?=function switchVoice|function copySleeperBlast|function prevSlide)'
new_archive_func = """function handleArchiveSelect(val) {
      if (val === 'wk1' || val === 'wk2' || val === 'wk3' || val === 'wk4' || val === 'wk5' || val === 'wk6' || val === 'wk7' || val === 'wk8' || val === 'wk9') {
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

        if (d1) d1.style.display = (val === 'wk1') ? 'block' : 'none';
        if (d2) d2.style.display = (val === 'wk2') ? 'block' : 'none';
        if (d3) d3.style.display = (val === 'wk3') ? 'block' : 'none';
        if (d4) d4.style.display = (val === 'wk4') ? 'block' : 'none';
        if (d5) d5.style.display = (val === 'wk5') ? 'block' : 'none';
        if (d6) d6.style.display = (val === 'wk6') ? 'block' : 'none';
        if (d7) d7.style.display = (val === 'wk7') ? 'block' : 'none';
        if (d8) d8.style.display = (val === 'wk8') ? 'block' : 'none';
        if (d9) d9.style.display = (val === 'wk9') ? 'block' : 'none';

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

# G. Update default currentEdition to wk9
html = html.replace("let currentEdition = 'wk8';", "let currentEdition = 'wk9';")

# H. Update copySleeperBlast
old_blast_pattern = r'function copySleeperBlast\(\) \{.*?(?=function|\Z)'
new_blast_func = """function copySleeperBlast() {
      const blast = `🏈 F.F.U.C. WEEK 9 OFFICIAL REPORT IS LIVE! 🏈
A monumental Week 9 has completely rewritten the championship race!

👑 HIGH ROLLER CHAMPION:
• Mark (Saquon Deez Nacuas) takes the Week 9 scoring crown with 137.28 PTS, routing Pedro by 33.10!

⚡ $10 BOUNTY WINNER (Highest Scoring QB):
• iRob (Njigbas in Paris) claims the $10 cash bounty behind Joe Burrow's 29.54-point masterclass!

🔥 3-WAY CHAMPIONSHIP DEADLOCK:
• iRob (1,110.40 PF), Mark (1,107.04 PF), and Arnulfo (1,095.24 PF) are now locked in a 3-way tie for 1st place at 6-3!

💔 HEARTBREAK OF THE WEEK:
• Herrador puts up 122.76 PTS (4th highest in FFUC), but runs headfirst into Franky's 136.46 explosion!

🎯 PICK-EM EXPLOSION ($45 Pot):
• Arnulfo detonates for a season-best 15.0 pts in Week 9 to catch Robert in a 90.0 tie for 1st place! iRob stalks in 3rd at 89.0!

🚽 5K TOILET RUNNER & BAR TAB METER:
• Eric posts the low score of the week (86.36 PTS). Pedro remains firmly anchored in last place at 814.46 PF (-292.50 deficit) with $0 FAAB!

⚔️ WEEK 10 PREVIEW:
• Game of the Week: #1 Mark vs #2 Arnulfo for sole possession of 1st place! Week 10 Bounty: Highest Scoring RB ($10)!

🎙️ Qwen3-VL 32B scripted audio broadcast, power rankings, and full interactive deck live now:
👉 https://ffucleague.com`;

      navigator.clipboard.writeText(blast).then(() => {
        const btn = document.getElementById('copyBlastBtn');
        const orig = btn.innerHTML;
        btn.innerHTML = '✅ Copied Week 9 Blast!';
        setTimeout(() => { btn.innerHTML = orig; }, 2500);
      });
    }
"""
html = re.sub(old_blast_pattern, new_blast_func, html, count=1, flags=re.DOTALL)

# Write updated index.html
with open(INDEX_PATH, "wb") as f:
    f.write(html.encode("utf-8"))

print("🎉 Successfully built and updated index.html with Week 9 deck!")


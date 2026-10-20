import re, json, os, sys

sys.stdout.reconfigure(encoding='utf-8')

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX_PATH = os.path.join(BASE_DIR, "index.html")

print("Reading index.html...")
with open(INDEX_PATH, "r", encoding="utf-8") as f:
    html = f.read()

# -------------------------------------------------------------
# 1. NEW NAV PILLS (12 SLIDES, NO VEGAS ODDS)
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
        <button onclick="goToSlide(9)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">10. 🏥 Injuries</button>
        <button onclick="goToSlide(10)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">11. ⚔️ Scoreboard</button>
        <button onclick="goToSlide(11)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-400 hover:text-white transition">12. ⚡ Wk 7 Gameday Hub</button>
      </nav>"""

# -------------------------------------------------------------
# 2. DEFINE SLIDES FOR DECK-WK6
# -------------------------------------------------------------

# SLIDE 0: HARDWARE & WEEKLY ROASTS
slide_0 = """      <!-- SLIDE 0: HARDWARE & ROASTS -->
      <section id="wk6-slide-0" class="slide active space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-500/20 via-slate-900 to-yellow-500/10 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL WEEK 6 AWARDS • F.F.U.C. HONORS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏆 Hardware & Weekly Roasts</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 6 official scoring titles, cash bounties, brutal bad beats, and toilet honors.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-900 border border-amber-500/30 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 6 Final</span>
          </div>
        </div>

        <!-- FFUC AI BROADCAST PLAYER (ALLTALK TTS) -->
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/70 to-slate-900 border-2 border-indigo-500/40 rounded-2xl p-4 sm:p-5 shadow-2xl relative overflow-hidden">
          <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
            <!-- Left Info & Play Button -->
            <div class="flex items-center gap-3.5">
              <div class="relative flex-shrink-0">
                <button id="broadcastPlayBtn" onclick="toggleBroadcastAudio()" class="w-12 h-12 sm:w-14 sm:h-14 rounded-full bg-gradient-to-tr from-amber-500 to-yellow-400 text-slate-950 flex items-center justify-center font-black shadow-xl hover:scale-105 active:scale-95 transition-all focus:outline-none cursor-pointer">
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
                    FFUC AI Studio • Local Broadcast
                  </span>
                  <!-- Voice Switcher Pills -->
                  <div class="inline-flex items-center bg-slate-950 border border-slate-700 rounded-lg p-0.5 text-[11px] font-mono font-bold">
                    <button id="voiceBtnMcafee" onclick="switchVoice('mcafee')" class="px-2.5 py-0.5 rounded bg-amber-500 text-slate-950 transition cursor-pointer">
                      🔥 Pat McAfee
                    </button>
                    <button id="voiceBtnFreeman" onclick="switchVoice('freeman')" class="px-2.5 py-0.5 rounded text-slate-400 hover:text-white transition cursor-pointer">
                      👑 Morgan Freeman
                    </button>
                  </div>
                </div>
                <div class="text-white font-extrabold text-sm sm:text-base tracking-tight flex items-center gap-2">
                  <span id="broadcastTitleText">Week 6 Official Audio Recap (Pat McAfee Edition)</span>
                  <!-- Animated Waveform Equalizer -->
                  <div id="audioWaveform" class="flex items-end gap-0.5 h-4 opacity-40 transition-opacity">
                    <span class="w-1 bg-amber-400 rounded-full h-2 animate-bounce" style="animation-delay: 0.1s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-4 animate-bounce" style="animation-delay: 0.3s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-3 animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-1 animate-bounce" style="animation-delay: 0.4s"></span>
                  </div>
                </div>
                <div id="broadcastDescText" class="text-xs text-slate-400 mt-0.5">
                  High-energy recap: Franky's 149.80 shootout win over Joey, Pedro's $10 DEF bounty upset of Alex, Herrador's 50-pt blowout, and Robert's 5K panic.
                </div>
              </div>
            </div>

            <!-- Right Controls: Progress Bar & Duration -->
            <div class="flex flex-col sm:items-end justify-center gap-1.5 min-w-[200px]">
              <div class="flex items-center justify-between sm:justify-end gap-3 text-xs font-mono w-full">
                <span id="audioCurrentTime" class="text-amber-400 font-bold">0:00</span>
                <span class="text-slate-600">/</span>
                <span id="audioDuration" class="text-slate-400">0:45</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2 border border-slate-800 cursor-pointer overflow-hidden" onclick="seekBroadcastAudio(event)">
                <div id="audioProgressBar" class="bg-gradient-to-r from-amber-500 to-yellow-400 h-full w-0 rounded-full transition-all duration-100"></div>
              </div>
              <span class="text-[10px] text-slate-500 font-mono">TTS Voice Synthesis • Click to stream</span>
            </div>
          </div>
          <!-- Audio Element -->
          <audio id="broadcastAudio" src="assets/audio/wk6_recap_mcafee.wav" preload="metadata" ontimeupdate="updateBroadcastProgress()" onended="onBroadcastAudioEnded()"></audio>
        </div>

        <!-- AWARDS GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Award 1: High Roller Champion -->
          <div class="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border-2 border-amber-500/60 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-amber-500 text-slate-950 px-2.5 py-0.5 rounded">👑 Week 6 High Roller Champion</span>
              <span class="text-xl font-athletic font-bold text-amber-400">149.80 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">CULT OF THE LAMB <span class="text-amber-400 text-sm font-semibold">(Franky)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Franky unleashes an unstoppable 149.80-point offensive clinic! Led by James Cook (22.80), Bhayshul Tuten (22.70), Malik Nabers (22.50), and Colston Loveland (15.50), Franky outduels Joey in a 285-point slugfest, collects the $10 High Roller bounty, and captures the #1 overall season scoring throne (814.62 PF)!
            </p>
            <!-- FaceFusion AI Coronation Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-amber-500/40 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-amber-500/40 text-[9px] font-mono font-bold text-amber-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                FaceFusion AI Meme • Franky Coronation Toast
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline>
                <source src="assets/video/franky_high_roller.mp4" type="video/mp4">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Season Scoring Leader: Franky (814.62 PF)</span>
              <span class="text-amber-400 font-bold font-mono">+$10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 2: $10 DEF Bounty Winner -->
          <div class="bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-emerald-500 text-slate-950 px-2.5 py-0.5 rounded">⚡ $10 Weekly Bounty: Highest DEF</span>
              <span class="text-xl font-athletic font-bold text-emerald-400">16.00 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">Kansas City Chiefs DEF <span class="text-emerald-400 text-sm font-semibold">(I Didn’t Hear No Bell / Pedro)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Pedro collects his first cash bounty of 2026! The Kansas City Chiefs defense put up a suffocating 16.00-point performance to edge out Denver (14.00) and Pittsburgh (10.00), earning Pedro the $10 defense cash prize and fueling his massive 112.04 to 87.04 upset blowout over Alex!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Runner-Up: Denver Broncos DEF (14.00 PTS)</span>
              <span class="text-emerald-400 font-bold font-mono">Pedro: $10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 3: Heartbreak Bad Beat (Joey) -->
          <div class="bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-900 border border-rose-500/40 rounded-2xl p-5 shadow-xl">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-bold uppercase tracking-wider bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-0.5 rounded">💔 Heartbreak of the Week</span>
              <span class="text-lg font-athletic font-bold text-rose-400">135.28 PTS (L)</span>
            </div>
            <h3 class="text-xl font-black text-white">TheGreatSwagsby <span class="text-rose-400 text-sm font-semibold">(Joey)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Joey puts up an elite 135.28 points—the 3rd highest score in the entire league this week—only to run headfirst into Franky's 149.80 juggernaut! Despite monster showings from Kenneth Walker (26.90), Christian McCaffrey (26.20), and C.J. Stroud (23.98), Joey falls in a 285-point shootout where he would have defeated 8 out of 9 other teams in FFUC!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Defeated by: Franky (149.80)</span>
              <span class="text-rose-400 font-bold font-mono">Would Defeat 8 of 9 Teams</span>
            </div>
          </div>

          <!-- Award 4: 5K Toilet Runner of the Week (Robert) -->
          <div class="bg-gradient-to-br from-red-950/40 via-slate-900 to-slate-900 border border-red-500/40 rounded-2xl p-5 shadow-xl">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-bold uppercase tracking-wider bg-red-950 text-red-300 border border-red-800 px-2.5 py-0.5 rounded">🚽 5K Toilet Runner of the Week</span>
              <span class="text-lg font-athletic font-bold text-red-400">79.62 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">WE GOIN’ BACK 2 BACK <span class="text-red-400 text-sm font-semibold">(Robert)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Defending champion Robert hits rock bottom! Robert puts up a week-low 79.62 PTS in a 26.74-point blowout loss to iRob (106.36). With Mark Andrews (0.90) and Derrick Henry (4.50) laying goose-eggs, Robert slides to 2-4 and enters the dangerous 5K punishment conversation alongside season cellar-dweller Pedro (550.56 PF)!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Week 6 Low Score: 79.62 PTS</span>
              <span class="text-red-400 font-bold font-mono">Record: 2-4 (L2 Streak)</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 1: STATE OF THE UNION & STANDINGS
slide_1 = """      <!-- SLIDE 1: STATE OF THE UNION -->
      <section id="wk6-slide-1" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 6 LEAGUE AUDIT • COMMISSIONER'S DESK
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏛️ State of the Union: Week 6</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">iRob takes sole possession of 1st place at 5-1, Franky wins the 285-point shootout of the year, and a 5-way logjam forms at 3-3.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-blue-400 font-mono font-bold px-3 py-1 rounded-lg">6 of 14 Weeks Complete</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">👑 Top Seed Breakaway</span>
            <div class="text-base font-bold text-white mt-1">5-1 Sole Monarch: iRob</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob (<em>Njigbas in Paris</em>: 746.66 PF) stands alone atop the FFUC mountaintop at 5-1! Behind Isaiah Likely (20.90) and JSN (19.40), iRob dispatched Robert (106.36 to 79.62) to take sole possession of 1st place. Arnulfo (742.36 PF) sits just behind at 4-2.
            </p>
          </div>

          <div class="bg-slate-900 border border-blue-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-400">⚔️ Midfield Gridlock</span>
            <div class="text-base font-bold text-white mt-1">5 Franchises Tied at 3-3</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Parity reigns across FFUC! Herrador (784.10 PF), Joey (776.14 PF), Alex (775.64 PF), Eric (703.86 PF), and Mark (692.58 PF) are all locked in a ferocious dogfight for the 6 playoff spots, separated by razor-thin scoring margins.
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">🔥 Cellar Battles</span>
            <div class="text-base font-bold text-white mt-1">The 2-4 Resurgence & Panic</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Franky scored 149.80 PTS to jump to a league-leading 814.62 season PF while moving to 2-4. Defending champion Robert slumped to a league-low 79.62 (2-4), while Pedro (2-4) claimed his first signature upset over Alex!
            </p>
          </div>
        </div>

        <!-- Standings Snapshot Grid (OFFICIAL SLEEPER WEEK 6 STANDINGS) -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Official Week 6 Standings Snapshot</span>
            <span class="font-mono text-slate-400">W-L Record • Points For • Points Against</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-8 font-bold text-emerald-400">1</span>
              <span class="flex-1 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">5-1</span>
              <span class="w-20 text-right text-slate-300">746.66 PF</span>
              <span class="w-20 text-right text-slate-500">703.90 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-8 font-bold text-emerald-400">2</span>
              <span class="flex-1 font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">4-2</span>
              <span class="w-20 text-right text-slate-300">742.36 PF</span>
              <span class="w-20 text-right text-slate-500">720.18 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-8 font-bold text-blue-400">3</span>
              <span class="flex-1 font-bold text-white">Brock To The Future (Herrador)</span>
              <span class="w-16 text-center text-blue-400 font-bold">3-3</span>
              <span class="w-20 text-right text-amber-400 font-bold">784.10 PF</span>
              <span class="w-20 text-right text-slate-500">729.88 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-8 font-bold text-blue-400">4</span>
              <span class="flex-1 font-bold text-white">TheGreatSwagsby (Joey)</span>
              <span class="w-16 text-center text-blue-400 font-bold">3-3</span>
              <span class="w-20 text-right text-slate-300">776.14 PF</span>
              <span class="w-20 text-right text-slate-500">685.54 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-8 font-bold text-blue-400">5</span>
              <span class="flex-1 font-bold text-white">Amon-Ra's Maye-hem (Alex)</span>
              <span class="w-16 text-center text-blue-400 font-bold">3-3</span>
              <span class="w-20 text-right text-slate-300">775.64 PF</span>
              <span class="w-20 text-right text-slate-500">733.92 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-8 font-bold text-blue-400">6</span>
              <span class="flex-1 font-bold text-white">Show me dem TDs (Eric)</span>
              <span class="w-16 text-center text-blue-400 font-bold">3-3</span>
              <span class="w-20 text-right text-slate-300">703.86 PF</span>
              <span class="w-20 text-right text-slate-500">717.16 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-950/40">
              <span class="w-8 font-bold text-slate-400">7</span>
              <span class="flex-1 font-medium text-slate-300">Saquon Deez Nacuas (Mark)</span>
              <span class="w-16 text-center text-slate-400">3-3</span>
              <span class="w-20 text-right text-slate-400">692.58 PF</span>
              <span class="w-20 text-right text-slate-500">725.48 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-amber-950/20">
              <span class="w-8 font-bold text-amber-400">8</span>
              <span class="flex-1 font-bold text-white">CULT OF THE LAMB (Franky)</span>
              <span class="w-16 text-center text-amber-400 font-bold">2-4</span>
              <span class="w-20 text-right text-amber-400 font-extrabold">814.62 PF (1st)</span>
              <span class="w-20 text-right text-rose-400">834.68 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-8 font-bold text-rose-400">9</span>
              <span class="flex-1 font-medium text-slate-300">WE GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-16 text-center text-rose-400 font-bold">2-4</span>
              <span class="w-20 text-right text-slate-300">754.54 PF</span>
              <span class="w-20 text-right text-slate-500">775.48 PA</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-red-950/30">
              <span class="w-8 font-bold text-red-500">10</span>
              <span class="flex-1 font-medium text-slate-400">I Didn’t Hear No Bell / Bryce Wide Shut (Pedro)</span>
              <span class="w-16 text-center text-red-500 font-bold">2-4</span>
              <span class="w-20 text-right text-red-400">550.56 PF</span>
              <span class="w-20 text-right text-slate-500">714.84 PA</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 2: $10 WEEKLY BOUNTY BOARD
slide_2 = """      <!-- SLIDE 2: $10 BOUNTY BOARD -->
      <section id="wk6-slide-2" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-green-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEKLY PRIZE POOL • DIRECT CASH PAYOUTS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💵 $10 Weekly Bounty Board</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 6 Team Defense winner crowned; Week 7 Narrowest Victory bounty is now live!</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-emerald-400">$140.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Season Bounty Pot</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Week 6 Winner Card -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden flex flex-col justify-between">
            <div class="absolute top-0 right-0 bg-emerald-500 text-slate-950 text-xs font-extrabold px-3 py-1 rounded-bl-xl uppercase tracking-wider">
              Bounty Collected ($10)
            </div>
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">Week 6 Target: Highest Scoring DEF ($10)</span>
              <h3 class="text-2xl font-black text-white mt-1">Kansas City Chiefs DEF • 16.00 PTS</h3>
              <div class="text-xs text-slate-400 mt-0.5">Manager: <strong class="text-slate-200">Pedro</strong> (I Didn’t Hear No Bell)</div>

              <div class="my-4 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl space-y-2">
                <div class="text-xs text-emerald-300 font-semibold">⚡ The Dominant DEF Statline:</div>
                <div class="text-xs text-slate-300 leading-relaxed">
                  The Kansas City Chiefs defense dominated with 16.00 fantasy points, generating sacks and turnovers to secure Pedro his first direct cash bounty of the season and power his 112.04 upset over Alex!
                </div>
              </div>

              <!-- Top 5 DEF Standings -->
              <div class="space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-emerald-500/40">
                  <span class="font-bold text-emerald-400">1. Kansas City Chiefs • Pedro</span>
                  <span class="font-black text-white">16.00 PTS (WON $10)</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-300">
                  <span>2. Denver Broncos • iRob (Bench)</span>
                  <span class="font-bold text-amber-400">14.00 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-400">
                  <span>3. Pittsburgh Steelers • Alex (Bench)</span>
                  <span>10.00 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-400">
                  <span>4. Baltimore Ravens • Herrador</span>
                  <span>9.00 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-slate-400">
                  <span>5. New England Patriots • Alex</span>
                  <span>6.00 PTS</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Bounty Status:</span>
              <span class="text-emerald-400 font-bold uppercase">Paid / Confirmed ($10 to Pedro)</span>
            </div>
          </div>

          <!-- Week 7 Next Up Preview -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 bg-amber-950 border border-amber-800 px-2 py-0.5 rounded">Next Up</span>
              <h3 class="text-2xl font-black text-white mt-2">Week 7: Narrowest Victory ($10)</h3>
              <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                Heart-stopping drama! The manager who secures the narrowest margin of victory in Week 7 takes home the $10 direct cash prize! Every yard, reception, and stat-correction counts.
              </p>

              <div class="mt-4 p-3 bg-slate-950 rounded-xl border border-slate-800 space-y-2">
                <div class="text-xs font-bold text-white uppercase tracking-wider">Historical Narrow Clashes:</div>
                <div class="text-xs text-slate-400 space-y-1">
                  <div class="flex justify-between">
                    <span>Week 5 Arnulfo def Franky:</span>
                    <span class="text-rose-400 font-mono font-bold">3.96 Margin</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Week 2 Herrador def Eric:</span>
                    <span class="text-rose-400 font-mono font-bold">5.82 Margin</span>
                  </div>
                  <div class="flex justify-between">
                    <span>Week 1 Alex def Joey:</span>
                    <span class="text-rose-400 font-mono font-bold">7.24 Margin</span>
                  </div>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Bounty Target Rule:</span>
              <span class="text-amber-400 font-bold uppercase">Smallest Final Win Margin</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 3: BAR TAB & 5K TOILET METER
slide_3 = """      <!-- SLIDE 3: BAR TAB & 5K TOILET METER -->
      <section id="wk6-slide-3" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-red-950/80 via-slate-900 to-amber-950/80 border border-red-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-red-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              THE 5K PUNISHMENT PROTOCOL • LIVE BAR TAB TRACKER
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍻 The Bar Tab & 5K Toilet Meter</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Last-place manager runs the official FFUC 5K and funds the league open bar tab.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-red-400 font-mono font-bold px-3 py-1 rounded-lg">Week 6 Meter Active</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- The Cellar Dweller Card (Pedro) -->
          <div class="bg-slate-900 border-2 border-red-500/60 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <div class="flex items-center justify-between mb-2">
                <span class="text-xs font-mono font-bold uppercase tracking-wider text-red-400 bg-red-950 border border-red-800 px-2 py-0.5 rounded">Pace-Car / Season Cellar Dweller</span>
                <span class="text-lg font-athletic font-bold text-red-400">2-4 • 550.56 PF</span>
              </div>
              <h3 class="text-2xl font-black text-white">Bryce Wide Shut <span class="text-red-400 text-sm font-semibold">(Pedro)</span></h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                Pedro picked up a huge Week 6 victory and the $10 defense bounty, but his season total of 550.56 PF remains firmly anchored in last place—sitting <strong class="text-red-400">142.02 points behind Mark (692.58 PF)</strong> and over 215 points behind the league average. Pedro remains the odds-on favorite to lace up the running shoes!
              </p>

              <!-- FaceFusion AI 5K Punishment Video -->
              <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950">
                <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/40 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                  FaceFusion AI Meme • Pedro Forrest Gump 5K Training
                </div>
                <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline>
                  <source src="assets/video/pedro_5k_runner.mp4" type="video/mp4">
                </video>
              </div>

              <div class="mt-4 p-3 bg-red-950/30 border border-red-800/40 rounded-xl space-y-2 text-xs">
                <div class="flex justify-between items-center text-slate-300">
                  <span>Projected 5K Finishing Time:</span>
                  <span class="font-mono font-bold text-red-400">1 Hour 10 Mins (22:30/mi)</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Open Bar Tab Meter Liability:</span>
                  <span class="font-mono font-bold text-amber-400">$215.00 Est.</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Distance to 9th Place Safety:</span>
                  <span class="font-mono font-bold text-slate-200">142.02 Total Points</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Punishment Likelihood:</span>
              <span class="text-red-400 font-bold uppercase">84.2% Implied Probability</span>
            </div>
          </div>

          <!-- Danger Index & Rules -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 bg-amber-950 border border-amber-800 px-2 py-0.5 rounded">Rules & Liabilities</span>
              <h3 class="text-xl font-black text-white mt-2">How the 5K Tab Formula Works</h3>
              <p class="text-xs text-slate-300 mt-1 leading-relaxed">
                The last place franchise must complete an in-person, timed 5K run. For every minute over a 30:00 baseline time, a $5 surcharge is deposited directly into the post-season draft party open bar tab!
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
                  <span>Franky (2-4):</span>
                  <span class="text-emerald-400 font-mono font-bold">814.62 PF (Safe Floor)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Robert (2-4):</span>
                  <span class="text-rose-400 font-mono font-bold">754.54 PF (Trending Down)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Mark (3-3):</span>
                  <span class="text-slate-300 font-mono font-bold">692.58 PF (Low Cushion)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Next In Line Danger:</span>
              <span class="text-amber-400 font-bold">Robert (2-4) & Mark (3-3)</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 4: THE LUCK INDEX
slide_4 = """      <!-- SLIDE 4: THE LUCK INDEX -->
      <section id="wk6-slide-4" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-purple-950/80 via-slate-900 to-indigo-950/80 border border-purple-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-purple-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ADVANCED ANALYTICS • ALL-PLAY CORRELATION
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍀 The Luck Index: Schedule Variance</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Expected Wins vs Actual Wins across 54 total all-play matchup simulations through Week 6.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-purple-400 font-mono font-bold px-3 py-1 rounded-lg">54 All-Play Games</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">🍀 The Luckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">iRob (+1.78) & Pedro (+1.11)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob sits atop the league at 5-1 despite an expected win tally of just 3.22 (29-25 all-play). Pedro has won 2 head-to-head matchups despite an 8-46 all-play record (0.89 expected wins)!
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">💀 The Unluckiest Franchise</span>
            <div class="text-lg font-black text-white mt-1">Franky (-1.89 Wins Below Expectation)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Franky owns the #1 all-play record in the league at 35-19 (64.8%) and the #1 scoring offense (814.62 PF), yet sits at 2-4 due to absorbing an astronomical league-high 834.68 points against!
            </p>
          </div>
        </div>

        <!-- Luck Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Expected Wins Matrix (Week 6 Audit • 54 Games)</span>
            <span class="font-mono text-purple-400 font-bold">Actual vs Expected Delta</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-48 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">5-1 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.22 (Exp)</span>
              <span class="w-28 text-center text-slate-300">29-25 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.78 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-48 font-bold text-white">Bryce Wide Shut (Pedro)</span>
              <span class="w-20 text-center text-slate-300 font-bold">2-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">0.89 (Exp)</span>
              <span class="w-28 text-center text-red-400">8-46 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.11 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-48 font-bold text-white">MyDakMakesHerWaddle (Arnulfo)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">4-2 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.22 (Exp)</span>
              <span class="w-28 text-center text-slate-300">29-25 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+0.78 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-48 font-bold text-white">Show me dem TDs (Eric)</span>
              <span class="w-20 text-center text-blue-400 font-bold">3-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">2.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">23-31 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+0.44 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-48 font-bold text-white">Saquon Deez Nacuas (Mark)</span>
              <span class="w-20 text-center text-slate-400">3-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">2.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">25-29 All-Play</span>
              <span class="w-24 text-right text-slate-300 font-bold">+0.22 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between">
              <span class="w-48 font-bold text-white">Amon-Ra's Maye-hem (Alex)</span>
              <span class="w-20 text-center text-blue-400 font-bold">3-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.33 (Exp)</span>
              <span class="w-28 text-center text-emerald-400 font-bold">30-24 All-Play</span>
              <span class="w-24 text-right text-slate-300 font-bold">-0.33 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/15">
              <span class="w-48 font-bold text-white">TheGreatSwagsby (Joey)</span>
              <span class="w-20 text-center text-blue-400 font-bold">3-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.67 (Exp)</span>
              <span class="w-28 text-center text-emerald-400 font-bold">33-21 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.67 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/15">
              <span class="w-48 font-bold text-white">Brock To The Future (Herrador)</span>
              <span class="w-20 text-center text-blue-400 font-bold">3-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.67 (Exp)</span>
              <span class="w-28 text-center text-emerald-400 font-bold">33-21 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.67 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-48 font-bold text-white">WE GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-20 text-center text-rose-400 font-bold">2-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">2.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">25-29 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.78 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/30">
              <span class="w-48 font-bold text-white">CULT OF THE LAMB (Franky)</span>
              <span class="w-20 text-center text-rose-400 font-bold">2-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.89 (Exp)</span>
              <span class="w-28 text-center text-amber-400 font-extrabold">35-19 All-Play (1st)</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.89 💀</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 5: POWER RANKINGS
slide_5 = """      <!-- SLIDE 5: POWER RANKINGS -->
      <section id="wk6-slide-5" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-orange-950/80 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ANALYTIC POWER INDEX • STRENGTH OF SQUAD
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">📈 Power Rankings: Week 6</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">True hierarchy based on roster firepower, all-play strength, and total points generated.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 6 Edition</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- Rank 1: iRob -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">1</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Njigbas in Paris (iRob)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +2 (5-1)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                746.66 PF. Takes sole possession of the 1st place throne. Dispatched defending champ Robert (106.36 to 79.62). Isaiah Likely (20.90) and JSN (19.40) provide reliable weekly firepower.
              </p>
            </div>
          </div>

          <!-- Rank 2: Franky -->
          <div class="bg-slate-900 border border-amber-500/40 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">2</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">CULT OF THE LAMB (Franky)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +4 (2-4)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                814.62 PF (#1 overall scoring offense in FFUC!). Exploded for 149.80 PTS to capture the $10 High Roller bounty. Leads the league in all-play wins (35-19). An offensive juggernaut.
              </p>
            </div>
          </div>

          <!-- Rank 3: Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-200">3</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Brock To The Future (Herrador)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +4 (3-3)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                784.10 PF (#2 in scoring!). Delivered a savage 49.68-point demolition of Arnulfo (137.40 to 87.72). D'Andre Swift (21.00), Jayden Daniels (21.00), and Ray Davis (20.20) are firing on all cylinders.
              </p>
            </div>
          </div>

          <!-- Rank 4: Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-200">4</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">TheGreatSwagsby (Joey)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (3-3)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                776.14 PF (#3 in scoring!). Poured in 135.28 points in the heartbreak of the week against Franky. Christian McCaffrey (26.20) and Ken Walker (26.90) form the most terrifying RB duo in the league.
              </p>
            </div>
          </div>

          <!-- Rank 5: Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">5</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">MyDakMakesHerWaddle (Arnulfo)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -3 (4-2)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                742.36 PF. Stumbled with an 87.72-point performance against Herrador, but holds the league's 2nd place standing at 4-2. Tre Tucker (24.20) was the lone bright spot in Week 6.
              </p>
            </div>
          </div>

          <!-- Rank 6: Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">6</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Amon-Ra's Maye-hem (Alex)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -5 (3-3)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                775.64 PF (#4 in scoring). Suffered a shocking 112.04 to 87.04 upset defeat to Pedro. Left Drake Maye (23.80) on the bench while Cam Skattebo put up a 0.00-point stinker.
              </p>
            </div>
          </div>

          <!-- Rank 7: Robert -->
          <div class="bg-slate-900 border border-rose-500/30 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-rose-400">7</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">WE GOIN’ BACK 2 BACK (Robert)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -3 (2-4)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                754.54 PF. Hit rock bottom in Week 6 with a league-low 79.62 points. Derrick Henry (4.50) and Harold Fannin (1.40) disappeared. Needs an immediate rebound against Pedro in Week 7.
              </p>
            </div>
          </div>

          <!-- Rank 8: Mark -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">8</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (3-3)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                692.58 PF. Secured a crucial 101.42 to 82.20 win over Eric to climb into the 3-3 playoff bubble. Kirk Cousins (19.52) and George Kittle (15.40) stepped up in big spots.
              </p>
            </div>
          </div>

          <!-- Rank 9: Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-500">9</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Show me dem TDs (Eric)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -1 (3-3)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                703.86 PF. Slipped to 82.20 points in a loss to Mark. Mark Andrews (0.90) and Terry McLaurin (3.20) failed to produce, dropping Eric to 9th in power rating despite a 3-3 record.
              </p>
            </div>
          </div>

          <!-- Rank 10: Pedro -->
          <div class="bg-slate-900 border border-red-500/40 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-red-500">10</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">I Didn’t Hear No Bell (Pedro)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ Upset Win (2-4)</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                550.56 PF. Claimed his biggest win of the year (112.04 over Alex) and bagged the $10 DEF bounty (KC DEF 16.00). Still 10th in overall points, but showing signs of life!
              </p>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 6: FAAB RECEIPTS
slide_6 = """      <!-- SLIDE 6: FAAB RECEIPTS -->
      <section id="wk6-slide-6" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-teal-950/80 via-slate-900 to-emerald-950/80 border border-teal-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-teal-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              FINANCIAL AUDIT • WAIVER TRANSACTION LEDGER
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💰 FAAB Receipts: Week 6 Ledger</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official Sleeper waiver claims, spending velocity, and remaining FAAB bankrolls.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-teal-400 font-mono font-bold px-3 py-1 rounded-lg">Budget: $100 FAAB</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Week 6 Notable Moves -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-3">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-teal-400 bg-teal-950 border border-teal-800 px-2 py-0.5 rounded">Week 6 Completed Claims</span>
            <div class="space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <strong class="text-white">Kansas City Chiefs (DEF • KC)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro) — Won $10 DEF Bounty!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">$6 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Waiver Claim</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Los Angeles Rams (DEF • LAR)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-amber-400 font-bold">$3 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Waiver Claim</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tyler Allgeier (RB • ARI)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-300 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Waiver Claim</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Colston Loveland (TE • CHI)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky) — Scored 15.50 in shootout win!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent Add</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tre Tucker (WR • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">MyDakMakesHerWaddle (Arnulfo) — Exploded for 24.20 PTS!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent Add</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Aaron Rodgers (QB • PIT)</strong>
                  <span class="block text-slate-400 text-[11px]">WE GOIN’ BACK 2 BACK (Robert)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent Add</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Remaining FAAB Bankrolls -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400 bg-amber-950 border border-amber-800 px-2 py-0.5 rounded">Current FAAB Bankrolls (Post-Week 6)</span>
            <div class="mt-3 divide-y divide-slate-800/80 text-xs font-mono">
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-white font-bold">1. Robert (WE GOIN’ BACK 2 BACK)</span>
                <span class="text-emerald-400 font-bold">$100 (100%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">2. Mark (Saquon Deez Nacuas)</span>
                <span class="text-emerald-400 font-bold">$80 (80%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">3. iRob (Njigbas in Paris)</span>
                <span class="text-emerald-400 font-bold">$80 (80%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">4. Alex (Amon-Ra's Maye-hem)</span>
                <span class="text-emerald-400 font-bold">$70 (70%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">5. Eric (Show me dem TDs)</span>
                <span class="text-amber-400 font-bold">$57 (57%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">6. Herrador (Brock To The Future)</span>
                <span class="text-amber-400 font-bold">$56 (56%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">7. Franky (CULT OF THE LAMB)</span>
                <span class="text-amber-400 font-bold">$47 (47%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">8. Joey (TheGreatSwagsby)</span>
                <span class="text-amber-400 font-bold">$35 (35%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">9. Arnulfo (MyDakMakesHerWaddle)</span>
                <span class="text-amber-400 font-bold">$35 (35%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center bg-red-950/30 px-2 rounded">
                <span class="text-red-400 font-bold">10. Pedro (Bryce Wide Shut)</span>
                <span class="text-red-400 font-bold">$0 (0% • Bankrupt)</span>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 8: BOOMS & BUSTS
slide_8 = """      <!-- SLIDE 8: BOOMS & BUSTS -->
      <section id="wk6-slide-8" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-orange-950/80 via-slate-900 to-amber-950/80 border border-orange-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-orange-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              VOLATILITY TRACKER • BOOM & BUST AUDIT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💥 Booms & Busts: Week 6 Outliers</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">The game-winning fireworks and matchup-tanking disappointments of Week 6.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-orange-400 font-mono font-bold px-3 py-1 rounded-lg">Week 6 Outliers</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- The Boom Squad -->
          <div class="bg-slate-900 border border-emerald-500/40 rounded-2xl p-5 shadow-xl space-y-3">
            <div class="flex items-center justify-between border-b border-emerald-500/30 pb-2">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 px-2.5 py-0.5 rounded">🚀 Week 6 Boom Squad</span>
              <span class="text-xs font-mono text-emerald-400 font-bold">22+ Fantasy Points</span>
            </div>
            <div class="space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Trevor Lawrence (QB • JAX)</strong>
                  <span class="block text-slate-400 text-[11px]">Brock To The Future (Herrador)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">28.34 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Kenneth Walker III (RB • SEA)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">26.90 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Christian McCaffrey (RB • SF)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">26.20 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Tre Tucker (WR • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">MyDakMakesHerWaddle (Arnulfo)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">24.20 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">C.J. Stroud (QB • HOU)</strong>
                  <span class="block text-slate-400 text-[11px]">TheGreatSwagsby (Joey)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">23.98 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">James Cook (RB • BUF)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">22.80 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Bhayshul Tuten (RB • CLE)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">22.70 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Malik Nabers (WR • NYG)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-emerald-400">22.50 PTS</div>
              </div>
            </div>
          </div>

          <!-- The Bust Brigade -->
          <div class="bg-slate-900 border border-rose-500/40 rounded-2xl p-5 shadow-xl space-y-3">
            <div class="flex items-center justify-between border-b border-rose-500/30 pb-2">
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-rose-400 bg-rose-950 px-2.5 py-0.5 rounded">❄️ Week 6 Ghost Protocol (Busts)</span>
              <span class="text-xs font-mono text-rose-400 font-bold">Under 4.5 Fantasy Points</span>
            </div>
            <div class="space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Cam Skattebo (RB • NYG)</strong>
                  <span class="block text-slate-400 text-[11px]">Amon-Ra's Maye-hem (Alex) — Goose Egg!</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">0.00 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Keaton Mitchell (RB • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">0.40 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Mark Andrews (TE • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">0.90 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Harold Fannin Jr. (TE • CLE)</strong>
                  <span class="block text-slate-400 text-[11px]">WE GOIN’ BACK 2 BACK (Robert)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">1.40 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Terry McLaurin (WR • WAS)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">3.20 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">A.J. Brown (WR • PHI)</strong>
                  <span class="block text-slate-400 text-[11px]">MyDakMakesHerWaddle (Arnulfo)</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">4.20 PTS</div>
              </div>
              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white text-sm">Derrick Henry (RB • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">WE GOIN’ BACK 2 BACK (Robert) — Sunk Robert to 79.62</span>
                </div>
                <div class="text-right font-mono font-athletic text-lg font-bold text-rose-400">4.50 PTS</div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 9: INJURIES (UPDATED FOR WEEK 6/7)
slide_9 = """      <!-- SLIDE 9: INJURIES (WEEK 6 AUDIT & WEEK 7 RADAR) -->
      <section id="wk6-slide-9" class="slide space-y-4 animate-fade">
        <!-- Header Banner -->
        <div class="bg-gradient-to-r from-red-950/90 via-slate-900 to-emerald-950/80 border-2 border-red-500/40 rounded-2xl p-5 shadow-2xl">
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3">
            <div>
              <div class="inline-flex items-center gap-1.5 bg-red-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
                MEDICAL HEADQUARTERS • WEEK 6 AUDIT & WEEK 7 RADAR
              </div>
              <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white flex items-center gap-2">
                <span>🏥 Official Injury Audit & Return Radar</span>
              </h2>
              <p class="text-xs sm:text-sm text-slate-300 mt-1">
                Strict medical filter: Exclusively highlighting players who suffered in-game injuries during Week 6, alongside key injured stars trending to return for Week 7.
              </p>
            </div>
            <div class="flex flex-wrap items-center gap-2">
              <span class="text-xs bg-red-950/80 border border-red-700 text-red-300 font-mono font-bold px-3 py-1 rounded-lg">
                🚨 Week 6 In-Game Casualties
              </span>
              <span class="text-xs bg-emerald-950/80 border border-emerald-700 text-emerald-300 font-mono font-bold px-3 py-1 rounded-lg">
                🔄 Week 7 Return Targets
              </span>
            </div>
          </div>
        </div>

        <!-- SECTION 1: INJURED DURING WEEK 6 -->
        <div>
          <div class="flex items-center gap-2 mb-2.5">
            <span class="w-2.5 h-2.5 rounded-full bg-red-500 animate-pulse"></span>
            <h3 class="text-base sm:text-lg font-black uppercase tracking-wider text-red-400">
              🚨 Injured During Week 6 Action (Exited Contest / New Concerns)
            </h3>
            <span class="text-[11px] text-slate-400 font-mono ml-auto">In-Game Casualties</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <!-- 1. Chris Olave -->
            <div class="bg-slate-900 border border-red-500/40 rounded-xl p-4 shadow-lg hover:border-red-400 transition flex flex-col justify-between">
              <div>
                <div class="flex justify-between items-start mb-1.5">
                  <div>
                    <span class="font-extrabold text-white text-base">Chris Olave</span>
                    <span class="text-xs text-slate-400 ml-1">(WR • NO)</span>
                  </div>
                  <span class="bg-red-950 text-red-400 border border-red-800 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                    CONCUSSION PROTOCOL
                  </span>
                </div>
                <div class="text-[11px] text-slate-400 mb-2">Franchise: <strong class="text-amber-400">Amon-Ra's Maye-hem (Alex)</strong></div>
                <div class="bg-slate-950/60 p-2 rounded border border-slate-800 mb-2 text-xs flex justify-between">
                  <span class="text-slate-400">Week 6 Impact:</span>
                  <span class="font-mono font-bold text-red-400">Exited 1st Quarter</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Absorbed a helmet-to-helmet blow and was immediately ruled out with a concussion. Enters strict NFL protocol on a short turnaround for Week 7.
                </p>
              </div>
            </div>

            <!-- 2. Marvin Harrison Jr. -->
            <div class="bg-slate-900 border border-red-500/40 rounded-xl p-4 shadow-lg hover:border-red-400 transition flex flex-col justify-between">
              <div>
                <div class="flex justify-between items-start mb-1.5">
                  <div>
                    <span class="font-extrabold text-white text-base">Marvin Harrison Jr.</span>
                    <span class="text-xs text-slate-400 ml-1">(WR • ARI)</span>
                  </div>
                  <span class="bg-red-950 text-red-400 border border-red-800 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                    CONCUSSION PROTOCOL
                  </span>
                </div>
                <div class="text-[11px] text-slate-400 mb-2">Franchise: <strong class="text-amber-400">Brock To The Future (Herrador)</strong></div>
                <div class="bg-slate-950/60 p-2 rounded border border-slate-800 mb-2 text-xs flex justify-between">
                  <span class="text-slate-400">Week 6 Impact:</span>
                  <span class="font-mono font-bold text-red-400">Exited 2nd Quarter</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Hit the turf hard after an incomplete target against Green Bay. Diagnosed with a concussion. Must clear all five protocol phases before Week 7 kickoff.
                </p>
              </div>
            </div>

            <!-- 3. Dallas Goedert -->
            <div class="bg-slate-900 border border-red-500/40 rounded-xl p-4 shadow-lg hover:border-red-400 transition flex flex-col justify-between">
              <div>
                <div class="flex justify-between items-start mb-1.5">
                  <div>
                    <span class="font-extrabold text-white text-base">Dallas Goedert</span>
                    <span class="text-xs text-slate-400 ml-1">(TE • PHI)</span>
                  </div>
                  <span class="bg-red-950 text-red-400 border border-red-800 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                    HAMSTRING STRAIN
                  </span>
                </div>
                <div class="text-[11px] text-slate-400 mb-2">Franchise: <strong class="text-amber-400">Saquon Deez Nacuas (Mark)</strong></div>
                <div class="bg-slate-950/60 p-2 rounded border border-slate-800 mb-2 text-xs flex justify-between">
                  <span class="text-slate-400">Week 6 Impact:</span>
                  <span class="font-mono font-bold text-red-400">0 Targets (Left Early)</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Suffered a hamstring pull on the opening offensive series. Expected to miss at least Week 7 as the Eagles manage his recovery conservatively.
                </p>
              </div>
            </div>
          </div>
        </div>

        <!-- SECTION 2: RETURNING FOR WEEK 7 -->
        <div class="pt-2">
          <div class="flex items-center gap-2 mb-2.5">
            <span class="w-2.5 h-2.5 rounded-full bg-emerald-500 animate-pulse"></span>
            <h3 class="text-base sm:text-lg font-black uppercase tracking-wider text-emerald-400">
              🔄 Projected Returns & Health Upgrades for Week 7
            </h3>
            <span class="text-[11px] text-slate-400 font-mono ml-auto">Re-Entering Lineups</span>
          </div>

          <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            <!-- 1. Christian McCaffrey -->
            <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg hover:border-emerald-400 transition flex flex-col justify-between">
              <div>
                <div class="flex justify-between items-start mb-1.5">
                  <div>
                    <span class="font-extrabold text-white text-base">Christian McCaffrey</span>
                    <span class="text-xs text-slate-400 ml-1">(RB • SF)</span>
                  </div>
                  <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                    100% BELLCOW ROLE
                  </span>
                </div>
                <div class="text-[11px] text-slate-400 mb-2">Franchise: <strong class="text-amber-400">TheGreatSwagsby (Joey)</strong></div>
                <div class="bg-slate-950/60 p-2 rounded border border-slate-800 mb-2 text-xs flex justify-between">
                  <span class="text-slate-400">Week 6 Validation:</span>
                  <span class="font-mono font-bold text-emerald-400">26.20 PTS (Full Workload)</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Proven fully healthy with zero snap restrictions. Handled all high-leverage red zone work and looks like the consensus #1 overall cheat code once again for Week 7.
                </p>
              </div>
            </div>

            <!-- 2. Malik Nabers -->
            <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg hover:border-emerald-400 transition flex flex-col justify-between">
              <div>
                <div class="flex justify-between items-start mb-1.5">
                  <div>
                    <span class="font-extrabold text-white text-base">Malik Nabers</span>
                    <span class="text-xs text-slate-400 ml-1">(WR • NYG)</span>
                  </div>
                  <span class="bg-emerald-950 text-emerald-400 border border-emerald-800 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                    FULLY CLEARED
                  </span>
                </div>
                <div class="text-[11px] text-slate-400 mb-2">Franchise: <strong class="text-amber-400">CULT OF THE LAMB (Franky)</strong></div>
                <div class="bg-slate-950/60 p-2 rounded border border-slate-800 mb-2 text-xs flex justify-between">
                  <span class="text-slate-400">Week 6 Validation:</span>
                  <span class="font-mono font-bold text-emerald-400">22.50 PTS (Alpha Target Share)</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Put to rest all concussion protocol doubts with a dominant 22.50-point clinic. Anchors Franky's #1 ranked league scoring offense heading into Week 7.
                </p>
              </div>
            </div>

            <!-- 3. Jonathan Taylor -->
            <div class="bg-slate-900 border border-amber-500/40 rounded-xl p-4 shadow-lg hover:border-amber-400 transition flex flex-col justify-between">
              <div>
                <div class="flex justify-between items-start mb-1.5">
                  <div>
                    <span class="font-extrabold text-white text-base">Jonathan Taylor</span>
                    <span class="text-xs text-slate-400 ml-1">(RB • IND)</span>
                  </div>
                  <span class="bg-amber-950 text-amber-400 border border-amber-800 text-[10px] font-black uppercase px-2 py-0.5 rounded tracking-wider">
                    TESTING ANKLE FOR WK 7
                  </span>
                </div>
                <div class="text-[11px] text-slate-400 mb-2">Franchise: <strong class="text-amber-400">Show me dem TDs (Eric)</strong></div>
                <div class="bg-slate-950/60 p-2 rounded border border-slate-800 mb-2 text-xs flex justify-between">
                  <span class="text-slate-400">Status:</span>
                  <span class="font-mono font-bold text-amber-400">High Ankle Sprain Rehab</span>
                </div>
                <p class="text-xs text-slate-300 leading-relaxed">
                  Has ramped up linear running drills without a walking boot. Colts coaching staff optimistic he can participate in practice and suit up for Week 7.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 10: SCOREBOARD (WEEK 6 OFFICIAL BOX SCORES)
slide_10 = """      <!-- SLIDE 10: SCOREBOARD -->
      <section id="wk6-slide-10" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-indigo-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-indigo-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 6 OFFICIAL BOX SCORES • COMPLETED MATCHUPS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚔️ Week 6 Scoreboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Final certified Sleeper results, margins of victory, and key performers.</p>
          </div>
          <div class="text-right">
            <span class="text-xs bg-slate-950 border border-slate-700 text-indigo-400 font-mono font-bold px-3 py-1 rounded-lg">5 of 5 Matchups Final</span>
          </div>
        </div>

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
                    I Didn’t Hear No Bell (Pedro) <span class="text-[10px] bg-emerald-500 text-slate-950 font-black px-1.5 py-0.5 rounded">WIN (2-4)</span>
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
              <div class="flex justify-between items-center text-xs text-slate-400 mb-1">
                <span class="font-bold text-amber-400">Matchup 3 • The 285-Point Shootout of the Year</span>
                <span class="font-mono text-amber-400 font-semibold">Margin: +14.52 PTS</span>
              </div>
              <div class="flex justify-between items-center py-2 px-3 rounded-xl bg-amber-950/30 border border-amber-500/40 mb-1.5">
                <div>
                  <div class="font-black text-white text-base flex items-center gap-2">
                    CULT OF THE LAMB (Franky) <span class="text-[10px] bg-amber-500 text-slate-950 font-black px-1.5 py-0.5 rounded">HIGH ROLLER ($10)</span>
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
      </section>"""

# SLIDE 11: WEEK 7 GAMEDAY HUB (LOOKAHEAD)
slide_11 = """      <!-- SLIDE 11: WEEK 7 GAMEDAY HUB (LOOKAHEAD) -->
      <section id="wk6-slide-11" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-red-950/60 via-slate-900 to-blue-950/60 border border-amber-500/50 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              LOOKAHEAD • WEEK 7 SCHEDULE READY
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚡ Week 7 Gameday Hub</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Upcoming head-to-head showdowns, Narrowest Victory bounty preview, and key storylines.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 7 Matchups Live</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3.5">
          <!-- Matchup 1: Pedro vs Robert -->
          <div class="bg-slate-900 border border-red-500/30 rounded-2xl p-4 shadow-xl space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-mono text-slate-400 font-bold">Matchup 1 • 5K Toilet Avoidance War</span>
              <span class="text-amber-400 font-mono font-bold">Bounty Target: Narrowest Win ($10)</span>
            </div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-slate-300 text-sm">I Didn’t Hear No Bell (Pedro)</div>
              <span class="text-xs text-red-400 font-mono font-bold">2-4</span>
            </div>
            <div class="text-center font-athletic font-black text-amber-500 text-sm">VS</div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-white text-sm">WE GOIN’ BACK 2 BACK (Robert)</div>
              <span class="text-xs text-rose-400 font-mono font-bold">2-4</span>
            </div>
            <p class="text-[11px] text-slate-400 mt-2 leading-relaxed">
              Defending champion Robert faces the 5K pace-car Pedro! Both enter at 2-4. If Pedro upsets Robert, the defending champ drops into the deepest panic of the season.
            </p>
          </div>

          <!-- Matchup 2: Franky vs Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-mono text-slate-400 font-bold">Matchup 2 • #1 Scoring Offense vs Former Champ</span>
              <span class="text-amber-400 font-mono font-bold">Shootout Potential</span>
            </div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-amber-400 text-sm">CULT OF THE LAMB (Franky)</div>
              <span class="text-xs text-amber-400 font-mono font-bold">2-4 (814.62 PF)</span>
            </div>
            <div class="text-center font-athletic font-black text-amber-500 text-sm">VS</div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-white text-sm">Amon-Ra's Maye-hem (Alex)</div>
              <span class="text-xs text-blue-400 font-mono font-bold">3-3 (775.64 PF)</span>
            </div>
            <p class="text-[11px] text-slate-400 mt-2 leading-relaxed">
              Franky's league-leading offense (814.62 PF) takes on Alex, who looks to bounce back from an upset loss to Pedro. High points guaranteed.
            </p>
          </div>

          <!-- Matchup 3: Mark vs iRob -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-mono text-slate-400 font-bold">Matchup 3 • King of the Hill</span>
              <span class="text-emerald-400 font-mono font-bold">Sole Monarch on the Line</span>
            </div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-slate-300 text-sm">Saquon Deez Nacuas (Mark)</div>
              <span class="text-xs text-slate-400 font-mono font-bold">3-3</span>
            </div>
            <div class="text-center font-athletic font-black text-amber-500 text-sm">VS</div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-emerald-400 text-sm">Njigbas in Paris (iRob)</div>
              <span class="text-xs text-emerald-400 font-mono font-bold">5-1 (1st Place)</span>
            </div>
            <p class="text-[11px] text-slate-400 mt-2 leading-relaxed">
              Mark looks to build on his Week 6 win and play giant-killer against iRob, who stands alone in 1st place with an opportunity to extend his monarch reign.
            </p>
          </div>

          <!-- Matchup 4: Joey vs Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-mono text-slate-400 font-bold">Matchup 4 • Battle of the 3-3 Titans</span>
              <span class="text-amber-400 font-mono font-bold">Combined 1,560 Season Points</span>
            </div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-white text-sm">TheGreatSwagsby (Joey)</div>
              <span class="text-xs text-blue-400 font-mono font-bold">3-3 (776.14 PF)</span>
            </div>
            <div class="text-center font-athletic font-black text-amber-500 text-sm">VS</div>
            <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
              <div class="font-bold text-white text-sm">Brock To The Future (Herrador)</div>
              <span class="text-xs text-blue-400 font-mono font-bold">3-3 (784.10 PF)</span>
            </div>
            <p class="text-[11px] text-slate-400 mt-2 leading-relaxed">
              Both squads dropped 135+ points in Week 6 and are ranked top-3 in season scoring. A marquee collision that will define playoff seeding.
            </p>
          </div>

          <!-- Matchup 5: Eric vs Arnulfo -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl space-y-2 md:col-span-2">
            <div class="flex justify-between items-center text-xs">
              <span class="font-mono text-slate-400 font-bold">Matchup 5 • Bounce-Back Battle</span>
              <span class="text-amber-400 font-mono font-bold">Playoff Positioning</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2">
              <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="font-bold text-slate-300 text-sm">Show me dem TDs (Eric)</div>
                <span class="text-xs text-blue-400 font-mono font-bold">3-3 (703.86 PF)</span>
              </div>
              <div class="flex items-center justify-between bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="font-bold text-emerald-400 text-sm">MyDakMakesHerWaddle (Arnulfo)</div>
                <span class="text-xs text-emerald-400 font-mono font-bold">4-2 (742.36 PF)</span>
              </div>
            </div>
            <p class="text-[11px] text-slate-400 mt-2 leading-relaxed">
              Both Eric and Arnulfo suffered Week 6 losses and need a victory to protect their upper-bracket standing.
            </p>
          </div>
        </div>
      </section>"""

# -------------------------------------------------------------
# 3. COMBINE ALL 12 SLIDES INTO DECK-WK6
# -------------------------------------------------------------
deck_wk6_full = f"""    <!-- ========================================== -->
    <!-- DECK 6: WEEK 6 OFFICIAL REPORT (ACTIVE)    -->
    <!-- ========================================== -->
    <div id="deck-wk6">
{slide_0}

{slide_1}

{slide_2}

{slide_3}

{slide_4}

{slide_5}

{slide_6}

{html[html.find('<section id="wk6-slide-7"'):html.find('</section>', html.find('<section id="wk6-slide-7"'))+10]}

{slide_8}

{slide_9}

{slide_10}

{slide_11}
    </div>"""

# -------------------------------------------------------------
# 4. REPLACE IN HTML
# -------------------------------------------------------------

# Replace nav pills
m_nav = re.search(r'<nav class="flex items-center gap-1\.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">[\s\S]*?</nav>', html)
if not m_nav:
    print("Error: Could not find nav pills container")
    sys.exit(1)
html = html[:m_nav.start()] + new_nav_pills + html[m_nav.end():]

# Replace deck-wk6
deck6_start = html.find('id="deck-wk6"')
if deck6_start == -1:
    deck6_start = html.find('<!-- DECK 6: WEEK 6 OFFICIAL REPORT')
else:
    # go back to the comment
    c_start = html.rfind('<!-- ==========================================', 0, deck6_start)
    if c_start != -1 and (deck6_start - c_start) < 200:
        deck6_start = c_start
    else:
        deck6_start = html.rfind('<div id="deck-wk6"', 0, deck6_start + 20)

deck5_start = html.find('<!-- ==========================================\n    DECK 5: WEEK 5 ARCHIVE REPORT')
if deck5_start == -1:
    deck5_start = html.find('id="deck-wk5"')
    c5_start = html.rfind('<!-- ==========================================', 0, deck5_start)
    if c5_start != -1 and (deck5_start - c5_start) < 200:
        deck5_start = c5_start
    else:
        deck5_start = html.rfind('<div id="deck-wk5"', 0, deck5_start + 20)

print(f"Replacing deck-wk6 from pos {deck6_start} to {deck5_start}...")
html = html[:deck6_start] + deck_wk6_full + "\n\n    " + html[deck5_start:]

# -------------------------------------------------------------
# 5. UPDATE JAVASCRIPT NAVIGATION LOGIC
# -------------------------------------------------------------
# Update totalSlides = 12
html = re.sub(r'const totalSlides\s*=\s*\d+;', 'const totalSlides = 12;', html)
html = re.sub(r'let totalSlides\s*=\s*\d+;', 'let totalSlides = 12;', html)

# In updateSlides(), make total dynamic to the active deck
update_slides_js = """function updateSlides() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      const slides = currentDeck ? currentDeck.querySelectorAll('.slide') : [];
      const deckTotal = slides.length || totalSlides;
      
      slides.forEach((el, idx) => {
        el.classList.toggle('active', idx === currentSlide);
      });
      
      const indicatorText = `Slide ${currentSlide + 1} / ${deckTotal}`;
      const topInd = document.getElementById('slideIndicator');
      if (topInd) topInd.innerText = indicatorText;
      const botInd = document.getElementById('bottomSlideIndicator');
      if (botInd) botInd.innerText = indicatorText;
      
      const pills = document.querySelectorAll('.nav-pill');
      pills.forEach((p, idx) => {
        if (idx === currentSlide) {
          p.className = 'nav-pill px-3 py-1.5 rounded-full text-xs font-bold whitespace-nowrap bg-amber-500 text-slate-950 transition';
          p.scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'center' });
        } else {
          p.className = 'nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap bg-slate-900 text-slate-400 hover:text-white transition';
        }
      });

      window.scrollTo({ top: 0, behavior: 'smooth' });
    }"""

m_us = re.search(r'function updateSlides\(\)\s*\{[\s\S]*?window\.scrollTo\(\{\s*top:\s*0,\s*behavior:\s*\'smooth\'\s*\}\);\s*\}', html)
if m_us:
    html = html[:m_us.start()] + update_slides_js + html[m_us.end():]
    print("Updated updateSlides() JS function.")
else:
    print("Warning: Could not match exact updateSlides JS function; checking alternative match...")

# Next slide / Prev slide
html = re.sub(
    r'function nextSlide\(\)\s*\{[\s\S]*?\}',
    """function nextSlide() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      const deckTotal = currentDeck ? currentDeck.querySelectorAll('.slide').length : totalSlides;
      currentSlide = (currentSlide + 1) % deckTotal;
      updateSlides();
    }""",
    html
)

html = re.sub(
    r'function prevSlide\(\)\s*\{[\s\S]*?\}',
    """function prevSlide() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      const deckTotal = currentDeck ? currentDeck.querySelectorAll('.slide').length : totalSlides;
      currentSlide = (currentSlide - 1 + deckTotal) % deckTotal;
      updateSlides();
    }""",
    html
)

with open(INDEX_PATH, "w", encoding="utf-8") as f:
    f.write(html)

print("Saved updated index.html successfully!")

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
        <button onclick="goToSlide(10)" class="nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white">11. ⚡ Wk 8 Gameday Hub</button>
      </nav>"""

# -------------------------------------------------------------
# 2. DEFINE SLIDES FOR DECK-WK7
# -------------------------------------------------------------

slide_0 = """      <!-- SLIDE 0: HARDWARE & ROASTS -->
      <section id="wk7-slide-0" class="slide active space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-500/20 via-slate-900 to-yellow-500/10 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL WEEK 7 AWARDS • F.F.U.C. HONORS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏆 Hardware & Weekly Roasts</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 7 scoring crown, $10 narrowest margin bounty, century blowout roast, and heartbreak bad beats.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-900 border border-amber-500/30 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Halfway Mark (7 of 14 Weeks)</span>
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
                    🎙️ Official League Voice • Week 7 Recap
                  </span>
                </div>
                <div class="text-white font-extrabold text-sm sm:text-base tracking-tight flex items-center gap-2">
                  <span id="broadcastTitleText">Week 7 Official Audio Recap (Commissioner's Desk)</span>
                  <!-- Animated Waveform Equalizer -->
                  <div id="audioWaveform" class="flex items-end gap-0.5 h-4 opacity-40 transition-opacity">
                    <span class="w-1 bg-amber-400 rounded-full h-2 animate-bounce" style="animation-delay: 0.1s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-4 animate-bounce" style="animation-delay: 0.3s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-3 animate-bounce" style="animation-delay: 0.2s"></span>
                    <span class="w-1 bg-amber-400 rounded-full h-1 animate-bounce" style="animation-delay: 0.4s"></span>
                  </div>
                </div>
                <div id="broadcastDescText" class="text-xs text-slate-400 mt-0.5">
                  Robert's 153.82 High Roller explosion, Pedro's historic 101.50-point blowout humiliation, Arnulfo's $10 bounty thriller, and the 5-way logjam at 3-4.
                </div>
              </div>
            </div>

            <!-- Right Controls: Progress Bar & Duration -->
            <div class="flex flex-col sm:items-end justify-center gap-1.5 min-w-[200px]">
              <div class="flex items-center justify-between sm:justify-end gap-3 text-xs font-mono w-full">
                <span id="audioCurrentTime" class="text-amber-400 font-bold">0:00</span>
                <span class="text-slate-600">/</span>
                <span id="audioDuration" class="text-slate-400">0:47</span>
              </div>
              <div class="w-full bg-slate-950 rounded-full h-2 border border-slate-800 cursor-pointer overflow-hidden" onclick="seekBroadcastAudio(event)">
                <div id="audioProgressBar" class="bg-gradient-to-r from-amber-500 to-yellow-400 h-full w-0 rounded-full transition-all duration-100"></div>
              </div>
              <span class="text-[10px] text-slate-500 font-mono">Natural Voice Broadcast • Click to stream</span>
            </div>
          </div>
          <!-- Audio Element -->
          <audio id="broadcastAudio" src="assets/audio/wk7_recap.mp3" preload="metadata" ontimeupdate="updateBroadcastProgress()" onended="onBroadcastAudioEnded()"></audio>
        </div>

        <!-- AWARDS GRID -->
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Award 1: High Roller Champion -->
          <div class="bg-gradient-to-br from-amber-950/40 via-slate-900 to-slate-900 border-2 border-amber-500/60 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-amber-500 text-slate-950 px-2.5 py-0.5 rounded">👑 Week 7 High Roller Champion</span>
              <span class="text-xl font-athletic font-bold text-amber-400">153.82 PTS</span>
            </div>
            <h3 class="text-xl font-black text-white">WE NOT GOIN’ BACK 2 BACK <span class="text-amber-400 text-sm font-semibold">(Robert)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Defending champ Robert unleashes the single most ferocious offensive avalanche of the week! Led by Tony Pollard's league-leading 35.00-point explosion, Kyren Williams (17.10), Drake London (16.10), Bijan Robinson (14.70), and Devaughn Vele (13.90), Robert collects the $10 High Roller bounty and escapes the cellar in emphatic style!
            </p>
            <!-- FaceFusion AI Coronation Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-amber-500/40 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-amber-500/40 text-[9px] font-mono font-bold text-amber-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-amber-400 animate-pulse"></span>
                FaceFusion AI Video • Robert Coronation Toast
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline poster="assets/video/robert_high_roller.gif?v=20261027">
                <source src="assets/video/robert_high_roller.mp4?v=20261027" type="video/mp4">
                <img src="assets/video/robert_high_roller.gif?v=20261027" alt="Robert High Roller Meme" class="w-full h-44 sm:h-52 object-cover">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Week 7 High Score: 153.82 PTS</span>
              <span class="text-amber-400 font-bold font-mono">+$10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 2: $10 Bounty Winner (Narrowest Margin) -->
          <div class="bg-gradient-to-br from-emerald-950/40 via-slate-900 to-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-emerald-500 text-slate-950 px-2.5 py-0.5 rounded">⚡ $10 Weekly Bounty: Narrowest Margin</span>
              <span class="text-xl font-athletic font-bold text-emerald-400">2.98 PTS Margin</span>
            </div>
            <h3 class="text-xl font-black text-white">The Latin Touch / MyDakMakesHerWaddle <span class="text-emerald-400 text-sm font-semibold">(Arnulfo)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Heart-stopping Monday night drama! Arnulfo survived a nail-biter against Eric, holding on for a razor-thin 112.28 to 109.30 victory. Behind Dak Prescott (23.28) and Rhamondre Stevenson (20.00), Arnulfo took the win by just 2.98 points—earning the $10 cash bounty and seizing a share of 1st place in FFUC!
            </p>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Margin of Victory: 2.98 PTS (over Eric)</span>
              <span class="text-emerald-400 font-bold font-mono">Arnulfo: $10 Direct Bounty</span>
            </div>
          </div>

          <!-- Award 3: Heartbreak Bad Beat (Alex) -->
          <div class="bg-gradient-to-br from-rose-950/40 via-slate-900 to-slate-900 border border-rose-500/40 rounded-2xl p-5 shadow-xl">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-bold uppercase tracking-wider bg-rose-950 text-rose-300 border border-rose-800 px-2.5 py-0.5 rounded">💔 Heartbreak of the Week</span>
              <span class="text-lg font-athletic font-bold text-rose-400">129.54 PTS (L)</span>
            </div>
            <h3 class="text-xl font-black text-white">Amon-Ra's Maye-hem <span class="text-rose-400 text-sm font-semibold">(Alex)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              Alex put up a sterling 129.54 points—the 4th highest tally in the entire league this week—powered by rookie Drake Maye's 28.44-point breakout! In almost any other matchup, Alex cruises to victory (defeating 6 out of 9 FFUC squads), but he had the terrible misfortune of running straight into Franky's 150.02 blitzkrieg!
            </p>
            <!-- FaceFusion AI Heartbreak Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-rose-500/40 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-rose-500/40 text-[9px] font-mono font-bold text-rose-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-rose-400 animate-pulse"></span>
                FaceFusion AI Video • Alex Dawson Crying Meme
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline poster="assets/video/alex_heartbreak.gif?v=20261027">
                <source src="assets/video/alex_heartbreak.mp4?v=20261027" type="video/mp4">
                <img src="assets/video/alex_heartbreak.gif?v=20261027" alt="Alex Heartbreak Crying Meme" class="w-full h-44 sm:h-52 object-cover">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-slate-400 font-mono">Defeated by: Franky (150.02)</span>
              <span class="text-rose-400 font-bold font-mono">Would Defeat 6 of 9 Teams</span>
            </div>
          </div>

          <!-- Award 4: 5K Toilet Runner of the Week (Pedro - 100-Point Blowout!) -->
          <div class="bg-gradient-to-br from-red-950/40 via-slate-900 to-slate-900 border-2 border-red-600/70 rounded-2xl p-5 shadow-2xl relative overflow-hidden">
            <div class="flex items-center justify-between mb-3">
              <span class="text-xs font-mono font-black uppercase tracking-wider bg-red-600 text-white px-2.5 py-0.5 rounded shadow">🚽 5K Toilet Runner: CENTURY BLOWOUT</span>
              <span class="text-lg font-athletic font-bold text-red-400">52.32 PTS (-101.50)</span>
            </div>
            <h3 class="text-xl font-black text-white">I Didn’t Hear No Bell <span class="text-red-400 text-sm font-semibold">(Pedro)</span></h3>
            <p class="text-xs text-slate-300 mt-2 leading-relaxed">
              <strong class="text-red-400">HISTORIC 101.50-POINT HUMILIATION:</strong> Pedro didn't just lose—he suffered the worst beatdown in modern FFUC history! Pedro managed an abysmal 52.32 points while Robert dropped 153.82, losing by a staggering <strong>101.50 points</strong>! With Garrett Wilson (3.60), Xavier Worthy (2.60), and Roschon Johnson (1.30) doing next to nothing, Pedro sits isolated at 2-5 with $0 FAAB and trails 9th place by 210.28 total points!
            </p>
            <!-- 5K Runner Video -->
            <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950">
              <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                FaceFusion AI Meme • Pedro 100-Pt Blowout 5K Sprint
              </div>
              <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline>
                <source src="assets/video/pedro_5k_runner.mp4?v=20261027" type="video/mp4">
              </video>
            </div>
            <div class="mt-3.5 pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
              <span class="text-red-400 font-mono font-bold">Deficit: -101.50 PTS (Century Club)</span>
              <span class="text-red-400 font-bold font-mono">Record: 2-5 ($0 FAAB Left)</span>
            </div>
          </div>
        </div>
      </section>"""

print("Slide 0 built successfully.")

# SLIDE 1: STATE OF THE UNION & STANDINGS
slide_1 = """      <!-- SLIDE 1: STATE OF THE UNION -->
      <section id="wk7-slide-1" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-indigo-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 7 LEAGUE AUDIT • COMMISSIONER'S DESK
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🏛️ State of the Union: Week 7</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Arnulfo & iRob co-lead at 5-2, Robert delivers a historic 101.50-point century blowout over Pedro, and a ferocious 5-way logjam forms at 3-4.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-blue-400 font-mono font-bold px-3 py-1 rounded-lg">Halfway Mark: 7 of 14 Complete</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">👑 Co-Leaders (5-2)</span>
            <div class="text-base font-bold text-white mt-1">Arnulfo & iRob At The Summit</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Arnulfo (854.64 PF) survived a 2.98-pt thriller over Eric while iRob (850.78 PF) fell to Mark's 145-pt barrage. Both franchises now share 1st place at 5-2 and will clash head-to-head in Week 8 for solo dominance!
            </p>
          </div>

          <div class="bg-slate-900 border border-blue-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-blue-400">⚔️ Midfield Mayhem</span>
            <div class="text-base font-bold text-white mt-1">5 Franchises Logjammed at 3-4</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Total postseason anarchy! Franky (964.64 PF - #1 offense!), Robert (908.36 PF), Alex (905.18 PF), Herrador (886.02 PF), and Eric (813.16 PF) are all locked at 3-4 fighting tooth-and-nail for the 6-team playoff bracket!
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/30 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">🔥 Century Blowout & Isolation</span>
            <div class="text-base font-bold text-white mt-1">Pedro Crushed by 101.50 PTS</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Robert demolished Pedro 153.82 to 52.32—the largest blowout in modern league annals. Pedro sits completely stranded in the cellar at 2-5 with $0 FAAB, trailing 9th-place Eric by a staggering 210.28 total points!
            </p>
          </div>
        </div>

        <!-- Standings Snapshot Grid (OFFICIAL SLEEPER WEEK 7 STANDINGS) -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Official Week 7 Standings Snapshot (Halfway Mark)</span>
            <span class="font-mono text-slate-400">W-L Record • Points For • Points Against • FAAB</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-8 font-bold text-emerald-400">1</span>
              <span class="flex-1 font-bold text-white">The Latin Touch (Arnulfo)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">5-2</span>
              <span class="w-20 text-right text-slate-300">854.64 PF</span>
              <span class="w-20 text-right text-slate-500">829.48 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$34</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-8 font-bold text-emerald-400">2</span>
              <span class="flex-1 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-16 text-center text-emerald-400 font-bold">5-2</span>
              <span class="w-20 text-right text-slate-300">850.78 PF</span>
              <span class="w-20 text-right text-slate-500">849.10 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$80</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-blue-950/20">
              <span class="w-8 font-bold text-blue-400">3</span>
              <span class="flex-1 font-semibold text-slate-200">TheGreatSwagsby (Joey)</span>
              <span class="w-16 text-center text-blue-400 font-bold">4-3</span>
              <span class="w-20 text-right text-slate-300">889.96 PF</span>
              <span class="w-20 text-right text-slate-500">787.46 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$23</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-blue-950/15">
              <span class="w-8 font-bold text-blue-400">4</span>
              <span class="flex-1 font-semibold text-slate-200">Saquon Deez Nacuas (Mark)</span>
              <span class="w-16 text-center text-blue-400 font-bold">4-3</span>
              <span class="w-20 text-right text-slate-300">837.78 PF</span>
              <span class="w-20 text-right text-slate-500">829.60 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$80</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">5</span>
              <span class="flex-1 text-slate-300">CULT OF THE LAMB (Franky) <span class="text-amber-400 font-bold text-[10px]">#1 PF</span></span>
              <span class="w-16 text-center text-rose-400 font-bold">3-4</span>
              <span class="w-20 text-right text-amber-400 font-extrabold">964.64 PF</span>
              <span class="w-20 text-right text-slate-500">964.22 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$41</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">6</span>
              <span class="flex-1 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-4</span>
              <span class="w-20 text-right text-slate-300">908.36 PF</span>
              <span class="w-20 text-right text-slate-500">827.80 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$83</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">7</span>
              <span class="flex-1 text-slate-300">Amon-Ra's Maye-hem (Alex)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-4</span>
              <span class="w-20 text-right text-slate-300">905.18 PF</span>
              <span class="w-20 text-right text-slate-500">883.94 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$60</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">8</span>
              <span class="flex-1 text-slate-300">Brock To The Future (Herrador)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-4</span>
              <span class="w-20 text-right text-slate-300">886.02 PF</span>
              <span class="w-20 text-right text-slate-500">843.70 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$51</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">9</span>
              <span class="flex-1 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-16 text-center text-rose-400 font-bold">3-4</span>
              <span class="w-20 text-right text-slate-300">813.16 PF</span>
              <span class="w-20 text-right text-slate-500">829.44 PA</span>
              <span class="w-16 text-right text-amber-400 font-bold">$54</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-red-950/30">
              <span class="w-8 font-bold text-red-500">10</span>
              <span class="flex-1 font-medium text-red-400">I Didn’t Hear No Bell (Pedro) <span class="text-red-500 text-[10px] font-bold">(-210.28 PF Deficit)</span></span>
              <span class="w-16 text-center text-red-500 font-bold">2-5</span>
              <span class="w-20 text-right text-red-400 font-extrabold">602.88 PF</span>
              <span class="w-20 text-right text-slate-500">868.66 PA</span>
              <span class="w-16 text-right text-red-500 font-black">$0</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 2: $10 WEEKLY BOUNTY BOARD
slide_2 = """      <!-- SLIDE 2: $10 BOUNTY BOARD -->
      <section id="wk7-slide-2" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-green-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEKLY PRIZE POOL • DIRECT CASH PAYOUTS
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💵 $10 Weekly Bounty Board</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Week 7 Narrowest Margin of Victory crowned; Week 8 Largest Blowout bounty on deck.</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-emerald-400">$140.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Season Bounty Pot</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Week 7 Winner Card -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl relative overflow-hidden">
            <div class="absolute top-0 right-0 bg-emerald-500 text-slate-950 text-xs font-extrabold px-3 py-1 rounded-bl-xl shadow">
              Bounty Collected ($10)
            </div>
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400">Week 7 Target: Narrowest Margin of Victory</span>
              <h3 class="text-2xl font-black text-white mt-1">Arnulfo • 2.98 PTS Margin</h3>
              <div class="text-xs text-slate-400 mt-0.5">Franchise: <strong class="text-slate-200">The Latin Touch / MyDakMakesHerWaddle</strong></div>

              <div class="my-4 p-3 bg-emerald-950/40 border border-emerald-500/30 rounded-xl space-y-2">
                <div class="text-xs text-emerald-300 font-semibold">⚡ The Monday Night Thriller:</div>
                <div class="text-xs text-slate-300 leading-relaxed">
                  Arnulfo entered Monday night sweating a furious rally by Eric. When the final whistle blew, Arnulfo held on by exactly 2.98 points (112.28 to 109.30) to collect the $10 cash bounty and secure his tie for 1st place!
                </div>
              </div>

              <!-- Top 5 Narrowest Margins in Week 7 -->
              <div class="space-y-1.5 text-xs font-mono">
                <div class="flex justify-between items-center bg-slate-950 p-2 rounded-lg border border-emerald-500/40">
                  <span class="font-bold text-emerald-400">1. Arnulfo def. Eric</span>
                  <span class="font-black text-white">2.98 PTS (WON $10)</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>2. Joey def. Herrador</span>
                  <span class="font-bold text-amber-400">11.90 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>3. Franky def. Alex</span>
                  <span>20.48 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800">
                  <span>4. Mark def. iRob</span>
                  <span>41.08 PTS</span>
                </div>
                <div class="flex justify-between items-center bg-slate-950/60 p-2 rounded-lg border border-slate-800 text-red-400">
                  <span>5. Robert def. Pedro</span>
                  <span class="font-bold">101.50 PTS (Century Blowout!)</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Payout Method: League Safe / Direct</span>
              <span class="text-emerald-400 font-bold">$10.00 Sent to Arnulfo</span>
            </div>
          </div>

          <!-- Season Bounty Schedule & Leaderboard -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl flex flex-col justify-between">
            <div>
              <span class="text-xs font-mono font-bold uppercase tracking-wider text-amber-400">2026 Bounty Master Schedule</span>
              <h3 class="text-xl font-black text-white mt-1">7 of 14 Bounties Claimed ($70.00 Paid)</h3>

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
                <div class="py-1.5 flex justify-between items-center bg-emerald-950/30 px-2 rounded border border-emerald-500/30 text-white">
                  <span class="font-bold">Wk 7: Narrowest Victory</span>
                  <span class="text-emerald-400 font-bold">Arnulfo (2.98 Margin) • $10</span>
                </div>
                <div class="py-1.5 flex justify-between items-center bg-amber-950/30 px-2 rounded border border-amber-500/30 text-amber-300">
                  <span class="font-bold">Wk 8: Largest Blowout</span>
                  <span class="text-amber-400 font-bold">🔒 Up for Grabs ($10)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Next Bounty: Week 8 Largest Margin</span>
              <span class="text-amber-400 font-bold">$10.00 Target</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 3: THE BAR TAB & 5K TOILET METER
slide_3 = """      <!-- SLIDE 3: THE BAR TAB & 5K TOILET METER -->
      <section id="wk7-slide-3" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-red-950/80 via-slate-900 to-rose-950/80 border border-red-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-red-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              THE LAST PLACE PUNISHMENT WATCH • THE TOILET RUN
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍻 The Bar Tab & 5K Toilet Meter</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Live tracking of the FFUC Last Place in-person 5K Run and open bar tab liability.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-red-400 font-mono font-bold px-3 py-1 rounded-lg">High Risk Alert: Pedro (2-5, 602 PF)</span>
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
                <span class="text-lg font-athletic font-bold text-red-400">2-5 • 602.88 PF</span>
              </div>
              <h3 class="text-2xl font-black text-white">I Didn’t Hear No Bell <span class="text-red-400 text-sm font-semibold">(Pedro)</span></h3>
              <p class="text-xs text-slate-300 mt-2 leading-relaxed">
                <strong class="text-red-400">THE 100-POINT MASSACRE:</strong> Pedro was humiliated in Week 7, scoring 52.32 and losing by 101.50 PTS to Robert! With a season total of just 602.88 PF, Pedro is a monstrous <strong>210.28 points behind 9th place Eric</strong>. To make matters worse, Pedro has exactly $0 in FAAB remaining, rendering him virtually helpless on the waiver wire!
              </p>

              <!-- LivePortrait AI 5K Punishment Video -->
              <div class="mt-3 relative rounded-xl overflow-hidden border border-red-500/50 shadow-lg bg-slate-950">
                <div class="absolute top-2 left-2 z-10 bg-slate-950/80 backdrop-blur-sm border border-red-500/50 text-[9px] font-mono font-bold text-red-400 px-2 py-0.5 rounded-full flex items-center gap-1">
                  <span class="w-1.5 h-1.5 rounded-full bg-red-400 animate-pulse"></span>
                  FaceFusion AI Meme • Pedro Forrest Gump 5K Punishment Sprint
                </div>
                <video class="w-full h-44 sm:h-52 object-cover" autoplay loop muted playsinline>
                  <source src="assets/video/pedro_5k_runner.mp4?v=20261027" type="video/mp4">
                </video>
              </div>

              <div class="mt-4 p-3 bg-red-950/30 border border-red-800/40 rounded-xl space-y-2 text-xs">
                <div class="flex justify-between items-center text-slate-300">
                  <span>Projected 5K Finishing Time:</span>
                  <span class="font-mono font-bold text-red-400">1 Hour 15 Mins (24:10/mi)</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Open Bar Tab Meter Liability:</span>
                  <span class="font-mono font-bold text-amber-400">$275.00 Est.</span>
                </div>
                <div class="flex justify-between items-center text-slate-300">
                  <span>Distance to 9th Place Safety:</span>
                  <span class="font-mono font-bold text-red-400">210.28 Total Points Deficit</span>
                </div>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Punishment Likelihood:</span>
              <span class="text-red-400 font-bold uppercase">95.8% Implied Probability</span>
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
                  <span>Eric (3-4):</span>
                  <span class="text-amber-400 font-mono font-bold">813.16 PF (38% Risk)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Herrador (3-4):</span>
                  <span class="text-slate-300 font-mono font-bold">886.02 PF (14% Risk)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Alex (3-4):</span>
                  <span class="text-slate-300 font-mono font-bold">905.18 PF (8% Risk)</span>
                </div>
                <div class="flex justify-between text-slate-300">
                  <span>Robert (3-4):</span>
                  <span class="text-emerald-400 font-mono font-bold">908.36 PF (Cushion Rebuilt)</span>
                </div>
              </div>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Next In Line Danger:</span>
              <span class="text-amber-400 font-bold">Eric (3-4 • 813.16 PF)</span>
            </div>
          </div>
        </div>
      </section>"""

print("Slides 1-3 built.")

# SLIDE 4: THE LUCK INDEX
slide_4 = """      <!-- SLIDE 4: THE LUCK INDEX -->
      <section id="wk7-slide-4" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-purple-950/80 via-slate-900 to-indigo-950/80 border border-purple-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-purple-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ADVANCED ANALYTICS • ALL-PLAY CORRELATION
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🍀 The Luck Index: Schedule Variance</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Expected Wins vs Actual Wins across 63 total all-play matchups per franchise through Week 7.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-purple-400 font-mono font-bold px-3 py-1 rounded-lg">63 Total Games Audited</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-emerald-400">🍀 The Luckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">iRob (+1.56) & Arnulfo (+1.33) & Pedro (+1.11)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob and Arnulfo both co-lead FFUC at 5-2 despite expected win totals of just 3.44 and 3.67. Meanwhile, Pedro's 2 wins are mathematically lucky—his 8-55 all-play record yields an expected win count of only 0.89!
            </p>
          </div>

          <div class="bg-slate-900 border border-rose-500/40 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-rose-400">💀 The Unluckiest Franchises</span>
            <div class="text-lg font-black text-white mt-1">Franky (-1.78) & Alex (-1.00)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Franky continues to suffer the cruellest schedule variance in FFUC history! He owns the #1 all-play record (43-20) and #1 scoring offense (964.64 PF), yet sits at 3-4 (-1.78 luck). Alex also suffers at -1.00 below expectation.
            </p>
          </div>
        </div>

        <!-- Luck Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Expected Wins Matrix (Week 7 Audit)</span>
            <span class="font-mono text-purple-400 font-bold">Actual vs Expected Delta</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/20">
              <span class="w-48 font-bold text-white">Njigbas in Paris (iRob)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">5-2 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.44 (Exp)</span>
              <span class="w-28 text-center text-slate-300">31-32 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.56 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/15">
              <span class="w-48 font-bold text-white">The Latin Touch (Arnulfo)</span>
              <span class="w-20 text-center text-emerald-400 font-bold">5-2 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.67 (Exp)</span>
              <span class="w-28 text-center text-slate-300">33-30 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.33 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-emerald-950/10">
              <span class="w-48 font-bold text-slate-300">I Didn’t Hear No Bell (Pedro)</span>
              <span class="w-20 text-center text-red-400 font-bold">2-5 (Act)</span>
              <span class="w-20 text-center text-slate-400">0.89 (Exp)</span>
              <span class="w-28 text-center text-red-400">8-55 All-Play</span>
              <span class="w-24 text-right text-emerald-400 font-bold">+1.11 🍀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">Saquon Deez Nacuas (Mark)</span>
              <span class="w-20 text-center text-blue-400 font-bold">4-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.56 (Exp)</span>
              <span class="w-28 text-center text-slate-300">32-31 All-Play</span>
              <span class="w-24 text-right text-slate-300">+0.44 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">Show me dem TDs (Eric)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">2.89 (Exp)</span>
              <span class="w-28 text-center text-slate-300">26-37 All-Play</span>
              <span class="w-24 text-right text-slate-300">+0.11 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-48 text-slate-300">TheGreatSwagsby (Joey)</span>
              <span class="w-20 text-center text-blue-400 font-bold">4-3 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.22 (Exp)</span>
              <span class="w-28 text-center text-slate-300">38-25 All-Play</span>
              <span class="w-24 text-right text-slate-400">-0.22 ⚖️</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-48 text-slate-300">Brock To The Future (Herrador)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">34-29 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.78 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/10">
              <span class="w-48 text-slate-300">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">3.78 (Exp)</span>
              <span class="w-28 text-center text-slate-300">34-29 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-0.78 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/20">
              <span class="w-48 font-bold text-white">Amon-Ra's Maye-hem (Alex)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.00 (Exp)</span>
              <span class="w-28 text-center text-slate-300">36-27 All-Play</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.00 💀</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-rose-950/30">
              <span class="w-48 font-bold text-white">CULT OF THE LAMB (Franky)</span>
              <span class="w-20 text-center text-rose-400 font-bold">3-4 (Act)</span>
              <span class="w-20 text-center text-slate-400">4.78 (Exp)</span>
              <span class="w-28 text-center text-amber-400 font-extrabold">43-20 All-Play (1st)</span>
              <span class="w-24 text-right text-rose-400 font-bold">-1.78 💀</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 5: POWER RANKINGS
slide_5 = """      <!-- SLIDE 5: POWER RANKINGS -->
      <section id="wk7-slide-5" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-amber-950/80 via-slate-900 to-orange-950/80 border border-amber-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-amber-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              ANALYTIC POWER INDEX • STRENGTH OF SQUAD
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">📈 Power Rankings: Week 7</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">True hierarchy based on roster firepower, all-play strength, and momentum entering Week 8.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-amber-400 font-mono font-bold px-3 py-1 rounded-lg">Week 7 Audit</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- Rank 1: Franky -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">1</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">CULT OF THE LAMB (Franky)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (3-4) • 205.2 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                964.64 PF (#1 in scoring!). Put up 150.02 PTS to defeat Alex. Franky has the highest scoring offense and #1 all-play record (43-20). The record says 3-4, but this is the most lethal team in FFUC.
              </p>
            </div>
          </div>

          <!-- Rank 2: Arnulfo -->
          <div class="bg-slate-900 border border-amber-500/40 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-amber-400">2</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">The Latin Touch (Arnulfo)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +3 (5-2) • 199.4 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                854.64 PF. Survived a 2.98-pt thriller over Eric to claim the $10 narrowest victory bounty and a share of 1st place. Dak Prescott (23.28) and Rhamondre (20.00) are rolling.
              </p>
            </div>
          </div>

          <!-- Rank 3: Joey -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-200">3</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">TheGreatSwagsby (Joey)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +1 (4-3) • 198.9 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                889.96 PF (#3 in scoring!). Bounced back with a 113.82 to 101.92 win over Herrador. CMC (19.00), Ollie Gordon (16.80), and Braelon Allen (16.40) keep the backfield humming.
              </p>
            </div>
          </div>

          <!-- Rank 4: iRob -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">4</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Njigbas in Paris (iRob)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -3 (5-2) • 195.9 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                850.78 PF. Suffered a 145.20 to 104.12 defeat to Mark to lose sole possession of 1st place. Left Joe Burrow's 28.88 points on his bench. Faces Arnulfo for 1st place in Week 8.
              </p>
            </div>
          </div>

          <!-- Rank 5: Robert -->
          <div class="bg-slate-900 border border-emerald-500/40 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-emerald-400">5</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +5 (3-4) • 194.4 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                908.36 PF. Biggest riser in FFUC! Exploded for a week-leading 153.82 PTS behind Tony Pollard (35.00) to crush Pedro by 101.50 PTS. Defending champ is officially awake.
              </p>
            </div>
          </div>

          <!-- Rank 6: Mark -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">6</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                <span class="text-emerald-400 font-mono font-bold">▲ +2 (4-3) • 191.2 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                837.78 PF. Stunned 1st-place iRob with a 145.20 masterclass! Zay Flowers (23.70), Russell Wilson (21.70), and Saquon Barkley (16.20) propelled Mark to his 2nd straight victory.
              </p>
            </div>
          </div>

          <!-- Rank 7: Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-300">7</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Amon-Ra's Maye-hem (Alex)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -1 (3-4) • 190.4 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                905.18 PF (#4 in scoring). Scored 129.54 PTS in a tough loss to Franky. Drake Maye (28.44) looks like a superstar starter, but Alex falls into the dangerous 3-4 logjam.
              </p>
            </div>
          </div>

          <!-- Rank 8: Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-400">8</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Brock To The Future (Herrador)</span>
                <span class="text-rose-400 font-mono font-bold">▼ -5 (3-4) • 182.9 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                886.02 PF. Slipped with 101.92 PTS in an 11.90-pt loss to Joey. Bucky Irving (23.50) and D'Andre Swift (17.00) shined, but Tyler Shough and the WR room sputtered.
              </p>
            </div>
          </div>

          <!-- Rank 9: Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-slate-500">9</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-white text-sm">Show me dem TDs (Eric)</span>
                <span class="text-slate-400 font-mono font-bold">― 0 (3-4) • 168.3 Pwr</span>
              </div>
              <p class="text-slate-300 mt-1 leading-relaxed">
                813.16 PF. Suffered a brutal 2.98-pt loss to Arnulfo (109.30 to 112.28) for his 3rd straight defeat. Tee Higgins (23.80) and Jameson Williams (23.60) had big days, but Sam LaPorta (2.30) disappointed.
              </p>
            </div>
          </div>

          <!-- Rank 10: Pedro -->
          <div class="bg-slate-900 border-2 border-red-600/70 rounded-xl p-3.5 shadow-lg flex items-start gap-3">
            <span class="text-2xl font-athletic font-black text-red-500">10</span>
            <div class="flex-1">
              <div class="flex justify-between items-center">
                <span class="font-bold text-red-400 text-sm">I Didn’t Hear No Bell (Pedro)</span>
                <span class="text-red-500 font-mono font-bold">― 0 (2-5) • 106.0 Pwr</span>
              </div>
              <p class="text-slate-400 mt-1 leading-relaxed">
                602.88 PF (210.28 PF behind 9th place!). Suffered an all-time 101.50-point blowout loss (52.32 PTS). Sits on $0 FAAB and faces league scoring leader Franky in Week 8.
              </p>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 6: FAAB RECEIPTS & WAIVER LEDGER
slide_6 = """      <!-- SLIDE 6: FAAB RECEIPTS -->
      <section id="wk7-slide-6" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-teal-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-500 text-slate-950 text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              FINANCIAL AUDIT • WAIVER TRANSACTION WIRE
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💰 FAAB Receipts: Week 7 Ledger</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official transaction ledger and updated bankrolls through Week 7 waivers.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">Budget Cap: $100 FAAB</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- Recent Key Transactions -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded">
              Week 7 Key Wire Pickups
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tre Tucker (WR • LV)</strong>
                  <span class="block text-slate-400 text-[11px]">The Latin Touch (Arnulfo) — Free Agent Acquisition</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tyler Allgeier (RB • ARI)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark) — Free Agent Acquisition</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-amber-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Harold Fannin (TE • CLE)</strong>
                  <span class="block text-slate-400 text-[11px]">WE NOT GOIN’ BACK 2 BACK (Robert) — Scored 10.10 in starting TE slot!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-300 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Free Agent</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Drake Maye (QB • NE)</strong>
                  <span class="block text-slate-400 text-[11px]">Amon-Ra's Maye-hem (Alex) — Erupted for 28.44 PTS in starting lineup!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-slate-400 font-bold">$0 FAAB</span>
                  <span class="block text-slate-500 text-[10px]">Roster Active</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Colston Loveland (TE • CHI)</strong>
                  <span class="block text-slate-400 text-[11px]">CULT OF THE LAMB (Franky) — Key piece in 150-pt shootout</span>
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
                <span class="text-slate-300">2. iRob (Njigbas in Paris)</span>
                <span class="text-emerald-400 font-bold">$80 (80%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">3. Mark (Saquon Deez Nacuas)</span>
                <span class="text-emerald-400 font-bold">$80 (80%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">4. Alex (Amon-Ra's Maye-hem)</span>
                <span class="text-amber-400 font-bold">$60 (60%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">5. Eric (Show me dem TDs)</span>
                <span class="text-amber-400 font-bold">$54 (54%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">6. Herrador (Brock To The Future)</span>
                <span class="text-amber-400 font-bold">$51 (51%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">7. Franky (CULT OF THE LAMB)</span>
                <span class="text-amber-400 font-bold">$41 (41%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">8. Arnulfo (The Latin Touch)</span>
                <span class="text-rose-400 font-bold">$34 (34%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center">
                <span class="text-slate-300">9. Joey (TheGreatSwagsby)</span>
                <span class="text-rose-400 font-bold">$23 (23%)</span>
              </div>
              <div class="py-1.5 flex justify-between items-center bg-red-950/30 px-2 rounded">
                <span class="text-red-400 font-bold">10. Pedro (I Didn’t Hear No Bell)</span>
                <span class="text-red-500 font-black">$0 (BROKE - 0%)</span>
              </div>
            </div>
            <div class="mt-4 pt-3 border-t border-slate-800 flex justify-between text-xs text-slate-400">
              <span>Financial Health:</span>
              <span class="text-amber-400 font-mono">Pedro has $0 to fix -210 PF hole</span>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 7: PICK-EM LEADERBOARD ($45 POT)
slide_7 = """      <!-- SLIDE 7: PICK-EM LEADERBOARD -->
      <section id="wk7-slide-7" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-blue-950/80 via-slate-900 to-cyan-950/80 border border-blue-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-blue-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL SLEEPER PICK-EM POOL • $45 CASH POT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">🎯 F.F.U.C. Pick-em Leaderboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Arnulfo takes solo 1st place at 67.0 PTS, Robert trails by 1 point, and iRob sits 2 back.</p>
          </div>
          <div class="text-right">
            <span class="text-2xl font-black font-athletic text-blue-400">$45.00</span>
            <div class="text-[10px] uppercase font-bold text-slate-400">Winner Takes All Pot</div>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-3">
          <div class="bg-slate-900 border-2 border-amber-500/50 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-amber-400">🥇 Solo 1st Place</span>
            <div class="text-base font-bold text-white mt-1">Arnulfo (67.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Arnulfo posted a sterling 9-win Week 7 to pull ahead of the pack and claim exclusive possession of 1st place!
            </p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-300">🥈 2nd Place Chaser</span>
            <div class="text-base font-bold text-white mt-1">Robert (66.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              Robert put up 8 points in Week 7, sitting just 1 point back of Arnulfo in the $45 jackpot race.
            </p>
          </div>

          <div class="bg-slate-900 border border-slate-800 rounded-xl p-4 shadow-lg">
            <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-slate-400">🥉 3rd Place Contender</span>
            <div class="text-base font-bold text-white mt-1">iRob (65.0 PTS)</div>
            <p class="text-xs text-slate-300 mt-1 leading-relaxed">
              iRob scored 9 points in Week 7, staying within striking distance just 2 points off the lead.
            </p>
          </div>
        </div>

        <!-- Official Pick-em Table -->
        <div class="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-xl">
          <div class="p-3 border-b border-slate-800 flex justify-between items-center bg-slate-950/60 text-xs">
            <span class="font-bold uppercase tracking-wider text-slate-300">Certified Sleeper Standings Through Week 7</span>
            <span class="font-mono text-blue-400 font-bold">Total Correct Picks • W7 Score</span>
          </div>
          <div class="divide-y divide-slate-800/80 text-xs font-mono">
            <div class="p-2.5 flex items-center justify-between bg-amber-950/20">
              <span class="w-8 font-bold text-amber-400">1</span>
              <span class="flex-1 font-bold text-white">Arnulfo (AEscamilla94)</span>
              <span class="w-24 text-center text-slate-400">W7: 9.0 PTS</span>
              <span class="w-28 text-right text-amber-400 font-extrabold text-sm">67.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-300">2</span>
              <span class="flex-1 font-semibold text-slate-200">Robert (YaBoyRoZ)</span>
              <span class="w-24 text-center text-slate-400">W7: 8.0 PTS</span>
              <span class="w-28 text-right text-emerald-400 font-bold">66.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">3</span>
              <span class="flex-1 text-slate-300">iRob (irobgarza16)</span>
              <span class="w-24 text-center text-slate-400">W7: 9.0 PTS</span>
              <span class="w-28 text-right text-slate-200 font-bold">65.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">4</span>
              <span class="flex-1 text-slate-300">Herrador (DirtyDirties)</span>
              <span class="w-24 text-center text-slate-400">W7: 8.0 PTS</span>
              <span class="w-28 text-right text-slate-300">64.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">5</span>
              <span class="flex-1 text-slate-300">Joey (TheGreatSwagsby)</span>
              <span class="w-24 text-center text-slate-400">W7: 9.0 PTS</span>
              <span class="w-28 text-right text-slate-300">62.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">6</span>
              <span class="flex-1 text-slate-300">Franky (ChanciscoFravez)</span>
              <span class="w-24 text-center text-slate-400">W7: 8.0 PTS</span>
              <span class="w-28 text-right text-slate-300">62.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">7</span>
              <span class="flex-1 text-slate-300">Pedro (GuyNamedPedro)</span>
              <span class="w-24 text-center text-slate-400">W7: 7.0 PTS</span>
              <span class="w-28 text-right text-slate-400">61.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">8</span>
              <span class="flex-1 text-slate-300">Eric (emedina13)</span>
              <span class="w-24 text-center text-slate-400">W7: 8.0 PTS</span>
              <span class="w-28 text-right text-slate-400">61.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-400">9</span>
              <span class="flex-1 text-slate-300">Alex (abarrera731)</span>
              <span class="w-24 text-center text-slate-400">W7: 7.0 PTS</span>
              <span class="w-28 text-right text-slate-400">60.0 PTS</span>
            </div>
            <div class="p-2.5 flex items-center justify-between bg-slate-900">
              <span class="w-8 font-bold text-slate-500">10</span>
              <span class="flex-1 text-slate-400">Mark (fattymcfatty)</span>
              <span class="w-24 text-center text-slate-400">W7: 7.0 PTS</span>
              <span class="w-28 text-right text-slate-500">59.0 PTS</span>
            </div>
          </div>
        </div>
      </section>"""

print("Slides 4-7 built.")

# SLIDE 8: BOOMS & BUSTS
slide_8 = """      <!-- SLIDE 8: BOOMS & BUSTS -->
      <section id="wk7-slide-8" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-orange-950/80 via-slate-900 to-amber-950/80 border border-orange-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-orange-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              STATISTICAL ANOMALIES • HEROES & ZEROES
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">💥 Booms & Busts: Week 7 Outliers</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Tony Pollard's 35-point masterclass, Joe Burrow's bench lament, and Pedro's offense-wide blackout.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-orange-400 font-mono font-bold px-3 py-1 rounded-lg">Performance Extremes</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <!-- The Booms Card -->
          <div class="bg-slate-900 border-2 border-emerald-500/50 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-emerald-400 bg-emerald-950 border border-emerald-800 px-2.5 py-0.5 rounded">
              🚀 Week 7 Nuclear Booms
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tony Pollard (RB • TEN)</strong>
                  <span class="block text-slate-400 text-[11px]">WE NOT GOIN’ BACK 2 BACK (Robert) • 2 TD Eruption</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-extrabold text-sm">35.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Week 7 MVP</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Joe Burrow (QB • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">Njigbas in Paris (iRob) • Left on Bench!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">28.88 PTS</span>
                  <span class="block text-rose-400 text-[10px]">Bench Sorrow</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Drake Maye (QB • NE)</strong>
                  <span class="block text-slate-400 text-[11px]">Amon-Ra's Maye-hem (Alex) • Rookie Sensation</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">28.44 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Jaxon Smith-Njigba (WR • SEA)</strong>
                  <span class="block text-slate-400 text-[11px]">Njigbas in Paris (iRob) • Electric Performance</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">26.80 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Tee Higgins (WR • CIN)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">23.80 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Zay Flowers (WR • BAL)</strong>
                  <span class="block text-slate-400 text-[11px]">Saquon Deez Nacuas (Mark)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-emerald-400 font-bold">23.70 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>
            </div>
          </div>

          <!-- The Busts Card -->
          <div class="bg-slate-900 border-2 border-red-500/50 rounded-2xl p-5 shadow-xl">
            <span class="text-xs font-mono font-bold uppercase tracking-wider text-red-400 bg-red-950 border border-red-800 px-2.5 py-0.5 rounded">
              📉 Week 7 Catastrophic Busts
            </span>
            <div class="mt-3 space-y-2 text-xs">
              <div class="p-2.5 bg-slate-950 rounded-xl border border-red-600/40 flex justify-between items-center">
                <div>
                  <strong class="text-white">Carolina Panthers (DEF • CAR)</strong>
                  <span class="block text-slate-400 text-[11px]">The Latin Touch (Arnulfo) • Negative points!</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-500 font-extrabold text-sm">-3.00 PTS</span>
                  <span class="block text-red-400 text-[10px]">Sub-Zero</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Dominic Zvada (K • NYG)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">1.00 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Roschon Johnson (RB • CHI)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">1.30 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Sam LaPorta (TE • DET)</strong>
                  <span class="block text-slate-400 text-[11px]">Show me dem TDs (Eric) • Costly TE flop</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">2.30 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Xavier Worthy (WR • KC)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">2.60 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>

              <div class="p-2.5 bg-slate-950 rounded-xl border border-slate-800 flex justify-between items-center">
                <div>
                  <strong class="text-white">Garrett Wilson (WR • NYJ)</strong>
                  <span class="block text-slate-400 text-[11px]">I Didn’t Hear No Bell (Pedro)</span>
                </div>
                <div class="text-right font-mono">
                  <span class="text-red-400 font-bold">3.60 PTS</span>
                  <span class="block text-slate-500 text-[10px]">Starter</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 9: WEEK 7 SCOREBOARD
slide_9 = """      <!-- SLIDE 9: SCOREBOARD -->
      <section id="wk7-slide-9" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-slate-900 via-indigo-950/80 to-slate-900 border border-slate-800 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-indigo-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              OFFICIAL BOX SCORES • SLEEPER API AUDIT
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚔️ Week 7 Scoreboard</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Official final box scores, margins of victory, and statistical summaries for all 5 matchups.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-indigo-400 font-mono font-bold px-3 py-1 rounded-lg">5 Completed Matchups</span>
          </div>
        </div>

        <div class="space-y-3">
          <!-- Matchup 1: Century Blowout (Robert vs Pedro) -->
          <div class="bg-slate-900 border-2 border-red-500/60 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-red-400 bg-red-950/50 border border-red-800 px-2 py-0.5 rounded">
                💀 Matchup 1 • HISTORIC CENTURY BLOWOUT (+101.50 PTS)
              </span>
              <span class="text-xs font-mono text-slate-400">Largest Blowout in FFUC History</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">WE NOT GOIN’ BACK 2 BACK (Robert)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">153.82 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Tony Pollard (35.00), Jared Goff (18.02), Kyren Williams (17.10), Drake London (16.10), Bijan Robinson (14.70), Devaughn Vele (13.90), Seattle DEF (11.00).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-red-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-400 text-sm">I Didn’t Hear No Bell (Pedro)</span>
                  <span class="text-red-500 font-athletic text-lg font-black">52.32 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Ashton Jeanty (17.60), Bryce Young (7.42), Matthew Golden (6.90), Michael Mayer (4.70), Denzel Boston (4.20), Garrett Wilson (3.60), KC DEF (3.00), Worthy (2.60).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 2: Franky vs Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-amber-400 bg-amber-950/50 border border-amber-800 px-2 py-0.5 rounded">
                🔥 Matchup 2 • 280-Point Slugfest (+20.48 Margin)
              </span>
              <span class="text-xs font-mono text-slate-400">High-Scoring Showcase</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">CULT OF THE LAMB (Franky)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">150.02 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Caleb Williams (22.12), CeeDee Lamb (21.90), Emanuel Wilson (18.00), Blake Corum (16.60), Jayden Reed (16.40), Colston Loveland (14.20).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-rose-500/30">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-300 text-sm">Amon-Ra's Maye-hem (Alex)</span>
                  <span class="text-rose-400 font-athletic text-lg font-bold">129.54 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Drake Maye (28.44), Amon-Ra St. Brown (18.40), TreVeyon Henderson (17.80), Brian Thomas Jr. (13.60), Austin Seibert (11.00).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 3: Mark vs iRob -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-blue-400 bg-blue-950/50 border border-blue-800 px-2 py-0.5 rounded">
                ⚡ Matchup 3 • Upset Demolition (+41.08 Margin)
              </span>
              <span class="text-xs font-mono text-slate-400">Mark Topples Sole 1st Place</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">Saquon Deez Nacuas (Mark)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">145.20 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Zay Flowers (23.70), Russell Wilson (21.70), Saquon Barkley (16.20), Cooper Kupp (15.40), Kyle Pitts (15.20), Brandon Aubrey (14.00), James Conner (12.40).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-400 text-sm">Njigbas in Paris (iRob)</span>
                  <span class="text-slate-300 font-athletic text-lg font-bold">104.12 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Jaxon Smith-Njigba (26.80), Brock Purdy (14.02), George Pickens (13.70), RJ Harvey (13.00), McLaughlin (12.00). Bench: Joe Burrow (28.88).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 4: Joey vs Herrador -->
          <div class="bg-slate-900 border border-slate-800 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-slate-300 bg-slate-800 px-2 py-0.5 rounded">
                ⚔️ Matchup 4 • Ground & Pound Duel (+11.90 Margin)
              </span>
              <span class="text-xs font-mono text-slate-400">Joey Claims 4th Win</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">TheGreatSwagsby (Joey)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">113.82 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Christian McCaffrey (19.00), Ollie Gordon (16.80), C.J. Stroud (16.52), Braelon Allen (16.40), Tucker Kraft (12.80), Will Reichard (12.00).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-slate-800">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-400 text-sm">Brock To The Future (Herrador)</span>
                  <span class="text-slate-300 font-athletic text-lg font-bold">101.92 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Bucky Irving (23.50), D'Andre Swift (17.00), Tyler Shough (14.82), Ja'Marr Chase (14.70), Brock Bowers (10.30), Chuba Hubbard (8.00).
                </div>
              </div>
            </div>
          </div>

          <!-- Matchup 5: Arnulfo vs Eric -->
          <div class="bg-slate-900 border-2 border-emerald-500/40 rounded-2xl p-4 shadow-xl">
            <div class="flex justify-between items-center mb-2.5 border-b border-slate-800 pb-2">
              <span class="text-[11px] font-mono font-bold uppercase text-emerald-400 bg-emerald-950/60 border border-emerald-700 px-2 py-0.5 rounded">
                ⚡ Matchup 5 • $10 Bounty Thriller (+2.98 Margin)
              </span>
              <span class="text-xs font-mono text-emerald-400 font-bold">Arnulfo Takes 1st Place Tie</span>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
              <div class="bg-slate-950 p-3 rounded-xl border border-emerald-500/40">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-white text-sm">The Latin Touch (Arnulfo)</span>
                  <span class="text-emerald-400 font-athletic text-lg font-black">112.28 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Dak Prescott (23.28), Rhamondre Stevenson (20.00), Josh Jacobs (17.60), Jahmyr Gibbs (14.80), Chris Boswell (11.00), Watson (8.20).
                </div>
              </div>
              <div class="bg-slate-950 p-3 rounded-xl border border-rose-500/30">
                <div class="flex justify-between items-center font-bold">
                  <span class="text-slate-300 text-sm">Show me dem TDs (Eric)</span>
                  <span class="text-rose-400 font-athletic text-lg font-bold">109.30 PTS</span>
                </div>
                <div class="text-[11px] text-slate-400 mt-1">
                  Tee Higgins (23.80), Jameson Williams (23.60), Matthew Stafford (18.50), Jonathan Taylor (18.00), Matt Gay (8.00), Justin Jefferson (6.40).
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>"""

# SLIDE 10: WEEK 8 GAMEDAY HUB
slide_10 = """      <!-- SLIDE 10: WEEK 8 GAMEDAY HUB -->
      <section id="wk7-slide-10" class="slide space-y-4 animate-fade">
        <div class="bg-gradient-to-r from-emerald-950/80 via-slate-900 to-indigo-950/80 border border-emerald-500/40 rounded-2xl p-5 shadow-2xl flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          <div>
            <div class="inline-flex items-center gap-1.5 bg-emerald-600 text-white text-[10px] font-black px-2.5 py-0.5 rounded uppercase tracking-wider mb-1">
              WEEK 8 MATCHUP PREVIEWS • SPREADS & VEGAS LINES
            </div>
            <h2 class="text-2xl sm:text-3xl font-black uppercase tracking-tight text-white">⚡ Week 8 Gameday Hub</h2>
            <p class="text-xs sm:text-sm text-slate-300 mt-0.5">Clash of the Titans for 1st place, Pedro's survival test against Franky, and crucial 3-4 logjam battles.</p>
          </div>
          <div class="flex items-center gap-2">
            <span class="text-xs bg-slate-950 border border-slate-700 text-emerald-400 font-mono font-bold px-3 py-1 rounded-lg">5 Week 8 Matchups</span>
          </div>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
          <!-- Game of the Week: Arnulfo vs iRob -->
          <div class="bg-slate-900 border-2 border-amber-500/60 rounded-xl p-4 shadow-xl col-span-1 md:col-span-2">
            <div class="flex justify-between items-center border-b border-slate-800 pb-2 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-amber-400 bg-amber-950/80 border border-amber-700 px-2 py-0.5 rounded">
                👑 GAME OF THE WEEK • BATTLE FOR 1ST PLACE
              </span>
              <span class="font-mono text-emerald-400 font-bold">Spread: Arnulfo -1.5 | O/U: 228.5</span>
            </div>
            <div class="flex flex-col sm:flex-row justify-between items-center gap-4 py-2">
              <div class="text-center sm:text-left">
                <span class="text-base font-bold text-white">The Latin Touch (Arnulfo)</span>
                <span class="block text-emerald-400 font-mono font-semibold">5-2 • 854.64 PF</span>
              </div>
              <div class="text-xl font-black text-amber-400 font-athletic">VS</div>
              <div class="text-center sm:text-right">
                <span class="text-base font-bold text-white">Njigbas in Paris (iRob)</span>
                <span class="block text-emerald-400 font-mono font-semibold">5-2 • 850.78 PF</span>
              </div>
            </div>
            <p class="text-slate-300 mt-2 text-xs leading-relaxed border-t border-slate-800/80 pt-2">
              The stakes could not be higher! Arnulfo and iRob are deadlocked at 5-2. The winner takes sole possession of the 1st seed throne while the loser falls into the chasing pack. Will iRob start Joe Burrow after benching his 28.88 points?
            </p>
          </div>

          <!-- Matchup 1: Pedro vs Franky -->
          <div class="bg-slate-900 border border-red-500/40 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-red-400 bg-red-950 border border-red-800 px-2 py-0.5 rounded">
                Survival Test
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Franky -24.5 | O/U: 235.0</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-red-400">Pedro (2-5)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-amber-400">Franky (3-4)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Pedro just got blasted by 101.50 points, and his reward is facing Franky's #1 scoring juggernaut (964.64 PF). Pedro has $0 FAAB and desperately needs an upset of the millennium to stop his 5K descent.
            </p>
          </div>

          <!-- Matchup 2: Mark vs Robert -->
          <div class="bg-slate-900 border border-emerald-500/30 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-emerald-400 bg-emerald-950 border border-emerald-800 px-2 py-0.5 rounded">
                Heavyweight Clash
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Robert -4.5 | O/U: 255.5</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-white">Mark (4-3)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-amber-400">Robert (3-4)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Week 7's two highest scoring powerhouses! Mark dropped 145.20 to upset iRob, while Robert dropped 153.82 to claim the High Roller bounty. A playoff bubble battle with massive PF implications.
            </p>
          </div>

          <!-- Matchup 3: Herrador vs Alex -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-slate-400 bg-slate-950 px-2 py-0.5 rounded">
                3-4 Logjam Showdown
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Alex -1.5 | O/U: 238.0</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-slate-200">Herrador (3-4)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-slate-200">Alex (3-4)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Direct elimination pressure! Both sitting at 3-4, the winner regains an even .500 record and playoff positioning, while the loser falls to 3-5 into dangerous territory near the cellar.
            </p>
          </div>

          <!-- Matchup 5: Joey vs Eric -->
          <div class="bg-slate-900 border border-slate-800 rounded-xl p-3.5 shadow-lg">
            <div class="flex justify-between items-center border-b border-slate-800 pb-1.5 mb-2">
              <span class="text-[10px] font-mono font-bold uppercase text-slate-400 bg-slate-950 px-2 py-0.5 rounded">
                Playoff Hunt
              </span>
              <span class="font-mono text-slate-400 text-[11px]">Joey -6.5 | O/U: 222.0</span>
            </div>
            <div class="flex justify-between items-center font-bold text-sm">
              <span class="text-blue-400">Joey (4-3)</span>
              <span class="text-xs text-slate-500">VS</span>
              <span class="text-rose-400">Eric (3-4)</span>
            </div>
            <p class="text-slate-300 mt-2 text-[11px] leading-relaxed">
              Joey looks to solidify his hold on the 3rd seed with a 5th win. Eric is riding a heartbreaking 3-game losing streak and desperately needs Jonathan Taylor and Justin Jefferson to pull him out of the slump.
            </p>
          </div>
        </div>
      </section>"""

print("Slides 8-10 built.")

# -------------------------------------------------------------
# 3. ASSEMBLE FULL DECK-WK7 HTML
# -------------------------------------------------------------
deck_wk7_html = f"""    <!-- ========================================== -->
    <!-- DECK 7: WEEK 7 OFFICIAL REPORT (ACTIVE)    -->
    <!-- ========================================== -->
    <div id="deck-wk7">
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
# 4. PERFORM REPLACEMENTS IN index.html
# -------------------------------------------------------------
print("Performing replacements in index.html...")

# A. Replace Nav Pills
nav_pattern = r'<nav class="flex items-center gap-1\.5 sm:gap-2 overflow-x-auto no-scrollbar py-1">.*?</nav>'
html = re.sub(nav_pattern, new_nav_pills, html, count=1, flags=re.DOTALL)

# B. Replace Archive Selector Options & Synced Timestamp
old_archive_pattern = r'<select id="seasonArchive"[^>]*>.*?</select>'
new_archive_select = """<select id="seasonArchive" onchange="handleArchiveSelect(this.value)" class="bg-slate-950 border border-slate-700 text-amber-400 text-xs font-bold py-1.5 px-3 rounded-lg focus:outline-none focus:border-amber-500 cursor-pointer shadow-sm">
            <option value="wk7" selected>📅 Week 7: Official Report (Final)</option>
            <option value="wk6">📅 Week 6: Official Report (Archive)</option>
            <option value="wk5">📅 Week 5: Official Report (Archive)</option>
            <option value="wk4">📅 Week 4: Official Report (Archive)</option>
            <option value="wk3">📅 Week 3: Official Report (Archive)</option>
            <option value="wk2">📅 Week 2: Official Report (Archive)</option>
            <option value="wk1">📅 Week 1: Season Opener (Archive)</option>
            <option value="locked" disabled>🔒 Week 8 (Upcoming)</option>
          </select>"""
html = re.sub(old_archive_pattern, new_archive_select, html, count=1, flags=re.DOTALL)

# Timestamp
html = re.sub(r'id="portalSyncedTime">.*?</strong>', 'id="portalSyncedTime">Oct 27, 2026 • 11:30 AM CST (Week 7 Final Edition)</strong>', html, count=1)

# C. Ticker Items
ticker_segment = """<span>👑 <strong>High Roller ($10 Bounty):</strong> <span class="text-amber-400 font-bold">WE NOT GOIN’ BACK 2 BACK (Robert)</span> detonates for <span class="text-emerald-400 font-bold">153.82 PTS</span>!</span><span class="text-slate-500">•</span><span>💀 <strong>HISTORIC CENTURY BLOWOUT:</strong> <span class="text-amber-400 font-bold">Robert (153.82)</span> annihilates <span class="text-red-400 font-bold">Pedro (52.32)</span> by <span class="text-red-500 font-extrabold">101.50 PTS</span>!</span><span class="text-slate-500">•</span><span>⚡ <strong>$10 Bounty Winner (Narrowest Victory):</strong> <span class="text-amber-400 font-bold">Arnulfo (The Latin Touch)</span> edges Eric by <span class="text-emerald-400 font-bold">2.98 PTS</span> (112.28 to 109.30)!</span><span class="text-slate-500">•</span><span>💔 <strong>Heartbreak of the Week:</strong> <span class="text-amber-400 font-bold">Alex (129.54)</span> suffers bad beat against <span class="text-amber-400 font-bold">Franky's 150.02</span> offensive clinic!</span><span class="text-slate-500">•</span><span>🎯 <strong>Pick-Em Solo Leader:</strong> <span class="text-amber-400 font-bold">Arnulfo</span> takes 1st place alone at <span class="text-emerald-400 font-bold">67.0 PTS</span>!</span><span class="text-slate-500">•</span><span>🚽 <strong>5K Danger Zone:</strong> <span class="text-red-400 font-bold">Pedro</span> sits stranded at <span class="text-red-400 font-bold">2-5 with $0 FAAB</span> and -210 PF deficit!</span><span class="text-slate-500">•</span><span>🏆 <strong>Co-Leaders at 5-2:</strong> <span class="text-amber-400 font-bold">Arnulfo & iRob</span> locked atop FFUC before Week 8 clash!</span>"""

ticker_pattern = r'<div class="ticker-wrap flex-1 min-w-0">.*?</div>\s*</div>\s*</div>'
new_ticker = f"""<div class="ticker-wrap flex-1 min-w-0">
        <div class="ticker-content text-slate-200 text-xs">
          <!-- Segment A -->
          <div class="inline-flex items-center gap-6 pr-6">{ticker_segment}</div>

          <!-- Segment B (Identical for seamless infinite loop) -->
          <div class="inline-flex items-center gap-6 pr-6" aria-hidden="true">{ticker_segment}</div>
        </div>
      </div>"""

# Replace ticker wrap
html = re.sub(r'<div class="ticker-wrap flex-1 min-w-0">.*?(?=<!-- Quick Action Tab Button -->)', new_ticker + "\n\n      ", html, count=1, flags=re.DOTALL)

# D. Insert Deck 7 and Archive Deck 6
# Find <div id="deck-wk6">
if '<div id="deck-wk6">' in html:
    # Make deck-wk6 hidden/archived
    html = html.replace('<div id="deck-wk6">', '<div id="deck-wk6" style="display:none;">')
    # Prepend deck_wk7_html before deck-wk6
    html = html.replace('<div id="deck-wk6" style="display:none;">', deck_wk7_html + '\n\n    <!-- ========================================== -->\n    <!-- DECK 6: WEEK 6 OFFICIAL REPORT (ARCHIVED)  -->\n    <!-- ========================================== -->\n    <div id="deck-wk6" style="display:none;">')

# E. Update JavaScript handleArchiveSelect
old_archive_func = r'function handleArchiveSelect\(val\) \{.*?(?=function switchVoice|function copySleeperBlast|function prevSlide)'
new_archive_func = """function handleArchiveSelect(val) {
      if (val === 'wk1' || val === 'wk2' || val === 'wk3' || val === 'wk4' || val === 'wk5' || val === 'wk6' || val === 'wk7') {
        currentEdition = val;
        currentSlide = 0;
        const d1 = document.getElementById('deck-wk1');
        const d2 = document.getElementById('deck-wk2');
        const d3 = document.getElementById('deck-wk3');
        const d4 = document.getElementById('deck-wk4');
        const d5 = document.getElementById('deck-wk5');
        const d6 = document.getElementById('deck-wk6');
        const d7 = document.getElementById('deck-wk7');

        if (d1) d1.style.display = (val === 'wk1') ? 'block' : 'none';
        if (d2) d2.style.display = (val === 'wk2') ? 'block' : 'none';
        if (d3) d3.style.display = (val === 'wk3') ? 'block' : 'none';
        if (d4) d4.style.display = (val === 'wk4') ? 'block' : 'none';
        if (d5) d5.style.display = (val === 'wk5') ? 'block' : 'none';
        if (d6) d6.style.display = (val === 'wk6') ? 'block' : 'none';
        if (d7) d7.style.display = (val === 'wk7') ? 'block' : 'none';

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

# F. Update copySleeperBlast
old_blast_pattern = r'function copySleeperBlast\(\) \{.*?(?=function|\Z)'
new_blast_func = """function copySleeperBlast() {
      const blast = `🏈 F.F.U.C. WEEK 7 OFFICIAL REPORT IS LIVE! 🏈
We have reached the exact halfway mark of the season, and Week 7 delivered pure mayhem!

👑 HIGH ROLLER CHAMPION ($10 Bounty):
• WE NOT GOIN’ BACK 2 BACK (Robert) erupts for a week-high 153.82 PTS!
• Led by Tony Pollard's 35.00-pt masterclass, Robert takes the $10 High Roller crown!

💀 HISTORIC CENTURY BLOWOUT:
• Robert (153.82) demolishes Pedro (52.32) by 101.50 POINTS in the largest blowout in modern FFUC history! Pedro sits isolated at 2-5 with $0 FAAB and trails 9th place by 210 season points!

⚡ $10 BOUNTY WINNER (Narrowest Victory):
• Arnulfo (The Latin Touch) survives a 2.98-point Monday thriller against Eric (112.28 to 109.30) to capture the $10 bounty and claim a share of 1st place!

💔 HEARTBREAK OF THE WEEK:
• Alex (Amon-Ra's Maye-hem) puts up 129.54 PTS (would defeat 6 of 9 teams) but collides with Franky's 150.02 blitzkrieg!

🎯 PICK-EM LEADERBOARD ($45 Pot):
• Arnulfo takes solo 1st at 67.0 pts, followed by Robert (66.0) and iRob (65.0)!

🎙️ All-new single announcer audio broadcast, power rankings, and Week 8 previews live now:
👉 https://ffucleague.com`;

      navigator.clipboard.writeText(blast).then(() => {
        const btn = document.getElementById('copyBlastBtn');
        const orig = btn.innerHTML;
        btn.innerHTML = '✅ Copied Week 7 Blast!';
        setTimeout(() => { btn.innerHTML = orig; }, 2500);
      });
    }
"""
html = re.sub(old_blast_pattern, new_blast_func, html, count=1, flags=re.DOTALL)

# G. Update goToSlide to know about wk7
html = html.replace("const slide = document.getElementById(`${currentEdition}-slide-${index}`);", "const slide = document.getElementById(`${currentEdition}-slide-${index}`);")

# Write updated index.html
with open(INDEX_PATH, "wb") as f:
    f.write(html.encode("utf-8"))

print("🎉 Successfully built and updated index.html with Week 7 deck!")

import re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update currentEdition default to wk7
html = html.replace("let currentEdition = 'wk6';", "let currentEdition = 'wk7';")

# 2. Add complete Next/Prev/UpdateSlides controller
old_slider_ctrl = """    function prevSlide() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      const deckTotal = currentDeck ? currentDeck.querySelectorAll('.slide').length : totalSlides;
      currentSlide = (currentSlide - 1 + deckTotal) % deckTotal;
      updateSlides();
    }

    function goToSlide(index) {
      currentSlide = index;
      updateSlides();
    }"""

new_slider_ctrl = """    function nextSlide() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      const deckTotal = currentDeck ? currentDeck.querySelectorAll('.slide').length : totalSlides;
      currentSlide = (currentSlide + 1) % deckTotal;
      updateSlides();
    }

    function prevSlide() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      const deckTotal = currentDeck ? currentDeck.querySelectorAll('.slide').length : totalSlides;
      currentSlide = (currentSlide - 1 + deckTotal) % deckTotal;
      updateSlides();
    }

    function goToSlide(index) {
      currentSlide = index;
      updateSlides();
    }

    function updateSlides() {
      const currentDeck = document.getElementById('deck-' + currentEdition);
      if (!currentDeck) return;
      const slides = currentDeck.querySelectorAll('.slide');
      const deckTotal = slides.length || totalSlides;

      slides.forEach((s, idx) => {
        if (idx === currentSlide) {
          s.classList.add('active');
        } else {
          s.classList.remove('active');
        }
      });

      // Update pills
      const pills = document.querySelectorAll('.nav-pill');
      pills.forEach((p, idx) => {
        if (idx === currentSlide) {
          p.className = 'nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-amber-500 text-slate-950 font-bold';
        } else {
          p.className = 'nav-pill px-3 py-1.5 rounded-full text-xs font-semibold whitespace-nowrap transition bg-slate-900 text-slate-400 hover:text-white';
        }
      });

      // Update indicator
      const ind = document.getElementById('slideIndicator');
      if (ind) ind.innerText = `Slide ${currentSlide + 1} / ${deckTotal}`;
    }"""

if old_slider_ctrl in html:
    html = html.replace(old_slider_ctrl, new_slider_ctrl)
    print("Replaced slider controller with full next/prev/updateSlides.")
else:
    print("Warning: old_slider_ctrl not found exactly.")

# 3. Audio progress bar support for audioProgressBar and broadcastProgressBar
html = html.replace("const bar = document.getElementById('broadcastProgressBar');", "const bar = document.getElementById('audioProgressBar') || document.getElementById('broadcastProgressBar');")
html = html.replace("const cur = document.getElementById('broadcastCurrentTime');", "const cur = document.getElementById('audioCurrentTime') || document.getElementById('broadcastCurrentTime');")
html = html.replace("const dur = document.getElementById('broadcastDuration');", "const dur = document.getElementById('audioDuration') || document.getElementById('broadcastDuration');")

with open('index.html', 'wb') as f:
    f.write(html.encode('utf-8'))

print("Updated index.html successfully!")

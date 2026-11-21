import os
import re

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. ADD CSS FOR NARRATIVE DIALOG
css_to_add = """
    /* RETRO RPG / POKEMON STYLE NARRATIVE DIALOGUE BOX */
    #narrative-dialog {
      display: none;
      position: fixed;
      bottom: calc(22px + env(safe-area-inset-bottom));
      left: 50%;
      transform: translateX(-50%);
      width: 90%;
      max-width: 560px;
      background: rgba(255, 255, 255, 0.96);
      border: 3.5px solid #38bdf8;
      border-radius: 20px;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5), 0 0 16px rgba(56, 189, 248, 0.4), inset 0 2px 5px rgba(255, 255, 255, 0.9);
      padding: 16px 20px 14px 20px;
      z-index: 99999;
      cursor: pointer;
      user-select: none;
      animation: narrativeSlideUp 0.35s cubic-bezier(0.175, 0.885, 0.32, 1.25);
    }
    @keyframes narrativeSlideUp {
      from { opacity: 0; transform: translate(-50%, 25px) scale(0.95); }
      to { opacity: 1; transform: translate(-50%, 0) scale(1); }
    }
    @keyframes narrativeSlideDown {
      from { opacity: 1; transform: translate(-50%, 0) scale(1); }
      to { opacity: 0; transform: translate(-50%, 20px) scale(0.95); }
    }
    .narrative-tag {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: linear-gradient(135deg, #0284c7, #0369a1);
      color: #ffffff;
      font-weight: 900;
      font-size: 13px;
      padding: 3px 12px;
      border-radius: 12px;
      margin-bottom: 8px;
      box-shadow: 0 2px 6px rgba(2, 132, 199, 0.35);
      letter-spacing: 0.5px;
    }
    .narrative-text {
      color: #0f172a;
      font-size: 15px;
      font-weight: 700;
      line-height: 1.5;
      margin: 0 0 6px 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    .narrative-text .highlight {
      color: #0284c7;
      font-weight: 800;
      display: block;
      margin-top: 4px;
    }
    .narrative-prompt {
      text-align: right;
      font-size: 10px;
      font-weight: 800;
      color: #0284c7;
      letter-spacing: 1px;
      animation: pulseBlink 0.9s infinite alternate;
    }
    @keyframes pulseBlink {
      from { opacity: 0.4; }
      to { opacity: 1; }
    }
"""

# Insert CSS before </style>
target_style = "</style>"
assert target_style in text
text = text.replace(target_style, css_to_add + "\n  </style>", 1)

# 2. ADD HTML FOR NARRATIVE DIALOG BOX
dialog_html = """
  <!-- GAME DEV NARRATIVE DIALOGUE BOX (POKÉMON STYLE) -->
  <div id="narrative-dialog" onclick="closeNarrativeDialog()">
    <div class="narrative-tag">
      <span>👨‍💻</span>
      <span>Game Dev</span>
    </div>
    <div class="narrative-text">
      Don't expect too much, cause the developer is having exam ;)
      <span class="highlight">Enjoy the game !</span>
    </div>
    <div class="narrative-prompt">TAP ANYWHERE TO CONTINUE ▶</div>
  </div>
"""

# Insert right after #mission-banner
target_banner = 'id="mission-banner"'
assert target_banner in text
# Find end of mission-banner div
m = re.search(r'<div id="mission-banner"[\s\S]*?</div>', text)
assert m, "Could not find mission-banner div"
insert_pos = m.end()
text = text[:insert_pos] + "\n" + dialog_html + text[insert_pos:]

# 3. ADD JS FUNCTIONS & HOOK INTO startGameplay()
old_start = """    function startGameplay() {
      State.inMenu = false;
      mainMenuOverlay.classList.add('hidden');
      Sound.init();
      showToast(`WELCOME TO VICE CITY! VISIT BURGER SHOT OR GRAB YOUR RIDE!`);
    }"""

new_start = """    let _narrativeTimer = null;
    function showNarrativeDialog() {
      const el = document.getElementById('narrative-dialog');
      if (!el) return;
      el.style.display = 'block';
      Sound.playWhistle();
      clearTimeout(_narrativeTimer);
      _narrativeTimer = setTimeout(() => {
        closeNarrativeDialog();
      }, 8500);
    }

    function closeNarrativeDialog() {
      const el = document.getElementById('narrative-dialog');
      if (el) {
        el.style.animation = 'narrativeSlideDown 0.25s ease-out forwards';
        setTimeout(() => {
          el.style.display = 'none';
          el.style.animation = '';
        }, 240);
      }
      clearTimeout(_narrativeTimer);
    }

    function startGameplay() {
      State.inMenu = false;
      mainMenuOverlay.classList.add('hidden');
      Sound.init();
      showToast(`WELCOME TO VICE CITY! VISIT BURGER SHOT OR GRAB YOUR RIDE!`);
      // Trigger Game Dev Narrative Dialog right outside Safehouse!
      setTimeout(() => {
        showNarrativeDialog();
      }, 600);
    }"""

assert old_start in text, "Could not find old_start"
text = text.replace(old_start, new_start)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Narrative dialogue box added successfully!")

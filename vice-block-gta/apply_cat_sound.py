import os

index_file = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add <audio id="menu-cat-audio"> element right inside #main-menu-overlay
old_overlay_start = '<div id="main-menu-overlay">'
new_overlay_start = '''<div id="main-menu-overlay">
    <!-- Cat laugh sound that starts as soon as app opens to menu page -->
    <audio id="menu-cat-audio" src="menu_sound.mp3" preload="auto"></audio>'''

if old_overlay_start in content and 'id="menu-cat-audio"' not in content:
    content = content.replace(old_overlay_start, new_overlay_start, 1)
    print("Added <audio id='menu-cat-audio'> into main-menu-overlay.")

# 2. Add early autoplay script right after <head> or at top of <body>
early_script = '''  <!-- INSTANT MENU CAT AUDIO AUTOPLAY ON APP START -->
  <script>
    (function() {
      window._catAudioPlayed = false;
      function startCatAudio() {
        if (window._catAudioPlayed) return;
        const catAudio = document.getElementById('menu-cat-audio');
        if (!catAudio) return;
        catAudio.volume = 0.95;
        const p = catAudio.play();
        if (p !== undefined) {
          p.then(() => {
            window._catAudioPlayed = true;
          }).catch(() => {
            // If browser policy gated autoplay, it will trigger on first touch
          });
        }
      }

      // Try playing as early as possible
      document.addEventListener('DOMContentLoaded', startCatAudio);
      window.addEventListener('load', startCatAudio);

      // Instant fallback on first touch / tap anywhere on screen
      ['pointerdown', 'touchstart', 'click', 'keydown'].forEach(function(evt) {
        window.addEventListener(evt, startCatAudio, { once: true });
      });
    })();
  </script>
'''

if 'INSTANT MENU CAT AUDIO AUTOPLAY' not in content:
    content = content.replace('<body>', '<body>\n' + early_script, 1)
    print("Added early cat audio autoplay script.")

# 3. In startGameplay, ensure catAudio stops immediately
old_stop_menu = '''      if (menuAudio && !menuAudio.paused) {
        menuAudio.pause();
        menuAudio.currentTime = 0;
      }'''

new_stop_menu = '''      const catEl = document.getElementById('menu-cat-audio');
      if (catEl && !catEl.paused) {
        catEl.pause();
        catEl.currentTime = 0;
      }
      if (menuAudio && !menuAudio.paused) {
        menuAudio.pause();
        menuAudio.currentTime = 0;
      }'''

if old_stop_menu in content:
    content = content.replace(old_stop_menu, new_stop_menu)
    print("Updated startGameplay() to stop catAudio cleanly.")

# Also update menuAudio reference in main script to use menu-cat-audio element or fallback
old_menuAudio_init = '''    // Menu Audio: Evil laugh sound when menu is seen, played only once (no repetition, loop = false)
    const menuAudio = new Audio('menu_sound.mp3');
    menuAudio.loop = false;
    menuAudio.volume = 0.9;
    let menuAudioPlayed = false;

    function playMenuSoundOnce() {
      if (menuAudioPlayed) return;
      if (mainMenuOverlay && mainMenuOverlay.classList.contains('hidden')) return;

      const p = menuAudio.play();
      if (p !== undefined) {
        p.then(() => {
          menuAudioPlayed = true;
          cleanupMenuAudioTriggers();
        }).catch(() => {
          // Modern browsers gate audio autoplay until first user touch/click
        });
      }
    }'''

new_menuAudio_init = '''    // Menu Audio: Cat laugh sound when menu is seen, played only once (no repetition, loop = false)
    const menuAudio = document.getElementById('menu-cat-audio') || new Audio('menu_sound.mp3');
    menuAudio.loop = false;
    menuAudio.volume = 0.95;
    let menuAudioPlayed = window._catAudioPlayed || false;

    function playMenuSoundOnce() {
      if (menuAudioPlayed || window._catAudioPlayed) return;
      if (mainMenuOverlay && mainMenuOverlay.classList.contains('hidden')) return;

      const p = menuAudio.play();
      if (p !== undefined) {
        p.then(() => {
          menuAudioPlayed = true;
          window._catAudioPlayed = true;
          cleanupMenuAudioTriggers();
        }).catch(() => {
          // Modern browsers gate audio autoplay until first user touch/click
        });
      }
    }'''

if old_menuAudio_init in content:
    content = content.replace(old_menuAudio_init, new_menuAudio_init)
    print("Updated menuAudio initialization.")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Done configuring instant cat audio autoplay on menu start.")

import shutil, os, re

base_dir = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta'
index_file = os.path.join(base_dir, 'index.html')
sw_file = os.path.join(base_dir, 'sw.js')
bundle_file = os.path.join(base_dir, 'bundle_release.py')

# 1. Update index.html
with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

menu_audio_code = '''    // --- GTA MAIN MENU & ROBLOX MENU LOGIC ---
    const mainMenuOverlay = document.getElementById('main-menu-overlay');
    const btnStartGame = document.getElementById('btn-start-game');
    const btnMenuChar = document.getElementById('btn-menu-char');
    const btnMenuCheckpoint = document.getElementById('btn-menu-checkpoint');
    const btnMenuControls = document.getElementById('btn-menu-controls');
    const btnMenuAudio = document.getElementById('btn-menu-audio');
    const controlsModal = document.getElementById('controls-modal');
    const btnCloseControls = document.getElementById('btn-close-controls');

    // Menu Audio: Evil laugh sound when menu is seen, played only once (no repetition, loop = false)
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
    }

    function onMenuUserInteraction() {
      if (!menuAudioPlayed) {
        playMenuSoundOnce();
      }
    }

    function cleanupMenuAudioTriggers() {
      window.removeEventListener('pointerdown', onMenuUserInteraction);
      window.removeEventListener('touchstart', onMenuUserInteraction);
      window.removeEventListener('click', onMenuUserInteraction);
      window.removeEventListener('keydown', onMenuUserInteraction);
    }

    // Try playing immediately if browser allows autoplay
    playMenuSoundOnce();
    // Also listen for first touch/click/gesture anywhere to play if autoplay was gated
    window.addEventListener('pointerdown', onMenuUserInteraction);
    window.addEventListener('touchstart', onMenuUserInteraction, { passive: true });
    window.addEventListener('click', onMenuUserInteraction);
    window.addEventListener('keydown', onMenuUserInteraction);'''

old_menu_header = '''    // --- GTA MAIN MENU & ROBLOX MENU LOGIC ---
    const mainMenuOverlay = document.getElementById('main-menu-overlay');
    const btnStartGame = document.getElementById('btn-start-game');
    const btnMenuChar = document.getElementById('btn-menu-char');
    const btnMenuCheckpoint = document.getElementById('btn-menu-checkpoint');
    const btnMenuControls = document.getElementById('btn-menu-controls');
    const btnMenuAudio = document.getElementById('btn-menu-audio');
    const controlsModal = document.getElementById('controls-modal');
    const btnCloseControls = document.getElementById('btn-close-controls');'''

if old_menu_header in content:
    content = content.replace(old_menu_header, menu_audio_code)
    print("Added menuAudio logic to index.html")
else:
    print("Warning: old_menu_header not found in index.html")

# In startGameplay: stop menuAudio cleanly
old_start_game = '''    function startGameplay() {
      State.inMenu = false;
      mainMenuOverlay.classList.add('hidden');
      Sound.init();'''

new_start_game = '''    function startGameplay() {
      State.inMenu = false;
      mainMenuOverlay.classList.add('hidden');
      if (menuAudio && !menuAudio.paused) {
        menuAudio.pause();
        menuAudio.currentTime = 0;
      }
      cleanupMenuAudioTriggers();
      Sound.init();'''

if old_start_game in content:
    content = content.replace(old_start_game, new_start_game)
    print("Added menuAudio stop to startGameplay")
else:
    print("Warning: old_start_game not found in index.html")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

# 2. Update sw.js to cache menu_sound.mp3
with open(sw_file, 'r', encoding='utf-8') as f:
    sw_content = f.read()

if "'./menu_sound.mp3'" not in sw_content:
    sw_content = sw_content.replace("'./screenshot2.png'", "'./screenshot2.png',\n  './menu_sound.mp3'")
    sw_content = sw_content.replace("const CACHE_NAME = 'vice-blocks-v3';", "const CACHE_NAME = 'vice-blocks-v4';")
    with open(sw_file, 'w', encoding='utf-8') as f:
        f.write(sw_content)
    print("Updated sw.js with menu_sound.mp3")

# 3. Update bundle_release.py
with open(bundle_file, 'r', encoding='utf-8') as f:
    bundle_content = f.read()

if '"menu_sound.mp3"' not in bundle_content:
    bundle_content = bundle_content.replace('"screenshot2.png",', '"screenshot2.png",\n    "menu_sound.mp3",')
    with open(bundle_file, 'w', encoding='utf-8') as f:
        f.write(bundle_content)
    print("Updated bundle_release.py with menu_sound.mp3")

# 4. Sync files to android_native_app and ViceBlocks_AndroidStudio_Project
sync_targets = [
    os.path.join(base_dir, 'android_native_app', 'app', 'src', 'main', 'assets'),
    os.path.join(base_dir, 'ViceBlocks_AndroidStudio_Project', 'app', 'src', 'main', 'assets')
]

files_to_sync = ['index.html', 'menu_sound.mp3', 'sw.js']
for target_dir in sync_targets:
    if os.path.exists(target_dir):
        for fname in files_to_sync:
            src_f = os.path.join(base_dir, fname)
            dst_f = os.path.join(target_dir, fname)
            if os.path.exists(src_f):
                shutil.copyfile(src_f, dst_f)
        print(f"Synced {files_to_sync} to {target_dir}")

print("All updates and sync completed.")

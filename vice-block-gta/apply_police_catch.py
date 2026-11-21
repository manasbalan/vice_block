import shutil, os

base_dir = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta'
src_mp3 = r'C:\Users\rames\.gemini\antigravity\brain\6b4df872-92e0-407f-bfaf-d1acf225bd89\.user_uploaded\uploaded_media_1795257727202.mp3'

# 1. Copy mp3 to base and asset directories
dst1 = os.path.join(base_dir, 'police_catch.mp3')
shutil.copyfile(src_mp3, dst1)
print(f"Copied to {dst1} ({os.path.getsize(dst1)} bytes)")

android_dirs = [
    os.path.join(base_dir, 'android_native_app', 'app', 'src', 'main', 'assets'),
    os.path.join(base_dir, 'ViceBlocks_AndroidStudio_Project', 'app', 'src', 'main', 'assets')
]
for ad in android_dirs:
    if os.path.exists(ad):
        shutil.copyfile(src_mp3, os.path.join(ad, 'police_catch.mp3'))
        print(f"Copied to {ad}")

# 2. Update index.html
index_file = os.path.join(base_dir, 'index.html')
with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Add policeCatchAudio definition near menuAudio
old_menu_audio_def = '''    // Menu Audio: Evil laugh sound when menu is seen, played only once (no repetition, loop = false)
    const menuAudio = new Audio('menu_sound.mp3');'''

new_menu_audio_def = '''    // Police Catch Audio: Malayalam "Ayyoo!" despair sound when police catches player
    const policeCatchAudio = new Audio('police_catch.mp3');
    policeCatchAudio.volume = 1.0;

    // Menu Audio: Evil laugh sound when menu is seen, played only once (no repetition, loop = false)
    const menuAudio = new Audio('menu_sound.mp3');'''

if old_menu_audio_def in content:
    content = content.replace(old_menu_audio_def, new_menu_audio_def)
    print("Added policeCatchAudio definition to index.html")
else:
    print("Warning: old_menu_audio_def not found")

# Inside bustPlayer: play policeCatchAudio
old_bust_func = '''    function bustPlayer(onRespawn) {
      if (State.isBusted || State.isDead) return;
      State.isBusted = true;
      try {
        if (Sound && typeof Sound.playSiren === 'function') {
          Sound.playSiren();
        } else if (Sound && typeof Sound.updateSiren === 'function') {
          Sound.updateSiren(true);
          setTimeout(() => Sound.updateSiren(false), 2000);
        }
      } catch(e){}'''

new_bust_func = '''    function bustPlayer(onRespawn) {
      if (State.isBusted || State.isDead) return;
      State.isBusted = true;
      try {
        if (policeCatchAudio) {
          policeCatchAudio.currentTime = 0;
          policeCatchAudio.play().catch(e => console.log('[ViceBlocks] Police catch audio error:', e));
        }
      } catch(e){}
      try {
        if (Sound && typeof Sound.playSiren === 'function') {
          Sound.playSiren();
        } else if (Sound && typeof Sound.updateSiren === 'function') {
          Sound.updateSiren(true);
          setTimeout(() => Sound.updateSiren(false), 2000);
        }
      } catch(e){}'''

if old_bust_func in content:
    content = content.replace(old_bust_func, new_bust_func)
    print("Added policeCatchAudio playback to bustPlayer() in index.html")
else:
    print("Warning: old_bust_func not found in index.html")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Update sw.js
sw_file = os.path.join(base_dir, 'sw.js')
with open(sw_file, 'r', encoding='utf-8') as f:
    sw_content = f.read()

if "'./police_catch.mp3'" not in sw_content:
    sw_content = sw_content.replace("'./menu_sound.mp3'", "'./menu_sound.mp3',\n  './police_catch.mp3'")
    sw_content = sw_content.replace("const CACHE_NAME = 'vice-blocks-v4';", "const CACHE_NAME = 'vice-blocks-v5';")
    with open(sw_file, 'w', encoding='utf-8') as f:
        f.write(sw_content)
    print("Updated sw.js with police_catch.mp3 and bumped cache to v5")

# 4. Update bundle_release.py
bundle_file = os.path.join(base_dir, 'bundle_release.py')
with open(bundle_file, 'r', encoding='utf-8') as f:
    bundle_content = f.read()

if '"police_catch.mp3"' not in bundle_content:
    bundle_content = bundle_content.replace('"menu_sound.mp3",', '"menu_sound.mp3",\n    "police_catch.mp3",')
    with open(bundle_file, 'w', encoding='utf-8') as f:
        f.write(bundle_content)
    print("Updated bundle_release.py with police_catch.mp3")

# 5. Sync updated index.html & sw.js to Android Studio projects
for ad in android_dirs:
    if os.path.exists(ad):
        shutil.copyfile(index_file, os.path.join(ad, 'index.html'))
        shutil.copyfile(sw_file, os.path.join(ad, 'sw.js'))
        print(f"Synced index.html & sw.js to {ad}")

print("All police catch audio tasks completed.")

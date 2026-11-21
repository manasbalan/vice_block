import os, shutil

base_dir = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta'
index_file = os.path.join(base_dir, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Remove the BUG and TREX cheat buttons from cheat modal HTML
old_cheat_buttons = '''        <button class="cheat-btn" data-cheat="BUG" style="border-color:#ff007f;background:rgba(255,0,127,0.22);grid-column:span 2;">🐛 DEVELOPER BUG / GLITCH EASTER EGG</button>
        <button class="cheat-btn" data-cheat="TREX" style="border-color:#10b981;background:rgba(16,185,129,0.22);grid-column:span 2;">🦖 SPAWN GIANT T-REX STAMPEDE</button>'''

if old_cheat_buttons in content:
    content = content.replace(old_cheat_buttons, '')
    print("Removed BUG and TREX buttons from cheat modal.")
else:
    print("Warning: old_cheat_buttons not matched directly, checking individual buttons...")
    content = content.replace('<button class="cheat-btn" data-cheat="BUG" style="border-color:#ff007f;background:rgba(255,0,127,0.22);grid-column:span 2;">🐛 DEVELOPER BUG / GLITCH EASTER EGG</button>\n', '')
    content = content.replace('<button class="cheat-btn" data-cheat="TREX" style="border-color:#10b981;background:rgba(16,185,129,0.22);grid-column:span 2;">🦖 SPAWN GIANT T-REX STAMPEDE</button>\n', '')

# 2. Remove TREX and BUG branches from executeCheatCode(code)
old_trex_branch = '''      } else if (code === 'TREX' || code === 'DINO' || code === 'JURASSIC') {
        triggerTRexStampede();
        showToast("🦖 CHEAT ACTIVATED: GIANT T-REX STAMPEDE IN CENTRAL AVE!");'''

if old_trex_branch in content:
    content = content.replace(old_trex_branch, '')
    print("Removed TREX / DINO cheat code handler.")
else:
    print("Warning: old_trex_branch not found.")

old_bug_branch = '''      } else if (code === 'BUG' || code === 'GLITCH') {
        triggerDeveloperBugGlitch();'''

if old_bug_branch in content:
    content = content.replace(old_bug_branch, '')
    print("Removed BUG / GLITCH cheat code handler.")
else:
    print("Warning: old_bug_branch not found.")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

# 3. Sync to Android Studio projects
android_dirs = [
    os.path.join(base_dir, 'android_native_app', 'app', 'src', 'main', 'assets'),
    os.path.join(base_dir, 'ViceBlocks_AndroidStudio_Project', 'app', 'src', 'main', 'assets')
]
for ad in android_dirs:
    if os.path.exists(ad):
        shutil.copyfile(index_file, os.path.join(ad, 'index.html'))
        print(f"Synced to {ad}")

print("Cleaned up cheat codes and buttons successfully.")

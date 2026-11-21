import re

file_path = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Update police car theft roast
old_police = 'showNarrativeDialog("Game Dev", "Police vandiyum kondu evidekk... SI ippo varum!", null, 10000);'
new_police = 'showNarrativeDialog("Game Dev", "Police vandiyum kondu evidekk... Patunna paniki poya pore!", null, 10000);'
if old_police in content:
    content = content.replace(old_police, new_police)
    print("Updated police theft roast successfully.")
else:
    print("old_police not found directly, checking regex...")

# 2. Update exam question responses
exam_pat = re.compile(r'function answerExamQuestion\(option\) \{[\s\S]*?function executeBuildingAction', re.MULTILINE)
new_exam_func = '''function answerExamQuestion(option) {
      closeExamQuestionModal();

      setTimeout(() => {
        if (option === 4) {
          // 4th option is the correct answer (k = 2) - Developer fails roast!
          try { Sound.playCash(); } catch(e){}
          showNarrativeDialog(
            "Game Dev",
            "Aaah my bad...! Sthalam mari poi!",
            "DEVELOPER FAILED • YOU DEFEATED THE EXAM!",
            10000
          );
        } else if (option === 3) {
          // 3rd option (k = -5 when k > 0)
          try { Sound.playOof(); } catch(e){}
          showNarrativeDialog("Game Dev", " Excellent! Ennalum negative engane kiiti ", null, 10000);
        } else {
          // Option 1 or Option 2
          try { Sound.playWhistle(); } catch(e){}
          showNarrativeDialog("Game Dev", "Wrong one", null, 10000);
        }
      }, 400);
    }

    function executeBuildingAction'''

if exam_pat.search(content):
    content = exam_pat.sub(new_exam_func, content)
    print("Updated answerExamQuestion successfully.")
else:
    print("Warning: answerExamQuestion pattern not matched.")

# 3. Update ammo empty roasts in handleAction
# Let's inspect weapons in handleAction
old_pistol_ammo = '''      } else if (State.currentWeapon === 'pistol') {
        if (State.ammo.pistol <= 0) {
          showToast("OUT OF PISTOL AMMO! Swapping to Fists");'''

new_pistol_ammo = '''      } else if (State.currentWeapon === 'pistol') {
        if (State.ammo.pistol <= 0) {
          showToast("OUT OF PISTOL AMMO! Swapping to Fists");
          showNarrativeDialog("Game Dev", "Ammo teernada ", null, 10000);'''

if old_pistol_ammo in content and 'Ammo teernada' not in content:
    content = content.replace(old_pistol_ammo, new_pistol_ammo)
    print("Updated pistol out-of-ammo roast.")

old_smg_ammo = '''      } else if (State.currentWeapon === 'smg') {
        if (State.ammo.smg <= 0) {
          showToast("OUT OF SMG AMMO! Swapping to Fists");'''

new_smg_ammo = '''      } else if (State.currentWeapon === 'smg') {
        if (State.ammo.smg <= 0) {
          showToast("OUT OF SMG AMMO! Swapping to Fists");
          showNarrativeDialog("Game Dev", "Ammo teernu ", null, 10000);'''

if old_smg_ammo in content and 'Ammo teernu' not in content:
    content = content.replace(old_smg_ammo, new_smg_ammo)
    print("Updated smg out-of-ammo roast.")

old_shotgun_ammo = '''      } else if (State.currentWeapon === 'shotgun') {
        if (State.ammo.shotgun <= 0) {
          showToast("OUT OF SHOTGUN SHELLS! Swapping to Fists");'''

new_shotgun_ammo = '''      } else if (State.currentWeapon === 'shotgun') {
        if (State.ammo.shotgun <= 0) {
          showToast("OUT OF SHOTGUN SHELLS! Swapping to Fists");
          showNarrativeDialog("Game Dev", "Haaa aduta gun eduku ", null, 10000);'''

if old_shotgun_ammo in content and 'Haaa aduta gun eduku' not in content:
    content = content.replace(old_shotgun_ammo, new_shotgun_ammo)
    print("Updated shotgun out-of-ammo roast.")

old_rifle_ammo = '''      } else if (State.currentWeapon === 'rifle') {
        if (State.ammo.rifle <= 0) {
          showToast("OUT OF RIFLE AMMO! Swapping to Fists");'''

new_rifle_ammo = '''      } else if (State.currentWeapon === 'rifle') {
        if (State.ammo.rifle <= 0) {
          showToast("OUT OF RIFLE AMMO! Swapping to Fists");
          showNarrativeDialog("Game Dev", "Adum teernu ", null, 10000);'''

if old_rifle_ammo in content and 'Adum teernu' not in content:
    content = content.replace(old_rifle_ammo, new_rifle_ammo)
    print("Updated rifle out-of-ammo roast.")

old_grenade_ammo = '''      } else if (State.currentWeapon === 'grenade') {
        if (State.ammo.grenade <= 0) {
          showToast("OUT OF GRENADES! Swapping to Fists");'''

new_grenade_ammo = '''      } else if (State.currentWeapon === 'grenade') {
        if (State.ammo.grenade <= 0) {
          showToast("OUT OF GRENADES! Swapping to Fists");
          showNarrativeDialog("Game Dev", "Allelum grenede ninak ullad alla ", null, 10000);'''

if old_grenade_ammo in content and 'Allelum grenede ninak ullad alla' not in content:
    content = content.replace(old_grenade_ammo, new_grenade_ammo)
    print("Updated grenade out-of-ammo roast.")

old_rpg_ammo = '''      } else if (State.currentWeapon === 'rpg') {
        if (State.ammo.rpg <= 0) {
          showToast("OUT OF ROCKETS! Swapping to Fists");'''

new_rpg_ammo = '''      } else if (State.currentWeapon === 'rpg') {
        if (State.ammo.rpg <= 0) {
          showToast("OUT OF ROCKETS! Swapping to Fists");
          showNarrativeDialog("Game Dev", "Ada gommale ", null, 10000);'''

if old_rpg_ammo in content and 'Ada gommale' not in content:
    content = content.replace(old_rpg_ammo, new_rpg_ammo)
    print("Updated rpg out-of-ammo roast.")

# 4. Remove the red error box popup completely from animate() catch block
animate_catch_old = '''      } catch(e) {
        if (!_animErrShown) {
          _animErrShown = true;
          console.error('[ViceBlocks] animate() ERROR frame', _frameCount, e);
          document.body.insertAdjacentHTML('beforeend', `<div style="position:fixed;top:30%;left:50%;transform:translate(-50%,-50%);background:#c00;color:#fff;padding:20px;border-radius:8px;z-index:99999;font-size:13px;max-width:90vw;max-height:80vh;overflow:auto">animate ERROR frame ${_frameCount}:<br><b>${e.message}</b><br><pre style="white-space:pre-wrap;font-size:11px;margin-top:10px">${e.stack}</pre></div>`);
        }
      }'''

animate_catch_new = '''      } catch(e) {
        // Safe catch: Keep game running smoothly, never display red error popups on user screen
        console.error('[ViceBlocks] animate() catch:', e);
      }'''

if animate_catch_old in content:
    content = content.replace(animate_catch_old, animate_catch_new)
    print("Removed red error popup in animate() successfully.")
else:
    print("animate_catch_old not matched directly, checking regex...")
    catch_regex = re.compile(r'\} catch\(e\) \{\s*if \(!_animErrShown\) \{[\s\S]*?document\.body\.insertAdjacentHTML[\s\S]*?\}\s*\}', re.MULTILINE)
    if catch_regex.search(content):
        content = catch_regex.sub('} catch(e) {\n        console.error("[ViceBlocks] animate() catch:", e);\n      }', content)
        print("Removed red error popup with regex.")

# 5. Guard dt in RobloxVehicle methods and vehicle loop
# Check checkSolidCollisions definition
content = content.replace('checkSolidCollisions(dt = 0.016) {', '''checkSolidCollisions(dt = 0.016) {
        if (typeof dt === 'undefined' || isNaN(dt) || dt <= 0) dt = 0.016;''')

content = content.replace('update(dt, input) {', '''update(dt = 0.016, input = {}) {
        if (typeof dt === 'undefined' || isNaN(dt) || dt <= 0) dt = 0.016;
        if (!input) input = {};''')

content = content.replace('updateAirplane(dt, input) {', '''updateAirplane(dt = 0.016, input = {}) {
        if (typeof dt === 'undefined' || isNaN(dt) || dt <= 0) dt = 0.016;
        if (!input) input = {};''')

# Check vehicle loop in animate:
old_v_loop = 'vehicles.forEach(v => v.update(dt, (v === State.currentVehicle && !State.inMenu) ? keys : null));'
new_v_loop = 'const _safeDt = (typeof dt !== "undefined" && dt > 0) ? dt : 0.016;\n      vehicles.forEach(v => v.update(_safeDt, (v === State.currentVehicle && !State.inMenu) ? keys : {}));'

if old_v_loop in content:
    content = content.replace(old_v_loop, new_v_loop)
    print("Safeguarded vehicle update loop in animate.")

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying updates to index.html.")

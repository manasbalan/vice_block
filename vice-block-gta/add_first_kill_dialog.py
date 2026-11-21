import re
import os

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Update State to include hasKilledFirstPerson
old_state = """    const State = {
      cash: 500,
      health: 100,
      maxHealth: 100,
      wantedLevel: 0,
      wantedTimer: 0,
      character: 'Lucia',
      inVehicle: false,
      currentVehicle: null,
      currentMission: 1,
      radioPlaying: true,
      inMenu: true,"""

new_state = """    const State = {
      cash: 500,
      health: 100,
      maxHealth: 100,
      wantedLevel: 0,
      wantedTimer: 0,
      character: 'Lucia',
      inVehicle: false,
      currentVehicle: null,
      currentMission: 1,
      radioPlaying: true,
      inMenu: true,
      hasKilledFirstPerson: false,"""

assert old_state in text, "Could not find old_state"
text = text.replace(old_state, new_state)

# 2. Update HTML of #narrative-dialog to support dynamic text & speaker
old_dialog_html = """  <!-- GAME DEV NARRATIVE DIALOGUE BOX (POKÉMON STYLE) -->
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
  </div>"""

new_dialog_html = """  <!-- GAME DEV NARRATIVE DIALOGUE BOX (POKÉMON STYLE) -->
  <div id="narrative-dialog" onclick="closeNarrativeDialog()">
    <div class="narrative-tag">
      <span>👨‍💻</span>
      <span id="narrative-speaker-text">Game Dev</span>
    </div>
    <div class="narrative-text" id="narrative-message-text">
      Don't expect too much, cause the developer is having exam ;)
      <span class="highlight">Enjoy the game !</span>
    </div>
    <div class="narrative-prompt">TAP ANYWHERE TO CONTINUE ▶</div>
  </div>"""

assert old_dialog_html in text, "Could not find old_dialog_html"
text = text.replace(old_dialog_html, new_dialog_html)

# 3. Update showNarrativeDialog and add onPersonKilled()
old_narrative_js = """    let _narrativeTimer = null;
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

new_narrative_js = """    let _narrativeTimer = null;
    function showNarrativeDialog(speaker = "Game Dev", message = "", subtext = null, duration = 7500) {
      const el = document.getElementById('narrative-dialog');
      if (!el) return;

      const speakerEl = document.getElementById('narrative-speaker-text');
      if (speakerEl) speakerEl.innerText = speaker;

      const msgEl = document.getElementById('narrative-message-text');
      if (msgEl) {
        msgEl.innerHTML = `${message}${subtext ? `<span class="highlight">${subtext}</span>` : ''}`;
      }

      el.style.display = 'block';
      Sound.playWhistle();
      clearTimeout(_narrativeTimer);
      _narrativeTimer = setTimeout(() => {
        closeNarrativeDialog();
      }, duration);
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

    // First Kill Easter Egg Message from Developer!
    function onPersonKilled(victimType = 'civilian') {
      if (!State.hasKilledFirstPerson) {
        State.hasKilledFirstPerson = true;
        setTimeout(() => {
          showNarrativeDialog(
            "Game Dev",
            "maan what did he even do to you",
            null,
            6500
          );
        }, 400);
      }
    }

    function startGameplay() {
      State.inMenu = false;
      mainMenuOverlay.classList.add('hidden');
      Sound.init();
      showToast(`WELCOME TO VICE CITY! VISIT BURGER SHOT OR GRAB YOUR RIDE!`);
      // Trigger Game Dev Narrative Dialog right outside Safehouse!
      setTimeout(() => {
        showNarrativeDialog(
          "Game Dev",
          "Don't expect too much, cause the developer is having exam ;)",
          "Enjoy the game !"
        );
      }, 600);
    }"""

assert old_narrative_js in text, "Could not find old_narrative_js"
text = text.replace(old_narrative_js, new_narrative_js)

# 4. Hook onPersonKilled() into RobloxNPC.die()
old_npc_die = """      die() {
        this.isDead = true;
        this.group.rotation.x = Math.PI / 2;
        this.group.position.y = 0.5;
        addCash(100);
        showToast("Civilian Defeated! +$100 Cash Dropped!");
        Sound.playCash();

        if (State.wantedLevel === 0) {"""

new_npc_die = """      die() {
        this.isDead = true;
        this.group.rotation.x = Math.PI / 2;
        this.group.position.y = 0.5;
        addCash(100);
        showToast("Civilian Defeated! +$100 Cash Dropped!");
        Sound.playCash();

        // First Kill Easter Egg Check
        onPersonKilled('civilian');

        if (State.wantedLevel === 0) {"""

assert old_npc_die in text, "Could not find old_npc_die"
text = text.replace(old_npc_die, new_npc_die)

# 5. Hook onPersonKilled() into RobloxFootCop.die()
old_cop_die = """      die() {
        this.isDead = true;
        this.group.rotation.x = Math.PI / 2;
        this.group.position.y = 0.4;
        addCash(150);
        showToast("👮 COP DOWN! +$150 Cash & Ammo Dropped!");
        Sound.playCash();
        State.ammo.pistol += 20;
        if (player) player.updateWeaponBadge();"""

new_cop_die = """      die() {
        this.isDead = true;
        this.group.rotation.x = Math.PI / 2;
        this.group.position.y = 0.4;
        addCash(150);
        showToast("👮 COP DOWN! +$150 Cash & Ammo Dropped!");
        Sound.playCash();
        State.ammo.pistol += 20;
        if (player) player.updateWeaponBadge();

        // First Kill Easter Egg Check
        onPersonKilled('cop');"""

assert old_cop_die in text, "Could not find old_cop_die"
text = text.replace(old_cop_die, new_cop_die)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("First kill narrative dialog hook added successfully!")

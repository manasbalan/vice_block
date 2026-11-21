import re
import os

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add DEV_ROBBERY_QUOTES and onPersonRobbed() function
old_on_killed = """    // First Kill Easter Egg Message from Developer!
    function onPersonKilled(victimType = 'civilian') {"""

new_on_robbed = """    // --- DEVELOPER ROBBERY ROAST MESSAGES (CUSTOMIZABLE LIST) ---
    // Feel free to add more lines to this list anytime!
    const DEV_ROBBERY_QUOTES = [
      "Picha karane engilum verude vidu",
      "Adum mukki",
      "Valla panikum poda daridravasi"
    ];

    let _lastRobberyQuoteTime = 0;
    function onPersonRobbed() {
      const now = performance.now();
      // 3-second debounce so player can comfortably read each quote
      if (now - _lastRobberyQuoteTime > 3000) {
        _lastRobberyQuoteTime = now;
        const randomQuote = DEV_ROBBERY_QUOTES[Math.floor(Math.random() * DEV_ROBBERY_QUOTES.length)];
        showNarrativeDialog("Game Dev", randomQuote, null, 4200);
      }
    }

    // First Kill Easter Egg Message from Developer!
    function onPersonKilled(victimType = 'civilian') {"""

assert old_on_killed in text, "Could not find old_on_killed"
text = text.replace(old_on_killed, new_on_robbed, 1)

# 2. Hook onPersonRobbed() into RobloxNPC.takeDamage() and die()
old_rob_civilian = """        if (this.health <= 0) {
          this.die();
        } else {
          // Drop a small cash tip when hit
          addCash(25);
          showToast("Robbed Civilian! +$25 Cash");
        }"""

new_rob_civilian = """        if (this.health <= 0) {
          this.die();
        } else {
          // Drop a small cash tip when hit (Robbery)
          addCash(25);
          showToast("Robbed Civilian! +$25 Cash");
          onPersonRobbed();
        }"""

assert old_rob_civilian in text, "Could not find old_rob_civilian"
text = text.replace(old_rob_civilian, new_rob_civilian, 1)

old_npc_die_check = """        // First Kill Easter Egg Check
        onPersonKilled('civilian');"""

new_npc_die_check = """        // First Kill or Robbery Roast Check
        if (!State.hasKilledFirstPerson) {
          onPersonKilled('civilian');
        } else {
          onPersonRobbed();
        }"""

assert old_npc_die_check in text, "Could not find old_npc_die_check"
text = text.replace(old_npc_die_check, new_npc_die_check, 1)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Robbery roast quotes added successfully!")

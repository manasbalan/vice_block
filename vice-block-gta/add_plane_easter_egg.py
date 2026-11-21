import re
import os

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. Add hasStolenFirstPlane to State
if "hasStolenFirstPlane" not in text:
    old_state = """      hasKilledFirstPerson: false,"""
    new_state = """      hasKilledFirstPerson: false,
      hasStolenFirstPlane: false,"""
    assert old_state in text, "Could not find old_state"
    text = text.replace(old_state, new_state, 1)

# 2. Match nearest.isPlane block with regex
pattern = r'if \(nearest\.isPlane\) \{[\s\S]*?\} else if \(nearest\.isTank\)'
m = re.search(pattern, text)
assert m, "Could not match nearest.isPlane block"

matched_str = m.group(0)

injection = """            // --- FIRST TIME AIRPLANE THEFT EASTER EGG (MALAYALAM DEVELOPER ROAST) ---
            if (!State.hasStolenFirstPlane) {
              State.hasStolenFirstPlane = true;
              // 1. Initial message when stealing the plane
              setTimeout(() => {
                showNarrativeDialog("Game Dev", "Adu kond ninak enda karyam", null, 3600);
              }, 400);

              // 2. Blast the plane after riding for a few seconds!
              setTimeout(() => {
                if (State.inVehicle && State.currentVehicle && State.currentVehicle.isPlane) {
                  const stolenPlane = State.currentVehicle;
                  createExplosion(stolenPlane.group.position.clone(), 16, 120);
                  stolenPlane.takeDamage(600);

                  // 3. Follow-up narrative reaction immediately after the explosion
                  setTimeout(() => {
                    showNarrativeDialog("Game Dev", "Valla avashyam undayno task cheyda pore ", null, 8000);
                  }, 650);
                }
              }, 3800);
            }
          } else if (nearest.isTank)"""

new_matched_str = re.sub(r'\} else if \(nearest\.isTank\)', injection, matched_str)
text = text[:m.start()] + new_matched_str + text[m.end():]

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Plane theft Easter egg added successfully with regex!")

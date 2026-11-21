import re
import os

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. ADD BUSTED SYSTEM AND UPDATE damagePlayer
old_damage_player = """    function damagePlayer(amount) {
      State.health -= amount;
      if (State.health <= 0) killPlayer();
      updateHealthUI();
    }"""

new_damage_player = """    function damagePlayer(amount) {
      State.health -= amount;
      if (State.health <= 0) {
        if (State.wantedLevel > 0) {
          bustPlayer();
        } else {
          killPlayer();
        }
      }
      updateHealthUI();
    }"""

assert old_damage_player in text, "Could not find old_damage_player"
text = text.replace(old_damage_player, new_damage_player)

# 2. UPDATE killPlayer AND ADD bustPlayer
old_kill_player = """    function killPlayer() {
      Sound.playOof();
      const death = document.getElementById('death-screen');
      death.style.display = 'flex';
      if (State.inVehicle) toggleVehicle();

      setTimeout(() => {
        State.health = 100;
        State.cash = Math.max(0, State.cash - 200);
        setWantedLevel(0);
        updateHealthUI();
        document.getElementById('cash-val').innerText = State.cash.toLocaleString();
        const cp = State.activeCheckpoint || { name: "Ocean View Safehouse", x: -55, z: -100 };
        player.group.position.set(cp.x, 0, cp.z);
        resetAirportFleet(); // Airplanes and jets reset to original runway spots!
        death.style.display = 'none';
        showToast(`Respawned at ${cp.name} • Fleet Reset! (-$200 Hospital Bill)`);
      }, 2500);
    }"""

new_kill_player = """    function killPlayer() {
      Sound.playOof();
      const death = document.getElementById('death-screen');
      death.style.display = 'flex';
      const title = document.getElementById('death-title');
      if (title) {
        title.innerText = "WASTED";
        title.style.color = "#dc2626";
      }
      const desc = document.getElementById('death-desc');
      if (desc) desc.innerText = "Wasted in Vice City! -$200 Hospital Bill";
      if (State.inVehicle) toggleVehicle();

      setTimeout(() => {
        State.health = 100;
        State.cash = Math.max(0, State.cash - 200);
        setWantedLevel(0);
        updateHealthUI();
        document.getElementById('cash-val').innerText = State.cash.toLocaleString();
        const cp = State.activeCheckpoint || { name: "Ocean View Safehouse", x: -55, z: -100 };
        player.group.position.set(cp.x, 0, cp.z);
        resetAirportFleet();
        death.style.display = 'none';
        showToast(`Respawned at ${cp.name} • Fleet Reset! (-$200 Hospital Bill)`);
      }, 2500);
    }

    function bustPlayer() {
      Sound.playSiren();
      const death = document.getElementById('death-screen');
      death.style.display = 'flex';
      const title = document.getElementById('death-title');
      if (title) {
        title.innerText = "BUSTED";
        title.style.color = "#00f3ff";
      }
      const desc = document.getElementById('death-desc');
      if (desc) desc.innerText = "Arrested by Vice City Police! -$100 Bail Bill";
      if (State.inVehicle) toggleVehicle();

      setTimeout(() => {
        State.health = 100;
        State.cash = Math.max(0, State.cash - 100);
        setWantedLevel(0);
        updateHealthUI();
        document.getElementById('cash-val').innerText = State.cash.toLocaleString();

        // RESPAWN WALKING OUT OF VCPD POLICE STATION ENTRANCE!
        player.group.position.set(55, 0, 33);
        player.group.rotation.y = Math.PI; // Face outwards toward road
        resetAirportFleet();
        death.style.display = 'none';
        showToast("👮 BUSTED! Released on bail outside VCPD Police Station! (-$100)");
      }, 2500);
    }"""

assert old_kill_player in text, "Could not find old_kill_player"
text = text.replace(old_kill_player, new_kill_player)

# 3. UPDATE PoliceAI (EXIT SQUAD CAR TO ARREST, ENTER TO CHASE BY CAR)
old_police_ai = """    // --- POLICE SQUAD CRUISERS (3-5 Star High-Speed Pursuit) ---
    const policeUnits = [];
    class PoliceAI {
      constructor(x, z, type = 'cop') {
        this.vehicle = new RobloxVehicle({ x, z, type, colorMat: M.copBlack });
        policeUnits.push(this);
      }

      update(dt, playerPos) {
        if (this.disabled || this.vehicle.driver === player) return;
        if (State.wantedLevel <= 0) {
          if (this.vehicle.redL) this.vehicle.redL.material = M.wallDark;
          if (this.vehicle.blueL) this.vehicle.blueL.material = M.wallDark;
          return;
        }

        const carPos = this.vehicle.group.position;
        const targetAngle = Math.atan2(playerPos.x - carPos.x, playerPos.z - carPos.z);
        const dist = Math.hypot(playerPos.x - carPos.x, playerPos.z - carPos.z);

        // Flash emergency lights
        const flash = Math.sin(performance.now() * 0.015) > 0;
        if (this.vehicle.redL) this.vehicle.redL.material = flash ? M.neonPink : M.wallDark;
        if (this.vehicle.blueL) this.vehicle.blueL.material = flash ? M.wallDark : M.neonCyan;

        // WANTED LEVEL 1-2: Foot patrol cops pursue, squad cruisers follow at distance (DO NOT RAM)
        if (State.wantedLevel <= 2) {
          if (dist > 36) {
            let diff = targetAngle - this.vehicle.group.rotation.y;
            while (diff < -Math.PI) diff += Math.PI * 2;
            while (diff > Math.PI) diff -= Math.PI * 2;
            this.vehicle.group.rotation.y += THREE.MathUtils.clamp(diff, -1.5 * dt, 1.5 * dt);
            const cruiseSpeed = 12;
            const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), this.vehicle.group.rotation.y);
            carPos.addScaledVector(forward, cruiseSpeed * dt);
            this.vehicle.speed = cruiseSpeed;
          } else {
            this.vehicle.speed = 0;
          }
          return;
        }

        // WANTED LEVEL 3-5: HIGH SPEED AGGRESSIVE SQUAD CAR PURSUIT & RAMMING!
        let diff = targetAngle - this.vehicle.group.rotation.y;
        while (diff < -Math.PI) diff += Math.PI * 2;
        while (diff > Math.PI) diff -= Math.PI * 2;
        this.vehicle.group.rotation.y += THREE.MathUtils.clamp(diff, -2.8 * dt, 2.8 * dt);

        const chaseSpeed = 22 + State.wantedLevel * 2.5; // up to 34.5 m/s!
        const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), this.vehicle.group.rotation.y);
        carPos.addScaledVector(forward, chaseSpeed * dt);
        this.vehicle.speed = chaseSpeed;

        // Aggressively Ram player
        if (dist < 4.2) {
          damagePlayer(16);
          Sound.playCrash();
          Sound.playOof();
          carPos.addScaledVector(forward, -4);
        }
      }
    }"""

new_police_ai = """    // --- POLICE SQUAD CRUISERS (1-5 Star Pursuit & Tactical Response) ---
    const policeUnits = [];
    class PoliceAI {
      constructor(x, z, type = 'cop') {
        this.vehicle = new RobloxVehicle({ x, z, type, colorMat: M.copBlack });
        this.copOnFoot = null;
        policeUnits.push(this);
      }

      update(dt, playerPos) {
        if (this.disabled || this.vehicle.driver === player) return;
        if (State.wantedLevel <= 0) {
          if (this.vehicle.redL) this.vehicle.redL.material = M.wallDark;
          if (this.vehicle.blueL) this.vehicle.blueL.material = M.wallDark;
          return;
        }

        const carPos = this.vehicle.group.position;
        const targetAngle = Math.atan2(playerPos.x - carPos.x, playerPos.z - carPos.z);
        const dist = Math.hypot(playerPos.x - carPos.x, playerPos.z - carPos.z);

        // Flash emergency lights
        const flash = Math.sin(performance.now() * 0.015) > 0;
        if (this.vehicle.redL) this.vehicle.redL.material = flash ? M.neonPink : M.wallDark;
        if (this.vehicle.blueL) this.vehicle.blueL.material = flash ? M.wallDark : M.neonCyan;

        // DYNAMIC COP AI:
        // 1. If player is ON FOOT and squad car is near (within 22m):
        //    Stop cruiser, officer exits car on foot, draws weapon, and rushes to bust player!
        if (!State.inVehicle) {
          if (dist <= 22) {
            this.vehicle.speed = Math.max(0, this.vehicle.speed - 30 * dt);
            if (!this.copOnFoot || this.copOnFoot.isDead) {
              const exitPos = carPos.clone().add(new THREE.Vector3(2.4, 0, 0));
              this.copOnFoot = new RobloxFootCop(exitPos.x, exitPos.z);
              this.copOnFoot.speed = 14.5;
              Sound.playWhistle();
              showToast("👮 SQUAD CAR OFFICER DEPLOYED: FREEZE!");
            }
            return;
          }
        } else {
          // 2. If player is IN A VEHICLE:
          //    Cops on foot return to cruiser and chase by car!
          if (this.copOnFoot && !this.copOnFoot.isDead) {
            this.copOnFoot.group.visible = false;
            this.copOnFoot.isDead = true;
            this.copOnFoot = null;
          }
        }

        // WANTED LEVEL 1-2: Foot patrol cops pursue, squad cruisers follow at moderate speed
        if (State.wantedLevel <= 2) {
          if (dist > 30) {
            let diff = targetAngle - this.vehicle.group.rotation.y;
            while (diff < -Math.PI) diff += Math.PI * 2;
            while (diff > Math.PI) diff -= Math.PI * 2;
            this.vehicle.group.rotation.y += THREE.MathUtils.clamp(diff, -1.8 * dt, 1.8 * dt);
            const cruiseSpeed = 16;
            const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), this.vehicle.group.rotation.y);
            carPos.addScaledVector(forward, cruiseSpeed * dt);
            this.vehicle.speed = cruiseSpeed;
          } else {
            this.vehicle.speed = 0;
          }
          return;
        }

        // WANTED LEVEL 3-5: HIGH SPEED AGGRESSIVE SQUAD CAR PURSUIT & RAMMING!
        let diff = targetAngle - this.vehicle.group.rotation.y;
        while (diff < -Math.PI) diff += Math.PI * 2;
        while (diff > Math.PI) diff -= Math.PI * 2;
        this.vehicle.group.rotation.y += THREE.MathUtils.clamp(diff, -3.2 * dt, 3.2 * dt);

        const chaseSpeed = 24 + State.wantedLevel * 2.8; // up to 38 m/s!
        const forward = new THREE.Vector3(0, 0, 1).applyAxisAngle(new THREE.Vector3(0, 1, 0), this.vehicle.group.rotation.y);
        carPos.addScaledVector(forward, chaseSpeed * dt);
        this.vehicle.speed = chaseSpeed;

        // Aggressively Ram player vehicle or hit player
        if (dist < 4.5) {
          damagePlayer(18);
          Sound.playCrash();
          Sound.playOof();
          carPos.addScaledVector(forward, -4);
        }
      }
    }"""

assert old_police_ai in text, "Could not find old_police_ai"
text = text.replace(old_police_ai, new_police_ai)

# 4. ADD 3D ILLUMINATED SIGNBOARDS IN buildWalkInBuilding
old_sign = """      // Architectural Neon Accent Fascia Strip (Clean & Sightline-Friendly, No Bulky Floating Text)
      const fascia = new THREE.Mesh(new THREE.BoxGeometry(w * 0.7, 1.0, 0.4), new THREE.MeshBasicMaterial({ color: signCol || 0x00f3ff }));
      fascia.position.set(0, h + 0.5, d / 2 + 0.25);
      group.add(fascia);"""

new_sign = """      // Architectural Neon Accent Fascia Strip
      const fascia = new THREE.Mesh(new THREE.BoxGeometry(w * 0.7, 1.0, 0.4), new THREE.MeshBasicMaterial({ color: signCol || 0x00f3ff }));
      fascia.position.set(0, h + 0.5, d / 2 + 0.25);
      group.add(fascia);

      // 3D Illuminated Facade Signboard with Shop Name and Purpose!
      if (name) {
        const signColorHex = typeof signCol === 'number' ? '#' + signCol.toString(16).padStart(6, '0') : (signCol || '#00f3ff');
        const signMat = createSignCanvasMaterial(name, '#0f0a1c', signColorHex, purpose ? `• ${purpose} •` : null);
        const signMesh = new THREE.Mesh(new THREE.BoxGeometry(w * 0.78, 3.2, 0.45), signMat);
        signMesh.position.set(0, h + 1.8, d / 2 + 0.35);
        group.add(signMesh);
      }"""

assert old_sign in text, "Could not find old_sign"
text = text.replace(old_sign, new_sign)

# 5. ADD AMMU-NATION & PAY 'N' SPRAY SHOPS IN buildCity()
old_club = """      // 5. CLUB MALIBU (Nightclub with grooving NPCs)
      buildWalkInBuilding({
        id: 'club_malibu',
        x: -55, z: 150, w: 30, h: 12, d: 26,
        wallMat: M.wallClub,
        name: "CLUB MALIBU",
        purpose: "DANCE / CHILL",
        signCol: 0xff00aa,
        doorWidth: 9,
        zoneAction: 'club_dance'
      });
    }"""

new_club = """      // 5. CLUB MALIBU (Nightclub with grooving NPCs)
      buildWalkInBuilding({
        id: 'club_malibu',
        x: -55, z: 150, w: 30, h: 12, d: 26,
        wallMat: M.wallClub,
        name: "CLUB MALIBU",
        purpose: "DANCE / CHILL",
        signCol: 0xff00aa,
        doorWidth: 9,
        zoneAction: 'club_dance'
      });

      // 6. AMMU-NATION (Weapons & Ammo Store)
      buildWalkInBuilding({
        id: 'ammu_nation',
        x: 55, z: -140, w: 28, h: 12, d: 24,
        wallMat: new THREE.MeshLambertMaterial({ color: 0x78350f }),
        name: "AMMU-NATION",
        purpose: "GUNS & AMMO STORE",
        signCol: 0xff4500,
        doorWidth: 8,
        zoneAction: 'ammu_nation'
      });

      // 7. PAY 'N' SPRAY (Auto Repair & Clear Heat)
      buildWalkInBuilding({
        id: 'pay_n_spray',
        x: -55, z: -180, w: 32, h: 14, d: 28,
        wallMat: new THREE.MeshLambertMaterial({ color: 0x0284c7 }),
        name: "PAY 'N' SPRAY",
        purpose: "REPAIR CAR & CLEAR STARS",
        signCol: 0x38bdf8,
        doorWidth: 14,
        zoneAction: 'pay_n_spray'
      });
    }"""

assert old_club in text, "Could not find old_club"
text = text.replace(old_club, new_club)

# 6. REPLACE executeBuildingAction WITH REGEX TO INCLUDE AMMU-NATION & PAY 'N' SPRAY
pattern_exec = r'function executeBuildingAction\(z\) \{[\s\S]*?\n    \}'
m = re.search(pattern_exec, text)
assert m, "Could not match executeBuildingAction"

new_exec = """function executeBuildingAction(z) {
      if (z.action === 'safehouse_save') {
        State.health = 100;
        updateHealthUI();
        activateCheckpoint('safehouse', 'Ocean View Safehouse', -55, -112);
        showToast("🏠 SAFEHOUSE SAVED! Full Health Restored & Checkpoint Set!");
        if (State.currentMission === 4) {
          setWantedLevel(0);
          addCash(50000);
          Sound.playCash();
          showToast("🏆 STORYLINE COMPLETED! +$50,000 CASH • RESPECT +");
          setMission(1, "Freeroam Vice City! Visit any building or hijack planes anytime!", -55, -40);
        }
      } else if (z.action === 'heal_player') {
        State.health = 100;
        updateHealthUI();
        Sound.playCash();
        showToast("🍔 ATE BURGER SHOT COMBO! Full Health Restored!");
        if (State.currentMission === 1) {
          activateCheckpoint('burger_shot', 'Burger Shot Plaza', -55, -28);
          setMission(2, "Head South to Escobar Airport & steal the Stunt Plane!", 0, 230);
        }
      } else if (z.action === 'rob_gas') {
        addCash(1500);
        setWantedLevel(Math.min(5, State.wantedLevel + 2));
        Sound.playCash();
        showToast("💰 ROBBED GAS & GO REGISTER! +$1,500 Cash! Cops Dispatched!");
      } else if (z.action === 'rob_bank') {
        addCash(15000);
        setWantedLevel(4);
        Sound.playCash();
        showToast("💎 BANK VAULT CRACKED! +$15,000 Diamonds! 4-STAR WANTED!");
        if (State.currentMission === 3) {
          activateCheckpoint('bank', 'Vice National Bank', 55, -35);
          setMission(4, "Escape 4-Star Heat & Return to Ocean View Safehouse to Save!", -55, -112);
        }
      } else if (z.action === 'police_station') {
        setWantedLevel(3);
        showToast("🚨 INFILTRATED VCPD POLICE HQ! 3-STAR SWAT RESPONSE!");
      } else if (z.action === 'club_dance') {
        showToast("💃 PARTYING AT CLUB MALIBU! Health +20");
        State.health = Math.min(100, State.health + 20);
        updateHealthUI();
        activateCheckpoint('club_malibu', 'Club Malibu VIP', -55, 135);
      } else if (z.action === 'ammu_nation') {
        if (State.cash < 200) {
          showToast("❌ NOT ENOUGH CASH! Need $200 for Ammo Crate");
        } else {
          State.cash -= 200;
          State.ammo.pistol += 50;
          State.ammo.shotgun += 24;
          State.ammo.smg += 120;
          State.ammo.rpg += 6;
          State.ammo.grenades += 5;
          document.getElementById('cash-val').innerText = State.cash.toLocaleString();
          Sound.playCash();
          Sound.playGunshot();
          if (player) player.updateWeaponBadge();
          showToast("🔫 AMMU-NATION: FULL AMMO PACK BOUGHT! -$200");
        }
      } else if (z.action === 'pay_n_spray') {
        if (State.inVehicle && State.currentVehicle) {
          State.currentVehicle.health = State.currentVehicle.maxHealth;
          setWantedLevel(0);
          Sound.playCash();
          showToast("🚗 PAY 'N' SPRAY: VEHICLE REPAIRED & ALL WANTED STARS CLEARED!");
        } else {
          setWantedLevel(0);
          showToast("⭐ WANTED STARS CLEARED AT PAY 'N' SPRAY!");
        }
      }
    }"""

text = text[:m.start()] + new_exec + text[m.end():]

# 7. ADD DYNAMIC POLICE REINFORCEMENTS & EVASION TIMER IN animate()
old_wanted_timer = """      // Wanted timer
      if (State.wantedLevel > 0) {
        State.wantedTimer -= dt;
        if (State.wantedTimer <= 0) {
          setWantedLevel(State.wantedLevel - 1);
          if (State.wantedLevel > 0) State.wantedTimer = 20;
          showToast(`Lost 1 Wanted Star!`);
        }
      }"""

new_wanted_timer = """      // Dynamic Police Reinforcement & Evasion Wanted Timer
      if (State.wantedLevel > 0) {
        // Continuous reinforcements so cops NEVER run out while Wanted!
        window._copSpawnTimer = (window._copSpawnTimer || 0) + dt;
        const targetFootCops = State.wantedLevel * 2 + 1; // 3 to 11 cops
        const targetSquadCars = Math.min(4, Math.max(1, State.wantedLevel));

        const activeLiveFootCops = footCops.filter(c => !c.isDead && c.group.visible).length;
        if (activeLiveFootCops < targetFootCops && window._copSpawnTimer > 3.2) {
          window._copSpawnTimer = 0;
          const spawnAngle = Math.random() * Math.PI * 2;
          const spawnDist = 48 + Math.random() * 20;
          const sx = activePos.x + Math.sin(spawnAngle) * spawnDist;
          const sz = activePos.z + Math.cos(spawnAngle) * spawnDist;
          const newCop = new RobloxFootCop(sx, sz);
          newCop.speed = 13 + State.wantedLevel * 0.8;
          Sound.playWhistle();
        }

        const activeLiveCars = policeUnits.filter(u => u.vehicle.health > 0 && u.vehicle.driver !== player).length;
        if (activeLiveCars < targetSquadCars && window._copSpawnTimer > 4.5) {
          window._copSpawnTimer = 0;
          const spawnAngle = Math.random() * Math.PI * 2;
          const sx = activePos.x + Math.sin(spawnAngle) * 75;
          const sz = activePos.z + Math.cos(spawnAngle) * 75;
          new PoliceAI(sx, sz);
        }

        // Wanted timer only counts down if player is actively hiding / evading cops!
        let nearAnyCop = false;
        for (let c of footCops) {
          if (!c.isDead && c.group.visible && Math.hypot(activePos.x - c.group.position.x, activePos.z - c.group.position.z) < 26) {
            nearAnyCop = true;
            break;
          }
        }
        for (let u of policeUnits) {
          if (u.vehicle.health > 0 && Math.hypot(activePos.x - u.vehicle.group.position.x, activePos.z - u.vehicle.group.position.z) < 32) {
            nearAnyCop = true;
            break;
          }
        }

        if (nearAnyCop) {
          State.wantedTimer = 20; // Heat remains while cops are on player!
        } else {
          State.wantedTimer -= dt;
          if (State.wantedTimer <= 0) {
            setWantedLevel(State.wantedLevel - 1);
            if (State.wantedLevel > 0) State.wantedTimer = 20;
            showToast("🚔 EVADED COPS! Lost 1 Wanted Star!");
          }
        }
      }"""

assert old_wanted_timer in text, "Could not find old_wanted_timer"
text = text.replace(old_wanted_timer, new_wanted_timer)

# 8. ADD SHOP TOUCH PROMPT & TASKS MODAL IN HTML
old_banner = """  <!-- MISSION OBJECTIVE BANNER (COMPACT) -->
  <div id="mission-banner">
    <span class="tag">MISSION 1</span>
    <span id="mission-text">Explore Vice City! Visit Burger Shot or grab the ride at Motel</span>
    <span class="distance" id="mission-dist">(0m)</span>
  </div>"""

new_banner = """  <!-- MISSION OBJECTIVE BANNER (COMPACT & TOUCHABLE) -->
  <div id="mission-banner" onclick="openTasksModal()" style="cursor:pointer;pointer-events:auto;" title="Tap to view Tasks & Missions">
    <span class="tag" id="mission-tag">TASK 1</span>
    <span id="mission-text">Explore Vice City! Visit Burger Shot or grab the ride at Motel</span>
    <span class="distance" id="mission-dist">(0m)</span>
  </div>

  <!-- Interactive Touch Shop Prompt Button -->
  <div id="shop-prompt-container" style="display:none;position:absolute;bottom:85px;left:50%;transform:translateX(-50%);z-index:900;">
    <button id="btn-shop-action" style="background:linear-gradient(135deg, #00f3ff, #0066cc);color:#fff;border:2px solid #fff;border-radius:24px;padding:10px 22px;font-family:'Pricedown',Impact,sans-serif;font-size:16px;letter-spacing:1px;box-shadow:0 0 20px rgba(0,243,255,0.7);cursor:pointer;display:flex;align-items:center;gap:8px;">
      🏪 <span id="shop-prompt-text">ENTER SHOP</span>
    </button>
  </div>

  <!-- TASKS & STORYLINE OBJECTIVES MODAL -->
  <div id="tasks-modal" style="display:none;position:fixed;inset:0;background:rgba(10,5,20,0.88);z-index:99999;backdrop-filter:blur(6px);align-items:center;justify-content:center;padding:16px;">
    <div style="background:#151028;border:2px solid #00f3ff;border-radius:14px;max-width:540px;width:100%;max-height:85vh;overflow:auto;padding:20px;box-shadow:0 0 30px rgba(0,243,255,0.4);color:#fff;">
      <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:2px solid #ff007f;padding-bottom:10px;margin-bottom:15px;">
        <h2 style="margin:0;font-family:'Pricedown',Impact;font-size:24px;color:#fffa65;letter-spacing:1.5px;">VICE BLOCKS MISSIONS & TASKS</h2>
        <button onclick="closeTasksModal()" style="background:#ff0055;border:none;color:#fff;border-radius:6px;padding:6px 14px;font-weight:900;cursor:pointer;">✕</button>
      </div>
      <div id="tasks-list" style="display:flex;flex-direction:column;gap:12px;"></div>
    </div>
  </div>"""

assert old_banner in text, "Could not find old_banner"
text = text.replace(old_banner, new_banner)

# 9. WIRE SHOP BUTTON & TASKS MODAL JS IN animate() AND SETUP
old_minimap_call = """      // 7. RENDER MINIMAP & 3D SCENE
      renderMinimap(activePos);"""

new_minimap_call = """      // Shop Proximity Detection & Touch Button Update
      let activeShopZone = null;
      buildingZones.forEach(z => {
        const d = Math.hypot(activePos.x - z.x, activePos.z - z.z);
        if (d < z.radius + 4) {
          activeShopZone = z;
        }
      });
      const shopBtnContainer = document.getElementById('shop-prompt-container');
      if (shopBtnContainer) {
        if (activeShopZone) {
          shopBtnContainer.style.display = 'block';
          const pText = document.getElementById('shop-prompt-text');
          if (pText) pText.innerText = `${activeShopZone.name} — ${activeShopZone.purpose}`;
        } else {
          shopBtnContainer.style.display = 'none';
        }
      }

      // 7. RENDER MINIMAP & 3D SCENE
      renderMinimap(activePos);"""

assert old_minimap_call in text, "Could not find old_minimap_call"
text = text.replace(old_minimap_call, new_minimap_call)

# Add event listeners for shop button & tasks modal helper functions
old_init_tail = """    // Service Worker ONLY on web browsers, NOT inside native app wrapper (prevents blank screen in APK)"""

new_init_tail = """    // Touch Shop Action Listener
    const shopActionBtn = document.getElementById('btn-shop-action');
    if (shopActionBtn) {
      shopActionBtn.addEventListener('click', () => {
        let activeShopZone = null;
        const activePos = State.inVehicle ? State.currentVehicle.group.position : player.group.position;
        buildingZones.forEach(z => {
          const d = Math.hypot(activePos.x - z.x, activePos.z - z.z);
          if (d < z.radius + 4) activeShopZone = z;
        });
        if (activeShopZone) executeBuildingAction(activeShopZone);
      });
    }

    // Tasks Modal Functions
    window.openTasksModal = function() {
      const modal = document.getElementById('tasks-modal');
      const list = document.getElementById('tasks-list');
      if (!modal || !list) return;
      list.innerHTML = '';
      Missions.forEach((m, idx) => {
        const isCurrent = (State.currentMission === m.id);
        const isDone = (State.currentMission > m.id);
        const item = document.createElement('div');
        item.style.cssText = `padding:12px 14px;border-radius:8px;background:${isCurrent ? 'rgba(0,243,255,0.18)' : 'rgba(255,255,255,0.05)'};border:1px solid ${isCurrent ? '#00f3ff' : (isDone ? '#02b757' : '#475569')};`;
        item.innerHTML = `
          <div style=\"display:flex;justify-content:space-between;align-items:center;\">
            <span style=\"font-weight:900;color:${isCurrent ? '#fffa65' : (isDone ? '#02b757' : '#94a3b8')};\">${isDone ? '✔ COMPLETED' : (isCurrent ? '⭐ ACTIVE TASK' : 'LOCKED')}: ${m.title}</span>
            <span style=\"font-size:11px;background:#1e293b;padding:2px 6px;border-radius:4px;\">Checkpoint</span>
          </div>
          <div style=\"font-size:12px;color:#cbd5e1;margin-top:4px;\">${m.desc}</div>
        `;
        list.appendChild(item);
      });
      modal.style.display = 'flex';
    };

    window.closeTasksModal = function() {
      const modal = document.getElementById('tasks-modal');
      if (modal) modal.style.display = 'none';
    };

    // Service Worker ONLY on web browsers, NOT inside native app wrapper (prevents blank screen in APK)"""

assert old_init_tail in text, "Could not find old_init_tail"
text = text.replace(old_init_tail, new_init_tail)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Part 2 replacements applied successfully!")

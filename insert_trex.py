import os

index_file = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

trex_code = '''
    // --- GIANT T-REX DINOSAUR STAMPEDE SYSTEM ---
    let activeTRex = null;
    let _trexNextStampedeTimer = null;

    class TRexDinosaur {
      constructor(zStart = -350, zEnd = 350) {
        this.group = new THREE.Group();
        this.speed = 34; // Fast thunderous sprint!
        this.runPhase = 0;
        this.zStart = zStart;
        this.zEnd = zEnd;
        this.direction = (zEnd > zStart) ? 1 : -1;
        this.soundPlayed = false;
        this.isDespawned = false;

        this.buildModel();

        // Position in the middle of Central Ave (x = 0)
        this.group.position.set(0, 0, zStart);
        // Face the direction of travel
        this.group.rotation.y = (this.direction > 0) ? 0 : Math.PI;

        scene.add(this.group);
      }

      buildModel() {
        const scale = 2.4; // Towering huge prehistoric predator!

        // Torso / Ribcage
        const bodyGeo = new THREE.BoxGeometry(3.6 * scale, 4.2 * scale, 7.2 * scale);
        const body = new THREE.Mesh(bodyGeo, M.dinoGreen);
        body.position.set(0, 6.2 * scale, 0);
        body.rotation.x = -0.15;
        this.group.add(body);
        this.body = body;

        // Pale Belly Plate
        const bellyGeo = new THREE.BoxGeometry(3.2 * scale, 1.2 * scale, 6.5 * scale);
        const belly = new THREE.Mesh(bellyGeo, M.dinoBelly);
        belly.position.set(0, -1.8 * scale, 0.2 * scale);
        body.add(belly);

        // Spines / Dorsal scales running along the back
        for (let i = -3; i <= 3; i++) {
          const spineGeo = new THREE.ConeGeometry(0.35 * scale, 0.9 * scale, 4);
          const spine = new THREE.Mesh(spineGeo, M.dinoClaw);
          spine.rotation.x = -0.2;
          spine.position.set(0, 2.3 * scale, i * 0.9 * scale);
          body.add(spine);
        }

        // Neck
        const neckGeo = new THREE.BoxGeometry(2.6 * scale, 3.2 * scale, 3.4 * scale);
        const neck = new THREE.Mesh(neckGeo, M.dinoGreen);
        neck.position.set(0, 7.8 * scale, 4.4 * scale);
        neck.rotation.x = 0.35;
        this.group.add(neck);

        // Giant Head
        this.headGroup = new THREE.Group();
        this.headGroup.position.set(0, 9.4 * scale, 6.6 * scale);

        // Upper Skull & Snout
        const skullGeo = new THREE.BoxGeometry(2.8 * scale, 2.6 * scale, 5.2 * scale);
        const skull = new THREE.Mesh(skullGeo, M.dinoGreen);
        skull.position.set(0, 0, 1.2 * scale);
        this.headGroup.add(skull);

        // Ferocious Glowing Red Eyes
        const eyeGeo = new THREE.BoxGeometry(0.4 * scale, 0.4 * scale, 0.6 * scale);
        const eyeL = new THREE.Mesh(eyeGeo, M.dinoEye);
        eyeL.position.set(-1.45 * scale, 0.6 * scale, 0.8 * scale);
        const eyeR = new THREE.Mesh(eyeGeo, M.dinoEye);
        eyeR.position.set(1.45 * scale, 0.6 * scale, 0.8 * scale);
        this.headGroup.add(eyeL, eyeR);

        // Upper Teeth
        for (let t = -1.8; t <= 1.8; t += 0.6) {
          const toothL = new THREE.Mesh(new THREE.ConeGeometry(0.14 * scale, 0.65 * scale, 4), M.dinoTeeth);
          toothL.rotation.x = Math.PI;
          toothL.position.set(-1.3 * scale, -1.3 * scale, (2.2 + t) * scale);

          const toothR = new THREE.Mesh(new THREE.ConeGeometry(0.14 * scale, 0.65 * scale, 4), M.dinoTeeth);
          toothR.rotation.x = Math.PI;
          toothR.position.set(1.3 * scale, -1.3 * scale, (2.2 + t) * scale);

          this.headGroup.add(toothL, toothR);
        }

        // Lower Jaw (Hinged for snapping/roaring)
        this.jaw = new THREE.Group();
        this.jaw.position.set(0, -1.2 * scale, -0.6 * scale);
        const jawMesh = new THREE.Mesh(new THREE.BoxGeometry(2.4 * scale, 1.1 * scale, 4.8 * scale), M.dinoBelly);
        jawMesh.position.set(0, 0, 2.2 * scale);
        this.jaw.add(jawMesh);

        // Lower Teeth
        for (let t = -1.5; t <= 1.5; t += 0.6) {
          const lToothL = new THREE.Mesh(new THREE.ConeGeometry(0.12 * scale, 0.55 * scale, 4), M.dinoTeeth);
          lToothL.position.set(-1.1 * scale, 0.65 * scale, (2.2 + t) * scale);
          const lToothR = new THREE.Mesh(new THREE.ConeGeometry(0.12 * scale, 0.55 * scale, 4), M.dinoTeeth);
          lToothR.position.set(1.1 * scale, 0.65 * scale, (2.2 + t) * scale);
          this.jaw.add(lToothL, lToothR);
        }
        this.headGroup.add(this.jaw);
        this.group.add(this.headGroup);

        // Comical Tiny T-Rex Arms
        const armGeo = new THREE.BoxGeometry(0.5 * scale, 1.4 * scale, 0.6 * scale);
        this.armL = new THREE.Mesh(armGeo, M.dinoGreen);
        this.armL.position.set(-2.0 * scale, 5.8 * scale, 3.4 * scale);
        this.armL.rotation.x = 0.5;

        this.armR = new THREE.Mesh(armGeo, M.dinoGreen);
        this.armR.position.set(2.0 * scale, 5.8 * scale, 3.4 * scale);
        this.armR.rotation.x = 0.5;
        this.group.add(this.armL, this.armR);

        // Massive Hind Legs (Left & Right)
        this.thighL = new THREE.Group();
        this.thighL.position.set(-2.4 * scale, 5.8 * scale, -0.8 * scale);
        const upperLegL = new THREE.Mesh(new THREE.BoxGeometry(1.6 * scale, 4.2 * scale, 2.4 * scale), M.dinoGreen);
        upperLegL.position.y = -1.8 * scale;
        this.thighL.add(upperLegL);

        const shinL = new THREE.Mesh(new THREE.BoxGeometry(1.2 * scale, 3.6 * scale, 1.4 * scale), M.dinoGreen);
        shinL.position.set(0, -4.6 * scale, 0.4 * scale);
        this.thighL.add(shinL);

        const footL = new THREE.Mesh(new THREE.BoxGeometry(2.2 * scale, 0.9 * scale, 3.4 * scale), M.dinoBelly);
        footL.position.set(0, -6.1 * scale, 1.2 * scale);
        this.thighL.add(footL);

        for (let c = -0.7; c <= 0.7; c += 0.7) {
          const claw = new THREE.Mesh(new THREE.ConeGeometry(0.22 * scale, 0.8 * scale, 4), M.dinoClaw);
          claw.rotation.x = -Math.PI / 2;
          claw.position.set(c * scale, -6.1 * scale, 2.9 * scale);
          this.thighL.add(claw);
        }
        this.group.add(this.thighL);

        this.thighR = new THREE.Group();
        this.thighR.position.set(2.4 * scale, 5.8 * scale, -0.8 * scale);
        const upperLegR = new THREE.Mesh(new THREE.BoxGeometry(1.6 * scale, 4.2 * scale, 2.4 * scale), M.dinoGreen);
        upperLegR.position.y = -1.8 * scale;
        this.thighR.add(upperLegR);

        const shinR = new THREE.Mesh(new THREE.BoxGeometry(1.2 * scale, 3.6 * scale, 1.4 * scale), M.dinoGreen);
        shinR.position.set(0, -4.6 * scale, 0.4 * scale);
        this.thighR.add(shinR);

        const footR = new THREE.Mesh(new THREE.BoxGeometry(2.2 * scale, 0.9 * scale, 3.4 * scale), M.dinoBelly);
        footR.position.set(0, -6.1 * scale, 1.2 * scale);
        this.thighR.add(footR);

        for (let c = -0.7; c <= 0.7; c += 0.7) {
          const claw = new THREE.Mesh(new THREE.ConeGeometry(0.22 * scale, 0.8 * scale, 4), M.dinoClaw);
          claw.rotation.x = -Math.PI / 2;
          claw.position.set(c * scale, -6.1 * scale, 2.9 * scale);
          this.thighR.add(claw);
        }
        this.group.add(this.thighR);

        // Huge Segmented Tail (Sways side-to-side)
        this.tail = new THREE.Group();
        this.tail.position.set(0, 6.2 * scale, -3.6 * scale);

        const tailBase = new THREE.Mesh(new THREE.BoxGeometry(2.8 * scale, 3.2 * scale, 4.5 * scale), M.dinoGreen);
        tailBase.position.set(0, -0.4 * scale, -2.1 * scale);
        tailBase.rotation.x = -0.15;
        this.tail.add(tailBase);

        const tailMid = new THREE.Mesh(new THREE.BoxGeometry(2.0 * scale, 2.2 * scale, 4.8 * scale), M.dinoGreen);
        tailMid.position.set(0, -0.8 * scale, -6.2 * scale);
        tailMid.rotation.x = -0.05;
        this.tail.add(tailMid);

        const tailTip = new THREE.Mesh(new THREE.BoxGeometry(1.2 * scale, 1.4 * scale, 5.2 * scale), M.dinoGreen);
        tailTip.position.set(0, -0.9 * scale, -10.6 * scale);
        this.tail.add(tailTip);

        this.group.add(this.tail);
      }

      update(dt) {
        if (this.isDespawned) return;

        // Advance straight down Central Avenue (x = 0)
        this.group.position.z += this.direction * this.speed * dt;
        this.group.position.x = 0;

        // Heavy running animation cycle
        this.runPhase += dt * 8.5;
        const swing = Math.sin(this.runPhase);

        // Legs swinging
        this.thighL.rotation.x = swing * 0.75;
        this.thighR.rotation.x = -swing * 0.75;

        // Arms flailing
        this.armL.rotation.x = 0.5 + Math.sin(this.runPhase * 1.5) * 0.3;
        this.armR.rotation.x = 0.5 - Math.sin(this.runPhase * 1.5) * 0.3;

        // Body heavy stomping bob
        this.group.position.y = Math.abs(swing) * 1.2;

        // Tail balancing sway
        this.tail.rotation.y = swing * 0.35;

        // Jaw chomp / roaring
        this.jaw.rotation.x = 0.2 + (Math.sin(this.runPhase * 0.6) + 1) * 0.22;

        // Player proximity detection
        const pPos = (State.inVehicle && State.currentVehicle) ? State.currentVehicle.group.position : player.group.position;
        const distToPlayer = Math.hypot(this.group.position.x - pPos.x, this.group.position.z - pPos.z);

        // Screen rumble when nearby (< 65m)
        if (distToPlayer < 65) {
          const intensity = (1 - distToPlayer / 65) * 0.45;
          camera.position.x += (Math.random() - 0.5) * intensity;
          camera.position.y += (Math.random() - 0.5) * intensity;
        }

        // --- PLAY SOUND ONCE WHEN IT RUNS NEAR THE PLAYER ---
        if (distToPlayer < 45 && !this.soundPlayed) {
          this.soundPlayed = true;
          try {
            if (dinoScreamAudio) {
              dinoScreamAudio.currentTime = 0;
              dinoScreamAudio.play().catch(e => console.log('[ViceBlocks] Dino audio play error:', e));
            }
          } catch(e){}
          showToast("🦖 T-REX CHARGING NEARBY! WATCH OUT!");
        }

        // Trample / Launch vehicles in Central Avenue
        vehicles.forEach(v => {
          if (!v || !v.group) return;
          const d = Math.hypot(this.group.position.x - v.group.position.x, this.group.position.z - v.group.position.z);
          if (d < 7.5) {
            v.speed = this.direction * 38;
            v.group.position.y += 3.5;
            v.takeDamage(120);
            createExplosion(v.group.position, 6, 50);
            Sound.playCrash();
            showToast("🦖 T-REX SMASHED VEHICLE!");
          }
        });

        // Trample NPCs
        npcs.forEach(npc => {
          if (!npc || npc.isDead) return;
          const d = Math.hypot(this.group.position.x - npc.group.position.x, this.group.position.z - npc.group.position.z);
          if (d < 5.5) {
            npc.takeDamage(100);
            Sound.playPunch();
          }
        });

        // If player is directly run over
        if (distToPlayer < 5.0 && !State.isDead) {
          damagePlayer(25);
          Sound.playPunch();
          showToast("🦖 T-REX TRAMPLE DAMAGE! -25 HP!");
        }

        // Despawn once it has charged through the whole city
        const hasPassedEnd = (this.direction > 0) ? (this.group.position.z > this.zEnd) : (this.group.position.z < this.zEnd);
        if (hasPassedEnd) {
          this.despawn();
        }
      }

      despawn() {
        this.isDespawned = true;
        scene.remove(this.group);
        activeTRex = null;
        showToast("🦖 The Giant T-Rex stampeded out of the city!");
        scheduleNextTRexStampede();
      }
    }

    function triggerTRexStampede() {
      if (activeTRex) return; // already active
      const pPos = (State.inVehicle && State.currentVehicle) ? State.currentVehicle.group.position : player.group.position;
      // Start from opposite side of player along Central Ave
      const startFromNorth = (pPos.z > 0);
      const zStart = startFromNorth ? -350 : 350;
      const zEnd = startFromNorth ? 350 : -350;

      activeTRex = new TRexDinosaur(zStart, zEnd);
      showToast("🦖 WARNING: MASSIVE T-REX RUNNING DOWN CENTRAL AVENUE!");
    }

    function scheduleNextTRexStampede() {
      clearTimeout(_trexNextStampedeTimer);
      // Re-occurs after normal play (random 3 to 4.5 minutes)
      const nextDelay = 180000 + Math.random() * 90000;
      _trexNextStampedeTimer = setTimeout(() => {
        if (!State.inMenu && !State.isDead && !activeTRex) {
          triggerTRexStampede();
        } else {
          scheduleNextTRexStampede();
        }
      }, nextDelay);
    }

    // Schedule initial surprise T-Rex stampede 100 seconds after game start
    setTimeout(() => {
      if (!State.inMenu && !State.isDead && !activeTRex) {
        triggerTRexStampede();
      }
    }, 100000);
'''

# 1. Insert trex_code before `// --- MAIN GAME LOOP ---`
marker_game_loop = '    // --- MAIN GAME LOOP ---'
if marker_game_loop in content and 'class TRexDinosaur' not in content:
    content = content.replace(marker_game_loop, trex_code + '\n' + marker_game_loop)
    print("Inserted TRexDinosaur class and stampede manager.")

# 2. Add activeTRex.update call inside animate()
marker_vehicles = '      vehicles.forEach(v => v.update(_safeDt, (v === State.currentVehicle && !State.inMenu) ? keys : {}));'
dino_update_call = '''      // UPDATE GIANT T-REX DINOSAUR STAMPEDE
      if (activeTRex) {
        activeTRex.update(_safeDt);
      }

      vehicles.forEach(v => v.update(_safeDt, (v === State.currentVehicle && !State.inMenu) ? keys : {}));'''

if marker_vehicles in content and 'activeTRex.update' not in content:
    content = content.replace(marker_vehicles, dino_update_call)
    print("Inserted activeTRex.update inside animate().")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

# Sync to Android Studio projects
android_dirs = [
    os.path.join(r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta', 'android_native_app', 'app', 'src', 'main', 'assets'),
    os.path.join(r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta', 'ViceBlocks_AndroidStudio_Project', 'app', 'src', 'main', 'assets')
]
for ad in android_dirs:
    if os.path.exists(ad):
        shutil.copyfile(index_file, os.path.join(ad, 'index.html'))
        print(f"Synced index.html to {ad}")

print("Done updating index.html with T-Rex Dinosaur.")

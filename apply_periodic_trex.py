import os, shutil

base_dir = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta'
index_file = os.path.join(base_dir, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Add dino materials to M if missing
old_m_grass = 'grass: new THREE.MeshLambertMaterial({ color: 0x2e9b46 }), // Rich emerald green ground'
new_m_dino = '''grass: new THREE.MeshLambertMaterial({ color: 0x2e9b46 }), // Rich emerald green ground
      dinoGreen: new THREE.MeshLambertMaterial({ color: 0x225528 }),     // Deep prehistoric T-Rex reptile skin
      dinoBelly: new THREE.MeshLambertMaterial({ color: 0x6e8b4e }),     // Pale scaly underbelly
      dinoEye: new THREE.MeshBasicMaterial({ color: 0xff1100 }),          // Piercing glowing red eyes
      dinoTeeth: new THREE.MeshLambertMaterial({ color: 0xf8fafc }),       // Razor-sharp bone white teeth
      dinoClaw: new THREE.MeshLambertMaterial({ color: 0x111827 }),        // Dark slate talons & claws'''

if old_m_grass in content and 'dinoGreen' not in content:
    content = content.replace(old_m_grass, new_m_dino, 1)
    print("Added dino materials to M.")

# 2. Add audio elements/objects
old_police_audio_def = '''    // Police Catch Audio: Malayalam "Ayyoo!" despair sound when police catches player
    const policeCatchAudio = new Audio('police_catch.mp3');
    policeCatchAudio.volume = 1.0;'''

new_dino_audio_def = '''    // Police Catch Audio: Malayalam "Ayyoo!" despair sound when police catches player
    const policeCatchAudio = new Audio('police_catch.mp3');
    policeCatchAudio.volume = 1.0;

    // Dino Scream Audio: Funny scream sound when huge T-Rex charges near the player
    const dinoScreamAudio = new Audio('dino_scream.m4a');
    dinoScreamAudio.volume = 1.0;
    dinoScreamAudio.loop = false;'''

if old_police_audio_def in content and 'dinoScreamAudio' not in content:
    content = content.replace(old_police_audio_def, new_dino_audio_def, 1)
    print("Added dinoScreamAudio definition.")
elif 'dinoScreamAudio' not in content:
    # insert before let _narrativeTimer
    content = content.replace('let _narrativeTimer = null;', '''// Dino Scream Audio: Funny scream sound when huge T-Rex charges near the player
    const dinoScreamAudio = new Audio('dino_scream.m4a');
    dinoScreamAudio.volume = 1.0;
    dinoScreamAudio.loop = false;

    // Police Catch Audio: Malayalam "Ayyoo!" despair sound when police catches player
    const policeCatchAudio = new Audio('police_catch.mp3');
    policeCatchAudio.volume = 1.0;

    let _narrativeTimer = null;''', 1)
    print("Inserted dinoScreamAudio and policeCatchAudio before _narrativeTimer.")

# Ensure bustPlayer calls policeCatchAudio
old_bust = '''    function bustPlayer(onRespawn) {
      if (State.isBusted || State.isDead) return;
      State.isBusted = true;
      try {
        if (Sound && typeof Sound.playSiren === 'function') {'''

new_bust = '''    function bustPlayer(onRespawn) {
      if (State.isBusted || State.isDead) return;
      State.isBusted = true;
      try {
        if (typeof policeCatchAudio !== 'undefined' && policeCatchAudio) {
          policeCatchAudio.currentTime = 0;
          policeCatchAudio.play().catch(e => console.log('[ViceBlocks] Police catch audio error:', e));
        }
      } catch(e){}
      try {
        if (Sound && typeof Sound.playSiren === 'function') {'''

if old_bust in content and 'policeCatchAudio.currentTime = 0' not in content:
    content = content.replace(old_bust, new_bust, 1)
    print("Wired policeCatchAudio into bustPlayer().")

# 3. Add Cheat button in modal
old_cheat_btn = '<button class="cheat-btn" data-cheat="BUG" style="border-color:#ff007f;background:rgba(255,0,127,0.22);grid-column:span 2;">🐛 DEVELOPER BUG / GLITCH EASTER EGG</button>'
new_cheat_btn = '''<button class="cheat-btn" data-cheat="BUG" style="border-color:#ff007f;background:rgba(255,0,127,0.22);grid-column:span 2;">🐛 DEVELOPER BUG / GLITCH EASTER EGG</button>
        <button class="cheat-btn" data-cheat="TREX" style="border-color:#10b981;background:rgba(16,185,129,0.22);grid-column:span 2;">🦖 SPAWN GIANT T-REX STAMPEDE</button>'''

if old_cheat_btn in content and 'data-cheat="TREX"' not in content:
    content = content.replace(old_cheat_btn, new_cheat_btn, 1)
    print("Added TREX cheat button to modal.")

# 4. Add Cheat code handler
old_cheat_panzer = '''} else if (code === 'PANZER' || code === 'TANK') {
        spawnRhinoTankAtPlayer();
        showToast("⚡ CHEAT ACTIVATED: MILITARY RHINO TANK SPAWNED!");
        Sound.playCrash();'''

new_cheat_panzer = '''} else if (code === 'TREX' || code === 'DINO' || code === 'JURASSIC') {
        triggerTRexStampede();
        showToast("🦖 CHEAT ACTIVATED: GIANT T-REX STAMPEDE IN CENTRAL AVE!");
      } else if (code === 'PANZER' || code === 'TANK') {
        spawnRhinoTankAtPlayer();
        showToast("⚡ CHEAT ACTIVATED: MILITARY RHINO TANK SPAWNED!");
        Sound.playCrash();'''

if old_cheat_panzer in content and "'TREX'" not in content:
    content = content.replace(old_cheat_panzer, new_cheat_panzer, 1)
    print("Added TREX cheat code execution.")

# 5. Add TRexDinosaur class & periodic manager
trex_class_code = '''
    // --- GIANT T-REX DINOSAUR STAMPEDE SYSTEM ---
    let activeTRex = null;
    let _trexNextStampedeTimer = null;

    class TRexDinosaur {
      constructor(zStart = -360, zEnd = 360) {
        this.group = new THREE.Group();
        this.speed = 58; // High-velocity thunderous sprint down Central Ave!
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

        // Advance straight down Central Avenue (x = 0) at high speed!
        this.group.position.z += this.direction * this.speed * dt;
        this.group.position.x = 0;

        // High-speed furious running animation
        this.runPhase += dt * 14.0;
        const swing = Math.sin(this.runPhase);

        // Legs pumping furiously
        this.thighL.rotation.x = swing * 0.85;
        this.thighR.rotation.x = -swing * 0.85;

        // Arms flailing
        this.armL.rotation.x = 0.5 + Math.sin(this.runPhase * 1.5) * 0.45;
        this.armR.rotation.x = 0.5 - Math.sin(this.runPhase * 1.5) * 0.45;

        // Body heavy stomping bob
        this.group.position.y = Math.abs(swing) * 1.4;

        // Tail balancing sway
        this.tail.rotation.y = swing * 0.4;

        // Snapping jaws
        this.jaw.rotation.x = 0.2 + (Math.sin(this.runPhase * 0.7) + 1) * 0.28;

        // Player proximity detection
        const pPos = (State.inVehicle && State.currentVehicle) ? State.currentVehicle.group.position : player.group.position;
        const distToPlayer = Math.hypot(this.group.position.x - pPos.x, this.group.position.z - pPos.z);

        // Intense camera ground rumble when T-Rex charges nearby (< 70m)
        if (distToPlayer < 70) {
          const intensity = (1 - distToPlayer / 70) * 0.65;
          camera.position.x += (Math.random() - 0.5) * intensity;
          camera.position.y += (Math.random() - 0.5) * intensity;
        }

        // --- PLAY SOUND ONCE WHEN IT RUNS NEAR THE PLAYER ---
        if (distToPlayer < 45 && !this.soundPlayed) {
          this.soundPlayed = true;
          try {
            if (typeof dinoScreamAudio !== 'undefined' && dinoScreamAudio) {
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
          if (d < 8.5) {
            v.speed = this.direction * 48;
            v.group.position.y += 4.5;
            v.takeDamage(150);
            createExplosion(v.group.position, 7, 60);
            Sound.playCrash();
            showToast("🦖 T-REX SMASHED VEHICLE!");
          }
        });

        // Trample NPCs
        npcs.forEach(npc => {
          if (!npc || npc.isDead) return;
          const d = Math.hypot(this.group.position.x - npc.group.position.x, this.group.position.z - npc.group.position.z);
          if (d < 6.0) {
            npc.takeDamage(100);
            Sound.playPunch();
          }
        });

        // If player is directly run over
        if (distToPlayer < 5.5 && !State.isDead) {
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
        // Re-schedules automatically like the developer bug!
        scheduleNextTRexStampede();
      }
    }

    function triggerTRexStampede() {
      if (activeTRex) return; // already running
      const pPos = (State.inVehicle && State.currentVehicle) ? State.currentVehicle.group.position : player.group.position;
      // Start from opposite side of player along Central Ave
      const startFromNorth = (pPos.z > 0);
      const zStart = startFromNorth ? -360 : 360;
      const zEnd = startFromNorth ? 360 : -360;

      activeTRex = new TRexDinosaur(zStart, zEnd);
      showToast("🦖 PREHISTORIC ESCAPE! MASSIVE T-REX CHARGING DOWN CENTRAL AVENUE!");
      showNarrativeDialog("Game Dev", "Jurassic Park ninnu oru T-Rex odi vannittund! Central Avenuennu maari nilkku!", "TREX INCOMING", 8000);
    }

    function scheduleNextTRexStampede() {
      clearTimeout(_trexNextStampedeTimer);
      // Spontaneous surprise interval like the bug: 75 to 110 seconds!
      const nextDelay = 75000 + Math.random() * 35000;
      _trexNextStampedeTimer = setTimeout(() => {
        if (!State.inMenu && !State.isDead && !activeTRex) {
          triggerTRexStampede();
        } else {
          scheduleNextTRexStampede();
        }
      }, nextDelay);
    }

    // Schedule initial surprise T-Rex stampede 45 seconds after game start!
    setTimeout(() => {
      if (!State.inMenu && !State.isDead && !activeTRex) {
        triggerTRexStampede();
      } else {
        scheduleNextTRexStampede();
      }
    }, 45000);
'''

# Insert trex_class_code before // --- MAIN GAME LOOP ---
marker_main_loop = '    // --- MAIN GAME LOOP ---'
if marker_main_loop in content and 'class TRexDinosaur' not in content:
    content = content.replace(marker_main_loop, trex_class_code + '\n' + marker_main_loop, 1)
    print("Inserted TRexDinosaur class and periodic stampede scheduler.")

# In animate(), call activeTRex.update(_safeDt)
marker_vehicles_update = 'vehicles.forEach(v => v.update(_safeDt, (v === State.currentVehicle && !State.inMenu) ? keys : {}));'
dino_update_call = '''// UPDATE GIANT T-REX DINOSAUR STAMPEDE
      if (activeTRex) {
        activeTRex.update(_safeDt);
      }

      vehicles.forEach(v => v.update(_safeDt, (v === State.currentVehicle && !State.inMenu) ? keys : {}));'''

if marker_vehicles_update in content and 'activeTRex.update' not in content:
    content = content.replace(marker_vehicles_update, dino_update_call, 1)
    print("Wired activeTRex.update into animate loop.")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

# Update sw.js with dino_scream.m4a
sw_file = os.path.join(base_dir, 'sw.js')
with open(sw_file, 'r', encoding='utf-8') as f:
    sw_c = f.read()

if "'./dino_scream.m4a'" not in sw_c:
    sw_c = sw_c.replace("'./police_catch.mp3'", "'./police_catch.mp3',\n  './dino_scream.m4a'")
    sw_c = sw_c.replace("const CACHE_NAME = 'vice-blocks-v5';", "const CACHE_NAME = 'vice-blocks-v6';")
    sw_c = sw_c.replace("const CACHE_NAME = 'vice-blocks-v4';", "const CACHE_NAME = 'vice-blocks-v6';")
    with open(sw_file, 'w', encoding='utf-8') as f:
        f.write(sw_c)
    print("Updated sw.js with dino_scream.m4a.")

# Update bundle_release.py
bundle_file = os.path.join(base_dir, 'bundle_release.py')
with open(bundle_file, 'r', encoding='utf-8') as f:
    b_c = f.read()

if '"dino_scream.m4a"' not in b_c:
    b_c = b_c.replace('"police_catch.mp3",', '"police_catch.mp3",\n    "dino_scream.m4a",')
    with open(bundle_file, 'w', encoding='utf-8') as f:
        f.write(b_c)
    print("Updated bundle_release.py with dino_scream.m4a.")

# Sync to Android Studio projects
android_dirs = [
    os.path.join(base_dir, 'android_native_app', 'app', 'src', 'main', 'assets'),
    os.path.join(base_dir, 'ViceBlocks_AndroidStudio_Project', 'app', 'src', 'main', 'assets')
]
for ad in android_dirs:
    if os.path.exists(ad):
        shutil.copyfile(index_file, os.path.join(ad, 'index.html'))
        shutil.copyfile(sw_file, os.path.join(ad, 'sw.js'))
        if os.path.exists(os.path.join(base_dir, 'dino_scream.m4a')):
            shutil.copyfile(os.path.join(base_dir, 'dino_scream.m4a'), os.path.join(ad, 'dino_scream.m4a'))
        print(f"Synced to {ad}")

print("All periodic T-Rex dinosaur updates complete!")

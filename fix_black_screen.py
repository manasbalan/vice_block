import os, re

base_dir = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta'
index_file = os.path.join(base_dir, 'index.html')

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Fix startRadio with light, soothing ambient Miami synthwave chime
old_radio = '''      startRadio() {
        if (!this.ctx) return;
        const notes = [110, 110, 130.81, 146.83, 110, 110, 98, 87.31];
        let step = 0;
        setInterval(() => {
          if (!State.radioPlaying || !this.ctx || this.ctx.state !== 'running') return;
          const osc = this.ctx.createOscillator();
          const gain = this.ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(notes[step % notes.length], this.ctx.currentTime);
          gain.gain.setValueAtTime(0.035, this.ctx.currentTime);
          gain.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + 0.18);
          osc.connect(gain);
          gain.connect(this.ctx.destination);
          osc.start();
          osc.stop(this.ctx.currentTime + 0.2);
          step++;
        }, 220);
      }'''

new_radio = '''      startRadio() {
        if (!this.ctx) return;
        // Light, airy, soothing ambient Miami synthwave chimes (Gentle Cmaj7 / Am7 / Fmaj7 progression)
        const chords = [
          [261.63, 329.63, 392.00, 493.88], // Cmaj7
          [220.00, 261.63, 329.63, 440.00], // Am7
          [174.61, 261.63, 349.23, 440.00], // Fmaj7
          [196.00, 293.66, 392.00, 523.25]  // Gsus4 / G
        ];
        let chordIdx = 0;
        let noteStep = 0;

        setInterval(() => {
          if (!State.radioPlaying || !this.ctx || this.ctx.state !== 'running') return;
          const chord = chords[chordIdx % chords.length];
          const freq = chord[noteStep % chord.length];
          const now = this.ctx.currentTime;

          const osc = this.ctx.createOscillator();
          const filter = this.ctx.createBiquadFilter();
          const gain = this.ctx.createGain();

          osc.type = 'sine'; // Silky smooth, light sine wave
          osc.frequency.setValueAtTime(freq, now);

          // Warm low-pass filter to soften and smooth highs
          filter.type = 'lowpass';
          filter.frequency.setValueAtTime(950, now);

          // Gentle ambient chime envelope with long smooth release
          gain.gain.setValueAtTime(0.0001, now);
          gain.gain.linearRampToValueAtTime(0.016, now + 0.08);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 1.1);

          osc.connect(filter);
          filter.connect(gain);
          gain.connect(this.ctx.destination);

          osc.start(now);
          osc.stop(now + 1.15);

          noteStep++;
          if (noteStep % 4 === 0) {
            chordIdx++;
          }
        }, 580);
      }'''

if old_radio in content:
    content = content.replace(old_radio, new_radio)
    print("Updated startRadio() with light, soothing background sound.")
else:
    print("Warning: old_radio not found in content.")

# 2. Fix 'isMoving' Temporal Dead Zone inside animate()
# Move declaration of let isMoving = false; to the very top of animate()!
old_anim_top = '''    function animate() {
      requestAnimationFrame(animate);
      _frameCount++;
      try {

      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;'''

new_anim_top = '''    function animate() {
      requestAnimationFrame(animate);
      _frameCount++;

      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;
      let isMoving = false; // Declared at top of frame to prevent TDZ ReferenceError

      try {'''

if old_anim_top in content:
    content = content.replace(old_anim_top, new_anim_top)
    print("Moved isMoving to top of animate().")
else:
    print("Warning: old_anim_top not found.")

# Replace the later 'let isMoving = false;' with 'isMoving = false;'
old_later_isMoving = '''      // 1. UPDATE PLAYER ON FOOT (Camera-Relative Smooth 360° Movement)
      let isMoving = false;'''

new_later_isMoving = '''      // 1. UPDATE PLAYER ON FOOT (Camera-Relative Smooth 360° Movement)
      isMoving = false;'''

if old_later_isMoving in content:
    content = content.replace(old_later_isMoving, new_later_isMoving)
    print("Replaced later let isMoving declaration.")
else:
    print("Warning: old_later_isMoving not found.")

# 3. Ensure render always runs even if a gameplay script has an edge case
old_render_end = '''      // 7. RENDER MINIMAP & 3D SCENE
      renderMinimap(activePos);
      renderer.render(scene, camera);

      // Frame 1 debug: log camera & scene info
      if (_frameCount === 1) {
        console.log('[ViceBlocks] Frame 1 — cam:', camera.position, '| scene objs:', scene.children.length, '| canvas:', renderer.domElement.width, 'x', renderer.domElement.height);
      }
      } catch(e) {
        window._lastAnimErr = e.message + ' | ' + (e.stack || ''); console.error('[ViceBlocks] animate() catch:', e);
      }
    }'''

new_render_end = '''      } catch(e) {
        window._lastAnimErr = e.message + ' | ' + (e.stack || '');
        console.error('[ViceBlocks] animate() gameplay catch:', e);
      }

      // 7. RENDER MINIMAP & 3D SCENE (Guaranteed to run every frame, screen NEVER turns black!)
      try {
        const activePos = (State.inVehicle && State.currentVehicle) ? State.currentVehicle.group.position : (player ? player.group.position : new THREE.Vector3(0,0,0));
        renderMinimap(activePos);
        renderer.render(scene, camera);
      } catch(renderErr) {
        console.error('[ViceBlocks] Render catch:', renderErr);
      }

      // Frame 1 debug: log camera & scene info
      if (_frameCount === 1) {
        console.log('[ViceBlocks] Frame 1 — cam:', camera.position, '| scene objs:', scene.children.length, '| canvas:', renderer.domElement.width, 'x', renderer.domElement.height);
      }
    }'''

if old_render_end in content:
    content = content.replace(old_render_end, new_render_end)
    print("Separated gameplay logic and render loop to guarantee 3D scene renders every frame.")
else:
    print("Warning: old_render_end not matched directly, checking regex...")

with open(index_file, 'w', encoding='utf-8') as f:
    f.write(content)

print("Finished applying black screen fix and light background sound.")

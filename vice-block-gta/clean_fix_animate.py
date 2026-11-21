import os, shutil

index_file = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Put let isMoving = false right after lastTime = now;
old_anim_header = '''      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      const activePos = State.inVehicle ? State.currentVehicle.group.position : player.group.position;'''

new_anim_header = '''      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;
      let isMoving = false; // Declared at top of frame to prevent TDZ ReferenceError

      const activePos = State.inVehicle ? State.currentVehicle.group.position : player.group.position;'''

if old_anim_header in content:
    content = content.replace(old_anim_header, new_anim_header, 1)
    print("Fixed isMoving declaration at top of animate().")
else:
    print("Warning: old_anim_header not found!")

# 2. Change the later declaration from 'let isMoving = false;' to 'isMoving = false;'
old_later_decl = '''      // 1. UPDATE PLAYER ON FOOT (Camera-Relative Smooth 360° Movement)
      let isMoving = false;'''

new_later_decl = '''      // 1. UPDATE PLAYER ON FOOT (Camera-Relative Smooth 360° Movement)
      isMoving = false;'''

if old_later_decl in content:
    content = content.replace(old_later_decl, new_later_decl, 1)
    print("Changed later let isMoving to assignment.")
else:
    print("Warning: old_later_decl not found!")

# 3. Completely replace the catch block and ensure renderer.render() is protected
old_end_block = '''      // 7. RENDER MINIMAP & 3D SCENE
      renderMinimap(activePos);
      renderer.render(scene, camera);

      // Frame 1 debug: log camera & scene info
      if (_frameCount === 1) {
        console.log('[ViceBlocks] Frame 1 — cam:', camera.position, '| scene objs:', scene.children.length, '| canvas:', renderer.domElement.width, 'x', renderer.domElement.height);
      }
      } catch(e) {
        if (!_animErrShown) {
          _animErrShown = true;
          console.error('[ViceBlocks] animate() ERROR frame', _frameCount, e);
          document.body.insertAdjacentHTML('beforeend', `<div style="position:fixed;top:30%;left:50%;transform:translate(-50%,-50%);background:#c00;color:#fff;padding:20px;border-radius:8px;z-index:99999;font-size:13px;max-width:90vw;max-height:80vh;overflow:auto">animate ERROR frame ${_frameCount}:<br><b>${e.message}</b><br><pre style="white-space:pre-wrap;font-size:11px;margin-top:10px">${e.stack}</pre></div>`);
        }
      }
    }'''

new_end_block = '''      } catch(e) {
        console.error('[ViceBlocks] animate() gameplay error:', e);
      }

      // 7. RENDER MINIMAP & 3D SCENE (Guaranteed to run every frame, screen NEVER turns black!)
      try {
        const renderPos = (State.inVehicle && State.currentVehicle) ? State.currentVehicle.group.position : (player ? player.group.position : new THREE.Vector3(0,0,0));
        renderMinimap(renderPos);
        renderer.render(scene, camera);
      } catch(renderErr) {
        console.error('[ViceBlocks] Render catch:', renderErr);
      }

      // Frame 1 debug: log camera & scene info
      if (_frameCount === 1) {
        console.log('[ViceBlocks] Frame 1 — cam:', camera.position, '| scene objs:', scene.children.length, '| canvas:', renderer.domElement.width, 'x', renderer.domElement.height);
      }
    }'''

if old_end_block in content:
    content = content.replace(old_end_block, new_end_block, 1)
    print("Replaced old catch block and permanently removed red error popup.")
else:
    print("Warning: old_end_block not found directly!")

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

print("Clean fix applied!")

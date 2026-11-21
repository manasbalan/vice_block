index_file = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(index_file, 'r', encoding='utf-8') as f:
    content = f.read()

old_end = '''      // 7. RENDER MINIMAP & 3D SCENE
      renderMinimap(activePos);
      renderer.render(scene, camera);

      // Frame 1 debug: log camera & scene info
      if (_frameCount === 1) {
        console.log('[ViceBlocks] Frame 1 — cam:', camera.position, '| scene objs:', scene.children.length, '| canvas:', renderer.domElement.width, 'x', renderer.domElement.height);
      }
      } catch(e) {
        // Safe catch: Keep game running smoothly, never display red error popups on user screen
        window._lastAnimErr = e.message + ' | ' + (e.stack || ''); console.error('[ViceBlocks] animate() catch:', e);
      }
    }'''

new_end = '''      } catch(e) {
        window._lastAnimErr = e.message + ' | ' + (e.stack || '');
        console.error('[ViceBlocks] animate() gameplay catch:', e);
      }

      // 7. RENDER MINIMAP & 3D SCENE (Always runs every frame, screen NEVER turns black!)
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

if old_end in content:
    content = content.replace(old_end, new_end)
    with open(index_file, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully separated gameplay and render loops.")
else:
    print("Warning: old_end not matched.")

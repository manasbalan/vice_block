import subprocess
import os

curdir = os.path.dirname(os.path.abspath(__file__))

# Let's inspect the camera matrices, player bounds, and frustum in JavaScript!
test_script = """
<!DOCTYPE html><html><head><script src="three.min.js"></script></head><body>
<div id="status">Starting...</div>
<!-- REPLACE_GAME_SCRIPT -->
<script>
try {
  // Let's inspect camera and player after 1 frame of animate
  const pBox = new THREE.Box3().setFromObject(player.group);
  const camFrustum = new THREE.Frustum();
  const projScreenMatrix = new THREE.Matrix4();
  
  camera.updateMatrixWorld();
  camera.updateProjectionMatrix();
  projScreenMatrix.multiplyMatrices(camera.projectionMatrix, camera.matrixWorldInverse);
  camFrustum.setFromProjectionMatrix(projScreenMatrix);
  
  const inFrustum = camFrustum.intersectsBox(pBox);
  
  const report = {
    cameraPos: { x: camera.position.x, y: camera.position.y, z: camera.position.z },
    cameraRot: { x: camera.rotation.x, y: camera.rotation.y, z: camera.rotation.z },
    cameraNear: camera.near,
    cameraFar: camera.far,
    cameraAspect: camera.aspect,
    cameraFov: camera.fov,
    playerPos: { x: player.group.position.x, y: player.group.position.y, z: player.group.position.z },
    playerBBoxMin: { x: pBox.min.x, y: pBox.min.y, z: pBox.min.z },
    playerBBoxMax: { x: pBox.max.x, y: pBox.max.y, z: pBox.max.z },
    playerInFrustum: inFrustum,
    cheetahPos: { x: cheetah.group.position.x, y: cheetah.group.position.y, z: cheetah.group.position.z },
    cheetahInFrustum: camFrustum.intersectsBox(new THREE.Box3().setFromObject(cheetah.group)),
    rendererDomSize: { width: renderer.domElement.width, height: renderer.domElement.height },
    rendererStyleSize: { width: renderer.domElement.style.width, height: renderer.domElement.style.height }
  };
  
  document.getElementById('status').innerText = 'FRUSTUM_REPORT_START' + JSON.stringify(report) + 'FRUSTUM_REPORT_END';
} catch(err) {
  document.getElementById('status').innerText = 'FRUSTUM_ERR: ' + err.message + ' : ' + err.stack;
}
</script>
</body></html>
"""

with open(os.path.join(curdir, 'index.html'), 'r', encoding='utf-8') as f:
    orig = f.read()

s_idx = orig.find('<script>\n    /* =====================================================================')
if s_idx == -1:
    s_idx = orig.find('<script>')
e_idx = orig.rfind('</script>')
game_script = orig[s_idx:e_idx+9]
game_script_no_animate = game_script.replace('animate();', '// animate();')

full_test_html = test_script.replace('<!-- REPLACE_GAME_SCRIPT -->', game_script_no_animate)
tf_path = os.path.join(curdir, 'test_frustum.html')
with open(tf_path, 'w', encoding='utf-8') as f:
    f.write(full_test_html)

abs_path = tf_path.replace('\\', '/')
cmd = [
    r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
    '--headless=new',
    '--disable-gpu-compositing',
    '--dump-dom',
    '--no-sandbox',
    f'file:///{abs_path}'
]

p = subprocess.run(cmd, capture_output=True, text=True, encoding='utf-8', errors='ignore')
if 'FRUSTUM_REPORT_START' in p.stdout:
    s = p.stdout.split('FRUSTUM_REPORT_START')[1].split('FRUSTUM_REPORT_END')[0]
    import json
    print('REPORT:')
    print(json.dumps(json.loads(s), indent=2))
elif 'FRUSTUM_ERR' in p.stdout:
    print('ERROR:', p.stdout[p.stdout.find('FRUSTUM_ERR'):p.stdout.find('FRUSTUM_ERR')+300])
else:
    print('No report found. STDOUT len:', len(p.stdout), 'Returncode:', p.returncode)

if os.path.exists(tf_path):
    os.remove(tf_path)

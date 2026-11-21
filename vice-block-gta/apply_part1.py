import re
import os

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. FIX RECURSIVE EXPLOSION & VEHICLE TAKE DAMAGE
old_take_damage = """      takeDamage(amt) {
        this.health -= amt;
        if (this.health <= 0) {
          createExplosion(this.group.position, 12, 100);
          if (this.driver === player) {
            damagePlayer(60);
            toggleVehicle();
          }
          this.health = this.maxHealth;
          this.speed = 0;
          this.group.position.y = 0.5;
          showToast(`${this.name} Destroyed!`);
        }
      }"""

new_take_damage = """      takeDamage(amt) {
        if (this.isDead || this.isExploding) return;
        this.health -= amt;
        if (this.health <= 0) {
          this.isDead = true;
          this.isExploding = true;
          this.health = 0;
          this.speed = 0;

          // Safe non-recursive explosion
          createExplosion(this.group.position.clone(), 12, 100);
          if (this.driver === player) {
            damagePlayer(60);
            toggleVehicle();
          }
          showToast(`${this.name} Destroyed!`);

          // Restore vehicle cleanly after delay
          setTimeout(() => {
            this.health = this.maxHealth;
            this.isDead = false;
            this.isExploding = false;
            this.speed = 0;
            this.group.position.y = 0.5;
          }, 4000);
        }
      }"""

assert old_take_damage in text, "Could not find old_take_damage"
text = text.replace(old_take_damage, new_take_damage)

# 2. FIX createExplosion WITH RE-ENTRANCY GUARD & CIVILIAN WANTED STAR
old_exp = """    function createExplosion(pos, radius = 9, damage = 120) {
      Sound.playExplosion();

      // Visual blast sphere
      const sphereMat = new THREE.MeshBasicMaterial({ color: 0xff4500, transparent: true, opacity: 0.95 });
      const sphere = new THREE.Mesh(new THREE.SphereGeometry(1.2, 8, 8), sphereMat);
      sphere.position.copy(pos);
      scene.add(sphere);

      activeExplosions.push({
        mesh: sphere,
        maxRadius: radius,
        currentRadius: 1.2,
        life: 0.38,
        totalLife: 0.38
      });

      // Area Damage to vehicles
      vehicles.forEach(v => {
        const d = Math.hypot(pos.x - v.group.position.x, pos.z - v.group.position.z);
        if (d < radius + v.radius) {
          v.takeDamage(damage * Math.max(0.3, 1 - d / (radius + v.radius)));
          const push = new THREE.Vector3().subVectors(v.group.position, pos).normalize().multiplyScalar(14);
          v.group.position.add(push);
          v.speed = -18;
        }
      });

      // Area Damage to NPCs
      npcs.forEach(npc => {
        if (npc.isDead) return;
        const d = Math.hypot(pos.x - npc.group.position.x, pos.z - npc.group.position.z);
        if (d < radius + 1.2) {
          npc.takeDamage(damage);
        }
      });

      // Foot cops
      footCops.forEach(cop => {
        if (cop.isDead || !cop.group.visible) return;
        const d = Math.hypot(pos.x - cop.group.position.x, pos.z - cop.group.position.z);
        if (d < radius + 1.2) {
          cop.takeDamage(damage);
        }
      });

      // Player damage
      const pDist = Math.hypot(pos.x - player.group.position.x, pos.z - player.group.position.z);
      if (pDist < radius + 1.0 && !State.inVehicle) {
        damagePlayer(Math.round(damage * 0.45 * (1 - pDist / radius)));
        Sound.playOof();
      }
    }"""

new_exp = """    let _isExploding = false;
    function createExplosion(pos, radius = 9, damage = 120) {
      if (_isExploding) return;
      _isExploding = true;
      try {
        Sound.playExplosion();

        // Visual blast sphere
        const sphereMat = new THREE.MeshBasicMaterial({ color: 0xff4500, transparent: true, opacity: 0.95 });
        const sphere = new THREE.Mesh(new THREE.SphereGeometry(1.2, 8, 8), sphereMat);
        sphere.position.copy(pos);
        scene.add(sphere);

        activeExplosions.push({
          mesh: sphere,
          maxRadius: radius,
          currentRadius: 1.2,
          life: 0.38,
          totalLife: 0.38
        });

        // Area Damage to vehicles (Skip dead or exploding vehicles to prevent recursion)
        vehicles.forEach(v => {
          if (v.isDead || v.isExploding) return;
          const d = Math.hypot(pos.x - v.group.position.x, pos.z - v.group.position.z);
          if (d < radius + v.radius) {
            v.takeDamage(damage * Math.max(0.3, 1 - d / (radius + v.radius)));
            const push = new THREE.Vector3().subVectors(v.group.position, pos).normalize().multiplyScalar(14);
            v.group.position.add(push);
            v.speed = -18;
          }
        });

        // Area Damage to NPCs (Civilians)
        let hitCivilians = false;
        npcs.forEach(npc => {
          if (npc.isDead) return;
          const d = Math.hypot(pos.x - npc.group.position.x, pos.z - npc.group.position.z);
          if (d < radius + 1.2) {
            npc.takeDamage(damage);
            hitCivilians = true;
          }
        });

        // If explosion harmed civilians, increase Wanted Level!
        if (hitCivilians) {
          setWantedLevel(Math.min(5, Math.max(State.wantedLevel + 1, 2)));
          showToast("⭐ WANTED LEVEL INCREASED! Explosion harmed civilians!");
        }

        // Foot cops
        footCops.forEach(cop => {
          if (cop.isDead || !cop.group.visible) return;
          const d = Math.hypot(pos.x - cop.group.position.x, pos.z - cop.group.position.z);
          if (d < radius + 1.2) {
            cop.takeDamage(damage);
          }
        });

        // Player damage
        const pDist = Math.hypot(pos.x - player.group.position.x, pos.z - player.group.position.z);
        if (pDist < radius + 1.0 && !State.inVehicle) {
          damagePlayer(Math.round(damage * 0.45 * (1 - pDist / radius)));
          Sound.playOof();
        }
      } finally {
        _isExploding = false;
      }
    }"""

assert old_exp in text, "Could not find old_exp"
text = text.replace(old_exp, new_exp)

# 3. FIX JOYSTICK HORIZONTAL STEERING IN VEHICLES (Ground & Airplane)
old_v_steer = """        // Steering
        if (Math.abs(this.speed) > 0.2) {
          const dir = this.speed >= 0 ? 1 : -1;
          if (typeof joyVector !== 'undefined' && joyTouchId !== null && Math.abs(joyVector.x) > 0.12) {
            this.group.rotation.y -= joyVector.x * this.turnSpeed * dt * dir;
          } else {
            if (input.left) this.group.rotation.y += this.turnSpeed * dt * dir;
            if (input.right) this.group.rotation.y -= this.turnSpeed * dt * dir;
          }
        }"""

new_v_steer = """        // Steering (Right turns Right, Left turns Left)
        if (Math.abs(this.speed) > 0.2) {
          const dir = this.speed >= 0 ? 1 : -1;
          if (typeof joyVector !== 'undefined' && joyTouchId !== null && Math.abs(joyVector.x) > 0.12) {
            this.group.rotation.y += joyVector.x * this.turnSpeed * dt * dir;
          } else {
            if (input.left) this.group.rotation.y -= this.turnSpeed * dt * dir;
            if (input.right) this.group.rotation.y += this.turnSpeed * dt * dir;
          }
        }"""

assert old_v_steer in text, "Could not find old_v_steer"
text = text.replace(old_v_steer, new_v_steer)

old_plane_steer = """        // Yaw Steering & Roll Banking in flight
        if (input.left || (typeof joyVector !== 'undefined' && joyVector.x < -0.2)) {
          this.group.rotation.y += this.turnSpeed * dt;
          this.roll = THREE.MathUtils.lerp(this.roll, -0.4, 0.1);
        } else if (input.right || (typeof joyVector !== 'undefined' && joyVector.x > 0.2)) {
          this.group.rotation.y -= this.turnSpeed * dt;
          this.roll = THREE.MathUtils.lerp(this.roll, 0.4, 0.1);
        } else {
          this.roll = THREE.MathUtils.lerp(this.roll, 0, 0.1);
        }"""

new_plane_steer = """        // Yaw Steering & Roll Banking in flight (Right turns Right, Left turns Left)
        if (input.left || (typeof joyVector !== 'undefined' && joyVector.x < -0.2)) {
          this.group.rotation.y -= this.turnSpeed * dt;
          this.roll = THREE.MathUtils.lerp(this.roll, 0.4, 0.1);
        } else if (input.right || (typeof joyVector !== 'undefined' && joyVector.x > 0.2)) {
          this.group.rotation.y += this.turnSpeed * dt;
          this.roll = THREE.MathUtils.lerp(this.roll, -0.4, 0.1);
        } else {
          this.roll = THREE.MathUtils.lerp(this.roll, 0, 0.1);
        }"""

assert old_plane_steer in text, "Could not find old_plane_steer"
text = text.replace(old_plane_steer, new_plane_steer)

# 4. FIX ON-FOOT KEYBOARD & JOYSTICK STEERING
old_foot_keys = """        if (joyTouchId !== null && (joyVector.x !== 0 || joyVector.y !== 0)) {
          moveX = joyVector.x;
          moveZ = -joyVector.y;
        } else {
          if (keys.forward) moveZ += 1;
          if (keys.backward) moveZ -= 1;
          if (keys.left) moveX += 1;
          if (keys.right) moveX -= 1;
        }"""

new_foot_keys = """        if (joyTouchId !== null && (joyVector.x !== 0 || joyVector.y !== 0)) {
          moveX = joyVector.x;
          moveZ = -joyVector.y;
        } else {
          if (keys.forward) moveZ += 1;
          if (keys.backward) moveZ -= 1;
          if (keys.right) moveX += 1;
          if (keys.left) moveX -= 1;
        }"""

assert old_foot_keys in text, "Could not find old_foot_keys"
text = text.replace(old_foot_keys, new_foot_keys)

# 5. FIX COPS ASSAULT HEAT INCREASE & FASTER RESPAWN
old_cop_damage = """      takeDamage(amount) {
        if (this.isDead) return;
        this.health -= amount;
        Sound.playPunch();
        if (this.health <= 0) {
          this.die();
        }
      }"""

new_cop_damage = """      takeDamage(amount) {
        if (this.isDead) return;
        this.health -= amount;
        Sound.playPunch();
        State.copsAttackedCount = (State.copsAttackedCount || 0) + 1;
        if (State.copsAttackedCount % 2 === 0) {
          setWantedLevel(Math.min(5, State.wantedLevel + 1));
          showToast("⭐ 2 COPS ASSAULTED! WANTED LEVEL INCREASED!");
        }
        if (this.health <= 0) {
          this.die();
        }
      }"""

assert old_cop_damage in text, "Could not find old_cop_damage"
text = text.replace(old_cop_damage, new_cop_damage)

old_cop_die = """        setTimeout(() => {
          this.isDead = false;
          this.health = 50;
          this.group.rotation.x = 0;
          this.group.position.y = 0;
          const p = State.inVehicle ? State.currentVehicle.group.position : player.group.position;
          this.group.position.set(p.x + (Math.random() > 0.5 ? 40 : -40), 0, p.z + (Math.random() > 0.5 ? 40 : -40));
        }, 15000);"""

new_cop_die = """        setTimeout(() => {
          if (State.wantedLevel > 0) {
            this.isDead = false;
            this.health = 50;
            this.group.rotation.x = 0;
            this.group.position.y = 0;
            const p = State.inVehicle ? State.currentVehicle.group.position : player.group.position;
            const ang = Math.random() * Math.PI * 2;
            this.group.position.set(p.x + Math.sin(ang) * 55, 0, p.z + Math.cos(ang) * 55);
            Sound.playWhistle();
          }
        }, 3500);"""

assert old_cop_die in text, "Could not find old_cop_die"
text = text.replace(old_cop_die, new_cop_die)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Part 1 replacements applied successfully!")

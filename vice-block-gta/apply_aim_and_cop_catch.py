import re
import os

filepath = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html"
with open(filepath, "r", encoding="utf-8") as f:
    text = f.read()

# 1. FIX AIM CAMERA: FIRST PERSON WEAPON SCOPE (HIDE PLAYER BODY SO TARGETS IN FRONT ARE VISIBLE)
old_cam_block = """        let camDist, camHeightBase;
        if (State.inVehicle && State.currentVehicle) {
          const v = State.currentVehicle;
          camDist = v.isPlane ? 34 : (v.isTank ? 22 : 17);
          camHeightBase = v.isPlane ? 12 : (v.isTank ? 8.5 : 6.0);
        } else {
          camDist = State.isAiming ? 6.5 : 12.0;
          camHeightBase = State.isAiming ? 2.6 : 4.4;
        }

        const horizDist = camDist * Math.cos(camOrbitPitch);
        const vertHeight = camHeightBase + camDist * Math.sin(camOrbitPitch);

        // Aiming over-shoulder camera offset
        const sideOffset = (State.isAiming && !State.inVehicle) ? 1.4 : 0.0;
        const offX = -Math.sin(camOrbitYaw) * horizDist + Math.cos(camOrbitYaw) * sideOffset;
        const offZ = -Math.cos(camOrbitYaw) * horizDist - Math.sin(camOrbitYaw) * sideOffset;
        const offY = Math.max(1.0, vertHeight);

        const desiredCamPos = new THREE.Vector3(activePos.x + offX, activePos.y + offY, activePos.z + offZ);
        camera.position.lerp(desiredCamPos, 0.25);

        const lookTarget = new THREE.Vector3(
          activePos.x + (State.isAiming ? Math.sin(camOrbitYaw) * 12 : 0),
          activePos.y + (State.inVehicle ? 2.0 : 1.8),
          activePos.z + (State.isAiming ? Math.cos(camOrbitYaw) * 12 : 0)
        );
        camera.lookAt(lookTarget);"""

new_cam_block = """        if (State.isAiming && !State.inVehicle) {
          // 1. Hide player model so it NEVER blocks the scope or people in front!
          player.group.visible = false;

          // 2. Place camera directly at character eye-level (True 1st-Person Tactical Scope View)
          const forwardX = Math.sin(camOrbitYaw);
          const forwardZ = Math.cos(camOrbitYaw);
          const pitchY = Math.sin(camOrbitPitch);

          const desiredCamPos = new THREE.Vector3(
            activePos.x + forwardX * 0.4,
            activePos.y + 3.6,
            activePos.z + forwardZ * 0.4
          );
          camera.position.copy(desiredCamPos);

          // Direct look vector straight through the scope crosshair towards distant targets in front!
          const lookTarget = new THREE.Vector3(
            desiredCamPos.x + forwardX * 80,
            desiredCamPos.y - pitchY * 80,
            desiredCamPos.z + forwardZ * 80
          );
          camera.lookAt(lookTarget);
        } else {
          // Normal Third-Person View (Character model visible)
          player.group.visible = true;

          let camDist, camHeightBase;
          if (State.inVehicle && State.currentVehicle) {
            const v = State.currentVehicle;
            camDist = v.isPlane ? 34 : (v.isTank ? 22 : 17);
            camHeightBase = v.isPlane ? 12 : (v.isTank ? 8.5 : 6.0);
          } else {
            camDist = 12.0;
            camHeightBase = 4.4;
          }

          const horizDist = camDist * Math.cos(camOrbitPitch);
          const vertHeight = camHeightBase + camDist * Math.sin(camOrbitPitch);

          const offX = -Math.sin(camOrbitYaw) * horizDist;
          const offZ = -Math.cos(camOrbitYaw) * horizDist;
          const offY = Math.max(1.0, vertHeight);

          const desiredCamPos = new THREE.Vector3(activePos.x + offX, activePos.y + offY, activePos.z + offZ);
          camera.position.lerp(desiredCamPos, 0.25);

          const lookTarget = new THREE.Vector3(
            activePos.x,
            activePos.y + (State.inVehicle ? 2.0 : 1.8),
            activePos.z
          );
          camera.lookAt(lookTarget);
        }"""

assert old_cam_block in text, "Could not find old_cam_block"
text = text.replace(old_cam_block, new_cam_block)

# 2. FIX PROJECTILE LAUNCH VECTOR WHEN AIMING (Shoot exactly where crosshair aims including pitch)
old_proj_forward = """        const fireAngle = State.isAiming ? camOrbitYaw : player.group.rotation.y;
        const forward = new THREE.Vector3(Math.sin(fireAngle), 0, Math.cos(fireAngle));
        const spawnPos = pPos.clone().add(new THREE.Vector3(0, 2.1, 0)).addScaledVector(forward, 1.2);"""

new_proj_forward = """        const forward = State.isAiming ? 
          new THREE.Vector3(Math.sin(camOrbitYaw) * Math.cos(camOrbitPitch), -Math.sin(camOrbitPitch), Math.cos(camOrbitYaw) * Math.cos(camOrbitPitch)).normalize() :
          new THREE.Vector3(Math.sin(player.group.rotation.y), 0, Math.cos(player.group.rotation.y));
        const spawnPos = pPos.clone().add(new THREE.Vector3(0, State.isAiming ? 3.4 : 2.1, 0)).addScaledVector(forward, 1.2);"""

assert old_proj_forward in text, "Could not find old_proj_forward"
text = text.replace(old_proj_forward, new_proj_forward)

# 3. FIX COPS CATCHING / ARRESTING MECHANISM IN RobloxFootCop.update
old_cop_update = """        // Pursue player on foot
        if (dist > 2.2) {
          const spd = (State.wantedLevel >= 2 ? this.speed * 1.15 : this.speed) * dt;
          this.group.position.x += Math.sin(angle) * spd;
          this.group.position.z += Math.cos(angle) * spd;

          this.animTime += dt * 12;
          const swing = Math.sin(this.animTime) * 0.9;
          this.leftArm.rotation.x = -swing;
          this.rightArm.rotation.x = swing;
          this.leftLeg.rotation.x = swing;
          this.rightLeg.rotation.x = -swing;
        } else {
          // Melee hit player
          this.attackCooldown -= dt;
          if (this.attackCooldown <= 0) {
            this.attackCooldown = 1.0;
            damagePlayer(12);
            Sound.playPunch();
            Sound.playOof();
            showToast("👮 PATROL COP HIT YOU! -12 HP");
          }
        }"""

new_cop_update = """        if (!State.inVehicle) {
          // 1. PURSUE PLAYER ON FOOT (High sprint speed so cops ACTUALLY catch up!)
          const copSpeed = (15.5 + State.wantedLevel * 1.6);
          if (dist > 1.6) {
            const spd = copSpeed * dt;
            this.group.position.x += Math.sin(angle) * spd;
            this.group.position.z += Math.cos(angle) * spd;

            this.animTime += dt * 16;
            const swing = Math.sin(this.animTime) * 1.1;
            this.leftArm.rotation.x = -swing;
            this.rightArm.rotation.x = swing;
            this.leftLeg.rotation.x = swing;
            this.rightLeg.rotation.x = -swing;
          }

          // 2. ACTIVE ARREST / TACKLE CATCH MECHANISM
          if (dist < 3.2) {
            this.tackleTimer = (this.tackleTimer || 0) + dt;

            // Melee strike with nightstick
            this.attackCooldown -= dt;
            if (this.attackCooldown <= 0) {
              this.attackCooldown = 0.8;
              damagePlayer(15);
              Sound.playPunch();
              Sound.playOof();
              showToast("🚨 COP TACKLING YOU! -15 HP (RUN OR GET BUSTED!)");
            }

            // If cop stays on suspect for 1.1 seconds without escape: BUSTED!
            if (this.tackleTimer > 1.1 || State.health <= 0) {
              this.tackleTimer = 0;
              bustPlayer();
              return;
            }

            // If 2 or more cops surround the player within 3.6m: IMMEDIATE ARREST!
            let nearbyCops = 0;
            for (let c of footCops) {
              if (!c.isDead && c.group.visible && Math.hypot(playerPos.x - c.group.position.x, playerPos.z - c.group.position.z) < 3.6) {
                nearbyCops++;
              }
            }
            if (nearbyCops >= 2) {
              this.tackleTimer = 0;
              bustPlayer();
              return;
            }
          } else {
            this.tackleTimer = 0;
          }
        } else {
          // Player is in a vehicle!
          // If vehicle is stopped or moving very slow (< 4.0 mph) and cop reaches the driver door (< 4.2m):
          if (Math.abs(State.currentVehicle.speed) < 4.0 && dist < 4.2) {
            bustPlayer();
            showToast("👮 BUSTED! DRAGGED OUT OF VEHICLE & ARRESTED!");
            return;
          }
          // Otherwise sprint toward vehicle
          const spd = (16.0 + State.wantedLevel * 1.6) * dt;
          this.group.position.x += Math.sin(angle) * spd;
          this.group.position.z += Math.cos(angle) * spd;
        }"""

assert old_cop_update in text, "Could not find old_cop_update"
text = text.replace(old_cop_update, new_cop_update)

# 4. FIX POLICE CRUISER BOX-IN ARREST IN PoliceAI
old_police_ram = """        // Aggressively Ram player vehicle or hit player
        if (dist < 4.5) {
          damagePlayer(18);
          Sound.playCrash();
          Sound.playOof();
          carPos.addScaledVector(forward, -4);
        }"""

new_police_ram = """        // Aggressively Ram player vehicle or hit player
        if (dist < 4.8) {
          damagePlayer(18);
          Sound.playCrash();
          Sound.playOof();
          carPos.addScaledVector(forward, -4);

          // If player's car is pinned or stopped (< 4.0 m/s), box in and arrest!
          if (State.inVehicle && State.currentVehicle && Math.abs(State.currentVehicle.speed) < 4.0) {
            this.boxInTimer = (this.boxInTimer || 0) + dt;
            if (this.boxInTimer > 1.2) {
              this.boxInTimer = 0;
              bustPlayer();
              showToast("👮 BUSTED! SQUAD CAR BOXED YOU IN!");
              return;
            }
          } else {
            this.boxInTimer = 0;
          }
        }"""

assert old_police_ram in text, "Could not find old_police_ram"
text = text.replace(old_police_ram, new_police_ram)

with open(filepath, "w", encoding="utf-8") as f:
    f.write(text)

print("Aim camera & Cop arrest fixes applied successfully!")

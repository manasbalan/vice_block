# VICE BLOCKS: Grand Theft Auto Miami (Roblox Edition)

A high-performance 3D open-world GTA game with a chunky Roblox R6 aesthetic, built for Android mobile phones, low-spec PCs, and browsers. 100% self-contained and offline-ready with procedural Web Audio synthesis and Three.js r128.

---

## 📱 What Files Belong in Your GitHub Repository?

To keep your repository clean, fast to clone, and compatible with the automated Android APK builder, include these files:

### ✅ Essential Game Files (Must Add)
| File / Directory | Purpose |
| :--- | :--- |
| [`index.html`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/index.html) | **Main Game**: Entire 3D world, camera system, touch UI, sound, logic, and cheats. |
| [`three.min.js`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/three.min.js) | **3D Engine**: The Three.js WebGL library (kept local for 100% offline gameplay). |
| [`manifest.json`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/manifest.json) | **PWA Config**: Allows users to "Install" the game directly to their Android/iOS home screen. |
| [`sw.js`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/sw.js) | **Service Worker**: Caches assets so the game loads instantly without internet. |
| `icon-192.png`, `icon-512.png` | **App Icons**: High-res icons for phone launcher and APK packaging. |
| `screenshot1.png`, `screenshot2.png` | **Screenshots**: App previews and store metadata. |
| [`.github/workflows/build-apk.yml`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/.github/workflows/build-apk.yml) | **Automated CI/CD**: Compiles a native Android `.apk` automatically whenever you push to GitHub! |
| [`server.py`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/server.py) & [`play.bat`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/play.bat) | **PC Launchers**: One-click local web server for PC/laptop testing. |
| [`README.md`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/README.md) & [`ANDROID_RELEASE_GUIDE.md`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/ANDROID_RELEASE_GUIDE.md) | **Documentation**: Guides for setup, controls, and Android APK deployment. |
| [`.gitignore`](file:///C:/Users/rames/.gemini/antigravity/scratch/vice-block-gta/.gitignore) | Excludes scratch test files, pycache, and heavy zip archives. |

---

## 🎮 How to Push to GitHub

From your project directory (`vice-block-gta`):

```bash
# 1. Initialize git (if not already done)
git init

# 2. Stage all project files (ignoring temp/scratch files via .gitignore)
git add .

# 3. Commit your changes
git commit -m "Vice Blocks: Mobile touch controls, weapons, tank, cheats, and lush world"

# 4. Link your remote GitHub repository and push
git branch -M main
git remote add origin https://github.com/<YOUR_USERNAME>/<YOUR_REPO_NAME>.git
git push -u origin main
```

> **Automatic APK Build**: Once pushed, check your GitHub repo's **Actions** tab. The `build-apk.yml` workflow will automatically compile and produce an installable **`ViceBlocks-Android-APK`** file ready to download onto any Android phone!

---

## 🕹️ Game Features & Highlights

* **Touch & Mobile First**: Virtual analog joystick for fluid movement, free 360° swipe camera orbit, and dedicated touch pedals for driving, flying, and combat.
* **Camera-Relative 360° Movement**: Character heading dynamically adapts to camera rotation—turn around and push forward to run toward where you look.
* **Weapons & Explosives**:
  * 👊 Fists (melee punch & robbery)
  * 🔫 9mm Pistol (rapid single fire)
  * 💥 Assault Rifle (automatic sustained fire)
  * 🚀 Rocket Launcher / RPG (high-velocity missile projectiles with smoke trails and explosive blast radii)
  * 🎯 Over-the-shoulder Aim mode with on-screen reticle crosshair.
* **Vehicles**:
  * 🚗 Sports Cars (Pink Cheetah, Sedan)
  * 🏍️ Sanchez Dirt Bike
  * ✈️ Flyable Stunt Plane & Jet (at Escobar Airport with altitude and pitch controls)
  * 💣 Military Rhino Tank (heavy caterpillar treads, ramming mass, and explosive artillery cannon)
* **Police Heat System**:
  * **1–2 Stars**: Foot patrol cops pursue on foot, blowing police whistles with nightsticks. Cruisers shadow at a distance.
  * **3–5 Stars**: Squad cruisers launch high-speed ramming pursuits with flashing emergency lights and blaring sirens.
* **One-Tap Cheat Codes**: Tap **⚡ CHEATS** to instantly activate:
  * `TURTLE`: Full 100 HP + $5,000 Cash
  * `GUNSGUNSGUNS`: All Weapons + 999 ammo + 30 RPG rockets
  * `PANZER`: Spawns the Military Rhino Tank
  * `LAWYERUP`: Clear all wanted stars
  * `BRINGITON`: 5-Star maximum police heat
  * `SPEEDFREAK`: 2.5× Super Speed boost
  * `AIRPORT`: Teleport to Escobar Airport Runway
  * `HOME`: Teleport to Ocean View Safehouse
* **Lush Tropical World**: Rich emerald green lawn, palm tree boulevards, park shade trees, concrete sidewalks, glowing streetlamps, water-spraying fire hydrants, and traffic cones.
* **100% Offline Procedural Audio**: Synthwave Miami radio, engine revs, gunfire, explosions, police whistles, and horns synthesized in real-time via Web Audio API.

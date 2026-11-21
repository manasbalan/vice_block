# 📱 Android APK & Google Play Release Guide
## Vice Blocks: Leonida Heist

This guide explains how to package and release your 3D blocky game as a native **Android APK** (for direct phone installs) and an **Android App Bundle (.aab)** for the **Google Play Store**.

---

### ⚠️ IMPORTANT: Trademark & Store Policy Safety
* **DO NOT** name the app *"GTA 6"* or *"Grand Theft Auto"* on the Google Play Store or in your APK package name!
* Take-Two Interactive aggressively files DMCA takedowns against games using the GTA name, which can lead to your Google Play developer account being banned.
* **Safe, Approved App Names:**
  * *Vice Blocks: Leonida Heist*
  * *Block City: Vice Stories*
  * *Block Heist: 3D Crime World*
  * *Duo Heist: Ocean Coast*

---

## 🚀 Method 1: Fast Cloud Packaging via PWABuilder (Recommended - No Android Studio Needed)

Because your game already includes `manifest.json`, `sw.js`, and high-res app icons (`icon-192.png`, `icon-512.png`), you can generate an APK and Google Play bundle in under 3 minutes using Microsoft and Google's official PWA tool.

### Step 1: Upload to Free Web Hosting
Your game needs a live HTTPS link. You can host it for free in 60 seconds on **GitHub Pages**, **Vercel**, or **Netlify**:

#### Free GitHub Pages Option:
1. Create a free account at [github.com](https://github.com)
2. Create a new repository named `vice-blocks`
3. Push or drag-and-drop the files from `C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta` into the repository:
   * `index.html`
   * `three.min.js`
   * `manifest.json`
   * `sw.js`
   * `icon-192.png`
   * `icon-512.png`
4. In GitHub, go to **Settings > Pages > Branch: main > Save**.
5. Your game will now be live at: `https://<your-username>.github.io/vice-blocks/`

### Step 2: Generate the Android APK & AAB
1. Open [PWABuilder.com](https://www.pwabuilder.com/) in your browser.
2. Paste your live game URL (e.g., `https://<your-username>.github.io/vice-blocks/`) and click **Start**.
3. PWABuilder will scan your manifest and report a score of **100% Ready**.
4. Click **Package for Stores** > **Android**.
5. Customize:
   * **App Name:** `Vice Blocks`
   * **Package ID:** `com.yourname.viceblocks`
   * **Display Mode:** `Fullscreen` (or `Standalone`)
   * **Screen Orientation:** `Landscape`
6. Click **Generate Package**.
7. Download the `.zip` file! Inside you will find:
   * `app-release-signed.apk` → Send this to any Android phone to install and play immediately!
   * `app-release-bundle.aab` → Upload this directly to the Google Play Console!

---

## 🏪 How to Publish on the Google Play Store

Once you have your `app-release-bundle.aab`:

1. **Sign Up for Google Play Console:**
   * Go to [play.google.com/console](https://play.google.com/console).
   * Pay the one-time $25 Google Developer registration fee.
2. **Create New App:**
   * Click **Create App** > Enter App Name: *Vice Blocks: Leonida Heist*.
   * Select **Game** > **Free**.
3. **App Setup & Questionnaire:**
   * Complete the Content Rating questionnaire (Action / Violence).
   * Set Privacy Policy (you can generate a free one using `privacypolicygenerator.info`).
4. **Store Listing:**
   * Upload 2-3 screenshots of the game (take in-game screenshots of the sports car, bank robbery, and city).
   * Upload the 512x512 app icon (`icon-512.png`).
   * Upload a Feature Graphic banner (1024x500).
5. **Upload the Bundle:**
   * Go to **Production > Releases > Create Release**.
   * Drag and drop the `app-release-bundle.aab` file from PWABuilder.
6. **Submit for Review:**
   * Google typically reviews and approves indie games within 24 to 72 hours.
   * Once approved, your game is live globally on the Google Play Store!

---

## 📲 How to Install Directly on an Android Phone (Sideloading)

You don't even need Google Play to give the game to friends or test it on your own phone:
1. Copy `app-release-signed.apk` to your phone via USB or Google Drive / WhatsApp.
2. Tap the `.apk` file on your phone.
3. Allow *"Install from unknown sources"*.
4. Tap **Install** → The game will appear on your home screen with its custom neon car icon and launch in full screen with responsive touch controls!

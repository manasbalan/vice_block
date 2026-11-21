import zipfile
import os

DIST_FILES = [
    "index.html",
    "three.min.js",
    "pricedown.otf",
    "rage.ttf",
    "gta_logo.png",
    "manifest.json",
    "sw.js",
    "icon-192.png",
    "icon-512.png",
    "screenshot1.png",
    "screenshot2.png",
    "menu_sound.mp3",
    "police_catch.mp3",
    "dino_scream.m4a",
    "README.md",
    "ANDROID_RELEASE_GUIDE.md",
    "generate_android_icons.py",
    "create_master_gta_logo.py"
]

def make_zip():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    zip_path = os.path.join(base_dir, "vice_blocks_android_release.zip")
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for f in DIST_FILES:
            full_path = os.path.join(base_dir, f)
            if os.path.exists(full_path):
                zipf.write(full_path, arcname=f)
                print(f"Added {f}")
            else:
                print(f"Warning: {f} not found")
                
        # Also bundle android_res directory
        res_dir = os.path.join(base_dir, "android_res")
        if os.path.exists(res_dir):
            for root, dirs, files in os.walk(res_dir):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, base_dir)
                    zipf.write(file_path, arcname=arcname)
            print("Added android_res/ with full Android launcher mipmaps & splash screens")
            
        # Also bundle .github workflow
        wf_path = os.path.join(base_dir, ".github", "workflows", "build-apk.yml")
        if os.path.exists(wf_path):
            zipf.write(wf_path, arcname=".github/workflows/build-apk.yml")
            print("Added .github/workflows/build-apk.yml")
                
    print(f"\nUpdated release bundle: {zip_path}")
    print(f"Size: {os.path.getsize(zip_path) / 1024:.1f} KB")

if __name__ == "__main__":
    make_zip()
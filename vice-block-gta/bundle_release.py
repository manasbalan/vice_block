import zipfile
import os

DIST_FILES = [
    "index.html",
    "three.min.js",
    "manifest.json",
    "sw.js",
    "icon-192.png",
    "icon-512.png",
    "screenshot1.png",
    "screenshot2.png",
    "README.md",
    "ANDROID_RELEASE_GUIDE.md"
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
                
    print(f"\nUpdated release bundle: {zip_path}")
    print(f"Size: {os.path.getsize(zip_path) / 1024:.1f} KB")

if __name__ == "__main__":
    make_zip()

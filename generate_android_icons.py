import os
import shutil
from PIL import Image, ImageDraw, ImageFilter

def generate_all_android_icons(base_dir):
    res_dir = os.path.join(base_dir, "android_res")
    if os.path.exists(res_dir):
        shutil.rmtree(res_dir)
    os.makedirs(res_dir, exist_ok=True)
    
    gta_logo_path = os.path.join(base_dir, "gta_logo.png")
    if not os.path.exists(gta_logo_path):
        import create_master_gta_logo
        create_master_gta_logo.create_master_gta_logo(base_dir)
        
    gta_logo = Image.open(gta_logo_path).convert("RGBA")
    
    # Base background color: Miami Vice dark purple/night #0F0A1C
    BG_COLOR = (15, 10, 28, 255)
    
    # 1. GENERATE ADAPTIVE FOREGROUND (ic_launcher_foreground.png)
    # The canvas is 108dp. Safe zone is center 72dp (66% of canvas).
    def create_foreground(sz):
        img = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        d = ImageDraw.Draw(img)
        
        safe_d = sz * 0.66
        cx, cy = sz // 2, sz // 2
        
        # 80s Retro Sunset in upper half of safe zone
        sr = int(safe_d * 0.36)
        sun_cy = int(cy - safe_d * 0.08)
        d.ellipse([cx - sr, sun_cy - sr, cx + sr, sun_cy + sr], fill=(255, 215, 0, 255))
        
        # Sun horizontal stripes
        st_h = max(2, sz // 48)
        for y in range(sun_cy, sun_cy + sr, st_h * 2):
            d.rectangle([cx - sr, y, cx + sr, y + st_h], fill=(0, 0, 0, 0))
            
        # Fit GTA logo nicely inside safe area (95% safe width)
        target_w = int(safe_d * 0.96)
        aspect = gta_logo.width / gta_logo.height
        target_h = int(target_w / aspect)
        scaled_logo = gta_logo.resize((target_w, target_h), Image.LANCZOS)
        
        px = (sz - target_w) // 2
        py = int(cy - target_h * 0.45)
        img.paste(scaled_logo, (px, py), scaled_logo)
        return img
        
    # 2. GENERATE LEGACY FULL SQUARE ICON (ic_launcher.png)
    def create_legacy_square(sz):
        icon = Image.new("RGBA", (sz, sz), BG_COLOR)
        d = ImageDraw.Draw(icon)
        
        # Neon magenta border
        bw = max(2, sz // 32)
        d.rounded_rectangle([bw, bw, sz - bw, sz - bw], radius=sz // 6, outline=(255, 0, 128, 255), width=bw)
        
        # Sunset
        sr = int(sz * 0.38)
        cx, cy = sz // 2, int(sz * 0.44)
        d.ellipse([cx - sr, cy - sr, cx + sr, cy + sr], fill=(255, 215, 0, 255))
        
        st_h = max(2, sz // 44)
        for y in range(cy, cy + sr, st_h * 2):
            d.rectangle([cx - sr, y, cx + sr, y + st_h], fill=BG_COLOR)
            
        target_w = int(sz * 0.92)
        aspect = gta_logo.width / gta_logo.height
        target_h = int(target_w / aspect)
        scaled_logo = gta_logo.resize((target_w, target_h), Image.LANCZOS)
        
        px = (sz - target_w) // 2
        py = int(sz * 0.52 - target_h * 0.5)
        icon.paste(scaled_logo, (px, py), scaled_logo)
        return icon

    # 3. GENERATE LEGACY FULL ROUND ICON (ic_launcher_round.png)
    def create_legacy_round(sz):
        sq = create_legacy_square(sz)
        mask = Image.new("L", (sz, sz), 0)
        d_mask = ImageDraw.Draw(mask)
        d_mask.ellipse([2, 2, sz - 2, sz - 2], fill=255)
        
        # Outer neon circle border
        d_sq = ImageDraw.Draw(sq)
        bw = max(2, sz // 32)
        d_sq.ellipse([bw, bw, sz - bw, sz - bw], outline=(0, 243, 255, 255), width=bw)
        
        round_icon = Image.new("RGBA", (sz, sz), (0, 0, 0, 0))
        round_icon.paste(sq, (0, 0), mask)
        return round_icon

    # Mipmap specifications: (density_name, launcher_size, foreground_size)
    mipmaps = [
        ("mipmap-mdpi", 48, 108),
        ("mipmap-hdpi", 72, 162),
        ("mipmap-xhdpi", 96, 216),
        ("mipmap-xxhdpi", 144, 324),
        ("mipmap-xxxhdpi", 192, 432),
    ]
    
    for folder_name, l_sz, fg_sz in mipmaps:
        folder_path = os.path.join(res_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)
        
        # Square launcher icon
        sq_img = create_legacy_square(l_sz)
        sq_img.save(os.path.join(folder_path, "ic_launcher.png"), "PNG")
        
        # Round launcher icon
        rd_img = create_legacy_round(l_sz)
        rd_img.save(os.path.join(folder_path, "ic_launcher_round.png"), "PNG")
        
        # Adaptive foreground
        fg_img = create_foreground(fg_sz)
        fg_img.save(os.path.join(folder_path, "ic_launcher_foreground.png"), "PNG")
        
        print(f"Generated {folder_name}: launcher {l_sz}x{l_sz}, foreground {fg_sz}x{fg_sz}")
        
    # 4. XML ADAPTIVE LAUNCHER DEFINITIONS (mipmap-anydpi-v26)
    v26_dir = os.path.join(res_dir, "mipmap-anydpi-v26")
    os.makedirs(v26_dir, exist_ok=True)
    
    adaptive_xml = """<?xml version="1.0" encoding="utf-8"?>
<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@drawable/ic_launcher_background" />
    <foreground android:drawable="@mipmap/ic_launcher_foreground" />
</adaptive-icon>
"""
    with open(os.path.join(v26_dir, "ic_launcher.xml"), "w", encoding="utf-8") as f:
        f.write(adaptive_xml)
    with open(os.path.join(v26_dir, "ic_launcher_round.xml"), "w", encoding="utf-8") as f:
        f.write(adaptive_xml)
        
    # 5. DRAWABLE ASSETS
    drawable_dir = os.path.join(res_dir, "drawable")
    os.makedirs(drawable_dir, exist_ok=True)
    
    # Background XML
    bg_xml = """<?xml version="1.0" encoding="utf-8"?>
<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp"
    android:height="108dp"
    android:viewportWidth="108"
    android:viewportHeight="108">
    <path
        android:fillColor="#0F0A1C"
        android:pathData="M0,0h108v108h-108z" />
</vector>
"""
    with open(os.path.join(drawable_dir, "ic_launcher_background.xml"), "w", encoding="utf-8") as f:
        f.write(bg_xml)
        
    # 6. SPLASH SCREENS (Landscape & Portrait)
    # Splash with centered GTA logo on dark background
    splash_land = Image.new("RGBA", (1920, 1080), BG_COLOR)
    target_w = 900
    aspect = gta_logo.width / gta_logo.height
    target_h = int(target_w / aspect)
    scaled_splash = gta_logo.resize((target_w, target_h), Image.LANCZOS)
    px = (1920 - target_w) // 2
    py = (1080 - target_h) // 2
    splash_land.paste(scaled_splash, (px, py), scaled_splash)
    splash_land.save(os.path.join(drawable_dir, "splash.png"), "PNG")
    
    # Splash densities
    splash_densities = [
        ("drawable-land-mdpi", 800, 480),
        ("drawable-land-hdpi", 1280, 720),
        ("drawable-land-xhdpi", 1600, 960),
        ("drawable-land-xxhdpi", 1920, 1080),
        ("drawable-land-xxxhdpi", 2560, 1440),
        ("drawable-port-mdpi", 480, 800),
        ("drawable-port-hdpi", 720, 1280),
        ("drawable-port-xhdpi", 960, 1600),
        ("drawable-port-xxhdpi", 1080, 1920),
        ("drawable-port-xxxhdpi", 1440, 2560),
    ]
    
    for s_folder, sw, sh in splash_densities:
        s_path = os.path.join(res_dir, s_folder)
        os.makedirs(s_path, exist_ok=True)
        s_img = Image.new("RGBA", (sw, sh), BG_COLOR)
        s_target_w = int(min(sw * 0.85, sh * 1.5))
        s_target_h = int(s_target_w / aspect)
        s_scaled = gta_logo.resize((s_target_w, s_target_h), Image.LANCZOS)
        spx = (sw - s_target_w) // 2
        spy = (sh - s_target_h) // 2
        s_img.paste(s_scaled, (spx, spy), s_scaled)
        s_img.save(os.path.join(s_path, "splash.png"), "PNG")

    # 7. VALUES / STRINGS.XML (Ensures app_name is "Vice Blocks")
    values_dir = os.path.join(res_dir, "values")
    os.makedirs(values_dir, exist_ok=True)
    strings_xml = """<?xml version='1.0' encoding='utf-8'?>
<resources>
    <string name="app_name">Vice Blocks</string>
    <string name="title_activity_main">Vice Blocks</string>
    <string name="package_name">com.viceblocks.game</string>
    <string name="custom_url_scheme">com.viceblocks.game</string>
</resources>
"""
    with open(os.path.join(values_dir, "strings.xml"), "w", encoding="utf-8") as f:
        f.write(strings_xml)
        
    print(f"Android resources successfully created in: {res_dir}")

if __name__ == "__main__":
    generate_all_android_icons(r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta")
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def create_master_gta_logo(out_dir):
    pricedown_path = os.path.join(out_dir, "pricedown.otf")
    rage_path = os.path.join(out_dir, "rage.ttf")
    
    # --- 1. FULL LOGO (gta_logo.png) ---
    W, H = 1000, 560
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    # Fonts
    font_small = ImageFont.truetype(pricedown_path, 110)
    font_large = ImageFont.truetype(pricedown_path, 175)
    font_script = ImageFont.truetype(rage_path, 195)
    
    # Grand Theft Auto text
    # GTA words: "grand", "theft", "auto"
    words = [
        ("grand", font_small, (50, 15)),
        ("theft", font_small, (50, 120)),
        ("auto", font_large, (50, 225))
    ]
    
    # Draw drop-shadow (offset 8, 8)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_shadow = ImageDraw.Draw(shadow_layer)
    for text, font, (x, y) in words:
        draw_shadow.text((x + 10, y + 10), text, font=font, fill=(0, 0, 0, 255), stroke_width=14, stroke_fill=(0, 0, 0, 255))
    
    # Main GTA text with thick black outline and crisp white interior
    gta_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw_gta = ImageDraw.Draw(gta_layer)
    for text, font, (x, y) in words:
        # Thick black outline
        draw_gta.text((x, y), text, font=font, fill=(0, 0, 0, 255), stroke_width=12, stroke_fill=(0, 0, 0, 255))
        # White fill
        draw_gta.text((x, y), text, font=font, fill=(255, 255, 255, 255))
        
    img = Image.alpha_composite(img, shadow_layer)
    img = Image.alpha_composite(img, gta_layer)
    
    # Script "Vice Blocks"
    # Create on a larger sub-canvas so we can apply rotation & glow smoothly
    SW, SH = 850, 320
    s_canvas = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    
    script_text = "Vice Blocks"
    sx, sy = 50, 60
    
    # 1. Cyan neon glow
    glow_img = Image.new("RGBA", (SW, SH), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow_img)
    for r in range(12, 0, -2):
        draw_glow.text((sx, sy), script_text, font=font_script, fill=(0, 243, 255, 120), stroke_width=r + 8, stroke_fill=(0, 243, 255, 120))
    glow_img = glow_img.filter(ImageFilter.GaussianBlur(radius=8))
    s_canvas = Image.alpha_composite(s_canvas, glow_img)
    
    # 2. Bold black & white outline
    draw_s = ImageDraw.Draw(s_canvas)
    # Black outline
    draw_s.text((sx + 5, sy + 5), script_text, font=font_script, fill=(0, 0, 0, 255), stroke_width=14, stroke_fill=(0, 0, 0, 255))
    # White highlight border
    draw_s.text((sx, sy), script_text, font=font_script, fill=(255, 255, 255, 255), stroke_width=8, stroke_fill=(255, 255, 255, 255))
    # Electric magenta / hot pink fill
    draw_s.text((sx, sy), script_text, font=font_script, fill=(255, 0, 128, 255), stroke_width=2, stroke_fill=(255, 0, 128, 255))
    
    # Tilt script by -8 degrees (classic Vice City angle)
    # In PIL rotate positive is counter-clockwise, so +7.5 degrees tilts the right side up
    s_rotated = s_canvas.rotate(7.5, resample=Image.BICUBIC, expand=True)
    
    # Paste rotated script across bottom right of GTA words
    img.paste(s_rotated, (190, 220), s_rotated)
    
    logo_path = os.path.join(out_dir, "gta_logo.png")
    img.save(logo_path, "PNG")
    print(f"Generated master GTA logo: {logo_path}")
    
    # --- 2. GENERATE SQUARE APP ICONS (icon-192.png & icon-512.png) ---
    for sz in [192, 512]:
        icon = Image.new("RGBA", (sz, sz), (15, 10, 28, 255))
        d_icon = ImageDraw.Draw(icon)
        
        # Rounded neon border
        bw = max(4, sz // 32)
        d_icon.rounded_rectangle([bw, bw, sz - bw, sz - bw], radius=sz // 6, outline=(255, 0, 128, 255), width=bw)
        
        # 80s Sunset circle in upper background
        sr = int(sz * 0.38)
        cx, cy = sz // 2, int(sz * 0.44)
        d_icon.ellipse([cx - sr, cy - sr, cx + sr, cy + sr], fill=(255, 215, 0, 255))
        
        # Sun horizontal stripes
        st_h = max(2, sz // 44)
        for y in range(cy, cy + sr, st_h * 2):
            d_icon.rectangle([cx - sr, y, cx + sr, y + st_h], fill=(15, 10, 28, 255))
            
        # Resize GTA logo to fit icon
        logo_aspect = img.width / img.height
        target_w = int(sz * 0.92)
        target_h = int(target_w / logo_aspect)
        scaled_logo = img.resize((target_w, target_h), Image.LANCZOS)
        
        # Paste centered in lower half
        px = (sz - target_w) // 2
        py = int(sz * 0.52 - target_h * 0.5)
        icon.paste(scaled_logo, (px, py), scaled_logo)
        
        icon_path = os.path.join(out_dir, f"icon-{sz}.png")
        icon.save(icon_path, "PNG")
        print(f"Generated GTA App Icon: {icon_path} ({sz}x{sz})")

if __name__ == "__main__":
    create_master_gta_logo(r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta")

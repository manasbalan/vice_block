import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def make_gta_vice_blocks_logo(out_path, width=800, height=450):
    # Transparent canvas
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    
    pricedown_path = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\pricedown.otf"
    rage_path = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\rage.ttf"
    
    font_gta_small = ImageFont.truetype(pricedown_path, int(height * 0.18))
    font_gta_large = ImageFont.truetype(pricedown_path, int(height * 0.28))
    font_vice = ImageFont.truetype(rage_path, int(height * 0.28))
    
    # 1. Draw "grand theft auto" block (left-aligned)
    # Layer for GTA text
    gta_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw_gta = ImageDraw.Draw(gta_layer)
    
    lines = [
        ("grand", font_gta_small, (50, int(height * 0.08))),
        ("theft", font_gta_small, (50, int(height * 0.24))),
        ("auto", font_gta_large, (50, int(height * 0.40)))
    ]
    
    # Draw drop shadow & thick black outline
    stroke_w = max(4, int(height * 0.015))
    shadow_offset = (int(height * 0.02), int(height * 0.02))
    
    # Shadows
    for text, font, pos in lines:
        draw_gta.text((pos[0] + shadow_offset[0], pos[1] + shadow_offset[1]), text, font=font, fill=(0, 0, 0, 240), stroke_width=stroke_w + 2, stroke_fill=(0, 0, 0, 240))
        
    # Outlines & white text
    for text, font, pos in lines:
        draw_gta.text(pos, text, font=font, fill=(255, 255, 255, 255), stroke_width=stroke_w, stroke_fill=(10, 10, 10, 255))
        
    img = Image.alpha_composite(img, gta_layer)
    
    # 2. Draw "Vice Blocks" in the iconic slanted hot-pink script with cyan glow
    # Render script onto rotated layer
    script_layer = Image.new("RGBA", (int(width * 1.2), int(height * 0.6)), (0, 0, 0, 0))
    draw_script = ImageDraw.Draw(script_layer)
    
    script_text = "Vice Blocks"
    sx = int(width * 0.08)
    sy = int(height * 0.12)
    
    # Cyan outer glow
    glow_layer = Image.new("RGBA", (int(width * 1.2), int(height * 0.6)), (0, 0, 0, 0))
    draw_glow = ImageDraw.Draw(glow_layer)
    for ox in range(-6, 7, 2):
        for oy in range(-6, 7, 2):
            draw_glow.text((sx + ox, sy + oy), script_text, font=font_vice, fill=(0, 243, 255, 180), stroke_width=6, stroke_fill=(0, 243, 255, 180))
    glow_layer = glow_layer.filter(ImageFilter.GaussianBlur(radius=6))
    script_layer = Image.alpha_composite(script_layer, glow_layer)
    
    # White outline for script
    draw_script.text((sx, sy), script_text, font=font_vice, fill=(255, 255, 255, 255), stroke_width=7, stroke_fill=(255, 255, 255, 255))
    # Hot-pink fill
    draw_script.text((sx, sy), script_text, font=font_vice, fill=(255, 0, 128, 255), stroke_width=2, stroke_fill=(200, 0, 100, 255))
    
    # Rotate script by -8 degrees (classic Vice City tilt)
    rotated_script = script_layer.rotate(8, resample=Image.BICUBIC, expand=True)
    
    # Position script overlaying the bottom right of the GTA block
    script_paste_x = int(width * 0.22)
    script_paste_y = int(height * 0.42)
    img.paste(rotated_script, (script_paste_x, script_paste_y), rotated_script)
    
    img.save(out_path, "PNG")
    print(f"Generated GTA Vice Blocks Logo: {out_path} ({width}x{height})")

if __name__ == "__main__":
    out_dir = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta"
    make_gta_vice_blocks_logo(os.path.join(out_dir, "gta_logo.png"), 900, 520)

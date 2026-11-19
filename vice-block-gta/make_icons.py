from PIL import Image, ImageDraw, ImageFont
import os

def create_icon(size, path):
    # Create image with dark purple gradient/solid
    img = Image.new("RGBA", (size, size), (24, 16, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Outer neon border
    border_w = max(4, size // 32)
    draw.rounded_rectangle([border_w, border_w, size - border_w, size - border_w], radius=size // 6, outline=(255, 42, 133, 255), width=border_w)
    
    # Sunset circle in center
    sun_r = size // 3
    center = (size // 2, size // 2)
    draw.ellipse([center[0] - sun_r, center[1] - sun_r, center[0] + sun_r, center[1] + sun_r], fill=(255, 220, 0, 255))
    
    # Sun horizontal stripes (80s synthwave style)
    stripe_h = max(2, size // 40)
    for y in range(center[1], center[1] + sun_r, stripe_h * 2):
        draw.rectangle([center[0] - sun_r, y, center[0] + sun_r, y + stripe_h], fill=(24, 16, 42, 255))
        
    # Blocky sports car silhouette in foreground
    car_y = size * 0.65
    car_w = size * 0.7
    car_h = size * 0.18
    car_x = (size - car_w) / 2
    
    # Car body (Cyan blocky)
    draw.rectangle([car_x, car_y, car_x + car_w, car_y + car_h], fill=(0, 243, 255, 255))
    # Car roof
    draw.rectangle([car_x + car_w * 0.25, car_y - car_h * 0.7, car_x + car_w * 0.7, car_y], fill=(0, 243, 255, 255))
    # Windows
    draw.rectangle([car_x + car_w * 0.3, car_y - car_h * 0.55, car_x + car_w * 0.65, car_y], fill=(17, 17, 25, 255))
    # Headlight
    draw.rectangle([car_x + car_w - 6, car_y + 4, car_x + car_w, car_y + car_h * 0.5], fill=(255, 255, 255, 255))
    # Wheels
    wheel_r = car_h * 0.45
    draw.ellipse([car_x + car_w * 0.15 - wheel_r, car_y + car_h - wheel_r, car_x + car_w * 0.15 + wheel_r, car_y + car_h + wheel_r], fill=(10, 10, 15, 255))
    draw.ellipse([car_x + car_w * 0.85 - wheel_r, car_y + car_h - wheel_r, car_x + car_w * 0.85 + wheel_r, car_y + car_h + wheel_r], fill=(10, 10, 15, 255))
    
    img.save(path)
    print(f"Generated icon: {path} ({size}x{size})")

out_dir = r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta"
create_icon(192, os.path.join(out_dir, "icon-192.png"))
create_icon(512, os.path.join(out_dir, "icon-512.png"))

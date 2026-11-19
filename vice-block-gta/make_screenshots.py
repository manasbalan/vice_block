from PIL import Image, ImageDraw

def make_screenshot(path, title):
    img = Image.new("RGBA", (1280, 720), (24, 16, 42, 255))
    draw = ImageDraw.Draw(img)
    
    # Sunset gradient / ground
    draw.rectangle([0, 450, 1280, 720], fill=(34, 34, 40, 255)) # Road
    draw.ellipse([450, 100, 830, 480], fill=(255, 120, 180, 255)) # Sunset sun
    
    # Text title
    draw.text((640, 360), title, fill=(0, 243, 255, 255), anchor="mm")
    
    img.save(path)
    print(f"Created {path}")

make_screenshot(r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\screenshot1.png", "VICE BLOCKS: HEIST MISSION")
make_screenshot(r"C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\screenshot2.png", "POLICE PURSUIT 60FPS")

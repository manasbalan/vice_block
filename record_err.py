file_path = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    c = f.read()

old_catch = "console.error('[ViceBlocks] animate() catch:', e);"
new_catch = "window._lastAnimErr = e.message + ' | ' + (e.stack || ''); console.error('[ViceBlocks] animate() catch:', e);"

if old_catch in c:
    c = c.replace(old_catch, new_catch)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(c)
    print("Replaced catch successfully.")
else:
    print("old_catch not found.")

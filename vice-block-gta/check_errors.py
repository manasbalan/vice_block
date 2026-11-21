with open(r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Check if there is any error being thrown on load
# Let's inspect console.log/error in index.html
import re
print("Occurrences of console.error in index.html:")
for m in re.finditer(r'console\.error\([^)]+\)', text):
    print(m.group(0))

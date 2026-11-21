with open(r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('BUG in cheat buttons:', 'data-cheat="BUG"' in text)
print('TREX in cheat buttons:', 'data-cheat="TREX"' in text)
print('TREX in executeCheatCode:', "code === 'TREX'" in text)
print('BUG in executeCheatCode:', "code === 'BUG'" in text)
print('triggerTRexStampede exists:', 'function triggerTRexStampede()' in text)
print('triggerDeveloperBugGlitch exists:', 'function triggerDeveloperBugGlitch()' in text)

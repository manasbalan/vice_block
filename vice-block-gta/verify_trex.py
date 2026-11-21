index_file = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(index_file, 'r', encoding='utf-8') as f:
    text = f.read()

print('class TRexDinosaur:', 'class TRexDinosaur' in text)
print('activeTRex:', 'activeTRex' in text)
print('triggerTRexStampede:', 'triggerTRexStampede' in text)
print('dinoScreamAudio:', 'dinoScreamAudio' in text)
print('TREX cheat button:', 'data-cheat="TREX"' in text)
print('TREX cheat code:', "code === 'TREX'" in text)

start_script = text.find('<script>')
end_script = text.rfind('</script>')
js_code = text[start_script+8:end_script]

print('JS code length:', len(js_code))
open_braces = js_code.count('{')
close_braces = js_code.count('}')
open_parens = js_code.count('(')
close_parens = js_code.count(')')
open_brackets = js_code.count('[')
close_brackets = js_code.count(']')

print(f'Braces: {open_braces} vs {close_braces}')
print(f'Parens: {open_parens} vs {close_parens}')
print(f'Brackets: {open_brackets} vs {close_brackets}')

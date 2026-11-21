file_path = r'C:\Users\rames\.gemini\antigravity\scratch\vice-block-gta\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

quotes_to_check = [
    'Police vandiyum kondu evidekk... Patunna paniki poya pore!',
    'Adu kond ninak enda karyam',
    'Valla avashyam undayno task cheyda pore ',
    'Ammo teernada ',
    'Ammo teernu ',
    'Haaa aduta gun eduku ',
    'Adum teernu ',
    'Allelum grenede ninak ullad alla ',
    'Ada gommale ',
    'Aaah my bad...! Sthalam mari poi!',
    'DEVELOPER FAILED • YOU DEFEATED THE EXAM!',
    ' Excellent! Ennalum negative engane kiiti ',
    'Wrong one',
    'Picha karane engilum verude vidu',
    'Adum mukki',
    'Valla panikum poda daridravasi',
    'Enthina bro ithrayum aathirthi',
    'Pocketil onnum illa thappan nikkanda',
    'maan what did he even do to you'
]

all_passed = True
for q in quotes_to_check:
    found = q in text
    if not found:
        all_passed = False
    print(f'[{ "OK" if found else "FAIL" }] {q}')

print('--- Red Box Check ---')
has_red_box = 'animate ERROR frame' in text
print(f'Red error box present: {has_red_box} (Must be False)')
if has_red_box:
    all_passed = False

print('--- Tank Logic Check ---')
has_tank = 'isTank' in text and 'spawnRhinoTankAtPlayer' in text and 'fireTankCannon' in text
print(f'Tank fully present: {has_tank} (Must be True)')
if not has_tank:
    all_passed = False

print('Overall check passed:', all_passed)

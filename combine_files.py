import os

directory = r"C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\common\religion\religions"

files_to_combine = []

skip = [
    'family',
    'doctrine',
    'pagan_roots',
    '#',
    'traits',
    'virtues',
    'sins',
    'custom_faith_icons',
    'custom_faith_1',
    '}',
    'localization',
    'HighGod',
    'Creator',
    'HealthGod',
    'FertilityGod',
    'WealthGod',
    'HouseholdGod',
    'FateGod',
    'KnowledgeGod',
    'WarGod',
    'Trickster',
    'Night',
    'Water',
    'Pantheon',
    'Good',
    'Devil',
    'Evil',
    'House',
    'Religious',
    'Devotee',
    'Priest',
    'Alt',
    'Bishop',
    'GHW',
    'Divine',
    'Positive',
    'Negative',
    'Death',
    'Witch',
    'faiths',
    'color',
    'icon',
    'reformed',
    'holy',
    'graphical',
    'compassopmate',
    'calm',
    'humble',
    'lustful',
    'greedy',
    'arrogant'
    ]

skip_contains = [
    'high_god',
    'good_god',
    'devil',
    'evil_god'
    ]

def skip_this_line(line):
    for item in skip:
        if line.startswith(item):
            return True
    for item in skip_contains:
        if item in line:
            return True
    if line.isspace():
        return True
    return False

for filename in os.listdir(directory):
    if filename.endswith('.txt'):
        files_to_combine.append(directory + '\\' + filename)
        
outfile = open("combined.txt", "w", encoding='utf8')
for file in files_to_combine:
    infile = open(file, "r", encoding='utf8')
    for line in infile:
        content = line
        content = content.replace('\t', '')

        if skip_this_line(content):
            continue
        
        outfile.write(content)

import os

inputfile = "icons_to_create.txt"
outfile_icons = "icons/icons_$.txt"
outfile_documentation = "icon_documentation.txt"


# Input file:
# Comma separated key,value0,value1 lines

# Key = icon name (e.g. {{icon|NAME}})
# value0 = alt name
# value1 = file name (without file extensions, .png is implied always)

class icon_datum:
    def __init__(self, name, alt, image):
        self.name = name
        self.alt = alt
        self.image = image

icons = []


infile = open(inputfile, 'r', encoding='utf8')
line_counter = 0
for line in infile:
    line_counter = line_counter + 1
    if line.startswith('#'):
        continue
    formatted = line
    formatted = formatted.rstrip()
    data = formatted.split(',')
    if len(data) != 3:
        print("Unable to parse line " + str(line_counter) + " in file " + inputfile)
        continue

    name = data[0]
    name = name.lower()

    alt = data[1]
    if len(alt) == 0:
        alt = name
        alt = alt.title()
        print("Auto-generated alternative from name " + name + ": " + alt + ".")
    alt_temp = alt
    # Why does capitalize() also make other letters lowercase, what the actual hell.
    alt_temp = alt_temp[0].upper() + alt_temp[1:]
    alt = alt_temp
    
    image = data[2]
    image = image.replace('_', ' ')
    image = image.capitalize()
    
    d = icon_datum(name, alt, image)
    icons.append(d)

icons.sort(key=lambda x: x.name)

# Create icon stuff to drop in.
# Do this alphabetically.

# Key = alphabetical character
# Value = icons for that file
icon_files = {}

for icon in icons:
    first_char = icon.name[0]
    if first_char not in icon_files.keys():
        icon_files[first_char] = []
    icon_files[first_char].append(icon)
    
for character in icon_files.keys():
    outputfile = outfile_icons.replace('$', character)
    outfile = open(outputfile, 'w', encoding='utf8')

    for icon in icon_files[character]:
        outfile.write("| " + icon.name + " = [[File:" + icon.image + ".png|alt={{#if:{{{alt|}}}|" + icon.alt + "}}|link=|{{{w|24px}}}]]")
        outfile.write('\n')
    outfile.close()
    print("Completed printing icon file for char: " + character)
    
print("Completed printing all icon files.")

print("Starting documentation...")

doc_file = open(outfile_documentation, 'w', encoding='utf8')
doc_file.write('{{box wrapper}}\n'
               '{|class="wikitable" style="width:250px; float:left; margin-right: 10px;"\n'
               '! colspan=2 | AUTO-GENERATED\n')

counter = 0
for icon in icons:
    doc_file.write('|-\n')
    doc_file.write('| {} || '.format(icon.name))
    if counter == 0:
        doc_file.write('width=30px | ')
    doc_file.write('{{icon|' + icon.name + '}}')
    doc_file.write('\n')
    counter = counter + 1
print("Printed " + str(counter) + " icon(s).")

doc_file.write('|}\n')
doc_file.close()
print("Completed printing documentation. :)")
    


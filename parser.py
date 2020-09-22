import os, glob
import pyradox

titles = {} # nested dict empires:kingdoms:dutchies:counties:baronies:barony number
dev_867 = {}
dev_1066 = {}
special = {}
names = {}
colors = {}
capitals = {}

# Traits
# Also detect traits with non-matching ids (for console)
traits = {}

# Religions/holy orders
# Religions: holy_orders
# Faiths: holy_orders
religions = {}
faiths = {}

# Decisions
# Detect decisions with non-matching internal ids.
decisions = {}

# Parse localization file
def parse_names(filename, clear=False):
    root =  'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\localization\english\\'
    if clear:
        names.clear()
    files = []
    if filename == 'all':
        for x in glob.glob(os.path.join(root, '*.yml')):
            files.append(x)
    else:
        files.append(root + filename + ".yml")
    for file in files:
        name_file = open(
        file,
        "r", encoding='utf8')
    
        for line in name_file:
            words = line.split()
            if len(words) > 1:
                key = words[0][:-2]
                value = " ".join(words[1:]).strip('"')
                names[key] = value

def parse_dev():
    folder_path = 'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\history\\titles'
    for filename in glob.glob(os.path.join(folder_path, '*.txt')):
        # print(filename)
        dev = pyradox.txt.parse_file(filename, game="Stellaris")
        for key in list(dev.keys()):
            # print(key)
            if pyradox.Time('20.1.1') in list(dev[key].keys()):
                if "change_development_level" in list(dev[key][pyradox.Time('20.1.1')].keys()):
                    dev_867[key] = dev[key][pyradox.Time('20.1.1')]["change_development_level"]
                    dev_1066[key] = dev[key][pyradox.Time('20.1.1')]["change_development_level"]
            if pyradox.Time('867.1.1') in list(dev[key].keys()):
                if "change_development_level" in list(dev[key][pyradox.Time('867.1.1')].keys()):
                    dev_867[key] = dev[key][pyradox.Time('867.1.1')]["change_development_level"]
                    dev_1066[key] = dev[key][pyradox.Time('867.1.1')]["change_development_level"]
            if pyradox.Time('1000.1.1') in list(dev[key].keys()):
                if "change_development_level" in list(dev[key][pyradox.Time('1000.1.1')].keys()):
                    dev_1066[key] = dev[key][pyradox.Time('1000.1.1')]["change_development_level"]
            if pyradox.Time('1066.1.1') in list(dev[key].keys()):
                if "change_development_level" in list(dev[key][pyradox.Time('1066.1.1')].keys()):
                    dev_1066[key] = dev[key][pyradox.Time('1066.1.1')]["change_development_level"]

def parse_special():
    folder_path = 'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\history\provinces'
    for filename in glob.glob(os.path.join(folder_path, '*.txt')):
        # print(filename)
        provinces = pyradox.txt.parse_file(filename, game="Stellaris")
        for key in list(provinces.keys()):
            special[key] = 0
            # print(key)
            if type(provinces[key]) == pyradox.Tree:
                if "special_building" in list(provinces[key].keys()):
                    special[key] = 1
                if "duchy_capital_building" in list(provinces[key].keys()):
                    special[key] = 2
                for subkey in provinces[key].keys():
                    if type(provinces[key][subkey]) == pyradox.Tree:
                        if "special_building" in list(provinces[key][subkey].keys()):
                            special[key] = special[key] + 1
                        elif "special_building_slot" in list(provinces[key][subkey].keys()):
                            special[key] = special[key] + 1
                        if "duchy_capital_building" in list(provinces[key][subkey].keys()):
                            special[key] = special[key] + 1

def parse_titles():
    titles_tree = pyradox.txt.parse_file(
        'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\common\landed_titles\\00_landed_titles.txt',
        game="Stellaris")

    for key_e in list(titles_tree.keys()):
        if key_e[:2] == "e_":
            titles[key_e] = {}
            color = list(titles_tree[key_e].find_all('color'))
            if type(color[0]) == pyradox.datatype.Color:
                colors[key_e] = list(color[0].to_rgb())
            else:
                colors[key_e] = color
            capitals[key_e] = titles_tree[key_e]["capital"]

            for key_k in list(titles_tree[key_e].keys()):
                if key_k[:2] == "k_":
                    titles[key_e][key_k] = {}
                    color = list(titles_tree[key_e][key_k].find_all('color'))
                    if type(color[0]) == pyradox.datatype.Color:
                        colors[key_k] = list(color[0].to_rgb())
                    else:
                        colors[key_k] = color
                    capitals[key_k] = titles_tree[key_e][key_k]["capital"]

                    for key_d in list(titles_tree[key_e][key_k].keys()):
                        if key_d[:2] == "d_":
                            titles[key_e][key_k][key_d] = {}
                            color = list(titles_tree[key_e][key_k][key_d].find_all('color'))
                            if type(color[0]) == pyradox.datatype.Color:
                                colors[key_d] = list(color[0].to_rgb())
                            else:
                                colors[key_d] = color

                            capitals[key_d] = titles_tree[key_e][key_k][key_d]["capital"]

                            for key_c in list(titles_tree[key_e][key_k][key_d].keys()):
                                if key_c[:2] == "c_":
                                    titles[key_e][key_k][key_d][key_c] = {}
                                    colors[key_c] = list(titles_tree[key_e][key_k][key_d][key_c].find_all('color'))

                                    for key_b in list(titles_tree[key_e][key_k][key_d][key_c].keys()):
                                        if key_b[:2] == "b_":
                                            titles[key_e][key_k][key_d][key_c][key_b] = \
                                                titles_tree[key_e][key_k][key_d][key_c][key_b]["province"]

def parse_religion(filename):
    religions_tree = pyradox.txt.parse_file(
        filename,
        game="Stellaris")

    print('Parsing religion ' + filename)

    # Religions
    for key_r in list(religions_tree.keys()):
        religion[key_r] = {}
        holy_order = list(religions_tree[key_r].find_all('holy_order_names'))
        print(holy_order)

def parse_holy_orders():
    religion_folder = r'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\common\religion\religions'

    print(os.listdir(religion_folder))

    for filename in os.listdir(religion_folder):
        print('Found file: ' + filename)
        if filename.endswith('.txt'):
            parse_religion(filename)
    

def print_baronies():
    outfile = open("baronies.txt", "w", encoding='utf8')
    outfile.write('{| class="wikitable sortable mw-collapsible" style="text-align: left;"\n'
                  '|+ Counties\n'
                  '|-\n'
                  '! rowspan="2" | Barony\n'
                  '! rowspan="2" | [[Counties|County]]\n'
                  '! rowspan="2" | Holding slots\n'
                  '! rowspan="2" | [[Barony#Buildings|Special Buildings/Slots]]\n'
                  '! rowspan="2" | ID\n'
                  '|-\n')
    for empire in titles.keys():
        for kingdom in titles[empite].keys():
            for duchy in titles[empire][kingdom].keys():
                for county in titles[empire][kingdom][duchy].keys():
                    for barony in titles[empire][kingdom][duchy][county].keys():
                        
                        outfile.write('|-\n!style = "background-color:rgb({},{},{})" | {}\n | {} || {} || '
                                      '{} || align="right"| {} || align="right"| {} || align="right"| {} || '
                                  'align="right"| {} || {}\n'.format(
                        colors[county][0], colors[county][1], colors[county][2], names[barony], names[county],
                        holding_slots[barony], names[empire], baronies, county_dev_867, county_dev_1066, special_buildings,
                        county))
                        
                        


def print_counties():
    outfile = open("counties.txt", "w", encoding='utf8')
    outfile.write('{| class="wikitable sortable" style="text-align: left;"\n'
                  '|-\n'
                  '! colspan="2" rowspan="2" | County\n'
                  '! rowspan="2" | Duchy\n'
                  '! rowspan="2" | Kingdom\n'
                  '! rowspan="2" | Empire\n'
                  '! rowspan="2" | Baronies\n'
                  '! rowspan="2" | Special buildings/slots\n
                  '! colspan="2" | Development\n'
                  '! colspan="2" | Culture\n'
                  '! colspan="2" | Religion\n'
                  '! rowspan="2" | Title ID\n'
                  '|-\n'
                  '! 867\n'
                  '! 1066\n'
                  '! 867\n'
                  '! 1066\n'
                  '! 867\n'
                  '! 1066\n')
    for empire in titles.keys():
        for kingdom in titles[empire].keys():
            for dutchy in titles[empire][kingdom].keys():
                for county in titles[empire][kingdom][dutchy].keys():
                    county_dev_867 = 0
                    if empire in dev_867:
                        county_dev_867 = dev_867[empire]
                    if kingdom in dev_867:
                        county_dev_867 = dev_867[kingdom]
                    if dutchy in dev_867:
                        county_dev_867 = dev_867[dutchy]
                    if county in dev_867:
                        county_dev_867 = dev_867[county]

                    county_dev_1066 = 0
                    if empire in dev_1066:
                        county_dev_1066 = dev_1066[empire]
                    if kingdom in dev_1066:
                        county_dev_1066 = dev_1066[kingdom]
                    if dutchy in dev_1066:
                        county_dev_1066 = dev_1066[dutchy]
                    if county in dev_1066:
                        county_dev_1066 = dev_1066[county]

                    baronies = 0
                    special_buildings = 0
                    for barony in titles[empire][kingdom][dutchy][county].keys():
                        baronies = baronies + 1
                        barony_id = int(titles[empire][kingdom][dutchy][county][barony])
                        if(barony_id in list(special.keys()) and special[barony_id] > 0):
                            special_buildings = special_buildings + special[barony_id]

                    lines = [
                        '|- id="{}"'.format(names[county])
                        '{{title with color|{}|{}|{}|{}}}'.format(names[county], colors[county][0], colors[county][1], colors[county][2])
                        '| {}'.format(names[dutchy])
                        '| {}'.format(names[kingdom])
                        '| {}'.format(names[empire])
                        '| {}'.format(str(baronies))
                        
                        ]
                    for line in lines:
                        outfile.write(line + "\n")

                    outfile.write('|-\n')

                    outfile.write('|-\n!style = "background-color:rgb({},{},{})" | {}\n | {} || {} || '
                                      '{} || align="right"| {} || align="right"| {} || align="right"| {} || '
                                  'align="right"| {} || {}\n'.format(
                        colors[county][0], colors[county][1], colors[county][2], names[county], names[dutchy],
                        names[kingdom], names[empire], baronies, county_dev_867, county_dev_1066, special_buildings,
                        county))
    outfile.write("|}")

def print_dutchies():
    outfile = open("dutchies.txt", "w", encoding='utf8')
    outfile.write('{| class="wikitable sortable mw-collapsible" style="text-align: left;"\n'
                  '|+ De Jure Duchies\n'
                  '|-\n'
                  '! rowspan="2" | Duchy\n'
                  '! rowspan="2" | [[Kingdoms|Kingdom]]\n'
                  '! rowspan="2" | [[Empires|Empire]]\n'
                  '! rowspan="2" | [[Provinces|Counties]]\n'
                  '! rowspan="2" | Baronies\n'
                  '! rowspan="2" | Largest County\n'
                  '! colspan="4" | Developments\n'
                  '! rowspan="2" | Special Buildings\n'
                  '! rowspan="2" | ID\n'
                  '! rowspan="2" | Capital\n'
                  '|-\n'
                  '! Total Dev 867\n'
                  '! Max Dev 867\n'
                  '! Total Dev 1066\n'
                  '! Max Dev 1066\n')
    for empire in titles.keys():
        for kingdom in titles[empire].keys():
            for dutchy in titles[empire][kingdom].keys():
                counties = 0
                baronies = 0
                largest_county = 0
                total_dev_867 = 0
                highest_dev_867 = 0
                total_dev_1066 = 0
                highest_dev_1066 = 0
                special_buildings = 0
                for county in titles[empire][kingdom][dutchy].keys():
                    county_dev_867 = 0
                    if empire in dev_867:
                        county_dev_867 = dev_867[empire]
                    if kingdom in dev_867:
                        county_dev_867 = dev_867[kingdom]
                    if dutchy in dev_867:
                        county_dev_867 = dev_867[dutchy]
                    if county in dev_867:
                        county_dev_867 = dev_867[county]

                    total_dev_867 = total_dev_867 + county_dev_867
                    if county_dev_867 > highest_dev_867:
                        highest_dev_867 = county_dev_867

                    county_dev_1066 = 0
                    if empire in dev_1066:
                        county_dev_1066 = dev_1066[empire]
                    if kingdom in dev_1066:
                        county_dev_1066 = dev_1066[kingdom]
                    if dutchy in dev_1066:
                        county_dev_1066 = dev_1066[dutchy]
                    if county in dev_1066:
                        county_dev_1066 = dev_1066[county]

                    total_dev_1066 = total_dev_1066 + county_dev_1066
                    if county_dev_1066 > highest_dev_1066:
                        highest_dev_1066 = county_dev_1066

                    counties = counties + 1
                    local_baronies = 0
                    for barony in titles[empire][kingdom][dutchy][county].keys():
                        local_baronies = local_baronies + 1
                        barony_id = int(titles[empire][kingdom][dutchy][county][barony])
                        if(barony_id in list(special.keys()) and special[barony_id] > 0):
                            special_buildings = special_buildings + special[barony_id]
                    baronies = baronies + local_baronies

                    if local_baronies > largest_county:
                        largest_county = local_baronies

                capital = "None"
                if capitals[dutchy] in names.keys():
                    capital = names[capitals[dutchy]]
                outfile.write('|-\n!style = "background-color:rgb({},{},{})" | {}\n | {} || {} || '
                              'align="right"| {} || align="right"| {} ||  align="right"| {} ||align="right"| {} || '
                              'align="right"| {} || align="right"| {} || align="right"| {} || align="right"| '
                              '{} || {} || {}\n'.format(colors[dutchy][0], colors[dutchy][1], colors[dutchy][2],
                                                        names[dutchy], names[kingdom], names[empire], counties,
                                                        baronies, largest_county, total_dev_867, highest_dev_867,
                                                        total_dev_1066, highest_dev_1066, special_buildings, dutchy,
                                                        capital))
    outfile.write("|}")

def print_kingdoms():
    outfile = open("kingdom.txt", "w", encoding='utf8')
    outfile.write('{| class="wikitable sortable mw-collapsible" style="text-align: left;"\n'
                  '|+ De Jure Kingdoms\n'
                  '|-\n'
                  '! rowspan="2" | Kingdom\n'
                  '! rowspan="2" | [[duchies|Dejure duchies]]\n'
                  '! rowspan="2" | [[Empires|Empire]]\n'
                  '! colspan="2" | [[County|Counties]]\n'
                  '! rowspan="2" | ID\n'
                  '! rowspan="2" | Capital\n')
    for empire in titles.keys():
        for kingdom in titles[empire].keys():
            dejure_dutchies = []
            counties = 0
            for dutchy in titles[empire][kingdom].keys():
                dejure_dutchies.append(names[dutchy])
                for county in titles[empire][kingdom][dutchy].keys():
                    counties = counties + 1

            capital = "None"
            if capitals[kingdom] in names.keys():
                capital = names[capitals[kingdom]]

            outfile.write('|-\n!style = "background-color:rgb({},{},{})" | {}\n | {} || {} || '
                              'align="right"| {} || {} || {}\n'.format(
                colors[kingdom][0], colors[kingdom][1], colors[kingdom][2], names[kingdom], ', '.join(dejure_dutchies),
                names[empire], counties, kingdom, capital))
    outfile.write("|}")

def print_empires():
    outfile = open("empires.txt", "w", encoding='utf8')
    outfile.write('{| class="wikitable sortable" style="text-align: left;"\n'
                  '|-\n'
                  '! colspan=2 | [[Empire]]\n'
                  '! [[Capital]]\n'
                  '! [[Kingdoms|De jure kingdoms]]\n'
                  '! Special requirements\n'
                  '! AI additional requirements\n'
                  '! ID\n'
                  '! Alternate names\n')

    empires = {}
    for empire in titles.keys():
        empires[empire] = names[empire]
    empires_in_order = sorted(empires.items(), key=lambda x: x[1])

    for empire in empires_in_order:
        dejure_kingdoms = []
        dutchies = 0
        counties = 0
        for kingdom in titles[empire[0]].keys():
            dejure_kingdoms.append(names[kingdom])

        # Get this list alphabetical
        dejure_kingdoms.sort()
        
        capital = "None"
        if capitals[empire[0]] in names.keys():
            capital = names[capitals[empire[0]]]
        outfile.write('|-\n| rowspan=1 style="width: 2px; background-color: rgb({}, {}, {});" |\n| rowspan=1 style="text-align: left;" scope="row" | {}\n| {}\n| {}\n| {}\n| {}\n| {}\n| {}\n'.format(
            colors[empire[0]][0], colors[empire[0]][1], colors[empire[0]][2], names[empire[0]], capital, ", ".join(dejure_kingdoms), "", "", empire[0], ""
            ))
            
        #colors[empire[0]][0], colors[empire[0]][1], colors[empire[0]][2]
        # <span style="background-color:rgb({}, {}, {})">{}</span>
                  
    outfile.write("|}")
    print("Completed writing empires to file.")

def print_decisions():
    outfile = open("decision.txt", "w", encoding='utf8')
    outfile.write('{| class="mildtable"\n'
                  '! Decision\n'
                  '! Internal name\n')

    new_names = {}
    excluded = [
        'recently_took_tribal_challenge_ruler_decision',
        'action_take_decision'
        ]

    # Edit names for readability (localization, scopes)
    for decision in names.keys():
        new_value = names[decision]
        new_value = new_value.replace('[ROOT.Char.GetLiege.GetTitleAsNameNoTooltip|U]', 'Ruler')
        new_value = new_value.replace("[ROOT.Char.Custom('DogStoryName')]", 'Dog')
        new_value = new_value.replace("[ROOT.Char.Custom('CatStoryName')]", 'Cat')
        new_value = new_value.replace('$c_roma$', 'Roma')
        new_value = new_value.replace("[ROOT.Char.Custom2('RelationToMe', ROOT.Var('ancestor_to_bury').Char)|U]", "Ancestor")
        new_value = new_value.replace("[ROOT.Char.GetLiege.GetGovernment.GetNameNoTooltip]", 'Feudal / Clan')
        new_value = new_value.replace("[ROOT.Char.Custom('GetTribalReformGovernment')|U]", 'Feudal / Clan')
        new_value = new_value.replace('[ROOT.Char.GetFaith.GetAdjectiveNoTooltip]', "Faith")
        new_value = new_value.replace('[ROOT.Char.GetFaith.GetNameNoTooltip]', "Faith")
        new_value = new_value.replace("$magyar_pagan$", "Táltoism")
        new_value = new_value.replace('[ROOT.Char.GetFaith.HighGodName]', 'High God')
        new_value = new_value.replace('$knight_culture_player_plural_no_tooltip$', 'Knights')
        new_value = new_value.replace('$bosnian_church$', 'Krstjani')

        if decision not in excluded:
            if "game_concept" not in decision:
                new_names[decision] = new_value

    for decision in new_names.keys():
        if decision.endswith('decision'):
            decision_id = decision[:-9]
            
            decision_name = new_names[decision]
            decision_name = decision_name.replace(' ', '_')
            decision_name = decision_name.lower()
            # Mark disimilar decision names
            if decision_name != decision_id:
                format_name = new_names[decision]
                if decision == "Amnesty for False Conversions":
                    format_name = format_name + ("unused")
                outfile.write('|-\n'
                              '| {} || {}\n'.format(format_name, decision_id)
                              )
    outfile.write("|}")
    print("Completed writing decisions to file.")
            

def print_traits():
    outfile = open("traits.txt", "w", encoding='utf8')
    outfile.write('')

    for trait in names.keys():
        if trait.startswith('trait'):
            if not trait.endswith('_desc'):
                # Remove trait_ from beginning
                traitid = trait[6:]
                
                traitname = names[trait]
                traitname = traitname.replace(' ', '_')
                traitname = traitname.replace('\'', '')
                traitname = traitname.replace('-', '_')
                traitname = traitname.lower()
                outfile.write(traitid + ": " + names[trait])
                # Mark disimilar trait names
                if traitname != traitid:
                    outfile.write('*')
                outfile.write('\n')

    print("Completed writing traits to file.")



if False:
    parse_titles()
    parse_dev()
    parse_special()
    #print_baronies()
    print_counties()
    print_dutchies()
    print_kingdoms()


    parse_names('traits_l_english')
    print_traits()

    parse_holy_orders()

if False:
    parse_titles()
    parse_dev()
    parse_special()
    parse_names('titles_l_english')
    print_empires()

 
parse_names('all')
print_decisions()

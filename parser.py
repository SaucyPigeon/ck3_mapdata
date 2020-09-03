import os, glob
import pyradox

titles = {} # nested dict empires:kingdoms:dutchies:counties:baronies:barony number
dev_867 = {}
dev_1066 = {}
special = {}
names = {}
colors = {}
capitals = {}

def parse_names():
    name_file = open(
        'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\localization\english\\titles_l_english.yml',
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
        # 'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\history\\titles\\00_other_titles.txt',
        'C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\common\landed_titles\\00_landed_titles.txt',
        game="Stellaris")

    for key_e in list(titles_tree.keys()):
        if key_e[:2] == "e_":
            titles[key_e] = {}
            colors[key_e] = list(titles_tree[key_e].find_all('color'))
            capitals[key_e] = titles_tree[key_e]["capital"]

            for key_k in list(titles_tree[key_e].keys()):
                if key_k[:2] == "k_":
                    titles[key_e][key_k] = {}
                    colors[key_k] = list(titles_tree[key_e][key_k].find_all('color'))
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

    # title_file = open('C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\common\landed_titles\\00_landed_titles.txt', "r", encoding='utf8')
    # titulars = True
    # empire = "none"
    # kingdom = "none"
    # dutchy = "none"
    # county = "none"
    # barony = "none"
    # for line in title_file:
    #     if(line[:8] == "########"):
    #         titulars = False
    #
    #     if(titulars):
    #         continue
    #
    #     if(line[:2] == 'e_'):
    #         # print(line)
    #         empire = line.split()[0]
    #         titles[empire] = {}
    #     elif(line[:3] == '\tk_'):
    #         # print(line)
    #         kingdom = line.split()[0]
    #         titles[empire][kingdom] = {}
    #     elif(line[:4] == '\t\td_'):
    #         # print(line)
    #         dutchy = line.split()[0]
    #         titles[empire][kingdom][dutchy] = {}
    #     elif(line[:5] == '\t\t\tc_'):
    #         # print(line)
    #         county = line.split()[0]
    #         titles[empire][kingdom][dutchy][county] = {}
    #     elif(line[:6] == '\t\t\t\tb_'):
    #         # print(line)
    #         barony = line.split()[0]
    #         titles[empire][kingdom][dutchy][county][barony] = 0
    #     elif(line[:13] == '\t\t\t\t\tprovince'):
    #         titles[empire][kingdom][dutchy][county][barony] = line.split()[2]


def print_dutchies():
    outfile = open("dutchies.txt", "w", encoding='utf8')
    outfile.write('{| class="wikitable sortable mw-collapsible" style="text-align: left;"\n'
                  '|+ De Jure Duchies\n'
                  '|-\n'
                  '! rowspan="2" | Duchy\n'
                  '! rowspan="2" | [[Kingdoms|Kingdom]]*\n'
                  '! rowspan="2" | [[Empires|Empire]]*\n'
                  '! rowspan="2" | [[Provinces|Counties]]*\n'
                  '! rowspan="2" | Baronies*\n'
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

                outfile.write('|-\n!style = "background-color:rgb({},{},{})" | {}\n | {} || {} || '
                              'align="right"| {} || align="right"| {} || align="right"| {} || '
                              'align="right"| {} || align="right"| {} || align="right"| {} || align="right"| '
                              '{} || {} || {}\n'.format(colors[dutchy][0], colors[dutchy][1], colors[dutchy][2],
                                                        names[dutchy], names[kingdom], names[empire], counties,
                                                        baronies, total_dev_867, highest_dev_867, total_dev_1066,
                                                        highest_dev_1066, special_buildings, dutchy, capitals[dutchy]))
    outfile.write("|}")


parse_titles()
# print(colors)
parse_dev()
parse_special()
parse_names()
print_dutchies()


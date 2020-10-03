import os
from PIL import Image
import time, sys
import datetime
import cv2
import numpy as np

def create_plain_colour_map(im, province_rgb, province_types):
    # Create colour map (plain)
    im_plain_colour = im.copy()

    print("Colouring provinces (this will take some time.)")

    total_pixels = im.width * im.height
    counter = 0
    start_time = datetime.datetime.now()

    for x in range(im.width):
        for y in range(im.height):
            pixel = im_plain_colour.getpixel((x, y))
            province_id = province_rgb[pixel]
            province_type = "land"
            if province_id in province_types:
                province_type = province_types[province_id]
            province_color = (-1, -1, -1)
            if province_type == "land":
                province_color = (127, 127, 127)
            elif province_type == "water":
                province_color = (51, 67, 85)
            elif province_type == "impassable":
                province_color = (36, 36, 36)
            else:
                print("Did not expect province type " + province_type + " for " + str(province_id))
                raise Exception()
            im_plain_colour.putpixel((x, y), province_color)

            counter = counter + 1
            elapsed_time = datetime.datetime.now() - start_time
            if elapsed_time.total_seconds() - int(elapsed_time.total_seconds()) == 0:
                update_progress(counter / total_pixels)
                print('')

    print("Finished colouring provinces.")
    print("Total time elapsed (seconds): " + str((datetime.datetime.now() - start_time).total_seconds()))

    im_plain_colour.save("province types.png")
    print("Successfully saved generated plain colour map to province types.png")

# shamelessly copied from https://stackoverflow.com/a/15860757
# update_progress() : Displays or updates a console progress bar
## Accepts a float between 0 and 1. Any int will be converted to a float.
## A value under 0 represents a 'halt'.
## A value at 1 or bigger represents 100%
def update_progress(progress):
    barLength = 10 # Modify this to change the length of the progress bar
    status = ""
    if isinstance(progress, int):
        progress = float(progress)
    if not isinstance(progress, float):
        progress = 0
        status = "error: progress var must be float\r\n"
    if progress < 0:
        progress = 0
        status = "Halt...\r\n"
    if progress >= 1:
        progress = 1
        status = "Done...\r\n"
    block = int(round(barLength*progress))
    text = "\rPercent: [{0}] {1}% {2}".format( "#"*block + "-"*(barLength-block), progress*100, status)
    sys.stdout.write(text)
    sys.stdout.flush()

map_folder = r"C:\Program Files (x86)\Steam\steamapps\common\Crusader Kings III\game\map_data\\"
im = Image.open(map_folder + "provinces.png")

# Water provinces
province_types = {}

file = open(map_folder + "default.map")
lines = file.readlines()
for line in lines:
    content = line
    content = content.split('#')[0]
    content = content.lstrip()
    content = content.rstrip()
    
    if len(content) == 0:
        continue
    key_value = content.split(' = ')
    if len(key_value) != 2:
        print("Failed to parse this line: " + line)
        raise Exception()
    key = key_value[0]
    value = key_value[1]

    if key == "definitions":
        continue
    if key == "provinces":
        continue
    if key == "rivers":
        continue
    if key == "topology":
        continue
    if key == "continent":
        continue
    if key == "adjacencies":
        continue
    if key == "island_region":
        continue
    if key == "geographical_region":
        continue
    if key == "seasons":
        continue

    province_type = ""

    if key == "sea_zones":
        province_type = "water"
    if key == "river_provinces":
        province_type = "water"
    if key == "lakes":
        province_type = "water"
    if key == "impassable_seas":
        province_type = "water"
    if key == "impassable_mountains":
        province_type = "impassable"
    if province_type == "":
        print("Failed to parse this line: " + line)
        raise Exception()

    province_ids = []
    if value.startswith("RANGE"):
        parse_value = value
        parse_value = parse_value[8:]
        parse_value = parse_value.rstrip(" }")
        province_id_strings = parse_value.split(' ')
        if len(province_id_strings) != 2:
            print("Failed to parse this line: " + line)
            print("Expected two values for range.")
            print("Instead, only got " + str(len(province_id_strings)))
            print(str(province_id_strings))
            raise Exception()
        range_start = int(province_id_strings[0])
        range_end = int(province_id_strings[1])
        if range_end <= range_start:
            print("Failed to parse this line: " + line)
            print("Range end is meant to be greater than range start.")
            print("Range start: " + str(range_start))
            print("Range end: " + str(range_end))
            raise Exception()
        for i in range(range_start, range_end + 1, 1):
            province_ids.append(i)
    elif value.startswith("LIST"):
        parse_value = value
        parse_value = parse_value[7:]
        parse_value = parse_value.rstrip(" }")
        province_id_strings = parse_value.split(' ')
        for province_id_string in province_id_strings:
            province_ids.append(int(province_id_string))
    else:
        print("Failed to parse this line: " + line)
        raise Exception()

    for province_id in province_ids:
        province_types[province_id] = province_type

print("Finished parsing default.map")
print("Found " + str(len(province_types.items())) + " water and impassable provinces")

# Province colours
file = open(map_folder + "definition.csv")
lines = file.readlines()

province_rgb = {}

for line in lines:
    content = line
    content = content.split('#')[0]
    content = content.lstrip()
    content = content.rstrip()

    if len(content) == 0:
        continue

    values = content.split(';')
    if len(values) < 4:
        print("Failed to parse line " + line)
        raise Exception()
    values = values[:4]
    province_id = int(values[0])
    r = int(values[1])
    g = int(values[2])
    b = int(values[3])

    province_rgb[(r, g, b)] = province_id


print("Finished parsing definition.csv")
print("Found " + str(len(province_rgb)) + " provinces total.")

#create_plain_colour_map(im, province_rgb, province_types)
# Create province outlines
print("Generating province outlines (this will take some time.)")

img = cv2.imread("provinces no water.png")
#imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
img_c = np.copy(img)
for province_color in province_rgb:
    province_id = province_rgb[province_color]
    if province_id == 0:
        continue
    if province_id in province_types:
        if province_types[province_id] == "water":
            continue
    r = province_color[0]
    g = province_color[1]
    b = province_color[2]
    # bgr
    np_array = np.array([b, g, r])
    # convert to hsv
    np_array = cv2.cvtColor(np_array, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, np_array, np_array)
    _, contours = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    print(contours)

    if contours:
        print(str(len(contours)))
    
    cv2.drawContours(img_c, contours, -1, (0, 255, 0), 1)
cv2.imwrite("contours.png", img_c)
    
    
#ret, thresh = cv2.threshold(imgray, 1, 255, cv2.THRESH_BINARY)
#contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#print("Number of contours = {}".format(str(len(contours))))
#print('contours {}'.format(contours[0]))
#cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
#cv2.drawContours(imgray, contours, -1, (0, 255, 0), 3)
#cv2.imshow('Image', img)
#cv2.imshow('Image GRAY', imgray)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


#total_pixels = im.width * im.height
#counter = 0
#start_time = datetime.datetime.now()



